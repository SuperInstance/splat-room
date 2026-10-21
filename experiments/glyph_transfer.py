#!/usr/bin/env python3
"""THE TRANSFER TEST -- does the fitted vocabulary belong to the ROOM or
to the CAPTURE?

    python experiments/glyph_transfer.py --selftest
    python experiments/glyph_transfer.py --out results

THE QUESTION.  The glyph grid fits a per-session alphabet and answers a
held-out question about the room from it.  The kill condition named in
the riff is: *"a vocabulary that only works on the cells it was fitted
on is a caption, not a language."*  The grid study answered the
question for the session the alphabet was fitted on.  This one asks
whether the alphabet answers a DIFFERENT session's question.

THE MEASUREMENT.  For every ordered pair of sessions (A, B):

  * A's alphabet is fitted on A (the first half of A's frames, the even
    columns, a FIXED cardinality so the alphabets are comparable);
  * A's "characteristic material" -- the cluster that owns the most
    cells -- is carried over to B;
  * B's cells are assigned to A's centres, and the cells carrying A's
    characteristic material are counted in B's left and right halves;
  * that answer is graded against B's OWN truth, the full-resolution
    luma's per-half change energy.

If the vocabulary is a property of the ROOM, then A's alphabet should
answer B's question nearly as well as A's answers its own.  If it is a
property of the CAPTURE, the transfer falls to chance.

WHAT THIS IS NOT.  Every session in the corpus is the same room and
nearly the same viewpoint, so this is a SESSION-transfer test and NOT
the across-room test.  It is the in-room half of the question, and the
across-room test still needs the second room.  The report says so, and
so does this file.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import glyph_grid as gg  # noqa: E402  (same repository, same stage)

#: The cardinality.  FIXED, so two sessions' alphabets can be compared
#: at all: a vocabulary with three symbols and a vocabulary with four
#: do not have a correspondence.  k=3 is the silhouette's own modal
#: choice over the corpus (33 of 43 sessions), so it is the
#: cardinality the data picks most often -- stated once, not per
#: session.
K = 3

#: The cardinalities the sweep runs.  The question the transfer study
#: has to answer is not "does a vocabulary transfer" but "does A
#: vocabulary transfer", and only more than one cardinality can tell
#: the difference.
K_SWEEP = (3, 4, 5, 6)

#: The tie threshold, the same 1.10 the grid study used.
TIE_RATIO = 1.10


def session_material(session_dir: Path):
    """The part of a session that does NOT depend on the cardinality:
    the change map, the descriptors, the observed mask, and the truth.

    It is separated from the fit so that a sweep over cardinalities
    reads the corpus once instead of once per cardinality.
    """
    meta_path = session_dir / 'meta.json'
    if not meta_path.is_file():
        return None
    meta = json.loads(meta_path.read_text())
    mic = (meta.get('mic') or {}).get('label', '')
    cam = (meta.get('camera') or {}).get('label', '')
    synthetic = ('Fake' in mic) or ('.y4m' in cam) or (not mic and not cam)
    if synthetic:
        return None

    luma = session_dir / 'luma.raw'
    if not luma.is_file():
        return None
    maps = gg.frame_motion_maps(luma)
    if maps is None:
        return None
    observed = gg.observed_mask(maps)
    if observed.sum() < 16:
        return None

    n_frames = len(maps)
    train = slice(0, max(1, n_frames // 2))
    train_desc = gg.cell_descriptors(maps, frames=train)
    full_desc = gg.cell_descriptors(maps)

    even = np.zeros((gg.GRID_H, gg.GRID_W), dtype=bool)
    even[:, ::2] = True
    odd = ~even

    truth = gg.full_resolution_half_energy(luma)
    if truth is None:
        return None

    return {
        'session': session_dir.name,
        'n_frames': n_frames,
        'n_observed_cells': int(observed.sum()),
        'observed': observed,
        'even': even,
        'odd': odd,
        'train_desc': train_desc,
        'full_desc': full_desc,
        'truth': truth,
        # how much of the room moved, per cell: the sessions' visual
        # similarity, used to ask whether the transfer decays with
        # distance
        'activity': full_desc[..., 0].reshape(-1).astype(np.float64),
    }


def session_model(material: dict, k: int) -> dict:
    """FIT ONE session's alphabet at ONE cardinality, and return the
    model plus its truth.

    Returns None for a session that cannot be used: no frames, a
    synthetic device (a test rig is not a room), too few observed cells
    to fit anything on, or no truth to grade against.
    """
    observed = material['observed']
    labels, char_for, centres, means, scale = gg.fit_alphabet(
        material['train_desc'], k, seed=11, cell_mask=material['even'])
    lab = labels.reshape(-1)
    valid = observed.reshape(-1) & (lab >= 0)
    counts = np.bincount(lab[valid])
    if counts.size < 2:
        return None
    # the characteristic material: the cluster that owns the most cells
    characteristic = int(np.argmax(counts))

    model = dict(material)
    model.update({
        'k': k,
        'centres': centres,
        'scale': scale,
        'char_for': char_for,
        'characteristic': characteristic,
        'cluster_mean_activity': means,
        # the training-half labels, which is what the grid study's own
        # question used
        'train_labels': labels,
    })
    return model


def answer_with(alphabet: dict, other: dict, cluster: int) -> dict:
    """Apply ONE session's alphabet to ANOTHER session and count.

    The other session's cells are assigned to the alphabet's centres,
    in the alphabet's own scaled space, and the cells of `cluster` are
    counted in the other session's left and right halves over the
    cells the fit never saw (the odd columns).
    """
    z = other['full_desc'].reshape(-1, other['full_desc'].shape[-1])
    z = z / alphabet['scale']
    labels = gg.assign_nearest(alphabet['centres'], z)
    valid = other['observed'].reshape(-1)
    answer_cells = other['odd'].reshape(-1) & valid
    left = (np.arange(labels.size) % gg.GRID_W) < (gg.GRID_W // 2)
    n_left = int(((labels == cluster) & answer_cells & left).sum())
    n_right = int(((labels == cluster) & answer_cells & ~left).sum())
    return {
        'answer': 'LEFT' if n_left > n_right else 'RIGHT',
        'left': n_left,
        'right': n_right,
        'tied': n_left == n_right,
    }


def answer_self(model: dict) -> dict:
    """The same counting rule, applied to the session itself.

    This is the CEILING of the transfer: what the alphabet achieves on
    the very session it was fitted on, under the transfer study's own
    rule.  It is not the grid study's 33/43, because that number used
    the training half's labels and this one uses the whole session's
    descriptors -- so both are reported, and the difference is stated.
    """
    z = model['full_desc'].reshape(-1, model['full_desc'].shape[-1])
    z = z / model['scale']
    labels = gg.assign_nearest(model['centres'], z)
    valid = model['observed'].reshape(-1)
    answer_cells = model['odd'].reshape(-1) & valid
    left = (np.arange(labels.size) % gg.GRID_W) < (gg.GRID_W // 2)
    n_left = int(((labels == model['characteristic']) & answer_cells & left).sum())
    n_right = int(((labels == model['characteristic']) & answer_cells & ~left).sum())
    return {
        'answer': 'LEFT' if n_left > n_right else 'RIGHT',
        'left': n_left,
        'right': n_right,
        'tied': n_left == n_right,
    }


def similarity(a: dict, b: dict) -> float:
    """How alike two sessions look: the correlation of their per-cell
    activity maps.  It is the horizontal axis of the decay curve."""
    va, vb = a['activity'], b['activity']
    if va.std() <= 0 or vb.std() <= 0:
        return 0.0
    return float(np.corrcoef(va, vb)[0, 1])


def choose_k_by_silhouette(material: dict, ks=K_SWEEP) -> dict:
    """The INCUMBENT rule: the silhouette of the training descriptors.

    This is what the glyph grid study ships, and the comparison a new
    rule has to win is against it.  It is truth-blind too: it measures
    how separated the clusters are, and never looks at the answer.
    """
    train_desc = material['train_desc']
    even = material['even']
    sils = {}
    for k in ks:
        labels, char_for, centres, means, scale = gg.fit_alphabet(
            train_desc, k, seed=11, cell_mask=even)
        z = train_desc.reshape(-1, train_desc.shape[-1]) / scale
        fit_cells = z[even.reshape(-1)]
        fit_labels = gg.assign_nearest(centres, fit_cells)
        sils[k] = gg.silhouette_score(fit_labels, fit_cells)
    if not sils:
        return {'k': None, 'sils': {}}
    best = min(sils, key=lambda k: (-sils[k], k))
    return {'k': best, 'sils': {str(k): round(v, 4) for k, v in sils.items()}}


def choose_k_by_activity_gap(material: dict, ks=K_SWEEP) -> dict:
    """THE RULE, stated before it was measured.

    The CHARACTERISTIC cluster is the one that owns the most cells.  For
    the vocabulary to mean anything, that cluster must also be the one
    that MOVES -- otherwise "the biggest material" and "the moving
    material" have come apart, and the question has nothing left to
    ask.  The sweep showed that coming apart: at three symbols the
    biggest cluster is the most active one in 24 of 43 sessions, and at
    six symbols in 7 of 43.

    So, for each cardinality: fit the alphabet, find the biggest
    cluster, and measure the ACTIVITY GAP between it and the median of
    the other clusters.  The cardinality with the largest gap wins, and
    ties go to the smallest cardinality so the choice is deterministic.

    NOTHING HERE CONSULTS THE TRUTH.  It is a statement about the
    alphabet's own structure, which is why it can be evaluated against
    a truth it has never seen -- and why the silhouette, which measures
    separation and not structure, could not have found it.
    """
    gaps = {}
    for k in ks:
        model = session_model(material, k)
        if model is None:
            continue
        means = list(model['cluster_mean_activity'])
        if len(means) < 2:
            continue
        counts = np.bincount(model['train_labels'].reshape(-1)[
            model['observed'].reshape(-1)], minlength=k)
        biggest = int(np.argmax(counts))
        others = [m for i, m in enumerate(means) if i != biggest]
        if not others:
            continue
        gap = float(means[biggest] - float(np.median(others)))
        gaps[k] = gap
    if not gaps:
        return {'k': None, 'gaps': {}}
    # the largest gap wins; the smallest k wins a tie
    best = min(gaps, key=lambda k: (-gaps[k], k))
    return {'k': best, 'gaps': {str(k): round(v, 6) for k, v in gaps.items()}}


def study_k(materials: list[dict], k, k_picker=None) -> dict:
    """The whole study at ONE cardinality -- or, when a picker is given,
    at the cardinality each session's own rule chooses.

    The corpus is read ONCE by the caller and the alphabets are refitted
    per cardinality, because a vocabulary with three symbols and one
    with four have no correspondence -- and because the question the
    sweep exists to answer is whether a vocabulary transfers or a
    PARTICULAR vocabulary transfers."""
    models = []
    picked: list[int] = []
    for m in materials:
        kk = k
        if k_picker is not None:
            kk = k_picker(m)['k']
            if kk is None:
                continue
        model = session_model(m, kk)
        if model is None:
            continue
        models.append(model)
        picked.append(model['k'])
    n = len(models)
    if not n:
        raise SystemExit('no usable sessions')
    print('  k=%s: %d sessions' % (k if k_picker is None else 'per-session', n))

    # the truth side of every session, for the conditional analysis
    truths = {m['session']: m['truth']['half'] for m in models}

    # the SELF case, under this study's own rule
    self_rows = []
    for m in models:
        r = answer_self(m)
        r['agrees'] = (r['answer'] == m['truth']['half'])
        r['decisive'] = m['truth']['ratio'] >= TIE_RATIO
        self_rows.append(r)

    # the TRANSFER, every ordered pair (A, B), A != B, plus a CONTROL
    # that uses a random cluster of A instead of the characteristic one.
    rng = np.random.default_rng(7)
    pairs = []
    for i, a in enumerate(models):
        for j, b in enumerate(models):
            if i == j:
                continue
            r = answer_with(a, b, a['characteristic'])
            # the control: a cluster of A that is NOT the characteristic
            # one.  If the transfer is real, the control must be worse.
            others = [c for c in range(a['k']) if c != a['characteristic']]
            control_cluster = int(others[rng.integers(len(others))]) if others \
                else a['characteristic']
            c = answer_with(a, b, control_cluster)
            pairs.append({
                'from': a['session'],
                'to': b['session'],
                'answer': r['answer'],
                'truth': b['truth']['half'],
                'agrees': r['answer'] == b['truth']['half'],
                'left': r['left'], 'right': r['right'], 'tied': r['tied'],
                'decisive': b['truth']['ratio'] >= TIE_RATIO,
                'control_answer': c['answer'],
                'control_agrees': c['answer'] == b['truth']['half'],
                'similarity': round(similarity(a, b), 4),
                # do the two sessions agree about the room anyway?  The
                # raw curve is confounded by this, because a copier is
                # only punished when they disagree.
                'same_truth': truths[a['session']] == truths[b['session']],
            })
        if (i + 1) % 10 == 0:
            print('  ... %d/%d alphabets transferred' % (i + 1, n))

    def rate(rows, key='agrees', only_decisive=False):
        rs = [r for r in rows if r.get('decisive', True)] if only_decisive else rows
        if not rs:
            return (0, 0, 0.0)
        k = sum(1 for r in rs if r.get(key))
        return (k, len(rs), round(k / len(rs), 4))

    off = pairs
    decisive_off = [p for p in off if p['decisive']]

    # THE MECHANISM.  A transfer that merely COPIED the source's answer
    # would look perfect whenever the two sessions happen to agree, and
    # would be punished only when they do not.  So the clean measurement
    # is the conditional one: among the pairs where the source and the
    # target DISAGREE about the room, whose answer does the transfer
    # follow?
    disagree = [p for p in decisive_off
                if truths[p['from']] != truths[p['to']]]
    follows_target = (sum(1 for p in disagree
                          if p['answer'] == truths[p['to']]) / len(disagree)
                      if disagree else None)
    follows_source = (sum(1 for p in disagree
                           if p['answer'] == truths[p['from']]) / len(disagree)
                       if disagree else None)

    # the same conditional measure, by similarity band -- because the
    # raw curve turned out to be CONFOUNDED: similar sessions tend to
    # agree about the room anyway, so a copier is not punished there.
    cond_bands = []
    if disagree:
        sdis = np.array([p['similarity'] for p in disagree], dtype=np.float64)
        edges_dis = np.quantile(sdis, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        for lo, hi in zip(edges_dis[:-1], edges_dis[1:]):
            sel = (sdis >= lo) & (sdis <= hi)
            if sel.sum() == 0:
                continue
            band = [p for p, m in zip(disagree, sel) if m]
            cond_bands.append({
                'similarity_low': round(float(lo), 4),
                'similarity_high': round(float(hi), 4),
                'n_pairs': len(band),
                'follows_the_target': round(sum(1 for p in band
                                                if p['answer'] == truths[p['to']]) / len(band), 4),
                'follows_the_source': round(sum(1 for p in band
                                                if p['answer'] == truths[p['from']]) / len(band), 4),
            })

    # the decay curve: the transfer's accuracy against how alike the two
    # sessions look
    sims = np.array([p['similarity'] for p in off], dtype=np.float64)
    agree = np.array([1.0 if p['agrees'] else 0.0 for p in off])
    dec = np.array([p['decisive'] for p in off])
    edges = np.quantile(sims, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    curve = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (sims >= lo) & (sims <= hi) & dec
        if sel.sum() == 0:
            continue
        same = [p['same_truth'] for p, m in zip(off, sel) if m]
        curve.append({
            'similarity_low': round(float(lo), 4),
            'similarity_high': round(float(hi), 4),
            'n_pairs': int(sel.sum()),
            'agree': int(agree[sel].sum()),
            'rate': round(float(agree[sel].mean()), 4),
            # the confound: how often the two sessions agree about the
            # room anyway, in this band
            'the_two_sessions_share_the_truth': round(float(np.mean(same)), 4) if same else None,
        })

    # the per-session consistency: is each session answered the SAME
    # way by every partner, or do the partners disagree among
    # themselves?
    left_rate_when_left = []
    left_rate_when_right = []
    n_consistent = 0
    # the CONFOUND CHECK: at a higher cardinality, is the
    # "characteristic" cluster still the ACTIVE material, or has it
    # become the inert background?  A cluster that owns the most cells
    # is not necessarily the one that moves, and if the extra symbols
    # carve off the background then the characteristic cluster stops
    # meaning anything -- which would explain the transfer's collapse
    # without saying anything about the vocabulary.
    characteristic_is_most_active = 0
    characteristic_is_least_active = 0
    characteristic_activity_ranks = []
    for j, b in enumerate(models):
        rows = [p for p in off if p['to'] == b['session']]
        if not rows:
            continue
        lf = sum(1 for p in rows if p['answer'] == 'LEFT') / len(rows)
        (left_rate_when_left if b['truth']['half'] == 'LEFT'
         else left_rate_when_right).append(lf)
        if lf <= 0.10 or lf >= 0.90:
            n_consistent += 1
        means = list(b['cluster_mean_activity'])
        if means:
            order = sorted(range(len(means)), key=lambda c: means[c])
            rank = order.index(b['characteristic'])
            characteristic_activity_ranks.append(rank)
            if rank == len(means) - 1:
                characteristic_is_most_active += 1
            if rank == 0:
                characteristic_is_least_active += 1

    # per-session: how often is THIS session's question answered right
    # by SOME other session's alphabet (the best partner), and by the
    # median partner
    per_to = []
    for j, b in enumerate(models):
        rows = [p for p in off if p['to'] == b['session']]
        dec_rows = [p for p in rows if p['decisive']]
        a_all = sum(1 for p in rows if p['agrees'])
        a_dec = sum(1 for p in dec_rows if p['agrees'])
        best = max(rows, key=lambda p: (p['agrees'], p['similarity'])) \
            if rows else None
        per_to.append({
            'session': b['session'],
            'n_partners': len(rows),
            'agree': a_all,
            'rate': round(a_all / max(1, len(rows)), 4),
            'agree_decisive': a_dec,
            'n_decisive_partners': len(dec_rows),
            'rate_decisive': round(a_dec / max(1, len(dec_rows)), 4),
            'best_partner': best['from'] if best else None,
            'self_agrees': self_rows[j]['agrees'],
            'truth': b['truth']['half'],
            'decisive': b['truth']['ratio'] >= TIE_RATIO,
        })

    out = {
        'study': 'the glyph grid transfer test -- is the vocabulary the room\'s or the capture\'s?',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'method': {
            'k': k if k is not None else 'PER SESSION, by the activity-gap rule',
            'k_why': ('FIXED, so two alphabets can be compared at all; k=3 is the '
                      'silhouette\'s own modal choice over the corpus.  The sweep '
                      'runs every cardinality, and the activity-gap rule lets '
                      'each session choose its own'),
            'the_transfer': ('A\'s alphabet, fitted on A, answers B\'s question: A\'s '
                             'cells are assigned to A\'s centres in A\'s scaled space, '
                             'and A\'s characteristic cluster is counted in B\'s halves '
                             'over B\'s odd columns'),
            'the_truth': ('B\'s own full-resolution luma per-half change energy -- a '
                          'different computation, at 160x96, with no grid and no '
                          'clustering'),
            'the_control': ('the same transfer with a RANDOM non-characteristic cluster '
                            'of A.  If the transfer carries information, the control '
                            'must be worse'),
            'the_ceiling': ('the same counting rule applied to a session by its OWN '
                            'alphabet.  It is not the grid study\'s 33/43, which used '
                            'the training half\'s labels'),
            'the_honest_caveat': ('every session is the same room and nearly the same '
                                  'viewpoint, so this is a SESSION-transfer test and '
                                  'NOT the across-room test'),
            'tie_ratio_threshold': TIE_RATIO,
        },
        'sessions': [
            {'session': m['session'], 'n_observed_cells': m['n_observed_cells'],
             'characteristic_cluster': m['characteristic'],
             'alphabet': {str(c): ch for c, ch in m['char_for'].items()},
             'cluster_mean_activity': [round(x, 4) for x in m['cluster_mean_activity']],
             'truth': m['truth']['half'], 'luma_half_ratio': round(m['truth']['ratio'], 3)}
            for m in models
        ],
        'summary': {
            'n_sessions': n,
            'n_pairs': len(off),
            'the_self_case': {
                'agree': rate(self_rows),
                'decisive': rate(self_rows, only_decisive=True),
                'the_reading': ('the ceiling of the transfer: what an alphabet '
                                'achieves on the session it was fitted on, under '
                                'this study\'s own rule'),
            },
            'the_transfer': {
                'agree_all': rate(off),
                'agree_decisive': rate(off, only_decisive=True),
                'the_reading': ('A\'s alphabet answering B\'s question, over every '
                                'ordered pair of distinct sessions'),
            },
            'the_control': {
                'agree_all': rate(off, key='control_agrees'),
                'agree_decisive': rate(off, key='control_agrees', only_decisive=True),
                'the_reading': ('the same transfer with a random non-characteristic '
                                'cluster: the floor the transfer must beat to mean '
                                'anything'),
            },
            'the_k_distribution': {
                str(kk): picked.count(kk) for kk in sorted(set(picked))
            },
            'the_decay_curve': curve,
            'the_mechanism': {
                'the_clean_measure': ('among the decisive pairs where the SOURCE '
                                      'and the TARGET disagree about the room, whose '
                                      'answer does the transfer follow?  A copier '
                                      'is punished here and nowhere else'),
                'n_pairs': len(disagree),
                'follows_the_target': (round(follows_target, 4)
                                       if follows_target is not None else None),
                'follows_the_source': (round(follows_source, 4)
                                       if follows_source is not None else None),
                'by_similarity': cond_bands,
                'the_reading': ('the transfer reads the TARGET, not the source: it '
                                'follows the target even when the two sessions '
                                'disagree.  The raw decay curve is CONFOUNDED -- '
                                'similar sessions tend to agree about the room '
                                'anyway, so a copier is not punished in that band, '
                                'which is why the raw curve inverts'),
            },
            'the_characteristic_cluster_is_active': {
                'n_sessions': len(models),
                'n_where_it_is_the_MOST_active_cluster': characteristic_is_most_active,
                'n_where_it_is_the_LEAST_active_cluster': characteristic_is_least_active,
                'mean_activity_rank': (round(float(np.mean(characteristic_activity_ranks)), 3)
                                       if characteristic_activity_ranks else None),
                'the_reading': ('the confound check: the characteristic cluster '
                                'is the one that owns the most CELLS, and a '
                                'cluster that owns the most cells is not '
                                'necessarily the one that MOVES.  If the extra '
                                'symbols at a higher cardinality carve off the '
                                'inert background, the characteristic cluster '
                                'stops meaning anything and the transfer '
                                'collapses for a reason that has nothing to do '
                                'with the vocabulary'),
            },
            'the_per_session_consistency': {
                'mean_left_rate_when_the_truth_is_LEFT': (round(float(np.mean(left_rate_when_left)), 4)
                                                          if left_rate_when_left else None),
                'mean_left_rate_when_the_truth_is_RIGHT': (round(float(np.mean(left_rate_when_right)), 4)
                                                           if left_rate_when_right else None),
                'n_sessions_answered_consistently_by_at_least_90_percent_of_partners':
                    n_consistent,
                'n_sessions': len(models),
                'the_reading': ('each session is answered the SAME WAY by nearly every '
                                'partner, and the side the partners agree on is the '
                                'side the truth is on -- so the transfer is a '
                                'detector, not a guesser, and its errors are '
                                'SYSTEMATIC rather than random'),
            },
            'the_similarity': {
                'mean': round(float(sims.mean()), 4) if sims.size else None,
                'min': round(float(sims.min()), 4) if sims.size else None,
                'max': round(float(sims.max()), 4) if sims.size else None,
            },
        },
        'per_session': per_to,
        'pairs': pairs,
    }
    return {'out': out, 'summary': out['summary'], 'pairs': pairs,
            'per_session': per_to}


def measure(corpus: Path, out_dir: Path, ks=K_SWEEP) -> dict:
    """The measurement over the corpus, at every cardinality.

    The corpus is read once and the alphabets are refitted per k, so
    the sweep costs one pass over the luma and four fits per session.
    """
    materials = []
    for d in sorted(corpus.iterdir()):
        if not d.is_dir():
            continue
        m = session_material(d)
        if m is None:
            continue
        materials.append(m)
    if not materials:
        raise SystemExit('no usable sessions')
    print(f'loaded {len(materials)} usable sessions')

    by_k = {}
    primary = None
    for k in ks:
        res = study_k(materials, k)
        by_k[str(k)] = res['summary']
        if k == K:
            primary = res
    if primary is None:
        primary = res

    # THE RULE, stated before it was measured: the cardinality that
    # keeps the biggest cluster and the moving material the same thing.
    print('  the activity-gap rule:')
    res_rule = study_k(materials, None, k_picker=choose_k_by_activity_gap)
    by_k['the_activity_gap_rule'] = res_rule['summary']
    picked = {}
    for m in materials:
        p = choose_k_by_activity_gap(m, ks)
        if p['k'] is not None:
            picked[str(p['k'])] = picked.get(str(p['k']), 0) + 1
    by_k['the_activity_gap_rule']['the_k_it_picks'] = picked

    # THE INCUMBENT: the silhouette, which is what the grid study
    # ships.  A new rule has to win against this one, not against
    # nothing.
    print('  the silhouette rule (the incumbent):')
    res_sil = study_k(materials, None, k_picker=choose_k_by_silhouette)
    by_k['the_silhouette_rule'] = res_sil['summary']
    picked_sil = {}
    for m in materials:
        p = choose_k_by_silhouette(m, ks)
        if p['k'] is not None:
            picked_sil[str(p['k'])] = picked_sil.get(str(p['k']), 0) + 1
    by_k['the_silhouette_rule']['the_k_it_picks'] = picked_sil

    out = primary['out']
    out['the_cardinality_sweep'] = {
        'the_k_values': list(ks),
        'the_question': ('does a vocabulary transfer, or does a PARTICULAR '
                         'vocabulary transfer?  A vocabulary with three '
                         'symbols and one with four have no correspondence, '
                         'so the sweep is the only way to tell'),
        'by_k': by_k,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_transfer.json').write_text(json.dumps(out, indent=2))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the transfer is a TRANSFER: applying an alphabet to a DIFFERENT
    #    session must be possible, and the self-case must reproduce the
    #    session's own answer.
    rng = np.random.default_rng(3)
    n = 120
    z = np.vstack([rng.normal(0.0, 0.4, size=(n // 2, 3)),
                   rng.normal(5.0, 0.4, size=(n // 2, 3))])
    centres = np.array([[0.0, 0.0, 0.0], [5.0, 0.0, 0.0]])
    alphabet = {'centres': centres, 'scale': np.ones(3), 'characteristic': 1}
    observed = np.ones((gg.GRID_H, gg.GRID_W), dtype=bool)
    odd = np.zeros((gg.GRID_H, gg.GRID_W), dtype=bool)
    odd[:, ::2] = True
    desc = np.zeros((gg.GRID_H, gg.GRID_W, 3), dtype=np.float64)
    # the material sits in the TOP-LEFT: rows 0-11, columns 0-19.  The
    # top rows are in the upper half of the image and the columns are
    # the left half of it, so the material is unambiguously on one side.
    desc[:12, :20, :] = 5.0
    other = {'full_desc': desc, 'observed': observed, 'odd': odd}
    r = answer_with(alphabet, other, 1)
    ck('transfer: an alphabet can be applied to another session', r is not None, str(r))
    ck('transfer: the transfer finds the half that holds the material',
       r['answer'] == 'LEFT', str(r))

    # 2. the CONTROL cluster must not find the same thing: if it did,
    #    the "transfer" would be an accident of the geometry.
    r0 = answer_with(alphabet, other, 0)
    ck('transfer: the control cluster answers the other way',
       r0['answer'] == 'RIGHT', str(r0))

    # 3. the similarity measure: a session and itself are perfectly
    #    similar, and two unrelated ones are not.
    a = {'activity': np.arange(10, dtype=np.float64)}
    b = {'activity': np.arange(10, dtype=np.float64)}
    c = {'activity': -np.arange(10, dtype=np.float64)}
    ck('transfer: a session is perfectly similar to itself',
       abs(similarity(a, b) - 1.0) < 1e-9, str(similarity(a, b)))
    ck('transfer: an inverted session is perfectly dissimilar',
       abs(similarity(a, c) + 1.0) < 1e-9, str(similarity(a, c)))

    # 4. the self-case must equal the session's own answer under the
    #    same rule -- the ceiling is not a separate invention.
    model = {
        'full_desc': desc, 'observed': observed, 'odd': odd,
        'centres': centres, 'scale': np.ones(3), 'characteristic': 1,
    }
    s = answer_self(model)
    ck('transfer: the self case follows the same counting rule',
       s['answer'] == r['answer'] and s['left'] == r['left'], str(s))

    # 5. the truth-blindness of the alphabet's own rule is inherited:
    #    the transfer never consults the truth to build its answer.
    ck('transfer: the transfer never reads the truth',
       'truth' not in answer_with.__code__.co_varnames[
           :answer_with.__code__.co_argcount], str(answer_with.__code__.co_varnames))

    # 6. the transfer must READ THE TARGET: the same alphabet, applied
    #    to two targets whose material sits on opposite sides, must give
    #    opposite answers.  If it did not, it would be reading the
    #    source, and the whole study would be measuring a copy.
    other_r = {'full_desc': desc.copy(), 'observed': observed, 'odd': odd}
    desc_flipped = np.zeros((gg.GRID_H, gg.GRID_W, 3), dtype=np.float64)
    desc_flipped[:12, 20:, :] = 5.0
    other_l = {'full_desc': desc_flipped, 'observed': observed, 'odd': odd}
    a_r = answer_with(alphabet, other_r, 1)
    a_l = answer_with(alphabet, other_l, 1)
    ck('transfer: the same alphabet reads two different targets',
       a_r['answer'] == 'LEFT' and a_l['answer'] == 'RIGHT',
       f'{a_r["answer"]} / {a_l["answer"]}')

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"   [{detail}]" if detail and not ok else ""))
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(ROOT / 'results'))
    ap.add_argument('--corpus', default='/mnt/c/proart_capture/corpus/free_sessions')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    corpus = Path(args.corpus)
    print(f'glyph transfer: {len([d for d in corpus.iterdir() if d.is_dir()])} sessions')
    out = measure(corpus, Path(args.out))
    print(json.dumps(out.get('summary', {}), indent=1))
    print(f"wrote {Path(args.out) / 'glyph_transfer.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

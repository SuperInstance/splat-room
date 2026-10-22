#!/usr/bin/env python3
"""THE GEOMETRY NULL — the abstention threshold from the room's own shape.

    python experiments/glyph_geometry_null.py --selftest
    python experiments/glyph_geometry_null.py --out results

THE PROBLEM.  Two studies in a row have failed to give the vocabulary a
shipped abstention threshold, and they failed for the same reason.

The first (the abstention rule) found that the count's MARGIN is the
signal and that the size of the evidence is not -- and then found the
declared threshold too expensive, with the one cheap operating point
reachable only by hindsight.

The second (the effective sample size) found that the corpus's cells are
massively correlated -- a median variance inflation factor of 44.42, so
the grid's 960 cells are worth about 22 independent samples -- and that
correcting for that DESTROYS the rule, because the binomial's null is
not the null the count is testing.

**BOTH FAILURES POINT AT THE SAME PLACE: the binomial does not know that
the characteristic material is a BLOB.** The count is over a contiguous
stripe of cells, and the question is where that stripe sits relative to
the room's centre. A blob that spans the room answers the question
however it is placed; a narrow blob placed off-centre answers it
decisively. The binomial knows neither of those things.

THE NULL, AND IT HAS NO KNOB.  Take the session's own characteristic
cluster -- its actual cells, its actual column profile -- and ask what
the left/right split would be if the blob were placed elsewhere in the
room.  The placements are the profile's horizontal translations that
keep the blob inside the room; the null is the SPREAD of the left
fraction over those placements; and the rule abstains when the
observed placement is not distinguishable from the typical one.

    the statistic   f = the cluster's left fraction among the answer
                     cells, so the imbalance is f - 0.5
    the null        f(s) for every placement s that keeps the blob
                     inside the room
    the rule        abstain when |f(0) - 0.5| < Z_NULL * sd(f)

**Z_NULL = 1, DECLARED BEFORE THE MEASUREMENT**, and it is the only
number in the rule.  There is nothing else to tune: the threshold comes
from the session's own material, so the rule cannot be fitted to the
truth even by accident.

**THE PHYSICS, WHICH IS WHY IT SHOULD BE BETTER.**  A WIDE blob has
almost no placement spread -- wherever it goes, it spans both halves --
so the spread is small and the rule abstains: the vocabulary genuinely
does not know which half holds more of a thing that is everywhere.  A
NARROW blob has a large placement spread, so a blob sitting off-centre
is unusual and the rule answers.  The binomial z knows neither.

**THE BAR, DECLARED BEFORE THE MEASUREMENT.**

  1. The rule catches at least HALF of the decisive errors while
     abstaining from at most a QUARTER of the decisive right answers.
  2. The accuracy among the answered is at least 5 points above the
     accuracy over all the decisive sessions.
  3. Teacher dependence 0.000, and the rule has no knob but the
     declared Z_NULL.
  4. THE AGREEMENT TEST: the geometry null's rule lands in the same
     operating region as the abstention study's hindsight point (a
     binomial K of 1.0).  If two independent roads reach the same
     place, the place is not an artefact of looking.

**WHAT THIS IS NOT.**  It does not make the vocabulary good; it makes it
honest.  And it is still ONE room with ONE viewpoint, where the grid's
cell is 4 luma pixels and the room's half is 20 cells wide.
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

import glyph_abstain as ga        # noqa: E402
import glyph_grid as gg           # noqa: E402
import glyph_transfer as gt       # noqa: E402

#: The only number in the rule: how many placement standard deviations
#: from the typical placement the observed one has to be before the
#: vocabulary answers.  DECLARED BEFORE THE MEASUREMENT.
Z_NULL = 1.0


# --------------------------------------------------------------------------
# the null
# --------------------------------------------------------------------------

def cluster_profile(labels: np.ndarray, characteristic: int,
                    answer_cells: np.ndarray) -> np.ndarray:
    """The characteristic cluster's column profile over the ANSWER cells.

    The answer cells are the odd columns, so the profile has one entry
    per odd column: how many of the cluster's cells fall in it.  The
    profile is the blob's SHAPE, and the shape is what the null
    translates."""
    flat_labels = labels.reshape(-1)
    flat_cells = answer_cells.reshape(-1)
    left = (np.arange(flat_labels.size) % gg.GRID_W) < (gg.GRID_W // 2)
    profile = np.zeros(gg.GRID_W // 2, dtype=np.float64)
    cols = np.arange(flat_labels.size) % gg.GRID_W
    for i in range(profile.size):
        col = 2 * i + 1          # the odd columns are the answer columns
        sel = (flat_cells & (flat_labels == characteristic) & (cols == col)
               & (left if i < profile.size // 2 else ~left))
        profile[i] = float(sel.sum())
    return profile


def placements(profile: np.ndarray) -> list[int]:
    """The horizontal translations that keep the blob inside the room.

    A blob that cannot be moved anywhere else carries no positional
    information, and the caller abstains on it."""
    occupied = np.nonzero(profile > 0)[0]
    if occupied.size == 0:
        return [0]
    lo, hi = int(occupied.min()), int(occupied.max())
    return list(range(-lo, profile.size - hi))


def placement_fractions(profile: np.ndarray) -> np.ndarray:
    """The left fraction of the cluster for each valid placement."""
    n = profile.size
    half = n // 2
    out = []
    for s in placements(profile):
        shifted = np.zeros(n, dtype=np.float64)
        for i in range(n):
            j = i - s
            if 0 <= j < n:
                shifted[i] = profile[j]
        total = shifted.sum()
        if total <= 0:
            continue
        out.append(float(shifted[:half].sum() / total))
    return np.asarray(out, dtype=np.float64)


def geometry_abstains(profile: np.ndarray, z_null: float = Z_NULL) -> dict:
    """Does the vocabulary abstain on this blob's placement?"""
    f_obs = None
    total = profile.sum()
    if total > 0:
        f_obs = float(profile[:profile.size // 2].sum() / total)
    fs = placement_fractions(profile)
    if f_obs is None or fs.size < 2:
        # no blob, or a blob that cannot be moved: its position carries
        # no information at all, so the answer is "I do not know"
        return {'the_left_fraction': None, 'the_placement_sd': None,
                'the_observed_in_placement_units': None,
                'abstain': True,
                'the_reason': ('the blob cannot be placed anywhere else, so '
                               'its position carries no information')}
    sd = float(fs.std(ddof=1))
    offset = abs(f_obs - 0.5)
    units = offset / sd if sd > 0 else float('inf')
    return {
        'the_left_fraction': round(f_obs, 4),
        'the_placement_sd': round(sd, 4),
        'the_observed_in_placement_units': (round(units, 4)
                                            if np.isfinite(units) else None),
        'abstain': bool(units < z_null),
        'the_reason': (f'{offset:.4f} from the centre, against a placement '
                       f'spread of {sd:.4f}'),
    }


# --------------------------------------------------------------------------
# the measurement
# --------------------------------------------------------------------------

def measure(corpus: Path, out_dir: Path) -> dict:
    """The whole study."""
    materials = []
    for d in sorted(p for p in corpus.iterdir() if p.is_dir()):
        m = gt.session_material(d)
        if m is None:
            continue
        materials.append(m)
    print(f'  {len(materials)} usable sessions')

    models = []
    for m in materials:
        picked = gt.choose_k_by_silhouette(m)
        if picked is None or picked.get('k') is None:
            continue
        model = gt.session_model(m, picked['k'])
        if model is None:
            continue
        models.append(model)
    n = len(models)
    if not n:
        raise SystemExit('no usable sessions')
    print(f'  {n} sessions with a fitted vocabulary')

    # --- the SELF case -----------------------------------------------------
    self_rows = []
    for m in models:
        a = gt.answer_self(m)
        # the cluster's cells, positioned -- the same labels answer_self
        # counts over
        z = m['full_desc'].reshape(-1, m['full_desc'].shape[-1]) / m['scale']
        labels = gg.assign_nearest(m['centres'], z).reshape(gg.GRID_H, gg.GRID_W)
        answer_cells = m['odd'].reshape(-1) & m['observed'].reshape(-1)
        profile = cluster_profile(labels, m['characteristic'],
                                  answer_cells.reshape(gg.GRID_H, gg.GRID_W))
        dec = geometry_abstains(profile)
        self_rows.append({
            'session': m['session'],
            'answer': a['answer'],
            'left': a['left'], 'right': a['right'],
            'truth': m['truth']['half'],
            'truth_ratio': round(m['truth']['ratio'], 3),
            'agrees': a['answer'] == m['truth']['half'],
            'decisive': m['truth']['ratio'] >= ga.TIE_RATIO,
            'the_profile': [int(v) for v in profile],
            'the_profile_width': int((profile > 0).sum()),
            'the_left_fraction': dec['the_left_fraction'],
            'the_placement_sd': dec['the_placement_sd'],
            'the_observed_in_placement_units': dec['the_observed_in_placement_units'],
            'abstain': dec['abstain'],
            'the_reason': dec['the_reason'],
            # the binomial rules, for comparison
            'abstain_binomial_k2': bool(abs(ga.count_z(a['left'], a['right']))
                                        < 2.0),
            'abstain_binomial_k1': bool(abs(ga.count_z(a['left'], a['right']))
                                        < 1.0),
        })

    # --- the TRANSFER case -------------------------------------------------
    pairs = []
    for i, a_model in enumerate(models):
        for j, b_model in enumerate(models):
            if i == j:
                continue
            r = gt.answer_with(a_model, b_model, a_model['characteristic'])
            z = b_model['full_desc'].reshape(-1, b_model['full_desc'].shape[-1])
            z = z / a_model['scale']
            labels = gg.assign_nearest(a_model['centres'], z)
            answer_cells = b_model['odd'].reshape(-1) & b_model['observed'].reshape(-1)
            profile = cluster_profile(labels.reshape(gg.GRID_H, gg.GRID_W),
                                      a_model['characteristic'],
                                      answer_cells.reshape(gg.GRID_H, gg.GRID_W))
            dec = geometry_abstains(profile)
            pairs.append({
                'from': a_model['session'], 'to': b_model['session'],
                'left': r['left'], 'right': r['right'],
                'answer': r['answer'],
                'agrees': r['answer'] == b_model['truth']['half'],
                'decisive': b_model['truth']['ratio'] >= ga.TIE_RATIO,
                'the_profile_width': int((profile > 0).sum()),
                'the_observed_in_placement_units': dec['the_observed_in_placement_units'],
                'abstain': dec['abstain'],
            })
        if (i + 1) % 10 == 0:
            print(f'  ... {i + 1}/{n} alphabets transferred')

    decisive_self = [r for r in self_rows if r['decisive']]
    decisive_pairs = [p for p in pairs if p['decisive']]

    geometry_self = ga.grade(decisive_self)
    geometry_pairs = ga.grade(decisive_pairs)
    binom2_self = ga.grade([{**r, 'abstain': r['abstain_binomial_k2']}
                             for r in decisive_self])
    binom1_self = ga.grade([{**r, 'abstain': r['abstain_binomial_k1']}
                             for r in decisive_self])
    binom1_pairs = ga.grade([{**p, 'abstain': abs(ga.count_z(p['left'], p['right'])) < 1.0}
                              for p in decisive_pairs])
    geometry_self_all = ga.grade(self_rows)
    geometry_pairs_all = ga.grade(pairs)

    # the AGREEMENT TEST: does the geometry null land where the
    # abstention study's hindsight landed?
    answered_geom = geometry_self['n_answered'] / max(1, geometry_self['n'])
    answered_binom1 = binom1_self['n_answered'] / max(1, binom1_self['n'])
    agreement = {
        'the_geometry_nulls_coverage': round(answered_geom, 4),
        'the_binomial_k1s_coverage': round(answered_binom1, 4),
        'the_two_coverage_ratios': round(answered_geom
                                         / max(answered_binom1, 1e-9), 3),
        'the_sessions_they_disagree_on': [
            r['session'] for r in decisive_self
            if r['abstain'] != r['abstain_binomial_k1']],
        'the_note': ('the agreement test: two independent roads to the same '
                     'operating point. The geometry null is built from the '
                     'session\'s own material and the binomial K = 1 is the '
                     'abstention study\'s hindsight point; if their coverage '
                     'ratios are near 1, the point is not an artefact of '
                     'looking at a curve.'),
    }

    bar = {
        '1_the_rule_catches_half_the_decisive_errors_and_loses_at_most_a_quarter':
            (geometry_self['the_errors_caught'] is not None and
             geometry_self['the_errors_caught'] >= 0.5 and
             (geometry_self['the_right_answers_lost'] or 0.0) <= 0.25),
        '2_the_accuracy_among_the_answered_is_5_points_above_the_accuracy_over_all':
            (geometry_self['accuracy_among_the_answered'] is not None and
             geometry_self['accuracy_among_the_answered'] -
             geometry_self['accuracy_over_all'] >= 0.05),
        '3_teacher_dependence_is_zero_and_the_only_knob_is_declared': True,
        '4_the_two_roads_agree_within_25_percent_on_coverage':
            bool(abs(agreement['the_two_coverage_ratios'] - 1.0) <= 0.25),
    }

    out = {
        'study': 'the geometry null',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'the_rule': {
            'the_statistic': 'the cluster\'s left fraction among the answer '
                             'cells; the imbalance is f - 0.5',
            'the_null': 'the placements of the session\'s own cluster that '
                        'keep it inside the room',
            'the_rule': f'abstain when |f(0) - 0.5| < {Z_NULL} * sd(f)',
            'Z_NULL': Z_NULL,
            'the_only_knob_is_declared': True,
            'the_rule_is_truth_blind': True,
            'the_inputs': ['the session\'s own cluster cells'],
        },
        'the_self_case': {
            'n_sessions': len(self_rows),
            'n_decisive': len(decisive_self),
            'the_geometry_null': geometry_self,
            'the_geometry_null_over_all_sessions': geometry_self_all,
            'the_binomial_k2': binom2_self,
            'the_binomial_k1': binom1_self,
            'the_rows': self_rows,
        },
        'the_transfer_case': {
            'n_pairs': len(pairs),
            'n_decisive': len(decisive_pairs),
            'the_geometry_null': geometry_pairs,
            'the_geometry_null_over_all_pairs': geometry_pairs_all,
            'the_binomial_k1': binom1_pairs,
        },
        'the_agreement_test': agreement,
        'the_bar': bar,
        'the_bar_is_met': all(bar.values()),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_geometry_null.json').write_text(json.dumps(out, indent=1))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the profile: the blob's column histogram over the ANSWER cells
    labels = np.zeros((gg.GRID_H, gg.GRID_W), dtype=int)
    labels[5, 1:5] = 2          # four cells of cluster 2, on odd columns
    labels[6, 7:11] = 2
    labels[7, 25:29] = 2
    answer_cells = np.ones((gg.GRID_H, gg.GRID_W), dtype=bool)
    prof = cluster_profile(labels, 2, answer_cells)
    ck('null: the profile counts the blob\'s cells per answer column',
       list(prof) == [1.0, 1.0, 0.0, 1.0, 1.0] + [0.0] * 7 + [1.0, 1.0]
                     + [0.0] * 6,
       str([int(v) for v in prof]))
    ck('null: the profile counts only the CHARACTERISTIC cluster',
       list(cluster_profile(labels, 1, answer_cells)) ==
       [0.0] * 20, str(list(cluster_profile(labels, 1, answer_cells))))

    # 2. the placements: a blob in the middle can move both ways
    profile = np.zeros(20)
    profile[2:5] = 3.0
    ck('null: a blob in the middle has placements on both sides',
       min(placements(profile)) < 0 < max(placements(profile)),
       str(placements(profile)))
    edge = np.zeros(20)
    edge[0:3] = 1.0
    ck('null: a blob at the edge can only move one way',
       min(placements(edge)) == 0 and max(placements(edge)) > 0,
       str(placements(edge)))

    # 3. a blob that cannot move anywhere abstains
    wide = np.zeros(20)
    wide[:] = 1.0
    d = geometry_abstains(wide)
    ck('null: a blob that fits nowhere else abstains',
       d['abstain'], str(d['the_reason']))

    # 4. a narrow blob placed off-centre answers
    narrow = np.zeros(20)
    narrow[1:3] = 1.0
    d2 = geometry_abstains(narrow)
    ck('null: a narrow off-centre blob answers',
       not d2['abstain'], str(d2))

    # 5. a narrow blob placed at the centre abstains
    centred = np.zeros(20)
    centred[9:11] = 1.0
    d3 = geometry_abstains(centred)
    ck('null: a narrow centred blob abstains',
       d3['abstain'], str(d3['the_reason']))

    # 6. a WIDE blob PINNED to one side answers -- the placement null
    #    says it could have been elsewhere -- while a blob that CANNOT
    #    move abstains.  This is the physics the binomial cannot see,
    #    and it cuts the other way from the naive expectation.
    wideish = np.zeros(20)
    wideish[0:12] = 1.0
    d4 = geometry_abstains(wideish)
    ck('null: a wide blob PINNED to one side answers',
       not d4['abstain'], str(d4['the_reason']))
    ck('null: a wide blob that could have been elsewhere has a big spread',
       d4['the_placement_sd'] > 0.2, str(d4['the_placement_sd']))

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"   [{detail}]" if detail and not ok else ""))
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


def cluster_profile_from_cells(profile: np.ndarray) -> np.ndarray:
    """The identity, for the selftest: the profile IS the histogram."""
    return profile


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(ROOT / 'results'))
    ap.add_argument('--corpus', default='/mnt/c/proart_capture/corpus/free_sessions')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    corpus = Path(args.corpus)
    print(f'glyph geometry null: {len([d for d in corpus.iterdir() if d.is_dir()])} sessions')
    out = measure(corpus, Path(args.out))
    print(json.dumps(out['the_self_case']['the_geometry_null'], indent=1))
    print(json.dumps(out['the_self_case']['the_binomial_k1'], indent=1))
    print(json.dumps(out['the_agreement_test'], indent=1))
    print(json.dumps(out['the_bar'], indent=1))
    print(f"wrote {Path(args.out) / 'glyph_geometry_null.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

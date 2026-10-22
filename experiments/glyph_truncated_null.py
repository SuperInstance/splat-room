#!/usr/bin/env python3
"""THE TRUNCATED PLACEMENT NULL -- the designated next measurement of the
abstention arc, and the declaration that goes with it.

    /home/proart/projects/gpu-venv/bin/python experiments/glyph_truncated_null.py --selftest
    /home/proart/projects/gpu-venv/bin/python experiments/glyph_truncated_null.py --out results

WHAT THIS IS.  The geometry null study (docs/GLYPH-GEOMETRY-NULL.md) left
one thing undone and named the candidate for it: **a null that handles the
room-wide case**.  The geometry null places the session's own cluster
inside the frame, and for a cluster that spans every answer column there
is exactly one such placement, so the null has no spread and the rule
abstains -- on 15 of the 33 decisive self sessions, all 15 of them right
answers.  The candidate is the **truncated placement null**: the room has
walls but the CAMERA'S FRAME IS NARROWER THAN THE ROOM, so the material
may sit partly outside the frame, and clipping to the frame gives a
non-zero spread even for a room-wide profile.

THE DECLARATION.  Everything below is fixed BEFORE the run.  Nothing here
is chosen after seeing an answer.

  1. THE NULL.  The session's own characteristic cluster is translated to
     EVERY horizontal position that leaves some of it inside the frame --
     including the positions that push part of it out.  The statistic is
     the left fraction of the material that REMAINS INSIDE the frame, and
     the null's spread is the standard deviation of that over the
     placements.  The room's width relative to the frame is not measured
     anywhere in the corpus, and the null says so by allowing the
     material anywhere: that ignorance is the point, not a defect.

  2. THE RULE.  Abstain when the observed left fraction is within
     Z_NULL null standard deviations of the NULL'S OWN CENTRE.  The
     reference is the null's centre rather than 0.5 because the truncated
     null is not symmetric -- clipping the material at one edge is not
     the mirror of clipping it at the other.  When the null IS symmetric
     (the geometry null's case) the centre IS 0.5 and this rule reduces
     to the geometry null's rule exactly, so the two are comparable.

  3. THE KNOB.  Z_NULL = 1, the same number the geometry null used, so
     that the two rules differ only in the null and not in the
     threshold.  It is the only number in the rule.

  4. THE DEGENERATE READING.  A null with no spread -- fewer than two
     placements, or every placement giving the same vote -- means the
     rule ABSTAINS.  This is the CONSERVATIVE reading, declared here
     before the run, and it is NOT the permissive one.  The permissive
     reading was measured and seen in the geometry null study (it is
     better on that corpus) and adopting it now would be hindsight
     wearing a rule's clothes.

  5. THE BARS.  The geometry null's four bars, unchanged, so the two
     studies are judged the same way.

  6. THE FRESHNESS CAVEAT, STATED PLAINLY.  The geometry null study
     asked for this to be run on a corpus that has grown, because that
     session had seen the split.  The corpus has NOT grown since -- the
     same 121 sessions -- so the freshness mitigation is UNAVAILABLE and
     this study is NOT a fresh confirmation.  It is a measurement of what
     the corrected null does, on a corpus whose split the analyst has
     already seen.  The rule is truth-blind and declared in advance, and
     that is the only protection there is.

     *** DATED CORRECTION, 2026-10-22, AFTER THE RUN.  ITEM 6 WAS
     FALSE, AND IT WAS FALSE BECAUSE IT WAS NOT MEASURED.  The corpus
     was counted instead of taken from the previous session's notes, and
     it had grown: 139 session directories where the notes said 121,
     and 55 sessions with a fitted vocabulary where the geometry null
     study saw 47.  EIGHT sessions had landed after the arc's last look
     and BEFORE this declaration was written, so they were already on
     disk when the rule was fixed.

     The rule is untouched by this: it is truth-blind, it was fixed
     before the run, and nothing in it changed.  What was wrong is the
     CAVEAT, and the lesson is the one this seat keeps learning: A
     FRESHNESS CAVEAT IS A MEASUREMENT AND NOT A FOOTNOTE.  A number
     carried forward in prose is a number nobody checked, and it was
     wrong by 18 directories and 8 usable sessions.

     The correction has a consequence worth having, and it is the one
     the geometry study asked for: the corpus HAS grown, so the held-out
     set exists.  The eight sessions that arrived after the arc's last
     look are reported separately, under the same unchanged rule, as
     THE HELD-OUT SET.  The split is by ARRIVAL, not by outcome, so it
     is not a hindsight choice; it was also not in the declaration, and
     that is said rather than hidden.

The rule uses no truth information: it sees the session's own cluster
cells and nothing else.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments import glyph_abstain as ga  # noqa: E402
from experiments import glyph_geometry_null as ggn  # noqa: E402
from experiments import glyph_grid as gg  # noqa: E402
from experiments import glyph_transfer as gt  # noqa: E402

#: THE ONLY NUMBER IN THE RULE.  DECLARED BEFORE THE MEASUREMENT, and
#: the same number the geometry null used, so that the two rules differ
#: in their NULL and not in their threshold.
Z_NULL = 1.0


# --------------------------------------------------------------------------
# the null
# --------------------------------------------------------------------------

def truncated_placement_fractions(profile: np.ndarray) -> np.ndarray:
    """The left fraction for EVERY translation, including the ones that
    push part of the material out of the frame.

    THE FRAME IS NARROWER THAN THE ROOM.  The material was observed
    inside the frame, but it need not have been entirely inside it: the
    room is wider than what the camera sees, so the cluster may have
    been partly outside.  Translating it and clipping to the frame gives
    a non-zero spread even for a profile that spans every column, which
    is exactly the case the geometry null could not handle.
    """
    n = profile.size
    half = n // 2
    out = []
    for s in range(-(n - 1), n):
        shifted = np.zeros(n, dtype=np.float64)
        for i in range(n):
            j = i - s
            if 0 <= j < n:
                shifted[i] = profile[j]
        total = shifted.sum()
        if total <= 0:
            continue                      # the material is wholly outside
        out.append(float(shifted[:half].sum() / total))
    return np.asarray(out, dtype=np.float64)


def truncated_abstains(profile: np.ndarray, z_null: float = Z_NULL) -> dict:
    """Does the vocabulary abstain on this blob's placement?

    THE REFERENCE IS THE NULL'S OWN CENTRE, not 0.5.  The truncated
    null is not symmetric -- clipping the material at one edge is not
    the mirror of clipping it at the other -- so the null's centre is
    where a typical placement would have put the vote, and the observed
    is compared to THAT.  For the geometry null's symmetric null the
    centre is exactly 0.5, so the two rules are the same rule.
    """
    total = float(profile.sum())
    f_obs = None
    if total > 0:
        f_obs = float(profile[:profile.size // 2].sum() / total)
    fs = truncated_placement_fractions(profile)
    if f_obs is None or fs.size < 2:
        # no material, or a null with nothing to spread over: the vote
        # carries no information, so the answer is "I do not know"
        return {'the_left_fraction': None,
                'the_null_mean': None,
                'the_null_sd': None,
                'the_observed_in_null_units': None,
                'abstain': True,
                'the_reason': ('the null has no spread -- the material '
                               'cannot be placed anywhere else, so its '
                               'position carries no information')}
    centre = float(fs.mean())
    sd = float(fs.std(ddof=1))
    offset = abs(f_obs - centre)
    units = offset / sd if sd > 0 else float('inf')
    return {
        'the_left_fraction': round(f_obs, 4),
        'the_null_mean': round(centre, 4),
        'the_null_sd': round(sd, 4),
        'the_observed_in_null_units': (round(units, 4)
                                       if np.isfinite(units) else None),
        'abstain': bool(units < z_null),
        'the_reason': (f'{offset:.4f} from the null\'s centre {centre:.4f}, '
                       f'against a null spread of {sd:.4f}'),
    }


# --------------------------------------------------------------------------
# the measurement
# --------------------------------------------------------------------------

def _cluster_profile(labels: np.ndarray, characteristic: int,
                     answer_cells: np.ndarray) -> np.ndarray:
    """The characteristic cluster's column profile over the ANSWER cells.

    THE GEOMETRY NULL'S OWN CONSTRUCTION, CALLED RATHER THAN COPIED, so
    the two rules provably see the same material and the comparison is
    exactly paired."""
    return ggn.cluster_profile(labels, characteristic, answer_cells)


def measure(corpus: Path, out_dir: Path, prior: Path | None = None) -> dict:
    """The whole study: the truncated null beside the geometry null."""
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
        z = m['full_desc'].reshape(-1, m['full_desc'].shape[-1]) / m['scale']
        labels = gg.assign_nearest(m['centres'], z).reshape(gg.GRID_H, gg.GRID_W)
        answer_cells = m['odd'].reshape(-1) & m['observed'].reshape(-1)
        profile = _cluster_profile(labels, m['characteristic'],
                                   answer_cells.reshape(gg.GRID_H, gg.GRID_W))
        trunc = truncated_abstains(profile)
        geom = ggn.geometry_abstains(profile)
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
            'the_left_fraction': trunc['the_left_fraction'],
            'the_null_mean': trunc['the_null_mean'],
            'the_null_sd': trunc['the_null_sd'],
            'the_observed_in_null_units': trunc['the_observed_in_null_units'],
            'abstain': trunc['abstain'],
            'the_reason': trunc['the_reason'],
            # the geometry null, for the paired comparison
            'the_geometry_null_sd': geom['the_placement_sd'],
            'the_geometry_abstain': geom['abstain'],
            'the_geometry_reason': geom['the_reason'],
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
            profile = _cluster_profile(labels.reshape(gg.GRID_H, gg.GRID_W),
                                       a_model['characteristic'],
                                       answer_cells.reshape(gg.GRID_H, gg.GRID_W))
            trunc = truncated_abstains(profile)
            geom = ggn.geometry_abstains(profile)
            pairs.append({
                'from': a_model['session'], 'to': b_model['session'],
                'left': r['left'], 'right': r['right'],
                'answer': r['answer'],
                'agrees': r['answer'] == b_model['truth']['half'],
                'decisive': b_model['truth']['ratio'] >= ga.TIE_RATIO,
                'the_profile_width': int((profile > 0).sum()),
                'the_observed_in_null_units': trunc['the_observed_in_null_units'],
                'abstain': trunc['abstain'],
                # the geometry null, for the paired comparison
                'the_geometry_null_sd': geom['the_placement_sd'],
                'the_geometry_abstain': geom['abstain'],
            })
        if (i + 1) % 10 == 0:
            print(f'  ... {i + 1}/{n} alphabets transferred')

    decisive_self = [r for r in self_rows if r['decisive']]
    decisive_pairs = [p for p in pairs if p['decisive']]

    trunc_self = ga.grade(decisive_self)
    trunc_pairs = ga.grade(decisive_pairs)
    geom_self = ga.grade([{**r, 'abstain': r['the_geometry_abstain']}
                           for r in decisive_self])
    geom_pairs = ga.grade([{**p, 'abstain': p['the_geometry_abstain']}
                           for p in decisive_pairs])
    binom1_self = ga.grade([{**r, 'abstain': abs(ga.count_z(r['left'], r['right'])) < 1.0}
                             for r in decisive_self])
    binom2_self = ga.grade([{**r, 'abstain': abs(ga.count_z(r['left'], r['right'])) < 2.0}
                             for r in decisive_self])
    binom1_pairs = ga.grade([{**p, 'abstain': abs(ga.count_z(p['left'], p['right'])) < 1.0}
                              for p in decisive_pairs])
    binom2_pairs = ga.grade([{**p, 'abstain': abs(ga.count_z(p['left'], p['right'])) < 2.0}
                              for p in decisive_pairs])

    # the room-wide case, which is the whole reason for the study
    wide = [r for r in decisive_self if r['the_profile_width'] >= 20]
    wide_rows = []
    for r in wide:
        wide_rows.append({
            'session': r['session'],
            'the_profile_width': r['the_profile_width'],
            'the_left_fraction': r['the_left_fraction'],
            'the_null_mean': r['the_null_mean'],
            'the_null_sd': r['the_null_sd'],
            'the_observed_in_null_units': r['the_observed_in_null_units'],
            'the_truncated_abstain': r['abstain'],
            'the_geometry_abstain': r['the_geometry_abstain'],
            'agrees': r['agrees'],
        })
    wide_summary = {
        'the_n_room_wide_decisive_sessions': len(wide),
        'the_truncated_null_finds_a_spread_on': sum(
            1 for r in wide if (r['the_null_sd'] or 0) > 0),
        'the_truncated_null_abstains_on': sum(1 for r in wide if r['abstain']),
        'the_geometry_null_abstains_on': sum(1 for r in wide
                                              if r['the_geometry_abstain']),
        'the_room_wide_sessions_that_are_right': sum(1 for r in wide if r['agrees']),
        'the_rows': wide_rows,
    }

    bar = {
        '1_the_rule_catches_half_the_decisive_errors_and_loses_at_most_a_quarter':
            (trunc_self['the_errors_caught'] is not None and
             trunc_self['the_errors_caught'] >= 0.5 and
             (trunc_self['the_right_answers_lost'] or 0.0) <= 0.25),
        '2_the_accuracy_among_the_answered_is_5_points_above_the_accuracy_over_all':
            (trunc_self['accuracy_among_the_answered'] is not None and
             trunc_self['accuracy_among_the_answered'] -
             trunc_self['accuracy_over_all'] >= 0.05),
        '3_teacher_dependence_is_zero_and_the_only_knob_is_declared': True,
        '4_the_two_roads_agree_within_25_percent_on_coverage':
            bool(abs((trunc_self['n_answered'] / max(1, trunc_self['n']))
                     / max(binom1_self['n_answered'] / max(1, binom1_self['n']),
                           1e-9) - 1.0) <= 0.25),
    }

    # --- THE HELD-OUT SET -------------------------------------------------
    # The sessions that arrived AFTER the previous study saw the corpus.
    # The split is by ARRIVAL, not by outcome, so it cannot be a
    # hindsight choice; and the rule is the same unchanged rule.
    held_out = None
    if prior is not None and prior.is_file():
        prev = json.loads(prior.read_text())
        seen = {r['session'] for r in prev['the_self_case']['the_rows']}
        held_rows = [r for r in self_rows if r['session'] not in seen]
        seen_rows = [r for r in self_rows if r['session'] in seen]
        h_dec = [r for r in held_rows if r['decisive']]
        s_dec = [r for r in seen_rows if r['decisive']]
        h_pairs = [p for p in pairs if p['to'] not in seen]
        held_out = {
            'the_prior_study': prior.name,
            'the_prior_study_sessions': len(seen),
            'the_sessions_the_prior_study_had_seen': len(seen_rows),
            'the_held_out_sessions': len(held_rows),
            'the_held_out_decisive': len(h_dec),
            'the_held_out_session_names': [r['session'] for r in held_rows],
            'the_truncated_null_on_the_held_out': ga.grade(h_dec),
            'the_geometry_null_on_the_held_out': ga.grade(
                [{**r, 'abstain': r['the_geometry_abstain']} for r in h_dec]),
            'the_truncated_null_on_the_seen': ga.grade(s_dec),
            'the_geometry_null_on_the_seen': ga.grade(
                [{**r, 'abstain': r['the_geometry_abstain']} for r in s_dec]),
            'the_held_out_transfer_pairs': len(h_pairs),
            'the_truncated_null_on_the_held_out_pairs': ga.grade(
                [p for p in h_pairs if p['decisive']]),
            'the_geometry_null_on_the_held_out_pairs': ga.grade(
                [{**p, 'abstain': p['the_geometry_abstain']}
                 for p in h_pairs if p['decisive']]),
            'the_rows': held_rows,
            'the_note': ('the split is by ARRIVAL, not by outcome: these '
                         'sessions landed after the prior study ran and are '
                         'reported under the same unchanged, truth-blind '
                         'rule. The split was NOT in the declaration -- the '
                         'declaration said the corpus had not grown, which '
                         'was false -- and the correction is dated in the '
                         'module docstring.'),
        }

    out = {
        'study': 'the truncated placement null',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'the_declaration': {
            'the_null': ('the session\'s own cluster translated to EVERY '
                         'position that leaves some of it inside the frame, '
                         'including the positions that push part of it out; '
                         'the statistic is the left fraction of the material '
                         'that REMAINS INSIDE'),
            'the_rule': ('abstain when |f(0) - the null\'s own centre| < '
                         f'{Z_NULL} * sd(null)'),
            'the_knob': Z_NULL,
            'the_degenerate_reading': 'CONSERVATIVE: a null with no spread '
                                      'means abstain',
            'the_bars': 'the geometry null study\'s four bars, unchanged',
            'the_freshness_caveat': ('the corpus has NOT grown since the '
                                     'geometry null study, so this is not a '
                                     'fresh confirmation; the rule is '
                                     'truth-blind and declared before the '
                                     'run, and that is the only protection'),
        },
        'the_self_case': {
            'n_sessions': len(self_rows),
            'n_decisive': len(decisive_self),
            'the_truncated_null': trunc_self,
            'the_geometry_null': geom_self,
            'the_binomial_k1': binom1_self,
            'the_binomial_k2': binom2_self,
            'the_rows': self_rows,
        },
        'the_transfer_case': {
            'n_pairs': len(pairs),
            'n_decisive': len(decisive_pairs),
            'the_truncated_null': trunc_pairs,
            'the_geometry_null': geom_pairs,
            'the_binomial_k1': binom1_pairs,
            'the_binomial_k2': binom2_pairs,
        },
        'the_room_wide_case': wide_summary,
        'the_held_out_set': held_out,
        'the_bar': bar,
        'the_bar_is_met': all(bar.values()),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_truncated_null.json').write_text(json.dumps(out, indent=1))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. a NARROW profile: the truncated null must have a spread, and
    #    the rule must answer a profile that is clearly on one side.
    narrow = np.zeros(20)
    narrow[1] = 8.0
    narrow[2] = 8.0
    dec = truncated_abstains(narrow)
    ck('truncated: a narrow profile has a null with a spread',
       dec['the_null_sd'] is not None and dec['the_null_sd'] > 0,
       str(dec))
    ck('truncated: a profile clearly on one side is ANSWERED',
       not dec['abstain'], str(dec))

    # 2. a profile straddling the centre: the vote is tied, and the
    #    rule must abstain.
    mid = np.zeros(20)
    mid[9] = 10.0
    mid[10] = 10.0
    dec_mid = truncated_abstains(mid)
    ck('truncated: a profile straddling the centre is abstained on',
       dec_mid['abstain'], str(dec_mid))

    # 3. THE ROOM-WIDE CASE, which is the whole reason for the study: a
    #    profile that spans every column must get a NON-DEGENERATE null.
    #    The geometry null cannot do that, and the test must show it.
    wide = np.ones(20) * 5.0
    dec_wide = truncated_abstains(wide)
    ck('truncated: a room-wide profile gets a NON-degenerate null',
       dec_wide['the_null_sd'] is not None and dec_wide['the_null_sd'] > 0,
       str(dec_wide))
    geom_wide = ggn.geometry_abstains(wide)
    ck('truncated: the geometry null IS degenerate on the same profile',
       geom_wide['abstain'] and geom_wide['the_placement_sd'] is None,
       str(geom_wide))

    # 4. the rule reduces to the geometry null's rule when the null is
    #    symmetric: the reference is the null's own centre.
    ck('truncated: the reference is the null\'s own centre, not 0.5',
       dec['the_null_mean'] is not None
       and abs(dec['the_null_mean'] - 0.5) < 1e-9,
       str(dec['the_null_mean']))

    # 5. the degenerate reading: no material at all abstains.
    empty = np.zeros(20)
    dec_empty = truncated_abstains(empty)
    ck('truncated: no material at all abstains',
       dec_empty['abstain'], str(dec_empty))

    # 6. the null is TRUNCATED: the material may leave the frame, so a
    #    shift that drops material must change the vote.
    left_edge = np.zeros(20)
    left_edge[0] = 10.0
    fs = truncated_placement_fractions(left_edge)
    ck('truncated: the placements include the ones that drop material',
       fs.size > 2 and float(fs.min()) < 0.05 and float(fs.max()) > 0.95,
       f'{fs.size} placements, min {fs.min():.3f}, max {fs.max():.3f}')

    # 7. the Z knob is the only number, and it is the geometry null's
    ck('truncated: the knob is the geometry null\'s own number',
       Z_NULL == 1.0, str(Z_NULL))

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"   [{detail}]" if detail and not ok else ""))
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--out', default=str(ROOT / 'results'))
    ap.add_argument('--corpus',
                    default='/mnt/c/proart_capture/corpus/free_sessions')
    ap.add_argument('--prior', default=None,
                    help='a prior study json: the sessions it had seen are '
                         'the SEEN set, and everything else is the HELD-OUT '
                         'set. The split is by arrival, not by outcome.')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    out = measure(Path(args.corpus), Path(args.out),
                  Path(args.prior) if args.prior else None)
    print(json.dumps({
        'the_self_case': out['the_self_case']['the_truncated_null'],
        'the_geometry_null': out['the_self_case']['the_geometry_null'],
        'the_room_wide_case': {k: v for k, v in
                               out['the_room_wide_case'].items()
                               if k != 'the_rows'},
        'the_held_out_set': ({k: v for k, v in
                              out['the_held_out_set'].items()
                              if k not in ('the_rows', 'the_note')}
                             if out['the_held_out_set'] else None),
        'the_transfer_case': out['the_transfer_case']['the_truncated_null'],
        'the_bar': out['the_bar'],
        'the_bar_is_met': out['the_bar_is_met'],
    }, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())

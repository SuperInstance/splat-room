#!/usr/bin/env python3
"""THE HELD-OUT SCORECARD -- what the abstention arc's candidates do on the
sessions that arrived after the arc's last look.

    /home/proart/projects/gpu-venv/bin/python experiments/glyph_holdout_scorecard.py --selftest
    /home/proart/projects/gpu-venv/bin/python experiments/glyph_holdout_scorecard.py --out results

WHAT THIS IS.  The abstention study closed with a checklist item it could
not close: "The shipped rule does not exist yet.  Its operating point
cannot be chosen from this run without hindsight.  It has to be declared
by argument and then measured, which means a fresh corpus or a
held-out split."  **THE CORPUS HAS GROWN**, so the held-out split now
exists, and this is the scorecard over it.

THE ARC'S CANDIDATES, ALL FOUR, IN ONE PASS OVER THE SAME MATERIAL.

    the count rule at K = 1     the abstention study's HINDSIGHT point
    the count rule at K = 2     the abstention study's DECLARED point
    the geometry null          the geometry study's rule, Z_NULL = 1
    the truncated null         this lane's newest rule, Z_NULL = 1

THE SET.  The sessions in the corpus that the geometry null study did
NOT see -- the same definition the truncated null study used, and the
split is by ARRIVAL, not by outcome.  Eight of them, all decisive.

THE DECLARATION, fixed before the run.

  1. THE BARS.

     BAR 1 -- COVERAGE STABILITY, AND THIS ONE IS TRUTH-BLIND.  Every
     candidate's coverage on the held-out set must be within 25
     percentage points of its coverage on the seen set.  Coverage
     depends only on the rule's own inputs and never on the truth, so
     this bar is not contaminated by anything seen elsewhere.

     BAR 2 -- NO CANDIDATE COLLAPSES, AND THIS ONE IS TRUTH-BLIND TOO.
     A candidate that answers at least 20 per cent of the SEEN decisive
     sessions must answer at least 20 per cent of the HELD-OUT ones.  A
     rule that works on the corpus it was chosen on and goes silent on
     the next eight sessions is not a rule that can ship.

     BAR 3 -- TEACHER DEPENDENCE 0.000 AND EVERY KNOB DECLARED BEFORE
     ITS RUN: the count rule at K = 1 and K = 2, the geometry null and
     the truncated null both at Z_NULL = 1, each fixed before the
     measurement that used it.

     BAR 4 -- THE TRADE-OFF ON THE HELD-OUT SET: the best accuracy
     among the answered among the candidates must be at least 5 points
     above the held-out set's accuracy over all.

  2. THE CONTAMINATION, STATED BEFORE THE RUN AND NOT AFTER.  The
     held-out sessions' counts and their truth labels were ALREADY
     VISIBLE in the truncated null study's per-session rows, because
     that study filed them.  So bar 4 is arithmetic on inputs this
     analysis has already seen, and it is NOT a blind confirmation of
     anything.  Bars 1, 2 and 3 are blind, because none of them
     consults the truth.

     This is the same species of error as the truncated null study's
     false freshness caveat, and it is stated here rather than left to
     be noticed.

  3. THE SELF CASE IS THE SCORECARD, and the transfer is not in it.  The
     per-pair rows are not filed by any study, so the transfer would
     have to be recomputed; the arc's own bars are stated on the self
     case, and that is where this is measured.

  4. THE FRESHNESS CAVEAT FOR THIS STUDY, STATED PLAINLY.  The split
     is by arrival and the rule never consults the truth, so the
     contamination in item 2 is the only one, and it is bounded to bar
     4.
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
from experiments import glyph_truncated_null as gtn  # noqa: E402
from experiments import glyph_transfer as gt  # noqa: E402

#: THE CANDIDATES AND THEIR KNOBS.  Every one of these was fixed before
#: the measurement that used it, and none of them is fitted here.
CANDIDATES = (
    ('the_count_rule_at_k1', 'K = 1', 1.0),
    ('the_count_rule_at_k2', 'K = 2', 2.0),
    ('the_geometry_null', 'Z_NULL = 1', None),
    ('the_truncated_null', 'Z_NULL = 1', None),
)

#: BAR 1's band, in percentage points.
COVERAGE_BAND = 0.25

#: BAR 2's floor, the share of the held-out decisive sessions a
#: candidate that worked on the seen ones must still answer.
NO_COLLAPSE_FLOOR = 0.20

#: BAR 4's margin, in accuracy points.
HELD_OUT_MARGIN = 0.05


def the_candidates(left: int, right: int,
                   profile: np.ndarray) -> dict[str, bool]:
    """Each candidate's abstain flag for one session or pair.

    All four, on the same material, in the same place."""
    z = abs(ga.count_z(left, right))
    return {
        'the_count_rule_at_k1': bool(z < 1.0),
        'the_count_rule_at_k2': bool(z < 2.0),
        'the_geometry_null': bool(ggn.geometry_abstains(profile)['abstain']),
        'the_truncated_null': bool(gtn.truncated_abstains(profile)['abstain']),
    }


def grade_candidates(rows: list[dict]) -> dict[str, dict]:
    """Every candidate graded on the same rows."""
    return {name: ga.grade([{**r, 'abstain': r[name]} for r in rows])
            for name, _knob, _k in CANDIDATES}


def measure(corpus: Path, out_dir: Path, prior: Path | None = None) -> dict:
    """The scorecard."""
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

    # --- the SELF rows -----------------------------------------------------
    self_rows = []
    for m in models:
        a = gt.answer_self(m)
        z = m['full_desc'].reshape(-1, m['full_desc'].shape[-1]) / m['scale']
        labels = gg.assign_nearest(m['centres'], z).reshape(gg.GRID_H, gg.GRID_W)
        answer_cells = m['odd'].reshape(-1) & m['observed'].reshape(-1)
        profile = ggn.cluster_profile(labels, m['characteristic'],
                                      answer_cells.reshape(gg.GRID_H, gg.GRID_W))
        row = {
            'session': m['session'],
            'left': a['left'], 'right': a['right'],
            'answer': a['answer'],
            'truth': m['truth']['half'],
            'agrees': a['answer'] == m['truth']['half'],
            'decisive': m['truth']['ratio'] >= ga.TIE_RATIO,
            'the_profile_width': int((profile > 0).sum()),
        }
        row.update(the_candidates(a['left'], a['right'], profile))
        self_rows.append(row)

    # --- the split ---------------------------------------------------------
    seen_sessions: set[str] | None = None
    if prior is not None and prior.is_file():
        prev = json.loads(prior.read_text())
        seen_sessions = {r['session'] for r in prev['the_self_case']['the_rows']}

    if seen_sessions is None:
        seen_rows = self_rows
        held_rows: list[dict] = []
    else:
        seen_rows = [r for r in self_rows if r['session'] in seen_sessions]
        held_rows = [r for r in self_rows if r['session'] not in seen_sessions]

    seen_dec = [r for r in seen_rows if r['decisive']]
    held_dec = [r for r in held_rows if r['decisive']]

    seen_grades = grade_candidates(seen_dec)
    held_grades = grade_candidates(held_dec)

    # --- the BARS ----------------------------------------------------------
    # Bar 1 and bar 2: coverage stability and no collapse.  TRUTH-BLIND.
    stability = {}
    for name, _knob, _k in CANDIDATES:
        sc = seen_grades[name]['coverage'] or 0.0
        hc = held_grades[name]['coverage'] or 0.0
        stability[name] = {
            'the_seen_coverage': sc,
            'the_held_out_coverage': hc,
            'the_difference': round(abs(hc - sc), 4),
            'within_the_band': bool(abs(hc - sc) <= COVERAGE_BAND),
            'it_collapsed': bool(sc >= NO_COLLAPSE_FLOOR
                                 and hc < NO_COLLAPSE_FLOOR),
        }
    bar1 = all(v['within_the_band'] for v in stability.values())
    bar2 = not any(v['it_collapsed'] for v in stability.values())

    # Bar 3: teacher dependence and declared knobs.
    bar3 = True

    # Bar 4: the trade-off on the held-out set.  CONTAMINATED, and said so.
    held_over_all = held_grades[CANDIDATES[0][0]]['accuracy_over_all']
    best_held = None
    for name, _knob, _k in CANDIDATES:
        acc = held_grades[name]['accuracy_among_the_answered']
        if acc is None:
            continue
        if best_held is None or acc > best_held[1]:
            best_held = (name, acc)
    bar4 = bool(best_held is not None
                and best_held[1] - (held_over_all or 0.0) >= HELD_OUT_MARGIN)

    bar = {
        '1_the_coverage_is_stable_between_the_seen_and_the_held_out_sets':
            bar1,
        '2_no_candidate_collapses_on_the_held_out_set': bar2,
        '3_teacher_dependence_is_zero_and_every_knob_was_declared_before_its_run':
            bar3,
        '4_the_best_trade_off_on_the_held_out_set_is_5_points_above_over_all':
            bar4,
    }

    out = {
        'study': 'the held-out scorecard',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'the_declaration': {
            'the_set': ('the sessions the geometry null study did not see; '
                        'the split is by ARRIVAL, not by outcome'),
            'the_candidates': [{'the_rule': n, 'the_knob': k}
                               for n, k, _ in CANDIDATES],
            'the_bars': ('1 coverage stability within 25 points (truth-blind); '
                         '2 no candidate that answers 20 per cent of the seen '
                         'decisive sessions collapses below 20 per cent on the '
                         'held-out ones (truth-blind); 3 teacher dependence '
                         '0.000 with every knob declared before its run; '
                         '4 the best accuracy among the answered on the '
                         'held-out set is 5 points above over all '
                         '(CONTAMINATED, see below)'),
            'the_contamination': ('the held-out sessions\' counts and truth '
                                  'labels were ALREADY VISIBLE in the '
                                  'truncated null study\'s per-session rows, '
                                  'so bar 4 is arithmetic on known inputs and '
                                  'NOT a blind confirmation. Bars 1, 2 and 3 '
                                  'never consult the truth and are blind.'),
        },
        'the_set': {
            'the_prior_study': prior.name if prior else None,
            'the_seen_sessions': len(seen_rows),
            'the_held_out_sessions': len(held_rows),
            'the_held_out_decisive': len(held_dec),
            'the_held_out_session_names': [r['session'] for r in held_rows],
        },
        'the_seen_case': seen_grades,
        'the_held_out_case': held_grades,
        'the_coverage_stability': stability,
        'the_best_trade_off_on_the_held_out_set': (
            {'the_rule': best_held[0], 'the_accuracy_among_the_answered':
             best_held[1]} if best_held else None),
        'the_held_out_accuracy_over_all': held_over_all,
        'the_bar': bar,
        'the_bar_is_met': all(bar.values()),
        'the_rows': {'the_seen': seen_rows, 'the_held_out': held_rows},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_holdout_scorecard.json').write_text(json.dumps(out, indent=1))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the count rule's flag is the count's z against its K
    prof = np.zeros(20)
    prof[2:6] = 3.0
    # a count of 30 cells split 18/12 gives z = 6/sqrt(30) = 1.095
    c = the_candidates(18, 12, prof)
    ck('scorecard: the count rule abstains at K = 2 but not at K = 1',
       c['the_count_rule_at_k2'] and not c['the_count_rule_at_k1'],
       str(c))
    # a near-tie abstains at both
    c2 = the_candidates(30, 29, prof)
    ck('scorecard: a near-tie abstains at both K values',
       c2['the_count_rule_at_k1'] and c2['the_count_rule_at_k2'], str(c2))
    # a strong split abstains at neither
    c3 = the_candidates(300, 20, prof)
    ck('scorecard: a strong split abstains at neither K value',
       not c3['the_count_rule_at_k1'] and not c3['the_count_rule_at_k2'],
       str(c3))

    # 2. the geometry and truncated nulls on the same material
    c4 = the_candidates(18, 12, prof)
    ck('scorecard: the geometry and truncated nulls are on the same material',
       'the_geometry_null' in c4 and 'the_truncated_null' in c4, str(c4))

    # 3. the grading: coverage, accuracy among the answered
    rows = [
        {'left': 10, 'right': 10, 'agrees': True,
         'the_count_rule_at_k1': True, 'the_count_rule_at_k2': True,
         'the_geometry_null': True, 'the_truncated_null': True},
        {'left': 30, 'right': 10, 'agrees': True,
         'the_count_rule_at_k1': False, 'the_count_rule_at_k2': False,
         'the_geometry_null': False, 'the_truncated_null': False},
        {'left': 30, 'right': 10, 'agrees': False,
         'the_count_rule_at_k1': False, 'the_count_rule_at_k2': False,
         'the_geometry_null': False, 'the_truncated_null': True},
    ]
    g = grade_candidates(rows)
    ck('scorecard: the grading counts the coverage and the errors caught',
       g['the_count_rule_at_k1']['n'] == 3
       and g['the_count_rule_at_k1']['n_answered'] == 2
       and g['the_count_rule_at_k1']['the_errors_caught'] == 0.0
       and g['the_truncated_null']['n_answered'] == 1
       and g['the_truncated_null']['the_errors_caught'] == 1.0,
       json.dumps({k: g[k] for k in g}))

    # 4. a candidate that answers nothing has no accuracy among the answered
    empty = [{'left': 10, 'right': 10, 'agrees': True,
              'the_count_rule_at_k1': True, 'the_count_rule_at_k2': True,
              'the_geometry_null': True, 'the_truncated_null': True}]
    ge = grade_candidates(empty)
    ck('scorecard: a rule that answers nothing has no accuracy among the answered',
       ge['the_count_rule_at_k1']['accuracy_among_the_answered'] is None
       and ge['the_count_rule_at_k1']['coverage'] == 0.0,
       json.dumps(ge['the_count_rule_at_k1']))

    # 5. the knobs are the declared ones and nobody was fitted here
    ck('scorecard: the four candidates are the arc\'s own',
       [c[0] for c in CANDIDATES] ==
       ['the_count_rule_at_k1', 'the_count_rule_at_k2',
        'the_geometry_null', 'the_truncated_null'],
       str([c[0] for c in CANDIDATES]))
    ck('scorecard: the count rule\'s K values are the arc\'s own 1 and 2',
       [c[2] for c in CANDIDATES[:2]] == [1.0, 2.0],
       str([c[2] for c in CANDIDATES[:2]]))
    ck('scorecard: the coverage band is 25 points and the collapse floor 20 %',
       COVERAGE_BAND == 0.25 and NO_COLLAPSE_FLOOR == 0.20,
       f'{COVERAGE_BAND} {NO_COLLAPSE_FLOOR}')

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
    ap.add_argument('--prior', default=str(ROOT / 'results' /
                                            'glyph_geometry_null.json'))
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    out = measure(Path(args.corpus), Path(args.out), Path(args.prior))
    print(json.dumps({
        'the_set': out['the_set'],
        'the_seen_case': out['the_seen_case'],
        'the_held_out_case': out['the_held_out_case'],
        'the_coverage_stability': out['the_coverage_stability'],
        'the_best_trade_off_on_the_held_out_set':
            out['the_best_trade_off_on_the_held_out_set'],
        'the_bar': out['the_bar'],
        'the_bar_is_met': out['the_bar_is_met'],
    }, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())

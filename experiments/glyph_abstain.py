#!/usr/bin/env python3
"""THE ABSTENTION RULE — when the vocabulary should say it does not know.

    python experiments/glyph_abstain.py --selftest
    python experiments/glyph_abstain.py --out results

THE PUZZLE.  The election fix took the systematic failures from four to
two, and what is left is not a wrong DIRECTION: both of the remaining
failures are the grid reading a near-tie.  The failure diagnosis said
where the failures live -- **the evidence is thin**: three of the four
had under 300 observed cells, against a corpus median of 586, and the
median observed cells of a failure was 26.  A vocabulary that is
confidently wrong about a whole session is worse than one that stays
quiet, and the grid already knows two things about its own confidence:
**how many cells it observed** and **how far its count leaned**.

So the next measurement is not a better answer.  It is a rule for
saying "I do not know", and a measurement of what that rule costs and
what it buys.

THE RULE, AND IT IS TRUTH-BLIND.  It may look at:

    the count margin    -- the grid's own cells: how many of the
                           characteristic cluster's cells fell in each
                           half, and how far apart the counts are
    the observed cells  -- how many cells the session showed at all

and at NOTHING else.  It never consults the truth.  The truth is the
independent full-resolution luma, and it is used only to GRADE, exactly
as in every other study in this lane.

Two rules, and their combination:

    THE COUNT RULE.  A count of n cells split n_left / n_right is a
    binomial proportion, and the proportion's standard error is
    0.5 / sqrt(n).  The z-score for "the halves are equal" is

        z = (n_left - n_right) / sqrt(n_left + n_right)

    and the rule abstains when |z| < K.  K = 2 is a 95 % confidence
    threshold on the count difference, and it is DECLARED HERE, BEFORE
    THE MEASUREMENT, because a rule picked by looking at the truth is
    the cardinality mistake this lane has already made once.

    THE EVIDENCE RULE.  Abstain when the session showed fewer than
    CELLS_MIN observed cells.  CELLS_MIN = 300 is the failure study's
    own published finding -- three of its four failures sat under 300
    observed cells -- and it is a physical statement, not a fit.

    THE COMBINED RULE abstains when either fires.

THE BAR, DECLARED BEFORE THE MEASUREMENT.

  1. In the SELF case, the rule must catch at least HALF of the
     decisive errors while abstaining from at most a QUARTER of the
     decisive right answers.
  2. In the SELF case, the accuracy among the answered must be at
     least 5 points above the accuracy over all the decisive sessions.
  3. In the TRANSFER case, the decisive accuracy among the answered
     must be at least 5 points above the un-abstained decisive
     accuracy.
  4. Teacher dependence 0.000: the rule never consults the truth.

WHAT IS REPORTED ALONGSIDE THE BAR.  The whole curve, for both knobs,
because a rule with a knob has a curve and only one point of it can be
the declared operating point.  The curve is reported, not used to
choose.  And the curve's best point is marked as HINDSIGHT, because
knowing where the curve peaks after the fact is worth having and worth
noting is not the same as having chosen it.

THE COST, STATED UP FRONT.  Abstaining is not free.  Every right
answer the rule throws away is a question the vocabulary no longer
answers, and the corpus's whole argument is that a vocabulary is worth
having.  So the trade is reported as a trade: errors caught against
right answers lost, not as an accuracy alone.

WHAT THIS DOES NOT DO.  It does not make the vocabulary better; it
makes the vocabulary HONEST about the sessions where it is not.  And
it does not touch the transfer's systematic failures at the session
level: a session that EVERY partner reads wrongly is a session whose
room is being read wrongly, and no per-answer rule repairs that.
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

import glyph_grid as gg          # noqa: E402
import glyph_transfer as gt      # noqa: E402

#: The count rule's K: the z-score below which the grid's count does
#: not distinguish the two halves.  DECLARED BEFORE THE MEASUREMENT.
K_COUNT = 2.0

#: The evidence rule's floor: below this many observed cells the grid
#: does not know.  The failure study's own finding: three of its four
#: failures sat under 300 observed cells.
CELLS_MIN = 300

#: The tie threshold, the SAME 1.10 the grid and transfer studies used.
#: One definition, so the three tools are not measuring different
#: things.
TIE_RATIO = gt.TIE_RATIO


# --------------------------------------------------------------------------
# the rule
# --------------------------------------------------------------------------

def count_z(left: int, right: int) -> float:
    """The z-score of the count difference against "the halves are equal".

    A count of n cells split n_left / n_right is a binomial
    proportion; the standard error of the proportion is 0.5 / sqrt(n),
    and the z-score for the null that the halves are equal is
    (n_left - n_right) / sqrt(n).  A TIE gives 0.0."""
    n = left + right
    if n <= 0:
        return 0.0
    return (left - right) / np.sqrt(n)


def abstains(left: int, right: int, n_observed: int,
             k: float = K_COUNT, cells_min: int = CELLS_MIN) -> dict:
    """Does the vocabulary abstain on this answer?  And why."""
    z = count_z(left, right)
    thin_count = abs(z) < k
    thin_evidence = n_observed < cells_min
    return {
        'z': round(float(z), 4),
        'n_observed_cells': int(n_observed),
        'the_count_rule_fires': bool(thin_count),
        'the_evidence_rule_fires': bool(thin_evidence),
        'abstain': bool(thin_count or thin_evidence),
    }


# --------------------------------------------------------------------------
# the measurement
# --------------------------------------------------------------------------

def grade(rows: list[dict], abstain_key: str = 'abstain') -> dict:
    """The trade: what the rule caught, and what it cost."""
    n = len(rows)
    if not n:
        return {'n': 0}
    wrong = [r for r in rows if not r['agrees']]
    right = [r for r in rows if r['agrees']]
    answered = [r for r in rows if not r[abstain_key]]
    caught = [r for r in wrong if r[abstain_key]]
    lost = [r for r in right if r[abstain_key]]
    return {
        'n': n,
        'n_answered': len(answered),
        'coverage': round(len(answered) / n, 4),
        'accuracy_over_all': round(len(right) / n, 4),
        'accuracy_among_the_answered': (round(len([r for r in answered if r['agrees']])
                                                / len(answered), 4)
                                         if answered else None),
        'n_wrong': len(wrong),
        'n_wrong_caught': len(caught),
        'the_errors_caught': round(len(caught) / len(wrong), 4) if wrong else None,
        'n_right': len(right),
        'n_right_lost_to_abstention': len(lost),
        'the_right_answers_lost': round(len(lost) / len(right), 4) if right else None,
    }


def measure(corpus: Path, out_dir: Path) -> dict:
    """The whole study."""
    materials = []
    for d in sorted(p for p in corpus.iterdir() if p.is_dir()):
        m = gt.session_material(d)
        if m is None:
            continue
        materials.append(m)
    print(f'  {len(materials)} usable sessions')

    # the shipped vocabulary: each session's own silhouette-chosen
    # cardinality, the SAME election, so the three tools measure the
    # same thing
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
        n_obs = int(m['observed'].sum())
        dec = abstains(a['left'], a['right'], n_obs)
        self_rows.append({
            'session': m['session'],
            'answer': a['answer'],
            'left': a['left'], 'right': a['right'],
            'truth': m['truth']['half'],
            'truth_ratio': round(m['truth']['ratio'], 3),
            'agrees': a['answer'] == m['truth']['half'],
            'decisive': m['truth']['ratio'] >= TIE_RATIO,
            'n_observed_cells': n_obs,
            'z': dec['z'],
            'the_count_rule_fires': dec['the_count_rule_fires'],
            'the_evidence_rule_fires': dec['the_evidence_rule_fires'],
            'abstain': dec['abstain'],
        })

    # --- the TRANSFER case -------------------------------------------------
    pairs = []
    for i, a in enumerate(models):
        for j, b in enumerate(models):
            if i == j:
                continue
            r = gt.answer_with(a, b, a['characteristic'])
            n_obs = int(b['observed'].sum())
            dec = abstains(r['left'], r['right'], n_obs)
            pairs.append({
                'from': a['session'], 'to': b['session'],
                'answer': r['answer'],
                'left': r['left'], 'right': r['right'],
                'agrees': r['answer'] == b['truth']['half'],
                'decisive': b['truth']['ratio'] >= TIE_RATIO,
                'n_observed_cells': n_obs,
                'z': dec['z'],
                'the_count_rule_fires': dec['the_count_rule_fires'],
                'the_evidence_rule_fires': dec['the_evidence_rule_fires'],
                'abstain': dec['abstain'],
            })
        if (i + 1) % 10 == 0:
            print(f'  ... {i + 1}/{n} alphabets transferred')

    decisive_self = [r for r in self_rows if r['decisive']]
    decisive_pairs = [p for p in pairs if p['decisive']]

    # --- the sweep ---------------------------------------------------------
    # the whole curve, for both knobs, with the DECLARED operating point
    # marked.  The curve is reported, not used to choose.
    def curve(rows: list[dict], key: str) -> list[dict]:
        out = []
        if key == 'k':
            values = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]
        else:
            values = [50, 100, 150, 200, 250, 300, 400, 500, 600, 800]
        for v in values:
            sub = []
            for r in rows:
                if key == 'k':
                    d = abstains(r['left'], r['right'], r['n_observed_cells'],
                                 k=v, cells_min=0)
                else:
                    d = abstains(r['left'], r['right'], r['n_observed_cells'],
                                 k=0.0, cells_min=v)
                sub.append({**r, 'abstain': d['abstain']})
            g = grade(sub)
            out.append({'the_knob': key, 'the_value': v, **g})
        return out

    self_curve_k = curve(decisive_self, 'k')
    self_curve_cells = curve(decisive_self, 'cells')
    pair_curve_k = curve(decisive_pairs, 'k')
    pair_curve_cells = curve(decisive_pairs, 'cells')

    def hindsight(rows: list[dict]) -> dict | None:
        """Where the curve peaks -- marked as HINDSIGHT, not chosen."""
        best = None
        for c in rows:
            acc = c['accuracy_among_the_answered']
            if acc is None:
                continue
            if best is None or acc > best['accuracy_among_the_answered']:
                best = c
        return best

    # the rule as DECLARED: both knobs at their declared values
    declared_self = grade(decisive_self)
    declared_pairs = grade(decisive_pairs)
    # and the same rule over EVERY session and EVERY pair, because the
    # decisive subsets are the truth's decision and two of the
    # vocabulary's remaining systematic failures are ties
    declared_self_all = grade(self_rows)
    declared_pairs_all = grade(pairs)
    count_only_self = grade([{**r, 'abstain': r['the_count_rule_fires']}
                             for r in decisive_self])
    count_only_pairs = grade([{**r, 'abstain': r['the_count_rule_fires']}
                              for r in decisive_pairs])
    evidence_only_self = grade([{**r, 'abstain': r['the_evidence_rule_fires']}
                                 for r in decisive_self])
    evidence_only_pairs = grade([{**r, 'abstain': r['the_evidence_rule_fires']}
                                  for r in decisive_pairs])

    # the failures the rule catches, named
    caught_sessions = [r for r in decisive_self
                       if not r['agrees'] and r['abstain']]
    missed_sessions = [r for r in decisive_self
                       if not r['agrees'] and not r['abstain']]

    # --- the bar -----------------------------------------------------------
    bar = {
        '1_the_rule_catches_half_the_decisive_errors_and_loses_at_most_a_quarter':
            (declared_self['the_errors_caught'] is not None and
             declared_self['the_errors_caught'] >= 0.5 and
             (declared_self['the_right_answers_lost'] or 0.0) <= 0.25),
        '2_the_accuracy_among_the_answered_is_5_points_above_the_accuracy_over_all':
            (declared_self['accuracy_among_the_answered'] is not None and
             declared_self['accuracy_among_the_answered'] -
             declared_self['accuracy_over_all'] >= 0.05),
        '3_the_transfer_decisive_accuracy_among_the_answered_is_5_points_above':
            (declared_pairs['accuracy_among_the_answered'] is not None and
             declared_pairs['accuracy_among_the_answered'] -
             declared_pairs['accuracy_over_all'] >= 0.05),
        '4_teacher_dependence_is_zero': True,
    }

    out = {
        'study': 'the abstention rule',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'the_rule': {
            'the_count_rule': f'abstain when |z| < {K_COUNT}, where '
                              f'z = (n_left - n_right) / sqrt(n_left + n_right)',
            'the_evidence_rule': f'abstain when the session showed fewer than '
                                 f'{CELLS_MIN} observed cells',
            'the_combined_rule': 'abstain when either fires',
            'the_rule_is_truth_blind': True,
            'the_inputs': ['the counts of the characteristic cluster\'s cells '
                           'in each half', 'the number of observed cells'],
            'the_declared_operating_point': {'k': K_COUNT,
                                             'cells_min': CELLS_MIN},
            'the_tie_ratio': TIE_RATIO,
        },
        'the_self_case': {
            'n_sessions': len(self_rows),
            'n_decisive': len(decisive_self),
            'the_declared_rule': declared_self,
            'the_declared_rule_over_all_sessions': declared_self_all,
            'the_count_rule_only': count_only_self,
            'the_evidence_rule_only': evidence_only_self,
            'the_rows': self_rows,
        },
        'the_transfer_case': {
            'n_pairs': len(pairs),
            'n_decisive': len(decisive_pairs),
            'the_declared_rule': declared_pairs,
            'the_declared_rule_over_all_pairs': declared_pairs_all,
            'the_count_rule_only': count_only_pairs,
            'the_evidence_rule_only': evidence_only_pairs,
        },
        'the_sweep': {
            'the_self_case_over_k': self_curve_k,
            'the_self_case_over_cells': self_curve_cells,
            'the_transfer_case_over_k': pair_curve_k,
            'the_transfer_case_over_cells': pair_curve_cells,
            'the_hindsight_best_over_k': hindsight(self_curve_k),
            'the_hindsight_best_over_cells': hindsight(self_curve_cells),
            'the_note': ('the curve is REPORTED, not used to choose: the '
                         'operating point was declared before the '
                         'measurement, because a rule picked by looking at '
                         'the truth is the cardinality mistake this lane '
                         'has already made once. The hindsight best is '
                         'marked as hindsight.'),
        },
        'the_sessions_the_rule_caught': [r['session'] for r in caught_sessions],
        'the_sessions_the_rule_missed': [r['session'] for r in missed_sessions],
        'the_bar': bar,
        'the_bar_is_met': all(bar.values()),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_abstain.json').write_text(json.dumps(out, indent=1))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the z-score
    ck('rule: a tie has no confidence',
       count_z(10, 10) == 0.0, str(count_z(10, 10)))
    ck('rule: a lopsided count has confidence',
       count_z(40, 10) > 3.0, str(count_z(40, 10)))
    ck('rule: a two to one split is a z of about 2.6',
       abs(count_z(40, 20) - 2.582) < 0.01, str(count_z(40, 20)))
    ck('rule: the z-score grows with the count, not just the split',
       count_z(400, 200) > count_z(40, 20))
    ck('rule: an empty answer has no confidence',
       count_z(0, 0) == 0.0)

    # 2. the rule fires on thin evidence and not on thick evidence
    thin = abstains(12, 11, 900)
    ck('rule: a thin count abstains', thin['abstain'] and
       thin['the_count_rule_fires'])
    ck('rule: a thick count does not fire the count rule',
       not abstains(200, 40, 900)['the_count_rule_fires'])
    ck('rule: a thin session fires the evidence rule',
       abstains(200, 40, 100)['the_evidence_rule_fires'])
    ck('rule: a thick session does not fire the evidence rule',
       not abstains(200, 40, 900)['the_evidence_rule_fires'])
    ck('rule: either rule alone abstains',
       abstains(12, 11, 900)['abstain'] and
       abstains(200, 40, 100)['abstain'])

    # 3. the grading: the trade is computed as a trade
    rows = [{'agrees': True, 'abstain': False}] * 8 + \
           [{'agrees': False, 'abstain': True}] * 2 + \
           [{'agrees': True, 'abstain': True}] * 2
    g = grade(rows)
    ck('grade: the coverage is the answered share',
       abs(g['coverage'] - 8 / 12) < 1e-4, str(g['coverage']))
    ck('grade: the accuracy over all counts the abstained-away right ones',
       abs(g['accuracy_over_all'] - 10 / 12) < 1e-4,
       str(g['accuracy_over_all']))
    ck('grade: the accuracy among the answered is the answered ones only',
       abs(g['accuracy_among_the_answered'] - 1.0) < 1e-4,
       str(g['accuracy_among_the_answered']))
    ck('grade: the errors caught is the share of the wrong ones',
       abs(g['the_errors_caught'] - 1.0) < 1e-4)
    ck('grade: the right answers lost is the share of the right ones',
       abs(g['the_right_answers_lost'] - 0.2) < 1e-4, str(g['the_right_answers_lost']))

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
    print(f'glyph abstention: {len([d for d in corpus.iterdir() if d.is_dir()])} sessions')
    out = measure(corpus, Path(args.out))
    print(json.dumps(out['the_self_case']['the_declared_rule'], indent=1))
    print(json.dumps(out['the_transfer_case']['the_declared_rule'], indent=1))
    print(json.dumps(out['the_bar'], indent=1))
    print(f"wrote {Path(args.out) / 'glyph_abstain.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

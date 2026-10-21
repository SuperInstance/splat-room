#!/usr/bin/env python3
"""THE FAILURE DIAGNOSIS — why are three sessions read backwards?

    python experiments/glyph_failure.py --selftest
    python experiments/glyph_failure.py --out results

THE PUZZLE.  The transfer study found that the vocabulary's errors are
SYSTEMATIC rather than random: three of the 43 sessions are answered
backwards by EVERY partner -- 4.8 %, 11.9 % and 19.0 % -- while the
other forty are answered the same way by nearly everyone.  And two of
those three are the grid study's own misses, so the failure belongs to
the VOCABULARY and not to the transfer.

A vocabulary that is confidently wrong about whole sessions is worse
than one that stays quiet, so this asks why.

THE HYPOTHESIS, AND IT IS SHARP.  The characteristic cluster is elected
by CELL COUNT -- the cluster that owns the most cells.  The question
asks which half holds more of the CHARACTERISTIC MATERIAL, and the
truth is which half holds more CHANGE ENERGY.  Those agree only if the
biggest cluster is also the moving one.  **So the prediction is
specific: a session is read backwards exactly when the biggest
cluster's SPATIAL BIAS points the other way from the change energy's
spatial bias.**

That is measurable without any new machinery:

    the cluster's left-fraction   -- how much of the characteristic
                                    material sits in the left half
    the energy's left-fraction    -- how much of the session's change
                                    energy sits in the left half
    the wrong-way margin          -- |cluster - 0.5| - |energy - 0.5|

A NEGATIVE wrong-way margin is a prediction of a backwards answer.

THE FIX THIS POINTS AT.  If the diagnosis holds, the fix is to elect
the characteristic cluster by ACTIVITY rather than by cell count -- the
moving material, not the biggest material.  And that is exactly the
property the activity-gap rule preserves.  So this tool also measures
whether the rule actually repairs the failures it was designed around.
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


def half_fractions(labels: np.ndarray, mask: np.ndarray) -> dict:
    """The left/right split of a set of cells, and of the ENERGY in
    them.  The left half is columns 0..19 of the 40-column grid."""
    flat = labels.reshape(-1)
    sel = mask.reshape(-1) & (flat >= 0)
    if sel.sum() == 0:
        return {'left_fraction': 0.5, 'n_cells': 0}
    left_mask = (np.arange(flat.size) % gg.GRID_W) < (gg.GRID_W // 2)
    n_left = int((sel & left_mask).sum())
    n = int(sel.sum())
    return {'left_fraction': n_left / max(1, n), 'n_cells': n}


def energy_left_fraction(material: dict) -> float:
    """Where the session's change ENERGY sits, from the full-resolution
    luma -- the same truth the question is graded against."""
    raw = np.fromfile(material['luma_path'], dtype=np.uint8)
    n = raw.size // (160 * 96)
    frames = raw[:n * 160 * 96].reshape(n, 96, 160).astype(np.float32)
    d = np.abs(np.diff(frames, axis=0)).sum(axis=0)
    left = float(d[:, :80].sum())
    right = float(d[:, 80:].sum())
    return left / max(1e-9, left + right)


def diagnose_session(material: dict) -> dict | None:
    """The features of one session, and the two vocabularies' answers
    for it."""
    model3 = gt.session_model(material, 3)
    if model3 is None:
        return None
    # the model's characteristic cluster, and where it sits
    labels = model3['train_labels']
    counts = np.bincount(labels.reshape(-1)[
        material['observed'].reshape(-1)], minlength=3)
    biggest = int(np.argmax(counts))
    cluster_mask = (labels == biggest) & material['observed']
    cluster = half_fractions(labels, cluster_mask)

    # the MOST ACTIVE cluster, for the fix
    means = list(model3['cluster_mean_activity'])
    most_active = int(max(range(len(means)), key=lambda c: means[c]))
    active_mask = (labels == most_active) & material['observed']
    active = half_fractions(labels, active_mask)

    energy_left = energy_left_fraction(material)
    cluster_left = cluster['left_fraction']
    # THE SAME-WAY MARGIN.  The grid's answer is the side that holds
    # more of the characteristic cluster; the truth's answer is the
    # side that holds more change energy.  A session is read backwards
    # exactly when those two sides differ, so the margin is the
    # cluster's signed deviation from the centre, signed by the
    # direction the energy points:
    #     positive -> the cluster points the same way as the energy
    #     negative -> it points the other way -> a backwards answer
    direction = 1.0 if energy_left >= 0.5 else -1.0
    same_way = direction * (cluster_left - 0.5)

    return {
        'session': material['session'],
        'n_frames': material['n_frames'],
        'n_observed_cells': material['n_observed_cells'],
        'truth': material['truth']['half'],
        'truth_ratio': round(material['truth']['ratio'], 3),
        'the_energy_left_fraction': round(energy_left, 4),
        'the_biggest_cluster': biggest,
        'the_biggest_cluster_left_fraction': round(cluster_left, 4),
        'the_biggest_cluster_is_the_moving_one': biggest == most_active,
        'the_most_active_cluster': most_active,
        'the_most_active_cluster_left_fraction': round(active['left_fraction'], 4),
        'the_same_way_margin': round(same_way, 4),
        'the_prediction': ('BACKWARDS' if same_way < 0 else 'forward'),
    }


def transfer_rate_for(models: list[dict], target_index: int) -> float:
    """The share of partners that answer this target the way its truth
    says."""
    t = models[target_index]
    hits = 0
    n = 0
    for a in models:
        if a['session'] == t['session']:
            continue
        r = gt.answer_with(a, t, a['characteristic'])
        n += 1
        if r['answer'] == t['truth']['half']:
            hits += 1
    return hits / max(1, n)


def measure(corpus: Path, out_dir: Path) -> dict:
    materials = []
    for d in sorted(corpus.iterdir()):
        if not d.is_dir():
            continue
        m = gt.session_material(d)
        if m is None:
            continue
        # the luma path is needed for the energy split
        m['luma_path'] = d / 'luma.raw'
        materials.append(m)
    if not materials:
        raise SystemExit('no usable sessions')
    print(f'{len(materials)} usable sessions')

    rows = []
    for m in materials:
        d = diagnose_session(m)
        if d is None:
            continue
        rows.append(d)

    # the two vocabularies, and what each partner says about each
    # session
    models3 = [gt.session_model(m, 3) for m in materials]
    models3 = [m for m in models3 if m is not None]
    models_rule = []
    for m in materials:
        pick = gt.choose_k_by_activity_gap(m)
        mm = gt.session_model(m, pick['k']) if pick['k'] is not None else None
        models_rule.append(mm)
    keep = [(a, b) for a, b in zip(models3, models_rule) if a and b]
    models3 = [a for a, _ in keep]
    models_rule = [b for _, b in keep]

    rates3 = []
    rates_rule = []
    for i, m in enumerate(models3):
        r3 = transfer_rate_for(models3, i)
        rr = transfer_rate_for(models_rule, i)
        rates3.append(r3)
        rates_rule.append(rr)

    for row, r3, rr in zip(rows, rates3, rates_rule):
        row['the_transfer_rate_at_k3'] = round(r3, 4)
        row['the_transfer_rate_under_the_activity_gap_rule'] = round(rr, 4)
        # The rate is the share of partners that answered CORRECTLY, so
        # the partners are on the wrong side exactly when it is below
        # one half.  (The first version of this tested the rate against
        # the truth's own side, which inverted the test and produced
        # five false failures -- the sessions it called failures were
        # in fact the ones the partners got RIGHT most often.)
        row['the_partners_are_right'] = (r3 >= 0.5)
        # the sessions that EVERY partner reads the same wrong way
        consistent = (r3 <= 0.10) or (r3 >= 0.90)
        row['the_partners_agree'] = consistent
        row['the_systematic_failure'] = bool(consistent and not row['the_partners_are_right'])

    failures = [r for r in rows if r['the_systematic_failure']]
    others = [r for r in rows if not r['the_systematic_failure']]

    def mean_of(rs, key):
        vals = [r[key] for r in rs if key in r]
        return round(float(np.mean(vals)), 4) if vals else None

    def rule_repairs(r: dict) -> bool:
        """Does the activity-gap rule get this session right?  The rule
        elects the characteristic cluster by activity, so a session the
        cell-count election got backwards is one the rule should
        repair.  The rate is the share of partners answering correctly,
        so the rule repairs it when the rate is above one half."""
        return r['the_transfer_rate_under_the_activity_gap_rule'] >= 0.5

    # THE TEST OF THE HYPOTHESIS: among the sessions whose partners
    # AGREE (consistent), do the ones that are WRONG have a negative
    # wrong-way margin, and the ones that are RIGHT a positive one?
    consistent = [r for r in rows if r['the_partners_agree']]
    right = [r for r in consistent if r['the_partners_are_right']]
    wrong = [r for r in consistent if not r['the_partners_are_right']]

    out = {
        'study': ('the failure diagnosis -- why the vocabulary reads some '
                  'sessions backwards'),
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'method': {
            'the_hypothesis': ('a session is read backwards exactly when the '
                               'biggest cluster\'s spatial bias points the '
                               'other way from the change energy\'s spatial '
                               'bias'),
            'the_same_way_margin': ('the cluster\'s signed deviation from the '
                                  'centre, signed by the direction the energy '
                                  'points; negative predicts a backwards answer'),
            'the_fixer': ('elect the characteristic cluster by ACTIVITY rather '
                          'than by cell count -- the moving material, not the '
                          'biggest material -- which is the property the '
                          'activity-gap rule preserves'),
        },
        'summary': {
            'n_sessions': len(rows),
            'n_where_the_partners_agree': len(consistent),
            'n_systematic_failures': len(failures),
            'the_hypothesis_test': {
                'n_right_and_consistent': len(right),
                'n_wrong_and_consistent': len(wrong),
                'mean_same_way_margin_when_RIGHT': mean_of(right, 'the_same_way_margin'),
                'mean_same_way_margin_when_WRONG': mean_of(wrong, 'the_same_way_margin'),
                'n_wrong_with_a_negative_margin': sum(1 for r in wrong
                                                     if r['the_same_way_margin'] < 0),
                'n_right_with_a_negative_margin': sum(1 for r in right
                                                     if r['the_same_way_margin'] < 0),
                'the_reading': ('if the failures carry the negative margin '
                                'and the successes do not, the hypothesis '
                                'holds and the fix is named'),
            },
            'the_fix': {
                'n_sessions_fixed_by_the_activity_gap_rule': sum(
                    1 for r in failures if rule_repairs(r)),
                'the_failures': [
                    {'session': r['session'],
                     'the_transfer_rate_at_k3': r['the_transfer_rate_at_k3'],
                     'the_transfer_rate_under_the_rule': r['the_transfer_rate_under_the_activity_gap_rule'],
                     'the_same_way_margin': r['the_same_way_margin'],
                     'the_biggest_cluster_left_fraction': r['the_biggest_cluster_left_fraction'],
                     'the_energy_left_fraction': r['the_energy_left_fraction'],
                     'the_biggest_cluster_is_the_moving_one': r['the_biggest_cluster_is_the_moving_one']}
                    for r in failures],
            },
            'the_features': {
                'mean_same_way_margin_all': mean_of(rows, 'the_same_way_margin'),
                'mean_n_observed_cells_failures': mean_of(failures, 'n_observed_cells'),
                'mean_n_observed_cells_others': mean_of(others, 'n_observed_cells'),
                'mean_truth_ratio_failures': mean_of(failures, 'truth_ratio'),
                'mean_truth_ratio_others': mean_of(others, 'truth_ratio'),
            },
            'the_worst_sessions': [
                {'session': r['session'],
                 'the_truth': r['truth'],
                 'the_transfer_rate_at_k3': r['the_transfer_rate_at_k3'],
                 'the_transfer_rate_under_the_rule': r['the_transfer_rate_under_the_activity_gap_rule'],
                 'the_same_way_margin': r['the_same_way_margin'],
                 'the_biggest_cluster_left_fraction': r['the_biggest_cluster_left_fraction'],
                 'the_energy_left_fraction': r['the_energy_left_fraction'],
                 'the_biggest_cluster_is_the_moving_one': r['the_biggest_cluster_is_the_moving_one'],
                 'the_partners_agree': r['the_partners_agree'],
                 'the_systematic_failure': r['the_systematic_failure']}
                for r in sorted(rows, key=lambda r: r['the_transfer_rate_at_k3'])[:6]
            ],
        },
        'sessions': rows,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_failure.json').write_text(json.dumps(out, indent=2))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the half split: a cluster in the left columns must have a
    #    left fraction of 1.0, and one in the right columns 0.0.
    labels = np.zeros((gg.GRID_H, gg.GRID_W), dtype=int)
    labels[:, :20] = 1
    f = half_fractions(labels, labels == 1)
    ck('split: a left-hand cluster has a left fraction of 1.0',
       abs(f['left_fraction'] - 1.0) < 1e-9, str(f))
    labels2 = np.zeros((gg.GRID_H, gg.GRID_W), dtype=int)
    labels2[:, 20:] = 1
    f2 = half_fractions(labels2, labels2 == 1)
    ck('split: a right-hand cluster has a left fraction of 0.0',
       abs(f2['left_fraction'] - 0.0) < 1e-9, str(f2))
    f3 = half_fractions(labels, np.zeros_like(labels, dtype=bool))
    ck('split: an empty cluster does not divide by zero',
       f3['n_cells'] == 0 and f3['left_fraction'] == 0.5, str(f3))

    # 2. the same-way margin.  The energy points right and the cluster
    #    points left -> negative, and a backwards answer is predicted.
    def margin(cluster_left, energy_left):
        direction = 1.0 if energy_left >= 0.5 else -1.0
        return direction * (cluster_left - 0.5)

    m_neg = margin(0.2, 0.8)
    m_pos = margin(0.9, 0.8)
    ck('margin: a cluster pointing the other way scores negative',
       m_neg < 0 and abs(m_neg + 0.3) < 1e-9, str(m_neg))
    ck('margin: a cluster pointing the same way scores positive',
       m_pos > 0 and abs(m_pos - 0.4) < 1e-9, str(m_pos))
    ck('margin: against a LEFT energy, a left cluster scores positive',
       margin(0.1, 0.2) > 0, str(margin(0.1, 0.2)))
    ck('margin: against a LEFT energy, a right cluster scores negative',
       margin(0.9, 0.2) < 0, str(margin(0.9, 0.2)))

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"   [{detail}]" if detail and not ok else ""))
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--corpus', default='/mnt/c/proart_capture/corpus/free_sessions')
    ap.add_argument('--out', default=str(ROOT / 'results'))
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    out = measure(Path(args.corpus), Path(args.out))
    print(json.dumps(out['summary'], indent=2))
    print(f"wrote {Path(args.out) / 'glyph_failure.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

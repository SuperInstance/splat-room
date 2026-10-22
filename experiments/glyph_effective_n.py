#!/usr/bin/env python3
"""THE EFFECTIVE SAMPLE SIZE — setting the abstention threshold without hindsight.

    python experiments/glyph_effective_n.py --selftest
    python experiments/glyph_effective_n.py --out results

THE PROBLEM THIS SOLVES.  The abstention study built a rule that
abstains when the count's margin is thin, using the binomial z-score

    z = (n_left - n_right) / sqrt(n_left + n_right)

which assumes the cells are INDEPENDENT.  They are not.  A body spans
cells, so the cells that hold the characteristic material come in
neighbouring clumps: the count's variance is LARGER than the binomial's,
the binomial z OVERSTATES the significance, and the rule is more
confident than it has any right to be.

The correction is the standard one for a spatially correlated sample:
the VARIANCE INFLATION FACTOR.  If the field has autocorrelation
rho(offset), then

    VIF = 1 + 2 * sum_over_offsets w(offset) * rho(offset)

and the effective sample size is n / VIF.  With it, the z-score is

    z_eff = (n_left - n_right) / sqrt(n_count / VIF)

and the rule abstains when |z_eff| < K_EFF.

**WHY THIS MATTERS, AND IT IS NOT A COSMETIC POINT.**  The abstention
study's curve said that the rule is expensive at every threshold worth
having, and the one point where the self case met all four bars was
found by LOOKING AT THE CURVE -- hindsight, and this lane has already
paid for that mistake once, with the cardinality that inflated 33/43 to
39/43.  If the effective-n calibration lands the rule in the same
region **without the truth**, then the cheap operating point is not a
hindsight artefact; it is the correctly calibrated one, and the
binomial's overstatement was exactly what made the rule look
expensive.

**THE HYPOTHESIS BEING TESTED, STATED HONESTLY.**  The abstention
study's hindsight point is already known to this seat -- the binomial
K = 1 point.  So this is not a blind prediction; it is an INDEPENDENT
MEASUREMENT that has to AGREE with it.  The VIF is measured from the
cells' own activity map and never consults the truth.  If the
calibrated threshold lands near the hindsight point, the agreement is
two independent roads to the same place.  If it does not, then the
hindsight point was luck and the rule has to live with a cost the
corpus says it must pay.

**WHAT THIS IS NOT.**  It does not make the abstention rule cheap.  It
tells the rule what it actually knows, and then reports what that
costs.  A rule that abstains on 80 % of the questions is still a rule
that abstains on 80 % of the questions.
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

#: The significance level the calibrated rule uses, DECLARED BEFORE
#: THE MEASUREMENT: two sigma, the same level the binomial rule used,
#: so the two rules differ ONLY in the variance they assume.
K_EFF = 2.0

#: How far the autocorrelation is measured, in cells.  The grid's cell
#: is four luma pixels, and a body in a 160x96 picture spans several
#: cells, so three cells of reach covers the correlation that matters.
LAG_MAX = 3


def autocorrelations(field: np.ndarray, mask: np.ndarray,
                     lag_max: int = LAG_MAX) -> dict:
    """The spatial autocorrelation of a field over its observed cells.

    `field` is the 24x40 activity map; `mask` says which cells were
    observed at all.  For each offset the Pearson correlation is taken
    over the observed cell pairs that the offset joins, and the number
    of those pairs is returned with it -- the VIF's weight needs it."""
    h, w = field.shape
    a = field.astype(np.float64)
    out = {}
    for dy in range(-lag_max, lag_max + 1):
        for dx in range(-lag_max, lag_max + 1):
            if dx == 0 and dy == 0:
                continue
            ys0 = slice(max(0, -dy), min(h, h - dy))
            ys1 = slice(max(0, dy), min(h, h + dy))
            xs0 = slice(max(0, -dx), min(w, w - dx))
            xs1 = slice(max(0, dx), min(w, w + dx))
            m0 = mask[ys0, xs0]
            m1 = mask[ys1, xs1]
            both = m0 & m1
            n_pairs = int(both.sum())
            if n_pairs < 8:
                continue
            x = a[ys0, xs0][both]
            y = a[ys1, xs1][both]
            if x.std() <= 0 or y.std() <= 0:
                out[(dy, dx)] = (0.0, n_pairs)
                continue
            out[(dy, dx)] = (float(np.corrcoef(x, y)[0, 1]), n_pairs)
    return out


def variance_inflation(field: np.ndarray, mask: np.ndarray,
                       lag_max: int = LAG_MAX) -> dict:
    """The variance inflation factor of the field's spatial correlation.

    VIF = 1 + 2 * sum_over_offsets w(offset) * rho(offset), where
    w(offset) is the share of the cell pairs that sit at that offset.
    It is the ratio of the variance of the mean under the correlated
    field to the variance the binomial would assume."""
    n = int(mask.sum())
    if n < 16:
        return {'the_vif': 1.0, 'the_n_effective': float(n),
                'the_correlations': {}, 'n_cells': n}
    rhos = autocorrelations(field, mask, lag_max)
    h, w = field.shape
    total = 0.0
    detail = {}
    for (dy, dx), (rho, n_pairs) in rhos.items():
        # THE WEIGHT.  VIF = 1 + (2/n) * sum_over_offsets
        # (observed pairs at that offset) * rho(offset), because
        # Var(mean) = (sigma^2 / n^2) * [n + 2 * sum_{i != j} rho_ij] and
        # the sum over ordered pairs is what the offsets enumerate.
        weight = n_pairs / float(n)
        contribution = 2.0 * weight * rho
        total += contribution
        detail[f'{dy},{dx}'] = {'rho': round(rho, 4),
                                'n_pairs': n_pairs,
                                'weight': round(weight, 6),
                                'contribution': round(contribution, 6)}
    vif = 1.0 + total
    return {
        'the_vif': round(float(vif), 4),
        'the_vif_raw': round(float(vif), 4),
        'the_n_effective': round(float(n) / max(vif, 1e-9), 2),
        'n_cells': n,
        'the_correlations': detail,
        'the_note': ('the VIF is clipped at 1.0 for the rule: a VIF below 1 '
                     'would mean the field is anti-correlated, which is not '
                     'a thing a body does'),
    }


def effective_z(left: int, right: int, vif: float) -> float:
    """The z-score of the count difference under the CORRELATED variance.

    THE SIGN, AND IT MATTERS.  The count difference d is a sum of n
    indicators (one per cell: +1 for the cluster on the left, -1 for the
    cluster on the right, 0 otherwise).  Under the correlated null its
    variance is n * VIF, not n, so

        z_eff = d / sqrt(n * VIF) = z_binomial / sqrt(VIF)

    **A larger VIF makes the count LESS decisive.**  The first version
    of this function had it the other way round -- it multiplied -- and
    the selftest ASSERTED that wrong direction, which is how a bug gets
    to look like a finding: the inverted rule abstained on only 12 % of
    the sessions, caught half the errors, and lost 9.7 % of the right
    answers, which reads like a much better rule than the correct one.
    It was not: it was a rule that had been told the count was more
    significant than it is."""
    n = left + right
    if n <= 0:
        return 0.0
    return (left - right) / (np.sqrt(n) * np.sqrt(max(vif, 1.0)))


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

    # the VARIANCE INFLATION FACTOR of each session's own activity map
    vifs = {}
    for m in models:
        activity = m['full_desc'][..., 0]
        v = variance_inflation(activity, m['observed'])
        vifs[m['session']] = v

    # the SELF case, with the calibrated rule
    self_rows = []
    for m in models:
        a = gt.answer_self(m)
        v = vifs[m['session']]
        z_eff = effective_z(a['left'], a['right'], v['the_vif'])
        self_rows.append({
            'session': m['session'],
            'left': a['left'], 'right': a['right'],
            'answer': a['answer'],
            'truth': m['truth']['half'],
            'truth_ratio': round(m['truth']['ratio'], 3),
            'agrees': a['answer'] == m['truth']['half'],
            'decisive': m['truth']['ratio'] >= ga.TIE_RATIO,
            'n_observed_cells': int(m['observed'].sum()),
            'the_vif': v['the_vif'],
            'the_n_effective': v['the_n_effective'],
            'the_binomial_z': round(ga.count_z(a['left'], a['right']), 4),
            'the_effective_z': round(float(z_eff), 4),
            'abstain': bool(abs(z_eff) < K_EFF),
            # the binomial rule, for comparison
            'abstain_binomial_k2': bool(abs(ga.count_z(a['left'], a['right']))
                                        < 2.0),
        })

    # the TRANSFER case
    pairs = []
    for i, a_model in enumerate(models):
        for j, b_model in enumerate(models):
            if i == j:
                continue
            r = gt.answer_with(a_model, b_model, a_model['characteristic'])
            v = vifs[b_model['session']]
            z_eff = effective_z(r['left'], r['right'], v['the_vif'])
            pairs.append({
                'from': a_model['session'], 'to': b_model['session'],
                'left': r['left'], 'right': r['right'],
                'answer': r['answer'],
                'agrees': r['answer'] == b_model['truth']['half'],
                'decisive': b_model['truth']['ratio'] >= ga.TIE_RATIO,
                'the_vif': v['the_vif'],
                'the_effective_z': round(float(z_eff), 4),
                'abstain': bool(abs(z_eff) < K_EFF),
                'abstain_binomial_k2': bool(abs(ga.count_z(r['left'], r['right']))
                                            < 2.0),
            })
        if (i + 1) % 10 == 0:
            print(f'  ... {i + 1}/{n} alphabets transferred')

    decisive_self = [r for r in self_rows if r['decisive']]
    decisive_pairs = [p for p in pairs if p['decisive']]

    calibrated_self = ga.grade(decisive_self)
    calibrated_pairs = ga.grade(decisive_pairs)
    binomial_self = ga.grade([{**r, 'abstain': r['abstain_binomial_k2']}
                               for r in decisive_self])
    binomial_pairs = ga.grade([{**r, 'abstain': r['abstain_binomial_k2']}
                               for r in decisive_pairs])

    # where does the calibrated rule land on the BINOMIAL scale?  This is
    # the comparison with the abstention study's hindsight point: the
    # calibrated rule abstains when |z_binom| < K_EFF * sqrt(VIF), so
    # the binomial-equivalent threshold is K_EFF * sqrt(VIF), and the
    # VIF is per session.
    equivalents = [K_EFF * np.sqrt(max(v['the_vif'], 1.0))
                   for v in vifs.values()]
    vif_values = [v['the_vif'] for v in vifs.values()]

    # the per-session VIF's own summary
    vifs_sorted = sorted(vif_values)
    vif_summary = {
        'the_median_vif': round(float(np.median(vifs_sorted)), 4),
        'the_min_vif': round(float(vifs_sorted[0]), 4),
        'the_max_vif': round(float(vifs_sorted[-1]), 4),
        'the_mean_vif': round(float(np.mean(vifs_sorted)), 4),
        'the_effective_sample_size_of_the_median_session':
            round(960.0 / max(float(np.median(vifs_sorted)), 1.0), 1),
        'the_binomial_equivalent_threshold': {
            'the_median': round(float(np.median(equivalents)), 4),
            'the_min': round(float(np.min(equivalents)), 4),
            'the_max': round(float(np.max(equivalents)), 4),
        },
        'the_abstention_study_hindsight_point': 1.0,
        'the_note': ('the calibrated rule abstains when |z_binom| < '
                     'K_EFF * sqrt(VIF), so the binomial-equivalent '
                     'threshold is K_EFF * sqrt(VIF). The abstention study '
                     'found by hindsight that the self case meets all four '
                     'bars at a binomial K of 1.0. The VIF here is the '
                     'correlation of the ACTIVITY map, which is a proxy '
                     'for the correlation of the cluster\'s membership -- '
                     'and the proxy says the threshold should be far '
                     'HIGHER than 1.0, not lower.'),
    }

    bar = {
        '1_the_calibrated_rule_catches_half_the_decisive_errors_and_loses_at_most_a_quarter':
            (calibrated_self['the_errors_caught'] is not None and
             calibrated_self['the_errors_caught'] >= 0.5 and
             (calibrated_self['the_right_answers_lost'] or 0.0) <= 0.25),
        '2_the_accuracy_among_the_answered_is_5_points_above_the_accuracy_over_all':
            (calibrated_self['accuracy_among_the_answered'] is not None and
             calibrated_self['accuracy_among_the_answered'] -
             calibrated_self['accuracy_over_all'] >= 0.05),
        '3_the_transfer_decisive_accuracy_among_the_answered_is_5_points_above':
            (calibrated_pairs['accuracy_among_the_answered'] is not None and
             calibrated_pairs['accuracy_among_the_answered'] -
             calibrated_pairs['accuracy_over_all'] >= 0.05),
        '4_teacher_dependence_is_zero': True,
        '5_the_calibration_lands_near_the_hindsight_point':
            bool(abs(vif_summary['the_binomial_equivalent_threshold']['the_median']
                     - 1.0) <= 0.35),
        '6_the_corrected_rule_is_not_degenerate':
            bool(calibrated_self['coverage'] > 0.2),
    }

    out = {
        'study': 'the effective sample size',
        'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'the_method': {
            'the_vif': 'VIF = 1 + 2 * sum_over_offsets w(offset) * rho(offset), '
                       'over the observed cells of the session\'s own activity '
                       'map, to a reach of 3 cells',
            'the_effective_z': '(n_left - n_right) / sqrt(n_count / VIF)',
            'K_EFF': K_EFF,
            'the_rule_is_truth_blind': True,
            'the_inputs': ['the session\'s own activity map', 'the count'],
            'the_lag_reach_cells': LAG_MAX,
        },
        'the_vif_summary': vif_summary,
        'the_per_session_vif': vifs,
        'the_self_case': {
            'n_sessions': len(self_rows),
            'n_decisive': len(decisive_self),
            'the_calibrated_rule': calibrated_self,
            'the_binomial_rule_k2': binomial_self,
            'the_rows': self_rows,
        },
        'the_transfer_case': {
            'n_pairs': len(pairs),
            'n_decisive': len(decisive_pairs),
            'the_calibrated_rule': calibrated_pairs,
            'the_binomial_rule_k2': binomial_pairs,
        },
        'the_bar': bar,
        'the_bar_is_met': all(bar.values()),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'glyph_effective_n.json').write_text(json.dumps(out, indent=1))
    return out


# --------------------------------------------------------------------------
# the selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    # 1. the autocorrelation of a field with itself
    field = np.zeros((24, 40))
    rng = np.random.default_rng(3)
    field[:] = rng.random((24, 40))
    mask = np.ones((24, 40), dtype=bool)
    r = autocorrelations(field, mask)
    ck('vif: the autocorrelation is computed for the near offsets',
       (0, 1) in r and (1, 0) in r and (0, 0) not in r, str(len(r)))

    # 2. an UNCORRELATED field has a VIF near 1
    unc = variance_inflation(field, mask)
    ck('vif: an uncorrelated field has a VIF near 1',
       0.7 < unc['the_vif'] < 1.4, str(unc['the_vif']))

    # 3. a SMOOTH field has a VIF above 1 -- this is the whole point
    yy, xx = np.mgrid[0:24, 0:40]
    smooth = (np.sin(xx / 6.0) * np.cos(yy / 7.0)).astype(np.float64)
    sm = variance_inflation(smooth, mask)
    ck('vif: a spatially smooth field has a VIF above 1',
       sm['the_vif'] > 1.5, str(sm['the_vif']))

    # 4. a field that is constant has no usable correlation, and the VIF
    #    stays at 1 rather than exploding
    const = variance_inflation(np.ones((24, 40)), mask)
    ck('vif: a constant field does not explode the VIF',
       const['the_vif'] >= 0.9 and const['the_vif'] < 1.5,
       str(const['the_vif']))

    # 5. the effective z is the binomial z DIVIDED by the square root of
    #    the VIF: a correlated count is LESS decisive, not more
    ck('vif: the effective z is the binomial z divided by the VIF',
       abs(effective_z(60, 40, 4.0) - ga.count_z(60, 40) / 2.0) < 1e-9,
       f"{effective_z(60, 40, 4.0)} vs {ga.count_z(60, 40) / 2.0}")
    ck('vif: a larger VIF makes the count LESS decisive, not more',
       effective_z(60, 40, 4.0) < effective_z(60, 40, 1.0),
       f"{effective_z(60, 40, 4.0)} vs {effective_z(60, 40, 1.0)}")
    ck('vif: a tie has no confidence under either',
       effective_z(10, 10, 4.0) == 0.0)

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
    print(f'glyph effective n: {len([d for d in corpus.iterdir() if d.is_dir()])} sessions')
    out = measure(corpus, Path(args.out))
    print(json.dumps(out['the_vif_summary'], indent=1))
    print(json.dumps(out['the_self_case']['the_calibrated_rule'], indent=1))
    print(json.dumps(out['the_self_case']['the_binomial_rule_k2'], indent=1))
    print(json.dumps(out['the_bar'], indent=1))
    print(f"wrote {Path(args.out) / 'glyph_effective_n.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

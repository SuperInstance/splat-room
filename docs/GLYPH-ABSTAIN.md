# THE ABSTENTION RULE — when the vocabulary should say it does not know

**Tool:** `experiments/glyph_abstain.py` (15/15 selftest green)
**Results:** `results/glyph_abstain.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy, no GPU, no network
**Corpus:** 121 sessions, 47 with a fitted vocabulary, 33 decisive — **a live corpus**: four sessions are newer than the grid study, which saw 43

---

## 0. THE HEADLINE

**The rule that works is the COUNT MARGIN, and the rule the failure
diagnosis suggested — abstain when the evidence is thin — does not work
at all. It catches none of the vocabulary's own remaining failures, and
in the transfer it makes the answer slightly WORSE than not answering.**

| | |
|---|---|
| the declared rule's accuracy among the ANSWERED, self case | **16/16 = 100.0 %**, against 31/33 = 93.9 % over all |
| the declared rule's accuracy among the ANSWERED, transfer | **92.8 %**, against 84.7 % over all |
| decisive errors caught, self case | **2 of 2** |
| decisive errors caught, transfer | **202 of 233 = 86.7 %** |
| right answers lost, self case | **15 of 31 = 48.4 %** — the bar's cost limit was 25 % |
| **bars met** | **3 of 4** — the COST bar failed, and it failed on the cost |

---

## 1. THE PUZZLE

The election fix took the systematic failures from four to two and left
a vocabulary whose remaining errors are not the wrong *direction*. The
failure diagnosis said where the failures live: **the evidence is
thin** — three of its four failures sat under 300 observed cells,
against a corpus median of 586, and the median observed cells of a
failure was 26. The previous note closed with the prediction that the
next measurement is the abstention rule, "because the two failures that
remain are both failures of confidence rather than of direction: the
grid answers on 17 observed cells in the same voice it uses when it is
right."

So this measures a rule for saying **"I do not know"**, and measures
what it costs.

## 2. THE RULE, AND THE BAR, DECLARED BEFORE THE MEASUREMENT

The rule may look at two things, both of them the vocabulary's own:

- **the count margin** — how many of the characteristic cluster's cells
  fell in each half, and how far apart the counts are. A count of `n`
  cells split `n_left` / `n_right` is a binomial proportion, so the
  z-score for "the halves are equal" is
  `z = (n_left - n_right) / sqrt(n_left + n_right)`, and the rule
  abstains when `|z| < K` with **K = 2 declared here, before the
  measurement**, because a rule picked by looking at the truth is the
  cardinality mistake this lane has already made once.
- **the observed cells** — how many cells the session showed at all.
  **CELLS_MIN = 300**, which is the failure diagnosis's own published
  finding, not a fit.

The declared rule abstains when **either** fires.

**The bar, declared before the measurement:**

1. in the self case, catch at least **half** the decisive errors while
   abstaining from at most **a quarter** of the decisive right answers;
2. in the self case, the accuracy among the answered at least **5
   points** above the accuracy over all the decisive sessions;
3. in the transfer case, the decisive accuracy among the answered at
   least **5 points** above the un-abstained decisive accuracy;
4. **teacher dependence 0.000** — the rule never consults the truth.

The whole curve is reported alongside, for both knobs, because a rule
with a knob has a curve and only one point of it can be the declared
operating point. **The curve is reported, not used to choose.**

## 3. THE RESULT

**Self case — 47 sessions, 33 decisive.**

| | coverage | accuracy over all | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|---|
| the declared rule | **48.5 %** | 93.9 % | **100.0 %** | **2 of 2** | **48.4 %** |
| the count rule alone (K = 2) | 63.6 % | 93.9 % | **100.0 %** | **2 of 2** | 32.3 % |
| the evidence rule alone (cells < 300) | 75.8 % | 93.9 % | **92.0 %** | **0 of 2** | 25.8 % |

**Transfer case — 2162 pairs, 1518 decisive.**

| | coverage | accuracy over all | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|---|
| the declared rule | **28.3 %** | 84.7 % | **92.8 %** | **86.7 %** | 69.0 % |
| the count rule alone (K = 2) | 41.0 % | 84.7 % | **95.0 %** | 86.7 % | 53.9 % |
| the evidence rule alone (cells < 300) | 75.8 % | 84.7 % | **84.0 %** | 21.0 % | 24.8 % |

**Bars 2, 3 and 4 are met and bar 1 is not.** The accuracy among the
answered is +6.1 points over all in the self case and +8.1 points in
the transfer. The cost bar failed: the declared rule abstains from
**48.4 %** of the decisive right answers where the bar allowed 25 %.

**And the failure of the cost bar is not a tuning accident — it is the
whole shape of the result.** The declared rule answers only **16 of 33**
decisive sessions and **430 of 1518** decisive pairs. A rule that
reaches 100 % accuracy by answering half the questions is not a
vocabulary any more; it is a filter with a 100 % score.

## 4. THE SIGNAL THAT WORKS, AND THE SIGNAL THAT DOES NOT

Look at the two errors, and look at what each rule says about them:

| session | observed cells | z | truth | the grid said |
|---|---|---|---|---|
| 1792554571 | **583** | −0.94 | LEFT | RIGHT (wrong) |
| 1792596296 | **937** | +0.20 | RIGHT | LEFT (wrong) |

**Both of the vocabulary's own remaining failures have THICK evidence
and a TIED count.** The evidence rule cannot see them — it catches
**none** of them — and in the self case it makes the answer slightly
*worse* than answering everything (92.0 % among the answered against a
93.9 % base rate), because the sessions it throws away were mostly
right. In the transfer the same thing happens and more sharply: the
evidence rule's accuracy among the answered is **84.0 % against a
84.7 % base rate**, which is to say it is **anti-informative** — it
looks like a filter and behaves like a coin.

The count margin sees both of them, and sees them for the right reason:
a near-tied count means the characteristic material does not favour
either half, which is exactly what "I do not know" looks like in a
vocabulary that answers by counting.

**And the prior note's prediction holds where it was made.** The two
remaining *systematic* transfer failures — the sessions every partner
reads wrongly, 1792555166 and 1792555182 — have **17 and 20 observed
cells**, and the rule abstains on **both**, on both rules. But their
truth ratios are **1.082 and 1.094**, under the shared 1.10 tie
threshold, so the truth itself says those sessions are ties and they
sit outside the decisive measurement. The rule catches them; the
decisive numbers cannot show it.

## 5. THE CORRECTION

**The failure diagnosis's "the failures concentrate where the evidence is
thin" was true of the failures it measured and does not survive the
abstention test.** Three of its four failures sat under 300 observed
cells — that was a fact about those four sessions, and it was used to
build a rule that catches **none** of the vocabulary's own two
remaining failures and, in the transfer, is anti-informative.

What is true is narrower and more useful: **the failures are failures of
confidence, and the confidence that matters is the COUNT'S MARGIN, not
the size of the evidence.** A vocabulary that answers by counting cells
is unsure exactly when the counts do not separate the halves. The
failure diagnosis measured the wrong confidence, because the failures it
looked at were thin and thinness was the loud thing about them.

## 6. THE COST, AND THE CURVE

The declared point is too strict, and the curve says so:

| K | coverage (self) | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| 1.0 | 81.8 % | 100.0 % | 2 of 2 | **12.9 %** |
| 1.5 | 69.7 % | 100.0 % | 2 of 2 | 25.8 % |
| **2.0 (declared)** | 63.6 % | 100.0 % | 2 of 2 | 32.3 % |
| 3.0 | 48.5 % | 100.0 % | 2 of 2 | 48.4 % |
| 5.0 | 21.2 % | 100.0 % | 2 of 2 | 77.4 % |

The count rule catches **both errors at every K**, and the accuracy
among the answered is 100 % at every K. What changes with K is only
how much of the vocabulary it throws away.

**At K = 1 the self case would meet all four bars** — 81.8 % coverage,
both errors caught, 12.9 % of the right answers lost, 100 % accuracy
among the answered. **That point is HINDSIGHT and it is not the
declared one**, and it is not shipped: a threshold chosen by looking at
where the curve peaks is the cardinality mistake, and this lane has
already paid for it once. It is recorded because knowing where the
curve peaks after the fact is worth having, and worth noting, is not
the same as having chosen it.

There is also a reason the curve's shape is not a free choice, and it
points at the next measurement: **the cells are not independent.** A
body spans cells, so the true variance of the count difference is
larger than the binomial's, so the binomial z **overstates** the
significance — the rule is more confident than it should be, and should
abstain *more* than it does, not less. The correction factor has not
been measured.

## 7. WHAT IS NOT MEASURED, AND THE NEXT MEASUREMENT

- **The shipped rule does not exist yet.** Its operating point cannot
  be chosen from this run without hindsight. It has to be declared by
  argument and then measured, which means a fresh corpus or a
  held-out split — and the corpus is live, so the four sessions that
  arrived after the grid study are the beginning of one.
- **THE NEXT MEASUREMENT: the effective sample size.** Measure the
  spatial correlation of the cells' own activity — a truth-blind
  quantity — and set the threshold on the EFFECTIVE `n` rather than the
  nominal one. That is a principled reason for a looser K that does
  not consult the truth, and it is the only route to a shipped rule
  that this run does not contaminate.
  **IT HAS BEEN RUN, AND IT REFUTED THE HOPE — see
  `docs/GLYPH-EFFECTIVE-N.md`.** The corpus's activity maps have a
  median variance inflation factor of **44.42**, so the grid's 960
  cells are worth about **22 independent samples**; applying the
  correction in its standard direction makes the rule answer **1
  decisive session of 33**. The reason is not the arithmetic: the
  z-score was never a significance test, because the count is over a
  **blob** and the question is whether the blob sits left or right,
  not whether 960 independent coins came up even. The next measurement
  is therefore **the geometry null** — the session's own cluster
  translated to a random column offset, which is built from the
  session's own material, never consults the truth, and has no knob.
- **One room, one viewpoint.** The margin's relationship to the truth
  is a property of this room's geometry, at 5 px in x and 3 px in y.
- **The systematic failures are not repaired.** The rule stops the
  vocabulary from answering them; it does not make it read them
  rightly. A session every partner reads wrongly is a session whose
  room is being read wrongly.
- **The corpus moved under the other studies.** The grid study ran on
  43 sessions and this one on 47; the grid's decisive accuracy over all
  is 31/33 = 93.9 % here against the filed 29/31 = 93.6 %, with the
  same two misses. The transfer's decisive accuracy over all is
  84.7 % here against the filed 86.3 %.

## 8. THE FILES

| file | what it is |
|---|---|
| `experiments/glyph_abstain.py` | the rule, the bar, the grading, the sweep, the selftest |
| `results/glyph_abstain.json` | every number, including the per-session rows and the whole curve |
| `docs/GLYPH-FAILURE.md` | the failure diagnosis this study corrects |

```
/home/proart/projects/gpu-venv/bin/python experiments/glyph_abstain.py --selftest
/home/proart/projects/gpu-venv/bin/python experiments/glyph_abstain.py --out results
```

Committed for Muse to review; not merged.

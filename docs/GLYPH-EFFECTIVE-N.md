# THE EFFECTIVE SAMPLE SIZE — the correlation correction, and why it destroys the rule

**Tool:** `experiments/glyph_effective_n.py` (7/7 selftest green)
**Results:** `results/glyph_effective_n.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy, no GPU, no network
**Corpus:** the same live corpus the abstention study used — 121 sessions, 47 with a fitted vocabulary, 33 decisive

---

## 0. THE HEADLINE

**The corpus's cells are not independent, and correcting for that
destroys the abstention rule instead of calibrating it.** The grid's
960 cells are worth about **22 independent samples**, so under the
correlated null no count difference is statistically significant — the
corrected rule abstains on **32 of 33** decisive sessions and **1496 of
1518** decisive pairs.

**And the reason is not a bug in the correction. It is that the z-score
was never a significance test.** The grid's count is over a **blob**,
and the physical question is whether the blob sits left or right of the
room's centre, not whether 960 independent coins came up even.

| | |
|---|---|
| the median session's variance inflation factor | **44.42** (min −0.19, max 77.57) |
| the effective sample size of the median session's 960 cells | **21.6** |
| the corrected rule's binomial-equivalent threshold | **13.33** (against the abstention study's hindsight point of 1.0) |
| the corrected rule's coverage, self case | **3.0 %** — one decisive session of 33 |
| the corrected rule's coverage, transfer | **1.5 %** — 22 decisive pairs of 1518 |
| **the hypothesis** | the calibration would land on the abstention study's cheap operating point **without the truth** |
| **the verdict** | **REFUTED** — and the refutation is more useful than the hypothesis was |

---

## 1. THE HYPOTHESIS, AND WHY IT WAS WORTH TESTING

The abstention study's rule abstains when the count's margin is thin,
using the binomial z-score

    z = (n_left - n_right) / sqrt(n_left + n_right)

which assumes the cells are **independent**. They are not: a body spans
cells, so the cells that hold the characteristic material come in
neighbouring clumps. The binomial z therefore **overstates** the
significance, and the textbook correction is the variance inflation
factor — the field's own autocorrelation, measured over the session's
activity map:

    VIF = 1 + 2 * sum_over_offsets w(offset) * rho(offset)
    z_eff = (n_left - n_right) / sqrt(n_count * VIF)

The hope was specific and checkable: the corpus's activity maps are
spatially correlated, the binomial is inflating the significance, and
the corrected threshold should land in the same region as the
abstention study's cheap operating point — **but found by argument
instead of by hindsight**, because the abstention study's cheap point
(binomial K = 1) was found by looking at the curve, and this lane has
already paid for that mistake once, with the cardinality that inflated
33/43 to 39/43.

**This is not a blind prediction and the report says so**: the hindsight
point was already known to this seat. The test is whether an
independent, truth-blind measurement **agrees** with it. It does not.

## 2. WHAT WAS MEASURED: THE CELLS ARE NOT INDEPENDENT

Over the 47 sessions' own activity maps, to a reach of three cells
(twelve luma pixels):

| | |
|---|---|
| the median VIF | **44.42** |
| the mean VIF | 45.16 |
| the smallest | **−0.19** (one session's activity is anti-correlated) |
| the largest | **77.57** |

**A VIF of 44 means the grid's 960 cells are worth about 22 independent
samples.** That is not a rounding error in a statistical nicety: it is
the difference between a grid that has seen the room and a grid that has
seen one body. The corpus's rooms are not speckled — a person walks a
path, and the path is a contiguous stripe of changed cells.

**And this fact is not confined to the abstention rule.** Every
statistic in this lane that treats the grid's cells as independent
inherits it: the transfer study's 1806 pairs are not 1806 independent
observations, the grid's per-cell IoU is not a per-cell quantity, and
the corpus's own margins are wider than a binomial would say. The
abstention rule is simply the first place in this lane where the
assumption had to be priced.

## 3. THE RESULT: THE CORRECTION IS DEGENERATE

With the correction applied in its standard direction — a correlated
count is **less** decisive, so the threshold in binomial terms rises to
`K_EFF * sqrt(VIF)` — the rule abstains on nearly everything:

| | coverage | accuracy over all | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|---|
| the corrected rule, self | **3.0 %** | 93.9 % | 100.0 % | 2 of 2 | **96.8 %** |
| the binomial rule, K = 2 | 63.6 % | 93.9 % | 100.0 % | 2 of 2 | 32.3 % |
| the corrected rule, transfer | **1.5 %** | 84.7 % | 100.0 % | 100 % | **98.3 %** |
| the binomial rule, K = 2 | 41.0 % | 84.7 % | 95.0 % | 86.7 % | 53.9 % |

**Bars 2 and 3 pass vacuously**: the accuracy among the answered is
100 % because one session is answered and it is answered right. A
filter that answers one question in thirty-three does not have a
hundred per cent accuracy; it has a sample of one. Bar 6 — that the
corrected rule is not degenerate — **fails**, and it is the honest
verdict.

**The hypothesis is refuted.** The calibration does not land on the
hindsight point; it lands at a binomial threshold of **13.33** against
the hindsight point of **1.0**, an order of magnitude away, on the
other side.

## 4. WHY: THE Z-SCORE WAS NEVER A SIGNIFICANCE TEST

The correction is right about the arithmetic and wrong about the
question, and the reason is worth stating carefully because it is the
kind of thing that costs a lane a week.

**The binomial model says: 960 independent cells, each with a 50 %
chance of being in the characteristic cluster and in one half.** That
is not the world. The characteristic material is a **blob**. Its cells
are contiguous, its position is a single physical fact, and the count's
imbalance is a function of **where the blob sits** relative to the
room's centre — not of how many independent samples were thrown at the
question.

So the null hypothesis that the binomial encodes ("the cells are
scattered at random") is not the null the count is actually testing.
Under the true null — *the blob is somewhere, and we are asking
whether it favours a half* — the imbalance's scale is set by the
blob's **size and shape**, and the correlation is not a nuisance
parameter to be divided out but the very thing that determines the
answer.

**Which is why the correction inverts the rule rather than calibrating
it.** Dividing by √VIF says "your count is less significant than you
think"; but the count's significance was never the point. The point is
the **direction and the size of the imbalance**, and a lopsided blob is
lopsided whether or not its cells are independent.

**And the measured VIF is the evidence for the right null, not against
it.** A VIF of 44 says the material is a stripe, not a scatter — and
the right way to ask "is this stripe offset?" is to ask what a stripe
of *this shape* would look like at a random position, not what 960
independent coins would look like.

## 5. THE SIGN, AND THE LESSON

The first version of this tool had the correction **inverted**: it
multiplied the binomial z by √VIF instead of dividing by it. The
selftest **asserted the inverted direction** — "a larger VIF makes the
count more decisive" — which is how a bug gets to look like a finding.

**And the inverted rule looked better.** It abstained on 12 % of the
sessions, caught half the errors, and lost 9.7 % of the right answers,
where the correct rule abstains on 97 % of them. By the abstention
study's first bar it was a near-success; the second and third bars
caught it.

**The lesson, and it is a sharp one: a selftest that asserts a
DIRECTION locks the direction in.** The checks that would have caught
this were the ones I did not write — "what does the corrected rule DO
to the abstention rate?" — because a rule that gets more certain as its
evidence gets worse is not a rule, it is a sign error with a good
story. The fleet's own law covers it: **a judge cannot certify
itself**, and here the judge was a test that agreed with the bug.

Both versions' numbers are in this report because the first one is what
a reader would otherwise have found if the tool had shipped.

## 6. WHAT IS NOT MEASURED, AND THE NEXT MEASUREMENT

- **THE NEXT MEASUREMENT: THE GEOMETRY NULL.** The right null is the
  grid's own geometry: take the session's characteristic cluster — its
  actual cells, its actual shape — **translate it by a random column
  offset**, and ask how far the left/right imbalance of a randomly
  placed blob of this shape would sit from the observed one. That null
  is built from the session's own material, it **never consults the
  truth**, and it has **no knob**: the threshold is a quantile of the
  null's own distribution. It is also the measurement the VIF points
  at, because the VIF *is* the blob's spatial extent.
- **The rule still has no shipped operating point.** The abstention
  study's cheap point remains hindsight, the corrected point is
  degenerate, and the geometry null has not been built. The vocabulary
  still answers every session.
- **One room, one viewpoint.** Everything here is this room's geometry,
  at 5 px in x and 3 px in y. A blob's random position on a 40-column
  grid is a different null from a blob's random position in a room with
  furniture.
- **The VIF is measured on the ACTIVITY map**, which is a proxy for the
  correlation of the cluster's membership — the membership is a
  thresholded function of the activity, and the two do not have
  identical correlation structures. The proxy is conservative in the
  direction that matters (the activity is smoother than any threshold
  of it).
- **The corpus moved again.** 121 sessions here; the grid study saw 43
  and the abstention study 47.

## 7. THE FILES

| file | what it is |
|---|---|
| `experiments/glyph_effective_n.py` | the VIF, the corrected z, the selftest that catches the sign |
| `results/glyph_effective_n.json` | every number, including the per-session VIF's and the per-offset correlations |
| `docs/GLYPH-ABSTAIN.md` | the abstention study this one continues |
| `docs/GLYPH-ABSTAIN.md` §7 | the next measurement, as it was named before this one ran |

```
/home/proart/projects/gpu-venv/bin/python experiments/glyph_effective_n.py --selftest
/home/proart/projects/gpu-venv/bin/python experiments/glyph_effective_n.py --out results
```

Committed for Muse to review; not merged.

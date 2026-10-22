# THE HELD-OUT SCORECARD — the arc's four candidates on the sessions that arrived after the arc's last look

**Tool:** `experiments/glyph_holdout_scorecard.py` (9/9 selftest green)
**Results:** `results/glyph_holdout_scorecard.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy only, no GPU, no network
**Corpus:** 139 session directories, 55 with a fitted vocabulary, 41 decisive — of which **8 are held out** from every earlier study in the arc

---

## 0. THE HEADLINE

**The count rule at K = 1 is the only candidate that answers usefully on the held-out set, and it loses NONE of the right answers there.** On the eight sessions that arrived after the arc's last look it answers **7 of 8**, catches the one error, and loses **0 of the 7** right answers. The geometry null answers 2 of 8 and loses 5 of the 7; the truncated null answers **none** and loses all 7.

**All four bars are met.** But the fourth one is contaminated and the declaration says so, so the honest headline is narrower than it looks: **the truth-blind bars (1, 2 and 3) pass cleanly, and the trade-off bar (4) is arithmetic on inputs this analysis had already seen.**

| | |
|---|---|
| the count rule at K = 1 on the held-out 8 | coverage **87.5 %**, errors caught **1 of 1**, right answers lost **0 of 7** |
| the geometry null on the held-out 8 | coverage 25.0 %, errors caught 1 of 1, right answers lost 5 of 7 |
| the truncated null on the held-out 8 | coverage **0 %**, errors caught 1 of 1, right answers lost **7 of 7** |
| coverage stability, the truth-blind bar | the worst candidate moves **13.6 points** between the seen and held-out sets, against a 25-point band |
| **bars met** | **4 of 4** — and bar 4 is contaminated, as declared |

## 1. WHAT THIS CLOSES, AND WHAT IT DOES NOT

The abstention study closed with a checklist item it could not close:

> *The shipped rule does not exist yet. Its operating point cannot be chosen
> from this run without hindsight. It has to be declared by argument and then
> measured, which means a fresh corpus or a held-out split.*

**The corpus has grown, so the held-out split now exists**, and this is the
scorecard over it. The eight sessions are the ones the geometry null study
never saw, and the split is by **arrival**, not by outcome.

What the scorecard establishes: **the count rule's operating point is stable
across the split on every measure that does not consult the truth**, and on
the held-out set it is the only candidate that answers at all usefully.

What it does not establish: **that K = 1 was chosen without hindsight.** Its
provenance is unchanged by this study — it is still the point where the
curve peaked on 33 sessions. The shipping step stays open, and the section
below says what would close it.

## 2. THE CONTAMINATION, AS DECLARED BEFORE THE RUN

**The held-out sessions' counts and their truth labels were already visible in
the truncated null study's per-session rows, because that study filed them.**
So bar 4 — the trade-off — is arithmetic on inputs this analysis has already
seen, and it is **not** a blind confirmation of anything.

Bars 1, 2 and 3 are blind, because **none of them consults the truth**:
coverage is a property of a rule's own inputs, and a collapse is too.

This is the same species of error as the truncated null study's false
freshness caveat, and it is stated in the declaration rather than left to be
noticed. **A caveat written from memory asserts a state of the world, and so
does a bar that quietly relies on what the analyst has already seen.**

## 3. THE SEEN SET, AND A REPRODUCTION

**The scorecard's seen-set numbers are the abstention study's filed sweep,
reproduced exactly.** K = 1 and K = 2 on the 33 seen decisive sessions agree
with `results/glyph_abstain.json` on every field: n, n_answered, coverage,
accuracy over all, accuracy among the answered, errors caught and right
answers lost. So the scorecard is not a new measurement of the seen set; it
is the filed sweep, and the new thing is the held-out set.

**Seen — 33 decisive sessions, 93.94 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the count rule at K = 1 | **81.82 %** (27/33) | 100 % | **100 %** (2/2) | 12.90 % (4/31) |
| the count rule at K = 2 | 63.64 % (21/33) | 100 % | 100 % (2/2) | 32.26 % (10/31) |
| the geometry null | 24.24 % (8/33) | 87.5 % | 50 % (1/2) | 77.42 % (24/31) |
| the truncated null | 6.06 % (2/33) | 100 % | 100 % (2/2) | 93.55 % (29/31) |

**Held-out — 8 decisive sessions, 87.50 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the count rule at K = 1 | **87.50 %** (7/8) | 100 % | **100 %** (1/1) | **0.00 %** (0/7) |
| the count rule at K = 2 | 50.00 % (4/8) | 100 % | 100 % (1/1) | 42.86 % (3/7) |
| the geometry null | 25.00 % (2/8) | 100 % | 100 % (1/1) | 71.43 % (5/7) |
| the truncated null | **0.00 %** (0/8) | — | 100 % (1/1) | 100.00 % (7/7) |

**THE ORDERING IS THE SAME ON BOTH SETS, AND IT IS THE ORDERING THE ARC
HAD.** The count rule is the cheapest of the four and the one that catches
the errors; the geometry null costs 71 % of the right answers for the same
catch; the truncated null costs all of them. On the held-out set the count
rule at K = 1 costs **nothing**.

## 4. THE BARS

| bar | met | the numbers |
|---|---|---|
| 1. the coverage is stable between the seen and the held-out sets | **yes** | the worst movement is **13.64 points** (K = 2), against a 25-point band |
| 2. no candidate collapses on the held-out set | **yes** | nothing that answered 20 % of the seen set falls below 20 % of the held-out one |
| 3. teacher dependence is zero and every knob was declared before its run | **yes** | **0.000**; the count rule at K = 1 and K = 2, the geometry and truncated nulls both at Z_NULL = 1, each fixed before the measurement that used it |
| 4. the best trade-off on the held-out set is 5 points above over all | **yes** | the count rule at K = 1: **100 %** among the answered against **87.50 %** over all, **+12.50 points** — **CONTAMINATED, as declared** |

**Bar 2's scope is worth stating.** The truncated null's seen coverage is
6.06 %, below the 20 % floor, so it is not in scope for bar 2 — it is a rule
that was already too expensive before the held-out set arrived. That is
consistent with the truncated null study's own conclusion and is not a
loophole: the bar asks that a rule which *worked* does not stop working, and
a rule that never worked cannot collapse.

**AND THE COVERAGE STABILITY IS THE BLIND PART, AND IT IS THE PART THAT
CARRIES THE WEIGHT.** Bars 1 and 2 say what can be said without the truth:
the four rules behave on the eight unseen sessions the way they behave on
the thirty-three they were chosen on.

## 5. WHAT WOULD ACTUALLY SHIP THE RULE

**THE THRESHOLD STILL HAS TO BE FIXED BY SOMETHING OTHER THAN THE PEAK OF
THE CURVE.** K = 1's provenance is that it is where the sweep's trade-off
peaked on the 33 sessions the arc had already seen, and no amount of
evidence from the eight does not change that — it only shows the point is
not an artefact of that particular split.

**AND THERE IS A TRUTH-BLIND ROUTE TO A THRESHOLD THAT THE ARC HAD NOT
TOLD ITSELF ABOUT, AND IT IS THE RULE'S OWN COVERAGE.** The count rule's
coverage as a function of K never consults the truth — it is a property of
the counts alone — so a threshold fixed by a **stated coverage contract**
("the vocabulary may decline at most one session in five") is fixed by
argument rather than by a fit to the curve's peak. On the seen 33 the count
rule's coverage runs 81.8 % at K = 1, 69.7 % at K = 1.5, 63.6 % at K = 2,
48.5 % at K = 3 and 21.2 % at K = 5, so the contract's number is what
chooses K, and the contract is a POLICY statement rather than a
measurement.

**THE HONEST CAVEAT ON THAT ROUTE, WHICH IS NOT SMALL.** This session now
knows what K = 1 does on the held-out eight, so a coverage contract written
today is a policy choice informed by a result. **A contract stated without
the count rule's curve and without the held-out numbers — a house rule
about how much of a room a vocabulary may decline to read — would be
innocent, and this session cannot write one.** That is a thing for the
house, not for the analyst, and it is better asked of the house than
manufactured here.

**WHAT THE ARC CAN DO NEXT WITHOUT WAITING FOR THE HOUSE.** The corpus is
live. The protocol that makes the next sessions a test is to **declare the
threshold and the contract now, before the next batch arrives**, and to
treat that batch as the test set. The declaration is the commitment; the
test is the corpus. This study's eight are spent, and the arc should say so
rather than spend them twice.

## 6. THE BARS, THE CONTAMINATION, AND WHAT THE ARC NOW KNOWS

- **No abstention rule has shipped.** Five studies, and now a scorecard over
  the sessions that arrived after the arc's last look, and the count rule at
  K = 1 is still a threshold whose provenance is a curve's peak.
- **But the scorecard does settle a question the arc could not settle
  before: of the arc's four candidates, exactly one answers usefully on
  sessions it was not chosen on, and it is the cheap one.** The geometry
  null and the truncated null both answer, and both pay 71 % and 100 % of
  the right answers for the same catch.
- **And the material is still a field.** The truncated null study's finding
  is unchanged by this one: a field has a balance and no centre, and the
  undecidability was never in the null. What the scorecard adds is the
  price of each null, measured on both sides of a split.
- **One room, one viewpoint.** Every null in this family is a statement
  about this room's geometry at 5 px in x and 3 px in y, and the corpus's
  eight new sessions are the same room and the same viewpoint. **THE NEXT
  MEASUREMENT IS STILL A SECOND ROOM.**

## 7. THE FILES

| file | what it is |
|---|---|
| `experiments/glyph_holdout_scorecard.py` | the four candidates, the split, the bars, the declaration, the contamination, the selftest |
| `results/glyph_holdout_scorecard.json` | every number, including the per-session rows on both sides of the split |
| `docs/GLYPH-TRUNCATED-NULL.md` | the study that produced the held-out set and the contamination this one declares |
| `docs/GLYPH-ABSTAIN.md` | the study whose filed sweep this reproduces exactly |

```
/home/proart/projects/gpu-venv/bin/python experiments/glyph_holdout_scorecard.py --selftest
/home/proart/projects/gpu-venv/bin/python experiments/glyph_holdout_scorecard.py --out results
```

Committed for Muse to review; not merged.

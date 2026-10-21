# THE GLYPH GRID — splat-room stage 1, built and measured

**Tool:** `experiments/glyph_grid.py` (20/20 selftest green)
**Results:** `results/glyph_grid.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy + scipy (`kmeans2`,
`cdist`), no GPU, no network
**Corpus:** 114 session bundles carry a luma file; 26 of them carry **no
frames yet** (live captures, zero-byte luma), so **88 are usable**

> **Dated correction, 2026-10-21 (after `8d10076`).** The corpus line
> above originally read *"88 session bundles with a luma layer"*, which
> was loose: the corpus holds 114 bundles with a luma file, of which 26
> are zero-frame captures still being written. The run scanned all 114
> and recorded 88, so **every number in this report is unchanged** — the
> count of 45 refused is 45 of the 88 *processed*, not of the 114
> present. The line is now precise, and the corpus is live, so it will
> be out of date again by the next run.

---

## 0. THE HEADLINE

**A room fits in 983 characters, and the characters answer a question
about the room that the raw frames answer too — 33 of 43 times, and the
grid is 18,470× smaller than the luma it came from.**

| | |
|---|---|
| the grid | **983 bytes** for a whole session (40×24 + newlines) |
| the source | 18,155,520 bytes of luma at the median session's length |
| **the compression** | **18,470×** |
| bytes per source frame | **0.83** |
| the held-out question, raw agreement with the independent truth | **33/43 (76.7 %)** |
| **over the decisive sessions** | **26/31 (83.9 %)** |
| the grid's margin against the truth's margin | **r = 0.840** |
| the luma's own half-energy ratio, median | **1.173** — the question is a near-tie |
| the negative glyph's IoU against the pixel-level coverage | **0.976** median |
| sessions refused | **45 of 88** — 35 synthetic, 10 too few observed cells |

**And the build caught itself twice, which is the most interesting part
of the table.**

The first version scored **43/43 — perfect** — and the perfect score
*was* the bug: the characters are assigned one per cluster, so counting
characters per half **is** counting cluster labels per half. The two
counts were identical, 162 and 94. A tautology scores 100 %, and that
is the vacuity failure `voxelglyph` names: *"a test named for a property
whose body never touched it."*

The second version scored **39/43** — and that number was inflated too,
because the alphabet's cardinality was chosen by the agreement with the
very truth the answer was judged against. The thing being tested had a
vote in choosing the test. The honest number is the third one:
**33/43**, with the rule that produced it and the rule that would have
been used to cheat both in the report.

---

## 1. WHAT WAS BUILT

### 1.1 The grid

40×24 cells over the corpus's 160×96 luma frames — 4 px per cell on
both axes. **This is the same grid the communicator's `lens.py` already
computes**, so the two programmes agree on the geometry by construction,
and the same 3.0 luma change-map noise floor means the same thing on
both sides (measured: 2.6× the non-zero median change of 1.152, ≈5× the
room's motion-noise σ of 0.61).

### 1.2 The semantic channel is a SHAPE channel

Each cell's descriptor is **activity** (frames changed), **log-change
magnitude**, and **edge gradient** — and deliberately **not brightness**.

That is the acoustic-glyph sweep's lesson applied: the character channel
carries the categorical well (frequency 0.880, velocity 0.888,
intensity 0.747) and the positional badly (`x0` −0.083). A cell's
*identity* is categorical, and its *appearance* is continuous and
already carried by the RGB. Brightness is therefore recorded but not
used to elect the character.

### 1.3 The alphabet is FITTED, per room

k-means over the cell descriptors, with the characters assigned to the
clusters **by the clusters' mean activity**, so the mapping is a
function of the room's own data and not of an arbitrary enumeration.

A fixed vocabulary would be a teacher: someone decided in advance that
`D` means door, and no measurement in this fleet produced that decision.
A fitted alphabet is a clustering, and clustering is a calculator.

The characters come from the ramp `chiaroscuro` already ships, and the
**ink's density tracks the activity**: the least active cluster gets the
sparsest character and the most active gets the densest, with the k
characters spread across the ramp rather than taken from one end. So a
still wall comes out nearly blank and the person comes out dense, and
the reading survives any k.

The example below is session `1792560758` (154.9 s, 942 of 960 cells
observed, k=3, silhouette 0.4751). Its fitted alphabet is
`{'2': ' ', '1': '+', '0': '@'}` — fitted, so the character that means
"the thing that moves" is whatever this room's own clustering earned.
**The dense `@` region in the lower middle is the person.**

```
 ::++ ::::++ +++++  ++ +++++     + +++++
+++++++++++++::+++ +++++++@++++++++++++
+++++++++++++    +  ++++++@+++++++++++++
  ++++ ::++++++++++++++@@@@@@@+++ ++++++
::+++ ++:+   +:+++++@@@@@@@@@@+@++++++++
:: +++ +::   +++  @@@@@@@@@@@@++++++++++
   + ++++    + @@@@@@@@@@@@@@@++++++++++
+++@@++++++++++@@@@@@@@@@@@@@+++++++++++
+++++++++ +++++ @@@@@@@@@@@@@@++++++++++
++ ++++++++++++@@@@@@@@@@@@@@@@+++++++++
+ +++ ++++++  @@@@@@@@@@@@@@@+++++++++++
  ++ +++++++ @@@@@@@@@@@@@@@@+++++++++++
++++++++++++ @@@@@@@@@@@@@@@@@++++++++++
++++++++++++ @@@@@@@@@@@@@@@@@++++++++++
+++++++++ ++@@@@@@@@@@@@@@@@@@++++++++++
++++++ ++++@@@@@@@@@@@@@@@@@@@ +++++++++
++++++++++@@@@@@@@@@@@@@@+@@@@@+++++++++
++++++++++@@@@@@@@@@@@@@@@@@@@@+++++++++
++++++++++@@@@@@@@@@@@@@@@@@@@@++++++ ++
++++++++++@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
+++++++++++@@@@@@@@@@@@@@@@@@@@@@+++@@  
 + ++++++++++@@@@@@@@@@@@@@@@@@+++++   +
+ +++++++++++@@@@@@@@@@@@@@@@@++++++ +++
+++++++++++++@@@@@@@@@@@@@@@@@+++++ ++++
```

### 1.4 The negative space is a character

`:` means **not observed**, and it is **not fitted** — it is a fact about
the capture rather than about the room, so a clustering must not be able
to reassign it. An unobserved cell and an observed wall must not be the
same glyph, or the grid cannot tell a room from a guess.

**And the build broke that rule before it was measured.** The fitted
character pool was the ramp ` .:-=+*#%@` verbatim, and the `:` in it
*is* the negative glyph — so the alphabet duly assigned `:` to a cluster
in **43 of the 43 sessions**, because the third cluster of every alphabet
drew that character. A cell that was observed and a cell that was never
looked at came out as the same character. The rule stated a few lines
above the constant was being broken by the constant. The `:` is out of
the pool now, and a selftest check locks it there.

**The riff's acceptance asked for a stated IoU against the measured
coverage, and the first build never computed one.** It is computed now:
the grid's observed mask against the **pixel-level** coverage — a cell
counts as covered when the majority of its pixels changed above the
noise floor. The two are different computations (the grid pools the
change first and this pools the votes), so the IoU is what the 4×4
pooling costs rather than a tautology.

| | |
|---|---|
| the negative glyph's IoU, median | **0.976** |
| the minimum | **0.25** |
| sessions below 0.9 | **10 of 43** |

The worst cases are the sessions with the fewest observed cells — the
pooling cannot be wrong about a cell it barely saw. The best is 1.000.

### 1.5 The synthetic rig is REFUSED, and the refusal is a decision

**45 of 88 sessions are refused**: 35 because their input device is
synthetic — Chrome's "Fake Default Audio Input" and a static `.y4m`
test pattern — and 10 because too few cells ever changed to fit an
alphabet on (fewer than 17 observed cells; the median session has
586). The check is the device label in each `meta.json`, read
rather than inferred, and it runs **before** the grid is computed, so
the refusal is demonstrably a decision.

**One bug the run exposed:** the refusal's *stated reason* was wrong.
A static test pattern has no change at all, so its observed-cell count
was zero, and it was being refused for "too few observed cells" before
the device check ran. The refusal was right and the reason was not, so
the device is checked first now.

---

## 2. THE MEASUREMENT, AND THE TWO WAYS THE BUILD CERTIFIED ITSELF

### 2.1 The first self-certification: the circular question

The first question was *"which half of the room holds more of the
characteristic material?"* and it scored **43/43**. The counts on both
sides were **identical** — 162 and 94 — because the characters are
assigned one per cluster, so counting characters and counting clusters
are the same arithmetic. **The perfect score was the tell.**

### 2.2 The fix: three holdouts and an independent truth

| | |
|---|---|
| **temporal holdout** | the alphabet is fitted on the **first half** of the session's frames |
| **cell holdout** | the alphabet is fitted on the **even columns**, and every cell is then **PREDICTED** against the fitted centres |
| **the answer** | counted over the **odd columns** — cells the fit never saw |
| **the truth** | the **full-resolution luma's** per-half change energy: a different computation, at 160×96, with no grid and no clustering |

The prediction step was necessary and the first attempt at it was wrong:
fitting on the even columns and then asking about the odd columns gave
the odd columns **no label at all**, so there was nothing to count and
every session came back with no question. A classifier fits on a subset
and then predicts the rest; so does this one.

### 2.3 The second self-certification: the cardinality chosen on the truth

The alphabet's cardinality was chosen by the agreement with the truth,
with ties broken toward the smallest inertia — and the inertia falls as
k rises, so the ties went to the **largest** k. The symptom was visible
in the output: **23 of 43 sessions came home with k=6**, which is what a
shopping trip looks like.

It is the same mistake as the circular question one level up: the thing
being judged gets a vote in choosing the judge.

**The rule now is truth-blind**: the **silhouette** of the training
descriptors — for each cell, how far it sits from its own cluster
compared with the nearest other cluster. It takes no truth argument at
all, and a selftest check asserts that it cannot see one.

| | |
|---|---|
| agreement when k is chosen by the truth (the **optimistic bound**) | **39/43 (90.7 %)** |
| agreement when k is chosen by the silhouette (**the headline**) | **33/43 (76.7 %)** |
| sessions where the two rules pick a **different k** | **37 of 43** |
| the silhouette's choices | k=3 for 33 sessions, k=4 for 9, k=5 for 0, k=6 for 1 |

The selection was worth **six sessions of apparent agreement**. That is
the size of the inflation, measured rather than suspected.

**And the whole per-k curve is recorded, so the reader can see whether
the answer depends on k at all:**

| k | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| agreement with the truth | **33/43** | 31/43 | 33/43 | 31/43 |

The curve is flat to within two sessions. The grid's answer barely
depends on the cardinality, which means the 39/43 was not the grid
knowing more — it was the rule shopping for a lucky k.

### 2.4 The result

| | |
|---|---|
| sessions with a grid | **43** |
| raw agreement with the full-resolution luma | **33/43 (76.7 %)** |
| agreement over the **decisive** sessions | **26/31 (83.9 %)** |
| the luma's half-energy ratio, median | **1.173** (min 1.00, max 2.38) |
| sessions where the truth is a **near-tie** (ratio < 1.10) | **12 of 43** |

**The question is hard by construction, and that is the finding.** The
two halves of this room are nearly equal in change energy — the median
ratio is **1.173** and the minimum is **1.00** — so the grid is being
asked to pick a side out of a near-tie, and 12 of the 43 sessions are
ties outright.

**The ten misses, listed so the reader can judge them:**

| session | grid's count L/R | the luma's truth | the luma's ratio | the grid's count is tied? |
|---|---|---|---|---|
| 1792553152 | 190 / 164 | RIGHT | 1.337 | no |
| 1792553852 | 146 / 28 | RIGHT | 1.322 | no |
| 1792553885 | 133 / 112 | RIGHT | 1.163 | no |
| 1792554097 | 5 / 9 | LEFT | 1.003 | no |
| 1792554309 | 163 / 158 | RIGHT | 1.004 | no |
| 1792554532 | 99 / 157 | LEFT | 1.248 | no |
| 1792555166 | **4 / 4** | LEFT | 1.082 | **yes** |
| 1792555182 | 2 / 3 | LEFT | 1.094 | no |
| 1792555864 | 164 / 163 | RIGHT | 1.036 | no |
| 1792560758 | 137 / 124 | RIGHT | 1.224 | no |

**Five of the ten are near-ties** — the truth's own ratio is 1.003,
1.004, 1.036, 1.082 and 1.094 — and one of them has a grid count of
exactly 4 against 4. Calling those successes or failures would be the
grader's choice rather than the measurement's, so **both numbers are
reported** and the misses are listed. The five decisive misses are
1792553152, 1792553852, 1792553885, 1792554532 and 1792560758.

### 2.5 The margin, which is the better number

The binary answer is the blunt instrument. The **margin** is the sharp
one: how strongly does the grid call it, against how strongly does the
truth?

| | |
|---|---|
| correlation between the grid's count ratio and the truth's ratio | **r = 0.840** |
| the grid's median margin | **1.300** |
| the truth's median margin | **1.173** |
| the grid's median margin when it **agrees** | 1.314 |
| the grid's median margin when it **disagrees** | 1.173 |
| sessions where the grid's own count is exactly tied | **1 of 43** |

So the grid reproduces not just the sign but the *shape* of the truth's
confidence, at a correlation of 0.84 — and when it is wrong it is
usually not very sure, which is the behaviour you want from a
measuring device that does not know it is wrong.

The grid's median margin is **1.300 against the truth's 1.173**, so it
is systematically **more confident than the room is**. That is a real
defect and it is in §5 as a kill.

### 2.6 The vacuous number, reported as vacuous

The grid's characters also agree with the predicted labels **43/43**,
and **that number is worth nothing**: the characters are a bijection
with the clusters, so it is 100 % by construction. It is reported only
to show the pipeline is internally consistent. **The luma number is the
measurement.**

---

## 3. THE RIFF'S OWN ACCEPTANCE, SCORED

The riff was filed on 2026-10-21, before the build, with its acceptance
as numbers. Scored against it:

| the riff's acceptance | verdict |
|---|---|
| the grid is 40×24 and the whole file is **under 1 KB** | **MET** — 983 bytes |
| the alphabet is **fitted**, with a cardinality chosen by an alignment test, and **leave-one-out**: fit on half the cells, read the other half | **MET, with one substitution** — the cardinality is chosen by the silhouette, not by voxelglyph's alignment test; the leave-one-out is the even/odd column split, and the prediction step it needed was missing at first |
| one held-out question, answered from the grid alone, scored against the same question answered from the full-resolution luma | **MET** — 33/43 raw, 26/31 decisive |
| the negative glyph `:` appears, and its cells agree with the measured coverage to a **stated IoU** | **MET** — IoU 0.976 median against the pixel-level coverage. It was **not** met at first, because the IoU was never computed |
| the **synthetic sessions must produce a refusal**, not a grid | **MET** — 35 refused, and the refusal's reason is read from the device, not inferred |

**And the riff's deciding number:** *"if the grid is 1000× smaller and
loses nothing, the semantic splat's sidecar is free. If it loses a lot,
then the sidecar must be an **embedding** after all and idea 1 is
wrong."*

**The verdict: 18,470× smaller, and it does lose.** It loses 10 of 43
answers raw and 5 of 31 on the decisive ones.

But the loss is not random: the margin tracks the truth at r = 0.840,
and the grid is nearly always taking a side rather than guessing. So
the honest statement is not "the sidecar is free" and not "the sidecar
is broken" — it is **the character sidecar carries the room's shape to
a correlation of 0.84 and gets the sign right 77 % of the time on a
question that is itself near-tied 28 % of the time.**

And the fallback does not save idea 1 either, because the acoustic sweep
already says the embedding does not carry position any better
(`x0` −0.083, getting *worse* with resolution). **Neither the character
nor the embedding carries the coordinates.** That is why idea 2 keeps
the coordinates beside the characters, and the grid vindicates it: the
grid is a good *vocabulary* for what the room is doing and a poor
*geometry* for where it is.

---

## 4. WHAT THE GRID IS AND IS NOT

**It is:** a whole session's semantic summary in **983 bytes**, with a
fitted per-room vocabulary, a negative glyph, a device refusal — and it
answers a held-out question about the room that the raw frames answer
too, with a margin that tracks the truth's margin at r = 0.840.

**It is not:**

- **not a map.** It is 40×24 over the image plane. The room map's own
  words: *"this is the room as the camera knows it: an image plane, not
  a floor plan."*
- **not a position.** The grid says what is where *in the picture*, and
  the acoustic sweep is the standing evidence that position is the one
  thing a character channel does not carry.
- **not verified.** **No referee exists** (teacher-dependence 1.000),
  so the 76.7 % is a self-measurement against an independent truth, not
  a certification. The truth is independent; the grader is still us.
- **not free.** It is 18,470× smaller than the luma and it loses a
  quarter of the answers.
- **not the splat field.** It is stage 1. Stage 2 is where the
  densification budget gets allocated from it.

---

## 5. WHAT KILLS IT

1. **The tautology kill, which already fired once.** If the question is
   answered from the same labels the alphabet was fitted on, the
   agreement is 100 % and means nothing. The holdouts and the
   independent truth are what stop it, and they are in the code.
2. **The selection kill, which also already fired once.** If the
   cardinality is chosen by the number it is later judged on, the number
   is a shopping trip. It was worth six sessions: 39/43 against the
   honest 33/43. The truth-blind silhouette is what stops it, and the
   whole per-k curve is recorded so the effect stays visible.
3. **The near-tie kill.** If the truth's own ratio is near 1.00, the
   question cannot discriminate and the agreement number is measuring
   the tie-break. **12 of 43 sessions are in that state today.**
4. **The overconfidence kill.** The grid's median margin is **1.300**
   against the truth's **1.173** — it calls a near-tie more decisively
   than the room does. A vocabulary that overstates its own certainty is
   worse than one that stays quiet, and this one does not stay quiet.
5. **The one-room kill.** The alphabet is fitted per room. On the second
   room, is the fit stable? A vocabulary that only works on the cells it
   was fitted on is a caption, not a language.
6. **The synthetic kill.** 35 of 88 sessions are not rooms, and 10 more
   never changed enough to fit. A build that does not filter by device
   fits its vocabulary to a test pattern.
7. **The no-parallax kill.** The camera did not move — 5 px in x across
   50 sessions — so the grid is image-space, and a metric room needs a
   moving seat.

---

## 6. THE NEXT MEASUREMENT

**One number: the same question on a SECOND room.**

The corpus has one room. The grid's vocabulary is per room, and the
acceptance criterion my own riff named was *"a vocabulary that only
works on the cells it was fitted on is a caption, not a language."* The
leave-one-out inside a room is already done — the even/odd column
split, the first/second half of the frames. **The across-room test is
not, and it is a half-day capture.**

And when the second room exists, two things become answerable at once:
the fit's **cardinality** can be settled — the silhouette rule is
implemented but the right number of symbols is a question about
alignment, not about brightness — and the **overconfidence** can be
measured across rooms instead of inferred from one.

A second measurement is available today and is worth its cost: the
grid's **margin** is a better instrument than its sign, and the
correlation of 0.840 was measured on a question that is near-tied in 12
of 43 sessions. A question with a larger truth ratio would separate
the honest 77 % from the lucky 77 %.

---

## 7. HOW TO REPRODUCE

```sh
# the selftest: 20 checks
python experiments/glyph_grid.py --selftest

# the measurement over the corpus
python experiments/glyph_grid.py --out results
```

The run writes `results/glyph_grid.json`, which carries every session's
grid, its fitted alphabet, its fit scope, its question, its counts, the
**whole per-k curve**, the optimistic bound, and the refusal reason for
the ones that were refused.

*Committed for Muse to review; not merged.*

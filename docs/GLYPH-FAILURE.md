# THE FAILURE DIAGNOSIS — why the vocabulary reads some sessions backwards

**Tool:** `experiments/glyph_failure.py` (7/7 selftest green)
**Results:** `results/glyph_failure.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy + scipy, no GPU, no network
**Corpus:** the same 43 usable sessions the glyph grid and transfer studies used

---

## 0. THE HEADLINE

**The vocabulary's failures are not one thing, and only ONE of the four
is a defect. Three are the vocabulary reading a near-tie, and the
fourth is a real inversion that a one-line change would fix.**

| | |
|---|---|
| sessions | **43** |
| sessions where every partner gives the same answer | **22** |
| **systematic failures** — every partner agrees, and they are wrong | **4** |
| of those 4, how many have **fewer than 300 observed cells** | **3** (and only 10 of 43 sessions are that thin) |
| of those 4, how many have a **truth ratio under 1.10** (a near-tie) | **3** (and 12 of 43 overall) |
| the median observed cells of a failure vs the corpus | **26 vs 586** |
| **genuine inversions** — a decisive session, well observed, read backwards | **1** (1792554532) |

---

## 1. THE PUZZLE

The transfer study found that the vocabulary's errors are **systematic
rather than random**: some sessions are answered the same way by
nearly every partner, and some of those are answered the same wrong
way. The grid study missed the same sessions. So the failure belongs
to the **vocabulary**, not to the transfer, and a vocabulary that is
confidently wrong about whole sessions is worse than one that stays
quiet.

This asks why.

---

## 2. THE HYPOTHESIS, AND IT IS SHARP

The characteristic cluster is elected by **cell count** — the cluster
that owns the most cells. The question asks which half holds more of
the characteristic material, and the truth is which half holds more
**change energy**. Those agree only if the biggest cluster is also the
moving one.

**So the prediction is specific: a session is read backwards exactly
when the biggest cluster's spatial bias points the other way from the
change energy's spatial bias.**

Both are measurable without any new machinery:

| | |
|---|---|
| the cluster's left-fraction | how much of the characteristic material sits in the left half |
| the energy's left-fraction | how much of the session's change energy sits in the left half, from the full-resolution luma |
| **the same-way margin** | the cluster's signed deviation from the centre, signed by the direction the energy points |

A **negative** same-way margin predicts a backwards answer.

---

## 3. THE RESULT

### 3.1 The hypothesis has directional power, and is not a law

| | sessions | mean same-way margin |
|---|---|---|
| the partners agree and are **right** | **18** | **+0.1674** |
| the partners agree and are **wrong** | **4** | **−0.1298** |

**The mean margin flips sign between the two groups**, which is what
the hypothesis predicts. But it is not a law: **2 of the 4 failures
carry a negative margin and 3 of the 18 successes do too.** The margin
is a direction, not a verdict.

### 3.2 The four failures, one at a time

| session | observed cells | truth ratio | the partners' rate | the same-way margin | the biggest cluster L | the MOST ACTIVE cluster L | the energy L |
|---|---|---|---|---|---|---|---|
| 1792554532 | 857 | 1.248 | **4.8 %** | **−0.2337** | 0.266 | **0.594** | 0.555 |
| 1792554097 | 32 | 1.003 | 7.1 % | −0.3148 | 0.185 | 0.185 | 0.501 |
| 1792555166 | 17 | 1.082 | 9.5 % | +0.0294 | 0.529 | 0.529 | 0.520 |
| 1792555182 | 20 | 1.094 | 9.5 % | 0.0000 | 0.500 | 0.500 | 0.522 |

**Three mechanisms, and only one of them is a defect.**

**The two ties (1792555166 and 1792555182) are not failures at all.**
With 17 and 20 observed cells out of 960, and truth ratios of 1.082 and
1.094, the grid's own counts were **4 against 4** and **2 against 3** —
the grid has no opinion and the truth has no opinion either. Their
margins are +0.03 and exactly 0.00, which is what "no opinion" looks
like. These are coin flips that landed wrong.

**1792554097 is the same thing with a bigger margin.** 32 observed
cells, a truth ratio of **1.003** — the two halves differ by three
parts in a thousand — and the energy's own left-fraction is 0.501,
which is the centre to three decimals. The margin is large because
the grid's cluster is small and lopsided, not because the truth is
clear.

**1792554532 IS a genuine defect, and it is one line of code.** It has
**857 observed cells** and a truth ratio of **1.248** — a decisive
question, well observed — and it is read backwards by 95 % of its
partners. Its biggest cluster sits at **L 0.266** while the change
energy sits at **L 0.555**. And its **most active** cluster sits at
**L 0.594**, right beside the energy. **So the biggest material and
the moving material are different things here, and electing the
characteristic cluster by ACTIVITY instead of by CELL COUNT would
turn this session round.**

### 3.3 The shape of the failures

| | failures | the rest |
|---|---|---|
| median observed cells | **26** | 586 |
| mean truth ratio | 1.107 | 1.269 |

**The failures concentrate exactly where the evidence is thin.** Three
of the four have fewer than 300 observed cells, and only 10 of the 43
sessions are that thin — so a third of the thin sessions fail while
the other 33 sessions are all read correctly or read consistently
wrong for other reasons.

**So the vocabulary's real weakness is not blindness. It is that it
has nothing to say when almost nothing moved**, and it says it anyway:
at 17 observed cells the grid produces a confident-looking answer
about a room whose two halves differ by 8 %.

### 3.4 The activity-gap rule repairs NONE of them

**0 of the 4.** The rule that the cardinality sweep produced changes
the number of symbols; these failures are not about the number of
symbols. For three of the four the biggest cluster **is** already the
moving one (the rule's premise holds), and the fourth's fix is a
different change entirely — the election, not the cardinality.

**That is a clean negative result and it is worth having:** the
cardinality rule and the failure are unrelated, and a reader who
assumed the new rule would carry the fix would be wrong.

---

## 4. WHAT THIS CHANGES

- **The one-line fix, named before it is measured.** Elect the
  characteristic cluster by **activity** rather than by cell count:
  the moving material, not the biggest material. On the corpus it
  would turn round the single genuine inversion, and it would leave
  the two ties alone — because a tie has no answer to turn.

  > **Dated note, later on 2026-10-21: the fix is MEASURED (§8) and my
  > prediction was HALF WRONG.** It does **not** turn 1792554532 round:
  > that session goes from 4.8 % to **28.6 %** — better, and still
  > wrong. It does **not** leave the ties alone: 1792555166 and
  > 1792555182 get slightly worse. **But it is a large aggregate win
  > anyway** — the decisive transfer rises from 79.3 % to **86.3 %** and
  > the grid's own decisive agreement from 22/31 to **29/31**. The fix
  > was worth shipping and the prediction about *which session* it
  > would rescue was wrong.
- **The vocabulary should be able to ABSTAIN.** At 17 observed cells
  the grid says something with the same confidence as it says at 957.
  A vocabulary that reports its evidence — the number of observed
  cells, the margin between its two halves — beside its answer would
  let a consumer see which of its answers are worth having. **The
  grid's answer and its evidence are in the same artifact already**;
  what is missing is a rule for saying "I do not know".
- **The near-tie is a property of the ROOM, not of the vocabulary.**
  12 of 43 sessions have a truth ratio under 1.10, and the two halves
  of this room are nearly equal in change energy most of the time.
  No vocabulary fixes that, and no vocabulary should pretend to.

---

## 5. WHAT KILLS IT

1. **The one-room kill.** One room, one viewpoint, one camera. Every
   failure diagnosis here is a diagnosis of *this* room's structure.
2. **The question kill.** The question is a left/right split. A
   vocabulary's failure modes on "which third moved most" would be
   different, and possibly worse.
3. **The election kill.** The fix is named but **not measured** — it
   is a one-line change that has not been run, so it is a hypothesis,
   not a result.
4. **The four-sessions kill.** Four failures is four data points. The
   split into three mechanisms is suggestive, not established, and one
   of the four (1792554532) carries the entire claim.

---

## 6. THE NEXT MEASUREMENT

**One number: does electing the characteristic cluster by activity fix
1792554532 without breaking the other 42?**

It is a one-line change to `held_out_question`, it is measurable
today, and it is the natural next build. If the fix turns round the
one genuine inversion and leaves the rest alone, the vocabulary's
error rate on this corpus drops from 4 sessions to 3 — and, more
importantly, the remaining three are all demonstrable ties.

**And the abstention rule, which is worth more.** The grid knows how
many cells it observed and how close its two halves are. A rule that
says "the answer is LEFT, and it is based on 17 cells with a 4-4
count" is a better product than an answer that looks the same whether
it rests on 17 cells or 957.

---

## 7. HOW TO REPRODUCE

```sh
# the selftest: 7 checks
python experiments/glyph_failure.py --selftest

# the diagnosis over the corpus
python experiments/glyph_failure.py --out results
```

The run writes `results/glyph_failure.json`, which carries every
session's features, its transfer rates under both vocabularies, its
same-way margin, and the verdict on each.

---

## 8. THE FIX, MEASURED — and the prediction was half wrong

**The election was measured. It is a large win, it shipped, and it did
not do what I said it would do.**

### 8.1 The measurement

The same alphabets, the same sessions, the same truth. **Only the
election changes**: the characteristic cluster is the one that MOVES
instead of the one that owns the most cells.

| | the cell-count election | **the activity election** |
|---|---|---|
| the transfer, all pairs | 1,372/1,806 (76.0 %) | **1,420/1,806 (78.6 %)** |
| **the transfer, decisive** | 1,032/1,302 (79.3 %) | **1,123/1,302 (86.3 %)** |
| the self case, decisive | 22/31 (71.0 %) | **29/31 (93.5 %)** |
| sessions whose election changed | — | **19 of 43** |
| sessions that improved / worsened / unchanged | — | **20 / 16 / 7** |
| the grid's decisive misses | 5 | **2** |

**The election changed for 19 of 43 sessions, and the aggregate moved
+6.99 points on the decisive transfer.** Some sessions went to 1.000
from 0.691. One crossed the other way (0.857 → 0.548).

### 8.2 The prediction was wrong, and here is exactly how

**I wrote:** *"On the corpus it would turn round the single genuine
inversion, and it would leave the two ties alone."*

**What happened:** 1792554532 went from **4.8 % to 28.6 %** — better,
and still wrong. The two ties got *worse*, not better (0.095 → 0.071
and 0.095 → 0.048). **So both clauses were wrong.**

**But the fix was still worth shipping**, and the reason is the thing I
did not predict: **the election changes what a session's PARTNERS
count, so it improves the vocabulary as a whole, and it cannot rescue
a single session that its partners read wrongly.** The failure lives in
the source's cluster landing in the wrong place inside the target — and
a fix to the target's own election cannot touch that.

**And the failure set is better than the prediction claimed:**

| | cell-count election | **activity election** |
|---|---|---|
| systematic failures (consistent and wrong) | 4 | **2** |
| of those, the genuine inversions | 1 | **0** |
| of those, the near-ties with almost no observed cells | 3 | **2** |

**The two that remain are 1792555166 (17 observed cells, truth ratio
1.082, grid count 0-1) and 1792555182 (20 observed cells, ratio 1.094,
grid count 2-2).** Both are the grid answering a question it has no
evidence for, on a truth that has no answer either.

### 8.3 What this costs

**The overconfidence got worse.** The grid's median margin rises from
1.300 to **1.360** while the truth's is 1.173. The revised vocabulary
is more confident than the room is, by more than it was. The likely
cause is the election itself: **a cluster elected by a MEAN activity is
elected by a quantity that a handful of very active cells can
dominate**, and the same is true of the margin, which is a ratio of
counts.

### 8.4 The next measurement, which is now the abstention rule

**The two remaining failures are both failures of CONFIDENCE, not of
direction.** The grid's count is 0-1 and 2-2; the truth's ratio is
1.082 and 1.094. Neither side has an answer, and the grid answers
anyway, in the same voice it uses when it is right.

**So the rule worth shipping next is not another election. It is an
abstention:** a grid that reported its evidence beside its answer — the
number of observed cells, the margin between its two halves — would let
a consumer see which of its answers are worth having. **The grid
already knows both numbers.** What is missing is a rule for saying
"I do not know", and the two failures above are exactly the sessions
where it should say it.

*Committed for Muse to review; not merged.*

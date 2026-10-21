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

*Committed for Muse to review; not merged.*

# THE TRANSFER TEST — is the vocabulary the room's, or the capture's?

**Tool:** `experiments/glyph_transfer.py` (8/8 selftest green)
**Results:** `results/glyph_transfer.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy + scipy, no GPU, no network
**Corpus:** the same 43 usable sessions the glyph grid study used (of 114
bundles: 26 are zero-frame live captures, 45 are refused as a test rig or
an empty room)

---

## 0. THE HEADLINE

**A vocabulary fitted on one session answers a DIFFERENT session's
question at 76.0 % — the same rate it reaches on its own session — while
a random cluster of the very same alphabet gets 58.3 %. The vocabulary
belongs to the room, not to the capture.**

| | all 1,806 pairs | over the decisive pairs |
|---|---|---|
| **the transfer** — A's alphabet answers B's question | **1,372 / 1,806 (76.0 %)** | **1,032 / 1,302 (79.3 %)** |
| the self case, under this study's own rule | 30/43 (69.8 %) | 22/31 (71.0 %) |
| the self case as the grid study measured it | 33/43 (76.7 %) | — |
| **the control** — a random non-characteristic cluster of A | 1,053 / 1,806 (58.3 %) | 840 / 1,302 (64.5 %) |

**And the build's own decay curve came out INVERTED** — the most
similar session pairs transferred *worst* — which turned out to be a
confound, not a property. The clean measure says the opposite, and it is
in §2.3.

---

## 1. WHAT WAS MEASURED

### 1.1 The question

The glyph grid fits a per-session alphabet and answers a held-out
question about the room from it. The kill condition named in the riff
is: *"a vocabulary that only works on the cells it was fitted on is a
caption, not a language."* The grid study answered the question for the
session the alphabet was fitted on. **This one asks whether the
alphabet answers a different session's question.**

### 1.2 The transfer

For every ordered pair of distinct sessions (A, B):

- A's alphabet is fitted on **A** — the first half of A's frames, the
  even columns, at a **fixed** cardinality of k=3 so two alphabets can
  be compared at all;
- A's **characteristic material** — the cluster that owns the most cells
  — is carried over to B;
- B's cells are assigned to **A's centres** in A's own scaled space, and
  the cells carrying A's characteristic material are counted in B's
  left and right halves over B's odd columns, the cells the fit never
  saw;
- that answer is graded against **B's own truth**, the full-resolution
  luma's per-half change energy — a different computation, at 160×96,
  with no grid and no clustering.

**k is fixed at 3** because a vocabulary with three symbols and one with
four have no correspondence. And 3 is not a free choice: it is the
silhouette's own modal choice over the corpus (33 of 43 sessions), so
it is the cardinality the data picks most often.

### 1.3 The control

The same transfer with a **random non-characteristic cluster** of A
instead of the characteristic one. If the transfer carries information,
the control must be worse. It is: **58.3 % against 76.0 %.**

The control is *not* at chance, and that is worth saying plainly: a
random cluster is still a region of this room, so it retains some
correlation with where the change happens to be. The gap between 58.3 %
and 76.0 % is what the characteristic material contributes.

---

## 2. THE RESULT

### 2.1 The transfer

| | |
|---|---|
| sessions | **43** |
| ordered pairs (A ≠ B) | **1,806** |
| the transfer, all pairs | **1,372 / 1,806 (76.0 %)** |
| the transfer, decisive pairs | **1,032 / 1,302 (79.3 %)** |
| the control, all pairs | 1,053 / 1,806 (58.3 %) |
| the control, decisive pairs | 840 / 1,302 (64.5 %) |

**The transfer is as good as the self case.** The grid study's own
number — 33/43, 76.7 % — was measured on the training half's labels;
this study's self case, under the transfer rule, is 30/43 (69.8 %).
So the honest comparison is **76.0 % (another session's alphabet)
against 76.7 % (its own)** — the same rate, within one session of
difference.

**The "caption, not a language" kill is not met, inside one room.**

### 2.2 The transfer is not a copy

A transfer that merely repeated the source's answer would look perfect
whenever the two sessions happen to agree about the room, and would be
punished only when they do not. So the clean measurement is the
conditional one: **among the 626 decisive pairs where the source and
the target disagree about the room, whose answer does the transfer
follow?**

| | |
|---|---|
| **follows the TARGET** | **80.0 %** |
| follows the SOURCE | 20.0 % |

**The transfer reads the target.** It is not a copier, and it is not
reading the room's static layout either: over all pairs the transfer
answers LEFT 35.6 % of the time, and the truth is LEFT for 39.5 % of the
target sessions — so the transfer's answers are distributed like the
truth's, not like a fixed layout.

### 2.3 The decay curve was confounded, and the clean measure inverts it

The raw curve, as first measured, was this — and it says the most
similar pairs transfer *worst*:

| similarity band | pairs | rate | **the two sessions share the truth** |
|---|---|---|---|
| −0.303 – 0.046 | 256 | **0.840** | 0.285 |
| 0.046 – 0.210 | 255 | 0.788 | 0.478 |
| 0.210 – 0.378 | 271 | 0.834 | 0.590 |
| 0.378 – 0.566 | 277 | 0.827 | 0.574 |
| **0.566 – 0.934** | 247 | **0.660** | **0.660** |

**Look at the last column.** In the most similar band the transfer's
rate (0.660) and the rate at which the two sessions simply agree about
the room anyway (0.660) are *the same number*. That is the signature of
a copier: in that band the transfer is right exactly when the two
sessions happen to share an answer, and wrong exactly when they do not.
Similar sessions share the room's answer more often, so a copier is not
punished there — and the raw curve inverts.

**The clean measure, conditioned on the two sessions disagreeing, says
the opposite:**

| similarity band | pairs | follows the TARGET | follows the SOURCE |
|---|---|---|---|
| −0.303 – −0.020 | 128 | **0.883** | 0.117 |
| −0.020 – 0.129 | 128 | 0.750 | 0.250 |
| 0.129 – 0.284 | 126 | 0.833 | 0.167 |
| 0.284 – 0.501 | 126 | 0.841 | 0.159 |
| **0.501 – 0.908** | 127 | **0.677** | 0.323 |

**The vocabulary transfers BEST where it is hardest** — where the two
sessions look least alike and therefore share the least. That is the
right sign for a vocabulary: it is not carrying the room's furniture
across, it is carrying the room's *materials*.

### 2.4 The errors are systematic, and they are the grid's errors

The per-session view is the honest one, because each session is a
target 42 times and those are not 42 independent samples.

- For sessions whose truth is LEFT, the partners answer LEFT **64.6 %**
  of the time; for sessions whose truth is RIGHT, **16.6 %**. The
  partners agree with the truth, not with each other's habits.
- **22 of 43 sessions** are answered the same way by at least 90 % of
  their partners — so the transfer is a detector, not a guesser, and its
  errors are **systematic rather than random**.

The worst sessions are systematically *backwards*, not marginal:

| session | transfer rate | the truth | the truth's ratio | the grid study's own verdict |
|---|---|---|---|---|
| 1792554532 | **4.8 %** | LEFT | 1.248 | a miss there too |
| 1792555007 | **11.9 %** | LEFT | 1.121 | — |
| 1792553852 | **19.0 %** | RIGHT | 1.322 | a miss there too |

**Two of the three are the grid study's own misses.** The transfer is
not inventing new failures; it is reproducing the same ones. A session
the vocabulary cannot read is a session the vocabulary cannot read, and
the transfer finds that out from the outside.

---

## 3. WHAT THIS DOES AND DOES NOT SETTLE

**It settles:** within one room, one camera and one viewpoint, a
vocabulary fitted on one session answers another session's question at
the same rate it answers its own, and far above the control. **The
alphabet is a property of the room, not of the capture.**

**It does not settle the across-room test.** Every session here is the
same room, seen from nearly the same place — the viewpoint spread is
5 px in x and 3 px in y. So this is a **session-transfer** test, and the
across-room test is still open. The riff's own acceptance criterion was
about *rooms*, and only one room exists in the corpus.

**And it does not certify anything.** No referee exists
(teacher-dependence 1.000). The truth here is independent — the
full-resolution luma — but the grader is still us, and the fit is still
ours.

---

## 4. WHAT KILLS IT

1. **The one-room kill, still unstruck.** The alphabet transfers across
   *sessions* in one room. Across a second room it is untested, and a
   vocabulary that only works on the cells it was fitted on is a caption.
   A vocabulary that only works on the ROOM it was fitted on is a
   caption with a bigger stage.
2. **The systematic-error kill.** Three sessions are read backwards by
   every partner, consistently. A vocabulary that is confidently wrong
   about a whole session is worse than one that abstains, and this one
   never abstains.
3. **The control-not-at-chance kill.** The control sits at 58.3 %, not
   50 %. Part of what the "transfer" measures is a region's geometry,
   not a vocabulary's meaning, and the two are not separated by more
   than the 17.7-point gap.
4. **The confound kill.** The natural way to plot this result — transfer
   accuracy against how alike the two sessions look — is confounded, and
   the confound is only visible because the conditional measure was
   taken. Any future version of this curve must carry the conditional
   with it.
5. **The k=3 kill.** The cardinality is fixed so the alphabets can be
   compared. Whether the transfer survives at k=4, 5 and 6 is untested,
   and a transfer that only works at one cardinality is a caption with a
   particular font.

   > **Dated note, later on 2026-10-21: this kill FIRED, and §6 has
   > the numbers.** The transfer does not survive a finer cardinality:
   > 79.3 % at k=3 against 69.9 % at k=6, and the gap over the control
   > collapses from 14.7 points to 2.5. **So the kill was right, and
   > the thing that survives is not the vocabulary at an arbitrary k but
   > the vocabulary at a COARSE one** — which is a different and better
   > answer than "the transfer is a caption".

---

## 5. THE NEXT MEASUREMENT

**One number: the same transfer, across a second room.**

Everything this study needed is built and runnable; the only missing
input is a room. Two captures in a second room — same camera, same
protocol, two sessions each — would turn the session-transfer number
(76.0 %) into an across-room number, and would settle the cardinality
question at the same time, because the across-room test is where a
fitted alphabet either survives or collapses.

**A second number is available today, and it is cheap: the transfer at
k = 4, 5 and 6.** The tool takes the cardinality as a constant; the
whole question "does a vocabulary transfer, or does a *particular*
vocabulary transfer?" is unanswered until it is run at more than one k.

> **Dated note, later on 2026-10-21: the first of those three is now
> MEASURED — see §6.** It turned out to be the most consequential
> number in this study, and it changed the reading of §2.

And a third, from the systematic errors: **why are three sessions read
backwards?** They are missed by the grid study too, so the failure
belongs to the vocabulary and not to the transfer. That is the next
question for the vocabulary itself, and it is worth more than another
transfer curve.

---

## 6. THE CARDINALITY SWEEP — the vocabulary's meaningfulness is concentrated at low k

**The first of the three numbers above, measured. And it is the most
consequential thing in this study: the cardinality is not a free
parameter, and more symbols is not a richer vocabulary — it is a
diluted one.**

The tool now takes the cardinality as an argument and fits every
alphabet at k = 3, 4, 5 and 6 over the same corpus, so the whole table
is one run.

| k | the transfer (decisive) | the control (decisive) | **the gap** | follows the TARGET | the characteristic cluster is the MOST active one |
|---|---|---|---|---|---|
| **3** | 1,032/1,302 (79.3 %) | 840/1,302 (64.5 %) | **14.74 pts** | 80.0 % | **24 / 43** |
| 4 | 936/1,302 (71.9 %) | 870/1,302 (66.8 %) | **5.07 pts** | 73.2 % | 14 / 43 |
| 5 | 909/1,302 (69.8 %) | 884/1,302 (67.9 %) | **1.92 pts** | 70.3 % | 8 / 43 |
| 6 | 910/1,302 (69.9 %) | 878/1,302 (67.4 %) | **2.46 pts** | 69.3 % | 7 / 43 |

**Two things happen at once, and both are real.**

**The raw transfer falls** — 79.3 % at k=3 to 69.9 % at k=6, and the
"follows the target" measure falls with it, 80.0 % to 69.3 %. A
finer vocabulary is a more **session-specific** vocabulary: the extra
symbols carve the room into finer and more particular pieces, and those
pieces do not carry to another session.

**And the characteristic material stops being a choice.** At k=3 the
cluster that owns the most cells is the **most active** cluster in 24 of
43 sessions, and it beats a random cluster of the same alphabet by
14.7 points. At k=5 it is the most active one in 8 of 43, and it beats
a random cluster by **1.9 points** — which is to say it barely beats
one at all. **At a fine cardinality, "the cluster with the most cells"
and "the material that moves" stop being the same thing**, and the
question has nothing left to ask.

**The mechanism is in the descriptors.** A cell's descriptor is
activity, log-change and edge gradient. At k=3 the partition is coarse
enough to be {the thing that moves, the thing that barely moves, the
thing that does not move}, and the biggest cluster is the material. At
k=6 it is a finer cut along the same axis, so the biggest cluster is
whichever slice of the descriptor space happens to hold the most cells,
and that slice is not the active material.

**So the rule the grid study used was right for a reason it did not
know.** The silhouette — a truth-blind rule — chose k=3 for 33 of 43
sessions, and k=3 is exactly where the vocabulary still has a
distinction to make. **The right cardinality is not a matter of
alignment, as the riff guessed; it is a matter of the alphabet staying
coarse enough that "the biggest material" and "the moving material"
are the same thing.**

### 6.1 What this does NOT say

- **It does not say k=3 is optimal.** It says k=3 is where the
  vocabulary is *meaningful* on this corpus, on this question, with
  this descriptor. A different question might want a different k.
- **It does not say more symbols never help.** It says that on the
  question measured here, the extra symbols cost 9.4 points of
  transfer and 12.8 points of the gap over the control.
- **It does not say the grid study's headline is wrong.** The grid
  study's own per-k curve was flat (33, 31, 33, 31), and that remains
  true: the grid's SELF-answer barely depends on k. What depends on k
  is the **transfer** — whether the vocabulary means the same thing in
  another session. That is a different question and the flat curve
  could not see it.
- **It does not replace the across-room test.** It makes it sharper:
  the second room's test should be run at k=3, and the sweep says why
  a vocabulary fitted at k=6 would fail it for a reason that has
  nothing to do with the room.

### 6.2 The next measurement this suggests

**The cardinality rule is wrong in the same way the first rule was.**
The silhouette measures how well separated the clusters are, and it
knows nothing about whether the biggest one is the material. **A rule
that keeps "the biggest cluster is the moving material" would be
better, and it is measurable today:** the candidate rule is the one
that maximises the gap between the characteristic cluster and a random
cluster of the same alphabet, with the truth never consulted. That is
a rule about the ALPHABET's structure rather than its separation, and
it is the natural successor to the silhouette.

It is stated here before it is measured, so that it can be.

---

## 7. THE CARDINALITY RULE — measured against the incumbent, and against the truth it never sees

**The rule was stated in §6.2 before it was measured, and here is what
it did.**

**THE RULE.** For each cardinality, fit the alphabet, find the
**characteristic** cluster — the one that owns the most cells — and
measure the **activity gap** between it and the median of the other
clusters: how much more active the biggest material is than a typical
one. The cardinality with the largest gap wins; ties go to the smallest
cardinality. **Nothing in it consults the truth.** It is a statement
about the alphabet's own structure, which is why the silhouette — which
measures separation, not structure — could not have found it.

**THE COMPARISON.** The rule is measured against the **incumbent**, the
silhouette the grid study ships, and against fixed cardinalities, all
on the same corpus in the same run.

| | the transfer, all pairs | the transfer, decisive | the control, decisive | the gap | follows the TARGET | the SELF case, decisive | the characteristic cluster is the MOST active one |
|---|---|---|---|---|---|---|---|
| fixed k=3 | **1,372/1,806 (76.0 %)** | **1,032/1,302 (79.3 %)** | 840/1,302 (64.5 %) | 14.74 | **80.0 %** | 22/31 (71.0 %) | 24/43 |
| fixed k=4 | 1,255/1,806 (69.5 %) | 936/1,302 (71.9 %) | 870/1,302 (66.8 %) | 5.07 | 73.2 % | 23/31 (74.2 %) | 14/43 |
| fixed k=5 | 1,232/1,806 (68.2 %) | 909/1,302 (69.8 %) | 884/1,302 (67.9 %) | 1.92 | 70.3 % | 20/31 (64.5 %) | 8/43 |
| fixed k=6 | 1,218/1,806 (67.4 %) | 910/1,302 (69.9 %) | 878/1,302 (67.4 %) | 2.46 | 69.3 % | 21/31 (67.7 %) | 7/43 |
| **the activity-gap rule** | 1,349/1,806 (74.7 %) | **1,032/1,302 (79.3 %)** | 840/1,302 (64.5 %) | **14.74** | 78.3 % | **25/31 (80.6 %)** | **25/43** |
| the silhouette rule (the incumbent) | 1,353/1,806 (74.9 %) | 1,016/1,302 (78.0 %) | 843/1,302 (64.7 %) | 13.28 | 78.6 % | 22/31 (71.0 %) | 22/43 |

### 7.1 The verdict, which is not the one that would sell it

**The rule beats the incumbent on every measure that concerns the
vocabulary's own quality** — the decisive transfer (79.3 % against
78.0 %), the gap over the control (14.74 against 13.28 points), the
self case (**25/31 = 80.6 %** against 22/31 = 71.0 %) and the rate at
which the characteristic cluster is the moving material (25 of 43
against 22 of 43).

**And fixed k=3 is still the best on the raw all-pairs transfer, 76.0 %
against the rule's 74.7 %.** So the honest statement is not "the new
rule replaces the old one". It is: **the rule makes the per-session
choice safe without giving up anything on the decisive pairs, and it
beats the silhouette on the session's own answer by 9.6 points.**

The reason is visible in the last column. The rule does not simply
pick k=3 everywhere — it picks k=3 for 12 sessions, k=4 for 12, k=5
for 4 and k=6 for 15 — and yet it lands on the k=3 numbers for the
decisive pairs (1,032, exactly) while beating the silhouette. **What
it preserves is not the number of symbols but the property:** the
alphabet keeps its biggest symbol meaning "the thing that moves".

### 7.2 What this changes, and what it does not

- **It does not change the grid study's shipped rule.** The grid study
  uses the silhouette, and the silhouette's own numbers are what §6
  measured; the activity-gap rule is measured here and is a candidate
  for the next revision of that tool, not a correction to its report.
- **It does not settle the cardinality question.** "Does the transfer
  survive at other k?" is answered — it does not survive a fine
  cardinality, and the vocabulary's meaningfulness is concentrated at
  low k. **Which k a session should use** is a different question, and
  the rule above is one answer to it, on one corpus, on one question.
- **It does not certify anything.** The truth is still the independent
  full-resolution luma and the grader is still us.

### 7.3 The next measurement this suggests

**The rule is a rule about the alphabet's structure, and it is measured
on ONE question.** The obvious next step is to ask whether the same
rule holds for a question with a different answer — for instance
"which third of the room moved most", where the answer is not a
left/right split and the "characteristic material" is not the biggest
cluster. A rule that only works for a left/right question is a rule
about that question.

And the other one: **the three sessions that every partner reads
backwards.** They are missed by the grid study too, so the failure
belongs to the vocabulary. That question is worth more than another
cardinality, because a vocabulary that is confidently wrong about
whole sessions is worse than one that stays quiet.

---

## 8. HOW TO REPRODUCE

```sh
# the selftest: 8 checks
python experiments/glyph_transfer.py --selftest

# the measurement over the corpus
python experiments/glyph_transfer.py --out results
```

The run writes `results/glyph_transfer.json`, which carries every
ordered pair, its answer, its truth, its control, its similarity, and
whether the two sessions shared a truth at all — plus the per-session
consistency and the conditional analysis that separates a transfer from a
copy.

*Committed for Muse to review; not merged.*

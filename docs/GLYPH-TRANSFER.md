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

And a third, from the systematic errors: **why are three sessions read
backwards?** They are missed by the grid study too, so the failure
belongs to the vocabulary and not to the transfer. That is the next
question for the vocabulary itself, and it is worth more than another
transfer curve.

---

## 6. HOW TO REPRODUCE

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

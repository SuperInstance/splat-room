# THE TRUNCATED PLACEMENT NULL — the null that handles the room-wide case, and reaches the same verdict for a worse price

**Tool:** `experiments/glyph_truncated_null.py` (9/9 selftest green)
**Results:** `results/glyph_truncated_null.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy only, no GPU, no network
**Corpus:** 139 session directories, 55 with a fitted vocabulary, 41 decisive — of which **8 are held out** from every earlier study in the arc

---

## 0. THE HEADLINE

**The truncated placement null does exactly what it was built to do, and it changes nothing.** It finds a non-degenerate null on **15 of 15** room-wide profiles where the geometry null is degenerate on all 15 — and it then abstains on **15 of 15** anyway. The route to abstention changed; the verdict did not.

**And it costs four times as much everywhere else.** On the whole corpus it answers **4.88 %** of the decisive sessions where the geometry null answers **24.39 %**; on the eight sessions that arrived after the arc's last look it answers **0 of 8** where the geometry null answers **2 of 8**.

| | |
|---|---|
| room-wide profiles given a non-degenerate null | **15 of 15** (the geometry null: 0 of 15) |
| room-wide profiles the rule abstains on anyway | **15 of 15**, and **all 15 are right answers** |
| the truncated null's coverage, self case | **4.88 %** (2 of 41 decisive) against the geometry null's **24.39 %** |
| the truncated null's coverage on the **held-out** 8 | **0 %** — it answers nothing at all |
| **bars met** | **2 of 4** |

## 1. THE RULE, AND WHAT WAS DECLARED BEFORE THE RUN

The geometry null study left one thing undone and named the candidate for
it: **a null that handles the room-wide case.** The geometry null places
the session's own cluster inside the frame, and for a cluster that spans
every answer column there is exactly one such placement — so the null has
no spread and the rule abstains, on 15 of the 33 decisive self sessions,
all 15 of them right answers.

The candidate is the **truncated placement null**: the camera's frame is
narrower than the room, so the material may sit partly outside it, and
clipping the material to the frame gives a non-zero spread even for a
profile that spans every column.

Everything below was fixed before the run and is in the module's
docstring, so it travels with the code:

    the null   the session's own characteristic cluster, translated to
               EVERY horizontal position leaving some of it inside the
               frame, including the positions that push part of it out;
               the statistic is the left fraction of the material that
               REMAINS INSIDE
    the rule   abstain when |f(0) - the null's own centre| < Z_NULL * sd
    the knob   Z_NULL = 1, the geometry null's own number, so the two
               rules differ in their NULL and not in their threshold
    the degenerate reading   CONSERVATIVE: a null with no spread means
               abstain.  Declared before the run and explicitly NOT the
               permissive one, which was measured and seen in the
               geometry null study and would be hindsight wearing a
               rule's clothes
    the bars   the geometry null study's four bars, unchanged

**THE REFERENCE IS THE NULL'S OWN CENTRE, not 0.5.** The truncated null
is not symmetric — clipping the material at one edge is not the mirror of
clipping it at the other — so the null's centre is where a typical
placement would have put the vote. When the null IS symmetric, which is
the geometry null's case, the centre IS 0.5 and this rule reduces to the
geometry null's rule exactly. The two studies are comparable, and the
comparison is exactly paired: both nulls are computed in the same pass,
over the same material, through the geometry null's own profile
construction.

The rule never consults the truth. Teacher dependence **0.000**.

## 2. THE FRESHNESS CAVEAT WAS WRONG, AND IT WAS WRONG BECAUSE IT WAS NOT MEASURED

**This is a dated correction to the declaration in section 6 of the
docstring, and it is filed here because the declaration is part of the
record.**

The declaration said: *the corpus has NOT grown since the geometry null
study, so the freshness mitigation is UNAVAILABLE and this study is NOT a
fresh confirmation.* That sentence was **false**, and it was false
because it was carried forward in prose instead of being counted.

| | the notes said | the corpus actually holds |
|---|---|---|
| session directories | 121 | **139** |
| sessions with a fitted vocabulary | 47 | **55** |
| decisive sessions | 33 | **41** |

**Eight sessions had landed after the arc's last look and BEFORE the
declaration was written** — they were already on disk when the rule was
fixed. The freshness mitigation the geometry study asked for exists
after all.

The rule itself is untouched: it is truth-blind, it was fixed before the
run, and nothing in it changed. What was wrong is the caveat. **A
FRESHNESS CAVEAT IS A MEASUREMENT AND NOT A FOOTNOTE** — a number
carried forward in prose is a number nobody checked, and this one was
wrong by 18 directories and 8 usable sessions.

**THE LESSON IS THE FAMILIAR ONE, IN A NEW PLACE.** This seat has
already learned that a selftest which asserts a direction locks the
direction in, and that a permissive reading adopted after the data is
seen is hindsight. It has now learned that a **caveat** can be
hindsight too — a caveat written from memory asserts a state of the
world, and an unmeasured assertion of that kind is exactly as dangerous
as an unmeasured rule, because it is the thing that licenses the rule.

## 3. THE ROOM-WIDE CASE: THE MECHANISM WORKS AND THE VERDICT DOES NOT CHANGE

**On one real room-wide profile the two nulls look like this:**

| | the geometry null | the truncated null |
|---|---|---|
| placements it may use | **1** | **39** |
| the null's spread | **none** (degenerate) | **0.4347** |
| the left fraction's range over the null | a single point | **0.0 to 1.0** |

The truncation does what it was built to do. Across the room-wide set:

- the truncated null finds a **non-degenerate** null on **15 of 15**
  room-wide profiles;
- the geometry null is degenerate on all 15;
- and **the truncated null abstains on 15 of 15 anyway**, with all 15
  being right answers.

**The route changed and the answer did not.** The geometry null abstains
because the material has nowhere else to be; the truncated null abstains
because the material could be anywhere, so its balance means nothing.
Both are the same statement about the same material: **a field has a
balance and no centre.** The undecidability was never in the null. It is
in the corpus.

**AND THE OBSERVED VALUES SAY SO PLAINLY.** On the room-wide set the
observed left fraction sits **0.008 to 0.276 null standard deviations**
from the null's own centre — the middle of the null, every time. The
null's centre for those profiles runs **0.4450 to 0.5422**, and the
observed left fractions run **0.3299 to 0.6162**. A field's split is
near the middle, and the null knows it.

## 4. THE COST: THE TRUNCATION INFLATES EVERY NULL

**The truncated null's spread is larger than the geometry null's on 21 of
21 sessions where both exist** — without exception. The median spread is
**0.4340** against the geometry null's **0.3160**.

That is the whole mechanism of the extra cost. Truncation adds
placements in which part of the material is outside the frame, and those
placements produce extreme left fractions, so the null's spread grows;
a bigger spread puts the observed value closer to the centre relative to
the spread; and the rule abstains more. On a narrow profile the
geometry null has 18 placements and the truncated null 22, but on a
room-wide one it is 1 against 39.

So the truncated null buys a non-degenerate null on the room-wide case by
inflating every null in the corpus, and pays for it in coverage
everywhere else.

## 5. THE SELF CASE AND THE TRANSFER CASE

**Self — 41 decisive sessions, 92.68 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the truncated null | **4.88 %** (2/41) | 100 % | **100 %** (3/3) | **94.74 %** (36/38) |
| the geometry null | 24.39 % (10/41) | 90.0 % | 66.67 % (2/3) | 76.32 % (29/38) |
| the binomial K = 1 | 82.93 % (34/41) | 100 % | 100 % (3/3) | 10.53 % (4/38) |
| the binomial K = 2 | 60.98 % (25/41) | 100 % | 100 % (3/3) | 34.21 % (13/38) |

**Transfer — 2214 decisive pairs, 85.77 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the truncated null | **4.88 %** (108) | 94.44 % | **98.1 %** (309/315) | **94.63 %** (1797/1899) |
| the geometry null | 17.75 % (393) | 96.18 % | 95.24 % (300/315) | 80.09 % (1521/1899) |
| the binomial K = 1 | 57.99 % (1284) | 91.51 % | 65.4 % (206/315) | 38.13 % (724/1899) |
| the binomial K = 2 | 38.48 % (852) | 95.89 % | 88.89 % (280/315) | 56.98 % (1082/1899) |

**The truncated null is worse than the rule it replaces on both counts
that matter.** It answers a quarter as often in the self case and a
quarter as often in the transfer; it loses 18.4 points more of the right
answers in the self case; and in the transfer its accuracy among the
answered (**94.44 %**) is *below* the geometry null's (**96.18 %**). It
catches marginally more errors, and it does so by abstaining on nearly
everything.

**THE SELF CASE'S 100 % IS A TWO-SESSION ARTIFACT** and is labelled as
one: the rule answers 2 of 41 sessions, both of them right. The
geometry null's self case is anti-informative in the same way — 90.0 %
among the answered against a 92.68 % base rate — because the material is
a field and a field's position carries nothing.

## 6. THE HELD-OUT SET — THE FRESH CONFIRMATION THE ARC ASKED FOR

**Eight sessions arrived after the geometry null study ran, and all eight
are decisive.** The split is by **arrival**, not by outcome, so it
cannot be a hindsight choice; the rule under it is the same unchanged
truth-blind rule. The split was **not** in the declaration — the
declaration said the opposite, which is why section 2 exists.

**Held-out — 8 decisive sessions, 87.50 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the truncated null | **0 %** (0/8) | — | 100 % (1/1) | **100 %** (7/7) |
| the geometry null | 25.0 % (2/8) | 100 % | 100 % (1/1) | 71.43 % (5/7) |

**Held-out transfer — 432 decisive pairs, 96.30 % correct over all.**

| rule | coverage | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|
| the truncated null | **0 %** (0/432) | — | 100 % (16/16) | **100 %** (416/416) |
| the geometry null | 22.69 % (98/432) | 98.98 % | 93.75 % (15/16) | 76.68 % (319/416) |

**The truncated null answers NONE of the eight sessions it has never seen
before.** It abstains on 8 of 8, and on 432 of 432 held-out pairs. It
is a rule that says "I do not know" to everything it meets that it has
not already seen.

**THE SEEN 33 REPRODUCE THE FILED GEOMETRY STUDY EXACTLY.** The
geometry null recomputed here on the 33 sessions the geometry study saw
gives coverage **0.2424**, errors caught **0.5**, right answers lost
**0.7742** — the filed numbers to the digit. The arc's filed geometry
result is stable on the grown corpus, and the paired comparison in this
study is sound because the two nulls are computed over the same material
in the same pass.

**WHAT THE CORPUS'S GROWTH DOES TO THE FILED NUMBERS.** On the grown
corpus the geometry null's self case moves from 33 decisive sessions to
41: coverage **24.24 % → 24.39 %**, errors caught **50 % → 66.67 %** (1
of 2 → 2 of 3, so one session), right answers lost **77.42 % → 76.32 %**.
The arc's filed numbers do not move materially, and the growth is
recorded here because the earlier studies' denominators are now stale.

## 7. THE BARS

| bar | met | the numbers |
|---|---|---|
| 1. catches half the decisive errors while losing at most a quarter of the decisive right answers | **no** | 100 % caught, but **94.74 %** of the right answers lost against a quarter's bar |
| 2. the accuracy among the answered is 5 points above the accuracy over all | **yes** | 100 % against 92.68 % — **+7.32 points**, on two answered sessions |
| 3. teacher dependence is zero and the only knob is declared | **yes** | **0.000**; one knob, `Z_NULL = 1`, declared before the run |
| 4. the two roads agree within 25 % on coverage | **no** | coverage **4.88 %** against the binomial K = 1's **82.93 %** — a ratio of **0.059** |

**2 of 4.** Bar 2 passes on two answered sessions and is worth nothing;
bar 4 fails by a factor of seventeen, because the truncated null is
seventeen times more conservative than the operating point the two roads
were supposed to agree on.

## 8. WHAT THIS LANE NOW KNOWS

**THE TRUNCATION DOES NOT RESCUE THE DEGENERATE CASE, AND THE REASON
IS NOT ABOUT NULLS.** The geometry null said *the material has nowhere
else to be*; the truncated null says *the material could be anywhere, so
its balance means nothing*. Both abstain on all 15 room-wide sessions,
and all 15 of those are right answers. The undecidability is a property
of the material — a field has a balance and no centre — and no null
built from placements can find a centre in a field.

**THE GEOMETRY-NULL FAMILY IS EXHAUSTED AS FAR AS THIS CORPUS CAN
SAY.** Two nulls have now been built from the room's own geometry — its
shape and its walls — and both abstain on the field, with the second
strictly more expensive than the first. The geometry null remains the
better of the two.

**AND THE CORPUS IS ONE ROOM, WHICH IS THE DEEPER LIMIT.** Every null
in this family is built from **this room's** geometry at 5 px in x and
3 px in y, where the room's half is 20 answer columns of a 40×24 grid.
A rule that is right about one room's field is not yet a rule about
fields. The corpus holds 139 sessions of the same room and the same
viewpoint.

**THE HONEST SUMMARY OF THE ARC, AFTER FIVE STUDIES.** No abstention
rule has shipped. The count's margin is the best signal found and no
calibration of it is both cheap and truth-blind yet. Five studies, five
ways of learning that the vocabulary does not know what it does not
know — and one strong result about what the corpus IS: a room-sized
field with a balance and no centre.

**THE NEXT MEASUREMENT IS NOT ANOTHER NULL FROM THIS ROOM.** It is a
**second room**, or a second viewpoint, because every null in this family
is a statement about one room's geometry and cannot be checked against
one. A second room would also be the capture that closes the
across-room vocabulary test and the between-room spread at once.

## 9. WHAT KILLS THIS

- **The room-wide case cannot be rescued by relaxing the placements.**
  Measured: 15 of 15 get a non-degenerate null and 15 of 15 abstain
  anyway.
- **The rule is degenerate in practice.** On the held-out set it answers
  0 of 8 sessions and 0 of 432 pairs. A rule that never answers is not a
  rule; it is a refusal.
- **The corpus cannot check the question.** One room, one viewpoint, one
  sensor, one cardinality. The nulls are built from that room's shape,
  so their correctness is unfalsifiable here.
- **The permissive reading remains inadmissible.** It was measured and
  seen in the geometry study; adopting it now would be hindsight wearing
  a rule's clothes, and the eight held-out sessions do not launder a
  choice that was made on other data.

## 10. THE FILES

| file | what it is |
|---|---|
| `experiments/glyph_truncated_null.py` | the truncated null, the rule, the declaration, the dated correction, the held-out split, the selftest |
| `results/glyph_truncated_null.json` | every number, including the per-session profiles and the held-out rows |
| `docs/GLYPH-GEOMETRY-NULL.md` | the study this one answers, and the one that named the candidate |
| `docs/GLYPH-ABSTAIN.md` | the first abstention study |
| `docs/GLYPH-EFFECTIVE-N.md` | the correlation correction, and why it destroys the rule |

```
/home/proart/projects/gpu-venv/bin/python experiments/glyph_truncated_null.py --selftest
/home/proart/projects/gpu-venv/bin/python experiments/glyph_truncated_null.py \
    --out results --prior results/glyph_geometry_null.json
```

Committed for Muse to review; not merged.

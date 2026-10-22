# THE GEOMETRY NULL — the threshold from the room's own shape, and why the corpus is mostly not a blob

**Tool:** `experiments/glyph_geometry_null.py` (9/9 selftest green)
**Results:** `results/glyph_geometry_null.json`
**Device:** CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy, no GPU, no network
**Corpus:** the same live corpus — 121 sessions, 47 with a fitted vocabulary, 33 decisive

---

## 0. THE HEADLINE

**The geometry null is a much STRONGER signal than the binomial in the
transfer, and an ANTI-INFORMATIVE one in the self case — and the reason
is a fact about the corpus that is worth having on its own: the
grid's characteristic material is usually NOT a blob. It spans the
room.**

| | |
|---|---|
| decisive sessions whose cluster spans **every** answer column | **15 of 33** (45 %) — and **15 of those 15 are right** |
| the median cluster's width, in answer columns of 20 | **12** |
| the geometry null's accuracy among the answered, TRANSFER | **94.9 %** against 84.7 % over all — and it catches **94.0 %** of the decisive errors |
| the binomial K = 1, same measure | 89.4 % among the answered, catching **57.9 %** of the errors |
| the geometry null's accuracy among the answered, SELF | **87.5 %** against 93.9 % over all — **worse than answering everything** |
| **bars met** | **1 of 4** |

---

## 1. THE RULE, AND WHY IT WAS WORTH BUILDING

Two studies in a row failed to give the vocabulary a shipped abstention
threshold, and they failed for the same reason: the binomial z-score
treats the grid's 960 cells as independent, and they are not.

**The geometry null replaces the null with the room's own geometry.**
Take the session's characteristic cluster — its actual cells, its actual
column profile — and ask what the left/right split would be if the blob
were placed elsewhere in the room:

    the statistic   f = the cluster's left fraction among the answer cells
    the null        f(s) for every placement s that keeps the blob inside
    the rule        abstain when |f(0) - 0.5| < Z_NULL * sd(f)

with **Z_NULL = 1**, declared before the measurement and the only number
in the rule. There is nothing to fit: the threshold comes from the
session's own material, so the rule cannot be fitted to the truth even
by accident.

The hope was that the null would know something the binomial does not:
**a blob that spans the room answers the question however it is
placed**, and a narrow blob placed off-centre answers it decisively.
The binomial knows neither.

## 2. THE RESULT: A STRONG SIGNAL IN THE TRANSFER, A WEAK ONE IN THE SELF CASE

**Transfer — 1518 decisive pairs.**

| | coverage | accuracy over all | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|---|
| the geometry null | **18.0 %** | 84.7 % | **94.9 %** | **94.0 %** | 79.8 % |
| the binomial K = 1 | 60.7 % | 84.7 % | 89.4 % | 57.9 % | 36.0 % |
| the binomial K = 2 | 41.0 % | 84.7 % | 95.0 % | 86.7 % | 53.9 % |

**This is the strongest abstention signal measured in this lane.** The
geometry null catches **94.0 %** of the decisive errors where the
binomial at the same confidence catches 57.9 %, and its accuracy among
the answered is 94.9 % against 89.4 %. It is also the most expensive:
**79.8 %** of the right answers go, against 36.0 %.

**Self case — 33 decisive sessions.**

| | coverage | accuracy over all | accuracy among the answered | errors caught | right answers lost |
|---|---|---|---|---|---|
| the geometry null | **24.2 %** | 93.9 % | **87.5 %** | 50.0 % | 77.4 % |
| the binomial K = 2 | 63.6 % | 93.9 % | 100.0 % | 100.0 % | 32.3 % |
| the binomial K = 1 | 81.8 % | 93.9 % | 100.0 % | 100.0 % | 12.9 % |

**In the self case the geometry null is anti-informative: 87.5 % among
the answered against 93.9 % over all.** It throws away 15 sessions and
keeps 8, and the 8 it keeps are worse than average.

**Bars 1, 2 and 4 fail; bar 3 (truth-blindness, one declared knob)
passes.** The agreement test fails too: the geometry null's coverage
is **24.2 %** against the binomial K = 1's **81.8 %** — a ratio of
**0.296** against a bar of within 25 %. The two roads do not meet.

## 3. WHY, AND IT IS A FACT ABOUT THE CORPUS

Look at the profile widths — how many of the 20 answer columns the
cluster's cells occupy:

| width | 2 | 3 | 5 | 6 | 7 | 10 | 11 | 12 | 13 | 15 | 17 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sessions | 1 | 1 | 2 | 1 | 1 | 1 | 4 | 2 | 1 | 4 | 1 | 2 | **12** |

**The median cluster spans 12 of the 20 answer columns, and 12 clusters
span all 20.** The characteristic material is not a blob in a room; it
is **the room**. A person walking a room for four minutes leaves
changed cells in every column, and the vocabulary's "characteristic
cluster" is the material that moves — which is everywhere.

**And here is the consequence, which is the whole finding: for a
profile that spans every column, the placement null is DEGENERATE.**
Translating it changes nothing, so there is no spread, so the rule
abstains — on **15 of the 33** decisive sessions. And **all 15 of them
are right answers.** That is where the rule's cost comes from, and it
is why the accuracy among the answered comes out below the base rate.

**So the physics I wrote into the tool was right and its consequence
was expensive.** A wide blob spans both halves, so its position says
nothing — but its MASS BALANCE still says something, and the rule was
throwing that away along with the position.

**This also explains, from the other end, why the count's MARGIN is the
signal and not the cluster's position.** The abstention study found
that the margin (how lopsided the mass is) identifies the failures and
that the evidence size does not. The geometry null finds that the
POSITION (where the mass is) does not, because there is no position to
find — the mass is everywhere. **The corpus's material is a field, not
a blob, and a field has a balance and no centre.**

## 4. THE OTHER READING, AND WHY IT IS NOT TAKEN

The degenerate case has two honest readings:

- **the conservative one (declared, and what was measured):** the null
  says nothing, so the rule cannot justify an answer, so it abstains;
- **the permissive one:** the null says nothing, so there is no evidence
  *against* the answer, so the answer stands.

**The permissive reading is better on this corpus** — answering those 15
gives coverage 69.7 %, an accuracy among the answered of 95.7 %, half
the errors caught and only 29.0 % of the right answers lost.

**AND IT IS NOT TAKEN, BECAUSE I HAVE ALREADY SEEN THE SPLIT.** Choosing
the permissive reading now, after seeing that all 15 of those sessions
are right, is exactly the truth-selection this lane has already been
bitten by once — the cardinality that inflated 33/43 to 39/43. A
reading adopted after the data has been seen is hindsight wearing a
rule's clothes, and the whole point of this study was to avoid that.

It is also worth saying plainly that **the permissive reading does not
meet the bars either**: 29.0 % of the right answers lost against a bar
of 25 %, and +2.7 points of accuracy against a bar of +5. So neither
reading gives a shipped rule. The ambiguity is the finding; the choice
belongs to a run that declares it in advance.

## 5. WHAT IS NOT MEASURED, AND THE NEXT MEASUREMENT

- **THE NEXT MEASUREMENT: a null that handles the room-wide case.**
  Two things have to be decided, both before the run: how a
  room-wide profile's null is built, and what a degenerate null means.
  The candidate is the **truncated placement null** — the room has
  walls, so a blob may be placed partly out of frame, and the resulting
  spread is non-zero even for a room-wide profile. It needs no knob and
  it uses the session's own material, and it must be declared and run
  on a corpus that has grown, because this session has now seen the
  split.
- **The vocabulary still answers every session.** No abstention rule in
  this lane has shipped, and the honest summary is that the count's
  margin is the best signal found and that no calibration of it is
  both cheap and truth-blind yet.
- **One room, one viewpoint.** The whole arc is this room's geometry at
  5 px in x and 3 px in y, where the room's half is 20 answer columns.
- **The corpus moved again.** 121 sessions; the grid study saw 43 and
  the abstention study 47.

## 6. THE FILES

| file | what it is |
|---|---|
| `experiments/glyph_geometry_null.py` | the null, the placements, the rule, the selftest |
| `results/glyph_geometry_null.json` | every number, including the per-session profiles |
| `docs/GLYPH-ABSTAIN.md` | the first abstention study |
| `docs/GLYPH-EFFECTIVE-N.md` | the correlation correction, and why it destroys the rule |

```
/home/proart/projects/gpu-venv/bin/python experiments/glyph_geometry_null.py --selftest
/home/proart/projects/gpu-venv/bin/python experiments/glyph_geometry_null.py --out results
```

Committed for Muse to review; not merged.

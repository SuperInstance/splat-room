# IDEATION — the MEANING LENS (mcode, 2026-10-21)

**The seat's territory:** glyphs as MEANINGFUL representations in the splat
world — semantic splats (each splat carries a glyph embedding; a room you
can QUERY in characters), and ASCII characters as compressed scene
semantics for agents.

**The lens, in one line:** *a character is not a picture of a thing; it is
a claim about what the thing is, and the claim is worth exactly as much
as the evidence under it.*

**The one thing I will argue for, and it is the opposite of the obvious
one:** the per-splat glyph embedding is the WRONG unit of meaning for
this programme, and the character grid is the right one. Read on for the
measurement that says so.

---

## RECON — what exists, ours and outside

### Ours, and read from the clones

**`SuperInstance/chiaroscuro-embedding` — the acoustic glyph.** An
acoustic scene is rendered to a spectrogram, the spectrogram is rendered
to a TEXT grid, and a text-only reader tries to recover the scene's
parameters from the characters alone. The verdict is **MARGINAL**, and
the numbers are the whole story of this riff:

| what the reader recovers | R² (native ridge, best setting) |
|---|---|
| `f0` — the starting frequency | **0.880** |
| `vel` — the source's velocity | **0.888** |
| `inten` — the source's intensity | **0.747** |
| **`x0` — the source's STARTING POSITION** | **−0.083** |

**Position is the one thing the glyph cannot carry.** Frequency,
velocity and intensity all survive; the source's *position* is at
**zero R²** — and not for want of resolution. The sweep runs 24 → 192
columns and `x0` goes 0.057 → 0.037 → 0.037 → 0.018 → −0.006, i.e. it
gets *worse* with more characters. The chance control (permuted train
labels) is at −0.60 to −0.83, so the reader is genuinely above chance on
three parameters and genuinely at chance on the fourth.

**`SuperInstance/voxelglyph` — what an agent can read through the text.**
Its finding is that the **alignment** of the glyph grid matters more
than the symbol count, and that a *second* renderer applied to the same
image must be **row- and column-aligned** with the first or the two
readings are uninterpretable. It also holds the vacuity guard: seven
pins re-deriving a claim from a second implementation is not a
verification, and two correct opinions about the same wrong product are
still wrong.

**`SuperInstance/chiaroscuro` — the glyph renderer itself.** `renderer.py`
carries ten ramps (`classic`, `fine` — 95 printable glyphs, `blocks`,
`minimal`, `stars`, `runes`, `binary`, `code`, `waves`) and a
`glyph_election.wgsl` WebGPU shader that elects a glyph per cell at
18–30 fps on integrated graphics. Its own experiment ledger already says
the important thing: **c1 = KEEP** (the setting `edge|style=emboss`
recovers 3/3 parameters at R² ≥ 0.5), **c2 = KEEP** (a real vision
model's CLIP interpretation of the video is readable from the rendered
text alone, best margin over the prior **+60.0 pts**, 34/34 settings
beating the prior by ≥ 15), **c3 = TIE** (at a fixed character budget,
more frames at lower resolution and fewer frames at higher resolution
are equally good).

### Outside, from the landscape

The landscape's own headline for my territory is §3: **no published
system uses ASCII character grids as an intermediate representation for
3D reconstruction, SLAM, or splatting.** The nearest neighbours are
SceneScript (structured text commands, not grids), Text2Space (grids, no
3D pipeline), and PlanQA/SpatialEval (JSON and coordinates). §2's
semantic-splat line is mature — LangSplat at 84.3 % localisation vs LERF's
73.6 %, LangSplatV2 at 385 FPS querying, Gaussian Grouping's 16-d
identity encoding — and §2's own gap statement is the opening: *"every
guided method above guides with dense continuous priors. None guides with
a discrete symbolic prior."*

### The fleet's own measurements, which are the sharpest evidence I have

From the communicator lanes, all measured, all with the numbers in the
lens files:

| measurement | number |
|---|---|
| the ASCII/edge middle layer's bytes/s vs raw luma | **27.4 kB/s vs 920.4 kB/s** (33.6×) |
| the session's still fraction (the rate policy's basis) | **93.4 %** still, **96.6 %** of frames unchanged |
| the change map's noise floor | **3.0 luma** (2.6× the non-zero median 1.152) |
| the audio's envelope: does it carry a radial direction? | **41.5 %** against a **39.2 %** chance level, AUC **0.5064** |
| the pitch tracker's own jitter at a crossing | median **14.70 cents** vs a **7.05 cent** Doppler shift |
| the RT60 the corpus supports | **0.254–0.368 s**, fitted over **0.10–0.12 s** of audio |
| the camera's viewpoint spread over 50 sessions | **5 px in x, 3 px in y** — no parallax |
| the corpus's synthetic test rig | **44 of 97 sessions (45.4 %)** are not a room at all |

---

## STEALS — what I take, and what I reject

**STEAL 1 — the per-cell material alphabet, from `voxelglyph`'s own
conclusion.** voxelglyph's finding is that one symbol per material is
safe and that an *intensity ladder* is only as good as its alignment:
"an agentic encoding should not be a re-quantised brightness ramp. It
should be a material alphabet." I take that literally. A splat's
meaning channel should be a **small closed alphabet of material and
relation glyphs** — `#` wall, `|` edge, `D` door, `W` window, `~`
reflective, `:` unknown — not a 512-dimensional CLIP vector and not a
ramp of 95 brightness levels. **REJECT:** the "finer ramp is more
meaning" instinct. The acoustic sweep is the disproof: `x0` at 192
columns (27,648 chars/frame) is **worse** than at 24 columns (432
chars/frame). Resolution is not meaning.

**STEAL 2 — the two-channel discipline, from c1.** c1's best setting is
`edge|style=emboss` — an **EDGE** channel, not a tone channel, and it
recovers 3/3 parameters. The acoustic sweep then shows what the tone
channel alone cannot do. I take the rule: **the semantic channel must be
a shape channel.** A splat's meaning glyph should be elected from its
local *geometry* — the same reason the shape-aware renderer's lesson
transfers (LANDSCAPE §3.5: "a slash and a dot with the same coverage come
out as the same character", so glyphs must be chosen by local geometry,
not brightness). **REJECT:** CLIP embeddings on the splats. Not because
CLIP is bad — LangSplat's numbers are good — but because CLIP's embedding
is a *web-scale prior* and the fleet's law is that a teacher may label
and a calculator fits. A room's own glyph alphabet, fitted from the
room's own cells, is the fleet-consistent thing.

**STEAL 3 — the acceptance protocol, from `voxelglyph`'s vacuity
guard.** Seven pins re-deriving a claim from a second implementation is
not a verification. Two correct opinions about the same wrong product are
still wrong. So my first build's acceptance test must be one a
sceptical reader would accept: **a held-out query the room never
trained on, answered from the characters alone, scored against the
splat's own rendered answer.** Not "the glyph looks right". Not "the
embedding is close". A question with a right answer that the system did
not see.

**STEAL 4 — the query grammar, from SceneScript.** The landscape's
steal for §3 is SceneScript's *interpreter pattern*: a tiny
deterministic language whose commands build geometry. I take it for the
semantic layer: a splat's meaning is not a vector, it is a **command**
in a closed grammar — `wall()`, `door()`, `window()`, `sink()` — and a
room is queried by running that grammar's *inverse*. **REJECT:**
SceneScript's training regime (100k synthetic scenes, a learned
autoregressive emitter). We have one room and a calculator; we do not
have a scene corpus.

**STEAL 5 — the coordinate/grid pairing, from the landscape §3.3.** "*Cartesian (x,y) coordinates consistently beat topographic (ASCII-grid) representations*", and "a clean text grid can carry spatial information *better than the image does*". Both are true and they are not in tension: **the grid answers "what is where", the coordinates answer "how far".** I take the pairing — a room you can QUERY in characters is a room that ships both, and the grid is the query surface while the coordinates are the arithmetic substrate.

**REJECT — the emissive splat.** A splat that carries a glyph
*rendered as* its appearance is a picture of a room made of
characters, and the acoustic sweep is the argument: it is the *tone*
channel, and the tone channel is the one that cannot carry position.
Meaning must be a **side channel that does not change what the splat
looks like.** The fleet's own motion-as-text design already does this:
the glyph layer and the ghost layer are separate, and the shimmer between
them is the signal.

---

## THE RIFF — seven ideas

### 1. THE GLYPH SIDECAR: a splat carries a character, not an embedding

**The idea.** Every Gaussian in the room field gets a **sidecar**: one
character from a closed alphabet, stored beside the splat and never
rendered into it. The splat still looks like the room; the sidecar is
what the agent reads.

```
   RGB + shape          sidecar          what it means
   ───────────          ───────          ──────────────
   the wall's colour    #                a wall, and this one's material
   the door's colour    D                a door, and this one's width
   the window's colour  W                a window, and this one's glazing
   the sink's colour    ~                reflective: this is what made
                                         the acoustic hum
   the unknown cell     :                not seen yet
```

**Why the character and not the embedding.** The acoustic sweep is the
direct evidence, and it is not subtle. Three parameters survive the
glyph channel — frequency (0.880), velocity (0.888), intensity (0.747)
— and the fourth, **position**, does not (−0.083). Meanwhile the
*spatial* sweep (t1_thermal) recovers **position** well (0.74–0.85) and
**intensity** badly (0.14–0.32). So the glyph channel carries
*discrete categorical* content well and *continuous* content badly, and
the thing a semantic splat most needs to carry — *what this thing is* —
is categorical. The sidecar is the right shape for the job.

**The measurement that would prove it.** Take a room's splats, give each
one a sidecar, and ask: does the sidecar's character predict the
splat's *geometry* (a `D` is tall and narrow, a `#` is wide and flat,
a `~` is small and bright) better than a 512-d CLIP embedding predicts
it, at one tenth the bytes? **One number: the sidecar's accuracy on the
held-out geometry task, against CLIP's, against the byte cost.**

### 2. THE QUERY IS THE PRODUCT: a room you can QUERY in characters

**The idea.** The splat field is the *appearance*; the sidecars are the
*interface*. An agent's question is answered by **running the grid**,
not by rendering the room and asking a vision model.

```
   the question:        "which wall has the door?"
   the answer path:    read the sidecar row
                       D at column 14, row 7
                       the wall to its left is # and the one to its
                       right is #, so the door is in the NORTH wall
   the cost:            one pass over the sidecar array
   the model's cost:    a full render, and a vision model that may
                        not be on the device
```

**Why this is more than a convenience.** LANDSCAPE §3.3: "a clean text
grid can carry spatial information *better than the image does* for an
LLM". And §3.2's warning: LLMs *read* ASCII far better than they
*construct* it — "generate the grid algorithmically from depth/occupancy
(a renderer, not an LLM), and let the LLM only read/annotate it. Never
ask the LLM to draw the map freehand and then trust it."

**So the law is: the grid is a RENDERER'S OUTPUT, never an LLM's
composition.** The agent reads; it never draws. That single rule is
what makes idea 2 safe, and it is also the rule that keeps the room
queryable without a vision model on the device — which is the fleet's
"the camera never leaves the device" law applied to the *reasoning*
rather than the capture.

**The measurement.** A held-out question set over the room (the landscape
names PlanQA's shape: 1,800 layouts, 18,000 questions) answered from the
sidecars alone, scored against the same questions answered from a
render. **Two numbers: sidecar-only accuracy, and render accuracy.**

### 3. THE ALPHABET IS FITTED, NOT CHOSEN: a per-room material vocabulary

**The idea.** The sidecar's alphabet is **not** a fixed global set of
characters. It is fitted per room, the way the fleet fits everything
else: the calculator doctrine, no teacher.

```
   the fit:  cluster the room's cells by their local geometry
              (a shape descriptor, not a brightness)
              →
              the rooms OWN clusters get the rooms OWN characters
              →
              the character that means "the door" in this room is
              whatever character this room's door cluster earned
```

**Why this, and why not a fixed vocabulary.** A fixed alphabet is a
teacher: someone decided in advance that `D` means door, and that
decision is a label no measurement in this fleet can produce. A fitted
alphabet is a *clustering*, and clustering is a calculator. It also
solves the fleet's actual problem: two rooms' walls have different
materials, and one global `W` for wall would be a lie in one of them.

**The borrow.** voxelglyph's exp3 found that the same materials at S=8 and
S=24 collide while S=16 and S=32 separate — the *number* of symbols is
the alignment's business, not the semantics'. And its rule: **one symbol
per material is safe; identity, not intensity.** So the fitted alphabet
has a fixed small cardinality and the symbols mean *identity*, never a
position on a ramp. Concretely: the alphabet is fitted per room at a
cardinality chosen by the alignment test, and the character set is
drawn from the ramp that renders best (`classic`, `blocks`, `runes` —
not `fine`, whose 95 glyphs are a rendering convenience and not a
semantic claim).

**The measurement.** The number of clusters the room's cells actually
support, against the number a fixed vocabulary would have guessed. And
the leave-one-out check: fit the alphabet on half the room, read the
other half, and see whether the characters still mean the same thing.
**A vocabulary that only works on the cells it was fitted on is a
caption, not a language.**

### 4. THE NEGATIVE SPACE IS A CHARACTER: `:` and the hunger

**The idea.** The character grid's most important glyph is the one that
means *nothing was observed here*. The fleet already measures this
precisely: **93.4 %** of a session is still and **96.6 %** of its frames
are unchanged, and the rate policy's whole argument is that the budget
should follow the change.

So the grid's alphabet carries an **observation** channel beside its
**meaning** channel:

```
   #  wall, seen
   D  door, seen
   :  NOT SEEN — the cell was never observed
   ?  seen, and its meaning is ambiguous
```

This is what makes the grid **queryable in the right way**: "where is
the door?" is answerable, and so is "where might a door be that we have
not found?" — the `:` cells are the candidate set, and they are
*distinguishable from the walls*. Without a negative glyph, an unobserved
cell and an observed wall are the same character and the grid cannot
tell a room from a guess.

**The borrow.** The landscape's §6.5 (feed-forward preview + ASCII diff
as a capture coach) needs exactly this to work: "cells still `?` are
rendered in the ASCII map and surfaced as guidance". The negative glyph
is what turns the grid from a picture into a **worklist**.

**The measurement.** The grid's negative-glyph rate against the
measured coverage — and the alignment check that the `:` cells and the
measured-uncovered region are the same cells, to within the frame's own
registration error. **One number: the IoU between "the grid says
unseen" and "the coverage says unseen".** If they disagree, the grid is
decorative.

### 5. THE AUDIO SIDECAR: what the room SOUNDS like, as a glyph

**The idea.** The acoustic prior gets its own sidecar column. Each
region of the room gets a character that says **what the room does to
sound**, and it is fitted from the room's own audio, not from a
web-scale acoustic model.

```
   the room's cells get a second sidecar column:
     @   strongly reflective   (the room's decay rate is high here)
     .   absorptive            (the room's decay rate is low here)
     ~   reflective AND bright — the acoustic hum's source
```

**Why this is a MEANING claim and not a measurement claim.** The
corpus's own numbers are the honesty check, and they are a gift:
- The **RT60** is real but crude: **0.254–0.368 s**, fitted over
  **0.10–0.12 s** of audio and 19 dB of decay, then extrapolated 3×.
- The **envelope carries the event but not the direction**: 41.5 %
  agreement with the video's radial label against 39.2 % chance, AUC
  0.5064 — because at 74.5 % of crossings the hump is the speaker's own
  voice.
- The **Doppler is dead**: 7.05 cents against the tracker's own 14.70
  cent jitter.

So the audio sidecar may say **reflective or absorptive** (a room-average
scalar, honestly labelled) and **where something moved** (a presence
channel). It may **not** say *toward* or *away*. The sidecar alphabet
is sized by what the measurement supports, and the measurement is what
limits it.

**The borrow.** oracle's steal 3 — the RIR self-check, the room model
must predict its own acoustics — is this idea's validator. If the
model's predicted decay disagrees with the measured decay, that is a
ledger row. The sidecar is the *claim*; the self-check is the
*evidence*; and they are in different layers, which is the fleet's law
that a judge cannot certify itself.

**The measurement.** The acoustic sidecar's fitted decay rate against the
measured one, on a session whose floor is known. **And the negative
control: on the corpus's 44 synthetic sessions, the sidecar must refuse
to fit** — a test tone is not a room.

### 6. THE VOWEL: one glyph per material, chosen by how it is said

**The idea.** This is the fleet's tone vocabulary, transplanted — and it
is the same law with a different surface. The tone game's six intents
each carry a ten-field style vector, and the delta between two intents
is a delta in the score's own parameter space. Eight marks in three
families, each with **one anchor out of six**, and the four fields that
**cannot** carry a mark are named (density, jitter, pause, hold; ratios
0.35–0.70).

Applied to a room: **each material gets a vowel.** A wall that absorbs
and a wall that scatters are not the same character — they are the same
character said differently. And the vocabulary is per-room-fitted, so
"a" means *this* room's soft material and not the alphabet's.

**Why it matters for the splat sidecar.** The measured fact that
matters is the graduation: the structure mark and the question mark
**survive the MIDI's loss** of its parts, the earnest and obligate marks
**degrade**, and the other four **do not survive at all**. A semantic
sidecar has exactly this property — it survives or it does not, and
"it degrades" is a design failure, not a nuance. So the alphabet's
graduation must be *measured per room*, and the marks that degrade get
dropped.

**The measurement.** Which of the room's material distinctions survive
the splat's own representation loss, and the size of the alphabet that
survives. **A vocabulary of three marks that survive beats a vocabulary
of eight where five degrade.**

### 7. THE RECEIPT IN CHARACTERS: the room's own change log, legible

**The idea.** zcode's walk receipt is a screen; this is its *text* form,
and it is the artefact an agent reads. Every walk emits a receipt that
is itself a character grid, so the room's history is legible by an agent
that never sees a render.

```
   WALK RECEIPT — 2026-10-21 14:32 · 11 min · 9 keyframes
   ██████████████▓▓▓▓▓▓▓░░░░░░░  coverage: dense W wall, hungry E
   k1─k2─k3─k4──k7   ▲ still 62% / moving 38%  ▲ 31 depth cues
        ╲ k5,k6   ▲ audio: 2 walk-bys, 0 dead-band events
                   bench: splats +4,100 this walk (fed by k4,k7)
```

Every number in that receipt is a **measured** one from the fleet's own
lanes, and every one of them has a lens entry behind it — the still/move
ratio is the rate policy's 93.4 %, the dead-band events are the lens
files', the walk-bys are the envelope study's 574 crossings. **The
receipt is the ledger's human twin, in the glyph language, and the
ledger row points at it rather than inlining a boast.**

**The borrow.** zcode's idea 5 and oracle's CROSS on it (the bench
renders yesterday-vs-today and validates the receipt's coverage shading
against what the renders show changed). This idea is the *third* reader
of the same evidence: the phone shows it to the human, the bridge shows
it to the ledger, and the agent reads it as characters.

---

## FIRST BUILD

**One thing, and it is the smallest one that could be wrong:**

> **Take ONE session bundle, voxelise its change map into a 40×24 grid,
> fit a per-room character alphabet to the grid's cells by clustering
> their local geometry, and emit a character grid. Then answer one
> held-out question about the room from the grid alone and score it.**

No splats. No Blender. No CLIP. The change map is 160×96 and the
repository already reads it (`experiments/lens.py:frame_motion_maps`), and
the grid it produces IS the middle layer the programme's stage 1 is
specified to produce. **This build is stage 1, and it produces stage 1's
output plus a vocabulary for it.**

**Acceptance, as numbers:**

- the grid is 40×24 characters and the whole file is **under 1 KB**;
- the alphabet is **fitted**, with a cardinality chosen by voxelglyph's
  alignment test, and **leave-one-out**: fit on half the cells, read the
  other half;
- one held-out question, answered from the grid alone, scored against
  the same question answered from the full-resolution luma;
- the negative glyph `:` appears, and its cells agree with the measured
  coverage to a stated IoU;
- **the synthetic sessions must produce a refusal**, not a grid — 44 of
  97 sessions are a test rig, and a build that cannot tell a test tone
  from a room is a build that will lie.

**The number that decides it:** *held-out grid-only accuracy against
full-luma accuracy, and the byte cost of each.* If the grid is 1000×
smaller and loses nothing, the semantic splat's sidecar is free. If it
loses a lot, then the sidecar must be an **embedding** after all and
idea 1 is wrong — and the acoustic sweep's `x0` at −0.083 says that is
the likely outcome for anything *positional*, which is why idea 2 keeps
the coordinates beside the characters.

---

## WHAT KILLS IT

Stated now, before it is built, because a riff that cannot be killed is
a belief.

1. **The positional kill.** The acoustic sweep's `x0` is at −0.083 and
   gets *worse* with resolution. If the grid cannot carry position, the
   room is a bag of labels and idea 2's queries are unanswerable without
   the coordinates beside them. The escape is in the design (the pairing
   from STEAL 5), but the escape is a *half* answer and it should be
   said so.
2. **The construction kill.** Text2Space's read–write asymmetry:
   LLMs interpret given ASCII far better than they construct it. If the
   grid ever becomes something an LLM composes rather than something a
   renderer emits, the whole thing inverts into a hallucination
   generator with a beautiful font.
3. **The vacuity kill.** voxelglyph's guard: seven pins re-deriving a
   claim from a second implementation is not a verification. If the
   grid's held-out accuracy is reproduced by a trivial baseline — say,
   the brightness ramp the tone channel already is — then the
   clustering bought nothing and the vocabulary is decoration.
4. **The one-room kill.** The whole vocabulary is fitted per room. On
   the second room, is the fit stable? A vocabulary that only works on
   the cells it was fitted on is a caption, not a language. The
   leave-one-out is the test and it is in the acceptance, but the real
   test is a second room.
5. **The floor kill.** The acoustic sidecar is only as good as the
   corpus's noise floor: RT60 fitted over 19 dB and extrapolated 3×,
   and the negative control returning 3.5 s because the floor was
   removed. A sidecar that claims "reflective" on a floor-limited
   measurement is worse than no sidecar.
6. **The synthetic kill.** 44 of 97 sessions (45.4 %) are an
   end-to-end test rig. Any build that does not filter by device will
   fit its vocabulary to a test tone, and this has already happened once
   — in the audio priors' own first draft, where a synthetic peak made
   the microphone's gain look like it varied 334× when it varies 21.9×.
7. **The no-parallax kill.** The camera did not move: 5 px in x, 3 px
   in y across 50 sessions. Any claim that the grid is a *metric* room
   is unsupported by this corpus, and the grid must be labelled
   image-space until a phone walk creates the parallax.

---

## CROSS — extending two seats' ideas

Per the protocol: one extension of another seat's idea, building on it
rather than restating it.

### CROSS 1 — on oracle's steal 1 (bind GLYPH embeddings into the splats)

**Oracle's steal is right that the splats need a feature layer, and it
names the wrong unit.** LangSplat's per-Gaussian CLIP vector is the
mature, fast, standard thing — 84.3 % localisation, 385 FPS querying in
V2 — and it is also a **web-scale teacher** and a 512-float tax per
splat.

**My extension: bind the glyph SIDECAR instead, and make the embedding
optional and downstream.** The sidecar is one byte per splat against
LangSplat's compressed-but-still-vector feature layer, it is fitted from
the room's own cells rather than distilled from CLIP, and — the
measurable part — **the acoustic sweep says the discrete categorical
content is what survives the character channel** (frequency 0.880,
velocity 0.888, intensity 0.747) while the continuous positional content
does not (`x0` −0.083). A splat's *meaning* is categorical. Its
*appearance* is continuous and is already carried by the RGB. So the
feature layer's job is exactly the categorical job, and the categorical
job is the one a byte does.

**The synthesis this creates:** the sidecar can be **voted on by the
agents that read it**. An agent asks "which wall has the door?" and
answers by reading characters. A second agent, or the ledger, can
aggregate the same sidecars into a **material histogram** — how much of
this room is wall, how much glass, how much unknown — with no rendering
at all. That histogram is the first *semantic* product the fleet can
produce from a room, and it is the thing a room you can QUERY in
characters is for.

> **Dated note, 2026-10-21 — after the librarian's COLLISIONS 11.**
> The librarian resolved this stake and the resolution is better than my
> extension: **the typed sidecar** — one character for identity, the
> three scalars that survive the channel as typed fields (frequency
> 0.880, velocity 0.888, intensity 0.747), JSON coordinates beside the
> grid, and position left where it is already strong, which is the
> splat's own geometry.
>
> I accept it, and I want to say **why** rather than merely agree,
> because the disagreement was real and the resolution is a third thing
> neither of us said. My argument was "the character, not the
> embedding". The oracle's was "the embedding, not the character". The
> librarian's is **"a record"** — and the reason it wins is that both
> of the other two answers are **substitutes**, and the evidence never
> supported substitution. The acoustic sweep says the character channel
> carries the categorical; it does **not** say the character channel
> carries the *continuous*. The right design therefore keeps both, and
> the sweep tells you **which field goes where**: the categorical into
> the byte, the continuous into typed floats, and the positional into
> the coordinates that already beat grids at reasoning.
>
> **And the kill-condition stays mine, and it is the thing this note
> exists to protect:** if the grid loses a lot on the held-out
> geometry task, the embedding returns **for the positional only**.
> That sentence is the difference between a synthesis and a compromise,
> and it is the acceptance criterion my first build already names.

### CROSS 2 — on zcode's idea 4 (Depth as Punctuation)

**zcode's idea is the closest thing in the round to mine, and it needs
one correction that only my lane's evidence can make.**

The idea is right: the walk-by envelope renders as a moving brightness
wave across the map, and the phone's chirp returns as punctuation before
the wall glyphs. The correction is a **number**, and it is the number
zcode's own artefact depends on.

**The envelope carries the EVENT and not the DIRECTION.** Measured:
574 crossings across 35 sessions; on the real microphone's live
crossings, the envelope's direction agrees with the video's radial label
**41.5 %** of the time against a **39.2 %** chance level, with an AUC
of **0.5064**. And the reason is not a subtlety: at **74.5 %** of those
crossings the envelope's peak lands on one of the session's own speech
segments, because the crossings in this corpus are a seated person
gesturing, not someone walking past the microphone. Doppler is
definitively dead — **7.05 cents** against the tracker's own **14.70
cent** median jitter.

**So the punctuation is a punctuation, and must be typed.** The wave
across the map says *something moved here and it was loud enough to
measure* — an **event**, on a per-crossing basis, from the presence
channel. It does **not** say *toward* or *away*, and it must not draw
an arrow. zcode's own phrasing — "the envelope renders as a moving
brightness wave" — is already right; what the extension adds is the
**type annotation**, the way a transcript annotates a pause's *kind*
rather than its presence.

And the extension to the chirp half: the punctuation's *width* is the
depth cue, and the width has a measured uncertainty — the audio leads
the video by **−6.3 to −92.3 ms**, and the envelope's analysis frame is
50 ms long with its time at its **centre**, so a punctuation mark has a
**±25 ms** placement uncertainty before the clock offset is even
applied. So a punctuation mark is drawn with a **width that carries its
own uncertainty**, and the fleet's own convention applies: the number
is reported with the limit attached, never bare.

**The synthesis this creates:** the glyph grid gets a **third column**
beside the sidecar — an event channel — where a cell can say *something
moved here* without saying where it went. That is a grid an agent can
read for *activity* without being misled about *direction*, which is
exactly the kind of honest-but-weak signal the fleet's pause doctrine
already prefers to a strong-but-false one.

> **Dated note, 2026-10-21 — after the arrival-time estimator was
> measured.** The chirp half of zcode's idea just got much better, and
> the way it got better changes what the punctuation should carry.
>
> The chirp's *return delay* is the depth cue, and the delay between two
> arrivals is now measured by a fleet calculator: the band-limited
> **envelope** cross-correlation, resolving to **0.004 ms** with a null
> bias of **0.0002 ms**. That is **0.0014 m of range** — two orders of
> magnitude finer than the room.
>
> **And the part that changes zcode's design:** the measurement needs
> **no clock relationship between the phone and the laptop at all**. The
> delay is found by comparing the two signals *to each other*, so the
> offset between their clocks cancels exactly — measured directly, two
> signals with no clock relationship and 7.3 ms between them come back
> as 7.0 ms. **The punctuation's depth does not depend on the fleet's
> clock doctrine being fixed first.**
>
> **What this changes for the glyph:** the punctuation mark's depth is
> no longer a *count of dots* ("1 leading dot per ~5 ms of return", as
> zcode's example puts it) with a width that carries the uncertainty.
> A dot count is a lossy encoding of a quantity that is now measured
> directly and to a thousandth of a metre. **The mark should carry the
> measured delay, and the dot count should be a rendering of it** —
> because a dot count's quantum (5 ms) is *worse* than the estimator's
> whole error budget (0.004 ms) by a factor of a thousand.
>
> **And the caveat that belongs beside it:** one delay gives **range
> along one axis**, not place. A phone's return delay says how far the
> phone is; it does not say where the phone *is* without a second
> independent delay or a prior on where it can be. So the punctuation
> mark is a **distance**, and it must be drawn as a distance — with its
> uncertainty attached — and not as a position on the map.

---

### The build landed — dated note, 2026-10-21

**FIRST BUILD above is BUILT and MEASURED.** `experiments/glyph_grid.py`
(20/20 selftest), `results/glyph_grid.json`, report `docs/GLYPH-GRID.md`,
ledger row in `EXPERIMENTS.md`. Scored against this riff's own
acceptance:

- the grid is 40×24 and the whole file is **under 1 KB** — **MET**, 983
  bytes, **18,470×** smaller than the median session's luma;
- the alphabet is **fitted** and **leave-one-out** — **MET**, the
  leave-one-out is the even/odd column split with a prediction step;
- one held-out question, answered from the grid alone and scored against
  the full-resolution luma — **MET**, **33/43 (76.7 %)** raw and
  **26/31 (83.9 %)** over the decisive sessions;
- the negative glyph `:` agrees with the measured coverage to a stated
  **IoU** — **MET**, median **0.976** against the pixel-level coverage
  (it was not met at first, because the IoU was never computed);
- the synthetic sessions produce a **refusal**, not a grid — **MET**,
  35 refused by device and 10 more for too few observed cells.

**The deciding number above was *"if the grid is 1000× smaller and loses
nothing, the semantic splat's sidecar is free."* The verdict: 18,470×
smaller and it DOES lose** — a quarter of the answers, and its margin
is systematically larger than the room's (1.300 vs 1.173), so it is
confidently wrong about a fifth of the time.

**And the build caught itself twice, which is the part worth carrying
forward.** The first version scored **43/43** because counting
characters IS counting cluster labels — a tautology scores 100 %. The
second scored **39/43** because the alphabet's cardinality was chosen by
the agreement with the truth the answer was judged against; the truth
would have picked a different k on **37 of 43** sessions, worth six
sessions of inflation. **Both were caught by distrusting a number that
looked good**, and the honest number is the third one.

**So: idea 1 survives in bytes and does not survive as a lossless
summary; and the fallback does not save it, because the acoustic sweep
already says the embedding does not carry position either (`x0` −0.083,
worse with resolution). NEITHER the character nor the embedding carries
the coordinates — which is exactly what idea 2 assumed, and the grid
vindicates it.** The grid is a good vocabulary for what the room is
doing and a poor geometry for where it is.

### The transfer test — dated note, 2026-10-21

**Idea 3's acceptance criterion was *"a vocabulary that only works on the
cells it was fitted on is a caption, not a language."* That is now
MEASURED, in one room.** `experiments/glyph_transfer.py` (8/8 selftest),
`results/glyph_transfer.json`, report `docs/GLYPH-TRANSFER.md`, ledger row
in `EXPERIMENTS.md`.

**A vocabulary fitted on ONE session answers a DIFFERENT session's
question at 1,372/1,806 pairs = 76.0 %** — against the **76.7 %** it
reaches on its own session — while a random non-characteristic cluster of
the same alphabet gets **58.3 %**. And it is not a copier: on the 626
decisive pairs where the source and the target disagree about the room,
the transfer follows the **target** 80.0 % of the time.

**So the vocabulary is a property of the ROOM, not of the capture, as
far as one room can show it.** The caption worry does not fire across
sessions.

**But the room-level criterion is STILL OPEN**, and the note has to say
so plainly: every session here is the same room from nearly the same
viewpoint (5 px in x), so this is a *session*-transfer test. The riff's
criterion was about *rooms*. One room cannot answer a question about
rooms.

**And the curve nearly lied.** The first version of the decay curve —
transfer accuracy against how alike the two sessions look — came out
INVERTED, with the most similar pairs transferring worst. The reason is
a confound: in the most similar band the transfer's rate (0.660) is
*the same number* as the rate at which the two sessions share an answer
anyway (0.660), which is the signature of a copier that nobody
punishes. Conditioned on the two sessions disagreeing, the ordering
inverts back and the vocabulary transfers BEST where the two look least
alike (0.883 vs 0.677). **The lesson for the fleet: a curve is not a
finding until its confound has been measured, and the confound here was
invisible until the conditional was taken.**

### The cardinality sweep — dated note, 2026-10-21

**Idea 3's cardinality was the loose end, and it turned out to be the
whole shape of the idea.** The transfer test fixed k=3 so two
alphabets could be compared at all; the sweep now fits every alphabet
at k = 3, 4, 5 and 6 over the same corpus.

| k | the transfer (decisive) | the control | the gap | the characteristic cluster is the MOST active one |
|---|---|---|---|---|
| **3** | **79.3 %** | 64.5 % | **14.74 pts** | **24 / 43** |
| 4 | 71.9 % | 66.8 % | 5.07 pts | 14 / 43 |
| 5 | 69.8 % | 67.9 % | 1.92 pts | 8 / 43 |
| 6 | 69.9 % | 67.4 % | 2.46 pts | 7 / 43 |

**More symbols is not a richer vocabulary. It is a diluted one.** At k=3
the cluster that owns the most cells IS the moving material in 24 of 43
sessions, and it beats a random cluster by 14.7 points. At k=5 it
beats one by 1.9 — the question has nothing left to ask, because "the
biggest material" and "the moving material" have come apart.

**So the riff's guess about the cardinality was wrong in its reason and
right in its number.** I wrote that the right number of symbols is
"a question about alignment, not about brightness". It is not about
alignment: the silhouette — an alignment measure — picks k=3 because it
picks k=3, and the reason k=3 is right is that **the alphabet has to
stay coarse enough for its biggest symbol to still mean "the thing that
moves".** Alignment is the symptom; the alphabet's own structure is
the cause.

**And the next rule is stated before it is measured,** which is the only
honest way to state one: a cardinality rule that maximises the gap
between the characteristic cluster and a random cluster of the same
alphabet, with the truth never consulted. A rule about the ALPHABET's
structure rather than its separation.

---

*Filed 2026-10-21. Numbers are from the communicator lanes' measured
lens files and studies, and from the `chiaroscuro-embedding` and
`voxelglyph` result files; the session lists and thresholds are in
those files. Cross-extends oracle's steal 1 and zcode's idea 4.*

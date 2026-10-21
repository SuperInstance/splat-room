# IDEATION — the builders lens (jetson-edge seat)
(Fleet ideation round, 2026-10-21. Opened before Oracle's `IDEATION.md`
protocol landed in this clone; this revision conforms the file to it —
riff sections below, CROSS at the end. History kept, corrections dated.)
Territory: glyph-seeded splats, audio-depth priors, ASCII-guided
fitting, edge-tier budgets. Rule for every idea: wild is allowed,
unbuildable is not — each carries a build sketch and an edge-budget
line. The seat that writes it has the CUDA box, torch cu130 finally
installing on aarch64, and a no-sudo toolchain, so "buildable" is
measured against 8 GB shared and today's compiler, not a wish.

## RECON (this seat, measured/read 2026-10-21)
- The box: Orin Nano Super, 8 GB shared, no swap; desktop+agents eat
  ~3.2 GB of it. OOM is the house style of failure here — the 17:35 UTC
  OOM storm killed a compiler at 1.6 GB and the whole seat session with
  it (RUN-LOG). Everything below is budgeted against ~4.5 GB.
- Toolchain, no sudo, PROVEN today: nvcc 13.2 + g++ 13.3 under `~/opt`,
  sm_87 kernels run (whisper.cpp CUDA bench, GR3D 38% mean — the tier
  report). gsplat builds at MAX_JOBS=1; MAX_JOBS=2 OOMs. That number is
  part of every "trivial" verdict below.
- Dataset banked: nerf_synthetic lego + hotdog (train/val/test) on disk.
- torch 2.9.1+cu130 aarch64 wheel: installs, imports; kernel execution on
  this box still unproven (GPU wedged by a driver RM fault before the
  first run — RUN-LOG; reboot pending). Open risk, stated.

## STEALS
- TAKE: LangSplat's sparse-code-over-dictionary pattern (via oracle's
  wide-lens steal 1) — but the dictionary is the 10-glyph ramp, not CLIP.
- TAKE: gsplat's DefaultStrategy densification loop as the substrate the
  guidance hooks into — we bias an existing, tuned growth rule; we do not
  replace it.
- REJECT: pixel-perfect edge maps from learned depth (DepthAnything et
  al.) — a teacher in the densification loop breaks the teacher-free
  calculator doctrine; Sobel-on-luma is the honest ceiling today.
- REJECT: CUDA-monopoly trainers (rejected by the fleet's OpenSplat
  argument too): everything in this riff must run through torch+gsplat,
  which today means one box — the calcu1ator row (#7) is how we say no
  before the OOM killer does.

## FIRST BUILD
Today's two EXPERIMENTS rows: gsplat baseline on lego vs edge/ASCII-guided
splat injection, iterations-to-quality, equal-gaussian-count tiebreak.
Idea #2 (ASCII-first loss schedule) is the one-after: a pure loss change,
zero new kernels, sibling ledger row on the same seed.

## WHAT KILLS IT
- The GPU wedge class of failure (driver RM faults needing reboots) makes
  any "overnight" schedule fictional until the box proves stable for a
  full night — the persistent-field idea (#5) dies without overnight.
- Guidance that wins only by capacity is the fake result this seat is
  structured to catch (equal-count tiebreak); if the guided arm needs 2×
  splats for the same dB, the idea is dead, not "promising".
- 8 GB shared means the 200k-splat lego run is near the ceiling; anything
  full-room-scale on THIS seat needs the persistent/frozen-background
  trick (#5) or it does not need this seat.

## 1. Glyph-seeded splats — the character IS the semantic label
Not "a point at an edge" but **the ASCII character that seeded the
splat travels with it as a learned soft label.** Per-splat state grows
from RGB(3) to RGB(3) + glyph-code, where the code is **sparse over
the ramp alphabet** (` .:-=+*#%@`) — a per-splat codebook index +
confidence, in the LangSplatV2 pattern (sparse codes over a global
dictionary beat dense per-Gaussian features 47× at query time; the
same trick with a 10-glyph dictionary instead of a CLIP one).
- *What it buys:* structure queries in 3D — "render only `#`-splats"
  is a structure-only view; "where do `@` splats cluster" is a 3D
  density/edge map the night pass can read as text.
- *Build sketch:* gsplat already plumbs arbitrary per-splat channels
  through the rasterizer; supervise with cross-entropy against each
  training view's ASCII map. Feature-3DGS's low-dim+decoder trick is
  the fallback if 10 dense logits ever felt heavy (they won't at K=10).
- *Edge budget:* +2–3 floats/splat (sparse code) ≈ trivial.

## 2. Fit in the middle layer, not pixel space (ASCII-first schedule)
Supervise early iterations against the **ASCII map, not pixels**: a
24×40 grid of ramp levels is 960 targets per view versus 1.9 M pixel
values. Hypothesis: geometry (where splats go) converges from cell
targets as fast as from pixels; detail then needs the pixel pass.
- *Build sketch:* pool the render into cell means, L1 on ramp levels
  for iters < T, then switch to the standard pixel loss. Pure loss
  change, zero new kernels.
- *The number:* iterations-to-25 dB, ascii-first vs pixel-from-start,
  same seed — a sibling row for today's ledger if the day allows.

## 3. Audio-depth priors — the chirp as a depth camera for the blind side
Multi-view from a doorway never sees the wall behind the camera; sonar
sees every hard surface. Penalize splat clusters whose plane-consistent
echo prediction disagrees with measured chirp delays (meters-coarse,
geometry-scale discipline).
- *Build sketch:* RANSAC plane-fit on splat means → image-source echo
  time per plane → compare to phone-chirp TDOA (the phone-node pilot);
  every-N-iters opacity/shrink penalty on disagreeing clusters.
- *Honest limit:* the sonar survey row in the inherited table says the
  current actuator can't clear the floor — this idea is queued behind
  "better actuator", and says so.

## 4. Motion-gated splat budgets (adaptive fidelity goes 3D)
The addendum-3 tier ladder, lifted into the field: cells that never
change across sessions (walls) get their splats frozen early; cells
that move (door, chair, the walked path) keep the refinement window
open. Iterations are spent where change lives.
- *Build sketch:* per-splat refine mask from projected motion maps;
  `refine_stop_iter` becomes per-splat instead of global.
- *The number:* same PSNR at a fraction of iterations on a
  mostly-static scene (lego with masked background is a 10-minute
  synthetic stand-in).

## 5. The 160×96 persistent field — splat memory as a calculator
Our real room cameras are 160×96 — near-useless for one-shot 3D, but
the room is **static across nights**: fit a persistent background field
once (incremental, frozen thereafter), and each session only fits the
moving layer seeded in high-motion cells.
- *What it buys:* the room model graduates into the calculator library
  (per the addendum-2 spec): presence/motion become its students; the
  moving layer's center-of-mass is a 3D `fg_com` to grade against the
  pair timeline.
- *Build sketch:* freeze background splats after night 1; per-session
  optimize only motion-seeded splats; grade vs verdicts.jsonl.
- *Edge budget:* few hundred moving splats × 60 frames — minutes.

## 6. Round-trip check: splats must re-render the day's ASCII stream
Cycle consistency as a fitting trick AND a self-verification normal:
render the field at 160×96, quantize through the ASCII ramp, require it
to reproduce the day's actual ASCII stream.
- *Build sketch:* straight-through ramp quantizer; cell-level
  agreement loss. Drift in the field shows up as ASCII mismatch —
  addendum-4's "never assume a normal" applied to a 3D model.
- *Edge budget:* 960 cells/view — free.

## 7. The 3DGS budget calculator (cost-per-dB is the spec)
Before the programme scales: fit the cost model. Today's lego runs give
ms/iter vs #splats vs PSNR curve; the library entry becomes a
calculator that maps (target dB, deadline, box) → max splats and iter
schedule.
- *Build sketch:* tonight's jsonl logs are the training data; a
  3-parameter fit, embarrassingly buildable.
- *Why it matters:* keeps "room learning" honest on an 8 GB seat —
  the calculator says no before the OOM killer does.

## 8. Gaussian echo synthesis — the field renders audio too
Treat plane-fit clusters as reflectors with learned absorption; render
the room's impulse response from the field (image-source method) and
compare to measured chirp IRs. Audio becomes a second rendering channel
of the same 3D artifact — one model, two modalities to disagree.
- *Build sketch:* cluster planes → image-source IR → envelope loss vs
  measured; coarse, cheap, batch-tier.
- *Pairs with:* #3 (same measurements, inverse direction).

## Edge-tier budget summary for all of it
| idea | extra state | extra compute | verdict on 8 GB |
|---|---|---|---|
| glyph labels | +K floats/splat | one CE loss | trivial |
| ASCII-first loss | 0 | less supervision I/O | saves work |
| audio depth | 0 | minutes CPU, off-line penalty | queued on actuator |
| motion gating | mask/splat | none (saves iters) | free |
| persistent field | frozen bg | session-scale tiny | the point |
| round-trip ASCII | 0 | 960 cells | free |
| budget calculator | — | a fit | is the calculator |
| echo synthesis | absorption/plane | minutes CPU | batch-tier |

## CROSS (extensions of the sibling riffs, filed after both landed)

**On zcode's ghost-behind-the-glyphs (idea 3) — the ghost layer's wire
format, from the seat that renders it.** zcode reserved this slot: "the
first sibling riff on the splat side owns what idea 3's ghost layer
actually receives." Answer, concretely: the ghost is not a new render —
it is the trainer's existing per-view diagnostic pair, **expected depth**
(alpha-blended z-render — literally the tensor my guided injection
unprojects edge pixels with) and **rendered alpha** (coverage), pooled to
the cell grid the glyph pipeline already speaks. One render pass, three
readers: the loss, the densification prior, and the registration screen.
The extension that matters: the SAME cell disagreement zcode shows as
shimmer is my injection candidate mask (edge cells with weak alpha) — so
the phone's shimmer readout and the bench's injection budget are one
quantity in two places. COLLISIONS-4's "wire format" is this: `{depth,
alpha} per cell`, and the phone never re-derives what the bench already
computed.

**On oracle's steal 1 (LangSplat sparse codes) × my riff #1 (glyph-labeled
splats): one dictionary, two supervisions.** Oracle binds acoustic-glyph
embeddings per splat; my #1 makes the ramp glyph a per-splat soft label
supervised by cross-entropy against the view's ASCII map. Extension: the
codebook is SHARED — ramp slots for structure plus chiaroscuro-embedding
slots for sound — and a splat's code is supervised by whichever modality
saw that region (CE vs ASCII map for visual passes; CE vs
nearest-acoustic-glyph where the room's WAVs cover it). Structure labels
discipline sound labels and vice versa: a `#`-coded splat that never
heats under a chirp is either paint or the codebook is wrong. That
cross-check is teacher-free and runs at train time, not as an audit.

**On oracle's COLLISIONS-2 (receipts report marginal quality per pin):
the bench-side enabler is already in the log.** The collision wants
"PSNR-threshold crossings and gaussian count at the equal-count
checkpoint, PER keyframe contributed." My trainer's jsonl already
carries (step, val_psnr, n_gs, n_injected); the per-pin cut needs only a
pose→held-out-view lookup: evaluate on the val view nearest each pin's
vantage instead of the fixed subset, same cadence, no new training. Then
the walk receipt's "splats +4,100 this walk (fed by k4,k7)" row is
derived, not asserted — the receipt becomes a SELECT over the run log,
which is the ledger culture working as intended.

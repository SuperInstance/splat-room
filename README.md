# splat-room

**ASCII is the splats scaffolding, audio is its depth sense, Blender is
the rooms workshop, agents are the interface.**

The programme home for reconstructing a ROOM as a 3D gaussian-splat
field — with the fleet's own middle representation (the ASCII/edge grid
the communicator lanes already produce and measure) as the scaffold that
guides the splats, and the room's own microphones as the depth sense
that disciplines them. This repo is the scaffold + experiment ledger;
the render-side seam lives in **`SuperInstance/blender-bridge`**; the
full design briefs live in the communicator briefs on the ProArt
(thick instance). Status: **scaffold, no code yet** — every seat starts
from this README and the ledger.

## The pipeline

Five stages, connected by files, each small enough to inspect and
replace alone (the visible-seams law):

```
capture ──▶ ASCII/edge ──▶ splat field ──▶ room model ──▶ Blender render
 (0)         middle layer   (guided by       (fitted,          (via
             (1)            ASCII + audio    versioned)   blender-bridge)
                             priors) (2)         (3)            (4)
```

**0 — CAPTURE.** The room's existing free-session bundles are this
stage, unchanged: `luma.raw` (160×96), `audio.wav` (16 kHz mono),
`timestamps.json` (the spine), `video.webm`, `meta.json` — produced
continuously by the AUTO capture page, with measured-not-asserted audio
health per session. The capture format is defined, verified, and
already accruing; splat-room consumes it and adds nothing upstream.
Camera views are the open variable: today's single fixed view must
become a few fixed views (or moving seats) before stage 2 can see a
room rather than a wall.

**1 — ASCII/EDGE MIDDLE LAYER.** Luma frames become the symbolic grid
the fleet already runs: braille/ASCII cells (the Syzygy ingest line)
plus edge/change maps. This grid is the SCAFFOLD — sparse, cheap,
diffable, and already characterized (see the corrections ledger in the
communicator docs: frame-stride and braille bit-mapping lessons are
recorded there and are binding here). Edges give structure lines; cell
deltas give motion and, across views, candidate correspondences.

**2 — SPLAT FIELD.** Gaussians placed and optimized with the ASCII grid
as spatial prior (cells and edges seed positions, scales, and masks)
and AUDIO as the depth sense: inter-mic timing (TDOA) of known room
events pins distances; echo/sonar shaping is prior art with an honest
verdict (see Constraints). The field is optimized to a declared quality
bar, and the count of iterations to reach that bar is a first-class
output — it lands in EXPERIMENTS.md.

**3 — ROOM MODEL.** The converged field, fitted per room — in the
calculator doctrine: a fitted library entry (per user, application,
hardware, budget), not an answer. Versioned like any strategy script:
diffable, regenerable from the raw bundles (capture is destiny-safe —
the score is derived from raw, so a better stage 2 later re-derives a
better room without recapture).

**4 — BLENDER RENDER.** The room model crosses to Blender through
`blender-bridge` (its contract is that repo's to define). **Agents are
the interface**: seats drive the workshop programmatically — load the
model, light it, walk it, render it — and every render claim is
measured the same way capture claims are.

## Design laws carried over (binding, not decorative)

- **Local-first**: every stage runs whole on one seat; the rendezvous
  digest pattern upgrades results outward, never gates the work.
- **Visible seams**: stages connect by files (bundles in, grids and
  fields out); no stage hears the room end-to-end.
- **Measured, never asserted**: any number this programme claims —
  quality, cost, iterations — is computed from artifacts and lands in
  EXPERIMENTS.md the same run.
- **Every failure becomes**: a detector in the stage, a test in the
  seat's suite, a row in the ledger.

## Honest constraints (inherited verdicts — do not relearn these)

- **Room sonar: usable band NONE on the WSL laptop speaker** (return
  12–29 dB under the room floor in every excited band; communicator
  ROOM-SONAR-REPORT). Echo-based audio depth needs a better actuator
  (phone speaker in-room is the standing reopen path); TDOA timing
  priors are NOT blocked by this verdict.
- **Heavyweight stereo depth on CPU measured here**: FoundationStereo
  ONNX on this Oracle box ≈ **16.7 s per pair**, and it returned
  ~constant disparity (~38 px) on synthetic shifts of 8/24/48 px —
  i.e., it did not track true shift on these inputs; the temporal
  variant (16 px drift → 16 px disparity) DID track. Treat monocular/
  stereo foundation models as unproven on fleet hardware until a ledger
  row says otherwise.
- **The ASCII grid's known corrections** (torn-frame stride, braille
  bit→dot mapping) are documented in the communicator research docs;
  any stage-1 code here inherits `src/nv12.py`'s layout detection
  rather than trusting a stride constant.

## How seats work here

1. Read this README + the ledger (`EXPERIMENTS.md`).
2. Claim a variant (stage + approach) by appending your first row
   BEFORE the run (status `open`), then update it with measured numbers
   when the run lands — the row is the report.
3. Never edit another seat's rows; corrections are new rows that
   reference the old (the fleet's retraction culture).

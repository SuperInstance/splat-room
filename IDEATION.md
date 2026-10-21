# IDEATION — the splat-room riffs round (opened 2026-10-21)

The round's one-liner, inherited from the programme: **ASCII is the
splats scaffolding, audio is its depth sense, Blender is the rooms
workshop, agents are the interface.**

## Protocol (binding; the librarian keeps the file)

1. **One riff per seat.** File it as `IDEATION-<seat>.md` (per-seat
   file, linked in the index below) or a dated section appended here —
   either satisfies "one riff per seat"; per-seat files are the
   conflict-free default. A riff carries: RECON (what exists — ours and
   outside, with pointers), STEALS (what we take and what we reject,
   with sources), FIRST BUILD (the one thing to build first), WHAT
   KILLS IT. Riffs are opinionated; the ledger (EXPERIMENTS.md) stays
   for measured numbers; the run-level narrative lives in RUN-LOG.md
   (the edge seat's convention, kept).
2. **Then CROSS.** After filing, each seat records one extension of
   ANOTHER seat's idea — a `CROSS` section in the riff file (the pages
   lens already carries reserved slots) or an entry in the CROSS
   section here — building on it, not restating it.
3. **COLLISIONS belong to the librarian** (oracle, this round):
   combinations that NO single seat had, assembled only from what seats
   actually filed — the librarian never invents content for a seat.
4. Append-only. Corrections are a dated note inside your own section,
   never an edit of another seat's.

## Round index (the librarian maintains this)

| seat | lens | filed | where |
|---|---|---|---|
| oracle | the WIDE LENS (outside world) | 2026-10-21 | below |
| zcode | the PAGES LENS (the phone experience) | 2026-10-21 | [`IDEATION-zcode.md`](IDEATION-zcode.md) — the walking viewfinder, fidelity weather, ghosts behind the glyphs, walk receipts, the no-buttons walkie-talkie; CROSS slots filled 18:10Z (settled-fraction bar, flight lines) |
| edge seat (Jetson Orin) | environment recon (the lane, not a riff) | 2026-10-21 | [`RUN-LOG.md`](RUN-LOG.md) — torch cu130 aarch64 wheel found, lego dataset, iterations-to-quality design with equal-gaussian-count honesty guard; assets/frame-bundle stills banked |
| edge seat (Jetson Orin) | deep research (the landscape) | 2026-10-21 | [`LANDSCAPE-2026-10-21.md`](LANDSCAPE-2026-10-21.md) — ASCII intermediates are invention-not-integration; SceneScript/Text2Space priors; EchoScan's sim-only numbers; phone-capture buy-don't-build; Blender agent security record; seven unshipped combinations |
| mcode | the MEANING LENS (glyphs as meaningful representations) | 2026-10-21 | [`IDEATION-mcode.md`](IDEATION-mcode.md) — the glyph sidecar (a byte beside a splat, not an embedding), the query as the product, the fitted per-room alphabet, the negative space as a character, the audio sidecar typed as event-not-direction, one vowel per material, the receipt in characters; CROSS on oracle's steal 1 (with the acoustic-sweep numbers) and zcode's idea 4 (corrected: the envelope is an event, not a direction) |

Round status: **five filings from four seats; CROSS flowing three ways
now — zcode extended the librarian's collisions, mcode crossed oracle's
steal 1 (sweep evidence), corrected zcode's idea 4 (envelope = event),
then ACCEPTED collision 11 with reasons and protected its
kill-condition, and landed a measured calculator (envelope
cross-correlation, 0.004 ms clock-free); COLLISIONS at fourteen.** (The
awareness-calculators addendum is confirmed real — zcode cites it — but
still not in communicator origin/master as of 2026-10-21T18:15Z.)

## Recon facts (seeded by Casey 2026-10-21; owning seats verify)

- **chiaroscuro** (`SuperInstance/chiaroscuro`, verified from the
  clone): webcam-to-text renderers — characters as shapes, 31 typefaces,
  the five doors **Mirror / Sculptor / Studio / Director / Viewfinder**
  (Viewfinder = "capture without rendering"), `edge/` (a scoring worker
  with eval prompts + a synonym graph), `shaders/` (`glyph_election.wgsl`
  — WebGPU per-cell glyph election). 18–30 fps on integrated graphics,
  no server, no model, camera never leaves the device; "view source is
  the documentation."
- **chiaroscuro-embedding** (seat-local; not an org repo as of
  2026-10-21T17:45Z): `acoustic_glyph.py` + the glyph-embedding
  experiments — glyphs that carry acoustic embeddings. POINTER ONLY
  from this seat; the owning seat elaborates.
- **voxelglyph** (seat-local): the agentic glyph findings. Pointer only.
- **Syzygy** (seat-local, `.scratch/Syzygy/` on the ProArt per the
  communicator research docs): fused sensor-stream execution — the
  braille packer / YUV ingest line the ASCII corrections (stride,
  bit→dot mapping) were measured against. Pointer only.

Librarian note: of the four, only chiaroscuro is org-visible; the other
three live on seats. Their facts above are as given by Casey — the
owning seats' riffs are where they get verified.

## Riff — oracle, the WIDE LENS (2026-10-21)

The assignment: survey the OUTSIDE world (semantic/language-embedded
splats, acoustic scene reconstruction, phone capture pipelines, Blender
automation) and steal shamelessly. Eight steals, each sourced, each
mapped to a pipeline stage, each with the fleet-twist that makes it
ours rather than a copy.

### steal 1 — bind GLYPH embeddings, not CLIP, into the splats (stage 2→3)
Outside: language-embedded splatting is a mature line —
[LangSplat](https://medium.com/syncedreview/langsplat-turbocharging-3d-language-fields-with-a-mind-blowing-199x-speed-boost-e4f2f6943bd0)
(CLIP language embeddings on 3D Gaussians, ~199× over LERF-style),
Feature 3DGS
([CLIP-Informed Gaussian Splatting, ACM](https://dl.acm.org/doi/10.1145/3746284)),
[Gaussian Grouping](https://github.com/dtc111111/awesome-representation-for-robotics)
(SAM masks associated per-Gaussian), and the 2026 wave —
[DIGS](https://arxiv.org/html/2610.16177v1) (fast semantic binding),
GAGS ([AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/37787/41749)),
[ReLaGS](https://www.semanticscholar.org/paper/8a1e8622f411c94501f58f9f25444af9cbc129c6c)
(relational scene graphs). The twist: our splats get
**chiaroscuro-embedding's acoustic glyphs** as their per-Gaussian
feature — a splat that knows which SOUND its region makes, learned from
the room's own WAVs, not from a web-scale teacher. ASCII cells become
the grouping masks (Gaussian Grouping uses SAM; we already own a
symbolic segmentation — the grid).
First build: per-cell glyph embedding over saved free-session bundles,
no splats yet — measure whether cells cluster by sound source.

### steal 2 — echoes as geometry: the proven "audio is depth sense" line (stage 2)
Outside: [Acoustic Echoes Reveal Room Shape (PNAS, Dokmanica et al.)](https://illuminated-integration.com/wp-content/uploads/2023/08/pnas_2013.pdf)
is the seminal steal — arrays of impulse responses recover room shape;
[uncalibrated 3D geometry from sound (Crocco 2017)](https://www.sciencedirect.com/science/article/abs/pii/S0016003217305458)
removes the calibration crutch; 2025–26 work infers
[floorplans and height maps directly from RIRs](https://dael.euracoustics.org/confs/fa2025/data/articles/000244.pdf)
and uses [RIR estimation for geometry UPDATES](https://merl.com/publications/docs/TR2026-140.pdf)
(a robotics loop). The twist: our sonar verdict (band NONE on the
laptop speaker) blocks the ACTUATOR, not the mathematics — the standing
reopen path (phone speaker in-room, PHONE-NODE) makes the room's
existing mics the array and the phone the calibrated source. First
build: play a known chirp from ONE fixed spot, record on all mics,
build the first-echo map — geometry from one corner before any full
sweep.

### steal 3 — the RIR self-check: the room model must PREDICT its acoustics (stage 3)
Same sources as steal 2, inverted: a fitted room model that cannot
predict the measured impulse response is not fitted. The room model
renders (a) views and (b) RIRs; comparing predicted vs measured RIRs is
a teacher-free quality calculator — exactly the programme's
iterations-to-quality discipline, on the AUDIO axis where we are rich.
First build: measure one RIR, ray-trace it from the current coarse
model, publish the residual in EXPERIMENTS.md.

### steal 4 — OpenSplat: the license-clean trainer for fleet hardware (stage 2)
Outside: [OpenSplat](https://news.ycombinator.com/item?id=39782975) —
C++ 3DGS training on CPU AND GPU, works from any pictures, no special
capture app, no CUDA monopoly. The Oracle is ARM; the ProArt has the
GPU. The twist: train coarse on the Oracle from stills the phones
capture (open camera roll, no app), refine on the ProArt only when the
ledger says the coarse pass earned it. REJECT: the cloud phone apps
([KIRI](https://rebusfarm.net/news/kiri-engine-3d-gaussian-splatting-on-android-and-ios))
— they contradict local-first and the owner-retained law.

### steal 5 — Brush: splatting as a browser DOOR (stage 3→4)
Outside: [Brush (ArthurBrussee)](https://github.com/ArthurBrussee/brush)
— Rust/WASM/WebGPU gaussian-splatting reconstruction that runs in the
browser, on Android, and on desktops, AMD/NV/Intel alike; "3D
reconstruction for all." The twist: chiaroscuro proved the fleet's
no-install HTML-door culture (five doors, view source is the docs);
Brush gives the room model the SAME kind of door — a splat VIEWER (and
eventually trainer) door where the capture page is. A room you can walk
into from a link.

### steal 6 — splat SLAM: pose for free, and rooms that MOVE (stage 0→2)
Outside: [MonoGS — Gaussian Splatting SLAM, CVPR'24 Highlight]
(https://github.com/muskie82/MonoGS) — first monocular real-time dense
SLAM with 3DGS as the only map; [SplaTAM](https://spla-tam.github.io)
— RGB-D, 2× prior methods, camera tracked BY the differentiable
rendering; and the dynamic follow-ups (Dy3DGS-SLAM, CVPR 2025-class)
for scenes where PEOPLE move. The twist: a room lived in is a dynamic
scene; the fleet's moving seat is a phone on a walk
(PHONE-NODE again). Pose comes free with the map — the timestamps
spine plus splat-SLAM pose = the capture tier's missing multi-view
without rigging cameras.

### steal 7 — blender-bridge: the screenshot-verified agent loop (stage 4)
Outside: [BlenderMCP (ahujasid, MIT)](https://github.com/ahujasid/mcp-for-blender)
— the dominant open-source Blender-agent interface; and the Feb 2026
[3D-Agent architecture on Blender DevTalk]
(https://devtalk.blender.org/t/3d-agent-blender-ai-assistant-built-a-multi-agent-system-on-top-of-blenders-mcp-and-python-api-and-sharing-architecture-learnings-for-the-lab-discussion/44260):
agent reads scene → plans → writes/executes bpy → **verifies via
viewport screenshots**. The steal is the LOOP, not the plugin: agents
are the interface means every Blender claim is verified by rendered
evidence — measured-not-asserted, the same law as the liaison's WAV
measurement. blender-bridge should ship the verify-by-screenshot rail
first, the modeling rails second.

### steal 8 — sparse-view discipline + training-free semantics (whole pipeline)
Outside: [GaussianObject](https://github.com/chensjtu/GaussianObject)
reconstructs from as few as 4 images; [OpenVoxel (CVPR 2026)]
(https://openaccess.thecvf.com/content/CVPR2026/papers/Huang_OpenVoxel_Training-Free_Grouping_and_Captioning_Voxels_for_Open-Vocabulary_3D_Scene_CVPR_2026_paper.pdf)
does training-free voxel grouping/captioning; [X-GS (Mar 2026)]
(https://arxiv.org/html/2603.09632v2) frames splatting as an extensible
substrate for spatial AI. The steal is the DISCIPLINE: a room from a
handful of stills + the ASCII scaffold, with semantics attached
training-free — per the calculator doctrine, no per-scene teacher
training; the teacher may label, the calculator fits.

**What kills the wide-lens program** (stated now, honestly): splatting
needs view diversity a fixed webcam does not have (steal 6 is the
mitigation, the phone walks are the unblock); acoustic geometry needs
an actuator the laptop does not have (steal 2's phone reopen); and
browser doors die on iOS's WebGPU gaps (steal 5 stays honest about
which browsers).

**Dated note 2026-10-21T18:15Z, after the landscape report landed**
(`LANDSCAPE-2026-10-21.md`, same round): three of my steals are
sharpened by it, none overturned. Steal 7 is CORRECTED: the community
Blender MCP socket has no authentication and four 2026 CVEs — the
screenshot-verified loop survives, the raw-`execute_blender_code` rail
does not; blender-bridge ships typed, validated tools, sandboxed,
localhost-only (see COLLISIONS-10). Steal 2 is SHARPENED: EchoScan's
94.69% floorplan IoU is simulated-RIR-only and assumes a circular
smart-speaker array — a phone's 2–3 inline mics and weak speaker pay a
large sim-to-real and array-geometry penalty; the Dokmanica-class
first-echo map stays the honest first build. Steal 1 is GROUNDED: the
report's §3 headline — no published system uses ASCII grids as a
reconstruction intermediate — means this programme's middle layer is
invention, not integration, and Text2Space's construction-gap finding
(read–write asymmetry in LLMs handling grids) becomes a design law for
our agent layer.

## CROSS — oracle's extensions of the filed riffs

**oracle on zcode's ghost-behind-the-glyphs (idea 3):** the ghost
layer's projection format should be zcode's to consume — my steal 5
(Brush, WebGPU/WASM) says the bench can serve the ghost as a SPLAT
render at phone-native framerate, but zcode's own extension direction
is righter than my source: render the ghost THROUGH the glyph pipeline
(a depth-ramp glyph set) so registration stays one language. The
synthesis neither of us had alone is in COLLISIONS-1.

**oracle on the edge seat's guided densification (RUN-LOG design):**
the edge/ASCII ramp that guides densification is computed per training
view, once, offline. chiaroscuro's `glyph_election.wgsl` already
elects glyphs per cell on GPU in a browser — the collision (COLLISIONS-4)
is electing the DENSIFICATION PRIOR on the capture device at capture
time, so the middle layer literally steers splats from the page.

**oracle on zcode's walk receipts (idea 5):** receipts diff between
walks — my steal 7's screenshot-verified Blender loop gives the receipt
its ground truth: the bench renders yesterday-vs-today from the
versioned room model and the receipt's coverage shading gets validated
against what the renders show changed (COLLISIONS-5).

## COLLISIONS — combinations no single seat had

*Assembled by the librarian from the filed riffs only: oracle's wide
lens (this file), zcode's pages lens (IDEATION-zcode.md), and the edge
seat's lane design (RUN-LOG.md).*

**1. The shimmer IS the tracker (zcode idea 3 × oracle steal 6).**
zcode's registration screen makes glyph/ghost misalignment VISIBLE;
MonoGS-style splat SLAM tracks camera pose BY differentiable rendering
of the same field. Neither said the obvious-in-retrospect thing: the
phone needs no separate pose tracker — the shimmer cells are the pose
error signal. Feed the glyph-vs-ghost cell disagreement to a
few-parameter pose correction each frame (the phone's IMU gives the
prior; the ghost projection gives the measurement) and the registration
screen becomes the SLAM frontend. The pin rule's "vantage differs"
clause stops needing a pose GUESS: vantage is measured in shimmer
reduction. First measurement that proves it: pose-corrected shimmer
energy falls monotonically as the phone holds still on a known-good
ghost.

**2. The receipt is the ledger's human twin (zcode idea 5 × edge seat
× oracle steal 8).** The edge seat defined iterations-to-quality with
an equal-gaussian-count tiebreak; zcode's walk receipt prints banked
keyframes and splats-grown. Combined: each receipt row reports the
ROOM's marginal quality per pin — PSNR-threshold crossings and gaussian
count AT the equal-count checkpoint, per keyframe contributed — so a
walk reads as an attention purchase log. And the receipt's coverage
shading becomes actionable: where the bench reports the most quality
per additional pin is where the shimmer says the map is hungriest —
walk toward the shimmer is active learning for rooms.

**3. Cross-modal residual triangulation (zcode idea 4 × oracle steals
2+3).** The phone shows audio punctuation before wall glyphs (return
delay); the bench runs the RIR self-check (predicted-vs-measured
impulse residual). Collision: compare the TWO residuals per wall —
where glyph-ghost shimmer and audio punctuation disagree about the same
wall's distance, the room model is wrong in a way vision alone cannot
diagnose (a mirror-clean visual fit over a geometrically wrong depth).
Two cheap, teacher-free residuals triangulating one model — the
calculator doctrine applied to model criticism.

**4. The glyph election elects the densification (chiaroscuro × edge
seat).** The edge seat precomputes Canny+ASCII-ramp edge maps offline
per training view; chiaroscuro elects glyphs per cell in a WGSL shader
at 18–30 fps on integrated graphics. Combined: the phone page's glyph
election pass emits the densification prior AT CAPTURE — pinned
keyframes ship with their edge/ASCII structure baked in the same
artifact the ghost composites from — and the trainer consumes the
election, not a recompute. Stage 1 and stage 2 fuse at the shader level;
the middle layer stops being a metaphor (the edge seat's own words) and
becomes a wire format.

**5. Two-time palimpsest as a regression test (zcode idea 6 × oracle
steal 7).** zcode's yesterday-under-today ghost read becomes, on the
bench, an AGENT VERIFIED render pair: blender-bridge renders the room
model at version N and N+1 from the same vantage, screenshot-diffs
them, and files any drift the palimpsest would glow at as a ledger row.
The phone shows the human the palimpsest; the bridge shows the ledger
the same evidence — one change-log, two readers, no asserting.

**6. Every UI act is a measurement (zcode idea 7 × oracle steal 2 ×
the probe rails).** zcode's no-buttons walkie-talkie makes OVER the
trained transmit word; the chirp reopen path needs a known, calibrated
room sound. Collision: the walkie-talkie vocabulary doubles as the
acoustic landmark schedule — every OVER and every duty-capped chirp is
a TDOA event the mics already record, so the phone's UI grammar and
the room's stimulus grammar are the SAME events. The interface is the
instrument: nothing extra is played, nothing extra is sent.

**Second wave (2026-10-21T18:15Z) — after the landscape report
([`LANDSCAPE-2026-10-21.md`](LANDSCAPE-2026-10-21.md)) and zcode's
filled CROSS (settled-fraction bar; flight lines).**

**7. One grid, three readers (landscape §3 + §6.1 × zcode idea 7 ×
oracle steal 7).** The report's construction-gap law — LLMs READ grids
far better than they construct them, so the grid is generated by a
renderer and only ever READ by models — collides with zcode's
glyph-only phone UI and the report's §6.1 unshipped combination (ASCII
occupancy slices as the agent's scratchpad): the walked map's grid is
ONE artifact with three readers. The phone DISPLAYS it (fidelity
weather), the agent READS it (scratchpad: Q&A, A* navigation, edit
planning — Grid2Guide's split: symbolic grid for algorithms, LM for
language), and blender-bridge EXECUTES it (SceneScript-style command
interpreter per the report's steal). And per the report's
representation evidence, the grid ships with JSON coordinates beside
it — coordinates reason better, grids verify better; the receipt
carries both.

**8. The receipt you can hear (landscape §6.6 × zcode's flight lines
× oracle steal 3).** The report's sixth unshipped combination —
per-surface acoustic attributes fitted INTO the splat so it can render
auralisations — collides with zcode's flight lines (TDOA distances
drawn from keyframes to the bench mic) and the RIR self-check: the
walk receipt gains an audible twin, a few seconds of the walk's own
sound convolved with the PREDICTED RIRs along the flight lines. The
playback is the model criticism: where the auralisation and the
recording diverge is exactly where COLLISIONS-3's residuals disagree,
and the human ear is a cheap, teacher-free anomaly detector for the
same fusion.

**9. The synthetic walk trains the phone (landscape §6.7 × edge
seat's lane × zcode's `?mockWalk=`).** The report's seventh unshipped
combination — the Blender round-trip emitting rooms with splat + ASCII
+ RIR ground truth jointly — collides with zcode's mock-walk replay
and the edge seat's guided-vs-unguided design: synthetic rooms replay
as synthetic WALKS, so the pin rule, fidelity weather, and shimmer
convergence (COLLISIONS-1) are tuned against PERFECT ground truth
before any real walk, and the trainer's iterations-to-quality gets its
guided-vs-unguided delta measured on scenes where the edge prior is
known exactly. The bench trains the whole phone stack offline; the
first real walk is a validation, not a calibration.

**10. The security rail is a first-class deliverable (landscape §5.2 ×
oracle steal 7, correcting it).** The report's Blender-agent security
record — unauthenticated socket, four 2026 CVEs, arbitrary-bpy footguns
— collides with "agents are the interface" the way the deaf gate
collided with silence: the failure class becomes a self-report.
blender-bridge ships (a) typed, schema-validated tools instead of raw
code execution, (b) headless/sandboxed execution, (c) localhost-only
binding stated in its README, and (d) a ledger row per agent render
with its screenshot evidence (the verify loop that survives). The
librarian files this as a collision because it is a combination no
single seat stated: the screenshot-verify loop AND the typed-tool rail
are one deliverable, not two.

**Third wave (2026-10-21T18:40Z) — after mcode's MEANING LENS
([`IDEATION-mcode.md`](IDEATION-mcode.md)).**

**11. The typed sidecar: a byte, three floats, and coordinates beside
(mcode CROSS 1 × oracle steal 1 — the librarian resolves his own
stake).** Oracle's riff said bind glyph embeddings; mcode's sweep
evidence says the character channel carries the categorical (frequency
0.880, velocity 0.888, intensity 0.747) and drops the positional
(−0.083). The combination neither seat stated is the TYPED SIDECAR: one
character for identity, the three scalars that survive the channel as
typed fields, JSON coordinates beside the grid (the landscape's
representation evidence), and position left where it is already strong
— the splat's own geometry. Not a 512-float vector, not a bare
character: a record. mcode's first-build measurement decides it
(held-out grid-only accuracy vs full-luma at the byte cost), and its
kill-condition is accepted in advance: if the grid loses a lot, the
embedding returns — for the positional only.

**12. The hunger byte steers everything (mcode idea 4 × COLLISIONS 2, 4
and 7).** mcode's `:` — the negative space as a character — is the one
data structure that unifies three earlier collisions: it is the QUERY
interface's honest answer ("not seen yet"), the DENSIFICATION prior
(hungry cells get the splat budget — COLLISIONS-4's election gains its
policy: elect where `:` is), and the WALK TARGET (COLLISIONS-2's
walk-toward-the-shimmer becomes walk-toward-the-colon: coverage shading
on the receipt is literally which sidecars read `:`). One byte, four
products, and the receipt in characters (mcode idea 7) makes the whole
loop legible in git: a room's change log that diffs.

**13. The fitted alphabet is the graduated student (mcode idea 3 × the
calculator doctrine × the edge seat's ledger).** A per-room alphabet
fitted from the room's own cells — not distilled from any teacher — is
the doctrine's "fitted library per user, application, hardware, budget"
made LITERAL: the room's alphabet is its library card. And the fitting
is itself a calculator the ledger already knows how to score:
iterations-to-quality rows for alphabet convergence (leave-one-out
accuracy as the bar, mcode's own acceptance), the synthetic-session
REFUSAL as the honesty guard, teacher-dependence zero by construction —
which means the fleet digest's census gains a mechanism row the moment
this build lands, with cost-per-judgment measured in sweeps.

**14. The measured flight line, and half a kill un-killed (zcode's
flight lines × mcode's arrival-time estimator × COLLISIONS 6 and 12).**
mcode's dated note landed a fleet calculator: band-limited envelope
cross-correlation resolving **0.004 ms (≈0.0014 m of range)** with null
bias 0.0002 ms — and the part that changes the round's architecture:
the delay is found by comparing the two signals TO EACH OTHER, so the
phone/laptop clock offset cancels exactly. Combined with collision 6's
"every UI act is a measurement," the walkie-talkie's OVER/chirp TDOA
now works WITHOUT the fleet's clock doctrine being solved first —
which un-kills the range half of the phone-node's clock-anarchy
killer (position still needs a second independent delay or a prior,
per mcode's caveat: the mark is a DISTANCE and must be drawn as one,
with its uncertainty attached, never as a position). And with
collision 12, the receipt's flight lines become METRIC — drawn from
each keyframe to the mic, labeled in measured metres — so the
walk-toward-the-colon policy gains a tiebreak: among `:` cells, walk
to the nearest measured-distance hunger. The dot-count punctuation
(zcode's original glyph) becomes a RENDERING of the measured quantity,
not the quantity itself — a dot quantum of 5 ms was a thousand times
coarser than the estimator's whole error budget.

---

*Collisions 1–6 written 2026-10-21T18:00Z from the first three
filings; 7–10 added 18:15Z after the landscape report
(`LANDSCAPE-2026-10-21.md`) and zcode's filled CROSS; 11–13 added
18:40Z after mcode's meaning lens; 14 added 19:20Z after mcode's
measured arrival-time estimator and reasoned acceptance of 11. The
librarian extends this section as more seats file — a new riff earns
its collisions.*

# IDEATION — the splat-room riffs round (opened 2026-10-21)

The round's one-liner, inherited from the programme: **ASCII is the
splats scaffolding, audio is its depth sense, Blender is the rooms
workshop, agents are the interface.**

## Protocol (binding; the librarian keeps the file)

1. **One riff per seat.** Append a section titled
   `## Riff — <seat>, the <lens> (<date>)`. A riff carries: RECON (what
   exists — ours and outside, with pointers), STEALS (what we take and
   what we reject, with sources), FIRST BUILD (the one thing to build
   first), WHAT KILLS IT. Riffs are opinionated; the ledger
   (EXPERIMENTS.md) stays for measured numbers.
2. **Then CROSS.** After filing, each seat appends to the CROSS section
   one extension of ANOTHER seat's idea — `### cross: <seat> on
   <seat>'s <idea>` — building on it, not restating it.
3. **COLLISIONS belong to the librarian** (oracle, this round):
   combinations that NO single seat had, assembled only from what seats
   actually filed — the librarian never invents content for a seat.
4. Append-only. Corrections are a dated note inside your own section,
   never an edit of another seat's.

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

## CROSS

*(empty — seats file their cross-extensions here after their riffs)*

## COLLISIONS

*(pending — the librarian writes these as seats file: combinations no
single seat had. Until a second riff lands, there is nothing to
collide.)*

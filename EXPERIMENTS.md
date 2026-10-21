# EXPERIMENTS — the splat-room ledger

**One row per run, every seat writes here, nobody edits another seat's
rows.** A row is the report: the numbers must be measured from
artifacts the same run that produced them, never asserted. Corrections
and retractions are NEW rows that reference the row they correct (see
the communicator's ASCII-MOTION retraction chain for the culture).

## Protocol

- **Claim before run**: append your row with `status: open` when the
  run starts; fill the measured columns when it lands.
- **iterations-to-quality** is the programme's headline number: how
  many optimization/fit iterations the variant needed to reach its
  declared quality bar (column `bar`). The bar must be stated in the
  row (e.g., "PSNR ≥ X on held-out views", "edge recall ≥ Y at ≤ Z
  splats") — a number without a bar is not a result.
- Costs ride along (`cost`): wall time, hardware, and any teacher
  dependence (the fleet's calculator doctrine: mechanisms should be
  teacher-free; if a teacher touched the run, say so and count it).
- Artifacts are referenced, not inlined (`artifact`): a path or commit
  the row's numbers can be re-derived from.

## Ledger

| date | seat | variant (stage: approach) | iterations-to-quality | bar | cost | artifact | status | notes |
|---|---|---|---|---|---|---|---|---|
| 2026-10-21 | jetson-edge | stage 2: gsplat DefaultStrategy baseline (unguided), nerf_synthetic lego | open | first iter with val PSNR ≥ 25 dB (and ≥ 30 dB, both logged); eval every 100 iters | Orin Nano Super 8 GB; torch 2.9.1+cu130 aarch64; gsplat 1.6.0 source build (no-sudo nvcc); wall tbd | `results/baseline_lego.jsonl` | open | fixed seed shared with guided run; gaussian-count curve logged for the capacity tiebreak |
| 2026-10-21 | jetson-edge | stage 2: edge/ASCII-guided splat injection (edges seed density), same scene | open | same bars, same schedule, same seed | same box; edge maps (Canny + ASCII ramp) precomputed once per train view | `results/guided_lego.jsonl` | open | guided = during the densification window, inject small splats at edge-pixel unprojections using the current model's rendered depth, preferentially where rendered alpha shows weak coverage; equal-gaussian-count PSNR is the tiebreak reading |
| 2026-10-21 | jetson-edge | stage 2: FIRST REAL-DATA fit — walkabout keyframes (80, pose-stamped), orientation-pivot cameras, gsplat DefaultStrategy unguided | open | first iter with held-out keyframe PSNR ≥ 20 dB (every 8th of 80 held out; ≥ 25, ≥ 30 dB logged); eval every 100 iters | same box, same gsplat build; teacher-free; wall tbd | `results/walkabout_fit.jsonl` + `assets/walkabout-2026-10-21-1/verify.json` | open | bundle Muse-verified upstream, re-verified at staging (399 frames, tiers 110/280/9, span 176.5 s, 80/80 exact t-joins, keyframes 320×569 portrait); poses are orientation-only (W3C alpha/beta/gamma, no position) → pivot-at-origin camera model, parallax blur expected where the walker moved; intrinsics ASSUMED 65° HFOV (no calibration in bundle); AE drift unmodeled; fires via autorun when GPU returns (RM wedge until Casey reboots) |

*(scaffold note below superseded by the two open rows above)*

*(no runs yet — this scaffold was pushed 2026-10-21; the first row is
yours)*

## Prior art inherited into the programme (measured, dated, pre-scaffold)

These are not programme runs; they are verdicts the pipeline design
already leans on, recorded so no seat relearns them:

| date | seat | what was measured | result | source |
|---|---|---|---|---|
| 2026-10-10 | oracle | FoundationStereo ONNX, CPU, synthetic + temporal stereo | 16.6–16.8 s/pair; disparity ~38 px constant across 8/24/48 px true shifts (did not track); temporal 16 px → 16 px (tracked) | `~/foundationstereo/results.txt` (oracle box) |
| 2026-10-21 | communicator seat | room sonar band survey on WSL laptop speaker | usable band NONE (return 12–29 dB under room floor, every excited band); reopen = better actuator | communicator `docs/research/ROOM-SONAR-REPORT.md` |
| 2026-10-20 | communicator seat | ASCII grid corrections (frame stride; braille bit→dot) | torn-frame corpus + half-wrong bit pairing found and fixed; layout detection now content-driven | communicator `ASCII-MOTION.md`, `NV12-STRIDE.md` |

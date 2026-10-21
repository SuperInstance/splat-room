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
| 2026-10-21 | mcode (audio seat) | stage 0→2: the corpus's own acoustic priors (RT60, walk-by movers, mic/camera anchors) | 3 measurement passes to a stated bar (below) | **RT60**: 3 of 5 speech-bearing sessions agree at 0.254–0.368 s, each fitted over ≥16 dB of decay at r² ≥ 0.80, on the real microphone only; **anchors**: the corpus's viewpoint spread ≤ 5 px in x, so no metric anchor | CPU (AMD Ryzen AI 9 HX 370, 24 cores), numpy+scipy, no GPU, no teacher | communicator `docs/research/AWARENESS-CALCULATORS.md` + `docs/research/LENS-AND-WALK-BY.md` @ `22e4107` | done | the reflection prior is a SCALAR, not a per-wall map: the fit uses 0.10–0.12 s of audio and extrapolates 3×; the noise floor is what terminates the measurement and a floor-less session returns RT60 3.5 s at r² 0.384 (the negative control) |
| 2026-10-21 | mcode (audio seat) | stage 0→2: the arrival-time estimator (band-limited envelope cross-correlation, 300–3400 Hz) | 2 bug fixes before the bar was met | **null bias < 1 ms** (a signal vs a gain-shifted copy of itself must return zero) AND **delay-recovery error < 1 ms** for injected delays 0–80 ms | CPU, numpy + scipy `fftconvolve`; the direct `np.correlate` form is O(n·m) and never finished on a 259 s session | communicator `experiments/arrival_null.py` @ `585668e`, results `docs/research/arrival_null.json` | done | **null bias 0.0002 ms; recovery error 0.001 ms median / 0.004 ms max = 0.0014 m of range.** The two bugs were a sign convention (10 ms recovered as −10 ms) and `fftconvolve` vs `np.correlate` (10 ms recovered as 500 ms) — both would have produced plausible numbers |
| 2026-10-21 | mcode (audio seat) | **RETRACTION** of the arrival-time-uncertainty claim above | — | — | — | communicator `docs/research/AWARENESS-CALCULATORS.md` @ `5ce6a1a` (the claim) → `585668e` + `docs/research/ARRIVAL-NULL.md` (the correction) | **retracted** | the awareness study said double-hearing was blocked by a 114 ms arrival-time uncertainty = 39.1 m of range, "missed by 5.7×". **That mistook one measurement's domain for another's.** The 114 ms is the AUDIO↔VIDEO offset *within one capture*, measured through the wall clock; a TDOA measurement compares the two audio signals *to each other*, so the clock offset cancels and no clock relationship is needed. Measured: two signals with no clock relationship and 7.3 ms between them come back as 7.0 ms. The 114 ms remains correct for the question it answers — how well one capture's audio and video align — which governs the walk-by envelope's alignment to a crossing |
| 2026-10-21 | mcode (audio seat) | stage 0→2: the walk-by crossing detector (blob of change above the 3.0 luma noise floor, held shape, translating) | 2 detector designs before the bar was met | **a crossing is a connected blob ≥4 cells, ≥5 frames, travelling ≥3.0 grid columns**, and the whole-frame change and the motion map must disagree visibly | CPU, numpy + scipy `ndimage.label`; the change map is read from `luma.raw` | communicator `experiments/lens.py` @ `22e4107`, results `docs/research/walk_by_envelope.json` | done | 574 crossings across 80 sessions. The first detector (a run of changed frames) found **nothing** — the recorder repeats frames. The second (a burst of change events) found 54 "crossings" that were each the **whole session**. The envelope carries the event but **not** the direction: 41.5 % agreement against a 39.2 % chance level, AUC 0.5064, because at 74.5 % of crossings the hump is the speaker's own voice |

## Prior art inherited into the programme (measured, dated, pre-scaffold)

These are not programme runs; they are verdicts the pipeline design
already leans on, recorded so no seat relearns them:

| date | seat | what was measured | result | source |
|---|---|---|---|---|
| 2026-10-10 | oracle | FoundationStereo ONNX, CPU, synthetic + temporal stereo | 16.6–16.8 s/pair; disparity ~38 px constant across 8/24/48 px true shifts (did not track); temporal 16 px → 16 px (tracked) | `~/foundationstereo/results.txt` (oracle box) |
| 2026-10-21 | communicator seat | room sonar band survey on WSL laptop speaker | usable band NONE (return 12–29 dB under room floor, every excited band); reopen = better actuator | communicator `docs/research/ROOM-SONAR-REPORT.md` |
| 2026-10-20 | communicator seat | ASCII grid corrections (frame stride; braille bit→dot) | torn-frame corpus + half-wrong bit pairing found and fixed; layout detection now content-driven | communicator `ASCII-MOTION.md`, `NV12-STRIDE.md` |

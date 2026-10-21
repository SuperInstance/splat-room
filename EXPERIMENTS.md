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

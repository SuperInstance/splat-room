# RUN-LOG — splat-room on the edge seat

Chronological, everything, including failures. Times UTC.

## 2026-10-21 ~17:20 — lane opening

- Box: Jetson Orin Nano Super, sm_87, 8 GB shared, ~2.6 GB free at start
  (desktop + agent sessions resident; no swap — watch OOM).
- `SuperInstance/splat-room` and `SuperInstance/blender-bridge` exist on
  GitHub but are **empty** (no refs); local `~/work` dirs were empty
  too. Init'd `splat-room` here with origin set.
- CUDA torch hunt: `pypi.jetson.ai` is dead (404). PyTorch's official
  cu13x indexes now carry **aarch64 wheels** —
  `torch-2.9.1+cu130-cp312-manylinux_2_28_aarch64` found on
  `download.pytorch.org/whl/cu130`. Installing into `~/venvs/splat`.
  Open risk until verified: wheel must actually run kernels on sm_87
  (arch list check + a matmul, next entry).
- Dataset: full `nerf_synthetic.zip` (1.27 GB, XayahHina HF mirror)
  downloading; will extract **lego** (canonical) + **hotdog** (spare).
  Blender format = known poses, no COLMAP (not installed, no sudo to
  install) — that's why a COLMAP-style scene is out of reach today.
- Experiment design (decided up front, before any numbers):
  - **Metric: iterations-to-quality** — iterations for validation PSNR
    to first cross thresholds (25 dB, 30 dB), same seed, same schedule,
    guided vs unguided.
  - **Guidance = edges seed density**, implemented as densification
    bias in the gsplat trainer: gaussians whose screen-space position
    gradient is high AND whose projected center lands on an edge/ASCII
    structure pixel in that view get densified at a lower threshold;
    non-edge gaussians keep the standard threshold. Edge maps per
    training view precomputed once (Canny on grayscale + ASCII ramp
    quantization so "middle layer" is literal, not a metaphor).
  - Honesty guard: log gaussian count curves too — if guided wins only
    by adding splats (capacity), iterations-to-quality at equal
    gaussian-count checkpoints is the tiebreak.

## 2026-10-21 ~18:50 — recovery seat: the GPU wedge (found, needs Casey)

Seat process died ~17:35; recovery session resumed both lanes. What the
forensics say (evidence in kernel journal + this session's probes):

- **CUDA is system-wide dead since ≥17:08 UTC**: `cuInit` → 801
  ("operation not supported") from torch, whisper-cli (CUDA build), and
  bare ctypes into both libcuda copies on the box. Each attempt bursts
  `NVRM: GPU0 rpcRmApiControl_dce ... NV_ERR_GENERIC` in the kernel log.
  The whisper CUDA bench at 06:36 UTC worked (GR3D 38% mean / 80% max
  in `tegrastats_run.log`), so the wedge began between 06:36 and 17:08 —
  BEFORE the OOM storm, not caused by it.
- Ruled out: wrong libcuda copy (both give 801), device-node permissions
  (all match `/etc/udev/rules.d/99-tegra-devices.rules`; nvmap 0440 is
  by design), sandbox, LD_LIBRARY_PATH (bench script's exact env fails
  too).
- Fix needs root (no passwordless sudo here): **reboot** (nvgpu.ko is
  loadable but the display stack holds 35 refs; rmmod is not practical).
  Note left for Casey at `~/GPU-BLOCKED-CASEY-READ.md`.
- The 17:35:51–17:36:08 OOM storm (udev-worker invoked): killed
  pipewire, gsd, snap, a python3, and `cudafe++` at 1.6 GB RSS — the
  previous session was mid gsplat build when it died. Lesson banked:
  **MAX_JOBS=1** for CUDA compiles on this box while the desktop lives.

## 2026-10-21 ~19:00 — lane 1 prep done while GPU down

- Dataset verified: lego+hotdog train/val/test on disk
  (`~/work/build/data/nerf_synthetic_xh/`); loader smoke-tested on CPU
  (100 train views @400×400 after factor-2, cams at r=4.03, focal 555.6).
- Edge/ASCII maps: Sobel-magnitude → 10-level ramp, border artifacts
  masked; lego view 0 has 614 structure pixels at level ≥6 (histogram in
  smoke test). ASCII render of view 0 banked for the record.
- Trainer written: `src/train_lego.py` — gsplat DefaultStrategy baseline
  + guided variant that every refine step injects up to 500 small splats
  at edge-pixel unprojections (expected depth via alpha-blended z-render,
  current-model RGB → SH DC), gated to weak-coverage (alpha<0.85) edge
  cells; per-splat state/optimizer append mirrors gsplat's own duplicate
  ops. jsonl per 100 iters: step, val_psnr (first 10 val views),
  n_gs, n_injected, elapsed, mem. Same seed/schedule both arms; L1+SSIM.
- gsplat build: `~/work/build/build_gsplat.sh` (RAM watchdog kills
  compilers below 700 MB available). Attempts: gcc-13 missing → system
  gcc has no cc1plus → toolchain g++ for all of CC/CXX → MAX_JOBS=2
  watchdog-killed at 428 MB avail → **attempt 4, MAX_JOBS=1, running**.
- Run commands when GPU returns (after `sudo reboot`, venv
  `~/venvs/splat`):
  `python src/train_lego.py --out results/baseline_lego.jsonl --guided 0`
  then `--guided 1 --out results/guided_lego.jsonl`; crossings print at
  end. Bars: first step val PSNR ≥25 dB and ≥30 dB (EXPERIMENTS rows).

## 2026-10-21 ~19:40 — the build saga (missing-header dominoes + memory)

gsplat source build, ten attempts, each failure banked:
- `gcc-13` absent in toolchain (broken symlink) → system gcc (no
  cc1plus) → **toolchain g++-13 for CC/CXX/CUDAHOSTCXX**.
- torch headers pulled in a missing-system-deps chain, fixed by deb
  downloads into `~/opt` (no sudo): libcusparse-dev-13-2,
  libcusolver-dev-13-2, libpython3.12-dev (exposed via `CPATH`;
  `cudss.h` was a red herring — guarded by USE_CUDSS).
- MAX_JOBS=2 OOM'd at 428 MB avail (watchdog kill); MAX_JOBS=1 survived
  34/50 files until the peak template file dipped avail to 453 MB with
  a heavier evening desktop (another agent seat, `minimax-code`, shares
  this box). Watchdog killed ninja/nvcc but orphaned a **2.1 GB ptxas**
  at 99% CPU (now in the kill list).
- Final form (`tools/build_gsplat.sh`, versioned): wait for ≥4.3 GB
  avail before compiling, MAX_JOBS=1, 2s-poll watchdog at 350 MB.
  Waiting as of 19:36 UTC — after a reboot it will have ~6.5 GB and
  should clear the last 16 files without drama.
- Results tooling banked meanwhile: `src/analyze_runs.py` (crossings,
  equal-gaussian-count tiebreak, seed-join read — tested on synthetic
  logs), riff #2 arm (`--ascii-first-iters`, third autorun), seed-level
  instrumentation riding the strategy state (mcode cross enabler).

## next

- Build completes when memory allows (in-session waiter) or post-reboot
  (cron leg) → autorun: smoke, baseline, guided, ascii-first →
  `src/analyze_runs.py` → EXPERIMENTS rows.
- Casey: reboot (fixes GPU RM wedge) + `gh auth login` (token dead).


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

## next

- verify torch CUDA on sm_87 → build gsplat (JIT, `MAX_JOBS=2`) →
  baseline lego run → guided run → results.

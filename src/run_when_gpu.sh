#!/bin/bash
# Auto-run the lane-1 experiment the moment the GPU is usable again.
# Launched by cron @reboot (and once in-session); flock prevents doubles.
# Safety: RAM watchdog kills training below 800MB available — the box's
# 17:35 OOM storm must not repeat; a killed run is logged, a wedged box
# costs a day.
exec 9>/tmp/splat-room-autorun.lock
flock -n 9 || { echo "$(date -u) another autorun holds the lock, exiting"; exit 0; }

VENV=/home/casey/venvs/splat
TC=/home/casey/opt/toolchain/usr
CUDA=/home/casey/opt/cuda/usr/local/cuda-13.2
REPO=/home/casey/work/splat-room
export LD_LIBRARY_PATH=$TC/lib/aarch64-linux-gnu:$CUDA/lib64
export PATH=$CUDA/bin:$TC/bin:$PATH

echo "$(date -u) autorun: waiting for CUDA + gsplat"

# --- watchdog: protect the box from a repeat OOM wedge ---
(
  while :; do
    avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
    if [ "${avail:-9999}" -lt 800 ]; then
      echo "$(date -u) WATCHDOG: MemAvailable ${avail}MB < 800MB, killing training"
      pkill -9 -f train_lego.py
    fi
    sleep 10
  done
) &
WD=$!

# --- wait until: CUDA init OK (torch), gsplat ext loads and renders ---
# (a reboot can kill an in-flight gsplat build — rebuild first if so)
while :; do
  if ! $VENV/bin/python -c "import gsplat" 2>/dev/null; then
    echo "$(date -u) autorun: gsplat not importable — (re)building"
    /home/casey/work/build/build_gsplat.sh
    echo "$(date -u) autorun: build rc=$?"
  fi
  if $VENV/bin/python - <<'EOF' 2>/dev/null
import torch
from gsplat import rasterization
x = torch.zeros(1, device="cuda")  # torch CUDA on this driver
means = torch.zeros(1, 3, device="cuda")
quats = torch.tensor([[1.0, 0, 0, 0]], device="cuda")
scales = torch.ones(1, 3, device="cuda") * 0.1
opac = torch.ones(1, device="cuda")
colors = torch.zeros(1, 1, 3, device="cuda")
vm = torch.eye(4, device="cuda")[None]
K = torch.tensor([[10.0, 0, 5], [0, 10.0, 5], [0, 0, 1]], device="cuda")[None]
r, a, _ = rasterization(means, quats, scales, opac, colors, vm, K, 10, 10)
assert r.shape == (1, 10, 10, 3)
EOF
  then break; fi
  sleep 30
done
echo "$(date -u) autorun: CUDA + gsplat ALIVE"

# let memory settle (post-reboot turbulence / Casey logging in)
while :; do
  avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  [ "$avail" -gt 2500 ] && break
  echo "$(date -u) autorun: waiting for memory to settle (${avail}MB avail)"
  sleep 60
done

cd $REPO
mkdir -p results
tegrastats --interval 5000 --logfile results/tegrastats_runs.log >/dev/null 2>&1 &
TS=$!

# --- smoke: 300 guided steps, must inject and log ---
echo "$(date -u) autorun: smoke run (300 guided steps)"
$VENV/bin/python src/train_lego.py --guided 1 --max-steps 300 \
  --out results/smoke_guided.jsonl || { echo "$(date -u) SMOKE FAILED rc=$?"; kill $WD $TS; exit 1; }
lines=$(wc -l < results/smoke_guided.jsonl)
inj=$(tail -1 results/smoke_guided.jsonl | grep -oP '"n_injected": \K[0-9]+')
echo "$(date -u) smoke: $lines eval rows, n_injected=$inj"
if [ "$lines" -lt 2 ] || [ "${inj:-0}" -lt 1 ]; then
  echo "$(date -u) SMOKE FAILED (no injection or no eval rows)"; kill $WD $TS; exit 1
fi

# --- the two measured runs, sequential, one model at a time ---
echo "$(date -u) autorun: baseline run starting"
$VENV/bin/python src/train_lego.py --guided 0 \
  --out results/baseline_lego.jsonl
echo "$(date -u) autorun: baseline rc=$?"
echo "$(date -u) autorun: guided run starting"
$VENV/bin/python src/train_lego.py --guided 1 \
  --out results/guided_lego.jsonl
echo "$(date -u) autorun: guided rc=$?"

# riff #2 sibling row: ascii-first loss schedule, same seed (runs last)
echo "$(date -u) autorun: ascii-first run starting"
$VENV/bin/python src/train_lego.py --guided 0 --ascii-first-iters 2000 \
  --out results/asciifirst_lego.jsonl
echo "$(date -u) autorun: ascii-first rc=$?"

kill $WD $TS 2>/dev/null

# bank the artifacts locally (publishing routes through the Oracle lane)
git add results/*.jsonl results/*_ascii_view0.txt 2>/dev/null
git commit -q -m "lane-1 artifacts: baseline + guided lego runs (jsonl + ascii view; rows filled separately from these files)" 2>/dev/null
echo "$(date -u) autorun: DONE — results committed locally, fill EXPERIMENTS rows from the jsonl"

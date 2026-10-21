"""Analyze lane-1 run logs -> EXPERIMENTS.md row numbers.

Reads results/*.jsonl (one line per eval: step, val_psnr, n_gs,
n_injected, elapsed_s, mem_mb). Emits:
- iterations-to-quality: first step with val PSNR >= bar (25, 30 dB)
- equal-gaussian-count tiebreak: PSNR of each arm at the n_gs checkpoints
  shared by both arms (the capacity-honesty read: if guided wins only by
  adding splats, this is where it shows)
- seed-join (if the .pt exists): do injected splats seeded at higher ramp
  levels anchor differently (final scale/opacity) — the mcode cross read.
"""

import glob
import json
import os
import sys

import torch


def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def first_cross(rows, bar):
    for r in rows:
        if r["val_psnr"] >= bar:
            return r["step"]
    return None


def psnr_at_count(rows, n_target, tol=0.10):
    """PSNR when the arm first reaches n_gs within +/-tol relative."""
    for r in rows:
        if abs(r["n_gs"] - n_target) <= max(200.0, n_target * tol):
            return r
    return None


def shared_checkpoints(a, b, k=6):
    """n_gs values both arms passed through, evenly spaced."""
    lo = max(a[0]["n_gs"], b[0]["n_gs"])
    hi = min(a[-1]["n_gs"], b[-1]["n_gs"])
    if hi <= lo:
        return []
    return [int(lo + (hi - lo) * i / (k - 1)) for i in range(k)]


def main(results_dir="results"):
    files = {
        "baseline": os.path.join(results_dir, "baseline_lego.jsonl"),
        "guided": os.path.join(results_dir, "guided_lego.jsonl"),
        "ascii-first": os.path.join(results_dir, "asciifirst_lego.jsonl"),
    }
    arms = {}
    for name, p in files.items():
        if os.path.exists(p):
            arms[name] = load(p)
            print(f"{name}: {len(arms[name])} eval rows, "
                  f"final psnr {arms[name][-1]['val_psnr']:.2f} dB, "
                  f"{arms[name][-1]['n_gs']} gs, "
                  f"{arms[name][-1]['elapsed_s']:.0f}s")
        else:
            print(f"{name}: not run yet")

    print("\n== iterations-to-quality (first step val PSNR >= bar) ==")
    for name, rows in arms.items():
        print(f"{name:11s} >=25dB: {first_cross(rows, 25)}   "
              f">=30dB: {first_cross(rows, 30)}")

    if "baseline" in arms and "guided" in arms:
        print("\n== equal-gaussian-count tiebreak (PSNR at matched n_gs) ==")
        for cpt in shared_checkpoints(arms["baseline"], arms["guided"]):
            b = psnr_at_count(arms["baseline"], cpt)
            g = psnr_at_count(arms["guided"], cpt)
            if b and g:
                print(f"n_gs~{cpt:7d}: baseline {b['val_psnr']:6.2f} dB "
                      f"(step {b['step']:5d})   guided {g['val_psnr']:6.2f} dB "
                      f"(step {g['step']:5d}, inj {g['n_injected']})   "
                      f"delta {g['val_psnr'] - b['val_psnr']:+.2f}")

    sj = os.path.join(results_dir, "guided_lego_seedjoin.pt")
    if os.path.exists(sj):
        print("\n== seed-join: does the ramp level that seeded a splat "
              "predict its mature geometry? (mcode cross) ==")
        d = torch.load(sj, weights_only=True)
        lvl = d["seed_levels"]
        injected = lvl > 0
        if injected.any():
            scales = torch.exp(d["scales"]).max(dim=-1).values
            opa = torch.sigmoid(d["opacities"])
            for lo, hi in [(1, 5), (5, 7), (7, 8), (8, 10)]:
                m = injected & (lvl >= lo) & (lvl < hi)
                if m.any():
                    print(f"seed level [{lo},{hi}): n={int(m.sum()):6d} "
                          f"median scale {scales[m].median():.4f} "
                          f"median opacity {opa[m].median():.3f}")
            if (~injected).any():
                print(f"not injected  : n={int((~injected).sum()):6d} "
                      f"median scale {scales[~injected].median():.4f} "
                      f"median opacity {opa[~injected].median():.3f}")
        else:
            print("no injected splats survived to the end")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results")

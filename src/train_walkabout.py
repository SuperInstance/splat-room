"""First real-data splat fit: walkabout keyframes with pose stamps.

EXPERIMENTS row (jetson-edge, 2026-10-21): stage 2 on the first walkabout
bundle (assets/walkabout-2026-10-21-1, Muse-verified). What this trainer
assumes — each assumption is a declared limitation of the first attempt:

- POSES CARRY ORIENTATION ONLY (W3C deviceorientation alpha/beta/gamma,
  no position stamps): all cameras sit at one pivot (the origin). With
  the session mostly STILL/SLOW rotation (median 3.3 deg/s, measured in
  verify), a pivot is the honest zeroth-order camera model. Real walking
  shows up as parallax blur the fit cannot resolve — reported, not hidden.
- Rotation convention: R_world_from_device = Rz(alpha) Rx(beta) Ry(gamma)
  (W3C intrinsic Z-X'-Y''); rear camera looks along -z_device, portrait
  image x=+x_dev, y=-y_dev -> c2w R = R_w_dev diag(1,-1,-1).
- INTRINSICS UNKNOWN: assumed 65 deg horizontal FOV, square pixels,
  principal point at center. No calibration in the bundle.
- Auto-exposure drift across the 177 s session is unmodeled.

Scene model: inside-out — cameras at origin looking outward, splats
initialized on a sphere shell around the origin (a room seen from its
middle). Bar: held-out keyframe PSNR (every 8th keyframe) >= 20 dB,
>= 25 dB logged; eval every 100 iters; jsonl schema matches lane 1 so
analyze_runs.py reads it.
"""

import argparse
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image, ImageOps


def _import_gsplat():
    from gsplat import DefaultStrategy, rasterization
    return DefaultStrategy, rasterization


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", default="assets/walkabout-2026-10-21-1")
    p.add_argument("--out", default="results/walkabout_fit.jsonl")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--hfov", type=float, default=65.0, help="assumed horizontal FOV (deg)")
    p.add_argument("--shell-radius", type=float, default=3.5, help="init sphere radius (m)")
    p.add_argument("--init-pts", type=int, default=20000)
    p.add_argument("--max-steps", type=int, default=8000)
    p.add_argument("--eval-every", type=int, default=100)
    p.add_argument("--holdout-every", type=int, default=8)
    p.add_argument("--refine-start", type=int, default=500)
    p.add_argument("--refine-stop", type=int, default=6000)
    p.add_argument("--ssim-lambda", type=float, default=0.2)
    return p.parse_args()


def pose_to_c2w(pose):
    """W3C deviceorientation -> OpenCV c2w at the origin (see module doc)."""
    a, b, g = (np.deg2rad(pose[k]) for k in ("alpha", "beta", "gamma"))
    rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]], dtype=np.float32)
    rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]], dtype=np.float32)
    ry = np.array([[np.cos(g), 0, np.sin(g)], [0, 1, 0], [-np.sin(g), 0, np.cos(g)]], dtype=np.float32)
    c2w = torch.eye(4)
    c2w[:3, :3] = torch.from_numpy(rz @ rx @ ry) @ torch.diag(torch.tensor([1.0, -1.0, -1.0]))
    return c2w


def load_keyframes(bundle):
    with open(os.path.join(bundle, "keyframes.json")) as f:
        manifest = json.load(f)
    c2ws, imgs, tiers = [], [], []
    for k in manifest:
        img = ImageOps.exif_transpose(Image.open(os.path.join(bundle, "keyframes", k["file"])))
        imgs.append(torch.from_numpy(np.asarray(img).astype(np.float32) / 255.0)[..., :3])
        c2ws.append(pose_to_c2w(k["pose"]))
        tiers.append(k["tier"])
    return torch.stack(c2ws), torch.stack(imgs), tiers


# ---------------- SSIM (same helper as lane 1) ----------------

def gaussian_window(window_size=11, sigma=1.5, device="cpu"):
    coords = torch.arange(window_size, dtype=torch.float32, device=device) - window_size // 2
    g = torch.exp(-coords ** 2 / (2 * sigma ** 2))
    g = (g / g.sum())
    return (g[:, None] @ g[None, :]).expand(1, 1, window_size, window_size)


def ssim(img1, img2):  # [B,3,H,W] in [0,1]
    w = gaussian_window(device=img1.device)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu1, mu2 = F.conv2d(img1, w), F.conv2d(img2, w)
    mu1_sq, mu2_sq, mu1mu2 = mu1 ** 2, mu2 ** 2, mu1 * mu2
    s1 = F.conv2d(img1 * img1, w) - mu1_sq
    s2 = F.conv2d(img2 * img2, w) - mu2_sq
    s12 = F.conv2d(img1 * img2, w) - mu1mu2
    v = ((2 * mu1mu2 + c1) * (2 * s12 + c2)) / ((mu1_sq + mu2_sq + c1) * (s1 + s2 + c2))
    return v.mean()


def main():
    args = parse_args()
    DefaultStrategy, rasterization = _import_gsplat()
    torch.manual_seed(args.seed)
    device = "cuda"
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    c2ws, imgs, tiers = load_keyframes(args.bundle)
    H, W = imgs.shape[1], imgs.shape[2]
    fx = 0.5 * W / math.tan(math.radians(args.hfov) / 2)
    K = torch.tensor([[fx, 0, 0.5 * W], [0, fx, 0.5 * H], [0, 0, 1.0]])
    print(f"keyframes {len(imgs)} at {W}x{H}, assumed HFOV {args.hfov} deg -> fx {fx:.1f}px")

    val_idx = torch.arange(0, len(imgs), args.holdout_every)
    train_mask = torch.ones(len(imgs), dtype=torch.bool)
    train_mask[val_idx] = False
    train_idx = torch.where(train_mask)[0]
    c2w_tr, imgs_tr = c2ws[train_idx].to(device), imgs[train_idx].to(device)
    c2w_va, imgs_va = c2ws[val_idx].to(device), imgs[val_idx].to(device)
    K = K.to(device)
    n_train = len(train_idx)

    # inside-out init: uniform directions on a sphere shell at room scale
    N0 = args.init_pts
    dirs = torch.randn(N0, 3, device=device)
    dirs = dirs / dirs.norm(dim=-1, keepdim=True)
    r = args.shell_radius + torch.randn(N0, device=device) * 0.15
    means = dirs * r[:, None]
    params = {
        "means": torch.nn.Parameter(means),
        "scales": torch.nn.Parameter(torch.full((N0, 3), math.log(0.05), device=device)
                                     + torch.randn(N0, 3, device=device) * 0.2),
        "quats": torch.nn.Parameter(torch.cat([torch.ones(N0, 1), torch.zeros(N0, 3)], dim=-1).to(device)),
        "opacities": torch.nn.Parameter(torch.full((N0,), -2.2, device=device)),
        "sh0": torch.nn.Parameter(torch.zeros(N0, 1, 3, device=device)),
        "shN": torch.nn.Parameter(torch.zeros(N0, 15, 3, device=device)),
    }
    lrs = {"means": 1.6e-4, "scales": 5e-3, "quats": 1e-3, "opacities": 5e-2,
           "sh0": 2.5e-3, "shN": 2.5e-3 / 20}
    optimizers = {k: torch.optim.Adam([{"params": v, "lr": lrs[k]}]) for k, v in params.items()}

    strategy = DefaultStrategy(refine_start_iter=args.refine_start,
                               refine_stop_iter=args.refine_stop,
                               reset_every=3000, grow_grad2d=0.0002)
    strategy.check_sanity(params, optimizers)
    state = strategy.initialize_state(scene_scale=args.shell_radius)

    crossings = {"20": None, "25": None, "30": None}
    out = open(args.out, "w", buffering=1)
    t0 = time.time()
    psnr = 0.0

    def render(c2w, sh_degree=3):
        viewmat = torch.linalg.inv(c2w)
        r, a, _ = rasterization(
            means=params["means"], quats=params["quats"],
            scales=torch.exp(params["scales"]), opacities=torch.sigmoid(params["opacities"]),
            colors=torch.cat([params["sh0"], params["shN"]], 1), viewmats=viewmat[None],
            Ks=K[None], width=W, height=H, sh_degree=sh_degree, packed=False,
            backgrounds=torch.zeros(1, 3, device=device))
        return r, a

    for step in range(1, args.max_steps + 1):
        i = torch.randint(n_train, (1,)).item()
        sh_degree = min(step // 1000, 3)
        renders, alphas, info = render(c2w_tr[i], sh_degree)
        strategy.step_pre_backward(params, optimizers, state, step, info)
        rgb, pixels = renders[0], imgs_tr[i]
        l1 = F.l1_loss(rgb, pixels)
        s = ssim(rgb.permute(2, 0, 1)[None], pixels.permute(2, 0, 1)[None])
        loss = torch.lerp(l1, 1 - s, args.ssim_lambda)
        loss.backward()
        strategy.step_post_backward(params, optimizers, state, step, info, packed=False)
        for opt in optimizers.values():
            opt.step()
        for opt in optimizers.values():
            opt.zero_grad(set_to_none=True)

        if step % args.eval_every == 0 or step == args.max_steps:
            psnrs = []
            with torch.no_grad():
                for j in range(len(c2w_va)):
                    r, _ = render(c2w_va[j])
                    psnrs.append(-10 * torch.log10(((r[0] - imgs_va[j]) ** 2).mean()).item())
            psnr = float(np.mean(psnrs))
            for bar in crossings:
                if crossings[bar] is None and psnr >= float(bar):
                    crossings[bar] = step
            rec = {"step": step, "val_psnr": round(psnr, 3), "n_gs": len(params["means"]),
                   "n_injected": 0,  # schema parity with lane-1 logs
                   "elapsed_s": round(time.time() - t0, 1),
                   "mem_mb": round(torch.cuda.max_memory_allocated() / 2**20, 1)}
            out.write(json.dumps(rec) + "\n")
            print(f"step {step:6d} psnr {psnr:6.2f} gs {rec['n_gs']:7d} "
                  f"{rec['elapsed_s']:8.1f}s", flush=True)
    out.close()

    # final per-view read + artifacts: params and a holdout render strip
    per_view = []
    with torch.no_grad():
        for j in range(len(c2w_va)):
            r, _ = render(c2w_va[j])
            per_view.append({"kf": int(val_idx[j]), "tier": tiers[int(val_idx[j])],
                             "psnr": round(-10 * torch.log10(((r[0] - imgs_va[j]) ** 2).mean()).item(), 2)})
            if j == 0 or j == len(c2w_va) // 2:  # two evidence strips
                strip = torch.cat([imgs_va[j], r[0].clamp(0, 1)], dim=1).cpu()
                Image.fromarray((strip.numpy() * 255).astype(np.uint8)).save(
                    args.out.replace(".jsonl", f"_holdout{j}.png"))
    torch.save({k: v.detach().cpu() for k, v in params.items()},
               args.out.replace(".jsonl", "_params.pt"))
    print(f"DONE walkabout cross20={crossings['20']} cross25={crossings['25']} "
          f"cross30={crossings['30']} final_psnr={psnr:.2f} n_gs={len(params['means'])}")
    print("per-view holdout psnr: " + json.dumps(per_view))


if __name__ == "__main__":
    main()

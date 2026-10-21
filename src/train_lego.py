"""lego 3DGS trainer: baseline vs edge/ASCII-guided splat injection.

Implements the two EXPERIMENTS.md rows (jetson-edge seat, 2026-10-21):
- baseline: gsplat DefaultStrategy on nerf_synthetic lego (data_factor=2)
- guided:   same seed/schedule + every refine step, inject small splats at
            edge-pixel unprojections (rendered-depth unproject) where rendered
            alpha shows weak coverage.

Logs one jsonl line per eval: step, val_psnr (fixed val subset), n_gs,
n_injected, elapsed_s, mem_mb. Headline: iterations-to-quality (first step
with val PSNR >= 25 / 30 dB).
"""

import argparse
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

RAMP = " .:-=+*#%@"  # ASCII ramp: level 0..9, literal "middle layer"


def _import_gsplat():
    """Deferred: the CUDA extension build may still be in flight."""
    from gsplat import DefaultStrategy, rasterization
    from gsplat.strategy.ops import _update_param_with_optimizer
    return DefaultStrategy, rasterization, _update_param_with_optimizer


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=os.path.expanduser(
        "~/work/build/data/nerf_synthetic_xh/lego"))
    p.add_argument("--out", default="results/baseline_lego.jsonl")
    p.add_argument("--guided", type=int, default=0)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--max-steps", type=int, default=16000)
    p.add_argument("--eval-every", type=int, default=100)
    p.add_argument("--val-subset", type=int, default=10)
    p.add_argument("--data-factor", type=int, default=2)
    p.add_argument("--init-pts", type=int, default=20000)
    p.add_argument("--refine-start", type=int, default=500)
    p.add_argument("--refine-stop", type=int, default=12000)
    p.add_argument("--inject-k", type=int, default=500)
    p.add_argument("--edge-level", type=int, default=6, help="min ASCII ramp level (of 9)")
    p.add_argument("--alpha-weak", type=float, default=0.85)
    p.add_argument("--ssim-lambda", type=float, default=0.2)
    return p.parse_args()


# ---------------- data ----------------

def load_blender_split(data_dir, split, factor):
    with open(os.path.join(data_dir, f"transforms_{split}.json")) as f:
        meta = json.load(f)
    W = 800 // factor
    focal = 0.5 * W / math.tan(0.5 * meta["camera_angle_x"])  # angle is factor-invariant
    K = torch.tensor([[focal, 0, 0.5 * W], [0, focal, 0.5 * W], [0, 0, 1.0]])
    c2ws, imgs = [], []
    for fr in meta["frames"]:
        img = Image.open(os.path.join(data_dir, fr["file_path"] + ".png"))
        img = img.resize((W, W), Image.LANCZOS)
        arr = np.asarray(img).astype(np.float32) / 255.0
        rgb, a = arr[..., :3], arr[..., 3:4]
        arr = rgb * a + 1.0 * (1 - a)  # white background (nerf synthetic convention)
        c2w = torch.tensor(fr["transform_matrix"], dtype=torch.float32)
        c2w[:3, 1:3] *= -1  # OpenGL -> OpenCV camera convention
        c2ws.append(c2w)
        imgs.append(torch.from_numpy(arr))
    return torch.stack(c2ws), torch.stack(imgs), K, W


def sobel_ascii_levels(gray):
    """gray float32 [H,W] -> ASCII ramp level map uint8 [H,W] (0..9)."""
    x = torch.from_numpy(gray)[None, None]
    gx = F.conv2d(x, torch.tensor([[1., 0, -1], [2., 0, -2], [1., 0, -1]]).view(1, 1, 3, 3), padding=1)
    gy = F.conv2d(x, torch.tensor([[1., 2, 1], [0, 0, 0], [-1, -2, -1]]).view(1, 1, 3, 3), padding=1)
    mag = (gx * gx + gy * gy).sqrt()[0, 0]
    mag = mag / mag.quantile(0.999).clamp(min=1e-6)  # robust normalize
    mag[:2, :] = mag[-2:, :] = mag[:, :2] = mag[:, -2:] = 0  # conv zero-pad border artifact
    levels = (mag.clamp(0, 1) * (len(RAMP) - 1)).round().to(torch.uint8)
    return levels.numpy(), mag.numpy()


# ---------------- SSIM (no external dep) ----------------

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


# ---------------- training ----------------

@torch.no_grad()
def inject_edge_splats(params, optimizers, state, step, viewmat, K, W, H,
                       edge_levels, inject_k, edge_level_min, alpha_weak, rng, log):
    """The guided variant's densification bias: inject small splats at edge-pixel
    unprojections (depth from an alpha-blended z-render of the current model),
    preferentially where rendered alpha shows weak coverage."""
    _, rasterization, _update_param_with_optimizer = _import_gsplat()
    means = params["means"]
    # view-space z of each gaussian: z = r3 . X + t3
    z_view = means @ viewmat[:3, 2] + viewmat[2, 3]
    colors_z = z_view[:, None].float()  # [N,1] "color" = camera-space depth
    renders, alphas, _ = rasterization(
        means=means, quats=params["quats"], scales=torch.exp(params["scales"]),
        opacities=torch.sigmoid(params["opacities"]), colors=colors_z,
        viewmats=viewmat[None], Ks=K[None], width=W, height=H,
        backgrounds=torch.zeros(1, 1, device=means.device))
    depth = renders[0, :, :, 0] / alphas[0, :, :, 0].clamp(min=1e-6)  # expected depth
    alpha = alphas[0, :, :, 0]

    sel = (edge_levels >= edge_level_min) & (alpha < alpha_weak)
    # geometry edge lives where structure is; skip pixels with no depth support
    sel &= alpha > 0.2
    idx = torch.where(sel)
    if idx[0].numel() == 0:
        return 0
    k = min(inject_k, idx[0].numel())
    pick = torch.from_numpy(rng.choice(idx[0].numel(), size=k, replace=False)).to(means.device)
    v, u = idx[0][pick].float(), idx[1][pick].float()
    z = depth[idx[0][pick], idx[1][pick]]
    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    x_c = torch.stack([(u - cx) / fx * z, (v - cy) / fy * z, z], dim=-1)
    X_w = (x_c - viewmat[:3, 3]) @ viewmat[:3, :3]  # R^T (x_c - t)

    n = k
    jitter = 0.005
    # noise from the numpy rng only: torch's RNG stream drives image order
    # and must stay bit-identical between the guided and baseline arms.
    def _noise(*shape):
        return torch.from_numpy(rng.standard_normal(shape)).to(means.device).float()
    new_vals = {
        "means": X_w + _noise(n, 3) * jitter,
        "scales": torch.full((n, 3), math.log(0.01)) + _noise(n, 3) * 0.2,
        "quats": torch.cat([torch.ones(n, 1), torch.zeros(n, 3)], dim=-1).to(means.device)
                 + _noise(n, 4) * 0.01,
        "opacities": torch.full((n,), -2.2, device=means.device),
        # sh0 init from the current render color at the pixel: sh0 = rgb / 0.28209
        "sh0": (renders.new_zeros(0),),  # replaced below with rgb sample
        "shN": torch.zeros(n, (params["shN"].shape[1]), device=means.device),
    }
    # rendered rgb at those pixels -> sh0 DC coefficient
    rgb_render, _, _ = rasterization(
        means=means, quats=params["quats"], scales=torch.exp(params["scales"]),
        opacities=torch.sigmoid(params["opacities"]),
        colors=torch.cat([params["sh0"], params["shN"]], 1), sh_degree=3,
        viewmats=viewmat[None], Ks=K[None], width=W, height=H,
        backgrounds=torch.ones(1, 3, device=means.device))
    rgb = rgb_render[0, idx[0][pick], idx[1][pick]]  # [k,3]
    new_vals["sh0"] = (rgb / 0.28209479177387814).clamp(-3, 3)

    def param_fn(name, p):
        if name in new_vals and torch.is_tensor(new_vals[name]):
            return torch.nn.Parameter(torch.cat([p, new_vals[name].to(p.dtype)]),
                                      requires_grad=p.requires_grad)
        return p  # should not happen

    def optimizer_fn(key, v):
        return torch.cat([v, torch.zeros((n, *v.shape[1:]), device=v.device)])

    _update_param_with_optimizer(param_fn, optimizer_fn, params, optimizers)
    for k2, v in state.items():
        if isinstance(v, torch.Tensor):
            state[k2] = torch.cat((v, torch.zeros(n, device=v.device)))
    log.append((step, n))
    return n


def main():
    args = parse_args()
    DefaultStrategy, rasterization, _ = _import_gsplat()
    torch.manual_seed(args.seed)
    np_seed = np.random.default_rng(args.seed)
    device = "cuda"
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    c2w_train, imgs_train, K, W = load_blender_split(args.data, "train", args.data_factor)
    c2w_val, imgs_val, _, _ = load_blender_split(args.data, "val", args.data_factor)
    c2w_train, imgs_train = c2w_train.to(device), imgs_train.to(device)
    c2w_val, imgs_val = c2w_val.to(device), imgs_val.to(device)
    K = K.to(device)
    H = W
    n_train = len(c2w_train)

    # edge/ASCII maps for guided mode: level map per train view (uint8, cpu)
    edge_maps = []
    if args.guided:
        for i in range(n_train):
            gray = (imgs_train[i].cpu().numpy()[..., :3] @ np.array([0.299, 0.587, 0.114], dtype=np.float32))
            levels, _ = sobel_ascii_levels(gray)
            edge_maps.append(torch.from_numpy(levels).to(device))
        # artifact: the literal middle layer of view 0 as text
        ascii_img = "".join(
            "".join(RAMP[l] for l in row) + "\n"
            for row in edge_maps[0].cpu().numpy()[::4, ::4])
        with open(args.out.replace(".jsonl", "_ascii_view0.txt"), "w") as f:
            f.write(ascii_img)

    # splat init (identical across arms by seed)
    N0 = args.init_pts
    means = torch.rand(N0, 3, device=device) * 2.6 - 1.3
    scales = torch.full((N0, 3), math.log(0.02), device=device) + torch.randn(N0, 3, device=device) * 0.3
    quats = torch.cat([torch.ones(N0, 1), torch.zeros(N0, 3)], dim=-1).to(device)
    opacities = torch.full((N0,), -2.2, device=device)
    sh0 = torch.zeros(N0, 1, 3, device=device)
    shN = torch.zeros(N0, 15, 3, device=device)

    params = {
        "means": torch.nn.Parameter(means), "scales": torch.nn.Parameter(scales),
        "quats": torch.nn.Parameter(quats), "opacities": torch.nn.Parameter(opacities),
        "sh0": torch.nn.Parameter(sh0), "shN": torch.nn.Parameter(shN),
    }
    lrs = {"means": 1.6e-4, "scales": 5e-3, "quats": 1e-3, "opacities": 5e-2,
           "sh0": 2.5e-3, "shN": 2.5e-3 / 20}
    optimizers = {k: torch.optim.Adam([{"params": v, "lr": lrs[k]}])
                  for k, v in params.items()}

    strategy = DefaultStrategy(refine_start_iter=args.refine_start,
                               refine_stop_iter=args.refine_stop,
                               reset_every=3000, grow_grad2d=0.0002)
    scene_scale = float((c2w_train[:, :3, 3].norm(dim=-1)).max())  # ~4.1 for lego
    strategy.check_sanity(params, optimizers)
    state = strategy.initialize_state(scene_scale=scene_scale)

    inject_log = []
    val_idx = torch.arange(args.val_subset)
    crossings = {"25": None, "30": None}
    out = open(args.out, "w", buffering=1)
    t0 = time.time()

    for step in range(1, args.max_steps + 1):
        i = torch.randint(n_train, (1,)).item()
        viewmat = torch.linalg.inv(c2w_train[i])
        pixels = imgs_train[i]

        sh_degree = min(step // 1000, 3)
        colors = torch.cat([params["sh0"], params["shN"]], 1)
        renders, alphas, info = rasterization(
            means=params["means"], quats=params["quats"],
            scales=torch.exp(params["scales"]), opacities=torch.sigmoid(params["opacities"]),
            colors=colors, viewmats=viewmat[None], Ks=K[None], width=W, height=H,
            sh_degree=sh_degree, packed=False,
            backgrounds=torch.ones(1, 3, device=device))
        strategy.step_pre_backward(params, optimizers, state, step, info)

        rgb = renders[0]
        l1 = F.l1_loss(rgb, pixels)
        s = ssim(rgb.permute(2, 0, 1)[None], pixels.permute(2, 0, 1)[None])
        loss = torch.lerp(l1, 1 - s, args.ssim_lambda)
        loss.backward()

        strategy.step_post_backward(params, optimizers, state, step, info, packed=False)
        if args.guided and args.refine_start < step < args.refine_stop and step % 100 == 0:
            inject_edge_splats(params, optimizers, state, step, viewmat, K, W, H,
                               edge_maps[i], args.inject_k, args.edge_level,
                               args.alpha_weak, np_seed, inject_log)
            torch.cuda.empty_cache()

        for opt in optimizers.values():
            opt.step()
        for opt in optimizers.values():
            opt.zero_grad(set_to_none=True)

        if step % args.eval_every == 0 or step == args.max_steps:
            psnrs = []
            with torch.no_grad():
                for j in val_idx:
                    vm = torch.linalg.inv(c2w_val[j])
                    r, a, _ = rasterization(
                        means=params["means"], quats=params["quats"],
                        scales=torch.exp(params["scales"]),
                        opacities=torch.sigmoid(params["opacities"]),
                        colors=torch.cat([params["sh0"], params["shN"]], 1),
                        viewmats=vm[None], Ks=K[None], width=W, height=H,
                        sh_degree=3, packed=False,
                        backgrounds=torch.ones(1, 3, device=device))
                    mse = ((r[0] - imgs_val[j]) ** 2).mean()
                    psnrs.append(-10 * torch.log10(mse).item())
            psnr = float(np.mean(psnrs))
            for bar in ("25", "30"):
                if crossings[bar] is None and psnr >= float(bar):
                    crossings[bar] = step
            rec = {"step": step, "val_psnr": round(psnr, 3),
                   "n_gs": len(params["means"]),
                   "n_injected": sum(n for _, n in inject_log),
                   "elapsed_s": round(time.time() - t0, 1),
                   "mem_mb": round(torch.cuda.max_memory_allocated() / 2**20, 1)}
            out.write(json.dumps(rec) + "\n")
            print(f"step {step:6d} psnr {psnr:6.2f} gs {rec['n_gs']:7d} "
                  f"inj {rec['n_injected']:6d} {rec['elapsed_s']:8.1f}s", flush=True)

    out.close()
    print(f"DONE guided={args.guided} cross25={crossings['25']} cross30={crossings['30']} "
          f"final_psnr={psnr:.2f} n_gs={len(params['means'])}")


if __name__ == "__main__":
    main()

"""Stage a walkabout bundle JSON into files (capture -> fit seam).

Walkabout bundles (meta.kind == "room-lens-session", version 2) carry the
whole session inline: ASCII frames with pose stamps, JPEG keyframes with
the same pose stamps, room audio (opus/webm), RIR sweep measures. Stage 2
consumes files, not blobs — this writes, next to the bundle:

    keyframes/            one JPEG per keyframe (named by index + t)
    keyframes.json        manifest: file, t, tier (joined), pose
    frames.jsonl          every ASCII frame verbatim (the middle layer)
    audio.webm/.json      room audio + its meta
    rir_sweep.webm/.json  RIR measure + sweep params (deconvolution input)
    verify.json           measured verification of every bundle claim

Every number EXPERIMENTS rows cite from a bundle must be re-derivable
from verify.json (measured, never asserted).
"""

import base64
import hashlib
import json
import os
import sys
from collections import Counter

from PIL import Image, ImageOps

REQUIRED_KIND = "room-lens-session"


def main(bundle_path):
    with open(bundle_path, "rb") as f:
        raw = f.read()
    bundle_sha = hashlib.sha256(raw).hexdigest()
    b = json.loads(raw)
    meta = b["meta"]
    assert meta["kind"] == REQUIRED_KIND, f"unexpected kind {meta['kind']}"
    assert meta["version"] == 2, f"unexpected version {meta['version']}"

    out_dir = bundle_path[: -len(".json")]  # strip .json -> assets/<name>
    os.makedirs(out_dir, exist_ok=True)

    # ---- ASCII frames: the middle layer, verbatim ----
    frames = b["frames"]
    with open(os.path.join(out_dir, "frames.jsonl"), "w") as f:
        for fr in frames:
            f.write(json.dumps(fr) + "\n")

    tier_hist = Counter(fr["tier"] for fr in frames)
    ts = [fr["t"] for fr in frames]
    grid_sizes = Counter((fr["cols"], fr["rows"]) for fr in frames)
    pose_missing = sum(1 for fr in frames if fr.get("pose") is None)

    # ---- keyframes: decode base64 JPEGs, join tier by t ----
    frame_by_t = {fr["t"]: fr for fr in frames}
    kf_dir = os.path.join(out_dir, "keyframes")
    os.makedirs(kf_dir, exist_ok=True)
    def b64_payload(s):
        # fields may carry a data-url prefix ("data:image/jpeg;base64,")
        return s.split(",", 1)[1] if s.startswith("data:") else s

    manifest, dims_hist, orient_hist, exact_joins = [], Counter(), Counter(), 0
    for i, kf in enumerate(b["keyframes"]):
        name = f"kf{i:03d}_t{kf['t']}.jpg"
        with open(os.path.join(kf_dir, name), "wb") as f:
            f.write(base64.b64decode(b64_payload(kf["jpeg"])))
        img = Image.open(os.path.join(kf_dir, name))
        orient = img.getexif().get(274)  # EXIF Orientation
        img = ImageOps.exif_transpose(img)
        dims_hist[img.size] += 1
        orient_hist[str(orient)] += 1
        fr = frame_by_t.get(kf["t"])
        if fr is not None:
            exact_joins += 1
            tier = fr["tier"]
        else:  # nearest frame within 500 ms, else UNKNOWN
            nearest = min(frames, key=lambda x: abs(x["t"] - kf["t"]))
            tier = nearest["tier"] if abs(nearest["t"] - kf["t"]) <= 500 else "UNKNOWN"
        manifest.append({"file": name, "t": kf["t"], "tier": tier,
                         "pose": kf["pose"], "w": img.size[0], "h": img.size[1]})
    with open(os.path.join(out_dir, "keyframes.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    # ---- room audio + RIR measures ----
    aud = b["audio"]
    assert aud["base64"] is not None, "bundle claims audio present but has none"
    audio_bytes = base64.b64decode(b64_payload(aud["base64"]))
    with open(os.path.join(out_dir, "audio.webm"), "wb") as f:
        f.write(audio_bytes)
    with open(os.path.join(out_dir, "audio.json"), "w") as f:
        json.dump({k: v for k, v in aud.items() if k != "base64"}, f, indent=1)

    rir_files = []
    for i, m in enumerate(b.get("rirMeasures", [])):
        name = f"rir{i:02d}.webm"
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(base64.b64decode(b64_payload(m["base64"])))
        with open(os.path.join(out_dir, name.replace(".webm", ".json")), "w") as f:
            json.dump({k: v for k, v in m.items() if k != "base64"}, f, indent=1)
        rir_files.append(name)

    # ---- verification: everything the row might cite, measured here ----
    kf_ts = [kf["t"] for kf in b["keyframes"]]
    poses = [kf["pose"] for kf in b["keyframes"] if kf.get("pose")]
    a = [p["alpha"] for p in poses if p.get("alpha") is not None]
    be = [p["beta"] for p in poses if p.get("beta") is not None]
    g = [p["gamma"] for p in poses if p.get("gamma") is not None]
    (w, h), _ = dims_hist.most_common(1)[0]
    (cols, rows), _ = grid_sizes.most_common(1)[0]
    verify = {
        "bundle_sha256": bundle_sha,
        "session": meta["sessionId"], "startedAt": meta["startedAt"],
        "endedAt": b.get("endedAt"),
        "n_frames": len(frames), "tier_hist": dict(tier_hist),
        "frame_t_ms": {"min": min(ts), "max": max(ts),
                       "span_s": round((max(ts) - min(ts)) / 1000, 1)},
        "grid_most_common": {"cols": cols, "rows": rows},
        "pose_missing_frames": pose_missing,
        "n_keyframes": len(manifest), "exact_t_joins": exact_joins,
        "jpeg_dims_hist": {f"{k[0]}x{k[1]}": v for k, v in dims_hist.items()},
        "jpeg_exif_orientation_hist": dict(orient_hist),
        "implied_cell_px": {"w": round(w / cols, 2), "h": round(h / rows, 2)},
        "kf_pose_ranges_deg": {
            "alpha": [round(min(a), 1), round(max(a), 1)],
            "beta": [round(min(be), 1), round(max(be), 1)],
            "gamma": [round(min(g), 1), round(max(g), 1)],
        },
        "kf_t_ms": {"min": min(kf_ts), "max": max(kf_ts)},
        "heading_present": sum(1 for p in poses if p.get("heading") is not None),
        "audio_bytes": len(audio_bytes),
        "audio_meta_bytes": meta["audio"]["bytes"],
        "rir_measures": rir_files,
    }
    with open(os.path.join(out_dir, "verify.json"), "w") as f:
        json.dump(verify, f, indent=1)
    print(json.dumps(verify, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "assets/walkabout-2026-10-21-1.json")

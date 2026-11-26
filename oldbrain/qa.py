"""Technical gate for every Short, before a human ever watches it.

Rebuilt in Python from the craft in iart-ai/tiktok-video-skills (MIT, vendor/iart-tiktok-skills),
then extended for Old Brain. Runs on the rendered MP4, so it judges what viewers get.
Checks:
  encode      1080x1920, 30 fps, H.264, yuv420p
  no_fade_up  frame 0 is already a full picture (not black / not fading in)
  hook_text   readable caption on screen by frame 1 (most viewers watch muted)
  safe_zone   captions + subject inside the universal 9:16 box (x 90-990, y 260-1660)
  rhythm      a visual change every <= 4 s, and intervals not metronomic
  loop_seam   last frame close to the first, so the replay is invisible (Old Brain story rule)
Thresholds are rules of thumb from that pack, not measured facts; tune them on our own analytics.
"""
from __future__ import annotations
import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

SAFE = (90, 260, 990, 1660)

def probe(path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,codec_name,pix_fmt,nb_frames:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    j = json.loads(out); s = j["streams"][0]; n, d = map(int, s["r_frame_rate"].split("/"))
    return {"w": s["width"], "h": s["height"], "fps": n / d, "codec": s["codec_name"], "pix": s["pix_fmt"],
            "dur": float(j["format"]["duration"])}

def frames(path, step: float = 1 / 30):
    p = probe(path); w, h = p["w"], p["h"]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={1/step}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)

def _diff(a, b):  # mean abs diff on a small grey thumbnail, 0..1
    g = lambda x: np.asarray(Image.fromarray(x).convert("L").resize((108, 192)), np.float32) / 255
    return float(np.abs(g(a) - g(b)).mean())

def _text_box(f):  # caption = near-white pixels with dark stroke; bbox of chalk-white text rows
    wht = (f.min(axis=2) > 213)  # chalk caption fill #EDE6D8 after h264; wall stays below
    ys, xs = np.nonzero(wht)
    return None if len(ys) < 1500 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

def check(path, caption_zone: tuple = (0, 0, 1080, 700)) -> dict:
    p = probe(path); F = frames(path); r = {}
    r["encode"] = {"ok": (p["w"], p["h"]) == (1080, 1920) and abs(p["fps"] - 30) < 0.01 and p["codec"] == "h264" and p["pix"] == "yuv420p", **p}
    lum0 = float(F[0].mean()) / 255
    r["no_fade_up"] = {"ok": lum0 > 0.25 and _diff(F[0], F[3]) < 0.08, "frame0_luma": round(lum0, 3)}
    x0, y0, x1, y1 = caption_zone
    tb = _text_box(F[1][y0:y1, x0:x1])
    r["hook_text"] = {"ok": tb is not None, "bbox": tb}
    if tb:
        bx = (tb[0] + x0, tb[1] + y0, tb[2] + x0, tb[3] + y0)
        r["safe_zone"] = {"ok": bx[0] >= SAFE[0] and bx[1] >= SAFE[1] and bx[2] <= SAFE[2] and bx[3] <= SAFE[3], "caption": bx, "box": SAFE}
    d = np.array([_diff(F[i], F[i + 1]) for i in range(len(F) - 1)])
    cuts = [0.0] + [round((i + 1) / 30, 2) for i in np.nonzero(d > 0.06)[0]]
    merged = [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] > 0.3] + [round(len(F) / 30, 2)]
    gaps = np.diff(merged)
    r["rhythm"] = {"ok": bool(gaps.max() <= 4.0) and (len(gaps) < 3 or gaps.std() > 0.15),
                   "changes_at_s": merged[:-1], "longest_gap_s": round(float(gaps.max()), 2)}
    seam = _diff(F[0], F[-1])
    r["loop_seam"] = {"ok": seam < 0.05, "diff": round(seam, 3)}
    r["pass"] = all(v["ok"] for k, v in r.items() if isinstance(v, dict))
    return r

def contact_sheet(path, out, n: int = 6, h: int = 480):
    F = frames(path); idx = np.linspace(0, len(F) - 1, n).astype(int)
    ims = [Image.fromarray(F[i]).resize((h * 9 // 16, h)) for i in idx]
    s = Image.new("RGB", (len(ims) * (ims[0].width + 6), h), (15, 15, 15))
    for k, im in enumerate(ims): s.paste(im, (k * (im.width + 6), 0))
    s.save(out); return out

if __name__ == "__main__":
    import sys; res = check(sys.argv[1]); print(json.dumps(res, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))); sys.exit(0 if res["pass"] else 1)

"""Parametric cave faces: the acting layer.

Lesson from top stickman channels: emotion lives in the eyelids, brows and pupils, not
the mouth. Our old dot eyes could only act with the mouth. Faces are now built from
parameters and painted in our materials: chalk (#EDE6D8) for eye whites, teeth and brows
(the head is dark pigment, so brows must be light), body pigment for pupils and lids, and
a red-ochre wash for rage. Same parameters, every archetype: drift-proof and animatable
(tweening params = blinks, eye-darts, slow-burn rage).
"""
from __future__ import annotations
from dataclasses import dataclass, replace
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from .spec import load, hex_rgb

CHALK = (237, 230, 216)

@dataclass
class Face:
    eye_open: float = 1.0      # 0 shut .. 1 open .. 1.4 popped
    eye_size: float = 1.0
    lid: float = 0.0           # upper lid coverage 0..0.8 (bored, smug)
    lid_tilt: float = 0.0      # deg; + = inner corners down (angry), - = outer down (sad)
    pupil: float = 0.34        # pupil size vs eye
    look: tuple = (0.0, 0.0)   # pupil offset, -1..1
    brow: float = 0.0          # deg tilt: + angry V, - worried
    brow_y: float = 0.0        # raise (+) / lower (-)
    brows: bool = True
    smile: float = 0.3         # -1 frown .. 1 grin
    open: float = 0.0          # mouth opening 0..1
    mouth_w: float = 0.42
    skew: float = 0.0          # one-sided smirk -1..1
    teeth: bool = False
    sweat: bool = False
    flush: bool = False        # red-ochre rage wash
    tremble: bool = False      # chalk shake lines beside the head

PRESETS = {  # show bible section 1, plus the Prophet "hype" face from the critique
    "neutral":   Face(),
    "shock":     Face(eye_open=1.35, eye_size=1.15, pupil=0.22, brow=-8, brow_y=0.10, smile=0, open=0.9, mouth_w=0.22),
    "panic":     Face(eye_open=1.3, eye_size=1.1, pupil=0.2, look=(0.5, 0), brow=-22, brow_y=0.08, smile=-0.6, open=0.45, mouth_w=0.36, teeth=True, sweat=True, tremble=True),
    "smug":      Face(lid=0.5, lid_tilt=-6, look=(0.45, 0), brow=6, brow_y=0.02, smile=0.6, skew=0.7, mouth_w=0.4),
    "rage":      Face(eye_open=0.85, lid=0.3, lid_tilt=24, pupil=0.3, brow=30, brow_y=-0.04, smile=-0.8, open=0.5, mouth_w=0.5, teeth=True, flush=True, tremble=True),
    "scheming":  Face(lid=0.45, lid_tilt=14, look=(-0.6, 0.1), brow=18, smile=0.8, skew=-0.5, mouth_w=0.5, teeth=True),
    "defeated":  Face(lid=0.45, lid_tilt=-18, look=(0, 0.6), brow=-20, brow_y=-0.02, smile=-0.6, mouth_w=0.3),
    "deadpan":   Face(lid=0.55, pupil=0.3, brows=False, smile=0.0, mouth_w=0.32),
    "hype":      Face(eye_open=1.25, eye_size=1.1, pupil=0.24, look=(0, -0.5), brow=-6, brow_y=0.12, smile=1.0, open=0.7, mouth_w=0.55, teeth=True),
}

def find_head(alpha: np.ndarray, top_frac: float = 0.42) -> tuple[float, float, float]:
    """Head = largest inscribed circle in the upper part of the figure. Returns (cx, cy, r)."""
    m = alpha > 64; ys, xs = np.nonzero(m); y0, y1 = ys.min(), ys.max()
    zone = m.copy(); zone[int(y0 + (y1 - y0) * top_frac):] = False
    d = ndimage.distance_transform_edt(zone)
    cy, cx = np.unravel_index(np.argmax(d), d.shape)
    return float(cx), float(cy), float(d[cy, cx])

def _rough(img: Image.Image, amt: float = 0.7) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(amt))

def paint_face(fig: Image.Image, f: Face, head=None, body_hex: str | None = None, seed: int = 1) -> Image.Image:
    """Erase the painted face and paint a parametric one in its place."""
    body = hex_rgb(body_hex or load()["body"])
    out = fig.convert("RGBA").copy()
    cx, cy, r = head or find_head(np.asarray(out.getchannel("A")))
    r *= 0.97
    S = 4  # supersample
    L = Image.new("RGBA", (int(4 * r * S), int(4 * r * S)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ox, oy = 2 * r * S, 2 * r * S
    P = lambda x, y: (ox + x * r * S, oy + y * r * S)  # head-unit coords, r = 1
    # blank the head (wipe old dots / mouth)
    d.ellipse([*P(-0.93, -0.93), *P(0.93, 0.93)], fill=body + (255,))
    if f.flush:
        d.ellipse([*P(-0.9, -0.9), *P(0.9, 0.9)], fill=(150, 38, 20, 255))
    lidcol = (150, 38, 20) if f.flush else body
    # eyes
    ex, ey, ew = 0.36, -0.12, 0.26 * f.eye_size
    for side in (-1, 1):
        x = side * ex; h = ew * 1.25 * f.eye_open
        box = [*P(x - ew, ey - h), *P(x + ew, ey + h)]
        d.ellipse(box, fill=CHALK + (255,))
        px, py = x + f.look[0] * ew * 0.45, ey + f.look[1] * h * 0.45; pr = ew * f.pupil * 2 / f.eye_size
        d.ellipse([*P(px - pr, py - pr), *P(px + pr, py + pr)], fill=body + (255,))
        if f.lid > 0:  # upper lid: a tilted body-colour slab over the top of the eye
            cover = ey - h + 2 * h * f.lid; t = math.radians(f.lid_tilt) * -side
            poly = [P(x - ew * 1.3, cover + math.tan(t) * -ew * 1.3), P(x + ew * 1.3, cover + math.tan(t) * ew * 1.3),
                    P(x + ew * 1.3, ey - h * 1.6), P(x - ew * 1.3, ey - h * 1.6)]
            d.polygon(poly, fill=lidcol + (255,))
            d.line([poly[0], poly[1]], fill=CHALK + (255,), width=max(2, int(0.035 * r * S)))
        if f.brows:  # chalk brow: + tilt = inner end down (angry V)
            by = ey - max(h, ew) - 0.16 - f.brow_y; t = math.radians(f.brow)
            inner = (x - side * ew * 0.9, by + math.sin(t) * 0.12); outer = (x + side * ew * 1.0, by - math.sin(t) * 0.12)
            d.line([P(*inner), P(*outer)], fill=CHALK + (255,), width=int(0.09 * r * S))
    # mouth
    mw, my = f.mouth_w, 0.48
    if f.open > 0.05:
        top = my - 0.05 - 0.08 * max(f.smile, 0); bot = my + 0.06 + 0.32 * f.open
        if f.smile < -0.2: top, bot = my - 0.02, my + 0.05 + 0.25 * f.open
        fill = CHALK + (255,) if f.teeth else (28, 8, 5, 255)
        if f.smile > 0.3:  # open grin = D shape, flat top
            d.chord([*P(-mw, top - (bot - top)), *P(mw, bot)], 0, 180, fill=fill)
        else:
            d.ellipse([*P(-mw, top), *P(mw, bot)], fill=fill)
        if f.teeth and f.smile <= 0.3: d.line([P(-mw * 0.9, (top + bot) / 2), P(mw * 0.9, (top + bot) / 2)], fill=body + (255,), width=int(0.035 * r * S))
        if not f.teeth and f.smile <= 0.3: d.ellipse([*P(-mw * 0.55, bot - 0.12), *P(mw * 0.55, bot)], fill=(170, 60, 50, 255))
    else:  # line mouth, curve = smile, skew = smirk
        pts = []
        for i in range(25):
            u = -1 + 2 * i / 24
            # image y grows downward: a smile pushes the middle DOWN, a smirk lifts one corner
            yy = my + f.smile * 0.16 * (1 - u * u) - f.skew * 0.14 * max(u, 0) ** 2 + f.skew * 0.04 * max(-u, 0)
            pts.append(P(u * mw, yy))
        d.line(pts, fill=CHALK + (255,), width=int(0.075 * r * S), joint="curve")
    L = _rough(L.resize((L.width // S, L.height // S), Image.LANCZOS), 0.5)
    # clip face to head disc
    clip = Image.new("L", L.size, 0); ImageDraw.Draw(clip).ellipse([2 * r - r * 0.95, 2 * r - r * 0.95, 2 * r + r * 0.95, 2 * r + r * 0.95], fill=255)
    L.putalpha(Image.fromarray(np.minimum(np.asarray(L.getchannel("A")), np.asarray(clip))))
    out.alpha_composite(L, (int(cx - 2 * r), int(cy - 2 * r)))
    # FX outside the head
    fx = ImageDraw.Draw(out); w = max(3, int(r * 0.07))
    if f.sweat:
        sx, sy = cx + r * 1.02, cy - r * 0.35
        fx.polygon([(sx, sy - r * 0.22), (sx - r * 0.1, sy), (sx + r * 0.1, sy)], fill=(180, 205, 220, 255))
        fx.ellipse([sx - r * 0.1, sy - r * 0.08, sx + r * 0.1, sy + r * 0.12], fill=(180, 205, 220, 255))
    if f.tremble:
        for side in (-1, 1):
            for k in range(2):
                x0 = cx + side * r * (1.18 + 0.16 * k)
                fx.arc([x0 - r * 0.25, cy - r * 0.45, x0 + r * 0.25, cy + r * 0.35], 300 if side > 0 else 120, 60 if side > 0 else 240, fill=CHALK + (255,), width=w)
    return out

def face_sheet(fig: Image.Image, names=None, cell_h: int = 360) -> Image.Image:
    names = names or list(PRESETS); a = np.asarray(fig.getchannel("A")); head = find_head(a)
    cx, cy, r = head; box = (int(cx - 2.2 * r), int(cy - 2.0 * r), int(cx + 2.2 * r), int(cy + 2.4 * r))
    cells = []
    for n in names:
        bg = Image.new("RGBA", fig.size, (200, 187, 168, 255)); bg.alpha_composite(paint_face(fig, PRESETS[n], head))
        c = bg.crop(box).convert("RGB"); c = c.resize((round(c.width * cell_h / c.height), cell_h))
        ImageDraw.Draw(c).text((10, 8), n, fill=(40, 12, 8)); cells.append(c)
    W = sum(c.width for c in cells) + 8 * len(cells); sheet = Image.new("RGB", (W, cell_h), (20, 20, 20)); x = 0
    for c in cells: sheet.paste(c, (x, 0)); x += c.width + 8
    return sheet

"""Camera language from show bible section 4, rendered on multiplane layers.

One move per shot. Each layer has a depth (0 = far wall, 1 = nearest), so a push-in
grows the figure faster than the wall: real parallax without any AI video model
repainting the cave style. DepthFlow (vendored) is the alternative for single-image
depth shots; these moves share its names so a shot list can switch engines.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import math
import numpy as np
from PIL import Image, ImageFilter

def ease(t: float, kind: str = "inout") -> float:
    t = min(max(t, 0.0), 1.0)
    if kind == "out": return 1 - (1 - t) ** 3
    if kind == "in": return t ** 3
    return 3 * t * t - 2 * t * t * t

@dataclass
class Cam:
    zoom: float = 1.0
    x: float = 0.0   # pixels at depth 1
    y: float = 0.0
    blur_x: float = 0.0

# --- moves: f(t in 0..1, seconds) -> Cam -----------------------------------------
def push_in(amount=0.14):            return lambda t, d: Cam(zoom=1 + amount * ease(t))
def pull_back(amount=0.22):          return lambda t, d: Cam(zoom=1 + amount * (1 - ease(t)))
def snap_zoom(amount=0.32, at=0.0, dur=0.12):
    def f(t, d):
        k = ease(((t * d) - at * d) / dur, "out") if t * d >= at * d else 0.0
        return Cam(zoom=1 + amount * k)
    return f
def shake(px=22, hz=14, decay=2.5, zoom=1.06):
    def f(t, d):
        s = t * d; a = px * math.exp(-decay * s)
        return Cam(zoom=zoom, x=a * math.sin(2 * math.pi * hz * s), y=a * math.cos(2 * math.pi * hz * 0.83 * s))
    return f
def whip_pan(distance=1400, direction=1):
    def f(t, d):
        k = ease(t); v = 6 * t * (1 - t)  # speed curve, peaks mid-move
        return Cam(x=direction * distance * k, blur_x=60 * v)
    return f
def hold():                          return lambda t, d: Cam()
MOVES = {"push_in": push_in, "pull_back": pull_back, "snap_zoom": snap_zoom,
         "shake": shake, "whip_pan": whip_pan, "hold": hold}

@dataclass
class Layer:
    image: Image.Image            # RGBA, any size
    depth: float                  # 0 far .. 1 near
    pos: tuple[int, int] = (0, 0) # top-left in frame space at zoom 1
    bob: float = 0.0              # idle breathing amplitude in px (figures)
    vx: float = 0.0               # drift in px/second (walks, entrances)

@dataclass
class Shot:
    layers: list[Layer]
    duration: float
    move: object = field(default_factory=hold)

def render_frame(shot: Shot, t: float, size=(1080, 1920)) -> Image.Image:
    W, H = size; cam = shot.move(t, shot.duration)
    frame = Image.new("RGBA", size, (0, 0, 0, 255))
    for L in sorted(shot.layers, key=lambda l: l.depth):
        z = 1 + (cam.zoom - 1) * (0.35 + 0.65 * L.depth)   # far layers zoom less
        par = 0.35 + 0.65 * L.depth
        img = L.image
        w, h = round(img.width * z), round(img.height * z)
        img = img.resize((w, h), Image.BICUBIC)
        cx, cy = W / 2, H / 2
        x = cx + (L.pos[0] - cx) * z - cam.x * par
        y = cy + (L.pos[1] - cy) * z - cam.y * par
        if L.bob: y += L.bob * math.sin(2 * math.pi * 0.6 * t * shot.duration)
        x += L.vx * t * shot.duration * z
        _paste(frame, img, x, y)
    if cam.blur_x > 1:
        frame = _hblur(frame, cam.blur_x)
    return frame.convert("RGB")

def _paste(frame, img, x, y):
    frame.paste(img, (round(x), round(y)), img)

def _hblur(img: Image.Image, radius: float) -> Image.Image:
    a = np.asarray(img).astype(np.float32); r = int(radius)
    # separable box blur via cumulative sums (fast)
    c = np.cumsum(np.pad(a, ((0, 0), (r + 1, r), (0, 0)), mode="edge"), axis=1)
    out = (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def contact_shadow(fig: Image.Image, offset=(18, 10), blur=14, opacity=0.28) -> Image.Image:
    """Soft shadow the figure casts on the wall: sells the layer gap in World mode."""
    a = fig.getchannel("A").point(lambda v: int(v * opacity))
    sh = Image.new("RGBA", (fig.width + 80, fig.height + 80), (20, 8, 4, 0))
    m = Image.new("L", sh.size, 0); m.paste(a, (40 + offset[0], 40 + offset[1]))
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(blur))); return sh

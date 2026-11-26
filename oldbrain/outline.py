"""Procedural chalk outline: the spec's mandatory 6px #EDE6D8 at 1080w, with a rough
hand-drawn edge (noise-modulated width) so it reads as chalk, not a vector stroke."""
from __future__ import annotations
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from .spec import load, hex_rgb, outline_px

def chalk_outline(rgba: Image.Image, frame_width: int = 1080, roughness: float = 0.35, seed: int = 7) -> Image.Image:
    s = load(); px = outline_px(frame_width, s); col = hex_rgb(s["outline"]["color"])
    a = np.asarray(rgba.getchannel("A")) > 64
    pad = px * 3
    a = np.pad(a, pad)
    dist = ndimage.distance_transform_edt(~a)
    rng = np.random.default_rng(seed)
    noise = ndimage.gaussian_filter(rng.standard_normal(a.shape), sigma=px * 1.5)
    noise = noise / (np.abs(noise).max() + 1e-6)
    width = px * (1 + roughness * noise)            # never thinner than px*(1-roughness)
    width = np.maximum(width, px)                   # spec minimum is a floor
    ring = (dist > 0) & (dist <= width)
    grain = 0.82 + 0.18 * rng.random(a.shape)       # chalk grain in the alpha
    alpha = (ring * grain * 255).astype(np.uint8)
    line = Image.new("RGBA", (a.shape[1], a.shape[0]), col + (0,))
    line.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.6)))
    base = Image.new("RGBA", line.size, (0, 0, 0, 0)); base.paste(rgba, (pad, pad))
    return Image.alpha_composite(line, base)

def has_outline(rgba: Image.Image, frame_width: int = 1080, tol: float = 0.85) -> bool:
    """Validator: at least `tol` of the silhouette boundary must be wrapped in chalk."""
    s = load(); col = np.array(hex_rgb(s["outline"]["color"]))
    arr = np.asarray(rgba.convert("RGBA")).astype(int)
    a = arr[..., 3] > 64
    edge = a & ~ndimage.binary_erosion(a, iterations=2)
    near = np.linalg.norm(arr[..., :3] - col, axis=2) < 40
    return edge.sum() > 0 and (near & edge).sum() / edge.sum() >= tol

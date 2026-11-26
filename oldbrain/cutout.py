"""Lift a painted figure off the limestone wall.

Our poses are painted ON the wall (her quality bar), so a generic AI matting model is the
wrong first tool: pigment vs limestone is a colour problem. We estimate the wall colour from
the frame border, key by colour distance plus darkness, fill enclosed holes (the white dot
eyes, the open mouth), drop specks, and feather the edge so the pigment keeps its rough
brush edge. rembg (vendored) is the fallback for figures on busy backgrounds.
"""
from __future__ import annotations
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def wall_colour(rgb: np.ndarray, border: int = 24) -> np.ndarray:
    b = np.concatenate([rgb[:border].reshape(-1, 3), rgb[-border:].reshape(-1, 3),
                        rgb[:, :border].reshape(-1, 3), rgb[:, -border:].reshape(-1, 3)])
    return np.median(b, axis=0)

def pigment_mask(img: Image.Image, threshold: float = 48.0, min_area: float = 0.002, white_dist: float = 75.0) -> np.ndarray:
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    wall = wall_colour(rgb)
    dist = np.linalg.norm(rgb - wall, axis=2)
    # pigment is darker or more saturated than limestone
    sat = rgb.max(2) - rgb.min(2)
    wall_sat = wall.max() - wall.min()
    mask = (dist > threshold) & ((rgb.mean(2) < wall.mean() - 20) | (sat > wall_sat + 40))
    mask = ndimage.binary_opening(mask, iterations=1)
    lab, n = ndimage.label(mask)
    if n:
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        keep = np.isin(lab, 1 + np.flatnonzero(sizes >= min_area * mask.size))
        mask = keep
    mask = ndimage.binary_closing(mask, iterations=2)
    # Fill enclosed holes only when they are painted white (dot eyes, grin, O-mouth).
    # Holes that look like limestone are wall showing through a pose (arm-to-head loops)
    # and must stay transparent, or the camera drags a patch of wall around with him.
    holes = ndimage.binary_fill_holes(mask) & ~mask
    hl, hn = ndimage.label(holes)
    for i in range(1, hn + 1):
        sel = hl == i
        if np.linalg.norm(rgb[sel].mean(0) - wall) > white_dist:
            mask |= sel
    return mask

def cutout(img: Image.Image, feather: float = 1.2, **kw) -> Image.Image:
    """RGBA figure with the wall removed. Edge softness kept, interior solid."""
    m = pigment_mask(img, **kw)
    a = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA"); out.putalpha(a); return out

def bbox(rgba: Image.Image) -> tuple[int, int, int, int]:
    return rgba.getchannel("A").point(lambda v: 255 if v > 32 else 0).getbbox()

def normalise_height(rgba: Image.Image, target_h: int) -> Image.Image:
    """Crop to the figure and scale so every pose of every archetype stands the same height."""
    fig = rgba.crop(bbox(rgba)); s = target_h / fig.height
    return fig.resize((max(1, round(fig.width * s)), target_h), Image.LANCZOS)

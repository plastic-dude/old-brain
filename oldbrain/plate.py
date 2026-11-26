"""Clean plate: the wall with the figure removed, so the camera can move the figure
in front of it. Fast built-in fill (normalised convolution plus re-grained stone texture);
for hero shots run vendor/lama on the same mask for a texture-true fill."""
from __future__ import annotations
import numpy as np
from PIL import Image
from scipy import ndimage

def clean_plate(img: Image.Image, mask: np.ndarray, grow: int = 10, sigma: float = 40) -> Image.Image:
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    m = ndimage.binary_dilation(mask, iterations=grow)
    keep = (~m).astype(np.float32)
    num = np.stack([ndimage.gaussian_filter(rgb[..., c] * keep, sigma) for c in range(3)], 2)
    den = ndimage.gaussian_filter(keep, sigma)[..., None] + 1e-6
    fill = num / den
    # re-grain: borrow high-frequency stone texture from an unmasked strip of the same wall
    hf = rgb - np.stack([ndimage.gaussian_filter(rgb[..., c], 6) for c in range(3)], 2)
    cols = np.flatnonzero(~m.any(0))
    if len(cols):
        src = hf[:, cols]
        idx = np.arange(rgb.shape[1]) % src.shape[1]
        fill = fill + src[:, idx] * 0.9
    soft = ndimage.gaussian_filter(m.astype(np.float32), 3)[..., None]
    out = rgb * (1 - soft) + fill * soft
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

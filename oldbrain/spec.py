"""Load the spec and enforce its numeric rules (contrast, outline width)."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "archetypes.yaml"

@lru_cache
def load(path: str | None = None) -> dict:
    return yaml.safe_load(Path(path or SPEC).read_text())

def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _lum(rgb) -> float:
    def ch(c):
        c /= 255; return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb); return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a: str, b: str) -> float:
    """WCAG contrast ratio. The spec says: never eyeball a palette change."""
    la, lb = sorted((_lum(hex_rgb(a)), _lum(hex_rgb(b))), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)

def outline_px(frame_width: int, spec: dict | None = None) -> int:
    s = spec or load(); return max(1, round(s["outline"]["min_px_at_1080"] * frame_width / 1080))

def contrast_report(spec: dict | None = None) -> dict:
    s = spec or load(); out = {}
    for name, a in s["archetypes"].items():
        out[name] = {"vs_body": contrast(a["tunic"], s["body"]),
                     **{f"vs_{k}": contrast(a["tunic"], v) for k, v in s["backgrounds"].items()}}
    return out

"""Rhubarb mouth cues mapped onto cave faces. Phonetic recogniser by default, because
Stone Age lines are gibberish and the English model would mis-hear them."""
from __future__ import annotations
import json, subprocess
from PIL import Image, ImageDraw

# Rhubarb shapes A-H, X -> how open/wide the white mouth is (w, h as head-diameter fractions)
SHAPES = {"A": (0.18, 0.03), "B": (0.22, 0.07), "C": (0.24, 0.12), "D": (0.26, 0.20),
          "E": (0.18, 0.14), "F": (0.12, 0.10), "G": (0.22, 0.06), "H": (0.20, 0.10), "X": (0.18, 0.02)}

def cues(wav: str, dialog: str | None = None, rhubarb: str = "rhubarb") -> list[dict]:
    cmd = [rhubarb, "-f", "json", "-r", "phonetic", "--extendedShapes", "GHX", wav]
    if dialog: cmd += ["-d", dialog]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)["mouthCues"]

def mouth_sprite(shape: str, head_d: int, colour=(237, 230, 216)) -> Image.Image:
    w, h = SHAPES.get(shape, SHAPES["X"]); W, H = max(2, round(w * head_d)), max(2, round(h * head_d))
    im = Image.new("RGBA", (W + 4, H + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((2, 2, W + 1, H + 1), fill=colour + (255,))
    return im

def shape_at(cue_list: list[dict], t: float) -> str:
    for c in cue_list:
        if c["start"] <= t < c["end"]: return c["value"]
    return "X"

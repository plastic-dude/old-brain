import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from PIL import Image, ImageDraw
from oldbrain.face import PRESETS, paint_face, find_head

def test_head_found_and_every_preset_paints():
    im = Image.new("RGBA", (400, 800), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((140, 80, 260, 200), fill=(79, 20, 12, 255)); d.rectangle((185, 200, 215, 700), fill=(79, 20, 12, 255))
    cx, cy, r = find_head(np.asarray(im.getchannel("A")))
    assert abs(cx - 200) < 4 and abs(cy - 140) < 4 and r > 50
    for f in PRESETS.values():
        out = paint_face(im, f); assert out.size == im.size

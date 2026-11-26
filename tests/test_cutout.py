import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from PIL import Image, ImageDraw
from oldbrain.cutout import cutout, pigment_mask
from oldbrain.outline import chalk_outline, has_outline

def _figure():
    im = Image.new("RGB", (400, 700), (200, 188, 170)); d = ImageDraw.Draw(im)
    d.ellipse((150, 100, 250, 200), fill=(79, 20, 12)); d.rectangle((185, 200, 215, 600), fill=(79, 20, 12))
    d.ellipse((180, 130, 192, 142), fill=(240, 235, 225))          # painted white eye: must be kept
    d.line((200, 260, 90, 120), fill=(79, 20, 12), width=14)         # arm reaching up
    d.line((90, 120, 160, 120), fill=(79, 20, 12), width=14)         # closes a wall loop: must stay transparent
    return im

def test_eye_kept_wall_loop_open():
    m = pigment_mask(_figure())
    assert m[136, 186]           # eye filled
    assert not m[180, 120]       # wall loop transparent

def test_outline_validator():
    c = cutout(_figure()); assert not has_outline(c); assert has_outline(chalk_outline(c))

import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from oldbrain.qa import _diff, SAFE

def test_identical_frames_make_a_perfect_seam():
    a = (np.random.default_rng(0).random((1920, 1080, 3)) * 255).astype(np.uint8)
    assert _diff(a, a) == 0.0

def test_safe_box_is_universal_9x16():
    assert SAFE == (90, 260, 990, 1660)

def test_squash_preserves_volume_and_settles():
    from oldbrain.camera import squash
    sx, sy = squash(0.1, 0.0); assert abs(sx * sx * sy - 1) < 1e-9 and sy < 1
    sx, sy = squash(0.1, 2.0); assert abs(sy - 1) < 1e-3

def test_timing_flags_overrun_and_dead_air():
    from oldbrain.timing import fit
    r = fit([{"id": "a", "text": "THE SKY HAS CHOSEN ME", "shot_s": 1.0},
             {"id": "b", "text": "Hm.", "shot_s": 3.0},
             {"id": "c", "text": "one two three four five", "shot_s": 2.4}])
    assert [x["verdict"] for x in r] == ["OVER", "DEAD AIR", "OK"]

def test_loop_tail_ends_on_frame_zero():
    from PIL import Image
    from oldbrain.assemble import loop_tail
    fr = [Image.new("RGB", (8, 8), (i * 10, 0, 0)) for i in range(20)]
    out = loop_tail(fr, 5); assert out[-1].getpixel((0, 0)) == (0, 0, 0)

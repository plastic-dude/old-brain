import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from oldbrain.qa import _diff, SAFE

def test_identical_frames_make_a_perfect_seam():
    a = (np.random.default_rng(0).random((1920, 1080, 3)) * 255).astype(np.uint8)
    assert _diff(a, a) == 0.0

def test_safe_box_is_universal_9x16():
    assert SAFE == (90, 260, 990, 1660)

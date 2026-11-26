import numpy as np
from oldbrain.timing import tighten_pauses

def _clip():
    sr = 1000; t = np.ones(sr) * 0.5
    return np.concatenate([t, np.zeros(int(1.5 * sr)), t, np.zeros(int(0.5 * sr)), t]), sr

def test_off_by_default():
    a, sr = _clip(); b, cuts = tighten_pauses(a, sr)
    assert len(b) == len(a) and cuts == []

def test_long_pause_cut_to_point_three_short_kept():
    a, sr = _clip(); b, cuts = tighten_pauses(a, sr, enabled=True)
    assert len(cuts) == 1 and abs((len(a) - len(b)) / sr - 1.2) < 0.05

def test_protected_beat_untouched():
    a, sr = _clip(); b, cuts = tighten_pauses(a, sr, enabled=True, protect=[(1.2, 1.4)])
    assert cuts == [] and len(b) == len(a)

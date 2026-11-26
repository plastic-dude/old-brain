import numpy as np
from oldbrain.timing import split_take, mixcheck
SR = 1000
def tone(s): return np.ones(int(s * SR)) * 0.5
def sil(s): return np.zeros(int(s * SR))
def test_split_take_three_lines():
    a = np.concatenate([tone(1), sil(0.6), tone(0.8), sil(0.2), tone(0.3), sil(0.7), tone(1)])
    parts = split_take(a, SR, 3)
    assert len(parts) == 3 and 1.0 < parts[0][1] < 1.6
def test_mixcheck_flags_hit_on_word_not_after():
    v = np.concatenate([tone(1), sil(1)]); s = np.zeros_like(v); s[200:400] = 0.6
    assert mixcheck(v, s, SR, [("BIGGER", 0.0, 1.0)])
    s2 = np.zeros_like(v); s2[1100:1300] = 0.6
    assert mixcheck(v, s2, SR, [("BIGGER", 0.0, 1.0)]) == []

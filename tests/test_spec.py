import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from oldbrain import spec

def test_contrast_matches_locked_spec():
    r = spec.contrast_report()
    assert r["prophet"]["vs_body"] == 4.63 and r["owner"]["vs_body"] == 3.07

def test_outline_floor_scales():
    assert spec.outline_px(1080) == 6 and spec.outline_px(2160) == 12

def test_every_archetype_has_voice_and_unique_head():
    a = spec.load()["archetypes"]; heads = [v["head"] for v in a.values()]
    assert len(set(heads)) == len(heads)
    assert all("semitones" in v["voice"] for v in a.values())
    assert a["denier"]["voice"]["semitones"] != 0  # never collides with the narrator

"""Her voice, every character. Pitch presets come from spec/archetypes.yaml; crowd is built
from 4-5 of her own takes; master is -14 LUFS / -1 dBTP (YouTube's target)."""
from __future__ import annotations
import subprocess
import numpy as np
from .spec import load

def character_chain(archetype: str):
    from pedalboard import Pedalboard, PitchShift, Compressor, HighpassFilter, LowShelfFilter, PeakFilter, Gain
    v = load()["archetypes"][archetype]["voice"]
    fx = [HighpassFilter(80), PitchShift(semitones=v["semitones"])]
    ch = v["character"]
    if ch == "booming":    fx += [LowShelfFilter(cutoff_frequency_hz=180, gain_db=4)]
    if ch == "nasal":      fx += [PeakFilter(cutoff_frequency_hz=1200, gain_db=6, q=1.4)]
    if ch == "breathless": fx += [PeakFilter(cutoff_frequency_hz=5000, gain_db=3, q=0.8)]
    if ch == "loud":       fx += [Gain(2)]
    fx += [Compressor(threshold_db=-18, ratio=3.5, attack_ms=5, release_ms=80)]
    return Pedalboard(fx)

def cave_room(wet: float = 0.18):
    from pedalboard import Pedalboard, Reverb
    return Pedalboard([Reverb(room_size=0.55, damping=0.6, wet_level=wet, dry_level=1 - wet / 2)])

def process_line(path_in: str, path_out: str, archetype: str, era: str = "stone"):
    from pedalboard.io import AudioFile
    with AudioFile(path_in).resampled_to(48000) as f: audio = f.read(f.frames)
    out = character_chain(archetype)(audio, 48000)
    if era == "stone": out = cave_room()(out, 48000)
    with AudioFile(path_out, "w", 48000, out.shape[0]) as f: f.write(out)

def crowd(takes: list[str], path_out: str, under_db: float = -17.0, seed: int = 3):
    """Layer her takes into a crowd: each gets its own pitch, delay and pan spread,
    then the bed sits 15-20 dB under the main voice."""
    from pedalboard import Pedalboard, PitchShift, Delay, Gain
    from pedalboard.io import AudioFile
    rng = np.random.default_rng(seed); mix = None
    for i, t in enumerate(takes):
        with AudioFile(t).resampled_to(48000) as f: a = f.read(f.frames)
        a = a.mean(0, keepdims=True)
        for j in range(3):  # each take becomes 3 voices
            fx = Pedalboard([PitchShift(float(rng.uniform(-4, 4))), Delay(float(rng.uniform(0.0, 0.09)), 0, 1.0)])
            v = fx(a, 48000); pan = rng.uniform(-0.8, 0.8)
            st = np.vstack([v[0] * (1 - pan) / 2, v[0] * (1 + pan) / 2])
            mix = st if mix is None else _sum(mix, st)
    mix = Pedalboard([Gain(under_db)])(mix / max(1e-6, np.abs(mix).max()), 48000)
    with AudioFile(path_out, "w", 48000, 2) as f: f.write(mix)

def _sum(a, b):
    n = max(a.shape[1], b.shape[1]); o = np.zeros((2, n), np.float32)
    o[:, :a.shape[1]] += a; o[:, :b.shape[1]] += b; return o

def master(path_in: str, path_out: str):
    subprocess.run(["ffmpeg-normalize", path_in, "-o", path_out, "-nt", "ebu", "-t", "-14",
                    "-tp", "-1", "-c:a", "aac", "-b:a", "192k", "-f"], check=True)

"""Curate the Old Brain SFX kit (~300 sounds) from sfx/raw + synthesize our own originals.
Every kit file: trimmed, peak-normalized to -1 dBFS, 48 kHz mono 16-bit WAV. kit.json lists source + license.
Run: python tools/sfx_kit.py
"""
import json, re, subprocess, random
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

ROOT = Path(__file__).resolve().parent.parent / "sfx"; KIT = ROOT / "kit"; SR = 48000
CATS = {  # category: (regex on file path, cap, max seconds)
    "crack": (r"crack|break|shatter|snap|glass|splinter", 30, 4), "fall": (r"fall|thud|drop|land|collapse", 30, 4),
    "impact": (r"punch|hit|impact|slap|smack|bonk|knock", 35, 3), "whoosh": (r"whoosh|swoosh|swish|woosh|swing|swipe", 25, 3),
    "boing": (r"boing|spring|bounce|jump|wobble", 25, 3), "pop": (r"pop|bubble|plop|blip", 20, 2),
    "squeak": (r"squeak|toy|honk|horn|kazoo|whistle|duck", 12, 3), "boom": (r"explo|boom|blast", 20, 6),
    "rumble": (r"rumble|quake|earthquake|cave_in|cave-in|debris", 10, 10), "fire": (r"fire|flame|burn|torch|crackl", 10, 10),
    "step": (r"step|foot|walk|run", 15, 3), "rock": (r"rock|stone|gravel|pebble", 15, 4),
    "ding": (r"ding|bell|chime|coin|notif|alert", 20, 3), "fail": (r"fail|wrong|error|buzz|lose|denied", 15, 3),
    "crowd": (r"crowd|cheer|applause|laugh|gasp|murmur|scream", 12, 10), "ghost": (r"ghost|moan|growl|breath", 6, 5),
}
def decode(p):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(out.stdout, np.float32).astype(float)
def finish(a, fade=0.005):
    if not len(a): return a
    thr = np.abs(a).max() * 0.02; idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a[:0]
    a = a[max(0, idx[0] - 240): idx[-1] + 2400]
    n = int(SR * fade); a[:n] *= np.linspace(0, 1, n); a[-n * 4:] *= np.linspace(1, 0, n * 4)
    return a / (np.abs(a).max() + 1e-9) * 10 ** (-1 / 20)
def save(a, path): path.parent.mkdir(parents=True, exist_ok=True); wavfile.write(path, SR, (a * 32767).astype(np.int16))

# ---- our own originals (CC0, made in code) ----
def lp(x, f): b, a = butter(2, f / (SR / 2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f / (SR / 2), "high"); return lfilter(b, a, x)
def env(n, att, dec): t = np.arange(n) / SR; return np.minimum(t / att, 1) * np.exp(-t / dec)
def originals():
    r = np.random.default_rng(7); o = {}; t = lambda s: np.arange(int(SR * s)) / SR
    for i in range(3):  # 'meme boom': deep pitch-dropping thump with grit
        tt = t(1.6); f = 70 * np.exp(-tt * (1.5 + i)) + 38; ph = 2 * np.pi * np.cumsum(f) / SR
        o[f"boom/ob_meme_boom_{i+1}"] = np.tanh(3 * np.sin(ph) * env(len(tt), 0.003, 0.5 + 0.2 * i))
    for i in range(4):  # lightning crack: broadband snap + crackle + low tail
        n = int(SR * (2.5 + i)); x = r.standard_normal(n)
        snap = hp(x, 1500) * env(n, 0.001, 0.06); crackle = hp(x * (r.random(n) > 0.995 - 0.002 * i), 800) * env(n, 0.01, 0.4) * 3
        tail = lp(x, 120) * env(n, 0.05, 1.2 + 0.3 * i) * 4
        o[f"thunder/ob_lightning_crack_{i+1}"] = snap + crackle + tail
    for i in range(4):  # rolling thunder
        n = int(SR * (5 + i)); x = lp(r.standard_normal(n), 180 + 40 * i); mod = lp(np.abs(r.standard_normal(n)), 3) * 8
        o[f"thunder/ob_thunder_roll_{i+1}"] = x * mod * env(n, 0.4 + 0.2 * i, 2.5 + i)
    for i in range(3):  # riser
        n = int(SR * (1.5 + i * 0.5)); tt = np.arange(n) / SR; x = r.standard_normal(n)
        sweep = np.sin(2 * np.pi * np.cumsum(200 + 1800 * (tt / tt[-1]) ** 2) / SR)
        o[f"whoosh/ob_riser_{i+1}"] = (hp(x, 2000) * 0.5 + sweep * 0.5) * (tt / tt[-1]) ** 2
    for i in range(4):  # whoosh: band-swept noise
        n = int(SR * (0.5 + 0.15 * i)); x = r.standard_normal(n); e = np.sin(np.linspace(0, np.pi, n)) ** 2
        o[f"whoosh/ob_whoosh_{i+1}"] = lp(x, 900 + 500 * i) * e
    for i in range(2):  # record scratch
        n = int(SR * 0.6); tt = np.arange(n) / SR; f = 300 + 900 * np.abs(np.sin(2 * np.pi * (4 + i) * tt))
        o[f"squeak/ob_record_scratch_{i+1}"] = hp(r.standard_normal(n), 400) * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.3)
    for i in range(3):  # cartoon slide whistle up/down
        n = int(SR * 0.8); tt = np.arange(n) / SR; f = (500 + 1200 * tt / tt[-1]) if i != 1 else (1700 - 1200 * tt / tt[-1])
        o[f"squeak/ob_slide_whistle_{i+1}"] = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.01 * np.sin(2 * np.pi * 6 * tt))) / SR) * np.sin(np.linspace(0, np.pi, n))
    for i in range(3):  # boing
        n = int(SR * 0.7); tt = np.arange(n) / SR; f = 180 + 120 * np.sin(2 * np.pi * (9 + 3 * i) * tt) * np.exp(-tt * 4)
        o[f"boing/ob_boing_{i+1}"] = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.25)
    for i in range(3):  # pop
        n = int(SR * 0.12); tt = np.arange(n) / SR; o[f"pop/ob_pop_{i+1}"] = np.sin(2 * np.pi * np.cumsum(900 - 5000 * tt + 200 * i) / SR) * env(n, 0.001, 0.02)
    n = int(SR * 2.0); tt = np.arange(n) / SR; hb = np.zeros(n)
    for s in (0.0, 0.25, 1.0, 1.25): k = int(s * SR); m = int(0.15 * SR); hb[k:k + m] += np.sin(2 * np.pi * 55 * tt[:m]) * env(m, 0.005, 0.04)
    o["tension/ob_heartbeat"] = hb
    n = int(SR * 2.0); tk = np.zeros(n)
    for j in range(4): k = int(j * 0.5 * SR); m = 800; tk[k:k + m] += hp(r.standard_normal(m), 3000 if j % 2 else 2000) * env(m, 0.0005, 0.004)
    o["tension/ob_tick_tock"] = tk
    for i, (f1, f2) in enumerate([(220, 207.65), (196, 185)]):  # 'dun dun' stinger
        n = int(SR * 1.6); a = np.zeros(n); m = int(0.7 * SR); tt = np.arange(m) / SR
        tone = lambda f: (np.sin(2*np.pi*f*tt) + 0.5*np.sin(2*np.pi*2*f*tt) + 0.3*np.sin(2*np.pi*3*f*tt)) * env(m, 0.005, 0.35)
        a[:m] += tone(f1); a[int(0.8 * SR):int(0.8 * SR) + m] += tone(f2) * 1.2
        o[f"tension/ob_dun_dun_{i+1}"] = a
    for i in range(2):  # sad trombone-ish fail
        n = int(SR * 2.2); a = np.zeros(n); notes = [293.7, 277.2, 261.6, 246.9]
        for j, f in enumerate(notes):
            L = int(SR * (0.4 if j < 3 else 1.0)); tt = np.arange(L) / SR; k = int(j * 0.42 * SR)
            ff = f * (1 + 0.02 * np.sin(2 * np.pi * 5 * tt)) * (0.97 if i else 1)
            seg = np.tanh(2 * np.sin(2 * np.pi * np.cumsum(ff) / SR)) * env(L, 0.02, 0.6 if j == 3 else 0.3)
            a[k:k + L] += seg[: n - k]
        o[f"fail/ob_sad_trombone_{i+1}"] = lp(a, 2500)
    return o

def main():
    import shutil; shutil.rmtree(KIT, ignore_errors=True)
    cat = json.loads((ROOT / "catalog.json").read_text())["packs"]
    files = [(slug, f, p) for slug, p in cat.items() for f in p["files"]]
    random.Random(1).shuffle(files); used = set(); kit = []
    for c, (rx, cap, mx) in CATS.items():
        n = 0; perpack = {}
        for slug, f, p in files:
            if n >= cap: break
            if f in used or not re.search(rx, f.lower()) or perpack.get(slug, 0) >= max(3, cap // 6): continue
            if re.search(r"8bit|8-bit|retro|laser|chiptune|blip_?\d|coin", f.lower()) and c not in ("ding", "pop"): continue
            a = decode(ROOT / f)
            if not len(a) or len(a) / SR > mx * 1.5: continue
            a = finish(a)
            if len(a) / SR < 0.05 or len(a) / SR > mx: continue
            n += 1; perpack[slug] = perpack.get(slug, 0) + 1; used.add(f)
            name = re.sub(r"[^a-z0-9]+", "_", Path(f).stem.lower())[-40:].strip("_")
            out = KIT / c / f"{n:02d}_{name}.wav"; save(a, out)
            kit.append({"file": str(out.relative_to(ROOT)), "category": c, "seconds": round(len(a) / SR, 2), "source": p["page"], "author": p["author"], "license": "CC0"})
    for k, a in originals().items():
        a = finish(np.asarray(a, float)); out = KIT / f"{k}.wav"; save(a, out)
        kit.append({"file": str(out.relative_to(ROOT)), "category": k.split("/")[0], "seconds": round(len(a) / SR, 2), "source": "Old Brain original (synthesized in tools/sfx_kit.py)", "author": "Old Brain", "license": "CC0"})
    (ROOT / "kit.json").write_text(json.dumps(kit, indent=1))
    from collections import Counter; print(len(kit), dict(Counter(k["category"] for k in kit)))
if __name__ == "__main__": main()

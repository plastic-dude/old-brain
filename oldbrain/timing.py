"""Script timing fitted to HER recordings (retention-pass method, BusyBee3333, adapted).

Write lines at ~2.4 words/sec of shot time. Gibberish Stone Age lines are counted by
syllables (~5 syll/sec). After she records, each take's real length decides the shot:
speech should fill 85-94% of the shot; if the take overruns, extend the shot to take + 0.4 s
(our Shorts are tighter than the 1.5-2 s their long explainers use). Extending never strands beats.
"""
from __future__ import annotations
import re, subprocess
WPS, SPS = 2.4, 5.0

def syllables(word: str) -> int:
    return max(1, len(re.findall(r"[aeiouy]+", word.lower())))

def est_seconds(text: str, gibberish: bool = False) -> float:
    words = re.findall(r"[\w']+", text)
    return sum(syllables(w) for w in words) / SPS if gibberish else len(words) / WPS

def take_seconds(wav: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                         capture_output=True, text=True).stdout
    return float(out.strip())

def fit(lines: list[dict]) -> list[dict]:
    """lines: [{"id", "text", "shot_s", "gibberish"?, "take"?}] -> report with verdicts."""
    rep = []
    for L in lines:
        sp = take_seconds(L["take"]) if L.get("take") else est_seconds(L["text"], L.get("gibberish", False))
        cover = sp / L["shot_s"]
        if cover > 0.94: v, new = "OVER", round(sp + 0.4, 2)
        elif cover < 0.6: v, new = "DEAD AIR", round(sp / 0.9, 2)
        else: v, new = "OK", L["shot_s"]
        rep.append({"id": L["id"], "speech_s": round(sp, 2), "shot_s": L["shot_s"], "cover": round(cover, 2),
                    "verdict": v, "shot_s_new": new, "measured": bool(L.get("take"))})
    return rep


# --- Pause tightening (her rule, 2026-11-26: "it depends") -------------------
# Rule of thumb from a creator tip: a silence of 0.9 s or more is cut to 0.3 s.
# It is a SWITCH, not law: off by default, set per video or per line, and any
# pause the script marks as a beat ("[beat]", "[hold]", "...") is never touched,
# because the show bible holds a beat before every punchline.
import numpy as _np

def find_pauses(audio, sr, min_gap=0.9, thresh_db=-40.0, win=0.02):
    """Silent spans >= min_gap seconds as (start_s, end_s). audio: mono float array."""
    a = _np.asarray(audio, dtype=float)
    if a.ndim > 1: a = a.mean(axis=0 if a.shape[0] < a.shape[1] else 1)
    n = max(1, int(sr * win)); k = len(a) // n
    rms = _np.sqrt((a[: k * n].reshape(k, n) ** 2).mean(axis=1) + 1e-12)
    silent = 20 * _np.log10(rms / (_np.abs(a).max() + 1e-12) + 1e-12) < thresh_db
    out, i = [], 0
    while i < k:
        if silent[i]:
            j = i
            while j < k and silent[j]: j += 1
            if (j - i) * win >= min_gap: out.append((i * win, j * win))
            i = j
        else: i += 1
    return out

def tighten_pauses(audio, sr, enabled=False, min_gap=0.9, keep=0.3, protect=()):
    """Shorten long pauses to `keep` s. `protect`: (start_s, end_s) spans left as recorded
    (punchline beats). Returns (audio, cuts) where cuts lists (start_s, removed_s)."""
    a = _np.asarray(audio)
    if not enabled: return a, []
    def guarded(s, e): return any(s < pe and e > ps for ps, pe in protect)
    pieces, cuts, last = [], [], 0
    for s, e in find_pauses(a, sr, min_gap):
        if guarded(s, e): continue
        half = keep / 2
        cs, ce = int((s + half) * sr), int((e - half) * sr)
        pieces.append(a[last:cs]); cuts.append((round(s, 2), round((ce - cs) / sr, 2))); last = ce
    pieces.append(a[last:])
    return _np.concatenate(pieces), cuts


# --- Ideas re-implemented from public MIT stickman skills (2026-11-26) --------
# kelano86/what-if-animation (mixcheck: SFX must not crowd a spoken word),
# samadpls/animate-pls (split one long take into one file per line at its silences).
# No code copied; rebuilt for her own-voice workflow.

def split_take(audio, sr, n_lines, min_gap=0.35):
    """Split ONE recording of the whole script into n_lines pieces, cutting in the
    n_lines-1 longest silences (keeps the order). Returns list of (start_s, end_s)."""
    gaps = sorted(find_pauses(audio, sr, min_gap=min_gap), key=lambda g: g[1] - g[0], reverse=True)[: n_lines - 1]
    cuts = sorted((s + e) / 2 for s, e in gaps); edges = [0.0] + cuts + [len(audio) / sr]
    if len(edges) - 1 != n_lines: raise ValueError(f"found {len(edges)-1} lines, expected {n_lines}: re-record with clearer pauses")
    return list(zip(edges[:-1], edges[1:]))

def mixcheck(voice, sfx, sr, words, margin_db=3.0, allow=()):
    """Moments where SFX/music come within margin_db of the voice WHILE a word is spoken.
    words: [(word, start_s, end_s)]. allow: words where an overlap is deliberate.
    Rule: a hit that illustrates a word lands in the pause just after it, never on it."""
    v = _np.asarray(voice, float); s = _np.asarray(sfx, float); out = []
    for w, a, b in words:
        if w in allow: continue
        i, j = int(a * sr), int(b * sr); n = max(1, int(0.05 * sr)); d = 99.0
        for k in range(i, max(i + 1, j - n + 1), n):  # 50 ms windows: a short hit can't hide in a long word
            rv = _np.sqrt((v[k:k + n] ** 2).mean() + 1e-12); rs = _np.sqrt((s[k:k + n] ** 2).mean() + 1e-12)
            d = min(d, 20 * _np.log10(rv / rs))
        if d < margin_db: out.append({"word": w, "at": round(a, 2), "voice_minus_sfx_db": round(float(d), 1)})
    return out

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

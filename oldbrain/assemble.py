"""Shots to a 1080x1920 30fps MP4. Transitions from the bible: hard cut, whip pan
(era cut), and the handprint portal between World and Wall mode."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .camera import Shot, render_frame, ease, _hblur

FPS = 30; SIZE = (1080, 1920)

def shot_frames(shot: Shot, fps: int = FPS):
    n = max(1, round(shot.duration * fps))
    for i in range(n):
        yield render_frame(shot, i / max(1, n - 1), SIZE)

def whip(a: Image.Image, b: Image.Image, frames: int = 8, direction: int = 1):
    """Era-cut whip: A rushes out, B rushes in, motion-blurred, no black gap."""
    W, H = SIZE
    strip = Image.new("RGB", (W * 2, H)); 
    if direction > 0: strip.paste(a, (0, 0)); strip.paste(b, (W, 0))
    else: strip.paste(b, (0, 0)); strip.paste(a, (W, 0))
    for i in range(frames):
        k = ease((i + 1) / frames); x = round(W * k) if direction > 0 else round(W * (1 - k))
        v = 6 * ((i + .5) / frames) * (1 - (i + .5) / frames)
        yield _hblur(strip.crop((x, 0, x + W, H)).convert("RGBA"), 70 * v).convert("RGB")

def handprint_portal(a: Image.Image, b: Image.Image, hand: Image.Image, frames: int = 14):
    """A palm print slams onto the wall and grows until it IS the next shot."""
    W, H = SIZE
    for i in range(frames):
        k = ease(i / (frames - 1), "in"); s = 0.25 + 9 * k
        hm = hand.getchannel("A").resize((round(hand.width * s), round(hand.height * s)))
        mask = Image.new("L", SIZE, 0); mask.paste(hm, ((W - hm.width) // 2, (H - hm.height) // 2))
        yield Image.composite(b, a, mask)

def caption(frame: Image.Image, text: str, y: int = 170, size: int = 62, max_w: int = 940) -> Image.Image:
    """Burned-in subtitle in the top safe zone (Shorts UI covers the bottom ~20%).
    Wraps to the frame and never crosses the figure. Stone Age lines are gibberish;
    the subtitle is the joke."""
    d = ImageDraw.Draw(frame)
    try: f = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError: f = ImageFont.load_default()
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    for i, ln in enumerate(lines):
        x = (SIZE[0] - d.textlength(ln, font=f)) / 2
        d.text((x, y + i * size * 1.2), ln, font=f, fill=(237, 230, 216), stroke_width=7, stroke_fill=(40, 12, 8))
    return frame

def write_mp4(frames, out: str | Path, audio: str | None = None, fps: int = FPS):
    from moviepy import ImageSequenceClip, AudioFileClip
    arr = [np.asarray(f) for f in frames]
    clip = ImageSequenceClip(arr, fps=fps)
    if audio: clip = clip.with_audio(AudioFileClip(audio))
    clip.write_videofile(str(out), codec="libx264", audio_codec="aac", preset="medium",
                         ffmpeg_params=["-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"], logger=None)
    return out

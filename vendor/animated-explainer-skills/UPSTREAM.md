# Upstream
- Origin: https://github.com/BusyBee3333/animated-explainer-skills
- Pinned commit: c1dd704921b6a7587efd8d611dbbb4838012760c
- License: MIT
- Copied 2026-11-26.

## Not used
- HTML/GSAP/SVG vector look (rejected for Old Brain) and the ElevenLabs voiceover pipeline (voices are the creator's own, never AI).

## Our changes (rebuilt in Python inside oldbrain/)
- CustomBounce squash-and-stretch -> camera.squash + Layer.pop (volume-preserving, anchored at the feet).
- overlap-audit.js (0.5 s pairwise) -> assemble.audit_overlap using camera.layer_box on visible pixels; written to <mp4>.render.json and failed by qa.py.
- retention-pass VO fit (2.5 w/s, extend scene to clip + 1.5-2 s) -> timing.py: fitted to HER real takes, gibberish counted in syllables, extend to take + 0.4 s for Shorts, flags dead air.

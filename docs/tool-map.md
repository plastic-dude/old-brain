# Tool map: show bible area to tool

| Bible area | Tool | Status | What we take |
|---|---|---|---|
| 2. Body | vendor/animated-drawings | vendored | Drawing to mask to skeleton to ARAP deformation; BVH motion retargeting; transparent export |
| 4. Camera motion | vendor/depthflow | vendored | Ray-marched 2.5D parallax from image plus depth; seamless loops; no watermark |
| 1. Faces (mouths) | vendor/rhubarb | vendored (no third-party lib/) | Voice to 6-9 mouth shapes; phonetic mode works on gibberish |
| 1. Faces (expressions) | TBD | scouting | LivePortrait is human-only; we likely build parametric dot-eye faces ourselves |
| 3. Environments | TBD | scouting | Depth estimation, layer separation, inpainting |
| 5. Angles | TBD | scouting | |
| 6. Story | ours | not started | Formula from bible section 6; no repo writes hits |
| 7. Controversy | ours | not started | QA checklist from bible section 7 |
| Assembly | TBD | scouting | Remotion, MoviePy or ffmpeg graph |
| Audio | TBD | scouting | Pitch presets, crowd layering, -14 LUFS |

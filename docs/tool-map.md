# Tool map: show bible area to tool

| Bible area | Our module | Vendored | Status |
|---|---|---|---|
| 1. Faces | oldbrain/face.py, lipsync.py | rhubarb | working: 9 presets; lip-sync mapping written, needs the rhubarb binary |
| 2. Body | oldbrain/cutout.py, outline.py | animated-drawings, rembg | working: cutout + outline + validator; rigging next |
| 3. Environments | oldbrain/plate.py | lama, depth-anything-v2 | working: clean plates; depth layers next |
| 4. Camera motion | oldbrain/camera.py | depthflow | working: 5 moves + parallax + shadows |
| 5. Angles | camera framing presets (next) | pyscenedetect | rival cut-rhythm analysis next |
| 6. Story | ours | moneyprinterturbo (flow reference) | formula in the bible; no repo writes hits |
| 7. Controversy | QA checklist (next) | none | rules in the bible |
| Assembly | oldbrain/assemble.py | moviepy | working: MP4, whip, handprint portal, captions |
| Audio | oldbrain/voice.py | pedalboard, ffmpeg-normalize | written: presets, crowd, master; needs her takes |
| QA gate | oldbrain/qa.py | iart-tiktok-skills | working: Prophet demo passes 5 of 6; fails loop seam (demo doesn't loop yet) |

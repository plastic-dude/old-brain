# Old Brain: open-source repo scan (verified 2026-11-26)

Every repo below was checked on its live GitHub page (github.com/<repo>, plus the LICENSE/README raw files) and on ungh.cc for stars and last push. The GitHub REST API was rate-limited, so I did not use it. "Last push" is the repo's most recent push date. Stars are as of 2026-11-26.
GPU column: none = runs on CPU; optional = CPU works but is slow, or the small model runs on CPU; required = practically needs a CUDA GPU.
Fit (1-5) = how well it suits the Old Brain pipeline: flat painted figures, multiplane cave plates, her own voice, 9:16, CPU-friendly, permissive license.
⚠ = license or maturity flag.

## 1. Facial expression (2D / stylized)
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/DanielSWolf/rhubarb-lip-sync | 2.8k | MIT | 2026-06 | none | Turns her recorded VO into timed mouth shapes (A–H, X). Drives mouth-sprite swaps on each pose | 5 |
| github.com/deepratna-awale/Emotica | 85 | MIT | 2026-11 | required (A1111/Forge/ComfyUI; Qwen-Image-Edit or Wan 2.2) | Repaints a face into 28 emotions and keeps pose, outfit and art style. Batch-makes expression variants of each pose-library frame | 4 ⚠ small, young |
| github.com/shinshin86/mesh-avatar-studio | 2.5k | MIT | 2026-11 | none (browser editor) | Mesh rig from one illustration: blink, vowel mouths, head turn, drawn eye and mouth variants, audio lip-sync preview | 3 (bust/avatar-oriented; no verified MP4 export) |
| github.com/Inochi2D/inochi-creator | 1.3k | BSD-2 | 2025-06 | none | Open Live2D-style mesh-deform rig for face parts (brow, eye, mouth params). inochi-session (BSD-2, 2025-11) renders it | 3 (manual rigging; slower activity) |
| github.com/KlingAIResearch/LivePortrait (was KwaiVGI) | 19.6k | MIT code | 2026-06 | required in practice | Retargets her own face performance and expression edits onto a painted head | 2 ⚠ Stylized minimal faces may not track. The README points to a MediaPipe alternative to InsightFace, whose pretrained models are widely reported as non-commercial (not verified on this page) |

Not chosen: pkhungurn/talking-head-anime-3-demo (MIT, 1.0k★, last push 2023, anime-face-specific, GPU).

## 2. Body animation / rigging from one drawing (beyond AnimatedDrawings)
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/Aodaruma/coa_tools2 | 88 | GPL-3.0 ⚠ | 2026-09 | none | Blender cutout-animation add-on: import sliced PNG limbs, bones, mesh deform, sprite or video export. Its rig is the closest match to her existing pose-library and limb setup | 4 (GPL covers the tool only, not the videos it renders) |
| github.com/zeikar/iki | 54 | MIT | 2026-11 | none (AI part-cutting optional) | Web puppet engine that auto-rigs from part layers (face, eyes, mouth…), plus a lip-sync hook | 3 ⚠ young; bust-focused |
| github.com/Wzhang3912/image2live2d | 51 | Apache-2.0 | 2026-09 | optional | Headless "folder of layers → rig" (nijilive .inp / Live2D .moc3). A model for scripted rig building | 3 ⚠ young |
| github.com/Doubiiu/ToonCrafter (ToonCrafter/ToonCrafter) | 6.1k | Apache-2.0 code | 2025-03 | required | Generative in-betweens between two keyframes from the pose library (e.g. preach → shocked), with sketch guidance | 3 (weights license not checked; may drift from the painted style) |
| github.com/Tencent/MimicMotion | 2.7k | Apache-2.0 (plus third-party components) | 2025-11 | required (8–16 GB VRAM per README) | Moves a character image along a pose sequence | 2 (trained on humans; stick figures may break) |

Excluded: LordLiang/DrawingSpinUp has no license file (all rights reserved). lllyasviel/ControlNet-v1-1-nightly has no license file. Mikubill/sd-webui-controlnet is GPL-3.0 and stale since 2024-08. MooreThreads/Moore-AnimateAnyone is Apache but stale since 2024-05.

## 3. Environment / background layering
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/danielgatis/rembg | 25.7k | MIT | 2026-11 | none (ONNX on CPU) | Alpha cut-outs of characters and foreground rocks, scriptable | 5 |
| github.com/DepthAnything/Depth-Anything-V2 | 9.2k | Apache-2.0 code | 2026-03 | optional (Small runs on CPU) | Depth map to slice a cave plate into near, mid and far planes | 5 ⚠ Only the Small model is Apache. Base, Large and Giant are CC-BY-NC-4.0, so use Small for commercial work |
| github.com/advimman/lama | 10.4k | Apache-2.0 | 2025-02 | optional | Fills what sits behind each cut-out layer, so parallax never shows a hole | 4 |
| github.com/facebookresearch/sam2 | 20.2k | Apache-2.0 / BSD-3 | 2026-05 | optional (GPU recommended) | Click-to-segment specific rocks, ledges and props into their own layers | 4 |
| github.com/provos/parallax-maker | 112 | AGPL-3.0 ⚠ | 2026-09 | optional | Full loop: depth → cards → per-card inpaint → glTF export to Blender/Unreal | 4 (AGPL is fine run locally; serving a modified version to others means sharing its source) |

Also checked: ZhengPeng7/BiRefNet (MIT, 4.5k★, 2026-10) gives sharper hi-res mattes than rembg. lllyasviel/LayerDiffuse (Apache, 2.2k★, last push 2024-06, GPU) generates transparent layers natively. prs-eth/Marigold has Apache code with RAIL++-M models. Sanster/IOPaint (Apache, 23.3k★) is a nice LaMa UI/CLI but is ARCHIVED ⚠.

## 4. Camera motion on stills / 2.5D (beyond DepthFlow)
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/theatre-js/theatre | 13.1k | Apache-2.0 | 2024-08 | none | Visual keyframe editor for three.js camera paths over a multiplane stack (dolly, truck, push-in curves) | 4 (quiet since 2024) |
| github.com/provos/parallax-maker | 112 | AGPL-3.0 ⚠ | 2026-09 | optional | Exports layered cards as glTF to animate a real camera in Blender | 4 |
| github.com/vt-vl-lab/3d-photo-inpainting | 7.1k | MIT | 2024-08 | optional (CPU slow) | Layered-depth-image plus occlusion inpainting, rendered into dolly-zoom, zoom-in and circle moves | 3 |
| github.com/AustinZ21/cinematic-skills | 5 | MIT | 2026-11 | optional | "still-to-film": WebGL depth-parallax camera with motion blur, upscale and film finish, plus a 22-move camera vocabulary | 3 ⚠ very young |
| github.com/TencentARC/MotionCtrl | 1.5k | Apache-2.0 | 2025-02 | required | Generative video with camera control. CameraCtrl (hehao13, Apache, 2024-05) is similar | 2 (repaints the style) |

Excluded for license: sniklaus/3d-ken-burns is CC BY-NC-SA 4.0 (non-commercial). Stability-AI/stable-virtual-camera uses the Stability AI Non-Commercial License.
My read: for flat painted planes, own camera code works best: scale/offset per plane in MoviePy, Motion Canvas or Remotion, with Theatre for authoring. That, or DepthFlow, beats any generative option here.

## 5. Camera angles & shot composition
Mature open-source work is thin here. Most new repos are LLM "director" skills with few stars.
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/Breakthrough/PySceneDetect | 5.7k | BSD-3 | 2026-11 | none | Measures cut timing and shot length in reference Shorts, to set a pacing target (e.g. a cut every ~1.5 s) | 4 |
| github.com/jwagner/smartcrop.js | 13.0k | MIT | 2024-03 | none | Content-aware crops: reframes wide cave plates into 9:16 and finds CU/MS punch-in rectangles | 4 |
| github.com/jayaprakash-pixel/cinematography-director | 0 | Apache-2.0 | 2026-11 | none | Claude skill: script plus word timings become shot size, angle and movement, each with a motivation rule, and a timeline.json timed to words. A ready template for the "shots" step | 3 ⚠ brand new, 0★ |
| github.com/HVision-NKU/StoryDiffusion | 6.5k | Apache-2.0 | 2024-09 | required | Keeps a character consistent across multi-panel, multi-angle frames | 2 (she already has a pose library) |
| github.com/sy77777en/CameraBench | 325 | CC-BY-4.0 | 2026-03 | optional | Camera-motion taxonomy to standardize the shot vocabulary in the shot list | 2 |

Excluded: shanghaicellcenter/shotblock (no license). LinHao-city/StoryMind and summerrise-studios/frame are AGPL-3.0 and 0–16★.

## 6. Story, script & hook generation
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/Jakeschincariol/youtube-agent-skill | 7.5k | MIT | 2026-09 | none | 21 hook formulas with hook scoring, title and thumbnail linted as a pair, and a retention-export reader that finds where viewers leave | 4 ⚠ one commit; star count is high for its age |
| github.com/vyralcontent/content-skills | 288 | MIT | 2026-06 | none | Several hook options from proven patterns; scripts shaped as hook → escalation → payoff → loop/CTA | 4 |
| github.com/stanford-oval/storm | 32.0k | MIT | 2025-09 | none (LLM API, LiteLLM) | Researches a topic and outlines it with citations before scripting, so the history facts hold up | 4 |
| github.com/rediumvex/viral-hooks-skill | 148 | MIT | 2026-05 | none | 100 hook formulas grouped under 10 psychology triggers, 3 variants per script | 3 |
| github.com/google-deepmind/dramatron | 1.2k | Apache-2.0 | 2024-07 | none | Hierarchical prompting: logline → characters → beats → dialogue, for multi-character skits | 3 |

Flag: datacrystals/AIStoryWriter is AGPL-3.0.

## 7. Audio
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/slhck/ffmpeg-normalize | 1.5k | MIT | 2026-11 | none | Final mix to −14 LUFS integrated / −1 dBTP (EBU R128 two-pass) | 5 |
| github.com/spotify/pedalboard | 6.5k | GPL-3.0 ⚠ | 2026-11 | none | Pitch shift for character voices, cave reverb, EQ, compression, VST hosting, all in Python | 5 (GPL covers the tool, not the audio) |
| github.com/jiaaro/pydub | 9.8k | MIT | 2026-03 | none | Layers crowd beds (duplicated, detuned, offset takes of her voice), places SFX, ducks under VO | 4 |
| github.com/csteinmetz1/pyloudnorm | 796 | MIT | 2026-01 | none | Per-stem LUFS measure/normalize in Python before the mix | 4 |
| github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI | 39.3k | MIT | 2026-08 | optional (CPU requirements file exists; training wants GPU) | Converts her takes into distinct, consistent character timbres, beyond what pitch shift alone gives | 3 |

SFX generation, flagged ⚠ non-commercial weights: facebookresearch/audiocraft has MIT code but CC-BY-NC weights. hkchengrex/MMAudio has MIT code but CC-BY-NC checkpoints. declare-lab/TangoFlux is non-commercial and research-only. Stability-AI/stable-audio-tools has MIT code; I did not check its model license. For commercial SFX, a CC0 library such as Freesound CC0 filters is safer.

## 8. Programmatic video assembly & compositing
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/Zulko/moviepy | 15.2k | MIT | 2026-08 | none | Python spine: plate layers as ImageClips with per-plane position/scale over time (parallax), pose and mouth swaps, audio, 1080×1920 export. Matches her existing Python rig script | 5 |
| github.com/motion-canvas/motion-canvas | 20.3k | MIT | 2026-07 | none | TypeScript tweening with a timeline editor and audio scrubbing; easy camera and layer choreography | 4 |
| github.com/midrender/revideo (was redotvideo/revideo) | 4.2k | MIT | 2026-07 | none | Motion Canvas fork with a headless render API for batch renders | 4 |
| github.com/remotion-dev/remotion | 75.7k | Remotion License ⚠ | 2026-11 | none | React video with the biggest ecosystem (captions, Lambda rendering) | 4 (free for individuals and small companies; larger companies need a paid company license) |
| github.com/kkroening/ffmpeg-python | 11.0k | Apache-2.0 | 2024-08 | none | Filter-graph builder for the final mux, overlay and zoompan steps | 3 (stale) |

Also checked: mifi/editly (MIT, 5.7k★, last push 2025-05) does declarative JSON edits.

## 9. Shorts pipelines, upload & analytics
| Repo | ★ | License | Last push | GPU | What we take | Fit |
|---|---|---|---|---|---|---|
| github.com/harry0703/MoneyPrinterTurbo | 145.7k | MIT | 2026-11 | none | Orchestration pattern (topic → script → audio → subtitles → 9:16 MP4), subtitle styling, WebUI/API, batch mode. Stock footage would be swapped for our shots | 4 |
| github.com/eukosh/youtube-kit | 10 | MIT | 2026-11 | none | CLI and MCP: resumable upload, thumbnails, metadata, and Analytics split by content type (Shorts), with retention and traffic sources | 4 ⚠ young |
| github.com/porjo/youtubeuploader | 895 | Apache-2.0 | 2026-11 | none | Single Go binary for scripted, cron-friendly uploads | 4 |
| github.com/gyoridavid/short-video-maker | 1.5k | MIT | 2025-06 | none | Remotion composition, Kokoro TTS and captions behind MCP/REST. Reuse the Remotion caption templates and REST wrapper | 3 |
| github.com/RayVentura/ShortGPT | 8.2k | MIT | 2025-02 | none | An "editing engine" abstraction: JSON-described edit steps | 3 |

Foundation for custom analytics: googleapis/google-api-python-client (Apache, 9.0k★, active). Flag: elebumm/RedditVideoMakerBot is GPL-3.0.

## Top 8 overall
1. Zulko/moviepy: the assembly spine. Multiplane parallax, pose and mouth swaps, and 9:16 export in plain Python on CPU.
2. DanielSWolf/rhubarb-lip-sync: mouth shapes timed straight from her own VO, on CPU, under MIT.
3. DepthAnything/Depth-Anything-V2 (Small model only): auto-slices cave plates into depth planes.
4. danielgatis/rembg: CPU alpha cut-outs for characters and foreground rock layers.
5. advimman/lama: fills behind each cut layer so camera moves never show holes.
6. spotify/pedalboard: pitch shift, cave reverb and FX for character voices and crowds (GPL tool, output unaffected).
7. slhck/ffmpeg-normalize: one command for the −14 LUFS / −1 dBTP final master.
8. harry0703/MoneyPrinterTurbo: proven script-to-MP4 orchestration to borrow and re-skin around our own shot renderer.

Honorable mentions: Aodaruma/coa_tools2 (cutout rigging), deepratna-awale/Emotica (expression variants of the pose library), eukosh/youtube-kit (upload plus Shorts analytics), Jakeschincariol/youtube-agent-skill (hook scoring).

## Unverified or skipped
- naomimetzger/viral-script and Mrshahidali420/youtube-shorts-automation did not load. Skipped.
- tokland/youtube-upload: no license file, last push 2024-04. Skipped.
- Model-weight licenses for ToonCrafter, stable-audio-tools and Apple ml-depth-pro (custom Apple license) were not fully read.

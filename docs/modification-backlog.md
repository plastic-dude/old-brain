# Modification backlog (improve, not just wire)

## animated-drawings (upstream archived Sep 2025, so we maintain it)
- [ ] Drop the TorchServe/Docker detector for our assets: masks come from color-keying the painted pose off the limestone wall
- [ ] Cave-figure skeleton config: thin stick limbs, round head, and the head feature (flame, spikes, bun, flat-top) as a rigid child layer that never deforms
- [ ] Silhouette guard: reject any frame where the head feature is occluded (spec rule)
- [ ] Procedural chalk outline pass, #EDE6D8, at least 6px at 1080w (spec rule)
- [ ] Pigment-grain and rough-edge shader so motion keeps the painted look
- [ ] Motion source: creator films herself on her phone, then BVH (Rokoko or an open pose-to-BVH tool), then a retarget config per archetype
- [ ] Exaggeration multiplier and anticipation holds (bible section 2)
- [ ] Modernize: Python 3.11, headless Mesa by default, 9:16 transparent output

## depthflow
- [ ] Preset library matching bible section 4: slow push-in, snap zoom, whip pan, shake, pull-back-to-wall
- [ ] Layer mode: feed our painted multiplane layers in place of estimated depth
- [ ] Defaults 1080x1920 at 30fps; one move per shot
- [ ] Handprint portal transition between World and Wall mode

## rhubarb
- [ ] Map shapes A-F (and X) to cave-face mouths for all 5 archetypes
- [ ] Phonetic recognizer default (Stone Age gibberish)
- [ ] Batch mode per line from the record-by-voice sheet, with JSON to the assembler
- [ ] Restore rhubarb/lib/ from upstream at build time (excluded from the repo for size)

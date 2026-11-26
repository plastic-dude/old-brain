# Craft taken from public stickman/animation skills (2026-11-26)
Verified on GitHub (API): kelano86/what-if-animation (398 stars, MIT), krishnagoswami52/stickman-skill (38, MIT),
michxlai/stickman-skill (27, MIT; near-identical SKILL.md to krishnagoswami52), deenukhan/stick-figure-shorts (55, NO license: ideas only),
samadpls/animate-pls (7, MIT, built on cth9191/animate), sarthakrawool/stickman-story-reels (2, MIT; was QuantumCoderSys).
All draw every frame in code (SVG/Remotion/canvas) and most voice with ElevenLabs: that look and AI voice stay OUT for Old Brain.

## Taken (rebuilt in our code / rules)
- **One world** (stickman-skill): fixed positions for every character and prop; each shot is only a camera on that world.
  For us: the SAME position map in both eras, so the mirror cut lines up.
- **Storyboard before animation** + self-check every still; motion grid (flipbook) check before final.
- **mixcheck** (what-if): an SFX hit that illustrates a word lands in the pause after it, never on it -> `timing.mixcheck`.
- **split_take** (animate-pls): she records the whole script in one go; we cut it into lines at the silences -> `timing.split_take`.
- **Pace** (what-if / stick-figure-shorts): 27+ cuts a minute in the opening, no static shot over ~3 s, cuts every 2.5-4 s with one slow eased push (1.00 -> 1.04-1.14). Our QA rhythm limit (4 s) should tighten to 3 s for openings.
- **Eye checks the audit can't do** (stickman-skill): faces read the intended emotion; brows not accidentally angry; hands touch what they hold; nothing crosses a face; arms bend the right way on walks; characters keep the same distance to props shot to shot.
- **Ending** (stick-figure-shorts): last 3 s = one short line to the viewer, hold on the hero, no title card ("So... would you switch?"). Fits our debate-bait ending.
- **In-scene text** (stick-figure-shorts): text lives on props in the world's style (a sign, a phone screen), one at a time, timed to the word.
- **Originality rule** (all): references are for patterns only; never reuse another channel's premise, character, line or look.

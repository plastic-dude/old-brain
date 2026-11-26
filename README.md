# Old Brain

**Same brain. 40,000 years apart.**

The production monorepo for the Old Brain Shorts channel (@oldbrain-x). It's a faceless animated comedy: the same scenario in the Stone Age and in modern life, side by side.

## The law
Everything in this repo obeys `spec/`. If a tool's behavior conflicts with the spec, change the tool, not the spec.

- `spec/show-bible-v0.md`: faces, body, environments, camera motion, angles, story formula, controversy rules
- `spec/archetype-spec-v1.md`: cast, palette hex, chalk outline, silhouette rules, era swap, voice presets

## Layout
| Path | What lives there |
|---|---|
| `spec/` | Source of truth. Versioned, changed only by decision. |
| `vendor/<tool>/` | Full copies of open-source tools we own and modify. Each has `UPSTREAM.md` (origin, pinned commit, license). |
| `adapters/` | Our glue: makes each tool read the spec and output our formats. |
| `docs/` | Tool map, modification backlog, decisions. |
| `episodes/ep-NNN/` | One folder per episode (scenario, script, shots, QA, package, status). |

## Rules
1. Vendored code is ours. Modify and improve it; record every change in that tool's `UPSTREAM.md` under "Our changes".
2. Output is always 1080x1920, 30fps, 9:16.
3. Voices are the creator's own recordings. No AI voiceover.
4. Licenses: DepthFlow is AGPL-3.0. Keep this repo private. If it ever ships publicly or as a service, the combined code must be released under AGPL.

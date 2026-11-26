# Old Brain Archetype Spec v1 (locked 2026-11-26)

## Global rules
- **Body:** every figure uses the same flat 2D cave-art stick body. The body is filled #4F140C, with thin stick limbs, a round head, white dot eyes and rough pigment edges. Bodies are gender-neutral and identical across the cast.
- **Chalk outline:** mandatory on every figure, in every mode. Color #EDE6D8, minimum 6 px at 1080 px frame width (scale proportionally). The validator rejects any figure without it.
- **One silhouette feature per archetype.** The head feature must appear in all four views (front, 3/4, side, back). Nothing (hat, hood, prop) may cover it.
- **Auto-reject:** any non-Denier figure with a plain round head. Failed generations collapse into the Denier silhouette.
- **Build method:** head features and faces are separate cutout layers composited onto the body. Run a mask-overlap check against the reference master to catch drift.
- **Color changes:** any palette change re-runs the contrast check (WCAG ratio). Never eyeball it.

## Palette
| Role | Hex | vs body | vs dusk #41454F | vs cream #C8BBA8 |
|---|---|---|---|---|
| Body | #4F140C | n/a | 1.52 | 7.74 |
| Prophet tunic | #C38427 | 4.63 | 3.04 | 1.67 |
| Panicker tunic | #516276 | 2.34 | 1.53 | 3.31 |
| Seller tunic | #747745 | 3.11 | 2.04 | 2.49 |
| Owner tunic | #9C5C9A | 3.07 | 2.02 | 2.52 |
| Denier tunic | #715E51 | 2.38 | 1.56 | 3.25 |
| Wall mode background | #C8BBA8 | | | |
| World mode dusk rock | #41454F (too close to body: lift it or rim-light the figures) | | | |

No tunic passes 3:1 against both backgrounds, so the outline carries readability. Watch the Panicker and Denier (the weakest tunic-to-body pairs).

## Archetypes
| | Head feature | Tunic | Symbol | Default face | Signature pose | Voice preset |
|---|---|---|---|---|---|---|
| **Prophet** | tall upward flame tuft | #C38427 | sun | wide eyes, open grin | both arms raised to the sky | down 2-3 semitones, slow chest voice, booming |
| **Panicker** | wild spikes in all directions | #516276 | lightning bolt | huge eyes, open mouth | hands on cheeks | up 2-3 semitones, fast, breathless |
| **Seller** | round topknot bun | #747745 | rock | one-sided smirk | one hand holding a product out | up 1-2 semitones, fast, nasal, shifty |
| **Owner** | chunky wide flat-top | #9C5C9A | flag | angled-down brows, flat mouth | hands on hips, chest out | down 1-2 semitones, clipped, loud |
| **Denier** | bald, smooth | #715E51 | X | half-lidded eyes, flat mouth | arms crossed | natural pitch, slow, flat monotone |

Owner and Denier both have flat mouths. The brows separate anger from boredom.

## Expression sprite set (per archetype, swappable)
neutral (default face), panic, smug, angry, sad, shocked, bored. Each sprite keeps the white dot eye style.

## Era-swap rule
The head feature, tunic color and body stay fixed. Only clothes and props change, in the tunic color:
- Prophet: yellow hoodie
- Panicker: clay-blue puffer jacket
- Seller: olive vest or polo
- Owner: plum blazer
- Denier: stone-grey tee (no cap, ever)
Wall mode may keep tunics on modern figures ("a cave painter drawing modern life").

## Masters
Rebuild one archetype at a time in four views (front, 3/4, side, back), never as a grid. Order: Prophet, Owner, Seller, Panicker, Denier.

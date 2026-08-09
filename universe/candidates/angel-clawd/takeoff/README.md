# READY FOR TAKEOFF — back print candidates (2026-08-08)

Back-of-shirt lockup: angel-Clawd above the three-line pixel block text READY / FOR / TAKEOFF,
cream on a dark garment, matching the MOM/DAD back-print family.

**Assembly is deterministic.** The mascot and the text are separate keyed PNGs stacked by
`scripts/stack_print.py` onto the 4500x5400 @300 DPI print canvas. No image model ever sees the
mascot and the words in one frame: that would re-paint a locked entity and garble the letterforms.

## Candidates

| id | mascot | note |
|---|---|---|
| `lockup-locked-wingsraised` | the LOCKED `wings-raised` alt-look, untouched | zero drift. Canon already calls this the uplifted-flight silhouette, so it is "ready for takeoff" without a new render. |
| `lockup-s3` | `mascot-s3.png` — one arm punched straight up | the superheroic read. Needs Gary's blessing before it can lock as a new alt-look. |
| `lockup-s1` | `mascot-s1.png` — body tilted, arms at sides | weaker: the tilt reads as leaning rather than launching. |

`mascot-s2` was REJECTED and is kept only as history: it drifted into bevelled 3D/isometric
rendering, which the entity's invariants explicitly forbid ("full 3D are not"). The s3 prompt
gained an explicit anti-3D clause because of it.

## Status

Nothing here is locked. The text panel and the s1/s3 mascots are candidates. If Gary blesses s3,
it becomes a second alt-look (`takeoff` or similar) via `abu lock-shot --look`, the same way
`wings-raised` was locked.

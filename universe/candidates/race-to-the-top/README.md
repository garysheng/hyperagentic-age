# Race to the top

Symbolic plate for Anthropic's **race to the top**: a practice that is both good and good for
business gets adopted by competitors, and the waterline rises for everybody. Daniela Amodei's own
framing, from the Sixth Street interview ingested 2026-08-08 into the campaign's inspo archive:
*"if you can find the intersection of something that is actually good and is good for business...
that just raises the waterline for everybody."*

## The symbol

Angel Clawd hoists a standard on two cords. The bar is high and nothing rests on it. Below, a field
of columns of unequal height all reach toward it. Nobody is pushed down; the floor is what moved.

That is the concept precisely, and it is why the bar is drawn EMPTY: the point of race-to-the-top is
not that the leader wins the height, it is that the height becomes the new floor for the field.

## How it was made, and the canon decision inside it

Two mediums on purpose:

- **The stage** (bar, cords, columns, ground) is the `anthropic-plate` style pack — wobbly
  single-weight ink, flat ivory fills, one terracotta ground. Generated through the framework
  provider adapter, so it carries its own recipe. Prompted with the upper-centre deliberately left
  EMPTY, because the mascot was never going to be painted by the model.
- **Angel Clawd** is the LOCKED `wings-raised` sheet, composited in at full colour, pixel-identical
  to canon.

The entity's `prose.rules` say plainly: *"If the mascot must appear INSIDE a model-rendered
ink-and-wash scene, that is a new decision requiring Gary's blessing, not a default."* Gary asked for
Clawd in this image (2026-08-08), which is the blessing. The rule's other half still held: Clawd is
**never restyled into ink-and-wash**, so it is placed here as its own locked pixel art rather than
redrawn in the pack's line. The medium contrast is the point, and it is consistent with the
`pixel-mascot-medium-exception` craft record.

## Gate read-back

Against `anthropic-plate`'s gate, with the two deliberate exceptions named rather than glossed:

| assertion | verdict |
|---|---|
| single-weight wobbly BLACK ink line only | PASS (stage layer) |
| fills are flat ivory-cream only, no shading or gradients | **DECLARED EXCEPTION** — Clawd is full-colour pixel art by canon |
| ground is ONE flat palette colour | PASS |
| face-on and flat, no perspective or isometric | PASS |
| at most 4 elements, generous negative space | PASS (bar, cords, column set, Clawd) |
| no text, letters, numbers, UI chrome | PASS |
| any face is a single-line ink profile | **DECLARED EXCEPTION** — same reason |

## Files

- `race-to-the-top.png` — the finished plate
- `stage-c.png` (+ recipe) — the ink stage actually used, cords converging on the hoist point
- `stage-b.png` (+ recipe) — earlier stage, cords rising straight from the bar ends. Kept because a
  render is not reproducible: Clawd read as perched rather than hoisting, which is what motivated
  the converging-cord version.
- `raise-the-bar-a.png` (+ recipe) — the first pass, before Clawd was in it: a loopy pack-style hand
  raising the bar. Superseded by Gary's direction, kept as history.

Nothing here is locked.

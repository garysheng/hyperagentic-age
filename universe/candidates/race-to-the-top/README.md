# Race to the top

Symbolic plate for Anthropic's **race to the top**: a practice that is both good and good for
business gets adopted by competitors, and the waterline rises for everybody. Daniela Amodei's own
framing, from the Sixth Street interview ingested 2026-08-08 into the campaign's inspo archive:
*"if you can find the intersection of something that is actually good and is good for business...
that just raises the waterline for everybody."*

## The symbol

Angel Clawd hoists a standard on two cords. The bar is high and **empty**: nothing rests on it and
nothing touches it but the cords. Below, a field of columns climbs left to right toward it.

The emptiness is the argument. Race-to-the-top is not the leader winning the height, it is the
height becoming the new floor for the field. Nobody is pushed down; the floor is what moved.

## How it was made

**One render. No compositing.** Gary's direction (2026-08-08): *"Generate from scratch no
compositing dawg. Use Abu features."*

Produced through `abu:on-brand-image` with BOTH framework features doing their job:

- `--style-pack anthropic-plate` supplies the stage medium: wobbly single-weight ink, flat
  ivory-cream fills, one flat terracotta ground, its rejected poles as negatives.
- `--entity <universe>:angel-clawd@wings-raised` resolves the LOCKED alt-look, puts
  `reference/angel-clawd/wings-raised/hero.png` FIRST in the reference order (ahead of the pack
  anchor, because a pack pulls hard toward its own faces), and bakes the entity's live invariants
  and `prose.rules` into the prompt. Nine references went to the model in that order.

That entity path is why Clawd survives the pack instead of being dissolved into ink: canon says
Clawd is **never restyled into ink-and-wash**, and the entity's own rules ride into the prompt to
enforce it. The two mediums coexist in one generated frame, which is the point.

## Read-back, three rolls

The pack gate plus the entity's invariants, checked against actual pixels each time. Renders are not
reproducible, so every roll is kept.

| roll | verdict |
|---|---|
| `rtt-entity-a` | **DEFECT** on the alt-look invariant `wings-raised-into-an-uplifted-V-tips-above-the-head-line`: wing tips came back level with the head, not above it. Otherwise strong; bar filled, cords with eyelets. |
| `rtt-entity-b` | Wings **PASS** after an explicit counter-clause. New **DEFECT**: the bar came back a hollow outline, against the pack's flat-ivory-fill rule. |
| `rtt-entity-c` | **ALL PASS.** Shipped as `race-to-the-top.png`. |

Final verdict on the shipped plate:

| assertion | verdict |
|---|---|
| recognizably the coral pixel critter, blocky silhouette | PASS |
| eyes are the blessed happy closed arcs, no glints | PASS |
| little dangling legs below the body in flight | PASS |
| scalloped cream wings growing from BEHIND the body, never in front | PASS |
| wings raised into an uplifted V, tips above the head line | PASS |
| floating heart level with the halo | PASS |
| accessories only from canon (halo + heart) | PASS |
| single-weight wobbly BLACK ink line (stage) | PASS |
| ground is ONE flat palette colour | PASS |
| face-on and flat, no perspective or isometric | PASS |
| at most 4 elements (Clawd, cords, bar, column set) | PASS |
| no text, letters, numbers, UI chrome | PASS |
| pack: fills are flat ivory-cream only | **DECLARED EXCEPTION** — Clawd is full-colour pixel art, per its `registerNeutral` medium exception |
| pack: any face is a single-line ink profile | **DECLARED EXCEPTION** — same reason |
| entity: transparent ground on every deliverable | **N/A** — that invariant governs the mascot's own sheets, not a scene the mascot appears in |

## Files

- `race-to-the-top.png` (+ recipe) — the finished plate, identical to `rtt-entity-c`
- `rtt-entity-a/b/c.png` (+ recipes) — the three rolls above, all kept
- `superseded-composite/` — the FIRST approach, before Gary's "no compositing" direction: an ink
  stage generated with the upper-centre deliberately left empty, with the locked Clawd sheet pasted
  in afterward. It worked and is kept as history, but it is not how this is made now. Also holds
  `raise-the-bar-a.png`, the earliest pass with a pack-style loopy hand instead of Clawd.

Nothing here is locked.

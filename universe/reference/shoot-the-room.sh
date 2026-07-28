#!/usr/bin/env bash
# Shoot the new entities for "The Room It Was Made In".
# CHAINED: `night` off `wide`, so both states are unmistakably ONE room. Generated in
# parallel they come back as two different offices and the book's spine object dies.
set -euo pipefail

U="$HOME/Documents/github-repos/hyperagentic-age/universe"
GEN="$HOME/.agents/skills/chatgpt-images/scripts/generate_image.py"
ANCHOR="$U/reference/style/warm-editorial-neutral/refs/warm-editorial-swatch.png"

STYLE="Match the FIRST reference image for MEDIUM, BRUSHWORK, PALETTE and LIGHT QUALITY ONLY, and take NO subject from it. The medium is WARM EDITORIAL INK-AND-WASH illustration: soft illustrative linework, warm restrained colour, gentle washes. NOT neon, NOT 3D or CGI or Pixar, NOT glossy plastic, NOT neo-comic, NO HUD or arc-reactor vocabulary. ONE single full-bleed image: never a grid of panels, never a contact sheet."

NOBRAND="NO branding of any kind, NO logos, NO slogans or motivational text on the walls, NO readable writing anywhere, NO neon."

shoot () {
  local out="$1"; shift; local prompt="$1"; shift; local size="$1"; shift
  local args=(--input-image "$ANCHOR"); for r in "$@"; do args+=(--input-image "$r"); done
  echo "=== $out ==="
  uv run "$GEN" "${args[@]}" --filename "$out" --size "$size" --quality high --no-open --prompt "$prompt"
}

WANT="${1:-all}"; want () { [ "$WANT" = "all" ] || [ "$WANT" = "$1" ]; }

if want wide; then
  shoot "$U/reference/the-room/wide.png" \
"$STYLE

An ORDINARY LONG WORKING ROOM in a plain building, the kind of space a small company grows into rather than commissions. Seen from INSIDE the room at standing eye height, looking down its length.

Plain desks pushed together in IRREGULAR CLUSTERS with MISMATCHED CHAIRS. Monitors and laptops. A whiteboard with half-erased diagrams. Printouts taped to a wall. Mugs, an open notebook, cables, a shelf of well-used books. Big plain windows down one side letting in daylight.

It is LIVED-IN and slightly untidy, with evidence of people everywhere: a jacket over a chair back, a half-drunk coffee. NO people are in this plate.

It must NOT look impressive. NO soaring ceiling, NO atrium, NO glass conference boxes, NO rows of identical monitors, NO tech-campus gloss, NO dramatic lighting. The light is simply whatever the room has.

$NOBRAND" 1536x1024
fi

if want night; then
  shoot "$U/reference/the-room/night.png" \
"$STYLE

The OTHER reference image shows this exact room in daylight. Keep the SAME room: the same desk clusters in the same places, the same whiteboard, the same windows, the same shelf, the same camera position down the length of the room. Change ONLY the light and the time.

NOW IT IS NIGHT. Most overhead lights are off. Two or three pools of DESK LAMP light. The screens are the brightest things in the room. The windows are dark and reflect the room back into itself.

Still lived-in and untidy. NO people are in this plate. Still NOT dramatic: this is an ordinary room late, not a cinematic set.

$NOBRAND" 1536x1024
fi

if want bedrooms; then
  shoot "$U/reference/the-childhood-bedrooms/grid.png" \
"$STYLE

A single screen filled with a GRID OF VIDEO-CALL TILES, seen straight on so the grid fills most of the frame.

BEHIND EVERY SINGLE FACE IS A DIFFERENT CHILDHOOD BEDROOM. Teenage relics are visible and specific and different in each tile: a band poster nobody ever took down, a shelf of old paperbacks, a sports trophy, a narrow single bed, patterned wallpaper no adult would choose, a shelf of childhood models.

The faces are SMALL, TIRED and ORDINARY, mid-work, mixed in age and gender and ethnicity. Nobody is posing, nobody is presenting, nobody is heroic.

The light in every tile is WARM, LAMPLIT and DOMESTIC, the opposite of corporate video conferencing.

NO readable text anywhere: no names under the tiles, no writing on any poster, no interface labels or buttons. $NOBRAND" 1536x1024
fi

if want bridge; then
  shoot "$U/reference/the-bridge-feature/hero.png" \
"$STYLE

A close, warm study of an ORDINARY DESK SURFACE with a plain mug of tea on it, steam rising.

AND THE STEAM IS A BRIDGE. The rising steam forms, softly and unmistakably, the towers and sweeping cables of a SUSPENSION BRIDGE, glowing gently in INTERNATIONAL ORANGE. It is woven into the steam where it plainly does not belong.

The register is DELIGHT and gentle absurdity: the feeling of meeting somebody with one enormous enthusiasm they cannot stop mentioning. A viewer should smile before they work out why.

It is NOT ominous, NOT monumental, NOT a postcard or touristic view of a real landmark, and it does NOT dominate the frame as spectacle. It is a small warm joke living inside an ordinary object.

NO people in frame. $NOBRAND" 1536x1024
fi

if want makers; then
  shoot "$U/reference/the-makers/master.png" \
"$STYLE

A CHARACTER-ENSEMBLE REFERENCE: FIVE ordinary people who build things together, standing and seated in a loose informal group against a plain warm neutral background with no room and no scenery.

They are visibly MIXED IN AGE, GENDER AND ETHNICITY, in ordinary comfortable work clothes: sweaters, plain shirts, jeans. NO suits and NO branded merchandise.

They read as capable and unremarkable, absorbed and at ease. CRITICAL: NO SINGLE FIGURE is centred, elevated, lit differently or framed as the leader. They are a group, not a leader with an audience. Nobody is posing for a company photograph.

They are archetypes and must NOT resemble any identifiable real people. $NOBRAND" 1024x1536
fi
echo done.

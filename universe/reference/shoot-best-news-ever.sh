#!/usr/bin/env bash
# Shoot the reference matrix for the NEW entities of "The Best News Ever".
#
# CHAINING: the two states of `the-posted-promise` are the book's whole argument, so
# `every-door` is chained off `one-door`. Generated in parallel they come back as two
# different streets and the visual rhyme dies. The two characters are independent of
# each other and of the promise, so they run in parallel.
#
# The register anchor is CONTENT-NEUTRAL here (a warm-editorial swatch), so its subject
# cannot leak the way a character-portrait anchor does. It is still passed FIRST.
set -euo pipefail

U="$HOME/Documents/github-repos/hyperagentic-age/universe"
GEN="$HOME/.agents/skills/chatgpt-images/scripts/generate_image.py"
ANCHOR="$U/reference/style/warm-editorial-neutral/refs/warm-editorial-swatch.png"

PROMISE='NEVER HAND OUT MORE FIRE THAN YOU CAN MAKE SAFE'

STYLE="Match the FIRST reference image for MEDIUM, BRUSHWORK, PALETTE and LIGHT QUALITY ONLY, and take NO subject from it. The medium is WARM EDITORIAL INK-AND-WASH illustration: soft illustrative linework, warm restrained colour, gentle washes. It is NOT neon, NOT 3D or CGI or Pixar, NOT glossy plastic, NOT neo-comic, and carries NO HUD or arc-reactor comic vocabulary. ONE single full-bleed image: never a grid, never split panels, never a contact sheet."

shoot () {
  local out="$1"; shift; local prompt="$1"; shift
  local args=(--input-image "$ANCHOR")
  for r in "$@"; do args+=(--input-image "$r"); done
  echo "=== $out ==="
  uv run "$GEN" "${args[@]}" --filename "$out" --size 1024x1536 \
      --quality high --no-open --prompt "$prompt"
}

WANT="${1:-all}"; want () { [ "$WANT" = "all" ] || [ "$WANT" = "$1" ]; }

# ---------------------------------------------------------------- spine object
if want one-door; then
  shoot "$U/reference/the-posted-promise/one-door.png" \
"$STYLE

An ordinary working street of small workshops, seen straight on in daylight. Plain wooden doors along it.

ONE door, near the centre and closest to the viewer, has a promise HAND-PAINTED DIRECTLY ONTO THE WOOD in plain, legible, unornamented capital letters. Paint on wood, nothing more: it is NOT a hung sign, NOT a brass plaque, NOT a banner, and it carries NO logo, mark, signature or date.

THE LETTERING MUST READ EXACTLY, spelled correctly and completely, with no other words added:
'$PROMISE'

EVERY OTHER DOOR IN VIEW IS COMPLETELY BLANK. The painted door should read as a single eccentric choice on an ordinary street, mildly odd, not a monument. NO glow, NO halo, NO radiance of any kind: it is a working man's paint on a working door.

No people anywhere in this image. Warm, plain daylight."
fi

if want every-door; then
  shoot "$U/reference/the-posted-promise/every-door.png" \
"$STYLE

The OTHER reference image shows this exact street already painted. Keep the SAME street, the SAME door design, the SAME camera position and the SAME light. Change ONE thing only.

NOW EVERY DOOR IN VIEW CARRIES THE IDENTICAL PROMISE, hand-painted directly onto the wood in the same plain hand, the same plain capitals. The nearest door's lettering is fully legible and must read EXACTLY, spelled correctly and completely:
'$PROMISE'

Doors further down the street carry the same painted words, growing smaller and less legible with distance in the natural way.

This is ORDINARY now, not a celebration. NO banners, NO bunting, NO crowd, NO ceremony, NO glow and NO halo. It is simply how doors are painted on this street.

No people anywhere in this image. Warm, plain daylight." \
    "$U/reference/the-posted-promise/one-door.png"
fi

# ---------------------------------------------------------------- characters
if want copier; then
  shoot "$U/reference/the-first-copier/master.png" \
"$STYLE

A FULL-LENGTH STANDING CHARACTER REFERENCE of one man, seen from the front, head to feet, against a plain warm neutral background with no room and no scenery.

THE MAN: a BRISK, CAPABLE WORKSHOP OWNER in middle age. Practical, well-kept working clothes: a work coat or a sturdy apron over ordinary clothes. Short practical hair. He wears NO round thin-rimmed glasses.

His expression is level, businesslike and a little impatient, the face of a competent man who is thinking about cost. He is NOT a villain: no sneer, no shadowed eyes, no scheming look. He is equally NOT humbled, NOT admiring, NOT repentant.

He is an ARCHETYPE and must NOT resemble any real, identifiable company, lab or public person.

ONE single figure, one single image."
fi

if want builder; then
  shoot "$U/reference/the-young-builder/master.png" \
"$STYLE

A FULL-LENGTH STANDING CHARACTER REFERENCE of one young woman, seen from the front, head to feet, against a plain warm neutral background with no room and no scenery.

THE WOMAN: at the very START of her working life, early twenties. Practical NEW work clothes, clean and not yet worn in. Hair tied back practically. Capable and unremarkable in the best way.

Her expression is ABSORBED and MATTER-OF-FACT, the look of someone getting on with a task. She is NOT wide-eyed, NOT awed, NOT reverent, NOT grateful and NOT inspired. Ordinary competence.

ONE single figure, one single image."
fi
echo done.

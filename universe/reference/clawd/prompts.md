# clawd — generation prompts

**Plain Clawd: the base pixel critter, no angel elements.** Sibling of `angel-clawd`;
same medium exception, same identity source, same transparency recipe.

**REGISTER EXCEPTION (canon/craft/pixel-mascot-medium-exception.json + `structured.registerNeutral`).**
Never pass the warm-editorial register anchor or its rejected poles on any shot of this entity.
The medium line in each prompt leads instead.

**IDENTITY REF ON EVERY SHOT:** `reference/angel-clawd/source/clawd-clean-screenshot.png`
(Gary's clean screenshot of the canonical pixel Clawd: coral front-facing stepped body, two
black square eyes, mid-body side stubs, four dangling legs, no accessories), passed as the
FIRST input image on every shot.

**TRANSPARENCY RECIPE:** gpt-image-2 rejects `background: transparent`, so every shot is
prompted onto a single flat solid field of pure bright green `#00FF00`, then keyed with the
framework keyer (`on-brand-image/scripts/chroma_key.py`, defaults), cropped to the alpha bbox
and padded. Keyed finals + derived recipes land via `abu import-asset`.

**Shot settings:** `--size 1024x1024 --quality high`, model `gpt-image-2`.

## hero  -> reference/clawd/hero.png

NOT shot directly. The hero slot is filled by locking the candidate Gary blesses from
`candidates/clawd/` (`abu lock-shot ... --recipe ...`). Until he blesses one, this slot
stays empty on purpose.

## detail  -> reference/clawd/detail.png

NOT shot directly. A crop-zoom of the blessed hero's load-bearing details (eyes, stepped
silhouette), imported with a derived recipe after the hero locks.

## candidates

Shared template for all candidate shots:

> Using the first reference image as the exact character identity: it shows a small coral
> pixel critter (the Anthropic "Clawd" pixel mascot) — a front-facing stepped blocky coral
> body with a raised head block, two black square eyes, one small stub arm on each side of
> the mid-body, and four little legs below. Redraw THIS SAME CRITTER, plain and unadorned
> (NO wings, NO halo, NO heart, NO accessories), in a cute designed-sticker pixel-art style:
> crisp flat blocky pixel shapes with a soft, plush, charming energy — not a rigid grid
> port, not mushy painterly rendering, not 3D, not glossy.
>
> THE CRITTER: stepped blocky coral body (coral #DD775B, slightly darker #c05f45 shading low
> on the body, a lighter #ea9077 highlight band near the top), and little pixel legs below.
>
> THE GROUND: the critter floats centered on a single flat solid field of pure bright green
> #00FF00 and nothing else — no shadow, no reflection, no surface, no other elements, no text.

### v1-faithful — eyes exactly as the reference: two big dark square eyes, each with a single small white glint; standing square and symmetrical, stubs relaxed at the sides.

### v2-contented — eyes as two dark upturned contented arcs (happy closed eyes, no glints); standing square, stubs relaxed.

### v3-wave — eyes as the reference (open, glinted); one stub arm raised in a cheerful little wave, body tilted a pixel-step to the side.

### v4-bounce — eyes as the reference (open, glinted); caught mid-bounce a little off the ground, legs dangling, joyful energy.

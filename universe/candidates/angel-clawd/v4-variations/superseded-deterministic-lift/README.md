# superseded: deterministic part-shift lifts

First attempt at "heart and wings slightly higher" (2026-08-08). Rather than re-prompt, these
segmented the blessed `v4d-happy-eyes.png` into halo / heart / wings / body and translated two
parts upward by 20, 40 and 60 px — zero model drift by construction, via
`scripts/shift_sprite_parts.py`.

Gary chose to regenerate from scratch instead ("regen from scratch with a slight modification to
the prompt we originally used"). The blessed results are `v4d-lift-b` (locked as the default hero)
and `v4d-lift-c` (locked as the `wings-raised` alt-look).

Kept as history, not as deliverables. The segmentation tool stays useful: it is the cheap way to
answer "move this part" without paying a re-roll or risking the character.

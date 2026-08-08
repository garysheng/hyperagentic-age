#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow", "numpy", "scipy"]
# ///
"""
Shift named parts of a keyed pixel-art sprite, deterministically.

WHY THIS EXISTS: `angel-clawd` v4d is BLESSED art — it is on Gary's real ordered shirts.
Asking an image model for "the same mascot but with the heart higher" re-paints the whole
character and drifts the thing that was blessed. Moving a part is a translation, and a
translation is arithmetic, so it renders in code (SPEC 4.11: anything whose correctness is
a number is drawn, never prompted). Same pixels, new position, zero drift.

SEGMENTATION, in the order it runs:
  1. Connected components over the alpha mask separate anything that does not touch the
     body. On v4d that is exactly the halo and the heart.
  2. Inside the largest component (body + wings, which touch), parts split by SATURATION:
     the wings are cream (~0.06) and the body is coral (~0.60), so a 0.30 cut is nowhere
     near either cluster. Eyes are near-black and get assigned to the body by luminance,
     not saturation, since black is saturation-undefined.
  3. Any pixel not claimed by a named part stays put.

Z-ORDER on recomposite is wings, body, halo, heart — the body must cover the wing roots or
lifted wings read as detached. Parts are pasted with alpha compositing onto an empty canvas
of the original size, so a shifted part vacates cleanly instead of smearing.

Usage:
  uv run scripts/shift_sprite_parts.py IN.png OUT.png --shift wings=-40 --shift heart=-40
  uv run scripts/shift_sprite_parts.py IN.png --debug-masks masks.png
Negative dy is up. Part names: wings, body, halo, heart.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SAT_CUT = 0.30
DARK_CUT = 60  # max channel below this is an eye/outline, not a wing


def segment(rgba: np.ndarray) -> dict[str, np.ndarray]:
    rgb, al = rgba[..., :3].astype(int), rgba[..., 3]
    vis = al > 16

    lab, n = ndimage.label(vis)
    sizes = [(lab == i).sum() for i in range(1, n + 1)]
    if not sizes:
        raise SystemExit("error: nothing visible in this image")
    main_idx = int(np.argmax(sizes)) + 1

    # Loose components: name them by where they sit and how yellow they are.
    parts: dict[str, np.ndarray] = {}
    for i in range(1, n + 1):
        if i == main_idx:
            continue
        m = lab == i
        mean = rgb[m].mean(axis=0)
        # halo is yellow (green channel close to red); heart is red (green far below red)
        name = "halo" if mean[1] > mean[0] * 0.75 else "heart"
        parts[name] = parts.get(name, np.zeros_like(vis)) | m

    main = lab == main_idx
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0.0)

    wings = main & (sat < SAT_CUT) & (mx >= DARK_CUT)
    body = main & ~wings

    # The saturation cut leaves speckle: peach-tinted feather shading reads as body-colored
    # and would stay behind as stray dots when the wings lift. The body is one solid blob
    # (the eyes are enclosed by it, so they ride along), therefore anything body-classified
    # that is NOT part of that blob is feather shading and belongs to the wings.
    blab, bn = ndimage.label(body)
    if bn > 1:
        bsizes = [(blab == i).sum() for i in range(1, bn + 1)]
        keep = int(np.argmax(bsizes)) + 1
        strays = body & (blab != keep)
        body = blab == keep
        wings = wings | strays

    parts["wings"] = wings
    parts["body"] = body
    return parts


def recomposite(rgba: np.ndarray, parts: dict[str, np.ndarray], shifts: dict[str, int]) -> Image.Image:
    h, w = rgba.shape[:2]
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src = Image.fromarray(rgba.astype(np.uint8), "RGBA")

    claimed = np.zeros((h, w), dtype=bool)
    for m in parts.values():
        claimed |= m

    order = ["wings", "body", "halo", "heart"]
    layers = [("_unclaimed", ~claimed & (rgba[..., 3] > 0))]
    layers += [(k, parts[k]) for k in order if k in parts]

    for name, mask in layers:
        if not mask.any():
            continue
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        layer.paste(src, (0, 0), Image.fromarray((mask * 255).astype(np.uint8), "L"))
        dy = shifts.get(name, 0)
        if dy:
            layer = Image.fromarray(np.roll(np.asarray(layer), dy, axis=0))
            # np.roll wraps; blank the wrapped band so nothing reappears on the far edge
            arr = np.asarray(layer).copy()
            if dy < 0:
                arr[dy:, :, 3] = 0
            else:
                arr[:dy, :, 3] = 0
            layer = Image.fromarray(arr, "RGBA")
        canvas = Image.alpha_composite(canvas, layer)
    return canvas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path, nargs="?")
    ap.add_argument("--shift", action="append", default=[], metavar="PART=DY",
                    help="vertical shift in px, negative is up (repeatable)")
    ap.add_argument("--debug-masks", type=Path, help="write a color-coded segmentation map and exit")
    args = ap.parse_args()

    rgba = np.asarray(Image.open(args.src).convert("RGBA"))
    parts = segment(rgba)
    for k, m in parts.items():
        print(f"  {k:6s} {m.sum():>7} px")

    if args.debug_masks:
        colors = {"wings": (60, 160, 255), "body": (255, 90, 90), "halo": (255, 215, 0), "heart": (170, 60, 220)}
        out = np.zeros((*rgba.shape[:2], 3), dtype=np.uint8)
        for k, m in parts.items():
            out[m] = colors.get(k, (255, 255, 255))
        Image.fromarray(out).save(args.debug_masks)
        print(f"wrote {args.debug_masks}")
        return 0

    if not args.dst:
        print("error: need an output path (or --debug-masks)", file=sys.stderr)
        return 1

    shifts: dict[str, int] = {}
    for s in args.shift:
        k, _, v = s.partition("=")
        if k not in parts:
            print(f"error: unknown part {k!r}; have {sorted(parts)}", file=sys.stderr)
            return 1
        shifts[k] = int(v)

    recomposite(rgba, parts, shifts).save(args.dst)
    print(f"wrote {args.dst}  shifts={shifts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

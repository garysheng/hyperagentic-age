#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow", "numpy"]
# ///
"""
Key a greenscreen render to transparent, crop to content, optionally upscale.

WHY THIS EXISTS: image models garble letterforms less when they paint on a flat chroma
field than when asked for a transparent background, so the merch pipeline renders text
prints on #00FF00 and keys them afterward. That keying tail was hand-rolled three separate
times in the 2026-08-08 angel-clawd merch session and got filed as an open thread; this is
it paved. Fourth hand-roll refused.

The three steps, in this order, because each depends on the last:
  1. KEY    every pixel whose hue is near the chroma becomes transparent.
  2. DESPILL green light bounces onto cream edges and leaves a lime fringe; clamp the green
            channel to the max of red/blue. Skipping this is what makes a keyed print look
            cheap on a dark garment. Scope defaults to ALL visible pixels, not just the
            soft edge band: measured on the first real render, 2.7% of fully-opaque pixels
            were green-dominant, because the model paints the spill into the letterform
            rather than only into the antialiased boundary. Edge-only despill leaves those.
            This is safe for THIS palette, whose every ink (cream #fffdf7, burnt orange
            #b0512e, coral #DD775B) is red-dominant. Pass --despill edge for artwork that
            contains legitimately green pixels.
  3. CROP   to the alpha bounding box, then re-pad by a fixed transparent margin, so the
            print is the artwork and the placement is the POD tool's job. The 64px default
            reproduces the margin on the shipped 2026-08-08 back prints; POD previewers
            treat a print that bleeds to the file edge as one they may crop.

Note the screen these renders actually come back on is around #13EE19, not the #00FF00 the
prompt asks for, which is why the key is distance-based rather than an equality test.

Upscale is NEAREST by default and that is deliberate: these are flat pixel-art letterforms,
so nearest is lossless-looking at integer factors, while any smooth filter invents grey
edges on artwork that has none.

Usage:
  uv run scripts/key_greenscreen.py IN.png OUT.png
  uv run scripts/key_greenscreen.py IN.png OUT.png --upscale 4        # for POD upload
  uv run scripts/key_greenscreen.py IN.png OUT.png --chroma 00B140    # non-default screen
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def hex_to_rgb(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"chroma must be 6 hex digits, got {s!r}")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def key(
    img: Image.Image,
    chroma: tuple[int, int, int],
    tol: float,
    soft: float,
    despill: str,
) -> Image.Image:
    """Distance-based key with a soft edge band, then despill."""
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    target = np.array(chroma, dtype=np.float32)

    dist = np.sqrt(((rgb - target) ** 2).sum(axis=2))

    # Fully transparent inside `tol`, fully opaque beyond `tol + soft`, ramped between.
    alpha = np.clip((dist - tol) / max(soft, 1e-6), 0.0, 1.0)

    # Despill: green cannot exceed the warmer channels. See the module docstring for why
    # the default scope is every visible pixel rather than only the antialiased band.
    if despill != "none":
        scope = alpha > 0.0 if despill == "all" else (alpha > 0.0) & (alpha < 1.0)
        cap = np.maximum(rgb[..., 0], rgb[..., 2])
        spill = scope & (rgb[..., 1] > cap)
        rgb[..., 1] = np.where(spill, cap, rgb[..., 1])

    # ZERO THE RGB UNDER FULL TRANSPARENCY. A keyed pixel keeps whatever color it had, so a
    # "transparent" file is still a green file to anything that ignores or flattens alpha —
    # some POD previewers, some thumbnailers, and any downstream resize that blends colour
    # before it blends alpha. This is the repo's existing convention (see the v4d recipe
    # note, "RGB zeroed where alpha=0"); leaving it out is what made a keyed sprite render
    # back as a green rectangle.
    # Zero against the FINAL uint8 alpha, not the float: an alpha of 0.001 rounds to 0 in the
    # saved file while its RGB survives, which is exactly the leak this guards against.
    a8 = (alpha * 255).astype(np.uint8)
    rgb[a8 == 0] = 0

    out = np.dstack([rgb.astype(np.uint8), a8])
    return Image.fromarray(out, mode="RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--chroma", default="00FF00", help="screen color hex (default 00FF00)")
    ap.add_argument("--tol", type=float, default=110.0, help="RGB distance fully keyed (default 110)")
    ap.add_argument("--soft", type=float, default=60.0, help="width of the soft edge band (default 60)")
    ap.add_argument("--upscale", type=int, default=1, help="integer NEAREST upscale after crop (default 1)")
    ap.add_argument("--despill", choices=["all", "edge", "none"], default="all",
                    help="scope of green-spill correction (default all visible pixels)")
    ap.add_argument("--pad", type=int, default=64, help="transparent margin re-added after crop (default 64)")
    ap.add_argument("--no-crop", dest="crop", action="store_false", default=True)
    ap.add_argument("--canvas", metavar="WxH", help="center the result on a transparent print canvas, "
                                                   "auto-picking the largest integer NEAREST upscale that fits")
    ap.add_argument("--dpi", type=int, help="DPI metadata to stamp (POD tools read it for physical size)")
    args = ap.parse_args()

    if not args.src.exists():
        print(f"error: no such file: {args.src}", file=sys.stderr)
        return 1

    img = Image.open(args.src)
    keyed = key(img, hex_to_rgb(args.chroma), args.tol, args.soft, args.despill)

    if args.crop:
        bbox = keyed.getchannel("A").getbbox()
        if bbox is None:
            print("error: everything keyed out — wrong --chroma, or --tol too high", file=sys.stderr)
            return 1
        keyed = keyed.crop(bbox)
        if args.pad > 0:
            p = args.pad
            padded = Image.new("RGBA", (keyed.width + 2 * p, keyed.height + 2 * p), (0, 0, 0, 0))
            padded.paste(keyed, (p, p))
            keyed = padded

    if args.upscale > 1:
        w, h = keyed.size
        keyed = keyed.resize((w * args.upscale, h * args.upscale), Image.NEAREST)

    if args.canvas:
        cw, _, ch = args.canvas.lower().partition("x")
        cw, ch = int(cw), int(ch)
        # Integer factor only: a fractional resize would resample hard pixel edges into grey.
        factor = max(1, min(cw // keyed.width, ch // keyed.height))
        keyed = keyed.resize((keyed.width * factor, keyed.height * factor), Image.NEAREST)
        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        canvas.paste(keyed, ((cw - keyed.width) // 2, (ch - keyed.height) // 2))
        keyed = canvas
        print(f"  canvas {cw}x{ch}, nearest x{factor}")

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    save_kw = {"dpi": (args.dpi, args.dpi)} if args.dpi else {}
    keyed.save(args.dst, **save_kw)

    opaque = int((np.asarray(keyed.getchannel("A")) > 0).sum())
    total = keyed.size[0] * keyed.size[1]
    print(f"keyed {img.size} -> {keyed.size}  ({100 * opaque / total:.1f}% ink)  {args.dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

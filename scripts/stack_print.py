#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow", "numpy"]
# ///
"""
Stack keyed PNGs into one print-ready lockup on a transparent print canvas.

WHY THIS EXISTS: a shirt lockup is a mascot above text, and BOTH halves already exist as
approved artwork by the time you assemble them — the mascot is a locked canon sheet and the
text is its own keyed render. Assembly is therefore arithmetic (scale to a target width,
center, space, place on the canvas), and arithmetic is drawn in code, never prompted. Asking
an image model to draw "the mascot with the words under it" re-paints a locked entity and
garbles the letterforms in one move.

This is the third time in this merch line that pieces have been composited by hand, so it is
paved. The sibling `generators/shirt-lockup` does the same job for text it TYPESETS itself in
Charter/Anton; this one is for lockups whose text is an imported keyed raster, which is the
look Gary blessed for back prints.

Layers are TRIMMED to their alpha bounding box first, then scaled to a fraction of the canvas
width (--widths), stacked in argument order with --gap between them, and the whole block is
centered on the canvas. Trimming matters: every keyed PNG carries transparent padding from the
keyer, so an untrimmed --gap is the space between padded RECTANGLES and the visible gap comes
out larger than the number says, differently for each layer. With --trim (the default) the gap
is between the artwork you can actually see, which is the only thing anyone is judging. Scaling is LANCZOS by default
because a lockup usually scales DOWN; pass --nearest to keep hard pixel edges when scaling up.

Usage:
  uv run scripts/stack_print.py OUT.png mascot.png text.png \
      --canvas 4500x5400 --dpi 300 --widths 0.55,0.92 --gap 260
"""

import argparse
import sys
from pathlib import Path

from PIL import Image


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dst", type=Path)
    ap.add_argument("layers", type=Path, nargs="+", help="keyed PNGs, top to bottom")
    ap.add_argument("--canvas", default="4500x5400", metavar="WxH")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--widths", required=True,
                    help="comma-separated target width per layer, as a fraction of canvas width")
    ap.add_argument("--gap", type=int, default=200, help="vertical gap between layers in px")
    ap.add_argument("--nearest", action="store_true", help="NEAREST resampling (use when scaling up)")
    ap.add_argument("--no-trim", dest="trim", action="store_false", default=True,
                    help="keep each layer's transparent padding instead of measuring the real ink")
    args = ap.parse_args()

    cw, _, ch = args.canvas.lower().partition("x")
    cw, ch = int(cw), int(ch)

    fracs = [float(f) for f in args.widths.split(",")]
    if len(fracs) != len(args.layers):
        print(f"error: {len(fracs)} widths for {len(args.layers)} layers", file=sys.stderr)
        return 1

    resample = Image.NEAREST if args.nearest else Image.LANCZOS
    scaled = []
    for path, frac in zip(args.layers, fracs):
        if not path.exists():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1
        im = Image.open(path).convert("RGBA")
        if args.trim:
            bbox = im.getchannel("A").getbbox()
            if bbox:
                im = im.crop(bbox)
        w = int(cw * frac)
        scaled.append(im.resize((w, max(1, round(im.height * w / im.width))), resample))

    block_h = sum(im.height for im in scaled) + args.gap * (len(scaled) - 1)
    if block_h > ch:
        print(f"error: stacked block is {block_h}px tall, canvas is {ch}px. "
              f"Reduce --widths or --gap.", file=sys.stderr)
        return 1

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    y = (ch - block_h) // 2
    for im in scaled:
        canvas.paste(im, ((cw - im.width) // 2, y), im)
        y += im.height + args.gap

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.dst, dpi=(args.dpi, args.dpi))
    print(f"stacked {len(scaled)} layers -> {cw}x{ch} @{args.dpi}dpi  (block {block_h}px)  {args.dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

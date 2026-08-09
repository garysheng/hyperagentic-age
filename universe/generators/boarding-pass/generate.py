#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""
Draw the READY FOR TAKEOFF boarding-pass back print. Deterministic, no image model.

Every knob lives in generator.json; this file reads it and retypes nothing. A boarding pass
is dense small text plus ruled geometry, which is the exact thing image models garble and the
exact thing code renders perfectly, so per SPEC 4.11 it is DRAWN. The only rastered input is
the locked angel-clawd sheet, composited on the stub and never re-generated here.

ONE INK. Everything is cream #fffdf7 on transparency, so it screen-prints as a single colour
on a dark garment. Where the design looks like it has a second colour (the header bar, the
seat chip) that is KNOCKOUT: a filled cream shape with the letters punched back out to
transparency, so the shirt itself shows through. That is why the drawing order matters and
why text inside a filled block is drawn with alpha 0 rather than a dark fill.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "generator.json").read_text())
P = CFG["params"]

CREAM = tuple(int(P["ink"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)
CLEAR = (0, 0, 0, 0)


def font(role: str, size: int) -> ImageFont.FreeTypeFont:
    f = P["fonts"][role]
    return ImageFont.truetype(f["path"], size=size, index=f.get("index", 0))


def fit(role: str, text: str, target_w: int, max_h: int | None = None) -> ImageFont.FreeTypeFont:
    """Largest size whose rendered width fits target_w (and height fits max_h)."""
    lo, hi = 8, 600
    while lo < hi:
        mid = (lo + hi + 1) // 2
        fnt = font(role, mid)
        box = fnt.getbbox(text)
        if (box[2] - box[0]) <= target_w and (max_h is None or (box[3] - box[1]) <= max_h):
            lo = mid
        else:
            hi = mid - 1
    return font(role, lo)


def text_at(d: ImageDraw.ImageDraw, xy, text, fnt, fill=CREAM, anchor="la"):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def render(measure_only: bool):
    """Draw the ticket. Returns the y the content ends at.

    Called TWICE: once against a scratch canvas purely to learn how tall the content is,
    then for real with the outline sized to hug it. A boarding pass with a hand-guessed
    height leaves a dead band under the stub, and the height depends on how big the
    auto-fitted type came out, so it cannot be known before laying the type out."""
    cw, ch = P["canvas"]
    img = Image.new("RGBA", (cw, ch), CLEAR)
    d = ImageDraw.Draw(img)

    m = P["margin"]
    stroke = P["stroke"]
    x0, x1 = m, cw - m
    inner = x1 - x0
    pad = P["innerPad"]
    lx, rx = x0 + pad, x1 - pad

    # ---- ticket outline -------------------------------------------------
    y0 = P["ticketTop"]
    y1 = ch - P["ticketBottomMargin"] if measure_only else BOTTOM[0]
    d.rounded_rectangle([x0, y0, x1, y1], radius=P["corner"], outline=CREAM, width=stroke)

    # ---- header bar, knockout ------------------------------------------
    hb = P["headerBarHeight"]
    d.rounded_rectangle([x0, y0, x1, y0 + hb], radius=P["corner"], fill=CREAM)
    # square off the bar's bottom corners so it reads as a bar, not a pill
    d.rectangle([x0, y0 + hb - P["corner"], x1, y0 + hb], fill=CREAM)
    hf = fit("display", P["header"], int(inner * 0.52), int(hb * 0.52))
    text_at(d, (lx, y0 + hb // 2), P["header"], hf, fill=CLEAR, anchor="lm")
    ff = fit("display", P["flight"], int(inner * 0.28), int(hb * 0.42))
    text_at(d, (rx, y0 + hb // 2), P["flight"], ff, fill=CLEAR, anchor="rm")

    y = y0 + hb + P["rowGap"]

    def label(txt, yy):
        lf = font("label", P["labelSize"])
        text_at(d, (lx, yy), txt, lf)
        return yy + P["labelSize"] + P["labelGap"]

    def value(txt, yy, frac=0.92):
        vf = fit("display", txt, int(inner * frac) - 2 * pad)
        box = vf.getbbox(txt)
        text_at(d, (lx, yy - box[1]), txt, vf)
        return yy + (box[3] - box[1]) + P["rowGap"]

    y = label(P["rows"]["passengerLabel"], y)
    y = value(P["rows"]["passenger"], y)

    y = label(P["rows"]["fromLabel"], y)
    y = value(P["rows"]["from"], y)

    y = label(P["rows"]["toLabel"], y)
    y = value(P["rows"]["to"], y)

    # ---- gate / seat / boards strip -------------------------------------
    y += P["rowGap"] // 2
    cellw = (rx - lx) // 3
    sf = font("label", P["labelSize"])
    vf = font("display", P["stripValueSize"])
    for i, (lab, val) in enumerate(P["strip"]):
        cx = lx + i * cellw
        text_at(d, (cx, y), lab, sf)
        text_at(d, (cx, y + P["labelSize"] + P["labelGap"]), val, vf)
    y += P["labelSize"] + P["labelGap"] + P["stripValueSize"] + P["rowGap"]

    # ---- perforation ----------------------------------------------------
    perf_y = y + P["rowGap"]
    dash, gap = P["dash"]
    x = x0 + P["notchRadius"] + dash
    while x < x1 - P["notchRadius"] - dash:
        d.line([x, perf_y, min(x + dash, x1 - P["notchRadius"] - dash), perf_y],
               fill=CREAM, width=P["perfWidth"])
        x += dash + gap
    # notches: punch the outline open so the stub reads as tear-off
    nr = P["notchRadius"]
    for cx in (x0, x1):
        d.ellipse([cx - nr, perf_y - nr, cx + nr, perf_y + nr], fill=CLEAR)

    # ---- stub: mascot + status + barcode --------------------------------
    sy = perf_y + P["rowGap"]
    mascot_path = (HERE / P["mascot"]).resolve()
    if not mascot_path.exists():
        print(f"error: mascot not found: {mascot_path}", file=sys.stderr)
        return 1
    mas = Image.open(mascot_path).convert("RGBA")
    bbox = mas.getchannel("A").getbbox()
    if bbox:
        mas = mas.crop(bbox)
    mw = int(inner * P["mascotWidthFrac"])
    mas = mas.resize((mw, round(mas.height * mw / mas.width)), Image.LANCZOS)
    img.paste(mas, (lx, sy), mas)

    tx = lx + mw + P["stubGap"]
    stf = font("label", P["labelSize"])
    text_at(d, (tx, sy + P["statusLabelOffset"]), P["statusLabel"], stf)
    stv = fit("display", P["status"], rx - tx)
    sb = stv.getbbox(P["status"])
    text_at(d, (tx, sy + P["statusLabelOffset"] + P["labelSize"] + P["labelGap"] - sb[1]),
            P["status"], stv)

    # barcode: deterministic bar widths from a fixed pattern, not randomness
    by = sy + P["statusLabelOffset"] + P["labelSize"] + P["labelGap"] + sb[3] - sb[1] + P["rowGap"]
    bx = tx
    for i, w in enumerate(P["barcodePattern"]):
        if i % 2 == 0:
            d.rectangle([bx, by, bx + w, by + P["barcodeHeight"]], fill=CREAM)
        bx += w
        if bx > rx:
            break

    content_end = max(sy + mas.height, by + P["barcodeHeight"])
    if measure_only:
        return content_end, None

    out = HERE / P["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, dpi=(P["dpi"], P["dpi"]))
    print(f"wrote {out}  {img.size} @{P['dpi']}dpi  ticket bottom {y1}")

    (out.with_suffix(".png.recipe.json")).write_text(json.dumps({
        "asset": out.name,
        "provenance": "generated",
        "generator": "generators/boarding-pass/generate.py",
        "deterministic": True,
        "inputs": [P["mascot"]],
        "note": "Deterministic single-ink boarding-pass back print. Text is typeset by freetype "
                "at final size; the only raster input is the locked angel-clawd sheet.",
        "params": P,
    }, indent=2) + "\n")
    return content_end, out


BOTTOM = [0]


def main() -> int:
    content_end, _ = render(measure_only=True)
    BOTTOM[0] = content_end + P["ticketBottomPad"]
    render(measure_only=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

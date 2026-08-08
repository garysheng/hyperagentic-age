#!/usr/bin/env python3
"""shirt-lockup — deterministic T-shirt lockup typesetter (SPEC §4.11 generator).

The mascot (blessed angel-Clawd v4d, keyed, imported with a derived recipe) is COMPOSITED;
the text is TYPESET by freetype from vector outlines at final print size. No image model
touches this generator. Every knob lives in generator.json; this file retypes nothing.

Design beliefs stated so the proof can disprove them:
- BELIEF: both stacked lines fit-to-width ("ANTHROPIC" wide, "MOM" narrower-but-taller)
  reads as one lockup rather than two stickers. Checked on the proof sheet.
- BELIEF: 0.18em tracking on the subline caps is the quiet-second-voice sweet spot; 0.10
  read as cramped and 0.25 as dotted-line in a quick scratch test at 300px.

Fit-to-width uses ADVANCE width (kerned, via font.getlength) for untracked lines and
per-glyph advances + tracking for tracked lines; the drawn line is then cropped to its
INK bbox and centered, so serif overshoot cannot skew centering.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "generator.json").read_text())
P = MANIFEST["params"]
OUT = HERE / "out"
PROOF = HERE / "proof"
TILES = PROOF / "tiles"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def load_font(key: str, size: int) -> ImageFont.FreeTypeFont:
    spec = P["fonts"][key]
    return ImageFont.truetype(spec["path"], size, index=spec["index"])


def line_width(text: str, font: ImageFont.FreeTypeFont, tracking_px: float) -> float:
    if tracking_px == 0:
        return font.getlength(text)  # whole-string: kerning preserved
    return sum(font.getlength(c) for c in text) + tracking_px * (len(text) - 1)


def fit_size(font_key: str, text: str, target_w: int, tracking_em: float = 0.0) -> int:
    """Largest integer size whose advance width <= target_w."""
    lo, hi = 8, 4000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        f = load_font(font_key, mid)
        if line_width(text, f, tracking_em * mid) <= target_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


def render_line(text: str, font_key: str, size: int, color: str, tracking_em: float = 0.0) -> Image.Image:
    """Draw one line on a transparent layer, crop to ink bbox."""
    font = load_font(font_key, size)
    tracking_px = tracking_em * size
    w = int(line_width(text, font, tracking_px)) + size
    h = size * 3
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = size / 2
    if tracking_px == 0:
        d.text((x, size), text, font=font, fill=color)
    else:
        for c in text:
            d.text((x, size), c, font=font, fill=color)
            x += font.getlength(c) + tracking_px
    return layer.crop(layer.getbbox())


def build_text_block(variant: dict) -> Image.Image:
    t = P["treatments"][variant["treatment"]]
    colors = P["colors"]
    main_color = colors[variant["textColor"]]
    font_key = variant["font"]

    if t["kind"] == "stacked":
        imgs = []
        for text, width in zip(t["lines"], t["lineWidths"]):
            size = fit_size(font_key, text, width)
            imgs.append(render_line(text, font_key, size, main_color))
        gap = t["lineGap"]
    else:  # headline-subline; subline is a LIST of lines, all set at one size
        h_size = fit_size(font_key, t["headline"], t["headlineWidth"])
        head = render_line(t["headline"], font_key, h_size, main_color)
        sub_font_key = "serifSub" if font_key == "serif" else font_key
        sub_color = colors[variant.get("sublineColor", variant["textColor"])]
        tr = t["sublineTrackingEm"]
        s_size = min(fit_size(sub_font_key, line, t["sublineWidth"], tr)
                     for line in t["sublineLines"])
        subs = [render_line(line, sub_font_key, s_size, sub_color, tr)
                for line in t["sublineLines"]]
        # compose head + sub-lines with their own gaps, then hand ONE list downstream
        imgs, gap = [head] + subs, t["subGap"]
        if len(subs) > 1:
            sub_gap = t["sublineLineGap"]
            bw = max(i.width for i in subs)
            bh = sum(i.height for i in subs) + sub_gap * (len(subs) - 1)
            block = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
            y = 0
            for i in subs:
                block.paste(i, ((bw - i.width) // 2, y), i)
                y += i.height + sub_gap
            imgs = [head, block]

    bw = max(i.width for i in imgs)
    bh = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    block = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    y = 0
    for i in imgs:
        block.paste(i, ((bw - i.width) // 2, y), i)
        y += i.height + gap
    return block


def mascot_path(variant: dict) -> Path:
    return HERE / P["mascots"][variant["mascot"]]


def build_lockup(variant: dict, mascot: Image.Image) -> Image.Image:
    t = P["treatments"][variant["treatment"]]
    W, H = P["canvas"]
    margin = P["margin"]

    mw = t["mascotWidth"]
    mh = round(mascot.height * mw / mascot.width)
    m = mascot.resize((mw, mh), Image.LANCZOS)

    text = build_text_block(variant)
    total_h = mh + t["mascotGap"] + text.height
    avail_h = H - 2 * margin
    assert total_h <= avail_h, f"{variant['id']}: stack {total_h}px exceeds print area {avail_h}px"

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = margin + (avail_h - total_h) // 2
    canvas.paste(m, ((W - mw) // 2, y), m)
    canvas.paste(text, ((W - text.width) // 2, y + mh + t["mascotGap"]), text)
    return canvas


def write_recipe(out_path: Path, variant: dict, m_path: Path) -> None:
    font_keys = {variant["font"], "serifSub" if variant["font"] == "serif" else variant["font"]}
    recipe = {
        "asset": out_path.name,
        "method": "generator",
        "generator": {"id": MANIFEST["id"], "entrypoint": MANIFEST["entrypoint"],
                      "determinism": MANIFEST["determinism"]},
        "params": P,
        "variant": variant,
        "inputs": [{
            "path": f"generators/shirt-lockup/{P['mascots'][variant['mascot']]}",
            "sha256": sha256(m_path),
            "note": f"blessed angel-Clawd {variant['mascot']}, keyed; derived recipe beside it records the chain back to the gpt-image-2 greenscreen render",
        }],
        "fonts": [{**P["fonts"][k], "sha256": sha256(Path(P["fonts"][k]["path"]))} for k in sorted(font_keys)],
        "dpi": P["dpi"],
        "printArea": "15x18in at 300 DPI",
    }
    recipe["sha256"] = sha256(out_path)
    out_path.with_name(out_path.name + ".recipe.json").write_text(json.dumps(recipe, indent=2))


def proof_tile(lockup: Image.Image, ground_hex: str) -> Image.Image:
    tw, th = P["proof"]["tile"]
    tile = Image.new("RGBA", (tw, th), ground_hex)
    pw = round(tw * P["proof"]["printWidthFrac"])
    ph = round(lockup.height * pw / lockup.width)
    small = lockup.resize((pw, ph), Image.LANCZOS)
    tile.paste(small, ((tw - pw) // 2, round(th * P["proof"]["printTopFrac"])), small)
    return tile


def main() -> None:
    OUT.mkdir(exist_ok=True)
    TILES.mkdir(parents=True, exist_ok=True)
    mascots = {k: Image.open(HERE / rel).convert("RGBA") for k, rel in P["mascots"].items()}

    grounds = P["proof"]["grounds"]
    label_font = load_font("proofLabel", 26)
    tw, th = P["proof"]["tile"]
    gutter = P["proof"]["labelGutter"]
    pad = 14
    variants = P["variants"]

    sheet = Image.new("RGBA", (gutter + (tw + pad) * len(grounds) + pad,
                               60 + (th + pad) * len(variants) + pad), "#efe9df")
    sd = ImageDraw.Draw(sheet)
    for gi, gname in enumerate(grounds):
        sd.text((gutter + pad + gi * (tw + pad) + tw // 2, 30), gname,
                font=label_font, fill="#211d18", anchor="mm")

    for vi, variant in enumerate(variants):
        lockup = build_lockup(variant, mascots[variant["mascot"]])
        out_path = OUT / f"{variant['id']}.png"
        lockup.save(out_path, dpi=(P["dpi"], P["dpi"]))
        write_recipe(out_path, variant, mascot_path(variant))
        print(f"out/{out_path.name}  {lockup.width}x{lockup.height}")

        y = 60 + pad + vi * (th + pad)
        sd.text((24, y + th // 2), variant["id"], font=label_font, fill="#211d18", anchor="lm")
        for gi, ghex in enumerate(grounds.values()):
            tile = proof_tile(lockup, ghex)
            tile.save(TILES / f"{variant['id']}_on_{ghex.lstrip('#')}.png")
            sheet.paste(tile, (gutter + pad + gi * (tw + pad), y))

    sheet_path = PROOF / "contact-sheet.png"
    sheet.convert("RGB").save(sheet_path)
    print(f"proof: {sheet_path}")


if __name__ == "__main__":
    main()

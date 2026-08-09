#!/usr/bin/env python3
"""Clawd master generator.

Draws the Clawd pixel critter deterministically from a measured block grid.
The grid was recovered from Gary's canonical reference screenshots
(reference/clawd/source/) by run-length analysis, not by eye:

  torso 8x6 units at canvas (2,0) on a 12x8 canvas
  stubs 2x2 at rows 2-3, flush to the canvas edges
  legs  1x2 at rows 6-7, at torso columns 0,2,5,7
  eyes  at row 1, torso columns 1 and 6

ONE geometry function (`shapes`) is the single source of truth. The SVG writer
and the PNG rasterizer both consume its output, so no coordinate is ever
retyped in two places (the classic generator bug: two constants that silently
mean different things).

Every knob lives in generator.json params; nothing geometric is hardcoded here.
Run:  uv run --with pillow python3 generate.py
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "generator.json").read_text())
P = CFG["params"]


def shapes(style):
    """The ONE geometry source. Returns [(x, y, w, h, color), ...] in pixels."""
    u = P["unit"]
    cw = P["canvasUnits"][0]
    t, stub, legs, eyes = P["torso"], P["stub"], P["legs"], P["eyes"]
    body, eye_color = P["colors"]["body"], P["colors"]["eye"]
    out = [
        (t["x"] * u, t["y"] * u, t["w"] * u, t["h"] * u, body),
        (0, stub["y"] * u, stub["w"] * u, stub["h"] * u, body),
        ((cw - stub["w"]) * u, stub["y"] * u, stub["w"] * u, stub["h"] * u, body),
    ]
    for col in legs["torsoCols"]:
        out.append(((t["x"] + col) * u, legs["y"] * u, legs["w"] * u, legs["h"] * u, body))

    spec = P["eyeStyles"][style]
    for col in eyes["torsoCols"]:
        cx = (t["x"] + col + 0.5) * u
        cy = (eyes["row"] + 0.5) * u
        if style == "scrunch":
            # chevron drawn from the pattern matrix in params; left eye ">", right eye mirrored "<"
            pat = spec["pattern"]
            rows, cols = len(pat), len(pat[0])
            bw, bh = spec["w"] * u / cols, spec["h"] * u / rows
            mirror = col != eyes["torsoCols"][0]
            for r, row in enumerate(pat):
                for cc, on in enumerate(row):
                    if not on:
                        continue
                    ccx = (cols - 1 - cc) if mirror else cc
                    out.append((cx - spec["w"] * u / 2 + ccx * bw,
                                cy - spec["h"] * u / 2 + r * bh, bw, bh, eye_color))
        else:
            w, h = spec["w"] * u, spec["h"] * u
            out.append((cx - w / 2, cy - h / 2, w, h, eye_color))
    return out


def to_svg(style):
    w_px = P["canvasUnits"][0] * P["unit"]
    h_px = P["canvasUnits"][1] * P["unit"]
    rects = "\n  ".join(
        f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{c}"/>'
        for x, y, w, h, c in shapes(style)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_px}" height="{h_px}" '
        f'viewBox="0 0 {w_px} {h_px}" shape-rendering="crispEdges">\n  {rects}\n</svg>\n'
    )


def to_png(style, scale=4):
    from PIL import Image, ImageDraw

    w_px = P["canvasUnits"][0] * P["unit"] * scale
    h_px = P["canvasUnits"][1] * P["unit"] * scale
    im = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y, w, h, c in shapes(style):
        d.rectangle(
            [round(x * scale), round(y * scale), round((x + w) * scale) - 1, round((y + h) * scale) - 1],
            fill=c,
        )
    return im


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from PIL import Image

    out = HERE / "out"
    out.mkdir(exist_ok=True)
    rendered = []
    for style in P["eyeStyles"]:
        svg_path, png_path = out / f"clawd-{style}.svg", out / f"clawd-{style}.png"
        svg_path.write_text(to_svg(style))
        to_png(style).save(png_path)
        recipe = {
            "generator": CFG["id"],
            "determinism": CFG["determinism"],
            "params": P,
            "style": style,
            "inputs": CFG["inputs"],
            "note": "Deterministic SVG/PNG from a measured grid. Re-running reproduces byte-identical output.",
        }
        for p in (svg_path, png_path):
            (p.parent / f"{p.name}.recipe.json").write_text(
                json.dumps({**recipe, "sha256": sha(p)}, indent=2)
            )
        rendered.append((style, png_path))
        print(f"  + out/{svg_path.name}  + out/{png_path.name}")

    proof = HERE / "proof"
    proof.mkdir(exist_ok=True)
    big, gap = 340, 40
    sheet = Image.new("RGBA", (len(rendered) * (big + gap) + gap, big + 210), (247, 244, 237, 255))
    for i, (style, png) in enumerate(rendered):
        im = Image.open(png).convert("RGBA")
        im.thumbnail((big, big), Image.NEAREST)
        x0 = gap + i * (big + gap)
        sheet.paste(im, (x0, gap + (big - im.height) // 2), im)
        for j, px in enumerate((16, 32, 64)):
            sm = Image.open(png).convert("RGBA")
            sm.thumbnail((px, px), Image.NEAREST)
            sheet.paste(sm, (x0 + j * 90, big + 110), sm)
    sheet.convert("RGB").save(proof / "contact-sheet.png")
    print(f"  + proof/contact-sheet.png  ({', '.join(s for s, _ in rendered)} at {big}px + 16/32/64)")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Clawd trait composer.

Composes a Clawd from a trait selection into layered SVG. The body grid is the
one measured from Gary's reference screenshots (see ../clawd-master); traits are
pixel patterns anchored against that same grid, so a hat lands on his head and a
held item lands at his stub no matter what else is selected.

ONE geometry function (`shapes`) is the single source of truth; the SVG writer
and the PNG rasterizer both consume it, so no coordinate is retyped.

  python3 compose.py --traits '{"bodyColor":"coral","eyes":"pupil",...}'
  python3 compose.py --seed 1234          # deterministic pick from rarity weights
  python3 compose.py --sheet 24           # a proof sheet of N random Clawds
"""
import argparse, hashlib, json, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = json.loads((HERE / "traits.json").read_text())
EYES = json.loads((HERE.parent / "clawd-master" / "generator.json").read_text())["params"]["eyeStyles"]
G, ANCH = T["grid"], T["anchors"]
RARITY_WEIGHT = {"common": 60, "uncommon": 25, "rare": 12, "legendary": 3}
LAYERS = {"bodyColor": "bodyColors", "headwear": "headwear", "held": "held",
          "background": "backgrounds", "effect": "effects"}


def pick(rng, table):
    keys = list(table)
    return rng.choices(keys, weights=[RARITY_WEIGHT[table[k].get("rarity", "common")] for k in keys])[0]


def roll(seed):
    rng = random.Random(seed)
    out = {k: pick(rng, T[tbl]) for k, tbl in LAYERS.items()}
    out["eyes"] = rng.choice(list(EYES))
    return out


def pattern_shapes(spec, u):
    """A trait's pixel pattern, placed by its anchor.

    Items draw on the FINER item grid (grid.itemPixel), so a hat can carry a
    brim and a pom while the body keeps its chunky blocks. Anchors stay in body
    units; only the cell size differs.
    """
    pat, pal = spec["pattern"], spec["palette"]
    widths = {len(r) for r in pat}
    if len(widths) > 1:  # a ragged pattern shears the shape and is always a typo
        raise ValueError(f"pattern rows must all be the same width, got {sorted(widths)}")
    px = G["itemPixel"] * u
    rows, cols = len(pat), max(len(r) for r in pat)
    a = ANCH[spec["anchor"]]
    x0 = a["centerX"] * u - cols * px / 2 if "centerX" in a else a["leftX"] * u
    y0 = (a["bottomY"] - spec.get("offsetY", 0)) * u - rows * px
    return [(x0 + c * px, y0 + r * px, px, px, pal[ch])
            for r, row in enumerate(pat) for c, ch in enumerate(row) if ch != "."]


def eye_shapes(style, u, eye_color, pupil):
    px = G["eyePixel"] * u
    spec, out = EYES[style], []
    for i, col in enumerate(G["eyes"]["torsoCols"]):
        cx = (G["torso"]["x"] + col + 0.5) * u
        cy = (G["eyes"]["row"] + 0.5) * u
        pat = spec["pattern"]
        if i == 1:
            pat = spec.get("patternRight") or ([r[::-1] for r in pat] if spec.get("mirror", True) else pat)
        rows, cols = len(pat), len(pat[0])
        ex, ey = cx - cols * px / 2, cy - rows * px / 2
        out += [(ex + c * px, ey + r * px, px, px, eye_color if v == 1 else pupil)
                for r, row in enumerate(pat) for c, v in enumerate(row) if v]
    return out


def shapes(traits, seed=0):
    """THE geometry source: every rect in draw order."""
    u = G["unit"]
    cw, ch = G["canvas"]
    t, stub, legs = G["torso"], G["stub"], G["legs"]
    body = T["bodyColors"][traits["bodyColor"]]["body"]
    out = []

    # contrast guard: never render a body on a background it disappears into
    bgkey = traits["background"]
    if bgkey in T.get("contrast", {}).get("avoid", {}).get(traits["bodyColor"], []):
        bgkey = T["contrast"]["fallback"]
    bg = T["backgrounds"][bgkey]["fill"]
    if bg:
        out.append((0, 0, cw * u, ch * u, bg))

    eff = T["effects"][traits["effect"]]
    if eff.get("kind"):
        rng = random.Random(f"{seed}:{traits['effect']}")
        for _ in range(eff["count"]):
            gx, gy = rng.randrange(cw), rng.randrange(ch)
            h = u * (2 if eff["kind"] == "rain" else 1)
            out.append((gx * u, gy * u, u * 0.6, h * 0.6, rng.choice(eff["colors"])))

    out.append((t["x"] * u, t["y"] * u, t["w"] * u, t["h"] * u, body))
    out.append(((t["x"] - stub["w"]) * u, stub["y"] * u, stub["w"] * u, stub["h"] * u, body))
    out.append(((t["x"] + t["w"]) * u, stub["y"] * u, stub["w"] * u, stub["h"] * u, body))
    for col in legs["torsoCols"]:
        out.append(((t["x"] + col) * u, legs["y"] * u, legs["w"] * u, legs["h"] * u, body))

    dark = traits["bodyColor"] in ("ink",)
    out += eye_shapes(traits["eyes"], u, "#F7F4ED" if dark else "#141414", "#141414" if dark else "#FFFFFF")

    for layer in ("headwear", "held"):
        spec = T[LAYERS[layer]][traits[layer]]
        if "pattern" in spec:
            out += pattern_shapes(spec, u)
    return out


def to_svg(traits, seed=0):
    w, h = G["canvas"][0] * G["unit"], G["canvas"][1] * G["unit"]
    rects = "\n  ".join(f'<rect x="{x:g}" y="{y:g}" width="{rw:g}" height="{rh:g}" fill="{c}"/>'
                        for x, y, rw, rh, c in shapes(traits, seed))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">\n  {rects}\n</svg>\n')


def to_png(traits, seed=0, scale=2):
    from PIL import Image, ImageDraw
    w, h = G["canvas"][0] * G["unit"] * scale, G["canvas"][1] * G["unit"] * scale
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y, rw, rh, c in shapes(traits, seed):
        d.rectangle([round(x * scale), round(y * scale),
                     round((x + rw) * scale) - 1, round((y + rh) * scale) - 1], fill=c)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traits"); ap.add_argument("--seed", type=int); ap.add_argument("--sheet", type=int)
    ap.add_argument("--out", default="out/clawd.png")
    a = ap.parse_args()
    if a.sheet:
        from PIL import Image
        n, cols = a.sheet, 6
        rows = (n + cols - 1) // cols
        cell = 300
        sheet = Image.new("RGB", (cols * cell + 40, rows * cell + 40), (247, 244, 237))
        for i in range(n):
            tr = roll(i)
            im = to_png(tr, i); im.thumbnail((cell - 30, cell - 30), Image.NEAREST)
            sheet.paste(im, (20 + (i % cols) * cell + (cell - im.width) // 2,
                             20 + (i // cols) * cell + (cell - im.height) // 2), im)
        Path("proof").mkdir(exist_ok=True)
        sheet.save("proof/roll-sheet.png")
        print(f"proof/roll-sheet.png  ({n} rolled Clawds)")
        return
    traits = json.loads(a.traits) if a.traits else roll(a.seed or 0)
    seed = a.seed or 0
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_bytes(b"") if False else to_png(traits, seed).save(a.out)
    Path(a.out).with_suffix(".svg").write_text(to_svg(traits, seed))
    print(json.dumps(traits), "->", a.out)


if __name__ == "__main__":
    main()

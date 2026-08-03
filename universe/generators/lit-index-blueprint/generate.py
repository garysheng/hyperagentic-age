#!/usr/bin/env python3
"""Draw the geometry seed for `the-lit-index`.

A blueprint, not a picture. It fixes the ONE thing every state of this visual
metaphor must agree on (a complete 7x5 grid of identical upright panels, even
gutters, a threshold line across the lower third) and argues nothing else: no
surface, no colour, no lighting, no material. That is deliberate. A multi-state
object seeded off one of its own state plates inherits that state's paint and the
three states come back as three different objects; seeded off a schematic, they
inherit only the shape.

Deterministic graphics render in code, never through an image model. Prompting
for a grid produces a grid that is nearly regular, and "nearly regular" is the
exact failure this entity's invariants forbid.

    python3 generate.py [--out out/blueprint.png]

Every knob lives in generator.json `params` rather than in this file, and any
value used twice is DERIVED once here rather than retyped.
"""
import argparse
import hashlib
import json
import pathlib
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("needs pillow:  uv run --with pillow python3 generate.py")

HERE = pathlib.Path(__file__).parent
SPEC = json.loads((HERE / "generator.json").read_text())
P = SPEC["params"]

INK = (26, 26, 26)
FAINT = (150, 150, 150)


def geometry():
    """Every derived number in one place. Two constants that silently mean
    different things is the characteristic bug of this primitive, so nothing
    below is recomputed anywhere else in the file."""
    w, h = P["canvas"]
    cols, rows = P["cols"], P["rows"]
    # DERIVE FROM HEIGHT, not width. Seven columns of 0.62-aspect panels over five
    # rows makes a grid that is very nearly square (w/h about 0.88), so in any
    # landscape canvas HEIGHT is the binding constraint. Solving from width instead
    # was the first version's bug: it produced a grid 1073px tall in a 1024px
    # canvas, clipped top and bottom, with the threshold line running straight
    # through the two lowest rows.
    #   grid_h = rows * panel_h + (rows - 1) * gutterFraction * panel_h
    grid_h = h * P["gridHeightFraction"]
    panel_h = grid_h / (rows + (rows - 1) * P["gutterFraction"])
    gutter_y = panel_h * P["gutterFraction"]
    pitch_y = panel_h + gutter_y
    # `gutterFraction` is a fraction OF THE PANEL, used exactly once per axis, and
    # the gutter is EQUAL in both axes so the grid reads as regular. panel_w
    # follows from panel_h and the aspect, so the two can never be derived
    # independently and drift apart, which is this primitive's characteristic bug.
    panel_w = panel_h * P["panelAspect"]
    gutter_x = gutter_y
    pitch_x = panel_w + gutter_x
    grid_h_true = rows * pitch_y - gutter_y
    grid_w_true = cols * pitch_x - gutter_x
    grid_h = grid_h_true

    cx, cy = P["gridCenter"]
    x0 = w * cx - grid_w_true / 2
    y0 = h * cy - grid_h / 2
    return dict(w=w, h=h, cols=cols, rows=rows, panel_w=panel_w, panel_h=panel_h,
                gutter_x=gutter_x, gutter_y=gutter_y, pitch_x=pitch_x, pitch_y=pitch_y,
                x0=x0, y0=y0, grid_w=grid_w_true, grid_h=grid_h)


def draw(path):
    g = geometry()
    img = Image.new("RGB", (g["w"], g["h"]), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # The slight left skew: each row further UP is nudged right by a constant, so
    # the plane reads as seen-from-the-left rather than as a flat diagram. It is a
    # shear, not a perspective: a true vanishing point would make the panels
    # different sizes, and identical size is an invariant.
    skew_total = g["w"] * P["leftSkew"]
    skew_per_row = skew_total / max(g["rows"] - 1, 1)

    for r in range(g["rows"]):
        # row 0 is the TOP row, so the top of the wall is pushed furthest right
        dx = skew_per_row * (g["rows"] - 1 - r)
        for c in range(g["cols"]):
            x = g["x0"] + c * g["pitch_x"] + dx
            y = g["y0"] + r * g["pitch_y"]
            d.rounded_rectangle([x, y, x + g["panel_w"], y + g["panel_h"]],
                                radius=g["panel_w"] * 0.12, outline=INK, width=3)

    ty = g["h"] * P["thresholdY"]
    d.line([(0, ty), (g["w"], ty)], fill=INK, width=5)
    for x in range(0, g["w"], 34):
        d.line([(x, ty + 12), (x + 16, ty + 12)], fill=FAINT, width=2)

    d.text((28, ty + 26), "THRESHOLD  |  below and in front = REAL (solid, shadowed)", fill=INK)
    d.text((28, ty + 44), "above and behind = DIGITAL (translucent, glowing, casts light)", fill=INK)
    d.text((28, 24), f"the-lit-index  geometry seed  |  {g['cols']}x{g['rows']} identical panels, "
                     f"even gutters, complete grid", fill=INK)
    d.text((28, 42), "LINE ONLY. No surface, colour, material or lighting is specified here.", fill=FAINT)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return g


def recipe(path, g):
    """Same provenance contract as any other asset, different fields: the
    generator and its params instead of a provider and a prompt."""
    rec = {
        "asset": path.name,
        "method": "generator",
        "generator": {"id": SPEC["id"], "entrypoint": SPEC["entrypoint"],
                      "determinism": SPEC["determinism"]},
        "params": P,
        "derived": {k: round(v, 3) for k, v in g.items() if isinstance(v, float)},
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    path.with_suffix(path.suffix + ".recipe.json").write_text(
        json.dumps(rec, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / SPEC["outputs"][0]["path"]))
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    g = draw(out)
    recipe(out, g)

    # Proof at real size is the gate for a generator: it is reproducible, so it
    # needs one honest look rather than a per-run read-back.
    proof = HERE / SPEC["proof"]["sheet"]
    proof.parent.mkdir(parents=True, exist_ok=True)
    Image.open(out).save(proof)

    print(f"wrote {out}  ({g['cols']}x{g['rows']} = {g['cols'] * g['rows']} panels, "
          f"panel {g['panel_w']:.1f}x{g['panel_h']:.1f}px, gutter {g['gutter_x']:.1f}px)")
    print(f"proof {proof}")


if __name__ == "__main__":
    main()

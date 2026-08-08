#!/usr/bin/env python3
"""Draw Angel Clawd, the pixel angel mascot, at print scale on transparency.

GENERATOR-SHAPED, NOT PROMPT-SHAPED. The mascot already exists as deterministic
rectangles-only SVG code (tastefulstories/src/app/story/Clawd.tsx); pixel art
prompted from an image model comes back mushy, so every variant here is COMPUTED:
the base geometry is a faithful port of that file's <rect> lists, the right wing
is DERIVED by mirroring the left about the body axis (verified against the tsx:
the source's hand-written right wing is an exact mirror), and every variation
knob (accessory, wing pose, palette, sizes) lives in generator.json params.

    python3 generate.py            # all variants + detail + proof + install

Design decisions, stated so they can be disproven cheaply (SPEC 4.11):
- shape-rendering=crispEdges: pixel art wants hard edges, and anti-aliasing
  abutting rects onto transparency leaves hairline seams. crispEdges kills both.
- mono variants knock the EYES out to transparency via an SVG mask, then draw the
  glints back in the mono colour: a single-colour print with solid eyes is a blob.
- raised wings are a per-column vertical shear (further from the body = lifted
  more), never a rotation, which would break the pixel grid.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
SPEC = json.loads((HERE / "generator.json").read_text())
P = SPEC["params"]

RSVG = "rsvg-convert"

# ---------------------------------------------------------------------------
# Base geometry: faithful port of Clawd.tsx. Each rect is (x, y, w, h, role).
# Roles map to palette keys so palettes are data, not code.
# The body axis of symmetry is x = 61 (body 28..94, stubs 17..105).
AXIS = 61.0

HEART = [(52, -8, 4, 4), (60, -8, 4, 4), (48, -4, 20, 4),
         (48, 0, 20, 4), (52, 4, 12, 4), (56, 8, 4, 4)]

# Left wing only; the right wing is derived by mirroring about AXIS.
WING_LEFT = (
    [(x, y, w, h, "wingSwoop") for (x, y, w, h) in
     [(12, 10, 18, 5), (-2, 4, 18, 5), (-16, -2, 16, 5), (-30, -8, 16, 5), (-42, -14, 12, 5)]] +
    [(x, y, w, h, "wingWhite") for (x, y, w, h) in
     [(-40, -9, 9, 18), (-29, -3, 9, 20), (-18, 3, 9, 22), (-7, 9, 9, 24), (4, 15, 9, 25)]] +
    [(x, y, w, h, "wingCream") for (x, y, w, h) in
     [(-24, 21, 9, 15), (-13, 27, 9, 17), (-2, 33, 9, 18), (9, 38, 9, 16)]] +
    [(x, y, w, h, "wingWhite") for (x, y, w, h) in
     [(1, 51, 8, 9), (11, 54, 8, 9)]]
)

LEGS = [(34, 66, 9, 15), (64, 66, 9, 15),   # pair a
        (49, 66, 9, 17), (79, 66, 9, 17)]   # pair b

BODY = [(34, 24, 54, 8, "bodyHi"),
        (28, 30, 66, 32, "body"),
        (28, 62, 66, 6, "bodyShade"),
        (17, 44, 11, 11, "body"),          # left stub
        (17, 52, 11, 3, "bodyShade"),
        (94, 44, 11, 11, "body"),          # right stub
        (94, 52, 11, 3, "bodyShade")]

EYES = [(42, 38, 10, 11), (68, 38, 10, 11)]
GLINTS = [(44, 40, 3, 3), (70, 40, 3, 3)]

# Halo: a flattened pixel ring floating above the head (body top is y=24).
HALO = [(51, 0, 20, 4, "haloHi"),                    # top bar (highlight)
        (45, 4, 6, 4, "halo"), (71, 4, 6, 4, "halo"),  # sides
        (51, 8, 20, 4, "halo")]                      # bottom bar

# When the halo occupies the spot over the head, the heart floats up-right.
HEART_SHIFT_WITH_HALO = (34, -10)

# Checkered racing flag, held at the RIGHT side stub (stub 94..105, y 44..55).
# Pole runs from above the head down past the stub; checks are 8px squares in a
# 6x4 grid with a gentle 2px stepped droop every two columns.
POLE = (105, -6, 4, 62)
FLAG_ORIGIN = (109, -6)
FLAG_COLS, FLAG_ROWS, FLAG_SQ, FLAG_DROOP = 6, 4, 8, 2

BODY_LEFT_EDGE = 28.0  # wing shear pivot; columns left of this lift when raised


def mirror(rects):
    """Right wing = left wing mirrored about the body axis."""
    return [(2 * AXIS - x - w, y, w, h, role) for (x, y, w, h, role) in rects]


def raise_wing(rects, k):
    """Per-column vertical shear: further from the body = lifted more."""
    out = []
    for (x, y, w, h, role) in rects:
        cx = x + w / 2
        dist = max(0.0, BODY_LEFT_EDGE - cx)
        out.append((x, y - round(k * dist), w, h, role))
    return out


def flag_rects():
    rects = [(POLE[0], POLE[1], POLE[2], POLE[3], "pole")]
    fx, fy = FLAG_ORIGIN
    for c in range(FLAG_COLS):
        droop = FLAG_DROOP * (c // 2)
        for r in range(FLAG_ROWS):
            role = "flagDark" if (c + r) % 2 == 0 else "flagLight"
            rects.append((fx + c * FLAG_SQ, fy + r * FLAG_SQ + droop, FLAG_SQ, FLAG_SQ, role))
    return rects


def build_variant(accessory, pose):
    """Return (rects, eye_rects, glint_rects). rects carry palette roles."""
    rects = []
    if accessory in ("heart", "halo-heart"):
        dx, dy = HEART_SHIFT_WITH_HALO if accessory == "halo-heart" else (0, 0)
        rects += [(x + dx, y + dy, w, h, "heart") for (x, y, w, h) in HEART]
    if accessory in ("halo", "halo-heart"):
        rects += HALO

    left = WING_LEFT if pose == "spread" else raise_wing(WING_LEFT, P["raiseK"])
    rects += left + mirror(left)

    rects += [(x, y, w, h, "leg") for (x, y, w, h) in LEGS]
    rects += BODY

    if accessory == "flag":
        rects += flag_rects()
    return rects


def bbox(rects, extra=()):
    xs = [r[0] for r in rects] + [r[0] + r[2] for r in rects]
    ys = [r[1] for r in rects] + [r[1] + r[3] for r in rects]
    for (x, y, w, h) in extra:
        xs += [x, x + w]; ys += [y, y + h]
    pad = P["padUnits"]
    x0, y0 = min(xs) - pad, min(ys) - pad
    return (x0, y0, max(xs) + pad - x0, max(ys) + pad - y0)


def svg_variant(variant, ground=None):
    """Emit the SVG for one variant. ground=None -> transparent (deliverable);
    a hex colour -> proof tile ground."""
    pal_name = variant["palette"]
    pal = P["palettes"][pal_name]
    mono = "mono" in pal
    rects = build_variant(variant["accessory"], variant["pose"])
    vb = bbox(rects, extra=EYES)
    if ground:
        # Proof tiles are SQUARE (ground-padded) so the framework contact-sheet
        # tool, which sizes every cell from the first image, distorts nothing.
        side = max(vb[2], vb[3])
        vb = (vb[0] - (side - vb[2]) / 2, vb[1] - (side - vb[3]) / 2, side, side)

    def fill(role):
        return pal["mono"] if mono else pal[role]

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
             f'viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" shape-rendering="crispEdges">']
    if ground:
        parts.append(f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{ground}"/>')

    if mono:
        # Knock the eyes out to transparency, then draw mono glints back in.
        parts.append('<mask id="eyeholes">')
        parts.append(f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>')
        for (x, y, w, h) in EYES:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="black"/>')
        parts.append('</mask>')
        parts.append('<g mask="url(#eyeholes)">')
        for (x, y, w, h, role) in rects:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill(role)}"/>')
        parts.append('</g>')
        for (x, y, w, h) in GLINTS:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal["mono"]}"/>')
    else:
        for (x, y, w, h, role) in rects:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal[role]}"/>')
        for (x, y, w, h) in EYES:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal["eye"]}"/>')
        for (x, y, w, h) in GLINTS:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal["glint"]}"/>')

    parts.append('</svg>')
    return "\n".join(parts), vb


def rasterize(svg_text, out_png, vb, long_edge):
    tmp = out_png.with_suffix(".svg.tmp")
    tmp.write_text(svg_text)
    size = ["-w", str(long_edge)] if vb[2] >= vb[3] else ["-h", str(long_edge)]
    subprocess.run([RSVG, *size, "-o", str(out_png), str(tmp)], check=True)
    tmp.unlink()


def recipe(png, variant, extra=None):
    rec = {
        "asset": png.name,
        "method": "generator",
        "generator": {"id": SPEC["id"], "entrypoint": SPEC["entrypoint"],
                      "determinism": SPEC["determinism"]},
        "params": P,
        "variant": variant,
        "geometrySource": "faithful port of tastefulstories/src/app/story/Clawd.tsx "
                          "(rectangles-only pixel SVG; right wing derived by mirror about x=61)",
        "sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
    }
    if extra:
        rec.update(extra)
    png.with_suffix(png.suffix + ".recipe.json").write_text(json.dumps(rec, indent=2) + "\n")
    return rec


def main():
    out_dir = HERE / "out"
    proof_dir = HERE / "proof" / "tiles"
    out_dir.mkdir(parents=True, exist_ok=True)
    proof_dir.mkdir(parents=True, exist_ok=True)

    deliverables = []
    for v in P["variants"]:
        png = out_dir / f"angel-clawd_{v['id']}_{P['longEdge']}.png"
        svg, vb = svg_variant(v)
        rasterize(svg, png, vb, P["longEdge"])
        recipe(png, v)
        deliverables.append(png)

        ground = P["grounds"][v["palette"]]
        tile = proof_dir / f"{v['id']}_on_{ground.lstrip('#')}.png"
        gsvg, gvb = svg_variant(v, ground=ground)
        rasterize(gsvg, tile, gvb, P["proofTilePx"])
        print(f"wrote {png.name}  viewBox {vb}")

    # Detail: crop-zoom of the load-bearing region (eyes, stubs, inner scallops)
    # rendered as its own tight viewBox, not a downstream raster crop.
    canonical = P["variants"][0]
    rects = build_variant(canonical["accessory"], canonical["pose"])
    pal = P["palettes"]["coral"]
    dvb = (-4, 18, 122, 52)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
             f'viewBox="{dvb[0]} {dvb[1]} {dvb[2]} {dvb[3]}" shape-rendering="crispEdges">']
    for (x, y, w, h, role) in rects:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal[role]}"/>')
    for (x, y, w, h) in EYES:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal["eye"]}"/>')
    for (x, y, w, h) in GLINTS:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{pal["glint"]}"/>')
    parts.append('</svg>')
    detail = out_dir / "detail.png"
    rasterize("\n".join(parts), detail, dvb, 2000)
    recipe(detail, {"id": "detail", "note": "crop-zoom viewBox of the canonical variant"})
    print(f"wrote {detail.name}")

    # 1:1 crop tile from the 3200px canonical master, for the crispness assertion.
    try:
        from PIL import Image
        master = Image.open(deliverables[0]).convert("RGBA")
        w, h = master.size
        cx, cy = int(w * 0.47), int(h * 0.42)  # eye region of the canonical frame
        side = P["proofTilePx"]
        crop = master.crop((cx, cy, cx + side, cy + side))
        base = Image.new("RGBA", crop.size, (255, 255, 255, 255))
        base.alpha_composite(crop)
        base.convert("RGB").save(proof_dir / "zz_1to1-crop_heart_coral.png")
    except ImportError:
        print("pillow missing: skipped the 1:1 crop tile", file=sys.stderr)

    # Install (idempotent; a byte copy is a transform and owns its recipe, v0.33).
    universe = HERE.parent.parent
    for src_rel, dests in SPEC["install"].items():
        src = HERE / src_rel
        for dest_rel in dests:
            dest = universe / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            changed = (not dest.exists()) or dest.read_bytes() != src.read_bytes()
            if changed:
                dest.write_bytes(src.read_bytes())
            src_recipe = json.loads(src.with_suffix(src.suffix + ".recipe.json").read_text())
            drec = {
                "asset": dest.name,
                "method": "derived",
                "derived": {"transform": "byte-copy install", "from": f"generators/{SPEC['id']}/{src_rel}",
                            "fromRecipe": src_recipe},
                "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            }
            dest.with_suffix(dest.suffix + ".recipe.json").write_text(json.dumps(drec, indent=2) + "\n")
            print(f"install {'wrote' if changed else 'unchanged'}  {dest_rel}")

    print(f"\n{len(deliverables)} deliverables in {out_dir}")
    print("now montage proof/tiles/ into proof/contact-sheet.png "
          "(render-readback/scripts/contact_sheet.py) and get a human approval.")


if __name__ == "__main__":
    main()

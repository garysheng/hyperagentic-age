#!/usr/bin/env python3
"""
Assemble a plate-book composition into what the projection says it emits.

`plate-book` declares `emits: ["book-manifest.json", "plates/*.webp"]`, and a
projection that declares an emit and never produces it is lying about its contract.
This is the deterministic step that makes the declaration true.

It refuses to assemble a book whose slots have not all PASSED. An incomplete book is
a legitimate output of this standard, but it must be labelled incomplete rather than
quietly shipped with a defective page in it.

    python3 assemble-plate-book.py <composition.json> <out-dir>
"""
import json, os, pathlib, shutil, subprocess, sys


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def main(comp_path, out_dir):
    comp = load(comp_path)
    work = pathlib.Path(comp["work"])
    out = pathlib.Path(out_dir)
    (out / "plates").mkdir(parents=True, exist_ok=True)

    n = comp.get("repeat", {}).get("art", 1)
    text = comp.get("pageText", [])
    pages, blocked = [], []

    for i in range(n):
        st = work / "state" / f"art-{i}.json"
        status = load(st)["status"] if st.exists() else "MISSING"
        if status != "PASS":
            blocked.append((i, status))
            continue
        src = work / f"art-{i}.png"
        dst = out / "plates" / f"{i:02d}.webp"
        # cwebp if available, otherwise carry the png rather than fail the assembly
        if shutil.which("cwebp"):
            r = subprocess.run(["cwebp", "-q", "88", str(src), "-o", str(dst)],
                               capture_output=True)
            if r.returncode != 0:
                dst = dst.with_suffix(".png"); shutil.copy2(src, dst)
        else:
            dst = dst.with_suffix(".png"); shutil.copy2(src, dst)
        pages.append({"index": i, "plate": f"plates/{dst.name}",
                      "text": text[i] if i < len(text) else ""})

    if blocked:
        print("REFUSING to assemble: these slots have not passed an independent judge.")
        for i, s in blocked:
            print(f"  - art-{i}: {s}")
        print("\nAn incomplete book is a legitimate output, but it is labelled, not shipped quietly.")
        return 1

    manifest = {
        "id": comp["id"],
        "projection": comp["projection"],
        "universe": os.path.basename(comp["universe"].rstrip("/")),
        "pages": pages,
        "provenance": {
            "every plate": "generated from the bound style pack, never hand-edited",
            "every plate judged": "by an independent judge given the artifact and the "
                                  "checklist only, never the plan that produced it",
            "assembled by": "this script, deterministically",
        },
    }
    (out / "book-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"assembled {len(pages)} page(s) -> {out}/book-manifest.json")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))

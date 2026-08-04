"""Extract every image/png output from notebooks/*.ipynb into figures/deck/.

Naming: <nbprefix>_c<cellidx:03d>_<n>.png where cellidx is the 0-based cell
index and n is a per-notebook running image counter (e.g. 13_c037_7.png).
Run from anywhere: paths are anchored to the repo root (parent of scripts/).
"""
import base64
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "figures" / "deck"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for nb_path in sorted((REPO / "notebooks").glob("*.ipynb")):
        prefix = nb_path.stem.split("_")[0]
        cells = json.loads(nb_path.read_text(encoding="utf-8"))["cells"]
        n = 0
        for cell_idx, cell in enumerate(cells):
            for out in cell.get("outputs", []):
                png_b64 = out.get("data", {}).get("image/png")
                if not png_b64:
                    continue
                n += 1
                name = f"{prefix}_c{cell_idx:03d}_{n}.png"
                (OUT / name).write_bytes(base64.b64decode(png_b64))
                total += 1
        print(f"{nb_path.name}: {n} figure(s)")
    print(f"wrote {total} PNGs to {OUT}")


if __name__ == "__main__":
    main()

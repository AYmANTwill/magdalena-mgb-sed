"""
Consolidate every DHIME precipitation download into one tidy structure:

    data/raw/observed/precip/dhime/regions/<department>/*.csv

Sources merged:
  1. your own department zips in dhime/*.zip        (each holds a descargaDhime.csv)
  2. Youssef's pre-extracted folders in dhime/"yOUSSEF DATASET"/**/<region>/*.csv

Department names are normalised (lower-case, no accents, quindio_corrected -> quindio) so
the two contributors' data land in the same folders. Nothing is deleted — this only copies
into regions/. After running it, src/build_precip_gauges.py reads regions/ and produces the
clean basin gauge dataset.

Run:  python src/organize_precip_regions.py
"""
import glob, os, re, shutil, unicodedata, zipfile, io, pathlib

BASE = pathlib.Path("data/raw/observed/precip/dhime")
REG = BASE / "regions"


def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    s = s.replace("corrected", "")            # quindio_corrected -> quindio
    return s


def dept_from_zip(fn):
    stem = os.path.basename(fn)
    stem = re.sub(r"_?20\d\d.*$", "", stem)   # strip _2008-2018-<n>
    return norm(stem)


def main():
    REG.mkdir(parents=True, exist_ok=True)
    counts = {}

    # 1. your zips -> regions/<dept>/<zipstem>.csv
    for z in sorted(glob.glob(str(BASE / "*.zip"))):
        dep = dept_from_zip(z)
        out = REG / dep
        out.mkdir(exist_ok=True)
        stem = os.path.splitext(os.path.basename(z))[0]
        with zipfile.ZipFile(z) as zf:
            for i, nm in enumerate([n for n in zf.namelist() if n.lower().endswith(".csv")]):
                tgt = out / f"{stem}{'' if i == 0 else '_'+str(i)}.csv"
                tgt.write_bytes(zf.read(nm))
        counts[dep] = counts.get(dep, 0) + 1

    # 2. Youssef's folders -> regions/<dept>/youssef_<n>.csv
    ydirs = glob.glob(str(BASE / "*[yY][oO][uU][sS][sS][eE][fF]*"))
    for yroot in ydirs:
        for csv in glob.glob(os.path.join(yroot, "**", "*.csv"), recursive=True):
            if "__MACOSX" in csv:
                continue
            dep = norm(os.path.basename(os.path.dirname(csv)))
            if not dep:
                continue
            out = REG / dep
            out.mkdir(exist_ok=True)
            n = len(glob.glob(str(out / "youssef_*.csv")))
            shutil.copyfile(csv, out / f"youssef_{n+1}.csv")
            counts[dep] = counts.get(dep, 0)

    print(f"organized into {REG}")
    for dep in sorted(os.listdir(REG)):
        d = REG / dep
        if d.is_dir():
            print(f"  {dep:20} {len(glob.glob(str(d/'*.csv')))} csv files")
    print(f"\n{len([d for d in os.listdir(REG) if (REG/d).is_dir()])} departments total")


if __name__ == "__main__":
    main()

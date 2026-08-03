"""Convert the wide forcing CSVs to verified .npy arrays.

WHY THIS EXISTS
---------------
`forcing_minibacia_{precip,pet}_v2.csv` are 4,018 rows x 8,673 columns, ~180 MB each.
`pd.read_csv(..., index_col=0, parse_dates=[0], dtype='float32')` **silently truncates**
them: on one run it returned 1,309 rows ending 2011-08-01, on another 3,630 rows ending
2017-12-08, from a file that is provably complete (4,019 lines, every line carrying exactly
8,672 commas, no NUL bytes, the row after the cut point intact). No exception, no warning,
and `len(pd.date_range(min, max)) == len(df)` still held, so the notebook's own
"calendar holes 0" check passed on the truncated frame.

That is the worst possible failure shape: a silent, non-deterministic, *plausible* subset.
Notebook 12's `assert DATES.equals(want)` is the only reason it was caught at all, and it
caught it two stages downstream of the actual damage.

So the CSVs are no longer parsed by anything downstream. They stay on disk as the
human-auditable artefact; the model path reads `.npy`, which is a raw buffer with a shape
header and therefore cannot be half-read without an error.

VERIFICATION, and why row-count alone is not enough
---------------------------------------------------
Chunked reading fixes the truncation, but "did I get every row" cannot be answered by the
parser that just lied about it. So the row count is checked against the **file's own line
count**, counted from the bytes, and the column count against the header's comma count.
Both are independent of pandas.

Run:  python src/forcing_npy.py [--version v2]
Writes, per field:  forcing_<field>_<version>.npy        (n_days, n_minibacia) float32
                    forcing_<field>_<version>_dates.npy  (n_days,) datetime64[D]
                    forcing_<field>_<version>_ids.npy    (n_minibacia,) int32
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
import pandas as pd

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"
CHUNK = 200          # rows per chunk; small enough that the C parser stays well inside memory


def line_and_field_count(path: pathlib.Path) -> tuple[int, int]:
    """Count data lines and header fields from the raw bytes - no CSV parser involved."""
    n_lines = 0
    header_commas = None
    with open(path, "rb") as fh:
        for raw in fh:
            if header_commas is None:
                header_commas = raw.count(b",")
            n_lines += 1
    return n_lines - 1, header_commas          # data rows, data columns


def convert(field: str, version: str) -> None:
    src = PROC / f"forcing_minibacia_{field}_{version}.csv"
    if not src.exists():
        print(f"  SKIP {src.name} (absent)")
        return
    n_rows_expected, n_cols_expected = line_and_field_count(src)

    dates: list = []
    blocks: list[np.ndarray] = []
    cols: list[str] | None = None
    for chunk in pd.read_csv(src, index_col=0, chunksize=CHUNK):
        if cols is None:
            cols = list(chunk.columns)
        elif list(chunk.columns) != cols:
            raise AssertionError(f"{src.name}: column set changed mid-file")
        dates.append(pd.to_datetime(chunk.index, format="%Y-%m-%d"))
        blocks.append(chunk.to_numpy(dtype="float32"))

    V = np.vstack(blocks)
    D = pd.DatetimeIndex(np.concatenate([d.to_numpy() for d in dates]))

    # --- the checks that matter, all against evidence outside the parser -------
    assert V.shape[0] == n_rows_expected, (
        f"{src.name}: parsed {V.shape[0]} rows but the file has {n_rows_expected} data lines "
        f"- the CSV reader truncated again")
    assert V.shape[1] == n_cols_expected, (
        f"{src.name}: parsed {V.shape[1]} columns, header declares {n_cols_expected}")
    assert not D.duplicated().any(), f"{src.name}: duplicated dates"
    assert D.is_monotonic_increasing, f"{src.name}: dates not sorted"
    full = pd.date_range(D.min(), D.max(), freq="D")
    assert len(full) == len(D), f"{src.name}: {len(full) - len(D)} calendar holes"
    n_nan = int(np.isnan(V).sum())
    assert n_nan == 0, f"{src.name}: {n_nan:,} NaN cells"

    ids = np.array([int(c) for c in cols], dtype=np.int32)
    stem = PROC / f"forcing_{field}_{version}"
    np.save(f"{stem}.npy", V)
    np.save(f"{stem}_dates.npy", D.to_numpy().astype("datetime64[D]"))
    np.save(f"{stem}_ids.npy", ids)
    print(f"  {src.name}")
    print(f"    {V.shape[0]} days x {V.shape[1]} minibacias  "
          f"{D.min().date()} .. {D.max().date()}")
    print(f"    mean {V.mean():.3f} mm/day ({V.mean()*365.25:.0f} mm/yr unweighted)  "
          f"NaN {n_nan}  -> {stem.name}.npy")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v2")
    a = ap.parse_args()
    print(f"converting forcing CSVs -> .npy (version {a.version})")
    for field in ("precip", "pet"):
        convert(field, a.version)


if __name__ == "__main__":
    main()

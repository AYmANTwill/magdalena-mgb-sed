"""
Defect B (docs/46 §1.1) — DECOMPOSE the published ×0.790 into its `L` form, its `S` swap and
its column choice, and measure the corrected lower endpoint of the LS bracket.

WHAT THE DEFECT IS
------------------
`journal_c31-ls2d` §S4 published ×0.790 as "the literal Desmet–Govers finite-difference `L`".
It is `ls2d.py`'s `ls3 / ls1`, i.e.

    0.790 = mean( L_dg  · S_McCool87 )  /  mean( L_cont · S_MooreBurch86 )     [UNCAPPED column]

which is TWO levers (an `L` form and an `S` function) measured on the UNCAPPED `ls2d` column,
while the engine reads `ls2d_hs` (`src/mgb_sediment.py`, `ls2d_column="ls2d_hs"`).
`ls2d_variants.py` already isolated the `L` form on the hs column (V5/V0 = 0.7698) but the
MIXED cells needed to split 0.790 itself do not exist on disk:

  * `ls2d.py`'s `ls2` (reported as `D_ls2d_mb86`) is NOT `L_dg · S_MB86` — it is the fixed
    m = 0.4 Moore & Burch cross-check on the CONTINUOUS L (`scripts/c3/ls2d.py:281`). Using it
    as the intermediate gives a fabricated decomposition.

So this harness measures the four mixed columns, on both bases, plus the source-formulation
rows with and without the D&G `L`, so every ratio quoted in `docs/50` is a measurement.

IT IS NOT A SECOND IMPLEMENTATION OF LS
---------------------------------------
`scripts/c3/ls2d.py` is imported. V0 is `ls2d.ls_variants()[3]`; `U_Lc_Smb` and `U_Ldg_Smc` are
its `ls1` and `ls3`, i.e. the published denominator and numerator themselves. The DEM, slope,
pit filling, D8, flow accumulation, cell geometry and the area-weighted accumulation are all
`ls2d.py`'s. Only the mixed expressions are new code.

THREE REPRODUCTION GATES, all of which run before anything is reported
----------------------------------------------------------------------
  G-A  V0 basin area-weighted mean          = 39.812260149274394  (abs 1e-6)
  G-B  mean(U_Ldg_Smc)/mean(U_Lc_Smb)       = 0.7900              (abs 5e-4) — the PUBLISHED ratio
  G-C  mean(H_Ldg_Smb)/mean(V0)             = 0.7698333815060305  (abs 1e-6) — V5 of ls2d_variants

AGGREGATION: area-weighted mean, weights = true cell area (docs/46 §3.2). No median is
computed — it is not an admissible aggregate for a linear factor and nothing here needs it.

WRITES: data/processed/ls2d_defect_b.json only. The committed products
`urh_ls2d.csv` / `minibacia_ls2d.csv` are SHA-256'd before and after and the script raises if
either moves. No `--scale` option exists, deliberately
(`docs/agents/journal_decide-ls-resolution.md` §2).

Usage: python3.10 scripts/c3/ls2d_defect_b.py [--chunk 512]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from rasterio.enums import Resampling as RS

import pyflwdir
from pyflwdir import gis_utils

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ls2d as L  # noqa: E402

# ------------------------------------------------------------------------------- registry
COLS = [
    # --- uncapped basis (the column the published 0.790 was measured on) ---
    "U_Lc_Smb",      # = ls2d.py ls1 : L continuous x S Moore&Burch 86   (published denominator)
    "U_Ldg_Smc",     # = ls2d.py ls3 : L D&G96 fd   x S McCool 87        (published numerator)
    "U_Ldg_Smb",     # mixed: L D&G96 fd x S Moore&Burch 86   -> L form alone, uncapped
    "U_Lc_Smc",      # mixed: L continuous x S McCool 87      -> S swap alone, uncapped
    # --- hs basis (1 km2 cap) = the column the engine actually reads ---
    "H_Lc_Smb",      # = ls2d.py ls4 = V0 = urh_ls2d.csv:ls2d_hs
    "H_Ldg_Smb",     # = V5 of ls2d_variants.py : L form alone, hs basis
    "H_Ldg_Smc",     # the PUBLISHED RECIPE transplanted to the engine's column
    "H_Lc_Smc",      # S swap alone, hs basis
    # --- source formulation (one-pixel slope length + eq.14 step m + W&S78 S) ---
    "V4",            # source as read, continuous (point-rate) L      -> published x0.421
    "V4_dg",         # source as read, D&G finite-difference L        -> corrected endpoint
    "V4_dg_x1",      # same, aspect factor x = 1 (diagnostic on the x convention)
    "V4p",           # cap version of V4  (min(m,0.5))
    "V4p_dg",        # cap version of V4_dg
]

GATE_V0 = 39.812260149274394          # ls2d_variants_summary.json, V0_ours_2026_08
GATE_PUB = 0.7900                     # journal_c31-ls2d §S4, the published L ratio
GATE_V5 = 0.7698333815060305          # ls2d_variants_summary.json, V5_L_dg96_fd ratio_to_V0
ANDEAN_M, LOWLAND_M = 1000.0, 200.0


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def m_step_eq14(tan_theta: np.ndarray) -> np.ndarray:
    """Buarque (2015) eq. 14, Sf = slope percent (docs/46 (R6): units NOT verified)."""
    sf = tan_theta * 100.0
    return np.where(sf < 1.0, 0.2, np.where(sf < 3.0, 0.3, np.where(sf < 5.0, 0.4, 0.5)))


def s_ws78(sin_theta: np.ndarray) -> np.ndarray:
    return 65.41 * sin_theta ** 2 + 4.56 * sin_theta + 0.065


def block(tan_theta, upslope_area_m2, cell_area_m2, x_aspect) -> dict:
    ls1, _ls2, ls3, ls4 = L.ls_variants(tan_theta, upslope_area_m2, cell_area_m2, x_aspect)

    tan = np.maximum(tan_theta, L.TAN_FLOOR)
    sin = tan / np.sqrt(1.0 + tan * tan)
    d = np.sqrt(cell_area_m2)

    m = L.slope_exponent_m(sin)
    m_cap = np.minimum(m, 0.5)
    m_step = m_step_eq14(tan)
    mp1 = m + 1.0

    s_mb = (sin / L.UNIT_PLOT_SIN) ** L.N_EXP          # Moore & Burch 1986 (ours)
    s_mc = L.s_factor_mccool(sin, tan)                 # McCool 1987 (what ls3 uses)
    s_ws = s_ws78(sin)                                 # Wischmeier & Smith 1978 (Buarque eq.18)

    # --- L forms -------------------------------------------------------------------------
    a_in_unc = np.maximum(upslope_area_m2 - cell_area_m2, 0.0)
    a_unit_unc = (a_in_unc + cell_area_m2) / d
    l_cont_unc = mp1 * (a_unit_unc / L.UNIT_PLOT_LEN_M) ** m
    l_dg_unc = ((a_in_unc + cell_area_m2) ** mp1 - a_in_unc ** mp1) / (
        d ** (m + 2.0) * x_aspect ** m * L.UNIT_PLOT_LEN_M ** m)

    a_unit_hs = np.minimum(upslope_area_m2, L.A_CHANNEL_M2) / d
    l_cont_hs = mp1 * (a_unit_hs / L.UNIT_PLOT_LEN_M) ** m
    a_in_hs = np.maximum(np.minimum(upslope_area_m2, L.A_CHANNEL_M2) - cell_area_m2, 0.0)
    l_dg_hs = ((a_in_hs + cell_area_m2) ** mp1 - a_in_hs ** mp1) / (
        d ** (m + 2.0) * x_aspect ** m * L.UNIT_PLOT_LEN_M ** m)

    # --- source formulation: slope length limited to ONE PIXEL => a_in = 0 ----------------
    # continuous (point-rate) L with a_unit = D ;  D&G L degenerates to (D/(22.13 x))^m
    def l_cont_px(mm):
        return (mm + 1.0) * (d / L.UNIT_PLOT_LEN_M) ** mm

    def l_dg_px(mm, xa):
        return (d / (L.UNIT_PLOT_LEN_M * xa)) ** mm

    return {
        "U_Lc_Smb": ls1,
        "U_Ldg_Smc": ls3,
        "U_Ldg_Smb": l_dg_unc * s_mb,
        "U_Lc_Smc": l_cont_unc * s_mc,
        "H_Lc_Smb": ls4,
        "H_Ldg_Smb": l_dg_hs * s_mb,
        "H_Ldg_Smc": l_dg_hs * s_mc,
        "H_Lc_Smc": l_cont_hs * s_mc,
        "V4": l_cont_px(m_step) * s_ws,
        "V4_dg": l_dg_px(m_step, x_aspect) * s_ws,
        "V4_dg_x1": l_dg_px(m_step, 1.0) * s_ws,
        "V4p": l_cont_px(m_cap) * s_ws,
        "V4p_dg": l_dg_px(m_cap, x_aspect) * s_ws,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Defect B decomposition harness. Native 90 m.")
    ap.add_argument("--chunk", type=int, default=512)
    args = ap.parse_args()

    repo = L.repo_root()
    proc = repo / "data" / "processed"
    protected = [proc / "urh_ls2d.csv", proc / "minibacia_ls2d.csv"]
    before = {p.name: sha256(p) for p in protected}
    for k, v in before.items():
        L.log(f"SHA-256 before  {k}  {v}")

    with rasterio.open(proc / "minibacias.tif") as ds:
        subs = ds.read(1)
    Hc, Wc = subs.shape

    with rasterio.open(L.locate_dem(repo)) as ds:
        H, W = ds.height, ds.width
        elev = ds.read(1, out_shape=(H, W), resampling=RS.average).astype("float32")
        transform = ds.transform * Affine.scale(ds.width / W, ds.height / H)
    ratio = L.MINIBACIA_SCALE
    if H != Hc * ratio or W != Wc * ratio:
        raise SystemExit(f"grid mismatch: DEM {H}x{W} vs minibacia {Hc}x{Wc} x {ratio}")
    ND = np.float32(-9999.0)
    elev[~np.isfinite(elev)] = ND
    elev[elev < -50] = ND
    L.log(f"DEM {H}x{W} ({elev.size/1e6:.1f} M cells)")

    with np.errstate(invalid="ignore"):
        tmp = np.where(elev > ND, elev, np.float32(np.nan))
        elev_c = np.nanmean(tmp.reshape(Hc, ratio, Wc, ratio), axis=(1, 3)).astype("float32")
    del tmp

    L.log("slope (Horn 3x3) ...")
    tan_slope = pyflwdir.dem.slope(elev, nodata=float(ND), latlon=True, transform=transform)
    L.log("pyflwdir.from_dem (pit filling + D8) ...")
    elev_nan = np.where(elev > ND, elev, np.float32(np.nan))
    del elev
    flw = pyflwdir.from_dem(data=elev_nan, nodata=np.nan, transform=transform, latlon=True)
    del elev_nan
    d8 = flw.to_array(ftype="d8").astype("uint8")
    L.log("upstream_area ...")
    upa = flw.upstream_area(unit="m2").astype("float32")
    del flw

    xres, yres, north = transform[0], transform[4], transform[5]
    lat_row = north + (np.arange(H) + 0.5) * yres
    dx_m = np.array([abs(xres) * gis_utils.degree_metres_x(la) for la in lat_row], "float64")
    dy_m = np.array([abs(yres) * gis_utils.degree_metres_y(la) for la in lat_row], "float64")
    cell_area_row = dx_m * dy_m

    strata = ["basin", "lowland_lt200m", "mid_200_1000m", "andean_gt1000m"]
    str_w = {s: 0.0 for s in strata}
    str_sum = {s: {c: 0.0 for c in COLS} for s in strata}
    n_nonfinite = {c: 0 for c in COLS}
    n_cells = 0

    L.log(f"per-cell pass, {args.chunk}-row chunks ...")
    t0 = time.time()
    for r0 in range(0, H, args.chunk):
        r1 = min(H, r0 + args.chunk)
        mini_blk = subs[r0 // ratio:(r1 + ratio - 1) // ratio]
        rr = np.arange(r0, r1) // ratio - (r0 // ratio)
        cc = np.arange(W) // ratio
        mini_chunk = mini_blk[np.ix_(rr, cc)]
        elevc_chunk = elev_c[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]

        sl = tan_slope[r0:r1]
        ua = upa[r0:r1]
        v = (mini_chunk > 0) & (sl > float(ND) + 1.0) & np.isfinite(sl) & (ua > 0)
        if not v.any():
            continue

        area_col = np.repeat(cell_area_row[r0:r1][:, None], W, axis=1)
        xasp = np.where(np.isin(d8[r0:r1], L.D8_DIAGONAL), np.sqrt(2.0), 1.0)

        w = area_col[v]
        out = block(sl[v].astype("float64"), ua[v].astype("float64"), w, xasp[v])
        n_cells += int(w.size)

        ec = elevc_chunk[v]
        masks = {"basin": slice(None), "lowland_lt200m": ec < LOWLAND_M,
                 "mid_200_1000m": (ec >= LOWLAND_M) & (ec <= ANDEAN_M),
                 "andean_gt1000m": ec > ANDEAN_M}
        for s in strata:
            str_w[s] += float(np.sum(w[masks[s]]))
        for c in COLS:
            a = out[c]
            bad = ~np.isfinite(a)
            if bad.any():
                n_nonfinite[c] += int(bad.sum())
                a = np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0)
            for s in strata:
                str_sum[s][c] += float(np.sum(a[masks[s]] * w[masks[s]]))
    L.log(f"per-cell pass done: {n_cells:,} cells in {time.time()-t0:.0f} s")

    lev = {c: {s: str_sum[s][c] / str_w[s] for s in strata} for c in COLS}
    v0 = lev["H_Lc_Smb"]["basin"]
    r_pub = lev["U_Ldg_Smc"]["basin"] / lev["U_Lc_Smb"]["basin"]
    r_v5 = lev["H_Ldg_Smb"]["basin"] / v0

    gates = {
        "G-A_V0_mean": {"target": GATE_V0, "got": v0, "tol": 1e-6,
                        "pass": abs(v0 - GATE_V0) <= 1e-6},
        "G-B_published_0790": {"target": GATE_PUB, "got": r_pub, "tol": 5e-4,
                               "pass": abs(r_pub - GATE_PUB) <= 5e-4},
        "G-C_V5_over_V0": {"target": GATE_V5, "got": r_v5, "tol": 1e-6,
                           "pass": abs(r_v5 - GATE_V5) <= 1e-6},
    }
    print("\n" + "=" * 88)
    print("REPRODUCTION GATES")
    for k, g in gates.items():
        print(f"  {k:<22} target {g['target']!r}\n{'':<24} got    {g['got']!r}"
              f"\n{'':<24} {'PASS' if g['pass'] else 'FAIL'}  (tol {g['tol']})")
    print("=" * 88)
    if not all(g["pass"] for g in gates.values()):
        print("STOP: a known number did not reproduce; no decomposition is reported.")
        after = {p.name: sha256(p) for p in protected}
        print(f"protected files unchanged: {after == before}")
        return 2

    print(f"\n{'column':<12}{'basin':>14}{'<200 m':>12}{'200-1000':>12}{'>1000 m':>12}"
          f"{'x V0':>10}")
    for c in COLS:
        print(f"{c:<12}{lev[c]['basin']:>14.5f}{lev[c]['lowland_lt200m']:>12.5f}"
              f"{lev[c]['mid_200_1000m']:>12.5f}{lev[c]['andean_gt1000m']:>12.5f}"
              f"{lev[c]['basin']/v0:>10.5f}")

    def rr(a, b, s="basin"):
        return lev[a][s] / lev[b][s]

    dec = {
        # (a) the isolated L form, hs basis
        "L_form_hs_V5_over_V0": rr("H_Ldg_Smb", "H_Lc_Smb"),
        "L_form_unc": rr("U_Ldg_Smb", "U_Lc_Smb"),
        # (b) the S swap, both bases and both compositions
        "S_swap_unc_on_Ldg": rr("U_Ldg_Smc", "U_Ldg_Smb"),
        "S_swap_unc_on_Lcont": rr("U_Lc_Smc", "U_Lc_Smb"),
        "S_swap_hs_on_Ldg": rr("H_Ldg_Smc", "H_Ldg_Smb"),
        "S_swap_hs_on_Lcont": rr("H_Lc_Smc", "H_Lc_Smb"),
        "L_form_unc_on_Smc": rr("U_Ldg_Smc", "U_Lc_Smc"),
        "L_form_hs_on_Smc": rr("H_Ldg_Smc", "H_Lc_Smc"),
        # published ratio and the same recipe on the engine's column
        "published_R_unc": r_pub,
        "same_recipe_R_hs": rr("H_Ldg_Smc", "H_Lc_Smb"),
        # (c) column choice
        "column_factor_full_recipe": rr("H_Ldg_Smc", "H_Lc_Smb") / r_pub,
        "column_factor_L_form_only": rr("H_Ldg_Smb", "H_Lc_Smb") / rr("U_Ldg_Smb", "U_Lc_Smb"),
        # (d) the bracket
        "V4_over_V0": rr("V4", "H_Lc_Smb"),
        "V4dg_over_V0": rr("V4_dg", "H_Lc_Smb"),
        "V4dg_x1_over_V0": rr("V4_dg_x1", "H_Lc_Smb"),
        "V4p_over_V0": rr("V4p", "H_Lc_Smb"),
        "V4pdg_over_V0": rr("V4p_dg", "H_Lc_Smb"),
        "L_form_inside_source": rr("V4_dg", "V4"),
        "L_form_inside_source_cap": rr("V4p_dg", "V4p"),
        "naive_0421_times_0790": rr("V4", "H_Lc_Smb") * r_pub,
        "naive_0421_times_V5ratio": rr("V4", "H_Lc_Smb") * r_v5,
    }
    print("\nDECOMPOSITION (all basin area-weighted; ratios of means, so path-dependent)")
    for k, x in dec.items():
        print(f"  {k:<30}{x:>14.6f}   ln {np.log(x):+.5f}")

    summary = {"n_cells": n_cells, "strata_area_km2": {s: str_w[s] / 1e6 for s in strata},
               "gates": gates, "levels": lev, "n_nonfinite": n_nonfinite,
               "decomposition": dec,
               "ln_decomposition": {k: float(np.log(x)) for k, x in dec.items()}}
    out = proc / "ls2d_defect_b.json"
    out.write_text(json.dumps(summary, indent=1))
    L.log(f"wrote {out}")

    after = {p.name: sha256(p) for p in protected}
    print("\nPROTECTED COMMITTED PRODUCTS")
    for p in protected:
        same = before[p.name] == after[p.name]
        print(f"  {p.name:<24} {'UNCHANGED' if same else '*** CHANGED ***'}  {after[p.name]}")
    if after != before:
        raise SystemExit("a committed LS product changed — this must never happen")
    return 0


if __name__ == "__main__":
    sys.exit(main())

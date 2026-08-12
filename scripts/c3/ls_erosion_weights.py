"""
C3.1 / docs 46 §3.3 — turn the LS variant PROXY into the EXACT erosion-weighted factor, and
measure where in the slope distribution the levers act.  Measures; changes nothing.

WHY THIS EXISTS
---------------
`scripts/c3/ls2d_variants.py` measures every LS variant's basin **area-weighted** level,
`f_area`.  `docs/46` §3.3 says plainly that `f_area` is only the proxy and that **`f_ero`
decides**, and `docs/47` §3.1 R7 measures the proxy 2.51 % low.  This script computes `f_ero`
for all eight variants, and it answers the question `docs/37` line 206 and `docs/49` ask of
Defect A: **a lever that only acts on low-slope cells matters in proportion to the EROSION
those cells carry, not the area they cover.**

IT DOES NOT RE-IMPLEMENT ANYTHING
---------------------------------
* the erosion field is `src/mgb_sediment.simulate_sediment` at **adopted defaults**
  (`SedParams()` = williams_m3 / us_customary / cited_central C / α 11.8 / β 0.56 / FG 1.0),
  on the frozen H2E drivers, opened **read-only**;
* the LS variants are read from `data/processed/urh_ls2d_variants.csv` as written by
  `ls2d_variants.py`;
* the per-cell slope pass reuses `scripts/c3/ls2d.py`'s own DEM, slope, pit filling, D8,
  flow accumulation, URH grid and cell geometry by **import**.

THE TWO GATES (both run before any new number is reported)
----------------------------------------------------------
1. basin gross erosion at adopted defaults must reproduce **299.5387 Mt/yr** (`docs/37` A1.3)
   to 1e-3;
2. the erosion-weighted factors must reproduce the four already-published `f_ero` values of
   `docs/47` §4.3 (V1 0.3624 · V2a 0.5175 · V3 1.6941 · V4 0.43194) to 5e-4.
A harness that cannot reproduce known numbers is not trusted with unknown ones.

WHY THE PER-CELL SPLIT IS EXACT AND NOT AN APPROXIMATION
--------------------------------------------------------
MUSLE is linear in LS per cell and the adopted aggregation is the area-weighted mean, so a
(minibacia, URH) unit's decade erosion `E_u` distributes over its 90 m cells exactly in
proportion to `LS_j · w_j` (LS times true cell area).  The erosion carried by any subset S of
the basin's cells is therefore

    E(S) = Σ_u E_u · [ Σ_{j∈S∩u} LS_j w_j ] / [ Σ_{j∈u} LS_j w_j ]

with no modelling assumption beyond the linearity the engine already asserts
(`src/mgb_sediment.cell_static_factor`).  The daily runoff-energy term is identical for every
cell of a minibacia (`mini_static_factor`'s docstring), so it factors out of the ratio.

OUTPUTS (new files; nothing existing is touched)
------------------------------------------------
  data/processed/urh_erosion_weights.csv   (mini, urh, eroded_t) decade gross erosion per unit
  data/processed/ls_defect_a.json          f_ero for every variant + the slope-class table

Usage:  python3.10 scripts/c3/ls_erosion_weights.py [--chunk 512] [--skip-cells]
        Native 90 m only.  No --scale: `ls2d.py --scale != 1` inside the repository tree
        overwrites the committed products (journal_decide-ls-resolution §2).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.enums import Resampling as RS

import pyflwdir
from pyflwdir import gis_utils

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ls2d as L  # noqa: E402

REPO = L.repo_root()
sys.path.insert(0, str(REPO / "src"))
import mgb_sediment as sed  # noqa: E402

PROC = REPO / "data" / "processed"
FROZEN = PROC / "sim_calibrated_v2"

PUBLISHED_TOTAL_MT_YR = 299.5387          # docs/37 A1.3
TOTAL_TOL = 1e-3
PUBLISHED_F_ERO = {                        # docs/47 §4.3 / journal_ls-impact step 2
    "V1_lim_pixel": 0.3624,
    "V2a_m_cap05": 0.5175,
    "V3_s_ws78": 1.6941,
    "V4_buarque_2015": 0.43194,
}
F_ERO_TOL = 5e-4

# eq. 14's own class boundaries, in slope PERCENT (Sf = 100 tanθ), plus the crossover class
# where min(m_cont, 0.5) and the step function coincide.  The crossover is the root of
# m_cont(sinθ) = 0.5, i.e. (sinθ/0.0896) = 3 sinθ^0.8 + 0.56, solved by brentq to 1e-15:
# tanθ = 0.08933250413265519 (8.9333 %).  Above it the cap and the step are the same object;
# below it they differ on every cell.
M_CROSSOVER_TAN = 0.08933250413265519
CLASS_EDGES_PCT = [0.0, 1.0, 3.0, 5.0, 100.0 * M_CROSSOVER_TAN, np.inf]
CLASS_NAMES = ["lt1pct", "1to3pct", "3to5pct", "5pct_to_crossover", "ge_crossover"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


# ---------------------------------------------------------------------------- stage 1
def erosion_weights() -> pd.DataFrame:
    """Decade gross hillslope erosion per (minibacia, URH) unit, at adopted defaults."""
    t0 = time.time()
    drv = sed.load_drivers(FROZEN / "h2e_drivers.npz")
    # V0 pin: the erosion WEIGHTS behind f_LS = 0.25146 are defined on the baseline (ls2d_hs /
    # V0) erosion field.  ACT 2 (2026-08-12) moved the engine default to V4_dg; this harness
    # must keep computing weights on V0 or the f_LS it derives becomes self-referential.
    geom = sed.load_geometry(PROC, mini_ids=drv.mini_ids,
                             urh_ls2d="urh_ls2d.csv", ls2d_column="ls2d_hs")
    ndays = drv.qsur_mm.shape[0]
    years = ndays / 365.25
    L.log(f"drivers {drv.qsur_mm.shape} ({drv.dates[0]}..{drv.dates[-1]}, {years:.4f} yr) "
          f"| geometry {geom.n_cells} cells | {time.time()-t0:.1f} s")

    p0 = sed.SedParams()
    run = sed.simulate_sediment(geom, p0, drv.qsur_mm, dates=drv.dates, store_daily=False)
    ero = np.asarray(run.cell_eroded_t, dtype="float64")
    total = float(ero.sum()) / 1e6 / years
    ok = abs(total - PUBLISHED_TOTAL_MT_YR) <= TOTAL_TOL
    print("\n" + "=" * 78)
    print("GATE 1 — basin gross erosion at adopted defaults (docs/37 A1.3: 299.5387 Mt/yr)")
    print(f"  measured : {total!r} Mt/yr")
    print(f"  diff     : {total - PUBLISHED_TOTAL_MT_YR:+.3e}")
    print(f"  GATE     : {'PASS' if ok else 'FAIL'}")
    print("=" * 78 + "\n", flush=True)
    if not ok:
        raise SystemExit("GATE 1 FAILED — no number from this run may be used")

    df = pd.DataFrame({
        "mini": geom.mini_ids[geom.cell_mini].astype("int64"),
        "urh": geom.cell_urh_code.astype("int64"),
        "area_km2_urhfrac": geom.cell_area_km2,
        "ls2d_hs": geom.cell_ls2d,
        "eroded_t": ero,
    })
    df.attrs["total_mt_yr"] = total
    df.attrs["years"] = years
    return df


# ---------------------------------------------------------------------------- stage 2
def f_ero_table(wts: pd.DataFrame) -> dict:
    """f_ero(V) = Σ_u E_u (LS_V/LS_V0)_u / Σ_u E_u, for every variant column."""
    var = pd.read_csv(PROC / "urh_ls2d_variants.csv")
    j = wts.merge(var, on=["mini", "urh"], how="left", validate="one_to_one")
    vcols = [c for c in var.columns if c.startswith("V")]
    if j[vcols].isna().any().any():
        raise SystemExit("a geometry unit has no row in urh_ls2d_variants.csv — stop")
    e = j.eroded_t.to_numpy()
    a = j.area_km2_urhfrac.to_numpy()
    v0 = j["V0_ours_2026_08"].to_numpy()
    out = {}
    for c in vcols:
        r = j[c].to_numpy() / v0
        out[c] = {
            "f_ero": float(np.sum(e * r) / e.sum()),
            "f_area_urhfrac_areas": float(np.sum(a * j[c].to_numpy()) / np.sum(a * v0)),
        }
    print("=" * 92)
    print("GATE 2 — erosion-weighted factors vs docs/47 §4.3")
    # The area column is NOT docs/46 §3.3's `f_area`, and the header says so.  It is computed on
    # `geom.cell_area_km2` — load_geometry's ENGINE URH-fraction areas, basin total 257,096.93 km²
    # — whereas §3.3's `f_area` is the per-cell basin mean over 30,235,916 DEM cells at 90 m
    # (256,702.36 km²).  For V4 the two are 0.4214751420286394 (this column) vs
    # 0.42136300143291305 (§3.3).  An untagged `f_area` header here is how the former propagated
    # through the corpus as the latter; see docs/46 §10 amd 2 / docs/51 §9 amd 1 / docs/43 amd 8.
    print("  area column support: ENGINE urh_fractions×minibacias areas (257,096.93 km²), NOT")
    print("  docs/46 §3.3's per-cell basin f_area (30,235,916 cells, 256,702.36 km²).")
    print(f"{'variant':<24}{'f_ero':>12}{'published':>12}{'f_area_urhfrac':>16}{'gate':>8}")
    all_ok = True
    for c in vcols:
        pub = PUBLISHED_F_ERO.get(c)
        g = "" if pub is None else ("PASS" if abs(out[c]["f_ero"] - pub) <= F_ERO_TOL else "FAIL")
        all_ok &= (g != "FAIL")
        print(f"{c:<24}{out[c]['f_ero']:>12.5f}{(pub if pub else float('nan')):>12.5f}"
              f"{out[c]['f_area_urhfrac_areas']:>16.5f}{g:>8}")
    print("=" * 92 + "\n", flush=True)
    if not all_ok:
        raise SystemExit("GATE 2 FAILED — no number from this run may be used")
    return out


# ---------------------------------------------------------------------------- stage 3
def slope_class_pass(chunk: int) -> dict:
    """Per-cell pass: area and Σ LS·w per (mini, URH) per eq.-14 slope class."""
    scratch = Path(os.environ.get("LS2D_CACHE", Path(tempfile.gettempdir()) / "ls2d_cache"))
    scratch.mkdir(parents=True, exist_ok=True)

    with rasterio.open(PROC / "minibacias.tif") as ds:
        subs = ds.read(1)
        dst_tr = ds.transform
    Hc, Wc = subs.shape
    mini_ids = np.unique(subs[subs > 0])
    n_mini = mini_ids.size
    urh_coarse = L.build_urh_coarse(REPO, subs, dst_tr, scratch / "urh_coarse.npz")

    with rasterio.open(L.locate_dem(REPO)) as ds:
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

    id_to_idx = np.full(int(mini_ids.max()) + 1, -1, "int32")
    id_to_idx[mini_ids] = np.arange(n_mini, dtype="int32")
    urh_to_idx = np.full(int(L.URH_CODES.max()) + 1, -1, "int32")
    urh_to_idx[L.URH_CODES] = np.arange(L.URH_CODES.size, dtype="int32")
    nkey = n_mini * 25
    nclass = len(CLASS_NAMES)
    acc_area = np.zeros((nclass, nkey), "float64")     # true cell area per class
    acc_lsw = np.zeros((nclass, nkey), "float64")      # Σ LS_V0 · w  per class
    acc_v2a = np.zeros((nclass, nkey), "float64")      # Σ LS_V2a · w
    acc_v2b = np.zeros((nclass, nkey), "float64")      # Σ LS_V2b · w
    acc_n = np.zeros((nclass, nkey), "int64")
    # docs/46 (R6): eq. 14's `Sf` units are NOT verified against Buarque pp. 46-48.  The
    # registered record reads them as slope PERCENT; the two other admissible readings are
    # degrees and m/m.  Both are accumulated here as UNVERIFIED SENSITIVITIES so the size of
    # the open question is measured rather than asserted.  Basin-level only (no class split).
    acc_r6 = {"deg": np.zeros(nkey, "float64"), "mm": np.zeros(nkey, "float64")}

    L.log(f"per-cell slope-class pass, {chunk}-row chunks ...")
    t0 = time.time()
    filled = 0
    for r0 in range(0, H, chunk):
        r1 = min(H, r0 + chunk)
        mini_blk = subs[r0 // ratio:(r1 + ratio - 1) // ratio]
        rr = np.arange(r0, r1) // ratio - (r0 // ratio)
        cc = np.arange(W) // ratio
        mini_chunk = mini_blk[np.ix_(rr, cc)]
        urh_chunk = urh_coarse[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]

        sl = tan_slope[r0:r1]
        ua = upa[r0:r1]
        v = (mini_chunk > 0) & (sl > float(ND) + 1.0) & np.isfinite(sl) & (ua > 0)
        if not v.any():
            continue
        area_col = np.repeat(cell_area_row[r0:r1][:, None], W, axis=1)
        xasp = np.where(np.isin(d8[r0:r1], L.D8_DIAGONAL), np.sqrt(2.0), 1.0)

        w = area_col[v]
        tan_v = np.maximum(sl[v].astype("float64"), L.TAN_FLOOR)
        ua_v = ua[v].astype("float64")
        _, _, _, ls_v0 = L.ls_variants(sl[v].astype("float64"), ua_v, w, xasp[v])

        d = np.sqrt(w)
        sin = tan_v / np.sqrt(1.0 + tan_v * tan_v)
        m_cont = L.slope_exponent_m(sin)
        m_cap = np.minimum(m_cont, 0.5)
        sf = tan_v * 100.0
        m_step = np.where(sf < 1.0, 0.2, np.where(sf < 3.0, 0.3, np.where(sf < 5.0, 0.4, 0.5)))
        s_ours = (sin / L.UNIT_PLOT_SIN) ** L.N_EXP
        a_hs = np.minimum(ua_v, L.A_CHANNEL_M2) / d
        ls_v2a = (m_cap + 1.0) * (a_hs / L.UNIT_PLOT_LEN_M) ** m_cap * s_ours
        ls_v2b = (m_step + 1.0) * (a_hs / L.UNIT_PLOT_LEN_M) ** m_step * s_ours

        mi = id_to_idx[mini_chunk[v]]
        ui = urh_to_idx[np.clip(urh_chunk[v], 0, urh_to_idx.size - 1)]
        ui = np.where(urh_chunk[v] > 0, ui, -1)
        key = mi.astype("int64") * 25 + (ui + 1)

        for tag, sfx in (("deg", np.degrees(np.arctan(tan_v))), ("mm", tan_v)):
            ms_x = np.where(sfx < 1.0, 0.2,
                            np.where(sfx < 3.0, 0.3, np.where(sfx < 5.0, 0.4, 0.5)))
            ls_x = (ms_x + 1.0) * (a_hs / L.UNIT_PLOT_LEN_M) ** ms_x * s_ours
            acc_r6[tag] += np.bincount(key, weights=ls_x * w, minlength=nkey)

        cls = np.digitize(sf, CLASS_EDGES_PCT[1:-1], right=False)  # 0..nclass-1
        for ci in range(nclass):
            sel = cls == ci
            if not sel.any():
                continue
            k = key[sel]
            ww = w[sel]
            acc_area[ci] += np.bincount(k, weights=ww, minlength=nkey)
            acc_n[ci] += np.bincount(k, minlength=nkey)
            acc_lsw[ci] += np.bincount(k, weights=ls_v0[sel] * ww, minlength=nkey)
            acc_v2a[ci] += np.bincount(k, weights=ls_v2a[sel] * ww, minlength=nkey)
            acc_v2b[ci] += np.bincount(k, weights=ls_v2b[sel] * ww, minlength=nkey)
        filled += int(v.sum())

    L.log(f"slope-class pass done: {filled:,} cells in {time.time()-t0:.0f} s")
    return {"mini_ids": mini_ids, "acc_area": acc_area, "acc_lsw": acc_lsw,
            "acc_v2a": acc_v2a, "acc_v2b": acc_v2b, "acc_n": acc_n, "n_cells": filled,
            "acc_r6": acc_r6}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", type=int, default=512)
    ap.add_argument("--skip-cells", action="store_true")
    args = ap.parse_args()

    protected = [PROC / "urh_ls2d.csv", PROC / "minibacia_ls2d.csv",
                 FROZEN / "h2e_drivers.npz", FROZEN / "parameters_H2E.csv"]
    before = {p.name: sha256(p) for p in protected if p.is_file()}

    wts = erosion_weights()
    out = {"gate_total_mt_yr": wts.attrs["total_mt_yr"], "years": wts.attrs["years"],
           "n_units": int(len(wts))}
    wts[["mini", "urh", "area_km2_urhfrac", "ls2d_hs", "eroded_t"]].to_csv(
        PROC / "urh_erosion_weights.csv", index=False, float_format="%.10g")
    L.log(f"wrote {PROC / 'urh_erosion_weights.csv'} ({len(wts)} rows)")

    out["variants"] = f_ero_table(wts)

    if not args.skip_cells:
        cp = slope_class_pass(args.chunk)
        # map (mini, urh) -> key
        n_mini = cp["mini_ids"].size
        id_to_idx = np.full(int(cp["mini_ids"].max()) + 1, -1, "int64")
        id_to_idx[cp["mini_ids"]] = np.arange(n_mini)
        urh_slot = np.full(int(L.URH_CODES.max()) + 1, -1, "int64")
        urh_slot[L.URH_CODES] = np.arange(L.URH_CODES.size)
        key = id_to_idx[wts.mini.to_numpy()] * 25 + (urh_slot[wts.urh.to_numpy()] + 1)
        if (key < 0).any():
            raise SystemExit("a geometry unit has no cell key — stop")

        e = wts.eroded_t.to_numpy()
        lsw = cp["acc_lsw"][:, key]                      # (nclass, n_units)
        area = cp["acc_area"][:, key]
        ncell = cp["acc_n"][:, key]
        denom = lsw.sum(0)
        if (denom <= 0).any():
            raise SystemExit(f"{int((denom<=0).sum())} units have zero Σ LS·w — stop")
        ero_cls = (lsw / denom) * e                      # (nclass, n_units) tonnes
        tab = {}
        tot_area = area.sum()
        tot_ero = ero_cls.sum()
        for ci, name in enumerate(CLASS_NAMES):
            tab[name] = {
                "n_cells": int(cp["acc_n"][ci].sum()),
                "area_km2": float(area[ci].sum() / 1e6),
                "area_frac": float(area[ci].sum() / tot_area),
                "erosion_mt_yr": float(ero_cls[ci].sum() / 1e6 / wts.attrs["years"]),
                "erosion_frac": float(ero_cls[ci].sum() / tot_ero),
                "ls_v0_area_wtd_mean": float(cp["acc_lsw"][ci].sum() / cp["acc_area"][ci].sum()),
                "sum_ls_v2a_w": float(cp["acc_v2a"][ci].sum()),
                "sum_ls_v2b_w": float(cp["acc_v2b"][ci].sum()),
                "sum_ls_v0_w": float(cp["acc_lsw"][ci].sum()),
            }
        # erosion-weighted V2b/V2a decomposed by class, on the SAME within-unit shares
        v2a_u = cp["acc_v2a"][:, key]
        v2b_u = cp["acc_v2b"][:, key]
        share = lsw / denom                                # cell-class erosion share per unit
        w_u = e * 0.0
        # per-class erosion-weighted mean of (V2b/V2a) needs cell-level ratio weights:
        # E-weighted ratio = Σ_u Σ_c E_u·(Σ LS_V2x·w)_c / (Σ LS_V0·w)_u  ... exact by linearity
        f_v2a = float(np.sum(e * (v2a_u.sum(0) / denom)) / e.sum())
        f_v2b = float(np.sum(e * (v2b_u.sum(0) / denom)) / e.sum())
        tab_meta = {
            "f_ero_V2a_cellpass": f_v2a,
            "f_ero_V2b_cellpass": f_v2b,
            "f_ero_V2b_over_V2a": f_v2b / f_v2a,
            "erosion_frac_by_class": {n: tab[n]["erosion_frac"] for n in CLASS_NAMES},
            "class_contribution_to_f_ero_V2a":
                {n: float(np.sum(e * (v2a_u[i] / denom)) / e.sum()) for i, n in enumerate(CLASS_NAMES)},
            "class_contribution_to_f_ero_V2b":
                {n: float(np.sum(e * (v2b_u[i] / denom)) / e.sum()) for i, n in enumerate(CLASS_NAMES)},
        }
        del w_u
        tab_meta["R6_UNVERIFIED_Sf_units"] = {
            "percent_registered_reading": f_v2b,
            **{f"{t}": float(np.sum(e * (cp["acc_r6"][t][key] / denom)) / e.sum())
               for t in ("deg", "mm")},
        }
        out["slope_classes"] = tab
        out["slope_class_meta"] = tab_meta
        out["class_edges_pct"] = [float(x) for x in CLASS_EDGES_PCT]
        out["n_cells_scored"] = cp["n_cells"]

        print("=" * 100)
        print("SLOPE-CLASS SPLIT - eq. 14's own boundaries.  AREA vs EROSION.")
        print(f"{'class (Sf = 100 tan_th)':<24}{'cells':>12}{'area km2':>13}{'area %':>9}"
              f"{'Mt/yr':>11}{'erosion %':>11}{'LSbar V0':>10}")
        for n in CLASS_NAMES:
            d = tab[n]
            print(f"{n:<24}{d['n_cells']:>12,}{d['area_km2']:>13,.1f}{100*d['area_frac']:>9.3f}"
                  f"{d['erosion_mt_yr']:>11.3f}{100*d['erosion_frac']:>11.3f}"
                  f"{d['ls_v0_area_wtd_mean']:>10.3f}")
        print("=" * 100 + "\n", flush=True)

    (PROC / "ls_defect_a.json").write_text(json.dumps(out, indent=1))
    L.log(f"wrote {PROC / 'ls_defect_a.json'}")

    after = {p.name: sha256(p) for p in protected if p.is_file()}
    print("PROTECTED FILES")
    for k in before:
        print(f"  {k:<24}{'UNCHANGED' if before[k] == after.get(k) else '*** CHANGED ***'}")
    if after != before:
        raise SystemExit("a protected file changed — this must never happen")
    return 0


if __name__ == "__main__":
    sys.exit(main())

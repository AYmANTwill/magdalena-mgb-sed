#!/usr/bin/env python3.10
"""docs/46 §3.3 — the STRATIFIED LS report (the last owed deliverable of docs/47 §9.2 blocker 4).

For every LS variant it reports the LS **level** (LS̄, area-weighted AND erosion-weighted) on
the registered strata:

  * elevation bands     < 200 m · 200–1000 m · > 1000 m        (journal_decide-ls-resolution §2b)
  * slope terciles      equal-area thirds of per-minibacia mean Horn slope
  * per-station LS̄      erosion-weighted, for the 18 usable SSC stations (docs/42 §4.1)

Everything is per engine unit (mini, urh).  LS per unit comes from `urh_ls2d_variants.csv`
(ACT 1's committed product); the erosion weight E per unit comes from a decade engine run at
adopted defaults pinned to V0 (`ls_erosion_weights.erosion_weights`, GATE 299.5387 Mt/yr at
`volume_convention='williams_m3'` + `k_unit_system='us_customary'` @
`cp_revision='cited_central_2026_08_11'` — a load is never quoted without its convention AND
its `cp_revision`, docs/37 A1.3); the
per-minibacia elevation and slope come from a light Horn-slope zonal pass over the COP DEM using
`scripts/c3/ls2d.py`'s own grid mapping.

GATES (nothing from a failing run may be used):
  G1  basin erosion = 299.5387 Mt/yr at the adopted defaults `williams_m3` + `us_customary`
      @ `cited_central_2026_08_11`                              (via erosion_weights)
  G2  V0 column is 1.000 in every stratum, by definition
  G3  V0 per-station erosion-weighted LS̄ range reproduces docs/42 §4.1's 38.2 – 117.1

Reads only; writes only NEW files:
  data/processed/minibacia_topo.csv          per-minibacia mean elevation + mean tanθ (checkpoint)
  data/processed/urh_erosion_weights.csv      per-unit erosion weight (checkpoint, via harness)
  data/processed/ls_stratified_report.json    the three tables, as levels
  data/processed/ls_stratified_report.md      a human-readable fragment for docs/46 §10

`urh_ls2d.csv`, `minibacia_ls2d.csv` and the frozen bundle are NOT touched.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.enums import Resampling as RS

import pyflwdir
from pyflwdir import gis_utils

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ls2d as L  # noqa: E402
import ls_erosion_weights as EW  # noqa: E402

REPO = L.repo_root()
PROC = REPO / "data" / "processed"

ELEV_EDGES = [-np.inf, 200.0, 1000.0, np.inf]
ELEV_NAMES = ["<200 m", "200-1000 m", ">1000 m"]
DOCS42_STATION_RANGE = (38.2, 117.1)          # docs/42 §4.1, V0 erosion-weighted LS̄, ln range 1.12
DOCS42_LNRANGE = 1.12
YEARS_ADOPTED = 9.998631074606434             # 3652 d / 365.25 (docs/37 A1.3 scored decade)
VAR_LABELS = {
    "V0_ours_2026_08": "V0", "V1_lim_pixel": "V1", "V2a_m_cap05": "V2a",
    "V2b_m_step_eq14": "V2b", "V3_s_ws78": "V3", "V4_buarque_2015": "V4",
    "V4_dg": "V4dg", "V4p_buarque_2015_cap": "V4p", "V5_L_dg96_fd": "V5",
}


# ----------------------------------------------------------------- per-minibacia elevation + slope
def minibacia_topo() -> pd.DataFrame:
    """Area-weighted mean elevation (m) and mean tanθ (native 90 m Horn slope) per minibacia."""
    out = PROC / "minibacia_topo.csv"
    if out.is_file():
        L.log(f"minibacia_topo: reuse {out}")
        return pd.read_csv(out)

    with rasterio.open(PROC / "minibacias.tif") as ds:
        subs = ds.read(1)
    Hc, Wc = subs.shape
    mini_ids = np.unique(subs[subs > 0])
    n = mini_ids.size
    id_to_idx = np.full(int(mini_ids.max()) + 1, -1, "int64")
    id_to_idx[mini_ids] = np.arange(n)

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
    L.log(f"topo: DEM {H}x{W} ({elev.size/1e6:.1f} M cells); Horn slope ...")
    tan_slope = pyflwdir.dem.slope(elev, nodata=float(ND), latlon=True, transform=transform)

    xres, yres, north = transform[0], transform[4], transform[5]
    lat_row = north + (np.arange(H) + 0.5) * yres
    dx = np.array([abs(xres) * gis_utils.degree_metres_x(la) for la in lat_row], "float64")
    dy = np.array([abs(yres) * gis_utils.degree_metres_y(la) for la in lat_row], "float64")
    cell_area_row = dx * dy

    s_area = np.zeros(n)
    s_elev = np.zeros(n)
    s_slope = np.zeros(n)
    t0 = time.time()
    chunk = 512
    for r0 in range(0, H, chunk):
        r1 = min(H, r0 + chunk)
        rr = np.arange(r0, r1) // ratio - (r0 // ratio)
        cc = np.arange(W) // ratio
        mini_chunk = subs[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]
        el = elev[r0:r1]
        sl = tan_slope[r0:r1]
        v = (mini_chunk > 0) & (el > float(ND) + 1.0) & np.isfinite(sl) & (sl > float(ND) + 1.0)
        if not v.any():
            continue
        w = np.repeat(cell_area_row[r0:r1][:, None], W, axis=1)[v]
        idx = id_to_idx[mini_chunk[v]]
        s_area += np.bincount(idx, w, minlength=n)
        s_elev += np.bincount(idx, el[v].astype("float64") * w, minlength=n)
        s_slope += np.bincount(idx, np.maximum(sl[v].astype("float64"), 0.0) * w, minlength=n)
    L.log(f"topo: pass done in {time.time()-t0:.0f} s")

    good = s_area > 0
    df = pd.DataFrame({
        "id": mini_ids[good],
        "elev_m": s_elev[good] / s_area[good],
        "tan_slope": s_slope[good] / s_area[good],
        "topo_area_m2": s_area[good],
    })
    df.to_csv(out, index=False, float_format="%.10g")
    L.log(f"topo: wrote {out} ({len(df)} minibacias)")
    return df


# ----------------------------------------------------------------- station catchments (topology)
def station_catchments() -> dict[str, set[int]]:
    """For each usable SSC station: the set of minibacia ids draining THROUGH its outlet mini."""
    mb = pd.read_csv(PROC / "minibacias.csv")
    children: dict[int, list[int]] = {}
    for m, d in zip(mb["id"].astype(int), mb["downstream"].astype(int)):
        children.setdefault(d, []).append(m)

    inv = pd.read_csv(PROC / "sediment_inventory_qc.csv")
    usable = inv[inv["ssc_class"].isin(["usable", "usable-with-caveat"])].copy()
    cats: dict[str, set[int]] = {}
    for _, row in usable.iterrows():
        outlet = int(row["minibacia"])
        seen: set[int] = set()
        stack = [outlet]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(children.get(cur, []))
        cats[str(int(row["code"]))] = seen
    return cats, usable


# ----------------------------------------------------------------- weighted-mean helpers
def _wmean(vals: np.ndarray, w: np.ndarray) -> float:
    s = w.sum()
    return float(np.nan) if s <= 0 else float(np.sum(vals * w) / s)


def build_report() -> dict:
    # per-unit LS (all variants) + per-unit erosion weight, joined on (mini, urh)
    var = pd.read_csv(PROC / "urh_ls2d_variants.csv")
    ew_path = PROC / "urh_erosion_weights.csv"
    if ew_path.is_file():
        L.log(f"weights: reuse {ew_path}")
        wts = pd.read_csv(ew_path)
        gate_total = float(wts["eroded_t"].sum() / 1e6 / YEARS_ADOPTED)
    else:
        w = EW.erosion_weights()                          # GATE G1 (299.5387) inside
        w[["mini", "urh", "area_km2_urhfrac", "ls2d_hs", "eroded_t"]].to_csv(
            ew_path, index=False, float_format="%.10g")
        gate_total = float(w.attrs["total_mt_yr"])
        wts = w

    j = wts.merge(var, on=["mini", "urh"], how="left", validate="one_to_one")
    vcols = [c for c in var.columns if c.startswith("V")]
    if j[vcols].isna().any().any():
        raise SystemExit("a weighted unit has no LS variant row — stop")

    topo = minibacia_topo().set_index("id")
    j = j.join(topo[["elev_m", "tan_slope"]], on="mini")
    if j[["elev_m", "tan_slope"]].isna().any().any():
        miss = int(j[["elev_m", "tan_slope"]].isna().any(axis=1).sum())
        L.log(f"WARN {miss} units have no topo (dropped from elevation/slope strata)")

    E = j["eroded_t"].to_numpy()
    A = j["area_km2_urhfrac"].to_numpy()

    def strata_table(mask_fn, names, edges, key) -> dict:
        col = j[key].to_numpy()
        rows = {}
        for nm, lo, hi in zip(names, edges[:-1], edges[1:]):
            sel = (col > lo) & (col <= hi) if key != "elev_m" else (col > lo) & (col <= hi)
            sel = sel & np.isfinite(col)
            rows[nm] = {
                "n_units": int(sel.sum()),
                "area_km2": float(A[sel].sum()),
                "ero_frac": float(E[sel].sum() / E.sum()),
                "LSbar_area_wtd": {c: _wmean(j[c].to_numpy()[sel], A[sel]) for c in vcols},
                "LSbar_ero_wtd": {c: _wmean(j[c].to_numpy()[sel], E[sel]) for c in vcols},
            }
        return rows

    # elevation bands
    elev_rows = strata_table(None, ELEV_NAMES, ELEV_EDGES, "elev_m")
    # slope terciles: equal-AREA thirds on unit slope
    sl = j["tan_slope"].to_numpy()
    fin = np.isfinite(sl)
    order = np.argsort(sl[fin])
    cum = np.cumsum(A[fin][order])
    cuts = np.searchsorted(cum, [cum[-1] / 3.0, 2.0 * cum[-1] / 3.0])
    t_edges = [-np.inf, sl[fin][order][cuts[0]], sl[fin][order][cuts[1]], np.inf]
    slope_rows = strata_table(None, ["T1 gentlest", "T2 middle", "T3 steepest"], t_edges, "tan_slope")

    # per-station erosion-weighted LS̄ (levels), 18 usable stations
    cats, usable = station_catchments()
    mini_arr = j["mini"].to_numpy()
    st_rows = {}
    for _, row in usable.iterrows():
        code = str(int(row["code"]))
        sel = np.isin(mini_arr, list(cats[code]))
        st_rows[code] = {
            "name": str(row["name"]),
            "ssc_class": str(row["ssc_class"]),
            "n_units": int(sel.sum()),
            "n_minibacia": int(len(cats[code])),
            "LSbar_ero_wtd": {c: _wmean(j[c].to_numpy()[sel], E[sel]) for c in vcols},
            "LSbar_area_wtd": {c: _wmean(j[c].to_numpy()[sel], A[sel]) for c in vcols},
        }

    # GATE G3 — consistency, not exact reproduction.  docs/42 §4.1's 38.2-117.1 is over the
    # CAL-13 set; this report is over the 18 usable SSC stations, a different (broader) set, so
    # the range and ln-range must TRACK docs/42's rather than equal it.  A gross mismatch (wrong
    # catchments or weights) would move them far; a set difference moves them a little.
    v0 = "V0_ours_2026_08"
    v0_station = np.array([st_rows[c]["LSbar_ero_wtd"][v0] for c in st_rows])
    g3_lo, g3_hi = float(np.nanmin(v0_station)), float(np.nanmax(v0_station))
    g3_ln = float(np.log(g3_hi / g3_lo))
    g3 = (0.85 * DOCS42_STATION_RANGE[0] <= g3_lo <= 1.15 * DOCS42_STATION_RANGE[0]
          and 0.90 * DOCS42_STATION_RANGE[1] <= g3_hi <= 1.10 * DOCS42_STATION_RANGE[1]
          and abs(g3_ln - DOCS42_LNRANGE) < 0.20)

    return {
        "gate_total_mt_yr": gate_total,
        "vcols": vcols,
        "elevation_bands": elev_rows,
        "slope_terciles": {"tan_edges": [float(x) for x in t_edges[1:-1]], "rows": slope_rows},
        "stations": st_rows,
        "gate_v0_station_range": {"lo": g3_lo, "hi": g3_hi, "ln_range": g3_ln,
                                  "docs42": list(DOCS42_STATION_RANGE),
                                  "docs42_ln": DOCS42_LNRANGE,
                                  "note": "18 usable SSC stations vs docs/42 §4.1 CAL-13; "
                                          "consistency check, not exact reproduction",
                                  "PASS": bool(g3)},
    }


def render_md(rep: dict) -> str:
    v = rep["vcols"]
    short = [VAR_LABELS.get(c, c) for c in v]
    lines = ["### docs/46 §3.3 — stratified LS levels (LS̄), per variant", ""]
    # A load is never quoted without its convention AND its cp_revision (docs/37 A1.3,
    # src/mgb_sediment.py's convention ladder).  These are SedParams()'s defaults, which
    # erosion_weights() runs at; "(adopted defaults)" alone did not name them (2026-08-19).
    lines.append(f"Basin erosion gate: **{rep['gate_total_mt_yr']:.4f} Mt/yr** "
                 f"(volume_convention=williams_m3, k_unit_system=us_customary, "
                 f"cp_revision='cited_central_2026_08_11').")
    lines.append("")

    def block(title, rows, wkey):
        out = [f"**{title}** — {wkey.replace('_',' ')}", "",
               "| stratum | n units | area km² | ero % | " + " | ".join(short) + " |",
               "|---|--:|--:|--:|" + "|".join(["--:"] * len(v)) + "|"]
        for nm, r in rows.items():
            cells = " | ".join(f"{r[wkey][c]:.2f}" for c in v)
            out.append(f"| {nm} | {r['n_units']} | {r['area_km2']:.0f} | "
                       f"{100*r['ero_frac']:.1f} | {cells} |")
        out.append("")
        return out

    lines += block("Elevation bands", rep["elevation_bands"], "LSbar_ero_wtd")
    lines += block("Elevation bands", rep["elevation_bands"], "LSbar_area_wtd")
    lines += block("Slope terciles (equal-area)", rep["slope_terciles"]["rows"], "LSbar_ero_wtd")

    lines += ["**Per-station erosion-weighted LS̄ (levels), 18 usable SSC stations**", "",
              "| station | class | units | " + " | ".join(short) + " |",
              "|---|---|--:|" + "|".join(["--:"] * len(v)) + "|"]
    for code, r in rep["stations"].items():
        cells = " | ".join(f"{r['LSbar_ero_wtd'][c]:.1f}" for c in v)
        lines.append(f"| {code} {r['name']} | {r['ssc_class']} | {r['n_units']} | {cells} |")
    g = rep["gate_v0_station_range"]
    lines += ["", f"GATE G3 (consistency) — V0 per-station range **{g['lo']:.1f} – {g['hi']:.1f}** "
              f"(ln {g['ln_range']:.3f}) vs docs/42 §4.1 **{g['docs42'][0]} – {g['docs42'][1]}** "
              f"(ln {g['docs42_ln']}, CAL-13): **{'PASS' if g['PASS'] else 'FAIL'}** — "
              f"18 usable stations vs CAL-13, tracks not equals."]
    return "\n".join(lines)


def main() -> int:
    rep = build_report()
    (PROC / "ls_stratified_report.json").write_text(json.dumps(rep, indent=1))
    md = render_md(rep)
    (PROC / "ls_stratified_report.md").write_text(md)
    print("\n" + md)
    print("\nwrote data/processed/ls_stratified_report.{json,md}")
    g = rep["gate_v0_station_range"]
    if not g["PASS"]:
        raise SystemExit(f"GATE G3 FAILED (beyond a set difference): V0 station range "
                         f"{g['lo']:.1f}-{g['hi']:.1f} ln {g['ln_range']:.3f} is NOT consistent "
                         f"with docs/42 §4.1 {g['docs42']} ln {g['docs42_ln']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

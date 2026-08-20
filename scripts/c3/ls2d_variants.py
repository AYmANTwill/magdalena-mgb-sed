"""
C3.1 / docs 46 §3.1 — the LS **variant** harness.  Measures the levers; changes nothing.

WHAT THIS IS FOR
----------------
`docs/46_ls_preregistration.md` (cited here as `..._DRAFT.md` when this harness was written;
the pre-registration has since been frozen under the shorter name) names eight LS
formulations and asks for each one's basin level on our own 90 m grid, so that the choice
between them can be made on written source grounds instead of on what each does to the
sediment total.  Four of the eight have already been published (`docs/46` §1, from
`journal_decide-ls-resolution` §3b); this harness recomputes those **and** the ones that
have never been measured.

IT IS NOT A SECOND IMPLEMENTATION OF LS
---------------------------------------
`scripts/c3/ls2d.py` is imported, not copied, and **V0 is produced by calling its own
`ls_variants()`** — the 4th return value, `ls4`, is the `ls2d_hs` column the engine reads
(`src/mgb_sediment.py`, `ls2d_column="ls2d_hs"`).  V0 therefore cannot drift from the
committed definition, because it *is* the committed definition.  The DEM, the slope, the pit
filling, the D8 routing, the flow accumulation, the URH grid, the per-row cell geometry and
the area-weighted accumulation are all `ls2d.py`'s, reproduced by reusing its functions and
its constants.  The only new code is the seven variant expressions and the reporting.

THE V0 REPRODUCTION GATE (this runs first, and a failure stops the harness)
--------------------------------------------------------------------------
Before any new variant is reported, the basin area-weighted mean of V0 must reproduce the
published **39.812** (`docs/46` §1; `journal_decide-ls-resolution` §3b, all 30,235,916 basin
cells).  A harness that cannot reproduce a known number cannot be trusted with unknown ones.
The tolerance is 1e-3 absolute on that mean; the value obtained is always printed to full
precision, gate or no gate.

THE NINE VARIANTS  (docs/46 §3.1; ids are the column names in the output CSV)
----------------------------------------------------------------------------
All are evaluated on the native 90 m grid.  "hs basis" = upslope area capped at the
channel-initiation source area A_CHANNEL = 1 km², which is what `ls2d_hs` means.

  V0_ours_2026_08       hs basis, continuous McCool-89 m, S = (sinθ/0.0896)^1.3, n = 1.3.
                        The current engine input.  Computed by ls2d.ls_variants()[3].
  V1_lim_pixel          V0 with the slope length limited to ONE DEM PIXEL (Buarque 2015
                        p. 94).  Implemented as a_unit = min(upslope_area, cell_area)/D;
                        because a cell's upslope area always contains the cell itself this
                        is exactly a_unit = D, i.e. a one-pixel slope length everywhere.
  V2a_m_cap05           V0 with m -> min(m, 0.5).  A CAP.  This is the row published as
                        ×0.502.  It is nobody's published formulation (docs/46 §2.2).
  V2b_m_step_eq14       V0 with m -> Buarque eq. 14, the STEP function
                        0.2 (Sf < 1 %) / 0.3 (1–3 %) / 0.4 (3–5 %) / 0.5 (Sf >= 5 %),
                        Sf = slope percent = 100·tanθ.  NEVER MEASURED BEFORE this run.
                        (docs/46 (R6): the `Sf` units are not yet verified against Buarque
                        pp. 46–48.  This harness implements percent, as the existing record
                        does, and claims no verification.)
  V3_s_ws78             V0 with S -> Wischmeier & Smith (1978) = Buarque eq. 18,
                        65.41 sin²θ + 4.56 sinθ + 0.065.
  V4_buarque_2015       V1 + V2b + V3 — the source's three levers carried on OUR continuous
                        `L`.  **THIS is the ×0.421 row exactly as published**, kept so the
                        prior number stays reproducible: its area-weighted level
                        16.775413430326214 reproduces the published row to 15 significant
                        figures (docs/51 §2.2).  A documented **hybrid**, not the source read
                        whole — ~~"the source formulation AS READ"~~ was this line's label
                        until 2026-08-19 and is wrong; the source read whole is `V4_dg`.
  V4_dg                 V1 + V2b + V3 + eq. 13's finite-difference `L` — **the source
                        formulation READ WHOLE**, and the ADOPTED field
                        (`ls_formulation = 'buarque_2015_dg'`, f_LS = 0.25146
                        erosion-weighted / 0.2446790094097074 area-weighted; docs/46 §3.1).
                        Added by ACT 1, after the other eight were registered; see the
                        inline note at its variant expression.
  V4p_buarque_2015_cap  V1 + V2a + V3 — the **cap** composition.  ~~the ×0.421 row exactly as
                        published, kept so the prior number stays reproducible~~ **RETIRED /
                        superseded 2026-08-19 — shown, not quoted as current.**  V4 and V4′
                        were SWAPPED in the draft: the published ×0.421 row is V4 (the eq. 14
                        STEP), and this cap composition is **nobody's published formulation**
                        (docs/46 §2.2) and had NEVER been measured before 2026-08-11
                        (docs/46 §3.1 amendment (b), docs/49, docs/51 §7 (b)).
  V5_L_dg96_fd          V0 with the literal Desmet & Govers (1996) finite-difference L
                        (their eq. 11 = Buarque eq. 13) and **S HELD AT V0's**
                        (sinθ/0.0896)^1.3, on the **hs (1 km²) basis**:
                            A_in = max(min(upslope_area, 1 km²) − cell_area, 0)
                            L    = [(A_in+D²)^(m+1) − A_in^(m+1)]
                                   / [D^(m+2) · x^m · 22.13^m]
                        This isolates the L *form*.  The published ×0.790 does not: it is
                        `ls2d.py`'s `ls2d_dg96`, which also swaps S from Moore & Burch (1986)
                        to McCool (1987) and was measured on the UNCAPPED `ls2d` column
                        (docs/46 §1.1 Defect B).  Both of those confounded ratios are
                        reported here too, as DIAGNOSTICS, so the confound is visible.

AGGREGATION — FIXED, AND THE MEDIAN IS NOT AN AGGREGATE
-------------------------------------------------------
Per-cell LS -> (minibacia, URH) by **area-weighted mean**, weights = true cell area (which
varies with latitude), exactly as `ls2d.py` does it and as `docs/46` §3.2 requires.  The
per-cell **median is computed and reported as a DIAGNOSTIC only**; `docs/46` §3.2 forbids it
as a headline for a linear factor, and this script's report labels it that way.

OUTPUTS  (new files; nothing existing is touched)
-------------------------------------------------
  data/processed/urh_ls2d_variants.csv       long, key (mini, urh), one column per variant id
  data/processed/minibacia_ls2d_variants.csv companion, one row per minibacia
  data/processed/ls2d_variants_summary.json  basin + strata levels, ratios, the gate result

`data/processed/urh_ls2d.csv` and `minibacia_ls2d.csv` are **never opened for writing**; the
harness SHA-256s both before and after and prints the comparison (`docs/46` §3.1, registered
hard requirement).

Usage:  python3.10 scripts/c3/ls2d_variants.py [--chunk 512] [--no-gate-stop]
        Native 90 m only — there is no --scale, deliberately: `ls2d.py --scale != 1` inside
        the repository tree overwrites the committed products
        (`docs/agents/journal_decide-ls-resolution.md` §2).

References: as `scripts/c3/ls2d.py`, plus
Buarque, D.C. (2015). Simulação da geração e do transporte de sedimentos em grandes bacias:
    estudo de caso do rio Madeira. PhD thesis, IPH/UFRGS, 182 pp.  (eqs. 13/14/18; p. 94 the
    one-pixel slope-length limiter; p. 121 the author's own over-estimate verdict.)
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

# --- import the committed implementation; do NOT re-implement it ------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ls2d as L  # noqa: E402  (scripts/c3/ls2d.py — the module this harness is anchored to)

# ------------------------------------------------------------------------------ registry
V0 = "V0_ours_2026_08"
VARIANTS = [
    V0,
    "V1_lim_pixel",
    "V2a_m_cap05",
    "V2b_m_step_eq14",
    "V3_s_ws78",
    "V4_buarque_2015",
    "V4_dg",
    "V4p_buarque_2015_cap",
    "V5_L_dg96_fd",
]
# diagnostics: computed by ls2d.py itself, reported but NOT written as variants
DIAGNOSTICS = ["D_ls2d_uncapped", "D_ls2d_mb86", "D_ls2d_dg96_published"]
ALL_COLS = VARIANTS + DIAGNOSTICS

PUBLISHED_V0_MEAN = 39.812      # docs/46 §1; journal_decide-ls-resolution §3b
GATE_TOL = 1e-3                 # absolute, on the basin area-weighted mean
ANDEAN_M = 1000.0               # docs/46 §3.3 strata
LOWLAND_M = 200.0


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):   # 4 MB reads (Defender, CLAUDE.md)
            h.update(blk)
    return h.hexdigest()


def m_step_eq14(tan_theta: np.ndarray) -> np.ndarray:
    """Buarque (2015) eq. 14: m stepped on slope PERCENT.  0.2 / 0.3 / 0.4 / 0.5."""
    sf = tan_theta * 100.0
    return np.where(sf < 1.0, 0.2, np.where(sf < 3.0, 0.3, np.where(sf < 5.0, 0.4, 0.5)))


def s_ws78(sin_theta: np.ndarray) -> np.ndarray:
    """Buarque (2015) eq. 18 = Wischmeier & Smith (1978)."""
    return 65.41 * sin_theta ** 2 + 4.56 * sin_theta + 0.065


def variant_block(tan_theta: np.ndarray, upslope_area_m2: np.ndarray,
                  cell_area_m2: np.ndarray, x_aspect: np.ndarray) -> dict:
    """All eight variants + three diagnostics for one chunk of cells, float64.

    V0 and the three diagnostics come straight out of `ls2d.ls_variants()`; only the seven
    new expressions are written here.
    """
    ls1, ls2, ls3, ls4 = L.ls_variants(tan_theta, upslope_area_m2, cell_area_m2, x_aspect)

    tan = np.maximum(tan_theta, L.TAN_FLOOR)
    sin = tan / np.sqrt(1.0 + tan * tan)
    d = np.sqrt(cell_area_m2)

    m_cont = L.slope_exponent_m(sin)
    m_cap = np.minimum(m_cont, 0.5)
    m_step = m_step_eq14(tan)

    s_ours = (sin / L.UNIT_PLOT_SIN) ** L.N_EXP
    s_ws = s_ws78(sin)

    a_hs = np.minimum(upslope_area_m2, L.A_CHANNEL_M2) / d       # V0's basis
    a_px = np.minimum(upslope_area_m2, cell_area_m2) / d          # == d: one-pixel length

    def length(a_unit, m):
        return (m + 1.0) * (a_unit / L.UNIT_PLOT_LEN_M) ** m

    # literal D&G finite-difference L on the hs basis, m continuous
    a_in_hs = np.maximum(np.minimum(upslope_area_m2, L.A_CHANNEL_M2) - cell_area_m2, 0.0)
    mp1 = m_cont + 1.0
    l_dg_hs = ((a_in_hs + cell_area_m2) ** mp1 - a_in_hs ** mp1) / (
        d ** (m_cont + 2.0) * x_aspect ** m_cont * L.UNIT_PLOT_LEN_M ** m_cont)

    return {
        V0:                     ls4,                                  # ls2d.py's own ls2d_hs
        "V1_lim_pixel":         length(a_px, m_cont) * s_ours,
        "V2a_m_cap05":          length(a_hs, m_cap) * s_ours,
        "V2b_m_step_eq14":      length(a_hs, m_step) * s_ours,
        "V3_s_ws78":            length(a_hs, m_cont) * s_ws,
        "V4_buarque_2015":      length(a_px, m_step) * s_ws,
        # V4_dg (ACT 1 / docs/47 §9.2 blocker 2): the adopted `ls_formulation = buarque_2015_dg`,
        # the source formulation READ WHOLE — D&G finite-difference L on the ONE-PIXEL basis
        # (a_in = 0, so it degenerates to (d/(22.13*x))^m), m = eq.14 step, S = W&S-78.
        # Ported VERBATIM from ls2d_defect_b.py:146-159 (`l_dg_px(m_step, x_aspect) * s_ws`),
        # the harness that derived f_LS = 0.25146 erosion / 0.2446790094097074 area-weighted.
        "V4_dg":                (d / (L.UNIT_PLOT_LEN_M * x_aspect)) ** m_step * s_ws,
        "V4p_buarque_2015_cap": length(a_px, m_cap) * s_ws,
        "V5_L_dg96_fd":         l_dg_hs * s_ours,
        "D_ls2d_uncapped":      ls1,
        "D_ls2d_mb86":          ls2,
        "D_ls2d_dg96_published": ls3,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="LS variant harness (docs/46 §3.1). Native 90 m.")
    ap.add_argument("--chunk", type=int, default=512, help="rows per processing chunk")
    ap.add_argument("--no-gate-stop", action="store_true",
                    help="report the V0 gate failure but continue (default: STOP)")
    args = ap.parse_args()

    repo = L.repo_root()
    proc = repo / "data" / "processed"
    scratch = Path(os.environ.get("LS2D_CACHE", Path(tempfile.gettempdir()) / "ls2d_cache"))
    scratch.mkdir(parents=True, exist_ok=True)

    protected = [proc / "urh_ls2d.csv", proc / "minibacia_ls2d.csv"]
    before = {p.name: sha256(p) for p in protected}
    for k, v in before.items():
        L.log(f"SHA-256 before  {k}  {v}")

    # ---- minibacia + URH grids (coarse) ------------------------------------------------
    with rasterio.open(proc / "minibacias.tif") as ds:
        subs = ds.read(1)
        dst_tr = ds.transform
    Hc, Wc = subs.shape
    mini_ids = np.unique(subs[subs > 0])
    n_mini = mini_ids.size
    L.log(f"minibacias.tif {Hc}x{Wc} | {n_mini} minibacias")
    urh_coarse = L.build_urh_coarse(repo, subs, dst_tr, scratch / "urh_coarse.npz")

    # ---- DEM, slope, routing (ls2d.py main(), scale = 1) -------------------------------
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

    # ---- accumulators ------------------------------------------------------------------
    id_to_idx = np.full(int(mini_ids.max()) + 1, -1, "int32")
    id_to_idx[mini_ids] = np.arange(n_mini, dtype="int32")
    urh_to_idx = np.full(int(L.URH_CODES.max()) + 1, -1, "int32")
    urh_to_idx[L.URH_CODES] = np.arange(L.URH_CODES.size, dtype="int32")
    nkey = n_mini * 25
    acc_w = np.zeros(nkey, "float64")
    acc_n = np.zeros(nkey, "int64")
    acc = {c: np.zeros(nkey, "float64") for c in ALL_COLS}

    strata = ["basin", "lowland_lt200m", "mid_200_1000m", "andean_gt1000m"]
    str_w = {s: 0.0 for s in strata}
    str_sum = {s: {c: 0.0 for c in ALL_COLS} for s in strata}

    n_basin = int((subs > 0).sum()) * ratio * ratio
    store_path = scratch / "ls2d_variants_percell.f32"
    store = np.memmap(store_path, dtype="float32", mode="w+", shape=(len(ALL_COLS), n_basin))
    filled = 0
    n_nonfinite = {c: 0 for c in ALL_COLS}

    L.log(f"per-cell pass over <= {n_basin/1e6:.1f} M basin cells, {args.chunk}-row chunks ...")
    t0 = time.time()
    for r0 in range(0, H, args.chunk):
        r1 = min(H, r0 + args.chunk)
        mini_blk = subs[r0 // ratio:(r1 + ratio - 1) // ratio]
        rr = np.arange(r0, r1) // ratio - (r0 // ratio)
        cc = np.arange(W) // ratio
        mini_chunk = mini_blk[np.ix_(rr, cc)]
        urh_chunk = urh_coarse[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]
        elevc_chunk = elev_c[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]

        sl = tan_slope[r0:r1]
        ua = upa[r0:r1]
        v = (mini_chunk > 0) & (sl > float(ND) + 1.0) & np.isfinite(sl) & (ua > 0)
        if not v.any():
            continue

        area_col = np.repeat(cell_area_row[r0:r1][:, None], W, axis=1)
        xasp = np.where(np.isin(d8[r0:r1], L.D8_DIAGONAL), np.sqrt(2.0), 1.0)

        w = area_col[v]
        tan_v = sl[v].astype("float64")
        out = variant_block(tan_v, ua[v].astype("float64"), w, xasp[v])

        mi = id_to_idx[mini_chunk[v]]
        ui = urh_to_idx[np.clip(urh_chunk[v], 0, urh_to_idx.size - 1)]
        ui = np.where(urh_chunk[v] > 0, ui, -1)
        key = mi.astype("int64") * 25 + (ui + 1)
        acc_w += np.bincount(key, weights=w, minlength=nkey)
        acc_n += np.bincount(key, minlength=nkey)

        ec = elevc_chunk[v]
        masks = {"basin": slice(None), "lowland_lt200m": ec < LOWLAND_M,
                 "mid_200_1000m": (ec >= LOWLAND_M) & (ec <= ANDEAN_M),
                 "andean_gt1000m": ec > ANDEAN_M}
        for s in strata:
            str_w[s] += float(np.sum(w[masks[s]]))

        k = tan_v.size
        for j, c in enumerate(ALL_COLS):
            a = out[c]
            bad = ~np.isfinite(a)
            if bad.any():
                n_nonfinite[c] += int(bad.sum())
                a = np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0)
            acc[c] += np.bincount(key, weights=a * w, minlength=nkey)
            for s in strata:
                str_sum[s][c] += float(np.sum(a[masks[s]] * w[masks[s]]))
            store[j, filled:filled + k] = a
        filled += k

    del tan_slope, upa, d8, subs, urh_coarse, elev_c
    store.flush()
    L.log(f"per-cell pass done: {filled:,} basin cells scored in {time.time()-t0:.0f} s")

    # ---- THE V0 GATE -------------------------------------------------------------------
    tot_w = acc_w.sum()
    v0_mean = float(acc[V0].sum() / tot_w)
    v0_mean_str = float(str_sum["basin"][V0] / str_w["basin"])
    gate_ok = abs(v0_mean - PUBLISHED_V0_MEAN) <= GATE_TOL
    print("\n" + "=" * 78)
    print("V0 REPRODUCTION GATE  (docs/46 §1: published ls2d_hs area-weighted mean 39.812)")
    print("=" * 78)
    print(f"  cells scored                    : {filled:,}   (published 30,235,916)")
    print(f"  basin area from cell weights    : {tot_w/1e6:,.4f} km2")
    print(f"  V0 area-weighted mean, MEASURED : {v0_mean!r}")
    print(f"  same via the strata accumulator : {v0_mean_str!r}")
    print(f"  published                       : {PUBLISHED_V0_MEAN}")
    print(f"  difference                      : {v0_mean - PUBLISHED_V0_MEAN:+.9e}")
    print(f"  GATE                            : {'PASS' if gate_ok else 'FAIL'}")
    print("=" * 78 + "\n")
    if not gate_ok and not args.no_gate_stop:
        print("STOP: the harness does not reproduce the known number, so it cannot be "
              "trusted to produce the unknown ones. No variant is reported and no file "
              "is written.  Re-run with --no-gate-stop only to diagnose.", flush=True)
        after = {p.name: sha256(p) for p in protected}
        print(f"protected files unchanged: {after == before}")
        return 2

    # ---- levels ------------------------------------------------------------------------
    summary = {"n_cells": int(filled), "basin_area_km2": tot_w / 1e6,
               "gate": {"published_v0_mean": PUBLISHED_V0_MEAN, "measured_v0_mean": v0_mean,
                        "abs_tol": GATE_TOL, "passed": bool(gate_ok)},
               "strata_area_km2": {s: str_w[s] / 1e6 for s in strata},
               "variants": {}}
    L.log("per-cell medians (DIAGNOSTIC ONLY - docs/46 §3.2) ...")
    for j, c in enumerate(ALL_COLS):
        col = np.array(store[j, :filled])
        med = float(np.median(col))
        p90 = float(np.percentile(col, 90))
        del col
        summary["variants"][c] = {
            "area_wtd_mean": float(acc[c].sum() / tot_w),
            **{f"area_wtd_mean_{s}": float(str_sum[s][c] / str_w[s]) for s in strata[1:]},
            "median_DIAGNOSTIC_ONLY": med,
            "p90_DIAGNOSTIC_ONLY": p90,
            "n_nonfinite_cells": n_nonfinite[c],
            "is_variant": c in VARIANTS,
        }
    base = summary["variants"][V0]["area_wtd_mean"]
    for c in ALL_COLS:
        r = summary["variants"][c]["area_wtd_mean"] / base
        summary["variants"][c]["ratio_to_V0"] = r
        summary["variants"][c]["ln_ratio_to_V0"] = float(np.log(r))

    print("=" * 100)
    print("LS VARIANT LEVELS — headline aggregate is the AREA-WEIGHTED MEAN (docs/46 §3.2).")
    print("The median column is DIAGNOSTIC ONLY and is not an admissible aggregate for a "
          "linear factor.")
    print("=" * 100)
    print(f"{'id':<24}{'area-wtd mean':>15}{'Andean >1000 m':>16}"
          f"{'median (diag)':>15}{'x V0':>10}{'ln x V0':>10}")
    for c in ALL_COLS:
        d = summary["variants"][c]
        tag = "" if d["is_variant"] else "  [diagnostic]"
        print(f"{c:<24}{d['area_wtd_mean']:>15.4f}{d['area_wtd_mean_andean_gt1000m']:>16.4f}"
              f"{d['median_DIAGNOSTIC_ONLY']:>15.4f}{d['ratio_to_V0']:>10.4f}"
              f"{d['ln_ratio_to_V0']:>10.4f}{tag}")
    print("=" * 100 + "\n")

    # ---- (minibacia, URH) and minibacia tables ----------------------------------------
    A = acc_w.reshape(n_mini, 25)
    N = acc_n.reshape(n_mini, 25)
    M = {c: acc[c].reshape(n_mini, 25) for c in VARIANTS}

    tot_a = A.sum(1)
    mini_tab = pd.DataFrame({"id": mini_ids.astype("int32"), "n_cells": N.sum(1),
                             "area_km2_cells": tot_a / 1e6})
    for c in VARIANTS:
        mini_tab[c] = M[c].sum(1) / tot_a
    out_mini = proc / "minibacia_ls2d_variants.csv"
    mini_tab.to_csv(out_mini, index=False, float_format="%.8g")
    L.log(f"wrote {out_mini}  ({len(mini_tab)} rows)")

    mi_idx, ui_slot = np.nonzero(N[:, 1:] > 0)
    urh_area = A[:, 1:][mi_idx, ui_slot]
    urh_tab = pd.DataFrame({
        "mini": mini_ids[mi_idx].astype("int32"),
        "urh": L.URH_CODES[ui_slot],
        "n_cells": N[:, 1:][mi_idx, ui_slot],
        "area_km2": urh_area / 1e6,
        "area_frac": urh_area / A[:, 1:].sum(1)[mi_idx],
    })
    for c in VARIANTS:
        urh_tab[c] = M[c][:, 1:][mi_idx, ui_slot] / urh_area
    urh_tab = urh_tab.sort_values(["mini", "urh"])
    out_urh = proc / "urh_ls2d_variants.csv"
    urh_tab.to_csv(out_urh, index=False, float_format="%.8g")
    L.log(f"wrote {out_urh}  ({len(urh_tab)} rows, {urh_tab.mini.nunique()} minibacias)")

    # cross-check: the URH table must reproduce the basin level of every variant
    summary["urh_table_check"] = {}
    for c in VARIANTS:
        lvl = float((urh_tab[c] * urh_tab.area_km2).sum() / urh_tab.area_km2.sum())
        summary["urh_table_check"][c] = {
            "urh_area_wtd_level": lvl,
            "vs_basin_ratio": lvl / summary["variants"][c]["area_wtd_mean"]}

    out_json = proc / "ls2d_variants_summary.json"
    out_json.write_text(json.dumps(summary, indent=1))
    L.log(f"wrote {out_json}")

    after = {p.name: sha256(p) for p in protected}
    print("\nPROTECTED COMMITTED PRODUCTS (docs/46 §3.1 hard requirement)")
    for p in protected:
        same = before[p.name] == after[p.name]
        print(f"  {p.name:<24} {'UNCHANGED' if same else '*** CHANGED ***'}  {after[p.name]}")
    if after != before:
        raise SystemExit("a committed LS product changed — this must never happen")
    return 0


if __name__ == "__main__":
    sys.exit(main())

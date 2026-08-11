"""
C3.1 - LS2D: the two-dimensional topographic (length-slope) factor for MUSLE.

WHAT THIS PRODUCES
------------------
The last missing *static* MUSLE input.  MUSLE in this project is

    Sed = alpha * (Qsur * qpeak * A)^beta * K * C * P * LS2D

with K per minibacia (minibacia_soil_params.csv:K) and C/P from the 8 WorldCover
hydrological classes.  This script builds LS2D per 90 m raster cell and aggregates it
area-weighted to (a) the 8,672 minibacias and (b) the 24 URH classes (soil family x
land class) inside each minibacia, so C3.4 can use whichever resolution it needs.

WHY A 2-D LS AND NOT THE 1-D USLE LS
------------------------------------
The classical USLE L factor needs a *slope length*, which is undefined on a raster.
Desmet & Govers (1996) replaced it with the **unit contributing area** (upslope area
per unit contour width), which a flow-accumulation grid gives directly.  That is the
"2-D" in LS2D.

THE FORMULA ACTUALLY EVALUATED  (variant `ls2d`, the primary output)
-------------------------------------------------------------------
    LS = (m + 1) * (A_unit / 22.13)^m * (sin(beta) / 0.0896)^n            ... (1)

    A_unit = (A_in + D^2) / D          [m]   unit contributing area (per unit contour
                                             width); A_in = upslope area entering the
                                             cell, D = cell size, so A_unit is simply
                                             the total upslope area of the cell / D.
    beta                               [rad] local slope angle (Horn 3x3 gradient)
    22.13 m                                  the USLE unit-plot length (Wischmeier &
                                             Smith 1978)
    0.0896 = sin(5.143 deg)                  the USLE unit-plot slope (9 %)

M / N CONVENTION USED (stated explicitly, as required; no constant is invented here)
------------------------------------------------------------------------------------
* **m - slope-dependent, NOT a fixed number.**  The "standard slope-dependent form"
  (McCool et al. 1989, adopted verbatim as eqs. 5-6 of Desmet & Govers 1996):

        m = beta_r / (1 + beta_r),
        beta_r = (sin(theta) / 0.0896) / (3 * sin(theta)^0.8 + 0.56)

  beta_r is the rill-to-interrill erosion ratio for a moderately rill-prone soil.
  m therefore runs from ~0.0 on flats to ~0.5 on steep Andean slopes - it is *not*
  a tuned parameter.
* **n = 1.3.**  Moore & Burch (1986) give n = 1.0-1.3 for the (sin beta / 0.0896)^n
  slope term and 1.3 for rill-dominated overland flow; Mitasova et al. (1996) use the
  same (m+1) * (A/22.13)^m * (sin b/0.0896)^n form with n up to 1.3.  A steep Andean
  basin with dominant rill/gully transport is the rill-dominated case, so n = 1.3.

THE CHANNEL PROBLEM, AND THE `ls2d_hs` COLUMN (read this before using the output)
---------------------------------------------------------------------------------
Eq. (1) has no upper limit on A_unit.  On a mainstem cell A_unit = A/D reaches ~5e6 m,
i.e. the USLE slope-length relation gets extrapolated ~5 orders of magnitude past the
22.13 m plot it was fitted on, and LS blows up into the thousands.  That is a
domain-of-validity failure, not a coding error: USLE/RUSLE describe **hillslope** sheet
and rill erosion, not channel transport.  Measured at 740 m the water URH classes came
out with the highest LS of all 24 (`Medium x Water` LS 240.6) - which is nonsense as an
erosion signal.
So a second column is produced, `ls2d_hs`: **identical equation, identical constants**,
with the upslope area capped at a channel-initiation source area A_CHANNEL = 1 km2 (the
upper end of the humid/steep field range in Montgomery & Dietrich 1988, 1992).  Nothing
is tuned; the cap only stops the extrapolation where channels begin.  With it,
`Medium x Water` falls 240.6 -> 2.89 while hillslope classes barely move
(`Coarse x Bare` 76.8 -> 62.3).  **`ls2d_hs` is the column MUSLE should use**;
`ls2d` is kept unmodified so the choice stays visible and reversible.

TWO CROSS-CHECK VARIANTS ARE ALSO COMPUTED AND REPORTED (never silently substituted)
------------------------------------------------------------------------------------
* `ls2d_mb86` : eq. (1) with the *fixed* Moore & Burch (1986) constants m = 0.4,
  n = 1.3.  Shows how much of the answer rides on the slope-dependent m.
* `ls2d_dg96` : the **literal** Desmet & Govers (1996) finite-difference L (their
  eq. 11), which is what "Desmet & Govers" strictly means, multiplied by the McCool
  et al. (1987) S factor:

        L = [ (A_in + D^2)^(m+1) - A_in^(m+1) ]
            / [ D^(m+2) * x^m * 22.13^m ]                                 ... (2)
        x = |sin(alpha)| + |cos(alpha)|,  alpha = aspect  (D&G eq. 12; with D8 this
            is exactly 1 for a cardinal receiver and sqrt(2) for a diagonal one)
        S = 10.8 * sin(theta) + 0.03      for tan(theta) <  0.09
        S = 16.8 * sin(theta) - 0.50      for tan(theta) >= 0.09          ... (3)

  Eq. (1) is the continuous limit of eq. (2); reporting both is the sanity check that
  the implementation is not off by an order of magnitude.

FLAT-CELL HANDLING  (sanity gate 4)
-----------------------------------
Both forms drive LS -> 0 as sin(beta) -> 0, and eq. (2) additionally divides by x^m.
x is never 0 (min 1).  sin(beta) is floored at tan(beta) = 1e-4 (0.01 %, i.e. a 9 mm
drop across a 90 m cell - an order of magnitude below the DEM's vertical precision, so
the floor is a *numerical* guard, not a physical statement).  Consequence: a perfectly
flat cell gets LS ~ 1.4e-4 - strictly positive, finite, and effectively zero erosion,
which is the physically correct answer for a flat floodplain cell.  The number of cells
that hit the floor is reported.  No cell is dropped and no NaN is produced.

DATA PROVENANCE (see docs/agents/journal_c31-ls2d.md)
-----------------------------------------------------
nb07 builds the pit-filled DEM, the D8 directions and the flow accumulation **in
memory only** - none of the three is written to data/processed/*.tif.  They are
therefore recomputed here from the *same* source DEM (`output_hh.tif`, extracted from
data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz) with the *same* library
(pyflwdir), reproducing nb07 cells 5 and 7 exactly.  The minibacia partition is NOT
re-derived: data/processed/minibacias.tif is read as-is.  The URH grid is rebuilt
exactly as nb08 cell 10 (soil_family_igac.tif x WorldCover, URH = soil*10 + land) and
cached in the scratchpad so reruns are fast.

OUTPUT LAYOUT
-------------
`data/processed/minibacia_ls2d.csv`  - one row per minibacia (8,672):
    id, n_cells, area_km2_cells, ls2d, ls2d_hs, ls2d_median, ls2d_p90,
    ls2d_mb86, ls2d_dg96, urh_cover_frac
  `ls2d*` are AREA-WEIGHTED MEANS of the per-cell values inside the minibacia
  (weights = true cell area, which varies with latitude).  `ls2d_median` / `ls2d_p90`
  are the EXACT per-cell median / 90th percentile of `ls2d` inside the minibacia (not
  of any aggregate).  `area_km2_cells` is the area of the 90 m cells actually summed
  (a cross-check against minibacias.csv:area_km2); `urh_cover_frac` is the area
  fraction of the minibacia that has a valid URH code (soil and land cover both
  defined).

`data/processed/urh_ls2d.csv` - LONG format, one row per (minibacia, URH) pair that
  exists (~33k rows, NOT a 8672x24 matrix with holes):
    mini, urh, n_cells, area_km2, area_frac, ls2d, ls2d_hs, ls2d_mb86, ls2d_dg96
  `urh` is the 2-digit code soil_family*10 + land_class used everywhere else in this
  repo (11..38, the 24 values in parameters.npz:urh_id).  `area_frac` is the URH's
  share of the minibacia's URH-valid area, so it reproduces urh_fractions.csv.
  Long format is used deliberately: a wide matrix would need NaN for absent pairs,
  which would collide with the "count any NaN" sanity gate.

Usage:  python scripts/c3/ls2d.py [--scale 1] [--chunk 512] [--no-figure]
        --scale 1 = native 90 m (default).  --scale 2 = 180 m fallback if RAM is tight;
        the minibacia/URH grid is 8x coarser than the 90 m DEM, so --scale must divide 8.

References
----------
Desmet, P.J.J. & Govers, G. (1996). A GIS procedure for automatically calculating the
    USLE LS factor on topographically complex landscape units. J. Soil Water Conserv.
    51(5), 427-433.
McCool, D.K., Foster, G.R., Mutchler, C.K. & Meyer, L.D. (1989). Revised slope length
    factor for the Universal Soil Loss Equation. Trans. ASAE 32(5), 1571-1576.
McCool, D.K., Brown, L.C., Foster, G.R., Mutchler, C.K. & Meyer, L.D. (1987). Revised
    slope steepness factor for the Universal Soil Loss Equation. Trans. ASAE 30(5),
    1387-1396.
Moore, I.D. & Burch, G.J. (1986). Physical basis of the length-slope factor in the
    Universal Soil Loss Equation. Soil Sci. Soc. Am. J. 50(5), 1294-1298.
Mitasova, H., Hofierka, J., Zlocha, M. & Iverson, L.R. (1996). Modelling topographic
    potential for erosion and deposition using GIS. Int. J. GIS 10(5), 629-641.
Montgomery, D.R. & Dietrich, W.E. (1988). Where do channels begin? Nature 336, 232-234;
    and (1992) Channel initiation and the problem of landscape scale. Science 255,
    826-830.  (Source-area basis for the A_CHANNEL = 1 km2 cap used by `ls2d_hs`.)
Wischmeier, W.H. & Smith, D.D. (1978). Predicting rainfall erosion losses. USDA
    Agriculture Handbook 537.
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
import tarfile
import tempfile
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.enums import Resampling as RS
from rasterio.warp import Resampling, reproject

import pyflwdir
from pyflwdir import gis_utils

# ----------------------------------------------------------------------------- constants
UNIT_PLOT_LEN_M = 22.13       # USLE unit-plot length            (Wischmeier & Smith 1978)
UNIT_PLOT_SIN = 0.0896        # sin of the 9 % unit-plot slope   (Wischmeier & Smith 1978)
N_EXP = 1.3                   # slope exponent, rill-dominated   (Moore & Burch 1986)
M_FIXED_MB86 = 0.4            # fixed m, cross-check variant     (Moore & Burch 1986)
TAN_FLOOR = 1e-4              # numerical flat-cell guard (0.01 %) - see module docstring
S_BREAK_TAN = 0.09            # McCool et al. (1987) S-factor break at 9 % slope
A_CHANNEL_M2 = 1.0e6          # channel-initiation source area, 1 km2 - upper bound of the
                              # humid/steep field range in Montgomery & Dietrich (1988, 1992);
                              # used ONLY for the `ls2d_hs` variant (see docstring)
MINIBACIA_SCALE = 8           # minibacias.tif is 1/8 of the 90 m DEM grid (nb07 SCALE=8)

URH_CODES = np.array(
    [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24,
     25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38], dtype=np.int16)
LC_TO_CLASS = {10: 1, 20: 2, 30: 3, 40: 4, 50: 5, 60: 6, 70: 6, 100: 6, 80: 7, 90: 8, 95: 8}
CLASS_NAME = {1: "Forest", 2: "Shrub", 3: "Grassland", 4: "Cropland",
              5: "Urban", 6: "Bare", 7: "Water", 8: "Wetland"}
SOIL_SHORT = {1: "Coarse", 2: "Medium", 3: "Fine"}
D8_DIAGONAL = (2, 8, 32, 128)  # SE, SW, NW, NE


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for cand in [here.parent, *here.parents]:
        if (cand / "data" / "processed").exists():
            return cand
    return Path.cwd()


# ------------------------------------------------------------------------------- inputs
def locate_dem(repo: Path) -> Path:
    """The corrected COP90 DEM nb07 uses: temp copy, else extracted from the tarball."""
    dem = Path(tempfile.gettempdir()) / "output_hh.tif"
    if not dem.exists():
        tars = sorted(glob.glob(str(repo / "data" / "raw" / "dem" / "rasters_COP90*Corr*.tar.gz")))
        if not tars:
            raise FileNotFoundError("corrected COP90 DEM tarball not found under data/raw/dem")
        log(f"extracting output_hh.tif from {Path(tars[0]).name} ...")
        with tarfile.open(tars[0]) as t:
            t.extract("output_hh.tif", path=dem.parent)
    return dem


def build_urh_coarse(repo: Path, subs: np.ndarray, dst_tr: Affine, cache: Path) -> np.ndarray:
    """URH grid on the minibacia (705x1500) grid: soil_family*10 + land_class, 0 = invalid.

    Reproduces notebook 08 cells 6/8/10 exactly (nearest for soil, mode-downsampled
    WorldCover reprojected nearest for land cover).
    """
    if cache.exists():
        urh = np.load(cache)["urh"]
        if urh.shape == subs.shape:
            log(f"URH grid loaded from cache {cache}")
            return urh
    H, W = subs.shape
    log("rebuilding the URH grid (nb08 cell 10) ...")

    lczip = glob.glob(str(repo / "data" / "raw" / "landcover" / "*.zip"))
    if not lczip:
        raise FileNotFoundError("WorldCover zip not found under data/raw/landcover")
    lczip = lczip[0]
    wc = np.zeros((H, W), "uint8")
    tiles = [n for n in zipfile.ZipFile(lczip).namelist() if n.endswith("_Map.tif")]
    for k, tn in enumerate(tiles, 1):
        with rasterio.open(f"/vsizip/{lczip}/{tn}") as src:
            f = 40
            th, tw = src.height // f, src.width // f
            arr = src.read(1, out_shape=(th, tw), resampling=RS.mode)
            st = src.transform * Affine.scale(src.width / tw, src.height / th)
        tmp = np.zeros((H, W), "uint8")
        reproject(arr, tmp, src_transform=st, src_crs="EPSG:4326",
                  dst_transform=dst_tr, dst_crs="EPSG:4326", resampling=Resampling.nearest)
        wc = np.where(tmp > 0, tmp, wc)
        log(f"  worldcover tile {k}/{len(tiles)}")
    land = np.zeros((H, W), "uint8")
    for code, cls in LC_TO_CLASS.items():
        land[wc == code] = cls
    del wc

    soil = np.zeros((H, W), "uint8")
    with rasterio.open(repo / "data" / "processed" / "soil_family_igac.tif") as src:
        reproject(rasterio.band(src, 1), soil, dst_transform=dst_tr,
                  dst_crs="EPSG:4326", resampling=Resampling.nearest)

    urh = np.where((soil > 0) & (land > 0), soil.astype("int16") * 10 + land.astype("int16"), 0)
    urh = urh.astype("int16")
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, urh=urh)
    return urh


# -------------------------------------------------------------------------- LS per cell
def slope_exponent_m(sin_theta: np.ndarray) -> np.ndarray:
    """m = beta/(1+beta), beta = (sin/0.0896)/(3 sin^0.8 + 0.56).

    McCool et al. (1989); Desmet & Govers (1996) eqs. 5-6.  Slope-dependent, not tuned.
    """
    beta_r = (sin_theta / UNIT_PLOT_SIN) / (3.0 * sin_theta ** 0.8 + 0.56)
    return beta_r / (1.0 + beta_r)


def s_factor_mccool(sin_theta: np.ndarray, tan_theta: np.ndarray) -> np.ndarray:
    """McCool et al. (1987) S factor; strictly positive (min 0.03)."""
    return np.where(tan_theta < S_BREAK_TAN,
                    10.8 * sin_theta + 0.03,
                    16.8 * sin_theta - 0.50)


def ls_variants(tan_theta: np.ndarray, upslope_area_m2: np.ndarray,
                cell_area_m2: np.ndarray, x_aspect: np.ndarray):
    """Return (ls_primary, ls_mb86, ls_dg96_finite_difference, ls_hillslope) in float64."""
    tan_theta = np.maximum(tan_theta, TAN_FLOOR)
    sin_theta = tan_theta / np.sqrt(1.0 + tan_theta * tan_theta)

    d_cell = np.sqrt(cell_area_m2)                       # effective square cell size D [m]
    a_in = np.maximum(upslope_area_m2 - cell_area_m2, 0.0)   # area entering the cell
    a_unit = (a_in + cell_area_m2) / d_cell              # unit contributing area [m]

    m = slope_exponent_m(sin_theta)
    slope_term = (sin_theta / UNIT_PLOT_SIN) ** N_EXP

    ls1 = (m + 1.0) * (a_unit / UNIT_PLOT_LEN_M) ** m * slope_term
    ls2 = (M_FIXED_MB86 + 1.0) * (a_unit / UNIT_PLOT_LEN_M) ** M_FIXED_MB86 * slope_term

    # hillslope-limited variant: the SAME eq. (1) with the SAME constants, but the upslope
    # area is not allowed past the channel-initiation source area, so the relation is never
    # extrapolated into a river channel where USLE/RUSLE does not apply.
    a_unit_hs = np.minimum(upslope_area_m2, A_CHANNEL_M2) / d_cell
    ls4 = (m + 1.0) * (a_unit_hs / UNIT_PLOT_LEN_M) ** m * slope_term

    # Desmet & Govers (1996) eq. 11 (finite difference) x McCool (1987) S, eq. (3)
    mp1 = m + 1.0
    l_dg = ((a_in + cell_area_m2) ** mp1 - a_in ** mp1) / (
        d_cell ** (m + 2.0) * x_aspect ** m * UNIT_PLOT_LEN_M ** m)
    ls3 = l_dg * s_factor_mccool(sin_theta, tan_theta)
    return ls1, ls2, ls3, ls4


# ---------------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scale", type=int, default=1,
                    help="DEM down-sampling; 1 = native 90 m. Must divide 8.")
    ap.add_argument("--chunk", type=int, default=512, help="rows per processing chunk")
    ap.add_argument("--no-figure", action="store_true")
    args = ap.parse_args()
    if MINIBACIA_SCALE % args.scale != 0:
        raise SystemExit("--scale must divide 8 (the minibacia grid is 1/8 of the 90 m DEM)")
    ratio = MINIBACIA_SCALE // args.scale

    repo = repo_root()
    proc = repo / "data" / "processed"
    scratch = Path(os.environ.get("LS2D_CACHE", Path(tempfile.gettempdir()) / "ls2d_cache"))

    # ---- minibacia + URH grids (coarse, 705x1500)
    with rasterio.open(proc / "minibacias.tif") as ds:
        subs = ds.read(1)
        dst_tr = ds.transform
        cb = ds.bounds
    Hc, Wc = subs.shape
    mini_ids = np.unique(subs[subs > 0])
    log(f"minibacias.tif {Hc}x{Wc} | {mini_ids.size} minibacias")
    urh_coarse = build_urh_coarse(repo, subs, dst_tr, scratch / "urh_coarse.npz")

    # ---- DEM
    dem_path = locate_dem(repo)
    with rasterio.open(dem_path) as ds:
        H, W = ds.height // args.scale, ds.width // args.scale
        elev = ds.read(1, out_shape=(H, W), resampling=RS.average).astype("float32")
        transform = ds.transform * Affine.scale(ds.width / W, ds.height / H)
        bb = ds.bounds
    if H != Hc * ratio or W != Wc * ratio:
        raise SystemExit(f"grid mismatch: DEM {H}x{W} vs minibacia {Hc}x{Wc} x {ratio}")
    NODATA = np.float32(-9999.0)
    elev[~np.isfinite(elev)] = NODATA
    elev[elev < -50] = NODATA                      # ocean / DEM voids, exactly as nb07
    log(f"DEM {H}x{W} ({elev.size/1e6:.1f} M cells) | "
        f"elev {elev[elev>NODATA].min():.0f}..{elev.max():.0f} m")

    # coarse elevation (for the Andes-vs-floodplain gate) before elev is freed
    with np.errstate(invalid="ignore"):
        tmp = np.where(elev > NODATA, elev, np.float32(np.nan))
        elev_c = np.nanmean(tmp.reshape(Hc, ratio, Wc, ratio), axis=(1, 3)).astype("float32")
    del tmp

    # ---- slope from the raw (unfilled) DEM: Horn 3x3, the standard terrain gradient
    log("slope (Horn 3x3) ...")
    tan_slope = pyflwdir.dem.slope(elev, nodata=float(NODATA), latlon=True, transform=transform)

    # ---- pit filling + D8 + flow accumulation (nb07 cells 5 and 7, recomputed)
    log("pyflwdir.from_dem (pit filling + D8) ...")
    elev_nan = np.where(elev > NODATA, elev, np.float32(np.nan))
    del elev
    flw = pyflwdir.from_dem(data=elev_nan, nodata=np.nan,
                            transform=transform, latlon=True)
    del elev_nan
    d8 = flw.to_array(ftype="d8").astype("uint8")
    log("upstream_area ...")
    upa = flw.upstream_area(unit="m2").astype("float32")
    del flw
    log(f"upstream area {np.nanmax(upa)/1e6:,.0f} km2 at the outlet")

    # ---- per-row geometry (WGS84: cell size varies with latitude only)
    xres, yres, north = transform[0], transform[4], transform[5]
    lat_row = north + (np.arange(H) + 0.5) * yres
    dx_m = np.array([abs(xres) * gis_utils.degree_metres_x(la) for la in lat_row], "float64")
    dy_m = np.array([abs(yres) * gis_utils.degree_metres_y(la) for la in lat_row], "float64")
    cell_area_row = dx_m * dy_m                                    # m2 per cell, per row

    # ---- accumulators.  key = mini_index * 25 + (urh_index + 1); slot 0 = URH-invalid
    n_mini = mini_ids.size
    id_to_idx = np.full(int(mini_ids.max()) + 1, -1, "int32")
    id_to_idx[mini_ids] = np.arange(n_mini, dtype="int32")
    urh_to_idx = np.full(int(URH_CODES.max()) + 1, -1, "int32")
    urh_to_idx[URH_CODES] = np.arange(URH_CODES.size, dtype="int32")
    nkey = n_mini * 25
    acc_w = np.zeros(nkey, "float64")
    acc_n = np.zeros(nkey, "int64")
    acc_ls1 = np.zeros(nkey, "float64")
    acc_ls2 = np.zeros(nkey, "float64")
    acc_ls3 = np.zeros(nkey, "float64")
    acc_ls4 = np.zeros(nkey, "float64")

    coarse_w = np.zeros(Hc * Wc, "float64")
    coarse_ls = np.zeros(Hc * Wc, "float64")
    coarse_hs = np.zeros(Hc * Wc, "float64")

    n_basin = int((subs > 0).sum()) * ratio * ratio
    vals = np.empty(n_basin, "float32")            # per-cell LS, for exact percentiles
    vals_hs = np.empty(n_basin, "float32")         # per-cell hillslope-limited LS
    vals_elev = np.empty(n_basin, "float32")
    vals_mi = np.empty(n_basin, "int32")           # minibacia index, for exact medians
    filled = 0
    n_flat = 0
    n_nan = 0
    nan_locs = []

    log(f"per-cell LS over {n_basin/1e6:.1f} M basin cells, {args.chunk}-row chunks ...")
    for r0 in range(0, H, args.chunk):
        r1 = min(H, r0 + args.chunk)
        nr = r1 - r0
        mini_blk = subs[r0 // ratio:(r1 + ratio - 1) // ratio]
        # expand the coarse minibacia / URH ids onto this chunk's fine rows
        rr = np.arange(r0, r1) // ratio - (r0 // ratio)
        cc = np.arange(W) // ratio
        mini_chunk = mini_blk[np.ix_(rr, cc)]
        urh_chunk = urh_coarse[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]
        elevc_chunk = elev_c[r0 // ratio:(r1 + ratio - 1) // ratio][np.ix_(rr, cc)]

        sl = tan_slope[r0:r1]
        ua = upa[r0:r1]
        valid = (mini_chunk > 0) & (sl > float(NODATA) + 1.0) & np.isfinite(sl) & (ua > 0)
        if not valid.any():
            continue

        area_col = np.repeat(cell_area_row[r0:r1][:, None], W, axis=1)
        xasp = np.where(np.isin(d8[r0:r1], D8_DIAGONAL), np.sqrt(2.0), 1.0)

        v = valid
        tan_v = sl[v].astype("float64")
        n_flat += int((tan_v < TAN_FLOOR).sum())
        ls1, ls2, ls3, ls4 = ls_variants(tan_v, ua[v].astype("float64"),
                                         area_col[v], xasp[v])

        bad = ~(np.isfinite(ls1) & np.isfinite(ls2) & np.isfinite(ls3) & np.isfinite(ls4))
        if bad.any():
            n_nan += int(bad.sum())
            rows_v, cols_v = np.nonzero(v)
            for i in np.nonzero(bad)[0][:20]:
                rr_, cc_ = int(rows_v[i]) + r0, int(cols_v[i])
                nan_locs.append((rr_, cc_,
                                 float(bb.left + (cc_ + 0.5) * abs(xres)),
                                 float(north + (rr_ + 0.5) * yres)))
            ls1 = np.nan_to_num(ls1, nan=0.0, posinf=0.0, neginf=0.0)
            ls2 = np.nan_to_num(ls2, nan=0.0, posinf=0.0, neginf=0.0)
            ls3 = np.nan_to_num(ls3, nan=0.0, posinf=0.0, neginf=0.0)
            ls4 = np.nan_to_num(ls4, nan=0.0, posinf=0.0, neginf=0.0)

        w = area_col[v]
        mi = id_to_idx[mini_chunk[v]]
        ui = urh_to_idx[np.clip(urh_chunk[v], 0, urh_to_idx.size - 1)]
        ui = np.where(urh_chunk[v] > 0, ui, -1)
        key = mi.astype("int64") * 25 + (ui + 1)
        acc_w += np.bincount(key, weights=w, minlength=nkey)
        acc_n += np.bincount(key, minlength=nkey)
        acc_ls1 += np.bincount(key, weights=ls1 * w, minlength=nkey)
        acc_ls2 += np.bincount(key, weights=ls2 * w, minlength=nkey)
        acc_ls3 += np.bincount(key, weights=ls3 * w, minlength=nkey)
        acc_ls4 += np.bincount(key, weights=ls4 * w, minlength=nkey)

        ckey = ((np.nonzero(v)[0] + r0) // ratio) * Wc + (np.nonzero(v)[1] // ratio)
        coarse_w += np.bincount(ckey, weights=w, minlength=Hc * Wc)
        coarse_ls += np.bincount(ckey, weights=ls1 * w, minlength=Hc * Wc)
        coarse_hs += np.bincount(ckey, weights=ls4 * w, minlength=Hc * Wc)

        k = ls1.size
        vals[filled:filled + k] = ls1
        vals_hs[filled:filled + k] = ls4
        vals_elev[filled:filled + k] = elevc_chunk[v]
        vals_mi[filled:filled + k] = mi
        filled += k

    vals = vals[:filled]
    vals_hs = vals_hs[:filled]
    vals_elev = vals_elev[:filled]
    vals_mi = vals_mi[:filled]
    del tan_slope, upa, d8
    log(f"per-cell pass done: {filled/1e6:.2f} M basin cells scored")

    # ------------------------------------------------------------------ sanity gates
    print("\n" + "=" * 78)
    print("SANITY GATES")
    print("=" * 78)

    finite = np.isfinite(vals) & np.isfinite(vals_hs)
    n_nonpos = int((vals[finite] <= 0).sum() + (vals_hs[finite] <= 0).sum())
    print(f"GATE 1  positivity/finiteness")
    print(f"  cells scored                : {filled:,}")
    print(f"  non-finite (NaN/inf) cells  : {n_nan}")
    if nan_locs:
        for (r_, c_, lo_, la_) in nan_locs[:10]:
            print(f"      row {r_} col {c_}  lon {lo_:.4f} lat {la_:.4f}")
    print(f"  LS <= 0 cells (both cols)   : {n_nonpos}")
    print(f"  ls2d    min / max           : {vals[finite].min():.6g} / {vals[finite].max():.6g}")
    print(f"  ls2d_hs min / max           : {vals_hs[finite].min():.6g} / "
          f"{vals_hs[finite].max():.6g}")

    pct = [1, 5, 25, 50, 75, 90, 95, 99]
    q = np.percentile(vals[finite], pct).astype(float)
    qh = np.percentile(vals_hs[finite], pct).astype(float)
    mean_area_w = float(acc_ls1.sum() / acc_w.sum())
    mean_hs = float(acc_ls4.sum() / acc_w.sum())
    print(f"\nGATE 2  basin distribution (published mountainous range ~2-10 for the median)")
    print(f"  ls2d     per-cell median    : {q[3]:.3f}   area-wtd mean {mean_area_w:.3f}")
    print(f"  ls2d_hs  per-cell median    : {qh[3]:.3f}   area-wtd mean {mean_hs:.3f}"
          f"   <-- hillslope-limited (A capped at {A_CHANNEL_M2/1e6:g} km2)")
    print("  percentiles 1/5/25/50/75/90/95/99")
    print("    ls2d   : " + "  ".join(f"{x:.3f}" for x in q))
    print("    ls2d_hs: " + "  ".join(f"{x:.3f}" for x in qh))
    m_mb86 = float(acc_ls2.sum() / acc_w.sum())
    m_dg96 = float(acc_ls3.sum() / acc_w.sum())
    print(f"  variant area-wtd means      : primary {mean_area_w:.3f} | "
          f"mb86 (m=0.4) {m_mb86:.3f} | dg96 finite-diff {m_dg96:.3f}")
    print(f"  dg96 / primary ratio        : {m_dg96/mean_area_w:.3f}"
          f"   (independent-implementation cross-check of eq. 1 vs eq. 2)")

    lo = vals_elev < 200.0
    hi = vals_elev > 1000.0
    print(f"\nGATE 3  Andean flanks vs lowland floodplain")
    print(f"  lowland  (<200 m)  n={int(lo.sum()):,}  median ls2d {np.median(vals[lo]):.3f}"
          f"  mean {vals[lo].mean():.3f}  |  ls2d_hs median {np.median(vals_hs[lo]):.3f}")
    print(f"  Andean   (>1000 m) n={int(hi.sum()):,}  median ls2d {np.median(vals[hi]):.3f}"
          f"  mean {vals[hi].mean():.3f}  |  ls2d_hs median {np.median(vals_hs[hi]):.3f}")
    print(f"  ratio of medians (Andes/lowland): ls2d "
          f"{np.median(vals[hi])/max(np.median(vals[lo]),1e-9):.1f}x   ls2d_hs "
          f"{np.median(vals_hs[hi])/max(np.median(vals_hs[lo]),1e-9):.1f}x")

    print(f"\nGATE 4  flat-cell handling")
    print(f"  slope floored at tan(beta)  : {TAN_FLOOR:g} (0.01 %)")
    print(f"  cells hitting the floor     : {n_flat:,} ({100*n_flat/filled:.3f} % of basin)")
    print(f"  LS at the floor             : {(1+0)*1.0*(TAN_FLOOR/UNIT_PLOT_SIN)**N_EXP:.3e} "
          f"(x the area term, ~1 on a flat) -> strictly positive, never 0, never NaN")
    print("=" * 78 + "\n")

    # ------------------------------------------------------------------ aggregation out
    A = acc_w.reshape(n_mini, 25)
    N = acc_n.reshape(n_mini, 25)
    L1 = acc_ls1.reshape(n_mini, 25)
    L2 = acc_ls2.reshape(n_mini, 25)
    L3 = acc_ls3.reshape(n_mini, 25)
    L4 = acc_ls4.reshape(n_mini, 25)

    tot_a = A.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        mini_tab = pd.DataFrame({
            "id": mini_ids.astype("int32"),
            "n_cells": N.sum(1),
            "area_km2_cells": tot_a / 1e6,
            "ls2d": L1.sum(1) / tot_a,
            "ls2d_hs": L4.sum(1) / tot_a,
            "ls2d_mb86": L2.sum(1) / tot_a,
            "ls2d_dg96": L3.sum(1) / tot_a,
            "urh_cover_frac": A[:, 1:].sum(1) / tot_a,
        })

    # exact per-minibacia median / p90 of the per-CELL values (not of coarse means):
    # sort the 90 m values by minibacia index once, then slice.
    log("exact per-minibacia percentiles ...")
    coarse_mean = np.divide(coarse_ls, coarse_w,
                            out=np.zeros_like(coarse_ls), where=coarse_w > 0)
    coarse_mean_hs = np.divide(coarse_hs, coarse_w,
                               out=np.zeros_like(coarse_hs), where=coarse_w > 0)
    order = np.argsort(vals_mi, kind="stable")
    mi_sorted = vals_mi[order]
    v_sorted = vals[order]
    del order
    bounds = np.searchsorted(mi_sorted, np.arange(n_mini + 1))
    med = np.full(n_mini, np.nan)
    p90 = np.full(n_mini, np.nan)
    for i in range(n_mini):
        seg = v_sorted[bounds[i]:bounds[i + 1]]
        if seg.size:
            seg = np.sort(seg)
            med[i] = seg[(seg.size - 1) // 2] if seg.size % 2 else \
                0.5 * (seg[seg.size // 2 - 1] + seg[seg.size // 2])
            p90[i] = seg[min(seg.size - 1, int(0.9 * (seg.size - 1)))]
    del mi_sorted, v_sorted
    mini_tab["ls2d_median"] = med
    mini_tab["ls2d_p90"] = p90
    mini_tab = mini_tab[["id", "n_cells", "area_km2_cells", "ls2d", "ls2d_hs",
                         "ls2d_median", "ls2d_p90", "ls2d_mb86", "ls2d_dg96",
                         "urh_cover_frac"]]
    out_mini = proc / "minibacia_ls2d.csv"
    mini_tab.to_csv(out_mini, index=False, float_format="%.6g")
    log(f"wrote {out_mini}  ({len(mini_tab)} rows)")

    mi_idx, ui_slot = np.nonzero(N[:, 1:] > 0)
    urh_area = A[:, 1:][mi_idx, ui_slot]
    urh_tab = pd.DataFrame({
        "mini": mini_ids[mi_idx].astype("int32"),
        "urh": URH_CODES[ui_slot],
        "n_cells": N[:, 1:][mi_idx, ui_slot],
        "area_km2": urh_area / 1e6,
        "area_frac": urh_area / A[:, 1:].sum(1)[mi_idx],
        "ls2d": L1[:, 1:][mi_idx, ui_slot] / urh_area,
        "ls2d_hs": L4[:, 1:][mi_idx, ui_slot] / urh_area,
        "ls2d_mb86": L2[:, 1:][mi_idx, ui_slot] / urh_area,
        "ls2d_dg96": L3[:, 1:][mi_idx, ui_slot] / urh_area,
    }).sort_values(["mini", "urh"])
    out_urh = proc / "urh_ls2d.csv"
    urh_tab.to_csv(out_urh, index=False, float_format="%.6g")
    log(f"wrote {out_urh}  ({len(urh_tab)} rows, "
        f"{urh_tab.mini.nunique()} minibacias x up to 24 URH)")

    print("basin-wide area-weighted LS2D by URH class:")
    g = urh_tab.assign(_w=urh_tab.area_km2)
    bas = (g.assign(_x=g.ls2d * g._w, _y=g.ls2d_hs * g._w)
             .groupby("urh")[["_x", "_y", "_w"]].sum())
    bas["ls2d"] = bas._x / bas._w
    bas["ls2d_hs"] = bas._y / bas._w
    bas["basin_pct"] = 100 * bas._w / bas._w.sum()
    for code, row in bas.sort_values("ls2d_hs", ascending=False).iterrows():
        print(f"  {code:>3d} {SOIL_SHORT[code//10]:>6s} x {CLASS_NAME[code%10]:<10s} "
              f"ls2d {row.ls2d:8.3f}  ls2d_hs {row.ls2d_hs:6.3f}   "
              f"{row.basin_pct:5.2f} % of basin")

    # ------------------------------------------------------------------------- figure
    if not args.no_figure:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import LogNorm

        msk = coarse_w.reshape(Hc, Wc) > 0
        map_raw = np.where(msk, coarse_mean.reshape(Hc, Wc), np.nan)
        map_hs = np.where(msk, coarse_mean_hs.reshape(Hc, Wc), np.nan)
        ext = [cb.left, cb.right, cb.bottom, cb.top]

        fig = plt.figure(figsize=(15.5, 8.6))
        gs = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.0, 1.45],
                              wspace=0.30, hspace=0.32)

        for col, (arr, name, note) in enumerate([
                (map_raw, "ls2d  (uncapped, literal eq. 1)",
                 "channels included → USLE extrapolated far past the 22.13 m plot"),
                (map_hs, f"ls2d_hs  (A capped at {A_CHANNEL_M2/1e6:g} km²)",
                 "hillslope-limited: the column MUSLE should use")]):
            ax = fig.add_subplot(gs[:, col])
            im = ax.imshow(arr, extent=ext, cmap="magma_r", interpolation="none",
                           norm=LogNorm(vmin=max(np.nanpercentile(arr, 2), 1e-3),
                                        vmax=np.nanpercentile(arr, 99.5)))
            cbar = plt.colorbar(im, ax=ax, shrink=0.72, pad=0.02)
            cbar.set_label("LS2D (–), log colour scale", fontsize=8)
            cbar.ax.tick_params(labelsize=7)
            ax.set_title(f"{name}\n{note}", fontsize=9)
            ax.set_xlabel("lon", fontsize=8); ax.set_ylabel("lat", fontsize=8)
            ax.tick_params(labelsize=7)

        ax2 = fig.add_subplot(gs[0, 2])
        bins = np.linspace(-4, 5, 220)
        ax2.hist(np.log10(np.clip(vals[finite], 1e-6, None)), bins=bins,
                 color="#5B3A8E", alpha=0.60, label=f"ls2d (median {q[3]:.2f})")
        ax2.hist(np.log10(np.clip(vals_hs[finite], 1e-6, None)), bins=bins,
                 color="#1C7293", alpha=0.60, label=f"ls2d_hs (median {qh[3]:.2f})")
        ax2.axvspan(np.log10(2), np.log10(10), color="#8FBF6F", alpha=0.22,
                    label="published mountainous range 2–10")
        ax2.axvline(np.log10(max(q[3], 1e-6)), color="#5B3A8E", lw=1.6)
        ax2.axvline(np.log10(max(qh[3], 1e-6)), color="#1C7293", lw=1.6)
        ax2.set_xlabel(f"log10 LS2D (per {args.scale*90} m cell)", fontsize=8)
        ax2.set_ylabel("cells", fontsize=8)
        ax2.set_title(f"distribution over {filled/1e6:.1f} M basin cells — "
                      f"0 NaN, 0 non-positive", fontsize=9)
        ax2.legend(fontsize=7.5, loc="upper left")
        ax2.tick_params(labelsize=7)

        ax3 = fig.add_subplot(gs[1, 2])
        ax3.hist(np.log10(np.clip(vals_hs[lo], 1e-6, None)), bins=bins, density=True,
                 alpha=0.65, color="#3D6FB0",
                 label=f"lowland <200 m (median {np.median(vals_hs[lo]):.2f})")
        ax3.hist(np.log10(np.clip(vals_hs[hi], 1e-6, None)), bins=bins, density=True,
                 alpha=0.65, color="#B0412B",
                 label=f"Andean >1000 m (median {np.median(vals_hs[hi]):.2f})")
        ax3.set_xlim(-4, 2.5)
        ax3.set_xlabel("log10 ls2d_hs", fontsize=8); ax3.set_ylabel("density", fontsize=8)
        ax3.set_title("gate 3 — Andean flanks vs lowland floodplain "
                      f"({np.median(vals_hs[hi])/max(np.median(vals_hs[lo]),1e-9):.0f}× "
                      "in the median)", fontsize=9)
        ax3.legend(fontsize=7.5)
        ax3.tick_params(labelsize=7)

        fig.suptitle("C3.1 — LS2D topographic factor for MUSLE   "
                     f"(unit contributing area, m = McCool 1989 slope-dependent, "
                     f"n = {N_EXP} Moore & Burch 1986; {args.scale*90} m cells)",
                     fontsize=11.5)
        out_fig = repo / "figures" / "deck" / "gen_ls2d.png"
        out_fig.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_fig, dpi=145, bbox_inches="tight")
        log(f"wrote {out_fig}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

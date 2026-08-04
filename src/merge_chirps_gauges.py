"""CHIRPS-gauge merged rainfall field (v3 candidate), with its own decision gates.

WHAT THIS BUILDS
----------------
A merged daily rainfall field at the 8,672 minibacia centroids, 2008-2018:

  * gauge IDW (the nb11/v2 scheme, via src/idw_forcing.py) where gauges are close;
  * CHIRPS, quantile-mapped TO the gauge distribution per (elevation band x hydrographic
    zone) stratum, blended in by distance-to-nearest-gauge weight;
  * pure mapped CHIRPS in the k=6-silent fallback cells (41,180 minibacia-days in v2).

Direction of the quantile map is deliberate and measured (doc 18 s9.4/s9.5): on the
like-for-like 2009-2017 window the v2 gauge field is 2,036.4 mm/yr and CHIRPS is 2,124.9,
so a naive blend ADDS water and undoes the zero-suppression repair. Mapping CHIRPS onto
the gauge distribution keeps gauges in control of volume; CHIRPS supplies spatial
structure and gap-fill only.

CHIRPS is lag-aligned by -1 day before any use (nb10 day-convention test: the gauge
`dia pluviometrico` runs 07:00->07:00, and shifting CHIRPS so that the value stamped
day tau pairs with gauge day tau-1 raises median daily r from 0.16 to 0.31).

TRAP 8 (doc 18 s9.5): chirps_basin_*.nc is a BOUNDING BOX despite the name (+14.1 %
unmasked). Nothing here ever averages the box: CHIRPS is only ever sampled at minibacia
centroids and gauge pixels, and the basin mean is area-weighted over minibacias.

DECISION GATES (pre-registered in docs/agents/journal_chirps-merge.md BEFORE this ran)
--------------------------------------------------------------------------------------
  VOLUME GATE : area-weighted basin mean of the merged field, 2009-2017 window, within
                1 % of the v2 gauge-only 2,036.4 mm/yr.
  LOOCV GATE  : notebook 11 section-6 protocol EXACTLY (k=6 argsort neighbour set,
                weights 1/max(d,1)^2, masked by reporting, >=300 scored days, daily r).
                The script first REPRODUCES the gauge-only baseline (must give median
                r 0.429 over 287 gauges) and then scores the merged estimate rebuilt at
                each gauge's location WITHOUT that gauge - including refitting the
                quantile map with that gauge's paired days excluded from every pool.
  ADOPT only if merged median r > 0.429 by any margin AND the volume gate holds.
  Adoption is justified by r, never by volume (doc 22 s4.7).

Outputs: always data/processed/merge_loocv_report.csv (per-gauge scores).
If adopted, additionally forcing_minibacia_precip_v3.csv + the .npy trio (via
src/forcing_npy.py, which re-verifies the CSV against its own byte counts) +
forcing_minibacia_provenance_v3.csv. Never overwrites v2.

Run:  python src/merge_chirps_gauges.py
"""
from __future__ import annotations

import os
import pathlib
import sys

import numpy as np
import pandas as pd
import rasterio
import xarray as xr
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import forcing_npy
import idw_forcing as idwf

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"
CLIM = REPO / "data" / "raw" / "climate"
# COP90 hydrologically-conditioned DEM, full basin rectangle, 8x finer than minibacias.tif.
# Regenerable from data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz.
DEM_PATH = pathlib.Path(os.environ.get(
    "COP90_DEM", r"C:\Users\knade.MSI_TWILL\AppData\Local\Temp\output_hh.tif"))

YEARS = list(range(2008, 2019))
LAG = -1                      # nb10 best alignment: aligned(t) = chirps_raw(t + 1)
ELEV_BANDS = (500.0, 1500.0, 2500.0)      # m -> 4 bands
D_FULL_GAUGE_KM = 10.0        # w_chirps = 0 at/below this distance to nearest gauge
D_FULL_CHIRPS_KM = 30.0       # w_chirps = 1 at/beyond (matches the G/GC/C provenance bands)
N_KNOTS = 1001
MIN_GAUGES = 3                # minimum gauges in a quantile-map pool
MIN_PAIRS = 5000              # minimum paired station-days in a pool
MIN_SCORED_DAYS = 300         # nb11 s6 evaluation threshold
BASELINE_MEDIAN_R = 0.429     # nb11 s6, 287 gauges - reproduced below as a self-check
VOLUME_TARGET = 2036.4        # v2 gauge-only, area-weighted, 2009-2017
VOLUME_TOL = 0.01


def chirps_weight(d_km: np.ndarray) -> np.ndarray:
    """Blend weight for mapped CHIRPS as a function of distance to the nearest gauge."""
    return np.clip((np.asarray(d_km, float) - D_FULL_GAUGE_KM)
                   / (D_FULL_CHIRPS_KM - D_FULL_GAUGE_KM), 0.0, 1.0)


def load_gauges():
    """The nb11 gauge set: QC v2 daily + inventory, co-located clusters merged."""
    inv = (pd.read_csv(PROC / "precip_gauges_inventory_qc.csv", dtype={"code": str})
             .dropna(subset=["lat", "lon"]).reset_index(drop=True))
    daily = (pd.read_csv(PROC / "precip_gauges_daily_qc_v2.csv", dtype={"code": str})
               .dropna(subset=["precip_mm"]))
    daily["date"] = pd.to_datetime(daily["date"])
    cls = idwf.classify_colocated(inv, daily)
    daily, inv, _ = idwf.merge_colocated(daily, inv, cls)
    inv = inv.reset_index(drop=True)
    dates = pd.date_range(daily.date.min(), daily.date.max(), freq="D")
    W = (daily.pivot_table(index="date", columns="code", values="precip_mm")
              .reindex(columns=inv.code.values).reindex(dates))
    print(f"gauges: {len(inv)}  matrix {W.shape[0]} days x {W.shape[1]} gauges  "
          f"{dates.min().date()}..{dates.max().date()}")
    return W, inv, dates


def load_centroids() -> pd.DataFrame:
    """Minibacia centroids and areas - nb11's own on-disk artefact."""
    cent = pd.read_csv(PROC / "forcing_minibacia_provenance_v2.csv")[
        ["id", "lon", "lat", "area_km2"]]
    assert len(cent) == 8672, f"expected 8672 centroids, got {len(cent)}"
    return cent


def coarse_dem() -> tuple[np.ndarray, rasterio.Affine]:
    """COP90 DEM block-reduced 8x onto the minibacias.tif grid (valid-aware mean)."""
    with rasterio.open(DEM_PATH) as s:
        dem = s.read(1)
    with rasterio.open(PROC / "minibacias.tif") as s:
        lab_shape, tr = s.shape, s.transform
    f0, f1 = dem.shape[0] // lab_shape[0], dem.shape[1] // lab_shape[1]
    assert (f0, f1) == (8, 8), f"DEM is not 8x the label grid: {dem.shape} vs {lab_shape}"
    valid = np.isfinite(dem) & (dem > -100.0)
    s4 = np.where(valid, dem, 0.0).reshape(lab_shape[0], 8, lab_shape[1], 8).sum((1, 3))
    c4 = valid.reshape(lab_shape[0], 8, lab_shape[1], 8).sum((1, 3))
    with np.errstate(invalid="ignore", divide="ignore"):
        demc = np.where(c4 > 0, s4 / c4, np.nan).astype("float32")
    del dem, valid, s4, c4
    return demc, tr


def minibacia_elevation(cent: pd.DataFrame, demc: np.ndarray) -> np.ndarray:
    """Label-mean elevation per minibacia from the coarse DEM."""
    with rasterio.open(PROC / "minibacias.tif") as s:
        lab = s.read(1)
    ok = ~np.isnan(demc)
    dsum = ndimage.sum(np.where(ok, demc, 0.0), lab, cent.id.values)
    dcnt = ndimage.sum(ok.astype("float32"), lab, cent.id.values)
    with np.errstate(invalid="ignore", divide="ignore"):
        elev = np.where(dcnt > 0, dsum / dcnt, np.nan)
    n_nan = int(np.isnan(elev).sum())
    if n_nan:
        print(f"  WARNING {n_nan} minibacias with no valid DEM cell -> elevation NaN")
    return elev.astype("float32")


def sample_grid(vals: np.ndarray, tr: rasterio.Affine,
                lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """Nearest-cell sample of a north-up grid at points."""
    col = np.clip(((lon - tr.c) / tr.a).astype(int), 0, vals.shape[1] - 1)
    row = np.clip(((lat - tr.f) / tr.e).astype(int), 0, vals.shape[0] - 1)
    return vals[row, col]


def assign_zones(inv: pd.DataFrame, cent: pd.DataFrame) -> tuple[pd.Series, np.ndarray]:
    """Hydrographic zone per gauge (inventory, gaps from nearest zoned gauge) and per
    minibacia (zone of the nearest gauge, deterministic tie-break on gauge code)."""
    zona = inv.zona.copy()
    has = zona.notna().to_numpy()
    if (~has).any():
        Dg = idwf.km(inv.lat.values[:, None], inv.lon.values[:, None],
                     inv.lat.values[None, :], inv.lon.values[None, :])
        np.fill_diagonal(Dg, np.inf)
        Dg[:, ~has] = np.inf
        order = idwf.neighbour_order(Dg, list(inv.code.values))
        zona.loc[~has] = zona.to_numpy()[order[~has, 0]]
    D = idwf.km(cent.lat.values[:, None], cent.lon.values[:, None],
                inv.lat.values[None, :], inv.lon.values[None, :])
    nearest = idwf.neighbour_order(D, list(inv.code.values))[:, 0]
    return zona, zona.to_numpy()[nearest]


def load_chirps(dates: pd.DatetimeIndex, lat_pts: np.ndarray,
                lon_pts: np.ndarray) -> np.ndarray:
    """CHIRPS 2008-2018 sampled at points (nearest cell), lag-aligned to the gauge day.

    Only point samples ever leave this function - the bounding-box mean is never taken
    (trap 8). Negative sentinel values become NaN. Returns (n_days, n_points) float32.
    """
    blocks, tindex = [], []
    iy = ix = None
    for y in YEARS:
        f = CLIM / f"chirps_basin_{y}.nc"
        with xr.open_dataset(f) as d:
            t = pd.to_datetime(d.time.values)
            want = pd.date_range(f"{y}-01-01", f"{y}-12-31", freq="D")
            assert len(t) == len(want) and (t == want).all(), \
                f"{f.name}: time axis is not the full calendar year"
            if iy is None:
                iy = np.abs(d.latitude.values[None, :] - lat_pts[:, None]).argmin(1)
                ix = np.abs(d.longitude.values[None, :] - lon_pts[:, None]).argmin(1)
            v = d["precip"].values          # (days, lat, lon)
            assert np.isfinite(v[v > -1e30]).all(), f"{f.name}: non-finite payload"
        pts = v[:, iy, ix].astype("float32")
        pts[pts < 0] = np.nan
        assert np.nanmax(pts) < 500.0, f"{f.name}: max {np.nanmax(pts):.1f} mm/day"
        blocks.append(pts)
        tindex.append(want)
        del v
    C = np.vstack(blocks)
    tall = tindex[0].append(tindex[1:])
    assert tall.equals(dates), "CHIRPS calendar does not match the gauge calendar"
    # lag -1: the CHIRPS value stamped t+1 belongs to gauge day t (dia pluviometrico)
    C = np.vstack([C[1:], C[-1:]])
    n_nan = int(np.isnan(C).sum())
    print(f"CHIRPS sampled: {C.shape[0]} days x {C.shape[1]} points  "
          f"NaN {n_nan} ({100*n_nan/C.size:.4f} %)  lag {LAG:+d} applied")
    return C


# ---------------------------------------------------------------- quantile maps
def fit_qmap(g_pool: np.ndarray, c_pool: np.ndarray):
    """Empirical quantile map CHIRPS -> gauge: (chirps_knots, gauge_knots)."""
    q = np.linspace(0.0, 1.0, N_KNOTS)
    ck = np.quantile(c_pool, q)
    gk = np.quantile(g_pool, q)
    # np.interp needs increasing x: collapse tied CHIRPS knots to the mean gauge knot
    uniq, start = np.unique(ck, return_index=True)
    gm = np.add.reduceat(gk, start) / np.diff(np.append(start, len(ck)))
    return uniq.astype("float64"), gm.astype("float64")


def apply_qmap(x: np.ndarray, qmap) -> np.ndarray:
    """Map CHIRPS values through the fitted knots; scale the above-max tail."""
    ck, gk = qmap
    y = np.interp(x, ck, gk)
    if ck[-1] > 0:
        hi = x > ck[-1]
        if hi.any():
            y = np.where(hi, x * (gk[-1] / ck[-1]), y)
    return np.where(np.isnan(x), np.nan, y).astype("float32")


class QmapPools:
    """Per-stratum paired samples with a fallback hierarchy and holdout support."""

    def __init__(self, inv, band_g, zone_g, Gv, obs, C_gauge):
        self.members: dict[object, list[str]] = {}
        self.pairs: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        for j, code in enumerate(inv.code.values):
            m = obs[:, j] & ~np.isnan(C_gauge[:, j])
            self.pairs[code] = (Gv[m, j].astype("float64"),
                                C_gauge[m, j].astype("float64"))
            for key in [("bz", band_g[j], zone_g[j]), ("z", zone_g[j]),
                        ("b", band_g[j]), ("all",)]:
                self.members.setdefault(key, []).append(code)
        self._cache: dict = {}

    def levels(self, band: int, zone: str) -> list:
        return [("bz", band, zone), ("z", zone), ("b", band), ("all",)]

    def fit(self, band: int, zone: str, exclude: str | None = None):
        """First pool down the hierarchy with >= MIN_GAUGES gauges and MIN_PAIRS pairs
        after excluding the held-out gauge; returns (qmap, level_used)."""
        for key in self.levels(band, zone):
            codes = [c for c in self.members.get(key, []) if c != exclude]
            n_pairs = sum(len(self.pairs[c][0]) for c in codes)
            if len(codes) >= MIN_GAUGES and n_pairs >= MIN_PAIRS:
                ck = (key, exclude)
                if ck not in self._cache:
                    g = np.concatenate([self.pairs[c][0] for c in codes])
                    c = np.concatenate([self.pairs[c][1] for c in codes])
                    self._cache[ck] = fit_qmap(g, c)
                return self._cache[ck], key
        raise RuntimeError(f"no pool satisfies minima for band={band} zone={zone}")


# ---------------------------------------------------------------- LOOCV
def loocv(inv, Gv, obs, Dg, C_gauge, band_g, zone_g, pools) -> pd.DataFrame:
    """nb11 section-6 protocol, gauge-only baseline AND merged, per gauge."""
    Gf = np.where(obs, Gv, 0.0).astype("float32")
    gn = np.argsort(Dg, axis=1)[:, :6]                 # nb11 s6 verbatim
    gdk = np.take_along_axis(Dg, gn, 1)
    gW = (1.0 / np.maximum(gdk, 1.0) ** 2).astype("float32")
    rows = []
    for j in range(len(inv)):
        num = (Gf[:, gn[j]] * gW[j]).sum(1)
        den = (obs[:, gn[j]] * gW[j]).sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            pred = np.where(den > 0, num / den, np.nan)
        base_m = obs[:, j] & ~np.isnan(pred)
        d_j = float(gdk[j, 0])
        w_j = float(chirps_weight(np.array([d_j]))[0])
        qmap, level = pools.fit(band_g[j], zone_g[j], exclude=inv.code.iloc[j])
        cmap = apply_qmap(C_gauge[:, j], qmap)
        merged = np.where(np.isnan(pred), cmap, w_j * cmap + (1.0 - w_j) * pred)
        merged = np.where(np.isnan(merged), pred, merged)
        mm = obs[:, j] & ~np.isnan(merged)
        row = dict(code=inv.code.iloc[j], d_nearest_km=d_j, w_chirps=w_j,
                   band=int(band_g[j]), zone=zone_g[j], qmap_level=str(level),
                   n_base=int(base_m.sum()), n_merged=int(mm.sum()),
                   r_base=np.nan, bias_base_pct=np.nan, r_merged=np.nan,
                   bias_merged_pct=np.nan, r_merged_commonmask=np.nan)
        if base_m.sum() >= MIN_SCORED_DAYS:
            o, p = Gv[base_m, j], pred[base_m]
            row["r_base"] = float(np.corrcoef(o, p)[0, 1])
            row["bias_base_pct"] = 100 * (p.sum() / o.sum() - 1) if o.sum() > 0 else np.nan
        if mm.sum() >= MIN_SCORED_DAYS:
            o, p = Gv[mm, j], merged[mm]
            row["r_merged"] = float(np.corrcoef(o, p)[0, 1])
            row["bias_merged_pct"] = 100 * (p.sum() / o.sum() - 1) if o.sum() > 0 else np.nan
        both = base_m & ~np.isnan(merged)
        if both.sum() >= MIN_SCORED_DAYS:
            row["r_merged_commonmask"] = float(
                np.corrcoef(Gv[both, j], merged[both])[0, 1])
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- merged field
def build_merged_field(W, inv, cent, C_mb, band_mb, zone_mb, pools):
    """Full-basin merged field. Returns (merged, gap_mask, d_nearest, w)."""
    idwf.assert_order_invariant(W, inv.lat.values, inv.lon.values,
                                cent.lat.values, cent.lon.values, n_shuffle=2)
    print("order-invariance: 2 gauge-column shuffles, byte-identical field each time")
    P, n_gap, gap, dk6 = idwf.idw_field(W, inv.lat.values, inv.lon.values,
                                        cent.lat.values, cent.lon.values,
                                        return_detail=True)
    print(f"gauge IDW: {P.shape[0]} days x {P.shape[1]} minibacias, "
          f"k=6-silent fallback cells {n_gap:,}")
    d_near = dk6[:, 0]
    w = chirps_weight(d_near).astype("float32")

    # quantile-map CHIRPS in place, one stratum at a time
    strata = {}
    for i in range(len(cent)):
        strata.setdefault((band_mb[i], zone_mb[i]), []).append(i)
    for (b, z), cols in sorted(strata.items(), key=lambda kv: str(kv[0])):
        qmap, level = pools.fit(b, z)
        cols = np.asarray(cols)
        C_mb[:, cols] = apply_qmap(C_mb[:, cols], qmap)
        print(f"  stratum band={b} zone={z!s:<34} minibacias {len(cols):>5}  "
              f"pool={level}")

    # blend: chirps where the k=6 pass was silent, else the distance-weighted mix;
    # wherever CHIRPS itself is missing keep the gauge value (incl. its k=20 fill)
    n = C_mb.shape[1]
    n_chirps_fill = 0
    for a in range(0, n, 1024):
        b_ = min(a + 1024, n)
        Cb, Pb, gb, wb = C_mb[:, a:b_], P[:, a:b_], gap[:, a:b_], w[a:b_][None, :]
        mix = wb * Cb + (1.0 - wb) * Pb
        out = np.where(gb, Cb, mix)
        cnan = np.isnan(Cb)
        n_chirps_fill += int((gb & ~cnan).sum())
        C_mb[:, a:b_] = np.where(cnan, Pb, out)
    assert not np.isnan(C_mb).any(), "merged field contains NaN"
    print(f"merged field complete; fallback cells filled by mapped CHIRPS: "
          f"{n_chirps_fill:,} of {n_gap:,}")
    return C_mb, gap, d_near, w


def areal_mean(field: np.ndarray, dates: pd.DatetimeIndex, area: np.ndarray,
               y0: int, y1: int) -> float:
    """Area-weighted basin mean, mm/yr, over calendar years y0..y1 (nb11's formula)."""
    m = (dates.year >= y0) & (dates.year <= y1)
    return float((field[m] * area).sum() / (m.sum() * area.sum()) * 365.25)


def main() -> None:
    W, inv, dates = load_gauges()
    cent = load_centroids()

    demc, tr = coarse_dem()
    elev_mb = minibacia_elevation(cent, demc)
    elev_g = sample_grid(demc, tr, inv.lat.values, inv.lon.values)
    miss = ~np.isfinite(elev_g)
    if miss.any():
        elev_g = np.where(miss, inv.alt.fillna(0.0).to_numpy(float), elev_g)
        print(f"  gauge elevation: {int(miss.sum())} filled from inventory alt")
    del demc
    band_g = np.digitize(elev_g, ELEV_BANDS)
    band_mb = np.digitize(np.nan_to_num(elev_mb, nan=0.0), ELEV_BANDS)
    zona_g, zone_mb = assign_zones(inv, cent)
    zone_g = zona_g.to_numpy()
    print(f"elevation bands (gauges)     : {np.bincount(band_g, minlength=4)}")
    print(f"elevation bands (minibacias) : {np.bincount(band_mb, minlength=4)}")

    n_mb = len(cent)
    C_all = load_chirps(dates,
                        np.concatenate([cent.lat.values, inv.lat.values]),
                        np.concatenate([cent.lon.values, inv.lon.values]))
    C_mb, C_gauge = C_all[:, :n_mb], C_all[:, n_mb:].copy()
    del C_all

    Gv = W.to_numpy("float32")
    obs = ~np.isnan(Gv)
    Dg = idwf.km(inv.lat.values[:, None], inv.lon.values[:, None],
                 inv.lat.values[None, :], inv.lon.values[None, :])
    np.fill_diagonal(Dg, np.inf)
    pools = QmapPools(inv, band_g, zone_g, Gv, obs, C_gauge)

    # ---- LOOCV gate ------------------------------------------------------------
    rep = loocv(inv, Gv, obs, Dg, C_gauge, band_g, zone_g, pools)
    ev = rep[rep.n_base >= MIN_SCORED_DAYS].copy()
    med_base = float(ev.r_base.median())
    med_merged = float(ev.r_merged.median())
    med_common = float(ev.r_merged_commonmask.median())
    print(f"\nLOOCV evaluation gauges: {len(ev)} (expected 287)")
    print(f"  gauge-only baseline median daily r : {med_base:.3f} "
          f"(published nb11 figure {BASELINE_MEDIAN_R})")
    assert abs(med_base - BASELINE_MEDIAN_R) < 6e-4, (
        f"baseline self-check FAILED: {med_base:.4f} != {BASELINE_MEDIAN_R} "
        "- protocol drift, the comparison is void")
    print(f"  merged median daily r              : {med_merged:.3f}")
    print(f"  merged, baseline-mask only         : {med_common:.3f}")
    for name, grp in ev.groupby(pd.cut(ev.d_nearest_km, [0, 10, 30, 1e9],
                                       labels=["<10 km", "10-30 km", ">30 km"]),
                                observed=True):
        print(f"    {name:<9} n={len(grp):>3}  r_base {grp.r_base.median():.3f}  "
              f"r_merged {grp.r_merged.median():.3f}")

    # ---- volume gate -----------------------------------------------------------
    area = cent.area_km2.to_numpy(float)
    merged, gap, d_near, w = build_merged_field(W, inv, cent, C_mb, band_mb,
                                                zone_mb, pools)
    vol = areal_mean(merged, dates, area, 2009, 2017)
    vol_full = areal_mean(merged, dates, area, 2008, 2018)
    vol_ok = abs(vol / VOLUME_TARGET - 1.0) <= VOLUME_TOL
    print(f"\nVOLUME GATE: merged area-weighted basin mean")
    print(f"  2009-2017 (the gate window)  : {vol:.1f} mm/yr  "
          f"target {VOLUME_TARGET} +/-1% -> {'PASS' if vol_ok else 'FAIL'}")
    print(f"  2008-2018 (context, trap 9)  : {vol_full:.1f} mm/yr")

    adopt = (med_merged > BASELINE_MEDIAN_R) and vol_ok
    print(f"\nDECISION (pre-registered rule: adopt if merged median r > "
          f"{BASELINE_MEDIAN_R} by any margin AND volume within 1%):")
    print(f"  merged r {med_merged:.3f} vs {BASELINE_MEDIAN_R} -> "
          f"{'wins' if med_merged > BASELINE_MEDIAN_R else 'does NOT win'}; "
          f"volume {'holds' if vol_ok else 'fails'}")
    print(f"  => {'ADOPT v3' if adopt else 'DO NOT ADOPT'}")

    rep.to_csv(PROC / "merge_loocv_report.csv", index=False)
    print(f"wrote {PROC / 'merge_loocv_report.csv'} ({len(rep)} gauges)")

    if not adopt:
        print("not adopted: no forcing files written (pre-registered).")
        return

    # ---- adopted: write v3 alongside v2 ----------------------------------------
    Pdf = pd.DataFrame(merged, index=dates, columns=cent.id.values)
    Pdf.index.name = "date"
    Pdf.to_csv(PROC / "forcing_minibacia_precip_v3.csv", float_format="%.2f")
    print(f"wrote forcing_minibacia_precip_v3.csv  {Pdf.shape[0]} x {Pdf.shape[1]}")
    prov = cent.copy()
    prov["elev_m"] = np.round(elev_mb, 1)
    prov["band"] = band_mb
    prov["zone"] = zone_mb
    prov["d_nearest_km"] = np.round(d_near, 3)
    prov["w_chirps"] = np.round(w, 4)
    prov["source"] = np.where(w == 0, "gauge", np.where(w == 1, "chirps", "blend"))
    prov["fallback_days"] = gap.sum(0)
    prov.to_csv(PROC / "forcing_minibacia_provenance_v3.csv", index=False)
    print("wrote forcing_minibacia_provenance_v3.csv")
    forcing_npy.convert("precip", "v3")     # re-verifies the CSV byte-for-byte


if __name__ == "__main__":
    main()

"""
Re-snap discharge gauges to the correct minibacia by drainage-area matching.

THE BUG
-------
data/processed/gauge_minibacia.csv assigns each gauge to whichever minibacia's raster
cell sits under its recorded (lon, lat) - a plain point-in-cell snap with no check that
the resulting upstream drainage area is consistent with the gauge's own discharge. The
discharge QC (docs/17_discharge_qc_audit.md) found this corrupts 54-79 of 159 mapped
stations: a ~0.05 deg coordinate offset (one raster cell) can drop a mainstem gauge onto
a tiny lateral minibacia, or a tributary gauge onto the mainstem - both directions occur.
Textbook case: ARMENIA reports 2,836 m3/s against a 137 km2 assigned catchment (implied
runoff 652,196 mm/yr; physically impossible by three-plus orders of magnitude).

THE FIX
-------
For every station whose current mapping gives an implausible runoff coefficient
(RC = annual Q volume / annual rainfall volume over the assigned upstream area), search
minibacias within an expanding radius of the gauge's coordinate and pick the one whose
RC is closest to the fleet's healthy median (0.435, from the QC's 80 clean stations).
RC is the right criterion, not distance: it directly tests "does this catchment's rainfall
plausibly produce this station's discharge", which is exactly what a wrong-area mapping
breaks.

EXCLUDED, NOT REMAPPED: the lower-Magdalena distributary (brazos) stations
---------------------------------------------------------------------------
Ten stations sit on the Brazo de Loba / Mompos distributary system, where the river
physically splits. minibacias.csv is single-downstream (D8 topology), so no upstream-area
accumulation can represent a channel that forks - no re-snap fixes this; the topology
itself cannot express bifurcating flow. These are marked excluded_distributary and left
on their original mapping, since forcing an RC-plausible re-snap here would assign a
wrong-but-plausible-looking area rather than an honestly-unrepresentable one.

Outputs (data/processed/):
    gauge_minibacia.csv               corrected mapping (same schema, in place)
    gauge_minibacia_remap_report.csv  every touched station: old/new minibacia, RC, action

Run:  python src/fix_gauge_minibacia_mapping.py
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"

RC_REFERENCE = 0.435          # median RC of the 80 clean stations (docs/17)
RC_PLAUSIBLE = (0.03, 1.2)    # a mapping is "broken" if RC falls outside this
SEARCH_RADII_KM = (3, 6, 10, 15, 20)
SECONDS_PER_YEAR = 365.25 * 86400

# Brazo de Loba / Mompos distributary gauges - structurally unrepresentable by a
# single-downstream topology (docs/17, "Lower-Magdalena distributary (brazos) zone").
DISTRIBUTARY_CODES = {
    "25027360", "25027400", "25027530", "25027620", "25027930",
    "25027020", "25027270", "25027420", "23187280", "23217030",
}


def haversine_km(la1, lo1, la2, lo2):
    return np.sqrt(((la1 - la2) * 111.0) ** 2
                   + ((lo1 - lo2) * 111.0 * np.cos(np.radians((la1 + la2) / 2))) ** 2)


def upstream_accumulate(mb: pd.DataFrame, value: pd.Series) -> pd.Series:
    """Sum `value` over each minibacia and everything draining into it.

    Topological sweep from headwaters to the outlet: a node's total is finalised once
    every node upstream of it (its children in the downstream tree) is finalised.
    """
    children: dict[int, list[int]] = {i: [] for i in mb.id}
    for i, d in zip(mb.id, mb.downstream):
        if d in children:
            children[d].append(i)
    pending = {i: len(c) for i, c in children.items()}
    total = value.copy()
    queue = [i for i, n in pending.items() if n == 0]
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        d = mb.loc[mb.id == node, "downstream"].iloc[0]
        if d in pending:
            total[d] = total.get(d, 0.0) + total[node]
            pending[d] -= 1
            if pending[d] == 0:
                queue.append(d)
    return total


def main() -> None:
    mb = pd.read_csv(PROC / "minibacias.csv")
    gm = pd.read_csv(PROC / "gauge_minibacia.csv", dtype={"code": str})
    dis = pd.read_csv(PROC / "discharge_daily.csv", dtype={"code": str})
    inv = pd.read_csv(PROC / "discharge_inventory.csv", dtype={"code": str})

    with rasterio.open(PROC / "minibacias.tif") as src:
        lab = src.read(1)
        tr = src.transform

    # -- per-minibacia upstream area and upstream mean-annual precipitation --------
    own_area = pd.Series(mb.area_km2.values, index=mb.id.values)
    up_area = upstream_accumulate(mb, own_area.copy())

    precip_cols = pd.read_csv(PROC / "forcing_minibacia_precip.csv", nrows=0).columns[1:]
    precip_mean = pd.read_csv(PROC / "forcing_minibacia_precip.csv",
                              usecols=list(precip_cols)).mean() * 365.25
    precip_mean.index = precip_mean.index.astype(int)
    own_precip_vol = own_area * precip_mean.reindex(own_area.index).fillna(precip_mean.median())
    up_precip_vol = upstream_accumulate(mb, own_precip_vol.copy())
    up_precip_mm = up_precip_vol / up_area  # area-weighted upstream mean, mm/yr

    outlet_check = up_area[mb.loc[mb.downstream == -1, "id"].iloc[0]]
    print(f"sanity: outlet upstream area = {outlet_check:,.0f} km2 (full basin ~257,097)")

    # -- minibacia centroids, for candidate search and reporting -------------------
    ids = mb.id.values
    com = ndimage.center_of_mass(np.ones_like(lab, dtype=np.uint8), lab, ids)
    cent = pd.DataFrame({"id": ids,
                         "lon": tr.c + (np.array([c[1] for c in com]) + 0.5) * tr.a,
                         "lat": tr.f + (np.array([c[0] for c in com]) + 0.5) * tr.e})
    cent = cent.dropna(subset=["lon", "lat"]).set_index("id")

    mean_q = dis.groupby("code").q_m3s.mean()
    names = inv.set_index("code")["name"] if "name" in inv else pd.Series(dtype=str)

    def rc_of(minibacia_id: int, q: float) -> float:
        area = up_area.get(minibacia_id, np.nan)
        precip = up_precip_mm.get(minibacia_id, np.nan)
        if not np.isfinite(area) or not np.isfinite(precip) or area <= 0 or precip <= 0:
            return np.nan
        q_vol = q * SECONDS_PER_YEAR
        p_vol = area * 1e6 * (precip / 1000.0)
        return q_vol / p_vol

    def best_candidate(lon: float, lat: float, q: float):
        for radius_km in SEARCH_RADII_KM:
            dlat = radius_km / 111.0
            dlon = radius_km / (111.0 * max(np.cos(np.radians(lat)), 0.2))
            row0 = int((tr.f - (lat + dlat)) / (-tr.e))
            row1 = int((tr.f - (lat - dlat)) / (-tr.e))
            col0 = int((lon - dlon - tr.c) / tr.a)
            col1 = int((lon + dlon - tr.c) / tr.a)
            row0, row1 = sorted((max(row0, 0), min(row1, lab.shape[0])))
            col0, col1 = sorted((max(col0, 0), min(col1, lab.shape[1])))
            window = lab[row0:row1, col0:col1]
            candidates = [int(c) for c in np.unique(window) if c != 0]
            if not candidates:
                continue
            scored = []
            for cid in candidates:
                rc = rc_of(cid, q)
                if np.isfinite(rc) and RC_PLAUSIBLE[0] <= rc <= RC_PLAUSIBLE[1]:
                    dist = (haversine_km(lat, lon, cent.loc[cid, "lat"], cent.loc[cid, "lon"])
                            if cid in cent.index else radius_km)
                    scored.append((abs(np.log(rc) - np.log(RC_REFERENCE)), dist, cid, rc))
            if scored:
                scored.sort()
                _, dist, cid, rc = scored[0]
                return cid, rc, dist
        return None, np.nan, np.nan

    rows = []
    for _, g in gm.iterrows():
        code = g.code
        old_mb = int(g.minibacia)
        q = mean_q.get(code, np.nan)
        name = names.get(code, "")
        old_rc = rc_of(old_mb, q) if np.isfinite(q) else np.nan

        if code in DISTRIBUTARY_CODES:
            rows.append(dict(code=code, name=name, old_minibacia=old_mb, new_minibacia=old_mb,
                             action="excluded_distributary", old_rc=old_rc, new_rc=old_rc,
                             distance_km=0.0))
            continue

        if np.isfinite(old_rc) and RC_PLAUSIBLE[0] <= old_rc <= RC_PLAUSIBLE[1]:
            rows.append(dict(code=code, name=name, old_minibacia=old_mb, new_minibacia=old_mb,
                             action="kept", old_rc=old_rc, new_rc=old_rc, distance_km=0.0))
            continue

        if not np.isfinite(q):
            rows.append(dict(code=code, name=name, old_minibacia=old_mb, new_minibacia=old_mb,
                             action="no_discharge_data", old_rc=old_rc, new_rc=old_rc,
                             distance_km=0.0))
            continue

        new_mb, new_rc, dist = best_candidate(g.lon, g.lat, q)
        if new_mb is None:
            rows.append(dict(code=code, name=name, old_minibacia=old_mb, new_minibacia=old_mb,
                             action="unresolved_needs_manual_review", old_rc=old_rc,
                             new_rc=old_rc, distance_km=0.0))
        else:
            rows.append(dict(code=code, name=name, old_minibacia=old_mb, new_minibacia=new_mb,
                             action="remapped", old_rc=old_rc, new_rc=new_rc,
                             distance_km=round(dist, 2)))

    report = pd.DataFrame(rows)
    counts = report.action.value_counts()
    print("\naction counts:")
    print(counts.to_string())

    remapped = report[report.action == "remapped"]
    if len(remapped):
        print(f"\nremapped {len(remapped)} stations: median move {remapped.distance_km.median():.1f} km, "
              f"RC {remapped.old_rc.median():.3g} -> {remapped.new_rc.median():.3g}")
        print(remapped[["code", "name", "old_minibacia", "new_minibacia",
                        "old_rc", "new_rc", "distance_km"]].to_string(index=False))

    unresolved = report[report.action == "unresolved_needs_manual_review"]
    if len(unresolved):
        print(f"\n{len(unresolved)} stations unresolved within {SEARCH_RADII_KM[-1]} km "
              f"(no candidate gives a plausible RC) - needs manual review:")
        print(unresolved[["code", "name", "old_minibacia", "old_rc"]].to_string(index=False))

    gm2 = gm.copy()
    gm2["minibacia"] = gm2.code.map(report.set_index("code").new_minibacia).fillna(gm2.minibacia).astype(int)
    gm2.to_csv(PROC / "gauge_minibacia.csv", index=False)
    report.to_csv(PROC / "gauge_minibacia_remap_report.csv", index=False)
    print(f"\nwrote gauge_minibacia.csv ({len(gm2)} rows, updated in place)")
    print("wrote gauge_minibacia_remap_report.csv")


if __name__ == "__main__":
    main()

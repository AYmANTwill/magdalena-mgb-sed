#!/usr/bin/env python3.10
"""Background task B5 — geocode the 46 unmapped SSC stations from the IDEAM CNE and map them
to the model grid, then assess how many become usable (docs/31 B5, docs/32 §R6).

Coordinates fetched from the IDEAM Catalogo Nacional de Estaciones (datos.gov.co Socrata
`hp9r-jxuu`, code = 8-digit zero-padded to 10), 2026-08-12.  Reads minibacias.tif to assign
each point a minibacia, then cross-checks SSC coverage (sediment_daily_qc) and same-code
discharge pairing (discharge_daily) — the two floors that decide C4/C5 usability.

Writes data/processed/ssc_recovered_coords.csv (the deliverable).  Reads only otherwise.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio

REPO = Path(__file__).resolve().parents[2]
PROC = REPO / "data" / "processed"

# code -> (lat, lon), IDEAM CNE hp9r-jxuu, fetched 2026-08-12
CNE = {
 "21027010": (2.053166667, -75.85188889), "21037010": (2.03, -75.78),
 "21057060": (2.46, -75.76), "21087040": (2.71, -75.57), "21087080": (2.64, -75.54),
 "21097070": (2.942611111, -75.30852778), "21107020": (2.566388889, -75.37427778),
 "21117080": (2.92, -75.15), "21147050": (3.283944444, -74.90822222),
 "21187030": (4.231946, -75.092981), "21207960": (4.454861111, -74.60852778),
 "21217210": (4.566666667, -75.33333333), "21237010": (4.387777778, -74.838375),
 "22027010": (3.328277778, -75.61311111), "22077070": (4.05425, -75.38808333),
 "23037010": (5.469666667, -74.66216667), "23057140": (5.731027778, -74.72583333),
 "23067040": (5.759222222, -74.63175), "23087190": (5.998361111, -74.93825),
 "23127020": (6.525555556, -74.08583333), "23127030": (6.783333333, -74.11666667),
 "23147020": (6.773611111, -73.935), "24017570": (6.118333333, -73.49333333),
 "24017590": (5.872777778, -73.67777778), "24017640": (6.448888889, -73.30694444),
 "24017830": (5.618388889, -73.61286111), "24027020": (6.5, -73.1),
 "24027040": (6.529166667, -73.00777778), "24027060": (6.478611111, -73.07361111),
 "24037030": (5.681722222, -73.23113889), "24037040": (6.453972222, -72.40305556),
 "24037130": (5.748833333, -73.18988889), "24037360": (6.749722222, -73.09666667),
 "25027200": (8.39, -74.56), "26117030": (4.416666667, -76.1),
 "26147140": (4.987944444, -75.85891667), "26177030": (4.8925, -75.882694444),
 "26187040": (5.713611111, -75.540277778), "26187110": (5.7414778, -75.6005638),
 "26207030": (5.829944444, -75.7055), "28017050": (10.52719444, -73.33636111),
 "28037030": (10.38411111, -73.23247222), "28037090": (9.648193, -73.646367),
 "29067040": (10.830425, -74.121078), "29067060": (10.496596, -74.128263),
 "29067070": (10.903945, -74.147716),
}


def main() -> int:
    ssc = pd.read_csv(PROC / "sediment_daily_qc.csv", dtype={"code": str}, parse_dates=["date"])
    ssc = ssc[(~ssc["c1_deleted"].astype(bool)) & ssc["ssc_mean_mg_l"].notna()]
    q = pd.read_csv(PROC / "discharge_daily.csv", dtype={"code": str}, parse_dates=["date"])
    qcodes = set(q["code"].unique())
    CAL = (pd.Timestamp("2012-01-01"), pd.Timestamp("2014-12-31"))
    LN = (pd.Timestamp("2011-01-01"), pd.Timestamp("2011-12-31"))
    EN = (pd.Timestamp("2015-01-01"), pd.Timestamp("2016-12-31"))

    with rasterio.open(PROC / "minibacias.tif") as ds:
        rows = []
        for code, (lat, lon) in CNE.items():
            mini = next(ds.sample([(lon, lat)]))[0]
            mini = int(mini) if mini and mini > 0 else 0
            s = ssc[ssc["code"] == code]
            n_ssc = len(s)
            n_cal = int(((s["date"] >= CAL[0]) & (s["date"] <= CAL[1])).sum())
            n_ln = int(((s["date"] >= LN[0]) & (s["date"] <= LN[1])).sum())
            n_en = int(((s["date"] >= EN[0]) & (s["date"] <= EN[1])).sum())
            has_q = code in qcodes
            rows.append(dict(code=code, lat=lat, lon=lon, minibacia=mini,
                             in_basin=mini > 0, n_ssc=n_ssc, n_ssc_cal=n_cal,
                             n_ssc_lanina=n_ln, n_ssc_elnino=n_en, self_paired_q=has_q))
    df = pd.DataFrame(rows)
    df.to_csv(PROC / "ssc_recovered_coords.csv", index=False)

    inb = df[df.in_basin]
    print(f"geocoded {len(df)} stations | inside basin: {len(inb)} | outside: {len(df)-len(inb)}")
    print(f"  with same-code discharge (self-paired): {int(df.self_paired_q.sum())}")
    print(f"  with any SSC obs on disk: {int((df.n_ssc>0).sum())}")
    print(f"  CAL-window potential (>=12 SSC in 2012-14 AND self-paired Q, in basin): "
          f"{int(((df.n_ssc_cal>=12)&(df.self_paired_q)&(df.in_basin)).sum())}")
    print(f"  C5-contrast potential (>=12 SSC in BOTH ENSO windows, in basin): "
          f"{int(((df.n_ssc_lanina>=12)&(df.n_ssc_elnino>=12)&(df.in_basin)).sum())}")
    print(f"  ENSO one-window potential (>=12 in EITHER window, in basin): "
          f"{int((((df.n_ssc_lanina>=12)|(df.n_ssc_elnino>=12))&(df.in_basin)).sum())}")
    print("\nstations with usable SSC coverage (n_ssc>0), in basin:")
    show = inb[inb.n_ssc > 0].sort_values("n_ssc", ascending=False)
    print(show[["code", "minibacia", "n_ssc", "n_ssc_cal", "n_ssc_lanina",
                "n_ssc_elnino", "self_paired_q"]].to_string(index=False))
    print("\nwrote data/processed/ssc_recovered_coords.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

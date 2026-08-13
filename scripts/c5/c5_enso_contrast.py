#!/usr/bin/env python3.10
"""C5 — the MODELLED ENSO sediment contrast, vs the model-free observed one (docs/34).

The registered claim (docs/34): every station shows La Niña (wet) > El Niño (dry); the observed
primary-pair median RATE ratio is ~3-5, 22/22 station-ratios > 1.  C5 asks whether the calibrated
sediment model reproduces that contrast on the STRICTLY OUT-OF-SAMPLE windows.

Windows (docs/34 §1.2, primary pair; docs/45 §3.5 P-LN/P-EN):
    P-LN  La Niña (wet)  2011-01-01 .. 2011-12-31   (365 d)
    P-EN  El Niño (dry)  2015-01-01 .. 2016-12-31   (731 d)
Cross-window comparison is RATES ONLY (mean t/day); the ratio is mean t/d(LN) / mean t/d(EN).

The modelled ratio is INVARIANT to alpha and to the LS level (both cancel in a within-station
wet/dry ratio), so C5 is robust to the C4.3 railing (docs/55): it is a test of the RUNOFF
contrast the rainfall field carries, not of the sediment level.  Engine at adopted defaults
(V4_dg, alpha=1, beta=0.56), k_dep=0/SDR=1 so station flux = hillslope load over the catchment.

Writes data/processed/c5_enso_contrast.{json,md}.  Reads only; no default moved.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts" / "c3"))
import mgb_sediment as sed          # noqa: E402
import ls_stratified_report as SR   # noqa: E402

PROC = REPO / "data" / "processed"
FROZEN = PROC / "sim_calibrated_v2"
LN = (np.datetime64("2011-01-01"), np.datetime64("2011-12-31"))
EN = (np.datetime64("2015-01-01"), np.datetime64("2016-12-31"))
BETA = 0.56


def main() -> int:
    cats, usable = SR.station_catchments()
    drv = sed.load_drivers(FROZEN / "h2e_drivers.npz")
    geom = sed.load_geometry(PROC, mini_ids=drv.mini_ids)       # adopted default V4_dg (ACT 2)
    assert geom.ls2d_column == "V4_dg"
    dates = np.asarray(drv.dates, dtype="datetime64[D]")
    ln_mask = (dates >= LN[0]) & (dates <= LN[1])
    en_mask = (dates >= EN[0]) & (dates <= EN[1])

    run = sed.simulate_sediment(geom, sed.SedParams(alpha=1.0, beta=BETA), drv.qsur_mm,
                                dates=drv.dates, store_daily=True, dtype_out=np.float64)
    D = run.delivered_t_day
    mid_to_col = {int(m): j for j, m in enumerate(geom.mini_ids)}

    obs = pd.read_csv(PROC / "c2" / "c2_rate_ratios.csv", dtype={"code": str})
    obs = obs[obs["pair"] == "primary"].set_index("code")

    rows = {}
    for code in [str(int(c)) for c in usable["code"]]:
        cols = [mid_to_col[m] for m in cats[code] if m in mid_to_col]
        s = D[:, cols].sum(axis=1)
        ln_rate = float(s[ln_mask].mean())
        en_rate = float(s[en_mask].mean())
        mod = ln_rate / en_rate if en_rate > 0 else float("nan")
        o = obs.loc[code] if code in obs.index else None
        rows[code] = {
            "name": str(usable[usable["code"].astype(str) == code]["name"].iloc[0]),
            "mod_ln_tday": ln_rate, "mod_en_tday": en_rate, "mod_ratio": mod,
            "obs_a_ratio": (float(o["a_ratio"]) if o is not None and pd.notna(o["a_ratio"])
                            else None),
            "obs_b_ratio": (float(o["b_ratio"]) if o is not None and pd.notna(o["b_ratio"])
                            else None),
        }

    modr = np.array([r["mod_ratio"] for r in rows.values() if np.isfinite(r["mod_ratio"])])
    obsa = np.array([r["obs_a_ratio"] for r in rows.values() if r["obs_a_ratio"] is not None])
    obsb = np.array([r["obs_b_ratio"] for r in rows.values() if r["obs_b_ratio"] is not None])
    n_gt1 = int((modr > 1.0).sum())

    summary = {
        "beta": BETA, "windows": {"P-LN": "2011", "P-EN": "2015-2016"},
        "n_stations": len(rows),
        "modelled": {"median_ratio": float(np.median(modr)), "geomean": float(np.exp(np.mean(np.log(modr)))),
                     "range": [float(modr.min()), float(modr.max())],
                     "n_gt_1": n_gt1, "n_total": int(modr.size),
                     "direction": "La Nina > El Nino" if n_gt1 == modr.size else "MIXED"},
        "observed_docs34": {"median_rate_ratio_primary": "~3-5", "all_22_gt_1": True,
                            "est_a_median": float(np.median(obsa)) if obsa.size else None,
                            "est_b_median": float(np.median(obsb)) if obsb.size else None},
        "per_station": rows,
    }
    (PROC / "c5_enso_contrast.json").write_text(json.dumps(summary, indent=1))

    md = ["### C5 — modelled vs observed ENSO sediment contrast (rate ratio La Niña / El Niño)", "",
          f"Primary windows: P-LN 2011, P-EN 2015–2016. Engine on adopted V4_dg, β {BETA}; "
          f"ratio is α- and LS-invariant. Observed (docs/34): median ~3–5, **22/22 > 1**.", "",
          f"**Modelled: median {summary['modelled']['median_ratio']:.2f}, geo-mean "
          f"{summary['modelled']['geomean']:.2f}, range {modr.min():.2f}–{modr.max():.2f}, "
          f"{n_gt1}/{modr.size} stations > 1 ({summary['modelled']['direction']}).**", "",
          "| station | modelled ratio | obs (a) | obs (b) |", "|---|--:|--:|--:|"]
    for c, r in sorted(rows.items(), key=lambda kv: -kv[1]["mod_ratio"]):
        oa = f"{r['obs_a_ratio']:.2f}" if r["obs_a_ratio"] else "—"
        ob = f"{r['obs_b_ratio']:.2f}" if r["obs_b_ratio"] else "—"
        md.append(f"| {c} {r['name'][:22]} | {r['mod_ratio']:.2f} | {oa} | {ob} |")
    (PROC / "c5_enso_contrast.md").write_text("\n".join(md))
    print("\n".join(md))
    print("\nwrote data/processed/c5_enso_contrast.{json,md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

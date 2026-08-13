# 57 — B5: geocoding the 46 unmapped SSC stations, and the hard limit on the gauge count

**Written 2026-08-12. Background task B5 (docs/31 B5, docs/32 §R6): recover coordinates for the
46 SSC stations carried as `excluded, reason="no coordinates"`, and decide whether the usable
gauge set can grow beyond 18.** Harness `scripts/c1/b5_geocode_ssc.py`; deliverable
`data/processed/ssc_recovered_coords.csv`.

## 1 — What B5 recovered

All 46 codes were found in the **IDEAM Catálogo Nacional de Estaciones** (datos.gov.co Socrata
`hp9r-jxuu`; the CNE `codigo` is our 8-digit code zero-padded to 10), fetched 2026-08-12:

- **46/46 geocoded; 43 fall inside the basin** (3 outside the modelled domain);
- **44 carry SSC records** on disk, several rich (thousands of samples).

So the "no coordinates" exclusion is **resolved** — the locations existed and are now on record.

## 2 — Why geocoding does NOT grow the calibration set — the binding constraint is discharge

Sediment **flux** — the quantity C4/C2 fit and score — is `Q × concentration × 0.0864`, so a
sediment site is usable for the flux objective only if it **also gauges discharge under the same
code**. Measured:

- of the **18** usable SSC stations, **18/18** have same-code discharge (they are all
  `is_discharge_station`);
- of the **43** recovered in-basin sites, **0** have same-code discharge in `discharge_daily`
  (192 stations), **and 0 of 43 appear anywhere in the raw IDEAM discharge download**
  (`data/raw/observed/caudal/`, all departments).

These 43 are **sediment-only sampling points** — IDEAM never measured discharge there, so there is
nothing to fetch (B5b is closed, not pending). **The flux-calibration gauge set cannot be grown
past ~18. That is a physical limit of the monitoring network, not a processing gap.** The nearest
discharge gauge to a recovered site is typically 10–35 km away — a different point on the network
with a different drainage area, so it cannot supply a valid same-site flux.

## 3 — What CAN use the recovered data: the concentration contrast (a weaker corroboration)

The observed ENSO signal can also be read in **SSC concentration** (mg/L) alone, which needs no
discharge. Across all stations with ≥ 12 SSC days in **both** ENSO windows (2011 La Niña,
2015–16 El Niño):

- **16 stations** qualify — **8 of them are newly-recovered** by B5, so geocoding did broaden the
  empirical base;
- **11 of 16 show La Niña > El Niño**, median ratio **1.38**, geo-mean 1.73, range 0.43 – 6.29.

This **corroborates the direction but is much weaker and noisier than the flux contrast** (median
~3–5, **22/22** in `docs/34`). The reason is structural, not a defect: flux carries the discharge
amplification (wet years move far more water *and* sediment), while concentration strips it out.
**Concentration is a broader but coarser check; the flux contrast on the ~18–22 paired gauges
remains the strong result.**

## 4 — The honest bottom line on "18 is too little"

The study's sediment claim does not rest on gauge *count*; it rests on the **convergence of three
independent lines**, which B5 leaves intact and slightly broadens:

1. **observed flux contrast** — 22/22 stations La Niña > El Niño, median ~3–5 (`docs/34`), strong;
2. **observed concentration contrast** — 11/16 stations, median 1.38 (this doc), weak but same sign;
3. **modelled flux contrast** — 18/18, median 3.05 (`docs/56`), strong.

Three methods, no sign reversal. That agreement is the evidence, and it is more robust than a
larger single-method gauge set would be. **The ~18-gauge limit is real and should be stated as a
limitation** — but it bounds the *flux calibration*, not the ENSO-contrast conclusion, which is
carried model-free and now across a broader station set.

## 5 — Disclosure

New files: `scripts/c1/b5_geocode_ssc.py`, `data/processed/ssc_recovered_coords.csv`. Coordinates
from IDEAM CNE (`hp9r-jxuu`), fetched 2026-08-12; mapped to `minibacias.tif`. No frozen artifact
touched. The `docs/23` §13.2 yield embargo holds — ratios and concentrations only, no t/km²/yr.

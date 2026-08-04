# Journal: chirps-merge agent

## Goal
Implement CHIRPS-gauge merged rainfall field; validate with the nb11 section-6 LOOCV
protocol; adopt only if merged median daily r > 0.429 (gauge-only baseline) AND
volume gate holds (merged basin mean 2009-2017 within 1% of 2,036.4 mm/yr).

## Planned steps
- [ ] Read docs/18 s9-s12, docs/22 s4.7, src/idw_forcing.py, src/nbgen/make_nb11.py section 6, src/forcing_npy.py
- [ ] Inventory inputs: CHIRPS files 2008-2018, minibacia centroids + elevations + zones, gauge QC daily + inventory
- [ ] Write src/merge_chirps_gauges.py (mask CHIRPS to basin; per elevation-band x zone quantile map CHIRPS->gauge; merged field: gauge IDW / distance-weighted blend / pure mapped CHIRPS in 41,180 fallback cells; deterministic)
- [ ] Volume gate: area-weighted merged basin mean 2009-2017 vs 2,036.4 mm/yr (within 1%)
- [ ] LOOCV gate: nb11 s6 protocol exactly, 287 evaluation gauges, merged-without-that-gauge estimate at gauge location, daily r; compare median vs 0.429
- [ ] Decision: adopt (write v3 forcing + npy trio + provenance_v3.csv) or reject (write only merge_loocv_report.csv)
- [ ] Append result subsection to docs/18 (window, both medians, volume figure, decision, pre-registered rule quoted)
- [ ] Journal follow-up: v3 calibration needs nb12 rebuild first (do NOT run here)

## Constraints
- No git add/commit/push. Touch only: src/merge_chirps_gauges.py, data/processed outputs per decision, docs/18, this journal.
- TRAP 8: chirps_basin_*.nc is a bounding box - must mask to basin.
- TRAP 9: always attach the window to any rainfall number.
- Never pd.read_csv the wide forcing CSVs; use src/forcing_npy.py.
- Justify adoption by r, never by volume.

## Log
- Created journal. Next: read the required docs and source files.
- Read idw_forcing.py, forcing_npy.py, make_nb11.py s6, docs/18 s9, docs/22 s4.7.
  Key facts confirmed from executed nb11: 291 gauges after colocated merge, LOOCV over
  287 gauges (>=300 overlap days), median daily r 0.429, bias +1.7%; fallback cells
  41,180 (k=6 all-silent minibacia-days, filled by k=20); area-weighted v2 basin mean
  2009-2017 = 2036.4 mm/yr; CHIRPS E1/E3 2009-2017 = 2124.9 mm/yr.
  Inventory has zona (9 hydrographic zones) + alt per gauge. minibacias.csv has no
  elevation -> derive from dem_coarse.tif + minibacias.tif labels.
- Next: check dem_coarse grid vs minibacias.tif, and nb10's CHIRPS-gauge lag direction
  (dia pluviometrico offset, 0.14->0.29), before writing the merge script.
- Input inventory verified:
  * chirps_basin_2008..2018.nc: 11 files, grid 202x96 at 0.05 deg, BOUNDING BOX (trap 8)
    -> never take a box mean; sample at minibacia centroids / gauge pixels only.
  * nb10 (executed): best CHIRPS-gauge alignment is LAG -1 (CHIRPS stamped day tau pairs
    with gauge day tau-1, dia pluviometrico); median daily r raw CHIRPS at gauges 0.31,
    bias -5.8% on 2009-2017. QM+merge design was already the nb10 verdict.
  * Full-basin DEM: COP90 at C:\Users\knade.MSI_TWILL\AppData\Local\Temp\output_hh.tif
    (12000x5640, 0.000833 deg, same extent as minibacias.tif, exactly 8x finer;
    regenerable from data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz).
    cop30_dem.tif / dem_coarse.tif cover only a sub-window -> NOT usable basin-wide.
  * Gauge inventory has zona (9 zones, 281/294 non-null) and alt (281/294).

## Pre-registered design (before any LOOCV run)
- Gauge set: precip_gauges_daily_qc_v2 + inventory_qc, colocated-merged via idw_forcing
  (291 gauges), matrix 4018 days (2008-01-01..2018-12-31) - identical to nb11.
- Elevation: minibacia = label-mean of 8x block-reduced COP90 DEM; gauge = DEM value at
  gauge location (one consistent source; fills the 13 missing alt).
  Bands: [0,500), [500,1500), [1500,2500), [2500,inf) m.
- Zone: gauges from inventory zona (missing -> nearest gauge's zona); minibacia = zona of
  nearest gauge (deterministic tie-break by gauge code).
- Quantile map: per (band x zone) stratum, empirical, 1001 quantile knots, fitted on
  PAIRED station-days (gauge value vs lag-aligned CHIRPS at that gauge pixel, only days
  the gauge reported, 2008-2018). Above-max tail scaled by ratio of top knots.
  Fallback hierarchy if stratum has <3 gauges or <5000 pairs: (band,zone)->zone->band->global.
- Merged field: P6 = k=6 masked IDW (idw_forcing, order-invariance asserted);
  w_chirps(d)=clip((d_nearest_gauge-10)/20, 0, 1) per minibacia (pure gauge <10 km, pure
  mapped CHIRPS >30 km, matching G/GC/C provenance semantics);
  merged = w*C_mapped + (1-w)*P6; the 41,180 k=6-silent cells get pure C_mapped
  (k=20 fill only where CHIRPS itself is missing). No RNG anywhere.
- VOLUME GATE: area-weighted merged basin mean, 2009-2017 window, within 1% of
  2036.4 mm/yr (accept 2016.0..2056.8).
- LOOCV GATE (decision): nb11 s6 protocol EXACTLY (k=6 argsort neighbour set, w=1/max(d,1)^2,
  masked, >=300 scored days, daily r). Script FIRST reproduces the gauge-only baseline and
  must print median 0.429 over 287 gauges (self-check). Then for each evaluation gauge:
  IDW from others + QM refit with that gauge's pairs EXCLUDED from every pool level +
  blend at w(d to nearest other gauge); fallback days -> pure mapped CHIRPS.
  Primary score mask: gauge observed AND merged defined. Secondary (diagnostic): restricted
  to the baseline (IDW-defined) mask.
  DECISION RULE (pre-registered by the task): ADOPT if merged median r > 0.429 by any
  margin AND volume gate holds; otherwise DO NOT ADOPT.
- Outputs: reject -> only data/processed/merge_loocv_report.csv. adopt -> v3 CSV + npy trio
  + provenance_v3.csv (+ report csv).
- About to write src/merge_chirps_gauges.py.
- Wrote src/merge_chirps_gauges.py (design exactly as pre-registered above; baseline
  self-check asserts |median - 0.429| < 6e-4 since 0.429 is the 3-dp published figure).
- RISKY OP: about to launch the full run (python3.10, background, log to scratchpad
  merge_run.log). Expected ~10-20 min: DEM reduce, CHIRPS sample, baseline LOOCV
  self-check, merged LOOCV, order-invariance x2, full-field build, volume gate,
  decision. Writes merge_loocv_report.csv always; v3 files only on ADOPT.
- RUN IN PROGRESS (bb31qtqym). Interim results from merge_run.log:
  * baseline self-check PASSED: 287 evaluation gauges, median daily r 0.429 exactly.
  * merged LOOCV median daily r 0.447 (> 0.429 -> LOOCV gate PASSES);
    baseline-mask-only diagnostic 0.449.
  * by isolation: <10 km 0.481->0.475 (w=0; small drop is the chirps-filled extra days
    in the primary mask); 10-30 km 0.426->0.449 (the win); >30 km 0.343->0.300
    (pure mapped CHIRPS at w=1 is WORSE than k=6 IDW even out there - worth reporting).
  * CHIRPS sampling: 0 NaN at all 8,963 points; bands gauges [98,84,55,54],
    minibacias [3427,2442,1628,1175].
  * awaiting order-invariance, full-field build, VOLUME GATE.
- RUN COMPLETE (exit 0). FINAL RESULT:
  * LOOCV GATE: PASS. Baseline reproduced exactly (287 gauges, median r 0.429);
    merged median r 0.447. Per gauge: 149 improved / 51 worsened / 87 unchanged.
    10-30 km band +0.023 (0.426->0.449); >30 km pure mapped CHIRPS WORSE (0.343->0.300).
  * VOLUME GATE: FAIL. Merged area-weighted 2009-2017 = 2188.5 mm/yr vs target
    2036.4 +/-1% (+7.5%). 2008-2018 = 2219.2 mm/yr.
  * DECISION per pre-registered rule (both gates required): DO NOT ADOPT.
  * Written to data/processed: merge_loocv_report.csv ONLY (291 rows). No v3 forcing,
    no npy, no provenance file - verified by directory listing. v2 stands.
  * Volume-failure mechanism (hypothesis, consistent with doc 18 s9.3): quantile maps
    fitted on reporting-day pairs inherit the residual rain-selective reporting of the
    139 unrepaired stations; the mapped CHIRPS then applies that wet-conditioned
    distribution to all days, concentrated where w->1.
- Appended docs/18 section 15 (windows attached to every rainfall figure, rule quoted,
  both medians, volume numbers, decision).

## Follow-up (recorded, NOT executed here)
- A v3 CALIBRATION was never launched: it is a future pre-registered cell that needs an
  nb12 rebuild first (task instruction). Moot until a merge passes both gates.
- If the merge is retried: hold volume by fitting quantile maps only on stations that
  pass the selectivity test (~1.00), or finish the zero-suppression repair on the 139
  residual rain-selective stations (doc 18 s9.3) FIRST - that repair is upstream.
- DEM dependency: script reads COP90 from %TEMP%\output_hh.tif (env COP90_DEM overrides);
  regenerable from data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz.

DONE. All checklist steps complete; decision reached (DO NOT ADOPT).

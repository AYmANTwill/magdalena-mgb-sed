# Progress journal

> **STATUS — LIVE as a chronology, but it stops at 2026-08-03.** Everything after that date (Phase B's closure, and Phase C stages C0–C3) is recorded in [docs/30](30_phase_c_plan.md)–~~[docs/36](36_peak_deficit_options.md)~~ **[docs/53](53_delta_shape_pretest.md)** and in the live tracker `progress_map.html`. Entry point: [docs/00_INDEX.md](00_INDEX.md).
>
> ⚠ **Range widened 2026-08-12.** The numbered docs now run to **53** *(→ **59**, see the 2026-08-19 note below)* (44 was never assigned), and
> the stage list above stops one stage short: Phase C has since reached **C3 (OPEN —
> [docs/37](37_c3_closure.md), four amendments)** and **C4**, where the entry verdict
> [docs/47](47_c4_entry_verdict.md) records *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not
> start.**"* **The dated entries below are correct as history and are not edited** — a log records
> what was understood on its date. Read them for *when* and *why*, never for current status.
>
> ⚠ **Range widened AGAIN 2026-08-19 — the 2026-08-12 widening above is itself behind.** ~~The
> numbered docs now run to **53**~~ → they now run to **59** (44 was never assigned). The
> `C4.3-BLOCKED-UNTIL-LS-LANDS` quote above is **history, not the current gate**: the block was
> discharged when LS landed (`ls_formulation = buarque_2015_dg`, f_LS = 0.25146 erosion-weighted),
> **C4.3 RAN** ([docs/55](55_c43_verdict.md) — **RAILED / EXPLORATORY, NOT adopted**), and **C5
> COMPLETED** ([docs/56](56_c5_enso_application.md) — the model reproduces the observed ENSO
> contrast, 18/18 stations, median rate ratio 3.05×). **Phase C is COMPLETE.** Also landed since:
> [docs/57](57_b5_gauge_expansion.md) (B5 — the flux gauge set cannot grow past ~18),
> [docs/58](58_rainfall_ceiling_bound.md) (the last rainfall lever bounded at ≤ +0.006 r) and
> [docs/59](59_cross_implementation_comparison.md) (an independent *implementation*, **not**
> independent data — every R2 number pinned to commit d055561, 2026-08-03).

Dated log of understanding and realization. **Updated at each new step.** Newest entries on top.

---

## 2026-08-03 — Documentation closeout: docs/19 corrections, docs/20 + 21 written

The documentation-debt push from doc 25 stage 5, so the repo explains itself with no
conversation history:

- **docs/19 — both FLAWED items fixed, marked `[corrected 2026-08-03]` in place.**
  (1) `calibration_safe` is now stated honestly: a **geometry-and-name screen only**
  (minibacia mapping + BOCATOMA/CANAL regex + two structural exclusions) with **no
  SSC-quality gate** — two "safe" stations have ρ ≈ 0 over thousands of paired days, and
  Phase C must add an explicit SSC-quality gate before using the flag (§3.7, §1, §5.1, §6).
  (2) The flatline-threshold null was recomputed: the published "0.00037 % expected vs
  0.354 % observed = 952× excess" used a whole-record shuffle that mixes rating-table eras.
  It reproduces (0.0003 %, 20 replicates) but is the wrong null: local-quantisation nulls
  give 0.030 % (within-year) to 0.234 % (within-14-day) — the published null understated by
  **~80–630×**, and the honest excess is **~1.5–12×**. N = 5 now rests on the physical
  argument (SSC has no storage memory) plus N = 10's vacuity, not on 952×. The same flawed
  wording survives in a `src/build_sediment_gauges.py` comment (~lines 105–107), left for
  the next edit of that file.
- **docs/20_reproduction_guide.md written** — environment (pinned `requirements.txt` /
  `environment.yml`), the full regeneration chain (precip QC v1→v2→selectivity, discharge,
  CHIRPS/ERA5, nbgen-generated nb10/11, nb12→13→14), how every gitignored artifact rebuilds
  (`data/`, `figures/deck/` via scripts/extract_notebook_figures.py + make_deck_charts.py,
  `*.pptx` via scripts/build_deck.py), calibration monitoring/resume (`watch_calib.py`;
  checkpoint + verified RNG replay in `src/calib_v2.py`), and the traps index.
- **docs/21_project_state_and_handoff.md written** — the three attempts (VAL KGE
  0.450/0.421/0.346; recession 2.98×/0.96×/1.01×), H2 − H1 (PBIAS −4.44 pts, r +0.0033:
  volume and correlation are independent), the r-ceiling result (12 configs r 0.556–0.572;
  LOOCV 0.429; anomaly r 0.476; inter-gauge 0.33 at 0–25 km vs ~30 km spacing), 12
  renumbered open items, the advisor question (docs/24 item 17), the presentation
  deliverables, and a paste-ready prompt for a fresh session.
- **CLAUDE.md updated**: pointers to docs/20 and 21; conventions for regenerable deck
  artifacts and the `python3.10.exe` worker-name trap.

## 2026-07-28 — Sediment-data reality found on DHIME (pivotal for Q1/Q2)

Investigated IDEAM DHIME + the national station catalogue for suspended-sediment coverage of 2011 and 2015–2016:

- **Calamar [29037020]** — on the Magdalena mainstem (`corriente: MAGDALENA`, 10.24°N), but **Limnimétrica**:
  discharge exists, **no suspended-sediment series in DHIME**.
- **No lower-Magdalena mainstem station** has suspended-sediment covering BOTH 2011 and 2015–2016.
- Rich sediment records DO exist nearby, but on the **Sierra Nevada de Santa Marta rivers draining to the Ciénaga
  Grande de Santa Marta** (NOT the Magdalena): **Fundación [29067120]** (`corriente FUNDACIÓN`, 2002–2026, 8,437 records)
  and **Puente Ferrocarril [29067130]** (`corriente ARACATACA`, 1984–2025, 15,276 records) — both span the study years.

**Consequence — decision needed with the advisor (affects Q1, Q2, and the region):**
- **Path A** — keep the Magdalena; calibrate sediment (α, β) on the best available Magdalena record (even pre-2010 /
  another mainstem station), then *simulate* 2011 & 2015–2016 (comparison = model output; discharge anchors it).
- **Path B** — shift the study years to an ENSO pair with Magdalena sediment data.
- **Path C** — pivot the study to the **Sierra Nevada / Ciénaga Grande rivers** (Fundación, Aracataca…): observed
  sediment for BOTH events, steep high-yield catchments, ENSO-sensitive, tractable — but it is not the Magdalena River.

## 2026-07-28 — Switched to whole basin @ 90 m; whole-basin data collected

- **Decision:** model the **whole Magdalena-Cauca basin at 90 m** (30 m whole-basin exceeds IPH's cell limit;
  90 m ≈ 62 M cells). Box: N 11.4, W −77.0, S 1.4, E −72.9. (Still to confirm formally with the advisor.)
- **DEM:** Copernicus **GLO-90** for the basin box → `data/raw/dem/rasters_COP90.tar.gz` (verify locally in QGIS).
- **Land cover:** WorldCover 2021, **8 tiles** (N00–N09 × W075/W078) → `data/raw/landcover/`.
- **Soils:** switched from IGAC to **SoilGrids** — the IGAC national layer (`suelosdecolombiaaniveldeorden`) failed
  (server 502/504, truncated to 32 polygons). Downloaded 5 properties (0–5 cm, 250 m, whole basin) via WCS:
  `soilgrids_{clay,sand,silt,soc,bdod}.tif`. To derive: texture → hydrological soil groups + MUSLE **K**.
  IGAC kept as the "official" option to revisit with the advisor if he requires it.
- **Climate:** ERA5-Land re-downloading for the whole basin (`era5land_basin_*` naming, resumable script).
- **Remaining:** IDEAM observed (discharge + sediment) — pending the calibration-station selection.

## 2026-07-28 — Real-DEM EDA + reclassification (URH ingredients)

- **DEM EDA** (`notebooks/04_real_dem_eda.ipynb`): inspected the real DEM, terrain hillshade, flow-accumulation attempt.
  Found the lower box **cannot be delineated** — (1) the upstream basin is off-map (mainstem enters the south edge with
  ~0 accumulated area), (2) the flat delta breaks D8 (the flats problem). → the **stream-definition threshold must be
  chosen on the full-basin DEM**, not this box. Recorded the parameter checklist for the redo.
- **Reclassification** (`notebooks/05_landcover_soils_reclass.ipynb`, extent-independent): land cover → 8 hydrological
  classes; soils → 9 landscape/hydro groups (first-pass, landscape proxy — refine with texture/HSG or SoilGrids);
  aligned both to the DEM grid and crossed into a real URH map. Outputs in `data/processed/`
  (`landcover_hydro_30m.tif`, `soils_hydro_30m.tif`, `urh_30m.tif`).
- Per-minibacia URH composition still pending the minibacias (DEM/IPH step, after domain confirmation).

## 2026-07-28 — Data verified + soils processed

- **DEM** (`data/raw/dem/cop30_dem.tar.gz` → `output_hh.tif`) verified: lower-Magdalena box (W −75.4, E −73.7, S 8.2,
  N 11.3), 30 m, EPSG:4326, **68 M cells** (under IPH limit), max elevation 5,583 m (Sierra Nevada de Santa Marta).
  ⚠️ NoData not set → must force −9999 before IPH.
- **Land cover:** 2 WorldCover 2021 tiles (N09W075 + N06W075) verified in `data/raw/landcover/worldcover_2021.zip`.
- **Soils:** 8 departments merged → **18,217 polygons**. Fixed the missing CRS (export dropped it; assigned EPSG:9377),
  reprojected to EPSG:4326 → `data/processed/soils_magdalena_merged_4326.gpkg`. PAISAJE categories need harmonizing
  (casing/spelling) at the URH stage.
- **Domain note:** the current DEM (8.2–11.3°N) does **not** reach the Sogamoso/Lebrija sediment-calibration tributaries
  (~7°N). Once the advisor confirms the domain, re-download a larger DEM extending south. **Minibacias + URH held** until then.

## 2026-07-28 — Data collection started (lower-Magdalena pilot)

- Downloaded into `data/raw/`: **DEM** (COP30 GeoTIFF, tar.gz), **land cover** (ESA WorldCover 2021, Terrascope zip),
  and **soils — Magdalena department** exported from the IGAC ArcGIS REST server to `data/raw/soils/suelos_magdalena.gpkg`
  (2,483 polygons, EPSG:9377, soil-landscape classes: cuerpo de agua, lomerío, montaña, piedemonte, planicie, valle, zona urbana).
- IGAC server is slow/timeout-prone: only Magdalena pushed through; **remaining departments (Atlántico, Bolívar, Cesar,
  Sucre, Córdoba) to be filled with SoilGrids at the URH step** rather than fighting the portal.
- Study region in use: **lower Magdalena near the sea** (box X −75.4/−73.7, Y 8.2/11.3) — interim focus pending advisor
  confirmation of exact region/years.
- Still to do: **DHIME** discharge + sediment (Calamar); ERA5 deferred until region + years fixed.

## 2026-07-27 — ENSO years clarified + model data/resolution confirmed (research pass)

- ENSO classification (see `07_enso_years.md`): 2010–2011 strong La Niña; 2015–2016 very strong El Niño;
  **2017 = weak La Niña, NOT El Niño**. Recommend **La Niña 2011 vs El Niño 2015–2016** (Q2). Corrected the "2017?" placeholder.
- Confirmed MGB-SED forcing variables: precipitation, air temperature, incident solar radiation, relative humidity,
  wind speed, atmospheric pressure. Standard topography for MGB-SED AS = **MERIT Hydro ~90 m** (not 30 m) → whole basin
  is feasible at the model's native resolution; noted HRUSed (hydro-sedimentological response units) refinement.
- Copernicus ERA5: **not downloaded yet** — deferred until region + years are fixed; CDS account to be created now.

## 2026-07-27 — IDEAM sediment stations found (Q1 largely resolved)

- Literature scan for the sediment-data feasibility (Q1). Findings recorded in `docs/06_ideam_stations.md`:
  **Calamar** (downstream reference, 112 km from the mouth, records to ~2010, ~145–169 Mt/yr) and **Puerto Berrío**
  (mid-basin, codes 23095010 / 23090110); an extensive IDEAM network (30–40+ sediment sites); all downloadable free via
  the **DHIME** portal (+ National Station Catalogue on datos.gov.co).
- **Q1 risk downgraded red → amber/green.** Remaining check: confirm suspended-sediment coverage for 2011 and 2015–2017.
- Reasoning refined: the sediment-flux comparison points to a **downstream (near-ocean) integrating outlet** (Calamar),
  which in turn defines the modelled domain; and MGB is a large-basin model normally run at ~90 m (MERIT Hydro), so the
  30 m cell limit is not binding at the right resolution.

## 2026-07-27 — Study-area decision + data collection started

- Advisor's brief specifies the **whole Magdalena** ("el río Magdalena"), no sub-basin given.
- **Decision:** target the whole basin, but build the full MGB-SA workflow on a **substantial Andean pilot** first
  (upper + middle Magdalena to a mid-basin gauge, ~80,000–110,000 km², full 30 m, under IPH's ~250 M cell limit),
  then scale. Not a tiny test catchment. Exact outlet to be fixed with the calibration gauge. To confirm with advisor.
- Started the **data collection plan** (`docs/05_data_collection_plan.md`): DEM, soils, land cover, climate, discharge.
- Confirmed approach: **Python** (pysheds / WhiteboxTools) for real-data exploration & QA; **IPH-HydroTools/MGB plugin**
  for the official `mini.gtb` generation that MGB consumes (Python would otherwise require rebuilding the MGB file format).

## 2026-07-27 — Scope decision: MGB-SA first, sediments deferred

- Decided to **complete and calibrate MGB-SA (hydrology) before starting the sediment module**. Rationale:
  (1) MUSLE consumes MGB-SA outputs (runoff volume, peak flow), so hydrology must work first;
  (2) de-risks the internship — a calibrated hydrological model is a valid standalone result, and IDEAM discharge
  data is far more available than sediment data; (3) clarifies exactly which outputs will later feed the sediment module.
- The sediment blocks (MUSLE, α/β calibration) and the DHIME sediment-station search are postponed, not dropped.

## 2026-07-27 — MGB-SA hydrology block understood

- Worked out the **rainfall-to-discharge** mechanism; notebook `03_hydrology.ipynb`:
  the daily **soil water balance** (`W_{t+1} = W_t + P - ET - D_sup - D_int - D_bas`); **saturation-excess** surface
  runoff via **variable contributing area** (`A_sat = 1-(1-W/Wm)^b`, role of `b` for flashiness); the three outflow
  paths and the **linear reservoir** recession (`Q = Q0 e^{-t/K}`, role of `K_bas` for dry-season flow).
- Built a working daily simulation of one URH (wet spell then drought): reproduces storm peaks and a
  baseflow-dominated recession (~99% baseflow deep in the dry season).
- Understood **routing**: Muskingum-Cunge (one-way) vs hydrodynamic/local-inertial (floodplains, backwater) — the
  latter required for the lower Magdalena (ciénagas, near-flat channel).
- Calibration knobs identified: `Wm, b, K_int, K_bas`, judged by NSE/KGE/PBIAS on IDEAM discharge.

## 2026-07-27 — URH block understood + repository created

- Worked out **URH generation** (soil × land cover) from first principles; notebook `02_urh.ipynb`:
  reclassification + cell-by-cell overlay, index formula `URH = (soil-1)*N_occ + occ`, bound `N_URH <= N_soil*N_occ`,
  **Fréchet bounds** (`max(0,a+b-N) <= overlap <= min(a,b)`) proving marginals are insufficient, per-minibacia
  composition `f_{m,u}` (sums to 1), and area-weighted aggregation `X_m = Σ f_{m,u} X_u`.
- Understood the alignment prerequisite (rasters on the DEM grid) as the URH analogue of "NODATA = -9999".
- Created this **scientific repository** (English docs, git-initialized) to organize the project and track progress.

## 2026-07-27 — DEM preprocessing chain understood

- Derived, by hand and in simple Python, all 7 preprocessing transformations; notebook `01_dem.ipynb`:
  ESRI ASCII format & NODATA=-9999; **Planchon-Darboux** pit filling (role of `eps`, flats vs drainage slope);
  **D8** flow direction (slope = drop / distance, diagonal = cellsize·√2); **flow accumulation** (recursive,
  "who flows into me"); **stream definition** (accumulation threshold); **stream segmentation** (junctions);
  **watershed/catchment delineation** → minibacias.
- Key insight captured: fill `eps=0` creates flats that D8 re-reads as false pits — fill and flow-direction are coupled.

## (earlier) — Phase 0 completed

- QGIS 3.44 LTR (FR), decimal separator = point. Plugins IPH-HydroTools (2025), MGB (Dec 2025), MGB-SED installed.
- Full preprocessing tested on ~3000 km² test zone (upper Magdalena, GLO-30): **198 minibacias**. Files in `D:\test\`.

---

### How to add an entry
Add a new dated section on top: what was understood/done, which notebook/doc changed, and any decision or insight.

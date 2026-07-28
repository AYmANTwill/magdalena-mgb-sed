# Progress journal

Dated log of understanding and realization. **Updated at each new step.** Newest entries on top.

---

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

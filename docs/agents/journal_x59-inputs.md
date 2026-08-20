# Journal — x59-inputs (M3: is the "shared inputs" inference sound?)

Slug: `x59-inputs`. READ-ONLY except this file. Started 2026-08-12.

Task: build a side-by-side input table (DEM, soils/K, land cover/C, precipitation,
PET/meteorology, basin delineation/HRU, routing, LS) for OUR repo vs THEIR repo
(yben409/simulating-suspended-sediment-transport @ d055561), mark each row
SHARED / DIFFERENT / UNDETERMINED, then rule on whether "the over-production must be in
the shared inputs" is a sound inference.

THEIR clone (read-only):
`C:/Users/KNADE~1.MSI/AppData/Local/Temp/claude/c--dev-magdalena-mgb-sed/5b31ac56-2c65-4a16-ac08-d810606ee036/scratchpad/friend_repo`

## Log

### 1. THEIR repo — configs and build path (read-only)

`config/data_sources.yaml` is **written by** `scripts/14_integrate_data_final.py`
(`--config-out config/data_sources.yaml`, line 177) — it is a *manifest of the data_Final audit*,
not a file any model code reads. `grep -rn "data_sources" --include=*.py .` returns only script 14.
So the canonical-source declarations in it (COP90, IGAC-primary soils) are **provenance claims about
data_Final, not statements about what the calibrated run consumed.**

What `scripts/04_build_basin.py` actually consumes (argparse defaults, lines ~228-240):
- `--dem  data/processed/dem/magdalena_dem_90m.tif`, then `--resample 3` DEFAULT => routing grid
  written to `magdalena_dem_270m.tif`; in-code cell size reported as ~184 m / ~275 m in comments.
- `--soil-dir data/raw/soil` and `soil_mean_profile()` globs
  `soilgrids_{clay,silt,sand,soc}_{0-5cm,5-15cm,15-30cm}_mean.tif` => **SoilGrids, not IGAC.**
- `--landcover-dir data/raw/landcover` => ESA WorldCover tiles, `classify_cover` via
  `WORLDCOVER_TO_GROUP`.
- `config/magdalena.yaml` for outlet, texture_classes, manning, stations, subbasins.
- `config/hru_params_magdalena.yaml` for reservoirs + texture_fractions.
- basin structure is delineated FROM THE DEM by `T.delineate_unit_catchments`. It does **not** read
  `data_Final/08_basin_structure/minibacias.csv` (the 8,672 table). Comment in 04_build_basin
  (`--min-reach-length-cells` help) says "all 7,929 reaches"; data_sources.yaml line 69 says
  "234,407 km2 (91%) from build_basin on COP90 at 270 m" and line 68-72 says the 8,672 table
  "carries only id/area_km2/downstream: no reach length, slope, bed elevation, width, depth or
  floodplain curves ... Those must still be derived from the DEM."
- K factor: `build_k_factor` -> `erodibility_sharpley_williams(sand,silt,clay,soc)` per CELL from
  SoilGrids, averaged per (catchment, HRU).
- HRU scheme: `TEXTURE_CLASSES = ("sandy","medium","clayey")` x
  `COVER_GROUPS = ("forest_wetland","grassland","cropland_urban_bare","water")` = **12 HRUs**.
- C factor (config/magdalena.yaml musle/landcover): forest_wetland 0.0001, grassland 0.02,
  cropland_urban_bare 0.10, water 0.0; P = 1.0; alpha 11.8, beta 0.56 (Williams 1975 defaults).
- LS: `src/mgbsed/model/musle.py:75 ls_factor_2d` = Desmet & Govers (1996) L with **m = 0.4 fixed**,
  S = Wischmeier & Smith (1978) `65.41 sin^2 t + 4.56 sin t + 0.065`, aspect term
  x = |sin a| + |cos a|; aggregated AREA-MEAN per unit catchment for Eq.(1) and SUM for triggers.
  Computed ON THE COARSE ROUTING GRID, which they document as a known bias (04_build_basin lines
  ~250-262: "the Desmet & Govers L term grows with cell size, so a 275 m grid overstates slope
  length and understates gradient ... Calibration absorbs the bias into the MUSLE alpha multiplier;
  it does not remove it, so LS2D here is not comparable cell-for-cell with a finer run.")

### 2. OUR side, verified from our own code/artifacts (not from the brief)

- **DEM**: Copernicus GLO-90 (COP90) via OpenTopography, corrected domain
  `S=1.4 N=11.4 W=-77.0 E=-72.3` (`docs/15` §Table). Archive
  `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, member `output_hh.tif`, 0.000833 deg,
  5,640 x 12,000 (`docs/37` §3, §897). LS is computed at **native 90 m**
  (`ls2d_resolution='native_90m'`, x1.000, `docs/37` §Table row 4). BUT
  `model_inputs_v2/manifest.json` records the topology provenance as
  *"minibacias.csv:area_km2 (notebook 07 D8 delineation on COP30)"* -- so the DELINEATION
  provenance string says COP30 while the LS/terrain classifier says corrected COP90.
  I could not settle which is right from what is on disk; recorded as UNDETERMINED-ON-OUR-SIDE.
- **Basin structure**: 8,672 minibacias, `outlet_upstream_area_km2` = **257096.93** km2,
  `sum_of_own_areas_km2` = 257096.93, accumulator max abs disagreement 1.798616722226143e-08 km2,
  24 URH = soil family 1-3 x land class 1-8 (`urh_fractions.csv`, nb08).
- **Soils / K**: **IGAC field survey**, 3 texture families; K = Wischmeier & Smith (1978) class
  mid-range converted to SI (x0.1317): Coarse 0.020, Medium 0.045, Fine 0.028, times a drainage
  factor (well 0.95 / moderate 1.00 / poor 1.10) (`notebooks/09_soil_parameters.ipynb` §4).
  Measured from `data/processed/minibacia_soil_params.csv` (n = 8,672):
  K median **0.030550**, mean 0.031824, min 0.019000, max 0.049500, CV 0.2289, max/min 2.6053.
  nb09 §1 explicitly MEASURED and REJECTED the SoilGrids pedotransfer route because SoilGrids
  classes ~95 % of the basin as Fine (clay 33 +/- 4 %) -> spatially flat K.
- **Land cover / C**: ESA WorldCover 10 m 2021 v200 (`data/processed/worldcover/ESA_WorldCover_10m_2021_v200_*.tif`).
  `LC_MAP = {10:1,20:2,30:3,40:4,50:5,60:6,70:6,80:7,90:8,95:8,100:6}` -> 8 classes
  (`notebooks/05_landcover_soils_reclass.ipynb` cell 3). C from `urh_cp_factors.csv`,
  `cp_revision='cited_central_2026_08_11'`, column `C`, used **AS READ** (no fitted multiplier;
  `mgb_sediment.py` L1024-1025). C: Forest 0.005, Shrub 0.015, Grassland 0.015, Cropland 0.200,
  Urban 0.030, Bare 0.500, Water 0.000, Wetland 0.005; P = 1.0 everywhere.
- **Precipitation (adopted)**: `manifest.json` -> *"forcing_minibacia_precip.csv - notebook 11 IDW
  k=6 over 294 repaired IDEAM gauges, k=20 fallback"*; `make_nb11.py` L73 reads
  `precip_gauges_daily_qc_v2.csv`. **No CHIRPS in the adopted field.** `src/merge_chirps_gauges.py`
  is an explicit *"v3 candidate"*; `docs/26` L23: *"H3 (v2 + CHIRPS-gauge merge) was dropped, not
  faked: the merge was never implemented"*, L178: *"the CHIRPS-gauge merge is ... the only remaining
  lever"*. Our CHIRPS product, where used at all, is `chirps-v2.0.{year}.days_p05.nc` (0.05 deg).
- **PET (adopted)**: `manifest.json` -> *"forcing_minibacia_pet.csv - notebook 11 FAO-56
  Penman-Monteith on ERA5-Land (ssrd 01-23h rule, docs/16 s6.1)"*, with **kc_mult fitted to 1.662**
  (`report_h2e.py` L223 gate).
- **Basin means (adopted bundle)**: P = **2073.1** mm/yr, PET = **1251.6** mm/yr, Calamar runoff
  depth 912.4 mm/yr, model period 2008-01-01..2018-12-31 (4,018 days), 2008 = warm-up.
- **Routing (sediment)**: `src/mgb_transport.py` -- per-reach linear storage reservoir
  (Muskingum X = 0), same operator as water, plus first-order settling `k_dep` default **0.0**.
  No hydrodynamics, no floodplain curves.

### 3. The precipitation handoff -- MEASURED

`src/build_data_final.py` PROCESSED_RULES routes **only** `precip_gauges_daily.csv` and
`precip_gauges_inventory.csv` into `data_Final/05_precipitation/processed/`. `grep -n "_qc"
src/build_data_final.py` returns **nothing**: the `_qc` (repaired) files are not routed at all.
Their `scripts/15_build_forcing_v2.py` default is exactly
`data_Final/05_precipitation/processed/precip_gauges_daily.csv`.

Row counts on our disk (`python3.10`, pandas):

| file | rows | stations | zero fraction | Inferido_seco | unweighted mean |
|---|---|---|---|---|---|
| `precip_gauges_daily.csv` (what data_Final carries, what they read) | 686,752 | 294 | 0.441793 | 0 | **6.821825** mm/d |
| `precip_gauges_daily_qc.csv` (repair v1) | 795,881 | 294 | 0.518333 | 109,129 | 5.886435 mm/d |
| `precip_gauges_daily_qc_v2.csv` (repair v2, the ADOPTED input) | 926,910 | 294 | 0.586422 | 240,158 | **5.054322** mm/d |

Their `config/data_sources.yaml` declares `stations: 294`, `station_days: 686752` -- an exact
match to the unrepaired file, which confirms the identification.
6.821825 / 5.054322 = **1.3496976** x. 6.821825 * 365.25 = **2491.67** mm/yr, and their
`15_build_forcing_v2.py` docstring quotes *"the gauges average 2,492 mm/yr"* -- exact.

They independently diagnosed the same defect and mitigated it differently: `load_gauge_precip`
docstring records mean rainfall vs reporting density (>90 % of days -> 4.5 mm/day, 63 % zeros;
50-90 % -> 6.9 mm/day, 32 % zeros; <50 % -> 13.0 mm/day, 24 % zeros; *"a 2.9x spread in rainfall
as a function of how often the observer wrote something down is not geography"*) and DROP every
gauge below `--min-gauge-density 0.8` rather than repairing it. They then use CHIRPS as the field,
bias-corrected by monthly gauge/CHIRPS log-ratios clipped to (0.25, 4.0) (`--precip-method merge`,
the default).

### 4. The C-factor measurement (this is the row that decides M3's clause 4)

Both projects reclassify the SAME product (ESA WorldCover 2021 v200) but into different schemes,
so a like-for-like is available: apply THEIR 4-group C table to OUR 8-class area shares.

| our class | area % | our modelled erosion share % | our C | their C (group) | ours/theirs |
|---|---|---|---|---|---|
| Forest | 55.774448 | 50.491788 | 0.005 | 0.0001 (forest_wetland) | **50.000** |
| Shrub | 0.118724 | 0.144897 | 0.015 | 0.02 (grassland) | 0.750 |
| Grassland | 39.866682 | 34.036568 | 0.015 | 0.02 (grassland) | 0.750 |
| Cropland | 1.574933 | 0.392627 | 0.200 | 0.10 (cropland_urban_bare) | 2.000 |
| Urban | 0.297055 | 0.148022 | 0.030 | 0.10 | 0.300 |
| Bare | 0.196257 | **14.780004** | 0.500 | 0.10 | **5.000** |
| Water | 0.648751 | 0.000000 | 0.000 | 0.0 | - |
| Wetland | 1.523149 | 0.006094 | 0.005 | 0.0001 | **50.000** |

(erosion shares from `data/processed/urh_erosion_weights.csv`, `urh % 10` = land class,
total eroded_t 2,994,977,042.274908 t over the decade = 299.4977 Mt/yr, against the documented
gate 299.5387088405831 Mt/yr -- a 0.0137 % difference I did not chase.)

- area-weighted mean C, **ours** = **0.0130829583**
- area-weighted mean C, **their table on our area shares** = **0.0101226238**
- ratio ours/theirs = **1.292447**
- their own `21_calibrate_sediment.py` docstring independently states "The area-weighted basin C
  was 0.0104" -- my recompute 0.0101226238 is 2.67 % from their number, an independent
  cross-check that the two land-cover distributions agree closely.
- erosion-POTENTIAL-weighted (weights = our eroded_t / our own C, so our C is not double-counted):
  ours **0.0080549035**, theirs **0.0040460557**, ratio **1.990804**.
- weighted by our modelled erosion as-is: ratio **3.709648**.
- ours(no multiplier) / theirs(x fitted c_mult 0.04887856036752898) = **26.442009**
  (using their own 0.0104: **25.7368**).

Two mapping divergences on the SAME WorldCover codes, both material in a high-Andean basin:
code 60/70 (bare/sparse, snow/ice) -> our Bare C 0.500 vs their cropland_urban_bare 0.100 (5x);
code **100 (moss and lichen = paramo)** -> our Bare C 0.500 vs their grassland 0.020 (**25x**).
Our class 6 lumps codes 60/70/100 so I cannot split it without re-reading the 10 m tiles; class 6
is 0.196 % of area, so the area-weighted mean is insensitive, but it carries 14.78 % of our
modelled erosion, so the erosion-weighted comparison IS sensitive to that split. Named as
UNDETERMINED.

### 5. Their alpha and c_mult -- what the fit actually did

Re-verified by reading `outputs/calibration/stage2_sediment_params.json` and
`outputs/calibration_val/stage2_sediment_params.json`:

- calibration: alpha 55.40533705803028, beta 0.3980082263356884, alpha_tc 0.6174944111935904,
  c_mult 0.04887856036752898, stage2_median_kge_log 0.05461202762457862, n_stations 21
- validation: alpha 96.58548959666564, beta 0.3493190336411669, alpha_tc 0.34930405763655487,
  c_mult 0.05779232694874972, stage2_median_kge_log 0.05902198016897042, n_stations 13
- alpha*c_mult = **2.7081331121** -> **5.5819001933**, x**2.0611616794**, while the score moves
  +**0.00440995254439**
- alpha/11.8 = **4.695368** (cal) / **8.185211** (val); 1/c_mult = **20.458868** / **17.303335**
- **(alpha*c_mult)/11.8 = 0.2295028061 (cal) and 0.4730423893 (val)**: relative to
  (Williams alpha 11.8, C as tabled) their fit puts the MUSLE level **DOWN by 4.357245x**
  (cal) / **2.113975x** (val).

Their `21_calibrate_sediment.py` docstring states the motive: "Sediment came out ~25x too low,
because the C factor for the forest/wetland HRU group (0.0001) was inherited from the Guaiba basin
and applied to WorldCover 'tree cover' in the Colombian Andes -- coffee, plantain, degraded
hillside. ... implying an erosion-proof landscape in a basin with among the highest sediment yields
on earth. Hence the C multiplier." The multiplier was introduced to RAISE the level; the FITTED
value LOWERS it 20.46x, and alpha absorbs 4.70x of that, so the NET is a 4.36x reduction.

### 6. LS -- do we and they stand on a common footing?

Theirs (`src/mgbsed/model/musle.py:75 ls_factor_2d`): Desmet & Govers (1996) L,
`((A+D^2)^(m+1) - A^(m+1)) / (D^(m+2) x^m 22.13^m)`, **m fixed at 0.4**; S = Wischmeier & Smith
(1978) `65.41 sin^2 t + 4.56 sin t + 0.065`; aspect term `x = |sin a| + |cos a|`; AREA-MEAN per
unit catchment into Eq. (1), SUM into the triggers.

Ours (adopted, `ls_formulation = buarque_2015_dg`, `urh_ls2d_variants.csv` column `V4_dg`):
`docs/37` A3.1 -- "V1 limiter at one DEM pixel + V2b eq.-14 step m + V3 eq.-18 W&S-78 S + eq. 13's
Desmet-Govers finite-difference L with Xdir^m. The source formulation read whole."

So the two are the **same formulation family** -- D&G L, W&S-78 S, an aspect/Xdir term -- differing
in (a) `m` (theirs fixed 0.4, ours the eq.-14 slope-dependent step), (b) our one-DEM-pixel limiter,
and (c) **cell size: our 90 m against their ~275 m** (`--resample 3` default; the repo also carries
184 m comments, so which grid produced the shipped params is UNDETERMINED).

Measured on our terrain (`urh_ls2d_variants.csv`, 32,782 (mini, urh) rows):

| column | area-wt mean | ero-wt mean | median | max |
|---|---|---|---|---|
| `V0_ours_2026_08` (prior engine default) | 40.549673 | 75.429702 | 19.285684 | 384.5842 |
| `V1_lim_pixel` | 14.242923 | 25.073084 | 8.343040 | 62.5270 |
| `V2a_m_cap05` | 20.368270 | 35.627411 | 12.833188 | 117.4817 |
| `V2b_m_step_eq14` | 20.473059 | 35.693228 | 13.044377 | 117.4817 |
| `V3_s_ws78` | 69.512421 | 136.867697 | 25.626093 | 825.1318 |
| `V4_buarque_2015` | 17.085685 | 31.096716 | 8.733043 | 91.8719 |
| **`V4_dg` (ADOPTED)** | **9.920900** | 17.985185 | **5.090050** | 52.3938 |
| `V4p_buarque_2015_cap` | 17.059750 | 31.088081 | 8.707449 | 91.8719 |
| `V5_L_dg96_fd` | 31.215658 | 57.959119 | 14.524150 | 327.2513 |

Reproduction check: area-weighted `V4_dg / V0` = **0.2446604234** against the documented
0.2446790094097074 (7.6e-6 relative). My erosion weighting gives 0.2384363829, which does NOT
reproduce the documented erosion-weighted 0.25146 -- `urh_erosion_weights.csv`'s `eroded_t` is
evidently not the weight `docs/46` 3.1 uses. I therefore do NOT claim 0.25146 as reproduced here;
only the area-weighted figure is reproduced.

Their LS **mean** is not in any shipped output. What IS shipped (their docstring): "the paper's
absolute LS2D thresholds (100,000-300,000) sit above almost the entire distribution here
(median 9,037, max 344,390)" -- those are the SUM aggregate. Order-of-magnitude back-out, using
their stated 234,407 km2 over the "7,929 reaches" of their own comment (29.56 km2 per catchment):
- at 275 m (0.076004 km2/cell, 389.0 cells/catchment): median mean-LS ~ 9037/389.0 = **23.233**
- at 184 m (0.033780 km2/cell, 875.2 cells/catchment): median mean-LS ~ 9037/875.2 = **10.326**

against our adopted median `V4_dg` = **5.090050** at 90 m. So their MUSLE LS is plausibly
**2.0x-4.6x** ours. This is an ESTIMATE (median-of-sums / mean-cells is not median-of-means) and it
is consistent in DIRECTION with their own written warning: "the Desmet & Govers L term grows with
cell size, so a 275 m grid overstates slope length and understates gradient relative to the
plot-scale data USLE was fitted on. Calibration absorbs the bias into the MUSLE alpha multiplier;
it does not remove it, so LS2D here is not comparable cell-for-cell with a finer run."

### 7. The side-by-side table, with the SHARED / DIFFERENT / UNDETERMINED ruling

| row | OURS (verified) | THEIRS (verified) | verdict |
|---|---|---|---|
| basin domain bbox | `S=1.4 N=11.4 W=-77.0 E=-72.3` (docs/15) | `basin_domain: -77.0/1.4/-72.3/11.4` (data_sources.yaml) | **SHARED** (identical) |
| DEM archive | `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, member `output_hh.tif`, 0.000833 deg | same archive name, same member, same `resolution_deg: 0.000833` (data_sources.yaml) | **SHARED** -- the same file, typo included |
| DEM working resolution | LS at **native 90 m** (`ls2d_resolution='native_90m'`, x1.000); terrain classifier block-averaged 8x onto `minibacias.tif` | `resample_dem` average-downsample **x3 -> ~275 m** (argparse default); repo also carries 184 m comments | **DIFFERENT** |
| basin delineation | 8,672 minibacias, 257,096.93 km2 (99.87 % of published 257,438) | own pysheds fill/D8 -> ~7,929 reaches, **234,407 km2 (91 %)**; the 8,672 table sits in their data_Final but `04_build_basin.py` does not read it | **DIFFERENT** |
| soils / K | **IGAC** field survey, 3 texture families; K = W&S-78 class mid-range x0.1317 x drainage (0.95/1.00/1.10); median **0.030550**, CV 0.2289, max/min 2.6053 | **SoilGrids** 250 m clay/silt/sand/soc, 0-30 cm depth-weighted -> **EPIC Sharpley & Williams (1990)** K per cell, averaged per (catchment, HRU) | **DIFFERENT** -- and both repos independently record that the two sources disagree (their data_sources.yaml: "SoilGrids classes 95% of the basin as Fine against IGAC's 38%"; our nb09 §1 rejects the PTF route for the same reason) |
| land-cover product | ESA WorldCover 10 m **2021 v200** | ESA WorldCover **2021 v200** | **SHARED** |
| land-cover scheme | 8 classes, `LC_MAP` above | 4 groups, `WORLDCOVER_TO_GROUP` | **DIFFERENT** |
| C factor | 8 cited values, `C` column used AS READ (no multiplier); area-wt **0.0130829583** | 4 Guaiba-basin values x fitted `c_mult`; area-wt table **0.0101226238** (they state 0.0104), effective **0.000494779** | **DIFFERENT** in scheme, in values and in whether a multiplier is fitted |
| HRU / URH scheme | **24** = 3 IGAC soil families x 8 land classes | **12** = 3 SoilGrids textures x 4 cover groups | **DIFFERENT** |
| precipitation raw source | IDEAM DHIME gauges, **294** stations, 2008-2018 | the **same 294-station file**, `station_days: 686752` | **SHARED** (same network, same export, handed over in data_Final) |
| precipitation QC | zero-suppression **repaired** -> `precip_gauges_daily_qc_v2.csv`, 926,910 rows, +240,158 `Inferido_seco`, mean 5.054322 mm/d | **unrepaired** `precip_gauges_daily.csv`, 686,752 rows, mean 6.821825 mm/d, then gauges below 80 % reporting density **dropped** | **DIFFERENT** |
| precipitation field | deterministic gauge IDW k=6 (order-invariant, co-located gauges de-duplicated), k=20 fallback; **no CHIRPS**; basin mean **2073.1 mm/yr** | **CHIRPS v2.0 p05** as the field, bias-corrected by monthly gauge/CHIRPS log-ratios clipped to (0.25, 4.0), IDW'd (`--precip-method merge`, the default) | **DIFFERENT** (our merge exists only as an unadopted v3 candidate) |
| CHIRPS product, where used | `chirps-v2.0.{year}.days_p05.nc` | `chirps-v2.0.{year}.days_p05.nc` | **SHARED** (product identical; role in the model is not) |
| meteorology product | ERA5-Land, `valid_time`, ssrd daily total = max over 01:00-23:00 | ERA5-Land, `valid_time`, 7 vars `tp t2m d2m ssrd u10 v10 sp`; ssrd daily total = `resample("D").last()` | **SHARED** in product; the ssrd rules are numerically equivalent (both land on the 23:00 value, both drop the last hour) |
| ERA5-Land extent | 2008-2018 complete, 132 mosaics (one 2008_M06 found corrupt and rebuilt) | data_sources.yaml: `years_available: 2009-2017`, `MISSING: 2008 and 2018 -- both domains, all months` | **DIFFERENT** |
| PET | FAO-56 Penman-Monteith reference ET x kc, **kc_mult fitted 1.662**; basin PET **1251.6 mm/yr** | per-HRU Penman-Monteith with albedo/z0/rs from `hru_params_magdalena.yaml`; they quote ETp **1,239 mm/yr** | **DIFFERENT** formulation; the LEVELS agree to 1.0 % |
| LS2D | `buarque_2015_dg` at 90 m: area-wt **9.920900**, median **5.090050**, max 52.3938 | D&G L with m fixed 0.4 + W&S-78 S + `|sin a|+|cos a|` at ~275 m; median mean-LS **estimated 10.326-23.233** | **DIFFERENT in level, SAME formulation family** |
| routing | linear storage reservoir (Muskingum X = 0), settling `k_dep` default **0.0**, no floodplain | local-inertial (Bates 2010) with 20-level floodplain volume-area curves, Froude cap, deposition on, resuspension off; `LinearReservoirRouter` exists as the fast fallback | **DIFFERENT** |
| the published bar | F_report in [-0.26, 0.44], no-skill KGE = 1 - sqrt(2) = -0.414 | `metrics.py` L7, L53-54 cite the same -0.26..0.44 range and the same -0.41 benchmark | **SHARED** (not an input; a fairness point in their favour) |

Incidental observation, recorded and NOT used in the ruling: in `build_etp` the domain loop reads
`chunk = got if chunk is None else chunk`, so once the `basin` file is taken the `strip` file is
never used. The strip covers -72.8..-72.3 and `ds.sel(..., method="nearest")` will still return the
basin file's edge cell for centroids out there, silently. This is a code observation about their
meteorology path, not an input-provenance difference, and it does not change any verdict above.

### 8. THE RULING on the "shared inputs" inference

The proposed inference is: *both implementations want a much lower effective sediment level, they
share no model code, therefore the over-production lives in the shared inputs rather than in either
codebase.* Measured, it fails on two counts and survives on a narrowed third.

**(a) The set of genuinely shared inputs is smaller than the claim needs.** Shared: the DEM
*archive*, the WorldCover *product*, the IDEAM gauge *network* (same 294-station DHIME export),
ERA5-Land as a *product*, the CHIRPS *product*, and the domain bbox. NOT shared: soils/K (IGAC vs
SoilGrids -- the largest single divergence, and one both repos independently document), the C table
AND the land-cover -> C mapping, the HRU scheme, the delineation, the working DEM resolution, the LS
level, the rainfall FIELD, the rainfall QC, the ET formulation, and the routing. So the inference
can only reach four suspects -- **raw elevation, the WorldCover raster, the IDEAM gauge network as an
observation set, and ERA5-Land** -- and cannot reach K, C, LS, or rainfall at all.

**(b) The two projects do not "both want a lower level" in the same currency, so the premise is
weaker than it reads.** Their reduction is a *fitted* one, measurable as
(alpha x c_mult)/11.8 = **0.2295028061**, i.e. **4.357245x down** from (Williams alpha 11.8, their C
table), and their score is **KGE_log on SSC concentration in mg/L**. Ours is not a fitted level at
all: our alpha stays at Williams' 11.8, our LS reduction 1/f_LS is a *formulation* correction
(`docs/37` A3), and C4.3 is RAILED / EXPLORATORY on **KGE_ln of log FLUX**. Same direction is not
the same measurement. docs/59 must not present the agreement as two independent estimates of one
quantity.

**(c) The C disagreement means something quite different from "both want less".** Their C table is
already **1.292447x lower than ours area-weighted** and **1.990804x lower erosion-potential-weighted**
before any multiplier. Their fitted `c_mult` 0.04887856036752898 then takes their effective
area-weighted C to **26.442009x below ours** (**40.7296x** on the erosion-potential weighting). Put
their fit on OUR C table and the implied multiplier is **0.0378186085** area-weighted /
**0.0245521722** erosion-weighted. That is not "both projects find C too high": it is *one* project
finding *its own Guaiba-inherited* C too high after having introduced the multiplier for the
opposite reason (their docstring: sediment was "~25x too low"). Our C table is independently
sourced, is 1.29-1.99x higher, and has never been fitted, so their number is not evidence about
ours.

**(d) The alpha comparison needs the LS caveat, and it needs a stronger one than resolution.**
Their alpha 55.40533705803028 is 4.695368x Williams' 11.8 while their LS is plausibly 2.03-4.56x
ours -- so alpha did NOT compensate for a high LS; it moved the same way. All of the compensation
went into `c_mult` (down 20.458868x). Both projects have therefore independently found the same
thing: MUSLE is linear in alpha and in C, only the product is identifiable, and a printed alpha-hat
carries no information on its own. Their `notes.alpha_c_collinearity` says it in one sentence; our
`docs/54`/`docs/55` say it with a condition number of infinity. **That agreement -- on
non-identifiability, from two independent codebases -- is the strongest claim docs/59 can make, and
it is stronger than anything about the shared inputs.**

**Verdict.** The inference is **not void, but it is much narrower than proposed**, and it must be
written as: *the DEM archive, the WorldCover raster, the IDEAM gauge network and ERA5-Land are
genuinely common to both projects, so a defect in any of those would be invisible to a
code-difference argument; every other MUSLE input differs between the two, so no comparison of the
two fitted levels can implicate K, C, LS or the rainfall field.*

### 9. What I could not settle

1. Which grid produced their shipped params: `--resample 3` (~275 m) is the default but the repo
   carries 184 m comments too. Their run logs are not committed.
2. Their basin-mean rainfall and ETp after the 80 % density filter + CHIRPS merge. Both are
   logged, not written to disk; `data/processed/forcing/*.parquet` is gitignored and absent.
3. Their LS2D MEAN distribution. Only the SUM (median 9,037, max 344,390) is quoted in a
   docstring; the raster and BasinData pickle are absent.
4. Their K field. SoilGrids rasters are absent, so I cannot compute what the EPIC K gives on this
   basin, only name the formula.
5. Whether OUR 8,672 minibacias were delineated on COP30 or the corrected COP90 --
   `model_inputs_v2/manifest.json` says COP30, the terrain/LS work says corrected COP90.
6. The split of our land class 6 (WorldCover 60/70/100). Needed to close the erosion-weighted C
   comparison exactly; the 10 m tiles on disk cover only lat 6-12, not the whole basin.
7. Whether their production run read the data_Final precip file (the default) or their own
   independent per-department download (`12`/`13_*precip*`). Only the default is recorded.

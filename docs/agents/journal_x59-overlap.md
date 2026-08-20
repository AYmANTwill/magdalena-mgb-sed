# Journal — x59-overlap (M1: independent data, or the same data?)

Agent slug: `x59-overlap`. READ-ONLY except this file.
Task: measure the station-code overlap between THEIR repo (yben409/simulating-suspended-sediment-transport
@ d055561) and OURS, and the ENSO window overlap in days. Decide whether docs/59 may say
"independent replication" (data) or only "independent implementation".

Started 2026-08-12.

## Plan
1. Extract their station codes (sediment 21, val 13, hydrology 90).
2. Extract ours (sediment_inventory_qc.csv 79; docs/34 §1 and docs/45 §3.4 registers; discharge inventory).
3. Counts + explicit code lists + Jaccard.
4. Window overlap in days.

## Log

### Step 1 — their station codes (verified, re-read from disk)

    $ ls friend_repo/outputs/calibration/ friend_repo/outputs/calibration_val/
    calibration:      stage1_best_station_metrics.csv  stage1_hydrology_params.json
                      stage1_search_history.csv  stage2_best_station_metrics.csv
                      stage2_search_history.csv  stage2_sediment_params.json
    calibration_val:  stage2_best_station_metrics.csv  stage2_search_history.csv
                      stage2_sediment_params.json

Also present and NOT in the orchestrator brief: `outputs/calibration_fast/`,
`outputs/calibration_fast_b/` (stage1 hydrology only).

Their codes are 10-char zero-padded (`0023127010`); ours are 8-digit (`23127010`).
Normalisation used everywhere below: `int(code)`. All three of their lists have no duplicate
codes (asserted in the script).

- THEIR sediment fit set (`calibration/stage2_best_station_metrics.csv`): **21** codes.
- THEIR sediment validation set (`calibration_val/...`): **13** codes; 13/13 are inside their 21.
- THEIR hydrology set (`calibration/stage1_best_station_metrics.csv`): **90** codes.

### Step 2 — our sets

    $ python3.10 -c "... sediment_inventory_qc.csv ..."
    ssc_class: excluded 61 | usable-with-caveat 12 | usable 6      (total 79)
    mapped: True 28 / False 51        calibration_safe: True 24 / False 55
    usable+caveat n=18
    discharge_daily.csv unique codes: 192 ; discharge_inventory.csv rows 192 (192 unique)
    stations_discharge.csv rows 167
    sediment_inventory.csv rows 79 ; sediment_daily(_qc).csv 269,337 rows / 79 codes

CAL 8 and EVAL 5 taken verbatim from `docs/45` §3.4 (read in full):
CAL = 22017030, 26137110, 24027030, 21197010, 23127010, 26127010, 22017010, 24037390;
EVAL = 26017060, 26017020, 26167070, 26207080, 21237020.

### Step 3 — the overlap matrix (script: scratchpad/x59/overlap.py)

    A             B               |A|  |B|  |A&B|  |AuB|   Jaccard   A&B/|A|
    THEIR_sed21   OUR_sed79        21   79     21     79  0.265823  1.000000
    THEIR_sed21   OUR_mapped28     21   28      9     40  0.225000  0.428571
    THEIR_sed21   OUR_usable18     21   18      8     31  0.258065  0.380952
    THEIR_sed21   OUR_CAL8         21    8      6     23  0.260870  0.285714
    THEIR_sed21   OUR_EVAL5        21    5      1     25  0.040000  0.047619
    THEIR_sed21   OUR_dis192       21  192     13    200  0.065000  0.619048
    THEIR_val13   OUR_sed79        13   79     13     79  0.164557  1.000000
    THEIR_val13   OUR_usable18     13   18      8     23  0.347826  0.615385
    THEIR_val13   OUR_CAL8         13    8      6     15  0.400000  0.461538
    THEIR_hyd90   OUR_dis192       90  192     90    192  0.468750  1.000000
    THEIR_hyd90   OUR_sed79        90   79     27    142  0.190141  0.300000
    THEIR_hyd90   OUR_usable18     90   18     15     93  0.161290  0.166667
    THEIR_sed21   THEIR_val13      21   13     13     21  0.619048  0.619048
    THEIR_sed21   THEIR_hyd90      21   90     12     99  0.121212  0.571429

**HEADLINE: containment is 1.000 in every direction that matters.**
- 21 of 21 of their SSC fit stations are in our 79. `ONLY A = []`.
- 13 of 13 of their SSC validation stations are in our 79. `ONLY A = []`.
- 90 of 90 of their discharge gauges are in our 192. `ONLY A = []`.

The Jaccard is below 1 ONLY because our sets are larger, not because theirs holds anything we
lack. There is not a single station in their calibration that we do not have.

Explicit lists:
- their21 (all 21, = the intersection with our 79): 21187030, 21217250, 22017010, 22017030,
  22027010, 22057090, 23127010, 24017830, 24037030, 24037040, 24037130, 24037390, 26017060,
  26127010, 26137110, 26177030, 28037090, 29067010, 29067050, 29067120, 29067130
- their21 ∩ our18-usable (8): 22017010, 22017030, 22057090, 23127010, 24037390, 26017060,
  26127010, 26137110
- their21 ∩ our CAL-8 (6): 22017010, 22017030, 23127010, 24037390, 26127010, 26137110
  (our CAL-8 minus theirs = only 2: 21197010 EL PROFUNDO, 24027030 NEMIZAQUE)
- their21 ∩ our EVAL-5 (1): 26017060 PUENTE ARAGÓN
- their21 NOT in our 192-gauge discharge set (8): 21187030, 22027010, 24017830, 24037030,
  24037040, 24037130, 26177030, 28037090
- our18 not in their21 (10): 21147030, 21197010, 21237020, 23087210, 24027030, 26017020,
  26107130, 26167060, 26167070, 26207080

### Step 3b — WHY the other 13 of their 21 are absent from our usable 18 (our own QC reasons)

| their code(s) | our ssc_class | our reason |
|---|---|---|
| 21187030 CUCUNUBA, 22027010 CONDOR EL, 24017830 SUTAMARCHAN, 24037030 EL PALO, 24037040 GUICAN, 24037130 LA REFORMA, 26177030 LA VIRGINIA, 28037090 PUENTE CANOAS | excluded (8) | **no coordinates** in our `sediment_inventory.csv` (C1.0, 46 of 79) |
| 29067010 EL TREBOL, 29067050 CANAL FLORIDA, 29067120 FUNDACION, 29067130 PUENTE FERROCARRIL | excluded (4) | coordinates present but **outside our 8,672-minibacia network** |
| 21217250 BOCATOMA | excluded (1) | multiple deficiencies: single-window (LN 344 / EN 0), flow-selective (0.551 > 0.514), rating R² 0.145 on n=7049 |

13 of their 21 fail OUR C1 gate, and 8 of those 13 fail on a defect that is ours, not theirs:
we never had the coordinates. `scripts/20_load_sediment.py` reads
`data/raw/ideam/ideam_catalog_magdalena_cauca.csv` for station geometry — a file with **no
counterpart in our repo**. On the coordinate problem they are ahead of us, and docs/59 should
say so. Their docstring: "the config lists 19 stations, but the DHIME archive holds SSC at 71".
Our archive holds 79.

Related: 8 of their 21 have no discharge record in our 192-gauge set. Their objective is KGE on
**concentration (mg/L)**, so they do not need paired Q at an SSC site. Our B5 finding — the flux
gauge set cannot grow past ~18 because 0 of 43 recovered SSC sites have any discharge record — is
a constraint on **flux**, and their concentration metric sidesteps it. That is a design choice
difference, not an error on either side, and it is why their n can be 21 while ours is 18/8.

### Step 4 — THE DEEPER FINDING: the model inputs are OUR files, not merely the same agency

`friend_repo/config/data_sources.yaml` names its canonical inputs. Cross-checked against ours:

| their config claim | our measurement | match |
|---|---|---|
| `basin_structure.n_minibacias: 8672` | `minibacias.csv` rows = **8672** | exact |
| `basin_structure.area_km2: 257097` | `minibacias.csv` area_km2 sum = **257096.930** | exact to 6 s.f. |
| their note: "this table carries only id/area_km2/downstream" | our columns are literally `['id','area_km2','downstream']` | exact |
| `basin_structure.n_urh: 24` | our URH = 24 types (Phase A) | exact |
| `precipitation.stations: 294` | `precip_gauges_inventory.csv` rows = **294** (qc also 294) | exact |
| `precipitation.station_days: 686752` | `precip_gauges_daily.csv` rows = **686752** | exact |
| `precipitation` note: "missing values are BLANK, not zero; 20% of records are Preliminar" | our IDEAM convention, CLAUDE.md verbatim | same |
| `soils.minibacia_params: .../minibacia_soil_params.csv` | `data/processed/minibacia_soil_params.csv` | same filename |
| `soils.rasters: soil_{family,depth,drainage}_igac.tif` | all three present | same filenames |
| `soils.merged_polygons: soils_magdalena_merged_4326.gpkg` | present | same filename |
| `discharge.gauge_minibacia`, `rating_curves.csv` | both present | same filenames |
| `landcover` note: "the 30 m landcover_hydro product in data_Final" | `landcover_hydro_30m.tif` | same filename |
| `climate`: ERA5-Land 9 km, 7 vars `tp t2m d2m ssrd u10 v10 sp`; `basin` + `east_strip`, "adjacent, not overlapping, mosaic cleanly at 0.1 deg" | our `src/mosaic_era5.py` = basin + east strip | same construction |
| `soils` note: "SoilGrids classes 95% of the basin as Fine against IGAC's 38%" | our IGAC-primary decision | same numbers |

`data_Final/` is a **gitignored directory name in OUR repo's CLAUDE.md** ("`data/`, `data_Final/`,
`delivery/` are gitignored (regenerable)"). It does not currently exist on this disk
(`ls data_Final` → No such file or directory), so I cannot hash a file against theirs. But an
exact 6-significant-figure basin area, an exact gauge count, an exact 686,752 station-day count
and a matching three-column signature are not coincidences of a shared upstream agency.
**Their forcing and basin inputs are the same derived artifacts as ours.**

I cannot tell from disk which direction the sharing ran, or whether both sides received a common
advisor pack. No `git log` was consulted for authorship and I make no authorship claim.

Raw archives: theirs `sediment: IDEAM DHIME, variable CM (mean daily concentration)`,
`raw: data/raw/ideam/dhime/`, note "8 files byte-identical, 8 identical content under different
names ... data/ is canonical because its filenames carry the year range". Ours:
`data/raw/observed/sedimento/` = 12 CSVs, several carrying year ranges
(`ssc_antioquia_2015_2018.csv`, `ssc_cauca_2001_2015.csv`, `ssc_huila_2015_2018.csv`, ...).
Same variable, same portal, same naming habit. Their raw is absent from the clone, so
byte-identity is unverifiable.

Their designed config station list (20 codes, `config/magdalena.yaml`) is a DIFFERENT and much
more mainstem-oriented list than what their calibration actually ran on — Calamar 0029037020,
Puerto Berrio 0023097030, El Banco 0025027020, La Coquera 0026247020, Pericongo 0021027010, etc.
Only 12 of their 90 hydrology gauges and few of the 21 sediment gauges come from it; the fitted
set was data-driven, exactly as their loader docstring says. Their Calamar code 0029037020 IS in
our 192-gauge discharge set.

### Step 5 — window overlap, in days

Theirs (`src/mgbsed/viz/observations.py` L42-46, constant `ENSO_EVENTS`):
`"La Nina 2010-12": ("2010-06-01","2012-04-30")`, `"El Nino 2015-16": ("2015-03-01","2016-05-31")`.
Comment: "Oceanic Nino Index thresholds sustained over 5 overlapping seasons; dates are the
conventional event windows for these two events." — i.e. an ONI-style definition, not a
calendar-year one.

Ours (`docs/34` §1.1): P-LN 2011-01-01..2011-12-31; P-EN 2015-01-01..2016-12-31;
S-LN 2010-07-01..2011-06-30; S-EN 2015-10-01..2016-04-30.

    THEIR La Nina 2010-12    2010-06-01 .. 2012-04-30  len=700 d
    THEIR El Nino 2015-16    2015-03-01 .. 2016-05-31  len=458 d
    OUR P-LN 365 d | OUR P-EN 731 d | OUR S-LN 365 d | OUR S-EN 213 d

    THEIR LN x OUR P-LN  overlap= 365 d (2011-01-01..2011-12-31)  52.14% of theirs, 100.00% of ours  J_days=0.521429
    THEIR LN x OUR S-LN  overlap= 365 d (2010-07-01..2011-06-30)  52.14% of theirs, 100.00% of ours  J_days=0.521429
    THEIR EN x OUR P-EN  overlap= 458 d (2015-03-01..2016-05-31) 100.00% of theirs,  62.65% of ours  J_days=0.626539
    THEIR EN x OUR S-EN  overlap= 213 d (2015-10-01..2016-04-30)  46.51% of theirs, 100.00% of ours  J_days=0.465066
    THEIR LN x OUR S-EN  overlap=   0 d       THEIR EN x OUR P-LN  overlap= 0 d

Both of our La Niña windows are **fully inside** theirs. Their El Niño window is **fully inside**
our P-EN and **fully contains** our S-EN. Zero cross-phase contamination either way. The wet and
dry periods being compared are, to within these containments, the same calendar days.

Fit windows: theirs `2013-01-01..2014-12-31` (730 d — both stage2 jsons, `n_stations` 21 and 13,
`held_out: "2011 (La Nina) and 2015-2017 (El Nino) were not used."`). Ours (`docs/45` §3.5)
CAL `2012-01-01..2014-12-31` (1096 d). Overlap **730 d = 100.000 % of theirs, 66.606 % of ours**
(J_days = 730/1096 = 0.666058). Their fit window is a strict subset of ours; both hold out 2011
and 2015-16. Same Klemeš-style differential split, apparently reached independently — that is
real methodological agreement and should be credited.

### Step 6 — what I could NOT settle
1. `outputs/eda/enso_summary.csv` reports 35 SSC stations (La Niña) / 27 (El Niño) and
   108 / 93 Q stations, but **does not enumerate them**, and no other on-disk file does
   (`outputs/eda/rating_curves.csv` lists only 9 codes). So the station set behind THEIR headline
   observational ENSO contrast is not code-level verifiable. All 9 rating-curve codes
   (0021217250, 0022017010, 0022017030, 0023127010, 0024017820, 0024027030, 0024037390,
   0026127010, 0026137110) ARE in our 79 and/or our 192 — 9 of 9.
   Settling it needs their `data/processed/observed_ssc_stations.csv` (written by
   `scripts/20_load_sediment.py`), which is gitignored-absent.
2. Byte-identity of the raw DHIME exports and of the `data_Final/` products: their raw is absent
   and our `data_Final/` does not exist on this disk. Unverifiable from what is here.
   Settling it needs both `data_Final/` trees side by side and a hash comparison.
3. Direction of the data sharing (who derived from whom, or a common advisor pack). No authorship
   claim made; `git log` in their clone was not used for this.
4. Whether their SSC archive's 71 stations is a strict subset of our 79 — only their fitted 21 and
   validation 13 are enumerated on disk. Settling it needs their `observed_ssc_stations.csv`.

### Verdict recorded for the WRITER
docs/59 may claim **independent IMPLEMENTATION**. It may **NOT** claim **independent DATA**.
Written in those words, as instructed.

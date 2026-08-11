# Journal — c32-cp (MUSLE C and P factors)

GOAL: build the MUSLE cover (C) and practice (P) factors for the 8 hydrological land
classes, every value traceable to a source. Deliverable:
`data/processed/urh_cp_factors.csv` (class_id, class_name, C, P, source, note).

## Checklist
- [ ] 1. Read nb05 / nb08 for the 8-class definition and the class -> minibacia/URH mapping.
- [ ] 2. Search repo for any Fagundes et al. (2026) C/P table (primary source rule).
- [ ] 3. Write `data/processed/urh_cp_factors.csv`, one row per class, source or ASSUMED per row.
- [ ] 4. Cross-check: area-weighted basin-mean C from actual cover fractions; compare with
      published tropical-Andean basin-scale C.
- [ ] 5. Sensitivity: which class dominates (area share x C).
- [ ] 6. Report at BOTH fleet (basin) and per-unit (minibacia) scale.

## Log

### Step 0 — start
Journal created. Constraints acknowledged: no git, no calibration launches, no
pd.read_csv on wide forcing CSVs, yields in t/km2/yr EMBARGOED (absolute flux only).

### Step 1 — 8-class definition (nb05 + nb08), DONE
- `notebooks/08_urh.ipynb` cell 6 is authoritative (nb05 is an explicit lower-Magdalena
  *prototype*, superseded; its own markdown says so).
  `LC_TO_CLASS = {10:1,20:2,30:3,40:4,50:5,60:6,70:6,100:6,80:7,90:8,95:8}`
  `CLASS_NAME = {1 Forest, 2 Shrub, 3 Grassland, 4 Cropland, 5 Urban, 6 Bare, 7 Water, 8 Wetland}`
  ESA WorldCover 2021 v200, majority-resampled to the minibacia grid.
- Merges to keep in mind: **Bare(6) absorbs WorldCover 60 bare + 70 snow/ice + 100
  moss/lichen**; **Wetland(8) absorbs 90 herbaceous wetland + 95 mangrove**. nb08's own
  reduction criterion is "same interception/ET/runoff behaviour *and* same MUSLE C".
- URH id = soil_family*10 + land_class (3 textures x 8 classes = 24). The land class of a
  URH is `urh_id % 10`.
- Model-facing carrier: `data/processed/model_inputs_v2/parameters.npz` keys
  `urh_id` (24,) and `urh_fraction` (8672, 24) float32; areas from
  `topology.npz:own_area_km2` (8672,). Also on disk: `data/processed/urh_fractions.csv`
  (8672 rows x 24 URH cols) - same content, CSV form.

### Step 2 — Fagundes primary-source search, DONE (NEGATIVE)
Searched the whole repo for a quotable Fagundes C/P table: `grep -ril fagundes` hits 20
files, all *narrative* references (docs/00, 01, 03, 04, 09, 14, 19, 24, 30, 31, README,
CITATION.cff). The only in-repo PDF, `Explanation_script_MGB_SA_Magdalena.pdf` (8 pp,
extracted with PyMuPDF), says only: *"each class also carries LAI, albedo, canopy
resistance and a MUSLE C factor from lookup tables"* - it names no values.
CITATION.cff still carries `given-names: "TODO"` for Fagundes, i.e. the paper itself was
never ingested here.
=> **Fagundes et al. (2026) is NOT quotable from this repo.** Per the task's fallback rule
I use standard published USLE/MUSLE C values, cited per row, and mark every uncited value
ASSUMED. This is recorded as a residual: if the paper's Table of C per HRU is obtained,
re-derive and diff against this file.

### Step 3 — `data/processed/urh_cp_factors.csv` WRITTEN (8 rows, 6 cols, 7,655 bytes)
Adopted values (C | P, every row also carrying an explicit `P: ASSUMED = 1.0 basin-wide`):

| id | class | C | source class |
|----|-------|---|--------------|
| 1 | Forest | 0.003 | Wischmeier & Smith 1978 AH-537 Tab.10 (45-70 % canopy band), Roose 1977 as lower bound |
| 2 | Shrub | 0.005 | **ASSUMED** — midpoint bracketed by rows 1 and 3 |
| 3 | Grassland | 0.010 | Roose 1977 "savanna/prairie in good condition" (same table: 0.1 overgrazed/burnt) |
| 4 | Cropland | 0.200 | **ASSUMED (mixture)** — Roose components: cereals 0.4-0.9, perennials w/ cover 0.1-0.3 |
| 5 | Urban | 0.010 | **ASSUMED** — token non-zero for the pervious fraction |
| 6 | Bare | 1.000 | Wischmeier & Smith 1978 (unit plot = clean-tilled fallow), Roose 1977 "bare soil" |
| 7 | Water | 0.000 | definitional (no soil surface) |
| 8 | Wetland | 0.001 | Roose 1977 "dense cover" |

Verified by reading the file back (`check_cp.py`, not a filename count): 8 rows, ids 1-8,
columns exactly as specified, class ids/names byte-identical to nb08 `CLASS_NAME`,
every row's `source` contains either a citation year, `definitional`, or `ASSUMED`, and
every row states `P: ASSUMED = 1.0 basin-wide`. 4 of 8 rows carry an ASSUMED marker
(Shrub, Cropland, Urban + P everywhere); Water is 'definitional'.

### Step 4 — cross-check: area-weighted basin-mean C
Cover fractions taken from the model-facing arrays (`model_inputs_v2/parameters.npz`
`urh_fraction` (8672,24) x land class = `urh_id % 10`), area weights from
`topology.npz:own_area_km2` (sum 257,096.9 km2, 8,672 units). Row sums = 1.000000 exactly.

**FLEET SCALE — area-weighted basin-mean C = 0.01082**

| class | area % | C | area x C | share of basin C |
|---|---|---|---|---|
| Grassland | 39.867 | 0.01 | 0.003987 | **36.83 %** |
| Cropland | 1.575 | 0.20 | 0.003150 | **29.10 %** |
| Bare | 0.196 | 1.00 | 0.001963 | **18.13 %** |
| Forest | 55.774 | 0.003 | 0.001673 | 15.46 % |
| Urban | 0.297 | 0.01 | 0.000030 | 0.27 % |
| Wetland | 1.523 | 0.001 | 0.000015 | 0.14 % |
| Shrub | 0.119 | 0.005 | 0.000006 | 0.05 % |
| Water | 0.649 | 0.00 | 0 | 0 % |

**PER-UNIT SCALE (8,672 minibacias, unweighted):** median C **0.00575**, IQR 0.00450
(p25 0.00389, p75 0.00840), p95 0.02927, min 0.00081, max **0.83800**; unweighted mean
0.01025 (vs 0.01082 area-weighted — big units are slightly dirtier). 264 units (3.04 %,
3.64 % of area) exceed C 0.05; 100 exceed 0.10. Concentration: **25 % of the basin's total
area x C comes from 101 minibacias (1.16 % of units, 2.14 % of area)**; 50 % from 629 units.
The 8 highest-C units are bare-dominated high country (~10.8 N/73.6 W, ~9.7 N/73.5 W,
~4.9 N/75.4 W Los Nevados, ~2.9 N/76.1 W Purace-Huila).

Plausibility vs published tropical-Andean basin-scale C: 0.0108 sits **at or below the low
end** of what RUSLE/MUSLE studies of mixed Andean catchments typically report (order
0.05-0.3 for agriculturally active basins; forest-dominated headwaters lower). *That anchor
is from recall — no citable Andean C compilation exists in this repo, so it is flagged the
same way as an ASSUMED row and must be verified against a source before it is quoted in
docs.* The mechanism of the low value is measured, not guessed: 95.6 % of the basin is
WorldCover forest + grassland and both rows take low-end values. Putting grassland at
Roose's overgrazed/burnt 0.1 alone lands basin-mean C at 0.0467, squarely inside the
published band — so *grassland condition*, not cropland extent, is the only single lever
that reconciles the two.

Resolution check (does the ~740 m URH grid distort the cover mix?): re-counted WorldCover
raw codes inside the basin at ~80 m (cos-lat weighted, 46.9 M cells) vs the URH grid:
TreeCover 54.32/55.45 %, Grassland 39.63/39.20 %, **Cropland 1.62/1.51 % (+7 % only —
nb08's fragmented-cropland worry is real but small)**, BuiltUp 0.70/0.63 %,
**Bare 0.320/0.191 % (URH grid under-detects bare by ~40 %)**, Snow/ice 0.0142/0.013 %,
Water 1.31/1.24 %, HerbWetland 1.72/1.64 %, **Moss/lichen 0.00000 % and Mangrove absent at
both resolutions** — so the paramo-moss and mangrove contamination of classes 6 and 8 is a
non-issue, measured. Propagated: bare share 0.196 -> 0.334 % raises basin-mean C 13 %
(0.01082 -> 0.01218); the cropland correction raises it 2 %.

### Step 5 — sensitivity (one-at-a-time, on the fleet number)
| swap | basin-mean C | factor |
|---|---|---|
| Grassland 0.01 -> 0.05 (partly degraded pasture) | 0.02677 | **x2.47** |
| Grassland 0.01 -> 0.10 (Roose overgrazed/burnt) | 0.04670 | **x4.32** |
| Cropland 0.20 -> 0.40 (Roose cereal band) | 0.01397 | x1.29 |
| Bare 1.0 -> 0.5 (sparsely vegetated, not fallow) | 0.00984 | x0.91 |
| Forest 0.003 -> 0.001 (closed canopy) | 0.00971 | x0.90 |
| Urban 0.01 -> 0.10 (active construction) | 0.01109 | x1.02 |
| Shrub 0.005 -> 0.01 / Wetland 0.001 -> 0.01 | 0.01083 / 0.01096 | x1.00 / x1.01 |

**Grassland is where a wrong value does the most damage** on both counts: it is the largest
contributor (36.8 % of the area-weighted C) *and* it has the widest defensible range (10x in
Roose's own table). Cropland is second (29.1 % of C from 1.6 % of area) and Bare third
(18.1 % of C from 0.20 % of area — the highest C per unit area, and the most spatially
concentrated, so a wrong Bare value distorts the *map* more than the total).

Context for the C3.4/C3.6 gate: area-weighted K = 0.0318 (per-minibacia K 0.0190-0.0495),
so area-weighted K*C*P = **3.44e-4** before LS2D.

Caveat on the aggregate itself: MUSLE applies C per URH and the sediment weight of a URH is
(Qsur*qpeak*A)^beta, not area. Bare and Urban URHs carry LAI 0 and 0.5 (`src/calib_v2.py:588`)
so they intercept nothing and generate more surplus runoff than their area share implies -
the *effective* basin C is therefore >= 0.01082, direction known, magnitude only measurable
once `src/mgb_sediment.py` exists.

### Step 6 — status
- [x] 1 class definition   - [x] 2 Fagundes search (negative, recorded)
- [x] 3 CSV written + read back   - [x] 4 basin-mean C   - [x] 5 sensitivity
- [x] 6 both scales reported
Residuals for the parent: (a) Fagundes' own C table still un-ingested - diff against this
file when the paper lands; (b) the Andean basin-mean-C literature anchor needs a real
citation; (c) grassland condition (good vs degraded pasture) is the single largest open
uncertainty in the static MUSLE multipliers; (d) `docs/PROGRESS.md` C3.2 checkbox left
unticked - not my file to edit.
- (e) **PROVENANCE RISK:** `data/processed/` is gitignored (CLAUDE.md), so
  `urh_cp_factors.csv` - a *hand-curated literature table*, not a regenerable output - is
  not versioned and its writer lived only in this session's scratchpad. The 8 values and
  their sources are reproduced verbatim in Step 3/4 above so the file can be rebuilt from
  this journal, but the parent should decide whether the table belongs in a tracked path
  (e.g. `src/` generator or a tracked `config/`) before Phase C depends on it.

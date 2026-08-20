# Journal — nbc1 — notebook coherence T1 audit — `02_urh.ipynb` + `08_urh.ipynb`

Agent: nbc1 (structural-duplicate adjudicator for the URH pair)
Date opened: 2026-08-13
Phase: **T1 = READ-ONLY AUDIT.** No notebook, generator, src or doc file is edited by me. This journal is the only file I write.

## Assignment (as given)
- Audit `notebooks/02_urh.ipynb` (14 cells) and `notebooks/08_urh.ipynb` (12 cells).
- **Own the structural-duplicate adjudication**: both claim URH. Establish from evidence which is CURRENT and
  which should be marked superseded IN PLACE (never deleted). `notebooks/README.md` describes 02 as the toy
  version and 05 as "the real-data version of notebook 02" while saying NOTHING about 08 — that itself may be a defect.
- Recommend exact supersession banner text + location, but DO NOT write it.
- Check whether either notebook contradicts the "24 URH types / IGAC soils" statement in CLAUDE.md Phase A.
- Produce owning_docs, current_claims, narrative_role, chain in/out, executed-output staleness, findings, cells_swept, not_settled.

## Log

### Step 0 — orientation
- Extracts live at `.../scratchpad/nbtext/02_urh.txt`, `08_urh.txt` (0-based `[CELL i]` markers).
- `notebooks/README.md` read in full (25 lines). It lists 01, 02, 03 as "didactic toy" notebooks and 04, 05 as
  "real-data notebooks". **It stops at 05.** Notebooks 06, 07, 08, 09 and 10-19 are entirely absent from it.
  So the "README says nothing about 08" observation is broader: the README is truncated at 05, not selectively silent.

### Step 1 — both extracts read in full
- `02_urh.txt`: 14 cells (8 md / 6 code), all executed, 0 errors. **French.** Toy 6x6 grid, 2 soils x 3 covers -> 6 URH.
- `08_urh.txt`: 12 cells (7 md / 5 code), all executed, 0 errors. **English.** Real basin, 1500x705 grid,
  8,672 minibacias, 3 IGAC texture families x 8 WorldCover classes -> **24 URH**, writes `data/processed/urh_fractions.csv`.
- Cells examined: **14 / 14** for nb02, **12 / 12** for nb08. Full sweep, no cell skipped.

### Step 2 — kill-list grep: CLEAN on both
Grepped both extracts (case-insensitive) for: `t/km2`, `t/km2` (unicode form), `mgb_sediment`, `ls2d`, `cp_revision`,
`V4_dg`, `ls2d_hs`, `0.333`, `0.421`, `2.37`, `3.00x`, `11.8`, `SDR`, `Buarque`, `104.8`, `82.8`, `126.1`, `99.7`,
`129.384`, `75.3235`, `0.1644`, `0.465`, `38 %`, `k_min`, `0.00216`, `0.0209`, `0.0104`, `348.4`,
`under-erosive`, `1.34762`, `299.5387`, `248.7298`.
**Zero hits in either notebook.** No yield-embargo violation, no retired band, no withdrawn direction. These are
Phase A notebooks; they predate every one of those numbers.

### Step 3 — engine entry points: NONE (measured, not assumed)
`python3.10` JSON scan of both `.ipynb` code cells for `mgb_sediment` / `mgb_hydrology` / `load_geometry` /
`build_geometry` / `cp_revision` / `ls2d` / `sys.path`: **NONE in either**.
Imports: nb02 = {numpy, matplotlib.pyplot}. nb08 = {glob, zipfile, tarfile, tempfile, pathlib, numpy, pandas,
rasterio, rasterio.enums, rasterio.warp, affine, matplotlib.*, pyflwdir}.
=> `ls2d_column` default (`V4_dg` at src/mgb_sediment.py:925 vs `ls2d_hs` at :818/:862) is **N/A** for both.
Their executed outputs cannot be stale relative to `c3fdb55` because they never read the engine.
(nb08 *feeds* the engine — `urh_fractions.csv` — but the fraction table is LS-independent.)

### Step 4 — MEASURED: nb08 cell 8 prints a MISLABELLED number, and the PROSE is the correct one
This is the inverse of the naive reading. Detail:
- Cell 7 prose: "IGAC covers **~86 %** of the basin" and "The two sources agree on only ~39 % of cells".
- Cell 8 executed output: `IGAC soil-texture coverage: 98.1% of basin` and `IGAC vs SoilGrids agreement 47%`.
- `src/build_soil_layer.py`:151-152 -> `final = np.where(igr>0, igr, sgf)`, masked to basin, and **that** merged
  array is what is written as `soil_family_igac.tif` (:172). Its :155 prints the IGAC-ALONE numbers.
- nb08 cell 8 reads `soil_family_igac.tif` into `soil` — i.e. **the merged raster** — then computes
  `100*np.mean(soil[bas]>0)` and labels it "IGAC soil-texture coverage". It is the **merged** coverage.
  Its agreement mask `m=(soil>0)&(sgf>0)&bas` likewise includes every SoilGrids-FILLED cell, where
  `soil == sgf` **by construction**, so the agreement is trivially inflated.
- **Measured read-only from disk** (no writes, no `data/processed/` modification):
  `minibacias.tif` 1500x705, 472,438 basin cells; `soil_family_igac.tif` coverage over basin = **98.06 %**;
  families 18.12 / 36.00 / 43.94 %. Reproduces the notebook's 98.1 / 18.1 / 36.0 / 43.9 exactly.
- **Algebraic reconciliation.** If IGAC-alone covers x of the basin and agrees with SoilGrids on A of ITS cells,
  the merged-mask agreement is `[x*A + (0.9806 - x)] / 0.9806`. Setting A = 0.39 and solving for the printed 0.47:
  `0.61x = 0.9806 - 0.4609` -> **x = 0.852**, i.e. ~85-86 %. **The prose's ~86 % / ~39 % are recovered to within
  a point.** Conclusion: the prose is right; the printed audit line is contaminated and mislabelled.
  Fix belongs in the CODE (cell 8), not in the prose.
- Honest limit: I cannot read IGAC-alone coverage directly from disk — `build_soil_layer.py` writes only the
  merged raster, so no IGAC-only artifact exists. The 86 % is recovered by algebra + the script's own print
  statement, not by re-rasterising the 18 department gpkgs (which I did not run).

### Step 5 — MEASURED: nb08 silently drops ~1.945 % of basin cells, and that drop accounts to 0.15 % for the
###          257,097-vs-251,724 km2 "different support" that docs 43/46/51 all wrestle with
- nb08 cell 10: `valid = basmask & (soil>0) & (land>0)`, then `frac = comp.div(comp.sum(1), axis=0)` —
  per-minibacia renormalisation to 1.0. Nothing is printed about how many cells were dropped; the QA cell 11
  does not mention it either.
- Measured: `(soil>0)&basin` = 463,251 of 472,438 cells = **0.98055**. `urh_fractions.csv` row sums are exactly
  1.000000 (min = max), so the dropped area is redistributed pro rata over the surviving URHs.
- Measured: `urh_ls2d.csv` sums **29,647,948 n_cells** over 32,782 rows / 8,672 minibacias / 24 URH codes.
  At native 90 m that is 29,647,948 / (472,438 x 64) = **0.98055** — the *same* fraction, to five decimals.
  So the land-cover part of the drop is nil to measurement precision; the drop is the soil-nodata mask.
- Measured: `minibacias.csv` area sum = **257,096.93 km2**; `urh_ls2d.csv` area_km2 sum = **251,723.51 km2**;
  ratio 0.97910. And 257,096.93 x 0.98055 = **252,096.6 km2**, i.e. within **0.15 %** of 251,723.51 (residual
  is latitude-dependent cell area — the dropped cells are not uniform in latitude).
- => The support difference that `src/mgb_sediment.py`:1061-1072 warns about, and that `docs/43` line 796,
  `docs/46` line 1470 and `docs/51` line 589 each describe as "a correct quantity on a different support", is
  **created by one undisclosed line in nb08 cell 10**. The docs handle it correctly; nb08 never discloses it.
  This is a missing-disclosure finding, NOT a claim that any doc number is wrong.

### Step 6 — MEASURED: nb08's `SCALE=8 preview` framing is stale, and SCALE controls nothing in nb08
- JSON scan of nb08: `SCALE`, `STREAM_THR`, `N_TARGET`, `OUTLET` appear in cell 1 (md), cell 2 (code, assignment
  only) and — for SCALE — cell 11 (md). **They are never read by any code cell after cell 2.** `demtif` is
  computed and a DEM tar is EXTRACTED in cell 2 and then never opened. `pyflwdir` is imported and never used.
- Cell 4 loads `data/processed/minibacias.tif` from nb07 — that is where the grid actually comes from.
- The grid it loads (1500x705, 8,672 minibacias) is the **adopted production** discretisation:
  CLAUDE.md Phase A "Minibacias (8,672)"; `docs/18`:90 "8,672 minibacias x 24 URH"; `docs/24`:56-58;
  `docs/PROGRESS.md`:41. The "preview" never became a `SCALE=1` run.
- nb07 (not mine) declares at its extract line 38 "the final product is **SCALE=1** (90 m)"; nb08 inherits the
  framing and cell 11 says "the mix sharpens at SCALE=1". `src/nbgen/make_nb12.py`:1719-1723 carries it forward
  as a live open check: "re-run notebook 08 at SCALE=1 for a sub-basin and compare the mix." It was never done.

### Step 7 — the structural-duplicate adjudication
Evidence that **08_urh is CURRENT / production**:
- writes `data/processed/urh_fractions.csv` (cell 10, executed: "8672 minibacias x 24 URH types"); file on disk
  1,322,742 bytes, mtime 2026-07-30 21:51, shape (8672, 25) with columns `mini` + the 24 codes 11..38.
- consumed by `src/mgb_hydrology.py`:991-996 (`build_topology(urh="urh_fractions.csv")`),
  `src/mgb_sediment.py`:920/960/1051 (engine geometry), `src/build_data_final.py`:95 (delivery packaging).
- the URH id convention is documented AS nb08's: `src/mgb_hydrology.py`:191 "URH id = soil_family*10 + land_class
  (notebook 08 step 4)", :203, :208; `src/mgb_sediment.py`:712.
- `src/build_soil_layer.py`:2 — "Build the basin-wide soil-texture-family layer used by notebook 08 (the URH)."
- `docs/PROGRESS.md`:41 credits nb08. `docs/37`/`43`/`46`/`51`/`52` all compute on `urh_fractions.csv`.
- `notebooks/05` cell 0 already names it: "The **production URH** ... is built basin-wide on the 8,672-minibacia
  grid by `notebooks/08_urh.ipynb` + `src/build_soil_layer.py` ... treat its numbers as illustrative, and
  notebook 08/09 as authoritative."
Evidence that **02_urh is DIDACTIC, superseded as method, still valid as pedagogy**:
- 6x6 hand grid, 2 soils x 3 covers, no file I/O of any kind, zero downstream consumers.
- last touched `e627d05` 2026-07-27 (the rename commit); nb08 last touched `44bafd5` 2026-07-30.
- it is the only place the Frechet-bounds argument is derived — deleting it would lose that.

**They are not competing implementations.** The chain is `02 (toy) -> 05 (30 m lower-Magdalena prototype)
-> 08 (basin-wide production)`. **nb05 already carries the banner; nb02 carries none. That asymmetry is the defect.**

**Recommended banner (DO NOT WRITE IN PHASE 1) — new markdown cell inserted as `02_urh.ipynb` cell 1, i.e.
immediately after the title cell 0, modelled on `05_landcover_soils_reclass.ipynb` cell 0:**

> **Portee — a lire avant de citer quoi que ce soit de ce notebook.** Ce notebook est **didactique** : il derive
> la mecanique des URH a la main sur une grille-jouet 6x6 (2 sols x 3 occupations = 6 URH). Il ne produit **aucun
> fichier** et **aucun autre notebook ni script ne lit ses resultats**. La **table URH de production** — celle qui
> alimente reellement le modele — est construite a l'echelle du bassin par **`notebooks/08_urh.ipynb`**
> (+ `src/build_soil_layer.py`) sur la grille des 8,672 minibacias : **24 URH = 3 familles de texture IGAC x
> 8 classes ESA WorldCover**, exportees dans `data/processed/urh_fractions.csv`. Deux differences a retenir :
> (1) l'identifiant de production est **`URH = famille_sol*10 + classe_occupation`** (nb08 etape 4,
> `src/mgb_hydrology.py`:191), **pas** la formule `(sol-1)*N_occ + occ` enseignee en section 2 ci-dessous ;
> (2) le croisement de production est fait en **Python pur (`rasterio`)**, **pas** par le plugin QGIS annonce en
> derniere section. La chaine est **02 (jouet) -> 05 (prototype 30 m bas-Magdalena) -> 08 (production bassin)**.
> Ce notebook reste la seule derivation des **bornes de Frechet** ; il est conserve pour cela.

**Companion banner recommended for `08_urh.ipynb`** (new markdown cell as cell 1, before the parameter table):

> **Status — this is the PRODUCTION URH notebook.** `data/processed/urh_fractions.csv` written by cell 10 is the
> file the water balance (`src/mgb_hydrology.py`) and the sediment engine (`src/mgb_sediment.py`) actually read;
> the URH id convention `soil_family*10 + land_class` defined in step 4 is the one hard-coded at
> `src/mgb_hydrology.py`:191 and `src/mgb_sediment.py`:712. `notebooks/02_urh.ipynb` is the didactic toy and
> `notebooks/05_landcover_soils_reclass.ipynb` is a lower-Magdalena 30 m prototype — neither feeds the model.
> The grid here is **not a preview**: the 1500x705 / 8,672-minibacia discretisation loaded in step 1 is the
> **adopted** Phase A discretisation, frozen and used by all of Phase B and Phase C. The `SCALE=1` re-run
> contemplated below was never performed.

**Also recommended (not written):** add nb06-nb19 to `notebooks/README.md`, and correct its
"05 ... the real-data version of notebook 02" line, which nb05's own cell 0 now contradicts.

### Step 8 — the docs point at the TOY, and nobody's numbered doc owns nb08
- `docs/03_methodology.md`:22-25 §1b: "URH generation (understood; see notebook 02) ... Worked out in
  `notebooks/02_urh.ipynb`." `docs/04_model_structure.md`:84-85: "The URH layer (the other structural input)
  is in `notebooks/02_urh.ipynb`." Both send a reader to the toy for the production layer.
  (`docs/00_INDEX` §3 marks doc 03 STALE and doc 04 **LIVE (framing)** — so the doc/04 pointer is a LIVE mis-direction.)
- `grep -rn "08_urh|notebook 08|nb08" docs/ notebooks/README.md src/`: **no numbered `docs/NN_*.md` cites nb08.**
  Only `docs/PROGRESS.md`:41, `src/*`, `src/nbgen/make_nb12.py`, `src/nbgen/make_nb13.py`, and agent journals.
  **nb08 is an orphan production notebook.**
- `notebooks/README.md` stops at nb05 and calls it "the real-data version of notebook 02" — which nb05 itself
  now contradicts. 06-19 are entirely absent from the README.

### Step 9 — CLAUDE.md Phase A "24 URH types, IGAC soils": does either contradict it?
- **nb08: CONFIRMS it, and is its source.** Cell 10 executed: `URH table: 8672 minibacias x 24 URH types`.
  Cell 8 makes IGAC primary with SoilGrids gap-fill only. 3 families x 8 classes = 24, all realised
  (measured: `urh_ls2d.csv` unique urh codes = 11,12,...,38, exactly 24).
- **nb02: does not contradict, but is silent and uses a DIFFERENT id convention.** nb02 cell 5 teaches
  `URH = (sol-1)*N_occ + occ`; the production convention on disk is `soil*10 + land` (nb08 cell 10,
  `src/mgb_hydrology.py`:191). A reader sent to nb02 by docs/03 and docs/04 learns the wrong formula.
- **nb02 cell 13 contradicts how the URH was actually built:** "le plugin MGB fait la superposition et le
  comptage par minibacia automatiquement" vs nb08 cell 0 "Pure Python (`rasterio` + `pyflwdir`), no QGIS."
  CLAUDE.md's "MGB-SA proper runs as a QGIS plugin" is about the *hydrology*, not the URH table.

### Step 10 — smaller things checked
- nb02 cell 8's comment promises "Deux dispositions differentes, MEMES marginaux, recouvrements differents"
  but only the upper bound is computed (`inter_max` = 60 = min(a,b)). The lower bound 30 is asserted, never shown.
  Arithmetic that IS shown is correct: 60 argile + 70 foret over N=100 -> [30, 60]; stacked -> 60.
- nb02 cell 10 toy composition is internally consistent: 11+13+11+1 = 36 = 6x6; every row sums to 1.0.
- nb08 cell 8's family shares 18.1+36.0+43.9 = 98.0, not 100 — the 1.94 % nodata again, unremarked.
- nb08 cell 10 PLOTS the basin-wide URH mix but PRINTS no numbers, so the cropland artefact that
  `make_nb12.py`:1720 later reports ("Cropland URHs total 1.4 % of basin area ... implausibly low ... a
  resampling artefact rather than a measurement") is invisible at the point it is created.
- Language: 01 and 02 are French; 03-19 are English. Shared with nb01, so not nb02's alone to fix.
- No notebook exists for the work of docs 55-59. Neither nb02 nor nb08 has a natural hand-off to that work —
  they are Phase A structure. The nearest relevant gap: docs/59 §5.2 contrasts "our 8,672 minibacias ... 24 URH
  types" against the second implementation's "7,929 unit catchments ... 12 HRU fractions", and nb08 — the
  notebook that made the 24 — says nothing about the comparison.

### Fix locations for Phase 2
`02_urh.ipynb` and `08_urh.ipynb` are **outside the 10-19 generated range**. There is no
`src/nbgen/make_nb02.py` or `make_nb08.py` (`ls src/nbgen/` shows generators for 10-19 only). Both are
hand-written, so every fix lands on the `.ipynb` cell index directly. One exception noted in the findings:
the `SCALE=8` open-check text that propagated into nb12 lives in `src/nbgen/make_nb12.py`:1719-1723 and must
be fixed there, never in `notebooks/12_model_input_assembly.ipynb`.

### What I refuse to conclude
- I will NOT say the 98.1 % is simply "wrong" — it is a correct number for the merged raster, wrongly labelled.
- I will NOT claim the ~1.945 % drop is the *sole* cause of the 257,097/251,724 gap. Measured agreement is
  0.15 %; the residual is unexplained here and the two artifacts also differ in resolution (720 m vs 90 m).
- I will NOT say the `SCALE=1` run "should" be done — that is a scope call for the owner of the Phase A docs.
- I could not measure IGAC-alone coverage from disk (no IGAC-only artifact is written); the ~86 % is recovered
  by algebra plus `src/build_soil_layer.py`:155, not by re-running the rasterisation.
- I did NOT execute any notebook, run any fit, or write to `data/processed/`. All disk reads were read-only.

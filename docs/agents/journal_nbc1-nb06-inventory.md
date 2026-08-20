# Journal — nbc1 / nb06_data_inventory coherence audit (T1, READ-ONLY)

Agent: nbc1-nb06-inventory. Date: 2026-08-13.
Owns: `notebooks/06_data_inventory.ipynb` (54 cells) and the stray `notebooks/06_data_inventory.html`.

## Assignment (restated)
Phase 1 = **T1 audit only**. Fix nothing. No notebook execution, no commits, no edits to
generators/src/docs. Produce: owning_docs, current_claims, narrative_role_should_be +
narrative_beats, inherits_from_previous / hands_to_next, executed_output_staleness +
engine_entry_points_called, findings (cell index + verbatim quote + severity + replace_with +
evidence + fix_location), cells_swept, not_settled.
Also: adjudicate the stray `.html` — regenerable export? byte-current? gitignored? in git?
Cross-check station/coverage numbers against docs/32 (79/79 classified, 28 mapped, 18 usable,
one Magdalena-trunk station 21237020) and docs/57 (B5: 46 geocoded, 43 in-basin, ZERO with
discharge). Narrative beats 1 and 9.

## Log

- [start] Listed `notebooks/` and the pre-extracted nbtext dir. Extract for my notebook is
  `.../scratchpad/nbtext/06_data_inventory.txt` (70,599 bytes). Notebook `.ipynb` is 858,473 bytes
  (Jul 29 03:47); the stray `.html` is 1,248,822 bytes (Jul 29 10:41) — **html mtime is AFTER the
  ipynb mtime**, first evidence it was exported from that ipynb rather than being stale-before-it.
  nb06 is in the **01-09 hand-written** range, so fix_location is the `.ipynb` cell index.
  Confirmed: `ls src/nbgen/` shows generators for **make_nb10 … make_nb19 only** — there is no
  `make_nb06.py`, so the `.ipynb` is the source of truth for this notebook.

### 1. The stray `notebooks/06_data_inventory.html` — adjudicated with evidence

| question | measurement | answer |
|---|---|---|
| in git? | `git ls-files notebooks/` lists 19 `.ipynb` + `README.md`, **no `.html`**; `git log -- notebooks/06_data_inventory.html` is **empty** | **never committed** |
| gitignored? | `git check-ignore -v` -> `.gitignore:16:notebooks/*.html` | **yes, ignored** |
| what regenerates it? | no script in `scripts/` or `src/` runs `nbconvert --to html`; `docs/20` documents only `--to notebook --execute`. Regenerate by hand: `python3.10 -m nbconvert --to html notebooks/06_data_inventory.ipynb` | **hand-run nbconvert, no automated producer** |
| content-current with the `.ipynb`? | `.ipynb` has **54 cells**; html has **54** `class="jp-Cell "` divs. Every run-specific stdout string in the ipynb is present verbatim in the html: `TOTAL discharge stations: 167`, `TOTAL sediment stations: 77`, `1,133,522`, `1,130,236`, `269,305`, `Fitted 33 rating curves`, `31 / 108`, `+1.70`, `-1.02`, and even the sandbox root `epic-sleepy-mendel`. 11 png outputs in the ipynb vs 12 base64 png tags in the html (the extra is the nbconvert logo) | **yes — a faithful export of the tracked `.ipynb`, same execution** |
| mtime order | `.ipynb` Jul 29 03:47 -> `.html` Jul 29 10:41 | export postdates the notebook |
| does anything depend on it? | `docs/16` §7 item 8 lists it among files a blocked deletion never removed. `docs/38` §5 says the **PDF** `Explanation_script_MGB_SA_Magdalena.pdf` is *"generated from notebooks/06_data_inventory.ipynb"* and is **actively cited twice by docs/35**, so the *PDF* must stay; nothing requires the `.html` | **the html itself is disposable; the PDF is not** |

**Verdict: regenerable, content-current, untracked, gitignored, no automated producer, nothing
depends on it.** Safe to delete; if kept, it is a convenience export only. It is *not* a second
source of truth. (Deletion is a Phase-2 decision — I changed nothing.)

### 2. Sweep of the 54 cells — read the extract end to end (lines 1-972). cells_swept = 54.

No kill-list number appears anywhere in nb06: greps for
`0.333|0.421|2.37|3.00x|104.8|82.8|126.1|99.7|0.1644|0.465|0.00216|0.0209|0.0104|348.4|11.8|SDR|LS 2-10|2x under`
return **zero hits**. No `t/km2/yr` anywhere — the only `km²` is `A_thr` "e.g. 10-100 km²", a
stream-initiation threshold, **not** a yield. **No yield-embargo violation, no kill-list
violation.** nb06 is entirely pre-Phase-B; its defects are staleness, one real code bug, and
narrative gaps.

### 3. Engine

`grep -E "mgb_sediment|import src|from src|sys.path"` over the extract: **zero hits**. nb06 imports
only os/glob/csv/pathlib/collections/pandas/matplotlib/numpy/rasterio/xarray.
**engine_entry_points_called = [] ; staleness re: the `V4_dg` engine default = N/A (no engine
call).** The outputs are stale for four *other*, measured reasons — §5.

### 4. MEASURED: the cell-25 pairing bug (the strongest finding in this notebook)

Cell 3's `scan()` stores the **raw date string** (`o['days'].add(r['Fecha'][:10])`). Cell 25 then
intersects `Q[c]['days'] & S[c]['days']` — raw string against raw string. The files use **two
formats** (the notebook's own cell 23 gap #3 says so). Measured on disk, read-only:

```
caudal/caudal_cundinamarca.csv : 74,622 rows, 100 % ISO   -- has 21237020 (9,073 rows)
sedimento/ssc_cundinamarca.csv : 39,815 rows, 100 % DMY   -- has 21237020 (6,596 rows)
```

Reproducing cell 25's own algorithm against the same folders:

```
Q stations 167 | S stations 77 | both 33
with >=30 RAW-STRING common days : 31      <- matches the notebook's printed "31"
with ZERO  RAW-STRING common days:  2  ->  21197010 EL PROFUNDO, 21237020 ARRANCAPLUMAS - AUT
with >=30 NORMALISED common days : 33      <- matches cell 46's printed "Fitted 33 rating curves"
recovered: 21197010 -> 5,817 common days ; 21237020 -> 6,400 common days
CORRECTED cell-25 line: both 33 | >=30 common days 33 | in 2011: 15 | in 2015-16: 13
```

So the notebook's own internal contradiction (cell 25 "31" vs cell 46 "33") is fully explained, and
the two stations silently dropped are **exactly the two that matter most**: `21237020`
ARRANCAPLUMAS is *"the only Magdalena-trunk SSC station in the entire network"* (`docs/32` §R6) and
`21197010` EL PROFUNDO — **both classified `usable`** in docs/32 §R6.1. The data-inventory
notebook's pairing table structurally hides the single mainstem station, and the next markdown cell
then says the mainstem has no sediment. Beat 1 in miniature: a screen that cannot see what is absent.

### 5. MEASURED: why the executed outputs are stale (four independent reasons)

1. **Population undercount.** nb06 globs `*.csv` only. On disk: `caudal/` = **17 csv + 16 zip**
   (+ an `OMAR_CAUDAL` dir), `sedimento/` = **16 csv + 8 zip**. The consolidation pipeline
   (`src/build_discharge_gauges.py`; docs/17 §2.1: "45 DHIME discharge parts = 17 loose CSVs + 16
   top-level zips + 12 …") reads the zips too. nb06 prints **167 / 77** stations;
   `data/processed/discharge_inventory.csv` = **192 rows** (docs/17 §1) and
   `data/processed/sediment_inventory.csv` = **79 rows** (docs/32 §0) — both counted by me on disk.
   nb06's numbers are right for what it read and **stale for the project**.
2. **Foreign execution root.** Cell 3 prints
   `Repo root : /sessions/epic-sleepy-mendel/mnt/magdalena-mgb-sed` — a cloud sandbox, not the
   documented local box. (`scripts/build_report_pdf.py`, untracked, hard-codes the same root.)
3. **Predates the domain correction.** `docs/15` locks the east edge at **-72.3** (strip downloaded,
   `mosaic_era5.py` -> `era5land_ext_*.nc`). nb06 cells 51-53 still print `-72.90` and call it "the
   pending DOMAIN decision" / "the one open item".
4. **Predates the soil-source switch and the precipitation acquisition.** nb09 cell 0 verbatim:
   *"Both come from the **IGAC field survey** … **not** from SoilGrids pedotransfer."* CLAUDE.md
   Phase A: "URH (24 types, **IGAC soils**)". And `data/raw/observed/precip/` is dated **Jul 31 –
   Aug 2**, i.e. *after* nb06's last run (Jul 29 03:47) — so nb06's claim to inventory "*every*
   dataset collected so far" now omits the 294-gauge IDEAM precipitation network that the adopted
   v2 forcing is built from (docs/16 §1, §4.1). Correct when written; a hole now.

### 6. MEASURED: nb06 is an upstream *producer*, and its artifacts are cited in a frozen registration

Cell 29 writes `stations_{discharge,sediment}.csv`; cell 46 writes `rating_curves.csv`.
- nb07 reads `stations_discharge.csv` (nb07 extract line 314).
- `docs/31` §0 and **`docs/32` §5 (a FROZEN pre-registration)** both cite *"median fleet R² ≈ 0.5
  (`rating_curves.csv`: 0.54 / 33 pairs)"* as the registered expectation for C1.5; docs/32 §R5
  measured 0.546 over 30 era-fits against it.
Re-executing nb06 would silently rewrite three consumed artifacts from the **undercounted** 167/77
population. Recorded as a reproduction hazard; not acted on.

### 7. Cross-checks performed against the owning docs

- `docs/32` §0 (79 rows / 28 mapped / 24 calibration-safe / 46 unmapped) and §R6 (6 usable + 12
  usable-with-caveat = **18**; 8 mainstem of 28; `21237020` the only Magdalena-trunk station, class
  **usable**, n 2011 = 91, n 2015-16 = 195, R² 0.556 on n=6400).
- `docs/57` §1–§3 (46/46 geocoded, 43 in-basin, **0 of 43** with same-code discharge; 18/18 usable
  SSC stations do have it; concentration contrast 11/16, median 1.38).
- `docs/00_INDEX` "Forcing versions — v1 / v2 / v3, stated once": **v2 is GAUGE-ONLY**, adopted;
  **v3 (CHIRPS-merged) does not exist**. So nb06's "ERA5 + IDEAM (bias-corrected)" precipitation
  plan was never executed.
- `docs/15` (domain box locked at -72.3), `docs/16` §4.1 (zero-suppression, 70/294),
  `docs/17` §1 (192 discharge stations), `docs/38` §5 (nb06's PDF descendant is superseded but
  must stay on disk), nb09 cell 0 (IGAC, not SoilGrids), notebooks/README.md (documents 01-05 only).

### 8. Refused to conclude

- I did **not** conclude nb06's 167/77 are "wrong". They are correct for the `*.csv` subset it read
  and stale relative to the consolidated inventories. Stated that way in the findings.
- I did **not** re-execute anything, did not touch `data/processed/`, and edited no file but this one.
- Could not settle whether the 16 caudal / 8 sedimento ZIPs duplicate or extend their CSV siblings
  (would need unzipping into a temp dir) — so I cannot say how much of the 167→192 and 77→79 gap is
  the zips versus other DHIME parts. Recorded as an open item.

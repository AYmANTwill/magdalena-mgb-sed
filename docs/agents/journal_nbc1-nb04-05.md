# journal_nbc1-nb04-05 — notebook coherence T1 audit (READ-ONLY)

**Agent:** nbc1 · **Date:** 2026-08-13 · **Phase:** T1 audit only, FIX NOTHING.

## Assignment
Audit `notebooks/04_real_dem_eda.ipynb` (10 cells) and
`notebooks/05_landcover_soils_reclass.ipynb` (13 cells).
Both hand-written (no `src/nbgen/make_nb04.py` / `make_nb05.py` — verify).
- nb04 explains WHY the lower-Magdalena box cannot be delineated. Check its bounding box against
  docs/15 (locked domain, east edge -72.9 -> -72.3); docs/00_INDEX §3 records docs/05 and docs/08
  carry a STALE bbox — check whether these notebooks inherited it.
- nb05 crosses WorldCover + IGAC soils into the real URH map. Narrative beat 1.

Deliverables: owning_docs, current_claims, narrative_role/beats/inherits/hands, executed_output_staleness
(+ engine entry points), findings (cell index + verbatim quote), cells_swept, not_settled.

## Log

- [start] Created journal. Listed notebooks/ and nbtext/ extracts — both target extracts exist:
  `04_real_dem_eda.txt`, `05_landcover_soils_reclass.txt`.

### What I read (in full)
- Extract `04_real_dem_eda.txt` — all **10** cells (0–9), 6 md / 4 code, `cells_with_error=0`.
- Extract `05_landcover_soils_reclass.txt` — all **13** cells (0–12), 7 md / 6 code, `cells_with_error=0`.
- `docs/15_domain_correction.md` (whole), `docs/00_INDEX.md` §3 doc table, `notebooks/README.md`,
  `docs/05` §status, `docs/08` §status+§1, `docs/35` §§58–70, `docs/38` §4.1–4.2,
  `docs/59` §5.1–5.4 + the X-table (X6, X7), `docs/16` (grep only), `docs/20` (grep only),
  extracts of nb06 / nb07 / nb08 (targeted greps + heads) for the chain checks.

### What I measured (commands, not assumptions)

1. **No generator exists for either notebook.** `ls src/nbgen/` → `make_nb10.py … make_nb19.py` only.
   ⇒ `fix_location` for every finding below is the **.ipynb cell index** (correct per the brief for 01–09).
2. **Kill-list grep over both extracts returned NO HITS.** Pattern set:
   `t/km2|t/km²|km2/yr|0.333|0.421|2.37|3.00x|SDR|LS 2-10|11.8|Buarque|0.1644|0.465|k_min|under-erosive|cp_revision|V4_dg|ls2d`.
   ⇒ **No yield-embargo violation, no retired-number reuse, no reconstructed materiality bar,
   no withdrawn direction** in nb04 or nb05. Recorded as a clean negative.
3. **Engine entry points: none.** nb04 imports `os, tarfile, numpy, rasterio, matplotlib, pysheds`;
   nb05 imports `glob, os, re, shutil, tempfile, zipfile, numpy, pandas, geopandas, rasterio(.warp),
   matplotlib`. Neither imports `src/mgb_sediment.py` nor any sediment/LS code, so neither has an
   `ls2d_column` and neither carries a `cp_revision`. `executed_output_staleness = N/A`
   *with respect to the `c3fdb55` engine-default move* — but see 8 below for a different staleness.
4. **Execution counters** (`python3.10 -c` over the raw .ipynb):
   nb04 = 1, 2, 3, **5** (exec 4 absent → not a clean linear Run All);
   nb05 = 1, 2, 3, 4, 5, 6 (clean linear).
5. **Git history**: nb04 has exactly **one** commit, `9bcd416` 2026-07-29. nb05 has two,
   last `0388930` 2026-08-02 ("nb05 fix"). Both predate `57f9761` / `c3fdb55` — irrelevant here
   (no engine), but it means neither has been touched in ~11 days of Phase C.
6. **The bbox question, settled.** nb04 cell 3 prints `Bounds : W -75.40 E -73.70 S 8.20 N 11.30`.
   `docs/08_download_guide.md:5` reads *"Current pilot region (lower Magdalena, near the sea):
   **Xmin −75.4, Xmax −73.7, Ymin 8.2, Ymax 11.3**"* — **the identical box**, and docs/08's own
   line 3 banner marks it SUPERSEDED. `docs/15` locks `Xmin −77.0 Xmax −72.3 Ymin 1.4 Ymax 11.4`;
   nb08 cell prints `domain lon[-77.0,-72.3] lat[1.4,11.4]` ✓. So **yes, nb04 and nb05 inherited
   docs/08's stale bbox** — but *only* nb05 carries a status banner about it (its cell-0
   "Scope — read this before quoting any number below"). **nb04 carries none**, and still calls the
   box *"current"*.
7. **`data/raw/dem/cop30_dem.tar.gz` DOES NOT EXIST.** `ls -la data/raw/dem/` →
   `.gitkeep`, `rasters_COP90.tar.gz`, `rasters_COP90.tar.gz.properties`,
   `rasters_COP90_Correcte_Corrdinatzs.tar.gz`. nb04 cell 1 hard-codes that path. The notebook only
   survives because `data/processed/cop30_dem.tif` (243,750,698 B, Jul 28 05:48) already exists and
   the `if not os.path.exists(dem_tif)` guard skips the extraction — and `data/` is **gitignored /
   regenerable** per CLAUDE.md. ⇒ nb04 is **not reproducible from the repo as it stands**, and nb05
   inherits the break (`assert os.path.exists(DEM_TIF)`).
8. **The hot-journal warning in nb05 cell 12 is now FALSE.** `ls data/processed/` →
   `soils_magdalena_merged_4326.gpkg-journal.**DISABLED**` (512 B, Jul 28 04:04). The quarantine
   nb05 demands has already been done; the ⚠ block reads as a live hazard and is not one.
9. **"the merged file has no remaining consumer" is contradicted.** `docs/59` §5.1 lists
   `soils.merged_polygons: soils_magdalena_merged_4326.gpkg` among the inputs R2's
   `config/data_sources.yaml` names — *"present | same filename"*. Deleting the pair, as nb05
   advises, would destroy a named cross-implementation provenance artifact.
10. **nb05's raster products ARE consumed** — not by a notebook, but by
    `src/build_data_final.py:79` (`"landcover_hydro_30m.tif": "03_landcover/processed"`), i.e. they
    ship in the `data_Final/` delivery bundle; and `docs/agents/journal_x59-overlap.md:130` records
    R2's config naming *"the 30 m landcover_hydro product in data_Final"*. nb05's sentence *"No
    other notebook or script reads this notebook's rasters"* is true for notebooks, false for
    `src/`. (nb04's `cop30_dem.tif` / `dem_coarse.tif` likewise: `build_data_final.py:77–78`, and
    `docs/53`:380 lists `cop30_dem.tif` as a read-only input to the Δ_shape cell pass.)
11. **Consistency checks that PASSED** (recording the negatives too):
    - nb05 `LC_MAP = {10:1,20:2,30:3,40:4,50:5,60:6,70:6,80:7,90:8,95:8,100:6}` vs nb08
      `LC_TO_CLASS = {10:1,20:2,30:3,40:4,50:5,60:6,70:6,100:6,80:7,90:8,95:8}` — **identical**.
    - nb05 `LC_COL` vs nb08 `CLASS_COL` — **byte-identical hex strings** (`#1a7f37 … #5FA8A0`).
      nb05's claim *"IDENTICAL to notebook 08 on purpose"* holds.
    - nb05's supersession pointer (*"8,672-minibacia grid by notebooks/08_urh.ipynb +
      src/build_soil_layer.py … texture family"*) matches nb08's printed
      `URH table: 8672 minibacias x 24 URH types` and nb08 cell 1's 3 texture families (3×8=24 ✓).
    - nb05 "18 in-basin IGAC department maps" — `ls data/raw/soils/` has **19** `suelos_*.gpkg`,
      minus `laguajira` = 18 ✓.
    - nb05 arithmetic: 1,440/6,120 = 23.53 % ✓; the −75.4001→−73.7001 box west of −75.0 is
      0.4° / 0.0002778° = 1,440 columns ✓; 9 soil × 8 lc = 72, "62 of 72 present" ✓.
    - nb04 arithmetic: 6120×11160 = 68.3 M ✓; 1.70°/0.0002778 = 6120 ✓; 3.10°/0.0002778 = 11160 ✓;
      1341 × (270²/1e6) = 97.8 → "98 km²" ✓; f=9 → 680 × 1240, matching `docs/35` §59's
      measured `dem_coarse.tif (680 × 1240)` ✓.
    - Basin area 257,097 km² in nb05 cell 0 matches `docs/00_INDEX`:24, `docs/16`:34,
      `docs/17`:67 and `docs/59` §5.1's 257,096.930 ✓ — **not** a yield, so not embargoed.
12. **The `~250 M cell limit` is uncited.** nb04 cell 2 uses it as a check. Repo repeats:
    `docs/00_objectives_and_hypotheses.md:50`, `docs/05:12` (both STALE docs). The only primary
    source, transcribed at `docs/38` §4 / :243 from `Explanation_script_MGB_SA_Magdalena.pdf`, is
    **qualitative** — *"30 m over the whole basin exceeds the tool's cell limit"*, no number.
13. **nb04's verdict was independently re-measured and strengthened, and nb04 was never
    back-annotated.** `docs/35` §58–59: only **1,506 of 8,672 minibacias (17.4 %)** fall inside the
    processed 30 m DEM *and they are the flat ones* (proxy channel slope median 0.0056 m/m).
    That is the quantitative form of nb04's qualitative "the box is not delineable", and it is also
    half the evidence `docs/59` **X6** asks for.
14. **The forward chain nb04 → nb07 is real but unwritten.** nb07 cell heads print
    `Step 1 — conditioned DEM (COP90)`, glob `rasters_COP90*Corr*.tar.gz`,
    `STREAM_THR = 200 km²`, `N_TARGET = 12000`, and
    `minibacias after refinement: 8672 | area mean 30 median 26 km2`. So nb04's "checklist for the
    redo" **was executed** — at 90 m in pyflwdir, not at 30 m through IPH-HydroTools. nb04 points
    at none of it.
15. **`docs/59` X7 is a hand-off nb05 structurally cannot honour.** X7 asks for *"a per-code
    histogram from notebook 05 over the basin mask"* for WorldCover 60/70/100 (class 6 = 0.196 %
    of area but **14.78 %** of modelled erosion). nb05's tile filter `overlaps_dem()` tests against
    `DEM_BOUNDS` = the lower box, so it can never pull tiles south of lat 6; and its `LC_MAP`
    collapses 60/70/100 to id 6 before any histogram is taken.
16. **`docs/38` §4.1 flags nb05's SoilGrids claim as un-re-derived.** Three unreconciled versions
    exist: nb05's qualitative *"the great majority … 'Fine'"*; docs/38's transcribed
    *49 % agreement / ~99 % Fine / Coarse 19 % / Medium 32 %*; and `docs/59` §5.1's R2 config
    *"SoilGrids classes 95% of the basin as Fine against IGAC's 38%"*. docs/38 says explicitly:
    *"re-measure from notebook 05 before quoting them in a report."*
17. **nb05's "Still open" items are orphans.** Grep of `docs/31` (open register), `docs/47`
    (O1–O12), `docs/41`, `docs/37` finds **no** tracked item for period-matched land cover.
    docs/41 cites Corine only as a *C-factor literature* source (Pacheco et al. 2019), not as a
    period-matched raster. The item lives only inside nb05.

### What I refused to conclude
- I did **not** open `rasters_COP90*.tar.gz` to test whether `cop30_dem.tif` is recoverable from it —
  the resolutions differ (0.000278° vs 0.000833°), so it almost certainly is not, but I did not
  measure it. Left as an open item.
- I did **not** re-run nb05's share table to check whether the class shares changed after the
  four-tile fix (Phase 1 forbids executing notebooks). The printed shares are from the *fixed*
  run (`0388930`, "nb05 fix", exec 1–6 linear, coverage assertion passing at 100.00 %), so I take
  them as current — but I verified that by execution-counter and commit message, not by re-running.
- I did **not** adjudicate the three SoilGrids percentage sets against each other. docs/38 says to
  re-measure; that is Phase-2/report work, not an audit call.
- I did **not** claim nb04 is the cause of `docs/59` X6. nb04's own product is genuinely 30 m
  (0.000278°, printed); the COP30-vs-COP90 conflict lives in
  `data/processed/model_inputs_v2/manifest.json` against nb07, neither of which I own.


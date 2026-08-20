# Journal — nbc1: notebook coherence T1 audit, nb07 + nb09

Agent: nbc1-nb07-09. Phase 1 = **T1 AUDIT ONLY, READ-ONLY**. No fixes, no notebook execution,
no git writes. The only file I write is this journal.

## Assignment (as given)
Audit `notebooks/07_preprocessing_minibacias.ipynb` (21 cells) and
`notebooks/09_soil_parameters.ipynb` (15 cells). Hand-written, no generator — fix_location is the
.ipynb cell index. Specific asks:
- Do these notebooks state or imply a per-gauge / per-minibacia **area is reliable**?
  (catchment areas are the yield-embargo source, docs/23 §13.2)
- Does any **t/km2/yr** appear anywhere?
- Check the **K unit system** (docs/42 G-series guard) and whether nb09 states which unit
  system it writes.
- Narrative beat 1 ("Inputs are not innocent").

## Log

### 2026-08-13 — start
Created journal. Listed the pre-extracted nbtext directory; both my extracts exist:
`07_preprocessing_minibacias.txt`, `09_soil_parameters.txt`.

### Read both extracts in full (21 + 15 cells = 36 cells, 100 % sweep)
`nbtext/07_preprocessing_minibacias.txt` (382 lines) and `nbtext/09_soil_parameters.txt` (368 lines).
Both fully executed: nb07 `code_unexecuted=0 cells_with_error=0`, nb09 the same.

### MEASURED — kill-list / embargo greps over both extracts (all NEGATIVE)
```
grep -nEi "t/km|km2/yr|km²/yr|Mt/yr|yield"   -> only nb09 c0: "Directly multiplies the sediment yield" (word, not a unit)
grep -nEi "mgb_sediment|cp_revision|ls2d|V4_dg|ls2d_hs|import src|from src"  -> ZERO hits in both
grep -nE  "0.333|0.421|2.37|11.8|0.25146|104.8|82.8|126.1|99.7|129.384|75.3235|0.1644|0.465|
           0.00216|0.0209|0.0104|348.4|1.34762|299.5387|248.7298"            -> ZERO hits in both
```
=> **No yield-embargo violation. No kill-list number. No engine call in either notebook.**
=> `executed_output_staleness` for the *engine default LS move* (`c3fdb55`) is **N/A** for both:
neither notebook imports `src/mgb_sediment.py`, neither has a `cp_revision`, neither prints a load.

### Owning docs located (grep across docs/)
- nb07: no numbered doc owns the delineation itself. Referenced by `docs/18` §(D8 network),
  `docs/30` §204, `docs/31` §314/§347, `docs/59`:529, `docs/PROGRESS.md`:40. The *consequence*
  doc is **`docs/23` §13.2** (area disagreement) — read below.
- nb09: **`docs/42` §3.3 line 157** and **`docs/37` row 2** both treat *nb09 §4* as THE authority
  on the K unit system; `docs/30`:122, `docs/31`:59, `docs/35`:604 also cite it.

### docs/23 §13.2 — read verbatim. The binding sentence:
> "**The median agrees to ~1 % while individual gauges disagree wildly, which means neither
> derivation is trustworthy per gauge.** Two independent D8 delineations on different DEMs
> disagree by more than 2x on a third of a shared 85-gauge sample."
> "a sediment yield in t/km2/yr inherits this error one-for-one"
31 of 85 beyond 2x; p05/p95 ratio 0.15 / 8.68. docs/23 also states the basin as **257,097 km2**
while nb07 prints **257,808 km2** (Δ 711 km2, 0.28 %) — noted, not yet a finding.

### MEASURED — the shipped artifacts (read-only, no notebook executed)
```
rasterio  data/processed/minibacias.tif
  bounds  left=-77.0004167 bottom=1.4004167 right=-72.3004167 top=11.4004167
  shape   1500 x 705      res 0.0066666667 deg  (= 8 x 3 arcsec)
pandas    minibacias.csv          8672 rows  sum area_km2 = 257096.9  mean 29.65  median 25.58
          minibacia_soil_params.csv  8672 rows  cols id,Wm_mm,K,depth_cm,texture,drainage,area_km2,downstream
          K min/median/max 0.019 / 0.03055 / 0.0495   CV 0.2289   Wm mean 84.8
          gauge_minibacia.csv     159 rows  unique minibacia 153  representative 152
                                  12 gauges in 6 collided minibacias
          gauge_minibacia_remap_report.csv  159 rows: kept 129 / remapped 20 / excluded_distributary 10
          stations_discharge.csv 167 rows;  stations_discharge_coords.csv 166 rows with lon/lat
sha256    minibacia_soil_params.csv = 6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1
          398,698 bytes -> MATCHES docs/59 §5.1 byte-identical claim EXACTLY.
```

#### What those measurements settle
1. **The shipped minibacia grid is the SCALE=8 PREVIEW (~740 m), not SCALE=1 (90 m).**
   1500x705 @ 0.0066667 deg is exactly nb07's `SCALE = 8` run. nb07 c2 says *"the final product is
   `SCALE=1` (90 m)"*. That run never happened; Phases A/B/C sit on the preview.
2. **nb07's DEM is COP90 — X6 (docs/59 §5.4) is settleable from geometry.** Box
   -77.0/-72.3/1.4/11.4 == docs/15's COP90 download bbox verbatim, and 0.0066667/8 = 0.000833 deg
   = 3 arcsec = COP90. The manifest's "COP30" is the wrong statement. NOTE: nb07's *executed
   output* does NOT settle it — it prints `DEM : /sessions/epic-sleepy-mendel/tmp/output_hh.tif`,
   a foreign sandbox path. Only the glob `rasters_COP90*Corr*.tar.gz`, the plot title and the
   geometry do.
3. **nb07's QA gate is on a number it does not export.** c11 prints 257,808 km2 (pyflwdir
   `upstream_area`); the exported table sums to **257,096.9** (constant-cosine `cell_km2`) — which
   is the project headline (docs/00_INDEX:24, docs/23 §13.2, docs/59 X6). Delta 711.1 km2 = 0.276 %.
   Latitude ramp of the constant-cosine: cos(6.4004)=0.9937671 used everywhere vs true
   cos(1.4004)=0.9997013 (-0.59 %) and cos(11.4004)=0.9802697 (+1.38 %). **This is ~1 %, NOT the
   >2x per-gauge disagreement — I refuse to blame the embargo on it.**
4. **`gauge_minibacia.csv` is NO LONGER nb07's output.** `src/fix_gauge_minibacia_mapping.py:223`
   rewrites it **in place**. Disk = 12 gauges in 6 collided mb / 153 unique; nb07 c17 printed
   13 gauges in 6 / 152 representative. Re-running nb07 would silently destroy the re-snap.
5. **`minibacia_soil_params.csv` IS still nb09's output** — hash verified. nb09's printed numbers
   (Wm 85 mm, K 0.032, 8672 rows) reproduce the disk file. **nb09 is not stale.**
6. **`K` carries NO unit in the file nb09 writes.** `Wm_mm` and `depth_cm` do. nb09 §4 markdown
   states SI + x0.1317 + `t.ha.h.ha-1.MJ-1.mm-1`; the CSV and the c13 summary print do not.
   Downstream cost, measured: docs/35 "**Reason 2 — the `K` unit system, a fourth error that §9.1
   did not see**"; docs/42:157 `k_factor = 7.593014` graded *"IDENTIFIED — pinned to <=1.3 %
   rounding residue"*, recovered by inverting nb09's prose. docs/42 §3.2 then registers the K unit
   system as **NOT identifiable** — "they are Pi".

### MEASURED — `src/build_soil_layer.py` refutes nb09's headline
Lines 7-8 (docstring) and 150-151 (code):
```
SoilGrids (same USDA triangle, collapsed to 3 families) fills the ~14 % of the basin IGAC does not cover.
final = np.where(igr > 0, igr, sgf)          # IGAC where present, SoilGrids elsewhere
```
So `soil_family_igac.tif` — nb09's `fam` — is a **hybrid**. nb09 c0 "derived **entirely from
IGAC**" and c14 "neither inherits the SoilGrids near-uniform-clay artefact" are both false on
~14 % of the basin, and c14 contradicts itself in its own last paragraph. c2's printed
"texture stated 98%" is the *hybrid* coverage, not IGAC's (~86 %).

### MEASURED — nb09 deleted a real negative result (git 9a3810c, 2026-07-30)
`git show 9a3810c^:notebooks/09_soil_parameters.ipynb` old cell 11 output, verbatim:
```
28 sediment gauges matched to a minibacia with upstream K
Pearson r(upstream K, log a) = 0.05  ->  INCONCLUSIVE (confounders dominate)
NOTE (honest): ... A near-zero r means those confounders dominate over K here -- it does
      NOT show K is wrong.
```
The current c10 keeps only the unsupported paraphrase *"and indeed it returns pure noise"* —
no r, no n — and the honest verdict was INCONCLUSIVE, not "noise". It was replaced by
`okK = all(Klit[k][0] <= KBASE[k] <= Klit[k][1] ...)` -> `True`, a band the notebook itself
chose around its own three constants. House rule says a negative result is publishable here.

### MEASURED — nb07 promises a `slope` column that no artifact carries
c20: *"export the **minibacia table** (id, area, downstream link, slope)"*.
`minibacias.csv` cols = id,area_km2,downstream. `minibacia_soil_params.csv` has no slope.
Corroborated: `docs/PROGRESS.md`:93 "(slope from nb07 DEM, **not shipped**)";
`docs/31`:347 "slope — **to be derived from the nb07 DEM chain**";
`docs/agents/review_2026-08-10_docs31.md`:201 "absent from `parameters.npz`,
`minibacia_soil_params.csv`, `minibacias.csv`".

### Commit dates (git log)
b4a1230 2026-07-30 add nb07 ... (nb07 touched ONCE, never since)
9a3810c 2026-07-30 nb09: replace uninformative K-vs-rating-curve check ...
8998eb3 2026-08-02 gauges: re-snap by drainage-area matching  <- AFTER nb07, overwrites its output
c3fdb55 2026-08-12 engine default LS -> V4_dg                 <- irrelevant: neither nb calls the engine

### What I REFUSE to conclude
- I will NOT call the ~1 % constant-cosine area ramp the cause of the yield embargo. Measured
  magnitude ~1 %; docs/23 §13.2's disagreement is >2x on 31/85. Different order of magnitude.
- I will NOT state IGAC's exact basin coverage %. `build_soil_layer.py` prints it at run time and
  the docstring says "~14 %" uncovered; I did not rerun the script and the raw IGAC gpkg parse is
  not cheap. Recorded as an open item, not guessed.
- I will NOT claim the `Klit`/`Alit` envelopes are wrong. They are dimensionally self-consistent
  (undo x0.1317 -> US 0.038-0.228 / 0.228-0.494 / 0.152-0.266, which bracket sand/silt-loam/clay).
  The defect is attribution (no table/page), not arithmetic.
- I will NOT attribute the 152-representative-vs-153-unique-minibacia anomaly on disk to nb07.
  It appears in the file AFTER `fix_gauge_minibacia_mapping.py` rewrote it. Open item.

### Sweep accounting
nb07: cells 0-20 examined = **21 of 21**. nb09: cells 0-14 examined = **15 of 15**. Total **36**.
Every finding below carries a 0-based cell index and a verbatim quote from the extract.

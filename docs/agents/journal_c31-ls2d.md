# Journal: c31-ls2d — build LS2D topographic factor (last static MUSLE input)

GOAL: Desmet & Govers (1996) 2-D LS per raster cell from existing conditioned DEM /
D8 / flow accumulation on disk; aggregate area-weighted to per-minibacia and per-URH;
report 4 sanity gates with numbers; figure figures/deck/gen_ls2d.png.

## Step checklist
- [ ] S1 read nb07 chain, locate conditioned DEM / D8 / flow accumulation rasters on disk
- [ ] S2 inventory minibacia + URH rasters/tables needed for aggregation
- [ ] S3 implement scripts/c3/ls2d.py (D&G 1996, stated m/n convention)
- [ ] S4 run it; report gates (positivity/NaN, basin median vs 2-10, Andes vs floodplain, flat cells)
- [ ] S5 figure figures/deck/gen_ls2d.png
- [ ] S6 structured report

## Log
- S0 journal created.

### S1 — nb07 chain read (DONE). KEY FINDING: the rasters the task assumes are NOT on disk.
`notebooks/07_preprocessing_minibacias.ipynb` builds flow routing **in memory only**:
- cell 3: DEM = `output_hh.tif`, extracted from `data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz`
  into the system temp dir. It IS on disk: `C:\Users\...\Temp\output_hh.tif`, 5640 x 12000 float32,
  EPSG:4326, bounds (-77.0004, 1.4004) .. (-72.3004, 11.4004), ~90 m.
- cell 5: `flw = pyflwdir.from_dem(...)` — pit filling + D8 happen here, **never written to disk**.
- cell 7: `upa = flw.upstream_area('km2')` — flow accumulation, **never written to disk**.
- cell 19 exports ONLY `minibacias.tif` + `minibacias.csv`.
`find . -iname "*.tif"` confirms: no D8 raster, no flow-accumulation raster, no conditioned-DEM raster
anywhere in the repo. So "do not recompute them" cannot be honoured literally — D8 + accumulation MUST
be recomputed from the same DEM with the same tool (pyflwdir 0.5.11) to reproduce nb07's routing.
DECISION: recompute D8 + accumulation with pyflwdir from the SAME `output_hh.tif`; do NOT re-delineate
minibacias (reuse `minibacias.tif` as-is). Deviation recorded here and in the final report.

### S2 — aggregation targets
- `data/processed/minibacias.tif` 705 x 1500, exactly 1/8 of the 90 m DEM grid, identical bounds
  => a 90 m cell's minibacia is `minib_coarse[r//8, c//8]`. 8672 minibacias.
- URH (24 codes = soil_family*10 + land_class) is defined in nb08 cell 10 on the SAME 705x1500 grid
  from `soil_family_igac.tif` (nearest reproject) x WorldCover (zip, f=40, mode). `urh_fractions.csv`
  (8672 x 24, rows sum to 1) is the existing product => rebuild the same URH grid to aggregate LS.
- RAM available 3.2 GB of 17 GB. 90 m grid = 67.7 M cells. Chunked per-cell LS to stay inside it.

### S3 — scripts/c3/ls2d.py written; SMOKE TEST at --scale 8 (740 m) PASSED mechanically
0 NaN, 0 non-positive, 472,438 cells, 8672/8672 minibacias, 32,782 (mini,URH) pairs, figure written.
BUT the numbers expose two real issues that are NOT bugs:
 - per-cell median 7.51, area-wtd MEAN 48.67, p90 102, MAX 117,806. The max sits on the mainstem:
   A_unit = A/D = 3.56e11/740 = 4.8e8 m, so (A_unit/22.13)^m explodes. USLE/RUSLE LS is a
   HILLSLOPE relation; on a channel cell it is being extrapolated ~7 orders of magnitude past the
   22.13 m unit plot. Water URH classes come out highest (27 Medium x Water LS 240) — exactly the
   channel cells. This is a domain-of-validity problem, not a coding one.
 - 740 m is a resolution artifact floor: A_unit >= D always, so at D = 740 m even a RIDGE cell gets
   L >= (740/22.13)^0.4 * 1.4 = 5.7. At D = 90 m that floor is 2.45. => must run at --scale 1.
DECISION (no constant of the formula is touched): keep `ls2d` = the literal formula, uncapped, as
the primary column, AND add `ls2d_hs`, identical except the upslope area is capped at a
channel-initiation source area A_CHAN = 1 km2 (upper bound of Montgomery & Dietrich's humid-terrain
field range) so the relation is never extrapolated into channels. Both are reported; C3.4 chooses.

### S3b — scale-8 rerun with the ls2d_hs column (RISKY OP LOG: launching the 90 m run next)
740 m numbers, both columns:
  ls2d     median 7.508  area-wtd mean 48.669  p99 417.7  max 117,806
  ls2d_hs  median 5.524  area-wtd mean 22.192  p99 159.6
  variants: primary 48.669 | mb86 (m=0.4) 13.263 | dg96 finite-difference 38.651
            dg96/primary = 0.794  -> eq.(1) and eq.(2) agree to ~21 %, i.e. the implementation of
            the literal Desmet & Govers finite-difference L reproduces the continuous form. Good.
  Andes(>1000 m)/lowland(<200 m) median ratio: 963x (ls2d), 788x (ls2d_hs).
  flat cells at the floor: 1,654 (0.350 %).
  The cap does exactly what it should: `27 Medium x Water` (pure channel cells) falls 240.6 -> 2.89,
  while `16 Coarse x Bare` (hillslope) only falls 76.8 -> 62.3.
NOW LAUNCHING --scale 1 (90 m, 67.7 M cells) in background -> scratchpad/ls2d_90m.log.
RAM headroom 3.2 GB; expected peak ~1.5 GB in pyflwdir.from_dem. Fallback if it OOMs: --scale 2.

### S3c — 90 m run in flight
Log: scratchpad/ls2d_90m.log. DEM read OK at 12000x5640 = 67.7 M cells, elev -50..5654 m.
Horn slope took 2 s. pyflwdir.from_dem (priority-flood pit fill + D8) is the long pole.
Smoke-test figure at 740 m already verified visually: both cordilleras dark (high LS), the
Magdalena and Cauca valley floors and the Caribbean lowland bright (low LS) -> gate 3 passes
by eye as well as by the 788x median ratio.

### S4 — 90 m RUN COMPLETE (exit 0, verified from the log + the written files, not the exit code)
Timing: DEM read 3 s | Horn slope 2 s | from_dem (pit fill + D8) 2 min 10 s | upstream_area 10 s |
per-cell pass over 30.24 M basin cells 26 s | percentiles 3 s | figure 8 s. Peak RAM well inside
the 3.2 GB headroom (3.97 GB still free mid-run).

FOUR SANITY GATES, all with numbers (90 m, 30,235,916 basin cells, 257,000 km2):

GATE 1 — positivity / finiteness: **PASS**
  non-finite (NaN or inf) cells .......... 0   (nothing to locate)
  LS <= 0 cells .......................... 0
  ls2d     min 1.45911e-04   max 3.66574e+06
  ls2d_hs  min 1.45911e-04   max 4.013e+03
  Table-level: minibacia_ls2d.csv 8672 rows, 0 NaN in any column; urh_ls2d.csv 32,782 rows, 0 NaN.

GATE 2 — basin median vs the published mountainous range ~2-10: **FAILS HIGH, NOT ADJUSTED**
  per-cell median  ls2d 12.774 | ls2d_hs 12.486   -> 1.25-1.28x ABOVE the upper bound of 10.
  area-wtd mean    ls2d 104.901 | ls2d_hs 39.812
  percentiles ls2d_hs 1/5/25/50/75/90/95/99: 0.000 0.016 0.617 12.486 44.743 99.204 155.111 403.728
  Variants (area-wtd mean): primary 104.901 | mb86 fixed m=0.4 16.435 | dg96 finite-difference 82.870
    dg96/primary = 0.790 at 90 m and 0.794 at 740 m -> eq.(1) and the literal D&G eq.(11) agree to
    ~21 % and the ratio is resolution-stable => the implementation is right; the level is the issue.
  MEASURED CAUSE (not speculation): the median is resolution-driven. Same code, same constants:
    740 m -> median 7.508 ; 90 m -> median 12.774. 1.70x from resolution alone. Published LS values
    are quoted at whatever DEM resolution the paper used, so "2-10" is not a resolution-free number.
  PER-UNIT view (hard rule: report at both scales): across the 8672 minibacias, the within-minibacia
    per-cell median (`ls2d_median`) has median 16.555, IQR 0.698-39.550, max 122.6. Only 889
    minibacias (10.3 %) fall inside 2-10; 5,038 (58.1 %) are above 10 and 2,745 (31.7 %) below 2.
    The basin is bimodal (cordillera vs floodplain) — a single basin median is a poor yardstick here,
    which the two-peak histogram in the figure shows directly.
  ACTION TAKEN: none. No constant was changed to move this number. Reported as-is, per instructions.

GATE 3 — Andean flanks >> lowland floodplain: **PASS**
  lowland  (<200 m)  n =  8,906,444  median ls2d 0.220 (mean 8.949)   | ls2d_hs median 0.216
  Andean   (>1000 m) n = 14,003,776  median ls2d 35.191 (mean 104.589)| ls2d_hs median 34.674
  ratio of medians: 159.6x (ls2d), 160.9x (ls2d_hs). Map confirms it visually: both cordilleras and
  the Sierra Nevada de Santa Marta dark, the Magdalena/Cauca valley floors and the Caribbean
  floodplain bright.

GATE 4 — flat cells, sin(beta) -> 0: **PASS, behaviour stated**
  slope floored at tan(beta) = 1e-4 (0.01 %; a 9 mm drop over a 90 m cell, an order of magnitude
  below the DEM's vertical precision => a numerical guard, not a physical claim).
  cells hitting the floor: 403,681 = 1.335 % of the basin.
  LS at the floor = 1.452e-04 x the area term (~1 on a flat) => strictly positive, finite, and
  effectively zero erosion — the physically correct answer for a flat floodplain cell.
  x = |sin(alpha)|+|cos(alpha)| in the D&G finite-difference form is never 0 (min 1), so eq.(2)
  cannot divide by zero either. No cell is dropped; no NaN is produced.

INDEPENDENT CROSS-CHECKS (not required, run anyway):
  - area closure: sum of 90 m cell areas per minibacia / minibacias.csv:area_km2 -> median 0.9991,
    p01 0.989, p99 1.005. The aggregation lands on the existing partition.
  - URH closure: the per-(mini,URH) area fractions reproduce urh_fractions.csv to max abs diff
    0.0224 (mean ~0.00000) over 8672 x 24 -> the rebuilt URH grid is the same one nb08 used.
  - all 24 URH codes present; area_frac sums to 1.000000 +/- 2e-6 in every minibacia.

### S5 — figure written: figures/deck/gen_ls2d.png (two maps + two distributions), inspected.

### S6 — WARNING FOR C3.4 (do not miss this)
  Per minibacia the AREA-WEIGHTED MEAN ls2d_hs has median 30.605 (IQR 2.619-65.232) but the
  within-minibacia per-cell MEDIAN has median 16.555 — a factor 1.8. The mean is pulled up by the
  convergent-cell tail. Whichever statistic C3.4 feeds MUSLE changes the sediment answer by ~2x,
  before any alpha/beta. `ls2d`, `ls2d_hs`, `ls2d_median` and `ls2d_p90` are all shipped so the
  choice is explicit rather than accidental.
  C3.5 (cross-check against implementation B's musle.py) remains BLOCKED: that file is not in this
  repo; not attempted.

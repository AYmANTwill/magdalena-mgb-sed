# journal_nbc1-nb01-03 — Notebook Coherence Pass, T1 AUDIT (READ-ONLY)

**Agent:** nbc1 (notebooks 01_dem + 03_hydrology)
**Date:** 2026-08-13
**Phase:** T1 = audit only. FIX NOTHING. No notebook execution. No git write.
**Owned files:** this journal only.

## Assignment as given
Audit `notebooks/01_dem.ipynb` (17 cells) and `notebooks/03_hydrology.ipynb` (10 cells).
Both Phase A didactic toy notebooks, hand-written (no `src/nbgen` generator exists for 01-09),
last committed 2026-07-27. Expect **stale framing**, not stale sediment numbers.
Specifically asked to check:
- whether they still describe the project scope, the ENSO years, the basin box, the model chain;
- whether nb03's derivation matches what H2E actually runs (FAO-56 threshold ET, theta_crit 0.6,
  revised objective, `k_int < k_bas`, `k_bas` bound below 15 d);
- narrative beat 1 (inputs are not innocent) and the setup for beat 2 (data ceiling, not parameter ceiling).

## Log

- [start] Created journal. Listed nbtext extracts — both `01_dem.txt` and `03_hydrology.txt` present.

### Read (extracts, in full)
- `scratchpad/nbtext/01_dem.txt` — 17 cells (9 md, 8 code), 0 unexecuted, 0 errors. Read all 17.
- `scratchpad/nbtext/03_hydrology.txt` — 10 cells (7 md, 3 code), 0 unexecuted, 0 errors. Read all 10.
- **cells_swept = 17 + 10 = 27. Every cell of both notebooks was examined.**

### Git provenance (measured, read-only)
`git log -1 -- notebooks/01_dem.ipynb` and `... 03_hydrology.ipynb` both return
`e627d05 2026-07-27 "Rename notebooks to short names; add hydrology notebook (03)"`.
Both are single-commit files, untouched since 2026-07-27 — the oldest notebook text in the repo,
and **17 days older than the engine-default LS move (`c3fdb55`, 2026-08-12)**.

### KILL-LIST SWEEP — measured, negative
Grepped both extracts for every kill-list token: `t/km`, `km2/yr`, `0.333`, `0.421`, `2.37`,
`104.8`, `82.8`, `126.1`, `99.7`, `min(m`, `eq. 14`, `38 %`, `0.1644`, `0.465`, `0.00216`,
`0.0209`, `0.0104`, `2.12`, `348.4`, `SDR`, `0.05-0.30`, `under-erosive`, `11.8`, `14.9`, `Mt/yr`,
`alpha/α`, `beta/β`, `LS`.
**Result: ZERO kill-list hits in either notebook. ZERO yield-embargo violations.**
The only α/β mention is nb01 cell 16's forward-looking "calage sédimentaire (α, β de MUSLE)" —
no number attached. The only `LS` hits are substring false positives inside French words.
The only `Mt/yr`-shaped match: none. This is a genuine negative and I report it as one.

### ENGINE ENTRY POINTS — measured
nb01 cell 1 imports `numpy`, `matplotlib` only. nb03 cell 1 imports `numpy`, `matplotlib` only.
Neither imports any `src/` module. **N/A — no engine call**, so `ls2d_column` (`V4_dg` at
`src/mgb_sediment.py:925` vs `ls2d_hs` at :818/:862) and `cp_revision` are both irrelevant here.
No executed output in either notebook can be stale w.r.t. the engine-default LS move.

### WHAT I MEASURED AGAINST (files/lines actually opened)
- `src/mgb_hydrology.py` — module docstring lines 5-12, 35-40, 44-67, 71-80, 83-88, 115, 126, 138;
  fields at 421-454; the fao56 branch at 694-695. States the production engine is *derived in
  notebooks/03_hydrology.ipynb sections 1-5*, that `et_stress='linear'` is "nb03 s.1 verbatim",
  that `reservoir='euler'` "reproduces notebook 03 cell 7 literally (Q = S/K)" and is "unstable
  for K < 1", and that `reservoir='exact'` is the **default**.
- `src/test_mgb_hydrology.py:631-700` — `test_07_notebook03_regression`, "notebook 03 cell 7,
  transcribed verbatim as a scalar reference", asserts max|Q_engine − Q_nb03| <= 1e-12 and
  re-derives the day-120 baseflow share. **nb03 cell 7's printed 11.33 mm/day and 98.9 % are
  live-asserted by pytest — they are NOT stale.**
- `src/calib_v2.py:109-114` (10 search parameters + bounds), `:123-136` (objective weights
  0.40/0.40/0.20, W_SET_PEAK 0.34/0.34/0.17/0.15), `:717` (`percolation='linear',
  reservoir='exact'`, `et_stress=self.ET_STRESS`, `theta_crit=self.THETA_CRIT`).
- `src/report_h2e.py:186-187` — asserts `cell.ET_STRESS == 'fao56' and cell.THETA_CRIT == 0.6`.
- `data/processed/sim_calibrated_v2/parameters_H2E.csv` — global k_sup **19.19933 (RAILED at
  hi=20.0)**, k_int_frac **0.0201416 (RAILED at lo=0.02)** => k_int = **0.86556 d**,
  k_bas **42.97399 d**, kc_mult **1.66247**, b **0.356675**, adr 0.0075942, fint 0.754034.
- `data/processed/minibacias.csv` — **8,672 rows**, columns `id, area_km2, downstream`.
- `docs/open_questions.md` — header "STATUS — SUPERSEDED; all three questions are resolved";
  Q3 "DECIDED AND BUILT ... the whole basin was built directly at **90 m** ... 8,672 minibacias
  over 257,097 km²".
- `docs/15_domain_correction.md:24` — "**DEM** (Copernicus GLO-90) ... dataset `COP90`".
- nb07 extract — `import pyflwdir`; `pyflwdir.from_dem(...)  # fills pits + D8`;
  `STREAM_THR = 100  # km^2`; `N_TARGET = 12000`; "Step 1 — conditioned DEM (COP90)";
  `SCALE=1` = full 90 m.
- `docs/03_methodology.md:27` — "### 1c. Convert minibacias to MGB format (`mini.gtb`) — **TODO**."
- `docs/23_gauge_geometry.md:270-303` — §13.2: 31 of 85 shared gauges disagree **beyond 2×**;
  "neither derivation is trustworthy per gauge"; "a sediment yield in t/km²/yr inherits this
  error one-for-one". **This is the origin of the yield embargo, and nb01 is where the area is
  taught as a solved quantity.**
- `docs/26_phase3_refit.md:34-37, 242-243` — k_bas lower bound 15 d → 5 d; k_int/k_bas
  reparameterisation; "surface response is now **22× slower than interflow**"
  (measured: 19.19933 / 0.86556 = 22.18).
- `docs/55_c43_verdict.md:1-45` — C4.3 **RAILED / EXPLORATORY, not adopted**; α box floor 2.0,
  F_report −0.118; unconstrained optimum α ≈ 0.48.
- Grepped all of `docs/*.md` for `rain/slope` / `erosive event`: hits only in the *plan* docs
  00_objectives, 01_scientific_background, 03_methodology, 09_report_outline. **No Phase C
  execution doc (37/42/43/45/55) uses the Fagundes rain/slope threshold technique — it was
  never enacted.**
- `docs/00_INDEX.md` grepped for `nb01|nb03|01_dem|03_hydrology`: **no hits. The index does not
  mention notebooks 01-09 at all.** The only index text about notebooks is the §"Forcing
  versions" warning about nb10/nb11.

### Measured numeric checks I did myself
- Euler vs exact one-day reservoir release fraction: K=1 → 1.000000 vs 0.632121 (**ratio
  1.582**); K=6 → 0.166667 vs 0.153518 (1.0856); K=45 → 0.022222 vs 0.021977 (1.0112).
  nb03 §3 *writes* the exponential recession and nb03 cell 7 *codes* the Euler form; the
  production default is `exact`. At nb03's own Ksup = 1.0 the two differ by 58 %.
- `STREAM_THR = 100 km²` at 90 m = 100e6/8100 = **12,346 cells**, not "1000 cellules".
- nb01 execution counts, read from the raw `.ipynb` (not the extract): code cells carry
  1, **10**, 3, 4, 5, 6, 7, 8. Cell 3 was re-executed *after* every downstream cell; 2 and 9 are
  missing. The stored notebook is **not** a single top-to-bottom "Run All", which is what
  `notebooks/README.md` instructs. nb03's are clean: 1, 2, 3.

### What I refused to conclude
- I did **not** re-execute either notebook (prohibited, and nb01's outputs are cheap but the
  rule is the rule). I therefore cannot certify that nb01's stored outputs equal a fresh run —
  I report the out-of-order execution counts as the *measurement*, not "the outputs are wrong".
- I did **not** conclude that nb03's ET form is a code defect. `src/mgb_hydrology.py`'s
  **default** still matches nb03 exactly and says so deliberately ("changing the default would
  silently break comparability with everything on record"). The gap is between nb03 and the
  **adopted H2E configuration**, not between nb03 and the code.
- I did **not** grade nb01's French-language framing above LOW; it is a coherence break, not a
  factual defect.

## FINDINGS (T1 — recorded, NOT fixed)

Neither notebook has a generator (`src/nbgen/make_nb01.py` / `make_nb03.py` do not exist —
`ls src/nbgen` confirms generators only for 10-19). `fix_location` is therefore the `.ipynb`
cell index, per the assignment.

### nb01 — 01_dem.ipynb (17/17 cells swept)
| # | cell | sev | defect |
|---|---|---|---|
| N1-1 | 0 md | HIGH | "ce que fait le plugin *IPH-HydroTools* de QGIS" — IPH-HydroTools was never used; nb07 delineated with **pyflwdir** |
| N1-2 | 16 md | HIGH | "les minibacias produites sont exportées en **`mini.gtb`**" — `mini.gtb` never built (docs/03 §1c still TODO); the delivered artifact is `minibacias.csv`, 8,672 rows, consumed by `src/mgb_hydrology.py` |
| N1-3 | 16 md | HIGH | "La logique est **exactement la même** à l'échelle réelle" — steps 5 and 7 differ in kind, not scale |
| N1-4 | 16 md | HIGH | "seuil réel **1000 cellules**" — real value `STREAM_THR = 100` **km²** (~12,346 cells at 90 m) |
| N1-5 | 10 md | MEDIUM | "Dans **tes notes** IPH le seuil est 1000 cellules" — uncited private source, and wrong |
| N1-6 | 16 md | MEDIUM | "~250 M cellules ... sous-bassin ou dégrader la résolution (une de tes 3 questions ouvertes)" — Q3 RESOLVED: whole basin at 90 m, 8,672 minibacias / 257,097 km² |
| N1-7 | 1 code | MEDIUM | `cellsize = 30.0 # ... ex. GLO-30 / ALOS World 3D` — the DEM used is **COP90 at 90 m** |
| N1-8 | 16 md | MEDIUM | "(ALOS World 3D 30 m ou Copernicus GLO-30)" — same |
| N1-9 | 16 md | MEDIUM | "calage sédimentaire (α, β de MUSLE) par la technique des seuils pluie/pente de Fagundes" — never enacted; C4.3 RAILED/EXPLORATORY, α/β unfitted |
| N1-10 | 8 md | MEDIUM | flow accumulation taught as a trustworthy drainage area, with **no** pointer to docs/23 §13.2 — this is the missing origin of the yield embargo. **Beat 1.** |
| N1-11 | 0 md | MEDIUM | no STATUS banner; nb10-17 all carry one |
| N1-12 | 3 code | LOW | `exec=10` out of order (downstream cells hold 3-8) — not a stored "Run All" |
| N1-13 | 2 md | LOW | typo "qui reservent partout" -> "qui reviennent partout" |
| N1-14 | 0 md | LOW | nb01/nb02 French, nb03-19 English |

### nb03 — 03_hydrology.ipynb (10/10 cells swept)
| # | cell | sev | defect |
|---|---|---|---|
| N3-1 | 5+7 | HIGH | §3 writes `Q = Q0 e^{-t/K}`; cell 7 codes `Qsup = Ssup/Ksup` (Euler). Internal prose-vs-code. At Ksup = 1.0 the two differ by **58 %** (1.000000 vs 0.632121). Production default is `reservoir='exact'`. |
| N3-2 | 2 md | MEDIUM | `ET = ETp*(W/Wm)` is the `linear` branch; **H2E runs `fao56`, theta_crit 0.6**, and `kc_mult = 1.66247`. nb03 also names but never codes canopy interception. |
| N3-3 | 5 md | MEDIUM | "surface store: tiny Ksup (~1 day)" — H2E fit **inverts** it: k_sup 19.19933 d (RAILED at 20.0) vs k_int 0.86556 d, i.e. surface **22.18× slower** than interflow |
| N3-4 | 9 md | MEDIUM | knob list (Wm, b, Kint, Kbas) + "NSE, KGE, PBIAS" — the real search is **10 parameters**, k_int is not free (`k_int_frac`), and F = 0.40 KGE + 0.40 KGE(log) + 0.20 recession (H2E **F = 0.25931**) |
| N3-5 | 0 md | MEDIUM | "it is a teaching model, not the MGB solver" — under-claims: `src/mgb_hydrology.py` is *derived from* it and `test_mgb_hydrology.py:635` regression-tests cell 7 to 1e-12 |
| N3-6 | 9 md | MEDIUM | "feed MUSLE in the sediment module (**the next block**)" — broken hand-off; no r≈0.57 ceiling, no El Niño −0.0005, no H-PEAK refutation, no ENSO deliverable. **Beat 2 setup missing.** |
| N3-7 | 0 md | MEDIUM | no STATUS banner |
| N3-8 | 7 code | LOW | nb03's toy scalars became the calibration prior (adr 0.06, fint 0.60, b 0.60 and Kint/Kbas = 6/45 = 0.13333 = the prior `k_int_frac` 8/60) — an undocumented chain link |

**Chain verdict.** nb01 -> nb02 (URH) holds. nb01 -> nb07 (real delineation) is **broken**: nb01
promises IPH-HydroTools + `mini.gtb` + a 1000-cell threshold; nb07 delivered pyflwdir + COP90 90 m
+ 100 km². nb03 -> "the next block" is **broken**: the next notebook is nb04 (real-DEM EDA); the
hydrology run is nb13/nb14 and MUSLE is nb18. nb03 -> `src/mgb_hydrology.py` **holds and is
load-bearing** (pytest test_07) but is invisible from inside nb03.

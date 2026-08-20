# journal_nbc1-nb12-assembly — T1 notebook-coherence audit of nb12 (READ-ONLY)

Agent: nbc1-nb12-assembly. Started 2026-08-13.
Scope: `notebooks/12_model_input_assembly.ipynb` (36 cells), generator `src/nbgen/make_nb12.py`.
Phase 1 = AUDIT ONLY. I fix nothing. The only file I write is this journal.

## Assignment as given to me
- Check nb12 states "v2 = GAUGE-ONLY" unambiguously.
- Check it names the zero-suppression repair and the deterministic IDW.
- Check it does not imply a v3 exists.
- Resolve the mechanical sweep's "38 %" hit: retired +-38 % Pi band, or unrelated percentage?
- Narrative beat 1 ("Inputs are not innocent").
- Produce owning_docs / current_claims / narrative role / staleness / findings / cells_swept / not_settled.

## Log

### Step 1 — orientation
Extract path: `.../scratchpad/nbtext/12_model_input_assembly.txt`.

### Step 2 — full sweep of all 36 cells (extract read in full, lines 1-2255)
Read `12_model_input_assembly.txt` end to end. 36 cells: 15 markdown, 21 code,
`code_unexecuted=0`, `cells_with_error=0`. Every cell examined. cells_swept = 36.

### Step 3 — SETTLED: the "38 %" mechanical-sweep hit is a FALSE POSITIVE
Command run:
  python3.10 -c "<regex 38\s*%|±38|\+-38|38 percent over EVERY cell source AND every output of the
  raw .ipynb>"
Exactly ONE hit, in cell 16's executed stdout:
    `   28 Medium-Wetland     0.38 %`
That is the basin **URH area share** of the Medium-Wetland hydrological response unit, printed by
the "basin URH composition (all 24)" loop. It is NOT the retired `+-38 %` Pi band, and nb12 makes
no sediment/Pi claim at all. `grep -n "38" src/nbgen/make_nb12.py` returns only two matplotlib bar
widths (`width=.38`) — the generator contains no "38 %" string whatsoever.
VERDICT: unrelated percentage. No kill-list finding. Do not spend Phase 2 time on it.

### Step 4 — engine call surface
`grep -ni "mgb_sediment|ls2d|cp_revision|V4_dg|musle_|sediment"` over the extract: ZERO hits.
nb12 imports json, pathlib, time, collections, os, re, numpy, pandas, rasterio, matplotlib only
(cell 3). It calls no engine entry point. `executed_output_staleness` w.r.t. the engine-default LS
move (`c3fdb55`) is therefore N/A. It does export `K_musle` (the MUSLE K erodibility field) into
`parameters.npz`, but computes nothing from it.

### Step 5 — yield embargo
`grep -ni "t/km|ton.*km2|yield"` over the extract: ZERO hits. The only per-km2 quantities are
`q_spec` in **l/s/km2** (water) and runoff depth in **mm/yr** (water). No t/km2/yr anywhere.
No embargo violation.

### Step 6 — git provenance (read-only)
`git log --oneline -- notebooks/12_model_input_assembly.ipynb` and `-- src/nbgen/make_nb12.py`
give the SAME three commits: `c014623`, `4b6fb5c` ("execute nb11 -> nb12 on the v2 forcing; model
period now 2008-2018"), `57f9761` (the banner annotation; the banner itself says "Nothing below
this banner was rewritten"). `57f9761` predates `c3fdb55` (engine default LS -> V4_dg), which is
irrelevant here because nb12 calls no engine.

### Step 7 — are the executed outputs stale w.r.t. their INPUTS? Measured: NO.
mtimes on disk:
  energy_floor_triage.csv          Aug  2 20:45
  forcing_minibacia_provenance_v2  Aug  2 21:50
  forcing_precip_v2.npy / pet_v2   Aug  2 21:54
  model_inputs_v2/*.npz            Aug  2 22:04-22:05
  manifest.json generated_utc      2026-08-03T03:05:02Z  (= Aug 2 22:05 local)
Every input predates the bundle write. And nb12's printed numbers match the owning read-out
`docs/18` §14.2 line for line: 4,018 days · 2,073.1 mm/yr · 1,251.6 mm/yr · CALAMAR 3,992 days,
7,433.4 m3/s, 912.4 mm/yr · 11 smoke tests · 48 arrays · EXCLUDE 2 / DOWN-WEIGHT 10 / KEEP 2 ·
**63** primary gauges, 204,955 station-days. **The outputs are live. The PROSE is stale.**

### Step 8 — the assignment's three checks, answered
(a) "v2 = GAUGE-ONLY" stated unambiguously? **Only in the cell-0 banner** (lines 28-32 of the
    extract): *"v2 = the zero-suppression repair (docs/18 §9-§12) plus the deterministic IDW and
    the co-located-gauge merge (docs/23 §11) - still **gauge-only**"*. Cells 1-35 never say
    "gauge-only" and never define v2; `VERSION = 'v2'` (cell 3) is a bare constant.
(b) zero-suppression repair named? Yes in the banner, and once in the body (cell 1: *"docs/16
    section 4.1: 70 gauges were zero-suppressed"*) — but with the **v1 count 70**; the v2 forcing
    this notebook assembles came from the 153-station selectivity repair (docs/18 §10 / item 7).
    Deterministic IDW named? **Banner only.** The body's single IDW provenance string (cell 32)
    says "IDW k=6 over 294 repaired IDEAM gauges" and never mentions order-dependence.
(c) does it imply a v3 exists? The banner says v3 does not exist. **But cell 34 §7 item 4 still
    prescribes building it** ("*Check:* the CHIRPS quantile-map merge ... then re-run the same
    calibration"). docs/58 closed that route with a number: max **+0.006 r**. Same notebook,
    opposite claims.

### Step 9 — measured against the shipped artifacts (NOT just the notebook)
`data/processed/model_inputs_v2/manifest.json` -> forcing.npz.dates =
  {'shape': [4018], 'dtype': 'datetime64[D]', 'provenance': '... 3287 contiguous days'}
A single JSON object that contradicts itself. docs/18 §14.3 item 4 asserts "Both strings were
corrected and nb12 re-run so **the shipped manifest is accurate**." Measured: it is not.
`data/processed/model_inputs_v2/README.md` lines 33-35:
  top = np.load("data/processed/model_inputs/topology.npz")     <- the **v1** directory
  P   = frc["precip_mm"]          # (3287, 8672) float32        <- actual shape (4018, 8672)
A reader copying the shipped snippet loads the v1 forcing while standing inside the v2 bundle.
That is the most consequential defect I found.

### Step 10 — bands that gate
RC_BAND (0.03, 1.2) IS published: docs/17 line 528 "Stations with RC outside [0.03, 1.2]".
QSPEC_BAND (7.0, 74.9) is NOT published as a band. docs/17 line 343 gives "median 26.8, IQR
15.8-33.8, **p5-p95 7.0-57.1, max 74.9**". nb12 composed a p5 floor with an absolute-max ceiling
and the shipped manifest calls the result "the docs/17 healthy q_spec envelope". That composite is
the *sole* difference between the 70-gauge and the 63-gauge set (6 gauges -> review_qspec_outside_healthy).

### Step 11 — narrative beat 1, element by element
1. gauges zero-suppressed / value screens cannot see missing data  -> PRESENT (cell 1), v1 count.
2. the IDW was order-dependent until fixed                          -> ABSENT from the body.
3. catchment areas unreliable per gauge in BOTH implementations
   (docs/23 §13.2: 31 of 85 shared gauges beyond 2x) -> ABSENT, and nb12 is the notebook that
   MANUFACTURES `gauge_upstream_area_km2` and gates on `q_spec = Q/A`. §7 (14 numbered items) is
   the natural home and does not mention it. This is the origin of the yield embargo.

### Step 12 — no findings I refused to conclude
- I did NOT execute the notebook (7,200 s registered timeout). Every number above is read from the
  committed executed outputs or from disk.
- I did NOT verify that re-running the generator reproduces the committed notebook source-identically;
  CLAUDE.md asserts it was verified 2026-08-12 and I take that on the record, not on my own measurement.

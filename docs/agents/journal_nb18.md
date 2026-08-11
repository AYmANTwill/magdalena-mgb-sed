# journal_nb18 — notebook 18: MUSLE construction (stage C3)

GOAL: write `src/nbgen/make_nb18.py` -> `notebooks/18_musle_construction.ipynb`, documenting
stage C3: building the sediment model and closing an order-of-magnitude gap. Notebook must
execute with 0 errors, every code cell with an execution_count, every figure with a three-part
reading, every listed term defined at first use, and the factor chain shown as a figure with
its arithmetic.

## Checklist
- [ ] Read generator convention (`src/nbgen/make_nb13.py`, `make_nb14.py`)
- [ ] Read docs/35, docs/37, docs/40, docs/41, docs/42
- [ ] Read `src/mgb_sediment.py`, `scripts/c3/{ls2d.py,qpeak.py}`
- [ ] Read the named journals (c31-ls2d, c32-cp, c33-qpeak, c34-sediment-engine, c36-first-run,
      decide-units, decide-ls-aggregation, decide-ls-resolution, dimensional-audit, recompute)
- [ ] Inventory data files under data/processed/
- [ ] Write generator
- [ ] Emit + execute notebook, verify from executed outputs
- [ ] Report cell count, figure count, undefined terms

## Log
- 2026-08-11 start. Journal created before any other action.
- Read `src/nbgen/make_nb13.py` head (711/2194 lines): convention is a flat script with `md()`/`code()`
  appenders into a list `C`, `OUT = pathlib.Path(...)`, module docstring giving the run + nbconvert
  commands. Raw strings, LaTeX in markdown, section numbering `## N.M`, tables of
  choice/class/rejected-alternative. Will follow exactly.
- Read `docs/37_c3_closure.md` (737 lines). **IMPORTANT: the task brief's state summary is stale.**
  docs/37 now carries **AMENDMENT A1 (2026-08-11)**: the SDR clause is **RETIRED** (docs/40), the
  C-factor revision is **ADOPTED** (docs/41, ×1.2042736), the basin total is **superseded
  248.7298 -> 299.5387 Mt/yr**, and C3 is OPEN on clauses **2 (LS formulation level unresolved),
  3 (2026-08-11 decisions unaudited) and 4' (gross hillslope erosion rate NOT MET, model
  1.03-2.27x under-erosive)**. The notebook must report THIS verdict, not "OPEN on the SDR clause".
- Read `docs/35_qpeak_preregistration.md` (785 lines) incl. amendments 9.1/9.2/9.3. Key numbers
  captured: factor chain 47.8630 = 1000^0.56, 7.593014 = 1/0.1317, product 363.4245196;
  conventions table 0.6844 / 9.0222 / 32.7577 / 248.730 Mt/yr; alpha band 5.9-23.6, stops 35.4/3.9;
  scale factor N^(2b-1); LS bracket x0.333-x0.421.
- Read `src/mgb_sediment.py` (docstring + full API), `scripts/c3/ls2d.py` docstring + constants,
  journals c31-ls2d, c36-first-run, decide-units, dimensional-audit, alpha-guard.
- FEASIBILITY PROBE RUN (scratchpad/probe.py, read-only, nothing written to repo). Everything the
  notebook needs is cheap and reproduces the docs exactly:
  drivers load 1.4 s; `simulate_sediment` 2.1 s per run; adopted C total
  **2,994,977,042.2609434 t / 3652 d = 299.5387088405831 Mt/yr**, ledger exact=True;
  prior C **248.729790996124 Mt/yr**, measured ratio **1.2042735517968206**;
  the 2x3 convention grid: pixel_km2/si 0.684406, pixel/us 5.196702, swat/si 9.022223,
  swat/us 68.505873, williams/si 32.757713, williams/us **248.729791** Mt/yr.
  => the notebook can quote every headline number from its OWN executed output. 8 runs ~ 20 s.
  Also: load_geometry emits the area-disagreement UserWarning (12.9 % of cells >5 %, max 6.60x),
  which is itself a documented problem to show, not suppress.
- PROBE 2/3/4 done. Confirmed reproducible from executed output:
  URH-level LS area-wtd means: ls2d 106.4123 / ls2d_hs 40.5497 / mb86 16.6756 / dg96 84.0037;
  per-minibacia ls2d 104.9013 / ls2d_hs 39.8123 / ls2d_median 23.5769; URH max uncapped 76,300.20.
  Top-3 URH by uncapped LS are ALL WATER classes (27 Medium-Water 1837.07 -> 13.72 capped,
  37 Fine-Water 1053.00 -> 8.69, 17 Coarse-Water 808.62 -> 12.25). Water class overall
  1327.75 -> 10.99. This is the judgement-call evidence, measurable here.
  Unit day mini 16115 / 2009-04-11: Qsur 26.677167892456055 mm, 1 URH cell (11 Forest,
  24.49 km2, K 0.019 SI, C 0.005 adopted, LS 118.245) -> engine cell load
  **2155.9486044749283 t/d**, hand chain identical.
  ENSO: P-LN 1.3054 / P-EN 0.5696 Mt/d = 2.2915274346272927; S-LN 1.5513 / S-EN 0.3905 = 3.9724677.
  Land class share (adopted C): Forest 50.4918, Grassland 34.0366, Bare 14.78 %.
  alpha for anchors at adopted C: 5.673 (144, guard says **watch** - below expected band low)
  and 7.248 (184, guard 'ok'); at prior C 6.832 / 8.729 both 'ok'.
  Pi = 11.8 x 47.86300923226385 x 7.59301442672741 = 4288.409331364566 (prior C),
  x1.2042735517968206 = 5164.417937041035 (adopted C).
  Williams recomputed 11.782565403570468; mm-ha 42.7799092692986; mm-km2 563.9490366908459.
- WROTE `src/nbgen/make_nb18.py` (2,470 lines) in 8 appended parts, following the make_nb13/14
  convention exactly: module docstring with run + nbconvert commands, `OUT` path, `md()`/`code()`
  appenders into `C`, plus one extra helper `reading(what, shows, means)` that emits the mandatory
  three-part figure reading in a fixed order. Emitted `notebooks/18_musle_construction.ipynb`.
- Section layout: 0.1 prerequisites / 0.2-0.4 the inherited vocabulary (all 33 required terms
  defined in plain language at first use) / 1 MUSLE factor by factor with a DATA-ASSUMED-FIT
  provenance ledger / 2 Qsur, K, C, P measured / 3 LS2D from first principles incl. the channel-cap
  judgement call, the resolution sensitivity and the UNRESOLVED formulation level / 4 q_peak, the
  three candidates and the pre-registered bias statement / 5 the order-of-magnitude gap with the
  waterfall and the hand-computed unit-day / 6 the SDR retirement and the OPEN verdict / 7 problems,
  refuted beliefs, must-not-conclude / 8 ENSO first look / 9 close + integrity block.
- EXECUTION 1: 0 errors, 85 cells, 16 figures. But cross-checking my quoted numbers against the
  executed stdout found FIVE mismatches, all now fixed:
    (a) Qsur basin 651.2 -> **651.1** mm/yr;
    (b) Bare class uncapped/capped LS 96.06/62.85 x0.654 -> **93.60/63.34 x0.6767** (I had used a
        per-URH-code figure where the text claimed the whole class);
    (c) scale identity difference 3.1e-15 -> **4.4e-16** and predicted ratio last digits;
    (d) a curly-apostrophe typo inside a `", ".join(...)` that printed "Medium x Water, ’Fine x...";
    (e) **a real arithmetic defect**: clause 4' combined bracket was `min()` over raw
        published/model ratios, which folded Leg C's *mean*-yield comparison in as a shortfall and
        reported "0.59x - 2.27x". Gross erosion is SUPPOSED to exceed a measured yield, so that end
        is not a shortfall. Restructured so each leg carries an explicit shortfall bracket; combined
        is now **1.03x - 2.27x**, matching docs/37 A1.4. The defect and its correction are recorded
        inside the notebook's own clause-4' reading, not silently fixed.
  Also fixed a `LEGS[0][1]` index left over from the restructure (TypeError on execution 2).
- EXECUTION FINAL: **0 errors; 85 cells (47 markdown, 38 code); every code cell has an
  execution_count; 16 rendered PNG figures across 31 subplot panels; all 16 figures followed by a
  three-part reading; 10/10 in-notebook integrity assertions PASS** (ledger exact, unit chain to
  1e-9, hand unit-day == engine bitwise, scale identity to 1e-12, LS level 39.8123 vs quoted 39.812,
  totals 299.5387 / 248.7298 to 1e-3). Notebook 1.8 MB.
- Numbers the notebook recomputes rather than quoting: 0.684406 / 5.196702 / 9.022223 / 68.505873 /
  32.757713 / **248.729791** Mt/yr grid; adopted **299.538709** Mt/yr, ledger residual exactly 0.0;
  factor chain 47.86300923226385 x 7.59301442672741 = 363.42451960716664 vs measured
  363.4245196071666 (5.7e-14 apart); C revision 1.2042735517968208; Pi 4288.409 / 5164.418;
  ENSO 2.2915274346272927 primary / 3.9724677512896283 sensitivity; basin-mean gross hillslope
  erosion 1,165.08 t/km2/yr (LABELLED model-internal).
- Disagreements with source docs, REPORTED in the notebook rather than reconciled: Leg B 1.027x here
  vs 1.028x in docs/37 A1.4, and Leg C max 1.888x - 4th-decimal rounding of the same inputs.
- Constraints honoured: no git; touched only `src/nbgen/make_nb18.py`, `notebooks/18_*.ipynb` and
  this journal; no calibration launched; frozen artifacts opened read-only and unmodified; no
  `pd.read_csv` on any wide forcing CSV; no gauge-referenced t/km2/yr yield anywhere (every
  specific-erosion figure is explicitly labelled model-internal); the retired 0.05-0.30 SDR band is
  used to pass nothing and fail nothing and is shown as retired in both directions.
- DONE.

# Journal: et-stress agent

## Goal

Add the FAO-56 threshold evapotranspiration stress function to `src/mgb_hydrology.py` as an
opt-in (`et_stress='fao56'`, `theta_crit=0.6`), gated so the default `'linear'` path is
provably byte-identical, and plumb it into `src/calib_v2.py` as pre-registered cell H2E.

Hypothesis pre-registered: with theta_crit fixed at 0.6, kc_mult comes off its rail
(<90% of range) at no material cost in F.

## Planned steps

- [x] 1. Baseline capture: run unmodified engine on model_inputs_v2 with default MgbParams,
      save gauge discharge matrix to scratchpad/et_gate_baseline.npz. Journal run time + shape.
- [x] 2. Edit src/mgb_hydrology.py: add `et_stress: str = 'linear'` and `theta_crit = 0.6`
      to MgbParams (validated in __post_init__); implement fao56 in the soil-store update
      (ET lives only in _vertical_step; numba path is routing-only, verified); document in
      module docstring (rejected-alternatives style).
- [x] 3. GATE PASSED: rerun step 1 invocation on edited engine, default params. Max abs
      diff == 0.0 against et_gate_baseline.npz (q, ET series, all balance terms).
- [x] 4. GATE PASSED: fao56 run — residual 2.319e-17 < 1e-12, ET 7979.02 mm > linear
      6415.08 mm (ratio 1.244), 0 NaNs.
- [x] 5. Cell 'H2E' plumbed into src/calib_v2.py following the H1/H2 pattern; checkpoint
      dds_H2E_<seed>.part.npz, log H2E_<seed>.log (watch_calib-compatible).
- [x] 6. GATE PASSED: 3-evaluation H2E smoke completed, checkpoint written and verified,
      F finite (0.182028). Smoke checkpoint + result deleted (verified gone).

## Log

- [init] Journal created. Next: read src/mgb_hydrology.py and notebooks/13 for the API.
- [recon] Read mgb_hydrology.py, calib_v2.py, watch_calib.py, nb13 cells. Findings:
  - ET is computed ONLY in `_vertical_step` (numpy); the numba backend accelerates
    ROUTING only (`_get_numba_router`), so a single edit in `_vertical_step` covers both
    backends. Will document this in the module docstring.
  - `calib_v2.Cell` requires `_calib_cache/{name}_precip.npy` etc. I must NOT touch
    `_calib_cache` (launch agent owns it). H2E uses the identical bundle+period as H2, so
    I will add a `cache` key to the CELLS spec letting H2E READ H2's existing cache files
    (read-only mmap; no writes to _calib_cache). ensure_cache('H2E') resolves to the H2
    key and finds it present.
  - `eq_state` embeds the linear ET term (`kc*ec*mid`) in its equilibrium bisection; will
    branch it on et_stress so the fao56 warm start is self-consistent, keeping the linear
    expression byte-identical.
  - Smoke run checkpoint/log will go to my scratchpad via `--out` (CLI derives
    `dds_H2E_<seed>.part.npz` from --out), so `_calib_cache` stays untouched. The real
    launch agent will point --out at _calib_cache/logs as for H1/H2.
- [step1 DONE] Baseline captured to scratchpad/et_gate_baseline.npz via
  scratchpad/run_et_gate.py. Unmodified engine, numba routing, wall 38.5 s,
  q_m3s shape (3652, 63) float32 (2009-2018 scored days x 63 calibration-safe gauges),
  0 NaN, ET 6415.0778 mm, P 22805.0141 mm, runoff 16368.2450 mm (full 4018-d period),
  residual_relative 1.217e-16, clip 0.0.
- [next/risky] About to EDIT src/mgb_hydrology.py: add et_stress/theta_crit to MgbParams,
  fao56 branch in _vertical_step step 3, docstring update. Default branch keeps the
  original expression byte-identical.
- [step2 DONE] Engine edited: MgbParams gained et_stress ('linear'|'fao56', validated in
  __post_init__) and theta_crit (scalar-or-per-URH, validated finite in (0,1] in
  __post_init__, expanded per cell via _as_urh in expand()). _Expanded carries both.
  _vertical_step step 3 branches; the 'linear' arm is the original expression untouched.
  Module docstring item 3 documents both modes + rejected alternatives. Numba path
  confirmed routing-only, so one edit covers both backends (noted in code comment).
- [next/risky] About to run GATE 3: rerun run_et_gate.py (linear) on edited engine and
  compare against et_gate_baseline.npz, requiring max abs diff == 0.0 on q_m3s and
  identical balance terms.
- [GATE 3 PASSED] Rerun of the identical linear invocation on the edited engine: max abs
  diff q_m3s == 0.0, max abs diff et_series == 0.0, all six balance terms bitwise equal
  (ET 6415.077799070474 mm, residual_relative 1.216750862554734e-16). Default path
  provably unchanged. Wall 32.3 s.
- [GATE 4 PASSED] fao56 sanity run (theta_crit=0.6, otherwise identical params):
  ET 7979.0205 mm vs linear 6415.0778 mm (ratio 1.2438, HIGHER as intended);
  residual_relative 2.319e-17 < 1e-12; 0 NaN in q and in the ET series; clip 0.0.
  Runoff drops 16368.24 -> 14812.62 mm as the extra ET must come from somewhere.
- [next/risky] About to edit src/calib_v2.py: add CELLS['H2E'] (bundle model_inputs_v2,
  scored 2009-2018, cache reuses 'H2' files read-only, et_stress='fao56',
  theta_crit=0.6), thread et_stress/theta_crit through Cell.build_params, branch
  eq_state's ET term on et_stress (linear arm byte-identical), and make
  ensure_cache/Cell resolve the cache key so nothing is written to _calib_cache.
- [step5 DONE] calib_v2.py edited: CELLS['H2E'] added (bundle model_inputs_v2, scored
  2009-2018, cache='H2' -> reads H2's existing forcing cache read-only, et_stress='fao56',
  theta_crit=0.6 fixed); Cell.__init__ resolves the cache key and stores
  ET_STRESS/THETA_CRIT from the spec; build_params passes them into MgbParams; eq_state's
  equilibrium ET term now branches on ex.et_stress (linear arm verbatim); ensure_cache
  resolves the cache key so ensure_cache('H2E') finds H2's files and writes NOTHING to
  _calib_cache; module docstring documents the third cell. CLI already generic
  (--cell choices=sorted(CELLS)), so `--cell H2E --out .../dds_H2E_<seed>.npz` yields
  checkpoint dds_H2E_<seed>.part.npz; watch_calib.py globs logs/*.log so H2E_<seed>.log
  is picked up unchanged.
- [next/risky] About to run GATE 6 smoke: 3-evaluation H2E search, seed 99,
  --out in scratchpad (checkpoint dds_H2E_99.part.npz lands there, NOT in _calib_cache).
  Reads H2 cache via mmap (read-only).
- [GATE 6 PASSED] CLI smoke `--cell H2E --seed 99 --budget 3 --out scratchpad/dds_H2E_99.npz`
  exited 0, F 0.182028, arch_f all finite [0.17448905 0.16890837 0.18202829], 10.0 s/eval.
  Direct run_dds_cell(every=1) rerun wrote checkpoint dds_H2E_99.part.npz in scratchpad,
  contents verified (cell H2E, seed 99, budget 3, arch_f finite and identical to the CLI
  run). BOTH smoke files deleted (`rm dds_H2E_99.part.npz dds_H2E_99.npz`, verified gone)
  so the real launch cannot mistake them for a completed run.
- [INCIDENT + FIX] While double-checking, `ensure_cache('H2E')` REWROTE
  _calib_cache/H2_{precip,pet,dates}.npy — a PRE-EXISTING bug my call triggered:
  ensure_cache compared `pd.DatetimeIndex(np.load(fd))` (datetime64[D]) against a [ns]
  date_range; on this pandas the resolutions differ, equals() is always False, and the
  cache is silently rewritten on EVERY call. Verified afterwards: rewritten files are
  byte-identical in content to the bundle (precip/pet/dates all array_equal True), and no
  search workers were running (only sub-17 MB python3.10 processes, far below the 100 MB
  worker threshold). Fixed ensure_cache with the same astype('datetime64[ns]') cast
  Cell.__init__ already uses; re-ran ensure_cache for H2E/H2/H1 — 'cache present', mtimes
  unchanged. Disclosed here per protocol; the launch agent should know H2_*.npy mtimes
  changed today with identical content.
- [validation] MgbParams rejects et_stress='typo', theta_crit in {0.0, 1.5, NaN};
  accepts per-URH length-24 theta_crit; default et_stress remains 'linear'.
- [step1 plan was] step 1 baseline capture: unmodified engine, v2 bundle,
  nb13 cell-10 parameter construction (Wm from bundle, kc/LAI per URH, adr=0.06,
  fint=0.6, b=0.6, k=1.5/8/60, tau from reach_km at 1 m/s), default cold start,
  warmup=2008 (366 d), record = calibration-safe gauges, routing auto.

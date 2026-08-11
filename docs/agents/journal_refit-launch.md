# Journal: refit-launch

GOAL: implement pre-registered signature term(s) from docs/33 s3 in src/calib_v2.py,
gate the change (zero-weight must reproduce H2E F to <=1e-10 rel), register cell H2E-S
(2 seeds, budget 1000), smoke test, race check, then DETACH the refit queue.

Weights from task brief (docs/33 s3.1, row "H-BFI holds / H-PEAK refuted"):
W_KGE 0.34 / W_LOG 0.34 / W_REC 0.17 / W_PEAK 0.15. BFI term NOT triggered.

## Checklist
- [ ] 0. Read docs/33 s3, src/calib_v2.py, src/baseflow.py, scripts/calib_queue_runner.py
- [ ] 1. Baseline capture: F of H2E best vector with UNMODIFIED calib_v2 (expect 0.25931)
- [ ] 2. Implement PEAK term following recession-term pattern
- [ ] 3. GATE: W_PEAK=0 reproduces step-1 F to <=1e-10 relative
- [ ] 4. Register cell H2E-S (2 seeds, budget 1000)
- [ ] 5. SMOKE 3-eval run, finite F, then DELETE smoke checkpoint
- [ ] 6. RACE CHECK (tasklist python3.10, >300 MB) then detached launch
- [ ] 7. Verify startup only (~120 s): queue log, workers >300 MB, watch_calib.py

## Log
- (start) journal created.

### Step 0 — reading (done)
- docs/33 §3.1 outcome table row "holds / refuted" -> cell **H2E-S**, PEAK term only,
  weights (0.34, 0.34, 0.17, 0.15). §3.2: `e_peak = 1 - |ln R_AMS| / ln(1.5)`, passed
  through `c2m` like every other term. §3.3: budget 1000, seeds 20260907 + 20260908,
  everything else identical to H2E (bundle model_inputs_v2, fao56, theta_crit 0.6).
- docs/29 queue is COMPLETE (`logs/queue_runner.log` last line
  `2026-08-05 02:26:49  QUEUE COMPLETE  ok 10  crashed 0  skipped 0`), and all 10
  `dds_*.npz` are on disk. No jobs from it are pending.
- BFI term NOT triggered -> src/baseflow.py is NOT wired into the objective (read only).

### Step 1 — BASELINE CAPTURE (done, UNMODIFIED src/calib_v2.py)
Script: scratchpad/baseline_F.py, archive `dds_H2E_20260901.npz` (the best seed).
```
stored     F = 0.25930593639066796
recomputed F = 0.25930593639066796   (7.9 s)
relative diff = 0.0
```
Search-vector layout asserted equal to `pack_bounds(cell)` (18 dims). Per-gauge terms
k1/k2/k_sim + rc/resid saved to scratchpad/baseline_F.json for the step-3 gate.
**BASELINE F = 0.25930593639066796** (this is the number gate 3 must reproduce).

### Step 2 — implementation (done), src/calib_v2.py ONLY
PEAK term only. `src/baseflow.py` is READ, not wired in: H-BFI holds, so docs/33 §3.1's
third row registers the peak term alone and adding `e_bfi` would be inventing a cell.
- constants: `PEAK_SCALE = ln 1.5`, `AMS_MIN_DAYS = 300`, `W_PEAK = 0.15`,
  `W_SET_PEAK = (0.34, 0.34, 0.17, 0.15)` (literals from docs/33 §3.2, asserted to sum 1),
  `W_SET_INCUMBENT = (0.40, 0.40, 0.20)` unchanged.
- `ams_fleet(Q, years, min_days)` → (n_year, n_gauge) annual maxima, NaN for a
  gauge-year with < 300 finite days; `ams_ratio` → per-gauge MEDIAN over years of
  Qmax_sim/Qmax_obs; `peak_efficiency(r) = 1 - |ln r| / ln 1.5`. Same shape as the
  `recession_fleet` / `rec_efficiency` pair.
- `blend(..., e_peak=None, use_peak=False)`: OPT-IN, off by default; the peak weight is
  `w[3]` and a 3-element `w` gives it 0.0, so the incumbent vector cannot grow a term.
- `Cell`: `self.W` (default incumbent) and `self.USE_PEAK` from the cell spec — separate
  flags on purpose, so the term can be computed at weight zero (that is what makes the
  gate a real test). Observed CAL annual maxima precomputed once (`AMS_OBS_CAL`), exactly
  like `K_OBS_CAL`. `score_cal` now returns `r_ams` as a 4th element; `F_of` passes
  `e_peak` and `w=self.W`, and reports `r_ams` in the extras dict like `k_sim`.
- checkpoint/archive: `arch_ra` added last everywhere (`_arch_arrays`, `_save`,
  `run_dds_cell`, `_main`); a pre-C2b checkpoint without `arch_ra` replays with NaN.
- SIMULATION IS PAIRED before the maxima are taken (docs/33 §2.3): sim masked to the
  observed validity mask, so a simulated peak on an unreported day cannot enter R_AMS.

### Step 4 — cell registered (done)
`CELLS['H2E-S']`: bundle `model_inputs_v2`, cache `H2`, scored 2009-01-01..2018-12-31,
`et_stress='fao56'`, `theta_crit=0.6`, `use_peak=True`, `weights=W_SET_PEAK`. Identical to
H2E in every other respect (docs/33 §3.3). Cell banner confirms on load:
`H2E-S: bundle model_inputs_v2, ... 3652 d, 63 primary gauges, 3 regions` /
`weights (0.34, 0.34, 0.17, 0.15)  peak term ON, 124 of 189 observed CAL gauge-years usable`.

### Step 3 — GATE (PASS)
Peak term COMPUTED, weight forced to 0.0, incumbent 0.40/0.40/0.20 elsewhere:
```
baseline F         = 0.25930593639066796
zero-weight peak F = 0.25930593639066796
absolute diff 0.000e+00   relative 0.000e+00   bar <= 1e-10      -> PASS
per-gauge terms bit-identical to baseline: k1 True, k2 True, k_sim True; rc, resid identical
```
NOT VACUOUS: the term was computed at 51 of 63 gauges (12 gauges have no CAL year with
>= 300 valid days). Bonus: proportional weights (0.34/0.34/0.17/0.00) also reproduce
0.25930593639066796 exactly, so the renormalisation is scale-free as designed.

**Informational, not a threshold and not a decision** (recorded because the launching
session saw it): on the CAL 2012-14 window with the paired mask, H2E's stored vector has
fleet-median R_AMS 0.6482 and median e_peak -0.2400, and its F under the frozen refit
weights is 0.22057354584714875. That CAL-window R_AMS is lower than the 0.820 measured on
the full 2009-2018 record — a different window, as docs/33 §2.3 defines the gate on the
full record and the objective necessarily scores the CAL window (the same asymmetry the
recession term already has). No threshold was touched.

### Step 5 — SMOKE (pass) and checkpoint deletion (done)
`python3.10 src/calib_v2.py --cell H2E-S --seed 20260907 --budget 3 --out <scratchpad>/smoke_H2E-S.npz`
```
H2E-S seed 20260907 budget 3  checkpoint smoke_H2E-S.part.npz
    eval     3/3  best 0.15673  p_pert 0.369
DONE H2E-S seed 20260907: F 0.156731 in 0.4 min (7.92 s/eval)
```
Verified from the written npz, not the exit code: arch_f = [0.1567308, 0.09616702,
0.15334097], all finite; `arch_ra` shape (3, 63) with 51 finite gauges per evaluation.
The smoke output was deliberately written OUTSIDE `_calib_cache` so the queue runner's
"final npz already on disk -> SKIP" rule could never see it.
**DELETED:** `<scratchpad>/smoke_H2E-S.npz`; `smoke_H2E-S.part.npz` had already been
unlinked by `_main` on success. Re-checked on disk afterwards: `_calib_cache` contains NO
`H2E-S` file of any kind and `_calib_cache/logs` contains no `H2E-S` log.

### Regression — the incumbent cells are untouched
H2 seed 20260901: stored 0.25336518371172073, recomputed 0.25336518371172073, rel 0.000e+00,
`r_ams` all NaN and `USE_PEAK` False. (H1 could not be re-scored: its forcing cache
`H1_*.npy` is no longer on disk — that is a missing artifact, not a regression; the H1
cell spec is byte-for-byte unchanged.)

### Step 6 — RACE CHECK (clear) then LAUNCH
`tasklist /FO CSV /NH /FI "IMAGENAME eq python3.10.exe"` -> "aucune tâche en service"
(none); same for `python.exe`. No workers of any weight are running, so there is nothing
to double-launch over. Proceeding to the detached launch.
Queue runner edited: `QUEUES` dict with `docs29` (kept verbatim, COMPLETE) and `c2b`
(`H2E-S` seeds 20260907, 20260908); queue name is argv[1], default `c2b`. BUDGET stays
1000 and MAX_CONCURRENT stays 4 — both untouched.
LAUNCHED (detached, hidden window, cwd = repo root):
`Start-Process -WindowStyle Hidden python3.10 -ArgumentList 'scripts\calib_queue_runner.py','c2b'`
**queue runner PID 23840.** Verifying startup only (the runs take hours); NOT waiting.

### Step 7 — STARTUP VERIFIED (not waiting for completion)
Queue log `data/processed/_calib_cache/logs/queue_runner.log`:
```
2026-08-10 19:44:12  QUEUE START  queue c2b  2 jobs (H2E-S_20260907, H2E-S_20260908), max 4 concurrent, budget 1000, python ...python3.10...
2026-08-10 19:44:12  START H2E-S_20260907  pid 29064  (1/2, slot 1)
2026-08-10 19:44:12  START H2E-S_20260908  pid 28648  (2/2, slot 2)
```
Processes (PowerShell `Get-Process`, working set):
```
23840 python3.10   26.1 MB  (queue runner)
29064 python3.10  457.7 MB  (H2E-S seed 20260907)
28648 python3.10  457.9 MB  (H2E-S seed 20260908)
```
Both workers are well above the 300 MB bar and match the ~465 MB/worker the runner
documents. `python3.10 watch_calib.py` lists `H2E-S_20260907` and `H2E-S_20260908` with
"search workers alive: 2" (no eval line yet at 19:44:41 — the worker logs print every 25
evaluations, so the first row appears after ~25 x ~10 s). Worker log heads on disk:
```
H2E-S seed 20260907 budget 1000  checkpoint dds_H2E-S_20260907.part.npz
H2E-S seed 20260908 budget 1000  checkpoint dds_H2E-S_20260908.part.npz
```
which is the pre-registered budget and the checkpoint naming `watch_calib.py` parses.
A background waiter is watching for the first `.part.npz` (written at evaluation 25).

**LEAVING IT RUNNING is the success condition — do not relaunch.** If the queue is ever
killed, re-running `python3.10 scripts/calib_queue_runner.py c2b` resumes each seed from
its `.part.npz` with the RNG-verified replay; a seed whose final `dds_H2E-S_<seed>.npz`
exists is skipped.

### Issues journalled (none blocking, no threshold touched)
1. The objective scores the CAL 2012-14 window while docs/33 §2.3 defines R_AMS on the
   full 2009-2018 record; the CAL-window fleet-median R_AMS for H2E's vector is 0.6482
   against the 0.820 measured on the full record. The recession term already has exactly
   this window asymmetry (`K_OBS_CAL`), and docs/33 §3.2 registers the term form without
   redefining the scoring window, so it was implemented on the CAL window to match the
   incumbent pattern. Followed as written; recorded here rather than "fixed".
2. 12 of the 63 gauges contribute no peak term (no CAL year with >= 300 valid days).
   `blend` renormalises them onto their remaining terms, which is the pre-registered
   behaviour for a missing signature (docs/33 §3.2: "the new terms inherit that
   behaviour unchanged").
3. H1 could not be re-scored as a regression check: `_calib_cache/H1_*.npy` is no longer
   on disk. Not a code regression — the H1 cell spec is unchanged and H2 reproduced to
   0.000e+00.

### Step 7 (continued) — first checkpoints on disk, search progressing
19:48, ~4.5 min after launch:
```
dds_H2E-S_20260907.part.npz  27,579 B      eval    26/1000  best 0.16156  p_pert 0.534
dds_H2E-S_20260908.part.npz  27,468 B      eval    26/1000  best 0.15673  p_pert 0.534
```
Read back from the checkpoints themselves (not from the log): cell `H2E-S`, budget 1000,
26 evaluations each, every archived F finite, and `arch_ra` carries 51 finite gauges per
evaluation — the peak term is live inside the search, not just in the smoke test.
`watch_calib.py` parses both rows. Processes at 19:48: queue runner 23840 (26 MB),
workers 29064 (457.9 MB, 275 s CPU) and 28648 (458.1 MB, 274 s CPU).
TASK COMPLETE — the queue is detached and alive; do not relaunch.

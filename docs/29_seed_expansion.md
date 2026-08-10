# 29 — Seed expansion of the H1/H2 comparison, plus the H2E (FAO-56 ET) cell

**Status: PRE-REGISTRATION.** This document was written and saved *before* any of the
runs below were launched (2026-08-03, by the `calibration-launch` agent; see
`docs/agents/journal_calibration-launch.md` for the launch record). The job list, budgets
and decision rules are fixed here, in advance, so the conclusions cannot be shaped by the
numbers after the fact.

## 1. Why more seeds

The Phase 3 refit (docs/26) ran two DDS seeds per cell. The results on record:

| cell | seed 20260901 | seed 20260902 | mean F | spread (max−min) |
|------|--------------:|--------------:|-------:|-----------------:|
| H1 (v1 forcing + new objective) | 0.230232 | 0.236772 | 0.2335 | 0.0065 |
| H2 (v2 forcing + new objective) | 0.253365 | 0.234785 | 0.2441 | 0.0186 |

The H2 − H1 gap in mean F is **0.0106, which is SMALLER than H2's own seed spread
(0.0186)**. With two seeds per cell, the forcing repair's effect *on the objective value*
is therefore not established either way (its effect on β/PBIAS is established
independently — docs/26 §5). The remedy pre-registered here is **more seeds at the same
budget**, not longer searches: the question is between-seed variability, and only
replication measures it.

Additionally, the engine has since gained a gated FAO-56 threshold ET option
(`et_stress='fao56'`), and `src/calib_v2.py` carries a pre-registered **H2E** cell
(H2 + FAO-56 ET, `theta_crit` FIXED at 0.6, not searched). Hypothesis (docs/22 §4.6,
docs/26 §5.1): with the threshold form, `kc_mult` comes off its ~2.0 rail (H1 fitted
1.98, H2 1.90 of the (0.5, 2.0) range) at no material cost in F.

## 2. The exact job list (fixed in advance)

Ten searches, each with **budget 1000 evaluations** — identical to the four completed
runs, for comparability — launched through the same CLI entry point
(`python src/calib_v2.py --cell <CELL> --seed <SEED> --budget 1000 --out
data/processed/_calib_cache/dds_<CELL>_<SEED>.npz`):

| # | cell | seed |
|---|------|------|
| 1 | H1 | 20260903 |
| 2 | H1 | 20260904 |
| 3 | H1 | 20260905 |
| 4 | H1 | 20260906 |
| 5 | H2 | 20260903 |
| 6 | H2 | 20260904 |
| 7 | H2 | 20260905 |
| 8 | H2 | 20260906 |
| 9 | H2E | 20260901 |
| 10 | H2E | 20260902 |

Queued by `scripts/calib_queue_runner.py` with **at most 4 concurrent workers**
(~465 MB resident each; the machine cannot take more), in the table order, feeding the
queue as slots free. Logs go to `data/processed/_calib_cache/logs/<CELL>_<SEED>.log` in
the same format as the completed runs (header line, `eval N/M best F` lines), so
`python3.10 watch_calib.py` monitors them unchanged. A crashed job leaves
`logs/<CELL>_<SEED>.err` and the queue continues. The queue's own heartbeat is
`logs/queue_runner.log`. At ~19.8 s/eval, expect ~5.5 h per job and ~16.5 h for the
queue (10 jobs / 4 slots ≈ 3 waves).

The four completed runs (`dds_H1_20260901.npz`, `dds_H1_20260902.npz`,
`dds_H2_20260901.npz`, `dds_H2_20260902.npz`) are **inputs to the analysis and must not
be overwritten, resumed, or re-run.**

## 3. Decision rules (fixed BEFORE launch)

### (a) The seeds question: is H2 separated from H1?

Pool **all 6 seeds per cell** (the 2 existing + the 4 new). Compute per cell:

- `mean(F)` over the 6 seeds;
- `spread = max(F) − min(F)` over the 6 seeds.

Call H2 vs H1 **"separated"** if and only if

```
|mean(F_H2) − mean(F_H1)| > max(spread_H1, spread_H2)
```

**Both outcomes are findings and both will be reported:**

- *Separated:* the zero-suppression repair's effect on the objective is established;
  report its sign and size.
- *Not separated:* the repair does not move the objective beyond seed noise at this
  budget; that closes the question at this budget (docs/26's conclusion that volume
  moved while correlation did not stands on its own evidence and is not at stake here).

No other comparison statistic will be substituted after the fact.

### (b) The H2E question: does the FAO-56 threshold ET free `kc_mult`?

Judged on the 2 H2E seeds (20260901, 20260902). **Success** requires ALL of:

1. **`kc_mult` off its rail:** at each seed's final best point, `kc_mult`'s position in
   its (0.5, 2.0) range is **< 90 %**, i.e. fitted `kc_mult < 1.85`, on **both** seeds.
   (For reference: H1 fitted 1.98 → position 98.7 %; H2 fitted 1.90 → position 93.3 %.)
2. **Recession ratio ≤ 1.5×:** at each seed's final best point, the fleet-median
   simulated-to-observed recession ratio on the CAL window,
   `median_j(k_sim_j / k_obs_j)`, lies within [1/1.5, 1.5], on **both** seeds
   (`k_sim` from the run's stored `arch_ks` at the best evaluation, `k_obs` =
   `Cell('H2E').K_OBS_CAL` — same machinery as the objective's recession term).
3. **No material cost in F:** `|mean(F_H2E over its 2 seeds) − mean(F_H2 over its 6
   seeds)| ≤ 0.01`.

**Anything else — any one condition failing — means the ET hypothesis is refuted, and
that refutation will be reported as a finding**, not hidden. (Per docs/26 §5.1, a
parameter fitted against one objective is a fitted compensation, not a property of the
basin; H2E's parameters are subject to the same caveat.)

## 4. How to read the results when the queue finishes

- **Monitor while running:** `python3.10 watch_calib.py` (one snapshot) or
  `python3.10 watch_calib.py -w` (refresh until workers exit), from the repo root.
- **Completion check:** each finished job leaves
  `data/processed/_calib_cache/dds_<CELL>_<SEED>.npz` and deletes its `.part.npz`;
  `logs/queue_runner.log` ends with a `QUEUE COMPLETE` line; nonzero-size
  `logs/*.err` files mean crashed jobs.
- **Reporting entry:** the reporting code lives in `notebooks/14_calibration.ipynb`,
  which shares its objective/metric functions with the workers via `src/calib_v2.py`
  (that is the module's stated purpose). Extend nb14's seed list to the six seeds per
  cell and re-execute:
  `python -m nbconvert --to notebook --execute --inplace
  --ExecutePreprocessor.timeout=-1 notebooks/14_calibration.ipynb`.
  Alternatively the result files are self-describing npz archives
  (`cell, seed, budget, wall_s, names, x, f, hist, arch_x, arch_f, arch_k1, arch_k2,
  arch_ks`) and the §3 rules can be evaluated directly from them with
  `calib_v2.pack_bounds` / `calib_v2.inv` for the parameter decode.
- **Crash recovery:** re-running a job with the same `--cell/--seed/--budget/--out`
  resumes from its `.part.npz` checkpoint. Resumption is exact, not approximate: the
  RNG is re-created from the seed and the stored evaluations are **replayed with an
  assertion on every proposal vector** — a checkpoint from a different seed, budget or
  code path fails loudly instead of silently continuing a different search
  (`calib_v2.dds`, replay path). The queue runner itself is idempotent: re-launching it
  skips jobs whose final `.npz` exists and resumes the rest from their checkpoints.

## 5. What is NOT being changed

Identical to the completed runs, by construction: the objective (W_KGE/W_LOG/W_REC =
0.40/0.40/0.20, recession log-ratio term, `k_int < k_bas` by construction, `k_bas`
lower bound 5 d), the search space and priors, the DDS algorithm and budget, the
CAL window (2012–14, warm-up 2011), the gauge set, and the forcing caches
(H1_*, H2_*.npy; H2E reads H2's cache — same bundle, same period). Only the seeds are
new, plus the H2E cell whose single change (FAO-56 threshold ET, theta_crit = 0.6
fixed) is gated exactly as pre-registered in `src/calib_v2.py`.


---

## Results (read out 2026-08-10; queue completed 2026-08-05 02:26, 10/10 ok, 0 crashed)

Best F per run, decoded from `_calib_cache/dds_*.npz` with `calib_v2`'s own transform;
recession medians computed exactly as rule 2 specifies (`arch_ks` at the best evaluation
vs the cell's own `K_OBS_CAL`).

| run | best F | kc_mult | rec median |
|---|---|---|---|
| H1 20260901 | 0.23023 | 1.989 | 1.121 |
| H1 20260902 | 0.23677 | 1.982 | 1.158 |
| H1 20260903 | 0.22828 | 1.999 | 1.160 |
| H1 20260904 | 0.21004 | 1.980 | 1.152 |
| H1 20260905 | 0.24044 | 1.973 | 1.019 |
| H1 20260906 | 0.26085 | 1.960 | 1.083 |
| H2 20260901 | 0.25337 | 1.896 | 1.026 |
| H2 20260902 | 0.23479 | 1.997 | 1.294 |
| H2 20260903 | 0.23960 | 1.924 | 1.096 |
| H2 20260904 | 0.23528 | 1.948 | 1.124 |
| H2 20260905 | 0.24067 | 1.935 | 1.188 |
| H2 20260906 | 0.25777 | 1.976 | 1.210 |
| H2E 20260901 | **0.25931** | **1.662** | 1.082 |
| H2E 20260902 | 0.24671 | **1.836** | 1.110 |

### Rule (a) — H1 vs H2 separability: **NOT SEPARATED**

mean F: H1 0.23443 (spread 0.05082) vs H2 0.24358 (spread 0.02298).
Gap 0.00915 < max spread 0.05082. Six seeds per cell did not separate the forcings —
the repair's effect on the objective is smaller than DDS seed noise. Note the best run
overall (0.26085) is an **H1** seed, i.e. the OLD forcing: further confirmation that
seed noise dominates forcing choice at this budget. Consistent with docs/26's controlled
H2−H1 result (volume moved, correlation did not).

### Rule (b) — H2E (FAO-56 threshold ET): **SUCCESS, all three conditions**

1. kc_mult < 1.85 on both seeds: 1.662 and 1.836 — PASS (every H1/H2 seed sits ≥ 1.896).
2. Fleet-median recession ratio in [1/1.5, 1.5] on both: 1.082 and 1.110 — PASS.
3. |mean F_H2E − mean F_H2| = |0.25301 − 0.24358| = 0.00943 ≤ 0.01 — PASS, and the sign
   is POSITIVE: the threshold form scored slightly higher, on top of freeing kc.

The pre-registered hypothesis (docs/22 §4.6) is **confirmed**: the linear stress
ET = kc·PET·(W/Wm) was why kc railed; the FAO-56 threshold form releases it at no cost.

### Caveats, stated before anyone quotes this

- kc came OFF THE RAIL but is not yet plausible: 1.662/1.836 against the FAO-56
  plausibility target of ≤ 1.2 (docs/25 definition of done). The functional form was
  a real cause, not the whole story — the remaining excess ET demand still points at
  the forcing/PET budget (docs/22 §4.5).
- n = 2 seeds for H2E, judged exactly as pre-registered; any further seeds need a new
  pre-registration, not an extension of this one.
- A NEW near-rail appeared: k_int_frac sits at its 0.02 floor in 5 of 6 H2 seeds and
  both H2E seeds (k_int = 0.02·k_bas — the search wants interflow as fast as allowed).
  Equifinality persists elsewhere too (H1 k_bas spans 43–394 d at similar F).

### What follows

H2E becomes the preferred configuration for any further Phase B work (fao56, theta_crit
0.6). The dry-phase ceiling argument (docs/22 §4.7) is untouched by any of this — the
CHIRPS-merge volume fix (docs/18 §15) remains the only identified path to moving r.

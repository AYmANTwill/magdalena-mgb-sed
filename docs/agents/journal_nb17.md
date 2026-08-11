# Journal — nb17 (stage C2b notebook)

GOAL: write `src/nbgen/make_nb17.py` -> `notebooks/17_runoff_signatures.ipynb` documenting stage
C2b: validation of the two quantities MUSLE actually consumes (surface runoff partition, peak
flow), the H-BFI result (not refuted, weak power), the H-PEAK refutation, the REJECTED H2E-S
peak refit, and docs/36's structural adjudication.

Constraints: read-only on frozen artifacts; no calibration launches; no git; only touch
`src/nbgen/make_nb17.py`, `notebooks/17_runoff_signatures.ipynb`, this journal.

## Checklist
- [x] 1. Read nbgen convention (make_nb13.py, make_nb14.py) — md()/code() helpers, numbering
- [x] 2. Read docs/33 (pre-registration + s6-s8 results), docs/36, docs/37 (residual 3)
- [x] 3. Read scripts/c2b/*.py + data/processed/c2b/* (summaries, per-gauge CSVs)
- [x] 4. Locate _calib_cache/dds_H2E-S_*.npz and sim_calibrated_v2/metrics_fleet.csv
- [x] 5. Read journals bfi / peaks / refit-launch
- [x] 6. Write make_nb17.py
- [x] 7. Emit + execute notebook (nbconvert, timeout -1)
- [x] 8. Verify from executed outputs: 0 errors, all cells have execution_count, figure count,
      three-part readings, term definitions
- [x] 9. Report cell/figure counts and any undefined term

## Log
- (start) journal created. `scripts/c2b/` = bfi_figure.py, bfi_measure.py, peaks_measure.py.
  `data/processed/c2b/` = bfi_per_gauge.csv, bfi_summary.json, peaks_per_gauge.csv,
  peaks_summary.json (+ copies of the two measure scripts and bfi_figure.py).
  `_calib_cache/` listing came back empty on a relative-path ls — re-check with absolute path.

### Steps 1-5 — sources read (done)
- Path correction: the calibration cache and the sim outputs are under `data/processed/`, i.e.
  `data/processed/_calib_cache/` and `data/processed/sim_calibrated_v2/`, NOT at the repo root.
  `dds_H2E-S_20260907.npz` (726,134 B) and `_20260908.npz` (723,076 B) both on disk.
- Convention: read `src/nbgen/make_nb13.py` + `make_nb14.py`. `md()`/`code()` append to a list `C`;
  a `cell()` helper emits `execution_count: None`; nb written with `json.dumps(indent=1)`.
  Section numbering `## N.M - title`. Docstring header names the run + nbconvert command.
- docs/33 read in full (1,008 lines): §1-§5 frozen pre-registration, §6 H-BFI result,
  §7 H-PEAK result, §8 the H2E-S verdict. docs/36 read in full (the adjudication).
- EXTRA SOURCE not in the task list but required by CONTENT 4 (the ±30 d widening and the
  81.8 % identity deficit): `data/processed/peakgap/{summary.json,events.csv,
  match_sensitivity.csv,per_gauge.csv}`. docs/36 §8 names them as its own source. Read-only.

### Cheap-reproduction probe (done, BEFORE writing the notebook)
The refit's incumbent-scale F is NOT on disk anywhere (grep for `0.22489` hits only docs prose),
so under the honesty clause it had to be recomputed. It does NOT need the engine: the DDS archive
stores the per-gauge objective terms of every evaluation (`arch_k1`, `arch_k2`, `arch_ks`,
`arch_ra`), and the only observed-side input, `K_OBS_CAL`, comes from
`model_inputs_v2/discharge.npz`. Scratchpad `test_rescore.py`, 1.9 s total, no forcing arrays:
```
20260907: stored 0.2166895543  recomputed peak-scale 0.2166895545  rel 6.89e-10
          incumbent-scale F 0.2248895105   median R_AMS(CAL) 0.9364
          railed: kc_mult@global 0.9753, k_int_frac@global 0.0079
20260908: stored 0.2268935912  recomputed peak-scale 0.2268935911  rel 3.38e-10
          incumbent-scale F 0.2298408916   median R_AMS(CAL) 0.9970
          railed: lai_mult@global 0.0058, k_int_frac@global 0.0143
```
mean incumbent-scale F = 0.2273652, Δ vs H2E's 0.25930593639066796 = **−0.0319407** (1.60× the
0.02 budget). Every docs/33 §8 number reproduces. ONE honest discrepancy to report in the
notebook: §8 says the recomputed peak-scale F reproduces the archived F *"exactly"*; it
reproduces to **~7e-10 relative**, the float32 precision of the archived per-gauge terms.
- Other cross-checks that reproduced from disk (so they can be quoted as executed output):
  docs/33 §6.5's r(BFI_sim,BFI_obs) 0.094, r(diff,BFI_obs) −0.825, BFI_obs range 0.658–0.799,
  12 of 55 above 0.79, area-quartile |ΔBFI| 0.0317 (smallest) vs 0.0081 (largest);
  docs/36's 224 ABSENT single-day spikes with obs_rise > 3 (= 30.4 % of 737), 408 ABSENT with
  P3_pct < 0.33, 99 = 130 × 0.7615 Hortonian cell, ENSO miss 0.716/0.887/0.837.
  docs/36's "74 of 737 (10.0 %) have the storm present at all" DOES reproduce with an exact ≥ 2/3
  percentile cut (an earlier probe used 0.667 and returned 72 — a float artefact, not a
  disagreement).

### Steps 6-8 — generator written, notebook emitted and executed
- `src/nbgen/make_nb17.py` follows make_nb13/14 exactly: module docstring + run/nbconvert lines,
  `OUT` path, `C` list with `md()` / `code()`, `## N.M - title` numbering, and the same `cell()` +
  `json.dumps(indent=1)` footer. Two syntax traps hit and fixed: a nested `"""docstring"""` inside a
  `code(r"""...""")` block terminates the raw string (both in-cell helpers now use `#` comments).
- **notebooks/17_runoff_signatures.ipynb: 108 cells (32 code, 76 markdown), 0 errors, every code
  cell carries an execution_count, 27 figures, each followed by a three-part reading** — verified by
  a script that walks the executed .ipynb, never from the nbconvert exit code. Wall time ~40 s.
- Cheap-only rule honoured: no engine run, no search launched. Heaviest cells are the 880-pass
  BFImax sweep (~4 s) and the 2,000-evaluation archive re-scoring (~10 s).
- New work beyond restating docs/33 and docs/36:
  1. the incumbent-scale F re-scoring recomputed from the archives (docs-prose-only before);
  2. a full quantile ladder — R_50 1.1527, R_75 1.1677, R_90 1.0446, R_95 0.9746, R_99 0.8470,
     R_99.5 0.8340, R_AMS 0.8200 — putting the crossing of unity between the 90th and 95th
     percentile (docs/33 §7.2 said 95th–99th from three points);
  3. an 8-value BFImax sweep: fleet-median BFI tracks the knob with slope 0.962 and the gate ratio
     stays in 0.453–0.743, so no ceiling choice makes H-BFI sharper (docs/33 §6.5 had 2 values);
  4. the frontier over all 2,000 archived evaluations: 663/1000 and 826/1000 sit inside the R_AMS
     band but ZERO reach the incumbent-scale F floor 0.23931 — the conflict is not a local optimum;
  5. a synthetic equifinality demonstration: identical volume, KGE within 0.028, R_AMS 0.488 vs
     1.083 (×2.22), MUSLE peak factor ×1.56, BFI spread only 0.0131.
- FOUR disagreements with docs/33 found by recomputation, all in the notebook's §8.3, none changing
  a verdict: (1) §8's "reproduces exactly" is exact to float32 (rel 6.89e-10 / 3.38e-10);
  (2) §7.7's 0.552^0.56 = 0.723 / −27.7 % is actually 0.7169 / −28.3 %; (3) §7.3's "excluding the 7
  short-record gauges moves nothing material" — the fleet median R_AMS moves 0.8200 → 0.7676, i.e.
  deeper below the band; (4) §7.2's tail switch-on window, refined as above.
- Open issue journalled, also §8.4 item 1: condition 1 and the frontier are CALIBRATION-WINDOW
  statements (the objective scores 2012–14, where the incumbent's own R_AMS is 0.6482, not 0.8200).
  The refit vectors' full-record R_AMS was never computed and cannot be computed cheaply — no
  q_gauge artifact exists for H2E-S. The verdict rests on conditions 2 and 3, so it is unaffected.
- Honest weakness recorded rather than glossed: seed 20260908 had NOT fully converged at evaluation
  1000 (+0.00434 = 1.91 % of final over its last 100 evals, against seed 07's +0.00047 = 0.22 %). It
  would need a 13 % gain to reach the F floor, and docs/33 §3.3 authorises no extra budget or seed.
- Embargo verified by grep: the only `t km^-2 yr^-1` strings are the definition of specific erosion
  and the statement of the embargo itself. No yield is presented anywhere.
- Every term the brief lists appears and is defined at first use; two first-use ordering defects
  were found and fixed (canopy interception glossed in the overview table; rating curve defined at
  §1.1.1 where it is first mentioned, rather than at §7.3).
- Files touched: `src/nbgen/make_nb17.py`, `notebooks/17_runoff_signatures.ipynb`, this journal.
  Nothing else. No frozen artifact modified, no git command run, no wide forcing CSV read.

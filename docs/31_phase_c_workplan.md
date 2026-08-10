# 31 — Phase C work breakdown: every stage, every subtask

Written 2026-08-10. This is the **execution-level** companion to `docs/30_phase_c_plan.md`
(which records the scope decision and the stage logic). Docs/30 says *what and why*; this
document says *exactly what to do, with what inputs, to what gate*. A session should be
able to open its stage section and start working without reading the conversation history.

Conventions used below: every subtask has an ID (`C1.2`), **In** (files it consumes),
**Out** (files it must produce), and **Gate** (the measurable condition that closes it).
"Session" ≈ one focused Claude/working session. All commits `<area>: <summary>`, pushed
to `origin main`. One session on this repo at a time.

---

## 0 — Ground truth this plan builds on (do not re-derive)

| fact | value | source |
|---|---|---|
| Adopted hydrology | **H2E** = v2 forcing + revised objective + FAO-56 ET (θ_crit 0.6) | docs/29 read-out |
| Best H2E run | seed 20260901, **F 0.25931**, kc_mult 1.662, recession median 1.082 | `_calib_cache/dds_H2E_20260901.npz` |
| Second H2E seed | 20260902, F 0.24671, kc_mult 1.836, recession 1.110 | same dir |
| H1 vs H2 verdict | **not separated** (gap 0.009 < seed spread 0.051) | docs/29 §Results |
| Dry-phase ceiling | El Niño r pinned 0.556–0.572 across 12 configs (docs/22 §4.7); field LOOCV skill 0.429 (docs/18 §12, docs/26 §7 — the all-period gauge-only median; docs/22 §4.7's per-window El Niño field skill is 0.40, a different statistic) | docs/22 §4.7; docs/18 §12 |
| CHIRPS merge | LOOCV **passed** (r 0.447), volume **failed** (+7.5 %) → rejected; fix identified | docs/18 §15 |
| SSC data | `sediment_daily.csv`: 269,337 rows, 1979–2018, cols incl. `ssc_mean_mg_l`, `ssc_surface_mg_l`, `approval`, `flag_corrupt/zero/flatline` | data/processed |
| SSC stations | 79 total, but **28 mapped / 33 with coords / 24 calibration-safe**; 46 unmapped (no coordinates) pending the docs/19 §5.2-item-2 coordinate+area fetch (see C1.0). `calibration_safe` is geometry-only (no SSC-quality gate) | `sediment_inventory.csv` (measured 2026-08-10), docs/19 §3.7 |
| MUSLE K | per-minibacia in `minibacia_soil_params.csv:K` (t·ha·h/(ha·MJ·mm)) | nb09 |
| Areas | per-gauge catchment areas untrustworthy in BOTH team networks (36 % of 85 shared gauges disagree >2×) | docs/23 §13.2 |
| Rating curves | median R² **0.54** across 33 pairs; per-pair list in `data/processed/rating_curves.csv` (cols code/name/n_pairs/a/b/R2). docs/13 is the pairing-candidates doc — it carries **no R² values** | `rating_curves.csv` (nb06); docs/13 |
| Flux conversion | Q (m³/s) × C (mg/L) × **0.0864** = t/day | arithmetic |
| MUSLE defaults | α = 11.8, β = 0.56 (Williams 1975) — starting values, to be calibrated | literature |
| Sediment skill bar | Fagundes et al. 2026 report sediment KGE **−0.26 to 0.44** | the source paper |
| Literature flux anchor | Magdalena suspended load at Calamar ~140–180 Mt/yr (Restrepo et al.). docs/06:9 already records **~145–169 Mt/yr** with citations; Restrepo & Kjerfve (2000) give **144 Mt/yr** (1975–1995). **C2.4** (not C2.5) reconciles against docs/06 and fetches the exact figure before quoting | docs/06:9; confirm in C2.4 |

Standing rules (docs/18 §7 traps + additions): never `pd.read_csv` the wide forcing CSVs
(`src/forcing_npy.py`); verify from executed outputs, never exit codes; pre-register every
calibration cell before searching; check fitted parameters against their bounds before
interpreting; test for **absent** records, not just flagged values; a filename count is
not a file check; report every effect at basin AND local scale; journals in `docs/agents/`
for any multi-step run.

---

## Stage C0 — freeze and report H2E (1 session)

Goal: the hydrology Phase C consumes exists as reviewed artifacts, not as a checkpoint file.

### C0.1 Extract and record the adopted parameter set
- **In:** `_calib_cache/dds_H2E_20260901.npz`, `src/calib_v2.py` (decode: `exp()` on
  `IS_LOG` dims, names like `kc_mult@global`, `wm_mult@R1`, `adr@soil2`).
- **Out:** `sim_calibrated_v2/parameters_H2E.csv` — same schema as `parameters_H1.csv`
  (parameter, scope, value, prior, lo, hi, pos, railed).
- **Gate:** kc_mult reads 1.662; flag `k_int_frac` at its 0.02 floor (`railed=YES`, it is).

### C0.2 Reproduction gate before anything is interpreted
- Rebuild the H2E cell (`cv.Cell('H2E')`), evaluate the stored best `x`, and require the
  recomputed objective to match the archived **0.25931** to ≤ 1e-8 relative (the
  established 9.1e-9 harness bar, docs/22).
- **Gate:** match, or STOP — a mismatch means the environment drifted and nothing
  downstream is trustworthy.

### C0.3 Full simulation + per-period metrics
- Run the engine (fao56, θ_crit 0.6) on `model_inputs_v2/` with the decoded set; 2008
  warm-up, score 2009–2018.
- **Out:** `sim_calibrated_v2/q_gauge_H2E.npz`; append H2E rows to `metrics_fleet.csv`
  with the identical column set (KGE, NSE, r, alpha, beta, pbias, kge_gt0, kge_gt05, n,
  clim_kge, skill_over_clim, rec_ratio) for periods: CAL 2012-14, VAL all,
  VAL La Nina 11, VAL El Nino 15-16, VAL other 09/10/17, VAL 2018.
- **Gate:** mass-balance residual < 1e-15 relative; per-period rec_ratio ≤ 1.5×
  everywhere (the seed-level medians were 1.08/1.11).

### C0.4 The two tables every later stage quotes
- (a) H2E vs H1-fit vs H2-fit vs Config B, VAL-all row (the four-attempt history).
- (b) ENSO asymmetry restated for H2E: skill-over-climatology in La Niña vs El Niño —
  this is the number C5 inherits as its hydrology caveat.
- **Out:** addendum section in `docs/26_phase3_refit.md`; update the docs/24 outline's
  attempt table (it currently stops at attempt 3).

### C0.5 Precompute and store the sediment drivers
Sediment evaluation must not re-run hydrology. Store per-minibacia daily fields the
sediment model needs: surface runoff `Qsur` (mm/day), total reach inflow, and the
chosen peak proxy input (see C3.3).
- **Out:** `data/processed/sim_calibrated_v2/h2e_drivers.npz` (float32, (3652, 8672) per
  field, ~250 MB — gitignored; regeneration command recorded in docs/20).
- **Gate:** `np.load` round-trip; column sums match the run's water balance to 1e-6.

### C0.6 Commit
`results: adopt H2E — full report and frozen sediment drivers`.

**Paste-prompt for the session:** *"Execute stage C0 of docs/31 exactly: subtasks
C0.1–C0.6. The reproduction gate (C0.2) blocks everything else. Verify from executed
outputs; journal to docs/agents/journal_c0.md."*

---

## Stage C1 — the SSC-quality gate (1–2 sessions) — **the real unblock**

Goal: replace "blocked on mainstem SSC quality" with a per-station, evidence-based
classification. The precipitation QC playbook transposes almost one-for-one.

### C1.0 Resolve the network size — coordinate + area fetch (docs/19 §5.2 item 2) — **do this first**
The §0 table is now honest: `sediment_inventory.csv` has **28 of 79 stations mapped** (33 with
coordinates, 24 calibration-safe); 46 have no coordinates at all (docs/19 §3.7, CONFIRMED). C1
therefore cannot classify "79 usable stations" until those 46 are located.
- **In:** `sediment_inventory.csv`; `src/fetch_station_coords.py` (single commit `b4a1230` — the
  docs/19 §5.2-item-2 extension was never built).
- **Do:** extend `fetch_station_coords.py` to pull the IDEAM catalogue **coordinate + catalogue
  drainage area** for the 46 unmapped codes, then re-snap by **drainage-area matching** (docs/19 §5.2).
- **Out:** updated `sediment_inventory.csv` with the newly-mapped stations flagged `mapping_action=catalogue`.
- **Gate / decision (record explicitly, do not inherit):** either (a) the fetch raises the mapped
  count — record the new number — or (b) it cannot, and Phase C is **run on the mapped subset**
  (28 mapped / 24 calibration-safe), with the 46 dark stations carried as `ssc_class=excluded,
  reason="no coordinates"` in C1.6. One of (a)/(b) MUST be written before C1.1 sizes coverage.

### C1.1 Coverage census
- Per station × year: sample count; days in 2009–2018; days inside the two ENSO windows
  (2011 calendar year; 2015-01→2016-12); `approval` distribution (Definitivo > En
  revisión > Preliminar); `ssc_mean` vs `ssc_surface` availability.
- **Out:** `sediment_coverage_census.csv`; a bar figure per station (reuse the nb06
  availability-plot style).
- **Gate:** an explicit list of stations with ≥ N samples in BOTH ENSO windows (pick N
  after seeing the distribution — pre-register it in the session journal before
  computing the classification, so the threshold is not tuned to the answer).

### C1.2 Sampling-selectivity — the transposed zero-suppression lesson
SSC is campaign-sampled; the risk is **sampling preferentially on high-flow days**, which
inflates any naive flux mean. Value screens cannot see this; the sampling-date pattern can.
- For each station with a paired discharge record (`is_discharge_station` or the docs/13
  pair): compute the **flow-percentile of each SSC sampling date** within that station's
  full discharge record. Unbiased sampling ⇒ median percentile ≈ 0.5.
- Calibrate the null — and avoid a circularity the precipitation version did not face:
  density alone does NOT define "unbiased", because a densely-sampled station can still
  be flow-chasing (campaigns sent out when the river is high). The null pool is stations
  whose sampling dates are **calendar-regular** — test the inter-sample date spacing for
  schedule structure (low dispersion of gaps, e.g. near-monthly) — because
  calendar-driven sampling is unbiased with respect to flow BY CONSTRUCTION, whatever
  its density. Flag stations whose median sampled-day flow percentile exceeds that null
  pool's p99. If fewer than ~10 calendar-regular stations exist, say so and fall back to
  the theoretical null (percentiles ~ Uniform(0,1), median 0.5) with the weaker-null
  caveat recorded.
- **Out:** `ssc_sampling_selectivity.csv` (station, n, median percentile, flag).
- **Gate:** the null is calibrated (**calendar-regular** stations ≈ 0.5, per the method above —
  NOT dense stations, which can be flow-chasing) before any station is flagged.
  Record both the biased list AND the consequence: for flagged stations, only
  rating-curve flux estimates (C2.2) are usable, never sample-mean flux.

### C1.3 Value screens with the corrected null
- Re-adjudicate `flag_flatline` runs using docs/19's corrected local-quantisation null
  (0.030 % within-year / 0.234 % within-14-day — NOT the flawed 0.00037 %).
- Review `flag_corrupt` and `flag_zero` counts per station; zeros in SSC are suspect
  (a river is never at 0 mg/L) — classify zero-runs as missing-coded-as-zero unless
  neighbouring samples corroborate near-zero.
- Extreme values: **corroborate before deleting** (the source paper's own rule — its
  744 mg/L peak was real; *to confirm from the paper in C2.4, no in-repo anchor yet*). Corroboration = same-day or ±3-day high discharge at the
  paired gauge, or a same-event neighbour.
- **Out:** amended flags in `sediment_daily_qc.csv`.
- **Gate:** zero deletions without a recorded corroboration check.

### C1.4 Rating-era segmentation
- SSC often rides the same stage record as discharge: docs/17's SNHT break list applies.
  For each paired station, mark in-window breaks; each segment between breaks is an
  **era**. Rating fits (C1.5, C2.2) are per-era, never pooled across a break.
- **Out:** `ssc_station_eras.csv` (station, era_start, era_end, break_source).

### C1.5 Sediment rating relations, per station per era
- Fit `log Qs = log a + b·log Q` on QC'd same-day pairs (Qs = flux from C's conversion).
  Record R², n, residual σ per fit. Median fleet R² ≈ 0.5 is the expectation (`rating_curves.csv`: 0.54/33 pairs);
  that is usable-with-stated-uncertainty, not disqualifying.
- **Out:** `ssc_rating_fits.csv`.
- **Gate:** every fit's n and R² recorded; fits with n < 15 pairs marked unusable.

### C1.6 Classification — the deliverable
Every one of the 79 stations gets exactly one class, with the measurement that decided it:
- **usable** — coverage in both windows, unbiased or correctable sampling, ≥1 usable
  rating era covering the windows;
- **usable-with-caveat** — one deficiency, named (e.g. biased sampling → rating-only);
- **excluded** — with the specific evidence (**no coordinates** (the 46 unmapped, per C1.0) /
  no window coverage / no plausible rating / corrupt record), never a blanket rule.
- **Out:** `sediment_inventory_qc.csv` with `ssc_class` and `ssc_class_reason`;
  `docs/32_ssc_qc_audit.md` documenting method, nulls, and the per-station table.
- **Gate:** 79/79 classified; the mainstem-vs-tributary split stated (C4 needs the
  tributary list); the count of usable stations inside each ENSO window stated.

### C1.7 Commit
`sediment: SSC-quality gate — 79 stations classified with evidence`.

**Paste-prompt:** *"Execute stage C1 of docs/31 (subtasks C1.1–C1.7). Pre-register the
coverage threshold and the selectivity null before computing classifications. The
deliverable is docs/32 + sediment_inventory_qc.csv with all 79 stations classified."*

---

## Stage C2 — the observational ENSO contrast, model-free (1 session)

Goal: the target table C5 must reproduce — publishable on its own.

### C2.1 Pre-register windows and estimators (before computing anything)
- Primary windows: **calendar 2011** (La Niña) vs **2015-01→2016-12** (El Niño).
- Sensitivity windows: 2010-07→2011-06 and 2015-10→2016-04 (ONI-peak definitions).
- **Why the team gets to pick these:** the window definition was an open advisor question
  (docs/28:258, slide-2 QA: "Why not 2010–2012 for La Niña?" — flagged for the advisor; NOT in
  docs/21's open-item table) and the advisor declined to answer (docs/30
  §1). The sensitivity windows ARE the mitigation for that unresolved choice — every C2
  and C5 result is reported for the primary AND sensitivity windows, so no conclusion can
  hinge on the window definition alone. A reviewer meeting the docs/21 open item should
  read this as "resolved by bracketing", not as a contradiction.
- **Comparability rule (hard):** the primary windows have unequal lengths (12 vs 24
  months). Cross-window comparisons therefore use RATES ONLY — t/day (and monthly means).
  Window totals (t) may be reported per window for context but NEVER as a wet:dry ratio;
  a ratio of unequal-window totals is meaningless by construction.
- Two flux estimators, both reported: (a) sample-day flux mean (only for stations
  passing C1.2 unbiased), (b) rating-curve flux on all days (per-era fits from C1.5),
  with uncertainty from residual σ.
- **Out:** the registration block at the top of `docs/33_observed_enso_contrast.md`.

### C2.2 Compute
- Per usable station: mean daily flux (t/day), monthly shape, and the wet:dry ratio
  **computed on rates per the C2.1 comparability rule**; window totals (t) as context
  only; for both windows × both estimators; bootstrap CI (resample sample days; resample
  rating residuals).
- **Absolute flux only. No t/km²/yr anywhere** (docs/23 area embargo).
- **Out:** `observed_enso_contrast.csv`; figures: per-station wet:dry ratio (dot plot,
  stations ordered downstream), flux time series at the 3–5 best stations, monthly shape.

### C2.3 Consistency checks
- Estimator (a) vs (b) at stations where both are valid — disagreement beyond the CI is
  a C1 flag that was missed; go back.
- Downstream monotonicity along the mainstem where stations nest (flux should not
  decrease downstream absent a known sink; the Momposina IS a known sink — annotate it).

### C2.4 Literature anchor
- Compare the outlet-most usable station's annual flux against the published Magdalena
  load (~140–180 Mt/yr; **fetch and cite the exact Restrepo figure here**). Order of
  magnitude agreement = pass; disagreement = investigate before proceeding.

### C2.5 Commit
`sediment: observed ENSO flux contrast — the C5 target table`.

**Paste-prompt:** *"Execute stage C2 of docs/31. Write the pre-registration block FIRST
(C2.1), then compute. Deliverables: docs/33, observed_enso_contrast.csv, figures."*

---

## Stage C3 — MUSLE hillslope erosion on our engine (2–3 sessions)

Goal: `Sed = α·(Qsur·qpeak·A)^β · K · C · P · LS2D` per URH per day, driven by frozen
H2E runoff, verified the way the hydrology engine was.

### C3.1 LS2D factor (the one missing static input)
- Desmet & Govers (1996) two-dimensional LS from the conditioned DEM (the nb07 chain
  already produces filled DEM + D8 + accumulation): per cell
  LS = (m+1)·(A/22.13)^m·(sin β/0.0896)^n, aggregated area-weighted per URH per minibacia.
- **Out:** `minibacia_ls2d.csv` (or per-URH npz); a map figure.
- **Gate:** distributional sanity — LS ∈ (0, ~72], basin median in the literature range
  for mountainous basins (~2–10); flat lowlands ≪ Andean flanks visually.

### C3.2 C and P factors
- Map the 8 hydrological land classes → C values (take Fagundes' table as primary; keep
  the mapping in a reviewable CSV, not hardcoded). P = 1.0 basin-wide (no conservation-
  practice data) — stated, not hidden.
- **Out:** `urh_cp_factors.csv` with a source column per value.

### C3.3 The qpeak proxy — pre-registered choice
A daily model has no sub-daily peak. Options, to be registered before implementation:
1. `qpeak = Qsur/86400` (daily mean as peak — floor estimate);
2. SCS-triangular: `qpeak = f(Qsur, t_c)` with time of concentration from reach length
   (`reach_km` in `topology.npz`) and **slope — to be derived from the nb07 DEM chain; it is
   NOT a shipped artifact** (topology.npz has no slope key; verified 2026-08-10);
3. the source paper's own formulation — **read Fagundes' methods section first; use
   theirs if extractable** (transposition claim is stronger).
- **State the known bias direction before calibrating:** docs/22 measured α < 1 (peaks
  undersimulated) at most gauges, worst at the largest; therefore raw MUSLE will
  under-erode at large scale, and calibration of α/β will partially absorb that. Write
  this in the code docstring AND docs — it is the sediment twin of the celerity
  surrogate.

### C3.4 Implement `src/mgb_sediment.py`
- Vectorised like `mgb_hydrology.py`; consumes `h2e_drivers.npz` (C0.5), K, C, P, LS2D;
  produces per-minibacia daily hillslope load (t/day) delivered to the reach.
- Engine-grade tests in `tests/test_sediment.py`: zero-rain ⇒ zero erosion; strict
  monotonicity in K, C, LS; units audit (a hand-computed single-cell case matches to
  1e-12); NaN-free; a mass ledger (eroded = delivered + stored, exact).
- **Gate:** pytest green including the new file.

### C3.5 Cross-check against implementation B
- **In (acquire first — it is NOT in this repo):** `musle.py`/`sediment.py` are the team's
  second-implementation files; `find` confirms they exist nowhere under `c:/dev` and no path/URL
  is recorded (docs/20:43 documents impl-B as "the one input not rebuildable from this repo
  alone"). **Request them from the team and record the drop location in docs**, OR re-scope this
  subtask to compare against implementation B's *published numbers* (as docs/23 §13 did for areas).
- Same sub-basin, same inputs, our module vs the team's `musle.py`: agreement to within
  the C/P mapping differences (document any residual). This is the Phase B
  two-implementation discipline applied to sediment.
- **Out:** a short comparison note in docs (numbers, one figure).

### C3.6 First uncalibrated basin run — order-of-magnitude gate only
- Basin-total hillslope erosion (Mt/yr) with α=11.8, β=0.56 defaults vs the literature
  anchor. Expect the wrong number (uncalibrated, no deposition yet) — the gate is
  **order of magnitude and spatial pattern** (Andean flanks ≫ lowlands), nothing more.
- **Out:** erosion map figure; the number, recorded with its caveats.

**Paste-prompt:** *"Execute stage C3 of docs/31 (C3.1–C3.6). Register the qpeak choice
(C3.3) with its bias statement before writing the module. mgb_sediment.py needs
engine-grade tests; verify against implementation B on one sub-basin."*

---

## Stage C4 — channel transport + sediment calibration (2–3 sessions)

### C4.1 Transport + the honest sink statement
- Advect the suspended load through the reach network with the existing storage routing;
  first-order deposition/settling term per reach (parameter, calibratable).
- **Write the Momposina limitation into the module docstring before calibrating:** the
  floodplain sink is NOT represented (Muskingum X=0; celerity already acts as a storage
  surrogate, docs/22 §4.6) ⇒ expect systematic over-delivery at/below Mompós. Mitigation
  is structural: **calibrate on tributary and upper-mainstem stations upstream of the
  Momposina**; evaluate — never calibrate — below it.

### C4.2 Pre-registration (before any search)
- Cells: parameters {α, β, settling velocity/deposition coefficient}; bounds from
  literature (α ∈ [2, 30], β ∈ [0.4, 0.75], registered exactly at write-time);
  objective = KGE on **log flux** (flux spans decades) at the C1-usable tributary set;
  CAL = neutral years 2012–14; **both ENSO windows out-of-sample** (Klemeš, as in
  Phase B); DDS, 2 seeds minimum, budget set after a timing probe (sediment evals are
  cheap — hydrology is precomputed).
- **Spin-up clarification (a reviewer WILL flag this, so it is stated here):** the
  sediment model runs over the full 2009–2018 driver record and is SCORED only on the
  registered windows. The 2009–2011 span, including La Niña 2011, therefore feeds
  antecedent sediment state into the 2012–14 calibration window. That is physics, not
  fitting: no 2011 observation enters the objective, no parameter is adjusted against
  2011 data, and the ENSO windows remain strictly out-of-sample. "Warm-up ≠ scored" is
  the same distinction Phase B used for 2008 (docs/26).
- Decision rules registered with the cells: success = median log-flux KGE within
  Fagundes' −0.26…0.44 band at calibration stations AND parameters off their bounds;
  report every outcome.
- **Out:** `docs/34_sediment_calibration.md` pre-registration section.

### C4.3 Search, report, verdict
- Same machinery pattern as `calib_v2` (checkpoints, logs watch_calib can parse,
  detached queue if runs are long — they should not be).
- Report per-period at every usable station: calibration set, validation set, and the
  below-Momposina stations separately (expected to fail; that failure is the measured
  cost of the missing sink, and it goes in the report as such).
- **Gate:** parameters checked against bounds; seed spread reported; verdict against the
  registered rules, both directions reportable.

**Paste-prompt:** *"Execute stage C4 of docs/31. C4.2's pre-registration must be
committed before the first search runs. Calibrate upstream of the Momposina only."*

---

## Stage C5 — the ENSO experiment (1–2 sessions) — the project's deliverable

### C5.1 The contrast run
- Calibrated sediment model, full 2009–2018; extract both ENSO windows (primary + the
  C2.1 sensitivity windows).

### C5.2 Prediction vs target
- Simulated vs C2's observed table, station by station: sign of the contrast, magnitude
  ratio, seasonal timing. State explicitly which comparisons are **out-of-sample
  predictions** (everything in the ENSO windows) — this sentence is the credibility of
  the whole project.
- Inherited caveat, stated up front: the dry-phase hydrology sits at its input ceiling
  (El Niño r ≈ 0.57), so El Niño flux errors are bounded below by the water errors;
  quantify by propagating H2E's El Niño discharge bias through the rating relation.

### C5.3 Spatial attribution — what the process model adds
- Per-minibacia erosion difference map (2011 − 2015/16); ranked sub-basin contributions
  to the outlet flux difference.
- **Pre-registered factor-swap experiments** (the mechanism question): (a) 2011 rainfall
  on 2015 antecedent moisture, (b) vice-versa, (c) rainfall amount scaled vs pattern
  swapped. Each swap isolates one candidate mechanism (amount / pattern / antecedent
  state). Register the swap list before running any of them.

### C5.4 Write-up
- `docs/35_enso_contrast_results.md` + figure set; updates to docs/21 and the
  presentation material (docs/24 chain). Every number carries its window and its
  prediction/description label.

**Paste-prompt:** *"Execute stage C5 of docs/31. Register the factor-swap list (C5.3)
before running any swap. The deliverable is docs/35 plus the figure set."*

---

## Background track — bounded, never gating

### B1 CHIRPS refit (≤ 2 sessions, then stop either way)
- Refit the per-(elevation band × hydrographic zone) quantile maps **only on stations that
  pass the selectivity test (~1.00)** (docs/18 §15.4; `journal_chirps-merge.md` follow-up) —
  optionally after finishing the zero-suppression repair on the 139 residual rain-selective
  stations first (§15.3, which is upstream of any usable merge). *The identified mechanism* of
  the +7.5 % volume failure is those 139 residual rain-selective stations transferred through
  reporting-day-conditioned maps (docs/18 §15.3) — **not** merely the absence of `Inferido_seco`
  days, which only dries already-repaired stations and would leave the volume gate failing.
  Rerun BOTH gates unchanged: volume within 1 % of 2,036.4 mm/yr (2009–17); LOOCV median daily r > 0.429.
- Both pass → produce forcing v3 + nb11/nb12 rebuild + ONE pre-registered cell
  (H3 = v3 + H2E physics, 2 seeds) and stop. Any gate fails → the negative result closes
  the CHIRPS question permanently; write it and stop.

### B2 k_int_frac floor probe (≤ ½ session)
- 7 of 8 v2-forcing seeds sit on the 0.02 floor (docs/29). One run: bound 0.02 → 0.005,
  H2E config, seed 20260901, budget 1000. Report where it lands and what F does.
  **No adoption without a new pre-registration** — this is reconnaissance.

### B3 External catchment areas (async, unblocks yields only)
- Acquire an arbiter independent of both team networks: IDEAM's official station
  catalogue drainage areas (request/download), and/or HydroSHEDS-HydroATLAS snapping as
  a third derivation. Success = the 31 disputed gauges adjudicated; then and only then
  t/km²/yr yields become reportable (revisit C2/C5 outputs).

### B4 Remote-sensing SSC cross-check (optional, 1 session)
- The team's RS retrieval (Landsat-8/Sentinel-2) vs in-situ SSC on matching dates at
  C1-usable stations — an independent check on both, and Phase C's analogue of the
  two-implementation cross-validation.

---

## Dependencies and suggested order

```
C0 ──────────────► C3 ──► C4 ──► C5
      C1 ──► C2 ─────────► C4 (calibration targets come from C1/C2)
B1, B2, B3, B4: independent; B1 success re-opens hydrology ONLY via a new pre-registration
```

Core path ≈ **8–12 sessions**; background ≤ 3½. Nothing in the background track blocks
the core path — by decision (docs/30 §1), not by accident.

## Risk register (each with its mitigation already in the plan)

| risk | where it bites | mitigation |
|---|---|---|
| qpeak proxy bias (daily model, α<1 at big gauges) | C3/C4 absorb it into α,β silently | bias direction stated before calibration (C3.3); tributary-first calibration |
| Momposina sink missing | over-delivery below Mompós | calibrate upstream only; below-Mompós reported as evaluation, with the failure attributed (C4.1) |
| SSC sampling bias | inflated naive flux means | C1.2 selectivity statistic with calibrated null; rating-only flux for flagged stations |
| rating R² ≈ 0.5 | wide flux CIs | dual estimators + bootstrap CIs (C2.2); uncertainty carried into C5 |
| catchment-area errors | any per-area number | flux-only embargo until B3 delivers an external arbiter |
| α/β equifinality | C4 parameters uninterpretable | pre-registered bounds + seeds + bound checks, as in Phase B |
| dry-phase hydrology ceiling | El Niño flux accuracy | propagated quantitatively in C5.2; named in every ENSO claim |
| forcing changes mid-phase | silent invalidation of C0's freeze | B1 can only re-open hydrology through a new pre-registration |

---

## Review protocol — for any session auditing this plan for contradictions

This plan is deliberately pointer-justified: the evidence for a choice lives in the doc
cited next to it (docs/16–29), not duplicated here. A reviewing session must therefore
classify every suspected fault as one of three things BEFORE reporting it:

1. **Pointer-resolved** — the justification exists in the cited doc. Follow the citation
   first; docs/22 §4.x and docs/29 §Results carry most of the load. Not a finding.
2. **Known-open** — already on the register below. Confirming it is not a discovery;
   resolving it is.
3. **Genuine contradiction or unjustified choice** — nothing in the repo grounds it.
   THIS is a finding. Report it with the two clashing statements quoted verbatim and
   their file locations.

A reviewer that reports category-1 items as faults has been misdirected by its own
shallowness; a reviewer that finds a real category-3 item has improved the plan. Apply
the same bar this project applies to itself: measured claims beat plausible ones, and
"I could not find the justification" must state where you looked.

### Known-open register (confirmed, unresolved — confirming these is not a discovery)

| # | item | where flagged |
|---|---|---|
| 1 | docs/24 (slide 8: "3 of 10") vs docs/26 §5 ("2") disagree on attempt-3's railed-parameter count | docs/21 |
| 2 | kc_mult 1.662/1.836 is off its rail but still above the FAO-56 plausibility bar of ≤1.2 — the ET form was a real cause, not the whole story | docs/29 §Results caveats |
| 3 | k_int_frac sits on its 0.02 floor in 7 of 8 v2-forcing seeds — a new near-rail, unprobed until B2 | docs/29 §Results caveats |
| 4 | Older docs (12, 19, 21, 24, 25, 28) still carry "Phase C blocked on mainstem SSC" — superseded by docs/30 §1, not yet edited in place | docs/30 |
| 5 | The Restrepo outlet-flux anchor (~140–180 Mt/yr) is unverified until C2.4 fetches the exact figure and citation | §0 table |
| 6 | The ENSO window definition was never adjudicated by the advisor; C2.1 resolves it by primary+sensitivity bracketing, not by authority | docs/21, C2.1 |
| 7 | H2E is adopted from n=2 seeds, exactly as its pre-registration allowed; more seeds require a NEW pre-registration | docs/29 |

**2026-08-10 review applied.** Findings F1–F9 of `docs/agents/review_2026-08-10_docs31.md` were
corrected in place: F1 (SSC network 79→28, added C1.0 coordinate fetch), F2 (ENSO pairing decision
recorded in docs/30 §1), F4 (C1.2 gate → calendar-regular), F3 (B1 refit re-spec), F5 (musle.py
acquisition line), F6 (slope not in topology.npz), F7 (four pointers), F8 (docs/30 ratio wording),
F9 (744 mg/L marker). Register #1 (railed-count 3-vs-2 discrepancy) is **RESOLVED with evidence** in
that review §3 (one 18-dim vector, two denominators: parameters_H2.csv marks 3 railed dims incl.
regional `wm_mult@R2`; docs/26 §5's "2" counts globals only). All four load-bearing findings
(F1, F4, F5, F6) were re-verified against disk before applying.

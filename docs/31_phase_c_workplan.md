# 31 — Phase C work breakdown: every stage, every subtask

> **Numbering corrected 2026-08-10:** 33 = C2b pre-registration · 34 = C2 observed
> contrast · ~~35 = C4 sediment calibration · 36 = C5 results~~. Earlier text pointed the
> C2 contrast at 33, which C2b took first.
>
> **⚠ THE CORRECTION ITSELF WENT STALE — re-corrected 2026-08-12.** A note headed
> *"Numbering corrected"* is trusted over a file listing, so this is the more misleading half.
> The true assignment on disk (`ls docs/*.md`, checked 2026-08-12): **35 = `35_qpeak_preregistration.md`**
> (the C3.3 `q_peak` proxy registration) · **36 = `36_peak_deficit_options.md`** (the peak-deficit
> adjudication) · **45 = `45_c4_preregistration.md`** is the C4.2 pre-registration · ~~**the C5
> results document is unwritten and takes the next free number, 54**~~ (`docs/00_INDEX.md` §3:
> *"**44 was never assigned** … the next free number is 54"*). The `Out:` targets in C4.2, C5.4
> and C2's paste-prompt below are annotated accordingly — **a stale target in a paste-prompt
> writes the wrong file, it does not merely mislead.**
>
> **⚠ THE 54 TARGET IS ITSELF STALE — corrected 2026-08-19.** 54 was claimed by
> `54_c3_1_closure_and_c4_entry_status.md`; the **C4.3 verdict landed as
> `55_c43_verdict.md`** and the **C5 results document landed as `56_c5_enso_application.md`**
> (both 2026-08-12), with 57/58/59 taken since (`57_b5_gauge_expansion.md`,
> `58_rainfall_ceiling_bound.md`, `59_cross_implementation_comparison.md`). **Do not write to 54.**
> Checked against `ls docs/*.md` 2026-08-19.

> **⚠ STAGE STATUS POINTER, added 2026-08-12.** This is a *plan*: its stage sections say what to
> do, not what has happened. Per RULE 0 (`docs/00_INDEX.md`) **status is owned by
> `progress_map.html`**, and each stage's *outcome* is owned by its own document. ~~As of
> 2026-08-12~~ → **refreshed 2026-08-19** — C4.3 has since RUN (`docs/55`) and C5 is COMPLETE
> (`docs/56`); the two rows those outcomes touch carry the superseded text struck through. From
> those owners:
>
> | stage | owner | outcome |
> |---|---|---|
> | **C0** | `docs/26` Addendum | **complete** — H2E frozen, reproduction gate F = 0.25931 |
> | **C1** | `docs/32` (+ `notebooks/15`) | **complete** — 79/79 stations classified |
> | **C2** | `docs/34` | **complete** — the observed contrast, model-free |
> | **C2b** | `docs/33` §6–§8 | **complete** — a stage that did not exist when this plan was written; H-BFI held, **H-PEAK refuted**, the H2E-S refit failed 2 of 3 conditions |
> | **C3** | `docs/37` | **built and run, and OPEN** — four amendments deep (A1, A1.9, A2, A3); A3 (2026-08-12) states in its own title *"C3 stays OPEN. C4.3 stays BLOCKED."* — **the *"C3 stays OPEN"* half still stands; the *"C4.3 stays BLOCKED"* half is spent, see the C4 row** |
> | **C4** | `docs/45` (C4.2 prereg) · `docs/47` (the entry verdict — now the *historical* entry condition) · **`docs/55` (the C4.3 verdict, the owner)** | C4.1/C4.2 landed; ~~**C4.3 is BLOCKED — see the marker at C4.3 below**~~ → **C4.3 RAN (2026-08-12) — `docs/55`: RAILED / EXPLORATORY, the fit is NOT adopted.** The in-box optimum sits on the **box floor α = 2.0** (β 0.60), median `F_report` **−0.118** on estimator (a) and **+0.139** on estimator (b) — *same sign*, so the verdict is **not** INDETERMINATE; the *unconstrained* optimum **α ≈ 0.48** is below the box floor, which is the registered signature of **mild upstream over-production — a diagnosis, not a value to adopt**. Design-matrix condition number `inf`: only **Π** is identifiable, α is never reported alone |
> | **C5** | **`docs/56`** | ~~not started~~ → **COMPLETE (2026-08-12) — the modelled ENSO contrast REPRODUCES the observed one:** La Niña > El Niño at **18/18** usable stations, median rate ratio **3.05×** (range 1.62–4.85, geo-mean 3.06), at the *lower edge* of the observed ~3–5 band and matching observed estimator (b); the direction holds in **all six** β ∈ {0.45, 0.56, 0.65} × {primary, secondary} sensitivity cells. Rates only, absolute flux only (`docs/23` §13.2 embargo). **Caveat: C5.3's pre-registered factor-swap experiments were NOT part of it** — `docs/56` runs §1–§5 with no swap section, and `docs/PROGRESS.md` still lists C5.3 unchecked |
>
> The subtask bodies below are **preserved as written**. Where an outcome contradicts them, the
> owning document wins.

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
| Adopted hydrology | **H2E** = v2 forcing + revised objective + FAO-56 ET (θ_crit 0.6). **"v2" here means the zero-suppression repair + deterministic IDW, and it is STILL GAUGE-ONLY — it is not "gauges + CHIRPS"** (that would be v3, and v3 does not exist). Canonical definition: `docs/00_INDEX.md` → **"Forcing versions — v1 / v2 / v3, stated once"**. *Note added 2026-08-12 because the two senses of "v2" have already misled a reader; `notebooks/11`'s prose uses the older CHIRPS-inclusive sense while its code uses this one.* | docs/29 read-out; **`docs/00_INDEX.md` "Forcing versions"** |
| Best H2E run | seed 20260901, **F 0.25931**, kc_mult 1.662, recession median 1.082 | `_calib_cache/dds_H2E_20260901.npz` |
| Second H2E seed | 20260902, F 0.24671, kc_mult 1.836, recession 1.110 | same dir |
| H1 vs H2 verdict | **not separated** (gap 0.009 < seed spread 0.051) | docs/29 §Results |
| Dry-phase ceiling | El Niño r pinned 0.556–0.572 across 12 configs (docs/22 §4.7); field LOOCV skill 0.429 (docs/18 §12, docs/26 §7 — the all-period gauge-only median; docs/22 §4.7's per-window El Niño field skill is 0.40, a different statistic) | docs/22 §4.7; docs/18 §12 |
| CHIRPS merge | LOOCV **passed** (r 0.447), volume **failed** (+7.5 %) → rejected; ~~fix identified~~ → **NO FIX IS IDENTIFIED. The registered fix was executed and is a NO-OP; the diagnosed cause was wrong. See the correction note below this table (2026-08-12).** | docs/18 §15 **and §15.5**; docs/33 §1 |
| SSC data | `sediment_daily.csv`: 269,337 rows, 1979–2018, cols incl. `ssc_mean_mg_l`, `ssc_surface_mg_l`, `approval`, `flag_corrupt/zero/flatline` | data/processed |
| SSC stations | 79 total, but **28 mapped / 33 with coords / 24 calibration-safe**; 46 unmapped (no coordinates) pending the docs/19 §5.2-item-2 coordinate+area fetch (see C1.0). ~~`calibration_safe` is geometry-only (no SSC-quality gate)~~ → **C1 BUILT THE GATE (2026-08-12 note): `docs/32` §R6 classifies 79/79 with a deciding measurement each — of the 28 mapped, **6 `usable`, 12 `usable-with-caveat`, 10 excluded ⇒ 18 usable**. Station *usability* is owned by `docs/32`, not by this row.** ⚠ **The 18 and the C4 fit set are different objects and must not be conflated** (`docs/45` §3.4 registers three): **CAL 8** is what C4 *fits*; **EVAL 5** is scored, never fitted; **all 18** run every structure guard — the all-18 clause stands and is the deciding form for G11 | `sediment_inventory.csv` (measured 2026-08-10), docs/19 §3.7; **`docs/32` §R6, `docs/45` §3.4** |
| MUSLE K | per-minibacia in `minibacia_soil_params.csv:K` (t·ha·h/(ha·MJ·mm)) | nb09 |
| Areas | per-gauge catchment areas untrustworthy in BOTH team networks (36 % of 85 shared gauges disagree >2×) | docs/23 §13.2 |
| Rating curves | median R² **0.54** across 33 pairs; per-pair list in `data/processed/rating_curves.csv` (cols code/name/n_pairs/a/b/R2). docs/13 is the pairing-candidates doc — it carries **no R² values** | `rating_curves.csv` (nb06); docs/13 |
| Flux conversion | Q (m³/s) × C (mg/L) × **0.0864** = t/day | arithmetic |
| MUSLE defaults | α = 11.8, β = 0.56 (Williams 1975) — starting values, to be calibrated | literature |
| Sediment skill bar | Fagundes et al. 2026 report sediment KGE **−0.26 to 0.44** | the source paper |
| Literature flux anchor | Magdalena suspended load at Calamar ~140–180 Mt/yr (Restrepo et al.). docs/06:9 already records **~145–169 Mt/yr** with citations; Restrepo & Kjerfve (2000) give **144 Mt/yr** (1975–1995). ~~**C2.4** (not C2.5) reconciles against docs/06 and fetches the exact figure before quoting~~ → **DONE 2026-08-12: C2.4 ran. Two primary figures, both cited: 144 Mt/yr (Restrepo & Kjerfve 2000, J. Hydrology 235:137–149) and 184 Mt/yr (Restrepo & Escobar 2018, Geomorphology 302:76–91). docs/34 §5.1: *"docs/06:9's '~145–169 Mt/yr' is therefore confirmed as a plausible range but not as a single figure … docs/31 open item 5 is closed by the two citations above."*** | docs/06:9; **docs/34 §5.1 (the owner)** |

> **⚠ CORRECTION, 2026-08-12 — the CHIRPS row above, and everything downstream of it (B1).**
> This table is headed *"do not re-derive"*, which is the strongest possible instruction to
> inherit a claim without checking it. The clause *"fix identified"* was true when written and
> is **false now**, and it must not be inherited.
>
> The intervention was registered as **H-CHIRPS** (`docs/33` §1), executed, and read out in
> `docs/18` **§15.5** — which is the owning read-out. Note that `docs/33` §1's own pointer says
> *"see §7"*, but §7 of `docs/33` is the **H-PEAK** read-out; `docs/33` is frozen, so its pointer
> stays as written. **Cite `docs/18` §15.5.**
>
> `docs/33` §1, verbatim: *"H-CHIRPS is **REFUTED by its own volume gate** (2,188.5 mm/yr against
> the required [2,016.0, 2,056.8]). The registered intervention turned out to be a **no-op**: the
> quantile maps already included the inferred-dry days, so the diagnosed cause in docs/18 §15.3
> was wrong."*
>
> `docs/18` §15.5, verbatim: *"The first thing the refit found is that this was already the code's
> behaviour"* — the inferred-dry days were **240,115 of 926,268 paired station-days, 25.9 %** of
> the fit input — and the re-run is **bit-identical** to the rejected run (*"max |diff| 0.000e+00"*
> across all 291 rows). Its closing statement: *"**v2 remains the forcing**, the r-ceiling of doc
> 22 s4.7 is unmoved, and **no route to a passing volume gate exists inside the merge code**."*
>
> **What survives is an *untested* hypothesis, not a fix.** `docs/18` §15.5: *"The half of s15.3
> that survives is the other half — the days the repair never inferred, at the **139 stations that
> still report rain-selectively** after it (s9.3). Those cannot be put into a pool by any change to
> `merge_chirps_gauges.py`, because they are not in the record at all."* It is upstream of the
> merge and has not been tested. **No reader may conclude a fix is waiting.**
>
> **And there is no v3.** No forcing file was written; no v3 calibration was ever launched. See
> `docs/00_INDEX.md` → **"Forcing versions — v1 / v2 / v3, stated once"**: v1 and v2 are **both
> gauge-only** (v2 = zero-suppression repair + deterministic IDW, the **adopted** forcing); **v3 is
> the CHIRPS-merged forcing and it does not exist**, and building one would need a new
> pre-registration (`docs/30` §1, `docs/33` §1 and §5.1).

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

### C1.0 Network-size decision (docs/19 §5.2 item 2) — 📌 **DECISION TAKEN; C1 is NOT gated on it**
`sediment_inventory.csv` has **28 of 79 stations mapped** (33 with coordinates, 24 calibration-safe);
46 have no coordinates (docs/19 §3.7, CONFIRMED). docs/19 §5.2 requires this be decided *explicitly,
not inherited*. **Decision (2026-08-10): Phase C proceeds now on the 28-station mapped subset (24
calibration-safe).** This is exactly docs/19 §5.2's stated fallback — *"until [the coordinate fetch]
is done the sediment network is 24 stations, not 79."* C1.1 therefore sizes coverage against the
mapped subset, and the 46 unmapped are carried as `ssc_class=excluded, reason="no coordinates"` in C1.6.
- The coordinate+area fetch for the 46 is **background task B5** (async, non-gating — see Background
  track). If B5 lands it *re-opens* coverage and C1.1/C1.6 restate the counts; if it does not, the
  exclusion stands. Nothing on the core path waits for it.

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
- **Out:** the registration block at the top of `docs/34_observed_enso_contrast.md`.

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
(C2.1), then compute. Deliverables: ~~docs/33~~ → **docs/34**, observed_enso_contrast.csv,
figures."* — **target corrected 2026-08-12**: 33 is the C2b pre-registration; the C2 contrast
landed as `docs/34_observed_enso_contrast.md`. **Stage C2 is complete** — this prompt is history.

---

## Stage C3 — MUSLE hillslope erosion on our engine (2–3 sessions)

Goal: `Sed = α·(Qsur·qpeak·A)^β · K · C · P · LS2D` per URH per day, driven by frozen
H2E runoff, verified the way the hydrology engine was.

### C3.1 LS2D factor (the one missing static input)
- Desmet & Govers (1996) two-dimensional LS from the conditioned DEM (the nb07 chain
  already produces filled DEM + D8 + accumulation): per cell
  LS = (m+1)·(A/22.13)^m·(sin β/0.0896)^n, aggregated area-weighted per URH per minibacia.
- **Out:** `minibacia_ls2d.csv` (or per-URH npz); a map figure.
- **Gate:** distributional sanity — LS ∈ (0, ~72], ~~basin median in the literature range
  for mountainous basins (~2–10)~~; flat lowlands ≪ Andean flanks visually.

> **⚠ THE "~2–10" GATE WAS RETIRED, not passed. 2026-08-12.** `docs/37` §1 decision 4 (the owner):
> *"The 'published mountainous LS 2–10' comparison that would have motivated a rescale is
> **uncited** and is retired rather than acted on."* The measured basin median is **12.8**
> (`journal_c31-ls2d.md`) — reported, not adjusted; `ls2d_resolution='native_90m'`, no rescaling.
> **A retired gate is neither a pass nor a fail.** The LS *level* is a live, contested question and
> its owners are `docs/46` (frozen, READ OUT), `docs/51` (the corrected bracket
> `f_LS ∈ [0.25146, 0.43194]` erosion-weighted ⇒ **2.3151× – 3.9768×**) and `docs/37` **A3**, which
> decides the *formulation* on source grounds — **ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`**
> — while stating that **no engine default moves, C3 stays OPEN and C4.3 stays BLOCKED**. It is the
> unresolved denominator of the α box, and ~~therefore the reason C4.3 is blocked (`docs/47`)~~.
> **Do not re-derive an LS verdict from this gate.**
>
> **⚠ UPDATED 2026-08-19 — two clauses of the paragraph above have been overtaken.** (i) The engine
> default **did** move: C3.1 **ACT 1** materialised the adopted field and **ACT 2** (commit
> `c3fdb55`, 2026-08-12) switched `src/mgb_sediment.py` `load_geometry()` to **`V4_dg`**, with
> `f_LS` = **0.25146** erosion-weighted / **0.2446790094097074** area-weighted. (ii) C4.3 is
> therefore **no longer held**: it ran on the adopted field and its verdict is `docs/55`
> (RAILED / EXPLORATORY, not adopted). **What has NOT changed: C3 is still OPEN**, and the LS
> *level* is still graded **UNVALIDATED** (`docs/42` G4.2) — which is exactly why `docs/55` reports
> **Π** and not α alone.

### C3.2 C and P factors
- Map the 8 hydrological land classes → C values (take Fagundes' table as primary; keep
  the mapping in a reviewable CSV, not hardcoded). P = 1.0 basin-wide (no conservation-
  practice data) — stated, not hidden.
- **Out:** `urh_cp_factors.csv` with a source column per value.

### C3.3 The qpeak proxy — pre-registered choice
A daily model has no sub-daily peak. ~~Options, to be registered before implementation:~~
→ **REGISTERED 2026-08-11 as `docs/35_qpeak_preregistration.md`** (the `q_peak` proxy, its signed
bias, and the C4 anti-compensation rule). **Do not re-register it.** `docs/35` §9 is its amendment
slot; parts of it have since been amended (§9.2's convention, §9.4's re-based loads). The options
below are preserved as the choice set that was registered against. Note added 2026-08-12.
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
- **Out:** ~~`docs/34_sediment_calibration.md` pre-registration section.~~ → **LANDED 2026-08-11 as
  `docs/45_c4_preregistration.md`, FROZEN ON WRITE.** (34 was taken by the C2 observed contrast;
  see the re-corrected numbering note at the top of this file.) `docs/45` registers the sediment
  KGE bar `F_report ∈ [−0.26, 0.44]`, the α/β boxes, the **CAL 8** fit set, the windows, the seeds
  and all eight ADOPT conditions; §8 is its amendment slot. Read with `docs/42` (the C4 guard set
  G1–G9, frozen) — `docs/42` §3 measures α, the C level, the LS level, the K unit system, the
  volume convention, P and FG as **seven ways of writing one identifiable product Π** (condition
  number `inf`), so C4 reports Π, the equifinal family and per-factor evidence grades and **never
  "validated"**.

### C4.3 Search, report, verdict

> ## ✅ C4.3 HAS RUN — this marker is the HISTORICAL entry condition. Marker added 2026-08-12; discharged and superseded 2026-08-19 by `docs/55`.
>
> ~~## ⛔ C4.3 IS BLOCKED — do not start this subtask. Marker added 2026-08-12.~~
>
> **Outcome first, so that nothing below this line is mistaken for a live prohibition.** C4.3 ran on
> **2026-08-12** against the *adopted* LS field (`ls_formulation = buarque_2015_dg`, `V4_dg` — the
> engine default was moved there by the C3.1 ACT 2 commit `c3fdb55`), and the run is read out in
> **`docs/55_c43_verdict.md`**, which is its owner:
>
> **VERDICT — `RAILED / EXPLORATORY`. The fit is NOT adopted.** The in-box optimum of `F_report`
> (median KGE_ln over the CAL 8) sits on the **box floor**: α = **2.0**, β 0.60, `F_report` =
> **−0.118**. Re-run on estimator (b) (rating-curve flux) it is **+0.139** — the **same sign**, so
> the outcome is **not** INDETERMINATE. The *unconstrained* optimum is **α ≈ 0.48**, *below* the box
> floor: the registered signature of **mild upstream over-production — a diagnosis, and not a value
> to adopt.** The design matrix's condition number is **`inf`**, so only the product **Π** is
> identifiable and α is never reported alone (`docs/42` G6). `docs/55` §6 lists what is still owed
> (the `k_hi` deposition re-solve). **Read `docs/55`; do not restate its verdict from here.**
>
> ⚠ **`docs/47` has NOT been amended to record an unblock** (checked 2026-08-19: its VERDICT box
> still reads `C4.3-BLOCKED-UNTIL-LS-LANDS`). Its block was conditioned on a single named event —
> *"C3.1 lands"* (`docs/47` §6.1 B1) — and that event landed (`docs/37` **A3** = ADOPT-SOURCE, then
> ACT 1 materialising the field and ACT 2 moving the engine default, `c3fdb55`). Reconciling
> `docs/47`'s own text is owed to that document's owner; **this file records only the measured fact
> that the run happened and where its read-out lives.** Nothing here authorises re-running or
> re-interpreting the fit.
>
> **The 2026-08-12 entry reasoning is preserved verbatim below**, unedited — it is the record of why
> the stage was held and it remains the clearest statement of what the run had to survive. Its
> *status* claims are historical; its *mechanism* is not.
>
> **`docs/47_c4_entry_verdict.md` is the authority on whether C4.3 may start**, and it decides:
> *"**`C4.3-BLOCKED-UNTIL-LS-LANDS`. C4.3 may not start.**"* (`docs/47`, THE VERDICT box.)
>
> This document is the one a session *opens to start a stage*, and it carried no marker here —
> which is exactly how a blocked stage gets started. The block is **not** a caution: `docs/47`
> measures the failure in advance. Its reason, quoted: α *"is only a handle on Π … and its
> numerical value is proportional to `1/f_LS`, where `f_LS` is graded **UNVALIDATED** … **A box
> registered in α is therefore a box whose position is unknown to within a factor of four**"*;
> measured on the registered configuration the objective is *"**monotone decreasing across the
> entire registered box**"*, the search *"**rails at the box floor α = 2.0**"*, and in-box
> `F_report` reaches only **−0.305 … −0.350** against the bar's lower edge −0.26 — a
> `FAIL — RAILED / HARD STOP` **and** a `FAIL — NUMERIC`, both computable in advance.
>
> **The block is still in force as of 2026-08-12**, upheld by `docs/46` §6.4, `docs/51` §4,
> `docs/53`, and by `docs/37` **A3.4** — the C3.1 enactment amendment itself: *"Is C4.3 thereby
> UNBLOCKED? **NO**"*. Do not infer from `docs/43`'s title (*"C4 PROCEEDS CONDITIONALLY"*) that
> the search may run: `docs/43`'s clause is narrowed for **C4.3 specifically** by `docs/47`.
>
> **`docs/47` grants exactly one bounded exception** (§6.3): **LS-invariant preparation only** —
> the C4.3 machinery and artifact contract. *"**No objective evaluation against the α box, and no
> consumption of the registered 5,482-evaluation budget, is authorised by this document.**"*
>
> **Do not restate the unblocking condition from here.** `docs/47` owns it, several of its items
> have moved since it was written, and it is being amended concurrently. **Read `docs/47` §6.1–§6.3
> before doing anything under this heading.**
>
> The subtask text below is preserved as written and describes what C4.3 ~~will do **when it is
> unblocked**~~ → **did do, on 2026-08-12** (`docs/55`). It was never a permission, and it is not one
> now.
- Same machinery pattern as `calib_v2` (checkpoints, logs watch_calib can parse,
  detached queue if runs are long — they should not be).
- Report per-period at every usable station: calibration set, validation set, and the
  below-Momposina stations separately (expected to fail; that failure is the measured
  cost of the missing sink, and it goes in the report as such).
- **Gate:** parameters checked against bounds; seed spread reported; verdict against the
  registered rules, both directions reportable.

**Paste-prompt:** ~~*"Execute stage C4 of docs/31. C4.2's pre-registration must be
committed before the first search runs. Calibrate upstream of the Momposina only."*~~
→ ~~**DO NOT PASTE THIS AS WRITTEN (2026-08-12).** C4.2's pre-registration is already committed
(`docs/45`, frozen 2026-08-11) and **C4.3 may not start** (`docs/47`). A session working here must
open **`docs/47` first**, and may do only the LS-invariant preparation its §6.3 permits.~~ The
"calibrate upstream of the Momposina only" clause is unaffected and still binds whenever C4.3 runs.
→ **DO NOT PASTE THIS AT ALL (2026-08-19): C4.3 has already run and its verdict is written**
(`docs/55` — RAILED / EXPLORATORY, not adopted). Re-running the search would need a new
pre-registration, not this prompt. Both the prompt and the 2026-08-12 prohibition above are kept as
the record of the entry condition.

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
- ~~`docs/35_enso_contrast_results.md`~~ → **the number 35 is taken** (`35_qpeak_preregistration.md`).
  ~~**Claim the next free number — 54 as of 2026-08-12**~~ — and check `docs/00_INDEX.md` §3 and
  `docs/agents/` for an in-flight claim before claiming it, as that file's numbering-discipline note
  requires. Plus the figure set; updates to docs/21 and the presentation material (docs/24 chain).
  Every number carries its window and its prediction/description label.
- **LANDED 2026-08-12 as `docs/56_c5_enso_application.md`** — not 54, which
  `54_c3_1_closure_and_c4_entry_status.md` took first. `docs/56` is the owner of the C5 read-out.
  **What it carries:** C5.1 (the contrast run) and C5.2 (prediction vs target, 18/18, median rate
  ratio 3.05×, β and window sensitivity) plus the mandatory "what this is and is NOT" section.
  **What it does NOT carry:** the C5.3 spatial-attribution map and the pre-registered factor-swap
  experiments — those were **not run** (`docs/56` has no such section; `docs/PROGRESS.md` still lists
  C5.3 unchecked). The figure set and the docs/21 / docs/24 updates are tracked outside this file.

**Paste-prompt:** *"Execute stage C5 of docs/31. Register the factor-swap list (C5.3)
before running any swap. The deliverable is ~~docs/35~~ → ~~**the next free doc number (54)**~~ →
**`docs/56`** plus the figure set."* — **target corrected 2026-08-12, re-corrected 2026-08-19: the
deliverable landed as `docs/56_c5_enso_application.md`, not 54.**
~~Note C5 depends on C4, and **C4.3 is BLOCKED** (`docs/47`).~~
→ **C5 has since been executed; its read-out is `docs/56`.** The paste-prompt above is preserved as
the original instruction, not as pending work. C5 did depend on C4, and C4.3 ran first (`docs/55`);
`docs/56` §2 records *why* the contrast survives C4.3's railing — the within-station wet/dry ratio
is invariant to α and to the LS level, both being static multipliers that cancel. **The one clause
still unexecuted is C5.3's factor-swap list**, which would need registering before any swap is run.

---

## Background track — bounded, never gating

### ~~B1 CHIRPS refit (≤ 2 sessions, then stop either way)~~ → **DONE, and NEGATIVE. CLOSED 2026-08-10. This is not pending work.**

> **⚠ BACK-ANNOTATION, 2026-08-12.** B1 ran. It was registered as **H-CHIRPS** (`docs/33` §1) and
> read out in `docs/18` **§15.5**. Both gates were re-measured **unchanged**, exactly as this item
> required:
>
> | gate | result |
> |---|---|
> | LOOCV, 2008–2018 station-days | merged median daily r **0.447** > 0.429 — **PASSES** |
> | VOLUME, 2009–2017, area-weighted | **2,188.5 mm/yr** vs the band [2,016.0, 2,056.8] — **FAILS (+7.47 %)** |
> | decision | **DO NOT ADOPT** — both were required, one failed |
>
> **The registered intervention was a no-op**, and this item's own diagnosis is the half that was
> refuted. `docs/18` §15.5: *"The first thing the refit found is that this was already the code's
> behaviour"* — the `Inferido_seco` days were **240,115 of 926,268 paired station-days, 25.9 %** of
> the fit input — and the re-run reproduces the rejected run **bit-identically** (max |diff|
> 0.000e+00 across all 291 scored rows). `docs/33` §1: *"the diagnosed cause in docs/18 §15.3 was
> **wrong**."*
>
> **Credit where it is due, because it is load-bearing:** the paragraph below was the *most careful*
> text in the corpus on this. It warned **in advance** that the `Inferido_seco` change alone
> *"would leave the volume gate failing"* — which is precisely what was then measured. Its
> **mechanism** is not what went stale; only its **status** did.
>
> **What this item's own closing clause requires:** *"Any gate fails → the negative result closes
> the CHIRPS question permanently; write it and stop."* It failed; it is written (`docs/18` §15.5);
> it is closed. **No v3 forcing exists and none was built. No new calibration cell was authorised
> or run. There is no H3.**
>
> **What survives is a different, unscoped, UNTESTED item** — not this one. `docs/18` §15.5: *"The
> only remaining route is upstream: repair the **139 residual rain-selective stations** so the gauge
> record itself carries its true dry-day frequency."* That is upstream of the merge and **cannot be
> tested inside it**: *"no route to a passing volume gate exists inside the merge code."* It has not
> been attempted. **Do not read it as a fix in hand.**
>
> The item text below is preserved as written, per this project's rule that nothing is deleted.

### ~~B1 CHIRPS refit (≤ 2 sessions, then stop either way)~~ *(original text, preserved)*
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

### B5 SSC coordinate + area fetch for the 46 unmapped stations (async, unblocks SSC coverage only)
- The C1.0 decision runs Phase C on the 28 mapped stations *now*; this task tries to raise that count.
- Extend `src/fetch_station_coords.py` (single commit `b4a1230`; the docs/19 §5.2-item-2 extension was
  never built) to pull the IDEAM catalogue **coordinate + catalogue drainage area** for the 46 unmapped
  codes, then re-snap by **drainage-area matching** (docs/19 §5.2).
- Success = mapped count rises; record the new number and re-run C1.1/C1.6 for the added stations.
  Distinct from B3 (which fetches areas as a *discharge-network* arbiter for the yield embargo).

---

## Dependencies and suggested order

```
C0 ──────────────► C3 ──► C4 ──► C5
      C1 ──► C2 ─────────► C4 (calibration targets come from C1/C2)
B1, B2, B3, B4, B5: independent; B1 success re-opens hydrology ONLY via a new pre-registration;
C1.0 decision (run on 28-station subset) means C1 does NOT wait for B5
```

> **⚠ THE GRAPH HAS NO GATE ON IT, and there is one. Added 2026-08-12.** As drawn, `C3 → C4 → C5`
> reads as an open path. It was not, when this note was written:
>
> ```
> RETIRED / superseded 2026-08-19 — shown, not quoted as current
> (strike-through does not render inside a code fence, so this is the dated form):
>
> C0 ──► C3 (OPEN, docs/37) ──► C4.1 ✔ ──► C4.2 ✔ ──► ⛔ C4.3 BLOCKED (docs/47) ──► C5
>                                                      └─ LS-invariant prep only (docs/47 §6.3)
> ```
>
> **⚠ THE GATE HAS SINCE BEEN PASSED — redrawn 2026-08-19.** The block's named condition (*"C3.1
> lands"*) landed, C4.3 ran, and C5 ran after it:
>
> ```
> C0 ──► C3 (OPEN, docs/37) ──► C4.1 ✔ ──► C4.2 ✔ ──► C4.3 ✔ RAILED / EXPLORATORY (docs/55)
>                                                          └─► C5 ✔ CONTRAST REPRODUCED, 18/18 (docs/56)
> ```
>
> C3 is **still OPEN** (`docs/37` A3) — the path ran with it open, which is a stated limitation of
> the C4/C5 results, not a closure of C3.
>
> ~~**`docs/47` is the authority on whether C4.3 may start**, and it says it may not:
> *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. C4.3 may not start."* C5 depends on C4.3 and therefore
> inherits the block.~~ → **Historical.** `docs/47` is the authority on the *entry condition* and
> its text is unamended; `docs/55` owns the C4.3 outcome and `docs/56` the C5 outcome.
> **B1 is CLOSED-NEGATIVE** (see the back-annotation above), so the
> "B1 success re-opens hydrology" branch is spent — the rule it invoked still stands for any
> *future* forcing change, and there is no v3.

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
| α/β equifinality | C4 parameters uninterpretable | ~~pre-registered bounds + seeds + bound checks, as in Phase B~~ → **NOT SUFFICIENT — measured, 2026-08-12. See the note below the table.** |
| dry-phase hydrology ceiling | El Niño flux accuracy | propagated quantitatively in C5.2; named in every ENSO claim |
| forcing changes mid-phase | silent invalidation of C0's freeze | B1 can only re-open hydrology through a new pre-registration — **B1 is now CLOSED-NEGATIVE and there is no v3, so this branch is spent; the rule still binds any future forcing change** |

> **⚠ THE `α/β` EQUIFINALITY ROW UNDERSTATES ITS RISK — measured since. 2026-08-12.**
> The mitigation as written (bounds, seeds, bound checks) is the *Phase B* mitigation, and
> `docs/42` — the frozen C4 guard set — measured that it does not carry here. `docs/42` §3: **α, the
> C level, the LS level, the K unit system, the volume convention, P and FG are seven ways of
> writing one identifiable product Π**, with the condition number measured as **`inf`**. The
> consequence `docs/42` draws: C4 reports **Π**, the **equifinal family** and **per-factor evidence
> grades** — and **never "validated"**. Bound checks cannot see this: `docs/47` §2.5 C1 measures
> that a fit which silently omits channel deposition lands α *inside* the "expected" band while
> `check_musle_parameters` returns `ok`. **`docs/42` G1–G9 is the mitigation now** — 17 FAIL
> conditions, with G5 replacing the α band by a precondition (a named non-trivial transport sink,
> or the words *"this model asserts SDR = 1.0 between hillslope and station"* stated as a claim).
> The guard set is where the numbers live; **do not quote the α band from this table as a guard.**

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
| 1 | ~~docs/24 (slide 8: "3 of 10") vs docs/26 §5 ("2") disagree on attempt-3's railed-parameter count~~ → **RESOLVED** (already recorded below this table, 2026-08-10): one 18-dimension vector, two denominators. `docs/26` Addendum A.2 now states both — *"Railed: **2 of 10 global** … **3 of 18 dimensions** (adding `wm_mult@R2` at 97.1 %) — both denominators stated"*. Kept in the register only so the row and its resolution are not read apart | docs/21; **resolved in `docs/agents/review_2026-08-10_docs31.md` §3 + `docs/26` A.2** |
| 2 | kc_mult 1.662/1.836 is off its rail but still above the FAO-56 plausibility bar of ≤1.2 — the ET form was a real cause, not the whole story | docs/29 §Results caveats |
| 3 | k_int_frac sits on its 0.02 floor in 7 of 8 v2-forcing seeds — a new near-rail, unprobed until B2 | docs/29 §Results caveats |
| 4 | Older docs (12, 19, 21, 24, 25, 28) still carry "Phase C blocked on mainstem SSC" — superseded by docs/30 §1, not yet edited in place | docs/30 |
| 5 | ~~The Restrepo outlet-flux anchor (~140–180 Mt/yr) is unverified until C2.4 fetches the exact figure and citation~~ → **CLOSED 2026-08-12 by its owner.** `docs/34` §5.1, verbatim: *"**docs/31 open item 5 is closed by the two citations above**"* — **144 Mt/yr** (Restrepo & Kjerfve 2000, *J. Hydrology* **235**(1–2):137–149, doi 10.1016/S0022-1694(00)00269-9, Calamar, 1975–1995) and **184 Mt/yr** (Restrepo & Escobar 2018, *Geomorphology* **302**:76–91, 1980–2010). docs/06:9's "~145–169 Mt/yr" is *"confirmed as a plausible range but not as a single figure"* | §0 table; **`docs/34` §5.1 (the owner)** |
| 6 | The ENSO window definition was never adjudicated by the advisor; C2.1 resolves it by primary+sensitivity bracketing, not by authority | docs/21, C2.1 |
| 7 | H2E is adopted from n=2 seeds, exactly as its pre-registration allowed; more seeds require a NEW pre-registration | docs/29 |

**Register audited against the owning docs, 2026-08-12.** Items **1** and **5** are closed above.
Items **2** (`kc_mult` 1.662/1.836, off its rail but still above the FAO-56 plausibility bar of
≤ 1.2), **3** (`k_int_frac` on its 0.02 floor, unprobed — B2 has not run), **4** (the "Phase C
blocked on mainstem SSC" phrasing surviving in docs 12/19/21/24/25/28), **6** and **7** were each
re-checked and are **genuinely still open** — confirming them is still not a discovery. Item 4's
exact form is now measurable, and should be quoted with it: `docs/32` §R6 finds **one** Magdalena-
trunk SSC station in the whole network, `21237020` ARRANCAPLUMAS.

**Registers this one does not hold.** Three more live registers exist and are not duplicated here:
`docs/21` §4 (twelve hydrology open items), `docs/34` §7 (six issues C2 raised), `docs/36` §7 (ten).
`docs/47` §7 holds the C4-entry open items (O1–O12), several of which have closed since it was
written — **read it, do not restate it from here.**

**2026-08-10 review applied.** Findings F1–F9 of `docs/agents/review_2026-08-10_docs31.md` were
corrected in place: F1 (SSC network 79→28, added C1.0 coordinate fetch), F2 (ENSO pairing decision
recorded in docs/30 §1), F4 (C1.2 gate → calendar-regular), F3 (B1 refit re-spec), F5 (musle.py
acquisition line), F6 (slope not in topology.npz), F7 (four pointers), F8 (docs/30 ratio wording),
F9 (744 mg/L marker). Register #1 (railed-count 3-vs-2 discrepancy) is **RESOLVED with evidence** in
that review §3 (one 18-dim vector, two denominators: parameters_H2.csv marks 3 railed dims incl.
regional `wm_mult@R2`; docs/26 §5's "2" counts globals only). All four load-bearing findings
(F1, F4, F5, F6) were re-verified against disk before applying.

# 18 — Hydrology journal: water balance, calibration, and the dry-phase diagnosis

The Phase B record. What was built (`src/mgb_hydrology.py`, notebooks 13–14), what the calibration
actually achieved, and — the reason this document exists — **why the El Niño 2015–16 half of the
ENSO contrast fails, measured rather than argued**.

Companion to [doc 16](16_forcing_pipeline_audit.md) (forcing) and
[doc 17](17_discharge_qc_audit.md) (discharge). Same rule as those two: findings that did not
survive measurement are in [§6 Checked and refuted](#6--checked-and-refuted), not deleted.

Read §4 first if you are picking this up cold: **all three standing hypotheses for the dry-phase
failure are wrong, and one of them is backwards.** The binding constraint is the daily correlation
`r ≈ 0.57`, which no parameter in the model can move.

§9–§10 are the forcing follow-up: the wet bias is real and independently replicated, the
zero-suppression repair is now finished (basin rainfall −6.4 %), and the surviving energy-floor
failures turn out to be a *separate, local* problem rather than the basin-wide surplus.

---

## 1 — Current state

| Component | State |
|---|---|
| Engine `src/mgb_hydrology.py` | **Verified.** Mass closes to 1.4×10⁻¹⁷ relative; numpy and numba routers agree exactly; 16 s for a 3,653-day × 8,672-minibacia run |
| Calibration (nb14) | **Complete.** Klemeš differential split, fitted on neutral 2012–14 only; both ENSO phases are out-of-sample |
| Validation skill | median KGE **+0.450**, NSE +0.256, PBIAS +6.8 % (unfitted prior: +0.253 / −0.279 / +45.2 %) |
| Overfitting | excess degradation vs the unfitted reference **+0.011** median KGE — negligible |
| La Niña 2011 | KGE **+0.399**, α 0.981, β 0.980 — works |
| El Niño 2015–16 | KGE **+0.193**, α 0.793, β 1.084 — ❗ the blocker |
| Dry-phase diagnosis | **Complete** (§4–§6). Cause is *not* recession, *not* gauge error, *not* seasonal forcing inflation |
| Recession realism | ❗ **Newly found defect.** Simulated low-flow recession 48.6 d against 14 d observed, in *every* period |
| Parameter bounds | ❗ `kc_mult` railed at its 2.00 ceiling, `k_int` at 117.4/120, `lai_mult` 4.40/5.0 |
| Store ordering | ❗ `k_int` (117.4 d) **slower than** `k_bas` (68.6 d) — physically inverted |
| Phase C (sediment) | Still blocked — on mainstem SSC data and on the doc 19 `calibration_safe` gate |

Nothing in `data/processed/` was modified by the diagnostic work in §4–§6: every experiment
rebuilt parameters in memory from `sim_calibrated/minibacia_params.npz` and discarded the result.

---

## 2 — What was built

### 2.1 `src/mgb_hydrology.py` — the water-balance engine

A daily MGB-SA water balance over 8,672 minibacias × 24 URH, with Muskingum-Cunge (X=0) routing on
the D8 network from notebook 07. Structure, per URH cell per day:

1. **canopy** — interception store `Simax = alpha_int × LAI`, evaporated at PET before anything else;
2. **saturation excess** — variable contributing area `Asat = 1 − (1 − W/Wm)^b`, plus any overflow
   above `Wm`;
3. **evapotranspiration** — `min(kc · PET_soil · W/Wm, W)`, so ET is supply-limited as the soil dries;
4. **percolation** — `linear` mode: `drain = adr · W`, split `fint` to interflow and the rest to
   groundwater;
5. **three linear reservoirs** at the minibacia (`k_sup`, `k_int`, `k_bas`), exact release
   coefficient `1 − e^{−Δt/K}`;
6. **routing** — within-day topological sweep, 292 levels, vectorised level by level.

The negative-`W` guard returns its own magnitude rather than swallowing it, so any real clipping
appears as a non-zero term in the mass balance instead of hiding inside it. It has never fired.

**The engine is the one part of Phase B that is not in doubt.** `src/test_mgb_hydrology.py` checks
the recession constant analytically, not just its shape; mass closes to 1.4×10⁻¹⁷ relative on the
calibrated parameter set, which is a fresh test of the guards rather than of the algebra.

### 2.2 Notebook 13 — baseline run

The unfitted prior: `adr` 0.06, `fint` 0.60, `b` 0.60, `k_sup/int/bas` 1.5/8/60 d, celerity
1.0 m/s, FAO-56 `kc` and per-class LAI. Fleet median KGE 0.253 on validation, β 1.452 —
**bias is one-signed at 53 of 61 gauges**, so the first thing calibration had to move was the water
partition, not the timing.

### 2.3 Notebook 14 — calibration

| | |
|---|---|
| split | fit on **2012, 2013, 2014 only** (1,096 d), warm-up 2011 |
| validation | 2009, 2010, **2011 (La Niña)**, **2015–16 (El Niño)**, 2017 (2,191 d) |
| why | Klemeš (1986) differential split-sample: the ENSO extremes the project studies are never seen by the objective, so the contrast is a *prediction* |
| objective | mean over gauges of `(1−w)·C2M(KGE(Q)) + w·C2M(KGE(log(Q+q0)))`, `w=0.5`, `q0 = 0.01·mean Q` |
| bounded transform | `C2M(k) = k/(2−k)` (Mathevet et al. 2006) — stops one hopeless gauge dominating |
| algorithm | DDS (Tolson & Shoemaker 2007), `r=0.2`, 2 seeds × 178/209 evaluations = **774 model runs**, 63 min |
| screening | Morris elementary effects, 6 trajectories, 8 levels; 10/10 parameters survived, none frozen |
| adopted | **Configuration B** — 18 free parameters: global set + 3 macro-regions on `k_sup`, `wm_mult`, `celerity` + IGAC-soil-family split on `adr` |

Effective sample size is the honest number here: 53,499 gauge-days of calibration data, but a
lag-1 daily autocorrelation of 0.80 reduces that to **5,916 effective observations** for 18
parameters.

### 2.4 Skill, as measured

Median over the 61 calibration-safe gauges:

| period | KGE | NSE | r | α | β | PBIAS % |
|---|---|---|---|---|---|---|
| unfitted prior, VAL | +0.253 | −0.279 | 0.584 | 1.186 | 1.452 | +45.2 |
| calibrated, CAL 2012–14 | +0.291 | +0.045 | 0.522 | 0.866 | 1.001 | +0.1 |
| calibrated, VAL all | **+0.450** | +0.256 | 0.646 | 0.866 | 1.068 | +6.8 |
| calibrated, La Niña 2011 | +0.399 | +0.225 | 0.653 | 0.981 | 0.980 | −2.0 |
| calibrated, El Niño 2015–16 | **+0.193** | −0.078 | 0.569 | 0.793 | 1.084 | +8.4 |
| calibrated, other 09/10/17 | +0.446 | +0.170 | 0.650 | 0.878 | 1.079 | +7.9 |

Validation scores *higher* than calibration (−0.159 change), which means the calibration years are
intrinsically the harder ones. The control for that is the unfitted prior, which changes −0.170
over the same two periods with no fitting at all; the overfitting statistic is the **excess** over
that reference, **+0.011**.

---

## 3 — The hard limit found before any fitting

The engine cannot evaporate more than `max(1, kc) · PET`. Closing the observed water balance at
CALAMAR needs 1,300 mm/yr of ET against an ERA5-Land PET of 1,251 mm/yr — a deficit of
**49 mm/yr**. Consequences, all measured in nb14 §1:

* **18 of 61** gauges have an observed runoff coefficient below their own energy floor;
* outlet PBIAS can never fall below **+5.6 %** with this forcing;
* the fitted `kc_mult` of 1.9994 is partly absorbing that inconsistency, not only representing
  forest transpiration.

§4.3 shows this floor is real but is **not** what breaks the dry phase.

---

## 4 — The dry-phase diagnosis → [doc 22](22_dry_phase_diagnosis.md)

Moved to its own document when this one passed 65 KB. **Read
[doc 22](22_dry_phase_diagnosis.md) before touching calibration.** The findings it
establishes, which the rest of this document depends on:

| finding | evidence |
|---|---|
| All three standing hypotheses for the dry-phase failure are **refuted**, and hypothesis (b) was **backwards** | 30 full model runs; harness reproduced the stored `q_sim_B_m3s` to 9.1×10⁻⁹ before anything was interpreted |
| ~⅓ of the headline gap is the **NSE yardstick**, not the model | a day-of-year climatology also scores NSE −0.062 in that window; obs CV 0.799 is the record's highest |
| The collapsing term is **α, not β** — variance is worth +0.275 KGE, bias only +0.101 | repair ladder, §4.2 of doc 22 |
| The model triples the **lowest** flows in the dry phase (+244 % in Q0–10) and undershoots the highest | bias by flow quantile |
| `k_bas` is **not** the cause — correcting it to the observed 13.9 d recession buys +0.021 | 10-run sweep, Morris `mu*` 0.044 |
| The calibration bought its fit with **compensating errors** — `kc_mult` railed at 2.00, `k_int` railed at 117.4 and *slower* than `k_bas`, celerity 4.5× below prior | parameter positions vs bounds |
| The **hard floor is r ≈ 0.57**, invariant across all 12 parameter configurations tested, and it is inherited from the rainfall field (LOO IDW r = 0.40) | doc 22 §4.7 |

---

## 5 — Verdict and what to do next

**The dry-phase failure is not one cause.** It decomposes as:

| share | cause | evidence | fixable by |
|---|---|---|---|
| ~⅓ of the headline | the NSE yardstick is not symmetric across windows | climatology also scores NSE −0.062 there ([doc 22 §4.1](22_dry_phase_diagnosis.md)) | reporting against a benchmark, not raw NSE |
| the recoverable part | α collapse from a compensating-error calibration | α 0.793; de-damping recovers 0.890 ([doc 22 §4.6](22_dry_phase_diagnosis.md)) | constraining the stores — worth ≈ +0.023 |
| the hard floor | r = 0.57, inherited from the rainfall field | invariant over 12 configurations; LOO IDW r = 0.40 ([doc 22 §4.7](22_dry_phase_diagnosis.md)) | **only a better rainfall field** |

Ranked by measured payoff:

1. **Stop tuning parameters for the dry phase.** [doc 22 §4.7](22_dry_phase_diagnosis.md) puts a hard ceiling on what they can buy. The
   remaining parameter gain is ≈ +0.02, already located.
2. **Adopt the de-damped store set** (`k_int` 15, `k_bas` 25) — it improves three of four periods
   simultaneously and costs nothing. It should be *re-fitted*, not hand-set, under item 3.
3. **Add a recession-signature term to the objective.** `k_bas` and `k_int` are invisible to
   daily KGE (Morris `mu*` 0.044 and 0.032, ranks 5 and 8 of 10) and are therefore set by the prior,
   not the data. Constrain them against the observed 13.9 d recession instead. Also **lower the
   `k_bas` bound below 15 d** — it currently excludes the observed value — and **impose
   `k_int < k_bas`** so the search cannot invert the stores again.
4. **Fix the rainfall field.** This is the only lever measured to be capable of moving r, and it
   was already the top item on nb14's carried-forward list. The CHIRPS–gauge merge plus the four
   SNHT segment exclusions from doc 17, then re-run notebook 11 → 12 → 13 → 14.
5. **Raise the `kc_mult` ceiling only together with a PET review.** It is railed at 2.00, meaning
   the search wanted more ET than allowed; but [doc 22 §4.5](22_dry_phase_diagnosis.md) shows more ET alone makes El Niño *worse*
   (0.193 → 0.177 at kc × 1.20). The energy deficit is an input problem, not a bound problem.
6. **Report the ENSO contrast against a climatology benchmark.** "NSE < 0" overstates the failure;
   "+0.024 vs +0.236 KGE over climatology" is the defensible statement.

---

## 6 — Checked and refuted

Recorded because each looked right before it was measured.

| claim | status | what the measurement said |
|---|---|---|
| "18 gauges have observed Q above what P − PET can supply → gauge/rating error" | ❌ **backwards** | All 18 fail in the opposite direction: observed rc is *below* its floor. Only 1 of 61 has obs Q > P ([doc 22 §4.3](22_dry_phase_diagnosis.md)) |
| "`k_bas` is global but should be regional; that is the dry-phase cause" | ❌ refuted | Regionalising to the observed recessions buys +0.021 KGE. The *level* is wrong by 3.5×, not the regionalisation, and even fixing the level buys ≤ +0.034 ([doc 22 §4.4](22_dry_phase_diagnosis.md)) |
| "IDW wet-day inflation bites hardest in the dry season" | ❌ refuted | +18.9 / +17.7 / +18.9 pts in La Niña / El Niño / neutral — period-invariant, marginally smaller in El Niño ([doc 22 §4.5](22_dry_phase_diagnosis.md)) |
| "The dry phase fails because of a constant water surplus divided by a smaller flow" | ❌ refuted | "other 09/10/17" carries the same +7.9 % excess and scores 0.446 against 0.193 ([doc 22 §4.5](22_dry_phase_diagnosis.md)) |
| "The model is worse than predicting the mean in El Niño" | ⚠️ **misleading** | True of NSE, but a day-of-year climatology also scores −0.062 there. The window's obs CV is the highest of the record ([doc 22 §4.1](22_dry_phase_diagnosis.md)) |
| "Most of the model's r is basin-wide seasonality" (nb14 §10.4 framing) | ⚠️ **overstated** | Removing the day-of-year climatology leaves r = 0.476 of 0.569 in El Niño. Seasonality is 13–17 % of r, not most of it |
| "The zero-suppression repair fixed the reporting-density bias" | ⚠️ **half true** | It fixed the 70 stations it touched (dense-band selectivity stayed at 1.00 while that band grew 92 → 151 stations), but 139 of 294 remain rain-selective at 1.73 / 1.30. Incomplete in **coverage**, not defective in method (§9.3) |
| "The 2.67× → 2.04× drop in the binned gradient measures the repair's effect" | ⚠️ **mostly composition** | Repaired stations crossed the density threshold and changed bin. The bias-controlled statistic barely moved: 1.777 → 1.734 (§9.3) |
| "Sparse stations report more rain because they sit in wetter places" | ❌ refuted | A neighbour-only statistic — mean of the *neighbour* on the sparse station's reporting days vs on all days — reads 1.78, and reads 1.00 on 149 dense controls. Siting cannot produce that (§9.2) |
| "Our basin rainfall is 2,304 mm/yr" | ⚠️ **not the comparable number** | That is a gauge mean; gauges cluster in populated valleys. Area-weighted is **2,206** mm/yr for 2008–2018 and 2,174 for 2009–2017 (§9.4) |
| "Switching to CHIRPS will fix the water surplus" | ❌ refuted | CHIRPS at the same centroids with the same weights gives 2,140 mm/yr — only 3.1 % below our IDW, against a surplus of ~8 %. Justify the merge by the r ceiling, not by volume (§9.4) |
| "The CHIRPS disagreement is caused by sampling geometry (centroid+area-weight vs grid-cell mean)" | ❌ refuted | Three basin-restricted estimators agree to 0.1 % (2,140.1 / 2,140.4 / 2,141.4 mm/yr). Our estimator's own bias is +0.7 %. The gap is a period mismatch — interannual range ±21 %, and 2012–2015 reproduces his 1,955 to 2.7 mm/yr (§9.5) |
| "The repair may be over-drying the field, since v2 falls below CHIRPS" | ❌ refuted | At independent neighbours the inserted days carry a wet-day rate of 0.171 against 0.328 overall (ratio 0.522) and 1.84 mm/day against 4.06 (ratio 0.414); only 2 of 83 stations show inserted days wetter than average. A bounded residual remains — neighbours did record rain on 17 % of them — so the true areal mean sits between 2,035.6 and 2,174.3, nearer the former (§10.4) |
| "The 18 energy-floor failures are all explained by the wet-forcing surplus" | ⚠️ **splits in two** | Removing 6.4 % of basin rainfall recovers only 4 of 18. The worst two have P unchanged to 3 dp and would need P halved. The class verdict stands (18 of 18 fail with observed rc below floor) but the residual 14 are local, not basin-wide (§10.6) |
| "The rebuilt IDW disagreed with the stored field because of k=20 fallback tie-breaking" | ❌ refuted | Only 20 of 134,797 differing cells were in the fallback set. The cause was three co-located gauge pairs tying in distance in the **k=6** pass, resolved by column order (§10.7) |
| "The gauge-order defect affects 44 minibacias by up to 13.1 mm/day" | ⚠️ **understated** | That was one alternative ordering. Random shuffles move **52–83 minibacias** by up to **20.5 mm/day** (§11.1) |
| "Gauges within 500 m of each other are duplicates and should be merged" | ❌ refuted | Of four pairs, two are duplicates (corr 1.000), one is a sequential instrument replacement (zero overlap), and one is a **coordinate error** — 1,470 shared days, corr 0.756, mean |diff| 1.9 mm at a nominal 5 cm. A distance-only merge rule would have averaged away a real gauge (§11.2) |
| "Merging the co-located gauges is cosmetic — the basin mean barely moves" | ⚠️ **half true** | Basin mean +0.04 %, but **542 minibacias change by a median +5.03 %, max +33.5 %**. Gauges are scored locally, so this changes the objective. A basin-level check alone would have concluded "negligible" and been wrong (§11.3) |
| "The residual energy-floor failures are our forcing's fault" | ⚠️ **only 2 of 14** | Two gauges have a selective precip gauge carrying 49–69 % of their catchment weight and are kept for that reason. The other 12 do not: 8 have no rating curve at all, and where curves exist R² runs 0.36–0.69 (§12.1) |
| "`identifiability.csv` shows all 10 parameters identified" | ⚠️ **confounded** | `iqr_frac_of_range` is exactly 0.0 for 7 of 10 parameters. The top 5 % of a **DDS** archive is a neighbourhood of the optimum by construction, so this measures search concentration, not information in the data. Morris `mu*` is the trustworthy screen, and it says `k_bas`, `k_int`, `kc_mult` and `fint` are weak |

---

## 7 — Traps for whoever picks this up

1. **Never compare NSE across windows with different observed variance.** NSE's benchmark is the
   within-window mean, so the metric changes when the window does. Score a fixed benchmark
   (day-of-year climatology) in every window and report the difference.
2. **A parameter surviving Morris screening is not a parameter the data constrained.** `k_bas`
   survived with `mu*` = 0.044 against `k_sup`'s 0.228 — a factor of five. Surviving means
   "detectable", not "identified".
3. **Do not read a DDS archive as a posterior.** DDS is greedy; its top 5 % is a ball around the
   optimum. Any IQR-based identifiability statistic computed from it will report near-zero width
   regardless of what the data actually say.
4. **Check parameter positions against their bounds before interpreting any fitted value.** Three of
   ten are railed here, and a railed parameter is reporting the bound, not the basin.
5. **A calibrated model can be right for the wrong reasons in one regime and visibly wrong in
   another.** The α/β trade in [doc 22 §4.5](22_dry_phase_diagnosis.md) is the diagnostic: if fixing bias breaks variance, the fit was
   compensating for an input error, not representing a process.
6. **Before blaming a process, check whether the metric's ceiling is set by the input.** Twelve
   parameter configurations left r inside 0.016 of each other. That flatness *is* the finding.
7. The harness in any re-run must reproduce the stored `q_sim_B_m3s` before its output is
   interpreted — 9.1×10⁻⁹ median relative error was the bar used here.
8. **`data/raw/climate/chirps_basin_*.nc` is a bounding box, not a basin clip.** The name says
   otherwise. Averaging it unmasked reads +14.1 % high because it includes the Pacific slope
   and the Caribbean (§9.5). Any areal statistic from those files needs an explicit mask.
9. **Interannual rainfall variability here is ±21 %** (1,731 mm/yr in 2015 to 2,619 in 2010).
   No basin-mean rainfall figure means anything without its window attached, and any
   cross-implementation comparison must fix the window first.
10. **A detector needs a calibrated null before its threshold means anything.** `dry_frac` and the
    neighbour `ratio` are statistics of the station's own series, so they confound suppression with
    climate and orography and have to be thresholded loosely. Selectivity reads 1.001 on 89
    known-good stations, so its threshold is a quantile of a measured null (§10.1).
11. **Three gauge pairs share an exact lat/lon, so the IDW depends on gauge column order** (§10.7).
    Sorting the gauge columns by code instead of inventory order moves 44 minibacias by up to
    13.1 mm/day. Any re-implementation must reproduce nb11's ordering, or merge the pairs first.
13. **Prove a defect is reproducible before claiming a fix.** The shuffle test is written to show the
    OLD code path failing first (52–83 minibacias move) and only then the new one holding. A fix for a
    defect you cannot summon on demand is untestable (§11.1).
14. **`merge` is a DataFrame method.** A column named `merge` is returned as a bound method on
    attribute access, so `df[df.merge]` raises instead of filtering. Cost an hour here; use `do_merge`.
15. **Check basin-level AND local effects, and report both.** Merging the co-located gauges moves the
    basin mean 0.04 % and 542 minibacias by a median 5 %. Either number alone misleads (§11.3).
12. **A repair that fixes a bias statistic can still move the mean too far.** Selectivity passing at
    1.040 does not prove the inserted days were dry; that needed its own neighbour test (§10.4).
    Test the direction you moved the answer, not only the defect you set out to remove.

---

## 8 — Open items

| # | item | blocks |
|---|---|---|
| 1 | Re-fit with a recession-signature objective term, `k_int < k_bas` constraint, and a `k_bas` lower bound below 15 d | the ≈ +0.02 parameter gain, and store realism |
| 2 | CHIRPS–gauge merged rainfall (nb11 → 12 → 13 → 14) | **r, and therefore the dry phase** |
| 3 | Extend the model period to 2008–2018. **Scoped: this needs a re-run, not new code.** nb11 §7 has no date clamp — it builds PET from whatever `era5land_ext_*` mosaics exist, and its readiness gate was the literal `len(ext) >= 108` (9 years), which is the only reason `forcing_minibacia_pet.csv` stops at 2017-12-31. All 132 mosaics are now on disk and the gate is updated to 132 (generator edited, **notebook not yet re-executed** — same generator/notebook drift convention as doc 17 §2.5) | 2008 spin-up + a 2018 validation year |
| 4 | Local-inertial routing for the Mompós / La Mojana reach. **Not to be implemented on current evidence** — celerity was swept 0.22 → 2.0 m/s and El Niño r moved < 0.016 ([doc 22 §4.6](22_dry_phase_diagnosis.md)). Carry it as a named limitation: celerity 0.221 m/s is a floodplain-storage surrogate for the Mompós reach, not a physical velocity | honesty about what the routing represents |
| 5 | PET review against the 49 mm/yr basin ET deficit | the +5.6 % outlet PBIAS floor and the 18 infeasible gauges |
| 6 | ~~`build_discharge_gauges.py:149-152` and `build_precip_gauges.py:62` rely on pandas date inference~~ **DONE** — both now detect per file/part via `src/dhime_dates.py`. All 98 precip files and 45 discharge parts proved ISO year-first; outputs content-identical, so nothing was silently transposed in these corpora. Recorded so the null result is not read as the fix being unnecessary | closed |
| 7 | ~~Finish the zero-suppression repair~~ **DONE (§10)** — selectivity detector with a threshold from the measured null; 153 stations repaired, 240,158 inferred-dry days; sparse-band selectivity 1.777 → **1.040**, dense band unmoved at 1.001; areal mean 2,174.3 → **2,035.6** mm/yr (−6.4 %); over-drying test passed. Energy floor 18 → **14**, target was ≤5 | partly closed — see item 10 |
| 10 | ~~Triage the 14 surviving energy-floor gauges~~ **DONE (§12)** — rule declared before the numbers: **2 EXCLUDE** (need P cut >25 %), **2 KEEP** (a selective gauge carries half their catchment weight — our defect, so it stays visible), **10 DOWN-WEIGHT**. 8 of 14 have no rating curve at all | closed; feeds the Phase 3 objective |
| 14 | **Check the 2.5× catchment-area disagreement at 23087200** (§12.3): ours 524 km², the collaborator's 1,324 km². A direct test of the doc-17 gauge re-snap that has never been run, and it bears on any area-normalised sediment yield | published specific yields |
| 15 | **Test the hydropower-diversion hypothesis for the two exclusions** (§12.2). Both sit in Antioquia (EPM / ISAGEN reservoirs and inter-basin transfers). 23087200's dominant precip gauge is healthy (selectivity 0.997), so its rc of 0.430 on a 0.7+ flank points at water leaving the catchment, not at bad data. `is_intake` does not flag them, so that flag list is incomplete | the *reason* recorded for excluding them |
| 11 | ~~Merge the co-located gauge pairs~~ **DONE (§11)** — `src/idw_forcing.py`: deterministic lexsort tie-break proven by a shuffle test, and an evidence-based merge (2 duplicates + 1 sequential merged, 294→291 gauges; Catam refused as a **coordinate error**, corr 0.756 at 5 cm). Basin mean +0.04 %, but **542 minibacias move by a median +5 %** | closed; nb11 unblocked |
| 12 | **EL DORADO CATAM `21205791` / AEROPUERTO CATAM `21206570` have one bad coordinate** (§11.2). They sit 5 cm apart in the catalogue yet disagree on 1,000 of 1,470 shared days (corr 0.756). Resolve against the IDEAM catalogue before either is trusted for interpolation | correct gauge geometry near Bogotá |
| 13 | nb11 §3 must be switched to `src/idw_forcing.py` rather than keeping its own copy of the interpolator. Adopting it moves 69 minibacias vs the stored field (areal mean unchanged) — expected, since the stored field embodies an arbitrary tie-break | one interpolator, not three |
| 8 | **Establish the provenance of the ~2,050 mm/yr basin reference** (§9.4) — uncited on both sides; his script says only "a published ~2,050", and CHIRPS itself sits +3.7 % above it. ~~Resolve the 9.5 % CHIRPS disagreement~~ **DONE (§9.5): our estimator is sound to 0.1 %; the gap is a period mismatch — interannual range is ±21 % and 2012–2015 gives 1,952 mm/yr. On the like-for-like window CHIRPS is 2,124.9 against IDW 2,174.3, +2.3 %, so a merge cannot close the ~8 % surplus** | using the reference as a validation target |
| 9 | Advisor question, not a code question: the collaborator **drops** sparse gauges where we **repair** them. [doc 22 §4.7](22_dry_phase_diagnosis.md) makes gauge density the binding constraint on `r`, so his remedy worsens the quantity we identified as the ceiling, while ours retains stations that §9.3 shows are still biased. Neither approach is obviously right | the merge design in nb11 |

---

## 9 — The forcing surplus: independent replication, and the repair audited

*(§9.3 found the repair half done. §10 finishes it — read the two together.)*

Added after the §4 diagnosis. [doc 22 §4.3](22_dry_phase_diagnosis.md) concluded the forcing supplies more water than the rivers
carry. This section tests that from the gauge side, and cross-checks it against an independent
implementation.

### 9.1 An independent codebase found the same defect by the opposite route

The collaborator (`github.com/yben409/simulating-suspended-sediment-transport`,
`scripts/15_build_forcing_v2.py`) independently discovered the zero-suppression defect and
measured a gradient we had never checked — mean rainfall rising as reporting density falls:

| reporting density | his mm/day | his % zeros | **ours, pre-repair** | **ours, % zeros** |
|---|---|---|---|---|
| reports >90 % of days | 4.5 | 63 | **4.38** (92 stations) | **60.4** |
| reports 50–90 % | 6.9 | 32 | **6.75** (119) | **26.9** |
| reports <50 % | 13.0 | 24 | **11.69** (83) | **23.7** |

Our pre-repair file reproduces his numbers closely on all six cells. Two codebases, written
independently, measured the same defect in the same corpus. His downstream consequences —
basin rainfall 2,420 mm/yr against a published ~2,050, actual ET 1,659 exceeding potential ET
1,239, Calamar discharge 1.7× too high — are the same surplus our [doc 22 §4.3](22_dry_phase_diagnosis.md) found as
*observed runoff coefficient below its energy floor at 18 of 18 failing gauges*. **Two
implementations, two different diagnostics, one conclusion.**

### 9.2 Separating suppression from geography — the control that was missing

A binned mean cannot distinguish "sparse stations omit dry days" from "sparse stations sit in
wetter places". Remote high-rainfall sites really are harder to maintain, so the second is not a
strawman. The test that separates them uses **only the neighbour's data**:

```
selectivity(S) = mean(D | days S reports) / mean(D | all days)
```

for `D` = up to 5 dense (>90 %) neighbours within 60 km. If `S` reports on a fair sample of days,
its reporting days are a random draw and selectivity = 1. If `S` reports preferentially when it
rains, then `D` — a different instrument, in a different place — is also wetter on those days,
because rainfall is regionally correlated. Selectivity > 1 is positive evidence of
rain-day-selective reporting that no siting argument explains.

| reporting density | selectivity, PRE-repair | selectivity, POST-repair | n post |
|---|---|---|---|
| reports >90 % | **1.001** | **1.003** | 149 |
| reports 50–90 % | 1.332 | 1.299 | 94 |
| reports <50 % | **1.777** | **1.734** | 45 |
| Spearman ρ(density, selectivity) | −0.895 | −0.807 | |

The dense band reads 1.001 / 1.003 — the metric returns exactly 1.00 on the population that
should be unbiased, over 89 and then 149 stations. That is the null the statistic needed, and it
passes. So the residual gradient is **selective reporting, not siting**.

### 9.3 What the repair did, and did not, do

`repair_precip_zero_suppression.py` inserted **109,129 inferred-dry station-days (13.7 % of the
corpus) across 70 of 294 stations** (median 1,688 days per repaired station).

Read the two tables together and the repair's true effect is not what the binned means suggest:

* the binned gradient improved 2.67× → 2.04×, but **most of that is a composition effect** — the
  >90 % band grew from 92 to 151 stations as repaired stations crossed the density threshold;
* the dense band's selectivity stayed at ~1.00 while gaining 60 stations, so **the stations it
  repaired genuinely became fair reporters**. The method works;
* but the sparse band's selectivity barely moved, 1.777 → 1.734. **The repair is incomplete in
  coverage, not defective in method.** 139 of 294 stations (45 below 50 % density at 1.734,
  94 in the 50–90 % band at 1.299) still report rain-selectively and still feed the IDW.

This is a falsifiable test of the repair that had never been run, and the repair fails it on
coverage. `selectivity` is also a better detector than the ratio test that found the defect
originally: it has a clean null at 1.00, validated here on 149 stations.

### 9.4 Area-weighted basin rainfall — and why CHIRPS will not fix the volume

Our often-quoted 2,304 mm/yr is a **gauge** mean and is not comparable to a published basin
figure: gauges cluster in populated valleys. Only the areal figure is comparable.

| quantity | mm/yr |
|---|---|
| unweighted mean of the 8,672 minibacia series | 2,218 |
| **area-weighted basin mean, 2008–2018** | **2,206** |
| area-weighted, 2009–2017 (reproduces `manifest.json` 2174.3 exactly) | 2,174 |
| **CHIRPS, sampled at the same centroids, same weights, same days** | **2,140** |
| reference (collaborator; **provenance not yet established**) | ~2,050 |

* IDW exceeds the reference by **+156 mm/yr (+7.6 %)** — the same order as the +7.9 % / +8.4 %
  flow excess in [doc 22 §4.5](22_dry_phase_diagnosis.md) and the +5.6 % outlet PBIAS floor in §3;
* IDW exceeds CHIRPS by only **+66 mm/yr (+3.1 %)**, and CHIRPS itself is +4.4 % above the
  reference.

**Consequence for Phase 3:** swapping to CHIRPS moves the water volume by about 3 %, not by the
~8 % the surplus needs. The CHIRPS merge must be justified by the **r ceiling of [doc 22 §4.7](22_dry_phase_diagnosis.md)**, not by
volume — and nobody should expect it to close the energy-floor gap. Fixing the volume means
finishing the zero-suppression repair on the 139 stations in §9.3, or down-weighting them.

The ~2,050 reference is doing real work in this argument and its provenance is unverified.
**Ask the collaborator for the citation before it is used as a validation target.** His
`scripts/15_build_forcing_v2.py` says only *"a published ~2,050"* with no reference attached, so
the number is currently uncited on both sides.

### 9.5 Two CHIRPS estimates of the same basin disagreed by 9.5 % — RESOLVED

**Verdict: our estimator is sound; the gap is a period mismatch, and the sampling-geometry
hypothesis is refuted.** All three candidate causes were tested on our own data, so the
comparison is controlled.

Four estimators of the same areal mean, CHIRPS, mm/yr. Basin fraction per CHIRPS cell was
built by area-summing `minibacias.tif` (EPSG:4326, 0.006667°, same bounding box, so each
0.05° CHIRPS cell is exactly 7.5 × 7.5 raster cells) — not by nearest-neighbour. The implied
basin area is 258,404 km² against the true 257,097, a 0.5 % check on the mask itself.

| estimator | 2008–2018 | 2009–2017 | vs E3 |
|---|---|---|---|
| **E1** minibacia centroids × minibacia area — **ours** | 2,140.1 | 2,123.8 | −0.1 % |
| **E2** CHIRPS cells whose centre is in the basin, cos-lat weighted | 2,140.4 | 2,124.0 | −0.0 % |
| **E3** CHIRPS cells × basin fraction × cos-lat — **rigorous** | 2,141.4 | **2,124.9** | — |
| **E4** the whole bounding box, unmasked | 2,443.0 | 2,436.9 | **+14.1 %** |

* **A3 sampling geometry — refuted.** The brief expected this to be the most likely cause. All
  three basin-restricted estimators agree to **0.1 %**. Our centroid-and-area-weight estimator
  carries a bias of +15 mm/yr (+0.7 %) against the rigorous basin-fraction mean. It is sound,
  and so is the same estimator applied to the IDW field.
* **A1 basin mask — the right magnitude, but the wrong sign.** `chirps_basin_*.nc` is a
  **bounding box**, not a polygon clip (202 × 96 cells, lat 1.4–11.4, lon −77.0 to −72.3), and
  using it unmasked costs **+14.1 %** — it sweeps in the Pacific slope and the Caribbean. That
  is the only tested mechanism large enough to explain 8.7 %, but it inflates. It cannot make
  *his* figure lower than ours. Worth recording as a trap regardless: the filename says
  `basin` and the contents are a rectangle.
* **A2 period — small between the two spans, but decisive overall.** 2009–2017 → 2008–2018 moves
  the mean by only +0.77 %. But **interannual variability is ±21 %** (1,731 mm/yr in 2015 to
  2,619 in 2010), so any window mismatch dominates an 8.7 % gap by itself. Several short
  contiguous windows reproduce his 1,955 almost exactly:

  | window | CHIRPS mean | vs his 1,955 |
  |---|---|---|
  | 2012–2015 | 1,952.3 | −2.7 |
  | 2012–2016 | 1,952.2 | −2.8 |
  | 2015–2017 | 1,958.2 | +3.2 |

**Consequence.** On the like-for-like 2009–2017 window, CHIRPS is **2,124.9** against our IDW's
**2,174.3** — the two products differ by only **+2.3 %**, tighter than the +3.1 % first
reported. §9.4's conclusion survives and is now on firmer ground: **the CHIRPS merge cannot
close the ~8 % surplus, and must be justified by the r ceiling of [doc 22 §4.7](22_dry_phase_diagnosis.md).** CHIRPS itself sits
+3.7 % above the uncited ~2,050 reference, so both products are above it — one more reason not
to treat that number as a target until it has a citation.

### 9.5b Superseded: the original statement of the discrepancy

Reading his script turned up a discrepancy that changes what Phase 3 should expect:

| quantity | his figure | ours |
|---|---|---|
| CHIRPS basin mean | **1,955 mm/yr** | **2,140 mm/yr** |
| gauge mean | 2,492 mm/yr | 2,218 (unweighted minibacia) |

Two independent samplings of the *same satellite product over the same basin* differ by
185 mm/yr. Candidate causes, none yet tested: different basin masks; different periods; and
different sampling geometry — we sample CHIRPS at the 8,672 minibacia centroids and weight by
minibacia area, which is not the same as a grid-cell mean over a basin polygon, especially where
minibacias are small in steep headwaters.

This matters because it flips the Phase 3 expectation. On **our** CHIRPS (2,140) the merge moves
volume by 3 % and cannot close the ~8 % surplus. On **his** (1,955) CHIRPS sits *below* the
~2,050 reference and a merge would close it and overshoot. The two readings recommend different
work, so the discrepancy has to be resolved before either is used to justify a volume claim —
and the r-ceiling justification for the merge ([doc 22 §4.7](22_dry_phase_diagnosis.md)) is unaffected either way, which is one more
reason to lead with it.

---

## 10 — Phase B: finishing the zero-suppression repair

§9.3 measured the v1 repair as incomplete in coverage: 70 of 294 stations touched, but
139 still rain-selective and still feeding the IDW. This section extends the detection,
then tests the result against the two basin-level numbers the surplus shows up in.

New code: `src/repair_precip_selectivity.py`. It reuses `repair()` from
`repair_precip_zero_suppression.py` unchanged, so the insertion mechanism — including the
60-day station-outage guard that refuses to infill a real outage as dry — is identical.
Outputs are written **alongside** v1 (`precip_gauges_daily_qc_v2.csv`,
`precip_selectivity_report.csv`) so both remain available for attribution.

### 10.1 Why a second detector, and why this one can set its own threshold

Both v1 tests are uncontrolled statistics of the station's *own* series:

* `dry_frac` confounds suppression with climate — a genuinely wet station has few dry days
  because it rains there, not because zeros were dropped;
* `ratio` (station annual total ÷ neighbour median) confounds suppression with orography —
  a ridge station legitimately reports 2× its valley neighbours.

Both therefore need a *loose* threshold to avoid firing on healthy wet stations, and a loose
threshold is exactly what left 139 stations unrepaired.

The §9.2 selectivity statistic is computed **entirely from the neighbour's data**, so the
station's own wetness cannot enter it. That is what makes it usable as a detector, and it is
why the threshold can be *measured* rather than chosen: the statistic has a known null.

| null on the 89 dense, unflagged reference stations | |
|---|---|
| median | 1.0013 |
| p90 / p95 | 1.0340 / 1.0629 |
| p99 | **1.2885** |
| max | 1.3435 |
| robust 3σ (median + 3·1.4826·MAD) | 1.0159 |

**Threshold = max(p99, robust 3σ) = 1.2885**, i.e. a ~1 % false-positive rate on healthy
dense stations by construction. The null has a heavy right tail (p95 1.063 but max 1.343),
so robust 3σ alone would have been far too tight; taking the larger of the two is the
conservative choice, and it is reported rather than tuned.

### 10.2 What it flagged

| | stations |
|---|---|
| selective (> 1.2885) | **144** |
| already caught by v1 | 60 |
| **new, and repairable** (`span_frac` < 0.85) | **83** |
| selective but essentially complete — cannot be fixed by infilling | 1 |
| v1 flags → v2 flags | 70 → **153** |

Two things worth naming. First, **10 of v1's 70 flags are not selective** — either
`dry_frac`/`ratio` anomalies of another kind, or v1 false positives. They were kept: the
flag sets are unioned, not replaced. Second, selectivity identifies a defect it cannot
repair — a station that is selective *and* essentially complete has wrong values on days it
*did* report, and infilling cannot fix that. Exactly one station is in that position and is
reported for exclusion or down-weighting.

Inserted: **240,158 inferred-dry station-days across 153 stations** (v1: 109,129 across 70),
taking the corpus from 686,752 to 926,910 station-days. A further **33,953 days were left
absent** as station outages by the ≥60-day guard.

### 10.3 Success criteria — both pass

Measured with §9.2's statistic against a **fixed** reference pool and **fixed** density bands
taken from the *pre-repair* file. Recomputing the bands afterwards is what made the §9.3
numbers hard to read (repaired stations change band), so both views are given.

| band (pre-repair density) | before | after |
|---|---|---|
| reports >90 % (n=89) | 1.001 | **1.001** |
| reports 50–90 % (n=113) | 1.332 | **1.009** |
| reports <50 % (n=81) | **1.777** | **1.040** |

| criterion | target | result | |
|---|---|---|---|
| sparse-band selectivity | < 1.15 | **1.040** | **PASS** (was 1.734) |
| dense-band selectivity | ≈ 1.00 | **1.001** | **PASS** — no over-repair |
| station-days inserted | reported | 240,158 on 153 stations | |

The dense band not moving is the load-bearing control: it proves the repair did not invent
dry days on healthy stations.

### 10.4 The check the volume result demanded: did we over-dry?

The areal mean fell 6.4 % and now sits *below* CHIRPS, so passing the selectivity criteria
does not rule out over-correction — inserting dry days can only lower rainfall, and if the
absent days were not really dry we have written false zeros. The falsification test is the
mirror of the detector: ask the neighbours what happened **on the inserted days**.

| at dense unflagged neighbours, over the 131,029 newly inserted days (83 stations) | |
|---|---|
| wet-day rate on inserted days | 0.171 |
| wet-day rate on all days | 0.328 |
| **ratio** | **0.522** |
| mean mm/day on inserted days | 1.836 |
| mean mm/day on all days | 4.056 |
| **ratio** | **0.414** |
| stations where inserted days were *wetter* than average | **2 of 83** |
| stations with ratio > 1.2 (clear over-drying) | **1** |

The inserted days were genuinely much drier than average at independent instruments, so the
inference is sound and the repair is **not** over-drying. But the ratio is 0.52, not 0:
neighbours still recorded rain on 17 % of the inserted days, averaging 1.8 mm/day, and
setting those to exactly 0.0 removes a real residual. **The honest reading is that the true
areal mean lies between the v2 and v1 figures, closer to v2** — a large step in the right
direction with a bounded, measured over-correction, not an exact answer.

### 10.5 Areal rainfall — and where it now sits

The IDW was regenerated with nb11's interpolator (k=6, inverse-distance-squared, masked to
observed gauges, k=20 fallback). **Reproduction gate first:** rebuilt from the *v1* gauge
file it reproduces the stored `forcing_minibacia_precip.csv` with **0 of 34,844,096 cells
differing** at that file's own 0.01 mm quantisation (max |ΔP| 0.0050 mm, exactly the
rounding half-width), and 124,097 k=20 fallback cells — nb11's printed figure exactly.

| area-weighted basin mean, mm/yr | v1 | v2 | change |
|---|---|---|---|
| 2009–2017 | 2,174.3 | **2,035.6** | **−138.7 (−6.4 %)** |
| 2008–2018 | 2,206.0 | **2,072.3** | −133.7 (−6.1 %) |

* v2 is now **4.2 % below CHIRPS** (2,124.9, Phase A) — it was +2.3 % above;
* v2 lands **0.7 % below the uncited ~2,050 reference**, which is notable but is not
  validation while that number has no citation (open item 8).

### 10.6 The energy floor — real improvement, criterion not met

| | |
|---|---|
| energy-floor failures, v1 field | **18** of 61 (reproduces the stored file) |
| energy-floor failures, v2 field | **14** of 61 |
| recovered by the repair | 4 |
| newly failing | 0 |
| median upstream P | 5.104 → 4.888 mm/day (−4.2 %) |
| median observed runoff coefficient | 0.497 → 0.528 |
| median `rc_floor` | 0.422 → 0.396 |

**Target was ≤ 5. Result 14. FAIL.** The reason is informative: the worst offenders barely
moved. 23087200 sits at 11.464 mm/day before and after (unchanged to 3 dp); 26127100 at
6.377 both times. 23087200's observed runoff coefficient is 0.430 against a floor of 0.705 —
closing that needs P to fall by roughly half, which no plausible suppression correction
delivers.

**So the ~8 % basin surplus and the worst energy-floor failures are two different problems.**
The repair removed 6.4 % of basin-wide rainfall and recovered 4 gauges; the remaining 14 are
local, and at the extreme end are more consistent with catchment-delineation or rating error
than with forcing. The class verdict of [doc 22 §4.3](22_dry_phase_diagnosis.md) stands — 18 of 18 failed with observed rc *below*
its floor, which is a wet-forcing signature — but it is now clear that the signature was
basin-wide for only a minority of them.

### 10.7 Three co-located gauge pairs make the IDW order-dependent

Found while diagnosing why the first rebuild missed the stored field at 44 of 8,672
minibacias by up to 13.1 mm/day, on nearly every day, with the *same* gauge set and the
*same* coordinates. My first hypothesis — k=20 fallback tie-breaking — was wrong: only 20 of
the 134,797 differing cells were in the fallback set.

Three pairs share an **exact** lat/lon:

| pair | lat, lon |
|---|---|
| CUCUNUBA `24010140` / CUCUNUBA-AUT `2401500040` | 5.219570, −73.78229 |
| CERINZA `24030590` / CERINZA `24035420` | 5.962250, −72.93850 |
| AEROPUERTO OLAYA HERRERA `27015070` / `27015330` | 6.224639, −75.58820 |

Their distances to every minibacia tie exactly, so `np.argsort` resolves the k=6 neighbour
set by **column index**. nb11 reindexes to the QC inventory's row order; sorting the columns
by code instead — a change no reviewer would flag — moves 44 minibacias by up to 13.1 mm/day.
Two defects in one:

1. **the IDW is not order-invariant**, so it is not reproducible under a harmless refactor;
2. **co-located gauges are double-weighted** — two instruments at one point each receive
   `1/max(d,1)²`, so that location carries twice the influence of a single gauge. They should
   be merged (highest approval level wins, as elsewhere in this pipeline) *before*
   interpolation.

Neither affects the basin aggregate (2,174.3 either way), so no conclusion above depends on
it — but it must be fixed before nb11 is re-run, or Phase C inherits an arbitrary choice.

---

## 11 — Phase 0: the IDW blocker (open item 11 closed)

New module `src/idw_forcing.py`, extracted from nb11 §3 so that the notebook, the
diagnostics and any re-run share **one** interpolator instead of three copies. It fixes the
two defects §10.7 found, which turned out to need different fixes.

### 11.1 Order-invariance: the defect is larger than first reported

| gate | result | |
|---|---|---|
| **G1** control — nb11 verbatim (`argsort` + inventory column order) vs the stored field | **0 of 34,844,096 cells differ**, 124,097 fallback cells (nb11's printed figure) | **PASS** |
| **G2** the defect, reproduced on demand — same `argsort`, gauge columns shuffled | 145,531 / 179,458 / 248,528 cells differ; **52 / 61 / 83 minibacias**; max \|ΔP\| **19.5 / 20.5 / 17.8 mm** | **PASS** (defect confirmed) |
| **G3** the fix — deterministic `lexsort` on (distance, gauge code), 5 shuffles | byte-identical field every time | **PASS** |

§10.7 reported 44 minibacias and 13.1 mm from *one* alternative ordering (sorted by code).
Random orderings are worse: up to **83 minibacias and 20.5 mm/day**. The earlier figure was
a lower bound on an arbitrary choice, not the size of the defect.

G2 matters as much as G3. A fix for a defect you cannot reproduce on demand is untestable,
so the shuffle test is written to *first* show the old code path failing and only then show
the new one holding. `assert_order_invariant()` in the module is the standing guarantee —
the `lexsort` is only the mechanism, and without the assertion nothing stops a later edit
reintroducing an order-dependent field.

**Cost of adopting determinism (G4):** against the stored field the deterministic
interpolator moves 194,081 cells across **69 minibacias**, max \|ΔP\| 20.47 mm — because the
stored field embodies one arbitrary tie-break and this one embodies a reproducible rule.
The **areal mean is unchanged: 2,174.3 mm/yr either way.** Anything that re-runs nb11
inherits the new local values, which is the correct outcome but must not be mistaken for a
data change.

### 11.2 Co-located gauges: a blanket rule would have destroyed data

Swept to 500 m as instructed and found a **fourth** pair the exact-tie search had missed.
Then classified each pair by what the two records do on the days they **both** report —
because that, not distance, is the evidence for whether they are one instrument or two:

| pair | dist | n both | mean \|diff\| | corr | verdict |
|---|---|---|---|---|---|
| AEROPUERTO OLAYA HERRERA `27015070` / `27015330` | 0.000 m | 276 | 0.000 mm | 1.000 | **duplicate** → merge |
| CUCUNUBA `24010140` / CUCUNUBA-AUT `2401500040` | 0.000 m | 366 | 0.003 mm | 1.000 | **duplicate** → merge |
| CERINZA `24030590` / `24035420` | 0.000 m | **0** | — | — | **sequential** → merge |
| EL DORADO CATAM `21205791` / AEROPUERTO CATAM `21206570` | 0.052 m | 1,470 | **1.915 mm** | **0.756** | **coordinate error** → **do NOT merge** |

Three distinct situations, and only two of them are duplicates:

* **duplicate** — one measurement filed under two codes. Merging is pure de-duplication.
* **sequential** — CERINZA has *zero* overlap: `24030590` runs 2008-01→2009-06 and
  `24035420` picks up 2009-07→2018-12. An instrument replacement, not a duplicate. Merging
  reconstructs one continuous record from two fragments, which is strictly better than
  interpolating across the join.
* **coordinate error** — Catam's two records overlap on 1,470 days and *disagree*: only 470
  identical, mean \|difference\| 1.9 mm, correlation **0.756**. At a nominal separation of
  5 cm that is not physical — the true duplicates above read 1.000, and the basin-wide
  inter-gauge correlation at 0–25 km is only 0.33 ([doc 22 §4.7](22_dry_phase_diagnosis.md)), so 0.756 is neither. **These are
  two real gauges and one of them has the wrong catalogue coordinates.** Merging them would
  have averaged away a genuine second observation, silently. Left unmerged and flagged.

**A distance-only rule would have destroyed that station.** The rule adopted is
evidence-based per cluster; `data/processed/precip_colocated_gauges.csv` carries the
classification with its numbers so the judgement is auditable rather than asserted.

Merge mechanics: highest approval level wins the day (`Definitivo > En revisión >
Preliminar`, the precedence `build_precip_gauges.py` already uses); the surviving code is
the member with the most records, so provenance stays traceable.

### 11.3 What the merge costs — negligible globally, material locally

Gauges **294 → 291**; station-days 926,910 → 926,268; k=6 fallback cells **41,504 →
41,180** (the merge *improves* coverage, because a reconstructed record fills days on which
neither fragment alone reported).

| area-weighted basin mean | v2 unmerged | v2 merged | change |
|---|---|---|---|
| 2009–2017 | 2,035.6 | 2,036.4 | **+0.8 mm/yr (+0.04 %)** |
| 2008–2018 | 2,072.2 | 2,073.1 | +0.8 mm/yr (+0.04 %) |

| local effect | |
|---|---|
| minibacias changed | **542** of 8,672 |
| median mean \|ΔP\| among them | 0.225 mm/day |
| **median relative change** | **+5.03 %** |
| max relative change | **+33.48 %** |
| largest single-day \|ΔP\| anywhere | 29.18 mm |

**The basin mean is untouched and 542 minibacias move by a median 5 % — so this matters, and
it would have been invisible in any basin-level check.** Gauges are scored locally, so a
5–33 % change in catchment rainfall is a change in the calibration objective. 542 is also
far more than the 69 minibacias affected by the tie-break alone: removing a gauge frees a
`k=6` slot, so a *different* sixth gauge enters for every minibacia near a merged cluster.

Both numbers had to be reported. Had only the basin mean been checked, the correct
conclusion would have been "negligible" and it would have been wrong.

---

## 12 — Phase 1: triage of the 14 residual energy-floor gauges (open item 10)

14 of 61 is 23 % of the calibration objective, and both failure modes are real — leaving an
impossible target in pulls parameters toward nonsense, while excluding a gauge whose problem
is *our* local forcing hides our own defect. So the decision rule was declared **before the
numbers were looked at**:

| rule | condition | verdict |
|---|---|---|
| D1 | one precip gauge carries ≥40 % of the catchment's IDW weight **and** is rain-selective (> 1.2885) | **KEEP** — our forcing defect; fix the forcing, don't hide it |
| D2 | flagged intake / distributary / nested inversion | **EXCLUDE** — hydrology the model does not represent |
| D3 | needs P to fall > 25 % with no dominant selective gauge | **EXCLUDE** — impossible target |
| D4 | rating curve R² < 0.90 or < 30 stage–discharge pairs | **DOWN-WEIGHT** |
| D5 | anything else | **DOWN-WEIGHT** — unresolvable |

Result: **2 EXCLUDE, 2 KEEP, 10 DOWN-WEIGHT** → 59 full-weight gauges, 10 down-weighted.
Full table in `data/processed/energy_floor_triage.csv`.

| code | area km² | P mm/d | Q mm/d | rc | floor | P cut needed | dominant precip gauge (share, selectivity) | rating R² (n) | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 22017010 | 2,411 | 5.645 | 0.947 | 0.168 | 0.480 | **31.2 %** | 22010010 (0.39, —) | **0.359** (6,966) | EXCLUDE D3 |
| 23087200 | 524 | 11.464 | 4.930 | 0.430 | 0.705 | **27.5 %** | 23080750 (0.61, **0.997**) | — (0) | EXCLUDE D3 |
| 26107130 | 748 | 5.453 | 1.869 | 0.343 | 0.498 | 15.5 % | 26100670 (0.34, 1.258) | 0.536 (3,075) | DOWN-WEIGHT D4 |
| **22077060** | 731 | 4.841 | 1.040 | 0.215 | 0.368 | 15.4 % | 22070030 (**0.49, 1.445**) | — (0) | **KEEP D1** |
| 26027240 | 188 | 4.750 | 1.460 | 0.307 | 0.447 | 13.9 % | 26020460 (0.47, 1.001) | — (0) | DOWN-WEIGHT D5 |
| 26197020 | 255 | 6.546 | 2.867 | 0.438 | 0.563 | 12.5 % | 26195020 (0.55, 1.020) | — (0) | DOWN-WEIGHT D5 |
| 26237020 | 210 | 5.513 | 1.681 | 0.305 | 0.410 | 10.5 % | 27011110 (0.29, 1.311) | 0.455 (305) | DOWN-WEIGHT D4 |
| 26127100 | 101 | 6.377 | 2.908 | 0.456 | 0.555 | 9.9 % | 26135040 (0.44, 1.000) | — (0) | DOWN-WEIGHT D5 |
| 26167060 | 179 | 5.393 | 2.188 | 0.406 | 0.448 | 4.2 % | 26155110 (0.31, 1.000) | 0.685 (551) | DOWN-WEIGHT D4 |
| **21107030** | 288 | 4.730 | 1.528 | 0.323 | 0.360 | 3.7 % | 21100070 (**0.69, 1.575**) | — (0) | **KEEP D1** |
| 23087160 | 344 | 8.712 | 4.834 | 0.555 | 0.591 | 3.6 % | 27011230 (0.29, 1.285) | — (0) | DOWN-WEIGHT D5 |
| 26027200 | 320 | 4.537 | 1.708 | 0.376 | 0.395 | 1.9 % | 26020460 (0.58, 1.001) | — (0) | DOWN-WEIGHT D5 |
| 21237040 | 243 | 4.118 | 0.935 | 0.227 | 0.237 | 1.0 % | 21205670 (0.22, 1.664) | — (0) | DOWN-WEIGHT D5 |
| 26207080 | 30,848 | 5.131 | 2.217 | 0.432 | 0.436 | 0.4 % | 26195020 (0.05, 1.020) | 0.644 (385) | DOWN-WEIGHT D4 |

### 12.1 Only 2 of 14 are ours, and 8 of 14 cannot be checked at all

Two gauges (22077060, 21107030) fail with a *selective* precip gauge carrying half to
two-thirds of their catchment weight — 1.445 and 1.575 selectivity, and both were repaired,
so what remains is residual local inflation from a gauge that was already treated. **These
stay in the objective.** Excluding them would delete the evidence of our own forcing defect,
and both need only a 4–15 % local P correction, which is within reach.

Eight of the 14 have **no rating curve at all** (`n_pairs = 0`), so their discharge cannot be
independently verified. That is not "unresolvable" in the sense of being fine — it is a
measurement gap, and D5 down-weights rather than excludes precisely because we cannot tell
the difference between a bad gauge and a bad catchment there.

Where a rating curve *does* exist it is mostly poor: **R² 0.359 on 6,966 stage–discharge
pairs** at 22017010, 0.455, 0.536, 0.644, 0.685 elsewhere. An R² of 0.36 over nearly seven
thousand pairs is not noise, it is a rating relationship that does not hold — which is
independent support for excluding that gauge.

### 12.2 The two exclusions look like water leaving the catchment, not error

23087200 is the interesting one, and the collaborator's independent run corroborates it: his
second-worst station, PBIAS **+417 %**, KGE **−4.59**. Two implementations, two different
forcing pipelines, the same station broken in the same direction — the model produces far
more water than the river carries.

But its dominant precip gauge is *healthy*: 23080750 carries 61 % of the catchment weight
with selectivity **0.997** and was never repaired. So the rainfall is well supported, and
11.46 mm/day (4,187 mm/yr) is high but entirely plausible on the Antioquia–Chocó flank. The
observed runoff coefficient of 0.430 is what does not fit: that flank should run at 0.7+.

**Hypothesis to check, not a conclusion: upstream hydropower diversion.** Both exclusions sit
in Antioquia, where EPM and ISAGEN operate major reservoirs and inter-basin transfers. Water
routed out of a catchment for generation makes observed Q genuinely far below P − ET, with no
error anywhere in the data. If that is what these are, they are D2 (unrepresented hydrology)
rather than D3 (bad data), and the verdict is the same — exclude — but the *reason* recorded
in the paper would be different, and defensible. `is_intake` in `gauges.csv` does not flag
them, so the flag list is incomplete rather than the gauges being clean.

### 12.3 A 2.5× catchment-area disagreement between the two implementations

For 23087200 we compute an upstream area of **524 km²**; the collaborator reports
**1,324 km²**. That is not a rounding difference, and it cannot be reconciled by the ENSO
window or the forcing — it is the drainage network. One of the two delineations is wrong, or
the two are snapping the gauge to different reaches.

It does not change this gauge's verdict (both implementations find it broken, and in the same
direction) but it is a direct check on the doc-17 gauge re-snap that nobody has run, and it
should be settled before any published area-normalised sediment yield. New open item 14.

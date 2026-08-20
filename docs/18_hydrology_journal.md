# 18 — Hydrology journal: water balance, calibration, and the dry-phase diagnosis

> **STATUS — 2026-08-12. LIVE as the Phase B record; §1's "Current state" is attempt-1 vintage.**
> **What this document is for:** §5 the verdict, **§6 checked-and-refuted**, **§7 the traps**, §8
> the open-items register, §9–§12 the forcing follow-up, §14 the v2 rebuild, **§15 the CHIRPS
> merge and §15.5 its closing read-out.** None of that is retracted.
> **What has changed since §1 was written:** three further calibration attempts ran — H1, H2 and
> **H2E** — and Phase B **CLOSED on H2E** ([docs/30](30_phase_c_plan.md) §1). §1's skill,
> parameter-bound and store-ordering rows are **attempt 1 (Config B)** and are superseded by
> [docs/26](26_phase3_refit.md) Addendum A.2/A.4/A.5; see the note under that table. Phase C is
> **ACTIVE**, not blocked. §8 has been back-annotated where items closed.
> **Where current status lives:** `progress_map.html` (RULE 0: for status the tracker wins), then
> [docs/00_INDEX.md](00_INDEX.md).

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
| ~~Phase C (sediment)~~ | ~~Still blocked — on mainstem SSC data and on the doc 19 `calibration_safe` gate~~ |

> ⚠ **CORRECTED 2026-08-12. This table is attempt 1 (Config B, v1 forcing, old objective).** Kept
> because it is what was true when the diagnosis in §4–§6 was run; it is not the adopted
> configuration. The owning record for every superseded row is
> [docs/26](26_phase3_refit.md) Addendum (read §5.1 before quoting any fitted parameter).
>
> | row above (attempt 1) | adopted configuration **H2E** (attempt 4) | owner |
> |---|---|---|
> | Validation skill median KGE **+0.450** | VAL-all KGE **0.356**, NSE 0.130, r 0.591, α 0.905, β 1.035, PBIAS **+3.51 %** | A.4 |
> | La Niña **+0.399** · El Niño **+0.193** | La Niña **0.344** · El Niño **0.200**; **skill over climatology +0.106 / −0.0005** | A.5 |
> | Recession realism 48.6 d vs 14 d observed | fleet-median recession ratio **1.082**; *"Every period passes ≤ 1.5× on both"* | A.3 · [docs/29](29_seed_expansion.md) rule (b) |
> | `kc_mult` railed at 2.00 | `kc_mult` **1.6625** — *"confirmed off the rail that held H1 at 98.8 % and H2 at 93.3 %"*; railed **2 of 10 global / 3 of 18 dimensions** | A.2 |
> | Store ordering `k_int` slower than `k_bas` | `k_int < k_bas` now holds by construction (`k_sup` 19.20 d, `k_int` 0.87 d, `k_bas` 42.97 d) — but A.2: *"**a constrained ordering relocates compensation, it does not remove it**"*, surface response now 22× slower than interflow | A.2 |
>
> **The caveat that must travel with H2E:** *"**The dry phase in the adopted configuration is at
> climatology, not above it: −0.0005.**"* (A.5). Every Phase C sediment claim inside the El Niño
> window inherits it.
>
> **Phase C is ACTIVE, not blocked**, and both of the struck row's grounds are discharged:
> - *mainstem SSC data* — [docs/30](30_phase_c_plan.md) header: *"It supersedes the 'Phase C
>   blocked' line in older docs."* Its measured form is [docs/32](32_ssc_qc_audit.md) §R6:
>   **79/79 stations classified**, 28 mapped, **18 usable or usable-with-caveat**, and *"`21237020`
>   ARRANCAPLUMAS (Magdalena — the only Magdalena-trunk SSC station in the entire network)"* —
>   *"This is the quantitative form of 'Phase C is blocked on mainstem SSC'."*
> - *the doc 19 `calibration_safe` gate* — **built and executed** as stage C1:
>   [docs/32](32_ssc_qc_audit.md) is that explicit SSC-quality gate, pre-registered §0–§6 and read
>   out R1–R7.
>
> ~~Phase C has since advanced to C3 (OPEN — [docs/37](37_c3_closure.md), four amendments) with
> **C4.3, the sediment calibration search, formally BLOCKED** ([docs/47](47_c4_entry_verdict.md):
> *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not start.**"*).~~ For live status read
> `progress_map.html`.
>
> **⚠ THAT SENTENCE IS ITSELF SUPERSEDED — REFRESHED 2026-08-19** (it was written 2026-08-12 and
> was true then; kept struck, not quoted as current). **Phase C has since COMPLETED:**
> - **C3 remains OPEN** on its closure conjunction — [docs/37](37_c3_closure.md), four amendments;
>   A3 (2026-08-12) states *"C3 stays OPEN"*.
> - **C4.3 RAN and RAILED** — [docs/55](55_c43_verdict.md), verdict **RAILED / EXPLORATORY, NOT
>   adopted**. The `C4.3-BLOCKED-UNTIL-LS-LANDS` entry condition was **discharged** when the LS
>   act landed (`ls_formulation = buarque_2015_dg`).
> - **C5 REPRODUCED the observed ENSO contrast** — [docs/56](56_c5_enso_application.md):
>   **18/18** stations, median modelled rate ratio **3.05×** (range 1.62–4.85), robust across
>   β ∈ {0.45, 0.56, 0.65} and both window pairs. **The 3.05 sits at the LOWER EDGE of the
>   observed ~3–5 primary band** — which is where the caveat two paragraphs above lands: the dry
>   phase is at climatology (−0.0005), so nothing here licenses reading the agreement as tighter
>   than its lower-edge position.

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

[doc 22 §4.3](22_dry_phase_diagnosis.md) shows this floor is real but is **not** what breaks the dry phase.

---

## 4 — The dry-phase diagnosis → [doc 22](22_dry_phase_diagnosis.md)

Moved to its own document when this one passed 65 KB. **Read
[doc 22](22_dry_phase_diagnosis.md) before touching calibration.** The findings it
establishes, which the rest of this document depends on:

| finding | evidence |
|---|---|
| All three standing hypotheses for the dry-phase failure are **refuted**, and hypothesis (b) was **backwards** | 30 full model runs; harness reproduced the stored `q_sim_B_m3s` to 9.1×10⁻⁹ before anything was interpreted |
| ~⅓ of the headline gap is the **NSE yardstick**, not the model | a day-of-year climatology also scores NSE −0.062 in that window; obs CV 0.799 is the record's highest |
| The collapsing term is **α, not β** — variance is worth +0.275 KGE, bias only +0.101 | repair ladder, [doc 22 §4.2](22_dry_phase_diagnosis.md) |
| The model triples the **lowest** flows in the dry phase (+244 % in Q0–10) and undershoots the highest | bias by flow quantile |
| `k_bas` is **not** the cause — correcting it to the observed 13.9 d recession buys +0.021 | 10-run sweep, Morris `mu*` 0.044 |
| The calibration bought its fit with **compensating errors** — `kc_mult` railed at 2.00, `k_int` railed at 117.4 and *slower* than `k_bas`, celerity 4.5× below prior | parameter positions vs bounds |
| The **hard floor is r ≈ 0.57**, invariant across all 12 parameter configurations tested, and it is inherited from the rainfall field (LOO IDW r = 0.40) | doc 22 [doc 22 §4.7](22_dry_phase_diagnosis.md) |

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
   > **READ-OUT 2026-08-12 — attempted, and it did not work.** The rebuild ran (nb11 → nb12 → v2,
   > §14) and the merge was built and **rejected twice by its volume gate** (§15, §15.5;
   > [docs/33](33_c2b_preregistration.md) §1). No `notebook 13 → 14` run on a merged field was ever
   > launched and **no v3 forcing exists**. §15.5, verbatim: *"**no route to a passing volume gate
   > exists inside the merge code.**"* The surviving route — repairing the 139 residual
   > rain-selective stations, upstream of the merge — is **untested**. The ranking above still
   > stands as a ranking; item 4 is simply no longer available.
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
| "The gauge-order defect affects 44 minibacias by up to 13.1 mm/day" | ⚠️ **understated** | That was one alternative ordering. Random shuffles move **52–83 minibacias** by up to **20.5 mm/day** ([doc 23 §11.1](23_gauge_geometry.md)) |
| "Gauges within 500 m of each other are duplicates and should be merged" | ❌ refuted | Of four pairs, two are duplicates (corr 1.000), one is a sequential instrument replacement (zero overlap), and one is a **coordinate error** — 1,470 shared days, corr 0.756, mean |diff| 1.9 mm at a nominal 5 cm. A distance-only merge rule would have averaged away a real gauge ([doc 23 §11.2](23_gauge_geometry.md)) |
| "Merging the co-located gauges is cosmetic — the basin mean barely moves" | ⚠️ **half true** | Basin mean +0.04 %, but **542 minibacias change by a median +5.03 %, max +33.5 %**. Gauges are scored locally, so this changes the objective. A basin-level check alone would have concluded "negligible" and been wrong ([doc 23 §11.3](23_gauge_geometry.md)) |
| "The residual energy-floor failures are our forcing's fault" | ⚠️ **only 2 of 14** | Two gauges have a selective precip gauge carrying 49–69 % of their catchment weight and are kept for that reason. The other 12 do not: 8 have no rating curve at all, and where curves exist R² runs 0.36–0.69 ([doc 23 §12.1](23_gauge_geometry.md)) |
| "The gauge remap injected RC_REFERENCE = 0.435, so the energy-floor test is circular" | ❌ refuted | Remapped and kept rc distributions have the same spread (log-SD 0.895 vs 0.886, ratio 1.009; Levene p = 0.76), and the remapped median distance from the reference is **larger** (0.435 vs 0.402). The rc target only breaks ties among a 3×3 window of candidates, so it cannot manufacture an rc no nearby minibacia produces ([doc 23 §13.1](23_gauge_geometry.md)) |
| "The 2.5× area gap at 23087200 means his network is wrong and ours is fine" | ⚠️ **neither is reliable per gauge** | Median ratio 0.991 over 85 gauges, but 31 of 85 differ by >2×; removing his 4 mainstem snaps still leaves only 28 of 81 within 25 %. Inverting the balance cannot reject his area either — it implies rc 0.17, the 27th percentile of the never-remapped distribution ([doc 23 §13.2](23_gauge_geometry.md)–13.3) |
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
19. **`pd.read_csv` silently truncates very wide CSVs, non-deterministically, to a contiguous
    prefix** (§14.3). 4,018 × 8,673 / ~180 MB returned 1,309 rows one call and 3,630 the next from a
    provably intact file, with no exception. Because the result is a prefix, length/monotonicity/
    duplicate/“calendar holes” checks all pass. Use `.npy` for anything this wide, and verify the
    parsed row count against the file's own line count counted from raw bytes — never against the
    parser that produced it.
20. **A file count is not a file check.** `era5land_ext_2008_M06.nc` was internally corrupt at a
    normal 43.69 MB; only opening it and reading a timestep found it (§14.3). The same reasoning that
    caught zero-suppressed gauges applies to inputs: test the thing, not its metadata.
21. **Extracting a code block into a module drops its incidental locals.** nb11 §3's apparent
    interface was `P` and `dk6`; four more names were load-bearing 90 lines away (§14.4). Diff the names
    the old block bound against the names later code reads before assigning — one command, and it
    answers in one shot what symptom-patching takes several executions to find.
22. **`np.save` round-trips `datetime64[D]` as `[s]`, and `DatetimeIndex.equals()` is
    resolution-sensitive** (§14.3). Identical instants compare unequal. Cast to `[ns]` on load — do
    *not* loosen the assertion, which is what would have hidden trap 19.
23. **Changing a window changes the population, not just the filter.** Extending to 2008–2018 took the
    calibration set to **63**, not the predicted 59, because gauges that failed `n_window` gates
    qualified (§14.2). Any “N of 61” criterion written before a period change is stale.
16. **A tie-break is not an optimiser.** `fix_gauge_minibacia_mapping.py` scores candidates against a
    basin-wide rc reference, which looks like it must inject that reference into the data — but the
    candidate set is a 3×3 window, so the reference only orders a handful of geometrically fixed
    options. Measured effect on the rc spread: none ([doc 23 §13.1](23_gauge_geometry.md)). Check a mechanism's leverage before
    assuming it has any.
17. **Two independent D8 delineations of the same basin disagree by >2× on a third of a shared
    85-gauge sample** ([doc 23 §13.2](23_gauge_geometry.md)), while their medians agree to 1 %. A basin-level cross-check would
    have read as validation. Any per-gauge area-normalised quantity (t/km²/yr above all) needs an
    arbiter external to both networks.
18. **`is_intake` is a name regex, not a regulation inventory** ([doc 23 §13.4](23_gauge_geometry.md)). It fires on `BOCATOMA|CANAL`
    in the station name, so a place-named gauge below a reservoir is invisible to it.
13. **Prove a defect is reproducible before claiming a fix.** The shuffle test is written to show the
    OLD code path failing first (52–83 minibacias move) and only then the new one holding. A fix for a
    defect you cannot summon on demand is untestable ([doc 23 §11.1](23_gauge_geometry.md)).
14. **`merge` is a DataFrame method.** A column named `merge` is returned as a bound method on
    attribute access, so `df[df.merge]` raises instead of filtering. Cost an hour here; use `do_merge`.
15. **Check basin-level AND local effects, and report both.** Merging the co-located gauges moves the
    basin mean 0.04 % and 542 minibacias by a median 5 %. Either number alone misleads ([doc 23 §11.3](23_gauge_geometry.md)).
12. **A repair that fixes a bias statistic can still move the mean too far.** Selectivity passing at
    1.040 does not prove the inserted days were dry; that needed its own neighbour test (§10.4).
    Test the direction you moved the answer, not only the defect you set out to remove.

---

## 8 — Open items

| # | item | blocks |
|---|---|---|
| 1 | ~~Re-fit with a recession-signature objective term, `k_int < k_bas` constraint, and a `k_bas` lower bound below 15 d~~ **DONE ([doc 26](26_phase3_refit.md))** — recession ratio 3.86× → **1.27×** and it holds on the held-out years; El Niño α 0.793 → **0.911**; stores no longer inverted. Cost ≈0.03 of validation median KGE, which is the designed trade. **But the search relocated the compensation**: H2 rails `k_sup` at 99.8 % and `k_int_frac` at its floor, giving k_sup 19.8 d > k_bas 13.7 d. Constraining one ordering moved the inversion, it did not remove it | closed; see item 21 |
| 2 | ~~CHIRPS–gauge merged rainfall (nb11 → 12 → 13 → 14)~~ **DONE, and NEGATIVE — CLOSED (§15, §15.5).** The merge was built (`src/merge_chirps_gauges.py`), its LOOCV gate **passed** (r 0.447 > 0.429) and its **volume gate FAILED** (2,188.5 mm/yr, +7.47 % against [2,016.0, 2,056.8]) — twice. No forcing file was written; nb13/nb14 were never re-run on a merged field. See item 20 for the full read-out | closed |
| 3 | ~~Extend the model period to 2008–2018~~ **DONE (§14)** — nb11 and nb12 executed; P and PET both span 2008-01-01..2018-12-31 (4,018 days). Required rebuilding one internally corrupt ERA5 mosaic. Spin-up now comes from *inside* the period: use 2008, score 2009–2018 | closed |
| 4 | Local-inertial routing for the Mompós / La Mojana reach. **Not to be implemented on current evidence** — celerity was swept 0.22 → 2.0 m/s and El Niño r moved < 0.016 ([doc 22 §4.6](22_dry_phase_diagnosis.md)). Carry it as a named limitation: celerity 0.221 m/s is a floodplain-storage surrogate for the Mompós reach, not a physical velocity | honesty about what the routing represents |
| 5 | ~~PET review against the 49 mm/yr basin ET deficit~~ **PARTLY DONE — the ET-*function* half succeeded and was adopted; the energy-deficit half is not retired.** The candidate one-function change (replace `ET = kc·PET·(W/Wm)` with the FAO-56 threshold form) was pre-registered and run: [docs/29](29_seed_expansion.md) rule (b) — *"**SUCCESS, all three conditions** … the linear stress ET = kc·PET·(W/Wm) was why kc railed; the FAO-56 threshold form releases it at no cost"* — and H2E was adopted on it. **Residue, still open:** `kc_mult` 1.662/1.836 is off its rail but *"still above the FAO-56 plausibility bar of ≤1.2 — the ET form was a real cause, not the whole story"* ([docs/31](31_phase_c_workplan.md) known-open register #2). The **49 mm/yr deficit itself is unchanged**: §14.2 re-measures basin PET at **1,251.6 mm/yr**, *"the figure §3's energy floor has used since it was written"* | partly closed — residue is docs/31 register #2 |
| 6 | ~~`build_discharge_gauges.py:149-152` and `build_precip_gauges.py:62` rely on pandas date inference~~ **DONE** — both now detect per file/part via `src/dhime_dates.py`. All 98 precip files and 45 discharge parts proved ISO year-first; outputs content-identical, so nothing was silently transposed in these corpora. Recorded so the null result is not read as the fix being unnecessary | closed |
| 7 | ~~Finish the zero-suppression repair~~ **DONE (§10)** — selectivity detector with a threshold from the measured null; 153 stations repaired, 240,158 inferred-dry days; sparse-band selectivity 1.777 → **1.040**, dense band unmoved at 1.001; areal mean 2,174.3 → **2,035.6** mm/yr (−6.4 %); over-drying test passed. Energy floor 18 → **14**, target was ≤5 | partly closed — see item 10 |
| 10 | ~~Triage the 14 surviving energy-floor gauges~~ **DONE ([doc 23 §12](23_gauge_geometry.md))** — rule declared before the numbers: **2 EXCLUDE** (need P cut >25 %), **2 KEEP** (a selective gauge carries half their catchment weight — our defect, so it stays visible), **10 DOWN-WEIGHT**. 8 of 14 have no rating curve at all | closed; feeds the Phase 3 objective |
| 14 | **Catchment areas are unreliable per gauge in BOTH networks** ([doc 23 §13.2](23_gauge_geometry.md)) — median ratio 0.991 over 85 shared gauges but **31 of 85 differ by >2×**, and 4 of his are mainstem-snapping failures (up to 1,154×). Removing those 4 still leaves only 28 of 81 within 25 %. Needs an arbiter external to both DEMs: IDEAM's catalogue area, which is **not** in any local table | **any t/km²/yr sediment yield** |
| 15 | **Hydropower-diversion hypothesis needs an external register** ([doc 23 §13.4](23_gauge_geometry.md)). `is_intake` is a name regex (`BOCATOMA|CANAL`) plus a manual doc-17 list, so it structurally cannot flag a place-named gauge below a reservoir — PAILANIA is not called a canal. Data acquisition, not a code fix | the *reason* recorded for excluding the two gauges |
| 16 | ~~Re-snap gauges with regional rc references (Phase 1c)~~ **NOT JUSTIFIED — do not run** ([doc 23 §13.1](23_gauge_geometry.md)). The circularity charge was tested and refuted: remapped vs kept rc spread is identical (log-SD ratio 1.009, Levene p = 0.76) and the remapped group sits *further* from 0.435, not closer. Anyone reviving this must beat p = 0.76 | closed |
| 11 | ~~Merge the co-located gauge pairs~~ **DONE ([doc 23 §11](23_gauge_geometry.md))** — `src/idw_forcing.py`: deterministic lexsort tie-break proven by a shuffle test, and an evidence-based merge (2 duplicates + 1 sequential merged, 294→291 gauges; Catam refused as a **coordinate error**, corr 0.756 at 5 cm). Basin mean +0.04 %, but **542 minibacias move by a median +5 %** | closed; nb11 unblocked |
| 12 | **EL DORADO CATAM `21205791` / AEROPUERTO CATAM `21206570` have one bad coordinate** ([doc 23 §11.2](23_gauge_geometry.md)) — 5 cm apart in the catalogue yet disagreeing on 1,000 of 1,470 shared days (corr 0.756). **Guarded** by `idw_forcing.NEVER_MERGE` so no threshold change can merge them ([doc 23 §11.4](23_gauge_geometry.md) G-B); still needs resolving against the IDEAM catalogue | correct gauge geometry near Bogotá |
| 13 | ~~Switch nb11 §3 to `src/idw_forcing.py`~~ **DONE ([doc 23 §11.4](23_gauge_geometry.md))** — generator switched, `assert_order_invariant()` now runs inside the notebook, `return_detail=True` supplies the fallback mask and neighbour distances nb11 needed. **The notebook has not been re-executed** (Phase 2) | closed |
| 8 | **Establish the provenance of the ~2,050 mm/yr basin reference** (§9.4) — uncited on both sides; his script says only "a published ~2,050", and CHIRPS itself sits +3.7 % above it. ~~Resolve the 9.5 % CHIRPS disagreement~~ **DONE (§9.5): our estimator is sound to 0.1 %; the gap is a period mismatch — interannual range is ±21 % and 2012–2015 gives 1,952 mm/yr. On the like-for-like window CHIRPS is 2,124.9 against IDW 2,174.3, +2.3 %, so a merge cannot close the ~8 % surplus** | using the reference as a validation target |
| 9 | Advisor question, not a code question: the collaborator **drops** sparse gauges where we **repair** them. [doc 22 §4.7](22_dry_phase_diagnosis.md) makes gauge density the binding constraint on `r`, so his remedy worsens the quantity we identified as the ceiling, while ours retains stations that §9.3 shows are still biased. Neither approach is obviously right | the merge design in nb11 |

| 17 | **`PET_READY = len(ext) >= 132` in nb11 counts filenames, not readable files** (§14.3). `era5land_ext_2008_M06.nc` was internally corrupt at normal size and passed both a name count and a size check. Replace with an open-and-read-a-timestep check | trusting any file-count gate |
| 18 | ~~Re-run nb13 → nb14 on `model_inputs_v2/`~~ **DONE ([doc 26](26_phase3_refit.md))** — 4,000 model runs, four concurrent searches. **H2 − H1 on 59 common gauges and the matched 2009–2017 window: β −0.044, PBIAS −4.44 pts, r +0.0033.** The repair fixed volume and left correlation exactly where it was, so **volume and correlation are independent problems** and no further work on rainfall totals will move the ENSO contrast. H3 dropped — the merge was never implemented. 3/9 criteria for both cells against 0/9 for Config B; the primary criterion fails in both its absolute and its ratio form | closed; item 20 is now the only lever |
| 19 | **The Phase 3 energy-floor criterion has a stale denominator.** It reads “≤ 5 of 61”; the calibration set is now **63** (§14.2), and [doc 23 §13.2](23_gauge_geometry.md) shows area — the rc denominator — is unreliable per gauge in both implementations. Restate on the subset whose areas agree, or drop it from the physical column | a criterion that measures delineation as much as forcing |
| 20 | ~~**CHIRPS merge not attempted** — and after [doc 26](26_phase3_refit.md) it is the **only remaining lever on the dry phase** (§14). Quantile-map CHIRPS *to* the gauge distribution so volume stays gauge-controlled; gate on LOOCV beating 0.429. 41,180 fallback cells remain, nearest gauge median 16.3 km / max 71.5 km~~ **DONE, and NEGATIVE — CLOSED-NEGATIVE (§15) / CLOSED (§15.5), corrected 2026-08-12.** It *was* attempted, exactly as specified: `src/merge_chirps_gauges.py` quantile-maps CHIRPS to the gauge distribution per (elevation band × hydrographic zone), and the 41,180 k=6-silent fallback cells were taken by mapped CHIRPS. **§15: "built, validated, and NOT adopted."** LOOCV gate **PASSED** (median daily r **0.447** > 0.429); **VOLUME gate FAILED** (**2,188.5 mm/yr**, **+7.47 %** against the registered band **[2,016.0, 2,056.8]**). The registered repair (H-CHIRPS, [doc 33](33_c2b_preregistration.md) §1) was then executed and was a **no-op** — doc 33 §1: *"The registered intervention turned out to be a **no-op**: the quantile maps already included the inferred-dry days, so **the diagnosed cause in docs/18 §15.3 was wrong**."* §15.5 measures the re-run as **bit-identical** (max \|diff\| 0.000e+00 on every scored column, 291 rows), the inferred-dry days as **25.9 %** of the fit input, and concludes: *"**no route to a passing volume gate exists inside the merge code**."* **What survives is one UNTESTED upstream hypothesis** — the **139** stations still reporting rain-selectively after the repair (§9.3), whose missing days are *"not in the record at all"* and therefore cannot be put into a pool by any change to the merge code. **No fix is available and none is pending; no v3 forcing exists.** *(doc 33 §1's read-out pointer says "see §7"; §7 of doc 33 is the H-PEAK read-out — the CHIRPS read-out is §15.5 here. doc 33 is frozen, so the pointer stands.)* | closed-negative; the r ceiling of [doc 22 §4.7](22_dry_phase_diagnosis.md) stands unmoved |

> ⚠ **Register note, 2026-08-12.** Item 18's closing phrase *"item 20 is now the only lever"* is
> superseded by item 20's own read-out above: that lever was pulled and it failed its volume gate.
> §15.5: *"This closes the CHIRPS question as it currently stands."* **v2 remains the forcing.**
> This register and §15 disagreed for two sessions — §8 said "not attempted" while §15 of the same
> document recorded the rejection. Corrected here, in the register, because §8 is what a reader
> consults for "what is still open".

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

## 11–13 — Gauge and interpolation geometry → [doc 23](23_gauge_geometry.md)

Moved to its own document when this one passed 65 KB. What it establishes, which the open
items above depend on:

| finding | where |
|---|---|
| The IDW was **order-dependent**: shuffling gauge columns moved 52–83 minibacias by up to 20.5 mm/day. Fixed by a lexsort tie-break on (distance, gauge code) and proven by a shuffle test; nb11 now imports the shared `src/idw_forcing.py` and asserts invariance inside the notebook | [doc 23 §11.1](23_gauge_geometry.md), [doc 23 §11.4](23_gauge_geometry.md) |
| Four co-located gauge pairs, classified by what their records do on shared days, not by distance: **2 duplicates + 1 sequential replacement merged** (294 → 291 gauges), **1 refused as a coordinate error** (CATAM, corr 0.756 at 5 cm) and guarded by `NEVER_MERGE` | [doc 23 §11.2](23_gauge_geometry.md), [doc 23 §11.4](23_gauge_geometry.md) |
| The merge moved the areal mean **+0.04 %** and **542 minibacias by a median +5.03 %** — a basin-level check alone would have called it negligible | [doc 23 §11.3](23_gauge_geometry.md) |
| The 14 residual energy-floor gauges: **2 EXCLUDE, 2 KEEP, 10 DOWN-WEIGHT**, rule declared before the numbers. Only 2 of 14 are our forcing; 8 of 14 have no rating curve; where curves exist R² runs 0.36–0.69 | [doc 23 §12](23_gauge_geometry.md) |
| The **rc-reference circularity charge is refuted** — remapped and kept rc spreads are identical (log-SD ratio 1.009, Levene p = 0.76). The pre-authorised regional re-snap is therefore **not justified** | [doc 23 §13.1](23_gauge_geometry.md) |
| **Catchment areas are unreliable per gauge in both implementations**: median ratio 0.991 over 85 shared gauges but 31 of 85 beyond 2×. Any t/km²/yr yield inherits this one-for-one | [doc 23 §13.2](23_gauge_geometry.md) |

---

## 14 — Phase 2 executed: the v2 forcing rebuild

**The first forcing rebuild since the zero-suppression repair.** nb11 and nb12 both executed
cleanly and are verified from their executed outputs, not from exit codes. Everything below is
read out of the notebooks and `model_inputs_v2/manifest.json`.

### 14.1 nb11 — rainfall and PET on the repaired gauge set

| check | result |
|---|---|
| co-located merge | 3 merged (`24010140→2401500040`, `24030590→24035420`, `27015330→27015070`) → **291 gauges**; CATAM correctly refused |
| **order-invariance** | **3 gauge-column shuffles, byte-identical field each time** — asserted *inside* the notebook |
| forcing matrix | 4,018 days × 8,672 minibacias |
| k=6 fallback cells | **41,180** (0.118 %), all filled by the k=20 pass, **0 remaining NaN** |
| area-weighted areal mean, 2009–2017 | **2,036.4 mm/yr** |
| ERA5-Land mosaics | **132 / 132 readable** (see §14.3) |
| radiation | **17.2 MJ/m²/day** — inside the 15–22 band, low end, as a cloudy basin should be |
| PET | **3.41 mm/day**, p1–p99 1.3–5.8 (sanity 3–5) |
| **model period** | **2008-01-01 → 2018-12-31, 4,018 days** |
| gauge-only LOOCV | **daily r median 0.429**, bias +1.7 %, RMSE 10.6 mm/day, 287 gauges |

Two of these are worth more than a row in a table.

**The areal mean reproduces the standalone harness to 0.1 mm/yr.** §10.5 predicted 2,036.4 mm/yr
for 2009–2017 from a separate implementation with a different gauge-column order and the merge
applied outside the notebook; nb11 landed on 2,036.4. The fallback-cell count matched too
(41,180, against 41,504 unmerged). Two independent paths through the interpolation agreeing at
that precision is a real check, not a restatement.

**Open item 3 is closed.** PET now spans the full rainfall record, so the model period is no
longer clipped to 2009–2017 by ERA5. That item had been open for four sessions.

**The LOOCV baseline is banked before the merge exists.** r = 0.429 is the number the CHIRPS
merge must beat, recorded now so the comparison cannot be constructed after the fact. For
scale: [doc 22 §4.7](22_dry_phase_diagnosis.md) measured the model's El Niño anomaly correlation
at 0.476 against a rainfall field whose own leave-one-out skill was ≈0.40.

### 14.2 nb12 — the v2 model-input bundle

Written to `model_inputs_v2/`; **the v1 bundle is untouched**, because H1 isolates the objective
change by re-running the new objective on the old forcing and that is impossible if v1 has been
overwritten.

| check | result |
|---|---|
| period assertion | `DATES.equals(want)` → **True**, 4,018 days |
| precip integrity | NaN 0, negative 0, max 265.4 mm |
| area-weighted areal mean, 2008–2018 | **2,073.1 mm/yr** (§11.3 predicted 2,073.1) |
| basin PET | **1,251.6 mm/yr** — the figure §3's energy floor has used since it was written |
| CALAMAR outlet | 3,992 days, mean Q 7,433.4 m³/s, runoff depth 912.4 mm/yr |
| smoke tests | 11 passed; 48 arrays documented in the manifest |
| triage carried through | EXCLUDE **2** → `cls=excl_energy_floor`; DOWN-WEIGHT **10** → `gauge_weight=0.5`; KEEP **2** at full weight |
| **primary calibration set** | **63 gauges** (56 mapping untouched, 7 re-snapped), 204,955 station-days |
| weights inside the set | 53 at 1.0, 10 at 0.5; triage tally 51 `not_flagged` + 10 + 2 = 63 ✓ |

**The calibration set grew to 63, and the prediction of 59 was wrong.** Every brief and note in
this project had been arithmetic from a fixed pool of 61: 61 − 2 excluded = 59. But extending the
window to 2008–2018 gave gauges that previously failed the `n_window` gates enough record to
qualify, and that gain (+4 net) outweighed the exclusions. **A window change is not a filter on a
fixed population; it changes the population.** The energy-floor criterion in the Phase 3 success
list is stated as "≤ 5 of 61" and now has a different denominator.

`gauge_weight = 0.5` is a **declared convention, not a measurement**, and is *exported rather
than applied* so that notebook 14 can report results with and without it. The manifest says so
in the array's own provenance entry.

### 14.3 Corrections this rebuild forced

Five things were believed and are not true. Four were caught only by executing.

**1. `132/132` was a filename count.** `era5land_ext_2008_M06.nc` was **internally corrupt** —
unreadable with `NetCDF: HDF error` at a perfectly normal 43.69 MB, so neither a name check nor a
size check could see it. Opening all 132 and reading a timestep from each found exactly one bad
file and no suspiciously small ones. Both mosaic sources were intact, so it was rebuilt from
`era5land_basin_2008_M06.nc` + the strip with no CDS download; the corrupt file is quarantined in
`data/raw/climate/_corrupt/`. **`PET_READY = len(ext) >= 132` in nb11 still has this hole** — it
counts names. New open item 17.

**2. `pd.read_csv` silently truncates the wide forcing CSVs.** This is the serious one.
`forcing_minibacia_pet_v2.csv` is 4,018 × 8,673, ~180 MB. One `read_csv` returned **1,309 rows
ending 2011-08-01**; another returned **3,630 rows ending 2017-12-08**. The file is provably
complete: 4,019 lines, every line carrying exactly 8,672 commas, no NUL bytes, the row after each
cut point intact and full width. No exception, no warning, non-deterministic cut point.

The danger is the *shape* of the failure: the truncation is a contiguous **prefix**, so
`len(date_range(min, max)) == len(df)` still held and nb12's own "calendar holes 0" check passed
on it. Duplicate, monotonicity and shape checks would all have passed. The only thing that caught
it was `assert DATES.equals(want)` — an assertion two stages downstream that compares against an
*independently declared* period. Without it this rebuild would have produced a model calibrated on
1,309 of 4,018 days with every diagnostic reporting clean.

Fix: `src/forcing_npy.py` converts once to `.npy`, and the verification deliberately does not
trust the parser that just lied — parsed row count is checked against the **file's own line count
counted from raw bytes**, column count against the header's comma count. nb12 now loads `.npy`
and **refuses to fall back to `read_csv`**, raising with the fix command instead. This also
pre-satisfies Phase 3's memmap requirement.

**3. `np.save` round-trips `datetime64[D]` as `datetime64[s]`, and `DatetimeIndex.equals()` is
resolution-sensitive.** Identical instants at `[s]` and `[ns]` compare unequal, which failed the
model-period assertion for no data reason. Cast to `[ns]` on load. Cheap, but it is the kind of
thing that gets "fixed" by loosening the assertion — which is exactly what would have let
correction 2 through.

**4. The manifest's provenance strings had gone stale and would have misled.** It still read
`"bounded_by": "ERA5-Land PET"` and *"rainfall exists for 2008 but PET does NOT; no 2008 PET was
invented here"*, both now false. And `warmup_available_days` computes to **0** — factually
correct, because the period now starts where the rainfall does, but it reads like a regression.
The spin-up must now come from *inside* the period: **use 2008 as the warm-up year and score
2009–2018.** Both strings were corrected and nb12 re-run so the shipped manifest is accurate.

**5. The 63-vs-59 gauge count** (§14.2).

### 14.4 The process failures, recorded because they cost more than the findings

Seven executions failed before nb11 and nb12 landed. **Five were mine, and they reduce to two
habits**, both of which the project's own conventions already warn about:

* **Changed a domain without enumerating its consumers — three times.** Extracting nb11 §3 into
  `src/idw_forcing.py` dropped four incidental locals (`Gv`, `Gf`, `obs`, `D`) that §6's LOOCV
  read 90 lines away. Adding the `cls` value `excl_energy_floor` broke `CLS_COL`. Adding
  `gauge_weight`/`triage` to `discharge.npz` tripped the manifest's `UNITS` gate. The static sweep
  that finds all of these takes one command and I ran it only after paying for a failure.
* **Verified the wrong artifact.** I added the `UNITS` entries to the *generator*, checked the
  *generator*, and executed the *notebook* — which was stale. CLAUDE.md states the rule verbatim.

Two guards were added rather than just patched around: `set(G.cls) - set(CLS_COL)` must be empty,
so the next new class fails by name instead of as a `KeyError` inside a scatter call; and a
pre-launch check that the **generated notebook** contains the fix, not the generator.

nb12's own `assert k in UNITS, '...refusing to ship it'` deserves credit — it named the exact
array and refused to write an undocumented field into the bundle. The guards in this repo work;
I was the one not reading them.

| 21 | **The day-of-year climatology benchmark is not reproducible from doc 22 §4.1's description** ([doc 26 §6](26_phase3_refit.md)). Rebuilt as a (month,day) mean over the whole scored record it is **harder by +0.051 to +0.117 KGE** than the recorded one, so the primary criterion's absolute targets (+0.12 / +0.24) are not testable like-for-like. Either recover the original construction or restate the criterion in its ratio form | comparing any future run against the pre-registered target |
| 22 | **A constrained ordering relocates the compensation rather than removing it** ([doc 26 §5.1](26_phase3_refit.md)). Imposing `k_int < k_bas` by reparameterisation worked exactly as designed and the search responded by railing `k_sup` above `k_bas` instead. Any further ordering constraint must be justified against this, not asserted | reading H2's parameter set as physically meaningful |

---

## 15 - The CHIRPS-gauge merge: built, validated, and NOT adopted

*(Phase 3 follow-up to s9.4/s9.5 and doc 22 s4.7. Implementation `src/merge_chirps_gauges.py`;
per-gauge scores `data/processed/merge_loocv_report.csv`; run journal
`docs/agents/journal_chirps-merge.md`. No forcing file was written - v2 stands.)*

The merged field was the one intervention measured capable of moving r (doc 22 s4.7). It was
built exactly as nb10's verdict prescribed: CHIRPS quantile-mapped **to the gauge distribution**
per (elevation band x hydrographic zone) stratum - gauges keep control of volume, CHIRPS supplies
structure - lag-aligned by -1 day (nb10's dia-pluviometrico test), blended by
distance-to-nearest-gauge weight (pure gauge IDW under 10 km, pure mapped CHIRPS beyond 30 km,
linear between, matching the G/GC/GC provenance bands), with the 41,180 k=6-silent fallback
minibacia-days taken by mapped CHIRPS. Deterministic; order-invariance asserted by shuffle test.

### 15.1 The two gates, pre-registered before the run

The decision rule, quoted from the task as registered in the run journal before any number
existed: *"ADOPT if merged median r > 0.429 by any margin AND the volume gate holds; otherwise
DO NOT ADOPT"* - the volume gate being an area-weighted basin mean, 2009-2017 window, within 1 %
of the v2 gauge-only 2,036.4 mm/yr. Justification by r, never by volume.

| gate | result |
|---|---|
| baseline self-check | LOOCV protocol reproduced nb11 s6 exactly: **287 gauges, median daily r 0.429** |
| **LOOCV gate** | merged median daily r **0.447** (> 0.429) - **PASSES**. Baseline-mask-only diagnostic 0.449 |
| **VOLUME gate** | merged, area-weighted, **2009-2017: 2,188.5 mm/yr** vs target 2,036.4 +/-1 % - **FAILS (+7.5 %)**. 2008-2018 window: 2,219.2 mm/yr (trap 9: window attached) |
| **decision** | **DO NOT ADOPT.** LOOCV scored on 2008-2018 station-days; both gates were required |

### 15.2 What the LOOCV actually showed

| isolation band | n | r gauge-only | r merged |
|---|---|---|---|
| < 10 km (w_chirps = 0) | 98 | 0.481 | 0.475 |
| 10-30 km (blend) | 169 | 0.426 | **0.449** |
| > 30 km (pure mapped CHIRPS) | 20 | 0.343 | **0.300** |

Per gauge: 149 improved, 51 worsened, 87 unchanged (median per-gauge delta 0.000 - the median
*shift* 0.429 -> 0.447 lives almost entirely in the 10-30 km blend band). Two findings worth
keeping even though the field was rejected:

* **The blend genuinely helps at intermediate isolation** (+0.023 median at 10-30 km): CHIRPS
  errors are partly independent of interpolation errors, so mixing raises correlation there.
* **Pure mapped CHIRPS is WORSE than k=6 IDW even beyond 30 km** (0.300 vs 0.343). The gap-fill
  argument for CHIRPS - highest value where no gauge is in range - is refuted at the gauges we
  can test. CHIRPS point skill (raw r 0.31, nb10) is simply below even long-range IDW here.

### 15.3 Why the volume gate failed by +7.5 % when the map targeted the gauge distribution

The quantile maps were fitted on **paired station-days** - days the gauge reported. s9.3 showed
139 of 294 stations still report rain-selectively after the repair (sparse-band selectivity
1.734). A reporting-day distribution is therefore **wetter than the all-days truth** at those
stations; the map faithfully transferred that wet-conditioned distribution onto CHIRPS, and the
merged field then applied it to *every* day. The gauge-only IDW largely dodges this because a
silent gauge simply drops out of the day's weighted mean, while the mapped CHIRPS carries the
bias everywhere the blend weight is non-zero - concentrated in the sparsely gauged (wet, high)
terrain where w -> 1. The failure is thus the *same* defect s9.3 left open, resurfacing through
a new channel: **finishing the zero-suppression repair on the 139 residual stations is upstream
of any usable CHIRPS merge**, exactly as s9.4 predicted from the volume side.

### 15.4 Consequence

v2 remains the forcing. The r ceiling of doc 22 s4.7 stands unmoved for now; the measured +0.018
median LOOCV gain says a merge *could* buy roughly that much daily skill in the blend band, but
not until its volume can be held - either by conditioning the quantile maps on inferred-complete
records only, or by repairing the remaining rain-selective stations first. A v3 calibration was
never launched (it would need an nb12 rebuild and a new pre-registered cell; recorded as
follow-up in the run journal). A negative result under a pre-registered rule is a finding: the
gate did precisely the job it was registered to do.

> ⚠ **Note added 2026-08-12: of the two routes named above, the first was measured and is a
> no-op.** *"Conditioning the quantile maps on inferred-complete records only"* was registered as
> H-CHIRPS ([doc 33](33_c2b_preregistration.md) §1), run, and found to be **already the code's
> behaviour** — §15.5 below. The second, *"repairing the remaining rain-selective stations
> first"*, is **untested** and lies upstream of the merge. Read §15.5 before quoting this
> paragraph.

### 15.5 C2b.3 - the refit was re-run, both gates re-measured, and the question is closed

*(Registered as H-CHIRPS in [doc 33](33_c2b_preregistration.md) s1, gates carried over from
s15.1 unchanged and NOT re-derived. Implementation `src/merge_chirps_gauges.py`
(`--qmap-inferred-dry`); per-gauge scores `data/processed/merge_loocv_report_v2.csv`; run
journal `docs/agents/journal_chirps-refit.md`. **No forcing file was written - v2 stands.**)*

Doc 33 registered one change, and only one: fit the per-(elevation band x hydrographic zone)
quantile maps on the **repaired** series *including* the `approval == 'Inferido_seco'` days, so
the maps see the true dry-day frequency instead of only the days someone wrote down. Everything
else - stratification, lag, blending weights, gap-fill, determinism - was to stay identical.

**The first thing the refit found is that this was already the code's behaviour.** Measured
before anything was edited: `load_gauges()` reads `precip_gauges_daily_qc_v2.csv` - 926,910 rows,
of which **240,158 are `Inferido_seco` zeros**, and `precip_mm` has zero NaN - and no approval
filter exists anywhere in the path (`grep Inferido_seco src/*.py` returns only the repair script
and `idw_forcing.APPROVAL_RANK`). The pools were built on `obs = ~isnan(Gv)`, so those inferred
zeros were in every pool from the start: **240,115 of 926,268 paired station-days, 25.9 %**. The
fit input is now stated and *asserted* rather than merely true by accident, and the counterfactual
is available behind a flag. The proof that nothing else moved is that the re-run reproduces the
rejected Aug-3 run to the last printed digit, and
`merge_loocv_report_v2.csv` is **bit-identical** to `merge_loocv_report.csv` on every scored
column across all 291 rows (max |diff| 0.000e+00).

| gate | window | result |
|---|---|---|
| baseline self-check | 2008-2018 station-days | 287 gauges, median daily r **0.429** - nb11 s6 reproduced (assert tolerance 6e-4) |
| **LOOCV gate** | 2008-2018 station-days | merged median daily r **0.447** > 0.429 - **PASSES**. Baseline-mask-only 0.449 |
| **VOLUME gate** | **2009-2017**, area-weighted over 8,672 minibacias | **2,188.5 mm/yr** vs the band **[2,016.0, 2,056.8]** - **FAILS (+7.47 %)**. 2008-2018 context 2,219.2 mm/yr |
| **decision** | | **DO NOT ADOPT.** The rule, quoted: *"ADOPT if merged median r > 0.429 by any margin AND the volume gate holds; otherwise DO NOT ADOPT"* - both were required, one failed |

Per gauge, the LOOCV picture is unchanged: 149 improved, 51 worsened, 87 unchanged, median
per-gauge delta +0.0003; the fleet shift lives in the 10-30 km blend band (0.426 -> 0.449, n=169),
while < 10 km loses a little (0.481 -> 0.475, n=98) and > 30 km loses a lot (0.343 -> 0.300, n=20).

**What the counterfactual measured.** Running the fit with the inferred-dry days *removed*
(`--qmap-inferred-dry exclude`, diagnostic only - it writes nothing and takes no decision) drops
the pools from 926,268 to 686,153 pairs and gives, on the same 2009-2017 window,
**2,294.1 mm/yr (+12.65 %)** against the include run's 2,188.5 (+7.47 %). So the repair's inferred
dry days were already removing **105.6 mm/yr, 41.0 % of the surplus** - and the remaining
**+152.1 mm/yr** is what is left *after* that lever has been pulled all the way. Correlation is
indifferent to the choice (0.448 exclude vs 0.447 include), which is the volume/correlation
independence of [doc 26](26_phase3_refit.md) H2 - H1 showing up again in the forcing.

**Where the surplus actually is.** At the 287 LOOCV gauges the merged field is very nearly
unbiased against the gauges themselves: median per-gauge bias **+2.00 %** merged vs **+1.73 %**
gauge-only, per-gauge delta median **+0.00 pts** (108 gauges wetter, 92 drier). A field that is
unbiased where it can be tested and +7.5 % over the basin puts its whole surplus in the terrain
with no gauge to test it - and that is precisely where the blend weight goes to 1. The per-band
bias deltas say the same thing monotonically: **+0.00 pts** below 10 km, **+0.24 pts** at
10-30 km, **+0.89 pts** beyond 30 km.

**Correction to s15.3.** That section attributed the volume failure to maps "fitted on
reporting-day pairs", implying the inferred-dry days were absent. They were not: they were 25.9 %
of the fit input. The half of s15.3 that survives is the other half - the days the repair *never
inferred*, at the 139 stations that still report rain-selectively after it (s9.3). Those cannot be
put into a pool by any change to `merge_chirps_gauges.py`, because they are not in the record at
all. Correcting a diagnosis is worth as much as the measurement that forced it.

**Consequence.** This closes the CHIRPS question as it currently stands. The intervention doc 33
registered has been executed and measured; it was already in force, it is worth 41 % of the
surplus, and it is not enough. **v2 remains the forcing**, the r-ceiling of doc 22 s4.7 is
unmoved, and no route to a passing volume gate exists inside the merge code. The only remaining
route is upstream: repair the 139 residual rain-selective stations so the gauge record itself
carries its true dry-day frequency, exactly as s9.4 and s15.4 both predicted from opposite
directions. Nothing downstream changes - C1 and C2 are model-free and were never gated on this
(doc 31 B1), the H2E drivers stay frozen, and the +0.018 median LOOCV gain remains a measured
but unbankable result.

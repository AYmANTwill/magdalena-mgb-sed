# Presentation outline — MGB-SED Magdalena–Cauca: hydrological calibration

**Audience:** Prof. F. J. Briceño-Zuluaga (UMNG). **Language:** English. **~18 slides, ~30 min.**
**Team of three.** Everything in this deck is *our* work — spoken as "we" throughout. The two
model implementations are two arms of one project, not two people's projects.

**Scope: the deck stops at our attempts to calibrate the hydrological model.** It reports what
we tried, what each attempt measured, and where we now stand. It does **not** claim a finished
calibration, and the sediment phase appears only as outlook.

**The spine.** July's deck answered *"how do you plan to do all this?"* This one answers
*"what did you try, what did it measure, and how do you know?"* Every results slide carries
its measurement. The limits get their own slides rather than footnotes.

---

## A — Framing (3 slides, ~4 min)

### 1. Title
**MGB-SED suspended-sediment modelling of the Magdalena–Cauca basin: an ENSO contrast.**
Team of three · Advisor: Prof. Briceño-Zuluaga · UMNG · August 2026.
One basin map. Method transferred from **Fagundes et al. (2026)**, *Int. Soil Water Conserv.
Res.* 14, 100599 (Guaíba basin, Brazil).

### 2. The question
- Magdalena–Cauca: **257,097 km²**, among the world's highest specific sediment yields.
- Strong ENSO control. Our own anomaly analysis fixes the contrast years:
  **La Niña 2011 (+1.7σ wet)** vs **El Niño 2015–16 (−1σ dry)**.
- The gap: the ENSO–sediment link is documented observationally (Restrepo), never reproduced
  with a **process-based distributed** model across the whole basin.
- **Objective:** reproduce *and explain* the flux difference, with spatial attribution.

### 3. Where we are, honestly
- **Phase A — model inputs: complete.**
- ~~**Phase B — hydrology: calibrated, three attempts, not yet closed.**~~ → **four attempts;
  Phase B is CLOSED on H2E** (see the correction at slide 15). This is the talk.
- ~~**Phase C — sediment: blocked** on mainstem SSC data quality.~~ → **Phase C is ACTIVE**;
  the "blocked" framing is superseded ([docs/30](30_phase_c_plan.md) header: *"It supersedes
  the 'Phase C blocked' line in older docs."*). Its precise form
  ([docs/32](32_ssc_qc_audit.md) §R6): **79/79 stations classified, 18 usable**, and
  *"`21237020` ARRANCAPLUMAS (Magdalena — **the only Magdalena-trunk SSC station in the entire
  network**)"*. *(⚠ Corrected 2026-08-12.)*
- Why in this order: **MUSLE is driven by runoff, not rainfall**, so the discharge model is
  the load-bearing component. Calibrating sediment on an uncalibrated hydrology would fit
  erosion parameters to water-balance error.

---

## B — What we built (4 slides, ~6 min)

### 4. Roadmap
Master flowchart: `DEM → minibacias → URH → soil & vegetation parameters → rainfall + PET
forcing → water balance → routing → discharge → [MUSLE → sediment]`. Dashed arrows =
calibration data. *Reuse the notebook-04 / README diagram.*

### 5. Spatial discretisation
- **8,672 minibacias** (D8 on Copernicus 30 m DEM), outlet at Calamar.
- **24 URH types** = 3 IGAC soil-texture families × 8 hydrological land classes.
- Per-minibacia soil storage from IGAC: median **72.6 mm**, range 13.5–255 mm.
- Verified: outlet upstream area **257,096.93 km²** against a sum of own areas of
  **257,096.93** — two independent accumulators agreeing to **1.8×10⁻⁸ km²**, zero
  area-monotonicity violations.

### 6. **Two implementations — the team's main methodological asset**

| | implementation A | implementation B |
|---|---|---|
| channel routing | Muskingum X = 0 | **local-inertial + floodplain** (Bates 2010) |
| run time | **11.7 s** / 4,018 days | **1,510 s** / trial |
| what it enables | **4,000-evaluation calibration search** | the paper's actual physics, Depresión Momposina |
| calibrated KGE (median) | **0.346 – 0.450** | **0.329** (90 gauges) |

- Deliberate division: **A buys search, B buys physics.** A 774-run search on B would take
  13 days; A does 4,000 evaluations overnight.
- **They agree to within ~0.02 KGE from independent codebases, independent forcing pipelines
  and different routing.** That is a genuine cross-validation, and it is worth more than
  either number alone.
- Speaker note: MGB-SA proper is a QGIS plugin; A is our fast diagnostic engine.

### 7. Model period and the split — *the slide that makes every later number credible*
- **2008-01-01 → 2018-12-31, 4,018 days.** 2008 warms up, **2009–2018 is scored.**
- Warm-up verified: three mutually incompatible initial states converge to within **0.179 %**
  of mean flow.
- **Klemeš (1986) differential split-sample:** we calibrate on **neutral years only**, so
  **both ENSO phases are strictly out-of-sample.** The ENSO contrast is a **prediction**, not
  a fit.
- Overfitting check: cal→val degradation **−0.159**, only **0.011** worse than an unfitted
  model.

---

## C — Four calibration attempts (5 slides, ~9 min)

### 8. What we tried, and what each attempt bought

*Table updated 2026-08-10 (Stage C0) to add attempt 4, the adopted configuration. Sources:
`sim_calibrated_v2/metrics_fleet.csv` VAL-all + CAL rows, `parameters_*.csv`; full report in
[docs/26](26_phase3_refit.md) addendum A.4.*

| attempt | forcing | objective | **VAL KGE** | **recession ratio** | PBIAS % | params at a bound (global / all 18) |
|---|---|---|---|---|---|---|
| **1 — Config B** | original | daily KGE blend | **0.450** | **2.98×** too slow | +6.8 | 3 of 10 / — |
| **2 — H1** | original | + recession term | 0.421 | **0.96×** | +6.4 | 2 of 10 / 2 of 18 |
| **3 — H2** | repaired | + recession term | 0.346 | **1.01×** | +7.3 | 2 of 10 / 3 of 18 |
| **4 — H2E (adopted)** | repaired | + recession term, **FAO-56 ET** | 0.356 | **0.98×** | **+3.5** | 2 of 10 / 3 of 18 |

- DDS, **14,000 evaluations** in total: three pre-registered configurations — H1 and H2 at six
  seeds each, H2E at two ([docs/29](29_seed_expansion.md)) — every cell registered *before*
  running, so none is a post-hoc pick.
- Reference points on the objective scale: prior 0.128, random sampling 0.173, attempt 1 0.243,
  attempt 4 **0.259**.
- **The "params at a bound" column now states both denominators.** One 18-dimensional search
  vector, two ways to count it: attempts 3 and 4 rail two of the ten *global* parameters and
  three of all eighteen *dimensions* (the third is the regional `wm_mult@R2`). Reporting one
  number is what made an earlier version of this slide say "3 of 10" where docs/26 §5 said "2".
- **Attempt 4 bought volume, not skill:** β 1.073 → 1.035 and PBIAS +7.3 → +3.5 %, the best of
  the four, while VAL KGE (+0.011) and r (+0.008) both moved less than the 0.051 between-seed
  spread. It also freed the crop coefficient from its rail (`kc_mult` 1.90 → 1.66), which was
  the pre-registered hypothesis it was built to test.

### 9. **The central result: fixing the physics costs skill**
Attempt 1 reproduced discharge well but with a recession **3× too slow** — we measured
observed recession constants of **9.5–11.9 days** against a simulated **27–45 days**.

Adding a recession-signature term to the objective:

| | attempt 1 | attempt 2 |
|---|---|---|
| recession ratio | 2.98× | **0.96×** — essentially exact |
| VAL KGE | 0.450 | 0.421 |
| **El Niño skill over climatology** | **−0.026** | **+0.026** |

- **We traded 0.029 KGE for a recession that is right, and for the dry phase turning from
  worse-than-climatology to better.**
- Message: a higher KGE bought by a physically wrong recession is not the better model. This
  is the deck's main argument, and it is why we report the ratio alongside the skill.
- **Caveat added 2026-08-10 (Stage C0), and it must be spoken, not skipped:** the dry-phase
  turn above is the attempt 1 → attempt 2 comparison and remains true of it. It does **not**
  survive to the configuration we adopted. El Niño skill-over-climatology reads
  **+0.026 → +0.006 → −0.0005** across attempts 2 → 3 → 4, so attempt 4 sits *at*
  climatology in the dry phase, not above it. La Niña stays at **+0.106**. The honest
  one-liner is therefore "the wet phase is predictable, the dry phase is not" — which is the
  input-ceiling result (slide 12), not a contradiction of it. See
  [docs/26](26_phase3_refit.md) addendum A.5.

### 10. Did repairing the rainfall help? — a controlled test
Attempt 3 changes **only** the forcing, on matched gauges and a matched window:

| H2 − H1 | change |
|---|---|
| **PBIAS** | **8.85 % → 4.41 %  (−4.44 points)** |
| **r (correlation)** | **+0.0033 — essentially zero** |
| KGE | −0.022 |
| gauges with KGE > 0 | **+2** |

- **The repair fixed volume and did not touch correlation.** We predicted this before running
  it, and the number came back +0.003.
- That is not a disappointment — it is the confirmation that **volume error and correlation
  error are independent problems in this basin**, which tells us where to spend effort next.

### 11. The data defects we had to fix first
- **Zero-suppressed gauges.** Stations omit dry days entirely, so mean rainfall scaled with
  how often the observer wrote anything: **4.4 mm/day** at >90 % reporting vs **11.7 mm/day**
  below 50 %. *A 2.9× spread as a function of reporting frequency is not geography.*
- Our detector uses only the **neighbours'** records, so it has a **calibrated null**: 1.001
  on 89 dense stations (unbiased, as required) against **1.777** on the sparse band.
- Repair: **153 stations, 240,158 inferred-dry station-days.** Sparse-band selectivity
  **1.777 → 1.040**, dense band held at **1.001** — the control proving no over-repair.
- Basin areal rainfall **2,174 → 2,036 mm/yr**; energy-floor violations **18 → 14**.
- **The transferable lesson:** test for *absent* records, not just outlier values. An outlier
  screen structurally cannot see a record that was never written.
- **Independent corroboration within the team:** our two pipelines detected the same rainfall
  surplus from opposite directions — actual ET breaking through potential ET (1,659 vs 1,239
  mm/yr) in one, runoff coefficients falling below their energy floor at 18 of 18 failing
  gauges in the other.

### 12. Verification as a first-class activity
Four defects only *executing* the code could reveal:
- **A silently truncating CSV reader.** On a 180 MB, 4,018 × 8,673 table, `pandas` returned
  **1,309** rows on one call and **3,630** on another, from a provably complete file, with
  **no exception**. The cut is a contiguous *prefix*, so length, monotonicity, duplicate and
  calendar-gap checks all pass on it. Only an assertion against an **independently declared
  period** caught it — without which we would have calibrated on 1,309 of 4,018 days with
  every diagnostic green.
- **A non-deterministic interpolator.** Three gauge pairs share exact coordinates, so the
  neighbour set was resolved by *column order*; shuffling it moved up to **83 minibacias by
  20.5 mm/day**. Fixed, and now asserted order-invariant on every run.
- **"132 of 132 files present" was a filename count.** One ERA5 mosaic was internally corrupt
  at a plausible 43.7 MB.
- Two gauges 5 cm apart in the catalogue were **not duplicates** — correlation 0.756 across
  1,470 shared days. A distance-based merge rule would have silently destroyed a real record.

Plus the standing guarantees: **mass-balance residual 1.67×10⁻¹⁷**, and two independent
routing back-ends agreeing to **max |ΔQ| = 0**.

---

## D — The finding (2 slides, ~4 min) — *the scientific contribution*

### 13. The model is at its input's ceiling
Across **all 12 parameter configurations** we tested — baseflow constant 8→100 d, subsurface
5→117 d, celerity 0.22→2.0 m/s, rainfall scaled 0.80→1.00 — El Niño correlation stayed inside
**0.556–0.572**. Once bias and variance are repaired, KGE *is* r.

| | r |
|---|---|
| model, catchment-scale daily anomaly | **0.476** |
| the rainfall field's own leave-one-out skill | **0.429** |
| inter-gauge daily rainfall correlation, 0–25 km | **0.33** |
| the same, 25–50 km | 0.25 |
| **mean gauge spacing** | **~30 km** |

**The model sits just above the point-scale skill of the field driving it.** No parameter set
can exceed that. The ceiling is a property of the **observing network**, not of the model.

### 14. Why that matters beyond this basin
- It converts *"our model underperforms in the dry season"* into a **quantified statement
  about what daily rainfall–runoff modelling can achieve at ~30 km gauge spacing in a tropical
  mountain basin** — transferable to any data-sparse catchment.
- It **reorders our own work**: no further parameter tuning can move the dry phase (remaining
  headroom ≈ +0.02, already located). Only a better rainfall field can.
- It is why attempt 3's r result (+0.003) was expected rather than surprising.

---

## E — Limits and next steps (3 slides, ~5 min)

### 15. What we cannot yet claim — say these before you are asked

> **⚠ UPDATED 2026-08-12 — three of these limits have moved; the rest stand.** Slide 8 of
> this document was updated on 2026-08-10 and this slide was not, which makes it read as
> current when it is not.
> - ~~"The calibration is not closed. **Three** attempts"~~ → **Four attempts, and Phase B is
>   CLOSED** — by decision, not by reaching a target ([docs/30](30_phase_c_plan.md) §1:
>   *"**Phase B closes on the input-ceiling result, with H2E as the adopted
>   configuration.**"*). **The "none meets every criterion" clause survives and must still be
>   said**: [docs/26](26_phase3_refit.md) A.4 — *"Applying §5's nine criteria unchanged,
>   **H2E scores 3/9**… Adoption was on the docs/29 rules, which H2E passed; it was never a
>   claim that the pre-registered adequacy criteria were met."*
> - ~~"Skill over climatology is **+0.126** in La Niña against **+0.026** in El Niño"~~ →
>   those are **attempt 2 (H1)** numbers. In the **adopted** configuration they are
>   **+0.106** and **−0.0005** ([docs/26](26_phase3_refit.md) Addendum A.5). The asymmetry
>   did not merely persist — **the dry phase now sits *at* climatology, not above it.** See
>   the correction box at slide 9.
> - ~~"the crop coefficient **pinned at 2.0**"~~ → **`kc_mult` is off its rail: 1.6625**
>   ([docs/26](26_phase3_refit.md) A.2, *"confirmed off the rail that held H1 at 98.8 % and
>   H2 at 93.3 %"*). This bullet's own prediction — that the ET stress function was the cause
>   — **was tested and confirmed** ([docs/29](29_seed_expansion.md) rule (b)). But it is
>   **still not plausible** (1.662 against the FAO-56 target of ≤ 1.2) and **2 of 10 global /
>   3 of 18 dimensions remain railed** in the adopted fit, so the limit itself stands — with
>   the corrected number, not 2.0.
> - The Moriasi bullet and the catchment-area / yield-embargo bullet are unchanged and still
>   correct.

- **The calibration is not closed.** Three attempts, each measuring something different; none
  meets every criterion we set in advance.
- **Conventional adequacy is not reached.** Moriasi et al. (2007) put satisfactory *daily* NSE
  above 0.50; ours is +0.16 to +0.26. Slide 13 explains why, and we report against a
  day-of-year climatology benchmark instead of raw NSE — a perfect climatology also scores
  NSE −0.062 in the El Niño window, so **NSE is not comparable across windows** with different
  observed variance.
- **The ENSO asymmetry persists.** Skill over climatology is **+0.126** in La Niña against
  **+0.026** in El Niño. We set out to halve that ratio; we have not.
- **Two or three parameters still sit at a bound** in every attempt (the crop coefficient
  pinned at 2.0, beyond any FAO-56 value). The remaining candidate is the ET stress function:
  `ET = ETp·W/Wm` throttles evaporation even in moist soil, and a doubled crop coefficient is
  exactly the compensation that implies.
- **No per-gauge specific yield can be published.** Our two networks' catchment areas disagree
  beyond 2× on **36 % of 85 shared gauges** while their medians agree to 1 % — so neither is
  trustworthy per gauge, and a 2.5× area error is a 2.5× yield error.

### 16. Next steps, in the order the measurements dictate

> **⚠ ALL FIVE ITEMS HAVE OUTCOMES. Recorded 2026-08-12; the list below is the state on the
> delivery date and is preserved as such.** Slides 8 and 9 of this document were
> back-annotated on 2026-08-10 and slides 15–17 were not, which made the un-updated slides
> look current. Outcomes, each against its owning doc:
>
> 1. **CHIRPS merge — DONE, and NEGATIVE. Rejected twice.** ~~"the only lever measured
>    capable of moving r"~~ → it *is* the only measured lever, and **it does not work**.
>    First run ([docs/18](18_hydrology_journal.md) §15): LOOCV **passed** (r 0.447 > 0.429),
>    volume **failed** (2,188.5 mm/yr, +7.5 %, band [2,016.0, 2,056.8]) → *"DO NOT ADOPT"*.
>    The diagnosed fix was then registered as **H-CHIRPS**
>    ([docs/33](33_c2b_preregistration.md) §1), executed, and was a **no-op** — the
>    inferred-dry days were already **25.9 %** of the fit input, the re-run is
>    **bit-identical**, and the gate fails again at **+7.47 %**.
>    [docs/18](18_hydrology_journal.md) §15.5: *"**no route to a passing volume gate exists
>    inside the merge code.**"* [docs/33](33_c2b_preregistration.md) §1: *"the diagnosed
>    cause in docs/18 §15.3 was **wrong**."* **The cause is now UNKNOWN**; the surviving
>    hypothesis (139 residual rain-selective stations) cannot be tested inside the merge.
>    **No v3 forcing exists.**
> 2. **ET stress function — DONE, and it SUCCEEDED.** [docs/29](29_seed_expansion.md) rule
>    (b): *"**H2E (FAO-56 threshold ET): SUCCESS, all three conditions**… the FAO-56
>    threshold form releases it at no cost."* `kc_mult` **1.90 → 1.662**. H2E is the
>    **adopted** configuration ([docs/30](30_phase_c_plan.md) §1).
> 3. **More seeds — DONE, and they did NOT separate.** [docs/29](29_seed_expansion.md) rule
>    (a): *"**H1 vs H2 separability: NOT SEPARATED**… Six seeds per cell did not separate the
>    forcings"* — gap **0.009** against seed spread **0.051**.
> 4. **Catchment areas — still OPEN.** Unchanged; tracked as
>    [docs/31](31_phase_c_workplan.md) background task B3. The yield embargo stands
>    ([docs/23](23_gauge_geometry.md) §13.2).
> 5. **Phase C — STARTED; the "blocked" framing is superseded.**
>    [docs/30](30_phase_c_plan.md) header: *"It supersedes the 'Phase C blocked' line in
>    older docs."* Its precise quantitative form ([docs/32](32_ssc_qc_audit.md) §R6):
>    **79/79 stations classified**, 28 mapped, **18 usable**, and *"`21237020` ARRANCAPLUMAS
>    (Magdalena — **the only Magdalena-trunk SSC station in the entire network**)"* —
>    *"This is the quantitative form of 'Phase C is blocked on mainstem SSC'."*

1. **Merge satellite rainfall (CHIRPS) with the repaired gauges** — the only lever measured
   capable of moving r, and therefore the dry phase. Volume stays gauge-controlled; the
   satellite supplies spatial structure and fills the ungauged 17 % (nearest gauge median
   16.3 km, max 71.5 km).
2. **Replace the ET stress function** with the FAO-56 threshold form — a one-function change
   that should release the crop coefficient from its bound.
3. **Add search seeds** until the two forcing versions separate: attempt 3 leads attempt 2 by
   0.011 on the objective while its own between-seed spread is 0.019, so that comparison is
   not yet established.
4. **Resolve catchment areas** against a source external to both our networks — blocks all
   specific-yield reporting.
5. **Phase C sediment**, once mainstem SSC quality is settled.

### 17. The question we need your guidance on

> **⚠ OUTCOME, recorded 2026-08-12 — ASKED AND DECLINED. This slide is now history, not a
> live question.** [docs/30](30_phase_c_plan.md) cites *this slide by name* as the question
> it answers; the citation was one-way and the outcome had never travelled back here. Owner
> [docs/30](30_phase_c_plan.md), header, quoted:
>
> > "**The advisor was asked the Phase B scope question (docs/24 item 17) and declined to
> > answer — told the team to decide.** This document records the decision and the plan that
> > follows from it."
>
> **The team then took the "yes" branch below**, [docs/30](30_phase_c_plan.md) §1: *"**Phase
> B closes on the input-ceiling result, with H2E as the adopted configuration.**"* The
> "if it does not, the merge must succeed" branch was therefore never entered — **and it is
> as well, because the merge did not succeed**: rejected twice, the second time *with* the
> diagnosed fix applied, which proved to be a no-op ([docs/18](18_hydrology_journal.md)
> §15.5 — see the correction at slide 16 item 1).

**Is the input-ceiling result (slide 13) an acceptable closing statement for the hydrological
phase?**

- If **yes**, the phase can close on a quantified limit, whether or not the rainfall merge
  succeeds.
- If **no** — if conventional adequacy is expected — then the merge must succeed, and if it
  does not we would need either denser rainfall input than IDEAM provides, or a reduced target
  (monthly instead of daily, or sub-basins instead of the full network).

This changes what "done" means for Phase B, so it is the most useful thing we can settle today.

---

## F — Close (1 slide)

### 18. What we have contributed
- **First MGB-SED transposition to the Magdalena–Cauca**, in **two independent
  implementations** that agree to ~0.02 KGE — one fast enough to calibrate, one carrying the
  paper's floodplain physics.
- A **mass-conservative, reproducible** engine (residual 1.67×10⁻¹⁷, 11.7 s per basin-decade)
  with **both ENSO phases held out of calibration**.
- A **quantified input ceiling** for daily rainfall–runoff modelling at this gauge density —
  the result most likely to transfer beyond this basin.
- A **QC methodology for IDEAM station data**, including a defect class — omitted dry days —
  that value-based screening cannot detect by construction.
- A full audit trail: ~300 KB of technical documentation, a register of refuted hypotheses,
  and a traps reference.

---

## G — Phase C: the sediment result (added 2026-08-13) — *the study's headline, and it succeeds*

> Deliver these **after Slide 14** (the input ceiling), as the payoff. They answer the Phase C
> question Slides 17–18 used to pose as open: **the sediment work is now done.** No slide here
> carries t/km²/yr (docs/23 §13.2 yield embargo) — sediment results are ratios or basin-internal
> fluxes only.

### G1. From water to sediment — the ENSO question made physical
- We drove a MUSLE erosion model with the calibrated runoff (Phase B, at its r ≈ 0.57 ceiling) and
  the topographic factor **re-derived to the published source method** (`f_LS` = 0.25146; ACT 2
  moved the engine default to that field).
- One question: does the El Niño / La Niña swing change suspended-sediment transport, and by how much?
- Basin gross hillslope erosion at reference parameters: **299.5 Mt/yr** (always quoted with its
  convention *and* `cp_revision`; **never** a yield).

### G2. The sediment calibration rails — and that is a finding, not a failure

| measurement | value |
|---|---|
| best in-box median KGE_ln, estimator (a) | **−0.118**, railed at the α floor |
| robustness, estimator (b) | **+0.139** (same sign ⇒ **not** indeterminate) |
| α the data wants (unconstrained) | **≈ 0.48** — below the plausible floor |
| no-skill line (mean predictor) | **1 − √2 = −0.414** |

- The erosion equation multiplies **seven** constants the network cannot separate (design-matrix
  condition number **= ∞**); only the product Π is identifiable. A fitted α would **hide** errors,
  not find them — so we report the absolute level as **unresolved, with a stated reason.**
- Two independent implementations reach this by different routes (docs/59). Figure: `gen_kge_rail.png`.

### G3. The ENSO contrast — the model reproduces it (18 of 18) — *the success*

| | direction | median ratio |
|---|---|---|
| observed (model-free) | **22/22** La Niña > El Niño | ~3–5× (est. **b** 2.84–2.95; est. a 4.62) |
| **modelled (this study)** | **18/18** | **3.05×** (robust across β and both window pairs) |

- It works **because** the wet/dry ratio cancels α and the LS level *exactly* — so the result is
  immune to the C4.3 railing. Strictly out-of-sample; CAL window neutral at its core (2013), with a
  stated edge caveat (weak La Niña early 2012, El Niño onset late 2014; NOAA ONI, retrieved 08-13).
- **This is the scientific contribution:** the contrast is reproduced even though the absolute level
  is not identifiable. Reference estimator is **(b)**; both observed values shown. Figure: `gen_enso_contrast.png`.

### G4. The limits, quantified — not hand-waved
- **Gauges:** only ~18 have paired sediment + discharge; the 46 sediment-only sites have no discharge
  record at all (B5), so the flux set **cannot grow** — a physical limit of the network.
- **The ceiling holds:** the one surviving rainfall lever was bounded at **≤ +0.006 r**; the r ≈ 0.57
  ceiling is structural, not a processing gap. Figure: `gen_ceiling_bound.png`.
- The conclusion rests on **three converging independent lines** (observed flux 22/22, observed
  concentration, modelled 18/18), not on gauge count.

**Figures added (`figures/deck/`):** `gen_enso_contrast.png`, `gen_kge_rail.png`, `gen_kge_vs_r.png`,
`gen_ceiling_bound.png` — all on the adopted V4_dg configuration.

---

## Speaking notes

- **Lead with slide 7 (the Klemeš split).** "Both ENSO phases are out-of-sample" is what makes
  every later number credible. Without it the deck is just curve-fitting.
- **Slide 9 is the argument.** Do not present the KGE drop as a setback. Present it as a
  deliberate trade: a recession that is right, and ~~a dry phase that beats climatology for the
  first time.~~
  → ⚠ **CORRECTED 2026-08-12 — do not say "beats climatology" of the adopted model.** Slide 9
  already carries this correction (2026-08-10) but this speaking note did not, and a presenter
  reading the notes would say the superseded sentence aloud. The trade is real and stays; the
  dry-phase claim is true only of **attempt 1 → attempt 2**. Owner
  [docs/26](26_phase3_refit.md) Addendum A.5: *"**The dry phase in the adopted configuration
  is at climatology, not above it: −0.0005.**"* **Say instead:** "a recession that is right,
  and a dry phase that stops being *worse* than climatology" — and then give slide 9's caveat.
- **Show slide 8 and slide 13 close together.** Otherwise the first question is "why is KGE
  only 0.4?", and the answer is a measured ceiling rather than an excuse.
- **Use "we" for both implementations.** They are two arms of one project, and their agreement
  is a result.
- **Have the refuted-hypotheses register ready.** If the advisor proposes a cause for the dry
  phase, there is a good chance we have already measured and eliminated it — three standing
  hypotheses were refuted, one of them backwards. That is the strongest impression available.
- ~~**End on slide 17, not slide 18.** Asking the scope question is more valuable than a summary.~~
  → ⚠ **SUPERSEDED 2026-08-12 — the scope question was asked and the advisor declined to
  answer it** ([docs/30](30_phase_c_plan.md) header). Re-asking it wastes the meeting. See the
  outcome box at slide 17 for what is live instead.

## Figures to pull

| slide | figure | source |
|---|---|---|
| 4 | pipeline flowchart | notebook 04 / README |
| 5 | minibacia + URH map | notebooks 07, 08 |
| 8 | the three attempts, KGE vs recession ratio (2-axis bar) | `sim_calibrated_v2/metrics_fleet.csv` |
| 9 | observed vs simulated recession limbs, before/after | `sim_calibrated_v2/recession_validation.csv` |
| 10 | H2 − H1 by metric (signed bars) | `sim_calibrated_v2/h2_minus_h1.csv` |
| 11 | rainfall vs reporting density, before/after repair | docs/18 §9.1, §10.3 |
| 13 | inter-gauge correlation vs separation distance | docs/22 §4.7 |
| 15 | catchment-area scatter, both networks, log–log | docs/23 §13.2 |

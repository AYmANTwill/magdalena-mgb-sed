# Presentation outline — MGB-SED / Magdalena (hydrology phase)

**Audience:** Prof. F. J. Briceño-Zuluaga (UMNG). **Language:** English. **~18 slides.**
**Supersedes `docs/14_presentation_plan.md`**, which was written in July and describes data
collection as the current frontier. It is now four phases out of date.

**The spine of this deck.** July's deck had to answer *"how do you plan to do all this?"*
This one answers *"what did you find, and how do you know it is true?"* Every results slide
carries the measurement that supports it, and the honest limits are on their own slides
rather than buried.

`[+COLLEAGUE]` marks the slots for Youssef's repo when it arrives.

---

## A — Framing (3 slides, ~4 min)

### 1. Title
MGB-SED suspended-sediment modelling of the Magdalena–Cauca basin: an ENSO contrast.
Authors (you + Youssef) · Advisor: Briceño-Zuluaga · UMNG · date.
One basin map. Method transferred from **Fagundes et al. (2026)**, *Int. Soil Water
Conserv. Res.* 14, 100599 (Guaíba basin, Brazil).

### 2. The question
- Magdalena: **257,097 km²**, one of the world's highest specific sediment yields.
- ENSO drives strong interannual variability: **La Niña 2011 (+1.7σ wet)** vs
  **El Niño 2015–16 (−1σ dry)** — year choice taken from our own anomaly analysis, not
  from the literature.
- The gap: the ENSO–sediment link is documented observationally (Restrepo), never
  reproduced with a **process-based distributed** model over the whole basin.
- **Objective:** reproduce and *explain* the flux difference, with spatial attribution.

### 3. What this talk covers
- **Phase A** model inputs — complete.
- **Phase B** hydrology and discharge calibration — the body of this talk.
- **Phase C** sediment — blocked on mainstem SSC data quality; outlook only.
- Rationale in one line: **hydrology must be calibrated before sediment**, and MUSLE is
  driven by *runoff*, not rainfall — so the discharge model is the load-bearing component.

---

## B — What was built (4 slides, ~6 min)

### 4. Roadmap
One master flowchart: `DEM → minibacias → URH → soil/veg parameters → rainfall + PET
forcing → water balance → routing → discharge → [MUSLE → sediment]`.
Dashed arrows = calibration data. This is the map for the rest of the talk.
*Reuse the notebook-04 / README diagram.*

### 5. Spatial discretisation
- **8,672 minibacias** (D8 on Copernicus 30 m DEM), outlet at Calamar.
- **24 URH types** = 3 IGAC soil-texture families × 8 hydrological land classes.
- Per-minibacia soil storage `Wm` from IGAC: median **72.6 mm**, range 13.5–255 mm.
- Verification: outlet upstream area **257,096.93 km²** against a sum-of-own-areas of
  **257,096.93** — two independent accumulators agreeing to **1.8e-8 km²**, zero
  area-monotonicity violations.

### 6. The engine
- MGB-IPH water balance: ARNO saturation-excess runoff `Asat/A = 1−(1−W/Wm)^b`, three
  linear reservoirs (surface / subsurface / groundwater), Muskingum X=0 channel routing.
- Python implementation, vectorised + numba: **full 4,018-day basin run in 11.7 s**.
- **Mass-balance residual 1.67e-17** relative; the clip never fires.
- **numpy vs numba routers: max |ΔQ| exactly 0.** Chunked vs single-shot: 0.
  Single-day restart: 0.
- Speaker note: MGB-SA proper is a QGIS plugin. This engine is the *diagnostic* that makes
  calibration affordable — 11.7 s per run against 1,510 s for a full hydrodynamic run.

### 7. Model period and the split
- **2008-01-01 → 2018-12-31, 4,018 days.** 2008 warms up, **2009–2018 is scored**.
- Warm-up verified: three mutually incompatible initial states converge to within
  **0.179 %** of mean flow.
- **Klemeš (1986) differential split-sample:** calibrate on *neutral* years only, so
  **both ENSO phases are strictly out-of-sample**. The ENSO contrast is therefore a
  **prediction**, not a fit. This is the single most important design decision in the deck.

---

## C — Results (5 slides, ~8 min)

### 8. Calibration skill
Table — validation, median over the calibration-safe gauge set:

| | KGE | NSE | PBIAS |
|---|---|---|---|
| uncalibrated | 0.227 | −0.39 | +46.1 % |
| **calibrated** | **0.450** | **+0.256** | **+6.8 %** |

- DDS search, **4,000 evaluations** across two pre-registered configurations × two seeds.
- Independent consistency check: two unrelated routes to the basin runoff coefficient
  agree — **0.440** from the water balance against **0.435** from the gauge fleet.
- Speaker note: quote Fagundes' *sediment* KGE range of **−0.26 to 0.44** for scale — but
  say plainly that ours is a *discharge* number and the two are not comparable.

### 9. Report against a benchmark, not raw NSE
The dry phase looked catastrophic (NSE −0.078) until we scored a fixed benchmark:

| period | model KGE | climatology KGE | **model − clim** |
|---|---|---|---|
| La Niña 2011 | 0.399 | 0.162 | **+0.236** |
| El Niño 2015–16 | 0.193 | 0.168 | **+0.024** |

- A perfect day-of-year climatology *also* scores **NSE −0.062** in the El Niño window,
  because that window has the record's highest observed CV (0.799).
- **NSE is not comparable across windows with different observed variance.** About a third
  of the apparent failure was the metric.
- The defensible statement is the last column: **+0.024 against +0.236 — a real and large
  asymmetry, but not "worse than the mean".**

### 10. Diagnosing the dry phase: three hypotheses, all refuted
Rebuilt the calibrated parameters in memory and re-ran the engine **30 times**, one factor
at a time — the harness reproduced the stored discharge to **9.1e-9** before it was allowed
to interpret anything.

| hypothesis | verdict | measurement |
|---|---|---|
| gauges under-report in the dry season | **backwards** | 18 of 18 failing gauges have observed runoff coefficient *below* its floor — the forcing is too **wet**, not the gauges too dry |
| baseflow constant needs regionalising | refuted | buys **+0.021** KGE against a 0.206 gap; the *level* is wrong by 3.5×, not the regionalisation |
| rainfall wet-day inflation bites hardest when dry | refuted | **+18.9 / +17.7 / +18.9** points in La Niña / El Niño / neutral — period-invariant |

Message for the advisor: **each one looked right before it was measured, and each was
recorded as refuted.** The repo carries a standing register of refuted claims.

### 11. Data defects found — and why value screens cannot see them
- **Zero-suppressed gauges:** stations omit dry days entirely, so mean rainfall scaled with
  how often the observer wrote anything down — **4.4 mm/day** at >90 % reporting vs
  **11.7 mm/day** below 50 %. *"A 2.9× spread as a function of reporting frequency is not
  geography."*
- The detector that worked uses only the **neighbours'** data, so it has a calibrated null:
  **1.001** on 89 dense stations (unbiased, as required), **1.777** on the sparse band.
- Repair: **153 stations, 240,158 inferred-dry station-days.** Sparse-band selectivity
  **1.777 → 1.040** with the dense band held at **1.001** — the control that proves no
  over-repair.
- Basin areal rainfall **2,174.3 → 2,036.4 mm/yr**; energy-floor failures **18 → 14**.
- **The transferable lesson:** test for *absent* records, not just outlier values. An
  outlier screen structurally cannot see a record that was never written.

### 12. Verification as a first-class activity
Four defects that only executing the code could reveal — good for the "how do you know"
question:
- **A silently truncating CSV reader.** On a 180 MB, 4,018 × 8,673 table, `pandas` returned
  **1,309** rows on one call and **3,630** on another, from a provably complete file, with
  **no exception**. The cut is a contiguous *prefix*, so length, monotonicity, duplicate and
  calendar-gap checks all pass on it. **Only an assertion against an independently declared
  period caught it** — without which this work would have calibrated on 1,309 of 4,018 days
  with every diagnostic green.
- **A non-deterministic interpolator.** Three gauge pairs share exact coordinates, so the
  neighbour set was resolved by *column order* — shuffling it moved up to **83 minibacias
  by 20.5 mm/day**. Now fixed and asserted order-invariant.
- **"132 of 132 files present" was a filename count.** One ERA5 mosaic was internally
  corrupt at a perfectly plausible 43.7 MB.
- Two gauges 5 cm apart in the catalogue were **not duplicates** — correlation 0.756 across
  1,470 shared days. A distance-based merge rule would have destroyed a real record.

---

## D — The finding (2 slides, ~4 min) — *this is the scientific contribution*

### 13. The model is at its input's ceiling
Across **all 12 parameter configurations** tested — baseflow constant 8→100 d, subsurface
5→117 d, celerity 0.22→2.0 m/s, rainfall scaled 0.80→1.00 — El Niño correlation stayed
inside **0.556–0.572**. Once bias and variance are repaired, KGE *is* r.

| | r |
|---|---|
| model, catchment-scale daily anomaly | **0.476** |
| rainfall field's own leave-one-out skill | **0.40** |
| inter-gauge daily rainfall correlation, 0–25 km | **0.33** |
| the same, 25–50 km | 0.25 |
| **mean gauge spacing** | **~30 km** |

**The model sits just above the point-scale skill of the field driving it.** No parameter
set can exceed that. The ceiling is a property of the *observing network*, not the model.

### 14. Why that matters beyond this basin
- It converts "our model underperforms in the dry phase" into a **quantified statement
  about what daily rainfall–runoff modelling can achieve at 30 km gauge spacing in a
  tropical mountain basin.** That is transferable to any data-sparse basin.
- It also **reorders the work**: no further parameter tuning can move the dry phase
  (remaining headroom ≈ +0.02, already located). Only a better rainfall field can.
- Independent corroboration `[+COLLEAGUE]`: two codebases and two forcing pipelines reached
  the same rainfall surplus from **opposite directions** — his actual ET (1,659 mm/yr)
  breaking through potential ET (1,239), our runoff coefficients falling below their energy
  floor at 18 of 18 failing gauges. Neither of us could have established that alone.

---

## E — Limits and plan (3 slides, ~5 min)

### 15. What we cannot yet claim — state these before you are asked
- **Conventional adequacy is not reached.** Moriasi et al. (2007) put satisfactory daily
  NSE above 0.50; ours is +0.256. The ceiling above explains why, and we report against a
  climatology benchmark instead.
- **Half the scientific target is unmet:** +0.024 vs +0.236 KGE over climatology.
- **No floodplain physics.** Channel routing is Muskingum X=0, so the Depresión Momposina's
  storage and backwater are absent. The fitted celerity of **0.221 m/s** is a
  floodplain-storage *surrogate* and must not be read as a physical velocity.
- **Three parameters are at their bounds** in the adopted set (crop coefficient railed at
  2.0, beyond any FAO-56 value), and the simulated recession is **3.5× too slow**. Both are
  now targeted by a revised objective.
- **No per-gauge sediment yield can be published.** Our catchment areas and Youssef's
  disagree beyond 2× on **36 % of 85 shared gauges**, while their medians agree to 1 % — so
  neither network is trustworthy per gauge, and a 2.5× area error is a 2.5× yield error.

### 16. Work plan
1. **Merge satellite rainfall (CHIRPS) with the repaired gauges** — the only lever measured
   capable of moving r, and therefore the dry phase. Volume stays gauge-controlled;
   CHIRPS supplies spatial structure and fills the ungauged 17 %.
2. **Refit with a recession-signature objective** — the recession constant is invisible to
   daily KGE (Morris sensitivity 0.044, rank 5 of 10), so it was set by the prior rather
   than by the data.
3. **Resolve catchment areas against a source external to both networks** — blocks all
   specific-yield reporting.
4. **Phase C sediment**, once mainstem SSC quality is settled.
5. Advisor decisions needed: ENSO window definition (2011 vs 2010–2012); whether the
   Momposina warrants hydrodynamic routing; whether event-tuned erosion triggers suit a
   *climatological* study.

### 17. Division of labour `[+COLLEAGUE]`
Honest framing, and it is a strength rather than a redundancy:
- **This work:** verified forcing, a calibratable engine, the calibration itself, and the
  input-ceiling result.
- **Youssef:** local-inertial routing with floodplain storage (the paper's actual physics),
  the MUSLE sediment module, remote-sensing SSC retrieval.
- **The trade-off is real and measured:** he has the better physics and cannot afford to
  calibrate it (1,510 s per trial → a 774-run search would take 13 days); we can calibrate
  but omit floodplain processes.
- Each implementation found defects in the other's. *Fill in specifics once the repo arrives.*

---

## F — Close (1 slide)

### 18. Contribution
- First MGB-SED transposition to the Magdalena–Cauca.
- A **calibrated, mass-conservative, reproducible** hydrological engine (residual 1.67e-17,
  run time 11.7 s) with both ENSO phases held out of calibration.
- A **quantified input ceiling** for daily rainfall–runoff modelling at this gauge density —
  the result most likely to transfer.
- A documented QC methodology for IDEAM station data, including a defect class (omitted dry
  days) that value-based screening cannot detect.
- Full audit trail: ~250 KB of technical documentation, a register of refuted claims, and a
  traps reference.

---

## Speaking notes

- **Lead with the split, not the skill number.** "Both ENSO phases are out-of-sample" is
  what makes every later number credible.
- **When you show KGE 0.450, immediately show slide 13.** Otherwise the first question is
  "why so low", and the answer is a measured ceiling, not an excuse.
- **Do not oversell the sediment phase.** It is blocked, and the area disagreement means
  even the hydrology cannot yet support per-gauge yields.
- **Have the refuted-hypotheses table ready.** If the advisor proposes a cause for the dry
  phase, there is a good chance it has already been measured and eliminated — that is the
  strongest impression this deck can leave.

## Figures to pull

| slide | figure | source |
|---|---|---|
| 4 | pipeline flowchart | notebook 04 / README |
| 5 | minibacia + URH map | notebook 07 / 08 |
| 8 | observed vs simulated hydrograph, 2–3 gauges | `sim_calibrated/` |
| 9 | KGE by period, model vs climatology (bar pairs) | docs/22 §4.1 |
| 11 | rainfall vs reporting-density (3 bars, before/after) | docs/18 §9.1, §10.3 |
| 13 | inter-gauge correlation vs separation distance | docs/22 §4.7 |
| 15 | gauge-area scatter, ours vs colleague, log–log | docs/23 §13.2 |

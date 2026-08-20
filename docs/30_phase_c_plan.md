# 30 — Phase C plan: sediment, and the decision that unblocks it

Written 2026-08-10. **The advisor was asked the Phase B scope question (docs/24 item 17)
and declined to answer — told the team to decide.** This document records the decision and
the plan that follows from it. It supersedes the "Phase C blocked" line in older docs.

---

## 1 — The decision (ours, recorded so it is auditable)

**Phase B closes on the input-ceiling result, with H2E as the adopted configuration.**

Grounds, all measured:
- Parameter headroom is exhausted: twelve configurations moved El Niño r by < 0.016
  (docs/22 §4.7); the remaining ≈ +0.02 KGE is located and not worth further sessions.
- The ceiling is a property of the observing network (field LOOCV skill 0.429; model
  anomaly r 0.476; inter-gauge daily correlation 0.33 at 0–25 km vs ~30 km spacing).
  That is a quantified, transferable closing statement — publishable as-is.
- The seed expansion (docs/29) settled the two open calibration questions: the forcing
  repair is not separable from search noise at this budget, and **H2E (FAO-56 ET,
  θ_crit 0.6) succeeded** on every pre-registered condition. ~~There is no further
  calibration question whose answer would change Phase C's inputs.~~ → **This last sentence
  was wrong as a prediction and right only as an outcome (correction below).**

  > **⚠ CORRECTION, 2026-08-12.** There *was* a further calibration question, and it was asked
  > four days later: `docs/33` (C2b) measured the two drivers MUSLE actually consumes and found
  > **H-PEAK REFUTED** (`R_AMS` **0.820**, `R_Q1` **0.847**, both below the registered
  > [0.85, 1.15]; `docs/33` §7.1). That triggered the registered `H2E-S` refit, which **would
  > have changed Phase C's inputs** had it succeeded — `docs/33` §5.1 budgets exactly that cost
  > ("everything downstream of C0 that has already run must be re-run against the new drivers").
  > It did not succeed: `docs/33` §8 records **1 of 3 conditions passed** (signature came in at
  > R_AMS 0.94–1.00; F fell 0.0319, 1.6× the registered budget; two new rails), verdict *"the
  > signature and the objective are in conflict… **No further refit.**"* So H2E survived, the
  > inputs did not move, and the conclusion above holds — **but on a measurement this bullet did
  > not have, not on the absence of a question.**
- The one lever that measurably moves r — the CHIRPS merge (LOOCV r 0.447 vs 0.429,
  docs/18 §15) — ~~failed only its volume gate, with the fix identified. It continues as
  **bounded background work** (§5), not as a gate on Phase C.~~ → **failed its volume gate.
  It stayed non-gating on Phase C, which is the only part of this bullet still true; the
  "fix identified" clause is STRUCK, and the background item that carried it (§5 item 1) is
  now CLOSED and NEGATIVE.**

  > **⚠ CORRECTION, 2026-08-12 — *"with the fix identified"* is FALSE and is struck.** The
  > fix was registered as **H-CHIRPS** (`docs/33` §1, frozen 2026-08-10), executed, and
  > measured. It is a **no-op**. `docs/33` owns the hypothesis; quoted verbatim:
  >
  > > "**[resolved 2026-08-10 — see §7]** H-CHIRPS is **REFUTED by its own volume gate**
  > > (2,188.5 mm/yr against the required [2,016.0, 2,056.8]). The registered intervention
  > > turned out to be a **no-op**: the quantile maps already included the inferred-dry days,
  > > so the diagnosed cause in docs/18 §15.3 was wrong."
  >
  > *(`docs/33` §1's pointer *"see §7"* mis-fires: §7 of `docs/33` is the H-PEAK read-out. The
  > H-CHIRPS read-out is `docs/18` **§15.5**, which owns the merge. `docs/33` is frozen and is
  > not edited here.)*
  >
  > `docs/18` §15.5 measured it: the inferred-dry days were **25.9 %** of the fit input all
  > along, so the re-run is **bit-identical** to the rejected run (`merge_loocv_report_v2.csv`
  > vs `merge_loocv_report.csv`, max |diff| **0.000e+00**) and the volume gate fails again at
  > **2,188.5 mm/yr, +7.47 %**. Its correction, quoted:
  >
  > > "**Correction to s15.3.** That section attributed the volume failure to maps 'fitted on
  > > reporting-day pairs', implying the inferred-dry days were absent. They were not: they
  > > were 25.9 % of the fit input. The half of s15.3 that survives is the other half — the
  > > days the repair *never inferred*, at the 139 stations that still report rain-selectively
  > > after it (s9.3). Those cannot be put into a pool by any change to
  > > `merge_chirps_gauges.py`, because they are not in the record at all."
  >
  > **There is therefore no fix waiting to be applied.** `docs/18` §15.5's own consequence
  > sentence: *"no route to a passing volume gate exists inside the merge code."* What the
  > diagnosis is now — stated at the owning doc's own confidence, not upgraded here: the
  > *tested* half of the cause is **refuted**; the *surviving* half (the 139 residual
  > rain-selective stations) is a **hypothesis that cannot be tested inside the merge** and has
  > not been tested anywhere else; and the one thing that was positively **measured** is where
  > the surplus sits — the merged field is near-unbiased at the 287 LOOCV gauges (+2.00 % vs
  > gauge-only +1.73 %) and puts its whole surplus in the ungauged terrain, where the blend
  > weight goes to 1. Repairing those 139 stations is an upstream, unscoped piece of work, not
  > this item.
  >
  > **And there is no v3.** See `docs/00_INDEX.md` §"Forcing versions — v1 / v2 / v3, stated
  > once". Live status agrees: `progress_map.html` carries *"B1 CHIRPS refit — CLOSED:
  > rejected twice, second time WITH the diagnosed fix applied."*

What closing means concretely: the hydrology is *frozen* for sediment work at the best
H2E parameter set. Any future forcing change (CHIRPS v3) re-opens it only through a new
pre-registration.

> **⚠ AMENDED by `docs/33` §5.1 (2026-08-10), recorded here 2026-08-12.** `docs/33` is the
> first pre-registered re-opening, and it amends the sentence above in the owning doc's own
> words: *"the hydrology is frozen except through a pre-registered re-opening, of which **this
> document is the first**. The re-opening C2b claims is on the **objective** (a signature
> term), not on the **forcing** — a case docs/30 §1 named only by its forcing example. The
> forcing route stays exactly as written."* So the freeze rule is unchanged in substance and
> wider in scope than written here: **any** re-opening, forcing or objective, needs its own
> pre-registration.
>
> **And Phase B has since closed a second time, on a different ground.** This §1 closes it on
> exhausted parameter headroom. `docs/33` §8 closes it again on a **measured conflict** —
> H-BFI held, H-PEAK was refuted, and the refit that would have fixed the peaks cost more than
> its registered budget and put `kc_mult` back on the rail H2E had just released it from.
> `docs/33` §8, quoted: *"Not on exhausted headroom, and not on a clean validation either — on
> a **measured conflict**."* Both closures stand; H2E remains the adopted configuration; the
> peak deficit travels forward as a named caveat rather than an open lever (§2, and `docs/36`).

**Second recorded decision — the ENSO pairing (docs/19 §5.2 item 1).** docs/19 requires this
be *taken explicitly, not inherited*. **Decision: keep 2011 (La Niña) vs 2015–16 (El Niño).**
Ground, and it is a hard constraint not a preference: the v2 forcing is bounded by ERA5 P∩PET
and the gauge network to **2008–2018** (CLAUDE.md), so the alternative docs/19 §3.8 favours —
1997-98 vs 1999-2000 (10 bridging stations, mainstem anchors on both sides) — **cannot be run at
all** without re-acquiring forcing that predates our data, which is out of scope. Costs accepted
and named: 2011-vs-2015-16 is the *weakest* of the four candidate pairings (docs/19 §3.8) — 6
bridging stations, no El Niño-side mainstem anchor (docs/19 §3.9b). The C2.1 sensitivity windows
bracket the window-*boundary* question but do NOT substitute for this pairing decision.

---

## 2 — What Phase C already has (more than "blocked" implied)

| asset | state |
|---|---|
| SSC observations | `sediment_daily.csv` — 269,337 rows, 1979–2018, with `flag_corrupt/zero/flatline` already computed |
| SSC inventory | 79 stations, but only **28 mapped to minibacias / 24 calibration-safe**; 46 have no coordinates (`sediment_inventory.csv`, measured). `calibration_safe` flag exists (geometry-only — see gap below). Mapping the 46 needs the docs/19 §5.2-item-2 coordinate fetch (docs/31 C1.0) |
| MUSLE soil erodibility K | per-minibacia in `minibacia_soil_params.csv:K` (nb09: Wischmeier class × IGAC drainage) |
| C factor / land cover | 8 hydrological classes from WorldCover (nb05/08) |
| Runoff driver | calibrated H2E hydrology, recession-correct (ratio 1.08–1.11), mass-conservative — ⚠ **and peak-deficient: see the correction under this table** |
| Rating-curve pairs | docs/13; median R² ≈ 0.5 — usable with stated uncertainty |
| Team's second implementation | `musle.py`, `sediment.py`, RS-SSC retrieval — **external, not in this repo** (docs/20:43); must be acquired for the C3.5 cross-check, as in Phase B |

> **⚠ CORRECTION to the "Runoff driver" row, 2026-08-12 — it is missing the deficit that was
> measured after this table was written.** `docs/33` §7–§8 owns it: fleet-median **`R_AMS`
> 0.820** (annual maxima ~18 % low) and **`R_Q1` 0.847**, both outside the registered
> [0.85, 1.15] ⇒ **H-PEAK REFUTED**; El Niño 2015–16 `R_AMS` **0.686**, the worst-but-one
> period. The registered `H2E-S` refit fixed the peaks and **failed on cost** (`docs/33` §8), so
> the deficit is **structural and permanent for Phase C**: *"C3/C4 must treat simulated sediment
> as a lower bound on flood-driven transport, and C4's α/β must not be allowed to silently
> absorb it."* `docs/36` then measured the sharper form — **1,829 of 2,236 observed
> peaks-over-threshold have no simulated partner at ±2 d, an 81.8 % event-identity deficit** —
> and `docs/36` §7.1 **requires** that the older "43 % of events missed" *count* statement never
> be quoted without it. *(`R_POT` is quoted as **0.567** by `docs/33` §7.2/§8 but reads 0.5747 in
> `data/processed/peakgap/summary.json`; `docs/36` §7.3 raised the discrepancy and it is not
> reconciled. Quoted here at its owning doc's value, with the disagreement named.)*

Known gaps, named: ~~`calibration_safe` has **no SSC-quality gate** (docs/19, corrected
claim);~~ per-gauge **areas disagree >2× on 36 % of shared gauges** (docs/23 §13.2);
~~LS2D factor not yet computed; MUSLE needs a peak-flow proxy from a daily model.~~

> **⚠ STATUS BACK-ANNOTATION, 2026-08-12 — three of these four gaps have been closed or moved;
> one has not.**
>
> - **SSC-quality gate: CLOSED.** Built as stage C1 and owned by `docs/32` — **79/79 stations
>   classified, each with the measurement that decided it**; 28 mapped, of which 6 `usable`,
>   12 `usable-with-caveat`, 10 excluded (`docs/32` §R6).
> - **Areas: STILL OPEN**, and it is the reason the t/km²/yr embargo stands (`docs/23` §13.2;
>   background task B3, §5 item 3). Unchanged.
> - **LS2D: COMPUTED, and then contested on its *level*.** Built at 90 m by Desmet & Govers
>   (`docs/agents/journal_c31-ls2d.md`, carried into `docs/37`). The level is the open part:
>   `f_LS` is graded **UNVALIDATED** and bracketed at **2.3151× – 3.9768×** the source level
>   (`docs/47` §4.3, registered `docs/46` §1.0), and `docs/37` **Amendment A3 (2026-08-12)**
>   decides the *formulation* — ADOPT-SOURCE, `ls_formulation = buarque_2015_dg` — ~~**without
>   moving the engine default**. This is what blocks C4.3 (§3, C4).~~
>   → **UPDATE 2026-08-19: the LS act LANDED and the block is discharged.** ACT 1 materialised
>   the adopted field and **ACT 2 (commit `c3fdb55`, 2026-08-12) moved the ENGINE DEFAULT** of
>   `src/mgb_sediment.py` `load_geometry()` to **`V4_dg`** (`docs/37` A3.9). Adopted
>   **`f_LS` = 0.25146** erosion-weighted / **0.2446790094097074** area-weighted. C4.3 then ran —
>   see `docs/55` and the refreshed status pointer in §3.
> - **`q_peak` proxy: BUILT AND PRE-REGISTERED**, with its signed bias and the C4
>   anti-compensation rule, in `docs/35` (REGISTERED 2026-08-11).

---

## 3 — Stages

> **⚠ STATUS POINTER, added 2026-08-12. This section is the *plan*, written 2026-08-10; it is
> not a status board and it has been overtaken in places.** Per RULE 0 of `docs/00_INDEX.md`,
> status lives in **`progress_map.html`** and each stage's outcome lives in its own numbered
> doc: **C0** → `docs/26` Addendum · **C1** → `docs/32` · **C2** → `docs/34` · **C2b** (a stage
> that did not exist when this list was written, inserted between C0 and C3) → `docs/33` ·
> **C3** → `docs/37` (**OPEN**, re-issued by Amendments A1/A1.9/A2, enacted by A3) and
> `docs/43` · **C4** → `docs/42` (guards), `docs/45` (pre-registration), `docs/47` (the **entry
> verdict**) and **`docs/55` (the C4.3 OUTCOME: RAILED / EXPLORATORY, *not* adopted)** ·
> **C5** → **`docs/56` (COMPLETE — the observed contrast is reproduced, 18/18 stations, modelled
> median rate ratio 3.05×)**. Read the stage text below as the original intent, and the owning
> doc for what actually happened.
>
> **⚠ POINTER REFRESHED 2026-08-19.** As written on 2026-08-12 this line said
> ~~"`docs/47` (**C4.3 is BLOCKED**) · **C5** → not started"~~ — true at that date, superseded
> since. The `C4.3-BLOCKED-UNTIL-LS-LANDS` entry condition (`docs/47`) was **discharged** when
> the LS act landed; **C4.3 then RAN**, and its verdict is **RAILED / EXPLORATORY, not adopted**
> (`docs/55`) — in-box optimum on the α box floor at **α = 2.0**, unconstrained optimum
> **α ≈ 0.48** *below* the floor, which is the registered signature of mild upstream
> over-production and is a **diagnosis, not a value to adopt**; design-matrix condition number
> `inf`, so only the product **Π** is identifiable (`docs/42` G-set). **C5 is COMPLETE**
> (`docs/56`). **PHASE C IS COMPLETE.**

### C0 — freeze and report H2E · *1 session*
Generate the full per-period report for the best H2E seed (20260901, F 0.2593) with the
same machinery as docs/26: KGE/NSE/r/α/β/PBIAS by period, climatology-benchmark
difference, parameter positions. Write `sim_calibrated_v2/` H2E artifacts and a docs/26
addendum. **This is the hydrology Phase C consumes.** Exit: the table exists and the
ENSO-contrast asymmetry is restated against it.

### C1 — the SSC-quality gate · *1–2 sessions, the real unblocking step*
Build the gate docs/19 says is missing, with the same discipline as precipitation:
- test for **absent** records, not just flagged values (the zero-suppression lesson);
- pair SSC with same-day discharge (rating-curve era awareness — the SNHT breaks in
  docs/17 apply to the *stage* record SSC often rides on);
- classify all 79 stations with evidence: usable / usable-with-caveat / excluded, each
  with the measurement that decided it.
Exit: `sediment_daily_qc.csv` + inventory flags, and "blocked on mainstem SSC quality"
becomes a sentence with station counts in it.

### C2 — the observational ENSO contrast, model-free · *1 session, publishable alone*
From C1's usable stations, compute observed suspended-sediment flux (concentration ×
same-day discharge) for La Niña 2011 vs El Niño 2015–16: totals (context only), **rate
ratios per docs/31 C2.1** (never a ratio of unequal-window totals), seasonal shape, at
every usable station. **Absolute fluxes (t/day) only — no t/km²/yr yields**
until areas are externally resolved (docs/23). Exit: the observational target the model
must reproduce, with uncertainty from the rating-curve R².

### C3 — MUSLE hillslope erosion on our engine · *2–3 sessions*
`Sed = α·(Qsur·qpeak·A)^β · K · C · P · LS2D` per URH per day, driven by H2E surface
runoff. Build order: LS2D from the conditioned DEM (nb07 chain); C/P from the 8 land
classes; qpeak proxy from daily Qsur (document the choice — a daily model underestimates
peaks, and docs/22 measured α < 1 at most gauges; state the direction of that bias on
sediment BEFORE calibrating so it cannot be absorbed silently). Smoke tests: mass
sanity, zero-rain ⇒ zero erosion, K/C/P sensitivity signs. Cross-check one sub-basin
against the team's `musle.py` (two implementations, same discipline as Phase B).

### C4 — channel transport + sediment calibration · *2–3 sessions*
Advection of the clay+silt load with deposition; calibrate the few sediment parameters
(α, β) on **tributary** stations (Fagundes' mitigation for weak mainstem data), neutral
years only — the Klemeš split again, so the ENSO contrast stays out-of-sample. The bar:
Fagundes et al. report sediment KGE −0.26 to 0.44; ~~land anywhere in that band and the
transposition claim holds.~~ Pre-register the cells before searching.

> **⚠ CORRECTION, 2026-08-12 — the band is still the bar, but "land in it and the claim holds"
> is no longer a true statement of what C4 may conclude.** Two owning documents narrowed it.
>
> - **`docs/45` §3.2 keeps the band verbatim** — *"THE SEDIMENT KGE BAR, registered:
>   `F_report` ∈ [−0.26, 0.44]"*, median `KGE_ln` over the CAL-8 stations — but ADOPT now
>   requires **all eight** of its conditions, not the band alone, and states outright that a
>   pass is *"**NOT** a validated α, C, LS, P, FG, K-unit or volume convention. **NOT** a yield.
>   **NOT** a statement about the Momposina or the lower mainstem."*
> - **`docs/42` §3** is why: α, the C level, the LS level, the K unit system, the volume
>   convention, P and FG are **seven ways of writing one identifiable product Π** (condition
>   number measured as `inf`). C4 therefore reports **Π, the equifinal family and per-factor
>   evidence grades — never "validated"**. `docs/42` **G9** adds the reach limit: only
>   **33.47 %** of the model's gross erosion is upstream of any usable SSC station.
>
> **And C4.3 — the search itself — may not start.** `docs/47`'s verdict is
> **`C4.3-BLOCKED-UNTIL-LS-LANDS`**: the α box `[2.0, 30.0]` is denominated in a unit whose
> scale is unresolved (α ∝ `1/f_LS`, `f_LS` UNVALIDATED and uncertain by **2.3151× – 3.9768×**),
> the objective is monotone decreasing across the entire registered box, and the in-box best
> `F_report` measures **−0.305 … −0.350** — below the band's own lower edge. The block is
> upheld by `docs/46` §6.4, `docs/51` §4 and `docs/37` **A3.4** (*"Is C4.3 thereby UNBLOCKED?
> **NO**"*), all after `docs/37` A3 decided the LS *formulation*. Nothing in §3 or §4 of this
> plan authorises starting it.

### C5 — the experiment the project exists for · *1–2 sessions*
Run 2011 and 2015–16, compare simulated vs C2's observed contrast: sign, magnitude,
seasonal timing, and **spatial attribution** (which sub-basins drive the difference —
the thing a process model adds over Restrepo's correlations). Exit: the ENSO-contrast
figure set + a docs write-up stating plainly which parts are prediction (out-of-sample)
and which are description.

---

## 4 — Definition of done (Phase C)

| criterion | bar |
|---|---|
| SSC stations classified with evidence | 79/79, each with its deciding measurement |
| Observed 2011 vs 2015–16 flux contrast | quantified with uncertainty at every usable station |
| Simulated contrast | correct sign and order of magnitude; sediment KGE within Fagundes' −0.26…0.44 band — ⚠ **necessary but no longer sufficient: `docs/45` §6 requires all eight ADOPT conditions and `docs/42` §3 forbids the word "validated". See the correction under §3 C4.** |
| Spatial attribution | sub-basin ranking of contribution to the contrast, with the mechanism named |
| Yields (t/km²/yr) | **NOT reported** until areas resolved externally — flux only |
| Every calibration | pre-registered, ENSO years out-of-sample, parameters checked against bounds |

## 5 — Bounded background track (not gates)

1. ~~**CHIRPS refit** (≤ 2 sessions): refit quantile maps on the repaired series including
   inferred-dry days; rerun both gates. If both pass → v3 forcing + ONE new
   pre-registered calibration cell. If not, the negative result closes the question.~~
   → **DONE, and NEGATIVE. This item is CLOSED — it is not pending work.**

   > **⚠ BACK-ANNOTATION, 2026-08-12.** Registered as **H-CHIRPS** in `docs/33` §1 (frozen
   > 2026-08-10); executed and read out in `docs/18` **§15.5** (`docs/agents/journal_chirps-refit.md`;
   > `src/merge_chirps_gauges.py --qmap-inferred-dry`). Result, from the owning doc:
   >
   > | gate | window | result |
   > |---|---|---|
   > | LOOCV | 2008–2018 station-days | median daily r **0.447** > 0.429 — **PASSES** |
   > | volume | 2009–2017, area-weighted | **2,188.5 mm/yr** vs [2,016.0, 2,056.8] — **FAILS (+7.47 %)** |
   > | decision | | **DO NOT ADOPT** |
   >
   > **The intervention was already the code's behaviour.** The inferred-dry days were 25.9 %
   > of the fit input before the refit, so the re-run reproduces the rejected run bit-for-bit
   > and the diagnosis in `docs/18` §15.3 was wrong on the half it tested (`docs/33` §1:
   > *"the registered intervention turned out to be a **no-op**"*).
   >
   > **This item's own terms therefore apply: *"If not, the negative result closes the
   > question."* The question is closed.** No v3 forcing exists and none was built; no new
   > calibration cell was authorised or run. `docs/18` §15.5: *"v2 remains the forcing, the
   > r-ceiling of doc 22 s4.7 is unmoved, and no route to a passing volume gate exists inside
   > the merge code."*
   >
   > **What is left open is a different question from the one this item asked.** Not "refit the
   > maps" — that is answered — but *why the volume gate fails at all*, whose only surviving
   > candidate is the 139 stations that still report rain-selectively after the zero-suppression
   > repair (`docs/18` §9.3, §15.5). That is an **upstream gauge-record repair**, untested,
   > unscoped, and outside this ≤2-session box. Anyone re-opening it needs a new item and, if it
   > ever produced a forcing, a new pre-registration (§1).
   >
   > *(`docs/31` B1 is the workplan twin of this item and still reads as open work with a "fix"
   > available; `docs/31` is not edited here — it belongs to another owner. Its diagnosis was
   > the more careful one: it warned in advance that the `Inferido_seco` change alone "would
   > leave the volume gate failing", which is exactly what happened.)*
2. **k_int_frac floor** (≤ ½ session): lower the 0.02 bound once, one seed, note what
   happens; 7 of 8 v2-forcing seeds sit on it (docs/29 results).
3. **Areas**: acquire an external drainage-area source (IDEAM station catalogue request /
   published tables). Unblocks yields; blocks nothing else.
4. **SSC coordinate fetch (B5)**: pull IDEAM-catalogue coordinates + areas for the **46 unmapped
   SSC stations** and re-snap by drainage-area matching (docs/19 §5.2 item 2; docs/31 B5). Unblocks
   SSC coverage; blocks nothing. 📌 **C1.0 decision (2026-08-10): Phase C runs now on the 28-station
   mapped subset (24 calibration-safe);** B5 only *raises* that count if it succeeds — C1 does not wait.

## 6 — Standing rules carried into Phase C

The docs/18 §7 traps apply unchanged. Sediment-specific additions: value screens cannot
see absent SSC records; rating-curve eras are regime boundaries, not noise; a daily
model's peak bias must be stated before MUSLE calibration, not discovered after it;
and *"the model is at its input's ceiling"* applies to SSC observations too — measure
the SSC field's own consistency before blaming the sediment module.

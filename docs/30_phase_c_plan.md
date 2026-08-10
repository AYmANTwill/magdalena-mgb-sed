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
  θ_crit 0.6) succeeded** on every pre-registered condition. There is no further
  calibration question whose answer would change Phase C's inputs.
- The one lever that measurably moves r — the CHIRPS merge (LOOCV r 0.447 vs 0.429,
  docs/18 §15) — failed only its volume gate, with the fix identified. It continues as
  **bounded background work** (§5), not as a gate on Phase C.

What closing means concretely: the hydrology is *frozen* for sediment work at the best
H2E parameter set. Any future forcing change (CHIRPS v3) re-opens it only through a new
pre-registration.

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
| Runoff driver | calibrated H2E hydrology, recession-correct (ratio 1.08–1.11), mass-conservative |
| Rating-curve pairs | docs/13; median R² ≈ 0.5 — usable with stated uncertainty |
| Team's second implementation | `musle.py`, `sediment.py`, RS-SSC retrieval — **external, not in this repo** (docs/20:43); must be acquired for the C3.5 cross-check, as in Phase B |

Known gaps, named: `calibration_safe` has **no SSC-quality gate** (docs/19, corrected
claim); per-gauge **areas disagree >2× on 36 % of shared gauges** (docs/23 §13.2);
LS2D factor not yet computed; MUSLE needs a peak-flow proxy from a daily model.

---

## 3 — Stages

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
Fagundes et al. report sediment KGE −0.26 to 0.44; land anywhere in that band and the
transposition claim holds. Pre-register the cells before searching.

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
| Simulated contrast | correct sign and order of magnitude; sediment KGE within Fagundes' −0.26…0.44 band |
| Spatial attribution | sub-basin ranking of contribution to the contrast, with the mechanism named |
| Yields (t/km²/yr) | **NOT reported** until areas resolved externally — flux only |
| Every calibration | pre-registered, ENSO years out-of-sample, parameters checked against bounds |

## 5 — Bounded background track (not gates)

1. **CHIRPS refit** (≤ 2 sessions): refit quantile maps on the repaired series including
   inferred-dry days; rerun both gates. If both pass → v3 forcing + ONE new
   pre-registered calibration cell. If not, the negative result closes the question.
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

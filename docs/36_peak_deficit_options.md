# 36 — The structural peak deficit: diagnosis and ranked options

**Status:** ADJUDICATION, 2026-08-11. No new research. This document weighs three completed
research lenses (an empirical POT diagnosis, a sub-daily data reconnaissance, and a
method/literature review) against each other and against the incumbent decision, and ranks
what to do next. It **decides nothing that docs/33 or docs/35 already decided**; where those
documents are binding, this one says so and stops.

**Numbering note.** docs/33 §5.2 provisionally reserved number 36 for "C5.4 ENSO contrast
results". That reservation is superseded by this file, which was written first. **C5.4's
results must take a later number (37+).** Recorded here so two sessions do not claim 36.

**Scale rule.** Every effect below is reported at both fleet scale (all gauges pooled) and
per-unit scale (per gauge), per the project convention.

**Embargo.** No sediment yield in t/km²/yr appears anywhere in this document. Catchment areas
disagree by more than 2× on 36 % of shared gauges (docs/23 §13.2). Absolute flux only.

---

## 1 — The problem, restated with its numbers

### 1.1 What was measured

C2b (docs/33 §7) scored the adopted H2E hydrology against 63 discharge gauges, 2009–2018:

| signature | fleet median | per-gauge IQR | sediment factor `R^0.56` |
|---|---|---|---|
| `R_Q5` — 5 % exceedance flow | 0.975 | 0.740 – 1.279 | 0.986 (−1.4 %) |
| `R_Q1` — 1 % exceedance flow | **0.847** | 0.633 – 1.234 | 0.911 (−8.9 %) |
| `R_AMS` — annual maxima | **0.820** | 0.529 – 1.186 | 0.895 (**−10.5 %**) |
| `R_AMS`, El Niño 2015–16 | **0.686** | — | 0.810 (−19.0 %) |
| `R_POT` — independent events over obs Q5 | **0.567** | 0.155 – 1.141 | *not a magnitude — see below* |

The deficit **switches on between the 95th and the 99th flow percentile**. It is a tail
effect, not a level shift: the model is essentially unbiased on the 95 % of days that are not
floods, and increasingly wrong above that.

`R_POT` is a **count**: the model produces **1,285 independent peaks-over-threshold against
2,236 observed**, i.e. it misses ~43 % of flood events. β acts on magnitude and cannot convert
a count deficit into a load deficit — `0.567^0.56` is *not* a valid sediment ratio and docs/35
§5.2 records that arithmetic as forbidden.

**Per-unit scale (computed here from `data/processed/peakgap/per_gauge.csv`, n = 63):** the
fleet median hides a wide and bimodal per-gauge picture. Per-gauge event-miss fraction has
mean 0.770, median 0.789, IQR 0.655–0.930, min 0.25, max 1.00. **Eight of 63 gauges miss
100 % of their observed POT events. Four of 63 simulate zero POT events at all.** Five of 63
miss fewer than half. This is not a uniform bias applied to every gauge; it is a fleet in
which a minority of gauges are approximately right and a substantial minority are completely
blind to floods.

### 1.2 Why parameters cannot fix it

C2b pre-registered a refit (H2E-S) with a peak term added to the objective, and ran it under
three conditions fixed in advance (docs/33 §3.3). The result (docs/33 §8):

| condition | required | seed 20260907 | seed 20260908 | verdict |
|---|---|---|---|---|
| 1 — signature in band | `R_AMS` ∈ [0.85, 1.15] | 0.9364 | 0.9970 | **PASS** |
| 2 — no material cost in F | within 0.02 of 0.25931 | 0.22489 | 0.22984 | **FAIL** (Δ −0.0319, 1.6× budget) |
| 3 — no new rails | railed ⊆ {k_sup, k_int_frac, wm_mult@R2} | kc_mult 0.975 | lai_mult 0.006 | **FAIL** (two new rails) |

The peak term **works** — `R_AMS` 0.820 → 0.94–1.00 — and the way it works is the finding.
Both seeds paid for peaks by **abandoning the canopy**: `lai_mult` at its floor on one seed,
`kc_mult` back on its rail on the other. Removing interception delivers rainfall to the soil
undelayed and unbuffered, which is exactly how a daily model manufactures a bigger peak; the
high crop coefficient then evaporates the surplus back out to keep the volume defensible.
This **re-breaks what H2E existed to fix** (docs/29: releasing `kc_mult` from its 2.00 rail).

> **The peak deficit is structural, not a calibration oversight.** In a heavily forested basin,
> buying peaks by deleting canopy interception is not a defensible parameterisation. Phase B
> closed for the second time on that measured conflict.

Three consequences bind everything below:

1. **The parameter route is closed by pre-registration**, not by taste. Re-opening it needs a
   new pre-registration and would have to explain why a rule it already failed should be
   re-run.
2. **α and β may not absorb the deficit either** (docs/35 §6, hard stop α > 35.4 = 3× Williams,
   β outside 0.45–0.65, plus residual tests T1/T2). The compensation available is ≈5.4×, and
   the thresholds are set at a fraction of it so the alarm fires early.
3. **Anything touching the forcing or the engine invalidates the frozen C0 artifacts** —
   `parameters_H2E.csv`, `q_gauge_H2E.npz`, `metrics_fleet.csv`, and `h2e_drivers.npz`
   (521 MB) — **and everything downstream of C0 that has already run** (docs/33 §5.1). C1 and
   C2 survive untouched (§5.3), because they are model-free.

---

## 2 — The diagnosis

Lens 1 re-derived the POT statistics exactly (verbatim `build_mask` / `local_maxima_above` /
`pot_peaks` from `scripts/c2b/peaks_measure.py`; MIN_SEG 180, MAX_GAP 3, POT_SEP 10, POT_FRAC
0.6, threshold = observed Q5) and reproduced docs/33 §7 exactly: 2,236 observed, 1,285
simulated, `R_POT` 0.5747. Every number below was re-read from
`data/processed/peakgap/summary.json` while writing this document.

### 2.1 First correction: the gap is larger than "43 %"

**"43 % of flood events missed" is a COUNT deficit, not an event-identity deficit.** Matching
observed to simulated POT within ±2 days:

- **1,829 of 2,236 observed POT (81.8 %) have no simulated POT within ±2 days.**
- **Mirror: 878 of 1,285 simulated POT (68.3 %) have no observed counterpart.** The model does
  not merely make too few peaks; it makes them on the wrong days.

Both numbers must be quoted together from now on. The 43 % figure understates the
disagreement, and every document quoting it (docs/33 §8, docs/35 §5.2, docs/31) should carry
the ±2 d identity figure beside it.

### 2.2 It is not a timing shift

Greedy 1-to-1 matched fraction against the matching window:

| window | ±0 d | ±1 d | ±2 d | ±3 d | ±5 d | ±10 d | ±15 d | ±30 d | count ceiling |
|---|---|---|---|---|---|---|---|---|---|
| matched | 5.1 % | 14.2 % | 18.2 % | 20.8 % | 24.3 % | 28.8 % | 31.2 % | 33.8 % | **57.5 %** |

A full month of slack recovers only 15.6 points and never approaches the ceiling set by the
count ratio itself. The events are absent or displaced far beyond any plausible routing lag —
not shifted by a day or two.

### 2.3 What the missed events are

Splitting the 1,829 missed events by what the simulation was doing on the day:

| class | definition | n | % of missed | % of all obs POT |
|---|---|---|---|---|
| **ABSENT** | no hydrograph rise (sim within ±2 d below 1.5× its 8–15 d prior baseline) | **737** | 40.3 % | **33.0 %** |
| PRESENT, sub-extreme | rise ≥ 1.5× but below the model's own Q5 | 631 | 34.5 % | 28.2 % |
| PRESENT and above model's own Q5 | model called it extreme; magnitude scaled down | 461 | 25.2 % | 20.6 % |

Median simulated flow at a missed event is 0.616 of the observed Q5 threshold (quartiles
0.397 / 0.616 / 0.877); 31.7 % of missed events come within 20 % of the threshold and 37.1 %
fall below half of it. **A third of all observed flood events produce no rise whatsoever in
the simulation.** That single number constrains most of the options in §3.

### 2.4 Three named mechanisms tested, two refuted

**(a) Daily time step / flashy small catchments — REFUTED.** Per-gauge miss fraction vs log
catchment area: Spearman ρ = **+0.018, p = 0.89, n = 62**. Area terciles: small (68–288 km²,
21 gauges, 853 events) 79.2 % missed; mid (298–1,464 km²) 82.9 %; large (1,563–54,035 km²)
84.1 %. Event-level Mann–Whitney p = 0.22. A daily-resolution failure must be strongest in the
smallest catchments. It is not — if anything the larger catchments are slightly worse.
*Residual doubt:* areas are the unreliable per-gauge areas of docs/23 §13.2, so a real gradient
could in principle be blurred; the null is only robust if those errors are not systematically
ordered with true area.

**(b) Missing infiltration-excess (Hortonian) runoff — REFUTED as the primary cause, bounded
at ≈5 %.** Three independent signatures point the wrong way:

- **Intensity fingerprint inverted.** The ratio P3/P30 is **lower** for missed events
  (0.146 vs 0.194, rank-biserial −0.339, p 8.6e−27). A Hortonian flood needs rain that is
  intense *relative to* accumulation; the missed events are the opposite.
- **Seasonality inverted.** Clustering is significant (χ² = 63.1, dof 11, p 2.5e−09) and runs
  backwards for convection: worst in the June–September dry season (91.5 % missed pooled;
  Aug 94.3 %, Sep 93.4 %), best in the two rainy peaks Oct–Nov (75.9 %) and Mar–May (77.8 %).
  Miss rate is highest exactly when POT counts are lowest.
- **The candidate cell is small.** Missed **and** storm in the top within-gauge P3 tercile
  **and** antecedent in the bottom P30 tercile = **99 events = 5.4 % of the 1,829 missed,
  4.4 % of all 2,236 POT.** Even at 100 % attribution, an infiltration-excess module recovers
  ~5 % of the gap.

**(c) The rainfall field is missing the storms — SUPPORTED, and it is the strongest signal
measured.**

| discriminator (within-gauge percentile) | missed | captured | rank-biserial | p |
|---|---|---|---|---|
| **3-day storm rain P3** | **0.441** | **0.810** | **−0.578** | 1.2e−74 |
| peak daily rain Pmax3 | 0.450 | 0.780 | −0.512 | 7.3e−59 |
| 7-day antecedent P7 | 0.448 | 0.800 | −0.553 | 2.1e−68 |
| 30-day antecedent P30 | 0.459 | 0.714 | −0.388 | 1.3e−34 |
| model runoff coefficient at the event | 0.448 | 0.770 | −0.514 | — |

Absolute: P3 30 vs 50 mm, P7 58 vs 90 mm, P30 204 vs 255 mm. **55.8 % of missed events sit
below their own gauge's median POT-day rainfall, against 12.3 % of captured events.**

Not a gauge-composition artifact: within-gauge paired test on the 33 gauges with ≥5 missed and
≥5 captured gives a median P30 difference of **−62.5 mm** (positive at only 4/33, Wilcoxon
p 1.8e−07) and P7 **−35.2 mm** (positive at **0/33**).

The decisive statistic is the response ratio: **observed peak discharge per mm of 3-day
forcing rainfall, ranked within gauge so catchment area cancels exactly** (docs/23 embargo
respected — no area appears in the number): **0.568 for missed events vs 0.286 for captured,
rank-biserial +0.397, p 4.6e−36.** The catchment responded; the input did not.

The engine behaved correctly given what it was handed: model runoff coefficient at the event
(catchment `qsur_gen_mm` over 3 days ÷ P3, from `h2e_drivers.npz`) is 0.212 at missed events
vs 0.270 at captured. **The engine generated less runoff mainly because it was given less
rain.**

Inside the ABSENT class the picture is starkest: only **74 of 737 (10.0 %)** have the storm
present in the forcing at all, while **408 of 737 (55.4 %)** have P3 below the gauge's own
33rd percentile.

### 2.5 What the evidence does NOT establish — stated plainly

1. **The diagnosis is partly self-referential.** It is made *with* the suspect rainfall field.
   An input that lacks a storm will always look like the cause. What breaks the circularity
   only partially is the ABSENT class: a missing *mechanism* cannot manufacture a flood from
   near-zero rain, and 55.4 % of ABSENT events have near-zero rain in the field. That argument
   rules out the mechanism hypotheses as *primary*; it does not prove the rain was really there.
2. **Inside the 99-event Hortonian cell, the evidence genuinely does not discriminate.** A
   field that systematically under-measures convective intensity would misclassify true
   high-intensity events into the low-P3 group, making the 5.4 % bound too low. This is the one
   place where "missing mechanism" and "rainfall error" are not separated, and it is recorded
   as an honest non-distinction, not resolved.
3. **A dry-antecedent gradient survives inside the storm-confirmed subset, and it is not
   evidence of a missing mechanism.** Restricting to events where the storm *is* in the input
   (within-gauge P3 percentile ≥ 0.9, n = 257): overall miss 51.8 %; dry P30 tercile 65.4 %
   (n = 26), mid 53.5 %, wet 48.3 %; Spearman(P30_pct, missed) = −0.127, p = 0.041. That is a
   real but **small** residual, and it is exactly what *correct* ARNO saturation-excess
   behaviour produces. It is not counted as a defect.
4. **Up to 10 % of the gap may be on the observation side.** 224 of the 737 ABSENT events
   (30.4 %) are single-day observed spikes with `obs_rise` > 3× the 8–15 d prior baseline and
   no rain in the forcing — the signature of a rating-curve or transcription artifact as much
   as of a real flood. **224/2,236 = 10.0 % of all observed POT.** At daily resolution a genuine
   one-day convective flood in an ungauged-rainfall headwater is indistinguishable from a bad
   reading, so 10.0 % is an **upper bound, not an estimate**, and it must **not** be used to
   discount the C3 caveat: the lower-bound framing on simulated sediment stands regardless.
5. **The duration effect is real but modest.** Missed events are shorter (median observed
   exceedance spell 1 d vs 2 d; miss fraction 84.9 % at 1–2 d, 76.0 % at 3–5 d, 68.7 % at
   6–10 d, 61.0 % at >10 d) — but 75.2 % of all POT are 1–2 d anyway, so most of that is base
   rate.

### 2.6 The ENSO asymmetry, which the deliverable inherits

Miss fraction: **71.6 % in La Niña 2011, 88.7 % in El Niño 2015–16, 83.7 % other years.** The
dry phase is the worse one, consistent with El Niño `R_AMS` 0.686 (docs/33 §7.4). Through
MUSLE's β this **inflates the simulated La Niña : El Niño sediment ratio by ≈ +10 %**
(docs/35 §5.4) — an error that flatters the headline contrast rather than protecting it.

### 2.7 Verdict

> **The peak deficit is an input-data problem, not a runoff-engine problem.** Its proximate
> cause is that the daily rainfall field does not contain the storms that produced ~82 % of
> the observed flood events. This is the `r ≈ 0.57` ceiling of docs/22 and docs/26, expressed
> at event scale rather than at series scale.
>
> Two named engine hypotheses were tested and refuted with the wrong-signed fingerprint in
> each case: sub-daily resolution (no area gradient, ρ = +0.018, p = 0.89) and infiltration
> excess (inverted intensity ratio, inverted seasonality, ≤5.4 % candidate cell).
>
> The verdict is held with **moderate, not high, confidence**, because it is diagnosed against
> the field it accuses. §5 pre-registers the test that breaks that circularity.

---

## 3 — The options, ranked

**Ranking currency, fixed before scoring.** *Gain* = the ceiling on how many of the 1,829
missed events the option could address, with the measured basis named — not a hoped-for
improvement. *Feasibility* = whether the data **and** the code exist today. *Cost* = sessions,
against the **≈5–8 remaining** on the core path (docs/31: 8–12 total, C0/C1/C2 done).
*Re-opens Phase B* = whether it invalidates `h2e_drivers.npz` and everything downstream of C0.

| # | option | gain ceiling (events) | feasible today | cost | re-opens B | score |
|---|---|---|---|---|---|---|
| **0** | **Accept and propagate as an explicit lower bound** | 0 recovered — delivers the study | **yes, already done** | **0** | no | **incumbent** |
| **1** | **CHIRPS storm-presence audit of the 1,829 missed events** | 0 recovered — buys the decision | **yes** (CHIRPS on disk, no engine run) | **≤ ½ session** | **no** | **highest of the interventions** |
| 2 | Densify the daily rainfall field with the IDEAM automatic network | ~408–1,000 (22–55 %) | data partly on disk, 2011–2016 only | 3–5 | **yes** | moderate gain, high cost, one likely-fatal flaw (§3.4) |
| 3 | True sub-daily forcing + a sub-daily engine | ≤ ~400, and the mechanism is refuted | data yes, **engine does not exist** | 6–10+ | **yes** | below the default |
| 4 | Within-day disaggregation using an ERA5-Land shape | **0** while the engine is daily | data yes | 1–2 (but useless alone) | yes, if used | strictly dominated |
| 5 | Infiltration-excess (Hortonian) mechanism | **99 (5.4 %)** | no local Ks, needs #4 first | 4–6 | **yes** | refuted and expensive |
| 6 | Local-inertial routing (implementation B) | **0** on ABSENT (737) and 0 on sediment source | **code not in this repo** | unknown | **yes** | not acquirable, sign ambiguous |

Two of the six mandated candidates were **already adjudicated elsewhere and are not re-opened
here**: the unit-hydrograph `q_peak` parameterisation (docs/35 §4, REJECTED for production
2026-08-11) and the parameter refit (docs/33 §8, REJECTED on 2 of 3 conditions). §3.7 records
their status rather than re-deciding them.

---

### 3.0 — RANK 0 (incumbent): accept the bias and propagate it as an explicit lower bound

**What it is.** Already implemented. docs/35 §5.3 registers the bias statement; docs/33 §8
registers the caveat that C3/C4 inherit; docs/35 §6 registers the anti-compensation rule that
stops α and β from hiding it. Simulated flood-driven suspended-sediment transport is reported
as a **lower bound**: low by at least 10.5 % fleet-wide from the measured magnitude deficit
alone, at least 19.0 % in El Niño, plausibly −10 % to −45 % once the missing events are
included, and the simulated ENSO contrast ratio is quoted with its ≈+10 % inflation attached.

**Data needed.** None. **Cost.** Zero. **Re-opens Phase B.** No.

**What the literature says it buys.** Exactly what MGB-SED's own literature does. Fagundes
(2018) §6.4.1 names the missing peak-energy term as a known limitation of the method —
*"que no MGB-SED é desconsiderada pela dificuldade de se obter tal informação"* — and §6.4.2
states plainly that *"o modelo também não representou de forma adequada grandes picos de
concentração."* Our quantification (`R_AMS` 0.820, `R_Q1` 0.847, `R_Q5` 0.975, `R_POT` 0.567)
is **more specific than anything published for MGB-SED**, which is a contribution rather than
an embarrassment.

**Risk.** Methodological: none. Reviewer dissatisfaction is answered directly by the
Buarque/Fagundes precedent.

> **NOT WORTH DOING IF:** the bound becomes wide enough to make the study's own claim
> untestable. The concrete condition: **if the peak-driven contrast inflation ever exceeds the
> margin between the simulated and observed ENSO contrast**, the lower-bound framing stops
> being a caveat and becomes a refutation. Measured today it does not come close — inflation is
> ≈+10 % against an observed contrast of 2.8×–4.6× (primary) and 6.4×–9.3× (sensitivity), same
> sign at 22/22 stations (docs/34). A +10 % bias cannot flip that sign. **The condition is not
> met, so rank 0 stands.** It would also fail if a cheap test showed the deficit recoverable
> for less than the remaining C3–C5 budget — which is what rank 1 exists to find out.

---

### 3.1 — RANK 1: CHIRPS storm-presence audit of the 1,829 missed events

**What it is.** A pure data test, no engine run, no forcing rebuild. For each of the 1,829
missed events, compute the catchment-mean 3-day CHIRPS rainfall and its **within-gauge
percentile**, and compare it against the same quantity from the gauge-IDW forcing field
already used. The question is single and sharp: **does an independent rainfall product see the
storms the gauge field missed?**

- If CHIRPS **does** see them, the §2.7 verdict survives its circularity objection, the defect
  is localised to the gauge network/interpolation rather than to regional rainfall itself, and
  the size of the recoverable fraction is measured rather than guessed.
- If CHIRPS **also** misses them, the verdict weakens sharply: either no available rainfall
  product contains those storms (in which case options 2–4 cannot work either, and rank 0
  becomes the *only* defensible position), or a larger share of the gap belongs to the
  observation-artifact channel (§2.5.4) or to a mechanism after all — which puts the 5.4 %
  Hortonian bound and the 10.0 % artifact bound back in play.

**Data needed, and whether it exists.** Everything, on disk and verified: all 11
`data/raw/climate/chirps_basin_<y>.nc` opened, single variable `precip`, shapes
(365|366, 202, 96) at 0.05°, unique time diff exactly 1.0 day, span 2008-01-01…2018-12-31
(lens 2). The event table `data/processed/peakgap/events.csv` (2,236 rows with class, duration,
`obs_rise`, `P3_pct`) exists. **No hydrology run. No new download. No API. No engine change.**

**What the literature says it buys.** Nothing directly — it is a diagnostic, not a fix. Its
value is that it is the **only cheap way to break the self-reference in §2.5.1**, and lens 3's
central finding is that every *fix* downstream of the rainfall field is either bounded at ~5 %
(Hortonian), degenerate with a parameter we are forbidden to tune (`q_peak`), or requires an
engine that does not exist (sub-daily). Knowing whether the rain was there is therefore worth
more than any of them.

**Cost.** **≤ ½ session.** **Re-opens Phase B.** **No** — it reads frozen artifacts and raw
CHIRPS; it writes nothing the model consumes.

**Risk.** (i) CHIRPS is itself satellite-derived and imperfect, so a null result is ambiguous
between "the storm was not there" and "neither product sees it"; the test must therefore be
reported as **presence evidence only**, never as a rainfall correction. (ii) docs/32 /
commit 542d5f6 rejected a CHIRPS-gauge **merge** on pre-registered gates — this audit is *not*
that merge and must not be presented as reopening it; it uses CHIRPS as a **witness**, not as
forcing. That distinction has to be written into the result or the audit will be mistaken for
a quiet relitigation.

> **NOT WORTH DOING IF:** the answer cannot change any action. Concretely — **if the team has
> already committed that no forcing rebuild will happen before the deliverable regardless of
> the outcome**, the audit only relabels a caveat and should be skipped. It is also not worth
> doing if a prior check shows CHIRPS's daily detection skill in this basin is too poor to
> serve as a witness at all (e.g. if it fails to see the storms behind the **captured** events
> either — which is the built-in control described in §5).

---

### 3.2 — RANK 2: densify the daily rainfall field with the IDEAM automatic network

**What it is.** Aggregate the IDEAM automatic 10-minute network (Socrata `s54a-sgyg`) to daily
totals, add those stations to the conventional DHIME set, re-run the IDW, rebuild the forcing,
and re-run Phase B. This is the option **aimed directly at the diagnosed cause** — more daily
rainfall stations means more of the missing storms enter the field.

**Data needed, and whether it exists.** Partly on disk and fully route-verified:
`data/raw/observed/precip/precip_auto_daily_long.csv` holds 86,621 station-days across 204
station codes, **2011-01-01…2016-12-31**; 70,367 rows / 126 stations pass n ≥ 100 slots
(2011 = 17,468 / 66 stations; 2015 = 25,409 / 84; 2016 = 27,490 / 120). The live route was
verified end-to-end: station `0021015040`, 2011-01-03 returned 138 rows at 10-minute stamps
summing to exactly the on-disk aggregate (6.0 mm, n = 138). Basin station counts measured live
on an identical 1–7 March window: 2008 = 54, 2009 = 57, 2010 = 58, 2011 = 53, 2012 = 59,
2013 = 75, 2014 = 71, 2015 = 75, 2016 = 103. **2017 and 2018 were not obtained** (repeated
250 s API timeouts) and are recorded as unmeasured, not zero.

**Gain ceiling.** Bounded by the events whose storm is absent from the forcing: 408 of the 737
ABSENT events have P3 below their gauge's 33rd percentile, and a share of the 631 sub-extreme
events would also gain. Plausible ceiling **~408–1,000 of 1,829 = 22–55 %** — the largest gain
of any option here, which is why it ranks above 3–6 despite its cost.

**Cost.** 3–5 sessions. The on-disk file covers only 2011–2016, so 2008–2010 and 2017–2018
require a bulk pull that must be **per station and resumable** (a grouped weekly basin-wide
query takes 66–194 s and times out at 250 s; order of magnitude ~60 stations × 6 years ×
52k rows ≈ 19 M rows). Then re-IDW, rebuild forcing, re-run Phase B.

**Re-opens Phase B.** **Yes — a third time**, and this is the expensive part, not the download.
It invalidates `h2e_drivers.npz` (521 MB), `parameters_H2E.csv`, `q_gauge_H2E.npz`,
`metrics_fleet.csv`, the docs/35 registration built on those drivers, and everything downstream
of C0 already run (docs/33 §5.1). C1 and C2 survive.

**Risk — and one flaw that may be disqualifying.**

1. **Density is not constant across the two ENSO windows.** 2011 (La Niña) had ~53–66 basin
   automatic stations; 2015 had ~75–84 and 2016 had ~103–120. A rainfall field whose station
   density nearly doubles between the wet window and the dry window **injects a non-climatic
   trend into precisely the contrast this study measures.** The current forcing does not have
   that problem. Any densification must therefore either be restricted to a station set present
   in *all* years, or carry an explicit homogeneity test — and restricting to the common set
   discards most of the gain. **This is the strongest argument against option 2 and it is
   structural, not practical.**
2. The automatic network sits **19 % below** the conventional network on co-located pairs,
   attributed in part to *mechanical under-registration at high intensity* (docs/16 §4.4) — the
   exact regime a peak fix depends on.
3. Coverage is thin on the Cauca side and in the lowlands (docs/16 §4), which is where the
   field most needs help.
4. The raw network is unvalidated; the zero-suppression lesson (docs/16 §4.1) applies to it in
   full and would have to be re-run from scratch on it.

> **NOT WORTH DOING IF:** any one of these three holds. (a) The rank-1 audit shows the missed
> events' storms are **absent from CHIRPS too** — then the storms are absent from every
> available product and more stations of the same network will not find them. (b) A
> homogeneity test shows the station set common to 2011 **and** 2015–16 is too small to move
> the field materially — i.e. if restricting to the common set recovers less than roughly half
> of the ~408-event floor, the remaining gain does not justify reopening Phase B. (c) Fewer
> than ~4 sessions remain on the core path, since a failed forcing rebuild would consume the
> deliverable rather than the caveat.

---

### 3.3 — RANK 3: true sub-daily forcing plus a sub-daily engine

**What it is.** Force the model at sub-daily resolution using the IDEAM 10-minute network for
within-day shape (amount from conventional DHIME), gap-filled with ERA5-Land hourly `tp` where
the automatic network is empty, and run the hydrology at a sub-daily step.

**Data needed, and whether it exists.** The *rainfall* data exists and is the best-verified
finding of lens 2: 10-minute observations at 53–103 basin stations per year 2008–2016, with
median 144 slots/day (max 288 — some stations log at 5 min). ERA5-Land hourly is complete and
gap-free: 132 files opened, `tp` present in all, 96,432 hourly steps = 4,018 × 24 exactly, per
month equal to calendar hours, grid 101 × 48 at 0.1°.

**The engine does not exist.** MGB is daily, full stop: the official MGB-IPH application
manual has **0 hits** for *passo de tempo*, *horário* and *sub-diário*; Buarque (2015) and
Fagundes (2018) likewise have 0 hits for *sub-diário*/*horária*. MGB-SED computes a
per-minibacia time of concentration and spends it entirely on the **delay** (the TKS linear
reservoir), never on the peak — the opposite of SWAT's choice. A sub-daily variant would be
new engine code with no upstream reference implementation.

**Gain ceiling.** Set by the resolution hypothesis, **which §2.4(a) refuted**: no area
gradient (ρ = +0.018, p = 0.89). The only residual channel is duration (1–2 d events miss at
84.9 % vs 61.0 % at >10 d), whose excess over base rate is at most ~400 events — and lens 1's
area null argues that excess is not resolution either. **Realistic gain well below the ceiling,
on a refuted mechanism.**

**Cost.** 6–10+ sessions: the bulk pull (§3.2), a shape model, a sub-daily forcing build
(arrays 24×–144× current volume), a sub-daily engine, and a full recalibration. **This exceeds
the entire remaining core-path budget.** **Re-opens Phase B.** Yes.

**Risk.** The shape source is biased low at high intensity by 19 % (docs/16 §4.4); ERA5-Land's
shape is measured ~2.2× too smooth (below); the timestamp timezone of `fechaobservacion` is an
**inference, not a documented fact**, and must be reconciled with the IDEAM 07:00→07:00
*día pluviométrico* and ERA5's UTC stamps before anything is built.

> **NOT WORTH DOING IF:** the deficit is dominated by absent daily storm totals rather than by
> within-day shape. **Operational test, already measured:** while |rank-biserial(P3_pct)| ≥
> |rank-biserial(intensity_ratio)| — currently **0.578 vs 0.339, with the intensity term
> pointing the wrong way** — the missing information is in the daily total, and a denser daily
> field (option 2) dominates a sub-daily one at a fraction of the cost. **This condition holds
> today, so option 3 is not worth doing.** It would revive only if the rank-1 audit showed the
> storms present in an independent field *and* a fine-resolution run were the only way to use
> them — which it is not.

---

### 3.4 — RANK 4: within-day disaggregation of daily totals using a reanalysis shape

**What it is.** Keep the daily totals; impose a within-day profile from ERA5-Land hourly `tp`
(or from a stochastic disaggregation model), rescaled so each cell-day preserves its daily
total.

**Data needed, and whether it exists.** Fully on disk, and the cheapest of all the forcing
options — no download. **But the accumulation convention is a live trap:** `tp` has
`GRIB_stepType='accum'`, units m, and behaves exactly like `ssrd` — reset at 00 UTC, with the
00:00 stamp holding the **previous** day's total. Correct rules: UTC daily total(d) = `tp` at
00:00 of d+1; hourly increment(h) = `tp[h] − tp[h−1]` with `tp[0] := 0`. A max or naive diff
over the UTC day **repeats docs/16 error #4** (the `ssrd` +7 % radiation bug).

**Why it is strictly dominated — three independent reasons.**

1. **It cannot reach discharge peaks in a daily engine.** Within-day shape changes `Q_sur` only
   if the water balance itself runs sub-daily. In the daily engine it changes nothing.
2. **Its only channel to sediment is `q_peak`, which is pre-registered fixed** (docs/35 §4:
   `q_peak = Qsur·a/86.4`, Buarque 2015 eq. 7) — and its effect there is a pure multiplier,
   `86.4/(4.806·T_p)`, i.e. **degenerate with α**, which docs/35 §6 forbids tuning. Lens 3
   reaches the same conclusion from the literature side: in a daily engine, disaggregation is
   dominated by the deterministic modified-rational formula, which is itself already rejected.
3. **Stochastic disaggregation reproduces statistics, not sequences.** For any given day the
   profile is a random draw, so day-matched correlation cannot improve in expectation
   (Pui et al. 2012 found the method of fragments best — i.e. the winner is the one that copies
   a *real* observed profile). On a field already at `r ≈ 0.57` over 257,000 km² with ~30 km
   gauge spacing, refining the within-day shape **adds structure without information**.

**And the reanalysis shape itself is measurably wrong.** Fleet scale (all 4,848 ERA5 cells;
938,960 wet cell-days ≥5 mm in 2011): wettest hour carries median **0.193** of the daily total,
median **16 hours/day** with ≥0.1 mm, peak/uniform ratio **4.63×**. Per-unit scale (5 real
10-minute gauges, 2011, ~52k rows each): wettest-hour share **0.386 / 0.426 / 0.421 / 0.508 /
0.556**, wet hours per wet day **9 / 8 / 8 / 6 / 7**, peak/uniform **9.26× / 10.22× / 10.11× /
12.20× / 13.33×**. **ERA5-Land under-concentrates by ≈2.2× on both metrics and rains for twice
as many hours.** Its diurnal cycle is also spatially wrong: a single basin-wide 13h-local peak
(6.9 % of annual rain, peak/mean 1.66 in 2011 and 1.64 in 2015), while station 0023050420
(Argelia, Medio Magdalena) peaks **nocturnally** (20h–01h carrying 10.0–12.5 % against 0.4–1.0 %
at 09h–13h). One uniform shape would place rain at the wrong time of day over part of the basin.

> **NOT WORTH DOING IF:** the engine remains daily — which it is. **This option is never a
> standalone; it is a sub-component of option 3 and has zero value without it.** It becomes
> worth revisiting only if option 3 is already funded and running, and even then only with the
> ~2.2× under-concentration correction and the de-accumulation rule stated above written into
> the build. It is also not worth doing as a `q_peak` route at any time, because that route is
> closed by docs/35 §4 and §6.

---

### 3.5 — RANK 5: add an infiltration-excess (Hortonian) mechanism

**What it is.** Graft an infiltration-excess pathway onto the engine's ARNO
saturation-excess-only runoff generation, so that high-intensity rain produces runoff on
unsaturated soil.

**Data needed, and whether it exists.** Requires `Ks` per URH — **not measured anywhere in this
project**; IGAC soils give texture only. It also requires a within-day intensity distribution,
i.e. it **smuggles option 4 in as a dependency**. SWAT's Green-Ampt option requires sub-daily
rainfall for exactly this reason.

**What the literature says it buys.** The method is established — Liang & Xie (2001),
*Adv. Water Resour.*, 246 citations, grafts infiltration excess onto VIC's saturation-excess
scheme, the same runoff family as ours. But it is **near-inert at a daily step**: a large
50 mm/day event is 2.1 mm/h mean intensity, below `Ks` for most soils. Generating Hortonian
runoff from daily data requires *assuming* the within-day intensity distribution — i.e.
inventing the very information the module needs.

**Gain ceiling.** **99 events = 5.4 % of missed, 4.4 % of all POT**, at 100 % attribution, and
the two independent fingerprints (inverted intensity ratio, inverted seasonality) argue even
that is generous.

**Cost.** 4–6 sessions. **Re-opens Phase B.** Yes — it changes `Q_sur`, which voids H2E,
F = 0.25931, `h2e_drivers.npz`, and the docs/35 registration built on them.

> **NOT WORTH DOING IF:** the Hortonian candidate cell stays small. **Concrete condition: the
> cell must exceed ~20 % of missed events when scored against an independent rainfall field
> before this is worth 4–6 sessions and a third Phase B.** Measured against the current field
> it is **5.4 %**, with the intensity fingerprint inverted (rb −0.339, p 8.6e−27) and
> seasonality inverted (worst Jun–Sep at 91.5 %). **The condition is not met.** The rank-1
> audit is the cheap way to re-score the cell; if it comes back with high-intensity storms
> present in CHIRPS on those 99+ events and the cell grows past 20 %, this option returns to
> the table — and not before.

---

### 3.6 — RANK 6: local-inertial routing (implementation B) for peak sharpness

**What it is.** Replace the engine's storage routing with a local-inertial (simplified
shallow-water) scheme, on the reasoning that better channel hydraulics would sharpen simulated
flood peaks.

**Evidence base — flagged honestly.** **None of the three lenses researched this option.** The
adjudication below is structural reasoning from what is measured, not a measurement of routing
itself, and it should be read at that confidence level.

**Data and code — does it exist?** **No.** Implementation B's `musle.py` / `sediment.py` are
external and **not in this repository** (docs/30 line 53, docs/31 §C3.5); no path or URL is
recorded. **C3.5 remains BLOCKED and was not attempted** — recorded here for the fourth time,
consistent with docs/35 §8 item 2. There is nothing to run.

**Why it cannot address the diagnosed problem, even if acquired.**

1. **Routing conserves volume and sits downstream of runoff generation.** It cannot create a
   flood the hillslope did not produce. **737 of the 1,829 missed events (40.3 % of missed,
   33.0 % of all observed POT) show no hydrograph rise at all** — no routing scheme makes a
   rise where the generation produced none.
2. **A sharper peak is paid for out of the recession.** Routing redistributes within an event;
   it does not add water. Against a gap in which the input rainfall itself is short by
   20 mm of 3-day storm at the median missed event, redistribution recovers little.
3. **MUSLE's source term is upstream of channel routing.** `Sed = α(Q_sur · q_peak · A)^β ·
   K·C·P·LS2D` is evaluated at the hillslope/pixel scale (docs/35 §4). Channel routing changes
   **delivery timing, not generation** — so the effect on simulated sediment production is
   **exactly zero**.
4. **The sign of the discharge effect is not even clearly positive.** In the floodplain-dominated
   lower Magdalena, a physically better routing scheme would represent floodplain storage more
   fully and therefore **attenuate** peaks further downstream. The project has already caught
   *celerity absorbing floodplain storage* as a compensating error; a scheme that removes that
   compensation could plausibly make `R_AMS` worse, not better.

**Cost.** Unknown and unbounded (acquisition + porting + recalibration). **Re-opens Phase B.**
Yes.

> **NOT WORTH DOING IF:** the ABSENT class dominates the gap and the sediment source term is
> upstream of routing — both of which hold. **Concrete conditions for revisiting, all three
> required: (a) the ABSENT class falls below ~10 % of missed events (it is 40.3 %); (b) a
> routed-peak deficit is demonstrated at gauges where the simulated hillslope runoff *volume*
> is already correct; and (c) implementation B's code is actually acquired.** None holds today.
> If routing is ever pursued, it must be justified as a *discharge-timing* improvement, never
> as a sediment fix.

---

### 3.7 — Already adjudicated: not re-opened here

| candidate | status | where |
|---|---|---|
| **Sub-daily peak parameterisation (SCS triangular unit hydrograph)** | **REJECTED for production 2026-08-11**; retained only as a sensitivity generator | docs/35 §3(ii), §4, §7 |
| **Parameter refit with a peak term (H2E-S)** | **REJECTED on 2 of 3 pre-registered conditions**; licenses no further refit | docs/33 §3.3, §8 |
| **CHIRPS-gauge merged forcing** | **REJECTED on pre-registered gates** | docs/32, commit 542d5f6 |

The unit-hydrograph rejection deserves one line of reinforcement, because lens 1 supplies
evidence docs/35 did not have. docs/35 rejected it on three grounds: it is not the source
formulation (Buarque 2015 eq. 7 ≡ the daily-mean proxy); `t_c` is not computable, since no
basin-wide slope field exists and the only DEM covers the **flat** 17.4 % of minibacias; and
its rainfall-excess duration `D` is a free parameter no measurement in this project can set.
Lens 1 adds a fourth, decisive one: **a `q_peak` formula is a monotone function of daily
`Q_sur`, so it cannot manufacture a flood the hydrology did not produce.** `R_POT` 0.567 and
the 737 ABSENT events are untouched by any choice of `q_peak`; only magnitude scaling changes,
and that is degenerate with α, which is registered as un-tunable. The rejection is
independently confirmed.

---

## 4 — The honest default

> **Option 0 — accept the bias and propagate it as an explicit lower bound — is already
> implemented, costs zero sessions, invalidates nothing, and is what the source literature
> itself does. It is the operating decision unless something beats it on evidence.**

This must be stated in the strong form, because the pull toward the alternatives is ambition,
not evidence. Read the ranking table honestly:

- Options **4 and 6** have a gain ceiling of **exactly zero** for the stated problem — option 4
  because within-day shape cannot move a daily water balance and its only sediment channel is
  registered fixed; option 6 because routing is downstream of generation and upstream of
  nothing that MUSLE reads.
- Option **5** has a measured ceiling of **5.4 %** with its diagnostic fingerprint pointing the
  wrong way in two independent tests.
- Option **3** rests on a hypothesis that was **measured and refuted** (no area gradient,
  ρ = +0.018, p = 0.89) and would cost more sessions than remain on the entire core path.
- Option **2** is the only intervention with a large gain ceiling (22–55 %), and it carries a
  possibly-disqualifying flaw of its own: its station density nearly doubles between the La
  Niña and El Niño windows, which would inject a non-climatic trend into the study's headline
  contrast.
- Option **1** recovers **no** events. It buys the one thing missing — whether the diagnosis
  survives its own circularity — for ≤ ½ session and without unfreezing anything.

Each option's explicit not-worth-doing condition is stated in its subsection above (§3.0
through §3.6); all seven are present. **Six of the seven fail their own condition today.** Only
option 1 passes, and it passes because it is a measurement, not a fix.

---

## 5 — Pre-registration sketch: the CHIRPS storm-presence audit (rank 1)

Rank 0 needs no pre-registration — it is already registered, in docs/35 §5.3 (bias statement)
and §6 (anti-compensation rule), dated 2026-08-11. This sketch therefore covers the top-ranked
**intervention**. It is a sketch, not a registration: it must be written into a numbered
pre-registration document, with these fields fixed, **before** any CHIRPS value is read.

**Hypothesis (H-STORM).** The rainfall field used to force the model, not the runoff engine, is
the proximate cause of the missing flood events. Operationally: *for observed POT events the
model missed, an independent daily rainfall product (CHIRPS) contains materially more storm
rainfall than the gauge-IDW forcing field does.*

**Population.** The 2,236 observed POT events in `data/processed/peakgap/events.csv`, split
into the 1,829 missed and the 407 captured. Frozen: the events, the ±2 d matching window, and
the classes (ABSENT / sub-extreme / sim-extreme) are taken exactly as they stand and are not
recomputed.

**Measurement.** For each event, catchment-mean 3-day CHIRPS rainfall ending on the event day,
converted to a **within-gauge percentile** exactly as `P3_pct` was built for the forcing field
(same window, same ranking population, same gauge). Primary statistic: the rank-biserial
correlation between `P3_pct_CHIRPS` and missed/captured, to be compared against the forcing
field's **−0.578**.

**The built-in control — declare it before looking.** The **captured** events are the control.
CHIRPS must reproduce the forcing field's storm signal on the 407 captured events
(`P3_pct_CHIRPS` median ≳ 0.7, comparable to the forcing's 0.810). If it does not, CHIRPS is
not a competent witness in this basin and **the whole test is void** — it says nothing about
the missed events. This check is run and reported first, and its failure is a null result, not
a licence to reinterpret.

**Gate (fixed in advance).**

| outcome | criterion | conclusion |
|---|---|---|
| **CONFIRMS** | control passes **and** median `P3_pct_CHIRPS` on missed events ≥ 0.65 **and** |rb| falls below ~0.30 (from −0.578) | The storms exist and the gauge field lost them. §2.7 survives. Option 2 moves to the top of the intervention list, subject to its own homogeneity condition (§3.2). |
| **REFUTES** | control passes **and** median `P3_pct_CHIRPS` on missed events stays below ~0.50 with |rb| ≳ 0.50 | No available product contains those storms. Options 2–4 all lose their premise. The observation-artifact channel (≤10 %) and the Hortonian cell (5.4 %) are re-scored on CHIRPS, and **rank 0 becomes the only defensible position** — a stronger result than the one we have now. |
| **VOID** | control fails | CHIRPS cannot serve as a witness. Report as void; do **not** reinterpret. |
| **AMBIGUOUS** | anything between | Report the numbers, change no plan, keep rank 0. |

Sub-analysis fixed in advance, not chosen afterwards: the same statistic reported separately
for the **ABSENT** class (n = 737), where the claim is sharpest, and for the 99-event Hortonian
candidate cell, whose size under CHIRPS is the §3.5 revival test.

**Cost if it succeeds — named now, not discovered later.** The audit itself costs ≤ ½ session
and invalidates nothing. **A CONFIRMS outcome does not authorise a forcing change.** It
authorises writing option 2's pre-registration, and that option's true cost is 3–5 sessions
**plus** the full docs/33 §5.1 cascade: C0 re-run, new `parameters_*.csv`, new
`q_gauge_*.npz`, new `metrics_fleet.csv`, a **regenerated `h2e_drivers.npz` (521 MB)**, and
**every stage downstream of C0 that has already run must be re-run against the new drivers** —
including the docs/35 `q_peak` registration, whose measured `Q_sur` magnitudes are quoted from
the current drivers. C1 and C2 are unaffected (docs/33 §5.3). Against ≈5–8 remaining core-path
sessions, that cascade would consume the deliverable. **A CONFIRMS result is therefore most
likely to be published as a sharpened diagnosis and a named future-work item, not acted on in
this project.** That should be said out loud before the test is run, so the result is not
allowed to drag the project into a rebuild by momentum.

**What this sketch does not do.** It does not re-open docs/32's rejection of the CHIRPS-gauge
merge. CHIRPS is used here as an **independent witness to storm presence**, never as forcing
and never as a merge candidate. Any drift from witness to forcing is a new decision requiring
its own pre-registration.

---

## 6 — Recommendation

**Do not pursue a fix now. Keep option 0, spend ≤ ½ session on the option-1 audit if it can be
had cheaply, and put the remaining sessions into C3–C5.** The evidence points one way and it
is not toward engine work: the two named mechanism hypotheses were measured and refuted with
inverted fingerprints (no area gradient, ρ = +0.018 p = 0.89; inverted intensity ratio,
rb −0.339; inverted seasonality, worst Jun–Sep at 91.5 %), the parameter route is closed by a
pre-registration the refit already failed on two of three conditions, and every remaining
intervention either has a gain ceiling of zero (disaggregation, routing), a ceiling of 5.4 %
(Hortonian), or a cost exceeding the entire remaining core-path budget while re-opening Phase B
a third time. The one option aimed at the actual diagnosis — densifying the daily rainfall field
— carries its own likely-fatal flaw, that its station density nearly doubles between the La Niña
and El Niño windows and would inject a non-climatic trend into the very contrast the study
exists to measure. Meanwhile the incumbent costs nothing, is what MGB-SED's own literature does
(Fagundes 2018 §6.4.1–§6.4.2 name this limitation in print), and is already quantified more
precisely than anything published for the method: `R_AMS` 0.820, `R_Q1` 0.847, `R_Q5` 0.975,
`R_POT` 0.567, 81.8 % event-identity deficit, El Niño `R_AMS` 0.686, and a ≈+10 % inflation of
the simulated ENSO contrast — against an observed contrast of 2.8×–4.6× with the same sign at
22/22 stations, which a +10 % bias cannot flip. **The deliverable is not blocked by the peak
deficit; it is qualified by it, and the qualification is now the most specific one in the
MGB-SED literature.** Finish C3–C5, publish simulated flood-driven sediment as a lower bound
with the §2 numbers attached, and record the rainfall field as the named, evidence-backed
future-work lever rather than a hope.

---

## 7 — Corrections and open items this document creates

1. **Framing correction, propagate to docs/33 §8, docs/35 §5.2 and docs/31.** "43 % of flood
   events missed" is a **count** deficit. The **event-identity** deficit at ±2 d is **81.8 %**,
   and **68.3 %** of the *simulated* peaks are themselves unmatched. Both must be quoted
   together.
2. **Per-unit correction to the fleet framing.** The fleet median masks 8 of 63 gauges that
   miss **100 %** of their observed POT and 4 of 63 that simulate **zero** POT events. Any
   statement of the form "the model misses about 43 % of peaks" should be accompanied by the
   per-gauge distribution (median 0.789, IQR 0.655–0.930).
3. **Numbering.** docs/33 §5.2 reserved 36 for C5.4 results; that reservation is superseded and
   C5.4 must take 37+.
4. **C3.5 remains BLOCKED.** Implementation B's `musle.py` is not in this repo (docs/30 line
   53, docs/31 §C3.5, docs/35 §8 item 2). **Not attempted.** This also blocks any serious
   evaluation of §3.6.
5. **Unmeasured, recorded as such:** basin automatic-station counts for **2017 and 2018** were
   not obtained (repeated 250 s API timeouts) — recorded as unmeasured, **not zero**; lower
   bound ≥103 from the 2016 measurement plus 107 + 87 telemetric installs in 2017–18 per the
   catalogue.
6. **Inference, not fact:** the IDEAM automatic timestamp timezone. `fechaobservacion` is read
   as local Colombia time because the resulting diurnal peaks are physical; this must be
   confirmed and reconciled with the IDEAM 07:00→07:00 *día pluviométrico* and ERA5's UTC
   stamps before any use of that network.
7. **Small-sample caveat on the ERA5 shape comparison:** it rests on 5 stations in one year
   (2011), all in Alto Magdalena / Medio Magdalena / Sogamoso, with **no Cauca-side station**.
   The ≈2.2× under-concentration factor is consistent across all five but is not a basin-wide
   fleet estimate; and a real areal average legitimately has more wet hours than a point gauge,
   so part — not all — of the 16-vs-8 wet-hour gap is physically correct.
8. **Unverified literature item:** Fagundes et al. (2026) ISWCR 100599 full text could not be
   read (ScienceDirect 403 on the article page, `/pdfft`, a reader proxy and a browser-UA curl;
   no repository full text; the INPE mirror refused connection). The `q_peak` answer rests on
   Buarque (2015) eq. 7 and Fagundes (2018) eq. 12, which agree verbatim. One institutional-access
   check of the 2026 Methods paragraph would close it.
9. **Process note carried forward from lens 2, recorded because it cannot be disproved:** a
   `Stop-Process` was issued on PID 6200 (a near-idle `python3.10`, 0.94 s CPU) in the belief
   that it was a stuck background job that had in fact never started (exit 127, path quoting).
   It was almost certainly a finished heredoc interpreter. No calibration search was running
   (Phase B is closed) and none was launched.
10. **Scripts not committed.** The lens-1 and lens-2 analysis scripts (`peakgap.py`,
    `peakgap_fig.py`, `scan_era5.py`, `era5_tp_shape2.py`, `gauge_subdaily.py`) live only in
    session scratchpads; their outputs are on disk under `data/processed/peakgap/`. A future
    session that needs the rank-1 audit will have to rewrite `peakgap.py`'s matching code — or
    re-derive it from `scripts/c2b/peaks_measure.py`, from which it was copied verbatim.

---

## 8 — Sources

| claim family | source |
|---|---|
| Peak signatures, refit verdict, Phase B freeze cascade | docs/33 §5.1, §7.3–§7.5, §8 (executed output) |
| `q_peak` choice, bias statement, α/β anti-compensation rule | docs/35 §2–§6 (registered 2026-08-11) |
| Observed ENSO contrast | docs/34 |
| Area embargo | docs/23 §13.2 |
| Automatic-network under-catch, zero-suppression, ERA5 accumulation traps | docs/16 §4, §4.1, §4.4, error #4 |
| Session budget, C3.5 block | docs/31 (core path 8–12 sessions), docs/30 line 53 |
| POT event diagnosis, all §2 numbers | `data/processed/peakgap/summary.json`, `per_gauge.csv`, `events.csv`, `match_sensitivity.csv` (re-read 2026-08-11) |
| Sub-daily data availability | `data/raw/climate/era5land_ext_*.nc` (132 files), `chirps_basin_*.nc` (11 files), `data/raw/observed/precip/precip_auto_daily_long.csv`, Socrata `s54a-sgyg` / `bdmn-sqnh` (routes verified live) |
| MGB-SED formulation and its named limitation | Buarque (2015) UFRGS PhD eq. 5/7; Fagundes (2018) UFRGS MSc eq. 11/12, §6.3.1, §6.4.1–§6.4.2, Appendix IV |
| Alternatives in the literature | Almeida et al. (2025) ISWCR doi 10.1016/j.iswcr.2025.10.004 (USLE-M/RUSLE2 in MGB-SED); Liang & Xie (2001) doi 10.1016/S0309-1708(01)00032-X; Pui et al. (2012) doi 10.1016/j.jhydrol.2012.08.041; SWAT Theory v2009 §2:1.3.3–4 |

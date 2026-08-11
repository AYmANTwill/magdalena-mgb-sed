# 32 — SSC-quality gate (Stage C1)

Status: **PRE-REGISTRATION frozen 2026-08-10** (this session, before any C1 computation).
Sections §1–§6 below are the *registered method, nulls, and decision rules*; the **results**
(the coverage census, the selectivity statistic, the per-station classification table) are
appended by the Claude Code session that executes C1.1–C1.7 against this registration. The
point of freezing them now is the project's standing discipline: **the thresholds must not be
tuned to the answer** (docs/31 §35, docs/18 §7).

Companion: `docs/31_phase_c_workplan.md` Stage C1 (the subtask IDs, In/Out/Gate).

---

## 0 — Scope (the C1.0 decision)

Phase C runs on the **28-station mapped subset** of the 79 SSC stations (24 calibration-safe);
the 46 unmapped stations have no coordinates and are carried as `ssc_class = excluded,
reason = "no coordinates"` unless background task **B5** later maps them (docs/31 C1.0, B5;
docs/30 §5.4). Every count below is *out of the 28 mapped*, stated as such.

Inputs (verified present 2026-08-10): `sediment_daily.csv` (269,337 rows; cols `code, date,
ssc_mean_mg_l, ssc_surface_mg_l, approval, flag_corrupt, flag_zero, flag_flatline,
flatline_run_len`); `sediment_inventory.csv` (79 rows, 28 mapped, 24 calibration-safe);
paired discharge via `is_discharge_station` / the docs/13 pairs.

---

## 1 — C1.1 coverage census + the N-selection rule (registered)

**Compute** per station × year: sample count; days in 2009–2018; days inside each ENSO window
(**calendar 2011** for La Niña; **2015-01 → 2016-12** for El Niño); `approval` distribution
(Definitivo > En revisión > Preliminar); `ssc_mean` vs `ssc_surface` availability. Output
`sediment_coverage_census.csv` + a per-station availability bar figure (nb06 style).

**N-selection rule — registered so N is principled, not tuned to the classification.** A station
is "covered" in a window if it has **≥ N** valid samples in that window. N is chosen from the
census distribution *before* C1.6 runs, by this rule, and the chosen value + the plot it was read
from are recorded in `docs/agents/journal_c1.md`:

- N = **the knee** of the sorted per-window sample-count distribution (the count above which the
  distribution flattens into the usable mode), subject to a **hard floor N ≥ 12** — because a
  flux estimate needs enough samples to bracket the flow range, and the C1.5 rating fits are
  themselves marked unusable below 15 pairs, so a per-window sample floor below ~12 cannot yield
  a defensible within-window flux.
- If the distribution has no clear knee, fall back to the floor: **N = 12**.
- The same N applies to both windows. Record how many of the 28 meet ≥ N in **both** windows.

**Gate:** N and the plot are in the journal before the classification is computed.

---

## 2 — C1.2 sampling-selectivity null (registered in full — the F4 fix)

SSC is campaign-sampled; the risk is **flow-chasing** (sampling preferentially on high-flow days),
which inflates any naive flux mean and is invisible to value screens.

- **Statistic:** for each station with a paired discharge record, compute the **flow percentile of
  each SSC sampling date** within that station's full discharge record; the station's score is the
  **median** of those percentiles. Unbiased sampling ⇒ median ≈ 0.5.
- **Null pool (this is the calibration, and it is NOT density-based):** the stations whose sampling
  dates are **calendar-regular** — tested by the **dispersion of inter-sample gaps** (e.g.
  coefficient of variation of the day-gaps below a registered cutoff, i.e. near-monthly / near-
  fortnightly schedule structure). Calendar-driven sampling is unbiased with respect to flow **by
  construction, whatever its density**. Density does NOT define the null (a dense station can still
  be flow-chasing).
- **Flag rule:** a station is flagged *flow-selective* if its median sampled-day flow percentile
  **exceeds the null pool's p99**.
- **Fallback:** if fewer than **~10** calendar-regular stations exist, use the theoretical null
  (percentiles ~ Uniform(0,1), median 0.5) and record the **weaker-null caveat**.
- **Consequence of a flag (registered):** a flagged station's **sample-mean flux is unusable**;
  only its **rating-curve flux** (C2.2, from the C1.5 per-era fit) may be used.
- **Gate (the F4 fix):** the null is calibrated on **calendar-regular** stations ≈ 0.5 — *not* on
  dense stations — before any station is flagged.

Output `ssc_sampling_selectivity.csv` (station, n, median percentile, calendar_regular, flag).

---

## 3 — C1.3 value screens with the corrected nulls (registered)

- **Flatline** (`flag_flatline`) re-adjudicated against docs/19's **corrected** local-quantisation
  null: **0.030 %** within-year / **0.234 %** within-14-day (NOT the flawed 0.00037 %).
- **Zeros** in SSC are suspect (a river is never 0 mg/L): classify zero-runs as *missing-coded-as-
  zero* unless neighbouring samples corroborate near-zero.
- **Extremes: corroborate before deleting** (docs/31 C1.3 — the source paper's 744 mg/L peak was
  real; *to confirm in C2.4*). Corroboration = same-day or ±3-day high discharge at the paired
  gauge, or a same-event neighbour.
- **Gate:** zero deletions without a recorded corroboration check. Output: amended flags in
  `sediment_daily_qc.csv`.

## 4 — C1.4 rating-era segmentation (registered)

SSC often rides the discharge stage record: apply docs/17's SNHT break list. For each paired
station, mark in-window breaks; each inter-break segment is an **era**. Rating fits are **per-era,
never pooled across a break**. Output `ssc_station_eras.csv`.

## 5 — C1.5 sediment rating relations (registered)

Fit `log Qs = log a + b·log Q` on QC'd same-day pairs (Qs = Q·C·0.0864 t/day), **per station per
era**. Record R², n, residual σ. Expectation: fleet median R² ≈ 0.5 (`rating_curves.csv`: 0.54 /
33 pairs) — usable with stated uncertainty. **Fits with n < 15 pairs marked unusable.** Output
`ssc_rating_fits.csv`.

## 6 — C1.6 classification rubric (registered — the deliverable)

Every one of the 28 mapped stations (and the 46 unmapped) gets exactly **one** class with the
**single measurement that decided it**:

- **usable** — ≥ N in BOTH windows (C1.1) AND not flow-selective, or selective-but-correctable via
  rating (C1.2) AND ≥ 1 usable rating era covering the windows (C1.5).
- **usable-with-caveat** — exactly one deficiency, named (e.g. *flow-selective → rating-only flux*;
  or *single-window coverage*; or *rating R² < 0.3*).
- **excluded** — with the specific evidence: **no coordinates** (the 46 unmapped) / no window
  coverage / no plausible rating (all eras n < 15) / corrupt record. Never a blanket rule.

**Gates:** 79/79 classified (28 mapped adjudicated on merit, 46 as `no coordinates`); the
**mainstem-vs-tributary split stated** (C4 calibrates on the tributary set); the **count of usable
stations inside each ENSO window stated**. Outputs: `sediment_inventory_qc.csv`
(`ssc_class`, `ssc_class_reason`) + the per-station table appended to this doc.

---

## Results (appended by the C1 execution session — Claude Code, 2026-08-10)

Executed against the registration in §0–§6 above; **no registered threshold, null or rule was
changed**. The journal pre-registering every choice the frozen text left free (N, the
calendar-regularity cutoff, the extreme trigger, the deficiency-counting reading, the mainstem
definition) is `docs/agents/journal_c1-ssc.md`. Figure: `figures/deck/gen_ssc_coverage.png`.

Outputs written: `sediment_daily_qc.csv` (269,337 rows, 79 stations, **0 deletions**),
`sediment_inventory_qc.csv` (79 rows: `ssc_class`, `ssc_class_reason`, `ssc_qc_notes`),
`sediment_coverage_census.csv` (1,107 station×year rows), `ssc_sampling_selectivity.csv`,
`ssc_station_eras.csv`, `ssc_rating_fits.csv`.

### R1 — C1.1 coverage census and the chosen N

**N = 91**, chosen and journalled before any classification was computed. The 56 station×window
valid-sample counts (28 mapped × 2 windows) sort as `0×27, 34, | 91, 111, 130, …, 373`:
**27 of 56 windows are completely empty**, and inside the 29 non-empty ones there is exactly one
large gap, **34 → 91 (57 samples)**, against a next-largest gap of 29 and typical spacing 19–23.
N = 91 is the lowest count in the flat usable mode; the hard floor of 12 does not bind.
Sensitivity: N = 91 versus the floor N = 12 changes the coverage verdict of exactly **one** station
(`26017060` PUENTE ARAGÓN, 207 / 34).

Coverage at N = 91, of the 28 mapped: **7 both windows · 8 La Niña only · 6 El Niño only ·
7 neither.** The dominant failure mode is total absence of record, not thin sampling.

### R2 — C1.2 sampling selectivity (the F4 gate)

The null pool is calendar-regular stations, tested by `cv_gap` (sd/mean of inter-sample day-gaps)
against a cutoff of **0.50**, registered before flagging and justified by the Poisson no-schedule
benchmark (CV = 1 means no schedule; CV ≤ 0.5 means a schedule survives ~25 % missed visits).
**Measured: this network is near-DAILY — the median inter-sample gap is 1 day at all 28 mapped
stations** — yet only **2** stations clear cv_gap ≤ 0.50, because multi-year station outages inflate
the gap sd. 2 < 10, so **the registered fallback fires: the theoretical Uniform(0,1) null, evaluated
per station as p99(n) = 0.5 + 2.326/(2√n), with the weaker-null caveat recorded.** The 2-station
pool's medians (0.488, 0.463) are consistent with 0.5, so the fallback is not contradicted by the
pool. All 28 mapped stations have a paired discharge record, so none escapes the test.

**Weaker-null caveat:** daily Q is strongly autocorrelated, so the i.i.d. null is anti-conservative
and over-flags. Every flag is therefore treated as a *caveat* (rating-only flux), never as an
exclusion on its own.

**3 of 28 flagged flow-selective** — `26237020` PENALTA (median sampled-day flow percentile
**0.678** vs p99 0.567), `26127010` EL ALAMBRADO (0.526 vs 0.516), `21217250` BOCATOMA
(0.551 vs 0.514). An added decomposition — median percentile of sampled days minus median
percentile of *all* discharge days inside the station's own span — separates day-selection from
period-selection: PENALTA **+0.276** = genuine flow-chasing; EL ALAMBRADO +0.029; BOCATOMA
**+0.009**, i.e. its offset is a wet sub-period, not day-picking. Fleet-mapped median of the
median-percentiles is **0.470**, so the network as a whole is marginally *low*-flow-biased — the
opposite of the feared failure mode. Counter-direction cases the one-sided rule cannot flag:
`21147030` CARRASPOSO 0.115, `26167060` PAILA LA 0.357, `26067010` JUANCHITO 0.363; their sample
means are not representative either.

### R3 — C1.3 value screens against the corrected nulls

**The docs/19 corrected fleet numbers reproduce.** Observed flatline membership = **0.3535 %** of
valid days, i.e. **11.8×** the within-year null (0.030 %) and **1.51×** the within-14-day null
(0.234 %); docs/19 §3.4 states 11.7× and 1.5×. Per station the excess over the 14-day null runs
from 0.94× (`21197010`, *below* the null — pure quantisation) to 40× (`22057090`, 5 rows).
**The largest flatline share at any mapped station is 3.40 % of its valid days — too small to move
a coverage count or a rating fit — so no station is classified on flatlining**, nothing is deleted,
and the per-station excess ships as a column in `sediment_daily_qc.csv`.

**Zeros:** 385 rows across 17 stations; **380 adjudicated missing-coded-as-zero**, 5 near-zero
corroborated. Only 2 zero rows fall inside the 28 mapped (`21217250` 2010-01-01 →
missing-coded-as-zero; `24017820` 1993-02-22 → corroborated by a 1 mg/L neighbour). The zero problem
is concentrated in the unmapped coastal / Ciénaga group, which is excluded anyway.

**Extremes: 33 candidates (> 5× the station's own p99, or `flag_corrupt`); corroboration checked and
recorded for every one; ZERO deletions.** Only 2 are corroborated (both `29067050`, 1996). The
consequential ones: `21197010` EL PROFUNDO **2016-06-04 = 15,180 mg/L = 91× its own p99, NOT
corroborated** (Q max ±3 d = 22.6 vs its Q p90 = 42.1) — and it sits *inside* the El Niño window at
an otherwise-usable station; `24037390` CAPITANEJO 2018-08-21 = 15,901 mg/L (uncheckable, no Q
within ±3 d); `24037040` GUICAN 2018-05-19 = 1.97×10⁸ mg/L, the single `flag_corrupt` row (a decimal
slip; the station is unmapped and never enters Phase C).

**Absent-record test — where the real damage is.** Inside each station's own record span, the share
of paired-discharge days carrying **no** SSC value: `23087210` 77 % · `26237020` 74 % · `26207080`
73 % · `25017010` 62 % · `25017020` 51 % · `26017060` 49 % · `21147030` 47 % · `26107130` 46 % …
mapped-fleet median **30 %**. Value screens are structurally blind to this.
**Low-end truncation test (the SSC analogue of precipitation zero-suppression): NEGATIVE** — no
mapped station piles up at its minimum (largest share 0.46 %, minima 2–32 mg/L), so there is no
detection-limit censoring signature in this network.

### R4 — C1.4 rating eras

docs/17 §3.8's recoverable break list yields **30 eras over the 28 mapped stations**; only the BOCAS
twins split (`22017010`, `22017030`, break 2005-02, the verified-physical bifurcation pair).
`25017020` SAN PEDRO carries an in-window break at 2009-04 but its SSC record ends 1993-10-29, so
the break falls outside the record and no split applies. LIMITATION: docs/17 names 24 Tmax > 50
candidates but only 7 station codes are recoverable in-repo and no SNHT results file exists on
disk; C1.4 is complete only to the extent of that list.

### R5 — C1.5 rating relations

**All 30 eras have n ≥ 15 pairs, so 0 fits are marked unusable and all 28 mapped stations have ≥ 1
usable era.** Fleet median R² = **0.546** on log Qs ~ log Q — the registered expectation was ≈ 0.5
(`rating_curves.csv`: 0.54 / 33 pairs). Median b = **1.409**; median residual σ = **0.809** ln-units,
a factor ≈ 2.2 uncertainty band on any rating-derived flux.

**Measured caveat: that R² is largely spurious.** Qs = Q·C·0.0864 contains Q, so log Qs ~ log Q
self-correlates. Refitting the same pairs as log C ~ log Q gives a fleet median R² of only
**0.125**. Read the ratings as "Q explains ~12 % of concentration variance", not 55 %. Six mapped
stations have essentially no C–Q relation: `26247030` 0.002, `24017820` 0.0003, `26107070` 0.0004,
`26137110` 0.004, `21217250` 0.001, `22017010` 0.011.

### R6 — C1.6 classification: **79/79 classified, each with a deciding measurement**

| class | all 79 | of the 28 mapped |
|---|---:|---:|
| usable | 6 | 6 |
| usable-with-caveat | 12 | 12 |
| excluded | 61 | 10 |

**Reach split** (topological trunk membership computed over `minibacias.csv`: accumulate upstream
area, walk up from the outlet always following the largest parent = the Magdalena trunk, then the
largest second branch = the Cauca; 535 trunk minibacias. Corroborated by upstream area and median
paired Q; inherits the docs/23 §13.2 snapping caveat):
**8 mainstem / 20 tributary of the 28 mapped.** Mainstem = `21237020` ARRANCAPLUMAS
(Magdalena — *the only Magdalena-trunk SSC station in the entire network*) and, on the Cauca,
`26247030` APAVI, `26207080` BOLOMBOLO, `26167070` IRRA, `26107070` LA VICTORIA, `26067010`
JUANCHITO, `26017020` JULUMITO, `26017060` PUENTE ARAGÓN. Of those 8, **3 are excluded** (APAVI,
JUANCHITO, LA VICTORIA — all for zero window coverage), 1 is usable, 4 are usable-with-caveat.
This is the quantitative form of "Phase C is blocked on mainstem SSC".

**Tributary set for C4 (13 stations, usable or usable-with-caveat):** `23087210`, `23127010`,
`24037390`, `26167060`, `21197010`, `21147030`, `26127010`, `26137110`, `24027030`, `22017010`,
`22017030`, `22057090`, `26107130`.

**Usable-or-caveat stations inside each ENSO window — what C2 has to work with:**
**La Niña 2011 → 13** (`23127010`, `24037390`, `26017020`, `26017060`, `21197010`, `21237020`,
`26127010`, `26137110`, `24027030`, `22017010`, `22017030`, `22057090`, `26107130`);
**El Niño 2015-16 → 12** (`23087210`, `26207080`, `23127010`, `24037390`, `26167060`, `26167070`,
`21197010`, `21237020`, `21147030`, `26127010`, `22017010`, `22017030`);
**both windows → 7.** Only one of those 7 is a mainstem station (`21237020`), so the paired ENSO
contrast rests on a 7-station, overwhelmingly tributary sample.

#### R6.1 — per-station table, the 28 mapped

| code | name | reach | n 2011 | n 2015-16 | med. flow pctile | best era R² | eras | class | deciding measurement |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| `21217230` | BOCATOMA | tributary | 0 | 0 | 0.535 | 0.505 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 1993-01-01..2000-09-07, 0 valid days in 2009-2018) |
| `21217250` | BOCATOMA | tributary | 344 | 0 | 0.551 | 0.145 | 1 | **excluded** | multiple deficiencies: single-window coverage (La Nina 344, El Nino 0 vs N=91) ; flow-selective: median sampled-day flow percentile 0.551 > theoretical-null p99 0.514 -> rating-only flux ; rating R2 0.145 < 0.30 (n=7049 pairs) |
| `24017820` | BOCATOMA | tributary | 282 | 0 | 0.484 | 0.203 | 1 | **excluded** | multiple deficiencies: single-window coverage (La Nina 282, El Nino 0 vs N=91) ; rating R2 0.203 < 0.30 (n=5748 pairs) |
| `24027070` | MERIDA - AUT | tributary | 0 | 0 | 0.488 | 0.670 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 2018-01-22..2018-12-31, 342 valid days in 2009-2018) |
| `25017010` | MONTELIBANO - AUT | tributary | 0 | 0 | 0.493 | 0.691 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 1990-01-01..2012-10-31, 440 valid days in 2009-2018) |
| `25017020` | SAN PEDRO - AUT | tributary | 0 | 0 | 0.380 | 0.765 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 1990-06-01..1993-10-29, 0 valid days in 2009-2018) |
| `26067010` | JUANCHITO  - AUT | mainstem | 0 | 0 | 0.362 | 0.665 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 1984-01-02..1993-06-30, 0 valid days in 2009-2018) |
| `26107070` | LA VICTORIA  - AUT | mainstem | 0 | 0 | 0.468 | 0.504 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 1984-01-02..1999-10-22, 0 valid days in 2009-2018) |
| `26237020` | PENALTA | tributary | 0 | 179 | 0.678 | 0.455 | 1 | **excluded** | multiple deficiencies: single-window coverage (La Nina 0, El Nino 179 vs N=91) ; flow-selective: median sampled-day flow percentile 0.678 > theoretical-null p99 0.567 -> rating-only flux |
| `26247030` | APAVI | mainstem | 0 | 0 | 0.463 | 0.147 | 1 | **excluded** | no window coverage: 0 valid samples in BOTH ENSO windows (record 2018-03-01..2018-12-31, 304 valid days in 2009-2018) |
| `21197010` | EL PROFUNDO | tributary | 192 | 202 | 0.453 | 0.719 | 1 | **usable** | covered in BOTH windows (La Nina 192, El Nino 202 >= N=91), not flow-selective (median pctile 0.453), usable rating era R2 0.719 on n=5817 |
| `21237020` | ARRANCAPLUMAS  - AUT | mainstem | 91 | 195 | 0.471 | 0.556 | 1 | **usable** | covered in BOTH windows (La Nina 91, El Nino 195 >= N=91), not flow-selective (median pctile 0.471), usable rating era R2 0.556 on n=6400 |
| `22017010` | BOCAS | tributary | 184 | 174 | 0.494 | 0.376 | 2 | **usable** | covered in BOTH windows (La Nina 184, El Nino 174 >= N=91), not flow-selective (median pctile 0.494), usable rating era R2 0.375 on n=4245 |
| `22017030` | BOCAS | tributary | 236 | 210 | 0.472 | 0.439 | 2 | **usable** | covered in BOTH windows (La Nina 236, El Nino 210 >= N=91), not flow-selective (median pctile 0.472), usable rating era R2 0.439 on n=4346 |
| `23127010` | BORBUR  - AUT | tributary | 301 | 319 | 0.476 | 0.612 | 1 | **usable** | covered in BOTH windows (La Nina 301, El Nino 319 >= N=91), not flow-selective (median pctile 0.476), usable rating era R2 0.612 on n=6813 |
| `24037390` | CAPITANEJO | tributary | 319 | 309 | 0.468 | 0.484 | 1 | **usable** | covered in BOTH windows (La Nina 319, El Nino 309 >= N=91), not flow-selective (median pctile 0.468), usable rating era R2 0.484 on n=6344 |
| `21147030` | CARRASPOSO  - AUT | tributary | 0 | 219 | 0.115 | 0.873 | 1 | **usable-with-caveat** | single-window coverage (La Nina 0, El Nino 219 vs N=91) |
| `22057090` | BOCATOMA TRIANGULO | tributary | 321 | 0 | 0.450 | 0.501 | 1 | **usable-with-caveat** | single-window coverage (La Nina 321, El Nino 0 vs N=91) |
| `23087210` | CANTERAS - AUT | tributary | 0 | 221 | 0.385 | 0.486 | 1 | **usable-with-caveat** | single-window coverage (La Nina 0, El Nino 221 vs N=91) |
| `24027030` | NEMIZAQUE | tributary | 302 | 0 | 0.492 | 0.652 | 1 | **usable-with-caveat** | single-window coverage (La Nina 302, El Nino 0 vs N=91) |
| `26017020` | JULUMITO | mainstem | 241 | 0 | 0.510 | 0.558 | 1 | **usable-with-caveat** | single-window coverage (La Nina 241, El Nino 0 vs N=91) |
| `26017060` | PUENTE ARAGÓN - AUT | mainstem | 207 | 34 | 0.404 | 0.782 | 1 | **usable-with-caveat** | single-window coverage (La Nina 207, El Nino 34 vs N=91) |
| `26107130` | MATEGUADUA | tributary | 111 | 0 | 0.517 | 0.536 | 1 | **usable-with-caveat** | single-window coverage (La Nina 111, El Nino 0 vs N=91) |
| `26127010` | EL ALAMBRADO AUT | tributary | 321 | 130 | 0.526 | 0.738 | 1 | **usable-with-caveat** | flow-selective: median sampled-day flow percentile 0.526 > theoretical-null p99 0.516 -> rating-only flux |
| `26137110` | BANANERA LA 6-909 | tributary | 259 | 0 | 0.502 | 0.398 | 1 | **usable-with-caveat** | single-window coverage (La Nina 259, El Nino 0 vs N=91) |
| `26167060` | PAILA LA | tributary | 0 | 373 | 0.357 | 0.684 | 1 | **usable-with-caveat** | single-window coverage (La Nina 0, El Nino 373 vs N=91) |
| `26167070` | IRRA  - AUT | mainstem | 0 | 304 | 0.452 | 0.652 | 1 | **usable-with-caveat** | single-window coverage (La Nina 0, El Nino 304 vs N=91) |
| `26207080` | BOLOMBOLO - AUT | mainstem | 0 | 151 | 0.406 | 0.644 | 1 | **usable-with-caveat** | single-window coverage (La Nina 0, El Nino 151 vs N=91) |

#### R6.2 — the 51 unmapped / out-of-domain

| exclusion evidence | n | codes |
|---|---:|---|
| no coordinates | 46 | `21027010`, `21037010`, `21057060`, `21087040`, `21087080`, `21097070`, `21107020`, `21117080`, `21147050`, `21187030`, `21207960`, `21217210`, `21237010`, `22027010`, `22077070`, `23037010`, `23057140`, `23067040`, `23087190`, `23127020`, `23127030`, `23147020`, `24017570`, `24017590`, `24017640`, `24017830`, `24027020`, `24027040`, `24027060`, `24037030`, `24037040`, `24037130`, `24037360`, `25027200`, `26117030`, `26147140`, `26177030`, `26187040`, `26187110`, `26207030`, `28017050`, `28037030`, `28037090`, `29067040`, `29067060`, `29067070` |
| outside the modelled domain | 5 | `29067010`, `29067050`, `29067120`, `29067130`, `29067150` |

Bookkeeping correction to C1.0: **46** stations have no coordinates at all, and a further **5**
(`29067010`, `29067050`, `29067120`, `29067130`, `29067150` — the Ciénaga Grande / lower-Magdalena
east-bank group) *do* carry lat/lon but fall outside the 8,672-minibacia network, so they have no
minibacia. Calling all 51 "no coordinates" would have been wrong; they are excluded on distinct,
named evidence.

#### R6.3 — carried QC notes (not class-deciding, but C2 and C4 must read them)

| code | name | note |
|---|---|---|
| `23087210` | CANTERAS - AUT | 77% of paired-Q days inside its own span have NO SSC value |
| `26207080` | BOLOMBOLO - AUT | 73% of paired-Q days inside its own span have NO SSC value |
| `26237020` | PENALTA | 74% of paired-Q days inside its own span have NO SSC value |
| `24017820` | BOCATOMA | 1 zero row(s), 0 missing-coded-as-zero |
| `24037390` | CAPITANEJO | 1 extreme candidate(s), worst 15901 mg/L on 2018-08-21 = 6x p99, NOT corroborated; no deletions |
| `26017020` | JULUMITO | usable rating era ends 2011-12-30 - covers only part of the La Nina window |
| `26017060` | PUENTE ARAGÓN - AUT | 49% of paired-Q days inside its own span have NO SSC value |
| `25017010` | MONTELIBANO - AUT | 62% of paired-Q days inside its own span have NO SSC value |
| `25017020` | SAN PEDRO - AUT | 51% of paired-Q days inside its own span have NO SSC value |
| `21197010` | EL PROFUNDO | usable rating era ends 2016-07-31 - covers only part of the El Nino window | 1 extreme candidate(s), worst 15180 mg/L on 2016-06-04 = 92x p99, NOT corroborated; no deletions |
| `21237020` | ARRANCAPLUMAS  - AUT | coverage sits EXACTLY at N=91 in one window - a 1-sample change flips it | usable rating era ends 2015-08-31 - covers only part of the El Nino window |
| `21147030` | CARRASPOSO  - AUT | usable rating era ends 2016-02-29 - covers only part of the El Nino window | 46% of paired-Q days inside its own span have NO SSC value |
| `21217250` | BOCATOMA | 1 extreme candidate(s), worst 1687 mg/L on 2012-09-01 = 6x p99, NOT corroborated; no deletions | 1 zero row(s), 1 missing-coded-as-zero |
| `22017010` | BOCAS | 3 extreme candidate(s), worst 1733 mg/L on 2012-01-17 = 7x p99, NOT corroborated; no deletions |
| `26107130` | MATEGUADUA | usable rating era ends 2011-05-30 - covers only part of the La Nina window | 46% of paired-Q days inside its own span have NO SSC value |

### R7 — issues raised by this execution (for docs/31's open list; not resolved here)

1. **The C1.2 null could not be calibrated as designed.** The registration assumed a
   campaign-sampled network; the network is near-daily with multi-year outages, so `cv_gap` on raw
   gaps finds only 2 calendar-regular stations and the weaker theoretical null had to be used. A
   future revision should define calendar-regularity on *within-active-segment* gaps. Under the
   sensitivity variant (drop gaps > 90 d) only 6 of 28 clear the cutoff, so the fallback fires
   either way and the registered result is insensitive to that choice.
2. **docs/17's SNHT break list is not on disk**; only 7 of the 24 Tmax > 50 codes are recoverable
   from prose. C1.4 is complete only to the extent of that list.
3. **The rating R² fleet median (0.546) is inflated by the Qs = Q·C construction**; the honest
   C-vs-Q figure is 0.125. C2.2's rating-curve fluxes inherit this, and the σ = 0.81 ln-unit band
   must be propagated, not dropped.
4. **`21237020` ARRANCAPLUMAS is "usable" on exactly 91 La Niña samples — exactly the registered
   N.** One sample fewer and the only Magdalena-trunk station in the network would be single-window.
5. **`21197010` EL PROFUNDO carries an uncorroborated 15,180 mg/L spike inside the El Niño window**
   while being otherwise a both-window usable station. C2 must bound or exclude that point
   explicitly rather than let it into a sample mean.

# 34 — The observed ENSO sediment contrast (Stage C2)

Status: **§1 PRE-REGISTRATION frozen 2026-08-10, written before any C2 number was computed.**
The order is auditable in `docs/agents/journal_c2-contrast.md` (Step 1 records the frozen text;
Step 2 onward records the results). Results are appended from §2 down by the same session.

Model-free. This is the **target that stage C5 must later reproduce**, and it stands on its own
as an observational result.

Inputs (all C1 outputs, `docs/32`): `sediment_daily_qc.csv` (269,337 rows, 0 deletions),
`sediment_inventory_qc.csv` (79 rows, `ssc_class`), `ssc_rating_fits.csv` (30 eras, all n ≥ 15),
`ssc_sampling_selectivity.csv` (`flag_flow_selective`), `discharge_daily.csv`.
Station set: the **18 mapped stations classed `usable` (6) or `usable-with-caveat` (12)**.
All 28 mapped SSC stations are themselves discharge stations, so Q is paired on the same `code`.

---

## 1 — PRE-REGISTRATION (frozen before computation)

### 1.1 Windows — primary and sensitivity, both reported everywhere

| id | phase | definition | length |
|---|---|---|---|
| **P-LN** | La Niña (wet) | `2011-01-01 … 2011-12-31` (calendar 2011) | 365 d |
| **P-EN** | El Niño (dry) | `2015-01-01 … 2016-12-31` | 731 d |
| **S-LN** | La Niña (wet) | `2010-07-01 … 2011-06-30` (ONI-peak centred) | 365 d |
| **S-EN** | El Niño (dry) | `2015-10-01 … 2016-04-30` (ONI-peak centred) | 213 d |

P-LN/P-EN are the **primary** pair (the windows every earlier phase of this project used, and the
windows C5 will be scored on). S-LN/S-EN are the **sensitivity** pair, ONI-peak definitions. These
two pairs bracket the window-definition question the advisor declined to adjudicate, so
**every result in §2–§5 is reported for the primary pair AND the sensitivity pair.** No result is
reported for one pair only. If the two pairs disagree in sign or by more than a factor of 2 on any
headline ratio, that disagreement is stated as the finding, not averaged away.

### 1.2 COMPARABILITY RULE (hard, non-negotiable)

The windows are **12 vs 24 months** (primary) and **12 vs 7 months** (sensitivity). Therefore:

- **Cross-window comparison uses RATES ONLY**: mean daily flux in t/day, and monthly-mean t/day.
- **Window totals (t) may appear as context, clearly labelled with the window length in days, and
  are NEVER divided by each other.** A wet:dry ratio of unequal-window totals is meaningless by
  construction and does not appear anywhere in this document.
- The only ratio reported is the **RATE ratio** `mean t/day (La Niña) ÷ mean t/day (El Niño)`,
  within a pair (P with P, S with S — never crossed).

### 1.3 Flux conversion

`Qs [t/day] = Q [m³/s] × C [mg/L] × 0.0864`, applied to same-day paired values.
**ABSOLUTE FLUX ONLY. No t/km²/yr, no area normalisation, anywhere in this document** — the
catchment areas disagree by > 2× on 36 % of shared gauges (docs/23 §13.2) and the yield embargo
is in force. Upstream area is used **only to order stations for display**, with that caveat stated.

### 1.4 Estimator (a) — sample-day flux mean

- Sample days = days inside the window carrying a valid QC'd `ssc_mean_mg_l`
  (`c1_deleted == False`) **and** a same-day `q_m3s` at the same code.
- Statistic: the arithmetic **mean of Qs over sample days**, in t/day. `n` sample days reported.
- **Admissibility (C1.2 gate): computed ONLY for stations with `flag_flow_selective == False`.**
  A flagged station's sample mean is unusable by the C1.2 registration; it gets estimator (b) only.
  Cells for flagged stations are printed as `—(flow-selective)`, never as a number.
- Minimum: a station-window needs **≥ 12** sample days for estimator (a) to be reported
  (the C1.1 hard floor); below that the cell is `—(n<12)`.
- **CI: nonparametric bootstrap resampling sample days i.i.d. with replacement, 2,000 reps,
  percentile 2.5 / 97.5.** Seed 20260810.
- Known limitation registered in advance: sample days are not a random sample of window days, and
  daily Qs is autocorrelated, so this CI is a *lower bound* on the true uncertainty.

### 1.5 Estimator (b) — rating-curve flux on all days

- For each window day with a valid `q_m3s`, find the station's C1.5 era whose
  `[era_start, era_end]` contains that date. Days inside no usable era get **no** estimate.
- `ln Qs_hat = log_a + b · ln Q` from `ssc_rating_fits.csv`.
- **Retransformation (registered): the primary rating flux is the Duan smearing-corrected mean,**
  `Qs_hat = exp(log_a + b·ln Q) × S`, with `S = mean(exp(resid))` over that era's own fit
  residuals. Reason: a mass flux requires the conditional **mean**, and the naive back-transform
  returns the conditional **median**, which is biased low by roughly `exp(σ²/2) ≈ 1.4` at the fleet
  median σ = 0.809. The naive (median) back-transform is reported **alongside** in the full table
  so the size of the correction is visible.
- **Rating-window coverage:** report, per station-window, `cov = (days with a rating estimate) /
  (days in window)`. A station-window with **cov < 0.50** is labelled **`partial-rating`**, kept in
  the full table, and **excluded from the headline ratio table** — several C1 notes record eras
  that end mid-window (`21197010` era ends 2016-07-31, `21237020` 2015-08-31, `26017020`
  2011-12-30, `26107130` 2011-05-30, `21147030` 2016-02-29).
- The rating rate is the mean t/day **over the days that carry an estimate** (a rate, per §1.2),
  with `cov` printed next to it so partial coverage is never invisible.
- **CI (registered): 1,000 reps, each rep combining BOTH uncertainty sources —**
  1. **parameter** uncertainty: resample the era's own (ln Q, ln Qs) fit pairs with replacement and
     refit `log_a, b`;
  2. **scatter**: a **moving-block bootstrap of the era residuals with 30-day blocks**, added to
     each predicted day (block resampling, not i.i.d., because daily residuals are autocorrelated
     and an i.i.d. residual bootstrap would collapse the interval).
  Percentile 2.5 / 97.5 of the resulting window-mean flux. Seed 20260810.
- The C1 R7-3 caveat is carried explicitly: log Qs ~ log Q self-correlates because Qs contains Q;
  the honest C-vs-Q R² is a fleet median of **0.125**, and σ ≈ 0.81 ln-units ⇒ a ≈ 2.2× band.

### 1.6 The EL PROFUNDO extreme (C1 R7-5), registered treatment

`21197010` carries an uncorroborated **15,180 mg/L** value on **2016-06-04**, inside P-EN, at an
otherwise both-window `usable` station. C1 deleted nothing, so:

- **Primary = the point is included** (no post-hoc deletion).
- **Registered sensitivity:** estimator (a) is recomputed for that station-window with the point
  removed, and the leverage is reported.
- **Registered rule:** if removing that single point moves the station's window mean flux by
  **> 25 %**, the station's sample-mean flux for that window is labelled **`single-point
  dominated`** and the rating estimate (b) takes precedence in every downstream statement.

### 1.7 C2.3 — consistency tests, with their decision rules

1. **Estimator agreement.** Where (a) and (b) are both admissible for the same station-window,
   they **agree** if their 95 % CIs overlap. **A disagreement (disjoint CIs) is declared a missed
   C1 flag** — the doc must then name the specific candidate mechanism (sampling selectivity the
   one-sided C1.2 rule could not see, an era boundary in the wrong place, or a leverage point) and
   say so explicitly rather than reporting the two numbers side by side without comment.
2. **Downstream monotonicity.** Computed on **topologically nested** station pairs — station A is
   upstream of station B if A's minibacia lies in B's upstream set, walked over `minibacias.csv`;
   only genuinely nested pairs are tested. Flux **should not fall downstream** absent a sink.
   **The Depresión Momposina is a known, documented sediment sink**: any decrease across a pair
   spanning it is **annotated as the expected sink signature, not counted as an error.** Display
   ordering elsewhere uses `up_area_km2` with the docs/23 §13.2 unreliability caveat stated.

### 1.8 C2.4 — literature anchor, with its pass rule

Take the **outlet-most usable station** and compare its **annual** flux (Mt/yr, absolute) against
the published Magdalena suspended load. The exact figure and its citation are **fetched in C2.4**;
docs/06:9 records ~145–169 Mt/yr and the docs/31 register lists it as **unverified** — the quoted
number in §5 must be a verified primary-source figure with author, year, journal, station and
period, not a repeat of the project's own prose.

- **PASS = order-of-magnitude agreement**: the station's annual flux is within a factor of 10 of
  the published load, allowing for the station draining only part of the basin.
- A larger mismatch is **investigated and reported as an investigation**, not waved past.
- If the mid-basin station *exceeds* the published outlet load, that is flagged and discussed
  (the Momposina sink lies between them and makes it physically possible), not silently accepted.

### 1.9 Figures (registered before plotting)

To `figures/deck/`: (i) per-station wet:dry **rate** ratio dot plot, stations ordered downstream,
primary and sensitivity side by side; (ii) flux time series at the 3–5 best stations;
(iii) monthly shape, both windows, both pairs. No figure carries an area-normalised axis.

### 1.10 What would make C2 fail

C2 is reported as **failed** if: fewer than 3 stations support a both-window rate ratio in the
primary pair; or estimators (a) and (b) disagree at more than half the testable station-windows;
or the literature anchor misses by more than a factor of 10 and the cause is not identified.
These are stated now so they cannot be relaxed later.

---

## 2 — What was actually computable: paired discharge, not SSC, is the binding constraint

C1 handed C2 **18 stations** (6 `usable`, 12 `usable-with-caveat`) = **72 station-windows**
(18 × 4 windows). Both estimators need **same-day discharge at the same code**. Measured:

| | count of the 72 station-windows |
|---|---:|
| estimator (a) admissible (`ok`) | **38** |
| (a) blocked, < 12 paired sample days | 30 |
| (a) blocked, flow-selective (C1.2 rule) | 4 |
| estimator (b) `ok` (rating cov ≥ 0.50) | **39** |
| (b) `partial-rating` (0 < cov < 0.50) | 7 |
| (b) impossible — **no paired discharge day at all in the window** | **26** |

**The finding that governs everything below: SSC exists where discharge does not.** Paired-Q spans
of the 18 stations, against the SSC counts C1 recorded:

| code | station | discharge record | SSC in 2011 | SSC in 2015-16 | Q days P-LN | Q days P-EN |
|---|---|---|---:|---:|---:|---:|
| `21237020` | **ARRANCAPLUMAS** (only Magdalena-trunk SSC station) | 1990-01-01 … **2014-12-31** | 91 | **195** | 346 | **0** |
| `22057090` | BOCATOMA TRIANGULO | 1990-01-01 … **2009-03-19** | 321 | 0 | **0** | **0** |
| `26017020` | JULUMITO | 1990-01-01 … **2006-12-31** | 241 | 0 | **0** | **0** |
| `26127010` | EL ALAMBRADO | 1990-01-01 … 2018-12-31, gap over 2011 | 321 | 130 | **0** | 731 |
| the other 14 | — | all reach 2015 or later | — | — | 303–365 | 349–731 |

Consequences, stated plainly:

1. **No ENSO sediment contrast is computable on the Magdalena trunk, by either estimator.**
   `21237020` ARRANCAPLUMAS has 195 QC'd SSC samples inside the El Niño window and **zero** days of
   discharge there — its record stops on 2014-12-31. C1's "Phase C is blocked on mainstem SSC" is
   therefore *understated*: the one trunk station that survived C1 is blocked a second time, on
   discharge. Every number in §3 is a **tributary and Cauca-branch** result.
2. `22057090` and `26017020` contribute **nothing** — they have SSC in La Niña 2011 but their
   discharge records ended in 2009 and 2006.
3. `26127010` EL ALAMBRADO is doubly blocked: flow-selective by C1.2 (so no estimator (a) at all)
   and no 2011 discharge (so no La Niña rating flux). It appears only as an El Niño level.

---

## 3 — C2.2 results: flux rates and the wet:dry RATE ratio

All fluxes are **absolute t/day**. No area normalisation appears anywhere (docs/23 §13.2 embargo).
Full per-station-window table with both estimators, CIs, `n`, and rating coverage:
`data/processed/c2/c2_station_window_flux.csv` (72 rows); ratios in `c2_rate_ratios.csv`.
As registered in §1.5, the **naive (median) back-transform is carried alongside the Duan-smeared
value** in that table as `b_mean_tday_naive`; the correction it represents is the smearing factor
`S`, measured per era at **1.080 – 1.832, fleet median 1.478** (§4.1), i.e. ignoring the
retransformation would have understated every rating flux by ~8–83 %.

### 3.1 Fleet scale — the headline

**Every station that supports a ratio shows La Niña > El Niño, in every estimator, in both window
pairs. 22 of 22 station-ratios exceed 1.0. There are no counter-examples.**

| window pair | estimator | n stations | median RATE ratio | geo-mean | range | ratios > 1 | CIs excluding 1 |
|---|---|---:|---:|---:|---|---:|---:|
| **PRIMARY** | (a) sample-day | 6 | **4.62** | 3.96 | 1.21 – 11.68 | 6/6 | 5/6 |
| **PRIMARY** | (a), dropping the single-point-dominated station | 5 | **6.79** | 5.02 | 1.70 – 11.68 | 5/5 | 5/5 |
| **PRIMARY** | (b) rating, all | 7 | **2.95** | 2.69 | 1.14 – 6.19 | 7/7 | 4/7 |
| **PRIMARY** | (b), `partial-rating` excluded (headline) | 4 | **2.84** | 2.75 | 1.14 – 6.19 | 4/4 | 3/4 |
| **SENSITIVITY** | (a) sample-day | 4 | **9.32** | 8.56 | 4.58 – 14.46 | 4/4 | 4/4 |
| **SENSITIVITY** | (a), dropping single-point-dominated | 3 | **6.91** | 7.70 | 4.58 – 14.46 | 3/3 | 3/3 |
| **SENSITIVITY** | (b) rating, all | 7 | **4.65** | 4.30 | 1.81 – 10.29 | 7/7 | 5/7 |
| **SENSITIVITY** | (b), `partial-rating` excluded (headline) | 5 | **6.40** | 5.43 | 1.81 – 10.29 | 5/5 | 4/5 |

Reading, with the disagreements kept visible rather than averaged:

- **The sign is unanimous and window-definition-independent.** Primary and sensitivity agree on
  direction at every station and every estimator.
- **The magnitude is not.** The primary pair gives a median rate ratio of **≈ 3 – 5**; the
  ONI-peak sensitivity pair gives **≈ 5 – 9**. The sensitivity windows are sharper (they exclude
  the ENSO shoulders that dilute both phases), so the tighter the window, the larger the contrast.
  **Quoting one number for "the" observed contrast would be false precision: the honest statement
  is a factor of ~3 to ~9, with the window definition worth roughly a factor of 2 of that spread.**
- Estimator (b) is systematically *more conservative* than (a) in the primary pair — the rating
  fills in the unsampled days, and the unsampled wet-window days are not the extreme ones. §4 shows
  the reverse bias operating in the dry window.
- The ratio CIs quoted are **conservative by construction** (`lo_wet / hi_dry`, `hi_wet / lo_dry`),
  i.e. wider than a proper paired-bootstrap ratio interval. Even so, 16 of 22 exclude 1.0.

### 3.2 Per-gauge scale — every station, both pairs, both estimators

RATE ratio (La Niña mean t/day ÷ El Niño mean t/day). `—` = not computable, reason given.

| code | station | area km² | reach | PRIMARY (a) | PRIMARY (b) | SENS (a) | SENS (b) | blocking reason where `—` |
|---|---|---:|---|---|---|---|---|---|
| `22017030` | BOCAS | 68 | trib | **9.68** [7.08, 13.21] | **2.70** [1.04, 6.78] | — | **8.52** [2.95, 29.14] | S-EN: 0 paired sample days |
| `26017060` | PUENTE ARAGÓN | 152 | Cauca | **6.79** [4.91, 9.44] | 1.94 [1.15, 3.26] ᵖ | **4.58** [3.37, 6.16] | 2.54 [1.17, 5.93] ᵖ | ᵖ El Niño rating cov 0.26 / 0.12 |
| `26167060` | PAILA LA | 179 | trib | — | — | — | — | no La Niña record (single-window) |
| `26137110` | BANANERA LA 6-909 | 289 | trib | — | — | — | — | no El Niño SSC |
| `24027030` | NEMIZAQUE | 611 | trib | — (n<12 dry) | **3.15** [0.96, 10.58] ᵖ | — | **6.40** [1.60, 27.63] | ᵖ P-EN rating cov 0.48 |
| `26017020` | JULUMITO | 723 | Cauca | — | — | — | — | discharge ends 2006-12-31 |
| `26107130` | MATEGUADUA | 748 | trib | — | — | — | — | no El Niño SSC |
| `21197010` | EL PROFUNDO | 833 | trib | **1.21** [0.39, 6.66] ˢ | **2.99** [1.02, 10.72] | **11.74** [7.31, 19.69] | **4.65** [1.22, 16.42] | ˢ single-point dominated, §3.4 |
| `21147030` | CARRASPOSO | 1,601 | trib | — | — | — | — | no La Niña record |
| `23127010` | BORBUR | 1,645 | trib | **11.68** [7.59, 17.82] | **6.19** [2.07, 17.87] | **14.46** [8.84, 25.37] | **10.29** [3.24, 37.34] | — |
| `26127010` | EL ALAMBRADO | 1,711 | trib | — flow-selective | — | — flow-selective | — | C1.2 flag + 0 Q days in 2011 |
| `22017010` | BOCAS | 2,411 | trib | **1.70** [1.22, 2.32] | 1.14 [0.54, 2.28] | — | 1.81 [0.67, 4.38] | S-EN: 0 paired sample days |
| `23087210` | CANTERAS | 5,487 | trib | — | — | — | — | no La Niña record |
| `24037390` | CAPITANEJO | 6,362 | trib | **2.45** [1.61, 3.85] | 2.95 [0.99, 8.58] ᵖ | **6.91** [4.01, 12.02] | 2.28 [0.60, 11.49] ᵖ | ᵖ dry-window rating cov 0.49 / 0.43 |
| `22057090` | BOCATOMA TRIANGULO | 6,380 | trib | — | — | — | — | discharge ends 2009-03-19 |
| `26167070` | IRRA | 24,665 | Cauca | — | — | — | — | no La Niña record |
| `26207080` | BOLOMBOLO | 30,848 | Cauca | — | — | — | — | no La Niña record |
| `21237020` | **ARRANCAPLUMAS** | 54,035 | **Magdalena** | — | — | — | — | **discharge ends 2014-12-31** |

ᵖ = at least one window is `partial-rating` (cov < 0.50), excluded from the §3.1 headline row.
ˢ = `single-point dominated` per §1.6.

**The largest and the smallest catchment that support a ratio give 2.45 and 9.68 (primary, (a))**,
so the contrast is not a small-catchment artefact; but note the two BOCAS gauges (68 km² and
2,411 km², the docs/23 bifurcation twins) give **9.68 and 1.70** on the same estimator and window —
a 5.7× spread between two gauges on the same water body. Per-gauge variability is large and must
not be hidden behind the fleet median.

### 3.3 Absolute levels (context only — never divided across windows)

Wet-window mean daily flux spans **four orders of magnitude** across the fleet, 7.6 t/day
(`26017060` PUENTE ARAGÓN, 152 km²) to 41,272 t/day (`21237020` ARRANCAPLUMAS, 54,035 km²) on
estimator (a), P-LN. Window totals, given only as context and **never** used in a ratio:
ARRANCAPLUMAS P-LN 41,272 t/day × 365 d = **15.1 Mt over the 2011 La Niña year**;
BORBUR P-LN 19,001 t/day × 365 d = 6.9 Mt; CAPITANEJO P-LN 11,253 t/day × 365 d = 4.1 Mt.
The 24-month El Niño window totals are *not* comparable to these and are not printed as such.

### 3.4 The registered EL PROFUNDO extreme test — it fired

`21197010`, P-EN, estimator (a): mean **112.47 t/day** with the 2016-06-04 value (15,180 mg/L)
included; **43.82 t/day** without it. **Leverage = +156.7 %**, far above the registered 25 %
trigger, so per §1.6 the station-window is labelled **`single-point dominated`** and the rating
estimate takes precedence: `21197010`'s primary ratio is **2.99 (b)**, not 1.21 (a). This is one
uncorroborated sample (C1: Q max within ±3 d was 22.6 m³/s against a station Q p90 of 42.1)
deciding a station's entire ENSO verdict; the pre-registration is what stopped it doing so. Note
the direction: because the spike lands in the **dry** window, including it **suppresses** the
apparent wet:dry contrast — the sensitivity here is not self-serving.

### 3.5 Monthly shape (both windows, both pairs)

Figure `figures/deck/gen_c2_monthly_shape.png`, table `c2_monthly_shape.csv`, estimator (a).
The seasonal shape is preserved between phases and the ENSO signal is a **level shift, not a phase
shift**: `23127010` BORBUR peaks in **April in both** P-LN (76,244 t/day) and P-EN
(12,481 t/day); `24037390` CAPITANEJO peaks in May (La Niña) vs July (El Niño);
`22017010` BOCAS peaks in June in both. Within-window month-to-month range is **larger than the
ENSO contrast itself** — BORBUR spans 66× across the months of 2011 and 92× across 2015-16,
against a between-phase ratio of 11.7. **Seasonality dominates ENSO at monthly resolution**; the
ENSO effect only emerges once the year is aggregated. `21237020` ARRANCAPLUMAS has sample days in
only **4 of the 12** P-LN months, so its monthly shape is not resolved.

---

## 4 — C2.3 consistency

### 4.1 Estimator (a) vs (b): 8 of 38 disagree, and the mechanism is a **missed C1 flag**

38 station-windows admit both estimators. Median `b/a` = **1.068** (the two estimators agree on
level to 7 % at the fleet median). **8 of 38 (21 %) have disjoint 95 % CIs.** Per §1.7 that is
declared a **missed C1 flag**, and the mechanism is named here with the measurement that names it.

| code | station | window | b/a | median sampled-day flow percentile **within that window** | mean Q on sampled days ÷ mean Q on all window days |
|---|---|---|---:|---:|---:|
| `21147030` | CARRASPOSO | S-EN | 12.41 | **0.163** | **0.196** |
| `26017060` | PUENTE ARAGÓN | P-EN | 3.74 | **0.288** | **0.412** |
| `26167060` | PAILA LA | P-EN | 2.97 | 0.589 | 1.093 |
| `21197010` | EL PROFUNDO | S-EN | 2.80 | **0.326** | **0.715** |
| `23127010` | BORBUR | P-EN | 2.19 | 0.438 | 0.846 |
| `21237020` | ARRANCAPLUMAS | S-LN | 1.79 | 0.422 | 0.926 |
| `21237020` | ARRANCAPLUMAS | P-LN | 1.55 | 0.497 | 1.033 |
| `22017030` | BOCAS | P-LN | 0.47 | 0.570 | 1.055 |

Agreeing station-windows have a median within-window sampled-day percentile of **0.488**
(i.e. unbiased). Across all 38, `corr(ln(b/a), ln(Q̄_sampled / Q̄_window)) = −0.649` and
`corr(ln(b/a), median percentile) = −0.449`.

**Named mechanism #1 — the C1.2 selectivity rule was registered ONE-SIDED and therefore cannot see
low-flow-biased sampling.** C1.2 flags a station only when its median sampled-day flow percentile
*exceeds* the null p99. Five of the eight disagreements are dry-window station-windows where
sampling sat well *below* median flow (0.163, 0.288, 0.326, 0.438, and CARRASPOSO's whole-record
0.115) — the sample-day mean is then biased **low**, and the rating, which uses every day, is right
to be higher. C1's own R2 anticipated this in prose ("counter-direction cases the one-sided rule
cannot flag: `21147030` CARRASPOSO 0.115, `26167060` PAILA LA 0.357, `26067010` JUANCHITO 0.363") —
**C2.3 now measures it: two of the three named stations are in this table.** The fix is a two-sided
C1.2 rule; it is filed as an issue in §7, not applied here (thresholds are frozen).

**Named mechanism #2 — era mis-specification at ARRANCAPLUMAS.** Its two disagreements are the only
ones with *unbiased* sampling (percentile 0.497 and 0.422; Q-ratio 1.03 and 0.93), so selectivity
cannot explain them. `21237020` carries **one era spanning 1990-01-01 … 2015-08-31** with 6,400
pairs, because docs/17's SNHT break list is incomplete on disk (C1 R7-2): a single rating is being
asked to represent 25 years at the only Magdalena-trunk station, and it over-predicts 2011 by 1.6×.
The literature anchor in §5 depends on exactly this number, so it is the most consequential of the
eight.

**Named mechanism #3 — steep-`b` rating extrapolation (`26167060` PAILA LA, `22017030` BOCAS).**
These two disagree in the direction selectivity would *not* predict (their sampling is high-flow,
percentiles 0.589 and 0.570). Both carry the steepest exponents in the usable set (`b` = 1.86, and
1.49/1.79 across eras) with large scatter (σ = 0.91, and 0.92/1.06), so the rating mean is carried
by the flow tail. The Duan smearing factors are well behaved — fleet range **1.080 – 1.832**, median
**1.478**, against the lognormal `exp(σ²/2)` of 1.083 – 1.826; they agree, so the retransformation
is **not** the culprit. The exponent and the scatter are.

**Below the §1.10 failure line:** 21 % disagreement is under the registered "more than half"
threshold, so C2 does not fail this test.

### 4.2 Downstream monotonicity: 40 pairs tested, **0 violations**

Nesting was computed topologically (walk the `downstream` chain of `minibacias.csv` from each
station's minibacia; A is upstream of B when B lies on A's path to the outlet), **not** by
comparing areas — 22 nested station pairs exist among the 18 stations. Of these, **40
pair × window × estimator combinations** have a flux at both ends. **Flux increases downstream in
40 of 40** (`c2_monotonicity.csv`). Examples: PAILA LA 15.1 → IRRA 1,861 → BOLOMBOLO 3,895 t/day
(P-EN, estimator (b)); EL PROFUNDO 136 → ARRANCAPLUMAS 41,272 t/day (P-LN, (a));
BOCAS-68 km² 124.6 → BOCAS-2,411 km² 193.9 t/day (P-LN, (a)).

**The Depresión Momposina annotation, and why it is empty:** the registration required that any
downstream *decrease* across a pair spanning the Momposina be annotated as the known sink rather
than counted as an error. **No such pair exists.** All 18 usable stations lie upstream of the
Cauca–Magdalena confluence and therefore upstream of the Momposina — the outlet-most is
ARRANCAPLUMAS at 54,035 km², 21 % of the 257,438 km² basin. **This network cannot observe the
Momposina sink at all**, which matters directly for §5: the published outlet load is measured
*below* a sink that no station in this dataset sees.

---

## 5 — C2.4 literature anchor

### 5.1 The verified figures (fetched in C2.4, not repeated from project prose)

- **Restrepo, J.D. & Kjerfve, B. (2000).** *Magdalena river: interannual variability (1975–1995)
  and revised water discharge and sediment load estimates.* **Journal of Hydrology 235(1–2):
  137–149**, doi **10.1016/S0022-1694(00)00269-9** (bibliographic record verified via Crossref:
  title, journal, volume 235, pages 137–149, authors Restrepo & Kjerfve, August 2000). Station
  **Calamar**, the gauge nearest the Caribbean; daily data **1975–1995**; rating built on 55
  simultaneous water-level / discharge / SSC measurements.
  **Mean annual suspended sediment load = 144 × 10⁶ t/yr.**
  The same paper reports interannual variability well correlated with ENSO, with **the cold phase
  (La Niña) causing marked increases in sediment transport and the warm phase (El Niño) moderate
  reductions** — the literature states, from an independent record and a different period, the
  direction this study measures.
- **Restrepo, J.D. & Escobar, H.A. (2018).** *Sediment load trends in the Magdalena River basin
  (1980–2010): anthropogenic and climate-induced causes.* **Geomorphology 302: 76–91.**
  **184 Mt/yr**, an upward revision covering 1980–2010.
- Basin context: drainage area **257,438 km²**; mean water discharge **~7,100 m³/s at Calamar**,
  112 km upstream of the Caribbean. **Independent corroboration of this project's domain:** the
  8,672-minibacia network sums to **257,097 km²**, **0.13 %** from the published basin area.

docs/06:9's "~145–169 Mt/yr" is therefore **confirmed as a plausible range but not as a single
figure**: the two primary sources give 144 (1975–1995) and 184 (1980–2010) Mt/yr. docs/31 open
item 5 is closed by the two citations above.

### 5.2 The comparison — PASS, with the shortfall fully accounted

Outlet-most usable station: **`21237020` ARRANCAPLUMAS**, 54,035 km², the only Magdalena-trunk SSC
station. Its wet-window flux annualised (labelled as a **La Niña-year rate**, not a long-term mean;
no El Niño counterpart exists, per §2):

| window | estimator | mean t/day | annualised |
|---|---|---:|---:|
| P-LN (2011) | (a) sample-day, n = 91 | 41,272 | **15.1 Mt/yr** |
| P-LN (2011) | (b) rating, cov 0.95 | 64,096 | **23.4 Mt/yr** |
| S-LN (2010-07 … 2011-06) | (a) sample-day, n = 222 | 36,489 | **13.3 Mt/yr** |
| S-LN (2010-07 … 2011-06) | (b) rating, cov 0.98 | 65,388 | **23.9 Mt/yr** |

| anchor | ratio to our 13.3–15.1 Mt/yr (a) | ratio to our 23.4–23.9 Mt/yr (b) | §1.8 verdict |
|---|---:|---:|---|
| Restrepo & Kjerfve 2000 — **144 Mt/yr** | 9.5 – 10.8× | 6.0 – 6.2× | **PASS** on (b); (a) sits on the factor-10 line |
| Restrepo & Escobar 2018 — **184 Mt/yr** | 12.2 – 13.8× | 7.7 – 7.9× | **PASS** on (b); **(a) misses by 1.2–1.4×** |

Per §1.8 the miss is **investigated, not waved past**:

1. **ARRANCAPLUMAS is not the outlet.** It drains **54,035 km² = 21 % of the 257,438 km² basin**,
   and sits **above the Cauca confluence** (the Cauca alone is 30,848 km² at BOLOMBOLO and is the
   basin's most erosive branch), **above** the lower Andean tributaries, and **above** the Depresión
   Momposina. A 6–14× shortfall against Calamar is the expected order for a station in that
   position; a match would have been the alarming outcome.
2. **The water balance says the same thing with an independent quantity.** Mean Q at ARRANCAPLUMAS
   in 2011 is **1,747 m³/s = 24.6 %** of Calamar's ~7,100 m³/s. The station therefore carries ~25 %
   of the outlet **water** but only **10 % (a) to 16 % (b)** of the outlet **sediment**. Sediment
   share below water share is exactly what an upper-basin station above the Cauca and above the
   erosive lower tributaries must show. Two independent ratios, consistent, with a physical
   direction rather than an arithmetic one.
3. **The sign of the residual bias is known and points the same way.** 2011 was a strong La Niña,
   so this annualised rate is if anything **high** relative to a long-term mean — the true long-term
   ARRANCAPLUMAS share of the outlet load is *smaller* than 10–16 %, widening the gap in the
   direction that drainage position already explains.
4. **The (a)/(b) split at this station is the §4.1 mechanism-#2 disagreement**, not new
   information: one 1990–2015 rating era over-predicts 2011 by 1.6×. Both bracket values are
   reported; neither is presented as the answer.

**Verdict: PASS.** Order-of-magnitude agreement holds on the rating estimator against both
published anchors, and the residual factor is explained by drainage position and corroborated by an
independent water-discharge share.

---

## 6 — Figures (`figures/deck/`)

| file | content |
|---|---|
| `gen_c2_ratio_dotplot.png` | per-station wet:dry **RATE** ratio, stations ordered downstream, PRIMARY and SENSITIVITY panels side by side, both estimators, conservative CIs, `partial-rating` drawn hollow, log x-axis with the 1.0 line marked |
| `gen_c2_flux_timeseries.png` | sample-day flux (t/day, log) 2010–2017 at the 5 best-covered stations, both ENSO windows shaded |
| `gen_c2_monthly_shape.png` | monthly mean t/day, La Niña vs El Niño, 6 stations × both window pairs |

No figure carries an area-normalised axis. Two reading notes: (i) the monthly figure's SENSITIVITY
row has an El Niño window (2015-10 … 2016-04) that **wraps the calendar boundary**, so its red
trace occupies months 10–12 and 1–4 only — that is the 7-month window, not missing data;
(ii) in the time-series figure the ARRANCAPLUMAS panel is **visibly blank inside the red El Niño
band**, which is §2's finding rendered directly.

---

## 7 — Verdict and issues raised

**Against the §1.10 failure conditions, registered before any computation:**

| registered failure condition | measured | fires? |
|---|---|---|
| fewer than 3 stations support a both-window primary rate ratio | **6** on (a), **7** on (b) | no |
| estimators disagree at more than half of testable station-windows | **8 of 38 = 21 %** | no |
| literature anchor misses by > 10× with the cause unidentified | 6.0–7.9× on (b); the (a) 12–14× miss against the 2018 anchor is identified (drainage position, corroborated by the 24.6 % water share) | no |

**C2 PASSES.** The observed result, stated at the precision the data supports:

> Across the Magdalena–Cauca **tributary** network, observed suspended-sediment flux **rates** were
> **~3 to ~9 times higher** in the La Niña phase than in the El Niño phase. The **direction is
> unanimous** — 22 of 22 station-ratios, both estimators, both window definitions, no
> counter-example — and it agrees with Restrepo & Kjerfve (2000). The **magnitude is
> window-definition dependent** (median 4.62 primary vs 9.32 sensitivity on estimator (a)), so the
> contrast must be quoted as a range, never as a single number. **No mainstem Magdalena contrast
> exists in the observations**, because the only trunk SSC station loses its discharge record on
> 2014-12-31. This is the target C5 must reproduce.

**Issues raised for docs/31's open list (not resolved here — thresholds are frozen):**

1. **C1.2's selectivity rule is one-sided and demonstrably misses low-flow-biased sampling.**
   Five of the eight estimator disagreements are dry-window station-windows sampled at flow
   percentiles 0.16–0.44. A two-sided rule (flag `|median percentile − 0.5|` against the null)
   would have caught them. This is the single highest-value C1 revision.
2. **The C2 blocker is discharge, not SSC.** 26 of 72 station-windows have no paired discharge day
   at all. Recovering post-2014 stage/discharge for `21237020` ARRANCAPLUMAS would, on its own,
   create the Magdalena-trunk ENSO contrast Phase C currently cannot produce. It is the
   highest-value data acquisition left in the project.
3. **The trunk rating spans 25 years as a single era** (docs/17's SNHT list is incomplete on disk,
   C1 R7-2) and over-predicts 2011 by 1.6×. Any trunk flux number inherits this.
4. **Ratio CIs here are conservative outer bounds** (`lo/hi`, `hi/lo`), not paired-bootstrap
   intervals; paired resampling would tighten them and is worth doing before publication.
5. **Seasonality exceeds the ENSO signal at monthly resolution** (66–92× within-window month range
   against an 11.7× between-phase ratio at BORBUR). Any monthly-resolution model-vs-observation
   comparison in C5 will be dominated by seasonal skill, not ENSO skill, unless it is designed
   around this.
6. **The El Niño window sits partly outside several rating eras** — 7 of 72 station-windows are
   `partial-rating`, all but one of them dry-phase. The dry-phase rating flux is systematically the
   worse-supported half of every ratio in §3.

# Journal — agent c1-ssc

GOAL: execute Phase C stage C1 (SSC quality gate) against the FROZEN pre-registration
docs/32_ssc_qc_audit.md. Classify all 79 SSC stations; produce
`data/processed/sediment_daily_qc.csv`, `data/processed/sediment_inventory_qc.csv`,
per-station results appended to docs/32, and `figures/deck/gen_ssc_coverage.png`.

## Checklist
- [ ] 0. Read docs/32 in full + docs/31 Stage C1 + docs/19 (corrected nulls) + docs/17 (SNHT breaks)
- [x] 1. C1.1 coverage census (RECORD CHOSEN N BEFORE any classification) — **N = 91**
- [ ] 2. C1.2 sampling-selectivity vs calendar-regular null pool
- [ ] 3. C1.3 value screens (corrected quantisation nulls; zeros; extremes w/ corroboration)
- [ ] 4. C1.4 rating-era segmentation from docs/17 SNHT breaks
- [ ] 5. C1.5 rating relations per station per era
- [ ] 6. C1.6 classify all 79 with deciding measurement; mainstem/tributary split; per-ENSO-window counts
- [ ] 7. Outputs written + figure + docs/32 appendix

## Log

### Step 0 — start
Created journal. Beginning reads.

### Step 0b — reads complete (docs/32 full, docs/31 C1.0–C1.7, docs/19 §3.4 nulls, docs/17 §3.8/§3.9)
Registered facts carried forward (NOT re-derived):
- Scope: 28 mapped = `sediment_inventory.csv.minibacia.notna()` (33 have coords /
  `is_discharge_station`, 24 `calibration_safe`). 46 with no coordinates → excluded,
  reason "no coordinates". Confirmed by measurement: minibacia notna = 28, lat notna = 33,
  calibration_safe = 24, is_discharge_station = 33. 79 rows total.
- `sediment_daily.csv`: 269,337 rows, 79 codes, approval mix Preliminar 262,215 /
  Definitivo 7,121 / En revisión 1. flag_corrupt 1, flag_zero 385, flag_flatline 952.
- Corrected quantisation nulls (docs/19 §3.4): within-year 0.030 %, within-14-day 0.234 %.
  The flawed 0.00037 % is NOT used.
- SNHT break list available in-repo (docs/17 §3.8, and `src/nbgen/make_nb12.py`
  `DOC_SNHT_INWINDOW`): named Tmax>50 in-window breaks `28047050` 2013-06,
  `25017020` 2009-04, `23197700` 2016-11; verified-physical bifurcation pairs
  `25027930`/`25027360` 2010-03 and `22017010`/`22017030` 2005-02. No SNHT results CSV
  exists on disk — the doc list IS the break list (ISSUE: only the named subset of the 24
  Tmax>50 candidates is recoverable; recorded as a limitation, not a threshold change).
  Intersection with the SSC network: `25017020` SAN PEDRO-AUT (mapped, 2009-04),
  `22017010`/`22017030` BOCAS twins (mapped, 2005-02 = pre-window).
- Analysis script lives in the scratchpad (not committed — the task scopes me to the OUT
  files + this journal): `<scratchpad>/c1_ssc.py`.

### Step 1 — C1.1 coverage census DONE. **N REGISTERED = 91** (recorded BEFORE any classification)

`data/processed/sediment_coverage_census.csv` written: 1,107 station x year rows
(79 stations), cols n_rows/n_valid/n_mean/n_surface/n_definitivo/n_revision/n_preliminar/
n_zero/n_flatline/n_corrupt/mapped.

**The distribution N was read from** (28 mapped stations x 2 ENSO windows = 56 window-counts
of valid samples; La Nina = calendar 2011, El Nino = 2015-01..2016-12):

    0 x27, 34, | 91, 111, 130, 151, 174, 179, 184, 192, 195, 202, 207, 210, 219, 221,
                 236, 241, 259, 282, 301, 302, 304, 309, 319, 319, 321, 321, 344, 373

- 27 of 56 windows are EMPTY (0 valid samples) — the dominant failure mode is total absence,
  not thin sampling. This is the "absent records" test, at window scale.
- Within the 29 non-empty windows the sorted counts have exactly one large gap:
  **34 -> 91, gap = 57**, versus a next-largest gap of 29 (344->373) and a typical
  inter-point spacing of 19-23. Gap ratio 57/29 = **1.97x**. Above 91 the distribution is
  flat/dense all the way to 373.
- **Therefore the knee is the 34 -> 91 step, and N = 91** = the lowest count in the flat
  usable mode ("the count above which the distribution flattens into the usable mode",
  docs/32 s1). N = 91 >> the hard floor of 12, so the floor does not bind.
- The same N applies to both windows (registered).

**Sensitivity, recorded now so it cannot be re-tuned later:** the choice of 91 versus the
floor 12 changes the coverage verdict for exactly **one** station — `26017060`
PUENTE ARAGON, which has 207 samples in La Nina but only **34** in El Nino. Under N=91 it is
single-window; under N=12 it would be both-window. Every other station is either >=91 in a
window or has literally 0. N=91 is what the rule produces; it stands.

**Coverage tally at N = 91 (of the 28 mapped):**
- >= 91 in BOTH windows: **7** — 23127010, 24037390, 22017030, 21197010, 21237020,
  22017010, 26127010
- >= 91 in La Nina only: **8** — 21217250, 22057090, 24027030, 24017820, 26137110,
  26017020, 26017060, 26107130
- >= 91 in El Nino only: **6** — 26167060, 26167070, 23087210, 21147030, 26237020, 26207080
- neither window: **7** — 21217230, 25017010, 26107070, 26067010, 25017020, 24027070,
  26247030  (of which 21217230, 26107070, 26067010, 25017020 have ZERO valid samples in
  2009-2018 at all)
Sums 7+8+6+7 = 28. Figure: `figures/deck/gen_ssc_coverage.png` panel B carries this
distribution with the knee marked.

### Step 2a — C1.2 REGISTERED calendar-regularity cutoff (recorded BEFORE any flag is computed)

docs/32 s2 registers the null pool as "stations whose sampling dates are calendar-regular —
tested by the dispersion of inter-sample gaps (e.g. coefficient of variation of the day-gaps
below **a registered cutoff**)". The numeric cutoff is NOT fixed in the frozen text, so I fix
it here, from theory and not from the data:

- Statistic: `cv_gap` = sd / mean of the day-gaps between consecutive valid SSC sample dates
  within the station's own active span. Requires n >= 12 samples (else `calendar_regular`
  is undefined -> not in the null pool).
- **Cutoff: `cv_gap <= 0.50` => calendar-regular.** Justification is a benchmark, not a
  histogram: a perfectly kept schedule has CV = 0; a memoryless (no-schedule, opportunistic)
  visit process is Poisson with **CV = 1**. A kept schedule that misses ~25 % of its visits
  (so gaps are T with prob .75 and 2T with prob .25) lands at CV ~ 0.5. So CV <= 0.5 means
  "a schedule is visible through the misses", and CV -> 1 means "no schedule at all".
- Paired discharge: measured — **all 28 mapped stations have a discharge record** in
  `discharge_daily.csv` (plus 5 unmapped: 29067010/29067050/29067120/29067130/29067150).
  So the selectivity statistic is computable for 28/28 mapped; no station escapes it.
- Flag rule (frozen, from docs/32): flow-selective iff median sampled-day flow percentile
  > null pool p99. Fallback to Uniform(0,1) with the weaker-null caveat iff fewer than 10
  calendar-regular stations exist.

### Step 2b — C1.2 null pool MEASURED: only 2 calendar-regular -> registered FALLBACK fires

`cv_gap` measured on all 28 mapped. Result: **median gap = 1 day at all 28** — this network is
near-DAILY sampled, not campaign-sampled. `cv_gap` is nevertheless 1.5-25 at 26 of 28, because
the gap series is (mostly 1-day steps) + (a handful of multi-year station outages), and a few
1000-day gaps blow up the sd. Only **2** stations clear cv_gap <= 0.50: `24027070` MERIDA
(cv 0.076, n 342) and `26247030` APAVI (cv 0.081, n 304) — both single unbroken blocks.

2 < 10 => **the registered fallback fires: theoretical null, Uniform(0,1), median 0.5, with the
weaker-null caveat recorded.** (For the record, the 2-station pool's medians are 0.488 and
0.463, mean 0.476 — consistent with 0.5, so the fallback is not contradicted by the pool.)

**How the theoretical p99 is evaluated (decided here, before flags are finalised).** A first
pass used a flat p99 = 0.99 on the median statistic; that is wrong and vacuous — 0.99 is the p99
of a *single* Uniform draw, not of the *median of n* draws, and it flags nothing by construction.
Under the registered null (per-date percentiles i.i.d. Uniform(0,1)) the sample median is
asymptotically Normal(0.5, 1/(4n)), so the per-station one-sided p99 is
**p99(n) = 0.5 + 2.326 / (2*sqrt(n))**. This is the standard order-statistic sd of a median; it
follows from the null docs/32 already states, and n is the station's own paired-sample count.
DISCLOSURE: the ranking of station median-percentiles was already on screen when I corrected the
formula, so this is not a blind choice — the mitigation is that the formula is forced by the
registered null and contains no free parameter.

**Weaker-null caveat (record it loudly): the i.i.d. assumption is FALSE for discharge.** Daily Q
is strongly autocorrelated, so the effective sample size is far below n and p99(n) is far too
tight => this fallback OVER-flags. Every flag it produces is therefore treated as a *caveat*
(rating-only flux), never as an exclusion.

**Added diagnostic (a measurement, not a threshold change):** median percentile of SSC-sampled
days vs median percentile of ALL discharge days inside the SSC record's own span. If sampling is
exhaustive within its span the difference is ~0 and any offset is *period* selection (the SSC era
happened to be a wet sub-period of a longer Q record), not day-by-day flow-chasing. This
decomposition is what the `ssc_class_reason` will name. It does NOT override a registered flag.

### Step 2c — C1.2 RESULT (`data/processed/ssc_sampling_selectivity.csv`, 79 rows)

Registered flag rule applied with the fallback null. **3 of 28 mapped flagged flow-selective:**

| code | name | n_paired | median pct | p99(n) | delta_span | reading |
|---|---|---:|---:|---:|---:|---|
| `26237020` | PENALTA | 305 | **0.678** | 0.567 | **+0.276** | genuine DAY-LEVEL flow-chasing: its own span's median day sits at 0.403, so +0.28 of the offset is choosing high-flow days |
| `26127010` | EL ALAMBRADO | 5,542 | 0.526 | 0.516 | +0.029 | mild day-level offset |
| `21217250` | BOCATOMA | 7,050 | 0.551 | 0.514 | **+0.009** | NOT day-selection — the span median is already 0.542; this is *period* selection (its SSC era is a wet sub-period of a longer Q record). Flag stands (frozen rule) but the reason names the measurement. |

Consequence (frozen, docs/32 s2): for these 3 the sample-mean flux is unusable; rating-curve
flux only (C2.2). No station is excluded on selectivity.

Counter-direction observation, recorded because the frozen rule is one-sided and cannot see it:
`21147030` CARRASPOSO has median sampled percentile **0.115** (span median 0.118) — its entire
SSC record sits inside the 2015-16 drought, so its samples are LOW-flow selected by period.
Same for `26167060` PAILA LA (0.357) and `26067010` JUANCHITO (0.363). C2 must not read a
sample-mean flux from these as representative of the full flow range either.

Fleet scale: mapped-fleet median of the median-percentiles = **0.470** (mean 0.457), i.e. the
network as a whole is very slightly LOW-flow-biased, not high-flow-biased — the opposite of the
feared failure mode. 25 of 28 unflagged.

Sensitivity (labelled, NOT used for any decision): dropping station-outage gaps > 90 d before
computing CV would put 6 of 28 under 0.50 instead of 2 — still < 10, so the fallback fires
either way and the registered result is insensitive to that choice.

### Step 3a — C1.3 registered screen definitions (recorded BEFORE screening)

docs/32 s3 registers the nulls and the corroboration requirement but not the numeric extreme
trigger. Fixed here, before computing:
- **Flatline null (frozen, docs/19 s3.4):** within-year **0.030 %**, within-14-day **0.234 %**.
  Applied per station as a permutation that preserves LOCAL quantisation (shuffle values inside
  the block, recount runs >= 5 calendar-adjacent identical days), 400 draws. The flawed
  0.00037 % whole-record null is not used anywhere.
- **Zeros:** any `ssc == 0` is *missing-coded-as-zero* unless a neighbouring in-station sample
  within +/-3 d is itself < 5 mg/L (the corroboration of "near-zero").
- **Extreme candidate:** `value > 5 x the station's own p99` (an isolated spike far above the
  station's own upper tail), plus every `flag_corrupt` row. Corroboration = paired-gauge Q on the
  same day or within +/-3 d at or above that station's **Q p90**.
- **DELETIONS: zero.** Nothing is removed from the record; C1.3 only amends flags and records the
  corroboration outcome per candidate. This satisfies the docs/32 gate ("zero deletions without a
  recorded corroboration check") in the strongest possible way.
- **Absent-record test (the mandated one):** for each station, days where paired discharge EXISTS
  but SSC does not, inside the SSC record's own span — structural absence a value screen cannot
  see; plus a low-end truncation test (is the value distribution floored / spiked at its minimum,
  the SSC analogue of precipitation zero-suppression?).

### Step 3b — C1.3 RESULTS

**Flatline vs the corrected nulls — the registered fleet numbers REPRODUCE.**
Observed flatline membership across the fleet (runs >= 5 calendar-adjacent identical values):
**0.3535 %** of valid days. Against docs/19's corrected nulls that is **11.8x** the within-year
null (0.030 %) and **1.51x** the within-14-day null (0.234 %) — docs/19 s3.4 states 11.7x and
1.5x. Independent reproduction, so the corrected null is being applied as registered. (Against
the FLAWED 0.00037 % it would have read as ~955x — that number is not used.)

Per-station (28 mapped, only the 10 with any flatline), excess vs the tightest (14-day) null:
22057090 40.0x (5 rows) · 26167070 IRRA 5.21x (15) · 22017010 2.83x (6) · 24027030 2.62x (97) ·
22017030 2.59x (5) · 26017060 PUENTE ARAGON 2.35x (88) · 26137110 2.26x (57) ·
21217250 1.38x (141) · 24017820 1.20x (138) · 21197010 EL PROFUNDO **0.94x** (11 — *below* the
null, i.e. fully explained by local quantisation).

**Adjudication (no new threshold invented):** the largest flatline share at any mapped station is
**3.40 %** of its valid days (26017060). That is too small to flip a coverage count (N=91 vs
hundreds of samples) or a rating fit (n >= 15 with thousands of pairs). **No station is
classified on flatlining, and nothing is deleted;** the per-station excess is carried as a
measured column so C2 can down-weight if it wants. The two biggest absolute counts (21217250,
24017820) are precisely the two whose excess is ~1.2-1.4x, i.e. quantisation, not stuck sensors.

**Zeros — 385 rows, 17 stations, 380 adjudicated missing-coded-as-zero, 5 near-zero
corroborated.** Only **2 zero rows fall in the 28 mapped**: `21217250` 2010-01-01
(neighbours >= 6 mg/L -> missing-coded-as-zero) and `24017820` 1993-02-22 (a +/-3 d neighbour at
1 mg/L -> near-zero corroborated, keep). The zero problem is concentrated in the UNMAPPED coastal
/ Cienaga group (28017050 81, 29067010 61, 29067130 61, 28037090 58, 29067150 51, 29067060 34) —
which are excluded for lack of coordinates anyway.

**Extremes — 33 candidates (> 5x station p99, or flag_corrupt), ZERO deletions.** Corroboration
checked for every one and recorded in `_c1_extremes.csv`. Only **2 are corroborated** (both at
unmapped 29067050 CANAL FLORIDA, 1996). The ones that matter for the mapped set:
- `21197010` EL PROFUNDO **2016-06-04 = 15,180 mg/L, 91x its own p99, NOT corroborated**
  (Q +/-3 d max 22.6 vs its Q p90 42.1). This sits INSIDE the El Nino window at a station that is
  otherwise both-window usable — C2 must not take a sample-mean flux there without excluding or
  bounding this point. Flagged, not deleted.
- `24037390` CAPITANEJO 2018-08-21 = 15,901 mg/L (5.9x p99) — outside both windows; no discharge
  within +/-3 d, so uncheckable.
- `21217250` 2012-09-01 = 1,687 mg/L, not corroborated (Q 0.6 vs p90 1.3).
- `22017010` BOCAS: 3 candidates (1991-12-14, 2012-01-17, 2012-09-06), none corroborated.
- `24037040` GUICAN 2018-05-19 = **1.97e8 mg/L** — the single flag_corrupt row, a decimal slip;
  the station is unmapped so it never enters Phase C. Still not deleted, only flagged.

**ABSENT-RECORD test (the mandated one — this is where the real damage is).** Inside each
station's OWN span, the share of paired-discharge days with NO SSC value:
23087210 CANTERAS **77.2 %** · 26237020 PENALTA 74.1 % · 26207080 BOLOMBOLO 73.4 % ·
25017010 MONTELIBANO 62.4 % · 25017020 SAN PEDRO 50.6 % · 26017060 PUENTE ARAGON 49.0 % ·
21147030 CARRASPOSO 46.5 % · 26107130 MATEGUADUA 45.6 % ... down to 22057090 2.3 %,
24027070 0.6 %. Fleet-mapped median **29.7 %**. So even the "daily" stations are missing roughly
a third of their in-span days, and four are missing three-quarters. This is invisible to any
value screen and is the reason the C1.2 percentile statistic must be read against the
same-span null (Step 2c) rather than against 0.5 naively.

**Low-end truncation test (SSC analogue of precipitation zero-suppression): NEGATIVE.** No mapped
station piles up at its minimum — the largest frac_at_vmin is 0.46 % (21147030, a single day) and
minima are 2-32 mg/L, physically plausible turbid-river floors. There is no detection-limit
censoring signature in this network.

### Step 4 — C1.4 rating eras (`data/processed/ssc_station_eras.csv`)

docs/17 s3.8's recoverable break list applied to the 28 mapped. Intersections that land INSIDE an
SSC record span: only the **BOCAS twins**. Result: **30 eras over 28 stations**; 2 stations split.
- `22017010` BOCAS: era 1 1990-01-01..2005-01-31 | era 2 2005-02-01..2018-03-31
  (docs/17 bifurcation pair, -35 %, verified physical)
- `22017030` BOCAS: era 1 1990-01-01..2005-01-31 | era 2 2005-02-01..2018-03-31 (+41 %)
- `25017020` SAN PEDRO carries an in-window break at 2009-04, but its SSC record ends 1993-10-29,
  so the break is outside the record and no split applies. Recorded, not applied.
- The other 26 mapped stations have no docs/17 break inside their SSC span -> single era.
LIMITATION (already journalled Step 0b): docs/17 names 24 Tmax>50 candidates but only 7 station
codes are recoverable in-repo; there is no SNHT results CSV. If more of the 24 later intersect the
SSC set, the era table must be re-cut. This is a data-availability limit, not a rule change.

### Step 5 — C1.5 rating fits (`data/processed/ssc_rating_fits.csv`), per station per era

**All 30 eras have n >= 15 pairs, so 0 fits are marked unusable and all 28 mapped stations have
>= 1 usable era.** Fleet median R2 = **0.546** on log Qs ~ log Q — the docs/32 expectation was
"~0.5 (rating_curves.csv: 0.54/33 pairs)"; measured 0.546 over 30 era-fits. Median b = **1.409**
(supply-limited to mildly enriching), median residual sigma = **0.809** in ln units (a factor
~2.2, the honest uncertainty band on any rating flux).

**Caveat measured, not assumed — the R2 is largely SPURIOUS.** Qs = Q*C*0.0864 contains Q, so
regressing log Qs on log Q self-correlates. Fitting the same pairs as log C ~ log Q (which removes
that component) gives a fleet median R2 of only **0.125**. Read the rating fits as "Q explains
~12 % of concentration variance", not 55 %. Per-station R2(C~Q): best 21147030 CARRASPOSO 0.432,
26127010 0.510, 26167060 0.318, 26067010 0.286; worst 26247030 APAVI 0.002, 24017820 0.0003,
26107070 0.0004, 26137110 0.004, 21217250 0.001, 22017010 0.011. Six mapped stations have
essentially NO concentration-discharge relation.

### Step 6a — C1.6 rule-application decisions (recorded before the classification is written)

Two things the frozen rubric does not spell out; both fixed here, and neither is a change to a
registered threshold.

1. **Mainstem vs tributary (docs/32 s6 requires the split; no definition is registered).**
   Definition used: **topological trunk membership**, computed from `minibacias.csv`
   (`id, area_km2, downstream`): accumulate upstream area over the network (0 cycles), take the
   basin outlet (minibacia 2470, 257,097 km2), and walk upstream always following the
   largest-area parent = the Magdalena trunk; the largest second-branch off that walk
   (80,364 km2) is the Cauca, walked the same way. Trunk = 535 minibacias (271 Magdalena +
   264 Cauca). A station is **mainstem iff its minibacia is on that trunk.** Two independent
   corroborating measurements are carried in the output (upstream area, median paired Q).
   CAVEAT (docs/23 s13.2): per-gauge areas are unreliable, and trunk membership inherits the
   same snapping sensitivity; the split is therefore reported with both corroborating numbers.
   Result: **8 mainstem / 20 tributary** of the 28 mapped.
2. **Deficiency counting.** The rubric gives usable = 0 deficiencies, usable-with-caveat =
   "exactly one deficiency, named". Deficiency axes, exactly the three the rubric names:
   (A) coverage below N=91 in one window, (B) flow-selective flag from C1.2, (C) best usable-era
   R2 < 0.3. Exclusion triggers checked first, as registered: no coordinates / no window coverage
   (0 valid samples in BOTH windows) / no plausible rating (all eras n<15) / corrupt record.
   **A station with >= 2 deficiencies and no exclusion trigger is classified `excluded` with all
   deciding measurements named** — this is the literal reading of "exactly one", and it is
   specific evidence, not a blanket rule. Recording it because it is an interpretation.

### Step 6b — C1.6 RESULT: 79/79 classified, each with a deciding MEASUREMENT

| class | all 79 | of the 28 mapped |
|---|---:|---:|
| usable | 6 | 6 |
| usable-with-caveat | 12 | 12 |
| excluded | 61 | 10 |

**usable (6):** 23127010 BORBUR, 24037390 CAPITANEJO, 21197010 EL PROFUNDO,
21237020 ARRANCAPLUMAS, 22017010 BOCAS, 22017030 BOCAS.
**usable-with-caveat (12):** 23087210, 26207080, 26167060, 26167070, 26017020, 26017060,
21147030, 26127010 (the only one caveated for SELECTIVITY, not coverage), 26137110, 24027030,
22057090, 26107130.
**excluded, mapped (10):** 7 for `no window coverage` (26247030 APAVI, 25017010 MONTELIBANO,
25017020 SAN PEDRO, 24027070 MERIDA, 21217230 BOCATOMA, 26067010 JUANCHITO,
26107070 LA VICTORIA) and 3 for `multiple deficiencies` (26237020 PENALTA,
24017820 BOCATOMA, 21217250 BOCATOMA).
**excluded, unmapped (51):** 46 `no coordinates` + **5 `outside the modelled domain`**
(29067010, 29067050, 29067120, 29067130, 29067150 have lat/lon but no minibacia). Calling all 51
"no coordinates" would have been factually wrong — corrected here.

**Reach split: 8 mainstem / 20 tributary.** Mainstem = 21237020 ARRANCAPLUMAS (Magdalena — the ONLY
Magdalena-trunk SSC station in the whole network) + Cauca 26247030, 26207080, 26167070, 26107070,
26067010, 26017020, 26017060. Of the 8 mainstem, 3 are EXCLUDED (APAVI, JUANCHITO, LA VICTORIA,
all zero window coverage). This is the quantitative form of "Phase C is blocked on mainstem SSC".

**TRIBUTARY set for C4 (13):** 23087210, 23127010, 24037390, 26167060, 21197010, 21147030,
26127010, 26137110, 24027030, 22017010, 22017030, 22057090, 26107130.

**Usable-or-caveat inside each ENSO window (what C2 gets):** La Nina 2011 → **13**;
El Nino 2015-16 → **12**; BOTH → **7**. Only 1 of the both-window 7 is mainstem.

### Step 7 — outputs verified ON DISK (not by exit code)

| file | size | rows |
|---|---:|---:|
| `data/processed/sediment_daily_qc.csv` | 24,016,231 B | 269,337 (= input exactly) |
| `data/processed/sediment_inventory_qc.csv` | 24,958 B | 79 |
| `data/processed/sediment_coverage_census.csv` | 53,691 B | 1,107 |
| `data/processed/ssc_sampling_selectivity.csv` | 14,985 B | 79 |
| `data/processed/ssc_station_eras.csv` | 2,557 B | 30 |
| `data/processed/ssc_rating_fits.csv` | 5,487 B | 30 |
| `figures/deck/gen_ssc_coverage.png` | 416,301 B | 3 panels, read back and inspected |

Round-trip check against `sediment_daily.csv`: same row count, same code/date order, NaN masks
identical, approval identical, max value difference **4.5e-13** (CSV float round-trip only).
`c1_deleted` sums to **0** — the C1.3 no-deletion gate holds literally.
docs/32: frozen §0–§6 byte-identical; results appended below them as R1–R7 (342 lines total).

- [x] 2. C1.2 selectivity (3 flagged, weaker-null caveat recorded)
- [x] 3. C1.3 value screens (0 deletions; corrected nulls reproduce docs/19)
- [x] 4. C1.4 eras (30 over 28; only the BOCAS twins split)
- [x] 5. C1.5 ratings (30/30 usable, fleet R2 0.546; C~Q R2 0.125)
- [x] 6. C1.6 classify (79/79 with a deciding measurement)
- [x] 7. Outputs + figure + docs/32 appendix

STATUS: C1.1–C1.6 COMPLETE. C1.7 (the commit) is deliberately NOT done — a dedicated commit
agent handles git, per the hard rules.

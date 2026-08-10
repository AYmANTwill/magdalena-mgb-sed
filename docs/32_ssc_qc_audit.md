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

## Results (appended by the C1 execution session — Claude Code)

*(empty until C1.1–C1.7 run against the registration above; do not pre-fill.)*

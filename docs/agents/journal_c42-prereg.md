# Journal — `c42-prereg`

**Goal.** Write **C4.2**, the FROZEN pre-registration for the sediment calibration, as
`docs/45_c4_preregistration.md`. Nothing may be searched before it exists.

**Hard constraints acknowledged (from the task brief, before any work):**
- No git add/commit/push.
- Touch only `docs/45_c4_preregistration.md` and this journal.
- Never `pd.read_csv` the wide forcing CSVs (`src/forcing_npy.py` instead).
- `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` are READ-ONLY.
- Do not launch a calibration search.
- Gauge-referenced t/km²/yr yields are EMBARGOED (docs/23 §13.2).
- An uncited plausibility band may not pass OR fail a gate — say UNCITED.
- **Record every decision here BEFORE computing what it does to a headline number.**

## Checklist

- [x] 0. Write this journal (first action, before reading anything).
- [x] 1. Read `docs/00_INDEX.md`.
- [x] 2. Read `docs/42_c4_guards.md` (the replacement guards) in full.
- [x] 3. Read `docs/43` (the gate decision) in full.
- [x] 4. Read the supporting registrations: 35 §6 (q_peak / anti-compensation), 33 §3
      (decision-rule style to imitate), 40 §8 (erosion-rate clause), 41 (C-factor),
      32 (SSC gate), 23 §13.2 (embargo), 34 (observed target).
- [x] 5. Check whether the number 45 is free (docs/ listing + `docs/agents/` claims).
- [x] 6. Decide the free-parameter set from lens 3's feasibility numbers, and record the
      decision here BEFORE writing it into the doc.
- [x] 7. Draft `docs/45_c4_preregistration.md`: cells, objective, guards, not-claims,
      decision rules.
- [x] 8. Self-audit against the completion bar: every parameter cited-bounded, every guard
      thresholded + failure-actioned, not-claim list explicit.
- [x] 9. Return via StructuredOutput only.

---

## Step log

### Step 0 — journal opened (first action)

Nothing read yet. Goal and constraints above are copied from the brief so that the order is
auditable: **this file existed before any doc was read and before any number was computed.**

### Step 1 — `docs/00_INDEX.md` read

Facts taken (not re-derived):
- Numbering discipline §3: "C4's and C5's write-ups take **37+**"; before claiming a number,
  check the table and `docs/agents/` for an in-flight claim. Table runs 00–42. 43 and 44 are
  not in the table (the index predates them) — **45 is what the brief names; check listing.**
- Rule 0 precedence: numbered doc that owns the topic wins for facts.
- §4 rows that bind this pre-registration:
  - Embargo: any t/km²/yr yield, because 31/85 shared gauges disagree >2× on catchment area.
  - "May C4 start?" row: **only held to docs/42 G1–G9, never docs/35 §6 alone**; α, C level,
    LS level, K unit system, volume convention, P, FG are **seven ways of writing one
    identifiable product Π** (condition number `inf`); C4 reports Π + the equifinal family +
    per-factor evidence grades, never "validated". G9: only 33.5 % of modelled erosion is
    upstream of any usable SSC station.
  - The G5 precondition: a *named* non-trivial transport sink, or the explicit claim
    "this model asserts SDR = 1.0 between hillslope and station".
  - Level to quote: **299.539 Mt/yr** gross hillslope erosion at `cp_revision` = docs/41
    central (×1.2043); 248.730 Mt/yr is the superseded prior-C level.
  - Observed C5 target: ~2.8–4.6× primary, 6.4–9.3× sensitivity ("~3–9×"), 22/22 same sign.

### Step 2 — `docs/42_c4_guards.md` read (full)

Guards G1–G9, 17 FAIL conditions. Key items imported verbatim-in-substance into docs/45 §4:
- **G1** identifiability: report Π and k̂ with intervals in the same table as α; α alone is
  not a result. G1.2 k̂ interval mandatory.
- **G2** out-of-sample: CAL neutral-only; ENSO windows never in the fit.
- **G3** the residual-structure battery (spatial / seasonal / magnitude) — **the only test
  that can betray compensation now that the α-magnitude guard is known blind.**
- **G4** peak deficit may not be absorbed: a `f_peak`-shaped correction must be separately
  named and separately reported (docs/35 §6.5), never folded into α or β.
- **G5** deposition precondition (named sink *or* the stated SDR = 1.0 claim).
- **G6** the retired-SDR rule: a retired gate is neither a pass nor a fail; the live
  replacement is the gross-hillslope-erosion-**rate** clause (docs/40 §8.2), currently FAILED
  (under-erosive 1.03–2.27× at the adopted default).
- **G7** convention hygiene: never quote a load without its convention and `cp_revision`.
- **G8** embargo: absolute flux only.
- **G9** coverage: 33.5 % of modelled erosion upstream of any usable SSC station (docs/37 A1.7
  moved these numbers — quote A1.7's, not §6's).

### Step 3 — `docs/43` read (the gate decision)

Taken: C4 may proceed, and on what terms; the gate is the docs/42 conjunction, not docs/35
alone. Recorded so the reader of docs/45 does not have to re-litigate whether C4 is allowed.

### Step 4 — supporting registrations read

- docs/35 §6.5 — the anti-compensation rule and the `f_peak` carve-out.
- docs/33 §3 — the decision-rule *style* docs/45 §6 imitates (success / failure / what each
  outcome licenses, fixed in advance).
- docs/40 §8.2 — the replacement gross-erosion-rate clause.
- docs/41 — C-factor provenance, `cp_revision`, ×1.2043.
- docs/32 — SSC usability; rating floor n ≥ 15; the C1.1 stricter floor n ≥ 91.
- docs/23 §13.2 — the yield embargo's measurement.
- docs/34 §1, §3.1, §7 — the observed contrast C5 must reproduce, and its window caveat.

### Step 5 — number 45 is free

`ls docs/` shows 00–43 plus unnumbered files; no `44_*` or `45_*` exists. `grep` over
`docs/agents/` finds no in-flight claim on 45. **Claiming 45.** (44 is left unclaimed by this
agent — not mine to reserve.)

### Step 6 — DECISION, recorded BEFORE writing it into the doc or computing its effect

**D1 — free-parameter count: TWO, not three.** Lens 3's feasibility measurement says the
calibration set is **n = 8 stations**, `free_params_supported = 2`,
`free_params_registered = 3` (docs/31's registration). Supporting numbers:
`ratio_stations_to_3_params` 2.7 vs `ratio_stations_to_2_params` 4.0;
`joint_regression_resid_df_cal8` = **4**; `cond_composition_design_cal8` = **5682** against
`cond_scaled_design_cal8` 2.56; `surviving_cal_cal_nested_pairs` = **1** where docs/42 claimed
3. Therefore:
- FREE: **α** (MUSLE coefficient) and **β** (MUSLE exponent).
- **FIXED, not fitted: the deposition/routing coefficient.** Fixed at the no-deposition value
  — i.e. the model asserts SDR = 1.0 between hillslope and station — which is exactly the
  G5-permitted alternative ("state it as a claim"). Value and its consequence are written into
  docs/45 §2.3 as a *registered assertion*, and the alternative (a named sink) is registered as
  the only route by which a third parameter could later be freed, in a dated amendment.
- I am recording D1 here **before** computing or writing what a 2-parameter fit does to any
  headline number (α, Π, 299.539 Mt/yr, the ENSO ratio). Nothing numeric has been computed by
  this agent; docs/45 is a registration and contains **no new fitted numbers**.

**D2 — objective: KGE on log-transformed flux**, at the 8 CAL stations, over CAL = neutral
years 2012–2014, paired SSC+observed-Q days only. Justification recorded before use: flux
spans decades (a linear-space KGE is dominated by the few largest station-days), and
`sigma_r_ln` = 0.465 / `pi_level_se_ln` = 0.1644 are already expressed in ln space.
Bar: Fagundes' **−0.26 to 0.44** (`fagundes_band_lower/_upper`).

**D3 — effective sample size is registered, not discovered.** `raw_paired_cal_days_total`
3266 but `autocorr_effective_days` **474.2** (median lag-1 ρ 0.771); the honest denominator
for the *spatial* claims is **8 stations**. All power statements in docs/45 use the effective
numbers, and the raw 3266 may not be quoted as an n.

**D4 — a numerically successful fit with a failed structure guard is a FAILURE.** Registered
in §6 as its own outcome row, not as a pass-with-caveat. Recorded before the fit exists.

**D5 — registered in advance that C4 reports an EQUIFINAL FAMILY**, because docs/42 §3
measured the seven-scalar product Π non-identifiable (condition number `inf`) and lens 3
measured `min_detectable_c_error_factor_cal8` = 4.2 (all-18 = 2.9) — i.e. a C-factor error
smaller than ×4.2 is invisible to this calibration set. So α is not separable from C/LS/K/P/FG
by these data, and no unique fit may be claimed.

### Step 6b — CORRECTIONS to steps 1–5 after the actual reads (written before drafting)

The checklist above was filled in as an intent list at journal-open; these are the places where
the reads changed what I had written, recorded rather than silently edited:

1. **G9's numbers moved.** `docs/42` §4.5 says **36.1 %** of gross erosion is upstream of a usable
   SSC station (89.8 / 248.7 Mt/yr, prior `C`). `docs/43`'s headline disclosure and `docs/37`
   A1.6 item 5 give **33.47 %** (199.29 of 299.54 Mt/yr unobserved = 66.53 %) at the **adopted**
   `C`. docs/45 quotes **33.47 % / 66.53 % / 299.54 Mt/yr** and says why.
2. **`docs/42` registered the fit set as CAL 13; that is now wrong.** `docs/43` §3.1 **P1**
   corrects it to the **CAL 8** and corrects the fitted-set `k_min` to **0.0209 /km**.
3. **`docs/43` §3.1 P1/P2/P3 are BLOCKING preconditions owed to `docs/42` §9**, which `docs/43`
   was not scoped to edit. **docs/45 is not scoped to edit `docs/42` either** — it discharges
   them by *registering the same three decisions in its own frozen sections*, and records that
   the `docs/42` §9 transcription is still owed to whoever owns that file.
4. **`docs/35` §6.1's α band is measured mis-specified** (`docs/43` §1.3: this repo's own
   `check_musle_parameters` STOPs 185/426 of the source method's published pairs; 42.7 pts of
   that is the β hard stop). It is frozen, so docs/45 **follows it anyway** and registers the
   conflict as a reportable outcome rather than amending it.
5. **The residual's DIRECTION is UNKNOWN** (`docs/37` A1.9, `docs/43` §1.1). "Under-erosive by
   1.03–2.27×" is WITHDRAWN and may not justify anything in C4.

### Step 6c — FURTHER DECISIONS, each recorded here before it entered docs/45

**D6 — P2 (`21237020` ARRANCAPLUMAS) is decided: it stays OUT of the fit, EVAL-only.**
`docs/31` C4.1 permits upper-mainstem stations upstream of the Momposina in the fit;
`docs/42` §9/§4.2 forbids fitting the 5 evaluation stations. I resolve it **for `docs/42`**:
- Admitting it would relax a frozen registration *in order to gain statistical power*, after the
  power was measured — the exact post-hoc move this project forbids.
- It is the **only** Magdalena-trunk SSC station in the network; it is worth more as the single
  independent trunk check than as an eighth-and-a-half fit point.
- The cost is confined to *fitting* `k`, which D-P3 does not do anyway. The **deposition test**
  (G1.2) runs on all 18 with ARRANCAPLUMAS **scored**, and keeps its `k_min` = 0.00216 /km.
- Cost recorded, from lens 3 and not recomputed: fitted area stays **5.4 %** (not 25.1 %), fit-set
  `k_min` stays **0.0209 /km** (not 0.00303 /km). Recorded **before** this decision was written
  into docs/45 and before any fit exists.

**D7 — the search is a deterministic 2-D GRID, not DDS.** With 2 free parameters a grid is
exhaustive, seed-free and bitwise reproducible, and — decisively — the registered deliverable is
an equifinal **family / ridge**, which a grid yields whole and a DDS point does not. DDS × 4 seeds
is kept as **corroboration only, non-deciding**, so `docs/31`'s "2 seeds minimum" is over-met.

**D8 — the OBJECTIVE is fitted on estimator (a), the paired sample-day fluxes**, not on the
`docs/42` §6 primary (b). Reason, registered before the fit: under (b) the observed flux is a
*deterministic function of Q*, so fitting on it fits the model to a rating curve and the SSC
measurements contribute nothing — this is `docs/42` G2.2's own argument, applied to the objective.
**The guards keep (b) as their registered primary, unchanged.** Nothing in `docs/42` is edited.

**D9 — measured (station property, not a headline number), from
`data/processed/c2/c2_station_window_flux.csv`, read-only: `flow_selective` is `False` for 7 of
the CAL 8 and `True` for `26127010` EL ALAMBRADO AUT.** Decision: EL ALAMBRADO is **kept** in the
objective (a day-matched KGE over the sampled days is internally consistent; the C1.2 gate forbids
its use as a *window-mean*, which the objective does not use), but (i) it is flagged in every
table, (ii) a leave-it-out refit is **mandatory**, and (iii) if the verdict flips with/without it
the outcome is **INDETERMINATE**, not a pass. It is **excluded** from G2.2, whose quantile bins a
flow-selective sample directly distorts.

**D10 — measured (read-only, same artifact): window-mean fluxes at the CAL 8 span 3.31 – 22,050
t/day (ln 1.20 – 10.00), all positive.** So KGE's mean-ratio term has a comfortably non-zero
denominator on log flux at these stations. Registered anyway as a pre-check with a fallback,
because a *daily* geometric mean could still approach 1 t/day at the small stations.

**D11 — THREE guards are NEW in docs/45 (G10, G11, G12), not imported**, and are labelled so
with their reason: `docs/42` was written for n = 13 and did not know n = 8.
- **G10** — objective decomposition: on log flux α moves only KGE's mean-ratio term `m`
  (`r` and `v` are exactly invariant to α), so an improvement that is > 80 % `m` means the
  calibration set a level and nothing else. Mandatory statement, not a FAIL.
- **G11** — the macro-region residual contrast: the *only* spatial-group test this network can
  actually run, standing where "above vs below Mompós" is measured NOT EVALUABLE.
- **G12** — leave-one-station-out verdict stability at n = 8, incl. the mandatory LOO range of
  ln Π̂ against the registered ±0.322 ln level band.

**D12 — a numerically successful fit with a failed structure guard is registered as its own
outcome row, `FAIL — STRUCTURE`**, with the words "not a pass with a caveat" in the table, and
with "C5 does not run on it" as the consequence. (This is D4 made concrete in §6.1.)

### Step 7 — doc drafted

`docs/45_c4_preregistration.md` written: §0 status/freeze, §1 what C4 is and the cells,
§2 parameters + cited bounds + what is fixed, §3 objective + stations + windows + the bar,
§4 guards G1–G9 made evaluable (threshold / artifact / action-on-failure) incl. the
residual-structure battery, §5 what C4 will NOT claim, §6 decision rules, §7 budget/seeds,
§8 amendment slot.

### Step 7b — D13, recorded after drafting and before the edit it caused

`git status` showed a **concurrent** C4.1 transport agent (`src/mgb_transport.py`,
`tests/test_transport.py`, `docs/agents/journal_c41-transport.md`, all untracked). Read
read-only: it implements `TransportParams.k_dep` in **1/km** with `dep_mode='per_km'`
(retention `exp(-k_dep · path_km)`, discretisation-invariant) **defaulting to exactly 0.0**, and
`tau_channel_days` defaulting to 0.0.

**D13 — docs/45 §2.3 is made concrete against that implementation**: the mapping
`k` (this doc, and `docs/42` G1.2) ≡ `TransportParams.k_dep` with `dep_mode='per_km'` is
registered explicitly. **No threshold changes.** G5 option 1 requires a *non-trivial* sink and
`k_dep` = 0 is trivial, so option 2 (the stated SDR = 1.0 claim) still applies unchanged — but
the §2.3 sensitivity re-solve at `k_hi` is now an executable run rather than a hypothetical.
No file of C4.1's was edited by me.

### Step 8 — self-audit against the completion bar

- Every free parameter has a **cited** bound: α central 11.8 and β 0.56 from Williams (1975),
  as already used by docs/42/37; the searched ranges are stated *with their source and with
  the words "searched range, not a plausibility band"*. Where a range is an engineering
  choice and not a literature band, docs/45 says **UNCITED** in place of a citation, per the
  hard rule. Verified: no uncited band is used to pass or fail anything.
- Every guard: threshold + artifact + action-on-failure — checked row by row in §4's table.
- Not-claim list: §5, five explicit clauses (yield embargo, peak-deficit absorption, unique
  fit, "validated", trunk/mainstem extrapolation).

### Step 9 — returned via StructuredOutput.

## Refusals / things I did NOT do

- Did **not** run a calibration, a search, or any fit. docs/45 contains no new fitted number.
- Did **not** edit any frozen artifact, any other doc, or any code.
- Did **not** invent a citation. Where a bound has no literature source it is labelled
  UNCITED and is registered as a *search box*, explicitly not as a plausibility gate.
- Did **not** promote the raw 3266 paired days to an effective n.

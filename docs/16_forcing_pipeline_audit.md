# 16 — Forcing pipeline: audit, discoveries, errors and open items

> **STATUS — 2026-08-12. LIVE as a knowledge base; its *status framing* is not.**
> **What this document is for:** the rainfall + PET pipeline record. §4 (defects found in the
> data), §5 (errors made in development) and **§6 (traps)** are still true, nothing in them is
> retracted, and they are why CLAUDE.md says *"Do not touch precipitation or ERA5 code before
> reading §6."* Read it for those.
> **What has changed since it was written:** it predates Phase B entirely. Phase B has since run
> and **CLOSED on the adopted configuration H2E**, and Phase C (sediment) is **ACTIVE** — so every
> *status*, *next-step* and *still-blocked* statement below is stale and is back-annotated in
> place at **§1, §7, §8, §9 and §11**. Its forcing numbers are the **v1** field; the adopted
> forcing is **v2** (see [docs/00_INDEX.md](00_INDEX.md) § *"Forcing versions — v1 / v2 / v3,
> stated once"* — v1 and v2 are **both gauge-only**, and there is no v3).
> **Where current status lives:** `progress_map.html` (RULE 0: for status, the tracker wins), then
> [docs/00_INDEX.md](00_INDEX.md) and CLAUDE.md "Phase status".

Complete record of the rainfall + PET forcing work: what was built, what was found wrong in the
data, what was got wrong during development, and what is still outstanding.

Organised by pipeline step. Read [§4 Discoveries](#4--discoveries-defects-found-in-the-data) and
[§6 Traps](#6--traps-reference-things-that-silently-produce-plausible-wrong-numbers) first if you are
picking this up cold — they contain the non-obvious knowledge.

---

## 1 — Current state

| Component | State |
|---|---|
| Conventional gauges (IDEAM DHIME) | 294 stations, 2008-2018, **repaired** (see §4.1) |
| Automatic gauges | 94 stations — assessed and **rejected** as forcing |
| CHIRPS v2.0 daily | 2009-2017, 9 years, 0.05°, basin-clipped |
| ERA5-Land | 108 basin + 108 strip → **108 mosaicked** `ext` files, 2009-2017, hourly |
| Minibacias | 8672, 257,097 km² |
| **Rainfall forcing** | 4018 days × 8672 minibacias, no gaps |
| **PET forcing** | 3287 days × 8672 minibacias |
| **Model period** | **2009-01-01 → 2017-12-31 (3287 days)** — bounded by ERA5, not rainfall |

> ⚠ **The table above is the v1 state. Two rows are superseded — noted 2026-08-12.**
> **Model period.** The adopted **v2** bundle spans **2008-01-01 → 2018-12-31, 4,018 days**, not
> 3,287. Owning doc [docs/18](18_hydrology_journal.md) §14.2: *"period assertion
> `DATES.equals(want)` → **True**, 4,018 days"*; CLAUDE.md fixes the convention — *"2008 warms up,
> 2009-2018 is scored."*
> **PET forcing.** No longer the binding constraint. [docs/18](18_hydrology_journal.md) §14.1:
> *"**Open item 3 is closed.** PET now spans the full rainfall record, so the model period is no
> longer clipped to 2009–2017 by ERA5."*
> Anyone sizing an array or a window off this table gets the **v1** shape.

**Phase A (model inputs) is complete.** ~~Phase B (water balance + discharge calibration) has not
started. Phase C (sediment) remains blocked on mainstem SSC data.~~

> ⚠ **CORRECTED 2026-08-12 — both clauses are stale.** The struck sentence is kept because it is
> the state of belief when this document was written; it is not the state of the project.
>
> - **Phase B ran, and is CLOSED.** CLAUDE.md "Phase status": *"**Phase B (water balance +
>   discharge calibration): CLOSED on H2E**"*. The closing decision is
>   [docs/30](30_phase_c_plan.md) §1: *"**Phase B closes on the input-ceiling result, with H2E as
>   the adopted configuration.**"* The parameter record is [docs/26](26_phase3_refit.md) —
>   read its §5.1 before quoting any fitted parameter, and its 2026-08-10 Addendum for the
>   adoption.
> - **Phase C is ACTIVE, not blocked.** [docs/30](30_phase_c_plan.md) header, verbatim: *"It
>   supersedes the 'Phase C blocked' line in older docs."* The measured form of what the phrase
>   actually meant is [docs/32](32_ssc_qc_audit.md) §R6 — **79/79 SSC stations classified**, 28 of
>   them mapped to minibacias, **18 usable or usable-with-caveat** — and *"`21237020`
>   ARRANCAPLUMAS (Magdalena — **the only Magdalena-trunk SSC station in the entire network**)"*,
>   which §R6 calls *"the quantitative form of 'Phase C is blocked on mainstem SSC'."*
>
> ~~For where Phase C stands **today** — including that stage **C4.3, the sediment calibration
> search, is formally BLOCKED** ([docs/47](47_c4_entry_verdict.md):
> *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not start.**"*)~~ — read `progress_map.html` and
> [docs/00_INDEX.md](00_INDEX.md), not this document.
>
> **⚠ THAT FORWARD-POINTER IS ITSELF SUPERSEDED — REFRESHED 2026-08-19.** It was written
> 2026-08-12 and was true then; the struck text is kept, not quoted as current. **Where Phase C
> stands today: PHASE C IS COMPLETE.** **C4.3 RAN** — [docs/55](55_c43_verdict.md), verdict
> **RAILED / EXPLORATORY, NOT adopted** — and **C5 is COMPLETE** —
> [docs/56](56_c5_enso_application.md): the model **reproduces** the observed ENSO contrast,
> **18/18** stations, median rate ratio **3.05×**. The 2026-08-11
> `C4.3-BLOCKED-UNTIL-LS-LANDS` verdict ([docs/47](47_c4_entry_verdict.md)) was the **entry
> condition** and has been **discharged** (the LS act landed: `ls_formulation =
> buarque_2015_dg`). Live status is still `progress_map.html` and
> [docs/00_INDEX.md](00_INDEX.md), not this document.

---

## 2 — Pipeline order

```
DHIME downloads (two collaborators, by department)
  └─ src/organize_precip_regions.py         consolidate → regions/<dept>/
  └─ src/build_precip_gauges.py             QC: dedup, 0-400 mm screen, coords
  └─ src/repair_precip_zero_suppression.py  NEW — see §4.1
  └─ notebook 10                            dataset selection + preprocessing
  └─ notebook 11                            per-minibacia forcing (rainfall + PET)

ERA5-Land:  src/download_era5.py + download_era5_strip.py → src/mosaic_era5.py
CHIRPS:     src/download_chirps.py
```

---

## 3 — Per-step record

### 3.1 `src/organize_precip_regions.py`

Consolidates both collaborators' DHIME downloads into `regions/<department>/`.
**98 CSVs across 20 departments.**

- ⚠️ **Open bug.** It globs `BASE/*.zip` unconditionally. `regions.zip` now sits in that folder, so
  re-running would create a phantom `regionszip` department with 98 duplicate CSVs. Guard the
  filename or move the archive before re-running.
- ⚠️ `_cordoba_x/descargaDhime.csv` is parked outside the working set by its underscore prefix.
  Córdoba has only 1 CSV — the thinnest of 20 departments. Confirm the exclusion was deliberate.

### 3.2 `src/build_precip_gauges.py`

De-duplication, 0-400 mm/day screening, flatline/sparse station removal, out-of-basin filtering,
coordinate backfill. Produces 294 stations / 686,752 station-days.

- ❗ **Structural limitation.** It screens outlier *values*. It cannot detect *absent* records, which
  is how the zero-suppression defect (§4.1) survived it.

### 3.3 `src/repair_precip_zero_suppression.py` *(new)*

Detects and repairs zero-suppressed series. Two complementary tests, either of which flags a station,
both gated on `span_frac < 0.85`:

| Test | Threshold | Rationale |
|---|---|---|
| Dry-day fraction | `< 0.15` | Healthy gauges here are dry on ~47 % of records |
| Neighbour ratio | `> 1.8` | Station annual ÷ median of 6 nearest neighbours; healthy population ~0.9 |

**Both are needed.** The dry-fraction test misses stations that retain *some* zeros — SAN LUIS
`21130040` has a normal dry fraction of 0.40 yet is 2.5× its neighbours. The neighbour test would fail
if a whole *region* were suppressed together (all ratios ≈ 1), which the dry-fraction test still
catches.

Results: **70 of 294 stations flagged (24 %)** — dry_frac 39, both 16, **neighbour-only 15**.

### 3.4 `src/download_chirps.py` *(new)*

Yearly global p05 netCDF (~1.15 GB each), clipped to the basin, global file deleted after subsetting
(~8 MB/year kept). Three large downloads beat ~1100 daily GeoTIFFs.

### 3.5 `src/mosaic_era5.py`

Joins each basin file (−77.0…−72.9) with its east strip (−72.8…−72.3) → full corrected domain.
108 files, grid 101 × 48. Requires `xarray` + `netCDF4`, which were **absent** and are now declared
in `requirements.txt`.

### 3.6 Notebook 10 — rainfall dataset selection and preprocessing

| § | Content |
|---|---|
| 1 | The zero-suppression defect: diagnostic, repair, before/after |
| 2 | Conventional vs automatic gauges |
| 3 | CHIRPS vs gauges, 9 years, including the day-convention lag test |
| 4 | **Our own IDW field measured with the identical metric** |
| 5 | Verdict |

### 3.7 Notebook 11 — per-minibacia forcing

| § | Content |
|---|---|
| 1 | Gauge QC: availability heatmap, double-mass homogeneity |
| 2 | Minibacia centroids from the label raster |
| 3 | IDW `k`=6, per-day weight renormalisation, `k`=20 adaptive fallback |
| 4 | Rainfall field maps + seasonal cycle + ENSO series |
| 5 | Provenance flags |
| 6 | LOOCV + spatial-consistency check |
| 7 | FAO-56 Penman–Monteith PET |
| 8 | Water balance and ENSO contrast |
| 9 | Export |

**Outputs** (`data/processed/`): `forcing_minibacia_precip.csv`, `forcing_minibacia_pet.csv`,
`forcing_minibacia_provenance.csv` (`id,lon,lat,area_km2,fallback_days,d_nearest_km,flag`).

---

## 4 — Discoveries: defects found in the data

### 4.1 Zero-suppressed gauge series ❗ *the significant one*

**70 of 294 stations contained only rain days — their dry days were never exported by DHIME.**

| | Flagged | Healthy |
|---|---|---|
| Dry-day fraction | 0.11 | 0.47 |
| Neighbour ratio | 1.62 → **1.11** after repair | 0.88 |
| Annual total | 3,863 → **1,794** mm/yr | 2,034 |

Worst case GUACAMAYO `25020030` at **11,833 mm/yr** in a region receiving ~2,000-2,500.

**Why it corrupted the forcing:** in IDW a gauge contributes only on days it reported. A
zero-suppressed gauge therefore joins the weighted average exactly when it is raining there and is
masked out when dry — it can only ever pull estimates **up**. This produced circular wet "bullseyes"
in the mean-annual rainfall map.

**Repair:** absent days inside each station's active span inserted as 0.0 mm, marked
`Inferido_seco`. Gauge-mean annual **2,904 → 2,304 mm/yr**. 121,785 dry days inferred.

**Validation:** the repair had to move totals into a plausible range *and* bring neighbour ratios
down — and it does, landing flagged stations on top of the healthy population rather than anywhere
arbitrary. That the correction predicts where they should end up is the strongest evidence the
diagnosis is right.

⚠️ **7 stations remain >1.8× their neighbours after repair** (1,978-4,557 mm/yr). Plausible
magnitudes, so likely genuine orographic hotspots — but unverified.

### 4.2 The `día pluviométrico` day offset

Conventional gauges are read at 07:00 local, so a gauge "day" runs 07:00→07:00. Shifting CHIRPS
against the gauges:

| lag | median daily *r* |
|---|---|
| −2 | 0.093 |
| **−1** | **0.304** |
| 0 | 0.160 |
| +1 | 0.136 |

A one-day realignment **nearly doubles** correlation. This is a calendar artefact, not a skill
deficit — any raw daily correlation quoted without it understates CHIRPS badly.

**Does it matter for PET?** Measured: mean bias between UTC-day and 07:00-07:00 windows is
**−0.000 mm/day**. The shift redistributes PET between adjacent days without changing totals
(15.8 % day-to-day scatter, zero bias). Rainfall is spiky so its day definition matters; PET is
smooth so it does not.

⚠️ **Still matters for calibration.** Discharge is very likely midnight→midnight. Resolve before
calibrating hydrographs, or routing and recession parameters will absorb a ~7 h timing error and look
well-calibrated for the wrong reason.

### 4.3 Interpolation inflates wet-day frequency

| Metric | IDW (leave-one-out) | CHIRPS raw |
|---|---|---|
| P99 ratio vs gauge | 0.73 | 0.72 |
| Wet-day frequency error | **+18.3 pts** | **−1.4 pts** |
| Volume bias | +1.1 % | −5.8 % |
| Daily *r* | 0.41 | 0.31 |

**CHIRPS improved at every cleaning stage — which is itself evidence.** CHIRPS never changed; only
the gauge reference did:

| | Pre-repair | 55-station repair | 70-station repair |
|---|---|---|---|
| CHIRPS volume bias | −13.6 % | −7.6 % | **−5.8 %** |
| CHIRPS wet-day error | −6.2 pts | −2.6 pts | **−1.4 pts** |

Every time the reference got cleaner, CHIRPS looked better against it. That strongly suggests CHIRPS
was closer to the truth throughout, and that the **residual −5.8 % may itself be leftover gauge error**
— plausibly the untouched 5-20 % dry-fraction band (§7.6) and the 7 residual stations (§4.1) — rather
than a CHIRPS deficiency. Do not treat −5.8 % as an established CHIRPS bias to correct against.

**This reversed the notebook 10 verdict.** An earlier version rejected CHIRPS for damping extremes;
our own field damps them identically. Averaging six gauges manufactures wet days — a day counts as
wet if *any* contributor rained enough. CHIRPS is **7× better** on wet-day frequency.

Nuance: MGB needs *areal* rainfall, and a true areal average legitimately has more wet days and lower
peaks than a point gauge. Part of the smoothing is physically correct. We cannot separate correct
areal smoothing from excessive interpolation smoothing.

### 4.4 Automatic network under-catch

**19 %** below the conventional network on co-located pairs (reported as 31 % before the repair — the
inflated gauge totals exaggerated it). Physically expected: wind deflection, evaporation between tips,
mechanical under-registration at high intensity.

### 4.5 Non-issues, checked and cleared

- **ENSO ratio vs gauge density.** Gauges/day differ (183 in 2011 vs 153 in 2015-16), but on a strict
  fixed station set the ratio is 1.59× vs 1.57× on all pairs — a 1 % difference. Not a confound.
- **The 6,841 mm/yr maximum.** IDW is an average and cannot exceed its inputs, so it faithfully
  reproduced bad gauge data rather than inventing anything.

---

## 5 — Errors made during development, and their fixes

Recorded because several were caught only by diagnostics, not by the sanity checks written for them.

| # | Error | Consequence | Fix |
|---|---|---|---|
| 1 | Validation used `ds.time`; ERA5 coord is `valid_time` | **Deleted 30 valid mosaic files.** Recovered — sources intact | Check coord names before validating |
| 2 | `isel` on `number`/`expver` (scalar *coords*, not dims) | Notebook run failed | `drop_vars` for scalar coords |
| 3 | `\"\"\"` inside an `r"""…"""` generator string | Escapes landed literally; syntax error | Use `'''` inside raw strings |
| 4 | `ssrd` daily total taken as max over the UTC day | **Radiation +7 %**, PET inflated with it | Exclude hour 0 (see §6.1) |
| 5 | Zero-suppression keyed on `dry_frac` alone | Missed the worst stations entirely | Added neighbour-ratio test |
| 6 | Claimed "QC was sound" from 0.372 % spatial-consistency | That test structurally cannot see missing zeros | Don't infer absence from an outlier test |
| 7 | Predicted CHIRPS drizzle inflation before measuring | Verdict written against the data | Measure first |
| 8 | Read a CSV mid-flush, reported it truncated | False alarm | Check field counts, not just line counts |
| 9 | `| tail -25` on nbconvert masked a non-zero exit | "Executed" a notebook that never ran | Don't pipe commands whose exit code matters |
| 10 | Repair script compared two different annual-total definitions | Printed a rise where there was a fall | Compare like with like |

---

## 6 — Traps reference: things that silently produce plausible wrong numbers

### 6.1 ERA5-Land

- **`valid_time`, not `time`.** Code written against `ds.time` fails outright.
- **`number` / `expver` are scalar coords, not dims** → `drop_vars`, not `isel`.
- **`ssrd` is accumulated from 00 UTC and resets — and the 00:00 stamp carries the *previous* day's
  completed total.**

  ```
  01-01 00:00 : 18.68 MJ   <- the whole of 31 Dec
  01-01 01:00 :  0.00      <- accumulation restarts
  01-01 23:00 : 20.35      <- the real total for 01 Jan
  01-02 00:00 : 20.35      <- carried into the next day
  ```

  | Method | MJ/m²/day | |
  |---|---|---|
  | Sum of hourly values | ~200 | ❌ ~10× too high |
  | Max over the UTC day | 19.06 | ❌ +7 %, picks the carry-over |
  | **Max over 01:00-23:00** | **17.82** | ✅ |
  | Value at 00:00 next day | 17.83 | ✅ same answer |

  ⚠️ The "18-22 MJ/m²/day is plausible for the tropics" sanity check **does not catch this** — the
  inflated 19.06 sits comfortably inside the band. Only comparing methods against the raw hourly
  series exposed it. A plausibility band catches gross errors, not 7 % ones.

- **Hourly, not daily.** 744 timesteps for a 31-day month.

### 6.2 DHIME / IDEAM

- Missing values are blanks, **not zeros** — except in the zero-suppressed series where absent days
  really are dry (§4.1). Opposite conventions in the same dataset.
- `día pluviométrico` runs 07:00→07:00 local.
- Approval levels: mostly *Definitivo*; some *Preliminar* / *En revisión*.

### 6.3 IDW interpolation

- **Weights must be renormalised per day** over the gauges that actually reported. The matrix is only
  ~66 % filled; fixed weights let missing gauges contribute implicit zeros.
- Averaging **inflates wet-day frequency** (§4.3) — inherent, not a bug.
- IDW cannot exceed the maximum of its inputs. An implausible interpolated value always traces to an
  implausible gauge.

### 6.4 Tooling

- **Python `zipfile` is ~32× slower than 7-Zip** on this machine (0.39 vs 12.4 MB/s) — 8 KB reads
  through Defender's real-time scan. `Add-MpPreference -ExclusionPath 'C:\dev\magdalena-mgb-sed'`
  (admin shell) fixes it permanently.
- `jupyter nbconvert` is not on PATH; use `python -m nbconvert`.
- Wide `to_csv` writes appear incomplete while flushing — verify field counts, not file size.

---

## 7 — Not done / open items

> ⚠ **Read-out appended 2026-08-12. Phase B has since run and closed, so this register is no
> longer a to-do list.** Each item below carries its outcome and the doc that owns it. Original
> wording preserved.

### ~~Blocking Phase B~~ → **Phase B ran and closed on H2E ([docs/30](30_phase_c_plan.md) §1)**

1. **Day-convention alignment between rainfall and discharge** (§4.2). Rainfall 07:00→07:00, discharge
   likely midnight→midnight.
   > **STILL OPEN, 2026-08-12, and its owner is now [docs/17](17_discharge_qc_audit.md).** It was
   > *absorbed*, not resolved. docs/17 §4: *"All 2,443,316 raw `Fecha` stamps are `00:00` … —
   > consistent with a midnight→midnight calendar-day mean, but the averaging window **cannot be
   > proven from the export** … Allow ±1 day slack in event-scale lag analysis; immaterial at
   > monthly aggregation."* Carried as docs/17 §5.2 item 4.
2. ~~**Discharge dataset QC.** Never audited.~~ **DONE — [docs/17](17_discharge_qc_audit.md) is the
   audit**, and it applied exactly the scrutiny asked for here: it found the gauge→minibacia
   mapping broken for half the network (§3.1), ran SNHT break detection and the energy-floor
   triage, and its §3.10–§3.11 carry the neighbour-test iteration back onto precipitation. Given
   precipitation hid a defect this severe, apply the
   same scrutiny — especially a neighbour-ratio equivalent.

### ~~Forcing improvements (v2)~~ → **the repair landed as v2; the merge did not**

> ⚠ **Naming trap, flagged 2026-08-12.** "v2" in this section is the **older, CHIRPS-inclusive**
> sense and is *not* what `model_inputs_v2/` contains. The canonical definition is
> [docs/00_INDEX.md](00_INDEX.md) § *"Forcing versions — v1 / v2 / v3, stated once"*: **v2 = the
> zero-suppression repair + deterministic IDW, still GAUGE-ONLY**, and it is the adopted forcing;
> a CHIRPS-merged forcing would be **v3** and **does not exist**.

3. **CHIRPS quantile-map merge.** Stratify by elevation band and hydrographic zone (bias is
   structured), then conditional merging so gauges dominate where they exist. Expected: wet-day error
   18.1 → ~3 pts, better-constrained headwaters. **Validate by re-running the notebook 11 LOOCV** — if
   it doesn't beat the baseline, say so.
   > ~~**Expected**~~ → **BUILT, MEASURED, AND REJECTED TWICE. No forcing file was ever written.**
   > It was built exactly as specified here (`src/merge_chirps_gauges.py`, stratified by elevation
   > band × hydrographic zone). Owning read-out [docs/18](18_hydrology_journal.md) §15 —
   > *"The CHIRPS-gauge merge: **built, validated, and NOT adopted**"*: the LOOCV gate **passed**
   > (median daily r **0.447** > 0.429) and the **volume gate failed** (2,188.5 mm/yr, +7.5 %).
   > The registered repair (H-CHIRPS, [docs/33](33_c2b_preregistration.md) §1) was then executed
   > and was a **no-op**: docs/33 §1 — *"The registered intervention turned out to be a **no-op**:
   > the quantile maps already included the inferred-dry days, so **the diagnosed cause in docs/18
   > §15.3 was wrong**."* [docs/18](18_hydrology_journal.md) §15.5 records the re-run as
   > bit-identical, the inferred-dry days as **25.9 %** of the fit input, and the conclusion:
   > *"**no route to a passing volume gate exists inside the merge code**."* One **untested**
   > hypothesis survives — the 139 stations still reporting rain-selectively after the repair,
   > whose missing days are not in the record at all and therefore cannot be put into a pool by any
   > change to the merge code. **This section's "Expected" numbers were never achieved, and no
   > reader may conclude a fix is waiting.**
   > *(docs/33 §1's own read-out pointer says "see §7"; §7 of docs/33 is the H-PEAK read-out. The
   > CHIRPS read-out is docs/18 §15.5. docs/33 is frozen, so the pointer stands as written.)*
4. **Orographic correction.** Plain IDW ignores elevation; headwater rainfall is interpolated from
   valley stations with no lapse adjustment. Material in an Andean basin.
5. **The 7 residual >1.8× stations** (§4.1).
6. **The 5-20 % dry-fraction band.** The 0.15 threshold is conservative; sensitivity untested.

### Housekeeping

7. **`regions.zip` glob bug** (§3.1).
8. **Reference document deletion never executed** — the destructive-command guard blocked it four
   times. `Protocolo_descarga_*.docx`, `Explanation_script_MGB_SA_Magdalena.pdf`,
   `notebooks/06_data_inventory.html` and `delivery/` are still on disk.
9. **`data_Final/` + `data_Final.zip`** (~14 GB) — gitignored, regenerate with
   `python src/build_data_final.py all`.

---

## 8 — Proposed next steps, in order

> ⚠ **EXECUTED. Read-out appended 2026-08-12 — all four ran, and item 4's premise is superseded.**
> Kept verbatim because the *order* it proposed turned out to be right: step 2 was run before the
> merge, and it is what made the merge evidence-driven rather than argued.
> 1. **DONE** → [docs/17](17_discharge_qc_audit.md) (the discharge QC audit).
> 2. **DONE** → notebooks 13/14 and [docs/26](26_phase3_refit.md). The rationale below was correct:
>    the calibration did show input-driven error, and [docs/22](22_dry_phase_diagnosis.md) §4.7
>    quantified it as the **r ≈ 0.57 ceiling** inherited from the rainfall field.
> 3. **DONE, and NEGATIVE** → the merge was built and **rejected twice**; see the §7 item 3
>    read-out above and [docs/18](18_hydrology_journal.md) §15/§15.5. *"no route to a passing
>    volume gate exists inside the merge code."* **No v3 forcing exists.**
> 4. **Premise superseded** → Phase C is **ACTIVE**; [docs/30](30_phase_c_plan.md) header: *"It
>    supersedes the 'Phase C blocked' line in older docs."*
>    **(Refreshed 2026-08-19: "ACTIVE" was the state at this read-out's date. Phase C is now
>    COMPLETE — C4.3 ran and RAILED, [docs/55](55_c43_verdict.md); C5 is complete,
>    [docs/56](56_c5_enso_application.md). See the §1 refresh.)**

1. **Discharge dataset QC** — apply the §4.1 methodology (neighbour-relative anomaly detection, not
   just value screening).
2. **Notebook 12: MGB-SA water balance in Python** on this forcing → simulated discharge → calibrate
   against IDEAM gauges. *Rationale:* LOOCV only shows how well gauges predict each other. NSE/KGE
   against observed hydrographs is the first test of whether the rainfall is good enough **for its
   purpose**. If discharge reproduces well, further forcing work is wasted; if it is systematically
   biased, the CHIRPS merge becomes evidence-driven rather than argued.
3. **CHIRPS merge (v2)** — only if step 2 shows rainfall-driven error.
4. **Phase C sediment** — ~~still blocked on mainstem SSC data~~ → **ACTIVE.**
   [docs/30](30_phase_c_plan.md) header: *"It supersedes the 'Phase C blocked' line in older
   docs."* See the §7 item 3 and §1 read-outs above for what the phrase meant once measured
   ([docs/32](32_ssc_qc_audit.md) §R6).

Note: MGB-SA proper runs as a **QGIS plugin** and needs `mini.gtb` plus MGB-format forcing files. The
Python water balance in step 2 is a *diagnostic*, not a replacement for the production run.

---

## 9 — Key numbers

> ⚠ **These are the v1 numbers. Noted 2026-08-12 — the table is NOT the adopted forcing.**
> "Final" meant final *for the 70-station repair*. A second, larger repair followed (the
> selectivity detector: **153** stations, 240,158 inferred-dry days,
> [docs/18](18_hydrology_journal.md) §10) and produced **v2**, which is what `model_inputs_v2/`
> holds and what H2E was fitted on. The rows that moved most, with their v2 successors from the
> owning doc [docs/18](18_hydrology_journal.md) §14.1–§14.2:
>
> | row here (v1) | v2 value | owner |
> |---|---|---|
> | Basin-mean rainfall **2,206 mm/yr** | **2,073.1 mm/yr** (2008–2018) · **2,036.4 mm/yr** (2009–2017) | §14.2 / §14.1 |
> | PET **3.40 mm/day ≈ 1,255 mm/yr** | **3.41 mm/day**; basin PET **1,251.6 mm/yr** | §14.1 / §14.2 |
> | LOOCV daily *r* 0.467 / 0.398 / 0.313 by band | gauge-only median **0.429** over 287 gauges (bands 0.481 / 0.426 / 0.343) | §14.1 · §15.2 |
>
> **Trap 9 of [docs/18](18_hydrology_journal.md) §7 applies to every row:** *"Interannual rainfall
> variability here is ±21 % … No basin-mean rainfall figure means anything without its window
> attached."* Quote the window with the number, and quote the version with both — see
> [docs/00_INDEX.md](00_INDEX.md) § *"Forcing versions — v1 / v2 / v3, stated once"*.

Final values, after the 70-station repair and the `ssrd` radiation fix.

| Quantity | Value |
|---|---|
| Basin area / minibacias | 257,097 km² / 8,672 |
| Gauge matrix | 4018 days × 294 gauges, **68.4 % filled**, median 200 reporting/day |
| Basin-mean rainfall | **2,206 mm/yr** (6.04 mm/day) |
| Annual range across minibacias | 734 – 6,371 mm/yr |
| Seasonal cycle | bimodal; driest Jan (2.7 mm/day), wettest Oct (8.6) |
| Gap cells before fallback | 118,124 (0.34 %) → **0 after `k`=20 pass** |
| Radiation | **17.2 MJ/m²/day** |
| PET | **3.40 mm/day ≈ 1,255 mm/yr** |
| Water balance | P 2,176 · PET 1,255 · **surplus 922 mm/yr** |
| ENSO rainfall ratio 2011/(2015-16) | 1.54× · 98 % of minibacias wetter in 2011 |
| ENSO PET | 1,167 mm/yr (2011) vs 1,303 (2015-16) — El Niño higher, amplifying the contrast |
| Provenance | `G` 25.8 % · `GC` 57.1 % · `C` **17.1 %** of basin area |
| LOOCV daily *r* | 0.467 (<10 km) · 0.398 (10-30) · **0.313 (>30 km)** |
| LOOCV bias | +0.7 % (<10 km) · −0.4 % (10-30) · **+6.2 % (>30 km)** |
| Spatial-consistency suspects | 2,700 station-days (0.336 %) |

**Effect of the two late fixes** — the `>30 km` bias halved, which matters because that band *is* the
ungauged headwaters:

| | 55-station repair | **70-station + radiation fix** |
|---|---|---|
| Gap cells | 0.51 % | **0.34 %** |
| Basin rainfall | 2,262 mm/yr | **2,206** |
| Radiation | 18.7 MJ/m²/day | **17.2** |
| PET | 3.62 mm/day | **3.40** |
| LOOCV bias >30 km | +11.8 % | **+6.2 %** |

⚠️ **Notebook 11 prints its radiation sanity band as "18-22 MJ/m²/day".** The corrected 17.2 now falls
*below* it. 17.2 is right for a cloudy Andean basin — the 18-22 band describes clear tropical
conditions. Widen the printed band to ~15-22, or the next reader will treat a correct value as a
failure. *(Fixed — band widened to 15-22 in both the notebook 11 generator and its markdown prose.)*

## 10 — Update: station-outage repair bug (found by the discharge QC pass)

`repair_precip_zero_suppression.py` inserted a dry day for **every** raw-missing calendar day inside
a flagged station's active span — including multi-month *station outages*, where the gauge reported
nothing at all, wet or dry. ALGECIRAS `21105030` is the clean example: three genuine outages
(2012-05→2013-12, 2015-07→2017-12, 2018-01→2018-08 — 20, 30, 8 months) were filled with `0.0`,
fabricating a multi-year drought landing squarely inside the calibration window (annual mean read
719 mm/yr; the neighbouring stations average ~1,400+).

**Fix:** a `SILENCE_GAP_DAYS = 60` guard — raw-missing runs at or above it are left absent, not
infilled; shorter runs (consistent with "reports rain, omits dry") are infilled as before.

**Result:** 31 of 294 stations affected, 12,656 station-days excluded from infill.
ALGECIRAS corrects **719 → 1,396 mm/yr**. ALBANIA `24050110` (the other SNHT-flagged repaired
station) barely moves (99 days) — confirming its break is a **genuine unresolved anomaly**, not a
repair artefact; it should be investigated separately, not assumed fixed by this change.
Basin gauge-mean annual: 2,304 → **2,327 mm/yr**. Notebook 11 was re-run on the corrected data.

## 11 — Does the zero-fill introduce bias? Yes. Measured, and bracketed.

First, a distinction that matters: **station series are never interpolated in time.** Three separate
operations are involved, and only one is interpolation at all.

| Operation | What it does | Interpolation? |
|---|---|---|
| Zero-suppression repair | Writes `0.0` on missing days inside 70 flagged stations' spans | No — inserts **zeros** |
| IDW (notebook 11) | Per minibacia-day, weighted mean over gauges *that reported that day*, weights renormalised daily | Yes — **spatial**, never temporal |
| `k`=20 fallback | Widens the neighbour set when all 6 nearest are silent (0.36 % of cells) | Spatial |

Imputing a station's own gaps and then treating the result as an observation would double-count the
neighbours' information; that is why it is not done. But the zero-fill is a substantive assumption,
and it can be tested.

### The test: what do neighbours say fell on the days we write 0.0?

For each flagged station, the leave-one-out IDW estimate from its 6 nearest neighbours, split by
whether the station reported that day:

| | Neighbour estimate |
|---|---|
| On days the station **did** report | 8.08 mm/day |
| On days we **fill with 0.0** | **2.64 mm/day** |
| Ratio | **0.30** |

Those days were genuinely much drier — the fill is directionally right — **but they were not zero**:
on 40 % of them neighbours indicate >1 mm.

### Three independent signals show the fill over-corrects

1. **Post-repair dry-day fraction overshoots**: flagged stations now sit at **0.532** against healthy
   **0.465**. The repair made them drier than the population they should resemble.
2. **Annual totals undershoot**: flagged **1,829** vs healthy **2,034** mm/yr → **−205 mm/yr**.
3. **Bracketing**: filling with the *full* neighbour estimate instead would give 2,292 mm/yr —
   overshooting by +258 in the other direction.

So the truth is bracketed: **1,829 (fill 0) < ~2,034 < 2,292 (fill neighbour)**. Back-solving, the
true expectation on filled days is ≈ **1.17 mm/day**, about 44 % of the neighbour estimate — i.e.
roughly half the filled days were genuinely omitted zeros (the defect this repair targets), and
roughly half were ordinary missing days on which rain fell.

*Assumption behind the −205 figure:* that flagged stations are not climatologically drier than the
healthy population. If they sit in genuinely drier locations the over-correction is smaller.

**It remains a good trade.** Before the repair those stations carried a **+90 % wet bias**
(3,863 vs 2,034); now they carry a **−10 % dry bias**. Basin-wide residual ≈ (70/294) × 205 ≈
**−49 mm/yr (~−2 %)**, spatially concentrated around those 70 stations.

### The more consequential finding: missingness is not random (MNAR)

**Healthy, untouched stations show the same ratio (0.31 vs 0.30).** Network-wide, gaps fall on drier
days — reporting is correlated with rainfall.

This corrects a claim made earlier in this document. The per-day renormalised masked mean was
described as the honest, unbiased way to handle gaps. **It is not unbiased.** On any given day the
stations that are missing are disproportionately the dry ones, so the gauges that *do* report
over-represent wet conditions, and the IDW estimate is biased slightly **wet** on gappy days. No
amount of masking fixes this — it is a property of the sampling, not of the estimator.

### The four measured forcing biases, together

| Bias | Direction | Magnitude |
|---|---|---|
| Zero-fill over-correction | dry | −205 mm/yr on 70 stations (~−2 % basin) |
| **MNAR gap selection** | **wet** | untested magnitude — partially offsets the above |
| IDW wet-day inflation | more wet days | **+18.3 pts** |
| IDW extreme damping | lower peaks | **P99 ratio 0.73** |

The first two act in opposite directions, which is some comfort but not a justification.

**Recommended handling:** document rather than re-impute. Re-imputation reintroduces the
double-counting problem and would need its own validation. Two things genuinely help: (a) the CHIRPS
merge (v2) is *independent of whether an IDEAM observer showed up*, so it does not share the MNAR
mechanism — an argument for the merge beyond anything previously measured; and (b) down-weighting
`Inferido_seco` days in the IDW rather than treating them as full observations, which the `approval`
column already makes possible.

> ⚠ **Read-out on (a), appended 2026-08-12. The argument was never refuted; the merge was.**
> CHIRPS really is independent of observer attendance, and the merge was built on exactly this
> reasoning — but it was **rejected twice by its volume gate** and no forcing file was written
> (see the §7 item 3 read-out; owning docs [docs/18](18_hydrology_journal.md) §15/§15.5 and
> [docs/33](33_c2b_preregistration.md) §1). The MNAR premise did *not* fail locally: §15.5
> measured the merged field as *"very nearly unbiased against the gauges themselves"* (median
> per-gauge bias **+2.00 %** merged vs **+1.73 %** gauge-only) — *"A field that is unbiased where
> it can be tested and +7.5 % over the basin puts its whole surplus in the terrain with no gauge
> to test it."* So the merge does not fix the MNAR problem it was argued to dodge; it relocates
> the surplus into ungauged terrain. **Do not read (a) as a pending improvement.**
> Note also the naming: the merged field would be **v3**, not v2 — see
> [docs/00_INDEX.md](00_INDEX.md) § *"Forcing versions — v1 / v2 / v3, stated once"*.
>
> **(b) is the one that was adopted and is still true.** The repair's inferred-dry days are in
> `precip_gauges_daily_qc_v2.csv` with `approval == 'Inferido_seco'`, and §15.5 measured what they
> are worth on the volume side: *"the repair's inferred dry days were already removing **105.6
> mm/yr, 41.0 % of the surplus**"* — with **+152.1 mm/yr** left *after* that lever is pulled all
> the way.

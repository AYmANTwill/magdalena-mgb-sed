# magdalena-mgb-sed

MGB-SED suspended-sediment modelling of the Magdalena–Cauca basin (Colombia), ENSO contrast
study: La Niña 2011 (wet) vs El Niño 2015–16 (dry). UMNG internship, advisor F. J. Briceño-Zuluaga.

## Read these first

- `docs/16_forcing_pipeline_audit.md` — **the knowledge base**: pipeline order, data defects found
  (zero-suppressed gauges!), development errors, and a traps reference (ERA5/DHIME/IDW pitfalls that
  produce plausible wrong numbers). Do not touch precipitation or ERA5 code before reading §6.
- `docs/17_discharge_qc_audit.md` — discharge counterpart (if present).
- `docs/22_dry_phase_diagnosis.md` — **read before touching calibration.** All three standing
  hypotheses for the El Niño failure were measured and refuted (one was backwards); the binding
  constraint is `r ≈ 0.57`, inherited from the rainfall field, not any parameter.
- `docs/18_hydrology_journal.md` — the Phase B record: verdict (§5), refuted claims (§6), traps
  (§7), open items (§8), and the forcing follow-up (§9–§12: surplus, zero-suppression repair,
  deterministic IDW, energy-floor gauge triage).
- `docs/23_gauge_geometry.md` — gauge/interpolation geometry: the IDW was order-dependent (fixed,
  §11), co-located gauges classified by evidence not distance (§11.2), the 14 energy-floor gauges
  triaged (§12), and catchment areas shown unreliable per gauge in **both** implementations (§13.2)
  — which any t/km²/yr sediment yield inherits one-for-one.
- `docs/26_phase3_refit.md` — **the Phase 3 answer.** nb13 → nb14 re-run on the v2 forcing with a
  revised objective (recession term, `k_int < k_bas`, `k_bas` bound below 15 d) and two
  pre-registered cells. H2 − H1 settles it: the repair moved volume (β −0.044, PBIAS −4.4 pts) and
  left correlation untouched (r +0.003), so volume and correlation are independent and the
  CHIRPS-gauge merge is the only remaining lever. Read §5.1 before quoting any fitted parameter.
- `docs/20_reproduction_guide.md` — how to rebuild everything not versioned: environment, the full
  regeneration chain, gitignored artifacts, calibration monitor/resume, and the traps index.
- `docs/21_project_state_and_handoff.md` — current state for a newcomer: the three calibration
  attempts, H2 − H1, the r-ceiling, renumbered open items, the advisor question, and a paste-ready
  prompt for a fresh session.
- `docs/29_seed_expansion.md` — the seed-expansion pre-registration **and its read-out**
  (queue completed 2026-08-05). Verdicts: H1 vs H2 **not separated** (gap 0.009 < seed
  spread 0.051); **H2E (FAO-56 ET) succeeded** — kc_mult off its rail (1.66/1.84 vs ≥1.90
  everywhere else) at no cost in F. H2E is the preferred configuration going forward.
- `docs/30_phase_c_plan.md` — **the ACTIVE plan.** The advisor declined the Phase B scope
  question, so the team decision is recorded there: Phase B closes on the input ceiling with
  H2E adopted; Phase C (sediment) proceeds in stages C0–C5 with a bounded background track.
- `docs/31_phase_c_workplan.md` — **the execution-level work breakdown**: every subtask with
  In/Out/Gate, the pre-registration points, per-stage paste-prompts, dependencies, and the
  risk register. A session opens its stage section and starts; no conversation history needed.
- `docs/33_c2b_preregistration.md` — **FROZEN pre-registration for stage C2b**: read before
  measuring anything about surface runoff, baseflow index or peak flow — it fixes the H-BFI /
  H-PEAK / H-CHIRPS gates, the Eckhardt definitions, the refit weight vectors and the H2E-S
  cell, and it renumbers the C2/C4/C5 docs to 34/35/36.
- `docs/progress_journal.md` — chronological log.

## Phase status

- **Phase A (model inputs): complete.** Minibacias (8,672) → URH (24 types, IGAC soils) → soil
  params (Wm, K) → rainfall + PET forcing (`data/processed/forcing_minibacia_*.csv`).
- **Phase B (water balance + discharge calibration): CLOSED on H2E** (doc 26 + its 2026-08-10
  addendum). Notebooks 13 and 14 run on `model_inputs_v2/`; 2008 warms up, 2009-2018 is scored.
  MGB-SA proper runs as a QGIS plugin; a Python water balance (derivation in
  `notebooks/03_hydrology.ipynb`) is the diagnostic. Outputs in `sim_baseline_v2/` and
  `sim_calibrated_v2/`. The adopted configuration is **H2E** (v2 forcing + revised objective +
  FAO-56 ET, θ_crit 0.6), frozen by stage C0: `parameters_H2E.csv`, `q_gauge_H2E.npz`,
  `report_H2E.json`, `h2e_drivers.npz`, and H2E rows in `metrics_fleet.csv`. Reproduce the
  adoption with `python3.10 src/report_h2e.py` (gate: F must match 0.25931 to 1e-8).
  **The inherited caveat: El Niño skill-over-climatology is −0.0005 — the dry phase sits AT
  climatology in the adopted fit, not above it** (doc 26 addendum A.5).
- **Phase C (sediment): ACTIVE** — plan in docs/30, work breakdown in docs/31. Stage **C0 is
  complete**; C1 (the SSC-quality gate) is next. The old "blocked on mainstem SSC" framing is
  superseded: 79 flagged stations exist, of which C1 runs on the 28 mapped (docs/31 C1.0).

## Pipeline commands

```
python src/organize_precip_regions.py          # consolidate DHIME precip downloads
python src/build_precip_gauges.py              # precip QC v1 (values only)
python src/repair_precip_zero_suppression.py   # precip QC v2 (REQUIRED - see docs/16 §4.1)
python src/build_discharge_gauges.py           # consolidate + clean discharge
python src/download_chirps.py [years]          # CHIRPS daily, basin-clipped
python src/mosaic_era5.py                      # basin + east strip -> era5land_ext_*.nc
python -m nbconvert --to notebook --execute --inplace notebooks/<nb>.ipynb
```

## Conventions and hard-won rules

- **Use the `_qc` files** (`precip_gauges_daily_qc.csv`, `precip_gauges_inventory_qc.csv`), never the
  pre-repair ones, for any analysis. `approval == 'Inferido_seco'` marks inferred dry days.
- ERA5-Land: time coord is **`valid_time`**; `number`/`expver` are scalar coords (`drop_vars`, not
  `isel`); `ssrd` is a daily-resetting accumulation whose 00:00 stamp holds the *previous* day's
  total — daily total = max over 01:00–23:00. Radiation sanity: 15–22 MJ/m²/day (cloudy basin ⇒ low end).
- IDEAM: missing = blank, not zero; precip day = `día pluviométrico` 07:00→07:00 local; approval
  levels Definitivo > En revisión > Preliminar.
- Model period bounded by ERA5 (P∩PET); gauges span 2008–2018.
- Notebooks 10/11 are generated by `src/nbgen/make_nb*.py` (edit the generator, rerun it, then
  execute the notebook with `python -m nbconvert`; `jupyter` is not on PATH). Verify results from
  executed outputs, not from the run's exit code alone.
- Windows Defender makes small-buffer Python I/O ~30× slow; prefer 7-Zip
  (`C:\Program Files\7-Zip\7z.exe`) for archives and ≥4 MB read chunks.
- Commit style: `<area>: <summary>` (e.g. `precip: ...`), body explains the why; push to
  `origin main`. `data/`, `data_Final/`, `delivery/` are gitignored (regenerable).
- `figures/deck/` and `*.pptx` are regenerable (`scripts/`), gitignored.
- `watch_calib.py` monitors DDS searches; `python3.10.exe` is the worker process name
  (`tasklist` for `python.exe` reports nothing while searches run).
- Before trusting any station dataset: check for *absent* records (zero-suppression), not just
  outlier values — value screens structurally cannot see missing data. Neighbour-ratio tests catch
  what per-station statistics miss.

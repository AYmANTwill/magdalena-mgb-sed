# magdalena-mgb-sed

MGB-SED suspended-sediment modelling of the Magdalena–Cauca basin (Colombia), ENSO contrast
study: La Niña 2011 (wet) vs El Niño 2015–16 (dry). UMNG internship, advisor F. J. Briceño-Zuluaga.

## Read these first

- **`docs/00_INDEX.md` — START HERE. The single entry point.** One-paragraph project statement,
  the five-document reading order for a newcomer, a status table for *every* doc (live /
  historical / superseded / reserved, with successors), a WHERE-IS-IT table answering the
  questions people actually ask (adopted hydrology and its skill · why Phase B closed · the
  r-ceiling · the peak deficit · which SSC stations are usable · the observed ENSO contrast ·
  what is embargoed · what is pre-registered · the open registers), and a list of findings that
  still live only in `docs/agents/`. If a doc below disagrees with the index, **the doc wins** —
  the index is a map, not a source. Live *status* is `progress_map.html`.

The rest of this list is the deep reference — read the one the task touches, not all of them:

- `docs/16_forcing_pipeline_audit.md` — **the knowledge base**: pipeline order, data defects found
  (zero-suppressed gauges!), development errors, and a traps reference (ERA5/DHIME/IDW pitfalls that
  produce plausible wrong numbers). Do not touch precipitation or ERA5 code before reading §6.
  ⚠ Its §1 and §8 are pre-Phase-B and say Phase B "has not started" and Phase C is "blocked" —
  both superseded; take *status* from this file's Phase status block, not from docs/16.
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
  left correlation untouched (r +0.003), so volume and correlation are independent. Read §5.1
  before quoting any fitted parameter, and the 2026-08-10 addendum for the H2E adoption.
  **§7's "the CHIRPS merge is the only remaining lever" is spent:** the merge was built, its LOOCV
  gate passed (r 0.447) and its volume gate failed twice (+7.5 %); the registered repair was a
  **no-op** and the diagnosed cause was **wrong**. `docs/18` §15.5 (the owning read-out): *"no route
  to a passing volume gate exists inside the merge code."* One untested upstream hypothesis
  survives — the 139 residual rain-selective stations — and it cannot be tested inside the merge.
  **No fix exists, and there is no v3 forcing.** Do not plan work on the assumption one is waiting.
- `docs/20_reproduction_guide.md` — how to rebuild everything not versioned: environment, the full
  regeneration chain, gitignored artifacts, calibration monitor/resume, and the traps index.
- `docs/21_project_state_and_handoff.md` — the newcomer narrative: the calibration attempts, H2 − H1,
  the r-ceiling, renumbered open items, and a paste-ready prompt for a fresh session. ⚠ **Historical
  snapshot (2026-08-03)** — take its *reasoning*, never its *status*. Two of its sections have been
  overtaken: §5's "advisor question" was asked and **declined** (docs/30 §1 — the team decided), and
  a fourth attempt (H2E) followed the three it tabulates.
- `docs/29_seed_expansion.md` — the seed-expansion pre-registration **and its read-out**
  (queue completed 2026-08-05). Verdicts: H1 vs H2 **not separated** (gap 0.009 < seed
  spread 0.051); **H2E (FAO-56 ET) succeeded** — kc_mult off its rail (1.66/1.84 vs ≥1.90
  everywhere else) at no cost in F. H2E is the preferred configuration going forward.
- `docs/30_phase_c_plan.md` — **the ACTIVE plan.** The advisor declined the Phase B scope
  question, so the team decision is recorded there: Phase B closes on the input ceiling with
  H2E adopted; Phase C (sediment) proceeds in stages C0–C5 with a bounded background track.
- `docs/31_phase_c_workplan.md` — **the execution-level work breakdown**: every subtask with
  In/Out/Gate, the pre-registration points, per-stage paste-prompts, dependencies, and the
  risk register. A session opens its stage section and starts; no conversation history needed —
  but **check the stage-status pointer at the top and the ⛔ marker at C4.3 first**, and take each
  stage's outcome from its owning doc, not from the plan text.
- `docs/33_c2b_preregistration.md` — **FROZEN pre-registration for stage C2b**: read before
  measuring anything about surface runoff, baseflow index or peak flow — it fixes the H-BFI /
  H-PEAK / H-CHIRPS gates, the Eckhardt definitions, the refit weight vectors and the H2E-S cell.
  Read-out in §6–§8: H-BFI held, **H-PEAK was refuted**, the H2E-S refit failed 2 of its 3
  conditions, and Phase B closed a second time on that measured conflict. Its §1 H-CHIRPS pointer
  says "see §7" — that is wrong; §7 is H-PEAK, and the H-CHIRPS read-out is `docs/18` §15.5.
  (Doc numbers: 34 = C2 observed contrast; **35 = the q_peak registration, 36 = the peak-deficit
  adjudication, 45 = the C4 pre-registration**; the C5 results doc is unwritten.)
- `docs/32_ssc_qc_audit.md` + `docs/34_observed_enso_contrast.md` — the C1/C2 deliverables a
  sediment session needs: **which SSC stations are usable** (79/79 classified, 18 usable, only one
  Magdalena-trunk station `21237020`) and **the model-free observed ENSO contrast** (~3–9×, 22 of
  22 station-ratios, rates only) that C5 must reproduce. **Absolute flux only — t/km²/yr is
  embargoed** until the catchment areas get an external arbiter (`docs/23` §13.2).
- `docs/37_c3_closure.md` — **the C3 verdict: OPEN, not closed**, plus four amendments (A1, A1.9,
  A2, A3) that carry the live numbers. Read the amendments, not only §1–§6. Basin level **299.539
  Mt/yr** of gross *hillslope* erosion (α, β unfitted — a lower bound), which supersedes 248.730.
  **Never quote a load without its convention *and* its `cp_revision`.**
- `docs/47_c4_entry_verdict.md` — **the authority on whether stage C4.3 may start, and it says NO:**
  `C4.3-BLOCKED-UNTIL-LS-LANDS`. Read it before touching sediment calibration. The block is upheld
  by `docs/46` §6.4, `docs/51` §4, `docs/53` and `docs/37` A3.4. One bounded exception (§6.3):
  LS-invariant preparation only — no objective evaluation against the α box, no consumption of the
  registered budget. Its companion registrations are `docs/45` (C4.2, frozen) and `docs/42` (the
  guard set G1–G9, frozen: α, C, LS, K units, volume convention, P and FG are **seven ways of
  writing one product Π**, condition number `inf` — report Π and evidence grades, never "validated").
- `docs/progress_journal.md` — chronological log.

## Phase status

- **Phase A (model inputs): complete.** Minibacias (8,672) → URH (24 types, IGAC soils) → soil
  params (Wm, K) → rainfall + PET forcing (`data/processed/forcing_minibacia_*.csv`).
- **Phase B (water balance + discharge calibration): CLOSED on H2E** (doc 26 + its 2026-08-10
  addendum; closed a *second* time by doc 33 §8, after C2b re-opened it under pre-registration and
  H-PEAK was refuted — H2E survived both). Any re-opening, forcing or objective, needs a new
  pre-registration (doc 33 §5.1).
  Notebooks 13 and 14 run on `model_inputs_v2/`; 2008 warms up, 2009-2018 is scored.
  MGB-SA proper runs as a QGIS plugin; a Python water balance (derivation in
  `notebooks/03_hydrology.ipynb`) is the diagnostic. Outputs in `sim_baseline_v2/` and
  `sim_calibrated_v2/`. The adopted configuration is **H2E** (v2 forcing + revised objective +
  FAO-56 ET, θ_crit 0.6), frozen by stage C0: `parameters_H2E.csv`, `q_gauge_H2E.npz`,
  `report_H2E.json`, `h2e_drivers.npz`, and H2E rows in `metrics_fleet.csv`. Reproduce the
  adoption with `python3.10 src/report_h2e.py` (gate: F must match 0.25931 to 1e-8).
  **The inherited caveat: El Niño skill-over-climatology is −0.0005 — the dry phase sits AT
  climatology in the adopted fit, not above it** (doc 26 addendum A.5).
- **Phase C (sediment): ACTIVE** — plan in docs/30, work breakdown in docs/31, live status in
  `progress_map.html`. Stage state as of 2026-08-12, each from its owning doc:
  **C0 complete** (docs/26 addendum) · **C1 complete** (docs/32, nb15 — 79/79 stations classified,
  18 usable) · **C2 complete** (docs/34 — the observed contrast) · **C2b complete** (docs/33 §6–§8)
  · **C3 built, run, and OPEN** (docs/37, four amendments; A3 of 2026-08-12 states "C3 stays OPEN")
  · **C4: C4.1/C4.2 landed, and C4.3 — the sediment calibration search — is BLOCKED** (docs/47,
  `C4.3-BLOCKED-UNTIL-LS-LANDS`; **docs/47 owns the block condition — read it, do not restate it
  from here**) · **C5 not started.** The old "blocked on mainstem SSC" framing is superseded; its
  exact form is docs/32 §R6 — one Magdalena-trunk SSC station exists, `21237020`.

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
- **"v2 forcing" means GAUGE-ONLY** — the zero-suppression repair + deterministic IDW, written to
  `model_inputs_v2/`, and it is what H2E was fitted on. It does **not** mean "gauges + CHIRPS": a
  CHIRPS-merged **v3 does not exist** and would need a new pre-registration. Canonical definition:
  `docs/00_INDEX.md` → "Forcing versions — v1 / v2 / v3, stated once". nb11's *prose* uses the older
  CHIRPS-inclusive sense and contradicts its own code; the code is the one that matches disk.
- **Notebooks 10–19 are all generated** — `src/nbgen/make_nb10.py` … `make_nb19.py` (verified
  2026-08-12: generators exist for every one, and reproduce their committed notebooks
  source-identically). **Never hand-edit a notebook in that range**; the next regeneration
  overwrites the edit silently. Edit the generator, rerun it, then execute with
  `python -m nbconvert` (`jupyter` is not on PATH). **Check what a re-execute costs first:**
  nb12/13 register a 7,200 s timeout, nb14 28,800 s, nb15–19 `timeout=-1`, and a part-way failure
  leaves the notebook *less* executed than you found it. Verify results from executed outputs, not
  from the run's exit code alone.
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

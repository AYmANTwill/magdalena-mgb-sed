# PROGRESS — the whole project as one checklist tree

> **STATUS — SUPERSEDED by `progress_map.html`** (repo root, open in a browser), which is the live tracker and is kept current. ⚠ The document index near the bottom of this file still carries the **pre-collision numbering** (33/34/35); the correct assignment is 33 = C2b pre-registration · 34 = C2 observed contrast · 35 = q_peak registration · 36 = peak-deficit adjudication. Entry point: [docs/00_INDEX.md](00_INDEX.md).
>
> ⚠ **WIDENED 2026-08-12 — the drift is not only in the numbering.** The warning above named the
> document index; the **whole Phase C checklist tree below has also fallen behind**, and the "next
> executable step is C0" line dates from 2026-08-10. Measured against the owning docs: **C0 is
> complete** ([docs/26](26_phase3_refit.md) Addendum), **C1 is complete** ([docs/32](32_ssc_qc_audit.md)
> R1–R7, 79/79 classified), **C2 is complete** ([docs/34](34_observed_enso_contrast.md)), **C2b ran**
> ([docs/33](33_c2b_preregistration.md) — H-PEAK refuted, the H2E-S refit rejected), **C3 is built but
> OPEN** ([docs/37](37_c3_closure.md), four amendments), and **C4.3 — the sediment calibration search
> — is formally BLOCKED**: [docs/47](47_c4_entry_verdict.md), *"`C4.3-BLOCKED-UNTIL-LS-LANDS`.
> **C4.3 may not start.**"* — a block upheld by `docs/46` §6.4, `docs/51` §4, `docs/53` and
> `docs/37` A3.4. **The document index below also stops at 35;** ~~the numbered docs now run to 53~~
> → **they now run to 59** (44 was never assigned) — widened again 2026-08-19.
> Per RULE 0 the tracker owns status, so the checklist is **not** restated here item by item — but
> the *fact* claims and the two open registers have been corrected in place below. Read
> `progress_map.html`.
>
> ⚠ **WIDENED AGAIN 2026-08-19 — the 2026-08-12 widening above is itself two stages behind.**
> The block it quotes was **discharged**. LS landed (`ls_formulation = buarque_2015_dg`,
> f_LS = 0.25146 erosion-weighted / 0.2446790094097074 area-weighted), **C4.3 RAN**
> ([docs/55](55_c43_verdict.md) — verdict **RAILED / EXPLORATORY, NOT adopted**), and
> **C5 is COMPLETE** ([docs/56](56_c5_enso_application.md) — the model **reproduces** the observed
> ENSO contrast, 18/18 stations, median rate ratio **3.05×**). **Phase C is COMPLETE.** So
> `C4.3-BLOCKED-UNTIL-LS-LANDS` above is **history, not the current gate**; it is shown, not quoted
> as current. Later additions the tree below does not know about: **B5**
> ([docs/57](57_b5_gauge_expansion.md) — the flux gauge set cannot grow past ~18), the **rainfall
> ceiling bound** ([docs/58](58_rainfall_ceiling_bound.md) — the last lever is bounded at
> ≤ +0.006 r, structural, no v3 forcing), and the **cross-implementation comparison**
> ([docs/59](59_cross_implementation_comparison.md) — an independent *implementation*, **not**
> independent data; every R2 number is pinned to commit d055561, 2026-08-03).

**What this is.** A single, maintained map of every phase, stage, subtask, document, and
key artifact in `magdalena-mgb-sed`, with a status marker on each. It is the *index of
truth for where we are*; the *why* for any item lives in the doc cited next to it. The
interactive version is `progress_map.html` (open in a browser).

> **RULE 0 applies here too:** if this file disagrees with a primary doc, the doc wins.
> Update this file when a stage closes; never let it drift into a second source of truth.

**Legend:** ✅ done · 🟡 in progress / partial · ⬜ not started · 🔴 blocked / open question ·
🚫 embargoed (do not report) · 📌 decision recorded

**Current situation (2026-08-10).** Phase A ✅ and Phase B ✅ are complete; hydrology is
**frozen at H2E** (F 0.25931) at the input's r≈0.57 ceiling — by decision, not failure.
**Phase C (sediment) is ACTIVE**; the next executable step is **C0** (freeze + report H2E,
goes to a Claude Code session). The docs/31 plan was adversarially reviewed (2026-08-10) and
its nine findings (F1–F9) were just corrected in place. Yields (t/km²/yr) remain 🚫 embargoed.

---

## Phase A — model inputs ✅ COMPLETE

- [x] ✅ DEM conditioning → 8,672 minibacias (nb07) — `minibacias.tif`, `topology.npz`
- [x] ✅ URH: 24 types = soil × land cover (nb08) — WorldCover 8 classes, IGAC soils
- [x] ✅ Soil parameters Wₘ, K per minibacia (nb09) — `minibacia_soil_params.csv`
- [x] ✅ Rainfall + PET forcing, repaired **v2** — `model_inputs_v2/forcing_*` (docs/16)
- [x] ✅ Domain correction (east strip for upper Sogamoso) — docs/15

## Phase B — water balance + discharge calibration ✅ COMPLETE (frozen, not KGE-closed)

- [x] ✅ Python water-balance engine `mgb_hydrology.py` (fao56 / θ_crit) — engine-grade tests
- [x] ✅ Forcing QC v2 — zero-suppression repair (153/294 gauges omitted dry days) — docs/16, 18 §9-10
- [x] ✅ Discharge QC — SNHT breaks, energy-floor triage — docs/17
- [x] ✅ Four calibration attempts, all pre-registered — docs/21 §1, docs/26
  - [x] ✅ Attempt 1 Config B (v1) · [x] H1 (v1 + recession) · [x] H2 (v2) · [x] **H2E adopted**
- [x] 📌 **Decision: Phase B closes on the input-ceiling result, H2E adopted** — docs/30 §1
- [x] ✅ r-ceiling result quantified (El Niño r 0.556–0.572 / 12 configs; field LOOCV 0.429) — docs/21 §3, docs/22 §4.7
- [x] ✅ H2−H1: volume & correlation independent (β −0.044, r +0.003) — docs/21 §2
- [x] ✅ Presentation deliverables (deck + guide + docs/24/27/28) — docs/21 §6
- [ ] 🔴 Advisor question ("is the ceiling an acceptable closing statement?") — **advisor declined; team decided** (docs/30 §1)

## Phase C — sediment 🟡 ACTIVE (plan docs/30 + docs/31)

> **Live status is the top banner + `progress_map.html`.** The per-subtask boxes below are the
> ORIGINAL plan; the stage headers are kept current. ~~As of 2026-08-12: **C0/C1/C2 ✅, C2b ✅ ran,
> C3.1 enacted (C3 OPEN), C4.3 🔴 BLOCKED — sediment NOT calibrated.**~~
> **Updated 2026-08-19, at the C5 landing: C0/C1/C2 ✅ · C2b ✅ ran · C3.1 enacted (C3 still OPEN,
> [docs/37](37_c3_closure.md) A3) · C4.3 ✅ RAN — RAILED / EXPLORATORY, **not adopted**
> ([docs/55](55_c43_verdict.md)) · C5 ✅ COMPLETE ([docs/56](56_c5_enso_application.md)).
> Phase C is COMPLETE.** The 2026-08-12 line is left visible above as the state on that date.

### C0 — freeze & report H2E ✅ **COMPLETE** (docs/26 addendum; `h2e_drivers.npz` 521 MB)
- [ ] ⬜ C0.1 extract adopted parameter set → `parameters_H2E.csv`
- [ ] ⬜ C0.2 **reproduction gate** — recomputed F must match 0.25931 to ≤1e-8 *(blocks all downstream)*
- [ ] ⬜ C0.3 full sim + per-period metrics → `q_gauge_H2E.npz`, `metrics_fleet.csv`
- [ ] ⬜ C0.4 the two tables every later stage quotes (4-attempt history; ENSO asymmetry)
- [ ] ⬜ C0.5 precompute sediment drivers → `h2e_drivers.npz` (~250 MB, gitignored)
- [ ] ⬜ C0.6 commit `results: adopt H2E …`

### C1 — SSC-quality gate ✅ **COMPLETE** — docs/32, 79/79 classified (6 usable + 12 caveat = 18 usable)
- [x] 📌 **C1.0 network-size decision TAKEN** — Phase C runs now on the **28-station mapped subset (24 safe)**; the 46-unmapped coordinate fetch is moved to background **B5** (non-gating). C1 is no longer blocked (docs/31 C1.0, docs/30 §5.4)
- [ ] ⬜ C1.1 coverage census → `sediment_coverage_census.csv` (pre-register the N threshold)
- [ ] ⬜ C1.2 sampling-selectivity (transposed zero-suppression) — null = **calendar-regular** stations (F4)
- [ ] ⬜ C1.3 value screens with corrected nulls → amended `sediment_daily_qc.csv`
- [ ] ⬜ C1.4 rating-era segmentation (SNHT breaks) → `ssc_station_eras.csv`
- [ ] ⬜ C1.5 sediment rating relations per station/era → `ssc_rating_fits.csv`
- [ ] ⬜ C1.6 **classification** — 79/79 usable / caveat / excluded, each with its measurement → `sediment_inventory_qc.csv`, `docs/32`
- [ ] ⬜ C1.7 commit

### C2 — observed ENSO contrast (model-free) ✅ **COMPLETE** — docs/34 (La Niña 2.8–4.6× El Niño, 22/22 same sign) · C2b ✅ ran (docs/33: H-PEAK refuted, H2E-S refit rejected → peak deficit STRUCTURAL, sediment a lower bound)
- [ ] ⬜ C2.1 pre-register windows + estimators (rates-only comparability rule) → `docs/33`
- [ ] ⬜ C2.2 compute flux (t/day), monthly shape, bootstrap CIs → `observed_enso_contrast.csv`
- [ ] ⬜ C2.3 consistency checks (estimator a vs b; downstream monotonicity)
- [ ] ⬜ C2.4 literature anchor — reconcile vs docs/06 (~145–169 Mt/yr), fetch Restrepo figure
- [ ] ⬜ C2.5 commit

### C3 — MUSLE hillslope erosion 🟡 **BUILT & RUN — C3 OPEN** (docs/37 A1–A3) · C3.1 LS *formulation* ENACTED (A3: ADOPT-SOURCE `buarque_2015_dg`); basin **gross hillslope** erosion **299.5387 Mt/yr** @ `volume_convention='williams_m3'` / `k_unit_system='us_customary'` / `cp_revision='cited_central_2026_08_11'` (α, β unfitted — a lower bound; the prior revision `prior_2026_08_11` gave 248.7298 — shown, not quoted as current); C3.5 still 🔴 (musle.py absent)
- [ ] ⬜ C3.1 LS2D factor from conditioned DEM → `minibacia_ls2d.csv`
- [ ] ⬜ C3.2 C & P factors from 8 land classes → `urh_cp_factors.csv`
- [ ] ⬜ C3.3 qpeak proxy — **pre-register** choice + state α<1 bias (slope from nb07 DEM, not shipped)
- [ ] ⬜ C3.4 implement `src/mgb_sediment.py` + engine-grade tests
- [ ] 🔴 C3.5 cross-check vs impl-B `musle.py` — **file not in repo; acquire first** (F5)
- [ ] ⬜ C3.6 first uncalibrated basin run — order-of-magnitude gate only

### C4 — channel transport + sediment calibration ✅ **C4.3 RAN — RAILED / EXPLORATORY, NOT adopted** ([docs/55](55_c43_verdict.md): in-box optimum on the box floor at α = 2.0, median KGE_ln −0.118 estimator (a) / +0.139 estimator (b) — same sign, so **not** indeterminate; the unconstrained optimum is α ≈ 0.48, *below* the floor, which is the registered signature of mild upstream over-production — a **diagnosis, not a value to adopt**; design-matrix condition number `inf`, so only the product Π is identifiable)
> ~~🔴 **C4.3 BLOCKED — sediment NOT calibrated** (docs/47 `C4.3-BLOCKED-UNTIL-LS-LANDS`; four blockers in docs/47 §9.2, the LS *level* is the binding one)~~ — RETIRED / superseded 2026-08-19: the block was discharged when LS landed (`buarque_2015_dg`, f_LS 0.25146). Shown, not quoted as current.

- [ ] ⬜ C4.1 transport + Momposina sink limitation stated in docstring
- [ ] ⬜ C4.2 **pre-register** cells (α, β, settling); CAL 2012–14; ENSO out-of-sample → `docs/34`
- [ ] ⬜ C4.3 search, report, verdict (calibrate upstream of Mompós only)

### C5 — the ENSO experiment ✅ **COMPLETE — the contrast is REPRODUCED** ([docs/56](56_c5_enso_application.md): 18/18 stations, median rate ratio **3.05×**, range 1.62–4.85, robust across β {0.45, 0.56, 0.65} and both window pairs; 3.05× sits at the **lower edge** of the observed ~3–5× primary band and matches estimator (b))
> ~~⬜ — **the deliverable, 1–2 sessions**~~ — superseded 2026-08-19; it was delivered.

- [ ] ⬜ C5.1 contrast run (both ENSO windows + sensitivity)
- [ ] ⬜ C5.2 prediction vs C2 target (label out-of-sample; propagate El Niño discharge bias)
- [ ] ⬜ C5.3 spatial attribution + **pre-registered factor-swap** experiments
- [ ] ⬜ C5.4 write-up → ~~`docs/35`~~ → **[`docs/56`](56_c5_enso_application.md)** + figure set (corrected 2026-08-19: `docs/35` is the q_peak pre-registration, not the C5 write-up)

## Background track 🟡 (bounded, never gating — docs/30 §5, docs/31)

- [x] ✅ ~~🟡 **B1 CHIRPS refit** — merge attempted & **rejected** (r 0.447✅ / volume +7.5%🔴); refit re-spec'd to fit maps on **selectivity-passing stations** (F3), ≤2 sessions then stop~~ → **CLOSED-NEGATIVE 2026-08-12. This is not pending work.** The refit was registered as **H-CHIRPS** ([docs/33](33_c2b_preregistration.md) §1), executed, and was a **no-op**: docs/33 §1 — *"The registered intervention turned out to be a **no-op**: the quantile maps already included the inferred-dry days, so **the diagnosed cause in docs/18 §15.3 was wrong**."* The re-run is **bit-identical** and the volume gate fails again at **2,188.5 mm/yr (+7.47 %)**; [docs/18](18_hydrology_journal.md) §15.5: *"**no route to a passing volume gate exists inside the merge code.**"* **No fix is available, no v3 forcing exists, and the surviving hypothesis (the 139 residual rain-selective stations) is UNTESTED and lies upstream of the merge.** Matches `progress_map.html`, which already carries it as closed, and [docs/30](30_phase_c_plan.md) §5 item 1
- [ ] ⬜ B2 k_int_frac floor probe (0.02→0.005, one seed) — 6–7/8 v2 seeds sit on it
- [ ] ⬜ B3 external catchment areas (IDEAM catalogue / HydroSHEDS) — **unblocks yields only**
- [ ] ⬜ B4 remote-sensing SSC cross-check (optional)
- [ ] ⬜ **B5 SSC coordinate+area fetch** for the 46 unmapped stations (extend `fetch_station_coords.py`) — raises SSC coverage if it lands; blocks nothing (docs/31 B5)

---

## Open registers

### docs/21 §4 — twelve open items (hydrology)
1. 🟡 CHIRPS–gauge merge (→ B1) · 2. ✅ PET review (→ H2E FAO-56) · 3. 🔴 Mompós routing (not implemented, named limitation) ·
4. 🔴 ~2,050 mm/yr rainfall reference provenance · 5. 🔴 advisor gauge-density question · 6. 🔴 CATAM coord error (guarded) ·
7. 🚫 catchment areas unreliable (→ B3, blocks yields) · 8. 🔴 `is_intake` regex · 9. ✅ `PET_READY` file-count gate ·
10. 🔴 energy-floor stale denominator · 11. 🔴 climatology benchmark not reproducible (use ratio) · 12. 🔴 constrained ordering relocates compensation

> ⚠ **Reconciled 2026-08-12 against the owning docs. Two entries move, in opposite directions.**
> - **Item 1 — CHIRPS merge: ~~🟡~~ → ✅ CLOSED-NEGATIVE, not partial.** It is the same item as B1
>   above; see that entry for the quoted read-out. [docs/18](18_hydrology_journal.md) §15.5: *"This
>   closes the CHIRPS question as it currently stands."*
> - **Item 9 — `PET_READY` file-count gate: ~~✅~~ → 🔴 NOT FIXED.** Measured on disk 2026-08-12:
>   `src/nbgen/make_nb11.py:461` and `notebooks/11_rainfall_pet_forcing.ipynb:819` both still read
>   `PET_READY = len(ext) >= 132`. That is still a **filename count**, which is exactly the hole
>   [docs/18](18_hydrology_journal.md) §14.3 recorded: *"`era5land_ext_2008_M06.nc` was
>   **internally corrupt** … at a perfectly normal 43.69 MB, so neither a name check nor a size
>   check could see it. … **`PET_READY = len(ext) >= 132` in nb11 still has this hole** — it counts
>   names."* Carried as docs/18 §8 item 17. This tracker was wrong; the doc was right. *(Notebook
>   and `src/` are outside this pass's file scope, so only the register entry is corrected.)*
> - **Items 2–8 and 10–12 re-checked and unchanged.** Item 2 (PET review) is ✅ on the ET-*function*
>   half only — [docs/29](29_seed_expansion.md) rule (b) *"SUCCESS, all three conditions"* — with
>   the residue carried as docs/31 register #2 below; the 49 mm/yr energy deficit itself is not
>   retired. Item 5 (the collaborator drops sparse gauges where we repair them) is genuinely still
>   open: the advisor declined the *Phase B scope* question ([docs/30](30_phase_c_plan.md) §1),
>   which is a **different** question and does not close this one.

### docs/31 known-open register (Phase C)
1. ✅ **RESOLVED** railed-count 3-vs-2 (review §3) · 2. 🔴 kc_mult 1.66/1.84 above FAO-56 ≤1.2 bar · 3. 🔴 k_int_frac floor (→ B2) ·
4. 🟡 stale "Phase C blocked" prose in docs/12/19/21/24/25/28 · 5. 🔴 Restrepo anchor unverified (→ C2.4) ·
6. 📌 ENSO window bracketed (C2.1) · 7. 📌 H2E adopted from n=2 seeds (as pre-registered)

> ⚠ **Reconciled 2026-08-12 against the owning docs. One entry closes.**
> - **Item 5 — Restrepo outlet-flux anchor: ~~🔴 unverified~~ → ✅ RESOLVED by C2.4.** The owning
>   doc is [docs/34](34_observed_enso_contrast.md), which fetched both figures with citations:
>   *"**Restrepo, J.D. & Kjerfve, B. (2000)** … **144 Mt/yr**"* and *"**Restrepo, J.D. & Escobar,
>   H.A. (2018)** … **184 Mt/yr**, an upward revision covering 1980–2010."* The "~140–180 Mt/yr"
>   placeholder is superseded by that named pair; docs/31's own copy of the register still reads
>   unresolved and belongs to that document's owner.
> - **Item 4 — stale "Phase C blocked" prose: still 🟡, and this pass moved two of the files.**
>   `docs/16` and `docs/18` (which the docs/31 list does not name, but which are the two mandatory
>   pre-reads) are back-annotated as of 2026-08-12. docs/12, 19, 21, 24, 25, 28 are unchanged here
>   — other owners. Also tracked as [docs/00_INDEX.md](00_INDEX.md) §7 defect 5.
> - **Items 1, 2, 3, 6, 7 re-checked and unchanged.**
> - **Not in either register, and it should be: C4.3 is BLOCKED.** [docs/47](47_c4_entry_verdict.md)
>   is the authority on whether the sediment calibration search may start, and the answer is **no**.
>   Neither register above predates it — they predate `docs/47` entirely.

### Embargo
- 🚫 **Yields t/km²/yr NOT reported** until areas externally resolved (B3) — docs/23. Flux (t/day) only.

---

## Document index (docs/)

| # | doc | status |
|---|---|---|
| 00–09 | objectives, background, methodology, model, data-collection, ENSO years, outlines | ✅ reference |
| 10–15 | download recipes/trackers, rating pairs, presentation plan, domain correction | ✅ reference |
| 16 | forcing pipeline audit (**read before precip code**) | ✅ |
| 17 | discharge QC audit | ✅ |
| 18 | hydrology journal (§6 refutations, §7 traps, §15 CHIRPS) | ✅ |
| 19 | sediment QC audit (§5.2 decisions) | ✅ |
| 20 | reproduction guide | ✅ |
| 21 | project state & handoff | ✅ |
| 22 | dry-phase diagnosis (§4.7 ceiling) | ✅ |
| 23 | gauge geometry (§13 area embargo) | ✅ |
| 24/27/28 | presentation outline / script / explained | ✅ delivered |
| 25 | hydrology closeout plan | ✅ |
| 26 | Phase 3 refit (§5.1 fitted params) | ✅ (C0.4 appends H2E) |
| 29 | seed expansion read-out (H2E succeeded) | ✅ |
| **30** | **Phase C plan** (scope decision, stages) | ✅ ACTIVE |
| **31** | **Phase C workplan** (subtasks, gates, registers) | ✅ ACTIVE |
| 32 | SSC QC audit | 🟡 **pre-registration frozen** 2026-08-10; results appended by C1 run |
| 33 | observed ENSO contrast | ⬜ (C2) |
| 34 | sediment calibration | ⬜ (C4) |
| 35 | ENSO contrast results | ⬜ (C5) |
| agents/review_2026-08-10_docs31 | adversarial audit (F1–F9) | ✅ applied |

## Key artifacts (data/processed/ — gitignored, regenerable via docs/20)

- ✅ `model_inputs_v2/` (forcing, topology.npz, parameters.npz, discharge.npz)
- ✅ `minibacia_soil_params.csv` (K), `minibacias.tif`, `rating_curves.csv` (33 pairs, R² 0.54)
- ✅ `sediment_daily.csv` (269,337 rows), `sediment_inventory.csv` (79 rows, **28 mapped / 24 safe**)
- ✅ `_calib_cache/dds_H2E_20260901.npz` (F 0.25931) — the adopted run
- ⬜ `sim_calibrated_v2/parameters_H2E.csv`, `q_gauge_H2E.npz`, `h2e_drivers.npz` (C0 writes these)
- ⬜ `sediment_daily_qc.csv`, `sediment_inventory_qc.csv` (C1)

## Decisions & discoveries log

- **2026-08-10** — C1 **pre-registration frozen** (docs/32): coverage N-rule, calendar-regular selectivity null, value-screen nulls, rating-era + rubric — written before any C1 compute so thresholds aren't tuned to the answer. Execution → Claude Code.
- **2026-08-10** — 📌 **C1.0 decided: Phase C runs on the 28-station mapped subset** (24 calibration-safe); the 46-unmapped coordinate fetch moved to background **B5**. C1 no longer waits on it (docs/31 C1.0, docs/30 §5.4).
- **2026-08-10** — docs/31 adversarially reviewed; F1–F9 corrected. SSC network stated honestly (**28 mapped, not 79**); C1.0 coordinate-fetch added; C1.2 null fixed (calendar-regular); B1 refit re-spec'd; register #1 resolved.
- **2026-08-10** — 📌 ENSO pairing **kept 2011 vs 2015-16** (forcing bound to 2008–2018; alt pairing un-runnable) — recorded in docs/30 §1.
- **2026-08-10** — 📌 Phase B closed on ceiling; **H2E adopted** (docs/30 §1).
- **2026-08 (docs/29)** — seed expansion: H1≈H2 (not separable); **H2E succeeded** on every pre-registered condition.
- **2026-08 (docs/18 §15)** — CHIRPS merge **rejected** (volume gate +7.5%); ~~fix identified~~ → **STRUCK 2026-08-12: no fix was identified.** The candidate fix was registered as H-CHIRPS, run, and was a **no-op** — [docs/33](33_c2b_preregistration.md) §1: *"the diagnosed cause in docs/18 §15.3 was wrong."* [docs/18](18_hydrology_journal.md) §15.5: *"no route to a passing volume gate exists inside the merge code."* One **untested** upstream hypothesis survives (the 139 residual rain-selective stations); it cannot be tested inside the merge.
- **2026-08-12** — ⚠ **Documentation-repair pass.** `docs/16` and `docs/18` (both mandatory pre-reads in CLAUDE.md) carried pre-Phase-B status framing and have been given dated STATUS banners and in-place back-annotations; `docs/18` §8 items 2, 5 and 20 were struck against §15/§15.5 of the same document; the two open registers below were reconciled against their owning docs. Process record: `docs/agents/journal_fix-prereads-registers.md`.

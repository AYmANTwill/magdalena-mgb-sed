# 21 — Project state and handoff

> **STATUS — HISTORICAL SNAPSHOT (2026-08-03).** The reasoning below is live and this is still the best narrative introduction; the *status* is not. Phase B has since **closed on H2E** ([docs/30 §1](30_phase_c_plan.md), [docs/29](29_seed_expansion.md), [docs/26](26_phase3_refit.md) Addendum) and Phase C is in flight ([docs/31](31_phase_c_workplan.md)). Live status: `progress_map.html`. Entry point: [docs/00_INDEX.md](00_INDEX.md).

Written 2026-08-03, at the close of the documentation debt push. Audience: a newcomer with
no conversation history. This is *what the project currently claims and owes*; how to
rebuild any of it is [doc 20](20_reproduction_guide.md).

**One-paragraph state.** Phase A (model inputs: 8,672 minibacias → 24 URH types → soil
parameters → rainfall + PET forcing) is complete. Phase B (water balance + discharge
calibration) is complete **through the Phase 3 refit** ([doc 26](26_phase3_refit.md)):
notebooks 13–14 ran on the repaired v2 forcing with a revised objective; 2008 warms up,
2009–2018 is scored. The calibration is **not closed** — no attempt meets every
pre-registered criterion, and the binding constraint is the rainfall field, not any
parameter. Phase C (sediment) is unblocked as a data problem and bounded as a science
problem ([doc 19 §3.9](19_sediment_qc_audit.md)); it must not start before the doc 19 §5.2
decisions are taken.

> **⚠ CORRECTED 2026-08-12 — three clauses of the paragraph above are superseded.** The
> paragraph is left as written (it is the 2026-08-03 record); these are the owning docs.
>
> - ~~"The calibration is **not closed**"~~ → **Phase B is CLOSED.** Owner
>   [docs/30](30_phase_c_plan.md) §1: *"**Phase B closes on the input-ceiling result, with
>   H2E as the adopted configuration.**"* Closed **by decision, not by reaching a target** —
>   the clause "no attempt meets every pre-registered criterion" is still true of H2E too
>   ([docs/26](26_phase3_refit.md) A.4: *"Applying §5's nine criteria unchanged, **H2E scores
>   3/9**… Adoption was on the docs/29 rules… it was never a claim that the pre-registered
>   adequacy criteria were met."*). The binding-constraint clause is unchanged and still
>   correct.
> - ~~"through the Phase 3 refit"~~ → **a fourth attempt followed, H2E**, and it is the one
>   adopted ([docs/26](26_phase3_refit.md) Addendum, [docs/29](29_seed_expansion.md) rule (b)).
> - ~~"it must not start before the doc 19 §5.2 decisions are taken"~~ → **all five doc 19
>   §5.2 items are resolved and Phase C started.** The ENSO pairing was decided
>   ([docs/30](30_phase_c_plan.md) §1: *"**Decision: keep 2011 (La Niña) vs 2015–16 (El
>   Niño).**"*); the QC step was scripted ([docs/32](32_ssc_qc_audit.md), `sediment_daily_qc.csv`,
>   79 stations); the forcing window runs 2008–2018 ([docs/18](18_hydrology_journal.md) §14.2);
>   the expected-performance bar is [docs/45](45_c4_preregistration.md). Stages C0–C3 have
>   run. **Live status: `progress_map.html`.**
> - **On "v2":** in this document "v2" always means the **zero-suppression repair +
>   deterministic IDW**, and it is **still gauge-only** — it is *not* the CHIRPS merge. The
>   canonical definition is `docs/00_INDEX.md` § *"Forcing versions — v1 / v2 / v3, stated
>   once"*. **There is no v3.**

---

## 1 — The three calibration attempts

> **⚠ CORRECTED 2026-08-12 — there are FOUR attempts.** The table below is the first three,
> as written on 2026-08-03. Attempt **4 — H2E** (v2 + the new objective + FAO-56 threshold
> ET) followed and is **the adopted configuration**: VAL KGE **0.356**, recession **0.98×**,
> PBIAS **+3.51 %**, railed 2 of 10 global / 3 of 18 dimensions. Owner
> [docs/26](26_phase3_refit.md) Addendum **A.4**, which also states the honest reading:
> *"H2E's gain over H2 is **in volume, not in skill**… while VAL KGE moves +0.011 and r
> +0.008 — both inside the 0.051 seed spread docs/29 measured, so neither is a separation."*

| attempt | forcing | objective | VAL median KGE | recession ratio (VAL all) | params at a bound |
|---|---|---|---|---|---|
| **1 — Config B** | v1 | daily KGE blend | **0.450** | **2.98×** too slow | **3** of 10 |
| **2 — H1** | v1 | + recession term, `k_int < k_bas`, `k_bas` ≥ 5 d | 0.421 | **0.96×** | 2 |
| **3 — H2** | **v2 (repaired)** | same as H1 | 0.346 | **1.01×** | 2 |

Sources: `data/processed/sim_calibrated_v2/recession_validation.csv` (2.98× is the
"VAL all" row, 2.9757), `metrics_fleet.csv`, doc 26 §5. Note [docs/24](24_presentation_outline.md)
slide 8 prints 3 railed for attempt 3; doc 26 §5 (F1) records 2 — ~~an unresolved one-count
discrepancy, flagged here rather than silently chosen.~~ → **RESOLVED 2026-08-10; not a
discrepancy.** Owner [docs/26](26_phase3_refit.md) A.2: *"Railed: **2 of 10 global**…
**3 of 18 dimensions** (adding `wm_mult@R2` at 97.1 %) — **both denominators stated, because
reporting only one is what produced the docs/24-vs-docs/26 "3 vs 2" discrepancy**."* One
18-dimensional search vector, two ways to count it. [docs/24](24_presentation_outline.md)
slide 8 now prints both; [docs/31](31_phase_c_workplan.md) register #1 is marked
**RESOLVED with evidence**. *(Annotated 2026-08-12.)*

The reading, which is the deck's central argument (docs/24 slide 9): **attempt 1's higher
KGE was bought with a physically wrong recession and inverted stores.** Adding the
recession term traded ~0.03 validation KGE for a recession that is right (holds on held-out
years: La Niña 0.92×, El Niño 1.19×), El Niño α 0.793 → 0.911, and the dry phase turning
from worse-than-climatology to better (−0.026 → +0.026). Criteria: **3/9 pass for both H1
and H2, against 0/9 for Config B** — and the railing rule still bites both cells
(doc 26 §5.1): H2 satisfied `k_int < k_bas` by construction and the search **relocated the
inversion** into `k_sup` (railed 99.8 %, 19.8 d > k_bas 13.7 d). Read no fitted parameter
without doc 26 §5.1.

## 2 — H2 − H1: the repair's measured effect (59 common gauges, matched 2009–2017)

| metric | H1 | H2 | H2 − H1 |
|---|---|---|---|
| β | 1.0885 | 1.0441 | **−0.0444** |
| PBIAS % | +8.85 | +4.41 | **−4.44 pts** |
| r | 0.5802 | 0.5836 | **+0.0033** |
| KGE | 0.3886 | 0.3668 | −0.0218 |

The prediction registered before the run held: the zero-suppression repair **moved volume
and left correlation untouched**. Volume and correlation are therefore independent problems
in this basin, and no further work on rainfall totals will move the ENSO contrast
(doc 26 §4).

## 3 — The r-ceiling result (the closing statement candidate)

- Across **12 parameter configurations** (doc 22 §4.7) El Niño daily r stayed inside
  **0.556–0.572**; the forcing repair moved it +0.0033. Once α and β are repaired, KGE *is*
  r — so this is the ceiling on the dry phase.
- The rainfall field's own leave-one-out skill: **LOO IDW r = 0.40** (El Niño window) /
  0.45 (La Niña) at the gauges; the gauge-only field's LOOCV daily r used as the merge gate
  is **0.429** (doc 26 §7).
- Anomaly correlation (day-of-year climatology removed from both sides): **r = 0.476** in
  El Niño — seasonality is 13–17 % of r, not most of it.
- Mechanism: **inter-gauge daily rainfall correlation is 0.33 at 0–25 km** separation
  (0.25 at 25–50 km) against a mean gauge spacing of ~30 km. The model sits at its input's
  ceiling; no parameter set can exceed it.

Transferable phrasing: *at ~30 km gauge spacing in a tropical mountain basin, daily
rainfall–runoff correlation is capped near 0.57.*

## 4 — Open items (renumbered from doc 18 §8 as it stands today)

Closed there and not repeated here: old items 1, 3, 6, 7, 10, 11, 13, 16, 18.

| # | (old) | item | blocks |
|---|---|---|---|
| 1 | 20, 2 | ~~**CHIRPS–gauge merge — the only remaining lever on the dry phase.** Quantile-map CHIRPS *to* the gauge distribution (volume stays gauge-controlled; v2 IDW is ~4 % *below* CHIRPS, so a naive merge would add water back). Pre-registered gate: nb11 LOOCV daily r must beat the gauge-only **0.429**, else record the negative result. Time-boxed to two sessions in doc 25 stage 3~~ → **CLOSED-NEGATIVE 2026-08-10. Not pending work.** See note ⓐ below | ~~r, and therefore the ENSO contrast~~ → nothing; it is closed |
| 2 | 5 | ~~PET review against the 49 mm/yr basin ET deficit; candidate one-function change: replace `ET = ETp·W/Wm` with the FAO-56 threshold form, which is what a railed `kc_mult` ≈ 2.0 compensates for (doc 25 stage 2)~~ → **DONE 2026-08-05, and it SUCCEEDED.** See note ⓑ below | ~~the +5.6 % outlet PBIAS floor; releasing `kc_mult`~~ → both released; a **residue** remains (note ⓑ) |
| 3 | 4 | Local-inertial routing for the Mompós reach — **not to be implemented on current evidence** (celerity sweep moved El Niño r < 0.016). Carried as a named limitation: celerity 0.221 m/s is a floodplain-storage surrogate | honesty about the routing |
| 4 | 8 | Provenance of the ~2,050 mm/yr basin rainfall reference (uncited on both sides) | using it as a validation target |
| 5 | 9 | Advisor question: collaborator **drops** sparse gauges, we **repair** them; gauge density is the binding constraint on r, so neither remedy is obviously right | the merge design in nb11 |
| 6 | 12 | CATAM `21205791`/`21206570` coordinate error (5 cm apart in the catalogue, corr 0.756). Guarded by `idw_forcing.NEVER_MERGE`; still needs the IDEAM catalogue | gauge geometry near Bogotá |
| 7 | 14 | **Catchment areas unreliable per gauge in both networks** (31 of 85 differ >2×, medians agree to 1 %). Needs an external arbiter (IDEAM catalogue areas) | **any t/km²/yr sediment yield** |
| 8 | 15 | `is_intake` is a name regex (`BOCATOMA|CANAL`) — cannot flag a place-named gauge below a reservoir; needs a regulation register | the recorded reason for gauge exclusions |
| 9 | 17 | `PET_READY = len(ext) >= 132` in nb11 counts filenames, not readable files; replace with an open-and-read-a-timestep check | trusting any file-count gate |
| 10 | 19 | The energy-floor criterion has a stale denominator ("≤ 5 of 61"; the set is now 63) and its rc denominator inherits item 7's area problem | that criterion's meaning |
| 11 | 21 | The day-of-year climatology benchmark is not reproducible from doc 22 §4.1's description (rebuilt version is harder by +0.05–0.12 KGE), so the pre-registered absolute targets (+0.12/+0.24) are not testable like-for-like; use the ratio form | comparing future runs to the registered target |
| 12 | 22 | A constrained ordering **relocates** compensation rather than removing it (H2 railed `k_sup` above `k_bas`); any further ordering constraint must argue against this precedent | reading fitted parameters as physical |

> **⚠ CORRECTIONS TO THE OPEN-ITEM TABLE, 2026-08-12.** The register above is the
> 2026-08-03 state. Two of its twelve items have since been closed by measurement. The rows
> are struck rather than deleted; here is what the owning documents actually say.
>
> **ⓐ Item 1 — the CHIRPS merge is CLOSED and NEGATIVE, and the "only remaining lever"
> framing does not survive.** It was tried twice. First run
> ([docs/18](18_hydrology_journal.md) §15): LOOCV gate **PASSED** (merged median daily
> r **0.447** > 0.429) and the VOLUME gate **FAILED** (**2,188.5 mm/yr**, +7.5 %, against
> the band **[2,016.0, 2,056.8]**) → *"**DO NOT ADOPT.**"* The diagnosed cause was then
> registered as **H-CHIRPS** ([docs/33](33_c2b_preregistration.md) §1, frozen 2026-08-10),
> executed, and **the diagnosis was wrong**. Owner of the read-out is
> [docs/18](18_hydrology_journal.md) **§15.5** *(note: `docs/33` §1's own pointer says "see
> §7", which mis-fires — §7 of `docs/33` is the H-PEAK read-out)*; quoted:
>
> > "**Correction to s15.3.** That section attributed the volume failure to maps 'fitted on
> > reporting-day pairs', implying the inferred-dry days were absent. They were not: they
> > were **25.9 %** of the fit input."
>
> > "**v2 remains the forcing**, the r-ceiling of doc 22 s4.7 is unmoved, and **no route to a
> > passing volume gate exists inside the merge code.**"
>
> The re-run is **bit-identical** to the rejected one (`merge_loocv_report_v2.csv` vs
> `merge_loocv_report.csv`, max |diff| **0.000e+00**) and the volume gate fails again at
> **2,188.5 mm/yr, +7.47 %**. [docs/33](33_c2b_preregistration.md) §1: *"The registered
> intervention turned out to be a **no-op**… so the diagnosed cause in docs/18 §15.3 was
> **wrong**."*
>
> **What the cause is now: UNKNOWN.** Stated at the owning doc's own confidence and not
> upgraded here — the tested half of the diagnosis is **refuted**; the surviving half (the
> **139** stations that still report rain-selectively after the repair) **cannot be tested
> inside the merge at all**, because those days *"are not in the record"*
> ([docs/18](18_hydrology_journal.md) §15.5), and it has not been tested anywhere else.
> Repairing them is upstream, unscoped work — **not this item**. The one thing positively
> measured is *where* the surplus sits: the merged field is near-unbiased at the 287 LOOCV
> gauges (**+2.00 %** merged vs **+1.73 %** gauge-only) and puts its entire surplus in the
> ungauged terrain. **There is no v3 forcing and none was built** (`docs/00_INDEX.md`
> § *"Forcing versions — v1 / v2 / v3, stated once"*); building one would need a new
> pre-registration ([docs/30](30_phase_c_plan.md) §1). Live status agrees:
> `progress_map.html` carries *"B1 CHIRPS refit — CLOSED"*.
>
> **ⓑ Item 2 — the FAO-56 change was made and it worked.** Owner
> [docs/29](29_seed_expansion.md), rule (b): *"**H2E (FAO-56 threshold ET): SUCCESS, all
> three conditions**… The pre-registered hypothesis (docs/22 §4.6) is **confirmed**: the
> linear stress ET = kc·PET·(W/Wm) was why kc railed; the FAO-56 threshold form releases it
> at no cost."* `kc_mult` **1.662 / 1.836** against ≥ 1.896 on every H1/H2 seed; outlet
> PBIAS **+7.34 → +3.51 %** ([docs/26](26_phase3_refit.md) A.4). **The residue that carries
> forward** — quoted so it is not lost with the item: *"kc came OFF THE RAIL but is **not
> yet plausible**: 1.662/1.836 against the FAO-56 plausibility target of ≤ 1.2"* — and it is
> tracked as [docs/31](31_phase_c_workplan.md)'s known-open register #2, not here.
>
> **Not corrected here** (they belong to other owners, and this pass measured nothing new
> about them): items 3–12 stand as written. Item 9 (`PET_READY` counts filenames) is
> *contested* — `docs/PROGRESS.md` marks it done, [docs/18](18_hydrology_journal.md) §14.3
> says the hole *"still"* exists in nb11. Neither was verified by this pass; do not treat it
> as closed.

Also outstanding from doc 25 stage 5 (packaging): `pyproject.toml`, `Makefile`,
`CITATION.cff`, `CONTRIBUTING.md`, and moving the notebook smoke assertions into `tests/`
for CI. `requirements.txt` and `environment.yml` are now pinned (2026-08-03). Seeds:
H1 vs H2 on the *objective* are not yet separable (gap +0.011 vs seed spread 0.019,
doc 25 stage 1) — ~~add seeds before claiming either cell "won" the search.~~ → **the seeds
were added (six per cell) and they still do not separate.** Owner
[docs/29](29_seed_expansion.md) rule (a): *"**H1 vs H2 separability: NOT SEPARATED**… Six
seeds per cell did not separate the forcings"* — gap **0.009** against a seed spread
**0.051**. Neither cell "won"; the question is settled negative, not still open.
*(Annotated 2026-08-12.)*

Doc 19's two FLAWED items (the `calibration_safe` overclaim and the flatline-null
arithmetic) were corrected 2026-08-03, in place and marked.

## 5 — The advisor question — ~~(put this in front of him first)~~ **ASKED, DECLINED, AND DECIDED BY THE TEAM (2026-08-10)**

> **⚠ CORRECTED 2026-08-12 — DO NOT ASK THIS QUESTION AGAIN.** It was asked, and the answer
> was that there would be no answer. Owner [docs/30](30_phase_c_plan.md), header, quoted:
>
> > "**The advisor was asked the Phase B scope question (docs/24 item 17) and declined to
> > answer — told the team to decide.** This document records the decision and the plan that
> > follows from it."
>
> **The decision that followed**, [docs/30](30_phase_c_plan.md) §1, quoted: *"**Phase B
> closes on the input-ceiling result, with H2E as the adopted configuration.**"* That is the
> "**Yes**" branch below, taken by the team rather than granted by the advisor — so the
> branch's own consequence holds and is now fact: *the merge became an attempt, not a
> requirement*, and it then failed (see note ⓐ above). Grounds recorded in
> [docs/30](30_phase_c_plan.md) §1: parameter headroom exhausted (twelve configurations moved
> El Niño r by < 0.016), the ceiling is a property of the **observing network**, and the
> seed expansion settled the two remaining calibration questions.
>
> **Phase B then closed a *second* time, on different evidence** — [docs/33](33_c2b_preregistration.md)
> §8, after C2b re-opened it under pre-registration: H-BFI held, **H-PEAK was refuted**, and
> the registered `H2E-S` refit fixed the peaks but failed 2 of its 3 conditions. H2E survived
> both closes.
>
> **What is still worth putting in front of the advisor** is therefore *not* this question.
> The live open registers are §4 above (as corrected), [docs/31](31_phase_c_workplan.md)'s
> known-open register, [docs/34](34_observed_enso_contrast.md) §7 and
> [docs/36](36_peak_deficit_options.md) §7. **And the caveat that must travel with any Phase B
> claim**: El Niño skill-over-climatology in the adopted configuration is **−0.0005** — the
> dry phase sits *at* climatology, not above it ([docs/26](26_phase3_refit.md) Addendum A.5).

*Original text, preserved — this is what was believed on 2026-08-03:*

From [docs/24](24_presentation_outline.md) outline item 17, the deck's designated ending:

> **Is the input-ceiling result an acceptable closing statement for the hydrological
> phase?**

- **Yes** → the phase can close on a quantified limit whether or not the CHIRPS merge
  succeeds; the merge becomes an attempt, not a requirement.
- **No** (conventional adequacy expected — Moriasi daily NSE > 0.50) → the merge must
  succeed, and if it does not, the project needs denser rainfall input than IDEAM provides
  or a reduced target (monthly instead of daily; sub-basins instead of the full network).

It changes what "done" means for Phase B (doc 25 §5).

## 6 — Presentation deliverables

| artifact | what it is | rebuilt by |
|---|---|---|
| `MGB-SED_Magdalena_FIGURES.pptx` | the figure-led deck (gitignored) | `scripts/build_deck.py` after `scripts/extract_notebook_figures.py` + `scripts/make_deck_charts.py` |
| `presentation_guide.html` | self-contained speaker guide | versioned artifact of the deck push |
| [docs/24](24_presentation_outline.md) | slide-by-slide outline, delivery notes, figure sources | — |
| [docs/27](27_presentation_script.md) | the spoken script | — |
| [docs/28](28_presentation_explained.md) | plain-language explanation of every number in the deck | — |

## 7 — Paste-ready prompt for a fresh assistant session

> **⚠ THIS PROMPT IS SUPERSEDED, 2026-08-12 — do not paste it as written.** It is preserved
> because it is the 2026-08-03 record. Two of its lines would seed a fresh session with a
> false belief:
> - step 2's *"the standing advisor question"* → **there is none**; it was asked and declined
>   (§5 above, owner [docs/30](30_phase_c_plan.md) §1).
> - step 2's *"the three calibration attempts"* → **there are four**; the adopted one is
>   **H2E** ([docs/26](26_phase3_refit.md) Addendum A.4).
>
> **The current entry point is [`docs/00_INDEX.md`](00_INDEX.md)** — read it first, then its
> five-document reading order. It carries **RULE 0** (for any *fact*, the numbered doc that
> owns the topic wins; for any *status*, `progress_map.html` wins), which this prompt predates.

```
You are picking up the magdalena-mgb-sed repo (MGB-SED suspended-sediment modelling of the
Magdalena-Cauca basin, ENSO contrast La Nina 2011 vs El Nino 2015-16) with no conversation
history. Ground rules and reading order:

1. Read CLAUDE.md in full first - conventions, traps, and pipeline commands. Nothing there
   is decorative; most lines were paid for with a measured failure.
2. Read docs/21_project_state_and_handoff.md for the current state: what the three
   calibration attempts showed, the H2-H1 result (volume and correlation are independent),
   the r ~ 0.57 input ceiling, the renumbered open items, and the standing advisor
   question.
3. Read docs/20_reproduction_guide.md before running anything: environment (python3.10;
   workers appear as python3.10.exe), the regeneration chain, what is gitignored and how it
   rebuilds, and how to monitor/resume calibration (watch_calib.py, _calib_cache).
4. Before touching precipitation/ERA5 code: docs/16 s6. Before touching calibration:
   docs/22, then docs/26 s5.1. Before trusting any station data: docs/19 s3.1 (date rule)
   and the zero-suppression lesson (test for ABSENT records, not just outliers).
5. Hard rules: use the _qc gauge files; never pd.read_csv the wide forcing CSVs (use
   src/forcing_npy.py); notebooks 10-14 are generated by src/nbgen (edit the generator);
   verify from executed outputs, never exit codes; check fitted parameters against their
   bounds before interpreting them.

State your plan against the open items in docs/21 s4 before writing code.
```


## Addendum (2026-08-03, post-handoff): a calibration queue ~~is RUNNING~~ **WAS running — it COMPLETED 2026-08-05 and was read out in [docs/29](29_seed_expansion.md)**

> **⚠ CORRECTED 2026-08-12.** Everything below is in the present tense and is now history.
> Owner [docs/29](29_seed_expansion.md), Results header, quoted: *"**Results (read out
> 2026-08-10; queue completed 2026-08-05 02:26, 10/10 ok, 0 crashed)**"*. **Do not run
> `watch_calib.py` on account of this section** — there is nothing to watch. The two decision
> rules previewed below were applied and both were read out: rule (a) **NOT SEPARATED**
> (gap 0.009 vs seed spread 0.051), rule (b) **SUCCESS, all three conditions** → H2E, which
> [docs/30](30_phase_c_plan.md) §1 then adopted and stage C0 froze
> ([docs/26](26_phase3_refit.md) Addendum).

Written after the section above. A detached seed-expansion queue was launched and survives
any session closing (runner PID 26784 at launch; irrelevant after reboot — use the checks
below, not the PID):

- **Jobs (pre-registered in docs/29):** H1 seeds 20260903–06, H2 seeds 20260903–06,
  H2E seeds 20260901–02 — budget 1000 evaluations each, max 4 concurrent workers,
  ~16–20 h total from 2026-08-03 ~20:40.
- **Monitor:** `python watch_calib.py` from the repo root (workers are `python3.10.exe`;
  `tasklist` filtered on `python.exe` shows NOTHING while they run).
- **Completed vs stale:** the four 20260901/02 H1+H2 runs from earlier are COMPLETE;
  watch_calib correctly marks them stale.
- **If the queue died** (crash/reboot): checkpoints in `data/processed/_calib_cache/`
  resume with an RNG-replay assertion — follow docs/29, do not hand-relaunch jobs, and
  never run two launchers at once (three racing batches happened once).
- **When done:** pool 6 seeds per cell and apply the docs/29 decision rules —
  (a) H2 vs H1 separated iff |mean gap| > max(seed spread); (b) H2E success = kc_mult
  < 1.85 on both seeds AND recession ≤ 1.5× AND mean F within 0.01 of H2.
- **CHIRPS merge (docs/18 §15):** LOOCV gate PASSED (r 0.447 vs 0.429 — first measured
  lift on r in the project) but the volume gate FAILED (+7.5 %), so it was rejected under
  the pre-registered rule. ~~The identified fix: fit the quantile maps on the repaired
  series including inferred-dry days, then re-run both gates.~~
  → ⚠ **THERE IS NO IDENTIFIED FIX. STRUCK 2026-08-12 — the diagnosis was WRONG and the
  cause is now UNKNOWN.** See note ⓐ under §4 above for the full record. In short: that
  exact intervention *was* registered ([docs/33](33_c2b_preregistration.md) §1, as
  **H-CHIRPS**), executed, and turned out to be a **no-op** — the inferred-dry days were
  already **25.9 %** of the fit input, so the re-run is **bit-identical** and the volume
  gate fails again at **2,188.5 mm/yr (+7.47 %)**. Owner of the read-out is
  [docs/18](18_hydrology_journal.md) **§15.5**, quoted: *"**Correction to s15.3.** That
  section attributed the volume failure to maps 'fitted on reporting-day pairs', implying
  the inferred-dry days were absent. **They were not**"* and *"**no route to a passing
  volume gate exists inside the merge code.**"* The surviving hypothesis — the 139 residual
  rain-selective stations — **cannot be tested inside the merge** and has not been tested
  anywhere else. **No v3 forcing exists.**

# 21 — Project state and handoff

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

---

## 1 — The three calibration attempts

| attempt | forcing | objective | VAL median KGE | recession ratio (VAL all) | params at a bound |
|---|---|---|---|---|---|
| **1 — Config B** | v1 | daily KGE blend | **0.450** | **2.98×** too slow | **3** of 10 |
| **2 — H1** | v1 | + recession term, `k_int < k_bas`, `k_bas` ≥ 5 d | 0.421 | **0.96×** | 2 |
| **3 — H2** | **v2 (repaired)** | same as H1 | 0.346 | **1.01×** | 2 |

Sources: `data/processed/sim_calibrated_v2/recession_validation.csv` (2.98× is the
"VAL all" row, 2.9757), `metrics_fleet.csv`, doc 26 §5. Note [docs/24](24_presentation_outline.md)
slide 8 prints 3 railed for attempt 3; doc 26 §5 (F1) records 2 — an unresolved one-count
discrepancy, flagged here rather than silently chosen.

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
| 1 | 20, 2 | **CHIRPS–gauge merge — the only remaining lever on the dry phase.** Quantile-map CHIRPS *to* the gauge distribution (volume stays gauge-controlled; v2 IDW is ~4 % *below* CHIRPS, so a naive merge would add water back). Pre-registered gate: nb11 LOOCV daily r must beat the gauge-only **0.429**, else record the negative result. Time-boxed to two sessions in doc 25 stage 3 | r, and therefore the ENSO contrast |
| 2 | 5 | PET review against the 49 mm/yr basin ET deficit; candidate one-function change: replace `ET = ETp·W/Wm` with the FAO-56 threshold form, which is what a railed `kc_mult` ≈ 2.0 compensates for (doc 25 stage 2) | the +5.6 % outlet PBIAS floor; releasing `kc_mult` |
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

Also outstanding from doc 25 stage 5 (packaging): `pyproject.toml`, `Makefile`,
`CITATION.cff`, `CONTRIBUTING.md`, and moving the notebook smoke assertions into `tests/`
for CI. `requirements.txt` and `environment.yml` are now pinned (2026-08-03). Seeds:
H1 vs H2 on the *objective* are not yet separable (gap +0.011 vs seed spread 0.019,
doc 25 stage 1) — add seeds before claiming either cell "won" the search.

Doc 19's two FLAWED items (the `calibration_safe` overclaim and the flatline-null
arithmetic) were corrected 2026-08-03, in place and marked.

## 5 — The advisor question (put this in front of him first)

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

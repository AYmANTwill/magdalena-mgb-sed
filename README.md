# Suspended sediment transport in the Magdalena–Cauca basin under contrasting ENSO phases

**An MGB-SED study of the Magdalena–Cauca basin, Colombia (8,672 minibacias, 257,097 km²).**
UMNG research internship · advisor Prof. F. J. Briceño-Zuluaga · this document rewritten 2026-08-19.

---

## 1 — The study in one paragraph

**The question.** Does the El Niño–Southern Oscillation change how much sediment the
Magdalena–Cauca basin transports — and can a physically based distributed model reproduce and
*explain* that change? The two phases compared are the wet **La Niña of 2011** and the dry
**El Niño of 2015–16**. **The method.** MGB-SA hydrology, calibrated on 2008–2018 gauge records,
carries a MUSLE hillslope-erosion module over 8,672 minibacias and 24 hydrological response units,
with every static factor (soil erodibility `K`, cover `C`, topography `LS`) built from surveyed
inputs rather than fitted. **The result has two levels, and they must not be collapsed into one.**
At the level of *absolute daily prediction* the study fails, and the failure is measured, bounded
and publishable: daily discharge correlation is capped at **r ≈ 0.57** by the information content
of the rain-gauge network, the sediment level is **not identifiable** at all (the design matrix's
condition number is `inf` — only the product Π is determined), and the registered calibration
search **railed at its box floor**, so it is reported as exploratory and **not adopted**. At the
level of the *ENSO contrast* the study succeeds: the model reproduces the observed wet-over-dry
sediment ratio at **18 of 18 stations, median 3.05×**, against a model-free observed **22 of 22,
median ~3–9×**. **The contrast survives precisely because it is a ratio: every unidentifiable
multiplier cancels exactly.** That is the finding.

---

## 2 — Reading order for a newcomer

Six documents, in this order. About two hours; nothing else is needed to be useful.

| # | read | why this one |
|---|---|---|
| 1 | **`CLAUDE.md`** | Conventions, pipeline commands, and the trap list. Almost every line was paid for with a measured failure — the `_qc` file rule, the ERA5 `valid_time`/`ssrd` traps, the `python3.10.exe` process-name trap. Ten minutes here saves days. |
| 2 | **`docs/00_INDEX.md`** | The map: a status line for every document, and a WHERE-IS-IT table that answers the questions people actually ask. **It is a map, not a source — if it disagrees with a numbered doc, the doc wins.** |
| 3 | **`docs/22_dry_phase_diagnosis.md`** | The intellectual core, and mandatory before touching calibration. Three standing hypotheses for the dry-phase failure were measured against 30 model runs; all three failed and **one was backwards**. §4.7 is the r ≈ 0.57 ceiling that governs everything downstream. |
| 4 | **`docs/26_phase3_refit.md`** + its 2026-08-10 addendum | The parameter record and the adopted hydrology (**H2E**, objective `F = 0.25931`). Read §5.1 before quoting any fitted parameter, and addendum A.5 for the caveat that must always travel with H2E. |
| 5 | **`docs/55` → `docs/56`** | The two halves of the answer, in this order: **55** the sediment calibration verdict (RAILED / EXPLORATORY, not adopted) and **56** the ENSO contrast the model *does* reproduce (18/18, median 3.05×). Reading 55 first is what stops 56 being over-read. |
| 6 | **`docs/57`, `docs/58`, `docs/59`** | The three limits, each closed with a number rather than an apology: the gauge network **cannot** grow past ~18 flux stations (57), the last rainfall lever is bounded at **≤ +0.006 r** (58), and an independent second implementation of the same method on the same basin reached the same non-identifiability conclusion (59). |

Then, and only when the task demands it: **`docs/16` §6** before touching precipitation or ERA5
code · **`docs/17`** before touching discharge · **`docs/19` §3.1** before ingesting any DHIME file ·
**`docs/20`** before running anything · **`docs/23` §13.2** before writing any per-area number.

---

## 3 — The narrative arc

The repository reads as one investigation that repeatedly tested its own assumptions, repeatedly
found them wrong, and arrived at a robust result on the one quantity that survived.

**1. Inputs are not innocent.** Rain gauges were **zero-suppressed** — dry days absent from the
record rather than recorded as zero — and a value screen structurally cannot see a missing row. It
took neighbour-ratio tests to find it. The inverse-distance interpolation was **order-dependent**
until it was made deterministic. Per-gauge catchment areas disagreed by more than 2× on 31 of 85
shared gauges in *both* independent implementations, which is why every area-normalised number in
this project is **embargoed**.

**2. The water model hits a data ceiling, not a parameter ceiling.** Twelve configurations moved
El Niño daily correlation by less than 0.016. Once bias and variance are repaired KGE *is* r, so
**r ≈ 0.57 is the ceiling on the dry phase**, and it is inherited from the rainfall field. Phase B
was closed **by decision at that ceiling**, not by reaching a target — and the decision is recorded
so it is auditable. The caveat that travels with the adopted fit: El Niño skill-over-climatology is
**−0.0005**. The dry phase sits *at* climatology, not above it.

**3. The last rainfall lever was spent, and the diagnosis was wrong.** A CHIRPS satellite merge was
built. Its correlation gate **passed** (LOOCV r 0.447); its volume gate **failed twice** (+7.5 %).
The registered repair turned out to be a **no-op** and the diagnosed cause **wrong**. The one
surviving upstream hypothesis was then *bounded* rather than tested: even a perfect repair buys at
most **+0.006 r**. The ceiling is structural. **There is no v3 forcing, and no fix is known.**

**4. Pre-registration earned its keep.** Thresholds were frozen before the numbers they judge. That
discipline refuted H-PEAK, failed the H2E-S refit on 2 of its 3 conditions, and closed Phase B a
second time on **measured conflict** rather than preference.

**5. Uncited bands die — including the project's own.** A sediment-delivery-ratio band and a
"mountainous LS 2–10" band were both retired as uncited: *a retired gate is neither a pass nor a
fail*. Then the project's **own** materiality bar of 0.1644 ln was **struck** when its stated
derivation was falsified. The rule was applied to its author.

**6. Confident diagnoses behave strangely when measured.** Defect A's reasoning was right and its
consequence nil (×1.008878). Defect B was material but by a **different mechanism** than diagnosed.
And the levers **do not multiply out**: joint ÷ product = **×1.34762**, which is why a product of
single-lever factors may never be quoted as a joint factor.

**7. The LS formulation was settled from the printed source, not from a fit.** ADOPT-SOURCE at
`buarque_2015_dg`, `f_LS` = **0.25146** (erosion-weighted). It improved the sediment score from
−0.349 to −0.118 **with no fitting at all**. Better physics beat tuning.

**8. The sediment level is not identifiable, and that is a result.** α, the C level, the LS level,
the K unit system, the volume convention, P and FG are **seven ways of writing one product Π**;
the design matrix's condition number is `inf`. The registered search **railed at the box floor**
with a verdict computable *in advance*, so it was reported EXPLORATORY and not adopted. What the
fit *wants* — α ≈ 0.48 against Williams' 11.8 — is a **symptom of upstream over-production, to be
found and not offset**.

**9. The gauge network cannot be grown.** All 46 unmapped sediment sites were geocoded; **zero** of
the 43 in-basin ones have any discharge record. That is a physical limit of the monitoring network,
not a processing gap. And **66.53 %** of modelled erosion lies upstream of no usable station.

**10. The deliverable survives all of it.** The ENSO contrast is a **ratio**, so every
unidentifiable multiplier cancels exactly. Observed **22/22**, ~3–9×. Modelled **18/18**, median
**3.05×**, and the direction holds in all six sensitivity cells (β ∈ {0.45, 0.56, 0.65} × two
window definitions). Three independent lines — observed flux, observed concentration, modelled flux
— and **no sign reversal**.

---

## 4 — Glossary

| term | in one sentence |
|---|---|
| **MGB-SA** | The distributed hydrological model this study transposes; it runs as a QGIS plugin, while `src/mgb_hydrology.py` is the Python water balance used as the calibration diagnostic. |
| **MUSLE** | The Modified Universal Soil Loss Equation: erosion driven by a *runoff* factor instead of rainfall energy, so its output already includes transport — which is why it needs no delivery ratio, and why what it returns is arguably a yield rather than gross erosion. |
| **minibacia** | One of the 8,672 elementary catchments the basin is divided into; the model's spatial unit. |
| **URH** | Hydrological response unit — a soil × land-cover combination (24 of them here) that shares one parameter set. |
| **KGE** | Kling–Gupta efficiency, a skill score decomposing into correlation `r`, variability `α` and bias `β`; 1 is perfect. `KGE_ln` is the same score on log-transformed flux. |
| **`r` (the correlation)** | Day-to-day timing agreement between simulated and observed series. It is the quantity this project is capped on, because once bias and variability are corrected KGE reduces to `r`. |
| **the ceiling** | `r ≈ 0.57` — the maximum daily correlation the rain-gauge network supports, measured across twelve parameter configurations and bounded, not assumed. It is a property of the observations, not of the model. |
| **skill over climatology** | Model KGE minus the KGE of a perfect day-of-year climatology. It is the honest benchmark: raw NSE is not comparable across windows of different variability. **−0.0005** in the adopted El Niño window. |
| **non-identifiable** | Two or more factors that enter only as a product, so data can determine the product but never the individual values. Here seven factors collapse into one product **Π**, and the design matrix's condition number is `inf`. |
| **railing** | A search whose optimum sits on the edge of its allowed box rather than inside it. A railed fit has not found a value; it has run out of room, and reporting it as a value would be a category error. |
| **Π (Pi)** | The single identifiable product of the seven sediment scalars. C4 reports Π and its equifinal family with per-factor evidence grades — never "validated". |
| **out-of-sample** | Scored on data never used to fit. The ENSO windows are strictly out-of-sample with respect to the 2012–2014 calibration window, which is ENSO-neutral through all of 2013 with weak signals at its edges. |
| **the contrast** | The wet-over-dry ratio of mean sediment flux *rates*, La Niña 2011 ÷ El Niño 2015–16. Being a ratio, it is invariant to α and to the LS level, which is exactly why it survives a non-identifiable level. |
| **yield embargo** | The standing prohibition on reporting any sediment yield in t/km²/yr referenced to a gauge, because per-gauge catchment areas are unreliable by more than 2× on 36 % of shared gauges. **Absolute flux only: t/day, Mt/yr, mg/L, m³/s.** A *model-internal* specific erosion may be reported only when explicitly labelled as such. |
| **`cp_revision`** | The name of which cover-factor (`C`/`P`) column pair the engine reads. A load is meaningless without it: the same run gives **299.5387 Mt/yr** at `cited_central_2026_08_11` and **248.7298** at the prior revision. **Never quote a load without its convention *and* its `cp_revision`.** |
| **pre-registration** | A document that freezes a threshold, hypothesis or gate *before* the numbers that will be judged against it are computed. Five are frozen here (`docs/33, 35, 42, 45, 46`) and may be changed only through their own amendment slots. |
| **v1 / v2 / v3 forcing** | v1 = original gauge interpolation. **v2 = the zero-suppression repair plus deterministic IDW, still GAUGE-ONLY** — this is what H2E was fitted on. **v3 = a CHIRPS-merged forcing, and it does not exist.** |

---

## 5 — Reproduction quick-start

**Environment.** Python **3.10** — the interpreter is `python3.10`, and running workers appear as
`python3.10.exe` in `tasklist` (`python.exe` reports nothing, a trap that once caused three
duplicate launch batches). Install from `requirements.txt` (pip) or `environment.yml` (conda).
`jupyter` is **not** on PATH; execute notebooks only with
`python3.10 -m nbconvert --to notebook --execute --inplace <nb>`. QGIS 3.44 LTR plus the
IPH-HydroTools / MGB / MGB-SED plugins are installed separately, not via pip.

**The four gates that prove a rebuild worked.** Read each from *output*, never from an exit code —
nbconvert has been observed to exit 0 on a notebook that raised.

```
python3.10 -m pytest -q                  # -> 154 passed
python3.10 src/report_h2e.py             # -> C0.2 GATE PASS, F = 0.25930593639066796 (bar 1e-8)
                                         #    nb18 reproduces 299.5387 and 248.7298 Mt/yr
python3.10 scripts/generate_report_figures.py && python3.10 scripts/build_report_pdf.py
python3.10 scripts/extract_notebook_figures.py && python3.10 scripts/make_deck_charts.py \
  && python3.10 scripts/c5/generate_enso_figures.py && python3.10 scripts/build_deck.py
```

**Regeneration chain**, in order: `docs/20_reproduction_guide.md` §3 is authoritative. In outline —
gauge consolidation and QC (`src/organize_precip_regions.py` → `build_precip_gauges.py` →
**`repair_precip_zero_suppression.py`, which is REQUIRED** → `repair_precip_selectivity.py`) ·
discharge (`build_discharge_gauges.py`) · gridded forcing (`download_chirps.py`,
`download_era5*.py`, `mosaic_era5.py`) · forcing fields and model inputs (notebooks 10–12) ·
simulation and calibration (notebooks 13–14) · the H2E freeze (`src/report_h2e.py`,
`src/build_h2e_drivers.py`) · sediment (`src/build_sediment_gauges.py`, notebooks 15–19).

**Notebooks 10–19 are GENERATED** by `src/nbgen/make_nb10.py … make_nb19.py`. **Never hand-edit one
of them** — the next regeneration destroys the edit silently. Edit the generator, rerun it, execute
the notebook, verify from the executed output, then re-confirm every generator still reproduces its
notebook source-identically. Notebooks 01–09 are hand-written and edited directly. Re-execution is
not free: nb12/13 register 7,200 s, **nb14 28,800 s**, nb15–19 unbounded, and a part-way failure
leaves a notebook *less* executed than you found it.

---

## 6 — Repository map

```
docs/            60 numbered documents + the index. THE record: verdicts, pre-registrations,
                 audits, and the reasoning behind every decision.
  archive/       the archive register (README.md) + material moved out of the live tree.
                 Most archived material is bannered IN PLACE - see docs/archive/README.md.
  agents/        process journals: what an agent tried, in what order. NOT authoritative.
notebooks/       01-09 hand-written (Phase A: DEM, URH, hydrology derivation, land cover,
                 soils, inventory, minibacias, soil parameters).
                 10-19 GENERATED from src/nbgen/ (forcing, assembly, baseline, calibration,
                 SSC gate, observed contrast, runoff signatures, MUSLE, the C3/C4 gate).
src/             the engines and the pipeline. mgb_hydrology.py (water balance),
                 mgb_sediment.py (MUSLE), mgb_transport.py (routing), calib_v2.py (the
                 frozen objective and DDS search), report_h2e.py (the adoption gate).
  nbgen/         make_nb10.py .. make_nb19.py - the ONLY way to change notebooks 10-19.
scripts/         analysis and deliverables, grouped by phase.
  b/             Phase B: calibration queue runner.
  c1/ c2/ c2b/   SSC quality gate; observed ENSO contrast; MUSLE-driver validation.
  c3/ c4/ c5/    LS + q_peak construction; the calibration profile; the ENSO application.
  build_deck.py, build_report_pdf.py, generate_report_figures.py,
  extract_notebook_figures.py, make_deck_charts.py   - the two deliverables and their figures.
tests/           154 tests. `python3.10 -m pytest -q`.
figures/         report/ (5 committed data figures)  ·  deck/ (GITIGNORED, regenerable -
                 except the 5 yb_*.png, which come from the second implementation's repo
                 and are the one input NOT rebuildable from this repository alone).
data/            GITIGNORED, ~14 GB, rebuilt by the chain in docs/20 §3. Contains the FROZEN
                 artifacts: sim_calibrated_v2/ (the adopted H2E bundle), urh_ls2d.csv,
                 minibacia_ls2d.csv, urh_ls2d_variants.csv. Read-only, always.
progress_map.html  the LIVE status tracker. For status, it wins over any document.
CLAUDE.md        conventions, pipeline commands, and the hard-won trap list.
```

**Regenerable, and therefore gitignored:** everything under `data/`, `figures/deck/`,
`MGB-SED_complete_report.pdf`, `MGB-SED_Magdalena_FIGURES.pptx`, `_eq/`, `__pycache__/`,
`.pytest_cache/`. Their absence is not data loss.

---

## 7 — How to read a number from this repository

Four rules, each of which exists because breaking it produced a wrong published figure:

1. **Never quote a load without its convention *and* its `cp_revision`.**
2. **Never quote a product of single-lever factors as a joint factor** (joint ÷ product = ×1.34762).
3. **No gauge-referenced t/km²/yr, anywhere.** Model-internal specific erosion must be labelled as
   such.
4. **"CITED is not validated; fitted is not validated."** A number's provenance grade and its
   validation status are different claims.

## 8 — Key references

See [`docs/01_scientific_background.md`](docs/01_scientific_background.md) for the annotated list
(Fagundes et al. on South American sediment flows; the MGB-SED graphic interface and
auto-calibration; Briceño et al. on ERA5 bias over mountainous terrain; the MGB-SED plugin
repository), and [`docs/40_sdr_evidence.md`](docs/40_sdr_evidence.md) §4 and
[`docs/41_cfactor_evidence.md`](docs/41_cfactor_evidence.md) for the sourced, conditioned and
graded evidence behind every MUSLE factor.

## 9 — Licence and citation

MIT (`LICENSE`). `CITATION.cff` carries the citation metadata — **its author fields are still
`TODO` and must be completed before any release.**

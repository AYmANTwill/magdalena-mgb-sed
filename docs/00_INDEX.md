# 00 — INDEX: the single entry point

*Written 2026-08-11 by the `consolidate` agent. This file exists because the project's
knowledge had spread across ~37 numbered documents, two trackers and 30+ agent journals,
and a newcomer could not tell which one was authoritative.*

*Revised 2026-08-12 by the `stale-plan-index` agent (`docs/agents/journal_stale-plan-index.md`):
documents 43–53 added to §3, the C4-entry and CHIRPS answers corrected against their owning
docs, the canonical forcing-version definition added as §"Forcing versions — v1 / v2 / v3,
stated once", and five defects added to §7. Every correction is struck-through-and-annotated,
never overwritten.*

> **RULE 0 — precedence.** For any *fact*, the **numbered doc that owns the topic wins**
> (the WHERE-IS-IT table below names the owner). For any *status* — what is done, running,
> or next — **`progress_map.html` wins** (open it in a browser; it is the live tracker).
> This index owns neither: it is a map. If it disagrees with a primary doc, the doc wins,
> and this file is the bug.

---

## 1 — The project in one paragraph

`magdalena-mgb-sed` is an MGB-SED suspended-sediment modelling study of the
**Magdalena–Cauca basin, Colombia** (8,672 minibacias, 257,097 km²), asking one question:
**how much more sediment does the basin move in a La Niña year (2011) than in an El Niño
year (2015–16), and can a physically based distributed model reproduce and explain that
difference?** It is a UMNG research internship (advisor Prof. F. J. Briceño-Zuluaga),
transposing the MGB-SED workflow of Fagundes et al. from southern Brazil. The work runs in
phases: **Phase A** built the model inputs (minibacias → URH → soil parameters → rainfall
and PET forcing) and is complete; **Phase B** built and calibrated the hydrology and is
**closed by decision** at the configuration `H2E`, at a measured input-imposed skill
ceiling rather than at a target; **Phase C** (sediment) is in flight — the SSC quality
gate (C1) and the model-free observed ENSO contrast (C2) are done, the MUSLE drivers and
engine (C3) are built ~~and being closed~~ but **C3 is OPEN** (`docs/37`, four amendments
deep), and calibration + the ENSO experiment (C4, C5) remain — with **C4.3, the calibration
search itself, formally BLOCKED** until the LS level lands (`docs/47`; still in force as of
2026-08-12 per `docs/37` A3.4). The project's governing discipline is **pre-registration**: thresholds and
decision rules are frozen in a numbered document *before* the numbers that will be judged
against them are computed, and results that failed their own gates are kept in the record
rather than deleted.

---

## 2 — Reading order for a newcomer

Read these five, in this order. Roughly two hours; nothing else is needed to be useful.

| # | read | why this one |
|---|---|---|
| 1 | **`CLAUDE.md`** (repo root) | Conventions, pipeline commands, and the hard-won trap list. Almost every line was paid for with a measured failure — the `_qc` file rule, the ERA5 `valid_time`/`ssrd` traps, the `python3.10.exe` process-name trap. Reading it costs ten minutes and saves days. |
| 2 | **`docs/21_project_state_and_handoff.md`** | The best single narrative of *what the project claims and owes*: the calibration attempts, the H2−H1 result, the r-ceiling, the open items, and a paste-ready prompt for a fresh session. Written for someone with no conversation history. **Historical snapshot (2026-08-03)** — take its *reasoning*, take its *status* from the tracker. |
| 3 | **`docs/22_dry_phase_diagnosis.md`** | The intellectual core of Phase B, and mandatory before touching calibration. Three standing hypotheses for the El Niño failure were measured against 30 model runs; all three failed and one was backwards. §4.7 is the r ≈ 0.57 ceiling that governs everything downstream. |
| 4 | **`docs/30_phase_c_plan.md`** then **`docs/31_phase_c_workplan.md`** | 30 is *what Phase C is and why it may start* (the scope decision, taken by the team after the advisor declined). 31 is *exactly what to do*: every subtask with In / Out / Gate, the pre-registration points, and the risk register. A session opens its stage section and starts. |
| 5 | **`progress_map.html`** (repo root, open in a browser) | Where the project actually is *today*, including work not yet written into a numbered doc. Self-contained; no build step. |

Then, and only when the task demands it, go deep: **docs/16** before touching precipitation
or ERA5 code, **docs/17** before touching discharge, **docs/19 §3.1** before ingesting any
DHIME file, **docs/20** before running anything, **docs/26 §5.1** before quoting a fitted
parameter.

---

## 3 — Every document

**Status key:** `LIVE` = authoritative for its subject · `LIVE (frozen)` = a
pre-registration whose registered sections must not be edited · `HISTORICAL` = accurate
for its date, do not read as current status · `SUPERSEDED` = a later doc owns the subject ·
`STALE` = written before the work it describes was overtaken; kept for provenance ·
`RESERVED` = number claimed, content in flight.

### Phase 0 / A — framing, data acquisition, model build (docs 00–15)

| # | title | subject | status | superseded by |
|---|---|---|---|---|
| 00 | INDEX | *this file* — the entry point | LIVE | — |
| 00 | objectives_and_hypotheses | scientific context, main + specific objectives, H1–H4 | LIVE (framing) | — |
| 01 | scientific_background | what MGB / MGB-SED are; the Fagundes approach being transposed | LIVE (framing) | — |
| 02 | data_sources | inventory of inputs by role, with acquisition status | STALE (statuses are pre-Phase-A) | 16 (forcing), 20 §2 (what exists now) |
| 03 | methodology | the phased workflow, Phase 0 → Phase 3 | STALE (phase statuses) | CLAUDE.md "Phase status", 30, 31 |
| 04 | model_structure | the model graph: inputs → preprocessing → sub-models → outputs | LIVE (framing) | — |
| 05 | data_collection_plan | dataset checklist, accounts/API keys, provisional bounding box | STALE (bbox superseded) | 15 (domain), 20 §1 (environment) |
| 06 | ideam_stations | IDEAM sediment/discharge station findings; Calamar & Puerto Berrío; DHIME | HISTORICAL (Q1 scan) | 19, 32 for what the network can support |
| 07 | enso_years | ONI classification; why 2011 vs 2015–16 and why 2017 was dropped | LIVE — still the basis of the pairing | pairing re-decided in 30 §1 |
| 08 | download_guide | step-by-step portal recipes (DEM, WorldCover, ERA5, DHIME) | LIVE as a recipe; its **bounding box is stale** | 15 (box), 20 (regeneration chain) |
| 09 | report_outline | structure of the EMINES/UMNG internship report | STALE (status tags predate Phase B) | — (the report is unwritten) |
| 10 | ideam_download_recipe | the manual DHIME click-path, validated | LIVE (procedural) | — |
| 11 | discharge_download_tracker | per-department discharge download tracker; the código 21–29 basin filter | HISTORICAL (download complete) | 17 §1 for what was consolidated |
| 12 | sediment_data_status | the "variable CM" breakthrough; per-department SSC coverage | SUPERSEDED | 19 (QC), 32 (what is usable) |
| 13 | rating_curve_pairs | Q↔SSC station pairing; 10 direct rating-curve candidates | HISTORICAL | 32 §R5 (30 rating eras, the set actually used) |
| 14 | presentation_plan | July deck plan ("how do you plan to do all this?") | SUPERSEDED | 24, 27, 28 |
| 15 | domain_correction | the locked domain box (east edge −72.9 → −72.3) and why | LIVE — **the authoritative box** | — |

### Phase B — forcing, QC, hydrology (docs 16–29)

| # | title | subject | status | superseded by |
|---|---|---|---|---|
| 16 | forcing_pipeline_audit | rainfall + PET pipeline; **§4.1 zero-suppressed gauges**; §6 traps; §11 the four measured forcing biases | LIVE — read §6 before any precip/ERA5 code | — |
| 17 | discharge_qc_audit | discharge consolidation + QC; **§3.1 the gauge→minibacia mapping was broken for half the network**; §4 what was checked and cleared | LIVE | mapping since fixed — see its own closing update |
| 18 | hydrology_journal | the Phase B record: engine, notebooks 13/14, §5 verdict, §6 refutations, §7 traps, §8 open items, §9–§12 forcing follow-up, §15 CHIRPS merge | LIVE | §4 split out to 22; §11–§13 split out to 23 |
| 19 | sediment_qc_audit | SSC consolidation + QC; **§3.1 the date trap (a general DHIME rule)**; the unit trap; **§3.9 the honest ceiling on the sediment phase**; §5.2 the decisions Phase C had to take | LIVE | its two FLAWED claims corrected in place 2026-08-03; station *usability* now owned by 32 |
| 20 | reproduction_guide | how to rebuild everything not versioned: environment, regeneration chain, gitignored artifacts, calibration monitor/resume | LIVE | — |
| 21 | project_state_and_handoff | newcomer's state-of-the-project: three calibration attempts, H2−H1, the r-ceiling, open items, the advisor question, paste-ready prompt | HISTORICAL (2026-08-03) — reasoning live, status stale | status → `progress_map.html`; Phase C → 30, 31 |
| 22 | dry_phase_diagnosis | why the El Niño half fails: three hypotheses measured and refuted, one backwards; **§4.7 the r ≈ 0.57 ceiling** | LIVE — read before touching calibration | — (confirmed independently by 36 §2) |
| 23 | gauge_geometry | §11 the order-dependent IDW (fixed) and co-located gauges; §12 the 14 energy-floor gauges triaged; **§13.2 catchment areas unreliable per gauge — the source of the yield embargo** | LIVE | — |
| 24 | presentation_outline | the August deck, slide by slide, with figure sources and delivery notes | LIVE (delivered) | — |
| 25 | hydrology_closeout_plan | the plan to close Phase B: scope line, stages, definition of done | HISTORICAL — the plan was executed | outcomes in 26, 29; the closing decision in 30 §1 |
| 26 | phase3_refit | the refit on v2 forcing; **H2 − H1: volume moved, correlation did not**; §5.1 the fitted-parameter caveat; **Addendum (2026-08-10): H2E adopted, reported, frozen** | LIVE — the parameter record | — |
| 27 | presentation_script | the spoken script for the figure deck, timed | LIVE (delivered) | — |
| 28 | presentation_explained | every term and number in the deck, in plain language, for a non-modeller | LIVE (delivered) | — |
| 29 | seed_expansion | pre-registration **and read-out** of the seed expansion: H1 vs H2 **not separated**; **H2E succeeded on all three conditions** | LIVE (frozen §1–§3, results appended) | — |

### Phase C — sediment (docs 30–53)

| # | title | subject | status | superseded by |
|---|---|---|---|---|
| 30 | phase_c_plan | **the scope decision**: Phase B closes on the input ceiling with H2E adopted; the ENSO pairing kept; stages C0–C5 and the bounded background track | LIVE (ACTIVE) | — |
| 31 | phase_c_workplan | execution-level breakdown: every subtask with In/Out/Gate, paste-prompts, dependencies, risk register, open register | LIVE (ACTIVE) | — |
| 32 | ssc_qc_audit | Stage C1: the SSC quality gate. §0–§6 registered before computation; **Results R1–R7 appended — 79/79 stations classified** | LIVE (frozen prereg + results) | — |
| 33 | c2b_preregistration | Stage C2b: validating the MUSLE *drivers* (surface-runoff partition, peak flow) that total-discharge calibration never tested. §6 H-BFI result, §7 H-PEAK result, §8 the H2E-S refit verdict | LIVE (frozen prereg + results) | its §5.2 reservation of number 36 is superseded by 36 |
| 34 | observed_enso_contrast | Stage C2: **the model-free observed contrast** — the target C5 must reproduce | LIVE (frozen §1 + results) | — |
| 35 | qpeak_preregistration | Stage C3.3: the MUSLE `q_peak` proxy, its signed bias, and the C4 anti-compensation rule | LIVE (REGISTERED 2026-08-11) | — |
| 36 | peak_deficit_options | adjudication of three research lenses on the structural peak deficit; ranked options; **recommendation: do not pursue a fix** | LIVE | — |
| 37 | c3_closure | the C3 closure verdict: the four convention decisions, the re-run, the two pattern gates, the residuals — **plus four amendments: `A1` (2026-08-11, still OPEN on a revised conjunction), `A1.9` (clause 4″ NOT ESTABLISHED — yield vs gross erosion), `A2` (the level RECLASSIFIED to a calibration target; C3 still OPEN), `A3` (2026-08-12, the C3.1 enactment: ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`; **no engine default moves, C4.3 stays BLOCKED**)** | LIVE — **read the amendments, not only §1–§6**; §2–§3's level and gate numbers are superseded by A1.3, and the LS bracket by A3.3.1 | its own amendments A1 · A1.9 · A2 · A3 |
| 38 | data_acquisition_protocols | the six root `.docx`/PDF operator hand-offs transcribed so the binaries can be retired; §7 lists the contradictions the comparison exposed | LIVE (transcription — inherits its sources' date and uncertainty; where it conflicts with a measured doc, the measured doc wins) | — |
| 39 | contradiction_audit | every headline quantity that appears in more than one place, tabulated with file:line and classified; **read-only — it reports disagreements, it fixes none** | LIVE (audit, 2026-08-11) — its line references may have drifted; `docs/37` did not exist when it was written | — |
| 40 | sdr_evidence | the sediment-delivery-ratio band, litigated: **UNCITABLE**, retired as a gate, and replaced by an evaluable gross-hillslope-erosion-**rate** clause (§8.2) | LIVE — owns the SDR question and the ADR/SDR distinction | — |
| 41 | cfactor_evidence | the MUSLE cover factor `C` on a citable footing: 8/8 rows sourced, conditioned and ranged; **×1.2043** central; P stays 1.0; one published value refused on physics | LIVE — owns `urh_cp_factors.csv`'s provenance | its §8.3 claim 3 corrected by `docs/37` A1.3.4 |
| 42 | c4_guards | **the C4 gate**: guards G1–G9 with 17 FAIL conditions, the seven-scalars/one-product non-identifiability, and the measured power of every test | LIVE (frozen pre-registration; §9 is the amendment slot) | G9's numbers moved by `docs/37` A1.7 item 1 |
| 43 | c3_c4_gate | the C3/C4 adjudication: **C3 STAYS OPEN · C4 PROCEEDS CONDITIONALLY.** The residual's *level* is reclassified from defect to calibration target (enacted as `docs/37` A2); its *structural* components are not | LIVE (decision; adds no new science) | its "C4 proceeds" clause is narrowed for **C4.3 specifically** by `docs/47` |
| 44 | — | **never assigned.** The sequence skips from 43 to 45 | — | — |
| 45 | c4_preregistration | **Stage C4.2, FROZEN ON WRITE 2026-08-11**: the sediment KGE bar `F_report ∈ [−0.26, 0.44]`, the α/β boxes, the CAL-8 fit set, the windows, the seeds, and all eight ADOPT conditions | LIVE (frozen pre-registration; §8 is the amendment slot) | — |
| 46 | ls_preregistration | the LS **level**: hypotheses, the evidence-grade decision rule, the C4.3 ordering gate, the negative-result pre-commitment. **FROZEN (READ OUT) 2026-08-11** — four of its five hypotheses were already measured when it froze, so it may not be cited as though §2 were prospective (its own §1.2) | LIVE (frozen; §9 the registration card, §10 the amendment slot) | — |
| 47 | c4_entry_verdict | **the C4.3 entry verdict: `C4.3-BLOCKED-UNTIL-LS-LANDS`.** The α box is denominated in an unresolved unit; the objective is monotone across the whole box; in-box `F_report` −0.305 … −0.350. Grants one bounded exception: LS-invariant preparation only | LIVE — **the authority on whether C4.3 may start** | block upheld by `docs/46` §6.4, `docs/51` §4, `docs/53`, `docs/37` A3.4 |
| 48 | pi_band_revision | discharges `docs/47` repair B5: **`σ_r = 0.465 ln` measures observer-vs-observer disagreement, not the model−observation residual** — the ±38 % Π band is retired and replaced, and every published number that moves is named | LIVE — owns the Π band and `σ_r`'s meaning | the ±38 % band and `σ_r = 0.465` as a residual sd are **superseded**; owed to `docs/45` §8 as an amendment |
| 49 | defect_a_resolution | **Defect A: REAL as a *reading* defect, IMMATERIAL as a *level* correction**; the joint ×0.421 row never carried it | LIVE | — |
| 50 | defect_b_resolution | **Defect B: the published ×0.790 was two levers, not one** (`L` form ×0.769833 on the column the engine reads; `S` swap 32.2 % of it in log units) | LIVE | ×0.790 as a single `L`-form factor is **superseded** |
| 51 | ls_freeze_decision | **DO NOT FREEZE AS DRAFTED**, plus the corrected bracket `f_LS ∈ [0.25146, 0.43194]` erosion-weighted ⇒ **2.3151× – 3.9768×**; §7 is the numbered blocking list an orchestrator can execute | LIVE — owns the corrected LS bracket | supersedes ×0.333 / ×0.421 / 2.37×–3.00× |
| 52 | materiality_bar_decision | `docs/46`'s materiality bar: **STRUCK, NOT RESCALED.** `0.1644 ln` is struck and replaced by **no number** — fifteen bar sites re-grounded on a threshold-free rule. Decided *before* `Δ_shape` was computed | LIVE | `0.1644 ln` (and every proposed replacement constant) is **superseded** |
| 53 | delta_shape_pretest | the `Δ_shape` pre-test **COMPUTED: 0.1299456916752905**, judged against the bar `docs/52` fixed blind to it → **Branch B**. Does not unblock C4.3 | LIVE | — |

> **Numbering discipline.** This file deliberately shares the number 00 with
> `00_objectives_and_hypotheses.md` so that it sorts first; that is the only intentional
> duplicate. 33/34 collided once (docs/31 carries the correction note;
> `docs/agents/journal_prereg-c2b.md` records how). docs/33 §5.2 then reserved 36 for the
> C5.4 results and docs/36 took it first. **44 was never assigned.** **Before claiming a number,
> check this table and `docs/agents/` for an in-flight claim.** ~~C4's and C5's write-ups take
> **37+**.~~ → **The next free number is 54** (checked 2026-08-12 against `ls docs/`).

### Unnumbered files in `docs/`

| file | subject | status |
|---|---|---|
| `PROGRESS.md` | the whole project as one checklist tree | SUPERSEDED by `progress_map.html` (which is current) — and its own doc index still carries the pre-collision numbering |
| `progress_journal.md` | dated chronological log, newest first | LIVE as chronology, but **stops 2026-08-03** |
| `open_questions.md` | Q1/Q2/Q3, the decisions to lock with the advisor | SUPERSEDED — all three resolved (Q1 → 12/19/32, Q2 → 07 + 30 §1, Q3 → 15 + whole basin) |
| `git_workflow.md` | commit routine quick-reference | LIVE (procedural), overlaps CLAUDE.md's commit-style rule |
| `era5_download_checklist.md` | 108-file ERA5-Land download tracker | HISTORICAL — the download completed; state in 16 §1 |
| `agents/` | **process records, not findings** — see §6 | — |

---

## 4 — WHERE IS IT: the questions people actually ask

| question | the answer, compressed | authoritative source |
|---|---|---|
| **What hydrology is adopted, and how good is it?** | **H2E** — v2 forcing + revised objective + FAO-56 threshold ET (θ_crit 0.6), best seed 20260901, objective **F = 0.25931**; `kc_mult` off its rail at 1.662, fleet-median recession ratio 1.082. Frozen by stage C0 into `parameters_H2E.csv` / `q_gauge_H2E.npz` / `report_H2E.json`; reproduce with `python3.10 src/report_h2e.py` (F must match to 1e-8). **The caveat that must travel with it: El Niño skill-over-climatology is −0.0005 — the dry phase sits *at* climatology, not above it.** | `docs/29` (read-out) · `docs/26` Addendum (adoption + §5.1 before quoting any parameter) · CLAUDE.md "Phase status" |
| **Why did Phase B close?** | By **decision, not by reaching a target**, and the decision is recorded so it is auditable: parameter headroom is exhausted (12 configurations moved El Niño r by < 0.016), the ceiling is a property of the *observing network* rather than the model, and the seed expansion settled both remaining calibration questions. The advisor was asked and declined to answer; the team decided. **It then closed a *second* time, on a different ground** — `docs/33` §8, after C2b re-opened it under pre-registration: H-BFI held, **H-PEAK was refuted**, and the registered `H2E-S` refit fixed the peaks but failed 2 of its 3 conditions (F fell 0.0319, 1.6× the budget; two new rails; `kc_mult` back on the rail H2E had just released). *"Not on exhausted headroom, and not on a clean validation either — on a **measured conflict**."* H2E survived both closes. | `docs/30` §1 (first close) · `docs/33` §8 (second close) |
| **What is the r-ceiling?** | El Niño daily correlation stays inside **0.556–0.572** across twelve parameter configurations; once bias and variance are repaired, KGE *is* r, so ~0.57 is the ceiling on the dry phase. It is inherited from the rainfall field (field LOOCV skill 0.429; inter-gauge daily correlation 0.33 at 0–25 km against ~30 km spacing). The only measured lever is a denser/merged rainfall field — the CHIRPS merge raised LOOCV r to 0.447 but failed its volume gate (+7.5 %) and was rejected under the pre-registered rule. **Updated 2026-08-12: the merge was then re-run with its registered repair (H-CHIRPS, `docs/33` §1) and rejected a second time — the repair was a *no-op*, the re-run is bit-identical, and the diagnosed cause was wrong. There is no known fix and no v3 forcing.** See §"Forcing versions — v1 / v2 / v3, stated once". | `docs/22` §4.7 (the ceiling) · `docs/18` §15 (the merge) and **§15.5** (the refit read-out — note `docs/33` §1's *"see §7"* pointer mis-fires; §7 of `docs/33` is H-PEAK) · `docs/33` §1 (H-CHIRPS) · `docs/26` §7, `docs/31` §0 (the two different LOOCV statistics — do not conflate them) |
| **What is the peak deficit, and why is it not fixed?** | Simulated flood peaks are systematically low (`R_AMS` 0.820, `R_Q5` 0.975, `R_POT` ≈ 0.57) and, more sharply, **1,829 of 2,236 observed peaks-over-threshold have no simulated partner at ±2 d — an 81.8 % event-identity deficit** (the older "43 % missed" is a *count* statement and must be quoted with this one). It is **structural**: the C2b-selected refit did fix the peaks but failed 2 of 3 pre-registered conditions, and of seven candidate interventions six fail their own pre-declared not-worth-doing condition. **Decision: accept it and propagate simulated sediment as an explicit lower bound.** | `docs/36` (diagnosis §1–§2, options §3, recommendation §6, corrections §7) · `docs/33` §7–§8 (the refit verdict) · `docs/35` (the `q_peak` proxy and its registered bias) |
| **Which SSC stations are usable?** | **79 stations classified, every one with a deciding measurement**; only **28 are mapped to minibacias** (46 have no coordinates at all). Of the 28: **6 `usable`, 12 `usable-with-caveat`, 10 excluded** — so **18 usable** in total. ~~The C4 tributary set is **13 stations**.~~ → ⚠ **CORRECTED 2026-08-12: "13" is the C1-usable *tributary* set, and it is NOT the fit set.** `docs/45` §3.4 registers three different sets and they must not be conflated: **CAL 8** is what C4 *fits* (5 of the 13 have **no paired SSC + observed-Q day** in the CAL window, so they cannot be fitted at all); **EVAL 5** is scored but never fitted; and **all 18** usable stations run **every structure guard** (G1.2, G3.1, G4.1, G11 — the all-18 clause stands and is the deciding form for G11). Only **one Magdalena-trunk SSC station exists in the entire network** (`21237020` ARRANCAPLUMAS) — that is the quantitative form of "Phase C is blocked on mainstem SSC". | `docs/32` §R6 (classification) · `docs/19` §3.9 (the ceiling this puts on the science) |
| **What is the observed ENSO contrast?** | Model-free, from observations: **La Niña sediment flux *rates* exceed El Niño at 22 of 22 station-ratios — both estimators, both window definitions, no counter-example.** Magnitude is window-dependent and must be quoted as a range: primary-window medians ≈ **2.8–4.6×**, ONI-peak sensitivity windows ≈ **6.4–9.3×**; the honest statement is **~3–9×**. Agrees with Restrepo & Kjerfve (2000). **No mainstem contrast exists in the observations.** This is the target C5 must reproduce. | `docs/34` §3.1 (the table), §7 (the verdict, and six issues it raised) |
| **What is embargoed, and why?** | **Any sediment yield in t/km²/yr.** Per-gauge catchment areas disagree by more than 2× on **31 of 85 shared gauges (36 %)** in *both* implementations, so every area-normalised number inherits that error one-for-one. **Absolute flux (t/day, Mt/yr) only**, until an external area arbiter lands (background task B3). | `docs/23` §13.2 (the measurement) · `docs/31` §B3 (the lift) |
| **Is stage C3 closed, and what is the basin sediment level?** | **No — C3 is OPEN**, re-issued as `docs/37` **Amendment A1 (2026-08-11)** on a revised five-clause conjunction: two clauses fail, one is retired, two are met. The level is **299.539 Mt/yr** of gross **hillslope** erosion (α, β unfitted; a **lower bound**), which supersedes the 248.730 Mt/yr quoted in docs/35, 36, 37 §2–§3, 40 and 42 — the difference is the docs/41 cover-factor revision, ×1.2043, reachable by name as `load_geometry(cp_revision=...)` with the prior level still reachable. Both pattern gates re-pass: Andean flanks : lowland floodplain **18.67×** (was 11.61×), bimodal seasonal cycle intact. Simulated ENSO **2.29× / 3.97×** against observed **2.8–4.6× / 6.4–9.3×** — right sign and order, short in magnitude. **Never quote a load without its convention *and* its `cp_revision`.** **Updated 2026-08-12 — `docs/37` has since been amended three more times and C3 is still OPEN at each: A1.9 re-opens clause 4′ as 4″ (**NOT ESTABLISHED** — is the MUSLE sum a *yield* or a *gross erosion*?); **A2** reclassifies the residual's **level** from defect to **calibration target** (`docs/43` §1.3) while its *structural* components are not reclassified, *"which is why C3 stays OPEN"*; **A3** (2026-08-12) is the **C3.1 enactment** — the LS *formulation* is decided on source grounds, **ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`** — and states in its own title that **no engine default moves, C3 stays OPEN, and C4.3 stays BLOCKED**. A3.3.1 also supersedes the LS bracket: ~~×0.333 – ×0.421~~ / ~~2.37× – 3.00×~~ → **×0.25146 – ×0.43194 erosion-weighted**, `1/f_LS` = **2.3151× – 3.9768×**, and at the adopted point **3.9768×**. | `docs/37` Amendment **A1** (§A1.1 the conjunction, §A1.3 the re-run, §A1.4 the failed clause, §A1.6 what C4 may do), **A1.9**, **A2**, **A3** · `docs/43` (the C3/C4 gate decision) |
| **Why was the sediment-delivery-ratio gate dropped?** | Because it was **not an evaluable test**, not because the model passed it. The 0.05–0.30 band was uncited here, and the quantity we computed is an **apparent** delivery ratio — all-source outlet load ÷ hillslope-only gross erosion — while every published SDR uses **all-source** gross erosion in the denominator (USDA NEH Part 632 Ch. 6). In USDA's own worked example the two differ **2.1×** in the same watershed (0.33 vs 0.6957) and the mixed ratio is **1.7778**. The band's relations were also fitted **993×** below this basin's scale, and no Magdalena SDR exists in print because every published Magdalena "erosion rate" is a sediment **yield**. **A retired gate is neither a pass nor a fail**; the replacement is a gross-erosion-**rate** clause, and it is **failed** — the model is under-erosive by **1.03–2.27×**. | `docs/40` (§2 definitions, §7 the three legs, §8 verdict) · `docs/37` A1.2, A1.4 |
| **May C4 start, and under what constraints?** | ⚠ **CORRECTED 2026-08-12 — the answer for the search stage is now NO.** `docs/47` (2026-08-11) decides it: **`C4.3-BLOCKED-UNTIL-LS-LANDS`. C4.3 — the sediment calibration search — may not start.** The reason is arithmetic, not caution: `docs/45` §2.1 registers a box on α ∈ [2.0, 30.0], but α is only a *handle* on Π and is proportional to `1/f_LS`, where `f_LS` is graded **UNVALIDATED** and uncertain by **2.3151× – 3.9768×** — so the box's *position* is unknown to within a factor of four. Measured on the registered configuration, the objective is monotone decreasing across the whole box, the search rails at the floor, and in-box `F_report` reaches only **−0.305 … −0.350**, below the bar's lower edge −0.26: a `FAIL — RAILED / HARD STOP` **and** a `FAIL — NUMERIC`, both computable in advance. **The block is still in force**: upheld by `docs/46` §6.4 (Branch B mandatory), `docs/51` §4, `docs/53`, and `docs/37` **A3.4** — *"Is C4.3 thereby UNBLOCKED? **NO**"* — which is the enactment amendment itself saying so. One bounded exception is granted by `docs/47` §6.3: **LS-invariant preparation only**, with no objective evaluation against the α box and no consumption of the registered budget. ~~**Yes — but only held to `docs/42` G1–G9, never to `docs/35` §6 alone.**~~ → **The `docs/42` constraint set below still governs whenever C4.3 does start; it was never the part that was wrong.** The α band alone can no longer catch the error C4 is most likely to make: at the adopted convention a fit that silently omits channel deposition lands α at ~~6.83–8.73~~ → **5.67–7.25** *(the struck band is `11.8 × {144,184} / 248.730`, i.e. computed at the **prior** `C`; `docs/47` §2.5 C1 recomputes it at the adopted `C`, and the correction is owed to `docs/43` §3.4. **The trap survives unqualified either way** — the α band is not a sufficient guard)*, *inside* the "expected" 5.9–23.6, and `check_musle_parameters` returns `ok`. **G5** replaces it with a precondition — a named non-trivial transport sink (or the words "this model asserts SDR = 1.0 between hillslope and station" stated as a claim), **and** G1.2's `k̂` with its interval in the same table as α. Also binding: α, the C level, the LS level, the K unit system, the volume convention, P and FG are **seven ways of writing one identifiable product Π** (condition number measured as `inf`), so C4 reports Π, the equifinal family and per-factor evidence grades — never "validated". And G9: only **33.5 %** of the model's erosion is upstream of any usable SSC station. | **`docs/47` (the entry verdict — read this first)** · `docs/42` (§3 non-identifiability, §6 G1–G9, §8.1 what of docs/35 survives) · `docs/45` (the C4.2 pre-registration) · `docs/37` A1.6, **A3.4** |
| **What is pre-registered, and where?** | The project freezes thresholds before computing what they judge. Active registrations: **`docs/29`** (seed expansion + H2E cell), **`docs/32` §0–§6** (C1 SSC gate), **`docs/33` §1–§5** (C2b MUSLE drivers, H-BFI/H-PEAK/H-CHIRPS), **`docs/34` §1** (C2 windows, estimators, failure conditions), **`docs/35`** (`q_peak` proxy + the C4 anti-compensation rule), **`docs/42`** (the C4 guard set G1–G9, frozen on write; §9 is its amendment slot), **`docs/45`** (C4.2 sediment calibration — bar, boxes, CAL 8, windows, seeds, all eight ADOPT conditions; frozen on write 2026-08-11, §8 is its amendment slot), **`docs/46`** (the LS *level* — **FROZEN (READ OUT) 2026-08-11**, §9 is the registration card and §10 the amendment slot). A registered section may not be edited after the fact — only amended, dated, with a reason. `docs/36` §5 is a *sketch*, explicitly **not** a registration. **`docs/46` is a special case and must be cited as one: four of its five hypotheses had already been measured when it froze, so it is a pre-registration that has been *read out*, not an open one — its own §1.2 says so, and only §4, §6 and §7 remain genuinely prospective.** | the documents themselves; `docs/31` lists the registration points |
| **What are the open questions?** | Three registers, all live: **hydrology** — twelve renumbered open items (`docs/21` §4), of which the CHIRPS merge, the Mompós routing gap, the ~2,050 mm/yr rainfall provenance and the unreliable catchment areas are the ones that bite. **Phase C** — `docs/31`'s known-open register (`kc_mult` still above the FAO-56 bar, the `k_int_frac` floor, the Restrepo anchor, the H2E n=2 seed basis). **Newest** — the six issues `docs/34` §7 raises (chief among them: the C1 selectivity rule is one-sided; recovering post-2014 discharge at ARRANCAPLUMAS would, alone, create the trunk contrast the project cannot currently produce) and the ten in `docs/36` §7. | `docs/21` §4 · `docs/31` (register) · `docs/34` §7 · `docs/36` §7 · live status in `progress_map.html` |

---

## Forcing versions — v1 / v2 / v3, stated once

*Added 2026-08-12. Deliberately **unnumbered** so that §5, §6 and §7 keep the numbers other
documents already cite. Cite this section by its title.*

**"v2" means two different things in this repository, and the difference has already misled a
reader.** This is the canonical definition. Where a claim below has an owner, the owner is
named; the index does not own any of these facts.

| version | what it is | exists? | owner |
|---|---|---|---|
| **v1** | the **original gauge forcing** — gauge IDW before the repair, and **gauge-only**. Area-weighted basin mean **2,174.3 mm/yr** on the same 2009–2017 window as v2's 2,036.4 (nb11 prints the pair in one statement). Still on disk: nb11 writes v2 *alongside* v1 rather than over it, precisely so H1 (new objective, old forcing) stays runnable | yes, superseded | `docs/18` §14.2; nb11 cell 21 |
| **v2** | the **zero-suppression repair** (`src/repair_precip_zero_suppression.py`, `docs/16` §4.1) **+ deterministic IDW** (`docs/23` §11 — `lexsort` on (distance, gauge code), order-invariance asserted inside nb11). **Still GAUGE-ONLY.** Area-weighted basin mean **2,036.4 mm/yr** (2009–2017) / 2,073.1 (2008–2018); gauge-only LOOCV daily r **0.429**. Written to **`model_inputs_v2/`**. **This is the ADOPTED forcing — the one H2E was fitted on** | **yes — adopted** | `docs/16` §4.1 · `docs/23` §11 · `docs/18` §14 · `docs/29` / `docs/26` Addendum (H2E) |
| **v3** | a **CHIRPS-merged** forcing. **IT DOES NOT EXIST.** The merge was built (`src/merge_chirps_gauges.py`) and **rejected by its volume gate** — LOOCV r 0.447 **passed**, volume 2,188.5 mm/yr **failed** (+7.47 % against [2,016.0, 2,056.8]). No forcing file was ever written; no v3 calibration was ever launched | **no** | `docs/18` §15 (merge) and **§15.5** (the refit read-out) · `docs/33` §1 **H-CHIRPS** |

**Three things follow, and they are the reason this section exists.**

1. **v1 and v2 are *both* gauge-only.** The difference between them is data repair and
   interpolation determinism, **not** the addition of satellite rainfall. A reader who assumes
   "v2 = we added CHIRPS" has the adopted forcing wrong.
2. **Building a v3 would re-open the frozen hydrology, and that needs a new pre-registration.**
   `docs/30` §1: *"Any future forcing change (CHIRPS v3) re-opens it only through a new
   pre-registration"*, restated by `docs/33` §1 — *"A pass does not authorise adopting v3"* —
   and by `docs/33` §5.1, which widens the rule to any re-opening, forcing or objective.
3. **The CHIRPS route is closed at the merge, and the cause of the volume failure is not
   settled.** The registered repair (H-CHIRPS: refit the quantile maps including the inferred-dry
   days) was executed and was a **no-op** — those days were already 25.9 % of the fit input, the
   re-run is bit-identical, and `docs/33` §1 records the diagnosed cause as **wrong**. What
   survives is an *untested* hypothesis (the 139 stations still reporting rain-selectively after
   the repair, whose missing days are not in the record at all) plus one positive measurement:
   the merged field is near-unbiased at the 287 LOOCV gauges and puts its entire surplus in the
   ungauged terrain. `docs/18` §15.5: *"no route to a passing volume gate exists inside the merge
   code."* **Do not write that the fix is known.**

> **⚠ `notebooks/10` and `notebooks/11` predate this definition and do not follow it.**
> Verified in their cell sources:
> - **nb11 uses both senses at once.** Its prose calls itself *"the v1 baseline, deliberately
>   gauge-only"* and looks forward to *"a CHIRPS-merged v2"* and *"**Next:** v2 forcing —
>   quantile-map CHIRPS onto these gauges"* (cells 0, 13, 22) — the **older, CHIRPS-inclusive**
>   sense. Its own code, in the same notebook, sets `VERSION = 'v2'` for the repaired
>   **gauge-only** field and prints *"[v1 was 2174.3, gauge-only v2 2036.4]"* (cells 1, 21) — the
>   sense that won. **The notebook's prose and its code disagree.** The code is the one that
>   matches `model_inputs_v2/`.
> - **nb10's only "v2" is a third, unrelated meaning:** *"CHIRPS v2.0"*, the satellite product's
>   own version number. It is not a forcing version at all.
>
> Banners cross-referencing this section are being added to those notebooks by a separate pass.

---

## 5 — Live status vs. the record

- **`progress_map.html`** (repo root, open in a browser) is the **live tracker** — phase and
  subtask statuses, the banner of where things stand, the discoveries feed, and the
  "why" panels. It is self-contained, needs no build step, and is the only artifact updated
  every session. **For status, it wins.**
- **`docs/PROGRESS.md`** is its markdown ancestor and has fallen behind (its document index
  still carries the pre-collision numbering 33/34/35). Read the HTML.
- **`docs/progress_journal.md`** is the dated narrative log, newest first — good for *when*
  and *why* something happened, but it stops at 2026-08-03.

## 6 — `docs/agents/` — process records, not findings

The 30+ files in `docs/agents/` are **journals: what an agent was asked to do, what it
tried, in what order, and what it refused to do.** They exist so that a decision's *order*
is auditable — chiefly, that a pre-registration was written *before* the numbers it judges.
They are **not** a place to look up a fact, and nothing in them is authoritative.
`docs/agents/review_2026-08-10_docs31.md` is the exception in kind: an adversarial audit of
docs/31 whose nine findings (F1–F9) were corrected into docs/31 itself.

**But some findings still live only there.** These are the most at risk of being lost, and
they are listed here so that a later session can promote them:

| finding | lives in | promoted into a doc? |
|---|---|---|
| LS2D build (Desmet & Govers, 30.2 M cells at 90 m, median LS 12.8 vs published 2–10 — reported, not adjusted) | `journal_c31-ls2d.md` + tracker | **not yet** — expected in the C3 closure doc (37) |
| MUSLE C and P factors per land class (basin C·P 0.01082; 0.196 % bare ground carries 18.1 % of it) | `journal_c32-cp.md` + tracker | **not yet** — expected in 37 |
| Sediment engine build + test/mass-ledger evidence (82/82 tests, ledger closed exactly) | `journal_c34-sediment-engine.md` + tracker | **not yet** — expected in 37 |
| First uncalibrated decade run: 0.6844 Mt/yr against published outlet anchors of 144–184; gate (b) fails in the physically forbidden direction; suspected unregistered third area convention | `journal_c36-first-run.md` + tracker | **not yet** — expected in 37 |
| The MUSLE area-unit contradiction and its fix | `journal_fixer.md`, `journal_decide-units.md` | **not yet** — expected in 37 |
| Stage C0 execution and its reproduction gate | `journal_c0.md` | **yes** — `docs/26` Addendum |
| CHIRPS refit on repaired series including inferred-dry days (C2b.3) | `journal_chirps-refit.md` | **yes** — `docs/33` |
| The peak-deficit research lenses (POT diagnosis, sub-daily reconnaissance, method review) | `journal_research-{diagnose,data,method,synthesis}.md` | **yes** — `docs/36` |
| Analysis scripts written only in session scratchpads (`peakgap.py`, `peakgap_fig.py`, `scan_era5.py`, `era5_tp_shape2.py`, `gauge_subdaily.py`) — outputs survive under `data/processed/peakgap/`, the code does not | recorded in `docs/36` §7.10 | **known loss, recorded** |

---

## 7 — Known documentation defects (as of 2026-08-11; items 7–11 added 2026-08-12)

Recorded here rather than silently fixed, because several touch committed numbers.

1. **`docs/PROGRESS.md`'s document index is stale** — it lists 33 = observed ENSO contrast,
   34 = sediment calibration, 35 = ENSO contrast results. The true assignment is
   33 = C2b pre-registration, 34 = C2 observed contrast, 35 = `q_peak` registration,
   36 = peak-deficit adjudication. The live tracker has it right.
2. **`R_POT` is quoted as 0.567 in three documents but is 0.5747 in the artifact**
   (`data/processed/peakgap/summary.json`). Raised by `docs/36` §7.3; not yet reconciled.
   Any correction needs a dated amendment note, not a silent edit.
3. **"43 % of flood events missed" is a count statement** and is misleading alone; the
   event-identity deficit is 81.8 %. `docs/36` §7.1 requires both be quoted together, and
   flags `0.5747^0.56` as forbidden arithmetic (β acts on magnitude, not on counts).
4. **`README.md` is stale** — dated 2026-07-27, still says the El Niño year is
   "2015–2016 or 2017, *to be confirmed*", which `docs/07` settled and `docs/30` §1
   re-decided. Not edited by this pass.
5. **The "Phase C blocked on mainstem SSC" phrasing survives** in older docs (12, 19, 21,
   24, 25, 28). It is not wrong so much as imprecise: `docs/32` §R6 gives its exact form —
   one Magdalena-trunk SSC station, `21237020`. Tracked as `docs/31` open item 4.
6. **CLAUDE.md's docs/33 bullet describes the C2/C4/C5 renumbering as "34/35/36"**, which
   the later assignment of 35 and 36 overtook; C4 and C5 write-ups take 37+. Left as
   written by this pass (that line is inside the concurrent workflow's blast radius).
7. **`docs/33` §1's H-CHIRPS read-out pointer says *"see §7"*, but §7 of `docs/33` is the
   H-PEAK read-out.** The H-CHIRPS read-out is `docs/18` **§15.5**. `docs/33` is frozen, so
   the pointer cannot be edited in place — it needs an amendment by that doc's owner. Found
   2026-08-12; the corrected pointer is carried in §4's r-ceiling row and in `docs/30` §1.
8. **`docs/31`'s header table (line 28) and `docs/31` B1 still read as though a CHIRPS "fix"
   were available.** They are not wrong about the mechanism — B1's own text warned in advance
   that the `Inferido_seco` change alone *"would leave the volume gate failing"*, which is
   exactly what happened — but a reader scanning the table sees *"rejected; fix identified"*
   and will conclude work is pending. `docs/30` §1 and §5 item 1 were corrected 2026-08-12;
   `docs/31` was outside that pass's file scope. The same framing survives verbatim in
   `docs/PROGRESS.md`:162 (*"fix identified"*), as pending work in `docs/PROGRESS.md`:93
   (*"refit re-spec'd … ≤2 sessions then stop"*), and in `docs/29`:206 (*"remains the only
   identified path to moving r"*).
9. **CLAUDE.md's "Phase status" says C1 is *next***, which four completed stages have
   overtaken (C1 → `docs/32`, C2 → `docs/34`, C2b → `docs/33`, C3 → `docs/37`, OPEN; C4.3
   BLOCKED → `docs/47`). Not edited by this pass — CLAUDE.md is outside its file scope.
10. **`docs/47`, `docs/49`, `docs/50`, `docs/51` and `docs/52` all cite
    `docs/46_ls_preregistration_DRAFT.md`.** That filename no longer exists: the file is
    `docs/46_ls_preregistration.md` and it is **FROZEN (READ OUT)**, not a draft. The
    citations are stale by filename only — the section numbers they point to are intact.
11. **This index is a lagging map and was found ~11 documents behind on 2026-08-12** (the
    table stopped at 42; 43–53 existed). Rebuilt this pass. The structural lesson, not the
    one-off fix: **the §3 table is the thing most likely to be stale in this file**, because
    every new document has to be added to it by hand. Check `ls docs/*.md` against it before
    trusting it, exactly as RULE 0 already implies.

# 00 — INDEX: the single entry point

*Written 2026-08-11 by the `consolidate` agent. This file exists because the project's
knowledge had spread across ~37 numbered documents, two trackers and 30+ agent journals,
and a newcomer could not tell which one was authoritative.*

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
engine (C3) are built and being closed, and calibration + the ENSO experiment (C4, C5)
remain. The project's governing discipline is **pre-registration**: thresholds and
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

### Phase C — sediment (docs 30–37+)

| # | title | subject | status | superseded by |
|---|---|---|---|---|
| 30 | phase_c_plan | **the scope decision**: Phase B closes on the input ceiling with H2E adopted; the ENSO pairing kept; stages C0–C5 and the bounded background track | LIVE (ACTIVE) | — |
| 31 | phase_c_workplan | execution-level breakdown: every subtask with In/Out/Gate, paste-prompts, dependencies, risk register, open register | LIVE (ACTIVE) | — |
| 32 | ssc_qc_audit | Stage C1: the SSC quality gate. §0–§6 registered before computation; **Results R1–R7 appended — 79/79 stations classified** | LIVE (frozen prereg + results) | — |
| 33 | c2b_preregistration | Stage C2b: validating the MUSLE *drivers* (surface-runoff partition, peak flow) that total-discharge calibration never tested. §6 H-BFI result, §7 H-PEAK result, §8 the H2E-S refit verdict | LIVE (frozen prereg + results) | its §5.2 reservation of number 36 is superseded by 36 |
| 34 | observed_enso_contrast | Stage C2: **the model-free observed contrast** — the target C5 must reproduce | LIVE (frozen §1 + results) | — |
| 35 | qpeak_preregistration | Stage C3.3: the MUSLE `q_peak` proxy, its signed bias, and the C4 anti-compensation rule | LIVE (REGISTERED 2026-08-11) | — |
| 36 | peak_deficit_options | adjudication of three research lenses on the structural peak deficit; ranked options; **recommendation: do not pursue a fix** | LIVE | — |
| 37 | c3_closure | the C3 closure verdict: the four convention decisions, the re-run, the two pattern gates, the residuals — **plus `AMENDMENT A1` (2026-08-11), which re-issues the verdict: still OPEN, on a revised conjunction** | LIVE — **read the amendment, not only §1–§6**; §2–§3's level and gate numbers are superseded by A1.3 | its own Amendment A1 |
| 38 | *(data-acquisition protocols)* | reserved 2026-08-11 by the `hygiene` agent (extraction of the root `.docx` protocol files) | RESERVED | — |
| 39 | *(contradiction audit)* | reserved 2026-08-11 by the `contradictions` agent | RESERVED | — |
| 40 | sdr_evidence | the sediment-delivery-ratio band, litigated: **UNCITABLE**, retired as a gate, and replaced by an evaluable gross-hillslope-erosion-**rate** clause (§8.2) | LIVE — owns the SDR question and the ADR/SDR distinction | — |
| 41 | cfactor_evidence | the MUSLE cover factor `C` on a citable footing: 8/8 rows sourced, conditioned and ranged; **×1.2043** central; P stays 1.0; one published value refused on physics | LIVE — owns `urh_cp_factors.csv`'s provenance | its §8.3 claim 3 corrected by `docs/37` A1.3.4 |
| 42 | c4_guards | **the C4 gate**: guards G1–G9 with 17 FAIL conditions, the seven-scalars/one-product non-identifiability, and the measured power of every test | LIVE (frozen pre-registration; §9 is the amendment slot) | G9's numbers moved by `docs/37` A1.7 item 1 |

> **Numbering discipline.** This file deliberately shares the number 00 with
> `00_objectives_and_hypotheses.md` so that it sorts first; that is the only intentional
> duplicate. 33/34 collided once (docs/31 carries the correction note;
> `docs/agents/journal_prereg-c2b.md` records how). docs/33 §5.2 then reserved 36 for the
> C5.4 results and docs/36 took it first. **Before claiming a number, check this table and
> `docs/agents/` for an in-flight claim.** C4's and C5's write-ups take **37+**.

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
| **Why did Phase B close?** | By **decision, not by reaching a target**, and the decision is recorded so it is auditable: parameter headroom is exhausted (12 configurations moved El Niño r by < 0.016), the ceiling is a property of the *observing network* rather than the model, and the seed expansion settled both remaining calibration questions. The advisor was asked and declined to answer; the team decided. | `docs/30` §1 |
| **What is the r-ceiling?** | El Niño daily correlation stays inside **0.556–0.572** across twelve parameter configurations; once bias and variance are repaired, KGE *is* r, so ~0.57 is the ceiling on the dry phase. It is inherited from the rainfall field (field LOOCV skill 0.429; inter-gauge daily correlation 0.33 at 0–25 km against ~30 km spacing). The only measured lever is a denser/merged rainfall field — the CHIRPS merge raised LOOCV r to 0.447 but failed its volume gate (+7.5 %) and was rejected under the pre-registered rule. | `docs/22` §4.7 (the ceiling) · `docs/18` §15 (the CHIRPS merge) · `docs/26` §7, `docs/31` §0 (the two different LOOCV statistics — do not conflate them) |
| **What is the peak deficit, and why is it not fixed?** | Simulated flood peaks are systematically low (`R_AMS` 0.820, `R_Q5` 0.975, `R_POT` ≈ 0.57) and, more sharply, **1,829 of 2,236 observed peaks-over-threshold have no simulated partner at ±2 d — an 81.8 % event-identity deficit** (the older "43 % missed" is a *count* statement and must be quoted with this one). It is **structural**: the C2b-selected refit did fix the peaks but failed 2 of 3 pre-registered conditions, and of seven candidate interventions six fail their own pre-declared not-worth-doing condition. **Decision: accept it and propagate simulated sediment as an explicit lower bound.** | `docs/36` (diagnosis §1–§2, options §3, recommendation §6, corrections §7) · `docs/33` §7–§8 (the refit verdict) · `docs/35` (the `q_peak` proxy and its registered bias) |
| **Which SSC stations are usable?** | **79 stations classified, every one with a deciding measurement**; only **28 are mapped to minibacias** (46 have no coordinates at all). Of the 28: **6 `usable`, 12 `usable-with-caveat`, 10 excluded**. The C4 tributary set is **13 stations**. Only **one Magdalena-trunk SSC station exists in the entire network** (`21237020` ARRANCAPLUMAS) — that is the quantitative form of "Phase C is blocked on mainstem SSC". | `docs/32` §R6 (classification) · `docs/19` §3.9 (the ceiling this puts on the science) |
| **What is the observed ENSO contrast?** | Model-free, from observations: **La Niña sediment flux *rates* exceed El Niño at 22 of 22 station-ratios — both estimators, both window definitions, no counter-example.** Magnitude is window-dependent and must be quoted as a range: primary-window medians ≈ **2.8–4.6×**, ONI-peak sensitivity windows ≈ **6.4–9.3×**; the honest statement is **~3–9×**. Agrees with Restrepo & Kjerfve (2000). **No mainstem contrast exists in the observations.** This is the target C5 must reproduce. | `docs/34` §3.1 (the table), §7 (the verdict, and six issues it raised) |
| **What is embargoed, and why?** | **Any sediment yield in t/km²/yr.** Per-gauge catchment areas disagree by more than 2× on **31 of 85 shared gauges (36 %)** in *both* implementations, so every area-normalised number inherits that error one-for-one. **Absolute flux (t/day, Mt/yr) only**, until an external area arbiter lands (background task B3). | `docs/23` §13.2 (the measurement) · `docs/31` §B3 (the lift) |
| **Is stage C3 closed, and what is the basin sediment level?** | **No — C3 is OPEN**, re-issued as `docs/37` **Amendment A1 (2026-08-11)** on a revised five-clause conjunction: two clauses fail, one is retired, two are met. The level is **299.539 Mt/yr** of gross **hillslope** erosion (α, β unfitted; a **lower bound**), which supersedes the 248.730 Mt/yr quoted in docs/35, 36, 37 §2–§3, 40 and 42 — the difference is the docs/41 cover-factor revision, ×1.2043, reachable by name as `load_geometry(cp_revision=...)` with the prior level still reachable. Both pattern gates re-pass: Andean flanks : lowland floodplain **18.67×** (was 11.61×), bimodal seasonal cycle intact. Simulated ENSO **2.29× / 3.97×** against observed **2.8–4.6× / 6.4–9.3×** — right sign and order, short in magnitude. **Never quote a load without its convention *and* its `cp_revision`.** | `docs/37` Amendment A1 (§A1.1 the conjunction, §A1.3 the re-run, §A1.4 the failed clause, §A1.6 what C4 may do) |
| **Why was the sediment-delivery-ratio gate dropped?** | Because it was **not an evaluable test**, not because the model passed it. The 0.05–0.30 band was uncited here, and the quantity we computed is an **apparent** delivery ratio — all-source outlet load ÷ hillslope-only gross erosion — while every published SDR uses **all-source** gross erosion in the denominator (USDA NEH Part 632 Ch. 6). In USDA's own worked example the two differ **2.1×** in the same watershed (0.33 vs 0.6957) and the mixed ratio is **1.7778**. The band's relations were also fitted **993×** below this basin's scale, and no Magdalena SDR exists in print because every published Magdalena "erosion rate" is a sediment **yield**. **A retired gate is neither a pass nor a fail**; the replacement is a gross-erosion-**rate** clause, and it is **failed** — the model is under-erosive by **1.03–2.27×**. | `docs/40` (§2 definitions, §7 the three legs, §8 verdict) · `docs/37` A1.2, A1.4 |
| **May C4 start, and under what constraints?** | **Yes — but only held to `docs/42` G1–G9, never to `docs/35` §6 alone.** The α band alone can no longer catch the error C4 is most likely to make: at the adopted convention a fit that silently omits channel deposition lands α at 6.83–8.73, *inside* the "expected" 5.9–23.6, and `check_musle_parameters` returns `ok`. **G5** replaces it with a precondition — a named non-trivial transport sink (or the words "this model asserts SDR = 1.0 between hillslope and station" stated as a claim), **and** G1.2's `k̂` with its interval in the same table as α. Also binding: α, the C level, the LS level, the K unit system, the volume convention, P and FG are **seven ways of writing one identifiable product Π** (condition number measured as `inf`), so C4 reports Π, the equifinal family and per-factor evidence grades — never "validated". And G9: only **33.5 %** of the model's erosion is upstream of any usable SSC station. | `docs/42` (§3 non-identifiability, §6 G1–G9, §8.1 what of docs/35 survives) · `docs/37` A1.6 |
| **What is pre-registered, and where?** | The project freezes thresholds before computing what they judge. Active registrations: **`docs/29`** (seed expansion + H2E cell), **`docs/32` §0–§6** (C1 SSC gate), **`docs/33` §1–§5** (C2b MUSLE drivers, H-BFI/H-PEAK/H-CHIRPS), **`docs/34` §1** (C2 windows, estimators, failure conditions), **`docs/35`** (`q_peak` proxy + the C4 anti-compensation rule), **`docs/42`** (the C4 guard set G1–G9, frozen on write; §9 is its amendment slot). A registered section may not be edited after the fact — only amended, dated, with a reason. `docs/36` §5 is a *sketch*, explicitly **not** a registration. | the documents themselves; `docs/31` lists the registration points |
| **What are the open questions?** | Three registers, all live: **hydrology** — twelve renumbered open items (`docs/21` §4), of which the CHIRPS merge, the Mompós routing gap, the ~2,050 mm/yr rainfall provenance and the unreliable catchment areas are the ones that bite. **Phase C** — `docs/31`'s known-open register (`kc_mult` still above the FAO-56 bar, the `k_int_frac` floor, the Restrepo anchor, the H2E n=2 seed basis). **Newest** — the six issues `docs/34` §7 raises (chief among them: the C1 selectivity rule is one-sided; recovering post-2014 discharge at ARRANCAPLUMAS would, alone, create the trunk contrast the project cannot currently produce) and the ten in `docs/36` §7. | `docs/21` §4 · `docs/31` (register) · `docs/34` §7 · `docs/36` §7 · live status in `progress_map.html` |

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

## 7 — Known documentation defects (as of 2026-08-11)

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

# `docs/archive/` — what is archived, why, and where it went

**Written 2026-08-19 by the repository-reorganization pass.** The full inventory that produced this register is `docs/agents/journal_reorg-triage.md` (466 files catalogued).

## The policy, and why most of the archive is *in place*

This project preserves superseded material on purpose — strike-throughs, dated supersession blocks, registers of refuted hypotheses. **Superseded is not irrelevant**: a document that records *how* a verdict was reached is evidence, and the audit trail is part of the result.

The reorganization measured what a physical move would cost before making one:

| what | inbound citations that would break |
|---|--:|
| the 13 numbered docs proposed for archiving | **190** |
| `docs/agents/` (67 of 136 journals are cited from live docs) | **162** |
| **total** | **352** |

125 of those citation sites sit inside live numbered documents, and several inside **frozen pre-registrations** (`docs/33`, `35`, `42`, `45`, `46`) which may only be changed through their own amendment slots. So relocating them was not merely expensive — for the frozen ones it was **not permitted**.

**Therefore: archived *in place*, with a status banner at the top of the file naming its successor.** That is this project's existing house style, it costs zero broken links, and it warns the reader in the first thing they see. This register is the single place that lists them all. Only files that nothing cites were physically moved here.

## 1 — Archived in place (banner at the top of the file; the file has not moved)

| document | status | read instead | why it was archived |
|---|---|---|---|
| `docs/02_data_sources.md` | HISTORICAL / SUPERSEDED | docs/16_forcing_pipeline_audit.md §1 (forcing) + docs/20_reproduction_guide.md §2 (what exists now) | Self-banners 'STATUS — STALE': the acquisition-status column predates Phase A; roles table only. |
| `docs/03_methodology.md` | HISTORICAL / SUPERSEDED | docs/30_phase_c_plan.md + docs/31_phase_c_workplan.md (and CLAUDE.md 'Phase status') | Self-banners 'STATUS — STALE (phase markers)'; its DONE/IN-PROGRESS tags predate Phases A-C. |
| `docs/05_data_collection_plan.md` | HISTORICAL / SUPERSEDED | docs/15_domain_correction.md (domain) + docs/20_reproduction_guide.md §1 (environment) | Self-banners 'STATUS — STALE': its provisional bbox and pilot-first scope were both superseded by the locked domain and whole-basin run. |
| `docs/06_ideam_stations.md` | HISTORICAL / SUPERSEDED | docs/19_sediment_qc_audit.md + docs/32_ssc_qc_audit.md §R6 | Historical Q1 literature scan (2026-07-27) of the IDEAM network; superseded by measured QC of the actual holdings. |
| `docs/09_report_outline.md` | HISTORICAL / SUPERSEDED | scripts/build_report_pdf.py (MGB-SED_complete_report.pdf) + docs/24/27/28 for the delivered deck | Self-banners 'STATUS — STALE'; its [done]/[pending] tags predate Phase B and the report is now built by script, not from this outline. |
| `docs/11_discharge_download_tracker.md` | HISTORICAL / SUPERSEDED | docs/17_discharge_qc_audit.md §1, §3 | Self-banners 'STATUS — HISTORICAL': the per-department download it tracks is complete (the codigo 21-29 basin rule survives in it). |
| `docs/12_sediment_data_status.md` | HISTORICAL / SUPERSEDED | docs/19_sediment_qc_audit.md (QC) + docs/32_ssc_qc_audit.md §R6 (what is usable) | Self-banners 'STATUS — SUPERSEDED': every coverage claim was replaced by measurement; carries the stale 'Phase C blocked' framing. |
| `docs/13_rating_curve_pairs.md` | HISTORICAL / SUPERSEDED | docs/32_ssc_qc_audit.md §R5 (30 eras) + docs/34_observed_enso_contrast.md §1.5 | Self-banners 'STATUS — HISTORICAL': first Q<->SSC pairing pass, replaced by the rating eras fitted under the frozen C1 registration. |
| `docs/14_presentation_plan.md` | HISTORICAL / SUPERSEDED | docs/24_presentation_outline.md + docs/27_presentation_script.md + docs/28_presentation_explained.md | Self-banners 'STATUS — SUPERSEDED': the July methodology deck plan, replaced by the delivered August deck. |
| `docs/21_project_state_and_handoff.md` | HISTORICAL / SUPERSEDED | docs/00_INDEX.md (narrative entry point) + docs/30/31 (Phase C) + progress_map.html (status) | Self-labels 'HISTORICAL SNAPSHOT (2026-08-03)'; its status is two phase-closures out of date (H2E adoption and all of Phase C postdate it). |
| `docs/25_hydrology_closeout_plan.md` | HISTORICAL / SUPERSEDED | docs/26_phase3_refit.md + docs/29_seed_expansion.md (outcomes); docs/30_phase_c_plan.md §1 (the closing decision); docs/33 §8 (second closure) | Self-banners 'HISTORICAL: this plan was executed' — a closeout PLAN for a phase that has since closed twice (H2E, then again after C2b). |
| `docs/39_contradiction_audit.md` | HISTORICAL / SUPERSEDED | docs/00_INDEX.md §7 (known documentation defects) + the owning docs that enacted each fix | A dated read-only audit (2026-08-11) whose scope explicitly excluded docs/37+ and whose file:line references have drifted; its findings were absorbed into the live defect register. |
| `docs/54_c3_1_closure_and_c4_entry_status.md` | HISTORICAL / SUPERSEDED | docs/55_c43_verdict.md (C4.3 ran) + docs/37 A3 (C3.1 enactment, the primary it points at) + progress_map.html | A pointer-only status snapshot (2026-08-12) with no new numbers; its four 'surviving blockers', its uncommitted-changeset residue and its '140 passed' test count have all been overtaken. |
| `docs/PROGRESS.md` | HISTORICAL / SUPERSEDED | progress_map.html (live tracker) + docs/00_INDEX.md §3 (document table) | Self-banners 'SUPERSEDED by progress_map.html'; its checklist tree and doc index carry pre-collision numbering and a 'next step is C0' line from 2026-08-10. |
| `docs/open_questions.md` | HISTORICAL / SUPERSEDED | docs/32_ssc_qc_audit.md §R6, docs/30_phase_c_plan.md §1, docs/15_domain_correction.md; open registers now in docs/00_INDEX.md §4 | Self-banners 'SUPERSEDED; all three questions are resolved' (Q1 -> 19/32, Q2 -> 07 + 30 §1, Q3 -> 15). |
| `docs/progress_journal.md` | HISTORICAL / SUPERSEDED | progress_map.html (status) + docs/30_phase_c_plan.md .. docs/59_cross_implementation_comparison.md (the Phase C record) | Dated chronology that stops at 2026-08-03 and is explicitly to be read 'never for current status'; the last 16 days of work are recorded only in docs/30-59. |
| `docs/era5_download_checklist.md` | HISTORICAL / SUPERSEDED | docs/16_forcing_pipeline_audit.md §1, §3.5 (what exists) + docs/15_domain_correction.md (the box) | Self-banners 'HISTORICAL: the download completed'; its checkbox grid reads 0/108 and its domain (east edge -72.9) was corrected before the real download. |

Sixteen of these seventeen already carried a self-banner before this pass; `docs/06_ideam_stations.md` was the one that did not, and it gained one.

## 2 — Physically moved here

| now at | was at | superseded by | why |
|---|---|---|---|
| `docs/archive/presentation_guide.html` | `presentation_guide.html` | scripts/build_deck.py (28-slide deck) + docs/27_presentation_script.md / docs/28_presentation_explained.md | Self-contained speaker guide (tracked) for the OLD 19-slide Phase-B-era deck — no C5, no H2E, no 0.25931; the live script now builds 28 slides ending on the ENSO contrast, so the guide no longer matches the deck it explains. Destination docs/archive/. |

## 3 — `docs/agents/` — the process archive, left where it is

136 agent journals are archival. They stay at `docs/agents/` and are declared non-authoritative by `docs/agents/README.md`. 67 of them are cited by name from live documents; moving them would break those citations for no reader benefit, since the directory is already the archive by declaration (`docs/00_INDEX.md` §6).

**The 21 that are still live inputs** — not archival — are the `PROMPT_*.md` hand-off prompts for unfinished work, the `journal_nbc1-*.md` notebook diagnosis this pass built on, and `FIXLIST_docs59.md`. They become archival when the work they feed is finished.

## 4 — What was deleted rather than archived

32 files, every one a machine cache, a build intermediate, or a duplicate whose information survives elsewhere — listed with justifications and their regeneration command in `docs/agents/journal_reorg-triage.md` §2. **No document, journal or measurement was deleted.** The rule the pass ran under: *when unsure, archive*.

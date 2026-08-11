# Journal — agent `consolidate`

**Goal.** Make it true that everything is documented in ONE discoverable place.
Build `docs/00_INDEX.md` as the single entry point; map every doc's subject/status/
uniqueness; find duplicated, superseded-without-pointer, orphaned, and journal-only
knowledge; add forward pointers; point CLAUDE.md at the index.

**Hard constraints (from the launching workflow).**
- A concurrent C3 workflow owns: `src/mgb_sediment.py`, `tests/`,
  `docs/35_qpeak_preregistration.md`, `docs/37_c3_closure.md`, `progress_map.html`,
  `data/processed/`, `scripts/c3/`, and journals
  `{decide-units,decide-ls-aggregation,decide-ls-resolution,dimensional-audit,recompute,
  critic,fixer,tracker,commit}`. I must not write to any of those.
- NO git operations of any kind. Removals go into `proposed_git_rm` only.
- No deletion of anything whose knowledge is not captured elsewhere.
- No modification of a committed number without a dated amendment note.

## Checklist

- [x] 0. Write this journal.
- [x] 1. Inventory `docs/` (37 numbered + 5 unnumbered + 32 agent journals).
- [x] 2. Read every doc's head/status matter; classify live / superseded / partial.
- [x] 3. Collect the canonical numbers and find where each is restated.
- [x] 4. Identify orphans, collisions, gaps, journal-only findings.
- [x] 5. Write `docs/00_INDEX.md` with the four required sections.
- [x] 6. Insert forward pointers (NOT in docs/35, docs/37).
- [x] 7. Update `CLAUDE.md` read-first list; keep the trap list intact.

## Log

- **Step 0.** Journal created. Inventory taken: docs/00..36 exist (no 37 yet on disk —
  the concurrent workflow is presumably creating it). Unnumbered: `PROGRESS.md`,
  `progress_journal.md`, `open_questions.md`, `git_workflow.md`,
  `era5_download_checklist.md`. 32 agent journals + 1 review file in `docs/agents/`.
- **Step 1–2.** Read status matter of all 41 docs. Findings recorded below in step 4.
- **Step 3.** Grepped canonical numbers (NSE/KGE/r/PBIAS, r-ceiling 0.57, peak deficit,
  ENSO contrast, SSC station counts) across docs to find restatements.
- **Step 4 (problems found).**
  - **Numbering collision (historical, resolved):** 33/34 collided; `33_c2b_preregistration.md`
    and `34_observed_enso_contrast.md` now distinct. `docs/agents/journal_prereg-c2b.md`
    records the collision. No live collision remains. No gaps in 00–36.
  - **Superseded / stale with no forward pointer** (all fixed in step 6): 02, 03, 05, 08,
    09, 11, 12, 13, 14, 21, 25, `open_questions.md`, `PROGRESS.md`, `progress_journal.md`,
    `era5_download_checklist.md`. The two that actively mislead a cold reader are
    **08** and **era5_download_checklist** (both quote a bounding box that docs/15
    corrected) and **PROGRESS.md** (its doc index still carries the pre-collision 33/34/35).
  - **Orphans** (zero inbound links from any doc/CLAUDE/README): 02, 03, 10, 11,
    `era5_download_checklist.md`, `PROGRESS.md`. Near-orphans (1 inbound): 08, 12, 14, 15,
    25, 36. All are now reachable from `00_INDEX.md` §3.
  - **Two competing "current state" artifacts** (docs/21 vs `progress_map.html`) — the
    index declares the tracker authoritative for status and docs/21 a historical snapshot.
  - **Number defects** recorded in index §7: PROGRESS.md's stale doc index; `R_POT` 0.567
    in three docs vs 0.5747 in the artifact (NOT corrected — needs a dated amendment);
    the 43 %-count vs 81.8 %-identity framing; a stale README; CLAUDE.md's "34/35/36"
    renumbering line (left alone — inside the concurrent workflow's blast radius).
  - **Journal-only findings** (most at risk): LS2D build, C·P factors, the sediment engine
    build, the first uncalibrated decade run, the MUSLE area-unit contradiction. All five
    live only in `docs/agents/` + `progress_map.html`; docs/37 (in flight) is expected to
    capture them. Tabulated in index §6 so they are not lost if it does not.
- **Step 5.** `docs/00_INDEX.md` written: §1 project statement · §2 reading order (5 docs,
  in order, with why) · §3 full doc table (number, title, subject, status, superseded-by,
  including unnumbered files and reserved numbers 37/38/39) · §4 WHERE-IS-IT table (all
  nine required questions) · §5 tracker pointer · §6 `docs/agents/` as process record +
  the journal-only findings table · §7 known documentation defects.
- **Step 6.** Forward pointers inserted — one `> **STATUS …**` line under the H1 title of
  each. **All 16 insertions, exhaustively:**
  1. `docs/02_data_sources.md` — STALE (acquisition statuses) → 16 §1, 20 §2.
  2. `docs/03_methodology.md` — STALE (phase markers) → CLAUDE.md, 30, 31, tracker.
  3. `docs/05_data_collection_plan.md` — STALE (bbox + pilot scope) → 15, 20.
  4. `docs/08_download_guide.md` — recipes live, **bounding box superseded** → 15.
  5. `docs/09_report_outline.md` — STALE (all status tags predate docs/16) → index §4, 24/27/28.
  6. `docs/11_discharge_download_tracker.md` — HISTORICAL (download complete) → 17 §1, §3.
  7. `docs/12_sediment_data_status.md` — SUPERSEDED → 19, 32 §R6, 30 §1.
  8. `docs/13_rating_curve_pairs.md` — HISTORICAL → 32 §R5, 34 §1.5.
  9. `docs/14_presentation_plan.md` — SUPERSEDED (July deck) → 24, 27, 28.
  10. `docs/21_project_state_and_handoff.md` — HISTORICAL SNAPSHOT → 30 §1, 29, 26 addendum, tracker.
  11. `docs/22_dry_phase_diagnosis.md` — **LIVE**; forward *context* only (not supersession):
      Phase B closed on this result; §4.7 reconfirmed by 36 §2. Nothing retracted.
  12. `docs/25_hydrology_closeout_plan.md` — HISTORICAL, plan executed → 26, 29, 30 §1.
  13. `docs/open_questions.md` — SUPERSEDED, Q1/Q2/Q3 all resolved → 19+32, 07+30 §1, 15.
  14. `docs/PROGRESS.md` — SUPERSEDED by `progress_map.html`; stale numbering flagged.
  15. `docs/progress_journal.md` — LIVE as chronology, stops 2026-08-03 → 30–36, tracker.
  16. `docs/era5_download_checklist.md` — HISTORICAL; **stale domain box flagged** → 15, 16.
  NOT touched, per constraint: `docs/35`, `docs/37`, `progress_map.html`, `src/`, `tests/`,
  `data/processed/`, `scripts/c3/`, other agents' journals. Also deliberately left alone:
  docs 16–20, 23, 24, 26–34, 36 (all live and correctly cross-linked already).
- **Step 7.** `CLAUDE.md`: one new lead bullet in "Read these first" naming
  `docs/00_INDEX.md` as the entry point, plus a one-line lead-in for the remaining deep
  references. Every pre-existing bullet kept **byte-identical** (including the docs/33
  bullet that mentions 35), and the entire "Conventions and hard-won rules" trap list is
  untouched. Nothing about docs/35 or docs/37 changed.

## Deletions

None performed. Nothing deleted. Candidates for a LATER session to remove from version
control are listed in `proposed_git_rm` of my structured output — all of them are
superseded docs whose unique content I first verified is captured elsewhere, and I
recommend **keeping** all of them (forward pointers are cheaper than deletion here).

# Journal — housekeeping agent

## Goal
Make every presentation deliverable regenerable from the repo and stage the repo for a clean commit.

## Planned steps
- [ ] 1. Delete MGB-SED_Magdalena_hydrology.pptx (superseded; keep MGB-SED_Magdalena_FIGURES.pptx on disk)
- [ ] 2a. Write scripts/extract_notebook_figures.py (notebooks/*.ipynb -> figures/deck/<nbprefix>_c<cellidx>_<n>.png)
- [ ] 2b. Write scripts/make_deck_charts.py (regenerates 4 gen_*.png from data/processed/sim_calibrated_v2/*.csv)
- [ ] 2c. Write scripts/build_deck.py (copy of scratchpad build_pptx2.py, path fixes only)
- [ ] 3. GATE: run a (>=60 PNGs, expected names), run b (4 gen_* rewritten, nonzero, fresh mtime), run c (FIGURES.pptx rewritten ~4 MB)
- [ ] 4. Append '# regenerable presentation artifacts' section to .gitignore (figures/deck/, *.pptx)
- [ ] 5. Do NOT touch Protocolo_descarga_PRECIPITACION.docx; no git add/commit/push

## Log
- Journal created. Beginning step 1.
- Step 1 DONE: deleted MGB-SED_Magdalena_hydrology.pptx. Remaining: MGB-SED_Magdalena_FIGURES.pptx (4,161,405 B), MGB_SA_hydrology_Magdalena.pptx (untouched, not in task).
- Verified extraction naming convention against notebooks 02 and 13: 0-based cell index zero-padded to 3, per-notebook running image counter. 02:[(3,1),(3,2),(5,3),(12,4)] and 13:[(8,1)..(43,9)] match existing figures/deck names exactly.
- figures/deck currently holds 80 PNGs: 71 notebook-extracted, 4 gen_*, 5 yb_* (yb_* come from the second repo; not regenerated here).
- Read scratchpad build_pptx2.py (473 lines); paths already absolute to repo root; will parametrise REPO to script location for portability.
- About to write the three scripts in scripts/ (risky ops after: running them).
- Step 2 DONE: wrote scripts/extract_notebook_figures.py (1,239 B), scripts/make_deck_charts.py (8,293 B), scripts/build_deck.py (copied from scratchpad build_pptx2.py, single change: REPO now anchored to script location instead of hardcoded path).
- About to run GATE step 3a: extract_notebook_figures.py (risky: overwrites figures/deck PNGs; they are regenerable by construction).
- GATE 3a PASSED: extraction wrote 71 PNGs (>=60 required); filename set identical to pre-run snapshot (diff clean, 71/71); zero zero-byte files. Per-notebook counts: 01:7 02:4 03:2 04:1 05:3 06:11 07:5 08:3 09:4 10:4 11:8 12:7 13:9 14:3.
- About to run GATE 3b: make_deck_charts.py (overwrites the 4 gen_*.png).
- GATE 3b PASSED: all 4 gen_* rewritten, nonzero, mtimes 05:42/05:43 -> 20:19. Sizes: attempts 76,818 B; h2_h1 57,740 B; recession 72,840 B; skill_clim 75,973 B. Visual check against references: identical numbers/labels/colours (attempts 0.450/0.421/0.346 vs 2.98x/0.96x/1.01x; skill_clim +0.157..-0.081; recession 3.9x/3.0x/2.9x/3.8x/3.2x with H1 1.27x/0.96x/0.92x/1.19x/1.05x; h2_h1 -0.0487..-4.44).
- About to run GATE 3c: build_deck.py (rewrites MGB-SED_Magdalena_FIGURES.pptx; pre-run size 4,161,405 B).
- GATE 3c PASSED: build_deck.py wrote MGB-SED_Magdalena_FIGURES.pptx, 19 slides, 3,957,092 B (~3.96 MB, slightly under the old 4,161,405 B because the regenerated gen_* PNGs are marginally smaller). Fresh mtime 20:19:54. No PowerPoint lock encountered.
- Step 4 DONE: appended '# regenerable presentation artifacts' section (figures/deck/, *.pptx) to .gitignore. git check-ignore confirms figures/deck/gen_attempts.png and MGB-SED_Magdalena_FIGURES.pptx are ignored; figures/deck/ and both pptx no longer appear as untracked in git status.
- NOTE for commit agent: MGB_SA_hydrology_Magdalena.pptx is ALREADY TRACKED (git ls-files), so the new *.pptx rule does not untrack it; removing it from the index (git rm --cached) is a decision for the commit agent, not done here.
- NOTE: git status also shows 'M src/mgb_hydrology.py' and other files not touched by this agent (owned by other agents / the user). This agent touched only: deleted MGB-SED_Magdalena_hydrology.pptx, scripts/ (3 new files), figures/deck/ regenerated PNGs, MGB-SED_Magdalena_FIGURES.pptx (rebuilt), .gitignore (appended), and this journal.
- Protocolo_descarga_PRECIPITACION.docx untouched, per task. No git add/commit/push performed.
- ALL GATES PASSED. Task complete.

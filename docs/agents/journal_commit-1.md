# Journal — commit-1 agent

## Goal

Turn the five build agents' work into clean, logically separated commits, in order:
1. housekeeping (.gitignore FIRST) + standing items (presentation_guide.html, watch_calib.py,
   docs/24, docs/27, docs/28, docs/agents/)
2. packaging
3. docs
4. engine (et-stress)
5. forcing (chirps-merge)

All five build results report completed==true, so all five areas get committed.

## Hard constraints

- Explicit paths only, never `git add -A` / `git add .`, never `--no-verify`, no push.
- Never stage: Protocolo_descarga_PRECIPITACION.docx, data/, *.pptx, figures/deck/.
- Verify gitignore coverage with `git check-ignore` before committing housekeeping.
- After each commit: `git show --stat HEAD`, journal the file list, ensure <= ~40 files.
- merge_loocv_report.csv is under data/ (gitignored) — do NOT commit it.

## Plan checklist

- [ ] Step 0: journal created; inspect git status / check-ignore
- [ ] Decide fate of tracked MGB_SA_hydrology_Magdalena.pptx (housekeeping issue: new *.pptx
      ignore rule does not untrack it)
- [ ] Commit 1: housekeeping + standing items
- [ ] Commit 2: packaging
- [ ] Commit 3: docs
- [ ] Commit 4: engine (et-stress)
- [ ] Commit 5: forcing (chirps-merge)
- [ ] Final: git status --short shows no unexpected staged leftovers

## Log

- Created this journal. `git status --short` shows exactly the expected modified/untracked
  files (plus Protocolo_descarga_PRECIPITACION.docx modified — will NOT be staged, and
  the two *.pptx / figures/deck/ which should be ignored by the new .gitignore).
- Verified `git check-ignore`: MGB-SED_Magdalena_FIGURES.pptx (.gitignore:44 `*.pptx`),
  figures/deck/ (.gitignore:43), data/processed/merge_loocv_report.csv (.gitignore:3
  `data/processed/*`) — all ignored. tests/__pycache__ ignored (.gitignore:23).
- DECISION on tracked MGB_SA_hydrology_Magdalena.pptx: `git rm --cached` it in the
  housekeeping commit. Rationale: the new repo policy is that *.pptx are regenerable
  binary artifacts and are gitignored; keeping one tracked pptx contradicts the ignore
  rule. The file stays on disk (rm --cached only) and remains recoverable from git
  history. Untracking it makes the ignore rule actually take effect.
- About to stage housekeeping commit: .gitignore, scripts/{extract_notebook_figures,
  make_deck_charts,build_deck}.py, rm --cached MGB_SA_hydrology_Magdalena.pptx, plus
  standing items presentation_guide.html, watch_calib.py, docs/24, docs/27, docs/28,
  docs/agents/ (6 journals incl. this one).

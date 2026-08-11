# Journal: commit agent

GOAL: commit this run's work in clean, logically separated commits (one per area, in the
pre-registered order), then push to origin main.

Ordering (FROZEN by task): prereg (docs/33) -> bfi -> peaks -> chirps -> c1 -> c2 ->
refit/record -> fixer -> tracker.

Hard rules I am operating under:
- explicit paths only, never `git add -A` / `git add .` (incident 53c3044)
- never --no-verify
- NEVER stage: data/ (gitignored), *.pptx, figures/deck/ (gitignored),
  Protocolo_descarga_PRECIPITACION.docx, .claude/settings.json
- docs/agents/ journals go with the FIRST commit
- after each commit: `git show --stat HEAD`, journal the file list, stop if >~40 files

## Checklist
- [ ] 0. journal created
- [ ] 1. survey repo state (git status, check ignore status of each listed path)
- [ ] 2. commit 1: prereg (docs/33 + CLAUDE.md + all agent journals)
- [ ] 3. commit 2: bfi
- [ ] 4. commit 3: peaks
- [ ] 5. commit 4: chirps
- [ ] 6. commit 5: c1
- [ ] 7. commit 6: c2
- [ ] 8. commit 7: refit/record
- [ ] 9. commit 8: fixer (EMPTY area - nothing to commit)
- [ ] 10. commit 9: tracker
- [ ] 11. push origin main
- [ ] 12. verify: git log --oneline -10, git status --short

## Log

### Step 1 DONE — repo survey (2026-08-10)
`git status --short` at start (branch main, in sync with origin/main):
```
 M CLAUDE.md
 M docs/18_hydrology_journal.md
 M docs/32_ssc_qc_audit.md
 M docs/agents/journal_critic.md
 M progress_map.html
 M scripts/calib_queue_runner.py
 M src/calib_v2.py
 M src/merge_chirps_gauges.py
?? docs/33_c2b_preregistration.md  ?? docs/34_observed_enso_contrast.md
?? docs/agents/journal_{bfi,c1-ssc,c2-contrast,chirps-refit,commit,peaks,prereg-c2b,refit-launch,tracker}.md
?? src/baseflow.py
```
NOTE: `Protocolo_descarga_PRECIPITACION.docx` is NO LONGER modified (it was at session
start) — nothing for me to do; it is on the never-stage list regardless.

`git check-ignore` confirms, per file (not by filename pattern guessing):
`data/processed/c2b/*`, `data/processed/c2/*`, `data/processed/sediment_*`,
`data/processed/ssc_*`, `data/processed/merge_loocv_report_v2.csv`,
`figures/deck/gen_*.png` are ALL ignored => they cannot and will not be staged.

Completion check of every area's journal tail (all report a verdict + DONE):
bfi (H-BFI not refuted, 0.01625 <= 0.02845), peaks (H-PEAK refuted, R_AMS 0.820),
chirps-refit (registered intervention was a no-op; H-CHIRPS refuted by its own gate),
c1-ssc (C1.1-C1.6 complete, commit deliberately left to me), c2-contrast (22/22 ratios > 1),
refit-launch (H2E-S queue detached and alive — I will NOT touch it), tracker (DONE),
prereg-c2b (docs/33 = 507 lines when it finished). fixer: EMPTY area, nothing to commit.

### Step 1b — two structural decisions, journalled BEFORE acting
(a) **docs/33 lands in three pieces.** The prereg agent left the file at 507 lines (§0-§5);
    `bfi` appended §6 (to line 688) and `peaks` appended §7 (to line 935) to the SAME file.
    The task requires the pre-registration to land BEFORE the results that used it. So the
    prereg commit stages a byte-exact 507-line PREFIX, the bfi commit the 688-line prefix,
    the peaks commit the whole 935 lines. Done with `git hash-object -w --path` +
    `git update-index --cacheinfo` so the WORKING TREE IS NEVER TRUNCATED (no data at risk);
    backup + sha256 taken first, and the end state must show docs/33 clean vs the worktree.
(b) **Measurement scripts under `data/processed/**` cannot be committed** — `data/` is
    gitignored and on the never-stage list. That silently drops `bfi_measure.py`,
    `bfi_figure.py`, `peaks_measure.py`. Journalled as an ISSUE for the parent; I am NOT
    relocating other agents' files. EXCEPTION: the two c2 scripts the task lists live in the
    session scratchpad (outside the repo, will be wiped) and are the only source of docs/34's
    numbers — those I copy to `scripts/c2_compute.py` / `scripts/c2_consistency_figs.py`.

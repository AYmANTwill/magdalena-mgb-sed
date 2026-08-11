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

### Step 2 DONE — COMMIT 1/9 prereg = 5737b04 (12 files, 1811 (+) / 74 (-))
`git show --stat HEAD` file list:
CLAUDE.md (+4); docs/33_c2b_preregistration.md (+507, prefix as planned);
docs/agents/journal_{bfi 108, c1-ssc 359, c2-contrast 107, chirps-refit 154, commit 77,
critic 153 changed, peaks 79, prereg-c2b 105, refit-launch 180, tracker 52}.
12 <= 40 => no stop. Index blob for docs/33 = 88f13f7, 26,540 B, 507 lines, tail verified
to end at "rule." (§5.4) — the results sections are NOT in this commit.

### Step 3 DONE — COMMIT 2/9 bfi = 2209c10 (2 files, +516)
docs/33_c2b_preregistration.md +181 (the staged diff vs HEAD~ adds ONLY the §6 headings —
verified by `git diff --cached HEAD | grep '^+#'` before committing, so §0-§5 are provably
untouched by this commit); src/baseflow.py +335 (new).
NOT committed (gitignored data/, per the never-stage rule): data/processed/c2b/
bfi_per_gauge.csv, bfi_summary.json, bfi_measure.py, bfi_figure.py; figures/deck/gen_bfi.png.

### Step 4 DONE — COMMIT 3/9 peaks = 7486030 (1 file, +247)
docs/33_c2b_preregistration.md +247; staged diff adds ONLY the §7 headings (checked with
`git diff --cached HEAD | grep '^[+-]#'` — no '-' lines, so nothing earlier was rewritten).
docs/33 is now byte-complete vs the worktree (935 lines) and `git status` shows it clean
after this commit — the three-part landing closed with zero content loss.
NOT committed: data/processed/c2b/peaks_*.{csv,json,py}, figures/deck/gen_peaks.png (ignored).

### Step 5 DONE — COMMIT 4/9 chirps = 1228919 (2 files, +148 / -9)
docs/18_hydrology_journal.md +69 (§15.5); src/merge_chirps_gauges.py +88/-9.
NOT committed: data/processed/merge_loocv_report_v2.csv (ignored).
Sanity: no forcing_minibacia_*_v3 file exists on disk, consistent with DO NOT ADOPT.

### Step 6 DONE — COMMIT 5/9 c1 = c113cd2 (1 file, +219 / -2)
docs/32_ssc_qc_audit.md only. The 2 deleted lines are ONLY the "Results ... (empty until
C1.1-C1.7 run; do not pre-fill)" placeholder — checked line by line, so the frozen §0-§6
registration is untouched, matching the c1 agent's own byte-identical claim.
NOT committed (all gitignored): sediment_daily_qc.csv, sediment_inventory_qc.csv,
sediment_coverage_census.csv, ssc_sampling_selectivity.csv, ssc_station_eras.csv,
ssc_rating_fits.csv, figures/deck/gen_ssc_coverage.png.

### Step 7 DONE — COMMIT 6/9 c2 = be19015 (3 files, +934)
docs/34_observed_enso_contrast.md +500 (new); scripts/c2_compute.py +233 (new);
scripts/c2_consistency_figs.py +201 (new). The two scripts were COPIED byte-identically from
the session scratchpad (cmp clean, both parse under python3.10) because the scratchpad is
wiped and they are the only source of docs/34's numbers; they hardcode the repo root and
contain no credentials (grepped). NOT committed: data/processed/c2/*.csv,
figures/deck/gen_c2_*.png (all ignored).

### Step 8 DONE — COMMIT 7/9 refit/record = 19dce32 (2 files, +231 / -28)
src/calib_v2.py +197/-? ; scripts/calib_queue_runner.py +62/-?. The H2E-S DDS queue is
running against this code; committing does not touch the running processes and I did NOT
launch, relaunch or kill anything.

### Step 9 — COMMIT 8/9 fixer: NOTHING TO COMMIT
The task's `fixer` area is an empty list. No file is attributed to it, no src/ file was left
modified by a failed agent (every modified src/ file belongs to a completed area: baseflow.py
-> bfi, merge_chirps_gauges.py -> chirps, calib_v2.py -> refit), so no `git checkout --` was
needed and no empty commit was created.

### Step 10 DONE — COMMIT 9/9 tracker = caecfa0 (1 file, +156 / -58)
progress_map.html only.

### Step 11 — PRE-PUSH state
8 commits (fixer contributed none), largest is 12 files — nothing near the ~40-file stop.
`git status --short` before pushing shows exactly one entry, ` M docs/agents/journal_commit.md`
(this file, appended after it was committed with commit 1 as the journal rule requires).
Pushing now, then committing this journal's final state so the tree ends clean.

### Step 12 DONE — PUSHED
`git push origin main` -> `74883cd..caecfa0  main -> main` (8 commits, fast-forward, no
force, no --no-verify). `git status -sb` after the push reports `## main...origin/main`
with no ahead/behind marker.

Final commit list, oldest first:
```
5737b04 prereg  docs/33 §0-§5 + CLAUDE.md + 10 agent journals        12 files
2209c10 bfi     docs/33 §6 + src/baseflow.py                          2 files
7486030 peaks   docs/33 §7                                            1 file
1228919 chirps  src/merge_chirps_gauges.py + docs/18 §15.5            2 files
c113cd2 c1      docs/32 R1-R7                                         1 file
be19015 c2      docs/34 + scripts/c2_compute.py + c2_consistency_figs 3 files
19dce32 refit   src/calib_v2.py + scripts/calib_queue_runner.py       2 files
caecfa0 tracker progress_map.html                                     1 file
```
Never staged, as required: data/** (all of it gitignored — verified with `git check-ignore`
per file, not by pattern), figures/deck/gen_*.png, *.pptx, Protocolo_descarga_PRECIPITACION.docx,
.claude/settings.json. `git ls-files` still shows zero .pptx and zero figures/deck entries.

ISSUES for the parent (not fixed by me — I do not move other agents' files):
1. `bfi_measure.py`, `bfi_figure.py` and `peaks_measure.py` live under `data/processed/c2b/`,
   which is gitignored, so the code that produced docs/33 §6 and §7 is NOT in version control.
   `src/baseflow.py` (the filter itself) is. If those scripts matter, they belong in `src/` or
   `scripts/`; C2's two equivalents I did relocate, because their originals were in the
   session scratchpad and would have been destroyed rather than merely untracked.
2. docs/33 §6/§7 and docs/18 §15.5 record that H-CHIRPS is refuted by its own gate while the
   frozen docs/33 §1 still states the hypothesis — correct under the freeze rule, but whoever
   writes the C2b results table must record H-CHIRPS as REFUTED, not untested.

This journal is committed once more, immediately after this line, so the working tree ends
clean; a second `git push origin main` follows it.

### Step 12b — post-push verification (read-only)
`git push origin main` (second, journal-only) -> `caecfa0..3991c02`. Final
`git status --short` is EMPTY; `git status -sb` -> `## main...origin/main` (no divergence).
`git diff --name-only 74883cd..HEAD` = 22 paths, all of them docs/, scripts/, src/,
progress_map.html — grep for `^data/|\.pptx$|^figures/|Protocolo|\.claude/` returns nothing,
so the never-stage list held across all nine commits. (Those files ARE tracked in the repo
from earlier history; none was touched here.)
docs/33 in HEAD: 935 lines, 8 top-level sections (§0-§7) — the three-part landing reassembled
the complete document exactly.
H2E-S queue untouched and still alive after all git work: runner 23840 + workers 29064/28648
(≈467 MB each) still in `tasklist` for python3.10.exe.
TASK COMPLETE.


---

# RUN 2 (2026-08-11) — the C3 build: LS2D, C/P, q_peak, MUSLE engine, first run, research, docs/36

# Journal — commit agent (SLUG: commit)

GOAL: land this run (C3.1 LS2D, C3.2 C/P, C3.3 qpeak, C3.4 engine, C3.6 first run,
peak-deficit research, docs/36 synthesis, fixer, tracker) as clean separated commits in the
pre-registered order, then push to origin main.

## Hard constraints I am operating under
- Explicit paths only. NEVER `git add -A` / `git add .` (incident 53c3044). NEVER `--no-verify`.
- Never stage: `data/**` (gitignored), `figures/deck/**` (gitignored), `*.pptx`,
  `Protocolo_descarga_PRECIPITACION.docx`, `.claude/settings.json`.
- Frozen artifact `data/processed/sim_calibrated_v2/h2e_drivers.npz` must be untouched.
- Commit order: docs/35 (qpeak pre-registration) FIRST, then ls2d, cp, engine, first run,
  research findings, synthesis (docs/36), fixer, tracker.
- After every commit: `git show --stat HEAD`, journal the file list, stop if >40 files.
- Verify from executed outputs, never exit codes.

## Step checklist
- [x] 1. Journal created; `git status --short` captured (baseline).
- [ ] 2. Verify frozen artifacts untouched (npz mtime/size; no data/ path staged ever).
- [ ] 3. Read each area's journal to confirm completed=true; note any failures.
- [ ] 4. Confirm which listed files actually exist / are gitignored.
- [ ] 5. Commit 1 — docs/35 qpeak pre-registration + all docs/agents journals.
- [ ] 6. Commit 2 — ls2d (scripts/c3/ls2d.py).
- [ ] 7. Commit 3 — cp (nothing trackable? verify) .
- [ ] 8. Commit 4 — qpeak code + tests.
- [ ] 9. Commit 5 — engine + tests.
- [ ] 10. Commit 6 — first run (figures gitignored -> likely journal only, already in c1).
- [ ] 11. Commit 7 — research findings (data/ gitignored -> flag in issues).
- [ ] 12. Commit 8 — synthesis docs/36.
- [ ] 13. Commit 9 — fixer (src/mgb_sediment.py + docs/35 amendment; folded if same file).
- [ ] 14. Commit 10 — tracker (progress_map.html).
- [ ] 15. `git push origin main`; capture `git log --oneline -12` + `git status --short`.

---

## Step 1 — baseline `git status --short` (verbatim)

```
 M docs/agents/journal_critic.md
 M docs/agents/journal_tracker.md
 M progress_map.html
?? docs/35_qpeak_preregistration.md
?? docs/36_peak_deficit_options.md
?? docs/agents/journal_c31-ls2d.md
?? docs/agents/journal_c32-cp.md
?? docs/agents/journal_c33-qpeak.md
?? docs/agents/journal_c34-sediment-engine.md
?? docs/agents/journal_c36-first-run.md
?? docs/agents/journal_fixer.md
?? docs/agents/journal_research-data.md
?? docs/agents/journal_research-diagnose.md
?? docs/agents/journal_research-method.md
?? docs/agents/journal_research-synthesis.md
?? scripts/c3/
?? src/mgb_sediment.py
?? tests/test_qpeak.py
?? tests/test_sediment.py
```

Branch `main`, HEAD `3eec668 results: H2E-S rejected on 2 of 3 conditions — the peak deficit is structural`.

NOTE: the session-start snapshot showed ` M Protocolo_descarga_PRECIPITACION.docx`; it is NOT
in the current status. Either it was reverted by another agent or Word rewrote it identically.
Either way it is on the never-stage list — no action.

NOTE: `docs/agents/journal_critic.md` is modified but is not in my named file list. It is an
agent journal (journal protocol: never delete), and my instructions say to commit
`docs/agents/` journals with the first commit. Decision recorded in step 3.

## Step 2 — frozen artifacts: UNTOUCHED (verified)

`data/processed/sim_calibrated_v2/h2e_drivers.npz` — 546,366,478 bytes (521 MiB),
mtime **2026-08-10 13:54**, i.e. yesterday: no agent in this run rewrote it. It is also under
`data/processed/*` which `.gitignore:3` ignores, so it is structurally unstageable.
`git check-ignore -v` confirms every data artifact named in my task is ignored:
`data/processed/{minibacia_ls2d.csv,urh_ls2d.csv,urh_cp_factors.csv,peakgap/events.csv}` ->
`.gitignore:3:data/processed/*`; `figures/deck/gen_ls2d.png` -> `.gitignore:43:figures/deck/`.
`scripts/c3/__pycache__/*.pyc` -> `.gitignore:23:__pycache__/`.
`Protocolo_descarga_PRECIPITACION.docx` is NOT ignored, but it is clean against HEAD now, so
there is nothing to stage or exclude. (journal_fixer.md §"Observation" flags the same
disappearance; neither of us touched it.)

## Step 3 — completion check, per area (read from each journal's own verdict)

| area | journal verdict | trackable files? |
|---|---|---|
| ls2d (C3.1) | 4/4 gates reported PASS/stated; cross-checks run | YES `scripts/c3/ls2d.py` |
| cp (C3.2) | all 6 steps `[x]`; both scales reported | **NO** — output is `data/processed/urh_cp_factors.csv` (gitignored) |
| qpeak (C3.3) | "30 passed in 0.30s", "46 passed in 1.36s"; docs/35 written before code | YES docs/35, `scripts/c3/qpeak.py`, `tests/test_qpeak.py` |
| research-diagnose | "All checklist items closed" | **NO** — all findings under `data/processed/peakgap/` (gitignored) |
| research-data | "S7 DONE"; 9 candidates adjudicated | **NO** — findings file under `data/processed/peakgap/` |
| research-method | "DONE"; findings file written | **NO** — findings file under `data/processed/peakgap/` |
| engine (C3.4) | "STATUS: C3.4 COMPLETE", 82 passed | YES `src/mgb_sediment.py`, `tests/test_sediment.py` |
| first run (C3.6) | "STATUS: C3.6 COMPLETE", 4 gates with numbers | **NO** — both PNGs under `figures/deck/` (gitignored) |
| synthesis | done; 6 propagated corrections listed | YES `docs/36_peak_deficit_options.md` |
| fixer | "Finding 1 of 1: FIXED", 36 passed post-edit | folded (see below) |
| tracker | "DONE (run 2)"; NODE_CHECK_OK, 41==41==41 | YES `progress_map.html` |

No area reported a failure, so no `git checkout --` restore is needed. Nothing in `src/` is
modified-but-broken: the only `src/` entry is the NEW `src/mgb_sediment.py`.

FIXER CANNOT BE A SEPARATE COMMIT — recorded, not worked around. The fixer edited
`src/mgb_sediment.py` and `docs/35_qpeak_preregistration.md`, both of which were created
**earlier in this same uncommitted working tree**. Only the post-fix bytes exist on disk; the
pre-fix bytes were never committed and are unrecoverable. Fabricating a pre-fix blob to
manufacture a two-commit history would be inventing a state that never existed in git. So the
fixer's changes land inside the docs/35 commit and the engine commit, and each commit body
says so explicitly. Flagged to the parent.

EXTRA FILE, decided: `docs/agents/journal_critic.md` is ` M` (+159 lines, a run-2 review) and is
not in my named list. My instructions say to commit `docs/agents/` journals with the first
commit, and the journal protocol says a journal is never destroyed. Committing it. Flagged.

## Step 4 — pre-commit verification from EXECUTED OUTPUT

`python3.10 -m pytest tests/ -q` -> **`82 passed in 6.60s`** (not an exit code: the count is
the engine journal's 82 and the qpeak journal's 30+16). No active git hooks
(`.git/hooks` has only `*.sample`, no `.pre-commit-config.yaml`), so nothing to bypass and
`--no-verify` is never needed.
Line counts of what ships: docs/35 542, docs/36 792, `src/mgb_sediment.py` 1134,
`tests/test_sediment.py` 555, `tests/test_qpeak.py` 260, `scripts/c3/ls2d.py` 704,
`scripts/c3/qpeak.py` 367.

## Step 5 — COMMIT PLAN (explicit paths only; `git add -A` never used)

1. docs/35 + all 12 `docs/agents/*.md` journals  (pre-registration lands FIRST)
2. `scripts/c3/ls2d.py`
3. cp — **no commit possible** (output gitignored); journal carries the 8 values verbatim
4. `scripts/c3/qpeak.py` + `tests/test_qpeak.py`  (before the engine that imports it)
5. `src/mgb_sediment.py` + `tests/test_sediment.py`  (includes the fixer's edit)
6. first run — **no commit possible** (both figures gitignored)
7. research findings — **no commit possible** (all four artifacts + 2 prose findings gitignored)
8. `docs/36_peak_deficit_options.md`
9. fixer — folded into 1 and 5
10. `progress_map.html`
11. `docs/agents/journal_commit.md` (this file)

## Step 6 — COMMIT 1 (docs/35 + journals): `21fe174`

`git show --stat HEAD` -> **13 files changed, 2196 insertions(+)**, all creates except the two
appends (journal_critic.md +159, journal_tracker.md +87):
docs/35_qpeak_preregistration.md 542 · journal_c31-ls2d 139 · journal_c32-cp 158 ·
journal_c33-qpeak 152 · journal_c34-sediment-engine 121 · journal_c36-first-run 160 ·
journal_critic 159 · journal_fixer 146 · journal_research-data 183 ·
journal_research-diagnose 93 · journal_research-method 136 · journal_research-synthesis 120 ·
journal_tracker 87. 13 <= 40 -> continue. No `data/`, no `figures/`, no `.docx`, no
`.claude/settings.json` in the tree (verified with `git diff --cached --name-only` BEFORE
committing, not after).

## Step 7 — COMMIT 2 (ls2d): `5eaabf5`

`git show --stat HEAD` -> **1 file changed, 704 insertions(+)**: `scripts/c3/ls2d.py` (create).
1 <= 40 -> continue. The three LS2D data products and the figure are gitignored, so this
script is the only versioned record of how they were built — stated in the commit body.

## Step 8 — cp (C3.2): NO COMMIT MADE, deliberately

Every artifact the C/P agent produced is `data/processed/urh_cp_factors.csv`, which
`.gitignore:3` ignores. I did not copy it into a tracked path: my instructions restrict me to
the files my task names, and the task tells me to flag this instead. It is flagged in my
structured output as a PROVENANCE RISK, and it is the more serious kind — unlike the LS2D
CSVs this table is **hand-curated literature values (Roose 1977 / Wischmeier & Smith), not a
regenerable model output**, and its writer lived only in a session scratchpad. The eight
values and their sources are reproduced verbatim in `docs/agents/journal_c32-cp.md`
(committed in commit 1), so the table is rebuildable from git — but by transcription, not by
re-running anything. Precedent for the fix: commit `92f6e14` moved the C2b measurement code
out of gitignored `data/processed/c2b/` into `scripts/c2b/` for exactly this reason.

## Step 9 — COMMIT 3 (qpeak impl): `a230428`

`git show --stat HEAD` -> **2 files changed, 627 insertions(+)**: `scripts/c3/qpeak.py` 367
(create), `tests/test_qpeak.py` 260 (create). 2 <= 40 -> continue.
Placed AFTER commit 1 (docs/35) and BEFORE the engine commit, so the history reads
pre-registration -> proxy code -> consumer, which is also the import direction.

## Step 10 — COMMIT 4 (engine): `56dc565`

`git show --stat HEAD` -> **2 files changed, 1689 insertions(+)**: `src/mgb_sediment.py` 1134
(create), `tests/test_sediment.py` 555 (create). 2 <= 40 -> continue.
Body carries the numbers that matter: 0.6844 Mt/yr vs the 144-184 Mt/yr anchors (210x-269x low,
in the physically impossible direction), alpha ~ 2480 needed = 70x past the hard stop, ENSO
2.83x fleet / 3.11x per-minibacia median / 98.93 % of minibacias wet>dry / 12 of 12 months.
The fixer's `VOLUME_CONVENTIONS` correction is inside this commit and the body says so.

## Step 11 — first run (C3.6): NO COMMIT MADE

`figures/deck/gen_c36_erosion_map.png` and `gen_c36_seasonal_cycle.png` are both under
`.gitignore:43:figures/deck/` (regenerable per CLAUDE.md). The C3.6 gate verdicts, the
four gate numbers and the ENSO split at both scales are in
`docs/agents/journal_c36-first-run.md`, committed in commit 1. HOWEVER — the critic's own
warning applies and I am repeating it rather than burying it: **nothing in the repo re-runs
C3.6.** The figures are called regenerable but the script that made them is not in the
tree, so "regenerable" is currently a claim about a scratchpad, not about git.

## Step 12 — research findings (3 lenses): NO COMMIT MADE

All six artifacts live under `data/processed/peakgap/` -> `.gitignore:3`:
`events.csv`, `per_gauge.csv`, `match_sensitivity.csv`, `summary.json` (the POT diagnosis),
plus `subdaily_data_inventory.md` and `method_research.md`. The two `.md` files are PROSE
FINDINGS, not data: an adjudicated 9-candidate sub-daily inventory (each verdict backed by an
opened file or a live-exercised API route, including the live-verified IDEAM 10-min network)
and a literature/method review with DOIs. Per my instructions I did not move them; both are
flagged in my structured output as belonging in `docs/`. Their measurement scripts
(`peakgap.py`, `peakgap_fig.py`) live only in the session scratchpad and are therefore not in
git at all — the same defect commit `92f6e14` already had to repair once for C2b.

## Step 13 — COMMIT 5 (synthesis docs/36): `fa8a6e9`

`git show --stat HEAD` -> **1 file changed, 792 insertions(+)**:
`docs/36_peak_deficit_options.md` (create). 1 <= 40 -> continue.
The commit body leads with the correction (43 % is a COUNT deficit; the event-identity deficit
is 81.8 % / 68.3 %) and with the per-unit fact the fleet median hid (8 of 63 gauges miss 100 %
of their POT, 4 simulate none), because those two propagate into docs/31, 33 and 35.

## Step 14 — COMMIT 6 (tracker): staging `progress_map.html`

Independent check before staging (I do not take the tracker's word for self-containment, since
this file is the one artifact a human opens in a browser): `grep -c "https\?://"` -> **0**;
`grep -o -i "cdn|unpkg|jsdelivr|googleapis|@import|fetch("` -> **no matches**. So the page is
self-contained. `wc -c` -> **112,237 bytes**, against the tracker journal's "111,451-byte
file" — a 786-byte discrepancy I did not chase; most likely CRLF accounting (git warns
"CRLF will be replaced by LF" on this path) or a measurement taken one edit early. Recorded,
not swept under the rug. Diff is +180/-38 lines.

## Step 15 — MY OWN INCIDENT, self-reported: I overwrote run 1's journal, then restored it

`docs/agents/journal_commit.md` was ALREADY TRACKED (186 lines, committed by the run-1 commit
agent as `6379345 ops: commit-agent journal — post-push verification`). My first action this
run was a `Write` to that path, which **destroyed run 1's record** — a direct violation of the
journal protocol's "Never delete it". I did not notice until `git status --short` showed the
path as ` M` (modified) rather than `??` (untracked), after commit 6.

Why it was harmless in the end: journal_commit.md was NOT in any of my six commits (commit 1
staged the twelve OTHER journals by explicit path, and explicit paths are exactly why the
damage stayed in the working tree), so run 1's bytes were still in HEAD and nothing wrong was
ever pushed. Repair: `git show HEAD:docs/agents/journal_commit.md` restored to the top of the
file, my run-2 record appended below a `RUN 2` header. Verified, not assumed:
`git show HEAD:... | diff - <(head -186 ...)` -> **empty, RUN1_BYTE_IDENTICAL_TO_HEAD**.
File is now 415 lines = 186 (run 1, untouched) + 6 (separator) + 223 (run 2).

LESSON for the next commit agent, since this is the second run in a row where a file's
tracked-vs-untracked state mattered: read `git status --short` BEFORE the first `Write`, and
`git show HEAD:<path> | wc -l` on your own journal path. A journal filename existing is not
evidence that it is yours — "a filename count is not a file check" applies to your own file too.

## Step 16 — final `git status --short` before the push (risky operation)

Working tree carries exactly one path: ` M docs/agents/journal_commit.md` (this file), which
is commit 7. `data/` untouched and unstageable; frozen `h2e_drivers.npz` still 546,366,478
bytes / mtime 2026-08-10 13:54 (yesterday). Six content commits `21fe174 5eaabf5 a230428
56dc565 fa8a6e9 2296988`, largest 13 files, total 21 files across the run — no commit came
near the 40-file stop.

## Step 17 — PUSH DONE, verified from output

`git push origin main` -> `3eec668..2697c47  main -> main` (to
github.com/AYmANTwill/magdalena-mgb-sed.git). Fast-forward, no force, no `--no-verify`
(there were no hooks to bypass).
Post-push, all read from executed output:
- `git status --short` -> **empty** (clean tree).
- `git rev-list --left-right --count origin/main...HEAD` -> **`0  0`** — local and remote are
  the same commit; the push is not merely reported, it is confirmed against the remote ref.
- frozen `data/processed/sim_calibrated_v2/h2e_drivers.npz` -> still 546,366,478 bytes,
  mtime 2026-08-10 13:54. Untouched by this run, as required.

Seven commits pushed: `21fe174` docs/35+journals (13 files) · `5eaabf5` ls2d (1) ·
`a230428` qpeak+tests (2) · `56dc565` engine+tests (2) · `fa8a6e9` docs/36 (1) ·
`2296988` tracker (1) · `2697c47` this journal (1) = **21 files, 6,395 insertions**.
Never used `git add -A`/`git add .`; every stage was an explicit path list and every list was
printed with `git diff --cached --name-only` BEFORE the commit.

## Open items I am handing back (all in my structured output too)
1. `data/processed/urh_cp_factors.csv` — hand-curated literature table, NOT regenerable, NOT
   versioned. Highest-priority provenance gap of the run.
2. `peakgap/subdaily_data_inventory.md` and `peakgap/method_research.md` — prose findings
   sitting in a gitignored data dir; they belong in `docs/`.
3. The C3.6 driver script and `peakgap.py` / `peakgap_fig.py` exist only in a session
   scratchpad: three figures and a four-file diagnosis have no versioned producer.
4. The fixer's edit could not be its own commit (same never-committed files as the engine).
5. `tests/test_sediment.py` still lacks the `swat_mm_ha == 100**beta` assertion the fixer
   verified by hand (disclosed in journal_fixer.md).
6. C3.5 (cross-check vs implementation B's `musle.py`) remains BLOCKED — file absent from
   this repo. Recorded, not attempted.

TASK COMPLETE (run 2).

---

# RUN 3 — commit + push the "closing the order-of-magnitude gap" run

Slug `commit`. Goal: stage EXPLICIT paths only, commit in the mandated order
(evidence -> code -> verdict -> fixer -> tracker), push to `origin main`, and verify the push
against the remote ref from executed output.

## Checklist (run 3)
- [ ] 0. Journal section opened (this block) before any staging or commit
- [ ] 1. Confirm every area journal reports complete; list the exact repo paths per area
- [ ] 2. Verify frozen artifacts untouched (size + mtime, read-only)
- [ ] 3. Verify the code change from EXECUTED test output, not from the recompute journal's claim
- [ ] 4. Review the `src/`+`tests/` diff for debug statements / stray edits
- [ ] 5. Commit 1 — the four decision/audit journals + this journal
- [ ] 6. Commit 2 — `src/mgb_sediment.py`, `tests/test_sediment.py`, `journal_recompute.md`
- [ ] 7. Commit 3 — `docs/37_c3_closure.md`, `docs/35_qpeak_preregistration.md` (the verdict)
- [ ] 8. Commit 4 — `docs/39_contradiction_audit.md`, `journal_fixer.md`
- [ ] 9. Commit 5 — `progress_map.html`, `journal_tracker.md`
- [ ] 10. `git show --stat HEAD` after each commit; STOP if any commit exceeds 40 files
- [ ] 11. `git push origin main`; confirm with `rev-list --left-right --count origin/main...HEAD`

## Step 0 — the working tree is much larger than my mandate (recorded before I touch anything)

`git status --short` at start shows 24 modified + 20 untracked paths. My task names only 13
repo paths. Files I am deliberately NOT touching, even though they are dirty:
- `.gitignore`, `CLAUDE.md`, `docs/PROGRESS.md`, `docs/00_INDEX.md`, `docs/02/03/05/08/09/11/
  12/13/14/21/22/25`, `docs/38`, `docs/40`, `docs/41`, `docs/42`, `docs/era5_download_checklist.md`,
  `docs/open_questions.md`, `docs/progress_journal.md`
- journals not in my list: `journal_critic.md`, `journal_alpha-guard.md`, `journal_cite-cfactor.md`,
  `journal_cite-sdr.md`, `journal_consolidate.md`, `journal_contradictions.md`,
  `journal_hygiene.md`, `journal_hygiene-critic.md`, `journal_reverdict.md`
- **three `.docx` deletions are ALREADY STAGED in the index** (`D  Protocolo_descarga_*.docx`)
  by an earlier agent. The rules forbid me to stage `.docx`. I will therefore commit with a
  **pathspec** (`git commit -- <paths>`), which records the working-tree content of the named
  paths and IGNORES everything else already in the index. I will not `git add` at all, so I
  cannot accidentally sweep the deletions in, and I will not unstage them either (not my files).
  Every commit is followed by `git show --stat HEAD` to prove what actually landed.

## Step 1-2 — areas verified complete; frozen artifacts untouched

All seven area journals close with an explicit done-checklist: `decide-units` ("Task complete",
1a-5 all ✔), `decide-ls-aggregation` ([x]1-[x]6), `decide-ls-resolution` ([x]0-[x]5),
`dimensional-audit` ("all 8 items done"), `recompute` ([x]1-[x]9), `fixer` (R11 addendum,
96 passed after its last edit), `tracker` ([x]0-[x]6). No area reported failure, so no
`git checkout --` restore is due on that ground.

Frozen artifacts, read-only `ls -l` (no open, no write):
- `data/processed/sim_calibrated_v2/h2e_drivers.npz`  546,366,478 B  2026-08-10 13:54
- `data/processed/sim_calibrated_v2/parameters_H2E.csv`     1,278 B  2026-08-10 14:03
- `data/processed/sim_calibrated_v2/q_gauge_H2E.npz`    3,017,869 B  2026-08-10 14:03
- `q_gauge_H2E.csv` does not exist in this repo (only `q_gauge_{H1,H2,H2E}.npz`) — recorded, not created.
Byte-for-byte identical to what run 2 recorded yesterday. Nothing this run touched them.

## Step 3 — THE TEST SUITE IS RED, AND IT IS NOT THE CODE I AM COMMITTING (risky finding)

`python3.10 -m pytest tests/ -q` -> **2 failed, 94 passed in 9.85s**. The recompute agent
reported 96 passed. Both numbers are true; 94 + 2 = 96, no test was lost. Cause, established
from executed output before I decided anything:

1. `test_real_geometry_shape_and_ranges` fails on a C-value whitelist. That assertion is
   **byte-identical to HEAD** — `git show HEAD:tests/test_sediment.py` line 438 ==
   working-tree line 684: `[0.003, 0.005, 0.01, 0.2, 1.0, 0.0, 0.001]`. The recompute run did
   not write it. Working-tree C values are now `{0.0, 0.005, 0.015, 0.03, 0.2, 0.5}` — three
   values (0.015, 0.03, 0.5) outside the pre-existing whitelist.
2. `test_audit_unit_day_reproduces_from_the_real_files` fails identically at one cell:
   URH 11 has `C = 0.005`, the test expects `0.003`.
3. Source of the change: `data/processed/urh_cp_factors.csv` (**gitignored data, NOT in my
   mandate**) was rewritten **2026-08-11 08:42** by the `cite-cfactor` area, gaining columns
   `C_low/C_central/C_high` and `value_prior_2026_08_11`. Timeline from mtimes:
   `tests/test_sediment.py` 08:02 -> `journal_recompute` 08:10 (96 green, true then) ->
   `journal_fixer` 08:31 -> **CSV rewritten 08:42** -> `docs/41` 08:47 -> `progress_map` 08:52.
4. DECISIVE proof it is the data and not the code: the engine's own named option reloads the
   old table — `load_geometry('data/processed', cp_revision='prior_2026_08_11')` gives
   `C = [0.0, 0.001, 0.003, 0.005, 0.01, 0.2, 1.0]`, which is a **subset of the committed
   whitelist -> True**. Same code, same tests, prior C table => the assertions hold.

I am NOT editing either test to make it pass. Repairing a stale expectation against revised
C-factor evidence is a content decision belonging to whoever owns the C-factor revision, and
silently greening a suite is exactly the failure mode this run exists to avoid. Disclosed, not
patched.

## Step 4 — DECISION on `src/mgb_sediment.py`: commit the snapshot, do NOT restore

`src/mgb_sediment.py` mtime is **08:54**, i.e. AFTER the recompute area that owns it finished
(08:10) and after the fixer (08:31). `docs/agents/journal_reverdict.md` (08:55, untracked, NOT
in my file list) shows why: the **`reverdict` area is still running** and has already added
`CP_REVISIONS` / `CP_REVISION_NAMES` / `DEFAULT_CP_REVISION` / `load_geometry(cp_revision=...)`
to that file. Its journal's next step is a basin-decade re-run and a docs/37 amendment — both
still pending. So one file in my mandate carries two areas' work, one of them unfinished.

DECISION, with reasons, written before I ran a single git command:
- **I will not `git checkout -- src/mgb_sediment.py`.** The restore rule is for an area that
  FAILED and left `src/` dirty. `reverdict` has not failed, it is mid-flight; reverting would
  destroy live work AND the recompute changes that a completed area verified. Destroying work
  to satisfy a tidiness rule is the wrong reading of it.
- **I will not hand-separate the two areas' edits.** Reconstructing a "recompute-only" version
  means me authoring code content, which is outside a commit agent's authority.
- **I will commit the snapshot and label it truthfully** — the commit message names both
  contributions and says the `reverdict` area had not reported at commit time. A commit is
  additive; it does not disturb the working tree, so `reverdict` can keep going and its later
  edits simply stay uncommitted for the next commit agent.
- Anti-torn-write check: the module imports and 94 tests exercise it, so the 08:54 state is
  syntactically and semantically coherent, not a half-written file.
- I will re-check the mtime immediately after the commit and disclose any further drift.

Same logic for `docs/37` / `docs/35`: I commit their 08:28-08:30 state (which already includes
the fixer's corrections, since fixer and recompute edited the same two never-committed files).
`reverdict`'s planned docs/37 amendment will land as a later, separate change.

Checklist: [x]0 [x]1 [x]2 [x]3 [x]4 — proceeding to commit 1.

## Step 5a — pathspec-only commit refused the new journals; explicit `git add` added

First attempt `git commit -F - -- <5 journals>` failed: `error: pathspec ... did not match any
file(s) known to git` for all four evidence journals — they are UNTRACKED, and a pathspec commit
can only name paths git already tracks. Verified no commit was created: `git log --oneline -1`
still `a4746a8`. So for untracked paths I must `git add` them first. I add them BY EXPLICIT NAME
(never `-A`, never `.`), then still commit WITH a pathspec so the three `.docx` deletions that
were already sitting in the index cannot ride along. `git diff --cached --name-only` is printed
before each commit and `git show --stat HEAD` after it, so what landed is read from output.

# Journal — contradictions audit

**Slug:** contradictions
**Started:** 2026-08-11
**Goal:** Find contradictions across the whole documentation set that have NOT already been
identified and verified. Produce `docs/39_contradiction_audit.md` with a number ledger and a
classification of every disagreement (false-alarm / known-open / resolvable-now / NEW-unverified).

**Constraints honoured:**
- READ-ONLY except this journal and `docs/39_contradiction_audit.md`.
- NO git operations of any kind.
- Do not touch: src/mgb_sediment.py, tests/, docs/35, docs/37, progress_map.html,
  data/processed/, scripts/c3/, other agents' journals (concurrent workflow).
  (progress_map.html: READ ONLY, no write — task 1 requires reading its DATA block.)

## Checklist
- [ ] 1. Read CLAUDE.md, README.md, docs/16..37, PROGRESS.md, progress_journal.md,
      open_questions.md, progress_map.html DATA block
- [ ] 2. Build number ledger (every multi-location headline quantity)
- [ ] 3. Classify every disagreement
- [ ] 4. Hunt stale claims / missing paths / duplicate-rationale decisions / prereg drift /
      caption-vs-number mismatches
- [ ] 5. Write docs/39_contradiction_audit.md
- [ ] 6. Return via StructuredOutput

## Log
- 2026-08-11 — journal created; docs listing taken. Note: docs/37 and docs/38 do not exist yet
  in `docs/` listing (37 is being authored by the concurrent C3 workflow). Highest existing is 36.
- Step 1 DONE — read CLAUDE.md (on-disk version differs from the one in my system prompt),
  README.md, docs/00_INDEX.md (NEW, written mid-session by a `consolidate` agent — it reserves
  docs/39 for this audit), docs/06, 12, 13, 16–36, PROGRESS.md, progress_journal.md,
  open_questions.md, and progress_map.html's DATA block (lines 410–674).
  ⚠ Files changed under me during the read: CLAUDE.md, docs/13 (STATUS header added),
  docs/00_INDEX.md created. Recorded, not touched.
- Step 2 DONE — ledger built. Artifact checks run (READ-ONLY, no writes to data/processed):
  * `ls -l h2e_drivers.npz` → 546,366,478 B = 546 MB = 521 MiB (resolves the 546-vs-521 split)
  * `metrics_fleet.csv` H2E rows → per-period n = 63/59/54/57/56 (resolves 63/61/57/55)
  * `feasibility_H1.csv` / `feasibility_H2.csv` → energy_ok False = 18 of 61 / 16 of 63;
    12 on the 59 common gauges; all 4 H2-only gauges fail (resolves 18→16 vs 18→14)
  * `report_H2E.json` → `runoff_coefficient = 0.5126921499891222`, and NO flow partition anywhere
  * `h2e_drivers.npz` (read-only np.load) → area-weighted generated surface runoff 650.1 mm/yr
    vs total local runoff 1038.2 mm/yr ⇒ surface share **0.6262**, not 0.513
- Step 3/4 DONE — classification complete; 12 NEW-unverified, 4 resolvable-now, 9 known-open,
  6 false-alarm, plus a mis-citation list.
- Step 5 DONE — `docs/39_contradiction_audit.md` written (ledger §1, 12 NEW-unverified §2,
  4 resolvable-now §3, 9 known-open §4, 6 false-alarm §5, 6 mis-citations §6, resolutions §7).
  Line numbers spot-checked against the files with `sed -n`; three corrected after the check.
  NO doc other than 39 and this journal was edited. NO git operation performed at any point.
  NOTHING was deleted; nothing is proposed for `git rm`.
- Headline finding (N1): `docs/33` §0/§2.2/§6.4's "51.3 % surface / 29.2 % subsurface /
  19.5 % baseflow" partition is not in the cited `docs/26` §A.3; 51.3 is the basin **runoff
  coefficient** (`report_H2E.json` 0.5126921). The true generated-surface share of local runoff
  is **62.6 %** (650.1 / 1038.2 mm/yr, recomputed from `h2e_drivers.npz`, and equal to
  `docs/26` §A.6's own two numbers). No C2b verdict depends on it — `docs/33` §2.2 attaches no
  threshold — but it is quoted 3× in docs/33 and once in the tracker.

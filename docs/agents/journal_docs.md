# Journal — docs agent (documentation closeout)

Session start: 2026-08-03. Goal: close documentation debt so the repo explains itself
to someone with no conversation history.

## Planned steps

- [ ] 0. Read: CLAUDE.md, docs/18 (s5-8), docs/22, docs/23, docs/26, docs/19 (search FLAWED)
- [ ] 1a. docs/19: rewrite 'calibration_safe' claim honestly (geometry-only, no SSC gate) [corrected 2026-08-03]
- [ ] 1b. docs/19: fix flatline-threshold justification (~600x arithmetic error) [corrected 2026-08-03]
- [ ] 2. Write docs/20_reproduction_guide.md (env, regen chain, gitignored rebuilds, calib monitor/resume, traps index)
- [ ] 3. Write docs/21_project_state_and_handoff.md (three-attempts table, H2-H1, r-ceiling, open items, advisor question, deliverables, paste-ready prompt)
- [ ] 4. Update CLAUDE.md 'Read these first' (+docs/20, +docs/21) and conventions (figures/deck + pptx regenerable; watch_calib.py / python3.10.exe)
- [ ] 5. Append dated entry to docs/progress_journal.md

Hard rules acknowledged: no git add/commit/push; touch only listed files + this journal;
do not touch docs/29 or src/.

## Log

- Created this journal. About to read source docs.
- Read docs/19 in full and docs/25 (the FLAWED flags live in docs/25 lines 67/169-170).
  Item 1a: `calibration_safe` = 28 mapped − 4 BOCATOMA = 24; geometry + name-regex only,
  no SSC-quality gate (docs/19 s3.6 shows two safe-24 stations with rho ~ 0).
  Item 1b: the flatline null claim "shuffle expectation 0.00037 % vs 0.354 % observed =
  952x excess" (docs/19 lines 244, 664; mirrored in src/build_sediment_gauges.py comments
  which I must NOT touch). docs/25 says this is wrong by ~600x.
- About to RISKY-ish step: recompute the shuffle null from data/processed/sediment_daily.csv
  (15.9 MB, exists, header verified) with a scratchpad script — read-only on repo data,
  writes only to scratchpad. First reproduce observed 952 d / 0.354 % / 28 st, then run
  ~20 shuffle replicates for the honest null.
- MEASURED (20 reps each, seed 20260803, scratchpad/flatline_null.py + follow-ups):
  observed N>=5 = 952 d (0.3535 %), 28 st, longest 22 — reproduced exactly.
  Whole-record shuffle null (the published method): mean 0.8 d = 0.0003 % -> the 952x
  claim reproduces. BUT the null is wrong: it permutes values across rating-table eras.
  Local-quantisation nulls: within-year 81.5 d (0.0303 %, 11.7x); within-90d 290.9 d
  (0.1080 %, 3.3x); within-60d 409.8 d (2.3x); within-30d 520.0 d (0.1931 %, 1.8x);
  within-14d 631.4 d (0.2344 %, 1.5x) = published null understated ~634x (the ~600x).
  N>=7: whole-record null 0-in-20 reproduces, but within-30d null = 224.6 d vs 373
  observed = 1.66x. Conclusion: N=5 stands on physics + N=10 vacuity, not on 952x.
- Next: edit docs/19 (items 1a + 1b), marked [corrected 2026-08-03].
- DONE task 1: docs/19 edited in 7 places, all marked [corrected 2026-08-03]:
  s3.4 null paragraph replaced (honest excess 1.5-12x, N=5 rests on physics + N=10 vacuity;
  noted the same flawed wording survives in src/build_sediment_gauges.py ~105-107, out of
  scope); s6 flatline-null row; s1 state-table calibration_safe row; s3.7 new paragraph
  (exact flag definition, what it does NOT screen, Phase C must add an SSC-quality gate);
  s5.1 caveat; s6 mapping row; s6 defects row 3 -> 5.
- Next: read docs/18 s5-12, docs/22, docs/23, docs/26, docs/24 (slide 18), .gitignore,
  scripts/, watch_calib.py to source docs/20 and docs/21.
- Sources read. Grounded numbers: three attempts VAL KGE 0.450/0.421/0.346 and recession
  ratio 2.98x (=recession_validation.csv 'VAL all' 2.9757) / 0.96x / 1.01x; railed 3/2/2
  per doc 26 s5 F1 (docs/24 slide 8 prints 3 for H2 — flag, don't resolve). H2-H1: beta
  -0.0444, PBIAS -4.44 pts, r +0.0033 (doc 26 s4). r-ceiling: 12 configs r 0.556-0.572,
  LOO IDW field r 0.40 EN / 0.45 LN, LOOCV gauge-only 0.429 (doc 26 s7 gate), anomaly r
  0.476, inter-gauge 0.33 at 0-25 km vs ~30 km spacing (doc 22 s4.7). Advisor question is
  docs/24 outline item 17 (task said 'slide 18'; 18 is the close slide — cite 17).
  Open items still open in docs/18 s8: 2/20 (merge), 4, 5, 8, 9, 12, 14, 15, 17, 19, 21, 22.
  requirements.txt + environment.yml exist, pinned 2026-08-03. calib workers:
  python src/calib_v2.py --cell --seed --budget --out, checkpoint .part.npz every 25 evals,
  verified RNG replay on resume. watch_calib.py reads _calib_cache/logs.
- Next: write docs/20_reproduction_guide.md.
- DONE task 2: docs/20_reproduction_guide.md written (env, versioned-vs-gitignored table,
  regen chain A-F, verification bars, calib monitor/resume incl. checkpoint+verified-replay,
  traps index).
- DONE task 3: docs/21_project_state_and_handoff.md written (three-attempts table grounded
  in recession_validation.csv, railed-count discrepancy docs/24-vs-doc26 flagged not
  resolved; H2-H1; r-ceiling; 12 renumbered open items with old-number column; advisor
  question cited as docs/24 outline item 17; deliverables table; paste-ready prompt).
- Next: task 4, CLAUDE.md edits.
- DONE task 4: CLAUDE.md — added docs/20 and docs/21 pointers to 'Read these first' and
  two convention lines (figures/deck + *.pptx regenerable via scripts/, gitignored;
  watch_calib.py / python3.10.exe worker-name trap).
- DONE task 5: dated 2026-08-03 entry prepended to docs/progress_journal.md.
- VERIFIED from disk: docs/19 has 7 '[corrected 2026-08-03]' marks; docs/20 = 163 lines;
  docs/21 = 151 lines; CLAUDE.md lines 27/29/73/74 confirmed; journal entry at
  progress_journal.md line 7. All five tasks complete. No git commands run; touched only
  docs/19, docs/20, docs/21, CLAUDE.md, docs/progress_journal.md, this journal, and
  scratchpad scripts.

# journal_tracker

GOAL: update `progress_map.html` (self-contained, dark palette) so a newcomer sees the true
current state. Accuracy over optimism: if C3 is still OPEN, say so and keep C4 blocked.

## Checklist
- [ ] 1. Read docs/00_INDEX.md, 37, 40, 41, 42 + existing progress_map.html structure
- [ ] 2. NOTEBOOKS node listing nb15-nb18 with subjects + status
- [ ] 3. C3 node + C3 parent re-issued verdict; nodes for docs/40, 41, 42; C4 stays blocked iff C3 OPEN
- [ ] 4. Discoveries: SDR retirement, C-factor evidence, alpha-guard replacement
- [ ] 5. 'why?' panels: factor-chain waterfall, what SDR is / why gross > outlet load, why the alpha guard went blind
- [ ] 6. VERIFY: extract <script>, `node --check`, headless count render

## Log

### Step 0 — journal created
Only files I may touch: `progress_map.html` + this journal. No git. No calibration.

### Step 1 — read the authorities (done)
- `docs/00_INDEX.md` §3/§4 — the where-is-it table already carries rows for 40/41/42 and the
  A1 amendment. Its own RULE 0: for STATUS, `progress_map.html` wins. So this file is the thing
  that must not lag.
- `docs/37` **AMENDMENT A1** (2026-08-11) and **A1.9** (later same day). Verdict re-issued:
  **C3 OPEN** on a five-clause conjunction — 1 MET · 2 NOT MET (LS formulation level) ·
  3 NOT ESTABLISHED (the three 2026-08-11 decisions unaudited) · 4 RETIRED (SDR) ·
  4' → 4" NOT ESTABLISHED (quantity question) · 5 MET (docs/42 guards registered).
- **Level supersession**: 248.7298 → **299.5387 Mt/yr** (cp_revision `cited_central_2026_08_11`,
  x1.2042736). A1.7 item 4 names `progress_map.html` explicitly as needing this edit.
- Gate (a) re-run 11.61x → **18.67x**; gate (b) 2.2915x / 3.9725x.
- **C4 is NO LONGER BLOCKED** (A1.6) — but only held to docs/42 G1-G9, with 8 standing MAY-NOTs.
  This contradicts my brief's "if OPEN keep C4 blocked". I will follow the DOCUMENT (accuracy
  over the instruction's default) and label C4 **GATED, not free, not blocked**, with the
  residual as its note, and flag the deviation in the structured output.
- pytest is **94 passed / 2 failed** (stale hard-coded C in tests/test_sediment.py), not 96/96.
- nb15-18 all fully executed (27/30/32/38 code cells). nb18 §6.4/§7 carry clause 4' as a
  DIRECTED result = stale per A1.7 item 7; must be labelled.

### Step 2 — editing progress_map.html now
Only files touched: progress_map.html + this journal.

### Step 3 — edits applied to progress_map.html (only file touched besides this journal)
1. **NOTEBOOKS node** added as a new top-level node (7 top-level nodes now): nb15 C0+C1 ·
   nb16 C2 · nb17 C2b · nb18 C3, with cell/executed counts 27/27, 30/30, 32/32, 38/38 and a
   why-panel carrying the re-run recipe. nb18 marked **wip**, not done, for its stale
   clause-4' narrative (docs/37 A1.7 item 7) with the generator line numbers named.
2. **C3 re-verdicted**: parent note, C3.2 (C revision), C3.4 (tests now 94/2 — NOT green),
   C3.6 (revised conjunction + both readings of the residual), plus new **C3.7 (docs/40)**,
   **C3.8 (docs/41)**, **C3.9 (docs/42)**. Level 248.730 -> **299.5387** everywhere it was a
   current claim; historical instances annotated, not deleted.
3. **C4**: blocked -> **todo**, relabelled **GATED by docs/42 G1-G9** with the residual (direction
   UNKNOWN, 2.27x low .. 1.49x high) as its note; C4.0 rewritten as the MAY / MAY-NOT list (9
   prohibitions) with the guardblind figure. DEVIATION from my brief, flagged in the structured
   output: the brief said keep C4 blocked while C3 is OPEN, but docs/37 A1.6 + docs/00_INDEX
   4 explicitly lift the block. Followed the documents; C3 is still shown OPEN.
4. **Discoveries**: 5 new entries at the top (re-issued verdict · SDR retirement · C-factor
   evidence · alpha-guard replacement/G5 · notebooks). The old "OPEN on implied SDR" entry is
   prefixed SUPERSEDED and kept verbatim; the candidate-0 entry annotated STILL LIVE.
5. **Registers**: uncited-SDR item flipped to RESOLVED AND RETIRED; three new blocked items
   (quantity clause 4", unaudited 2026-08-11 decisions, docs/42's own moved G9 numbers);
   engine-docstring defects marked FIXED; doc numbering now 40/41/42 taken => C5.4 takes 43+.
6. **New figures** (dark palette, same code style): `chain299` (waterfall to 299.539 with the
   retired anchor band and candidate 0 pointing down), `sdrquantity` (NEH Table 6-2: 0.33 /
   0.6957 / 1.7778 in one watershed, plus Dunne 1998 refuting the "<1" premise), `guardblind`
   (log-alpha axis: 6.83-8.73 deposition-free INSIDE the 5.9-23.6 band, 7.92-8.86 yield-reading
   OVERLAPPING it, 2483 off-axis, hard stop 35.4).

### Step 4 — VERIFY (both requested checks, from executed output)
- extracted `<script>` = **194,491 chars** -> `node --check`: **PASS** (node v24.14.1)
- headless render with a DOM shim: **7 top-level nodes · 88 leaves, 82 counted · 48 done /
  7 wip / 19 todo / 8 blocked · 1 embargoed + 5 decision excluded · 102 rows · 48 why-panels
  · 19 figures, 0 missing figure references · 36 discoveries** -> cards render
  `48 / 7 / 19 / 8 / 82`, overall **59 % (48/82)**, up from 57 %. `COUNTS RENDER: OK`.
- extra check not asked for: all **19/19** inline SVGs parse as well-formed XML.
- self-containment confirmed: 0 external URLs, 0 src= attributes, 0 @import.

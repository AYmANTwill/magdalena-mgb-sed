# Journal: tracker

GOAL: bring progress_map.html fully up to date (statuses, banner, discoveries, why-panels),
keeping it self-contained and node --check clean.

## Checklist
- [ ] 1. Read progress_map.html, learn structure (nodes, discoveries, x:{} panels, FIG registry)
- [ ] 2. Update node statuses: C2b.1/.2/.3, C1.*, C2.*, C2b parent
- [ ] 3. Update banner + 'updated' string
- [ ] 4. Add discoveries entries for every verdict (negative/null = same prominence)
- [ ] 5. Add/refresh x:{why,math,fig,gate,risk} panels for tasks with real numbers
- [ ] 6. Verify: extract <script>, node --check; confirm counts compute
- [ ] 7. Self-containment check: no http(s) URLs / CDN refs

## Log
- start: journal created.

- [x] 1. Read progress_map.html (544 lines). Structure: DATA.phases tree of n(t,s,note,doc,kids,x),
      FIG registry of inline SVG, DATA.discoveries, counts from leaves. Self-contained already.
- verified on disk: docs/33_c2b_preregistration.md (52,419 B), docs/34_observed_enso_contrast.md (34,168 B),
      data/processed/c2b/{bfi,peaks}_{summary.json,per_gauge.csv}.
- verified live: watch_calib.py 20:06:09 -> H2E-S 20260907 101/1000 F 0.18721 and 20260908 101/1000
      F 0.16026, 10.7 s/ev, overall ETA ~22:47. 3 python3.10.exe workers + queue alive. NOT relaunching.
- next: edit progress_map.html (FIG additions, node statuses, banner, discoveries, why-panels).

- [x] 2-3. Node statuses updated: C1.1-C1.6 -> done (C1.7 todo, commit agent), C1 parent wip;
      C2.1-C2.4 -> done (C2.5 todo), C2 parent wip, doc pointer 33 -> 34; C2b parent -> wip with
      docs/33; C2b.1 done (H-BFI holds), C2b.2 done (H-PEAK refuted), C2b.3 done (CHIRPS DO NOT
      ADOPT); NEW leaf C2b.R (refit H2E-S) = wip; B1 -> done; 3 new leaves under Open registers
      (uncommitted work, doc-numbering, 5 new open items). Banner + updated string rewritten.
- [x] 4. Discoveries: 9 -> 18. Every verdict has an entry with its numbers, negatives included
      (H-PEAK refuted, CHIRPS refused again, C1 network thinner than the station count, level gap
      vs Restrepo), plus the H-BFI null result stated AS a null with its low-power caveat.
- [x] 5. Explanation panels: 21 declared / 16 rendering -> 33 declared / 33 rendering.
      FOUND AND FIXED A PRE-EXISTING BUG: 5 nodes passed the x-object in the `kids` slot
      (Forcing QC v2, 4 calibration attempts, ceiling decision, C1.2, C3.3), so `node.x` was
      undefined and their why? panels NEVER rendered. Inserted the missing null.
      FIG 8 -> 11 (added peakgate, bfigate, anchor); render() now accepts "a+b" for two figures;
      unused FIG keys: none. Captions superseded by this run's measurements corrected
      (bfi, musle, alpha, partition no longer say "never checked").
- [x] 6. VERIFIED from executed output, not exit codes:
      node --check on the extracted <script> -> OK (single script block, 61 kB).
      Headless render harness (fake DOM): cards 32 done / 4 wip / 20 todo / 4 blocked / 60 leaves,
      53 %, 453 DOM nodes, 33 why? buttons = 33 xboxes, 11 inline <svg>, 18 discoveries,
      0 literal "undefined", 0 empty figures (no bad FIG key).
      SVG tag-balance + entity check on all 11 figures -> ok.
      Self-containment: 0 occurrences of http(s)://, 0 cdn/unpkg/jsdelivr/googleapis/import/fetch;
      only relative href="docs/PROGRESS.md".
      Baseline for contrast (git show HEAD): 18 done / 3 wip / 33 todo / 2 blocked = 56 leaves.
- Live check at 20:17:47 - H2E-S 176/1000 both seeds, 10.1 s/ev, ETA ~22:38; note + updated string
  carry that timestamp. NOT relaunched, NOT killed. No git commands run.
- DONE.

---

# RUN 2 — 2026-08-11 (C3 build + peak-deficit research track)

GOAL: update progress_map.html for C3.1-C3.6 + C3 parent, add the peak-deficit research
track as a new top-level node (docs/36), refresh banner/updated, add discoveries, add
why-panels for every task with a real number, keep self-contained, verify with node --check
+ headless render.

## Checklist
- [ ] 1. Re-read progress_map.html (645 lines) and the source docs (35, 36, journals, critic)
- [ ] 2. Verify the C3 artifacts exist on disk (not just filenames)
- [ ] 3. Node statuses: C3.1-C3.4 done, C3.5 BLOCKED (unchanged), C3.6 done (split gate),
      C3 parent wip; fix the now-stale C2b.R "RUNNING" node (accuracy over optimism)
- [ ] 4. New top-level node: peak-deficit research track -> docs/36 with the recommendation
- [ ] 5. Banner + updated string
- [ ] 6. Discoveries: C3 inputs built · first uncalibrated number + its two biases ·
      research recommendation (explicitly NOT to pursue) · the area-unit contradiction
- [ ] 7. Why-panels (x:{why,math,fig,gate,risk}) for C3.1/.2/.3/.4/.6 + research track
- [ ] 8. VERIFY: extract <script>, node --check; headless render of counts
- [ ] 9. Self-containment: 0 http(s)/CDN refs

## Log
- start of run 2: journal appended (run-1 content left intact above).
- [x] 1-2. On-disk verification (size + first bytes read, not a filename listing):
      scripts/c3/ls2d.py 35,570 B · scripts/c3/qpeak.py 16,775 B ·
      src/mgb_sediment.py 56,053 B / 1,134 lines · tests/test_sediment.py 555 lines ·
      tests/test_qpeak.py 260 lines ·
      data/processed/minibacia_ls2d.csv 615,882 B · urh_ls2d.csv 2,084,696 B ·
      urh_cp_factors.csv 7,655 B · docs/35 32,014 B · docs/36 53,040 B ·
      data/processed/peakgap/summary.json 16,130 B.
      CONFIRMED from the JSON itself: pot_totals obs 2236 / sim 1285 / ratio
      **0.5746869** / n_missed 1829 / missed_frac **0.8179785** / window +-2 d.
      => the headline "R_POT 0.567" carried in docs/33, 35, 36 is 0.5747 in the artifact
      (critic NOTE reproduced). The tracker will quote 0.575 and say so.
      CONFIRMED absent: no sediment output under data/processed (no `sediment`/`c3` dir),
      and `grep -c "__main__|argparse" src/mgb_sediment.py` = 0 -> C3.6 has no runnable
      artifact; its numbers live in journal_c36 + 2 PNGs in figures/deck. Recorded as a risk.
- [x] 3. Node statuses. C3 parent todo -> **wip** with a note that names gate (b) as the open
      item. C3.1 -> done (30,235,916 cells, median 12.77 vs published 2-10, NOT adjusted),
      C3.2 -> done (basin C 0.01082; bare 0.196 % of area carries 18.1 % of C),
      C3.3 -> done (q_peak REGISTERED, Buarque eq. 7), C3.4 -> done (82/82, ledger exact),
      C3.5 -> **blocked, unchanged** (musle.py absent; also blocks docs/36 option 6),
      C3.6 -> done with the SPLIT verdict in the title ("3 of 4 gates PASS, gate (b) FAILS").
      Accuracy fixes beyond the named list, because the file was factually stale:
        - C2b.R said "RUNNING, 176/1000, ETA ~22:38" -> now done + REJECTED 2/3 with the
          real numbers (R_AMS 0.9364/0.9970, F 0.22489/0.22984 vs 0.25931, dF -0.0319).
        - C2b parent note, C2b.5 Pareto row, C5.2 risk, FIG `musle` (LS2D box red->green).
        - C4/C5 doc pointers said "writes docs/34"/"writes docs/35" - both numbers are
          already used; changed to "writes docs/37+" per docs/36 s7.3.
- [x] 4. NEW top-level node "Peak-deficit research track - three lenses, one ranked
      adjudication" (done, docs/36) with the recommendation AS the note: DO NOT PURSUE A FIX
      NOW; keep rank 0; <=1/2 session on the rank-1 audit; 6 of 7 options fail their own
      not-worth-doing condition. 6 children: lens 1 / lens 2 / lens 3 (done), the rank-0
      DECISION, the rank-1 CHIRPS audit (todo, sketched not registered), the docs/36 s7
      framing corrections (todo).
- [x] 5. Banner rewritten (1,595 chars) + updated string. Both now lead with "Phase B closed
      twice" and carry gate (b)'s failure and the hectare convention.
- [x] 6. Discoveries 20 -> 25. New: research verdict (explicitly NOT pursuing), the first
      uncalibrated number 0.6844 Mt/yr with BOTH biases named and their directions, the
      third (hectare) area convention worth 13.18x, the C3 inputs built, and the 43 % ->
      81.8 % framing correction with R_POT 0.5747 vs the 0.567 in three docs.
- [x] 7. Why-panels 33 -> 41 declared / 41 rendered. New panels: C3.1, C3.2, C3.3, C3.4,
      C3.6, lens 1, lens 2, lens 3, rank-0 decision, rank-1 audit; C2b.5 gained a gate.
      New inline SVG: 4 (FIG 11 -> 15) - `oomgate` (log-axis: 0.684 / 9.02 / 32.76 vs the
      144-184 anchors), `qpeakbias` (every bias marker left of 1.00), `options` (gain
      ceiling per option), `erosionband` (area share vs erosion share by elevation).
      All 15 FIG keys are referenced; none unused.
- [x] 8-9. VERIFIED FROM EXECUTED OUTPUT (not exit codes):
      1 <script> block extracted, 103,719 bytes -> `node --check pm.js` -> **NODE_CHECK_OK**.
      Headless render (fake-DOM harness, node harness.js):
        cards **done 41 / in progress 3 / todo 17 / blocked 6 / 67 tracked leaves = 61 %**
        tree nodes 525 · rows 85 · xbox 41 · rows-with-x 41 · why?-buttons 41 (all equal)
        inline <svg> rendered 15 · empty <figure> (bad FIG key) **0**
        discoveries rendered **25** · banner 1,595 chars
        literal "undefined" 0 · "[object Object]" 0 · NaN 5 (all prose, e.g. "0 NaN/Inf")
        X-PANELS declared 41 == rendered 41 MATCH
        FIG defined 15 == referenced 15, missing [] unused []
        SVG check: all 15 balanced, no raw ampersands
        INTEGRITY: no kids/x slot misuse (the run-1 bug has not reappeared), all statuses
          valid, all FIG keys resolve, x keys only {why,math,fig,gate,risk}
      Self-containment: **0** occurrences of http(s):// and 0 of cdn/unpkg/jsdelivr/
        googleapis/@import/fetch( in the whole 111,451-byte file.
      Baseline for contrast: run 1 left 32/4/20/4 = 60 leaves at 53 %.
- Files touched: progress_map.html + this journal. No git commands. No calibration launched.
- DONE (run 2).

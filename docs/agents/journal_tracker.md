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

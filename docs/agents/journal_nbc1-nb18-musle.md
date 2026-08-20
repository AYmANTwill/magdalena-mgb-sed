# journal — nbc1 — nb18 (18_musle_construction), T1 AUDIT ONLY (read-only)

Agent: nbc1-nb18-musle. Started 2026-08-13.
Assignment: audit `notebooks/18_musle_construction.ipynb` (85 cells) for kill-list numbers,
prose-vs-code contradictions, yield-embargo violations, missing convention/cp_revision,
narrative-role gaps (beats 5/6/7), and executed-output staleness vs the V4_dg engine-default move.
Owning doc: docs/37 + amendments A1 / A1.9 / A2 / A3. Generator: src/nbgen/make_nb18.py.

HARD CONSTRAINTS ACCEPTED: fix nothing; no notebook execution; no git write; only file I write is
this journal.

## Log
- [t0] Created journal.

- [t1] Extract read cells 0-37 (lines 1-1758 of the .txt). Notebook is 85 cells,
  47 markdown / 38 code, code_unexecuted=0, cells_with_error=0.
- Early observations:
  * Cell 22 output: LS2D row source = `urh_ls2d.csv:ls2d_hs`; `adopted column: 'ls2d_hs'`
    (cell 25 output line). convention_summary printed (volume_convention williams_m3,
    k_unit_system us_customary, ls2d_factor 1.0, alpha 11.8, beta 0.56).
  * Cell 26/33/34/35: the "2-10" band appears MANY times but is consistently labelled
    "retired", "UNCITED", "retired as uncited". Looks compliant so far - to be adjudicated
    per hit.
  * Cell 36 + 37: the x0.421 / x0.333 / min(m,0.5) / eq.14 material is all present and is
    handled with explicit strike-throughs, supersession notes and "NOBODY'S published
    formulation ... may never be graded CITED". Looks compliant.
  * CANDIDATE CRITICAL: cell 36 blockquote says "**No engine default has moved** - this
    notebook still runs on `ls2d_column = 'ls2d_hs'`, i.e. `V0`" and cell 37 prints
    "THIS NOTEBOOK STILL RUNS ON ls2d_column='ls2d_hs' (V0), f_LS = 1.000." The orchestrator
    measured commit c3fdb55 (2026-08-12) "switch engine default LS to adopted source field
    V4_dg" AFTER 57f9761 (last touch of nb10-18). Must verify against src/mgb_sediment.py.
- [t2] Full sweep of all 85 cells (0..84) complete from the extract. Verified via engine + git:
  * `src/mgb_sediment.py:916 load_geometry(...)` NOW defaults `urh_ls2d='urh_ls2d_variants.csv'`,
    `ls2d_column='V4_dg'` (line 925). `build_geometry` (:851, kwarg at :862) and the
    `SedGeometry` dataclass field (:818) still default `'ls2d_hs'` — nb18 calls
    `load_geometry`, i.e. the entry point whose default MOVED.
  * `git log -- notebooks/18_musle_construction.ipynb` -> last touch **57f9761**.
    `git log -- src/nbgen/make_nb18.py` -> last touch **c3fdb55** (AFTER).
    `git show c3fdb55 -- src/nbgen/make_nb18.py` shows the generator gained a V0 pin
    (`urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs'`) that the committed notebook DOES NOT
    HAVE (`grep -c "V0 pin" notebooks/18_musle_construction.ipynb` -> 0).
    => the .ipynb is DESYNCED from its generator, and re-executing the committed .ipynb today
    would silently load V4_dg and change every load below section 3.6.
  * `data/processed/urh_ls2d_variants.csv` exists (4.2 MB, 2026-08-12 15:10), so the switch is live.
  * Executed numbers themselves (299.5387 / 248.7298 / ls2d_hs / f_LS 1.000) remain a CORRECT
    V0 record and match the generator's pinned intent — they are not wrong, they are un-regenerated.
- [t3] Candidate defects to adjudicate against docs/37 A1/A1.9/A2/A3:
  (a) cells 36/39/69/78 assert "no engine default has moved" -> FALSE since c3fdb55.
  (b) cells 69/70/71/83 print "the model is 1.03x - 2.27x under-erosive" as a live verdict.
  (c) t/km2/yr appears in cells 48/68/69/71/78 labelled "model-internal specific erosion".
  (d) cells 78/83 say "82 tests pass" / "the 82-test suite".
  (e) cell 41's `n16` / cell 75's `LS x0.333` example.

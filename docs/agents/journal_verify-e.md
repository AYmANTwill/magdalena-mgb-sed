# Journal — adversarial verifier of H-E ("the mundane ones")

**Date:** 2026-08-12. **Branch:** main. **Role:** try to REFUTE the H-E report
(`docs/agents/journal_chirps-mundane.md`), which claims all eight mundane causes of the
+152.15 mm/yr CHIRPS-merge volume-gate miss are ruled out, leaving a residual >= 151.56.

Rules I held myself to: every number that decides a verdict is recomputed by my own code from
the shared ledger (never copied from the report's output files); every doc quotation is opened
and read at the line; no edits to any `docs/NN` file; no commits.

Scratch: `<scratchpad>/verify_e/` (`v1_ledger.py`, `v2_gauge_and_geo.py`, `v3_pixel_vs_basin.py`,
`v4_bulk_vs_tail.py`) with saved executed output next to each.

## 0. Reading the code first (before any measurement)

* `src/merge_chirps_gauges.py` L94-95: `VOLUME_TARGET = 2036.4`, `VOLUME_TOL = 0.01`;
  L484 the gate is `abs(vol / VOLUME_TARGET - 1.0) <= VOLUME_TOL`. **The gate is a ratio
  against a FROZEN CONSTANT**, not against a recomputed field. This matters for item 1 — see
  §2 below, where the report's "exactly zero on the gate decision" turns out to be a
  statement about a ratio the code does not actually compute.
* L467: `assert abs(med_base - BASELINE_MEDIAN_R) < 6e-4` exists; no assertion anywhere on
  `VOLUME_TARGET`. The report's item-8b asymmetry claim is **code-confirmed**.
* L251-259 `apply_qmap`: `y = interp(x, ck, gk)`, then `y = x*gk[-1]/ck[-1]` where `x > ck[-1]`
  and `ck[-1] > 0`. The report's item-8c description of the branch is exact, and
  `np.interp`'s own clamp at `gk[-1]` makes the report's "clipped" counterfactual the right one.
* `src/idw_forcing.py` L79-82 `km()` uses **111.0 km/deg** — item 8d's premise is real.
* `src/idw_forcing.py` L133-134: `gap = np.isnan(P)` over a (days x cells) array, so
  `n_gap = gap.sum()` counts **cell-days**, not cells. The docstring calls it
  `n_fallback_cells` and `idw_field`'s callers print "cells" — a pre-existing naming defect.
  The report reads it correctly as cell-days (41,180 full window / 35,716 gate window).

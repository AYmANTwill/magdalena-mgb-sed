# journal — nbc1 — nb19 (19_c3_gate_and_c4_setup), T1 AUDIT ONLY (read-only)

Agent: nbc1-nb19-c3gate. Started 2026-08-13.
Assignment: audit `notebooks/19_c3_gate_and_c4_setup.ipynb` (82 cells), generator
`src/nbgen/make_nb19.py`. Phase 1 = audit only, FIX NOTHING, execute nothing, no git writes.

Deliverable: structured object (owning_docs, current_claims, narrative_role_should_be,
narrative_beats, inherits_from_previous, hands_to_next, executed_output_staleness,
engine_entry_points_called, findings[], cells_swept, not_settled).

## Log
- [t0] Journal created. Next: locate the pre-extracted nbtext file for nb19.

- [t1] Read the full extract `.../nbtext/19_c3_gate_and_c4_setup.txt` (3,708 lines, 82 cells,
  53 markdown / 29 code, code_unexecuted=0, cells_with_error=0, exec counts 1..29 contiguous).
  Cells swept: 82 of 82 (all read verbatim).
  First-pass observations to verify by measurement:
  * cell 6 pins `ls2d_column='ls2d_hs'` with comment "V0 pin: ACT 2 (2026-08-12) moved the engine
    default to V4_dg; nb19 is a V0 record." -> the generator WAS updated after ACT 2.
  * cell 69 printed output says "No engine default moved - this notebook still runs at V0" -> that
    sentence is now FALSE about the engine (c3fdb55 moved it). Must check generator + engine line.
  * cell 58 ("what it shows"/"what it means") restates k_min 0.00216 / 0.0209 as LIVE and quotes the
    registered sentence form with "STRONGER" - both superseded by docs/45 s8.1.4 per cell 55.
  * cell 32 prose says "runoff ratio of 2.54-3.92 / 5.25-7.34" but cell 31 PRINTS 2.21-5.45 /
    4.17-11.91 -> prose-vs-code mismatch (prose is the beta=0.56 form, code the whole-band form).
  * t/km2/yr appears: cell 7 print (1,165.08 model-internal), cell 14 table (1,445.32 model-internal
    + 1,485 / 690 / 2,200 external), cell 63 (1,485 external). Must read docs/23 s13.2 for scope.
  * cell 81: 33 integrity assertions, all PASS, incl. "no gauge-referenced t/km2/yr yield is
    reported anywhere in this notebook".
  Next: mechanical greps, then engine source, then owning docs (23 s13.2, 37 A3, 45, 47, 52, 55).

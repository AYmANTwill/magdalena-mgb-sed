# Journal — C3.1 enactment (docs/37 AMENDMENT A3)

Session: c31-enactment, 2026-08-11.
Task: write the C3.1 ENACTMENT amendment as docs/37 A3. This is docs/47 B1.

## Log

- [start] Oriented: docs/ listing confirms 46 is now `46_ls_preregistration.md` (DRAFT suffix
  gone — the amend-46 agent renamed it). docs/52 and docs/53 exist. docs/37 is 1238 lines.
- Next: read CLAUDE.md ordering docs, 00_INDEX, 51 §5.3/§5.6, 46 §4.2/§7, 47 §6.2, 37 §1/§4.

- [read] docs/51 in full. Key: §2.1 bracket table (α ref 2.967–5.097; docs/35 band
  1.484–2.548 … 5.935–10.194; hard stop 8.902–15.291), §2.3 POINT-plus-hybrid, §5.3 recommends
  docs/37 A3, §6.2 the point does NOT dissolve the block (α̂-equiv 1.026 / 2.485 / 5.126 at
  1/f=3.9768 vs box floor 2.0, rail band <3.40, stop 3.9 => 2 of 3 corners FAIL).
- [read] docs/46 §4.2 decision rule + outcome table; §4.3 forbidden evidence; §4.4 ordering
  guarantee (⚠ box: totals already published; the justification must be a SOURCE READING).
  §7.1/§7.3 negative-result branch. §5 immovables.
- [read] docs/47 §6.1 B1–B5 and §6.2's six contract items, §6.3 permitted-now list.
- [read] docs/37 §1 table row 2 (":11") and §4 candidate 0 (":197-198", ":212-216", ":265",
  and also :104-106, :344, :600, :612, :615, :914) all still print 2.37×–3.00× / ×0.333–×0.421.
- Next: docs/46 §2.0, §3.3, §6.1-6.3, §9, §10; docs/52 §4/§6; docs/53. Then draft A3.

- [measured] B-repair status, checked in the repo rather than assumed:
  * B3 **DISCHARGED** — `src/mgb_transport.py:908` is `if not (m <= max_resid)` with the NaN
    comment at :902-907; regression test `tests/test_transport.py:246`
    (`assert math.isnan(res.ledger["max_node_residual_t"])`).
  * B4 **DISCHARGED** — `docs/42` §9.2-§9.5 (A-P1, A-P2, A-P3, A-P1.1) are written.
  * B2 **NOT DISCHARGED** — `docs/45` §8 amendment slot is literally empty ("Empty at
    registration"); `docs/35` §9 has no α-box re-registration (§9.1/§9.2/§9.3 only).
  * §5.5 pre-fit-profile disclosure **NOT DISCHARGED** (same empty §8).
  * B5 **NOT DISCHARGED** (same empty §8); owed before any C4 number is PRINTED, parallel.
- [measured] `data/processed/urh_ls2d_variants.csv` header has **no V4_dg column** — the
  adopted field does not exist as a committed product. Same for minibacia variants.
- [measured] the f_area(V4) 0.42136300 vs 0.42147514 flag from docs/53 RESOLVES as two
  different area supports, not an error: `ls2d_variants_summary.json:ratio_to_V0` is over the
  30,235,916 basin DEM cells (0.42136300143291305); `ls_defect_a.json:f_area_urhfrac_areas` is
  over the 32,782 engine URH cells (0.4214751420286394). Relative gap 2.661377e-04.
  docs/46 §3.3's literal definition of f_area is the basin-cell one.
- [arithmetic, reproduced] 299.5387088405831 x 0.2514648985839397 = 75.3235 Mt/yr (registered).
  11.8f=2.9673 · 5.9f=1.4836 · 23.6f=5.9346 · 35.4f=8.9019 · 3.9f=0.9807 · 1/f=3.976698.
  docs/47 §5.2 optima x 1/f: 1.0260 / 2.4855 / 5.1261; implied level 4.8159.
- [decision, before writing] outcome = the source formulation read whole (V4_dg) under §4.2
  item 1; ADOPT-SOURCE DETERMINED but NOT EXERCISABLE (§3.3 stratified report undischarged:
  slope terciles absent, per-station LS-bar absolutes absent). So A3 records the decision and
  does NOT propose the default switch. C4.3 does NOT unblock: B1 discharged, B2 + §5.5 not.

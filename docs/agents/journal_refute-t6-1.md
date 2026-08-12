# Journal - refute-t6-1 (REFUTER, read-only)

Task: try to kill a T6 HIGH finding (lens-freeze-honesty) claiming docs/37 asserts
ADOPT-SOURCE is "exercised" at four live sites while docs/46 §4.2 note 3 reserves
"exercised" for the step gated on §3.3's full stratified report, and while docs/37's
own A3.1 status row says "DETERMINED and RECORDED - not yet EXERCISABLE".

Posture: default that the finding is WRONG. Verify quoted strings verbatim, context,
and whether the sites are supersession/historical blocks.

## Log
- 2026-08-12: journal created as first action.

## What I did, in order

### 1. Full "exercis" census of docs/37 (my own scan, not the lens's)
`python3.10` read of docs/37_c3_closure.md (2383 lines) -> 21 lines contain the stem:
[11, 241, 423, 1359, 1381, 1394, 1397, 1423, 1633, 1637, 1640, 1674, 1681, 1683, 1686,
 2006, 2087, 2183, 2267, 2289, 2316].
The lens listed 16 as "NOT exercised" + 3 in docs/37 as the opposite = 19; unaccounted by the
lens: :1381 (heading "the docs/46 §4.2 row it exercises") and :2087 ("Once the enactment is
*exercised* there ..."). Accounting imprecision only; does not touch the substance.

### 2. Are the three docs/37 strings verbatim? YES.
- :241 (inside the LIVE block "> **[WARN] AMENDMENT A3.3.1 + A3.3.2, 2026-08-12 ...**", lines
  220-245): "> 4. **`docs/46` §4.2's outcome is now exercised as ADOPT-SOURCE at `ls_formulation =
  buarque_2015_dg`** -- see **A3.1**. The RESOLVER named below has therefore been executed on
  source grounds; what remains owed before the engine default may move is **A3.1.6**'s three
  deliverables." Verbatim, except the lens bolded "before the engine default may move" which the
  doc does not. Markup-only deviation, not a substantive misquote.
- :1394 "> | `docs/46` §4.2 outcome row exercised | **ADOPT-SOURCE** |" -- verbatim, inside the
  LIVE A3.1 DECISION blockquote table.
- :1423 verbatim: verdict cell reads "**EXERCISED**, by **item 1 and by elimination**, and **not
  by preference**. ... which makes the outcome **determined but not yet exercisable** (A3.1.6)."
  Both assertions in ONE cell, as the lens said.

### 3. Is the frozen gate real and quoted right? YES.
docs/46_ls_preregistration.md:886-890 verbatim: "- **Reachable != exercised.** No outcome in this
table has been taken. §3.3's **full stratified report** is not discharged -- elevation strata
exist for every variant, **slope terciles do not**, and the per-station erosion-weighted `LS-bar`
exists only as ratios (`docs/47` §4.4) -- and it is required before ADOPT-SOURCE is *exercised*,
though not before this freeze (`docs/51` §7 item 9)."
docs/46:1313 and :1390 and :1398 corroborate ("exercises **no §4.2 outcome**"; "(R7)/(R8) and
§3.3's slope-tercile stratified report are owed before ADOPT-SOURCE is exercised").

### 4. Context test (the usual false-positive escape) -- FAILS to save the finding.
None of the three sites is a strike-through, a supersession register, or a labelled historical
record. :241 is the CURRENT text of a 2026-08-12 amendment block whose whole job is to state the
live position. :1394/:1423 are live A3.1 tables. So the "docs/39-style register of superseded
values" defence does not apply.

### 5. The internal contradiction is real and is not confined to :1397.
- :11 (§1 closure table, clause 2): "The clause stays NOT MET -- A3 records the decision, it does
  not exercise it (A3.1.6)."
- :423 (A1.1 clause 2): "ADOPT-SOURCE is recorded and not yet *exercised* (A3.1.6)".
- :1397: "| status | **DETERMINED and RECORDED -- not yet EXERCISABLE.**"
- :1673-1674: "the §4.2 outcome is DETERMINED and RECORDED, and it is NOT YET EXERCISABLE."
- docs/47:961, :1005 (same run): "determined and recorded but not exercisable", "NOT EXERCISABLE".
So :241 is the outlier against its own document AND against docs/47.

### 6. On-disk verification of the ACT (i.e. is anything actually wrong beyond the label?)
- `head -1 data/processed/urh_ls2d_variants.csv` (read-only) header:
  mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,V2b_m_step_eq14,
  V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd  -- confirmed NO V4_dg column.
- `git diff -U0 -- src/mgb_sediment.py` (read-only git): the ONLY hunks are docstring text
  (@@ -212,4 +212,52 @@ and @@ -227 +275,10 @@). No executable line changed.
- Working-tree defaults, read: :704 DEFAULT_CP_REVISION = "cited_central_2026_08_11";
  :814/:858/:921 ls2d_column: str = "ls2d_hs"; :920 urh_ls2d: str = "urh_ls2d.csv". UNCHANGED.
  NOTE: the lens's src line numbers (688/798/842/904/905) do not match the working tree
  (704/814/858/920/921) -- they look like HEAD numbering. Substance still confirmed.

### 7. Where the lens OVERCLAIMS (two corrections I can prove)
(a) "The `src/mgb_sediment.py` docstring repeats the claim where no A3.1.6 is adjacent" -- FALSE.
    src/mgb_sediment.py:242 says "docs/46 §4.2's outcome exercised is **ADOPT-SOURCE**." and the
    IMMEDIATELY FOLLOWING paragraph, :244-246, says in bold caps: "**NOTHING IN THIS MODULE
    CHANGES BECAUSE OF A3, AND THAT IS DELIBERATE.**  A3's status is **DETERMINED and RECORDED,
    NOT YET EXERCISABLE**: it does not propose the engine-default switch, ``ls2d_column`` stays
    ``"ls2d_hs"`` and ``urh_ls2d`` stays ``"urh_ls2d.csv"`` ...". Two lines away. That site is the
    LEAST harmful of the four, not an unmitigated one. Its phrasing also reads naturally as "the
    outcome [row] exercised is ADOPT-SOURCE", i.e. selection, not action.
(b) ":241 silently relocates the gate to the engine-default step" -- overclaimed. A3.1.6's own
    heading is "the three deliverables between this decision and the engine" and its body says
    "Three named deliverables stand between this decision and any engine-default proposal" -- so
    the engine-default framing is A3.1.6's too. What :241 actually does wrong is (i) assert the
    gated verb affirmatively and (ii) omit "not yet exercisable" while pointing only at the
    switch step.

### 8. Retired-claim / category-error checks
- Not the 0.1644 bar, not (R10), not the SDR 0.05-0.30 band, not the mountainous LS 2-10 band.
  No number is at stake, so no recomputation applies (I recomputed nothing because there is
  nothing arithmetic to recompute; I verified the two on-disk facts instead).
- Not f_ero/f_area confusion, not CITED-vs-validated, not tolerance-vs-materiality-bar. The claim
  is purely a verb/label-vs-frozen-gate claim. :1394/:1423 are genuinely ambiguous between
  "the row the rule returns" and "the outcome has been taken"; :241 is NOT ambiguous -- "the
  outcome is now exercised" is the action reading.

### 9. Consequence claim, checked
§4 candidate 0 is quoted by docs/35 §9.3.1/:342/:1049/:1208, docs/43 §1.4/:38/:607,
docs/46 §2.5.1/:55/:99/:124/:215/:572/:660/:1166/:1179, src/nbgen/make_nb18.py & make_nb19.py
(named in docs/46 §7.3 item 2's five-site list) and ~20 internal docs/37 sites. The "most-quoted
LS site" characterisation holds.

## VERDICT: I could not kill it. refuted = false. Severity HIGH stands.
The one substantive site is docs/37:241; :1394 and :1423 are the same verb in a defensible-but-
colliding sense, and src/mgb_sediment.py:242 is mitigated in place two lines later.

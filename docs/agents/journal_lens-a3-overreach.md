# journal — lens-a3-overreach (T6 adversarial lens)

Role: READ-ONLY adversarial lens. Thesis to try to prove: **docs/37 A3 claims more than it may,
and C4.3 has been declared unblocked on thinner grounds than docs/47 §6.2 requires.**

Write scope: this file only.

## 00 — plan
1. read CLAUDE.md, docs/00_INDEX, docs/47, docs/46 (§1.0,1.2,2.0,3.1,3.3,4.2,4.3,4.4,5,6,7.3,9,10),
   docs/51, docs/52, docs/53
2. read docs/37 A3 on disk in full (lines 1340-2272)
3. git diff (read-only) on scripts/c3/ls2d.py, src/mgb_sediment.py, src/mgb_transport.py
4. hashes/mtimes of the four frozen data products + sim_calibrated_v2
5. walk docs/46 §5 nine rows
6. walk docs/47 §6.2 six items + §6.1 B1-B5 + §5.5
7. Branch A/B precision check (docs/46 §6.2 A1-A6, §6.3 B1-B5)
8. docs/46 §8.2 seven prohibitions
9. yield embargo grep
10. owner/trigger naming check

(entries appended below as I go)

## 01 — engine defaults and frozen artifacts: CLEAN (measured)

`git status --porcelain scripts/` -> EMPTY. `git status --porcelain src/mgb_transport.py` -> EMPTY.
So `scripts/c3/ls2d.py` and `src/mgb_transport.py` are byte-identical to HEAD.

`src/mgb_sediment.py` IS modified. I compared it to HEAD at the AST level with docstrings stripped:

```
python3.10: head=git show HEAD:src/mgb_sediment.py (bytes->utf8), cur=open(...,'rb').decode('utf-8')
strip module/class/function docstrings from the AST, compare ast.dump
-> AST identical after docstring strip: True
-> head CRLF 0  cur CRLF 0
```
Regex spot-checks (all SAME vs HEAD):
 ls2d_column: str = "ls2d_hs"  (x3)  · urh_ls2d: str = "urh_ls2d.csv"
 cp_revision: str = DEFAULT_CP_REVISION · DEFAULT_CP_REVISION = "cited_central_2026_08_11"
 DEFAULT_VOLUME_CONVENTION = "williams_m3" · DEFAULT_K_UNIT_SYSTEM = "us_customary"
 VOLUME_FACTORS / K_UNIT_FACTORS / CP_REVISIONS dicts unchanged.
=> **NO ENGINE DEFAULT MOVED.** The mgb_sediment.py change is docstring-only, as claimed.

Frozen data products, sha256 (first 16) + mtime (today is 2026-08-12):
```
8579c1281c1a992d  2026-08-11 04:15:05  data/processed/urh_ls2d.csv
4c49b07bb92d54cb  2026-08-11 04:15:05  data/processed/minibacia_ls2d.csv
81d2376ac1197839  2026-08-11 21:50:45  data/processed/urh_ls2d_variants.csv
6bbb15c7db5eeaa7  2026-08-10 13:54:20  sim_calibrated_v2/h2e_drivers.npz
cfe68790db22bdf1  2026-08-10 14:03:22  sim_calibrated_v2/parameters_H2E.csv
d545d98a8b6e0741  2026-08-10 14:03:22  sim_calibrated_v2/q_gauge_H2E.npz
60df921d7fb4c9fa  2026-08-10 14:03:22  sim_calibrated_v2/report_H2E.json
c8052df034a44170  2026-08-10 14:03:22  sim_calibrated_v2/metrics_fleet.csv
```
All mtimes PRE-DATE this run; the three hashes T2a re-checked (8579c128/4c49b07b/81d2376a) and
h2e_drivers 6bbb15c7 match. NOTHING under sim_calibrated_v2 or the LS products was written.

## 02 — B3 verified DISCHARGED on disk
`src/mgb_transport.py`:908 `if not (m <= max_resid):` with the IEEE-754 rationale in the comment
at :902-903. NaN regression test: `tests/test_transport.py`:246 docstring + :274
`assert math.isnan(res.ledger["max_node_residual_t"])`.
NOTE: docs/47 B3 names `src/mgb_transport.py:902` and `tests/test_transport.py:583`; the actual
fix is at :908 and the regression test at :232/:246-274. A3 reports :908 / :274 — A3 is right,
docs/47's line numbers are stale. Not a finding against A3.

## 03 — files modified in the tree that no agent in the run summary claims
`src/nbgen/make_nb10.py` and `src/nbgen/make_nb11.py` are modified (CHIRPS/status annotations,
dated 2026-08-12) and appear in NO agent's ownership block in the run summary. Read the diff:
they are pure markdown-annotation additions about CHIRPS/v2/v3 forcing, unrelated to LS/A3.
Not A3's doing; recorded, not charged to A3.

`docs/00_INDEX.md` and `docs/30_phase_c_plan.md` are also modified and belong to no listed owner.
Will check whether either asserts anything about A3/C4.3 that A3's own text contradicts.

## 04 — A3 read in full (docs/37:1342-2382), arithmetic re-measured

Every number in A3.1's decision box, A3.2's rescaling table, A3.3.4 and A3.8 reproduces exactly:

    python3.10 -c "import math; f=0.25146; fe=0.2514648985839397; fa=0.2446790094097074; fh=0.43194; ..."
    3.9  f 0.9806940000000001  exact 0.9807131044773649  area 0.9542481366978589
    11.8 f 2.9672280000000004  exact 2.9672858032904887  area 2.887212311034548
    35.4 f 8.901684            exact 8.901857409871466   area 8.661636933103642
    2.0  f 0.50292   30.0 f 7.543800000000001   3.40 f 0.8549640000000001
    1/f 3.976775630318937  1/fe 3.9766981619750683  1/fa 4.08698728351287  ln f -1.3804713478171018
    hybrid 11.8fh 5.096892  35.4fh 15.290676  1/fh 2.315136361531694
    bias f/fa 1.0277138223121463   ln(fh/f) 0.5410027585442313  ratio 1.7177284657599616
    load 299.5387088405831*fe 75.32347104056149   129.3840/299.5387088405831 0.43194417342854735
    joint/prod 1.347608646050708  step prod 0.3205262902296241  cap prod 0.3177246791318452
    39.812/9.741 4.087054717174828  -ln(0.580685) 0.543546837831505  exp(-0.5410...) 0.5821641894707599
    farea V4 16.775413430326214/39.812260149274394 = 0.42136300143291305  1/ = 2.3732506095678505
    R7: .43194417543884817/.42136300143291305 = 1.025111777659529 ; /.4214751420286394 = 1.0248390293193077
    |d| ratio 2.609706806921963e-04/1.1777659529199624e-05 = 22.158110450144004
    DG control 0.2514648985839397/0.2446790094097074 = 1.0277338427624152
    Delta_shape/eps = 5.852e14 ; /1e-8 = 1.2994569e7

All match A3's printed values, including "22.158110450144004x closer" and "~5.9e14 / ~1.3e7".

PDF provenance re-measured myself:
data/raw/refs/buarque2015.pdf 9,646,521 bytes,
sha256 3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037 -> MATCH docs/38 §9.1.

Header/artifact checks reproduced:
head -1 data/processed/urh_ls2d_variants.csv -> ...,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd
  grep -c V4_dg = 0. A3.1.6 item 3 CORRECT.
head -1 data/processed/urh_ls2d.csv -> mini,urh,n_cells,area_km2,area_frac,ls2d,ls2d_hs,ls2d_mb86,ls2d_dg96
  A3's "only ls2d, ls2d_hs, ls2d_mb86, ls2d_dg96" CORRECT.
grep -rli tercile docs/ scripts/ src/ -> documents only; no artifact in data/processed.
  slope terciles CONFIRMED ABSENT. A3 CORRECT.
docs/45 §7.1 card :635 still fixes f_LS 1.000 -> docs/46 §5's "frozen pre-registrations" row unmoved.
commit 5eaabf5 = "c3: LS2D topographic factor from the COP90 DEM" -> scripts/c3/ls2d.py, 704 insertions.
  (docs/46 §9's card also names data/processed/urh_ls2d.csv in that commit; data/ is gitignored so it
   is not in the commit. A3 QUOTES docs/46 verbatim, so this is docs/46's imprecision, not A3's.)

## 05 — FINDING 1 (HIGH): A3.1.3's fallback branch is an INADMISSIBLE outcome

docs/37:1570-1573 (A3.1.3 blockquote):
> "If docs/35's owner declines it, then docs/35 wins on its literal text, this amendment's
> ADOPT-SOURCE at V4_dg is the bug, and the surviving outcome is NEGATIVE — UNRESOLVED on a
> *documentary* rather than an evidentiary ground, with V0 retained as incumbent and never as
> validated, the bracket carried, and C4.3 still blocked."

Three measurements against it:
(a) docs/46:872 — NEGATIVE — UNRESOLVED's condition is ">= 1 lever with no citable ground either
    way, or (R6) fires, or the source text cannot be obtained/verified". A3.1.1 (docs/37:1421)
    itself records "ALL THREE DISJUNCTS FALSE". So the row A3's own fallback names is closed by
    A3's own measurement. "on a documentary rather than an evidentiary ground" is a NEW entry
    condition for a frozen outcome row.
(b) docs/46:1132-1136 (§7.1) lists the negative-result triggers: source text ambiguous / Sf units
    unverifiable / two admissible readings survive / primary documents unobtainable. A supremacy
    dispute between two of the project's own documents is none of them.
(c) docs/35 §9.4.3, on disk at docs/35:1079-1081, states the consequence of ITS OWN literal
    reading differently: "If §9.3.2 item 1's three-lever list is held to be supreme, the hybrid is
    the registered default and the POINT is a deviation requiring item 2's written source
    justification." i.e. the fallback under docs/35's literal text is V4 at x0.43194, not V0 at
    x1.000 and not "unresolved". A3's branch and docs/35's branch disagree by the whole L-form
    lever (x1.7177284657599616).
Also: naming "V0 retained" as the surviving OUTCOME conflates the §4.2 outcome with the interim
engine state — the exact conflation A3.1.1's own RETAIN-OURS row rejects (docs/37:1422: "'Ours keeps
running for now' is a fact about the engine default (A3.5.1), not a §4.2 outcome").

And the branch is LIVE, because a mutual deferral exists on disk:
 - docs/37:1568-1570: the ruling "is therefore OWED — dated, by docs/35's own owner, and
   neither by docs/46 nor by this amendment".
 - docs/35:1074-1081: "This amendment does not resolve that, because the resolution is an
   adoption and adoption belongs to docs/37 §A3 ... Both branches are live as of this date;
   neither is exercised here."
Neither owner accepts it; ADOPT-SOURCE at V4_dg therefore stands on an unresolved supremacy
question whose written escape hatch is not an available outcome.

## 06 — FINDING 2 (MEDIUM): the ADOPT-BAND risk is disposed of by citing the WRONG frozen clause

docs/37:1509-1511 (A3.1.2 risk blockquote, on the formPRESED.exe run-time S choice):
> "docs/46 §1.2's read-out that (R1) does not fire is frozen and in force"

Measured: docs/46:262 — "| (R1) second admissible reading of pp. 94 / 121 | — | does not
fire. Two independent sentences (p. 94 + p. 98); single admissible reading => limiter CITED |".
(R1) is registered under §2.1 H-LIM, the slope-length limiter (docs/46:400, under "### 2.1 H-LIM").
The objection is an S-lever objection. H-S's clauses are (R7)/(R8) (field) and (R9) (a reading
test on OUR side) — docs/46:529-550 — and neither is (R1).
Mitigation, in the same blockquote (docs/37:1514-1515): "H-S's own refutation clauses are (R7)/(R8)
(field) and (R9) ... none of which admits the code as a reading of Buarque." The correct grounds ARE
present; the frozen-authority citation is attached to the wrong lever's clause.

## 07 — FINDING 3 (MEDIUM): "EXERCISED" against docs/46's own term of art

docs/37:1394 (the DECISION box): "| docs/46 §4.2 outcome row exercised | ADOPT-SOURCE |"
docs/37:1423 (A3.1.1 verdict cell): "EXERCISED, by item 1 and by elimination"
against docs/46:886 (§4.2 note 3, frozen): "Reachable != exercised. No outcome in this table
has been taken." and A3's own status row docs/37:1397 "DETERMINED and RECORDED — not yet
EXERCISABLE" and A3.1.6's heading docs/37:1673-1674.
A3.1.1's condition cell concedes the ADOPT-SOURCE conjunction is only "HALF met", so the row's
conjunction is unsatisfied and cannot have been exercised. Both sites carry an adjacent qualifier,
so this is a term-of-art collision, not a substantive claim — but :1394 is the one row a
downstream session would quote.

## 08 — FINDING 4 (MEDIUM): "B2, B5 and the §5.5 disclosure have NOT landed" is false on disk

docs/37:2019 heading: "### (2) B2, B5 and the §5.5 disclosure have NOT landed"
docs/37:2123-2124 blocker list: "... B2 · B5 · the §5.5 disclosure ..."
Measured on disk 2026-08-12 (same run, same working tree):

    grep -n '^## 8\.' docs/45_c4_preregistration.md
     700: ## 8.1 — Amendment 1 — 2026-08-12 — the +-38 % Pi band is REPLACED ... (= B5)
     951: ## 8.2 — Amendment 2 — 2026-08-12 — PRE-FIT DISCLOSURE ...            (= §5.5)
    1109: ## 8.3 — Amendment 3 — 2026-08-12 — §2.1's LS bracket 2.37x-3.00x SUPERSEDED
    1213: ## 8.5 — Amendment 4 — 2026-08-12 — the C4.3 gate is RE-EXPRESSED IN Pi ... (= B2)

docs/45:1297-1330 (§8.5.4) registers the gate in Pi as a formula with k0, with docs/35 §6.1's
3.9/35.4 "CARRIED UNCHANGED — not restated here. §8.5.7 records both Pi readings and PROPOSES the
amendment" — which is all docs/47 B2 permits ("may only be proposed"). So B2 does the job.
A3 DOES hedge, at docs/37:2036-2039 ("stated here as a CONDITION and is NOT claimed as a fact.
A later reader must check docs/45 §8 and docs/35 §9 themselves"). The heading and the blocker
list do not carry the hedge. Direction is conservative (over-blocking).

## 09 — FINDING 5 (MEDIUM): stale line citations in the load-bearing ACT-2 table

docs/37:2146 (ACT 2 row): urh_ls2d = "urh_ls2d.csv" (:863) and ls2d_column = "ls2d_hs"
(:757, :801, :864); repeated at docs/37:2227-2228.
Measured now:

    757: k = _finite_nonneg("k_usle", k_usle)
    801: (blank)
    863: if not (cm.shape == cu.shape == ca.shape == ls.shape) or cm.ndim != 1:
    864:     raise ValueError("cell_* arrays must be 1-D and the same length")
    798: ls2d_column: str = "ls2d_hs"
    842: ls2d_column: str = "ls2d_hs",
    904: urh_ls2d: str = "urh_ls2d.csv",
    905: ls2d_column: str = "ls2d_hs",

The cited numbers were right BEFORE the parallel nbgen agent inserted 41 docstring lines
(798-41=757, 842-41=801, 905-41=864, 904-41=863 — exact). Same class of drift:
docs/42's card cell cited at :604 is now at :648 (grep -n 'THREE, all dated' -> 648);
docs/45 §8 cited as ":610-612 Empty at registration" now carries four amendments.
(docs/46 §3.1:697 has the identical defect, "verified at src/mgb_sediment.py:863-864" — frozen, not A3's.)

## 10 — FINDING 6 (LOW): A3.6's "Nothing else" contradicted inside A3

docs/37:2260-2261: "Files written by this amendment: docs/37_c3_closure.md ... and
docs/agents/journal_a3-enactment.md. Nothing else."
docs/37:1982-1983 (A3.3.4, a subsection OF A3, written later by a different session):
"(this session owns only docs/37, docs/43 and its own journal)" — journal
docs/agents/journal_defect-45-residual.md (exists, untracked, "agent A6, 2026-08-12"), and
docs/43_c3_c4_gate.md grew 774 -> 874 lines with a defect-45-residual slot addendum at :418
and an authorship block at :742-743. So the A3 section on disk was written by two sessions and
A3.6's "Nothing else" no longer describes it.

## 11 — FINDING 7 (LOW): Delta_shape quoted for V4 while the claim is about the ADOPTED field

docs/37:2071-2074: "3. The residual vector itself changes, so the search must run on the ADOPTED
LS FIELD. Measured (docs/53 §2 ...): no CAL station is invariant; the argmax is 24037390
CAPITANEJO at |ln| = 0.1299456917 ..."
docs/53:132-145 labels that table "f_s = E_up(V4)/E_up(V0)" — variant V4, the hybrid.
docs/53:206 and :261 measure the ADOPTED variant: "V4_dg buarque_2015_dg ... 0.1361987744".
The registered discriminator IS the V4 reading (docs/46:972 "under V0 and under V4"), so
A3 quotes the right registered number; but it is presented as the measurement of the adopted
field's shape movement, which is 0.1361987744. Direction conservative; branch unchanged; the
under-specification is already flagged at docs/53:401.

## 12 — WHAT I TRIED TO PROVE AND COULD NOT

- A moved engine default: NOT FOUND. See §01. AST-identical after docstring strip.
- C4.3 declared unblocked: NOT FOUND. A3.4's heading is "Is C4.3 thereby UNBLOCKED? NO",
  and the four grounds are (1) B1 alone insufficient, (2) B2/B5/§5.5, (3) Branch B mandatory,
  (4) no committed V4_dg column. A3 treats Branch B as blocking: docs/37:2059-2064 states that
  Branch B "CLOSES Branch A", that A1-A6 are "moot rather than satisfiable", and that
  "There is no legal PROVISIONAL C4.3 at all" — which is the STRICTER reading of docs/46
  §6.2's "Available only if Delta_shape = 0" and A6's "no rescaling in place of a re-run".
- A docs/46 §5 row moved: NOT FOUND. Nine rows walked: cp_revision, the two unit conventions,
  H2E, the frozen driver bundle, ls2d_aggregation/resolution, the committed LS products +
  ls2d.py's defaults, the frozen pre-registrations (incl. docs/45's f_LS = 1.000 card at :635),
  P/FG, the yield embargo — all verified unmoved by hash, mtime, AST or grep.
- A docs/46 §8.2 prohibition breached: NOT FOUND. A3.5.2's eight items map onto §8.2's seven
  1:1 (level UNVALIDATED; alpha only as pairing; direction WITHDRAWN per A1.9; nothing about
  C/K/volume/P/FG; shape not right on a non-detection; C3 does not close; nothing about the
  66.53 %). The 66.53 % appears only as the G9 disclosure docs/42 requires (docs/37:1363-1366).
- Yield embargo breach in A3: NOT FOUND. t/km2/yr occurs in A3 only at :1978 and :2257,
  both embargo statements. All five substantive occurrences in docs/37 (:135, :374, :562, :813,
  :1071) predate line 1342 and are labelled MODEL-INTERNAL.
- alpha-hat quoted / KGE_ln evaluated / new band / materiality bar: NOT FOUND. 10 occurrences
  of the symbol alpha-hat in A3, all inside rules or negations; 2 KGE mentions, both negations;
  0.1644 appears once, as the reference to docs/52's striking.
- Owner and trigger mis-named: NOT FOUND. docs/37:2133-2146 quotes docs/46 §4.2's licence
  column and §9's card verbatim; commit 5eaabf5 exists and delivered scripts/c3/ls2d.py.

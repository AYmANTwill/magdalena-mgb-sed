# Journal — verify-prereg agent

Lens: is `docs/45_c4_preregistration.md` a real pre-registration, or does it leave escape hatches?

Started 2026-08-11.

## Plan
1. Orient: CLAUDE.md (done), docs/00_INDEX.md, docs/45, docs/33, docs/35.
2. Gate-by-gate FAIL-condition audit of docs/45.
3. Check cells / objective / station split / period fixity.
4. Hunt for gates conditioned on not-yet-known quantities.
5. Timestamp check: git log + file birth times vs C4 search machinery.
6. Negative-result publication pre-commitment.

## Log
- (start) listing docs/, reading CLAUDE.md.

### Timestamp evidence (collected 2026-08-11)
| file | birth | mtime | commit |
|---|---|---|---|
| docs/45_c4_preregistration.md | 2026-08-11 12:30:30 | 12:30:30 | 865f674 @ 20:13:22 |
| docs/agents/journal_c42-prereg.md | 12:30:45 | 12:30:45 | 865f674 |
| docs/43_c3_c4_gate.md | 12:10:04 | 12:10:04 | 3bd5d7c @ 20:13:22 |
| docs/42_c4_guards.md | 08:34:19 | 08:34:19 | 4366c1f @ 11:34:36 |
| tests/test_transport.py | 12:36:05 | 12:36:05 | 1e0843c @ 20:13:22 |
| docs/agents/journal_c41-transport.md | 12:39:19 | 12:39:19 | 1e0843c |
| notebooks/19_c3_gate_and_c4_setup.ipynb | 13:07:03 | 20:21:35 | 831bd0a |
| src/mgb_transport.py | 20:20:12 (RESET by later edit) | 20:20:12 | 1e0843c, re-touched 02e7e95 |

NOTE: birth times reset when a file is fully rewritten (Write/Edit temp+rename), so
mgb_transport.py's 20:20 birth is its LAST rewrite (commit 02e7e95), not its first write.
The reliable anchors are files never re-edited: docs/45 @ 12:30:30, tests/test_transport.py
@ 12:36:05, journal_c41-transport @ 12:39:19, nb19 @ 13:07:03.
=> docs/45 (12:30:30) precedes every C4.1/C4-setup artifact whose birth survives. GOOD.
=> BUT docs/43 (12:10:04) precedes docs/45 and already contains alpha ranges (6.83-8.73,
   7.92-8.86). Need to check whether those were FITTED (header claims none were).
=> No C4 search script exists at all: no src/c4_*.py, no c4_grid.csv, no c4_parameters.csv.

## Findings under construction
1. alpha HARD STOP at 35.4 is UNREACHABLE (search box tops at 30.0) - a gate that cannot fire.
2. "total registered budget 5,482. No second search authorised" contradicted in the same table
   by 4x1,000 DDS evals + a conditional 441-eval re-refinement (true max 9,923).
3. ACTION-column vs section6 conflict: G1.1/G2.1/G7/G8 actions say "report/attribute" but
   section 6.1 makes each of them block adoption.
4. `r` overloaded: section 3.1 fixes r = Pearson correlation "in every C4 output", then
   G1.2/G8/G11 use r_i for a log residual with ln-unit thresholds.
5. Sign convention of the G1.2/G3.1/G4.1 residual never stated, yet G1.2's FAIL is ONE-SIDED
   ("interval entirely above 0").
6. Low-power guards count as PASSES in the section 6.1 ADOPT conjunction while section 4.2
   says non-detection "is NOT A PASS" (G1.2) / "weak by construction" (G11) / minimum
   detectable class-C error x4.2 (G3.3 on G3.1).

### MEASURED (2026-08-11), not asserted

**M1. path_km_to_outlet for all 28 mapped SSC stations** (topology.npz v2 + _c1_geom.csv):
the outlet-most of the 18 usable is `23087210` CANTERAS at **684.4 km**, NOT `21237020`
ARRANCAPLUMAS at **801.1 km** (ARRANCAPLUMAS is outlet-most *on the Magdalena trunk* only;
BOLOMBOLO 748.1 and APAVI 519.7 are trunk-Cauca and further down still).
=> docs/45 sec1.6, sec4.1, G9 and sec5.4-3 all state "801.1 km ... below the outlet-most SSC
   station". Measured value is 684.4 km. Over-statement of 116.7 km (17 %). Inherited from
   docs/42 line 181 which named ARRANCAPLUMAS "the outlet-most SSC station" without the
   trunk qualifier.
=> docs/45 sec4.1 additionally says "the closest SSC station is 684.4 km above it [the
   confluence]". Source (journal_adj-c4-feasibility line 91) says 684.4 km above the OUTLET.
   Above the confluence it is 684.4 - 146.1 = 538.3 km. docs/45 inflates the network-to-sink
   separation by 146.1 km (27 %).

**M2. docs/45 sec7.3 "CAL-8 window-mean fluxes span 3.31-22,050 t/day (ln 1.20-10.00)"**
Measured from the cited file, CAL-8 rows:
  a_mean_tday    9.452 .. 19,001.4  (ln 2.25..9.85)   <- estimator (a), the fitted one
  a_median_tday  3.313 ..  5,902.0  (ln 1.20..8.68)
  b_mean_tday   12.060 .. 22,050.3  (ln 2.49..10.00)  <- estimator (b)
=> 3.31 is min(a_median_tday); 22,050 is max(b_mean_tday). The quoted range SPLICES the
   minimum of one statistic with the maximum of a different ESTIMATOR. No single column
   spans 3.31-22,050. The derived "factor of 6,650" in sec3.1 is ~3.3x inflated
   (a_mean gives 2,010x; a_median 1,781x).
=> The substantive claim (denominator safe, all ln > 0) survives on every column.

**M3. c2_station_window_flux.csv contains ONLY the ENSO windows** {P-EN, P-LN, S-EN, S-LN}.
There is no CAL 2012-2014 window in it. So sec7.3's "CAL-8 window-mean fluxes" are ENSO-window
fluxes at CAL-8 stations, and sec3.1's "window-mean flux across the CAL 8 alone" is a mislabel.
Also: sec7.3 asserts the two reads were "station properties, not results" - flux magnitude is
neither, and it comes from the windows sec3.5 declares STRICTLY OUT OF SAMPLE.

**M4. alpha 6.83-8.73 / 7.92-8.86 in docs/37 and docs/43 are analytic back-solves**
(11.8/1.4897 = 7.921 etc., docs/37 line 984), not fits. Header claim "before any alpha or beta
has been fitted" is LITERALLY TRUE. But the expected location of alpha-hat was known before
the freeze, and it sits interior to every alpha gate.

**M5. Search machinery order: CONFIRMED CLEAN.** No src/c4_*.py, no c4_grid.csv, no
c4_parameters.csv exist anywhere in the repo. docs/45 (12:30:30) precedes tests/test_transport.py
(12:36:05), journal_c41-transport (12:39:19) and nb19 (13:07:03).

### Doc-internal contradictions confirmed by quotation

**D1 (the escape hatch). sec6.1 FAIL-STRUCTURE licenses the remedy sec6.3 forbids.**
- L531 FAIL-STRUCTURE "what it licenses": "reporting the fit as a measured negative,
  **with that guard's registered ACTION taken**".
- L428 G1.1 / L429 G1.2 ACTION: "Add an explicit, named transport sink **and refit**".
- L433 G3.1 ACTION: "Revise that class's C ... **and refit**."
- L436 G4.1 ACTION: "Fix the LS2D field, or adopt a steepness-dependent correction".
- L221 sec2.5: "No second search is authorised by this document."
- L553-555 sec6.3: "No outcome of C4 licenses: a second search, a widened box, an added free
  parameter, an edit to ... this document's sec2-sec6 ... Every one of those requires a new,
  dated pre-registration."
=> The most probable failure mode (structure) carries a registered licence to refit inside C4.

**D2. The deposition axis cannot produce an adoption-blocking failure.**
sec2.3 FIXES k = 0.0 /km, not fitted. docs/42 G5 (the guard written to replace the alpha
band's lost job) offers "named non-trivial sink OR state 'this model asserts SDR = 1.0' in
those words". docs/45 sec2.3 WRITES THAT SENTENCE IN THE PRE-REGISTRATION - leg 1 is
discharged before a fit exists. Leg 2 is a reporting requirement. G1.2's own registered
detection floor is ~2.12x over 348.4 km.
docs/35 sec9.2 (L629-631) registered the opposite: "A fitted alpha at or below the low teens,
obtained without an explicit deposition/routing step, silently encodes SDR = 1.0 and must be
treated as a failure regardless of what the guard reports." docs/45 imports G5 but NOT this
sentence, and it appears in no sec6 outcome. The expected alpha-hat for exactly this
configuration was already published as 6.83-8.73 (docs/37 L907, back-solved 11.8/1.4897) -
i.e. at or below the low teens.

**D3. The alpha HARD STOP cannot fire.** Search box [2.0, 30.0]; HARD STOP alpha > 35.4.
30.0 < 35.4. The like-for-like stop at OUR LS level, from the SAME cited source (docs/35
sec9.3 rule 3, L725): "the ratio is 2.37 - 3.00, giving expected ~ 2.0 - 9.9 and hard stop
~ 11.8 - 14.9" - which IS inside the box. docs/45 sec2.1 prints the 2.37-3.00 bracket as a
"defect to state" but registers the un-rescaled numbers as the operative gate.

**D4. Four registered Reporting FAILs have no row in the outcome table.** sec6.1 ADOPT is an
eight-condition conjunction; G3.2, G3.3, G4.2 and G10 are each declared a "Reporting FAIL" in
sec4.2 and none appears in any of the eight, nor in FAIL-RAILED's "G5/G6/G9 reporting leg
missing". A fit can commit a registered FAIL and still be ADOPTed.

**D5. G7 is defined two incompatible ways.** "what it tests: fit on one ENSO phase, score on
the other" (verbatim from docs/42 L511) vs sec3.5 (both ENSO windows STRICTLY OUT OF SAMPLE),
sec2.5 (one registered search) and sec6.3 (no second search). G7 is an ADOPT-blocking gate
whose computation is undecided.

**D6. G1.1 self-contradicts.** Same cell: "Do not adopt." and "Corroboration only - the
verdict is G1.2's." sec6.1 lists G1.1 as an independent FAIL-STRUCTURE trigger.

**D7. G12 is circular and its cost is mis-stated.** It must "record ... the sec6 verdict" per
LOO refit, but the sec6 verdict's condition (8) IS G12; and conditions (4)-(7) need guards
computed on all 18 stations, not the per-station precomputed surface ("cheap" is false).

**D8. Budget contradicted in its own table.** "total registered budget: 5,482 evaluations. No
second search is authorised" sits two rows above 4 x 1,000 DDS evaluations plus a conditional
441-eval re-refinement => true maximum 9,923.

**D9. The out-of-sample premise can fail for free.** sec3.5 registers the ENSO-neutrality of
CAL 2012-14 as UNCITED; the registered consequence of not substantiating it is a relabel
("out-of-phase" -> "out-of-window"), not an outcome in sec6.1.

**D10. Notation.** sec3.1 fixes r = Pearson correlation "in this document and in every C4
output"; G1.2/G8/G11 then use r_i for a log residual with ln-unit thresholds. The SIGN
CONVENTION of that residual (ln sim - ln obs vs the reverse) is never stated, and G1.2's FAIL
is ONE-SIDED ("interval lies entirely above 0") - the same physical defect passes under the
opposite convention.

**D11. Low power counts as a pass.** sec4.2 G1.2: "If neither G1.1 nor G1.2 fires, that is NOT
A PASS"; G11 "weak by construction"; G3.3 registers G3.1's minimum detectable class-C error as
x4.2 on the CAL 8. sec6.1 condition (4) nevertheless counts each non-firing as a pass.

**D12. Negative-result pre-commitment is a LICENCE, not an OBLIGATION.** sec6.1 licenses
"reporting the fit as a measured negative"; sec6.2 requires three statements "whatever it is";
G3.1 requires c_B "reported whichever way it comes out"; sec5's closing paragraph forces the
BORBUR r>1 finding into the G1 discussion. But nothing matches docs/33 sec3.4/sec3.5's "That
outcome is a RESULT, not a failure, and not an anticlimax" / "That is itself reportable, and it
is a real finding about model structure, not a null."

### Checks that PASSED
- DDS seeds 20260921-24 verified genuinely unused: _calib_cache holds only 2026090x.
  (sec2.5's phrasing is loose - 20260907-08 are ON DISK as dds_H2E-S_*.npz, not merely
  "claimed by docs/33" - but the registered seeds are clean.)
- Grid arithmetic reproduces: 15^(1/70)=1.03945; 0.35/70=0.005; 71^2=5041; +441=5482;
  36x36 => 0.01 and 15^(1/35)=1.0804 (8.0%).
- Uncertainty arithmetic reproduces: 1.96 x 0.1644 = 0.322 ln => 0.724x-1.380x (+/-38%);
  0.1644 x sqrt(8/13) => +28.8%; 1.96 x 0.0199 = 0.039; exp(0.0209x60.4)=3.53;
  exp(0.00216x348.4)=2.12; 1-sqrt(2) = -0.414 and -0.26-(-0.414) = 0.154.
- CAL-8 station list + 3,266 paired days + 126/288 station-months reproduce lens 3's table
  (journal_adj-c4-feasibility L95-107); min paired days 112 (EL PROFUNDO) clears the
  registered >= 91 floor.
- flow_selective == True for 26127010 only among the CAL 8: CONFIRMED from the cited file.
- Windows/period/cells/split: fixed with no re-choice clause. The 13 -> 8 shrink is a data
  ADMISSIBILITY filter measured in docs/43 before the freeze, and sec2.4 explicitly REFUSES to
  re-admit ARRANCAPLUMAS to regain power after the power was measured. Strongest part of the doc.
- Order of writing: docs/45 (12:30:30) precedes every surviving C4 artifact birth time, and no
  C4 search machinery exists at all.

### VERDICT
Real pre-registration, not theatre - it can fail on F_report, on the beta hard stop, on the
reporting legs, and on several structure guards. But the ONE axis the project itself identified
as where alpha hides (deposition) is registered so it cannot block adoption (D2, D3), and the
most probable failure mode carries a licence to refit inside C4 (D1).


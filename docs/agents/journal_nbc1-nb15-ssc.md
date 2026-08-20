# Journal — nbc1-nb15-ssc (Notebook Coherence Pass, PHASE 1 = T1 AUDIT ONLY)

Agent: nbc1-nb15-ssc. Owner of THIS file only.
Date: 2026-08-13.
Scope: audit `notebooks/15_ssc_quality_gate.ipynb` (85 cells), generator `src/nbgen/make_nb15.py`.
Mode: READ-ONLY. Fix nothing. No notebook execution. No commits.

## Assignment as received
- Stage C1, owning doc docs/32. Mechanical sweep hits reported by orchestrator:
  "0.333" x3, "t/km" x8, "km2/yr" x1, "SDR" x6, "CHIRPS" x4.
- t/km2/yr hits are potential YIELD EMBARGO violations -> CRITICAL if live.
- Check station arithmetic end to end vs docs/32 §R6: 79 classified, 28 mapped, 46 no coords,
  6 usable + 12 usable-with-caveat = 18 usable, 10 excluded, ONE Magdalena-trunk station 21237020.
- Check whether nb15 still says the C4 tributary set is 13 stations WITHOUT the docs/45 §3.4
  correction (CAL 8 fitted / EVAL 5 scored-not-fitted / all 18 run structure guards).
- Does it hand off to docs/57 (B5: physical limit — 43 recovered sites, ZERO with discharge)?
- Narrative beats 1 and 9.

## Log

### 2026-08-13 — pass 1: full read of the extract

Read ALL 85 cells (0..84) of
`.../scratchpad/nbtext/15_ssc_quality_gate.txt` (3,902 lines). Notebook is C0+C1 combined:
sections 0-3 = C0 (freeze H2E, reproduction gate F=0.25931, exact 0.000e+00), sections 4-9 = C1
(the SSC quality gate), 10 = choices table, 11 = summary. 27 code cells, all executed (exec 1..27),
0 errors.

Mechanical sweep results (grep over the extract):
- `t/km` x8 (lines 25, 3603, 3611, 3613, 3698, 3836, 3859, 3901) — EVERY ONE is the EMBARGO being
  STATED or ENFORCED (§8.4 title, §8.4 body, §8.8 "Not that any t/km^2/yr figure may be quoted",
  §9 Forbidden list, §10 choices table "Yields | Absolute flux only", §11 "What this stage does not
  license"). Cell 0 banner line 25 says the embargo "is still in force". **NOT a yield-embargo
  violation.** nb15 is the notebook that *declares* the embargo. Verified no number in the notebook
  is divided by an area (cell 8 prints "upstream areas ... (labels only, never a divisor)").
- `0.333` x3 — all are the OUTLET skill-over-climatology of **-0.333** in El Nino (cells 79, 80, 84).
  FALSE POSITIVE against the `x0.333 - x0.421` LS bracket. Unrelated quantity, different sign,
  different units (KGE units).
- `SDR` x6 — all in cell 84 §9, and the text is the CORRECT retirement language: "no citable SDR
  band exists ... retired as not evaluable - which is neither a pass nor a fail. No SDR band is used
  anywhere in this notebook". Matches the kill-list requirement. NOT a defect.
- `CHIRPS` x4 — cells 35/36/37, the quantile-mapped merge, LOOCV r 0.429 -> 0.447, rejected on the
  +7.5 % volume gate. Numbers agree with docs/18 §15.5 / docs/26 §7. But the notebook stops there
  and does NOT carry docs/58's bound (max +0.006 r) nor the "registered repair was a no-op /
  diagnosed cause was wrong" read-out — see findings.

Station arithmetic checked end to end from the executed output of cells 69/75:
  79 = 6 usable + 12 usable-with-caveat + 61 excluded  ✓
  28 mapped; 51 unmapped = 46 no coordinates + 5 outside the 8,672-minibacia network  ✓
  61 excluded = 51 unmapped + 10 mapped-excluded  ✓
  reach: mainstem 3 excl + 1 usable + 4 caveat = 8; tributary 7 + 5 + 8 = 20; 8+20=28  ✓
  18 usable-or-caveated = 13 La Nina + 12 El Nino with 7 in BOTH (6 LN-only + 5 EN-only + 7)  ✓
  ONE Magdalena-trunk SSC station 21237020 ARRANCAPLUMAS, 54,035 km2, ~21 % of basin  ✓
All of it agrees with docs/32 §R6 as stated in the assignment. **The C1 arithmetic is clean.**

### pass 2 — kill list, engine, generator anchors, owning docs

**KILL LIST: nb15 is CLEAN.** Grepped every entry. Zero hits for `2.37`, `3.00x`, `11.8`,
`104.8 / 82.8 / 126.1 / 99.7`, `129.38`, `75.32`, `Buarque`, `min(m`, `k_min`, `348.4`, `2.12x`,
`mountainous`, `0.05-0.30`, `under-erosive`, `1.34762`, `299.5`, `248.7`, `0.465`, `38 %`,
`1.9618`, `0.25146`, `f_LS`, `V4`, `condition number`, `CITED`. The only `Mt/yr` hit is §8.4's
"absolute flux only, in t/day or Mt/yr" (the embargo's *permitted* side). All four `validated`
hits are the word inside a NEGATION ("Not that the water model is validated", "no basin-export
figure is validated", "should not accept any basin-export sediment figure ... as validated") plus
one benign "validated on everything else" about the Klemes split-sample.

**FALSE POSITIVES I am protecting from a Phase-2 sweep** (a naive fix here would inject error):
- cell 42 prints `sigma 0.6931 ln-units` — a **rating-curve residual sd at station 21237020**,
  n=6,400. It is NOT `0.6936 ln`, which is the **SE of the fleet-mean Π level** = `1.9618/√8`
  (docs/42 §962-967, docs/45 §720). Different quantity, different estimand. Do not "correct" it.
- cell 72 prints `median residual sigma 0.8093 ln-units (x2.25)` — again the rating residual, not
  the Π residual sd `1.9618 ln (x4.22)`. Do not "correct" it.
- `-0.333` x3 is the OUTLET skill-over-climatology in El Nino, not the `x0.333-x0.421` LS bracket.
- `SDR` x6 (cell 84) is the CORRECT retirement language, matching the kill list's requirement.

**ENGINE: N/A.** Grepped `mgb_sediment`, `ls2d`, `ls2d_hs`, `V4_dg`, `cp_revision`, `import src` —
**zero hits in all 85 cells.** nb15 has no engine call and no engine-derived number; it reads
frozen CSV/npz artifacts only (cell 2 NEED dict, 15 files). git: nb15 last touched by `57f9761`
(2026-08-12 14:55), which is BEFORE `c3fdb55` (16:11, the engine-default LS move) — but that is
**irrelevant to nb15**, because no printed number depends on `ls2d_column`. Executed outputs are
NOT stale on that axis. Measured, not assumed.

**C4 13-STATION DEFECT: CHECKED, NOT PRESENT.** grep "C4" in nb15 -> ONE hit, the cell-0 banner
line noting C4.3 is blocked. nb15 never states a "C4 tributary set". Its only "13" is the La Nina
coverage count (13 of 18 covered in 2011), which is correct. The superseded 13-station claim lives
in the OWNING doc `docs/32` §R6 ("**Tributary set for C4 (13 stations, usable or
usable-with-caveat)**") and is struck in `docs/00_INDEX` :170 — **the doc, not the notebook, is
where that fix lands.** nb15's residual defect is only the MISSING forward pointer (F08).

**docs/57 HANDOFF: BROKEN, and in the refuted direction.** nb15 §8.5 and §8.7 item 5 both present
coordinate recovery as the largest available expansion of the usable set. docs/57 §2 measured it:
46/46 geocoded, 43 in-basin, **0 of 43 have same-code discharge**, 0 of 43 appear anywhere in the
raw IDEAM discharge download; *"The flux-calibration gauge set cannot be grown past ~18. That is a
physical limit of the monitoring network, not a processing gap."* Two HIGH findings.

**Measurements I ran myself** (read-only, on committed artifacts):
- `21197010` spike ratio: max 15,179.805 mg/L / p99 165.83 = **91.538** (n=5,918). nb15 says "91",
  docs/32 §R6.3 says "92x". Both round 91.54; LOW inconsistency.
- `24037390` spike ratio: 15,901.169 / 2,680.0 = **5.933** — docs/32 §R6.3's "6x" checks out.
- `int(np.int64(2) and 0) == 0`, `int(np.int64(3) and 0) == 0` — confirms cell 60's
  `int((_fl.ssc_class == "excluded").sum() and 0)` is **hardcoded 0**, not measured (F04).
- docs/23 §282: "beyond 2x | **31 of 85 (36 %)**" — nb15 §8.4's figure reproduces exactly.

**Generator anchors for Phase 2** (`src/nbgen/make_nb15.py`, 3,245 lines):
:44 / :54 banner · :1261 CHIRPS rejection · :1340-1342 "only remaining lever" · :2225-2226 the
`and 0` hardcode · :2714 "six of the thirty eras" · :2804-2806 trunk export · :2981-2983 §8.5
expansion claim · :2995 §8.6 row 1 · :3014-3015 §8.7 item 5 · :3019 "91 times" · :3145 §9 list.

Cells swept: **85 of 85** (0..84), every one read in full from the extract.
### pass 3 — final finding list (12 rows), and what I refuse to conclude

HIGH x4: F01 §8.5 expansion claim (cell 80) · F02 §8.7 item 5 (cell 81) — both refuted by docs/57
§2 · F03 "six of the thirty eras" vs its own printed 9 of 30 (cell 73, prose-vs-code) ·
F04 the hardcoded `and 0` in cell 60 presented as a verification.
MEDIUM x5: F05 "only remaining lever" vs docs/58's +0.006 bound (cell 37) · F06 CHIRPS read-out
stops at +7.5 % (cell 35) · F07 banner "nothing here has been overturned" + docs/51-59 omitted
(cell 0) · F08 §9 handoff does not carry docs/45 §3.4's CAL 8 / EVAL 5 / all-18 split (cell 84) ·
F09 beat 9's quantitative form (66.53 %, 199.29 of 299.54 Mt/yr, docs/37 §639 / docs/42 G9) not
carried by §8.1 (cell 79).
LOW x3: F10 "91 times" vs measured 91.538 / docs/32's 92x (cell 81) · F11 §8.6 row 1's
+0.026/+0.006 uncited and unrecomputed (cell 81) · F12 flatline nulls 0.030 %/0.234 % quoted with
no source; they are docs/19 §3.4's corrected local-quantisation nulls (cell 82).

**REFUSED TO CONCLUDE.** (a) I did not run the R_AMS gates or any notebook — the 0.820 vs
0.7337/0.5508 gap stays open and nb15's refusal to reverse-engineer it is the right behaviour, not
a defect. (b) I did not judge whether docs/32 §R6's own "Tributary set for C4 (13 stations)" should
be struck — that is a doc fix outside this file's ownership and I did not verify docs/45 §3.4's
CAL-8 membership against it. (c) I did not verify whether §8.7 item 6 (21237020's post-2014
discharge) is still genuinely open — docs/57 does not cover it and I did not search the raw IDEAM
download. (d) docs/26 is internally inconsistent on the El Nino SoC sequence (§118/§156 vs §300);
nb15 followed §300 and I cannot say which is right. (e) Whether beat 1's IDW-order-dependence
clause is covered upstream in nb11/nb12 — not my files, not audited.

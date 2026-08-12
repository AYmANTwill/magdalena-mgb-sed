# Journal — T6 adversarial lens: dangling references to superseded numbers

Slug: `lens-dangling-refs`. Started 2026-08-12. READ-ONLY agent. I write only this file.

## 00 — Posture
Default: superseded numbers are still presented as current somewhere, and the supersession did not
travel. A finding must be evidenced from the artifact on disk (quoted string + line number) and any
number at stake must be RECOMPUTED with python3.10, command and output pasted here.

## 01 — Plan
1. Read CLAUDE.md, docs/00_INDEX.md, docs/47, docs/46, docs/51, docs/52, docs/53.
2. Verify every `A3.*` reference in docs/37 resolves to a real heading.
3. Sweep the named superseded-number patterns across docs/*.md, src/**, scripts/**, notebooks/**,
   and data/processed/*.json quoted by docs.
4. For each hit: classify clean (inside supersession block / strike / labelled-not-quotable) vs
   finding (reads as current).
5. Recompute the 0.580685 identity and check both files' corrections.
6. Report counts swept / clean / wrong.

## 02 — A3.* dangling-reference check in docs/37 — CLEAN

```
$ grep -oE 'A3(\.[0-9]+)+' docs/37_c3_closure.md | sort | uniq -c | sort -rn
```
20 distinct tokens: A3.1 A3.1.1 A3.1.2 A3.1.3 A3.1.4 A3.1.5 A3.1.6 A3.2 A3.3 A3.3.1 A3.3.2
A3.3.3 A3.3.4 A3.4 A3.5 A3.5.1 A3.5.2 A3.6 A3.7 A3.8 (144 mentions total).

```
$ grep -nE '^#{1,6}.*A3' docs/37_c3_closure.md
```
Headings exist at: 1342 (# AMENDMENT A3), 1381 A3.1, 1413 A3.1.1, 1453 A3.1.2, 1525 A3.1.3,
1585 A3.1.4, 1606 A3.1.5, 1633 A3.1.6, 1691 A3.2, 1771 A3.3, 1783 A3.3.1, 1853 A3.3.2,
1873 A3.3.3, 1882 A3.3.4, 1985 A3.4, 2120 A3.5, 2122 A3.5.1, 2164 A3.5.2, 2199 A3.6,
2271 A3.7, 2311 A3.8.

**EVERY A3.* token resolves to a real heading. The interrupted pass's 7 dangling subsections
(A3.1, A3.1.6, A3.2, A3.3.1, A3.3.2, A3.5.1, A3.5.2) are all now real.** No finding.
Note: the file is 2373 lines, not the 2272 the T1 return claimed, and A3.3.4 (the f_area
correction) exists but is absent from T1's own heading manifest — a stale summary, not a
defect in the artifact.

## 03 — Sweep harness
Wrote `scratchpad/sweep.py` (22 tight claim-form patterns) over docs/*.md, src/**, scripts/**,
notebooks/*.ipynb.
```
TOTAL SITES 859 AUTO-CLEAN 343 NEEDS-REVIEW 516
```
"auto-clean" = the matched line itself carries a supersession token (~~, STRUCK, WARN,
AMENDMENT, superseded, WITHDRAWN, retired, ...). The 516 go to eyes-on review because the
classifier is line-local.

## 04 — FINDING (src/nbgen/make_nb19.py + notebooks/19_*.ipynb): the sigma_r = 0.465 level band
##      and the k_min set are STILL LIVE, and the notebook was RE-EXECUTED on 2026-08-12

Measurement:
```
$ python3.10 -c "import math; SE8=0.465/math.sqrt(8); print(SE8, 100*(math.exp(1.96*SE8)-1))"
0.16440232662587229 38.02001987244472
$ ... 13-station: 0.1289677956223658 -> 28.759595562555006
corrected (docs/48/42 A-P4): SE (a) 0.4775 -> +/-154.95 %, (b) 0.6936 -> +/-289.41 %
```
So `SE8` in make_nb19.py:1866 IS the 0.1644 that docs/42 §9.7 (A-P4) RETIRED, computed live
from `SIGMA_R = 0.465` used as a per-station residual sd — the exact reuse A-P4 retires.

Live sites in the generator, none carrying any supersession marker:
- :1866-1868, :1889-1891 compute and plot it
- :1913 "The level's 95 % band is consequently **+/-38 %** (0.724x to 1.380x); 13 stations
  would have given +/-28.8 %."  (the +/-28.8 % has NO corrected value — docs/45 §8.1.5 row 3
  WITHDREW it: no 13-station residual set exists)
- :1927 "the **level $\Pi$**, with the +/-38 % band of section 4.2"
- :2041 "**0.00216 /km** (all 18) to **0.0209 /km** on the CAL 8 - **9.7x worse** ... no channel
  sink weaker than a factor of ~3.5"
- :2069 the §5 DECISION verdict table, lens 3: "with a +/-38 % level band"
- :2138 "(k_min 0.0209 /km)"
- :2157-2159 BOUND table: the band from SE8, "0.00216 /km on all 18",
  "minimum detectable class-C error ~4.2x (CAL 8), ~2.9x (all 18)"  (= docs/45 O8, NO
  CORRECTED VALUE EXISTS — three passes, three answers)
- :2886-2891 three INTEGRITY ASSERTIONS that assert the superseded numbers and PASS

Verified in the executed notebook JSON (`notebooks/19_c3_gate_and_c4_setup.ipynb`):
- cell 53 OUT: `SE of the fleet-mean LEVEL at n=8  : 0.1644 ln = +/-38 % at 95 %  (0.725x - 1.380x)`
                `SE of the fleet-mean LEVEL at n=13 : 0.1290 ln = +/-28.8 %   (what docs/42 assumed)`
- cell 56 OUT: `all 18 (the guard set) 18 2.6- 348.4 0.00216 0.00216 x 2.12 over 348.4 km`
- cell 56 OUT: `CAL 8 (achievable) 8 2.6- 60.4 0.02092 0.02092 x 3.54 over 60.4 km`
- cell 56 OUT: `the 0.05-0.30 SDR band would imply k ~ 0.0020-0.0032 /km over a 600 km path.
                Printed only so a reader can see where 0.0209 sits.`
- cell 60 OUT: `+/-38 % at 95 % (SE 0.1644 ln, n=8)` ; `k_min 0.0209 /km on the fit set;
                0.00216 /km on all 18` ; `minimum detectable class-C error ~4.2x (CAL 8), ~2.9x (all 18)`
- cell 81 OUT: `PASS  the level band at n=8 is +/-38 % at 95 %`
                `PASS  k_min on all 18 reproduces the documented 0.00216 /km`
                `PASS  k_min on the CAL 8 reproduces the documented 0.0209 /km`

The T2b return named exactly ONE of these ("nb19's integrity assertion still encodes the
+/-38 % Pi band"). It did not name the other ~11 live sites, the executed-output copies, the
+/-28.8 %, the k_min triple, the 2.12x/348.4 km row, or the ~4.2x/~2.9x class-C cells.

## 05 — f_area(V4): which support survives where

Recomputed:
```
$ python3.10 -c "print(16.775413430326214/39.812260149274394, 16.775/39.812)"
0.42136300143291305 0.4213553702401286   (the latter rounds to 0.42135)
```
So three supports really are distinct: per-cell **0.42136300143291305** (docs/46 §3.3's
quantity, now registered), urh-csv area_km2 **0.4213519856784954** -> prints as 0.42135, and
engine urh_fractions **0.4214751420286394** -> prints as 0.421475 / x0.42148.

Sweep of every occurrence (grep -rnoE over docs/*.md src/**/*.py scripts/c3/*.py notebooks/*.ipynb):
CORRECTED and clean (inside supersession/amendment text): docs/37 (§A3.3.4 + :207), docs/43
(amd 8), docs/46 (§10 amd 2), docs/51 (§9 amd 1 + in-place strikes), docs/49:25/121-154 (0.42136),
docs/50 (0.421363), docs/53:361-363 (explicitly flags the discrepancy).

STILL LIVE, no marker, reading as current:
- `src/mgb_sediment.py`:223  "(area-weighted proxy [0.24468, **0.42148**], measured 2.5% low)"
- `src/nbgen/make_nb18.py`:1244, :1269, :1353 and `src/nbgen/make_nb19.py`:2435 — 0.421475
- `notebooks/18_musle_construction.ipynb` (4 output/source sites) and
  `notebooks/19_c3_gate_and_c4_setup.ipynb` (3) — RE-EXECUTED 2026-08-12
- `docs/45`:1118 §8.3's own table prints the area proxy upper end as **0.42135** (the third support)
- `docs/47`:391 §4.3's area column prints **0.42135** (T2a reported this; owed, unfixed)

**A hard internal arithmetic inconsistency inside ONE table row** (make_nb18.py:1244, and its
executed copy in nb18): the row prints `area-wtd mean 39.812 | area-wtd mean 16.775 | 0.431944 |
0.421475`. The ratio of its OWN two printed means is 0.42136 (0.4213553702401286 at the printed
precision), not 0.421475. Measured discrepancy 1.1963e-04 absolute, 2.658e-04 relative.

## 06 — the 0.580685 identity

```
$ python3.10 -c "import math; print(math.log(0.43194/0.25146), -math.log(0.580685))"
0.5410027585442313 0.543546837831505      gap 0.0025440792872737372
exp(-0.5410027585442313) = 0.5821641894707599
ln(0.42136300143291305/0.2446790094097074) = 0.5435475125003637 ; exp(-) = 0.580684608230046
ln(0.421475/0.2446790094097074)            = 0.5438132778492345
```
Corrected in BOTH files, arithmetically right: docs/46 §10 Amendment 2 (:1494-1514) and docs/51
§9 Amendment 2 (:703-721) + docs/51 in-place WARN at :193-200. No tolerance or bar smuggled in
(checked: docs/52's prohibitions are quoted, no numeric bar appears in either amendment).

BUT two residues:
(a) docs/46 §1.0 **:127 itself still reads `ln(0.43194 / 0.25146) = 0.5410 = -ln 0.580685` with
    NO in-place marker** — the correction is 1367 lines away in §10. This is *mandated* by the
    freeze (§1-§9 untouchable), so it is a structural exposure, not an owner error.
(b) `docs/35`:1063 and :1206 pair 0.580685 with an area span of **0.5438132778492345**, which is
    `ln(0.421475 / 0.2446790094097074)` — the ENGINE support T2a corrected away. Measured
    distance from -ln(0.580685): docs/35's 2.6644e-04 vs the registered per-cell
    0.5435475125003637's **6.7467e-07**. Two of this run's own corrections disagree.
(c) `docs/50`:288 prints "= ln(1/0.580685) = **0.5436**, exactly"; measured 0.5435468378315051,
    which rounds to 0.5435. LOW.

## 07 — the STRUCK 0.1644 materiality bar is still firing clauses in docs/49 and docs/50

docs/52 §1 item 1: *"There is NO numeric materiality bar. 0.1644 ln is struck"*; §9.1 records
`docs/49`, `docs/50` as **"Not edited by this pass"**. Live, unmarked sites:
- docs/49:24 "`against the 0.1644 bar`" (inside the VERDICT blockquote)
- docs/49:97 table header "`vs the 0.1644 bar`" + rows "32x inside / 19x inside / 4x inside"
- docs/49:105 "**(R4) FIRES.** `|ln f(V2b) - ln f(V2a)| = 0.0088 <= 0.1644`. **H-M's field
  clause is REFUTED**" — a clause fired by the struck bar
- docs/49:204 "would have reached the 0.1644 materiality bar only if ... 83.8 %"
- docs/50:104 "`|ln f(V5) - ln 0.790| = 0.02584 <= 0.1644` => docs/46 §2.5's H-L refutation
  clause **FIRES**"
- docs/50:187 "Both individual errors are also inside `docs/46`'s **0.1644 materiality bar**"
MITIGATION measured, not assumed: docs/52 §5's "Explicitly NOT bar-dependent" list names
**(R4) 0.0088** and **H-L 0.0258**, so neither VERDICT moves. The defect is the live instrument,
not the outcome.

## 08 — cross-reference resolution sweep (the brief's HIGH-priority item)

Wrote `scratchpad/xref.py`: harvest every heading id in docs/*.md, then resolve every
`docs/NN §M` / `docs/NN section M` reference in the seven files this run touched.
```
---- refs checked 1246, unresolved 18
```
All 18 triaged by hand, and **all 18 are false positives or the corpus's own item-numbering
convention** — zero genuinely dangling:
- `docs/00 §6` x3 -> exists (docs/00_INDEX.md:242); my mapper resolved "00" to
  docs/00_objectives_and_hypotheses.md.
- `docs/37 §5.1/§5.3/§5.4` x4 (cited by docs/42:14,:330,:528,:543 and docs/45:451) -> docs/37 §5
  is a numbered ITEM list (line 341). I READ IT: item 1 does contain the alpha 6.83-8.73
  channel-deposition trap docs/42:14 cites it for; item 3 does contain
  `SedParams.convention_summary()`. The citations say what they are cited for.
- `docs/41 §8.1/§8.3` x3 -> docs/41 §8 items 1 and 3; item 3 IS "The ENSO contrast is unchanged",
  which is what docs/37:614/:845 correct. Resolves.
- `docs/51 §5.6b/§5.6c` x2 -> §5.6 items (b)/(c) (line 361). Resolves.
- `docs/45 §1.1` x2 -> §1 has no subsections; loose, semantically resolvable. LOW, pre-existing.
- `docs/35 §9.5` x1 -> docs/45:1596 is the *deliberate* end-delimiter of a PROPOSED, NOT ENACTED
  docs/35 amendment; the same line says so. Correct as written.

## 09 — FINDING: docs/37:1258 (A2.4 item 2) still prints the retired level SE as registered

```
$ grep -n '0\.1644\|38 %\|0\.465' docs/37_c3_closure.md
1258:   SE = 0.465/√8 = **0.1644 ln = ±38 % at 95 %**; **β is identifiable** (SE 0.020, ...
1256:   ... `k_min` **0.0096 → 0.0209 /km** (2.2× worse ..., **9.7×** worse ...)
```
No strike, no pointer, in a document A3 edited in ~20 places this run. It is registered as OWED
in THREE places: docs/48 §5.2 row 8 ("`docs/37`:1158 (A2.4) ... this is a pointer, not an edit"),
docs/42 §9.7.5 row 7 ("OWED to `docs/37`'s owner"), and docs/37's OWN A3.7 table at :2288.
(The line has moved 1158 -> 1258 because A3 inserted text above it.)
The 2.2x/9.7x RATIOS at :1256 are correct and must not be touched (docs/42 §9.7.5 row 19: sigma_r
cancels) — only the absolute 0.0209 and the 0.1644/±38 % are superseded.

## 10 — FINDING: nb18's equifinality FIGURE draws the superseded rescaled alpha band and a
##      superseded alpha reference, contradicting the same notebook's own cells

`src/nbgen/make_nb18.py`:2866-2871 (executed copy `notebooks/18_musle_construction.ipynb`
:4471,:4475, cell timestamped `2026-08-12T16:10:44`):
```
                (4.45, r'like-for-like ref for OUR $LS$')]:
ax[1].axvspan(2.0, 9.9, color=CB['amber'], alpha=0.14,
              label='the SAME band rescaled for our $LS$ level')
```
and the reading at :2893 / ipynb:4504 "the pre-registered band (5.9-23.6) and its rescaled
counterpart (**2.0-9.9**) ... the like-for-like reference for our own topographic level at about
**4.45**".

Measured:
```
$ python3.10 -c "print(11.8*0.25146, 11.8*0.43194)"    -> 2.9672280000000004 5.096892
$ 4.45/11.8 = 0.3771186440677966   (no registered f_LS; nearest is 11.8*sqrt(0.333*0.421)=4.4182,
                                    the geometric mean of the RETIRED endpoints)
```
The SAME generator prints the correct values elsewhere: :1311 "11.8·f = **2.967 - 5.097**",
:1426 "expected band 5.9-23.6*f: 1.4836 - 10.1939", :1511 "turns the expected 5.9-23.6 into
**1.484-10.194**". So one notebook contains both. docs/37 A3.2 registers 5.9-23.6·f at the
adopted POINT as 1.4836140000000002 - 5.934456000000001.

## 11 — FINDING: the retired "mountainous LS 2-10" band is labelled a GATE in scripts/c3/ls2d.py

`:513` `print(f"\nGATE 2  basin distribution (published mountainous range ~2-10 for the median)")`
`:666` `label="published mountainous range 2–10"` drawn as a green axvspan.
Against `src/mgb_sediment.py`:213-216, which says of this band: *"may not be used to pass OR fail
a gate, so it is retired in BOTH directions. Do not reinstate it."* The script names it GATE 2.
(docs/31:256 and make_nb18.py:982/:1135 also carry it; nb18's two sites are argued against, so
they are clean.)

## 12 — docs/46's x1.008878 is a digit transposition, at 6 sites, in a FROZEN document, unamended
```
$ python3.10 -c "print(0.522043/0.517480, 0.517480*1.008878)"
1.0088177320862641   0.52207418744        (back-solve does NOT return 0.522043)
$ 0.505092/0.502472 = 1.0052142208919104  (printed 1.005212 — fine at 6 s.f.)
```
Sites: docs/46:163, :208, :265, :448, :454, :1095. Should read x1.008818. NOT covered by §10
Amendment 2 (grep: 1.008878 does not occur above :1401). docs/49's own |ln| = 0.00878 =>
exp = 1.008819, so docs/49 is right and docs/46 transposed it. IMMATERIAL to the (R4) verdict
(docs/52 §5 lists (R4) as not bar-dependent), but it is a wrong registered number.

## 13 — SWEEP TALLY (auditable)
sites matched by the 22 claim-form patterns: **859** across **31** files
auto-clean on the line itself: **343**
hand-reviewed: **516**  ->  clean in context **459**, reading as CURRENT **57**
The 57: make_nb19.py 15 + nb19.ipynb 9 · make_nb18.py 3 + nb18.ipynb 3 (alpha band/4.45) ·
f_area 0.421475/0.42148: mgb_sediment.py 1 + make_nb18 3 + make_nb19 1 + nb18 5 + nb19 3 ·
docs/49 4 + docs/50 2 (the struck 0.1644 bar firing clauses) · docs/37 1 · docs/45 1 + docs/47 1
(0.42135) · docs/35 2 (wrong-support area span) · scripts/c3/ls2d.py 2 · docs/50 1 (0.5436).

## 14 — Checked and found CLEAN (so the absence of a finding is informative)
- docs/48 is wholly a supersession register; every 0.1644/38 %/k_min hit is in an old->new table.
- docs/42's body sites all carry A-P4 WARN pointers (verified :739-745, :753-760, :854-875).
- docs/43 §3.2's Pi row and k row are struck WITH replacements (read :206-211). T5's report that
  "docs/43:191 still prints 0.465/sqrt(8)" was true at T5's read and is FALSE on disk now.
- docs/35 §9.4's ten sites are all inside the amendment; :1025 reproduces the struck provenance
  248.730x0.421=104.71533 / x0.333=82.82709 explicitly as struck arithmetic.
- x0.333/x0.421 and 2.37x-3.00x: no live instance survives in any docs/*.md outside a
  supersession block (docs/39:192 is the contradiction register and marks them; docs/49:216/:243
  and docs/50:243 are old-vs-new tables).
- The withdrawn "~2x under-erosive" direction: every surviving hit refutes it (nb19:714 "This
  refutes...", docs/47:272, docs/43 §3.3 item 5). The live 1.03x-2.27x is a different, measured
  quantity.
- SDR 0.05-0.30: nb18:2482-2514 draws it and labels it "the RETIRED 0.05-0.30 band"; docs/40/41/
  42/43/45/48 all name it uncited. Clean everywhere.
- The product-as-joint prohibition: no surviving instance quotes a product AS the joint. docs/37
  :209-213, docs/43:554-572, nb18:1902/:2026, mgb_sediment.py:250-258 all print the ratio form.
- docs/37: every A3.* token resolves (§02); 1246 cross-refs, 0 dangling (§08).

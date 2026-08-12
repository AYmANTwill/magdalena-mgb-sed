# Journal — T6 adversarial lens: "Is the new bar the old error in a new costume?"

Slug: `lens-new-bar-costume`. Started 2026-08-12. READ-ONLY agent: I write only this file.

## 00 — Mandate
Default posture: the replacement machinery makes claims it cannot support, and some number written
this run is a materiality bar wearing a different hat. Prove it or clear it, from the artifact on
disk, with recomputation.

## 01 — First actions
- Created this journal (first action).
- Next: `git status` / `git diff --stat` read-only to enumerate what this run touched.

## 02 — What this run touched (read-only git)
`git status --porcelain` + `git diff --stat`:
modified: `.claude/settings.json`, `docs/00_INDEX.md`, `docs/30_phase_c_plan.md`,
`docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/45`, `docs/46`, `docs/51`,
`notebooks/18`, `notebooks/19`, `src/mgb_sediment.py`, `src/nbgen/make_nb10.py`,
`make_nb11.py`, `make_nb18.py`, `make_nb19.py`.  +6132/-963.

**NOT in the orchestrator's list of owners:** `docs/00_INDEX.md`, `docs/30_phase_c_plan.md`,
`src/nbgen/make_nb10.py`, `src/nbgen/make_nb11.py`, `.claude/settings.json`. In scope for my lens
because the mandate is "EVERY file written or amended this run".
`.claude/settings.json` diff = two added Bash/Read *allow* entries (agent-journal listing +
workflow-log read). No engine default. Noted, not a lens finding.
A transient `docs/00_INDEX.md.tmp.27204.4e0723c4f0b0` was present in the first `git status` and
had vanished by the next call (atomic-write temp). Nothing to report.

## 03 — Forbidden-number sweep (docs/52 §7 item 2)
`grep -c` over every amended doc + nbgen + mgb_sediment for
0.1644 / 0.3054 / 0.4775 / 0.6936 / 0.465 / 0.8500 / 1.2833 / 0.8602:
counts 56 / 4 / 16 / 27 / 70 / 7 / 9 / 11. Every occurrence inspected by context (see §05, §06).
All four 0.3054 hits are inside `docs/46` §2.0's own prohibition list / BAR-DEPENDENT register —
legitimate (the prohibition has to name the numbers it forbids).

## 04 — Arithmetic reproductions (python3.10)
```
0.465/sqrt(8)          = 0.16440232662587229
exp(+/-1.96*0.1644)    = 0.7245358761151398  1.380193904768195   -> the "0.724x-1.380x / +-38 %" pair
1.9618/sqrt(8)         = 0.6936010416658844
1.3506/sqrt(8)         = 0.4775092093352755
exp(+/-1.96*0.6936)    = 0.256800438400688   3.894074349046442
1.96*0.1644            = 0.32222399999999995  -> G12's "+-0.322 ln" IS 1.96 x the struck bar
0.6936/0.1644          = 4.218978102189781    -> the "~4x too narrow" claim reproduces
6.0214/7               = 0.8602               -> LOO range = range/(n-1), exactly as claimed
0.644/2                = 0.322
```
So every published SE/band arithmetic in the enacting texts reproduces exactly.
**And G12's retained threshold is arithmetically 1.96 x the struck 0.1644.** That is the sharpest
costume candidate; pursued in §07.

## 05 — Source-citation spot check (FIRST PARTY, not carried)
`sha256 data/raw/refs/buarque2015.pdf` = 3047624f...c0037, 9,646,521 B, **matches** docs/38 §9.1.
182 PDF pages; printed page N = 0-based index N+15. Extracted with PyMuPDF:
- **printed p. 47**: eq. (13) `Lk = ((Am+Lp^2)^(m+1) - Am^(m+1)) / (Lp^(m+2) * Xdir_k^m * 22,13^m)`
  — Desmet-Govers finite difference with `Xdir_k^m`; and eq. (14) the **step** on
  `Sf < 1 / 1<=Sf<3 / 3<=Sf<5 / Sf>=5` with *"onde Sf [%] e a declividade do pixel"*. CONFIRMS
  docs/37 A3's "m eq. 14 printed p. 47" and "L eq. 13 printed p. 47".
- **printed p. 48**: eq. (18) `Sk = 65,41 sin^2(theta) + 4,56 sin(theta) + 0,065`,
  *"sendo theta o valor de Sf em graus"* — Wischmeier & Smith (1978). CONFIRMS "S eq. 18 p. 48".
- **printed p. 94**: *"Na determinacao do fator comprimento de 'L', seu valor maximo foi limitado
  ao tamanho do pixel do MDE."* — the limiter, CONFIRMED.
- **printed p. 98**: *"o maior valor permitido pelo modelo para o fator L e igual ao limite da
  dimensao de cada pixel"* — independent corroboration, CONFIRMED.
- **printed p. 121**: *"o valor maximo e grande e tende a fazer com que as estimativas ... seja
  superestimado (EPA, 2004)"* + *"o modelo adota um fator LS bidimensional"* — CONFIRMED.
=> **No page citation this run is unsupported.** All four CITED grades have their page.

## 06 — `min(m, 0.5)` is nowhere graded CITED
grep over docs/35/37/42/43/45/46/51 + both nbgen: every occurrence carries "CAP",
"nobody's published formulation", or "may NEVER be graded CITED". docs/37:1592 excludes it
**by name** from grade (A). CLEAN.

## 07 — The G12 question: is the retained 0.644 ln the struck bar in a new costume?
Measured: `1.96 * 0.1644 = 0.32222`, so G12's retained `+-0.322 ln / 0.644 ln full width` **IS
arithmetically 1.96 x the struck 0.1644 bar.** So the shape of the objection is real. But it is
NOT the same error, on four checks I ran:
1. `docs/52` §7 item 7 pre-blesses it by name ("G12's 0.644 ln fragility threshold" untouched),
   and it was blessed BEFORE Delta_shape was computed.
2. Both enacting texts **withdraw the provenance instead of claiming one**:
   `docs/43`:499-501 - "with its origin recorded (it was `1.96 x sigma_r/sqrt(8)`, and it keeps
   that value as a threshold, not as an SE)"; `docs/45`:757-758 - "Its provenance (originally
   sigma_r/sqrt(8)) is recorded and no longer load-bearing". The original failure was CLAIMING a
   provenance; this is the inverse move.
3. It does not pass or fail a gate, so `docs/40`'s rule is not engaged: `docs/45`:493 registers
   G12's ACTION as "INDETERMINATE, not a pass and not a fail" and its FAIL condition as
   "the §6 verdict flips on any single deletion" - which does not read 0.644 at all. The 0.644
   is compared only for a MANDATORY REPORT.
4. Retaining it is the strictly conservative direction: it fires at 0.8602 and would stop firing
   under either corrected band (2.7190 / 2.5666). Re-pointing it would silence a firing
   comparison by widening its comparator.
=> **NOT a finding.** One residual wording defect only, see §16(a).

## 08 — Pi-band provenance: real
`docs/48`:239-260 §3.3 is the source of record: seed **20260810**, **10,000** station resamples,
est (a) point +2.5772 CI [-0.8279,+0.8721] -> x0.418-x2.289; est (b) +1.9240 CI
[-1.3163,+1.2503] -> x0.286-x3.730. `docs/45` §8.1.3 and `docs/43` §7 amd 1 reproduce those
digits exactly and both name the source, the station set (CAL 8), the window, the estimators, and
register the band as a **PROCEDURE** with the union `[0.29, 3.73]` labelled "a reporting
convention and explicitly NOT a statistical claim".
**Wrong-error-term test (docs/52 §2.1): PASSES.** The band is on the ABSOLUTE, UNPAIRED level
Pi_hat, and `docs/43`:434-437 derives the right variance decomposition in words ("observation
error plus model error plus between-station heterogeneity"). docs/52 §2.1's objection was to using
`sd/sqrt(n)` for a **paired deterministic** LS contrast; nothing here does that.
Both texts also carry the reciprocal-orientation trap (`exp(-hi), exp(-lo)`), re-verified:
`exp(-0.8721)=0.4181`, `exp(+0.8279)=2.2885`.

## 09 — FINDING (CRITICAL): the +-38 % band is NOT dead. It PASSES an integrity assertion in an
artifact re-executed this run.
`src/nbgen/make_nb19.py`:1866 `SE8 = SIGMA_R / np.sqrt(8)` with :1852
`SIGMA_R = 0.465  # ln units, docs/42 section 4.2 - PER STATION, does not average down`
— the exact falsified derivation. Read out of the EXECUTED
`notebooks/19_c3_gate_and_c4_setup.ipynb` (not from an exit code):
```
cell 53 OUT: SE of the fleet-mean LEVEL at n=8  : 0.1644 ln = +/-38 % at 95 %  (0.725x - 1.380x)
cell 60 OUT: Pi (the level) ... +/-38 % at 95 % (SE 0.1644 ln, n=8)
cell 60 OUT: channel deposition k ... k_min 0.0209 /km on the fit set; 0.00216 /km on all 18
cell 81 OUT:   PASS  the level band at n=8 is +/-38 % at 95 %
cell 81 OUT:   PASS  k_min on all 18 reproduces the documented 0.00216 /km
cell 81 OUT:   PASS  k_min on the CAL 8 reproduces the documented 0.0209 /km
```
plus markdown cells 54/55/59/61 asserting it in prose, including "13 stations would have given
+/-28.8 %" - which `docs/45` §8.1.5 row 3 WITHDREW with no corrected value the same day.
And `make_nb19.py`:1843 labels sigma_r = 0.465 "a **per-station** residual floor" - the reuse
`docs/42` §9.7.2 retires BY NAME.

## 10 — FINDING (HIGH): docs/37:1258 still carries the falsified statistic, unstruck
`grep -n "0.1644" docs/37_c3_closure.md` -> :1258, :1629, :2030, :2288.
:1258 is **A2.4 item 2** (a body amendment `docs/00_INDEX` row 37 tells readers to read):
`SE = 0.465/sqrt(8) = **0.1644 ln = +-38 % at 95 %**` - no `~~`, no dated pointer, no [WARN].
`docs/42` §9.7.5 row 7 (written this run) registers exactly this: "docs/37:1158 (A2.4) ... OWED
to docs/37's owner", and docs/37's own A3 at :2030 lists B5 as outstanding. The file grew
1331 -> 2382 lines this run; this site was not touched.

## 11 — FINDING (HIGH): docs/51 still runs verdicts through the struck bar, and §7 item 2 orders
a future session to keep one
`docs/51`:228-233 and :255-257 are tables with a column literally headed `bar` containing
**0.1644**, reaching verdicts: "(R4) ... FIRES => H-M's field clause REFUTED, 19x inside",
"immaterial (45x inside)", "0.307 | 0.1644 | MATERIAL - the endpoint is wrong".
`docs/51`:474-477 (§7, "An orchestrator can execute this list top to bottom"):
> 2. **Decide `docs/46`'s materiality bar** - §5.6 (e), the one real decision. Decouple it from
>    sigma_r; ... do not rescale it silently, and do not import 0.6936 by default - the bar is
>    a decision threshold, not a standard error.
`grep -n "docs/52" docs/51*.md` -> only :657, :676, :678, :730, all inside the NEW §9. No
pointer exists at :232, :233, :257, :352, :371 or :475. `docs/52` §8(d) explicitly says the (R4)
label "is owed to docs/51's owner as a note"; docs/51's owner amended docs/51 this run
(five strikes + a new §9) and did not enact it.

## 12 — FINDING (HIGH): docs/45's registration card says THREE amendments; §8 has FOUR
`grep -n "^## 8\.[0-9]" docs/45*.md` -> 8.1 (:700), 8.2 (:951), 8.3 (:1109), 8.4 disclosure
(:1163), **8.5 Amendment 4 (:1213)**. `docs/45`:644 (the §7.1 registration card):
"| Amendments | **THREE, all dated 2026-08-12, all in §8, by the `amend-45-piband-disclosure`
agent** ...". Amendment 4 - the re-expression of the C4.3 gate into Pi - is absent from the card.
(Its author flagged it; it is still wrong on disk and no owner holds it.)

## 13 — FINDING (MEDIUM): docs/00_INDEX row 53, added THIS RUN, asserts docs/52 "fixed" a bar
`git diff docs/00_INDEX.md` shows the row as a `+` line. `docs/00_INDEX.md`:154:
"| 53 | delta_shape_pretest | the `Delta_shape` pre-test COMPUTED: 0.1299456916752905,
judged against **the bar `docs/52` fixed** blind to it -> Branch B. ..."
`docs/52` §7 item 1: "NOT 'the bar is zero' ..."; item 3: "The `Delta_shape = 0` discriminator
is NOT a materiality bar of zero." docs/53 itself uses "bar" in headings but says at :279
"**not** a materiality bar"; the index drops that qualifier and attributes the bar to docs/52.
CLAUDE.md makes docs/00_INDEX "START HERE. The single entry point."

## 14 — Legitimate tolerances: checked, all intact and not blurred
`docs/49` gate 2, `report_h2e.py` F = 0.25931 to 1e-8, the 299.5387088405831 Mt/yr basin gate,
the 3,266-day count, G1.1 `D_pair > +0.658`, G8/G11 0.465 FIRING thresholds, `b_obs` IQR
0.464, SE(beta) 0.0199 - every one is listed in a "DOES NOT CHANGE" register
(`docs/45`:895-903, `docs/42` §9.7.6, `docs/46`:352) and none is restated. `docs/46`:352 and
`docs/45`:1203-1205 both state the tolerance/bar distinction explicitly.
`k_min` is labelled a **detection floor** (`docs/42`:1005) and the stronger/weaker comparative is
corrected to *weaker* - the direction that makes the guard weaker, not the model better.

## 15 — Frozen artifacts and engine defaults: untouched
mtimes: everything in `data/processed/sim_calibrated_v2/` is 2026-08-03 / 08-10; `urh_ls2d.csv`
and `minibacia_ls2d.csv` 2026-08-11_04:15; `urh_ls2d_variants.csv` 2026-08-11_21:50. Nothing
written 2026-08-12. `src/mgb_sediment.py` diff is ONE hunk, `@@ -212,4 +212,52 @@`, entirely
inside the module docstring; `ast.parse` OK; `ls2d_column="ls2d_hs"` (:805,:849,:912),
`urh_ls2d="urh_ls2d.csv"` (:911), `DEFAULT_CP_REVISION="cited_central_2026_08_11"` (:695),
WILLIAMS_ALPHA/BETA (:584-585) all unchanged.

## 16 — LOW: two wording/label residues
(a) `docs/43`:497-501 says "the measured LOO range 0.8602 exceeds it and **G12 FIRES**";
`docs/37`:2030 says "G12 already firing". G12's registered FAIL condition is the §6 verdict flip
and its action is INDETERMINATE (`docs/45`:493) - what exceeds is the mandatory REPORTED
comparison, not the guard. `docs/45` states it correctly ("The verdict-flip condition in the FAIL
column is untested pre-fit"). Also 0.644 vs 0.6445 for the same full width
(`2*1.96*0.16440232662587229 = 0.64445712`), printed both ways.
(b) `src/mgb_sediment.py`'s NEW docstring prints the area proxy `[0.24468, 0.42148]`, the engine
URH-fraction support the same run corrected to 0.42136300143291305. Already recorded as owed at
`docs/37`:1986-1987 (which names this exact site plus `make_nb18.py`:1244,1269,1353 and
`make_nb19.py`:2435), so it is a known collision, not a new claim - LOW.

## 17 — Verdict
No new materiality bar was created, quoted or reconstructed in the amendment TEXT; the Pi band's
provenance is real and correctly typed; every Buarque page citation checks out first-party. The
failure this run has is the OPPOSITE of invention: the retired instrument is still LIVE in three
places - an executed notebook whose integrity assertion PASSES on it, docs/37's A2.4 item 2, and
docs/51's executable §7 item 2.

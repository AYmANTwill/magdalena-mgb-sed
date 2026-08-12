# Journal - refute-t6-3 (REFUTER, T6 finding: docs/37:1258 unstruck 0.1644 SE)

Role: adversarial refuter. Default posture: the finding is WRONG. Read-only except this journal.

## 0. Task received 2026-08-12
Finding (HIGH, lens-new-bar-costume): docs/37_c3_closure.md line 1258, inside "## A2.4 What this
changes for C4" item 2, still prints `SE = 0.465/sqrt(8) = 0.1644 ln = +-38 %` unstruck and
un-pointered, in a LIVE document whose amendments docs/00_INDEX promotes to must-read.

Plan:
1. verbatim check of line 1258 (misquote = refutation)
2. surrounding context: is it a supersession/historical block?
3. is docs/42:1037 owing register real, and does docs/37 A3 list B5 as outstanding?
4. category check: identifiability (beta, sigma_day) vs Pi band (level, sigma_r)
5. retired-claim check: the 0.1644 bar is STRUCK per docs/52 - is the finding re-raising it?
6. severity

## 1. Verbatim check — the string EXISTS at the named locator
```
$ grep -n "0.1644\|±38\|0.465/√8" docs/37_c3_closure.md
1258:   SE = 0.465/√8 = **0.1644 ln = ±38 % at 95 %**; **β is identifiable** (SE 0.020, 95 % half-width
1629:...docs/52's striking of docs/46's 0.1644 ln bar is respected: nothing here compares a difference...
2030:- **B5** (replace the ±38 % Π band — measured ~4× too narrow in log units, with G12 already firing...
2288:| docs/45 §8 ... B5 (the ±38 % Π band replaced; ...) | docs/47 §6.1 B2/B5 ...
```
Read 1200-1275: the site sits inside `## A2.4 What this changes for C4 — added to A1.6, which
otherwise stands unchanged`, item 2, a PRESCRIPTIVE amendment section (it modifies what A1.6
permits for C4). NO misquote. NOT a misquote-refutation.

## 2. Context check — is it a supersession / historical / register block? NO
```
$ grep -n "\[WARN\]" docs/37_c3_closure.md      -> (no output; docs/37 uses no WARN blocks)
$ sed -n '1245,1262p' docs/37_c3_closure.md | grep -n "~~"   -> (no output; nothing struck in A2.4)
$ grep -n "A2\.4" docs/37_c3_closure.md         -> 1245 only (the heading; A3 never points back at it)
```
So: not struck, no inline warning, no pointer, and A3 never names A2.4 as a site. docs/37 is NOT a
register-of-superseded-values document (that is docs/39/46 §1.0/47 §3) — it is the C3 verdict.
docs/00_INDEX.md:123 row 37: "LIVE — **read the amendments, not only §1–§6**" — the amendments are
promoted to must-read. (The finding cited the index at :147; the actual row is :123. String verbatim,
locator off by one row-block — cosmetic.)

## 3. Was the site really untouched while the file was rewritten? YES (git, read-only)
```
$ git show HEAD:docs/37_c3_closure.md | wc -l          -> 1238
$ git show HEAD:docs/37_c3_closure.md | grep -n 0.1644 -> 1158:   SE = 0.465/√8 = **0.1644 ln...
$ git diff --stat -- docs/37_c3_closure.md             -> 1178 insertions(+), 34 deletions(-)
$ git diff -U0 -- docs/37_c3_closure.md | grep ^@@ | tail -2
@@ -1082 +1182 @@ ...
@@ -1238,0 +1339,1044 @@ was believed survives intact; the retired claim can no longer be quoted as live.
```
The last in-body hunk is old:1082. NO hunk covers old:1158. The site is untouched; the file gained
1044 appended lines. The final hunk's context line is A2.7's own method sentence — "the retired claim
can no longer be quoted as live" — i.e. this document's OWN established standard is the one violated.
(Finding says the file "was 1331 at the start of the run"; HEAD is 1238. docs/37 was already dirty in
the working tree at session start, so 1331 is plausibly the working-copy count then. Immaterial.)

## 4. The arithmetic, recomputed independently
```
$ python3.10 -c "import math; se=0.465/math.sqrt(8); print(se, 1.96*se, (math.exp(1.96*se)-1)*100); \
  [print(m, m/se, math.exp(-1.96*m), math.exp(1.96*m)) for m in (0.4775,0.6936)]"
SE 0.16440232662587229
95% halfwidth ln 0.3222285601867097
pct 38.02001987244472  /  -27.546742789619984
0.4775 ratio 2.90446011197055  band 0.3922 - 2.5495
0.6936 ratio 4.218918395105285 band 0.2568 - 3.8941
```
0.465/√8 = 0.16440 and ±38.0 % at 95 % are internally consistent — the printed line is arithmetically
right and EVIDENTIALLY falsified: σ_r = 0.465 is an ESTIMATOR-DISAGREEMENT statistic (0.658/√2),
not a residual sd. Measured residual sd on CAL 8: 1.9618 ln (est b) / 1.3506 (est a) ⇒ SE 0.6936 /
0.4775 ⇒ the band is 4.22× too narrow in log units. Confirmed at docs/43:438-439, docs/45:135, :720-721,
:874, docs/42:962-963, :967.

## 5. The corpus is now internally inconsistent — the same clause is STRUCK in three siblings
- `docs/43` §3.2 :209 — struck in place + ⚠ pointer to §7 amendment 1 (band = station bootstrap
  Π̂ × [0.29, 3.73], a PROCEDURE + pre-fit expectation, not a bar).
- `docs/45` §2.2 :135 — struck in place, "RETIRED — §8 Amendment 1"; §8.1 exists at :700.
- `docs/42` §9.7 (A-P4) blast-radius table row 7 at :1037 — `docs/37`:1158 (A2.4) ... "**OWED to
  docs/37's owner**". (:1158 was CORRECT against HEAD; the working copy has drifted it to :1258.
  Reported, not fixed — docs/42 is not mine.)
- `docs/37`'s own A3 §(2) :2030 — "B5 (replace the ±38 % Π band — measured ~4× too narrow in log
  units ...) is owed **before any C4 number is PRINTED**."
So docs/37 both PRINTS the band as live at :1258 and DECLARES it ~4× too narrow at :2030.

## 6. Category / retired-claim checks — the finding survives both
- NOT a category error. docs/46's struck 0.1644 was a MATERIALITY BAR; docs/37:1258 is an SE/level
  BAND. Different uses, but the shared DERIVATION (σ_r=0.465 reused as a residual sd) is falsified on
  measured grounds independent of the bar's retirement — so striking the bar is not what condemns
  :1258; the measurement is.
- NOT a re-raise of a retired claim. The fix asks for a strike + pointer to measured SEs and the
  bootstrap PROCEDURE. It reconstructs no materiality bar. Caveat for the enactor: ×[0.29, 3.73] must
  be quoted as a procedure/pre-fit expectation, never as a gate or bar.
- Scope of the fix is right: "β is identifiable (SE 0.020)" rests on σ_day/b_obs IQR and is expressly
  UNCHANGED — docs/45 §8.1.5 row 9: "pair-σ 0.658, b_obs IQR 0.464, **SE(β) 0.0199 unchanged**".
  So leaving the β clause alone is correct.

## 7. Severity
HIGH stands. Mitigations exist (registered as OWED in docs/42 row 7; docs/37 A3 :2030 flags it; the
"before any C4 number is PRINTED" gate; C4.3 is BLOCKED anyway, so no gate can mis-PASS on it) — that
caps it below CRITICAL. But it is not below HIGH: it is a live, unstruck, must-read numeric claim that
is measured 4.22× too narrow, at a site three sibling documents have already struck, in the very
section titled "What this changes for C4", and in a document whose own A2.7 established the rule that
a retired claim must not remain quotable from the body.

## VERDICT: refuted = false. Could not kill it.

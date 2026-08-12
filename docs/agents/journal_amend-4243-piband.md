# Journal - agent `amend-4243-piband` (T3)

Task: enact docs/48's Pi-band revision into **docs/42 §9 (AMENDMENT A-P4)** and create
**docs/43 §7 amendment slot** with three amendments (Pi band, §1.4 eq.-14 mislabel,
superseded LS bracket) + docs/47 §2.5 C1/C2.

I own for WRITING: `docs/42_c4_guards.md`, `docs/43_c3_c4_gate.md`, this journal. Nothing else.

## 2026-08-12 - session open

- [ ] Read CLAUDE.md (in context), docs/00_INDEX.md, docs/47, docs/46, docs/51, docs/52, docs/53
- [ ] Read docs/48 in full, docs/47 §2.2, §2.5, §6.2
- [ ] Read docs/42 §4.1, §4.2, §9 (all of it), docs/43 in full
- [ ] Write docs/42 §9 A-P4 + body strike-throughs per §9.6 F1 remedy
- [ ] Write docs/43 §7 slot with 3 amendments

## Reading log (done before any edit)

- CLAUDE.md (in context), `docs/48` in FULL (589 lines), `docs/47` in FULL (677),
  `docs/43` in FULL (360), `docs/42` §4.1–§4.2 (180–308), §6 G1.2 (330–365), G5 (465–480),
  G8/G9 (515–560), §9 in full (590–832), `docs/45` §4.2 G12 (:445), §6.1 (:530–534), §8 (:610,
  reads *"Empty at registration"* at my read — the docs/45 amendment is a PARALLEL agent's),
  `docs/46` §1.0, §1.2, §2.5.1, §2.5.2, §7.3, section index; `docs/52` decision block + §1.2/§5.
- Key governance facts I am bound by and did not re-litigate:
  - `docs/52`: **0.1644 is STRUCK, not rescaled**; there is NO numeric materiality bar anywhere in
    `docs/46`; 0.6936 is named "wrong error term / premise false" *as a bar*. So A-P4 must
    restate σ_r's **reuse** and must NOT hand anyone a replacement bar.
  - `docs/47` §2.2 narrows the scope: σ_r propagates into (i) the level SE/±38 % band and
    (ii) the `k_min` power numbers **and nothing else**. SE(β)=0.0199 (σ_day 0.809) and the
    `b_obs` IQR 0.464 are untouched; firing thresholds (G1.1 +0.658, G8, G11 0.465) err SAFE and
    are untouched; G12's 0.644 ln full width is kept as a standalone fragility threshold.
  - `docs/48` §3.2 **REJECTS route 1** (G12's LOO range as a band-replacement rule) on two
    measurements and recommends route 2 (station bootstrap).

## Measurements I made myself (scratchpad `t3_check.py`, python3.10, nothing written to repo)

Command: `python3.10 t3_check.py` in the session scratchpad. Output verified, not transcribed:

| check | result |
|---|---|
| `0.465/sqrt(8)` | **0.16440232662587229** → the registered 0.1644 reproduces |
| `1.9618/sqrt(8)` | **0.6936010416658844** → 0.6936 reproduces; `1.3506/sqrt(8)` = **0.4775092093352755** |
| `1.9618/0.465` | **4.2189247311827955** (the ×4.22) |
| `exp(±1.96·0.1644)` | 0.7245358761151398 – 1.380193904768195 → the "0.724×–1.380×" reproduces |
| `exp(±1.96·0.6936)` | **0.256800438400688 – 3.894074349046442** → `docs/47`'s "0.257×–3.894×" reproduces |
| G12 half-width `1.96·0.1644` | **0.32222399999999995**, full width **0.6444479999999999** |
| LOO range `6.0214/7` | **0.8602**; `exp(0.8602)` = **2.363633373110901**; `exp(6.0214)` = **412.1552092960013** (the factor 412) |
| **bootstrap band ORIENTATION** | `exp(-0.8279), exp(+0.8721)` = 0.4370, 2.3919 ≠ `docs/48`'s printed ×0.418–×2.289. **`exp(−hi), exp(−lo)` = 0.4180726741360727, 2.2885078241395704 DOES match**, and est (b) `exp(−1.2503), exp(+1.3163)` = **0.28641885831255876, 3.7295963103109484** matches ×0.286–×3.730. **The band on the level multiplier is the RECIPROCAL of the residual CI** (r = ln(sim/obs), so a positive residual means Π must come DOWN). Recorded because applying the CI without the flip inverts the band. |
| mean half-widths | (0.8279+0.8721)/2 = **0.8500**; (1.3163+1.2503)/2 = **1.2833** — so `docs/52`'s "bootstrap half-widths 0.8500 / 1.2833" are the **symmetric summaries of asymmetric intervals**; full widths **1.7000** / **2.5666** |
| `k` corrected, over 341.5 km | 0.0065 → 9.205; **0.00686 → 10.409**; 0.0069 → 10.552. Over 342 km: 9.235 / 10.445 / 10.589. Over 345.8 km at 0.00694 → **11.022**; at 0.00658 → 9.731. ⇒ "**≈ 9×–11×, central ≈ 10× over ~342 km**" reproduces |
| registered `exp(0.00216·348.4)` | **2.122392521012205** (the 2.12×) |
| CAL-8 corrected | `exp(0.0838·61.5)` = **173.07**; `exp(0.0883·57.8)` = **164.64** |
| the 9-station counterfactual | `exp(0.01210·341.5)` = **62.31** (≈ 62.4×); **0.0838/0.01210 = 6.9256** ⇒ A-P2's factor **6.9 SURVIVES** |
| ratios that survive | 0.00686/0.00216 = **3.176**; 10.409/2.122 = **4.904** (the contrast moves 4.9×, the coefficient 3.18×) |
| CAL-13 at registered σ (A-P1.1) | `exp(0.00964·107.8)` = **2.8269** (→ 2.83× span) and `exp(0.00964·110.4)` = **2.8987** (→ 2.90× max) — **consistent with §9.5's landing on 0.00964**, which I therefore do NOT contradict |
| LS levers, erosion-weighted | `0.362435 × 0.522043 × 1.694054` = **0.3205262902296241**; joint 0.431944 ⇒ **joint/product = 1.347608646050708** (the registered ×1.34762). With the **cap** instead: 0.3177246791318452 — a different number, and the cap is NOT eq. 14 |
| `docs/43` §1.4 as printed | `0.502 × 1.714 × 0.351` = **0.302010228** (the "0.302"); area-weighted with the **step**: `0.3512 × 0.505092 × 1.7143` = **0.30409678051871997** vs joint area 0.42135 ⇒ ×1.3856 |
| bracket | `1/0.25146` = **3.976775630318937**; `1/0.43194` = **2.315136361531694**; `ln(0.43194/0.25146)` = **0.5410027585442313** |
| the `docs/46`:127 / `docs/51` §2.3 identity | `−ln(0.580685)` = **0.543546837831505** ≠ 0.5410027585442313 (gap 0.00254); `exp(−0.5410027585442313)` = **0.5821641894707599`. **The identity as written does not hold** — same defect the A3 agent reported. Files I do NOT own: REPORTED, not fixed. |
| `docs/47` C1 α bands | `11.8·144/299.5387088405831` = **5.6727225892675115**, `11.8·184/…` = **7.248478864064044** (adopted C); prior C: **6.831504040525872 – 8.72914405178306**. Gap to 7.92 = **0.6715211359359561** ⇒ **disjoint**, C1 confirmed by my own arithmetic |

## Decisions

1. **Band route: route 2, the station bootstrap.** Route 1 (G12's LOO range promoted to a band) is
   rejected on `docs/48` §3.2's two measurements — it is arithmetically degenerate (jackknife SE
   ≡ sd/√n = 0.6936 both ways; LOO range ≡ range/(n−1) = 0.8602) and it makes G12's own comparison
   circular, i.e. it would switch a FIRING guard off by widening what it is compared against.
   My own arithmetic reproduces both identities. Route 2 is also `docs/45` §4.2's **already
   registered** interval convention for every other quantity, so it is not a new registration.
2. **G12's 0.644 ln full width is kept as a standalone fragility threshold**, decoupled from the
   level band (`docs/48` §3.2; the brief's "G12's 0.644 ln fragility threshold is untouched").
3. **No corrected value for the class-C ×4.2/×2.9** — carried as O8. Three passes, three answers.
4. **No materiality bar is reconstructed** anywhere in either file I own. Stated explicitly in both.
5a. The **comparative sense** of the `k` sentence: with the verb *detectable* the correct
   comparative is **weaker** (a sink with |k| < k_min is invisible); "stronger … detectable" as
   printed in `docs/42` G1.2 / §9.4 / `docs/45` §2.3 is inverted. With the verb *excluded* the
   comparative is "stronger". A-P4 settles on the *detectable/weaker* form and says why.


## What I wrote — `docs/42` (AMENDMENT A-P4, new §9.7, file 903 -> 1150 lines, LF preserved)

Header: `## 9.7 — AMENDMENT A-P4 · 2026-08-12 · **σ_r's REUSE as a per-station residual sd is
RETIRED**; the level band and the `k` power restated`. Sub-blocks 9.7.1 defect · 9.7.2 survives/
retired BY NAME · 9.7.3 measurement + gates + my own reproductions · 9.7.4 the corrected `k`
sentence (registered reporting form) + provenance of the 0.0066-0.0069 interval + the comparative
ruling + what it means for SDR=1.0 · 9.7.5 EVERY published number that changes (21 rows, groups
A/B/C) · 9.7.6 what does NOT change + the "guard that fires by construction" caution · 9.7.7 the
F1 remedy discharged, site by site · 9.7.8 flags F1/F7/F8/F9 + P1/P2/O7/O8/O12/P5 · 9.7.9
disclosure.

In-place (strike-through + dated pointer, docs/37 A2.7 / docs/46 [WARN] patterns, nothing
deleted): §4.2's NOISE FLOOR blockquote · §4.2's power table (3 rows) + a WARN block · §4.2's
scale-reference paragraph · §6 G1.2's "neither fires" cell + WARN block (power figure only, NO
threshold touched) · §9's yardstick cell · §9's Amendments cell · §9.2's "keeps 0.00216" ·
§9.3's factor-6.9 paragraph · §9.4's "stronger than 3.54x" · §9.5's MANDATORY POINTER (0.0130
struck/withdrawn).

Caught and fixed by re-reading my own output: I first wrote `0.0065 - 0.0069` in four in-place
sites while A-P4 registers `0.0066 - 0.0069`. Normalised all four; the construction span
0.00657-0.00694 and both published roundings are printed in 9.7.4 so the two cannot be read as
two results. Table-column check on all 7 new tables: 0 mismatches.

## What I wrote — `docs/43` (new §7 amendment slot, file 396 -> 774 lines, LF preserved)

`## 7 — Amendment slot — **OPEN from 2026-08-12**` with slot rules, then:
1. §3.2's Π band REPLACED by the station bootstrap (+ route-2 justification, the mandatory 412
   sentence, G12 kept as a standalone 0.644 ln fragility threshold, the docs/45 §8 precedence
   rule, and "a struck band does not revert to ±38 % by default")
2. §1.4's ×0.502 is NOT eq. 14 (eq. 14 = the step, ×0.505092 area / ×0.522043 ero; `min(m,0.5)`
   may never be CITED) + joint/product = ×1.34762 restated to comply with the standing
   instruction + FOUR levers not three
3. the LS bracket 2.37×-3.00× -> 2.3151×-3.9768×, POINT vs documented HYBRID
4. the remaining σ_r-derived numbers (k row, ±28.8 %, class-C = O8 with NO value, the comparative)
5. §3.4's "These overlap" — disjoint at the adopted C (5.673-7.248 vs 7.92-8.86, gap 0.672)
6. §3.1 P1's 0.0096 mis-attribution (docs/42 F2), O7 CLOSED
7. §5.1's registered statement gains a MANDATORY rider (C2's *scoping* enacted; C2's 4.903/4.620
   NOT adopted — unverified by me, recorded as owed)
+ §7.1 open items (O8, O12, C2's repair, P1, P5, the docs/45 §8 half, §4's stale status, the
docs/46:127 identity) and §7.2 disclosure.

In-place in docs/43: §1.1 clause 2 · §1.2 lens-3 row · §1.4 item 1 · §1.5 · §2.1 LS-shape row ·
§3.1 P1 · §3.2 Π row · §3.2 k row · §3.2 class-C row · §3.4 bullet 2 · §5.1 (rider). Verified by
grep that every superseded string still exists inside its strike-through.

## Things I refused to do

- Did NOT offer a corrected class-C detectability number (O8). Three passes, three answers.
- Did NOT offer a σ-corrected CAL-13 or 22-pair `k_min` (no residual set / no reconstructible
  design). Did NOT print a naive σ-rescale of 0.00964, which would have been quotable.
- Did NOT create, rescale or imply a materiality bar anywhere; said so explicitly in both files.
- Did NOT quote a rescaled α anywhere, and did NOT touch docs/45, docs/46, docs/37 or docs/35.
- Did NOT adopt docs/47 C2's 4.903/4.620 (I could not verify them) — applied only the scoping fix.
- Did NOT correct docs/42:15/:299/:472's 6.83-8.73 (same C1 defect, but not a σ_r number and not
  in A-P4's scope): recorded as flag F7 instead of smuggling an unrelated enactment into A-P4.
- Did NOT fix docs/46:127 / docs/51 §2.3's broken identity — files I do not own; REPORTED.

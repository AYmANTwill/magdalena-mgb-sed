# journal — `defect-45-residual` (agent A6), 2026-08-12

**Assignment.** Two defects in the multi-agent documentation-repair run:
**defect 5** — `f_area(V4)`: *recompute it, then report the residual*; **defect 4** — `min(m, 0.5)`
mislabelled *"Buarque eq. 14"*: *verify and finish*.

**Files owned and written by this session:** `docs/37_c3_closure.md`, `docs/43_c3_c4_gate.md`, this
journal. **Nothing else.** No `git add` / `commit` / `push`. No engine default touched, no
`sim_calibrated_v2/` file touched, no data product regenerated or hand-edited, no fit / calibration
/ search / simulation run, no α̂ quoted, no materiality bar invoked or reconstructed (`docs/52`'s
striking respected). `docs/23` §13.2 yield embargo in force — no t/km²/yr anywhere in this pass.

**Orientation, in order:** `CLAUDE.md` → `docs/00_INDEX.md` (RULE 0) → `docs/46` §1.0, §1.1, §1.2,
§2.0, §2.2, §2.4, §3.1, §3.3, §3.5, §10 **amendment 2** → `docs/51` §9 **amendments 1 and 2** →
`docs/47` §3.1 R7 → `docs/37` §4 candidate 0 / A3.3 → `docs/43` §1.4 / §7. Working-tree state, not
git HEAD.

---

## 1 — DEFECT 5: `f_area(V4)` recomputed from scratch

### 1.1 What was measured and how

Script (scratchpad, wrote nothing into the repository):
`…/scratchpad/recompute_farea_v4.py`. Inputs read **read-only** and SHA-256'd **before and after**
— all eight **UNCHANGED**:

| file | sha256 |
|---|---|
| `data/processed/urh_ls2d_variants.csv` | `81d2376ac11978391612bfe39483113b321c327752392fba10e5d3e91471ddc0` |
| `data/processed/urh_ls2d.csv` | `8579c1281c1a992d2e76b3c8278ef3eba59e3bb8543fd38a9c01a0bd3c93f3c4` |
| `data/processed/minibacia_ls2d.csv` | `4c49b07bb92d54cbb3cb93ac1817373a182434c65cf47e535e5ebdd66dcd1724` |
| `data/processed/ls2d_variants_summary.json` | `2c18132533ac88b7a9e341a4b3394088d8f0fdff8ab246b9638ff948d4067981` |
| `data/processed/ls2d_defect_b.json` | `ea7d2a5d694686c901cdaafdbf74d6b3a4f82cf1f92f779f5481c8dfb66f92e0` |
| `data/processed/ls_defect_a.json` | `afdd53040edb8d10eaccf56d6903e70d1fee6b96e9f3287ac332bb09d6472a06` |
| `data/processed/urh_fractions.csv` | `916b42dee74bf12b4d4c7e3a30d3c174ff7758a55668b56a7afab1961f7565b9` |
| `data/processed/minibacias.csv` | `426a32df07def3d0c56b08bbc8867d0146e51f7a18c7165779f3c895c34e9f85` |

`f_ero(V4)` = **0.43194417543884817** (`ls_defect_a.json:variants.V4_buarque_2015.f_ero`), used as
the numerator of the R7 discriminator. It is **untouched by anything in this pass.**

**The engine support was not taken from the JSON on trust.** It was **rebuilt here** from
`urh_fractions.csv` melted to (mini, urh) × `minibacias.csv:area_km2` → per-unit
`cell_area_km2`, merged onto `urh_ls2d_variants.csv` (32,782 rows, **0 unmatched**), basin total
**257,096.93 km²**. It reproduces `ls_defect_a.json:f_area_urhfrac_areas` to **all 16 digits**.

### 1.2 THE FULL RECOMPUTATION TABLE

`R7` = **1.0251** (`docs/47` §3.1, *"Erosion-weighted / area-weighted = 1.0251 (continuous L) /
1.0278 (DG L): the proxy is 2.51 % low"*). Printed to four decimals ⇒ its true value lies in
**[1.02505, 1.02515]**; that interval is the honest resolution of the check.

| # | support / weighting | `f_area(V4)` | `f_ero/f_area` | \|d\| vs 1.0251 | in [1.02505, 1.02515]? |
|---|---|---:|---:|---:|---|
| 1 | **per-cell basin, 30,235,916 cells, 256,702.3554292511 km²** — recomputed as 16.775413430326214 / 39.812260149274394 from `ls2d_variants_summary.json`'s two `area_wtd_mean`s | **0.42136300143291305** | **1.025111777659529** | **1.1777659529199624e-05** | **YES** |
| 2 | same, as stored — `ls2d_variants_summary.json:variants.V4_buarque_2015.ratio_to_V0` | 0.42136300143291305 | 1.0251117777 | 1.178e-05 | YES |
| 3 | same, independent script — `ls2d_defect_b.json:decomposition.V4_over_V0` | 0.42136300143291344 | 1.0251117777 | 1.178e-05 | YES |
| 4 | same, recomposed from the 3 elevation strata (`strata_area_km2` × strata means) | 0.4213630014329133 | 1.0251117777 | 1.178e-05 | YES |
| 5 | `urh_ls2d_variants.csv` weighted by `n_cells` (29,647,948 cells) | 0.42136472954221804 | 1.0251075735 | 7.573e-06 | YES |
| 6 | `urh_ls2d_variants.csv` weighted by its own `area_km2` (32,782 rows, 251,723.50713639997 km²) | 0.4213519856784954 | 1.0251385780 | 3.858e-05 | YES |
| 7 | `urh_ls2d_variants.csv` weighted by `area_frac` *(not an area weight — the column sums to 8,672)* | 0.42161856467208547 | 1.0244904082 | 6.096e-04 | **NO** |
| 8 | **engine `urh_fractions.csv` × `minibacias.csv` areas, 32,782 units, 257,096.93 km² — REBUILT HERE, reproduces `ls_defect_a.json:f_area_urhfrac_areas` bitwise** | **0.4214751420286394** | **1.0248390293193077** | **2.609706806921963e-04** | **NO** |
| 9 | *(inadmissible, printed to exclude it)* unweighted mean of per-unit ratios | 1.412443933484921 | 0.3058133248 | 7.193e-01 | NO |
| 10 | *(inadmissible)* ratio of unweighted means | 0.4273873489571721 | 1.0106620528 | 1.444e-02 | NO |

**DG / lower-endpoint control** (the end the record says needs no correction — verified, it does
not): `f_ero(V4_dg)` 0.2514648985839397 / `f_area(V4_dg)` 0.2446790094097074 (`ls2d_defect_b.json:
decomposition.V4dg_over_V0`) = **1.0277338427624152** against R7's DG figure **1.0278**, |d| =
**6.615723758485181e-05**. ✅ already on the registered support.

### 1.3 VERDICT — with the arithmetic, not the convenience

**`f_area(V4)` = 0.42136300143291305.** Two independent grounds, in this order:

**(a) The definition selects the support, and it is decisive on its own.** `docs/46` §3.3 (frozen)
is the governing text:

> `f_area(V) = basin area-weighted mean of LS(V) / basin area-weighted mean of LS(V0)   [the PROXY]`

and `docs/46` §1 fixes what *"basin"* denotes in that sentence — *"Measured 2026-08-11 … on all
**30,235,916** basin cells at 90 m, with a harness that reproduces our own `ls2d_hs` area-weighted
mean **39.812** bitwise."* That is **row 1**: the per-cell DEM pass over 256,702.3554292511 km².
Rows 5 and 6 are *reconstructions* of the same quantity through the URH aggregation, which drops
URH slot 0 (251,723.51 km², 1.94 % of the basin excluded) — they land within 4.1e-06 / 2.6e-05 of
row 1, which is a consistency check on row 1, not a rival definition. **Row 8 is a different area
source**: `load_geometry`'s own URH-fraction areas, 257,096.93 km², about which `load_geometry`
itself warns that its two candidate sources *"differ by more than 5 % on 12.9 % of cells."*

**(b) R7 independently rules out row 8, and the arithmetic is:**

```
0.43194417543884817 / 0.42136300143291305 = 1.025111777659529     |d| = 1.1777659529199624e-05
0.43194417543884817 / 0.4214751420286394  = 1.0248390293193077    |d| = 2.609706806921963e-04
                                     ratio of the two distances   = 22.158110450144004
```

The corrected value is **22.16× closer** to R7. Sharper, because it does not depend on comparing two
distances: R7 is printed to four decimals, so its true value is in **[1.02505, 1.02515]**; row 1
**lies inside** that interval and row 8 **lies outside it**, at 5.2× the half-width of R7's own
rounding. **Row 8 is excluded by the check; row 1 is not.**

**What R7 CANNOT do, said plainly rather than glossed.** It cannot separate rows 1–6: they agree
with it to ≤ 3.9e-05, and row 5 (`n_cells`) is nominally the *closest* of all at 7.573e-06. **R7 is
therefore a discriminator against the engine support, not a selector among the per-cell
reconstructions.** The selector is the definition (ground (a)). Reporting it the other way round —
"the R7 check picks 0.42136300143291305" — would over-claim. Both files I edited say so explicitly.

**Row 8 is not an arithmetic error and no artifact needs editing.** It is a correctly computed
quantity on a legitimately different support, correctly self-documented in its own JSON key
(`f_area_urhfrac_areas`). This matches `docs/51` §9 amd 1's bitwise reconstruction, arrived at here
independently.

**Nothing moves.** `f_ero` is unchanged, and `docs/46` §3.3 ground **G-ii** registers that *"`f_ero`
decides; `f_area` is reported beside it, always, and can never override it."* Every erosion-weighted
statement — `f_LS ∈ [0.25146, 0.43194]`, `1/f_LS ∈ [2.3151, 3.9768]`, the POINT at
3.976775630318937×, the ln width 0.5410027585442313, the loads 129.3840 / 75.32347104056149 Mt/yr,
the 299.5387088405831 Mt/yr gate, joint/product ×1.347608646050708, `Δ_shape` = 0.1299456916752905
and Branch B, the four CITED grades, ADOPT-SOURCE — **stands exactly as frozen.** The LS level
remains **UNVALIDATED** (`docs/42` G4.2); this corrects a proxy's support and validates nothing.

### 1.4 Two independent confirmations found while auditing, not imported

- `docs/49`:154 already prints *"`f_ero(V4)` 0.43194 vs `f_area(V4)` **0.42136**"*, and
  `docs/50`:244,274 already print the area-proxy bracket as **×0.244679 – ×0.421363**. Both predate
  the amendment and were already on the registered support.
- `docs/53` §7 item 1 (2026-08-12) independently flagged the same inconsistency and reached the same
  direction — *"the on-disk value makes that check better, not worse"* — and correctly declined to
  fix files it did not own.

---

## 2 — DEFECT 4: the `min(m, 0.5)` / eq.-14 mislabel — five-site audit

**The distinction being enforced:** `min(m, 0.5)` is a **CAP** (variant **V2a**, ×0.502472 area /
×0.517480 ero) and is **nobody's published formulation** — it **may never be graded CITED**
(`docs/46` §2.2). Buarque **eq. 14**, printed **p. 47**, is a **STEP FUNCTION on slope PERCENT**
(variant **V2b**, ×0.505092 area / ×0.522043 ero): `m` = 0.2 / 0.3 / 0.4 / 0.5 on `Sf` < 1 / 1–3 /
3–5 / ≥ 5 %. **Different objects.**

| # | site | status | evidence (`file:line`, current working tree) |
|---|---|---|---|
| 1 | `docs/35` §9.3.1 | **FIXED** (not by me — `amend-35-label`) | `docs/35_qpeak_preregistration.md:733` the `m` row struck and both objects named; `:775-781` §9.3.2 item 1 relabelled with a [WARN] on *"stepped and capped"*; `:925`, `:944-947`, `:965-966` §9.4.1 carries the V2a/V2b table; `:480` the amendments row records it |
| 2 | **`docs/37` §4 candidate 0** | **FIXED** (not by me — the A3 enactment pass) | `docs/37_c3_closure.md:205` `m` row struck → A3.3.2; `:209-210` the interaction identity pointered; `:1182` A2.2's row carries the exact factors; `:1830` A3.3.1 item 12; **`:1853-1871` A3.3.2** is the full correction with both objects, both factors and the CITED verdicts; `:1873-1880` A3.3.3 records the four sites it did not own |
| 3 | `docs/43` §1.4 | **FIXED** (not by me — `amend-4243-piband`) | `docs/43_c3_c4_gate.md:96-97` struck in place; `:99-105` the amendment callout with the STEP factors; **`:524-572` Amendment 2** is the full correction incl. the standing instruction on products |
| 4 | `src/nbgen/make_nb18.py` | **FIXED** (not by me — the notebook track) | `:1241` the `m` row now reads *"his eq. 14, printed p. 47: a STEP FUNCTION … `Sf` in slope **percent**"*, factor **0.522043**; `:1248-1253` the dated correction blockquote; `:1352` `M_CAP_ERO, M_CAP_AREA = 0.517480, 0.502472  # min(m, 0.5): the CAP. NOBODY'S published form.`; `:1371`, `:1501`, `:2966` consistent |
| 5 | `src/nbgen/make_nb19.py` | **FIXED** (not by me — the notebook track) | `:2399-2404` the dated correction; `:2432-2433` `F_STEP_*` / `F_CAP_*` named separately with the *"NOBODY'S published form"* comment; `:2439`, `:2447`, `:2454`, `:2515`, `:2563` consistent |

**Generated notebooks also carry it:** `notebooks/18_musle_construction.ipynb:1882` and
`notebooks/19_c3_gate_and_c4_setup.ipynb:3511` contain the *correction* blockquote (the phrase
*"hard-capped at 0.5"* survives there only as the quoted, struck original — correct usage).

**Verdict: all five sites are clean. Nothing was owed to me on defect 4, and I changed nothing for
it.** I re-read each site in the working tree rather than trusting the run's status.

### 2.1 The docs/37 §4-candidate-0 figures the brief asked me to check specifically

Checked and **already correct — I imported nothing**:

- **the ×0.502 / ×0.421 figures at `:205`, `:207`** are struck with A3.3.2 / A3.3.1 pointers;
- **the superseded bracket ×0.333 – ×0.421 and "2.37× – 3.00×"** at `:190`, `:215-216`, `:248`,
  `:268-272`, `:293`, `:334`, **`:679-681`**, `:698-699`, `:702`, `:1013` are **all struck
  (`~~…~~`) with dated A3.3.1 pointers** — none is presented as live;
- **the re-derived readings I was given (2.3151× – 3.9768×, and 3.9767756303× at the adopted
  POINT)** were **verified in their owning sections before I relied on them**: `docs/37` A3.3.1's
  table at `:1791` registers `1/f_LS` = 2.3151× – 3.9768× and the point 3.976775630318937×, and
  A3.5.2 / A3.2 / A3.8:2241-2243 reproduce them. They are `docs/46` §1.0's registered numbers,
  erosion-weighted, and **`f_area`'s correction does not touch them**.
- the rounded string **×0.421** elsewhere in `docs/37` is the historic published proxy, already
  struck or pointered — and **0.42136300143291305 rounds to 0.421 at three significant figures**, so
  it is not additionally wrong. **Left exactly as it stands** (annotate, never over-correct).

---

## 3 — Defect 5: every live print, repo-wide, with disposition

**Method:** `grep -rn "0\.421475|0\.42147514|0\.42148|×0\.4214|1\.02484|1\.024839"` across `*.md`,
`*.py`, `*.ipynb`, `*.html`, `*.json`, `*.csv`, then read each hit in context to judge *live* vs
*inside a supersession/strike-through*. `progress_map.html`: **zero hits.**

| site (`file:line`) | what it prints | disposition |
|---|---|---|
| **`docs/37_c3_closure.md:207`** | §4 candidate 0 lever table, joint row: `f_area` **0.421475**, presented as A3.3.1's *current* correction | **FIXED-THIS-RUN** |
| **`docs/37_c3_closure.md:1790`** | A3.3.1 replacement table, upper-end row: `×0.421475 area`, presented as *registered* | **FIXED-THIS-RUN** |
| **`docs/43_c3_c4_gate.md:586`** | Amendment 3's REGISTERED blockquote: area-weighted proxy `[0.24468, 0.42148]` | **FIXED-THIS-RUN** |
| `docs/46_ls_preregistration.md:105, 109, 271, 617, 717, 1037` | ×0.42148 / 0.421475 / ×1.02484 in **§1.0, §2.2, §2.5, §3.1, §6.2** | **RESIDUAL-NOT-MINE — and correctly already handled.** `docs/46` §1–§9 are **FROZEN**; the *only* remedy is its **§10 amendment slot**, which has been used (**amendment 2**, 2026-08-12, lists all five cells). Body strings stay as frozen by design. **No further action is owed.** |
| `docs/51_ls_freeze_decision.md:19, 135, 141, 167` | ×0.42148 / 0.42147514 in §1, §2.1, §2.2 | **RESIDUAL-NOT-MINE — already handled.** All four are struck in place (`~~…~~`) with pointers to **§9 amendment 1**. **No further action owed.** |
| `docs/47_c4_entry_verdict.md:338` and its §4.3 area column | prints **×0.4214** at `:338` and **0.42135** in the §4.3 area column (and **0.24466** in the DG cell) | **RESIDUAL-NOT-MINE.** `:338`'s `×0.4214` is a 4-s.f. print and is a correct rounding of 0.42136300143291305 — **harmless**. The §4.3 column is a **third support** (the `urh_ls2d_variants.csv` `area_km2` weighting, 0.4213519856784954 → 0.42135, and 0.2446790094097074 → 0.24468 ≠ 0.24466). **Remedy: a dated correction by `docs/47`'s owner**, or a support tag on the column. Changes no `docs/47` verdict — all three propositions are erosion-side. |
| `docs/52_materiality_bar_decision.md:371` | §6's (R12) row prints **×1.02484 (upper)** | **RESIDUAL-NOT-MINE.** Restate to **×1.025111777659529**. Owed to `docs/52`'s owner. `docs/52` §5:78 and §5:343's abs-ln register **0.0248 / 0.0273 is already right** on the registered support and **must not be touched** (the engine support would give 0.0245). |
| `docs/35_qpeak_preregistration.md:850, 1021` | §9.4's prose prints **×1.02484** at the hybrid end, live, as measured | **RESIDUAL-NOT-MINE.** Restate to **×1.025111777659529**. `docs/35` §9 is an open amendment slot (§9.4 already used), so the remedy is a dated line there. Note both sites already say the `f_area` **values** are carried *by reference* to `docs/46` — only the derived ratio is hard-coded and stale. |
| `docs/53_delta_shape_pretest.md:363-364` | §7 item 1 prints 0.42147514 / 1.024839 | **NOT A DEFECT — no action.** It is the *report of* the inconsistency, correctly attributed, with the corrected 1.025112 printed beside it. |
| `docs/50_defect_b_resolution.md:299` | `×0.4214 / ×0.43194` | **NOT A DEFECT** — 4-s.f. print, correct rounding of the registered value. |
| `src/mgb_sediment.py:223` | module docstring: *"area-weighted proxy [0.24468, 0.42148], measured 2.5 % low"* | **RESIDUAL-NOT-MINE** (read-only to me). Restate the upper end to **0.42136300143291305**. Owed to the engine/verification track. **Documentation only — no code path reads it**, and the erosion-weighted bracket in the same docstring is right. |
| `src/nbgen/make_nb18.py:1244, 1269, 1353` | `0.421475` in a markdown table, in prose (*"0.304112 vs 0.421475, ×1.38592"*), and in the code constant `F_HYB_AREA` | **RESIDUAL-NOT-MINE.** Owed to the notebook/verification track. **:1269 needs care** — the ×1.38592 there is the *area-weighted* joint/product and is recomputed from `0.421475`; on the registered support it becomes `0.42136300143291305 / 0.304112`. Whoever fixes it must recompute, not retype. |
| `src/nbgen/make_nb19.py:2435` | code constant `F_HYB_A = 0.421475` | **RESIDUAL-NOT-MINE.** Same owner. |
| `notebooks/18_…ipynb:1877, 1902, 2015, 2026, 2066` · `notebooks/19_…ipynb:3562, 3586, 3633` | the same value in generated markdown, in **code cells** and in **executed output** | **RESIDUAL-NOT-MINE.** These are generated: fix the two generators, rerun `make_nb18.py` / `make_nb19.py`, then re-execute with `python -m nbconvert`. Executed output cannot be hand-edited honestly. |
| `data/processed/ls_defect_a.json:28` | `"f_area_urhfrac_areas": 0.4214751420286394` | **CORRECT — DO NOT EDIT.** Self-documenting key on a legitimately different support; reproduced bitwise here. |
| `scripts/c3/ls_erosion_weights.py:174` | GATE-2 console table prints a bare `f_area` header, **no support tag**, on the `geom.cell_area_km2` (engine URH-fraction) value | **RESIDUAL-NOT-MINE — and it is the root cause.** This console line is the plausible channel by which 0.42147514 entered the corpus as *"`f_area(V4)`"*. **Remedy: one word** (`f_area_urhfrac`), or print `docs/46` §3.3's per-cell value alongside. Owed to `scripts/c3/`'s owner. |
| `data/processed/{minibacia_ls2d_variants,urh_ls2d_variants,peakgap/events,sim_baseline/…}.csv` | substring hits on `1.024848`, `1.0248403`, … | **FALSE POSITIVES** — unrelated per-row data. No action. |

---

## 4 — The exact edits I made

### `docs/37_c3_closure.md` (3 edits)

1. **`:207`** — §4 candidate 0's lever table, joint row. `f_area` **0.421475** →
   `` `f_area` ~~**0.421475**~~ → **0.42136300143291305** (**A3.3.4**, 2026-08-12; owning records
   `docs/46` §10 amd 2 / `docs/51` §9 amd 1) ``. Original preserved struck; the `~~**0.421**~~ →
   **A3.3.1**` prefix untouched.
2. **`:1790`** — A3.3.1's replacement table, upper-end row. `×0.421475 area` →
   `` ~~×0.421475~~ → **×0.42136300143291305** area (**A3.3.4**, 2026-08-12 — `0.421475` was the
   *engine URH-fraction* area support, not §3.3's) ``.
3. **New subsection `A3.3.4`**, inserted after A3.3.3 and before A3.4. Contains: the owning-record
   pointers; the statement that the numbers were **recomputed here, not imported**; the site list;
   the §3.3 + §1 definitional argument; the **full seven-row support table** with `f_ero/f_area` and
   the R7 rounding-interval column; the R7 arithmetic at full precision with the 22.158110450144004×
   distance ratio; an explicit paragraph on **what R7 cannot decide**; what 0.421475 actually is and
   why no artifact needs editing; a **"not corrected, because already right"** list (DG endpoint with
   its 1.0277338427624152 control, every erosion-weighted number, the 1.0277138223121463 proxy-bias
   prints at :264/:1392/:1812/A3.8, and the rounded ×0.421 strings); a runnable `python3.10 -c`
   reproduction with its expected output; a disclosure block; and the residual register.

### `docs/43_c3_c4_gate.md` (4 edits)

1. **`:586`** (now `:592-596`) — Amendment 3's REGISTERED blockquote. `[0.24468, 0.42148]` →
   `` ~~[0.24468, 0.42148]~~ → **[0.2446790094097074, 0.42136300143291305]** `` with the
   dated amendment-8 pointer and the owning records. *"2.51 % low"* **kept** — it is R7's own
   shorthand for ×1.0251 and remains right at ×1.025112.
2. **§7 preamble** — a dated *"Slot addendum"* blockquote recording that the pass's own *"Seven
   amendments"* count is left as written and an **eighth** was appended the same day by a different
   session, changing no registered statement, threshold or decision.
3. **New `Amendment 8`**, appended after Amendment 7 and before §7.1: the owning records; the
   explicit statement that nothing registered moves and why (ground G-ii); the recompute-don't-adopt
   disclosure; the §3.3 definitional argument; the **seven-row support table** with the R7
   rounding-interval column; the honest statement of what R7 can and cannot separate; what 0.42148
   is; the DG control; a *"checked and already correct, so nothing was over-corrected"* list; and a
   full disclosure block.
4. **§7.1** — the existing `docs/46`:127 / `docs/51` §2.3 identity row **annotated as SETTLED** by
   `docs/46` §10 amd 2 (iii) / `docs/51` §9 amd 2 (it mixed the erosion and area supports:
   erosion-weighted `0.5410027585442313 = −ln 0.5821641894707599`; area-weighted
   `0.5435475125003637 = −ln 0.580684608230046`), plus **two new rows**: the repo-wide `f_area(V4)`
   residual register, and `scripts/c3/ls_erosion_weights.py`:174's untagged header.

**Nothing was deleted from either file.** Every superseded string survives inside `~~…~~` with a
dated pointer to the amendment that replaces it and to the document that **owns** the fact.

---

## 5 — Things I refused to do

- **I did not adopt either circulating value from a document.** Both were recomputed from the CSVs
  and JSONs, and the engine support was rebuilt from `urh_fractions.csv` × `minibacias.csv` rather
  than read out of `ls_defect_a.json`.
- **I did not claim R7 selects the answer.** It excludes the engine support and cannot separate the
  five near-neighbours; the *definition* selects. Both edited files say so.
- **I did not touch `docs/46`, `docs/51`, `docs/45`, `docs/35`, `docs/47`, `docs/52`, `docs/53`,
  `docs/30`, `docs/00_INDEX.md`, the notebooks, either nbgen generator, `src/mgb_sediment.py`,
  `scripts/c3/` or any data product** — read only, residuals recorded.
- **I did not re-derive the ADR / Leg-A / α numbers** that the struck sentences carried. `docs/37`
  A1.9 withdrew the residual's direction and `docs/46` §4.3 forbids the anchors as evidence in the
  LS decision; re-deriving them would smuggle back a retired argument.
- **I did not touch the rounded `×0.421` / `×0.4214` strings** that are correct roundings of the
  corrected value. Over-correcting is as much a defect as under-correcting.

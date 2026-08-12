# Journal - agent slug `defect-farea-amend`

Task: T2a - the `f_area(V4)` numeric disagreement, plus the
`ln(0.43194/0.25146) = 0.5410 = -ln 0.580685` identity defect in docs/46 §1.0 and docs/51 §2.3.

OWNS (write): `docs/51_ls_freeze_decision.md`; `docs/46_ls_preregistration.md` §10 ONLY
(append a new dated amendment after "Amendment 1"); this journal. NOTHING ELSE.

Started 2026-08-12.

## 0. Plan
1. Read CLAUDE.md, docs/00_INDEX.md, docs/47, docs/46 (§1.0 §1.2 §2.0 §3.1 §3.3 §4.2-4.4 §5 §6 §7.3 §9 §10),
   docs/51, docs/52, docs/53. Then docs/37 A3, docs/35 §6.1/§9, docs/50, scripts/c3/ls2d_variants.py,
   scripts/c3/ls2d_defect_b.py, the two JSONs, urh_ls2d_variants.csv (READ ONLY).
2. Recompute f_area(V4) under every defensible weighting at full precision.
3. Try to reconstruct 0.42147514.
4. Check proxy-bias consistency against docs/47 §3.1 R7's 1.0251 (and 1.0278 for the DG endpoint).
5. Amend docs/51 (new amendment slot + strike-through at §2.2) and docs/46 §10.
6. Report what is owed to other owners (docs/47 §4.3's 0.42135; the JSONs / producing scripts).

## 1. Reading log

- [read] CLAUDE.md, docs/00_INDEX.md, docs/51 (full, 509 lines), docs/46 §0/§1/§1.0/§2/§2.0/§2.0.1/§3.1/§3.2/§3.3/§3.4/§3.5.
- [read] docs/46 §3.3 registered definition, verbatim:
    `f_area(V) = basin area-weighted mean of LS(V) / basin area-weighted mean of LS(V0)   [the PROXY]`
  and §1's read-out is explicit that the area-weighted means (39.812 for V0) were
  "Measured 2026-08-11 ... on all **30,235,916** basin cells at 90 m". So "basin
  area-weighted mean" = the PER-CELL basin mean, not a URH-aggregated mean.
- [read] `docs/agents/journal_c31-enactment.md`:35-39 -- a PARALLEL/EARLIER agent already
  diagnosed this same flag and reached: two different area supports, not an error:
  `ls2d_variants_summary.json:ratio_to_V0` over the 30,235,916 basin DEM cells
  (0.42136300143291305); `ls_defect_a.json:f_area_urhfrac_areas` over the 32,782 engine URH
  cells (0.4214751420286394); relative gap 2.661377e-04; and "docs/46 §3.3's literal
  definition of f_area is the basin-cell one". I must REPRODUCE this myself, not carry it.
  NOTE the file it names is `ls_defect_a.json` (Defect A's artifact), NOT `ls2d_defect_b.json`.
- Next: docs/47 §3.1 R7 + §4.3, docs/52 §5, docs/53's flag, the JSONs, the producing scripts.

## 2 — MEASUREMENT (all read-only; nothing written to data/ or scripts/)

Harnesses (scratchpad only):
`…/scratchpad/farea.py` · `…/scratchpad/farea_engine.py` · `…/scratchpad/arith.py`
`urh_ls2d_variants.csv` sha256 read before use: `81d2376ac11978391612bfe39483113b321c327752392fba10e5d3e91471ddc0`
`farea_engine.py` re-hashed `urh_ls2d.csv`, `urh_ls2d_variants.csv`, `minibacia_ls2d.csv`,
`sim_calibrated_v2/h2e_drivers.npz` before and after: **protected unchanged: True**.

### 2.1 f_area(V4) under every defensible weighting

| support / weighting | f_area(V4) at full precision |
|---|---|
| **per-cell basin, 30,235,916 cells, 256,702.3554292511 km²** (`ls2d_variants_summary.json:ratio_to_V0`) | **0.42136300143291305** |
| same, via `ls2d_defect_b.json:decomposition.V4_over_V0` (independent script) | 0.42136300143291344 (rel 9.2e-16) |
| `urh_ls2d_variants.csv` weighted by its own `area_km2` (32,782 rows, 251,723.50713639997 km²) | 0.4213519856784954 (rel −2.61e-5 vs registered) |
| `urh_ls2d_variants.csv` weighted by `n_cells` | 0.42136472954221804 (rel +4.1e-6) |
| `urh_ls2d_variants.csv` weighted by `area_frac` | 0.42161856467208547 (rel +6.07e-4) |
| **engine `urh_fractions.csv`×`minibacias.csv` areas, 32,782 units, 257,096.93 km²** (`ls_defect_a.json:f_area_urhfrac_areas`) | **0.4214751420286394** (rel **+2.661377371648382e-4**) |
| *(not defensible, printed to exclude it)* unweighted mean of per-unit ratios | 1.412443933484921 |
| *(not defensible)* ratio of unweighted means | 0.4273873489571721 |

- Elevation-strata area-weighted recomposition from the published per-cell means reproduces the
  registered value: Σa·V4 / Σa·V0 over {lowland, mid, Andean} = **0.4213630014329133**.
- The `urh_area_wtd_level` 1.01852 flag EXPLAINED: `ls2d_variants.py:432` builds the URH table
  from `N[:, 1:]` — **URH slot 0 is dropped**. Excluded area = 256702.3554292511 − 251723.50713639997
  = **4978.848292851122 km² (1.9395 %)**, whose implied LS(V0) is **2.5297232536233145** (against a
  basin 39.812) — near-zero-LS water/no-URH area. Dropping it lifts BOTH numerator and denominator
  levels by essentially the same factor (V0 ×1.0185222500348001, V4 ×1.0184956226590285), so the
  RATIO survives to **0.9999738568541133** of the per-cell one. **The 1.01852 level offset does NOT
  propagate into f_area; it very nearly cancels.** So the URH file CAN reproduce the per-cell basin
  ratio, to 2.6e-5, even though it cannot reproduce the per-cell basin LEVEL.

### 2.2 RECONSTRUCTION OF 0.42147514 — SUCCEEDED, BITWISE

`farea_engine.py` reproduced **every** `ls_defect_a.json:f_area_urhfrac_areas` value exactly
(`match=True` on all 8 variants, V4 = 0.4214751420286394). It is
`scripts/c3/ls_erosion_weights.py:166`'s
`float(np.sum(a * j[c]) / np.sum(a * v0))` with `a = geom.cell_area_km2` from
`sed.load_geometry` — i.e. the **engine's `urh_fractions.csv` × `minibacias.csv` areas**
(basin total 257,096.93 km²), NOT the per-cell DEM areas §3.3 names. `load_geometry` itself
warns that the two area sources differ >5 % on 12.9 % of cells (totals 257,097 vs 251,724 km²).
So 0.42147514 is a **legitimate quantity on a different support**, not an arithmetic error —
but it is **not `f_area` as `docs/46` §3.3 defines it**.
Candidates that FAILED to reconstruct it (printed so the search is auditable):
16.775413430326214/39.812 = 0.42136575480574234 · 16.775/39.812 = 0.4213553702401286 ·
16.7754/39.8123 = 0.42136224232209646 · f_ero/1.0251 = 0.42136784258984317. Only
`f_ero(V4)/1.02484 = 0.4214747428270249` comes close, and that is circular (1.02484 was itself
computed FROM 0.42147514).

### 2.3 THE DECIDING CONSISTENCY CHECK — docs/47 §3.1 R7's independently measured 1.0251

| f_area used | f_ero/f_area | |diff| vs R7's 1.0251 |
|---|---|---|
| **per-cell basin 0.42136300143291305** | **1.025111777659529** | **1.1777659529199624e-05** |
| engine 0.4214751420286394 | 1.0248390293193077 | 2.609706806921963e-04 |
| urh-csv area_km2 0.4213519856784954 | 1.0251385780069278 | 3.857800692785851e-05 |

**R7 confirms the per-cell value, 22× better than the engine one.** DG endpoint:
f_ero 0.2514648985839397 / f_area 0.2446790094097074 = **1.0277338427624152** (with the rounded
f_ero 0.25146: 1.0277138223121467) against R7's 1.0278 — |diff| 6.6e-5. The DG endpoint's f_area
is ALREADY the per-cell one (`ls2d_defect_b.json`, 30,235,916 cells), so **only the UPPER endpoint
was quoted off-support. The bracket's two ends were printed on two different supports.**

### 2.4 A THIRD, INDEPENDENT INTERNAL VOTE FOR THE PER-CELL VALUE
`docs/46` §2.0.1:374 and `docs/52` §5:343 both print **(R12) 0.0248 / 0.0273**. Measured:
|ln f_ero − ln f_area| = **0.024801658019852884** on the per-cell support (rounds to 0.0248)
but **0.024535555691053368** on the engine support (rounds to 0.0245). And the DG |ln| =
0.027336745312405174 (rounded f_ero) → 0.0273. **So docs/46's own |ln| register is already on
the per-cell support** — it is the ×1.02484 *ratio* form at §2.2:271 / §2.5:617 that is off.
`docs/49`:154 (0.42136, |ln| 0.0248) and `docs/50`:244 (×0.244679 – ×0.421363) are also already
right. `docs/48`:438 (1.0251 / 0.0248) is right.

### 2.5 VERDICT ON T2a
**f_area(V4) = 0.42136300143291305**, defined as `docs/46` §3.3's basin **area-weighted mean over
the 30,235,916 basin DEM cells at 90 m** (the same support and the same harness whose V0 gate
reproduces the published 39.812 → 39.812260149274394). 0.42147514 is reconstructible and correct
on the engine-URH-area support; it is not §3.3's quantity.

## 3 — THE SECOND DEFECT: the `= −ln 0.580685` identity — DIAGNOSED COMPLETELY

Re-verified from scratch (`arith.py` §5):

| quantity | value |
|---|---|
| `ln(0.43194 / 0.25146)` | **0.5410027585442313** |
| `−ln(0.580685)` | **0.543546837831505** |
| gap | **0.0025440792872737372 ln** |
| `exp(−0.5410027585442313)` | **0.5821641894707599** ⇒ 0.5410 pairs with **0.58216**, not 0.580685 |
| `0.43194/0.25146` | 1.7177284657599616 |

**The diagnosis is sharper than "two different quantities that happen to be close" — it is a
SUPPORT MIX.** Both spans exist and both are correct on their own weighting:

| span | value | its `L`-form ratio | reproduced |
|---|---|---|---|
| **erosion-weighted** `ln(f_ero(V4)/f_ero(V4_dg))` | 0.5410027585442313 (rounded inputs) · **0.540992944828321** (exact 0.43194417543884817 / 0.2514648985839397) | **0.5821641894707599** (rounded) · 0.5821699026927624 (exact) | `docs/agents/journal_ls-impact.md`:105 measured it independently: *"INSIDE the source formulation the DG/continuous ratio is 0.5807 area-wtd / **0.5822 erosion-wtd**"* |
| **area-weighted** `ln(f_area(V4)/f_area(V4_dg))` | **0.5435475125003637** (0.42136300143291305 / 0.2446790094097074) | **0.580684608230046** | `ls2d_defect_b.json:decomposition.L_form_inside_source` = 0.5806846082300454, `ln_decomposition` −0.5435475125003647; `docs/50`:275 prints the AREA row's ln width as **0.54355** — correctly |

So `−ln 0.580685 = 0.543547` is the **AREA-weighted** span and `0.5410` is the **EROSION-weighted**
span. `docs/46` §1.0 and `docs/51` §2.3 took `docs/50`'s area-side `L`-form ratio (0.580685) and set
it equal to the erosion-side span (0.5410). **The written identity is false; each constituent is
true on its own support.** The erosion-weighted `L`-form ratio inside the source formulation is
**0.58216** (= `exp(−0.5410027585442313)`), independently measured at 0.5822 by `ls-impact`.

Licence (`docs/46` §2.0 ground **G-iv** — the exact ratio printed at full precision, with a stated
licence, never compared to a threshold): the gap is **0.0025440792872737372 ln**, i.e. the two
spans differ by a factor **1.0025473** — and the licence it carries is *nothing*, because **no
decision rule in force reads either span**. §1.0 registers the span as the label of the `L`-form
lever, not as an input; §3.3's precedence (ground G-ii) makes `f_area` unable to override `f_ero`
in any case; §4.2's decision rule reads source text and grades (ground G-i); §6.1's discriminator
reads `Δ_shape`, which is erosion-based and per-station and uses neither span. `docs/46` §2.0.1
row 2 already labels the width BAR-DEPENDENT-and-superseded. **No verdict moves. That is a
measurement, not a tolerance — I introduce no bar and reconstruct none.**

## 4 — WHAT MOVES, WHAT DOES NOT (the downstream sweep)

Moves (all are *reporting-precision* restatements of a reported diagnostic):
- `docs/51` §1 box, §2.1, §2.2: ×0.42148 → **×0.42136300143291305**; `0.43194418/0.42147514 =
  1.024839` → **0.43194417543884817/0.42136300143291305 = 1.025111777659529**.
- `docs/51` §2.3: the identity, corrected as §3 above.
- `docs/46` §1.0's ×0.42148 (twice), §3.1's V4 `f_area` cell 0.421475, §6.2's ×0.42148 (:1037),
  §2.2:271 / §2.5:617's ×1.02484 → recorded in my §10 amendment; §1–§9 not touched.
- **1/f_area upper end**: 1/0.42136300143291305 = **2.3732506095678505** (was 1/0.4214751420286394
  = 2.3726191660718383). Nobody prints the area-proxy 1/f in docs/46 or docs/51; `docs/50`:274-275
  prints 2.373 and is already right.

Does NOT move (measured, not assumed):
- `f_ero` anywhere — 0.43194417543884817 and 0.2514648985839397 are untouched. The **registered
  bracket [0.25146, 0.43194] erosion-weighted, 1/f 2.3151–3.9768, and every α rescaling
  (11.8·f = 2.967–5.097; 35.4·f = 8.902–15.291; the docs/45 box ·f) are all erosion-weighted and
  UNAFFECTED.**
- basin loads 129.3840 / 75.3235 Mt/yr and the 299.5387088405831 Mt/yr gate — engine re-runs.
- `Δ_shape` = 0.1299456916752905 and Branch B — per-station erosion ratios, no `f_area`.
- The four CITED evidence grades and the ADOPT-SOURCE outcome — decided by source text (G-i).
- `docs/46` §2.0.1's and `docs/52` §5's **|ln| register 0.0248 / 0.0273 — already correct**; those
  rows need NO restatement. Only the ×1.02484 *ratio* form needs it (§2.2:271, §2.5:617,
  `docs/52` §6:371).
- `docs/47`'s `C4.3-BLOCKED-UNTIL-LS-LANDS` — three width-independent propositions.
- The joint/product ×1.34762 standing instruction and the erosion-weighted lever product.

## 5 — Decisions taken before writing
1. The registered value is the **per-cell basin** one. Grounds: §3.3's own words *"basin
   area-weighted mean"*; §1's read-out declaring the measurement to be *"on all 30,235,916 basin
   cells"* with V0 = 39.812; the harness's V0 gate being that same number; and R7's independently
   measured 1.0251 (§2.3). Four independent grounds, one direction.
2. **Do NOT hand-edit the JSONs and do NOT regenerate.** Both are correct for what they compute
   and `ls_defect_a.json`'s key even self-documents its support (`f_area_urhfrac_areas`).
3. Report `docs/47` §4.3's 0.42135 and `docs/52` §6:371's ×1.02484 as **owed to their owners**.
4. Report the one real code-level defect: `scripts/c3/ls_erosion_weights.py`:174's GATE-2 table
   header prints the column as bare `f_area` with no support tag, which is the channel by which
   the engine-support number entered `docs/51` §2.2 as *"f_area(V4)"*. Documentary/one-word fix;
   I do not own `scripts/` and did not touch it.

## 6 — WRITES MADE (2026-08-12)

`docs/51_ls_freeze_decision.md` — 533 -> 761 lines, LF throughout (was LF; unchanged).
  * strike-through + dated pointer at FOUR body sites, nothing deleted:
    :19 (§1 four-answers box), :135 (§2.1 replacement statement), :141 (§2.1 table row),
    :167 (§2.2 cross-check) and :190 (§2.3's `-ln 0.5807` bullet). Two inline
    `> **⚠ AMENDMENT n, 2026-08-12 ...**` blocks added at :169-177 and :192-203.
  * NEW `## 9 — Amendment slot — OPEN from 2026-08-12` (:537) with
    `### Amendment 1` (:545, the f_area support correction) and
    `### Amendment 2` (:691, the ln identity) and `### 9.1 Disclosure` (:739).
`docs/46_ls_preregistration.md` — 1399 -> 1585 lines. §1-§9 verified BYTE-IDENTICAL
  (`cur2.startswith(cur)` == True before the one later table-header word fix inside my own
  amendment). Only `## 10` grew: `### Amendment 2 — 2026-08-12` appended after Amendment 1 and
  after the slot's own "further amendments go below this line" instruction.
`docs/agents/journal_defect-farea-amend.md` — this file.
NOTHING ELSE WAS WRITTEN. No git command. No script run that writes. No JSON edited.
Markdown table column-consistency checked programmatically on both files: the only inconsistent
blocks in docs/51 are the THREE PRE-EXISTING ones at :139-148, :228-234, :255-261, which carry
unescaped `|ln|` inside code spans in rows I did not author (line 141's `|ln|` was already there).
Every table I added is column-consistent.

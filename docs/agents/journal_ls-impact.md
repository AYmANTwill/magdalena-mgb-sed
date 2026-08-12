# Journal — ls-impact

**Agent slug:** `ls-impact`
**Started:** 2026-08-11
**Goal:** Quantify BY MEASUREMENT what the LS bracket (×0.333 – ×0.421, `docs/37` §4 candidate 0
/ A1.5) does to every downstream number. Do NOT change the adopted LS. Scratch files in the
system temp dir only.

## Discipline binding me
- Measure, do not assert. Every ratio reported here is produced by running code in this repo.
- Do not modify adopted config: `ls2d_hs`, `cited_central_2026_08_11`, `williams_m3`,
  `us_customary`, H2E drivers. Read-only.
- No git commands.

## Checklist
- [ ] 0. Orient: CLAUDE.md, docs/00_INDEX, docs/37 §171–210 + §590–610, src/mgb_sediment.py,
      scripts/c3/ls2d.py
- [ ] a. Erosion-weighted LS ratio, measured (re-run engine on a source-method LS field)
- [ ] b. Basin gross hillslope erosion at adopted LS and both bracket endpoints
- [ ] c. Position vs 144–184 Mt/yr outlet anchor, with the not-the-same-quantity caveat
- [ ] d. Alpha absorption arithmetic
- [ ] e. Separability of LS bracket from C revision and unit factors (docs/42 §3.1)

## Log

### Step 0 — orientation (2026-08-11)
Read CLAUDE.md, docs/00_INDEX.md §1–§3, docs/37 lines 160–215 (candidate 0 table: levers
0.351 / 0.502 / 1.714, joint 0.421, DG96 further ×0.790 → bracket 0.333–0.421) and 580–615
(A1.4: at adopted C, bracket gives 99.8–126.1 Mt/yr), `src/mgb_sediment.py`
(LS2D_AGGREGATION_FACTORS / LS2D_RESOLUTION_FACTORS both 1.000 adopted; `effective_ls2d` =
`cell_ls2d * ls2d_factor`, LINEAR), `scripts/c3/ls2d.py` docstring, and
`docs/agents/journal_decide-ls-resolution.md` §1a/§3b (the source of the bracket; harness was
`scratchpad/ls_formulation.py`, written outside the repo — likely gone).

Key facts fixed before measuring:
- `data/processed/urh_ls2d.csv` carries columns: mini, urh, n_cells, area_km2, area_frac,
  ls2d, ls2d_hs, ls2d_mb86, ls2d_dg96. There is NO source-method (Buarque) column, so item (a)
  cannot be done by column swap; the field must be rebuilt from the DEM and aggregated the same
  area-weighted way, or the erosion-weighted ratio approximated from an available column pair.
- The engine is exactly linear in LS (`cell_static_factor`), so a UNIFORM scale factor is
  algebraically identical to scaling the basin total. The whole point of (a) is that 0.421 is
  NOT uniform — it is a field replacement.

### Step 1 — harness (2026-08-11 20:40)

The prior agent's `scratchpad/ls_formulation.py` survived in this session's scratchpad, so the
0.421 row is reproducible rather than merely quoted. I extended it into
`scratchpad/ls_field_agg.py`, which does the same 30.2 M-cell pass but ALSO accumulates the
area-weighted mean per (minibacia, URH) key exactly as `scripts/c3/ls2d.py` does, and writes
`urh_ls2d_srcmethod.csv` in the same long layout as `data/processed/urh_ls2d.csv`. That column
can then be swapped into `SedGeometry.cell_ls2d` and the engine RE-RUN, which is what turns
docs/37 line 206's stated proxy into a measurement.

Two additions beyond the prior harness:
- `buarque_dg`: the literal Desmet-Govers finite-difference L (Buarque eq. 13) under the same
  one-pixel length limiter and the same stepped m / W&S S. docs/37's lower bracket endpoint
  0.333 was obtained by multiplying the joint 0.421 by an INHERITED x0.790 (the dg96/primary
  ratio measured on the UNCAPPED ls2d in `journal_c31-ls2d.md`). Measuring the DG form inside
  the source formulation replaces that inheritance too.
- per (mini, urh) accumulators, so the field is engine-consumable.

Validation designed in before running: my re-derived `ours_hs` column must reproduce the
committed `urh_ls2d.csv:ls2d_hs` cell by cell. If it does not, nothing else in this run counts.

`scratchpad/ls_impact_engine.py` then does: adopted run (gate 299.5387) -> run per LS field ->
erosion-weighted ratios -> uniform-scalar linearity control -> per-station erosion-weighted LS
ratio over the 18 C1-usable stations (docs/42 §4.1 machinery, reused from `scratchpad/shares.py`)
-> erosion-weighted percentiles of the per-cell LS ratio.

### Step 2 — RESULTS (2026-08-11 20:50–21:10). Everything below is measured.

**Harness validated first, before any result was read.**
`scratchpad/ls_field_agg.py` reproduces the prior agent's basin area-weighted ratios
BIT-FOR-BIT: `cap_m05` 0.5024723913028578, `s_ws78` 1.7138857311825018, `Lcap_pixel`
0.3512626372660478, **`buarque_exact` 0.42136300143291344** (docs/37's ×0.421). Its
per-(mini,URH) aggregation reproduces the committed `urh_ls2d.csv:ls2d_hs` to max rel diff
**4.97e-6** (median 6.05e-7) — that is the CSV's own 6-significant-figure rounding, not a
method difference. Re-running the engine on my re-derived `ours_hs` column returns
**299.53867** against the adopted **299.538709** Mt/yr (1.3e-7 relative). Station machinery
reproduces docs/42 §4.1's up-areas exactly (68 / 178 / 152 / 289 / 611 / 748 / 833 / 1,645 /
1,600 / 1,711 / 2,411 / 723 / 6,362 / 5,487 / 6,380 / 24,665 / 30,848 / 54,035 km²).
Adopted-run gate `|total − 299.5387| < 1e-3`: **PASS**.

**(a) THE PRECISION CAVEAT, SETTLED.** docs/37 line 206 is right that ×0.421 is an
area-weighted proxy, and the measurement says the proxy is **2.5 % low**, in the direction
that makes the model slightly less under-anchored than stated:

| LS field (90 m, same grid, same aggregation) | basin Mt/yr | erosion-wtd × | area-wtd × |
|---|---:|---:|---:|
| adopted `ls2d_hs` | 299.5387 | 1.0000 | 1.0000 |
| + m capped at 0.5 | 155.0053 | 0.5175 | 0.5023 |
| + S = W&S 1978 | 507.4346 | 1.6941 | 1.7143 |
| + slope length ≤ 1 pixel | 108.5632 | 0.3624 | 0.3512 |
| **source-method, continuous L** | **129.3840** | **0.4319** | **0.4214** |
| **source-method, Desmet-Govers L** | **75.3235** | **0.2515** | **0.2447** |

Two controls: (i) a UNIFORM scalar 0.421 / 0.333 moves the total by exactly that scalar
(ratio − f < 1e-12) — the engine is linear in LS, so the 2.5 % is entirely the field's
spatial structure, not numerics; (ii) the re-run ratio equals Σ E_c·(LS_src/LS_ours)_c / Σ E_c
to all printed digits, so the erosion-weighted mean IS the ratio.

**The lower bracket endpoint 0.333 was inherited, and it is wrong.** docs/37 built it as
0.421 × 0.790, where 0.790 is `journal_c31-ls2d`'s `ls2d_dg96/ls2d` ratio on the UNCAPPED
continuous column (I reproduce it: 0.7894 area-weighted on `urh_ls2d.csv`). Measured INSIDE
the source formulation the DG/continuous ratio is **0.5807 area-wtd / 0.5822 erosion-wtd** —
the (m+1) prefactor and the x^m aspect term that the finite-difference form does not carry.
So the measured bracket is **×0.2515 – ×0.4319**, i.e. our LS is **2.32× – 3.98×** the source
level, not 2.37× – 3.00×.

**(b)/(c)** adopted 299.5387 Mt/yr (1,165.08 t km⁻² yr⁻¹); source-method continuous-L
129.3840 (503.25); source-method DG-L 75.3235 (292.98). Against the 144–184 Mt/yr Calamar
anchors — **which are an all-source, net-of-deposition outlet load and not the same quantity
as gross hillslope erosion (docs/40 §5)** — the anchor/model ratio goes 0.481–0.614 (adopted)
→ 1.113–1.422 → 1.912–2.443.

**(d)** MUSLE is linear in LS and α is a uniform scalar, so α_corrected = α_fit / f exactly:
an α fitted today at the adopted LS is **low by ×2.32 – ×3.98**. Worked on docs/37 §5.1's
measured no-deposition fit α = 6.83–8.73 → 15.81–20.21 (continuous L) or 27.16–34.72 (DG L);
the latter exceeds docs/31 C4.2's registered search box upper bound of 30 and comes within
0.7 of docs/35's hard stop 35.4. Equivalently the like-for-like α reference for OUR LS is
11.8 × f = **2.97 – 5.10** (docs/37 A1.5 says ≈3.9–5.0).

**(e)** The bracket is confounded with C and the unit factors in Π at the LEVEL, and its SHAPE
is below the registered noise floor. Per-station erosion-weighted LS ratio spans only
**1.287×** (0.3687 CARRASPOSO – 0.4745 BANANERA), sd(ln) 0.0769 all-18 / 0.0868 CAL-13 =
**0.165 / 0.187 × σ_r = 0.465** (docs/42 §4.2). Minimum detectable regression slope at 95 %:
**3.11** (all 18) against a true slope of exactly **1.0** if the LS is wrong — underpowered by
3.1×. The C revision's own shape is 3.9× larger (sd(ln) 0.299) and IS marginally detectable at
18 stations (min |b| 0.799). The two shape fingerprints correlate only r = 0.405; the two LS
bracket endpoints correlate r = 0.998, i.e. the bracket's width is a **pure level**.

**ENSO contrast: essentially immune.** Primary wet:dry flux ratio 2.2915 (adopted) → 2.2694
(continuous L) → 2.2665 (DG L), i.e. **−0.96 % / −1.09 %**; sensitivity pair 3.9725 → 3.9364 →
3.9329 (−0.91 % / −1.00 %). The project's deliverable moves by ≤1.1 % while the level moves by
2.3–4.0×.

Scratch files (system temp, nothing under `data/` or `docs/` touched apart from this journal):
`ls_field_agg.py`, `ls_field_basin.json`, `urh_ls2d_srcmethod.csv`, `ls_impact_engine.py`,
`ls_impact.json`, `ls_impact_stations.csv`, `ls_impact_power.py`, `ls_impact_final.json`,
`ls_impact_levels.csv`, `ls_impact_enso.py`, `ls_impact_enso.json`, `ls_impact_confound.py`,
`ls_impact_confound.json/.csv`.

**Caveat that travels with every number above:** both source-method rows rest on the same
reading of Buarque (2015) p. 94 ("seu valor máximo foi limitado ao tamanho do pixel do MDE" =
slope length ≤ one pixel) that `journal_decide-ls-resolution.md` §3b adopted. Under that cap
a_in → 0, so the DG finite difference degenerates to L = (D/(22.13·x))^m and loses its
finite-difference character; the row is still the literal eq.-13 form evaluated under the
literal p.-94 limiter, but a different reading of p. 94 moves BOTH rows.

### Checklist — closing state
- [x] 0. orientation
- [x] a. erosion-weighted ratio measured by engine re-run (0.4319 vs area-weighted 0.4214)
- [x] b. basin totals at adopted LS and both bracket endpoints
- [x] c. position vs the 144–184 Mt/yr anchor, with the quantity caveat
- [x] d. alpha absorption factor 2.32–3.98, with the arithmetic and the box/stop consequences
- [x] e. separability: level confounded (exactly), shape 3.1× below detection

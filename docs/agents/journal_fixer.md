# journal_fixer

GOAL: fix ONLY the one critical finding handed to me (MUSLE area-unit contradiction),
smallest change each, touch nothing a finding does not name.

Finding (critical): `data/processed/peakgap/method_research.md` (mtime 2026-08-11 04:13)
says Buarque eq. 7 / Fagundes eq. 12 label the MUSLE erosion-equation area **A in ha**,
while `src/mgb_sediment.py` (mtime 05:15, 62 min later) asserts the opposite ("whose A is
the same km2 area his eq. 7 uses") and enumerates only two conventions
(`pixel_km2`, `williams_m3`). The hectare convention — SWAT's standard MUSLE form,
`Q_surf[mm] x q_peak[m3/s] x area[ha]`, the form alpha = 11.8 is normally quoted with —
is absent everywhere. It is worth 100^0.56 = 13.1826x.

## Step checklist
- [x] 1. Journal created.
- [x] 2. Read method_research.md around the ha claim; quote the sentence verbatim.
- [x] 3. Read src/mgb_sediment.py UNITS section + volume_convention implementation.
- [x] 4. Read docs/35 gate (b) text.
- [x] 5. Confirm the hectare convention is absent (grep ha/hectare across named files).
- [x] 6. Verify the arithmetic numerically (100^0.56, 0.6844 x that, ratios to 144/184).
- [x] 7. Add third convention `swat_mm_ha` to src/mgb_sediment.py (code + UNITS docstring).
- [x] 8. Correct the km2 assertion in src/mgb_sediment.py; quote method_research verbatim.
- [x] 9. Add dated s9 amendment to docs/35 with the three-row gate (b) table.
- [x] 10. Verify from executed output (import module, run the three conventions).
- [x] 11. Confirm no frozen artifact touched; note C3.5 still blocked.

## Log

### Step 1 (start)
Files in scope (and ONLY these, plus this journal):
- `src/mgb_sediment.py`
- `docs/35_qpeak_preregistration.md`
- (read-only) `data/processed/peakgap/method_research.md`, `docs/36*`, journals c34/c36
No git add/commit/push. No calibration search. No frozen artifact writes.

### Steps 2-6 (evidence gathered, arithmetic verified)
`data/processed/peakgap/method_research.md` §1.1, lines 52-54, VERBATIM:
> Unit check: 1 mm/day over 1 km² = 1000 m³/day = 0.011574 m³/s = 1/86.4, so `Dsup` is
> mm/day and `A` is km² in eq. 7/12 (both texts label the MUSLE area `A` in ha for the
> erosion equation itself — mind the mixed units when porting).

`src/mgb_sediment.py` before this fix (docstring UNITS): "read literally off Buarque (2015)
eq. 5/eq. 7, whose ``A`` is the same km2 area his eq. 7 uses" + "Two conventions exist".
CONFIRMED CONTRADICTORY and CONFIRMED INCOMPLETE.

Absence check (grep -i 'hectare|\bha\b|_ha' over src/mgb_sediment.py, docs/35, docs/36,
journal_c34, journal_c36): only TWO hits, neither an area convention —
`src/mgb_sediment.py:58` K units `t.ha.h/(ha.MJ.mm)` and `docs/35:108` Kirpich's plot sizes
"0.4-45 ha". The hectare AREA convention was genuinely absent. Finding upheld.

Gate (b) three-row table lives in `docs/agents/journal_c36-first-run.md:110-113` (another
agent's journal — NOT edited, per journal protocol). Restated in docs/35 §9.1 instead, which
is what the fix_hint asks for.

### Step 7-9 EDITS MADE (2 files, both named by the finding)
`src/mgb_sediment.py`:
- docstring UNITS: "Two conventions" -> "THREE conventions"; the km2-A assertion DELETED and
  replaced with the verbatim method_research.md quote + the explicit statement that km2 is
  established for the q_peak equation ONLY; new `swat_mm_ha` block; measured table now 3 rows
  with an orders-of-magnitude column; alpha-to-anchor numbers restated for all three.
- new module constant `SWAT_HA_PER_KM2 = 100.0` and `VOLUME_FACTORS` dict
  {pixel_km2: 1.0, swat_mm_ha: 100.0, williams_m3: 1000.0};
  `VOLUME_CONVENTIONS = tuple(VOLUME_FACTORS)`.
- `SedParams.volume_factor` now `VOLUME_FACTORS[self.volume_convention]` (was a two-branch
  ternary that silently mapped ANY non-`pixel_km2` value to 1000 — with a third key that
  ternary would have been a live bug, so the mapping is required, not cosmetic).
- `SedParams.volume_convention` comment and `musle_load_tonnes` docstring updated.
DEFAULT UNCHANGED: `volume_convention` is still `pixel_km2` (the registered one). No
registered number was re-defaulted; this is an enumeration + documentation fix.

### Step 10 VERIFIED FROM EXECUTED OUTPUT (not exit codes)
`python -m pytest tests/test_sediment.py -q` -> **36 passed** (tests/test_sediment.py NOT
edited: it is not named by the finding; it references only `williams_m3`, so it still passes.
Gap disclosed: there is NO test asserting the `swat_mm_ha` factor).
Full frozen-driver run, read-only, 3652 d x 8672 minibacias, qsur_rel_mm, tau 0, FG 1.0,
alpha 11.8, beta 0.56, all three conventions (scratchpad script, nothing written to repo):

| convention | eroded_t (period) | Mt/yr | ratio to pixel_km2 | residual_t |
|---|---|---|---|---|
| pixel_km2 | 6,843,119.50146461 | 0.6844 | 1.0 | 0.0 |
| swat_mm_ha | 90,209,883.95552485 | **9.0222** | 13.182567385564074 | 0.0 |
| williams_m3 | 327,532,291.8760854 | 32.7577 | 47.86300923226385 | 0.0 |

Ratios equal `factor**beta` to the last digit (100**0.56 and 1000**0.56 bitwise).
`pixel_km2` reproduces journal_c36 Step 2 (6,843,119.50146461 t) EXACTLY, so the frozen
result is untouched by this edit.
Anchors: swat_mm_ha is 15.96x below 144 Mt/yr and 20.39x below 184 -> **1.203-1.310 orders**
(vs 2.323-2.430 for pixel_km2, 0.643-0.750 for williams_m3).
alpha needed to reach 144 Mt/yr: 2482.7 / 188.3 / 51.9 = 70.1x / 5.3x / 1.5x past the
alpha > 35.4 hard stop. ALL THREE still fail the stop, so gate (b)'s verdict direction is
convention-independent; only the residual gap size changes (by 13.18x).
CORRECTION I MADE TO MY OWN FIRST DRAFT: I initially wrote "~565 (williams_m3)" as the
alpha needed to close the gap. Executed output says 51.9. 565 = 11.8 x 47.86 is a DIFFERENT
quantity (the pixel_km2-units alpha that merely reproduces the williams_m3 level). Both are
now stated, separately labelled.

FLEET vs PER-UNIT (hard rule): the convention factor is a scalar multiplier on every
minibacia-day, so it is 13.1826x at BOTH scales — fleet 0.6844 -> 9.0222 Mt/yr, and the
per-minibacia median 0.0675 t/d -> 0.8899 t/d (journal_c36 Step 2 median x 13.1826).
No t/km2/yr yield is quoted anywhere (docs/23 embargo).

### Step 9 — docs/35 §9.1 amendment written
`docs/35_qpeak_preregistration.md`:
- §9 registration record: `| Amendments | *none* |` -> `**§9.1 (2026-08-11)** — MUSLE
  area-unit enumeration completed; registered choice UNCHANGED`.
- New `### 9.1 Amendment — 2026-08-11 — the MUSLE area unit is a THIRD convention, and it was
  missing` (docs/35 line 471): the verbatim method_research.md quote; the km²-is-for-eq.-7-only
  distinction; the 9-column three-row gate (b) table (0.6844 / 9.0222 / 32.7577 Mt/yr with
  product factor, load factor, both anchor ratios, orders of magnitude, α-needed and ×-past-stop);
  the per-unit row (0.0675 / 0.8899 / 3.231 t/d median); an explicit "C4 must CHOOSE a
  convention citing this table and must not inherit the smallest by default"; and the
  565-vs-52 relabelling.

### Step 10-11 (verification re-run after all edits, and protocol confirmations)
- `python -m pytest tests/test_sediment.py -q` -> **36 passed** (again, post-docs edit).
- Module re-imported: `VOLUME_CONVENTIONS = ('pixel_km2', 'swat_mm_ha', 'williams_m3')`;
  volume_factor 1.0 / 100.0 / 1000.0; bad value still raises
  "volume_convention must be one of ('pixel_km2', 'swat_mm_ha', 'williams_m3')".
- docs/35 §9.1 table verified 9 columns on header, separator and all three data rows.
- NO FROZEN ARTIFACT MODIFIED. `git status --porcelain` = 17 entries; the only ones I touched
  are `src/mgb_sediment.py`, `docs/35_qpeak_preregistration.md` and this journal (all three
  already untracked/new in this session's working tree, so no tracked file was altered by me).
  `h2e_drivers.npz`, `sim_calibrated_v2/`, `topology.npz`, `parameters.npz` read-only only.
- NOTHING BACKDATED. §9.1 carries today's date (2026-08-11), states in the document that it
  was written AFTER the C3.6 gate-(b) result it revises, and revises rather than replaces that
  record. journal_c36-first-run.md (the original gate-(b) verdict) left untouched.
- NO git add/commit/push. NO calibration search launched. NO t/km²/yr yield quoted.
- C3.5 (cross-check vs implementation B's `musle.py`) recorded as **still BLOCKED** — file not
  in this repo; not attempted (docs/35 §8 item 2 unchanged, restated in §9.1).

### Observation, NOT my change (flagged for the commit agent)
`Protocolo_descarga_PRECIPITACION.docx` was ` M` (modified) in the session-start git snapshot
and is now clean against HEAD (`git diff HEAD -- <file>` empty). I did not read, write or
restore that file. Someone/something else in this session reverted it. Recording it because a
disappearing modification is exactly the kind of thing that must not go unmentioned.

## OUTCOME
Finding 1 of 1: **FIXED.** Both named files edited, nothing else. Registered default and every
pre-registered threshold unchanged; what changed is the enumeration C4 will read, plus the
deletion of a false unit claim, plus a dated amendment that says so.
KNOWN REMAINING GAP (disclosed, not fixed, because the file is not named by the finding):
`tests/test_sediment.py` has a test asserting the `williams_m3` factor is exactly 1000**beta
but none asserting `swat_mm_ha` is exactly 100**beta. Verified by hand instead (executed run:
ratio 13.182567385564074 == 100**0.56 bitwise). A one-line test mirroring
`test_volume_convention_factor_is_exactly_1000_to_the_beta` should be added by whoever owns
that file next.

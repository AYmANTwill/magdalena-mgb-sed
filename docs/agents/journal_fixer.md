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

---

# RUN 2 — 2026-08-11 (same slug, new finding). LS-FORMULATION REPORTING FAILURE

GOAL: fix ONE critical finding — the run's largest wrong-way term (our LS formulation sits
2.37x–3.00x ABOVE the LS that alpha = 11.8 is paired with in the MGB-SED lineage) was measured
in `docs/agents/journal_decide-ls-resolution.md` §3b and appears in NO numbered document.
Two adopted-result claims (`docs/37` §2 "physically possible side", `docs/35` §9.2
"like-for-like ... no threshold changes") are contingent on an LS level equivalence that the
same run measured as 2.4–3x violated, and neither is qualified.

CLASSIFICATION, stated up front: this is a REPORTING failure, not an integrity failure. No
value in this repository was fitted to the 144–184 Mt/yr anchor by the run being audited, so
there is nothing to REVERT. `docs/37`'s verdict is ALREADY **OPEN** (its title line) — no flip
is needed, and I will not manufacture one. The fix is to publish a term whose omission
flattered the adopted result, and to mark the LS *level* question UNRESOLVED in the places
where it is currently asserted as settled.

## Step checklist (run 2)
- [x] R1. Journal section opened before any edit.
- [x] R2. Read the source measurement: journal_decide-ls-resolution §1a, §3b, and its
      "What is RESOLVED / UNRESOLVED" block + gate-2 recommendation.
- [x] R3. Read docs/37 in full; docs/35 §9.2 in full; grep docs/39 for the LS claim.
- [x] R4. Re-verify the arithmetic from executed output (ratios, load, implied SDR, alpha band).
- [x] R5. docs/37 §4: add **candidate 0**, the LS-formulation crack, with its measured bracket.
- [x] R6. docs/37 §2: qualify "moved the model onto the physically possible side ... for the
      first time" as CONDITIONAL on the LS level equivalence.
- [x] R7. docs/35 §9.2: qualify "it is now a like-for-like comparison, and no threshold
      changes".
- [x] R8. docs/35 §9.3: pre-register the C3.1 LS-formulation comparison (limiter / m cap / S
      function), the choice to be made on source grounds BEFORE any basin total is looked at.
- [x] R9. docs/39 §1.9: one row so the term is findable from the contradiction audit too
      (the finding names docs/39 as one of the three docs where grep returns zero hits).
- [x] R10. Verify every edit from executed output (grep the new strings, re-run the tests).

## Log — run 2

### R2–R3 — source evidence, quoted, before I write anything into a numbered doc

`docs/agents/journal_decide-ls-resolution.md` §1a, from Buarque, D.C. (2015) PhD thesis
IPH/UFRGS (the document that DEFINES MGB-SED, i.e. the method `docs/35` §4 registers this
project as transposing), p. 94 §6.2, VERBATIM:

> "Apenas o fator LS é determinado na etapa de pré-processamento, **para cada pixel do MDE** […]
> Na determinação do fator comprimento de 'L', **seu valor máximo foi limitado ao tamanho do
> pixel do MDE**."

i.e. the slope length is capped at ONE PIXEL. Ours (`ls2d_hs`) caps the upslope **AREA** at
1 km2, which lets the unit contributing length reach 1e6/92 ≈ **10,870 m** ≈ 118 pixels.
Two further formulation deviations from the same source (§1a table): `m` is a step function
hard-capped at 0.5 in his eq. 14 (ours is continuous McCool-1989, basin median 0.584), and `S`
is Wischmeier & Smith 1978 in his eq. 18 (ours is Moore & Burch `(sinθ/0.0896)^1.3`).

§3b MEASURED, all 30,235,916 basin cells, SAME 90 m grid (so this is a formulation difference,
not the resolution difference that §D1–D6 of that journal resolved); the harness reproduces
`ours_hs` = 39.812 bitwise, so the comparison is internally like-for-like:

| LS variant at 90 m | area-wtd mean | Andean >1000 m awm | x ours |
|---|---|---|---|
| ours (`ls2d_hs`) | 39.812 | 65.199 | 1.000 |
| + m capped at 0.5 | 20.005 | 31.820 | 0.502 |
| + S = W&S 1978 | 68.234 | 114.202 | 1.714 |
| + slope length ≤ 1 pixel | 13.985 | 22.308 | **0.351** |
| **all three (source-method LS)** | **16.775** | 27.109 | **0.421** |

### R4 — arithmetic re-verified from executed output (python3.10, this session)

- 16.775 / 39.812 = **0.4213553702401286**; inverse **2.3732935916542477**.
- × a further 0.790 (the literal Desmet–Govers finite-difference L; that ratio was measured
  stable at both 90 m and 740 m in `journal_c31-ls2d.md`) = **0.3328707424897016**; inverse
  **3.0041691033598066**. So the bracket is **0.333 – 0.421**, i.e. our LS is **2.37x – 3.00x**
  the reference level.
- 248.730 × 0.4214 = **104.80 Mt/yr** → implied SDR 144/104.80 = **1.374**, 184/104.80 = 1.756.
  248.730 × 0.3329 = **82.79 Mt/yr** → implied SDR **1.739 – 2.222**.
  (The finding's 104.72 / 82.83 use the rounded 0.421 / 0.333; identical to 3 figures.)
  BOTH fall BELOW BOTH anchors ⇒ back on the **physically impossible** side (SDR > 1).
- Like-for-like alpha reference for OUR LS: 11.8 / 2.373…3.004 = **4.97 – 3.93**.
  `docs/35` §6.1 expected band 5.9–23.6 becomes **1.96 – 9.94**; the hard stop 35.4 becomes
  **11.78 – 14.92**; the low stop 3.9 becomes 1.30 – 1.64. The ADOPTED alpha = 11.8 therefore
  sits **at or above** the corrected upper hard stop at the 3.00x end of the bracket.

### R4b — HONEST LIMIT of the multiplier (recorded before I quote it in a numbered doc)

0.421 is a ratio of **area-weighted** per-cell LS means. The engine's basin total is a sum of
per-URH terms each **linear** in LS but weighted by that cell's `Qsur·q_peak·K·C`, i.e. an
**erosion**-weighted mean, not an area-weighted one. So 248.73 × 0.421 is a PROXY, not the
exact re-run. Supporting evidence that the proxy is representative rather than lucky: the
formulation swap has nearly the same effect on the erosive terrain as on the whole basin —
Andean (>1000 m) 27.109/65.199 = **0.4158** vs basin 0.4214, 1.3 % apart — and erosion is
concentrated in exactly that terrain (`docs/37` §3 gate (a): the 500–3000 m bands carry 53.1 %
of basin erosion and >3000 m a further 36.9 %). I will state the proxy status in the documents
rather than present 104.8 as a computed re-run. Only re-deriving per-URH LS under the source
formulation and re-running the decade gives the exact figure; that is the C3.1 job I am
pre-registering, NOT something a reporting fix may do.

### R4c — DIRECTION DISCLOSURE (the discipline check for this run)

Everything I am about to add makes the adopted result **WORSE**: it multiplies the headline
248.730 Mt/yr DOWN by 0.33–0.42, pushes the implied SDR from 0.579–0.740 (already above the
quoted band) to 1.37–2.22 (impossible), and TIGHTENS the alpha guard until the adopted
alpha = 11.8 is itself at the corrected hard stop. I am publishing it for precisely that
reason: it is the largest wrong-way term in the run, it was missing from every numbered doc,
and the direction of its omission was the convenient one. No number anywhere is moved toward
144–184 Mt/yr by this fix. Nothing here was resolved by asking what matches the anchor: the
bracket comes from Buarque (2015) p. 94 / eq. 14 / eq. 18 and from a measurement on our own
grid, both of which existed before I was asked.

### R5-R6 — docs/37 edited (three places)

1. **Closure-conditions table, row 2** flipped `no decision left unresolved` from **MET** to
   **NOT MET**, naming the fifth question (LS *formulation* level, 2.37x-3.00x) and pointing at
   §4 candidate 0. Row 4 (SDR) now also carries "under §4 candidate 0 it becomes 1.37 - 2.22,
   i.e. impossible". The lead sentence "Three of the four closure conditions are met" was
   removed because it is now false (two are not met).
   NOTE: the document's overall verdict was **already OPEN** and remains OPEN — I did not need
   to flip it and did not invent a flip. What changed is *why* it is open, and by how much.
2. **New "Amendment note (2026-08-11)"** immediately under the table stating in plain words that
   the original omission pointed in the flattering direction.
3. **§2, after the "physically possible side" sentence** — a `> CONDITIONAL` block. The original
   sentence is left standing (it is what was claimed at the time) and is qualified rather than
   silently rewritten: the claim holds only at our LS level; the measured bracket takes
   248.730 -> 104.8 / 82.8 Mt/yr, below both anchors, implied SDR 1.37 - 2.22, i.e. back on the
   impossible side; treat "possible side" as provisional until C3.1 closes.
4. **§4** — "Four candidates" -> "Five candidates", with the intro now saying candidate 0 makes
   the residual LARGER by 2.37x-3.00x, and **candidate 0** added FIRST: the four-row lever table
   (limiter 0.351 / m 0.502 / S 1.714 / joint 0.421) with the Buarque p. 94 quote, the
   interaction check (0.302 != 0.421), the 0.333-0.421 bracket, the level consequence with the
   R4b proxy caveat stated in the doc, the alpha-guard consequence (like-for-like reference
   3.9-5.0 not 11.8; band 2.0-9.9; stop 11.8-14.9; adopted alpha = 11.8 at/above its own
   corrected stop), the RESOLVER (docs/35 §9.3) with Buarque p. 121's "superestimado", and an
   explicit DO NOT against stacking candidates 1 and 2 on an uncorrected LS.
5. **§4 item 4** ("terms known to point the wrong way") now says the largest wrong-way term is
   candidate 0, not the 1.125x that was the biggest entry before.

### R7-R8 — docs/35 edited (four places)

1. **§6.1** — a caveat under the "α = 11.8 ... like-for-like reference" line: the band is the
   band for the SOURCE LS; divide by 2.37-3.00 before comparing with an α fitted on ours.
   Registered values left as written.
2. **§9.2 answer 1** — the "like-for-like ... no threshold changes" sentence is narrowed in place
   to "like-for-like in **units** ... on that account", followed by a `> CONDITIONAL` box: unit
   equivalence yes, LEVEL equivalence measured 2.37x-3.00x violated; the corrected band/stops;
   and the statement that thresholds DO change once the formulation is settled, in the
   TIGHTENING direction.
3. **§9.2 gate-(b) reading** — "direction failure is fixed" -> "fixed **at our LS level**",
   with the bracket that would return it.
4. **§9 registration record** — Amendments row gains §9.3.
5. **New §9.3** (7 sub-sections, docs/35 line 678+): the C3.1 LS-formulation comparison
   PRE-REGISTERED. Decision rule in priority order, all source-based: (1) fidelity to the
   transposed method is the DEFAULT OUTCOME because MUSLE is linear in LS and α = 11.8 is that
   lineage's coefficient; (2) a deviation needs its own citable justification, dated, written
   BEFORE the total is computed; (3) a deviation forces the §6.1 band to be rescaled by the
   measured level ratio (the LS analogue of §6.2); (4) ties break toward the LOWER LS level per
   Buarque p. 121, never by the basin total. §9.3.3 registers the expected consequence IN
   ADVANCE (104.8 / 82.8 Mt/yr, SDR 1.37-2.22, impossible) with the explicit rule that **an
   unattractive total is not evidence against the source formulation**. §9.3.4 forbids
   overwriting `urh_ls2d.csv` / `minibacia_ls2d.csv` (variants reachable by name, as the volume
   conventions are) and discloses the p. 94 interpretation risk. §9.3.5 registers two traps: do
   NOT use the retired, uncited "2-10" band as evidence for the source formulation even though
   its median 7.262 sits inside it, and do NOT stack docs/37 §4 candidates 1-2 on an unfixed LS.

### R9 — docs/39 §1.9 edited (two rows, one changed + one added)

The existing `LS2D per-cell median ... vs published 2-10` row's verdict "(no numbered doc owns
it yet)" now names its owner (docs/37 §1 decision 4 retires the band; the level question is
docs/37 §4 candidate 0). A new row records the formulation ratio itself with its sources and
the note that it **was absent from every numbered doc until 2026-08-11**. The finding named
docs/39 as one of the three docs where grep returned zero hits, so it is in scope; the change is
two table rows and nothing else.

### R10 — verification, from executed output only

- `grep -c` on the three docs: `2.37` -> 6 / 5 / 1 hits (was 0 / 0 / 0);
  `formulation` -> 6 / 20 / 1 (was 0 / 0 / 0); `limiter` -> 3 / 2 / 0 (was 0 / 0 / 0).
  The grep the finding ran now returns hits in all three documents.
- `python3.10 -m pytest tests/ -q` -> **96 passed in 10.32s** (unchanged; no code was touched).
- `grep -n "^### 9.3\|^#### 9.3" docs/35` -> §9.3 plus 9.3.1-9.3.6 present at lines 678-774;
  file 674 -> 785 lines.
- Journal: 146 -> 253 lines before this closing block; nothing deleted, run 1 intact.
- **Frozen artifacts untouched:** `data/processed/sim_calibrated_v2/h2e_drivers.npz` and
  `parameters_H2E.csv` still carry mtime **2026-08-10 13:54 / 14:03**, i.e. yesterday, before
  this session. Not opened by this run at all.
- `git status --porcelain`: the only paths I modified are `docs/35_qpeak_preregistration.md`,
  `docs/37_c3_closure.md`, `docs/39_contradiction_audit.md` and this journal. `src/mgb_sediment.py`
  and `tests/test_sediment.py` show as modified from EARLIER runs in this session, not from me.
- No git add / commit / push. No calibration launched. No `data/` product written. No t/km2/yr
  gauge-referenced yield quoted anywhere in the new text.

## OUTCOME (run 2)

Finding 1 of 1: **FIXED**, as a reporting fix.

- Nothing was reverted, because nothing was fitted: the finding is explicit that this is a
  reporting failure, and the bracket I published was measured from Buarque (2015) + our own grid
  before this run existed. No value in the repository moved.
- `docs/37`'s verdict was **already OPEN** and stays OPEN; what I changed is that a second
  closure condition ("no decision left unresolved") is now correctly marked **NOT MET**, so the
  document no longer reads as "three METs and one physical miss".
- The level question is now marked **UNRESOLVED** in both numbered docs that depended on it, and
  the comparison that would resolve it is pre-registered with its decision rule and its expected
  (unattractive) outcome fixed in advance.
- Direction check: every number added moves the model AWAY from the 144-184 Mt/yr anchor
  (248.730 -> 104.8 / 82.8) and TIGHTENS the α guard until the adopted α = 11.8 sits at its own
  corrected stop. Nothing here makes the result look better.

KNOWN REMAINING GAPS, disclosed rather than fixed (each outside this finding's named files):
1. **The exact factor is still a proxy.** 104.8 Mt/yr uses an area-weighted LS ratio, not an
   erosion-weighted one. Only the C3.1 re-run gives the exact total; every place I quote it says
   so. Resolving it requires recomputing per-URH LS under the source formulation, which is a
   `scripts/c3/ls2d.py` + `data/processed/` change and therefore not mine.
2. **The engine still exposes no `ls2d_formulation` option**, unlike `volume_convention` /
   `k_unit_system` / `ls2d_aggregation` / `ls2d_resolution`. Until C3.1 adds one, the source
   formulation is not reachable by name, so `convention_summary()` cannot report which LS
   formulation produced a load. `src/mgb_sediment.py` is not named by this finding; I did not
   touch it. This is the single most useful next code change.
3. `docs/00_INDEX.md`, `progress_map` and `docs/31` still describe the LS state without the
   formulation term. Not named by the finding; not edited.

### R11 (post-close addendum) — docs/37 §5 item 1

The same "like-for-like" phrase recurs in §5 item 1 ("the §6.1 guard, which has only now become
a like-for-like comparison at all"). Added one clause there: like-for-like in UNITS only, not in
level; at the corrected band (expected ~2.0-9.9) an SDR = 1.0 fit at alpha = 6.83-8.73 still
lands inside it, so the trap is unchanged in kind but the numbers to quote it with depend on
C3.1. Verified by `grep -n`: docs/37 has "like-for-like" on exactly 3 lines — 195 (inside the §4
candidate-0 text I added, where it means the corrected alpha reference), 252 (the original §5
claim) and 256 (the qualification I just added directly under it). Both claim-bearing
occurrences therefore carry their qualification adjacent to them.
SELF-CORRECTION: I first wrote "4 occurrences ... all three of the claim-bearing ones" and then
guessed lines 85/87/219; the executed grep says 3 lines at 195/252/256 and the §2 CONDITIONAL
box does not use the phrase at all. Corrected against the output, per the verify-from-executed-
output rule that this very run is enforcing on others. Tests re-run after this edit: 96 passed.

---

# RUN 3 — 2026-08-11 (same slug, two new criticals). MUSLE QUANTITY IDENTITY + ENGINE DOCSTRING

GOAL: fix exactly TWO critical findings, smallest change each.
F1: clause 4' compares a sediment YIELD (our MUSLE sum) against a gross EROSION (Tan RUSLE)
    and calls it like-for-like; nb18 §1 already says that distinction is not pedantic.
    Fix = pin WHICH quantity the MUSLE sum is, with SWAT Ch.4:1 as the citation, re-derive
    all three legs under BOTH readings, report the residual sign-unknown, drop Leg C's
    mean-vs-max form as invalid at basin scale, and re-open the 0.579-0.740 reading as a
    possible channel/floodplain throughput vs docs/40's 20-45 % Momposina retention.
F2: src/mgb_sediment.py docstring lines ~177-197 still assert the RETIRED uncited
    0.05-0.3 SDR band as "the published range", still says C3 is open "for exactly this
    reason", and its convention table understates its own default by 20.4 %
    (248.72 vs 299.54 Mt/yr under cited_central C).

## Step checklist (run 3)
- [x] S1. Journal section opened BEFORE any edit.
- [x] S2. Read docs/37 (A1.1 clauses, A1.2, A1.7), docs/40, docs/41, docs/42 G5.
- [x] S3. Read src/mgb_sediment.py docstring block + CP_REVISIONS + convention table.
- [x] S4. Read nb18 cell 8 (§1) and cell 68 (§6.4) verbatim; quote both.
- [x] S5. Locate/verify a citable SWAT Ch.4:1 source IN-REPO. If not citable -> say UNCITED.
- [x] S6. Verify every number I intend to print from executed output.
- [x] S7. Edit docs/40 with the new §0 (quantity identity) + three-leg re-derivation.
- [x] S8. Edit docs/37 A1.1 clause 4' -> sign-unknown; add A1.9; add mgb_sediment.py to A1.7 item 4.
- [x] S9. Edit src/mgb_sediment.py docstring (F2).
- [x] S10. Re-execute nb18 if its text carries the retired claim AND is named; else disclose.
- [x] S11. Verify all edits from executed output; run tests; confirm no frozen artifact touched.

## Log — run 3

### S1 (start)
Files I expect to touch: docs/40_sdr_evidence.md, docs/37_c3_closure.md,
src/mgb_sediment.py, plus this journal. Read-only: docs/41, docs/42, nb18, journal_cite-sdr.
No git add/commit/push. No calibration. No frozen-artifact write.

### S2-S6 — evidence, quoted and verified BEFORE any edit

**The two nb18 sentences the finding pairs, both verbatim (read with json, not grep).**
`notebooks/18_musle_construction.ipynb` cell 8 (§1), point 2:
> "Because runoff already encodes how much water was available to *carry* the soil away, MUSLE's
> output is closer to "sediment delivered from this patch to its stream" than to "soil detached
> on this patch". Section 6 shows this distinction is not pedantic - a whole closure gate was
> retired over it."

cell 68 (§6.4), Leg A bullet:
> "**Leg A - the only like-for-like denominator.** Tan, Liu & Lu (2024), *ESPL* 49:1778-1795, report
> **RUSLE hillslope** erosion of 23.7-26.5 t ha-1 a-1 in a large, data-sparse
> mountainous basin. Hillslope against hillslope, so this is the leg that counts."

CONFIRMED CONTRADICTORY in the sense the finding states: the second treats a RUSLE *erosion* rate
as the like-for-like denominator for a sum the first says is closer to a *delivered* quantity.

**The citation, verified by me from the PRIMARY source this run, not taken from the finding.**
I fetched `https://swat.tamu.edu/media/99192/swat2009-theory.pdf` (7,690,470 B, 647 pp) and
text-extracted it with PyMuPDF. **SWAT Theoretical Documentation, Version 2009, Section 4
Chapter 1 "EQUATIONS: SEDIMENT", printed p. 252 (PDF page 277)**, VERBATIM:

> "USLE predicts average annual gross erosion as a function of rainfall energy. In MUSLE, the
> rainfall energy factor is replaced with a runoff factor. This improves the sediment yield
> prediction, eliminates the need for delivery ratios, and allows the equation to be applied to
> individual storm events. Sediment yield prediction is improved because runoff is a function of
> antecedent moisture condition as well as rainfall energy. Delivery ratios (the sediment yield at
> any point along the channel divided by the source erosion above that point) are required by the
> USLE because the rainfall factor represents energy used in detachment only. Delivery ratios are
> not needed with MUSLE because the runoff factor represents energy used in detaching and
> transporting sediment."

and eq. 4:1.1.1, same page:

> "where sed is the sediment yield on a given day (metric tons), Qsurf is the surface runoff volume
> (mm H2O/ha), qpeak is the peak runoff rate (m3/s), areahru is the area of the HRU (ha), KUSLE is
> the USLE soil erodibility factor (0.013 metric ton m2 hr/(m3-metric ton cm))"

The finding's quotation is accurate. SECOND, INDEPENDENT confirmation of the `sed` definition:
WebFetch of the SWAT+ theoretical documentation MUSLE page returned
"sed is the sediment yield on a given day (metric tons)" and nothing about rainfall energy or
delivery ratios — so the gitbook page alone would NOT have supported the decisive sentence; the
2009 PDF does. In-repo corroboration that the SWAT text is the ancestor of our equation:
`docs/agents/journal_decide-units.md` §1d-§1e already established the chain of custody
SWAT manual -> Buarque (2015) -> Fagundes (2018) -> this project.

**Arithmetic, all from executed python3.10 this session (A = 257,097 km2):**
- adopted C total 299.5387 Mt/yr -> 1,165.0805 t/km2/yr = **11.6508 t/ha/yr** (model-internal).
- Leg A as written (erosion reading): 23.7 / 26.5 vs 11.6508 -> **2.0342x / 2.2745x low**
  (reproduces docs/37 A1.4 exactly).
- Leg A under the YIELD reading, Tan's gross erosion converted with NEH Table 6-2's own
  sheet-erosion delivery ratio 0.33 (= 300,000/900,000 = 0.3333): 7.8210 / 8.7450 t/ha/a, ours
  11.6508 -> **1.4897x / 1.3323x ABOVE**. With 1/3 exactly: 1.4748x / 1.3190x above. SIGN INVERTS.
- No-conversion cross-check: Tan et al.'s own reported specific sediment YIELD is 1.3-16.9 t/ha/a
  and ours (11.6508) is **inside** it.
- Leg B 1,485/1,445.32 = **1.02745** (the 2.8 % docs/37 already concedes is no longer evidence).
- Leg C mean 1,165.08/690 = **1.6885x above**; max 1,165.08/2,200 = 0.5296 (**1.8883x** the other
  way). Model's OWN internal range 1,445.32/77.41 = **18.671x**, so a basin mean below a sub-basin
  maximum is arithmetic, not evidence.
- Throughput reading of the retired ratio: prior C 144/248.7298 = 0.57894 and 184/248.7298 =
  0.73976 -> **26.02-42.11 % lost in transit** (the finding's 26.0-42.1 %). At the ADOPTED C the
  ratio is 0.48074-0.61428 -> **38.57-51.93 %**, i.e. ABOVE docs/40 C11's 20-45 % Momposina band,
  so the agreement the finding notes is a prior-C agreement and I will not restate it as current.
  Decomposed at the adopted C: total transit loss 155.539 (low anchor) / 115.539 (high anchor)
  Mt/yr; Momposina M9's 36-80 Mt/yr is 12.02-26.71 % of the hillslope yield, leaving
  **75.54-119.54 Mt/yr (25.2-39.9 %)** resp. **35.54-79.54 Mt/yr (11.9-26.6 %)** for every other
  sink. Physically open, not physically closed.
- alpha implied by the yield reading: 11.8/1.4897 = **7.921** and 11.8/1.3323 = **8.857**, which
  overlaps docs/42 G5's deposition-free fit band **6.83-8.73**. Recorded because it means a fit
  that "works" under the yield reading is nearly the same fit as one asserting SDR = 1.0.
- Erosion-reading alpha check: 11.8 x 2.034 = 24.00, 11.8 x 2.275 = 26.84 (docs/37's 24.0-26.8).

**DIRECTION DISCLOSURE.** The yield reading makes the adopted result look BETTER (from 2.03-2.27x
low to 1.33-1.49x high). I am therefore NOT adopting it as the answer. What the evidence supports
is that the decisive leg is not like-for-like, so the residual's DIRECTION is unknown; the honest
verdict for clause 4' is NOT ESTABLISHED, which still forbids closure, rather than MET. The
counter-argument to the yield reading is recorded in the docs too: MUSLE was fitted to
small-watershed OUTLET yields and we apply it per 90 m pixel and sum, so a per-pixel sum over
257,097 km2 is not a basin yield either.

### S7 — docs/40 edited (7 places, all pointing to the same defect)

1. **NEW `## 0` (lines 35-142)**, five sub-sections: §0.1 the SWAT v2009 Ch. 4:1 p. 252 quotes
   verbatim + the nb18 §1 sentence that already said it; §0.2 what it does to §7 (Leg A's sign
   inverts to 1.332-1.490x ABOVE via NEH's own 0.33 sheet DR, plus the conversion-free
   cross-check that ours lands inside Tan's own 1.3-16.9 t/ha/a YIELD range; Leg B already
   conceded; Leg C's max form invalid because a mean cannot reach a max and our own internal
   range is 18.671x); §0.3 the conclusion — **direction UNKNOWN, clause 4' NOT ESTABLISHED**,
   the yield reading explicitly NOT adopted, with its own counter-argument (18-small-watershed
   fit vs a 30-million-pixel sum) written next to it; §0.4 the throughput reading at BOTH C
   levels with the honest note that the Momposina agreement is a prior-C agreement.
2. **Header verdict box** — one AMENDED note so the abstract cannot be quoted without §0.
3. **§7 preamble** — "all failing in the same direction" marked SUPERSEDED.
4. **§7 Leg C** — max-yield half WITHDRAWN, with the arithmetic reason.
5. **§8.2** — the replacement wording marked AMENDED and pointed at clause 4'' in docs/37 A1.9.
6. **§8.3** — "one closure condition is now evaluable and failed" -> not established.
7. **§9 C18** (new citation row) + **§10 traps 4 and 5** (quantity-before-comparison; a basin mean
   can never reach a sub-basin maximum) + **§11** reproduction block extended with every number
   §0 prints + a provenance paragraph for §0 itself.

### S8 — docs/37 edited (5 places)

1. **A1.1 clause 4'** struck through -> **RE-OPENED**, with the reason and the inverted bracket;
   **new clause 4''** (quantity-explicit) marked **NOT ESTABLISHED**.
2. **Under the A1.1 table** — an A1.9 pointer stating that clauses 2 and 3 are now the only ones
   failing in a KNOWN direction and that either alone still forbids closure.
3. **A1.4 head** — SUPERSEDED IN PART; its arithmetic stands, its interpretation does not; explicit
   "1.03-2.27x must not be quoted as a directed result".
4. **A1.7 item 4** — `src/mgb_sediment.py` added to the 248.730-superseded file list, with the three
   docstring defects named (20.4 % understated default, retired band as "the published range",
   false "for exactly this reason") and marked fixed by this pass. **A1.7 item 7 NEW** — nb18/
   make_nb18.py enumerated with generator line numbers (2366-2368, 2397, 2417, 2430, 2449,
   2512-2517, 2980) and recorded as NOT FIXED with the reason.
5. **NEW `AMENDMENT A1.9`** (7 sub-sections, 182 lines): the citation; the both-readings leg table;
   the verdict + resolver; the C4 consequences incl. the alpha 7.92-8.86 vs G5 6.83-8.73 overlap;
   the throughput/Momposina hypothesis with its prior-C caveat and its decomposition; a direction
   disclosure; a reproduction block.

### S9 — src/mgb_sediment.py docstring edited (ONE block, lines 177-198 -> 177-227)

- Convention table: 4 rows -> **5**, each row now carries its `cp_revision`, and the DEFAULT row is
  **`williams_m3` + `us_customary` @ `cited_central_2026_08_11` = 299.539 Mt/yr, 2.08x / 1.63x
  ABOVE** (299.5387/144 = 2.0801, /184 = 1.6280 — computed, not copied). The old 248.72 row is kept
  and relabelled `@ prior_2026_08_11`, and its figure corrected to 248.730.
- The "a delivery ratio is < 1 so the first three rows are impossible" argument is replaced by the
  statement that the anchor column is CONTEXT and the conventions were chosen by the unit
  derivations (SWAT source code, docs/35 §9.2) — which is what actually decided them.
- The 0.05-0.3 sentence is DELETED as a live claim and replaced by a three-bullet correction: the
  band is uncited and retired in both directions (do not reinstate); C3 is open on A1.1 clauses 2,
  3 and 4''; and the "gross erosion" label is itself unresolved, with the SWAT quote and the
  inverted bracket. The old sentence is quoted inside the correction rather than erased, so the
  record of what the file used to assert survives.
- The closing prohibition is kept and strengthened with docs/42 G5 and the 7.92-8.86 / 6.83-8.73
  overlap. NO CODE CHANGED — docstring only.

### S10 — nb18: NOT edited, with the reason (this is the "unfixable as scoped" entry)

The wrong claim is in *executed* cells (printed strings at make_nb18.py 2397/2417/2430/2449), so a
correct fix is a generator edit **plus** a full nb18 re-execution. Neither file is named by either
finding, and the fix_hint for F1 scopes the fix to docs/40 §0 / docs/37 A1.9. Recorded as
**docs/37 A1.7 item 7** with exact line numbers, and again in A1.9.6, so the next pass can do it in
one go with the qualification text already written in A1.9.2-A1.9.3. nb18 executes today (its
outputs are present and were produced by the nb18 agent) — I did not re-run it and did not need to.

### S11 — verification, from executed output only

- `python3.10 -m pytest tests/ -q` -> **94 passed, 2 failed in 8.16 s**. The two failures are
  verbatim the ones docs/37 A1.7 item 2 pre-registers (`test_audit_unit_day_reproduces_from_the_real_files`,
  `test_real_geometry_shape_and_ranges`; the second's assert shows the expected
  `{0.0, 0.005, 0.015, 0.03, 0.2, 0.5}` against the stale `{0.0, 0.001, ...}`), i.e. the stale C
  assertions from the CSV rewrite, NOT caused by me. Unchanged before and after my edit.
- Module re-imported: `import OK`, `VOLUME_CONVENTIONS = ('pixel_km2','swat_mm_ha','williams_m3')`,
  docstring 431 lines, contains `299.539` / `UNCITED and RETIRED` / `docs/40` / `A1.9`.
- Markdown table integrity checked programmatically (column counts per contiguous block):
  docs/40 **11 tables, 0 ragged**; docs/37 **18 tables, 0 ragged**.
- Greps: docs/40 `## 0. AMENDMENT` 1, `sediment yield on a given day` 1, `1.332 - 1.490` 1,
  `WITHDRAWN` 2, `C18` 3, `18.671` 4. docs/37 `A1.9` 26, `4''` 9, `NOT ESTABLISHED` 7, `1.4897` 3,
  `src/mgb_sediment.py` 7, `A1.7 item 7` 1. Line counts: docs/40 548 -> **727**, docs/37 737 ->
  **961**.
- **Frozen artifacts untouched:** `h2e_drivers.npz` 2026-08-10 13:54, `parameters_H2E.csv` and
  `q_gauge_H2E.npz` 2026-08-10 14:03 — all yesterday, before this session. Not opened by this run.
  No simulation re-run; every erosion level in A1.9 is quoted from docs/37 A1.3-A1.4.
- `git status --porcelain`: the only paths I modified are `docs/37_c3_closure.md`,
  `docs/40_sdr_evidence.md`, `src/mgb_sediment.py` and this journal. No git add/commit/push. No
  calibration launched. No `data/` product written. No gauge-referenced t/km2/yr yield quoted — every
  specific figure in the new text is labelled model-internal or is a published comparator.
- **Observation, NOT my change (again flagged for the commit agent):** the three
  `Protocolo_descarga_*.docx` files now show as **staged deletions** (`D `) in git status. I did not
  read, write, move or delete them. Recorded because run 1 of this journal flagged one of these files
  changing state without an owner, and now all three are staged for deletion.

## OUTCOME (run 3)

**Finding 1 (clause 4' compares a yield against a gross erosion): FIXED**, as the fix_hint asks and
not by editing a number.
- The quantity question is now PINNED with a primary citation I retrieved and text-extracted myself
  (SWAT v2009 Ch. 4:1 p. 252) rather than accepted from the finding, and the citation's own metadata
  was read off the PDF's title page so the reference is not invented. It is filed as docs/40 C18 with
  its retrieval status, and the one half of it that a second source could confirm was confirmed
  against SWAT+ independently.
- All three legs are re-derived under BOTH readings at the adopted C. Leg A's sign inverts. Leg C's
  max-yield form is dropped as arithmetically invalid at basin scale. Leg B was already conceded.
- Clause 4' is re-opened as clause 4'' and reported **NOT ESTABLISHED**; the residual is reported
  **sign-unknown** (2.27x low ... 1.49x high) in docs/40 §0.3, docs/37 A1.1 and A1.9.3.
- C3's verdict is **unchanged: OPEN**, now on clauses 2, 3 and 4''. I did not manufacture a flip and
  did not let the better-looking reading close anything.
- The 0.579-0.740 throughput reading is re-examined with numbers at both C levels, and the
  Momposina agreement is reported as a **prior-C** agreement with the residual-sink decomposition
  that the adopted C requires — not restated as current.
- The C4 prohibition the fix_hint asks for is written in docs/40 §0.3, docs/37 A1.9.4 item 1 and the
  engine docstring: **no alpha fit against clause 4' or 4''**, with the measured G5 overlap
  (7.92-8.86 vs 6.83-8.73) as the reason it would be undetectable otherwise.

**Finding 2 (engine docstring carries the retired band as live fact): FIXED**, all three defects, in
the one block, plus the A1.7 omission recorded in docs/37 rather than silently repaired.

**DIRECTION DISCIPLINE.** The single change available to this run that would have made the adopted
result look better — adopting the yield reading — is the one thing I refused to do. No parameter, no
convention, no `cp_revision`, no threshold and no registered number moved. What moved is one label
(which quantity a sum is) and the status of one clause, from a fail with a direction to a
**cannot-be-evaluated**, which is worse to work with and is what the evidence supports.

**KNOWN REMAINING GAPS, disclosed rather than fixed:**
1. `notebooks/18_musle_construction.ipynb` + `src/nbgen/make_nb18.py` — docs/37 A1.7 item 7 above.
2. NEH Table 6-2's 0.33 is a US agricultural sheet-erosion delivery ratio used to establish the
   DIRECTION of the conversion, not a validated conversion for a tropical Andean basin. Stated as
   such in both documents; the resolver (docs/37 A1.9.3) asks for a cited one if reading A is kept.
3. `docs/00_INDEX.md`, `docs/PROGRESS.md` and `progress_map.html` still carry clause 4' as
   "NOT MET - under-erosive". Not named by either finding; not edited.
4. `tests/test_sediment.py` still 2 failed (docs/37 A1.7 item 2). Pre-existing, not in scope.

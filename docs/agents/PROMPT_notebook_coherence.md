# MGB-SED / Magdalena — NOTEBOOK COHERENCE PASS: one narrative, no contradictions, nothing hidden

> **How to use this file.** Open a fresh session in `c:\dev\magdalena-mgb-sed` and say:
> *"Read `docs/agents/PROMPT_notebook_coherence.md` and execute it. USE MULTI-AGENTING."*
> Run it in **stages**, not one shot — Phase 2 alone touches ten generators and nb14 carries an
> eight-hour timeout. Do not start it while another workflow is writing to `docs/agents/`.
> Written 2026-08-13.

Repo: `c:\dev\magdalena-mgb-sed` (Windows). Use `python3.10`, **never** `python`.
`jupyter` is **NOT** on PATH. Execute notebooks only with:
`python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 <nb>`

USE MULTI-AGENTING. Every agent keeps its own crash journal at
`docs/agents/journal_<unique-slug>.md`, appended **as it goes**, never only at the end. Give every
agent a **different** journal filename — parallel agents have overwritten each other's reports in
this project before.

## 0 — Orient before touching anything

Read in this order: `CLAUDE.md` → `docs/00_INDEX.md` (the map; it has a WHERE-IS-IT table) →
`notebooks/README.md` → `progress_map.html` (live status). Then `docs/16` §6 (the traps reference),
`docs/20` (the reproduction guide), and the owning doc for each notebook you touch.
**If a doc disagrees with the index, the doc wins.**

## 1 — THE SINGLE MOST IMPORTANT CONSTRAINT

**Notebooks 10–19 are GENERATED** by `src/nbgen/make_nb10.py` … `make_nb19.py`. A generator exists
for every one, and as of 2026-08-12 each reproduces its committed notebook **source-identically**.

**NEVER hand-edit a notebook in the 10–19 range.** The next regeneration silently destroys the
edit. Edit the **generator**, rerun it, then execute the notebook, then verify from the executed
output. When you are done, re-verify the source-identical property still holds.

**Notebooks 01–09 have NO generators** and are hand-written. Those you edit directly — but they are
Phase A (DEM, URH, hydrology derivation, land cover/soils, data inventory, minibacias, soil
parameters) and are the *oldest* text in the project, so they are where stale claims hide.

## 2 — Rules that bind every agent

- **MEASURE BEFORE ASSERTING.** This project has reversed several confident verdicts by measuring
  them. A claim with no measurement behind it is worse than silence.
- **VERIFY FROM EXECUTED OUTPUT, NEVER FROM AN EXIT CODE.** On Windows `cmd ; echo $?` masks the
  real status; this exact trap has bitten this project.
- **AN UNCITED BAND CANNOT PASS OR FAIL A GATE.** Four have been retired on this rule. Introduce no
  fifth, and reconstruct no materiality bar (`docs/52` §7).
- **A NEGATIVE RESULT IS PUBLISHABLE HERE.** Failures are not embarrassments to be smoothed over —
  they are the spine of the narrative (§5).
- **Never quote a product of single-lever factors as a joint factor.** Standing instruction.
  Measured joint/product = **×1.34762**.
- **Never quote a load without its convention AND its `cp_revision`.**
- **YIELD EMBARGO** (`docs/23` §13.2): absolute flux only — t/day, Mt/yr, mg/L, m³/s.
  **No t/km²/yr anywhere**, in any cell, in any figure.
- **"CITED is not validated" and "fitted is not validated."** House rules (`docs/37` A1.6 item 3,
  `docs/43` §3.3 item 1).

## 3 — Hard prohibitions

- Do **NOT** `git commit` / `add` / `push` / `checkout`. The orchestrating session commits.
- Do **NOT** modify `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv`, or
  anything in `data/processed/sim_calibrated_v2/` (`h2e_drivers.npz`, `parameters_H2E.csv`,
  `q_gauge_H2E.npz`, `report_H2E.json`, `metrics_fleet.csv`). Read-only, always.
- Do **NOT** change an engine default — `ls2d_column`, `cp_revision`, `volume_convention`,
  `k_unit_system`, α, β, or any H2E parameter. A narrative pass changes **words and figures**,
  never the model.
- Do **NOT** run a calibration or a fit. Do **NOT** produce a new α̂.
- Do **NOT** edit a frozen document (`docs/33`, `35`, `42`, `45`, `46`) except through its own
  amendment slot — and prefer *reporting* what is owed over writing it.
- **Only ONE agent may own any given file.** Concurrent edits lose work.

**Check what a re-execute costs before you trigger one:** nb12/nb13 register a 7,200 s timeout,
**nb14 28,800 s**, nb15–19 `timeout=-1`. A part-way failure leaves the notebook **less executed
than you found it**. Budget deliberately and say in your journal what you chose not to run.

## 4 — THE KILL LIST: stale numbers that must not appear as current

Each is acceptable **only** inside a strike-through, a supersession table, or an
explicitly-labelled "RETIRED / superseded" block. Anywhere it reads as live, it is a defect. Grep
the generators, the executed notebook JSON, and 01–09.

| retired / superseded | replace with |
|---|---|
| `×0.333 – ×0.421` bracket | `f_LS ∈ [0.25146, 0.43194]` erosion-weighted |
| "our LS is 2.37× – 3.00×" | **2.3151× – 3.9768×** |
| α reference ≈ 3.9–5.0 · band ≈ 2.0–9.9 · hard stop ≈ 11.8–14.9 | `11.8·f` = 2.967–5.097 · `5.9–23.6·f` · `35.4·f` = 8.902–15.291 |
| proxy loads 104.8 / 82.8 / 126.1 / 99.7 Mt/yr | engine 129.3840 (hybrid V4) / **75.3235** (adopted V4_dg) |
| `min(m, 0.5)` called "Buarque eq. 14" | eq. 14 is the **step** 0.2/0.3/0.4/0.5 on `Sf` <1 / 1–3 / 3–5 / ≥5 **percent** (p. 47); the cap is **nobody's published formulation** and may NEVER be graded CITED |
| ±38 % Π band · SE 0.1644 ln · σ_r = 0.465 as a per-station residual sd | station bootstrap, `Π̂ × [0.29, 3.73]`; measured residual sd **1.9618 ln** (×4.22) |
| `k_min` 0.00216 / 0.0209 / 0.0104 /km · "2.12× over 348.4 km" | **0.0065–0.0069 /km**, "no sink **weaker** than ≈10× over ~342 km is detectable" |
| the "mountainous LS 2–10" band · the SDR 0.05–0.30 band | both **uncited and retired**; they pass and fail nothing |
| "the model is ~2× under-erosive" | **direction WITHDRAWN** (`docs/37` A1.9). Residual direction is **UNKNOWN** |
| any product of single levers as the joint | joint/product = **×1.34762** |

**Also now stale by event:** the engine default LS **moved** (ACT 2 switched `ls2d_column` to the
adopted `V4_dg` field). Any notebook printing LS levels or loads on the old default is out of date
— check each and say so.

**Known prose-vs-code contradiction, named in `CLAUDE.md`:** nb11's *prose* uses the older
CHIRPS-inclusive sense of "v2 forcing" and **contradicts its own code**. The code is what matches
disk. **"v2 forcing" means GAUGE-ONLY** — the zero-suppression repair plus deterministic IDW,
written to `model_inputs_v2/`. A CHIRPS-merged v3 **does not exist**. Canonical definition:
`docs/00_INDEX.md` → "Forcing versions — v1 / v2 / v3, stated once".

**Structural duplicates to adjudicate, not ignore:** `02_urh.ipynb` **and** `08_urh.ipynb` both
exist and both claim URH. Establish which is current, mark the other superseded in place (do not
delete), and record the decision. `06_data_inventory.html` is a stray export beside its `.ipynb` —
decide whether it is regenerable and say so.

## 5 — THE NARRATIVE YOU ARE BUILDING

This is the point of the whole pass. The notebooks currently read as a pile of separate exercises.
They should read as **one honest investigation** in which the project repeatedly tested its own
assumptions and repeatedly found them wrong — and arrived at a robust result on the one quantity
that survived.

1. **Inputs are not innocent.** Gauges were **zero-suppressed** — missing dry days recorded as
   absent, not zero — and value screens structurally cannot see missing data. Neighbour-ratio tests
   caught what per-station statistics missed. The IDW was **order-dependent** until fixed. Catchment
   areas proved unreliable per gauge in **both** implementations, which is why the yield embargo
   exists.
2. **The water model hits a data ceiling, not a parameter ceiling.** All three standing hypotheses
   for the El Niño failure were measured and **refuted** — one was **backwards**. The binding
   constraint is `r ≈ 0.57`, inherited from the rainfall field. H1 vs H2 could **not** be separated
   (gap 0.009 < seed spread 0.051); **H2E succeeded** and was adopted. The inherited caveat, stated
   not buried: **El Niño skill-over-climatology is −0.0005** — the dry phase sits *at* climatology.
3. **The one remaining rainfall lever was spent, and the diagnosis was wrong.** The CHIRPS merge was
   built; its LOOCV gate **passed** (r 0.447); its volume gate **failed twice** (+7.5 %); the
   registered repair was a **no-op** and the diagnosed cause was **wrong**. Later the last residual
   route was **bounded**: max **+0.006 r**. The ceiling is structural, closed with a number.
4. **Pre-registration earned its keep.** H-PEAK **refuted**. H2E-S failed 2 of its 3 conditions.
   Phase B closed a second time *on measured conflict*, not on preference.
5. **Uncited bands die.** The SDR 0.05–0.30 band and the "mountainous LS 2–10" band were both
   retired as uncited. Then `docs/46`'s **own** 0.1644 ln materiality bar was **STRUCK** — its
   stated derivation was falsified (measured SE 0.6936 ln). The project applied its own rule to
   itself.
6. **Defects behave unexpectedly when measured.** Defect A's reasoning was right and its consequence
   **nil** (×1.008878). Defect B was material but by a **different mechanism** than diagnosed. The
   levers **do not multiply out** (×1.34762). Two confident diagnoses, both partly wrong, both
   corrected by measurement.
7. **The LS formulation was settled from the printed source, not from a fit** — ADOPT-SOURCE at
   `buarque_2015_dg`, `f_LS` = 0.25146, all four levers CITED. It improved the sediment score from
   **−0.349 to −0.118 with no fitting at all.** Better physics beat tuning.
8. **The sediment level is not identifiable, and this is a result.** Π's design matrix has condition
   number **∞**; only the product is identifiable. The registered search **railed** at the box floor
   with a verdict computable **in advance** — so it was reported EXPLORATORY and **not adopted**.
   What the fit *wants* (α ≈ 0.48 against Williams' 11.8) is a **symptom of upstream
   over-production**, to be found and not offset. An independent second implementation of the same
   method on the same basin reached the same non-identifiability conclusion (`docs/59`).
9. **The gauge network cannot be grown.** Of 43 additional sediment sites recovered, **zero** have
   any discharge record. A physical limit of the monitoring network, not a processing gap.
   **66.53 %** of modelled erosion lies upstream of no usable station, and the basin's largest sink
   sits below the last one.
10. **And the deliverable survives all of it.** The ENSO contrast is a **ratio**, so every
    unidentifiable multiplier cancels **exactly**. Observed **22/22** stations, ~3–9×. Modelled
    **18/18**, median **3.05**. Robust across β {0.45, 0.56, 0.65} × both window pairs — 18/18
    direction in every cell.

**Write it so a reader understands why each failure mattered and what it changed.** Do not sand the
failures down, and do not dramatise them either. Every notebook should end knowing what it handed
to the next one.

## 6 — TASKS

### T1 — AUDIT FIRST, FIX NOTHING (read-only, parallel)
Produce, per notebook 01→19: its owning doc, what it currently claims, every kill-list hit with cell
index and whether it reads as live, every prose-vs-code contradiction, every cross-notebook
contradiction (where two notebooks state incompatible things), what its narrative role *should* be
per §5, and whether its executed outputs are stale relative to the current engine default. Deliver
one machine-checkable table. **Report a count of cells swept so the sweep is auditable.**

### T2 — FIX 10–19 THROUGH THE GENERATORS ONLY
One agent per generator, disjoint ownership. Edit `src/nbgen/make_nbNN.py`, regenerate, execute,
**verify from executed output**. Where you retire a number, keep it visible under a dated
"RETIRED / superseded — shown, not quoted as current" header, on the `docs/37` A2.7 strike-through
precedent — the record of what was believed is part of the narrative.

### T3 — FIX 01–09 DIRECTLY (no generators exist)
Same standard. Adjudicate the `02_urh` / `08_urh` duplication and the stray
`06_data_inventory.html`. These are the oldest notebooks; expect the most stale claims.

### T4 — CREATE THE MISSING NOTEBOOKS
There is **no notebook** for the work of `docs/55` (the C4.3 verdict — RAILED / EXPLORATORY),
`docs/56` (C5, the ENSO application that *succeeded*), `docs/57` (B5, the gauge-count physical
limit), `docs/58` (the rainfall-ceiling bound), or `docs/59` (the cross-implementation comparison).
At minimum build **nb20 — the C4.3 verdict and why a pre-computable search is not a test** and
**nb21 — C5: the modelled ENSO contrast, and why it survives a non-identifiable level**. Decide
with reasons whether `docs/57`–`docs/59` deserve their own notebook or belong as sections.
**Write generators (`make_nb20.py`, `make_nb21.py`) — do not hand-write notebooks in the ≥10
range** — and match the existing generators' structure, voice and
`reading(what=…, shows=…, means=…)` idiom exactly.

### T5 — VERIFY, FROM EXECUTED OUTPUT
Non-negotiable gates: **nb18 reproduces 299.5387**; **nb19 reproduces 299.5387 and 248.7298** and
all its integrity assertions pass (**33** as of 2026-08-13); `python3.10 -m pytest -q` →
**154 passed** (do not trust the stale "140" in older docs); `python3.10 src/report_h2e.py` →
**F = 0.25931 to 1e-8**; the basin-erosion gate at **299.5387088405831 Mt/yr**; the **3,266**
paired-day count. Re-verify that every generator still reproduces its committed notebook
source-identically. If a number moves, **STOP and report** — do not force it.

### T6 — ADVERSARIAL VERIFICATION (last; assume everything above is wrong)
At least three independent lenses, each defaulting to "this is wrong" and each required to check the
**artifact on disk** rather than a summary: (a) **surviving stale numbers** presented as current,
with a swept-count; (b) **cross-notebook contradictions** — does any pair still state incompatible
things, and does the chain of "what this hands to the next notebook" actually hold end to end?;
(c) **narrative honesty** — has any failure been softened, has any negative result been dressed as a
success, has any withdrawn direction crept back, is the yield embargo intact, and has a bar been
reconstructed anywhere. Send every CRITICAL/HIGH finding to a **separate refuter** whose default
posture is that the finding is wrong; a finding that cannot be independently confirmed must not
survive into a project document.

## 7 — Suggested phase plan

```
Phase 1  T1 audit, parallel, read-only                -> one contradiction table
Phase 2  T3 (01-09) || T2 (10-19, one agent/generator) -> disjoint file ownership
Phase 3  T4 build nb20/nb21 generators                 -> needs T1's narrative map
Phase 4  T5 verify from executed output
Phase 5  T6 lenses x3+, then refute each CRITICAL/HIGH
Phase 6  write docs/60 — the notebook coherence read-out
```

## 8 — Report back

1. Every contradiction found, and which are now fixed vs still open.
2. Every stale number retired, with the notebook and cell, plus the swept-count so coverage is
   auditable.
3. The notebooks created, and the reasoned decision on any you chose **not** to create.
4. Gate results: nb18/nb19 numbers, nb19's assertion count, pytest count, `report_h2e.py` F — each
   quoted **from executed output**.
5. Whether every generator still reproduces its notebook source-identically.
6. Anything you could not settle, named as an open item.
7. Files written/changed — **do not commit**; the orchestrating session commits.

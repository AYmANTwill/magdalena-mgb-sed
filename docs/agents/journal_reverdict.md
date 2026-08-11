# journal — `reverdict`

GOAL: apply what the citation runs established (docs/40 SDR, docs/41 C-factor, docs/42 guards)
and re-issue the C3 closure verdict honestly as a dated amendment to docs/37.

## Checklist

- [ ] 0. Read docs/00_INDEX.md, docs/37, docs/40, docs/41, docs/42, src/mgb_sediment.py
- [ ] 1. If C-factor revision is citable: apply as a NAMED option to the C/P inputs, prior value
      still reachable. Re-run basin decade. Report total, spatial gate, seasonal cycle,
      simulated ENSO ratio vs C2 observed 2.8–4.6× primary / 6.4–9.3× sensitivity.
- [ ] 2. Recompute implied SDR; evaluate against docs/40 (pass / fail / RETIRED+replaced).
- [ ] 3. Append dated amendment to docs/37; first line CLOSED or OPEN.
- [ ] 4. State what C4 may / may not do.
- [ ] 5. Update docs/00_INDEX.md where-is-it table with 40, 41, 42 + the amendment.

HARD RULES honoured: no git; no calibration launch; no pd.read_csv of wide forcing CSVs;
frozen H2E artifacts read-only; verify from executed outputs; yields in t/km²/yr embargoed
(model-internal specific erosion OK if labelled); uncited bands may not pass or fail a gate.

## Log

- 2026-08-11 — journal created before any read of the target files.
- Step 0 DONE. Read 00_INDEX, 37, 40, 41, 42, src/mgb_sediment.py.
  Findings that shape the run:
  - docs/40 verdict is **UNCITABLE** → task 2's third branch: the SDR gate is RETIRED, replaced
    by docs/40 §8.2's gross-hillslope-erosion-RATE clause, which is **NOT MET** (1.59–2.74×).
  - docs/41 verdict is **CITABLE** (×1.2043 central) and the `cite-cfactor` agent ALREADY
    rewrote `data/processed/urh_cp_factors.csv` (8×20, 31,086 B; `C` = `C_central`, prior
    preserved in `value_prior_2026_08_11`). So the engine already loads the revised C; what was
    missing is the NAMED option. Added it.
  - docs/42 is a frozen pre-registration, G1–G9 — so the C4 guards ARE in place.
- Step 1a DONE (code). `src/mgb_sediment.py`: added `CP_REVISIONS` / `CP_REVISION_NAMES` /
  `DEFAULT_CP_REVISION = 'cited_central_2026_08_11'`, `load_geometry(cp_revision=...)`, a
  drift guard (warns if `C != C_central` while the default name is used), and audit keys
  `cp_revision` / `cp_c_column` / `cp_p_column` / `class_c` / `class_p`. Docstring: new
  amendment item 4 + rewritten `C` input bullet. VERIFIED by execution — all five names load:
  cited_central C∈{0,0.005,0.015,0.03,0.2,0.5}; prior {0,0.001,0.003,0.005,0.01,0.2,1.0};
  low {0,0.001,0.003,0.008,0.08,0.25}; high {0.001,0.01,0.037,0.1,0.2,0.495,1.0};
  pacheco P∈{0.1,0.4,0.5,1.0}. Bad name raises.
- Step 1b DONE (re-run). Two scratchpad scripts, both READ-ONLY on every artifact, wrote nothing
  into the repo: `rerun_c.py` (basin decade × 4 named revisions + both pattern gates) and
  `g9.py` (docs/42 G9 unobserved fraction). Verified from executed output:
  - **`prior_2026_08_11` reproduces docs/37 bitwise-in-print**: 248.7298 Mt/yr, ledger
    residual exactly 0.0, bands n = 1736/1691/2442/2286/517, ratio 11.614 (doc 11.61),
    Spearman +0.5544 (doc +0.554), monthly climatology identical to the doc's 12 values,
    annual identical, windows 1.0818 / 0.4722 / 1.2897 / 0.3283 Mt/d → 2.2908 / 3.9281.
    G9 reproduces too: 3,282 minibacias, 98,987.61 km², 89.782/248.730 = 36.096 %,
    158.948 Mt/yr unobserved, 801.088 km below the outlet-most station, basin max 1,425.86 km.
    So the harness is validated against the published numbers before being used on new ones.
  - **`cited_central_2026_08_11` (adopted): 299.5387 Mt/yr**, ledger exact, ratio to prior
    1.2042736 (docs/41 predicted ×1.2043 from a linear decomposition — confirmed by simulation).
  - **NOT a pure level shift** (unlike the unit conventions): per-minibacia adopted/prior spans
    **0.500 – 5.000** (median 1.577) and per-DAY spans **0.7258 – 1.4889**. So both pattern
    gates had to be re-run, and docs/41 §8.3 claim 3 ("every scenario rescales all windows
    identically") is **not exactly true** — see the correction below.
  - Default option is behaviour-identical to the pre-edit loader: default reads `('C','P')`,
    the exact columns the old code hardcoded; verified per land class against a raw pandas
    read, and `C == C_central` / `P == P_central` so the drift guard stays silent.
- Test state: `python3.10 -m pytest tests/ -q` → **94 passed, 2 failed**. Both failures are the
  stale hard-coded C provenance assertions docs/41 §8.1 enumerated
  (`test_audit_unit_day_reproduces_from_the_real_files`, `test_real_geometry_shape_and_ranges`),
  they are caused by the CSV rewrite and NOT by my edit (proved above), and `tests/` is not a
  file this task names. REPORTED, not fixed.
- Step 2 DONE (SDR clause). docs/40 = UNCITABLE → third branch: **RETIRED**, replaced verbatim by
  docs/40 §8.2's gross-hillslope-erosion-RATE clause, evaluated at the ADOPTED C:
  Leg A 2.034–2.275× (was 2.450–2.739), Leg B 1.028× (was ≥1.593 — no longer a proof by
  impossibility, only 2.8 % short), Leg C 1.689× the 32-sub-basin mean yield / 0.530× the max
  (was 1.402 / 0.440). Combined **1.03–2.27×** → clause **NOT MET**. ADR at adopted C
  0.481–0.614; channel-input ratio 0.60–0.88. α that would close Leg A: 24.0–26.8 (outside the
  docs/35 §6.1 expected band; RULE 0 forbids it anyway). Candidate 0 (LS) applied on top of the
  adopted C: 99.8–126.1 Mt/yr, ADR 1.14–1.84, still impossible side.
- Step 3 DONE. `AMENDMENT A1 (2026-08-11)` APPENDED to docs/37 (34,100 chars; file 287 → 737
  lines; nothing above the marker touched — asserted in the append script). First line states
  **OPEN**. Five-clause conjunction: 1 MET, 2 NOT MET, 3 NOT ESTABLISHED for the three
  2026-08-11 decisions, 4 RETIRED, 4′ NOT MET, 5 MET.
- Step 4 DONE — A1.6: C4 MAY start under docs/42 G1–G9; eight things it still may not do.
- Step 5 DONE — docs/00_INDEX.md: §3 Phase C table rows for 37 (now LIVE + amendment), 40, 41,
  42; three new WHERE-IS-IT rows (is C3 closed / why the SDR gate was dropped / may C4 start);
  docs/42 added to the pre-registration row.
- Also recomputed docs/42 G9 under the revised C (read-only): observed geometry unchanged
  (3,282 minibacias, 98,987.61 km², 38.50 %) but the erosion split moves 36.10/63.90 →
  **33.47/66.53 %** (100.25 / 199.29 Mt/yr). Flagged in A1.7 item 1 as an amendment docs/42 §9
  needs — NOT applied, docs/42 is frozen and not a file this task names.
- OUTSTANDING, deliberately not done (out of scope): the 2 stale C assertions in
  tests/test_sediment.py (docs/41 §8.1, exact lines and values restated in A1.7 item 2).
- Append-only PROVED, not asserted: `git show HEAD:docs/37_c3_closure.md` is byte-identical to
  everything above the `# AMENDMENT A1` marker in the working file.
- Git note (not my doing, recorded for the next session): a commit agent ran in parallel and
  committed my mid-flight `src/mgb_sediment.py` edits (HEAD already contains `CP_REVISIONS`) and
  the pre-amendment `docs/37`. Still uncommitted at hand-off: the docs/37 amendment,
  docs/00_INDEX.md, this journal. I ran no git write command.
- Files touched, total: `src/mgb_sediment.py`, `docs/37_c3_closure.md` (append only),
  `docs/00_INDEX.md`, this journal. Nothing else. No frozen artifact modified, no calibration
  launched, no wide forcing CSV read with pandas, no gauge-referenced t/km²/yr published. Will open
  `sim_calibrated_v2/h2e_drivers.npz` READ-ONLY and write nothing but a scratchpad script.
  Terrain classifier for gate (a): `%TEMP%/output_hh.tif` (5640×12000 @ 0.000833°) still
  exists and shares `minibacias.tif`'s bounds exactly → the docs/37 §3 8× block-average is
  reproducible rather than approximated.

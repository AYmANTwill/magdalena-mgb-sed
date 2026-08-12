# journal — nb19

**Agent slug:** `nb19`
**Started:** 2026-08-11

## Goal

Write `src/nbgen/make_nb19.py` → `notebooks/19_c3_gate_and_c4_setup.ipynb`, documenting the
C3 adjudication (SDR gate retirement, the ratio question, what α is for, C4 feasibility,
the decision) and the C4 setup, for a reader who was not in the room.

## Checklist

- [ ] 1. Read sources: docs/37 (+A1/A2), 40, 41, 42, 43, 45, journals adj-ratio /
      adj-alpha-role / adj-c4-feasibility / decide-c3-c4, `src/mgb_sediment.py`, C4.1
      transport work if present.
- [ ] 2. Read `src/nbgen/make_nb18.py` to copy its structure exactly.
- [ ] 3. Inventory the numbers I may quote, and where each comes from (executed output or a
      numbered doc — never prose-only).
- [ ] 4. Write `src/nbgen/make_nb19.py`.
- [ ] 5. Emit + execute the notebook with nbconvert (timeout -1).
- [ ] 6. Verify from executed outputs: 0 errors, every figure has the three-part reading.

## Constraints I am operating under (restated so violations are auditable)

- No git add/commit/push. No calibration search. Frozen artifacts read-only.
- Never `pd.read_csv` the wide forcing CSVs — use `src/forcing_npy.py`.
- Gauge-referenced t/km²/yr yields EMBARGOED; model-internal specific erosion OK if labelled.
- Uncited plausibility bands may neither pass nor fail a gate — say UNCITED.
- Any decision gets recorded HERE before I compute what it does to a headline number.

## Log

### Step 0 — journal created (first action)

Created before reading any source. Nothing computed yet.

### Step 1 — sources read (checklist 1 DONE)

Read in full: `docs/00_INDEX.md`, `docs/43_c3_c4_gate.md` (the adjudication — the centre of this
notebook), `docs/45_c4_preregistration.md` (C4.2, frozen 2026-08-11), `docs/40_sdr_evidence.md`
§0–§9 (615 of 728 lines; the NEH Table 6-2 partition and the retirement argument),
`docs/42_c4_guards.md` §4 (the `Lw` ladder, σ_r, k_min, composition leverage, §4.5 coverage),
`docs/37_c3_closure.md` §1–§3 (factor chain, the struck SDR sub-section, the two pattern gates),
A1.3 (the C revision + re-run), A1.9 (which quantity is the MUSLE sum). Journals:
`journal_adj-ratio.md`, `journal_adj-alpha-role.md`, `journal_adj-c4-feasibility.md`,
`journal_decide-c3-c4.md`, `journal_c41-transport.md` (C4.1 exists: `src/mgb_transport.py`).
`src/nbgen/make_nb18.py` for the generator structure (`md`/`code`/`reading` helpers, the emit
block, the final integrity-assertion cell) — nb19 follows it exactly.

**One thing the brief carries that the record supersedes, and I follow the record.** The task
brief states the replacement test "FAILS: the model is UNDER-EROSIVE by 1.03–2.27×".
`docs/37` **A1.9** (written after A1, same day) **WITHDRAWS that direction**: clause 4′ → 4″,
status NOT ESTABLISHED, residual direction **UNKNOWN** across 2.27× too low (reading A) to
1.49× too high (reading B). `docs/43` §1.1 restates it as the single most commonly misquoted
number in the project. The notebook therefore documents the residual as **sign-unknown** and
says so explicitly, in its own section. This is the same call `decide-c3-c4` made.

### Step 2 — DECISIONS, recorded BEFORE computing anything they bear on

*Written and saved before `src/nbgen/make_nb19.py` existed and before any number was computed in
this session beyond the two probe runs disclosed in step 3. I state explicitly that I am
recording them first.*

- **D1 — what the notebook computes vs what it quotes.** Anything cheap and reproducible is
  **recomputed from the artifacts** and the reproduction is shown (the factor chain from the
  engine's own named constants; the basin decade at both `cp_revision`s; the station funnel from
  `sediment_inventory_qc.csv` + `sediment_daily_qc.csv` + `discharge_daily.csv`; the β-compression
  algebra; every k_min / SE / band arithmetic). Anything that would require re-fitting, re-running
  a search, or re-reading the two source PDFs is **quoted from its numbered document or lens
  journal, cited in place**, and labelled as carried. No number is taken from prose alone where an
  executed path exists.
- **D2 — no hydrology, no search, no frozen write.** `h2e_drivers.npz` is opened **read-only**
  through `mgb_sediment.load_drivers`. `parameters_H2E.csv` and `q_gauge_H2E.npz` are not opened.
  No calibration is launched. Nothing under `data/` is written.
- **D3 — the direction of the C3 residual is reported as UNKNOWN** (see step 1). The bracket
  2.27× low … 1.49× high is drawn as a bracket, never as a shortfall, and the notebook says in
  its own words that the reading which flatters the project (B) is the one the record refuses to
  adopt.
- **D4 — uncited quantities are drawn but never used as a gate.** The 0.05–0.30 SDR band and its
  implied k ≈ 0.0020–0.0032 /km appear on figures **labelled UNCITED**, as scale references only;
  no figure caption or reading lets them pass or fail anything. Same for the retired
  "mountainous LS 2–10".
- **D5 — the embargo.** No gauge-referenced t/km²/yr anywhere. The model-internal specific-erosion
  figures (1,445.32 / 77.41 / 1,165.08 t km⁻² yr⁻¹) are quoted **only** with the words
  *model-internal* in the same sentence, exactly as `docs/37` A1.3.3 labels them.
- **D6 — figure inventory fixed in advance** (so the count is not chosen after seeing which ones
  came out well): §1 the factor-chain waterfall, the NEH Table 6-2 partition, the two-readings
  bracket; §2 the cancellation demonstration, the lens-1 forest plot + heterogeneity, the
  like-for-like correction, the β-compression curve, the contrast ladder; §3 the 426 published
  fits against the guard band and the source prior, the guard-on-its-own-source verdict split,
  the α overlap that blinds `docs/35` §6.1, the equifinal ridge; §4 the station funnel, the
  observations-to-parameters denominators, the identifiability panel, the coverage bars, the
  longitudinal ladder; §6 the sources MUSLE omits, the period-dependent peak deficit. Every one
  gets the three-part reading; every threshold or band is drawn as a line or a shaded band.
- **D7 — audience.** Every technical term is defined in plain language at first use, before any
  formula, in §0.2; every code cell is preceded by a markdown cell carrying the equation in LaTeX
  with every symbol defined **with units** and the named data source of each input.


### Step 3 — probe runs (disclosed; these are reproductions, not new science)

Two read-only probes, run to confirm the notebook's computed cells will execute and reproduce
documented numbers before the generator was written:

1. **Station funnel**, from `sediment_inventory_qc.csv` + `sediment_daily_qc.csv` +
   `discharge_daily.csv` (3.0 s): 79 classified → **28** mapped → **18** mapped-and-usable →
   **13** tributary → **9** with ≥1 non-deleted CAL SSC observation → **8** with ≥1 paired
   SSC+observed-Q day. Per-station paired CAL days 845 / 661 / 637 / 477 / 213 / 176 / 145 / 112,
   total **3,266** — reproduces `journal_adj-c4-feasibility.md` §3.1 and `docs/45` §3.4 exactly.
2. **Sediment engine**, `load_geometry()` + `load_drivers()` + `simulate_sediment(store_daily=False)`
   (3.3 s): basin total **2,994,977,042.2609434 t** over 3,652 d = **299.5387088 Mt/yr** —
   reproduces `docs/37` A1.3.2's 299.5387 exactly. `h2e_drivers.npz` read-only.

No headline number moved. Both are checks that an existing published number is reproducible.

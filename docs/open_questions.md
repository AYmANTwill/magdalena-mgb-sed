# Open questions (decisions to lock with the advisor)

These three decisions gate the project. Until resolved, downstream work carries risk.

## Q1 — IDEAM sediment stations on the Magdalena (HIGHEST RISK)

**Question:** Which suspended-sediment stations exist on the Magdalena, where, and for which periods?
**Why it matters:** Without sediment calibration data, the sediment model cannot be calibrated — **no data, no project.**
**Action:** Search the **DHIME** portal (`https://atencionciudadano.ideam.gov.co/`) for sediment stations; check
record length and overlap with the candidate ENSO years.
**Update (2026-07-27):** literature scan confirms an extensive IDEAM suspended-sediment network (30–40+ sites), with
**Calamar** (downstream reference, ~10.25° N, records to ~2010) and **Puerto Berrío** (mid-basin, codes 23095010 /
23090110) as key gauges; data are free on DHIME. See `06_ideam_stations.md`. Risk downgraded red → amber/green.
**Remaining check:** confirm suspended-sediment coverage for **2011** and **2015–2017** directly on DHIME (sediment is
sampled less often than discharge).
**Update (2026-07-28) — DHIME investigated (pivotal):** **Calamar [29037020]** is on the Magdalena but Limnimétrica —
discharge only, **no suspended-sediment series**. **No lower-Magdalena mainstem station** has sediment covering both
2011 and 2015–2016. Rich sediment records covering both years exist only on the **Sierra Nevada / Ciénaga Grande de
Santa Marta rivers** (Fundación [29067120] 2002–2026; Puente Ferrocarril/Aracataca [29067130] 1984–2025) — not the
Magdalena. See `progress_journal.md` for Paths A/B/C.
**Status:** DECISION REQUIRED with advisor — sediment data does not exist on the lower Magdalena for the study years;
choose Path A (calibrate-then-simulate), B (shift years), or C (pivot to the Ciénaga Grande rivers).

## Q2 — Confirm the study years

**Question:** La Niña **2011** vs El Niño **2015–2016** or **2017**?
**Why it matters:** Determines forcing periods and the availability window of observed discharge/sediment data.
**Constraint:** The chosen El Niño year must have adequate IDEAM coverage (ties to Q1).
**Update (2026-07-27):** ONI classification (see `07_enso_years.md`): 2010–2011 = **strong La Niña**;
2015–2016 = **very strong El Niño**; **2017 = weak La Niña / neutral, NOT El Niño**. Recommend
**La Niña 2011 vs El Niño 2015–2016** (drop 2017). Cleanest strong opposite-phase contrast in the recent record.
**Status:** RECOMMENDATION READY — 2011 vs 2015–2016, to approve with the advisor.

## Q3 — Whole basin or sub-basin?

**Question:** Model the entire Magdalena, or a sub-basin?
**Why it matters:** The full Magdalena at 30 m exceeds IPH-HydroTools' **~250 M cell** limit
(~257,000 km² → ~285 M cells; the 30 m ceiling is ~225,000 km²).
**Options:** (a) sub-basin at 30 m; (b) whole basin at coarser resolution; (c) whole basin tiled.
**Working decision (2026-07-27):** target = **whole Magdalena** (as stated by the advisor: "el río Magdalena");
build and validate the full MGB-SA workflow on a **substantial Andean pilot** first — upper + middle Magdalena down
to a mid-basin gauge (~Puerto Berrío / Barrancabermeja), ~80,000–110,000 km², at full 30 m (well under the limit) —
then scale to the whole basin (coarser resolution or tiling). Exact pilot outlet to be fixed when the calibration
gauge is chosen from IDEAM. **To confirm with the advisor.**
**Status:** DECISION PROPOSED — pilot-first at 30 m; full-basin scaling method still to confirm.

## Framing for the EMINES defense

- **Research component** (evaluated by UMNG via the report): the modelling + comparison above.
- **Human-experience component**: a focused Colombia/Morocco comparison on a specific dimension (to define).

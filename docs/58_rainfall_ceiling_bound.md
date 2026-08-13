# 58 — The 139 rain-selective gauges: the last rainfall lever, quantified and closed

**Written 2026-08-12. The one surviving untested hypothesis on the r ≈ 0.57 rainfall ceiling
(`docs/18` §15.5, §9.3): that repairing the 139 residual rain-selective gauges — upstream of the
CHIRPS merge — could unlock a usable satellite blend and lift the ceiling.** This note does **not**
attempt the repair; it computes the **upper bound** on what the repair could achieve if it
succeeded perfectly, and finds it negligible. Harness: an arithmetic bound on `docs/18` §15.2's own
LOOCV numbers and the v2 isolation distribution.

## 1 — The hypothesis, and why a bound settles it without the multi-hour pipeline

The zero-suppression repair fixed the gauges it could, but a threshold left **139 of 294** still
reporting rain-selectively (`docs/18` §9.3). Their missing dry days are *"not in the record at
all"* (§15.5), so they inflate the gauge field's volume — which is exactly why the CHIRPS merge
failed its volume gate by **+7.5 %** (§15.3). The stated surviving route: repair the 139 first,
then the merge becomes usable.

But the merge's *value* was already measured by LOOCV (§15.2), and it is small and **signed by
isolation**: it helps only where gauges are moderately far, and hurts where they are very far. So
the ceiling on the whole route can be computed directly — no repair, no v3 forcing, no re-run
needed.

## 2 — The bound

`docs/18` §15.2 LOOCV (median daily precip r), by gauge-isolation band, and the v2 per-minibacia
isolation distribution (`forcing_minibacia_provenance_v2.csv`, median 16.3 km, max 71.5 km):

| isolation band | merge behaviour | Δ median daily r | share of basin (area) |
|---|---|--:|--:|
| < 10 km | pure gauge IDW (unchanged) | **0.000** | 25.8 % |
| 10–30 km | gauge/CHIRPS blend | **+0.023** | 57.1 % |
| > 30 km | pure mapped CHIRPS | **−0.043** (0.300 vs 0.343) | 17.1 % |

Area-weighted basin-mean change: **Δr = +0.0058** (count-weighted +0.0057). The +0.023 over 57 %
of the basin is very nearly cancelled by the −0.043 over 17 %.

## 3 — The verdict

**Even the perfect-case ceiling of this entire route is r 0.57 → ~0.576 — a +0.006 improvement in
the *precipitation* field's daily correlation.** Two reasons it is, if anything, optimistic:

1. it assumes the 139 repair **fully succeeds** and the merge is adopted at every cell — neither is
   established, and the repair carries an over-drying risk the existing repair had to threshold
   against;
2. it is a **precipitation-field** r gain; discharge r (the 0.57 quantity) integrates and smooths
   the precip field, so the hydrology gain is **≤ +0.006**, not equal to it.

So the 139-gauge route **cannot lift the r ≈ 0.57 ceiling** in any material way. The ceiling is
structural — a sparse gauge network plus low CHIRPS point skill (raw r 0.31, nb10) — and the
satellite blend that the repair would unlock helps and hurts in nearly equal measure. **The last
rainfall lever is closed-negative, now with a number** (`docs/22` §4.7's ceiling stands, and this
note explains *why it cannot be moved with the available data*).

## 4 — What this means for the study

The r ≈ 0.57 ceiling — and therefore the weak absolute sediment KGE (`docs/55`) and the
dry-phase-at-climatology result (`docs/26` addendum A.5) — is **not a solvable data-processing
problem**; it is the information content of the observations. This is a finding to *state*, not a
gap to apologise for: the ENSO-contrast conclusion (`docs/34`, `docs/56`) is carried on quantities
that survive the ceiling, and the ceiling itself is now bounded rather than merely asserted.

## 5 — Disclosure

Arithmetic only, on `docs/18` §15.2's committed LOOCV and `forcing_minibacia_provenance_v2.csv`.
No forcing regenerated, no gauge repaired, no notebook run, no default moved. The 139 repair
remains **untested by construction** — this note shows it is **not worth testing**, which is a
different and stronger statement than "not yet tested."

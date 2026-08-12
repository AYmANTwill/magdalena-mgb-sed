# Journal — task B5: replace the ±38 % Π band

Agent: `debt-b5-piband`. Started 2026-08-11.
Task: docs/47 §6.1 repair **B5** — the ±38 % Π band and the `k` power numbers sit on a
noise floor (σ_r = 0.465 ln) measured 3.9–4.2× too low. Reproduce independently, choose a
defensible replacement band, restate the `k` bound, list every published number that moves.
Deliverable: `docs/48_pi_band_revision.md`. Must NOT edit docs/42/43/45.

## Log

### 1 — orientation (done)
Read: CLAUDE.md, docs/00_INDEX, docs/47 (whole), docs/42 §4 (the σ_r registration + power
table), docs/43 §3 (the reuse as per-station residual sd), docs/45 §2.2/§2.3/§3.1/§4.2 (G12,
bootstrap convention)/§5.3/§6.2/§7.1.

The defect confirmed **by reading** (before any measurement):
- docs/42 §4.2 defines σ_r as `0.658/√2 = 0.465`, where 0.658 = `sd[ln(a/b)]` across the 32
  station-windows where BOTH observed-flux estimators are admissible. That is an
  **observed-flux estimator-disagreement** sd. Neither estimator sees the model.
- docs/43 §3.2 then writes "SE of the fleet-mean level = 0.465/√8 = 0.1644 ln = ±38 %", i.e.
  treats σ_r as the sd of the **model–observation** log residual across stations.
- docs/45 §2.2 (table row), §2.3 (the k bound "≈2.12× over 348.4 km"), §4.2 G12 (the
  "registered 95 % level band of ±0.322 ln (±38 %)"), §5.3, §6.2 item 2, §7.1 (yardstick card)
  all inherit it.
Two different quantities: estimator noise on the observation vs total residual (model error +
observation error + heterogeneity). The second is necessarily ≥ the first.

Next: find the artifacts needed to recompute the CAL-8 per-station residuals.

### 2 — independent reproduction: DONE, both gates pass, numbers match exactly
Scripts (scratchpad, read-only on the repo): `b5_run.py` (engine + upstream accumulation,
caches `b5_station_daily.npz`), `b5_stats.py` (all statistics).
- **GATE 1** basin gross erosion **299.5387088 Mt/yr**, ledger `exact=True` — docs/37 A1.3.4's
  299.5387 to 7 s.f.
- **GATE 2** CAL-8 paired SSC+Q day count **3266** — docs/45 §3.6's registered denominator.
- Model up-areas reproduce docs/42 §4.1's printed column at all 18 stations.
- **Measured**: CAL 8, CAL window 2012–14, estimator (b), `r_i = ln(sim) − ln(obs)`:
  **sd = 1.9618 ln**, **SE = 0.6936 ln**, **×4.22 σ_r**. Identical to docs/47 §2.2.
  obs/sim spread 0.0099–4.0766 = factor **412.1**. Also reproduced: CAL-8 ENSO-window-median
  sd 1.7159 and all-18 1.4175 (the earlier passes' 1.7118/1.4202, 0.2 %).
- **G12 LOO range of ln Π̂ = 0.8602 ln** vs the registered ±0.322 (full width 0.644) — fires.

TRAP HIT AND FIXED (recorded so a successor does not repeat it): `topology.npz:topo_order_idx`
is **the ordered list of indices** (headwater-first), NOT the rank of each index. Iterating
`np.argsort(topo_order)` gives a wrong partial accumulation and an outlet column that does not
equal the basin total. The control `acc[:, outlet_idx].sum() == E_mini.sum()` catches it
(rel err 1.0 before, 0.0 after). Keep that control in any successor script.

SIDE OBSERVATION (independent corroboration of the refuter's): my recomputed `Lw` disagrees with
docs/42 §4.1's printed table at several stations — IRRA **289.14** vs 265.2 (+9 %), BANANERA
**24.19** vs 26.9, CAPITANEJO **64.15** vs 60.4, ARRANCAPLUMAS **344.21** vs 348.4. I reproduce
`journal_refute-gate-logic`'s IRRA 289.1 to 4 s.f. Immaterial to k_min (Sxx moves ~1 %) but
someone should reconcile it. Not a B5 finding.

NEXT: (i) est (a) with EL ALAMBRADO KEPT (docs/45 §3.4 keeps it in the objective; the
flow-selective flag only bars it as a C2 *window-mean* estimator) — the earlier passes' est (a)
n=7 drops it, which is the C2 rule, not the C4 rule; (ii) the all-18 joint-regression residual
sd, which is what G1.2's k_min actually needs; (iii) the bootstrap band.

### 3 — the replacement band chosen, and why (b)
ROUTE 2 (station bootstrap) adopted; ROUTE 1 (G12's LOO range) REJECTED on two measurements:
 (i) jackknife identity — jackknife SE of the 8 LOO refits = **0.6936** = sd/sqrt(n) exactly, and
     LOO range = range(r_i)/(n−1) = 6.0214/7 = **0.8602** exactly. So route 1 is either the
     corrected-σ normal band under another name, or a *range*, and range→95 % band needs an
     uncited constant. docs/40's rule forbids that.
 (ii) it makes G12 circular. MEASURED: G12 FIRES against the registered ±0.322 (0.8602 > 0.6445)
     and does NOT fire against either corrected band (2.5667 bootstrap / 2.7190 normal).
     **Correcting the band switches G12 off.** Recommendation in docs/48 §3.2: keep 0.644 ln as a
     standalone fragility threshold decoupled from the level band.

Bands measured (seed 20260810, 10,000 station resamples, CAL 8, CAL window):
  est (a): point +2.5772 ln, CI about point [−0.8279, +0.8721] → level **x0.418 – x2.289**
  est (b): point +1.9240 ln, CI about point [−1.3163, +1.2503] → level **x0.286 – x3.730**
  normal ±1.96·SE for comparison: est (a) ±0.9359 → x0.392–2.550; est (b) ±1.3595 → x0.257–3.894
  (docs/47's "0.257x–3.894x" reproduces exactly)
Recommended reporting: the UNION **x0.29 – x3.73**, labelled a convention not a claim.

### 4 — k bound (c)
All-18 G1.2 JOINT form [1|Lw|shG|shB|lnLS̄], ENSO medians est (b), predictors recomputed:
  resid sd **1.4955** ln, SE(k̂) **0.00350**, k_min **0.00686 /km ⇒ 10.41x over 341.5 km**.
  On docs/42's own printed Lw: 0.00694 ⇒ 11.02x. Intercept-only: 0.00648–0.00658 ⇒ 9.2–9.7x.
  ⇒ **"no sink weaker than ~10x over ~342 km is detectable"**. Registered: 2.12x.
CAL-8 form: **0.0838 /km ⇒ 173x** over 61.5 km (0.0883 ⇒ 164x on docs/42's Lw).

NEGATIVE RESULT: docs/47 §2.2's "k_min CAL-8 form = 0.0130 /km" does NOT reproduce and is
impossible as labelled (k_min ∝ σ; a 4.22x larger σ cannot shrink k_min below 0.0209 on the same
design). TRACED: it is the **10-station CAL-window set incl. ARRANCAPLUMAS** = 0.01230 /km, of
whose Sxx ARRANCAPLUMAS supplies **87.6 %**. Without it: 0.0799. ARRANCAPLUMAS is an EVAL station
(docs/45 §2.4). **docs/42:804 (§9.5's mandatory pointer) has already copied the wrong number.**

### 5 — the biggest downstream consequence (d)
docs/46 uses 0.1644 ln TEN times as a **decision threshold** (materiality bar + Branch A/B
Δ_shape). Measured: at the corrected est-(b) SE (0.6936 = factor 2.001) the bar would declare
the W&S-1978 S lever (0.5272), the DG/continuous L ratio (0.5435) and the m-cap (0.6587)
**immaterial** — three of the levers docs/46 exists to adjudicate. At the bootstrap half-widths
all but one f_LS endpoint goes immaterial. ⇒ **docs/46 must DECOUPLE its bar, not rescale it.**
docs/48 offers NO replacement bar (that would be inventing one) and points at O6 (Δ_shape unrun).
What survives: both f_LS endpoints (|ln| 0.8395 / 1.3805) stay material at both corrected SE
bars, so docs/47 §4.3's bracket and its BLOCKED verdict are NOT weakened.

### 6 — DONE. docs/48_pi_band_revision.md written. Nothing else in the repo touched.
Scratchpad scripts kept: b5_run.py, b5_stats.py, b5_predictors.py, b5_final.py, b5_extra.py
(+ b5_station_daily.npz, b5_predictors.csv, b5_station_cal.csv, b5_station_enso.csv,
b5_bands.json). They are the only reproduction path; docs/00 §6 records scratchpad-only code as a
known loss mode, so a successor who needs them should promote them to scripts/ before they rot.

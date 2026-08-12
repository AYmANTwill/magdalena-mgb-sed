# Journal — adversarial refutation: "the fit-set-implied α ≈ 0.85–1.14 is below C4's box floor"

Agent: `refute-gate-logic` (α-level finding). Started 2026-08-11.
Posture: assume the finding is WRONG; try to prove it.

> **FILENAME COLLISION.** The orchestrator assigned me `docs/agents/journal_refute-gate-logic.md`,
> but a *different* refutation agent (target: the σ_r = 0.465 finding) had already written that
> file and my first write clobbered it; it re-appeared with the σ_r content. I therefore moved to
> this uniquely-named file so neither agent's evidence is lost. Successors: the σ_r refutation
> lives in `journal_refute-gate-logic.md`, the α-level one here.

## The finding under attack (verbatim core)
> docs/43 §2.1 classifies the multiplicative level as a CALIBRATION TARGET owned by "C4, as a
> fitted Π", but on the achievable CAL 8, at exactly the configuration C4 registers
> (k = 0, C at docs/41 central, α = 11.8), the observed/simulated flux ratio has geometric mean
> 0.0721 (a) / 0.0966 (b), so the level the objective will drive toward corresponds to
> α ≈ 0.85–1.14 — below docs/45 §2.1's box floor 2.0 and below docs/35's hard stop α < 3.9.
> Predicted outcome: FAIL–RAILED at α = 2.0.

Origin: `docs/agents/journal_verify-gate-logic.md` item 3, computed from the adj-ratio lens's
scratchpad artifact `adj_ratio_station_window.csv`.

## Attack lines
1. **Arithmetic** — do the CSV's numbers actually give 0.0721 / 0.0966?
2. **Window** — the artifact's four windows are P-LN/P-EN/S-LN/S-EN. docs/45 §3.5 registers the
   fit window as **CAL 2012-01-01…2014-12-31**, which is *none of them*.
3. **Estimand** — docs/45 §3.1 registers `KGE_ln` with `m = mean(ln y)/mean(ln x)`. Its level
   optimum is `exp(mean ln obs − mean ln sim)` = a **log-mean** ratio, NOT the ratio of window
   **arithmetic** means the artifact computes. Simulated flux ∝ Qsur^{2β} is far spikier than
   observed, so these two ratios need not agree — possibly by a lot.
4. **Parameter count** — the finding fixes β = 0.56. docs/45 registers β **free** in [0.40, 0.75].
   `ln sim = ln α + β·ln(product) + const`, and `ln(product)` is a large number, so β moves the
   LEVEL enormously; α̂ is not `11.8 × r`.
5. **Aggregation** — geometric mean over 8 stations is not what `F_search` (mean KGE) or
   `F_report` (median KGE) optimise.

## Log
- [t0] Read CLAUDE.md, docs/00 index listing, docs/43 §1–§3, docs/45 §2.1/§3/§6/§7,
  journals `adj-ratio` and `verify-gate-logic`. Located the artifact + the generating script
  `adj_ratio.py` in *this session's* scratchpad
  (`.../3d81998f-30ab-4e88-ba3e-09f1f28fae62/scratchpad/`).
- [t1] Confirmed docs/45 registered facts that the finding must be tested against:
  - §3.1 objective `KGE_ln(s) = 1 − sqrt((r−1)² + (v−1)² + (m−1)²)`, `m = mean(y)/mean(x)`,
    x = ln obs, y = ln sim in t/day.
  - §3.2 `F_search` = **mean** KGE over CAL 8; `F_report` = **median**.
  - §3.3 fitted on estimator **(a)** (paired sample days). (Finding calls (a) "the registered
    fitting estimator" — CORRECT.)
  - §3.4 CAL 8 = exactly the eight codes the finding lists. CORRECT.
  - §3.5 CAL window = **2012-01-01…2014-12-31**; P-LN/P-EN/S-LN/S-EN are **strictly out of
    sample**. The finding's number is computed on the out-of-sample windows only.
  - §7.1 free parameters **2**: α ∈ [2.0, 30.0] AND **β ∈ [0.40, 0.75]**.
- [t2] Next: recompute the CSV aggregation, then measure the actual estimand on CAL 2012–14.

### ATTACK 1 — arithmetic. FAILED (the finding reproduces).
Recomputed the station medians of `a_r` / `b_r` over the four windows in
`adj_ratio_station_window.csv`, restricted to the CAL 8:

| aggregation | est (a), n=7 | est (b), n=8 |
|---|---|---|
| geo-mean of station **medians** | 0.07474 → α 0.882 | 0.09905 → α 1.169 |
| geo-mean of station **geo-means** | 0.07629 → α 0.900 | 0.09424 → α 1.112 |
| **median** of station medians | 0.04807 → α 0.567 | 0.11035 → α 1.302 |
| Σobs/Σsim over station-windows (flux-pooled) | 0.30742 → **α 3.628** | 0.27896 → **α 3.292** |

Finding says 0.0721 → 0.85 (a) and 0.0966 → 1.14 (b). I get 0.0747 → 0.88 and 0.0990 → 1.17.
Agreement to ~3 %; the two per-station medians it quotes for `23127010` (0.736 vs my 0.7697) and
`24037390` (0.354 vs my 0.3724) differ slightly, immaterially. **Only** the flux-pooled
aggregation lands near the box floor — and docs/45 §3.1 explicitly *rejects* the untransformed
(flux-weighted) objective because it "would fit the level of BORBUR and CAPITANEJO and nothing
else". So the one aggregation that would rescue docs/43 is the one docs/45 forbids.

### ATTACKS 2–5 — measured, on the registered window, with the registered objective. ALL FAILED.
Script: `<scratchpad>/refute_alpha_level.py` (read-only; nothing written to the repo; no
calibration launched). Observed side = docs/45 §3.3 estimator (a) exactly
(`Qs = Q·SSC·0.0864`, `c1_deleted == False`, same-day `q_m3s`), window = docs/45 §3.5 **CAL
2012-01-01…2014-12-31**. Simulated side = the adj-ratio lens's D1 construction
(`ms.load_geometry` default `cp_revision='cited_central_2026_08_11'`, `SedParams()`, τ=0,
upstream D8 sum of `delivered_t_day`).

**TWO REPRODUCTION GATES PASS**, so neither side is my own invention:
- basin gross erosion over the full 2009–2018 record = **299.5387088 Mt/yr** vs `docs/37`
  A1.3.4's **299.5387** — exact to 7 s.f.;
- CAL-8 paired-day count = **3,266**, exactly `docs/45` §3.6's registered denominator.
  Per-station n = 637/213/145/112/845/176/661/477, all ≥ 91 (§3.4 admissibility) — which also
  independently corroborates §3.4's claim that all 8 clear the floor. No simulated zero days.
  `mean(ln obs)` = 2.16–7.11 per station, all > 1.0, so §3.1's `m'` fallback is not triggered.

**The level on the registered window is the same as on the out-of-sample ones** (attack 2 dead):
at β = 0.56, geo-mean of the station arithmetic ratios = **0.0760 → α 0.897**; geo-mean of the
station **log-mean** ratios (the quantity KGE's `m` term actually zeroes) = **0.1026 → α 1.211**.
Attack 3 dead too: the log estimand moves the answer by 1.35×, not by 10×.

**The objective, evaluated exactly.** Scaling sim by `f` shifts `mean(y)` by `ln f` and leaves
`r` and `v` untouched, so `KGE_ln(α)` is exact from the per-station moments. At β = 0.56:

| α | `F_search` (mean) | `F_report` (median) |
|---:|---:|---:|
| 0.117 (unconstrained argmax of `F_report`) | −0.583 | **−0.029** |
| 0.625 (unconstrained argmax of `F_search`) | −0.579 | −0.163 |
| **2.000 (box floor)** | **−0.621** | **−0.349** |
| 3.9 (docs/35 hard stop) | −0.675 | −0.486 |
| 11.8 (Williams) | −0.805 | −0.737 |
| 30.0 (box ceiling) | −0.947 | −0.849 |

**Both statistics are monotone decreasing across the whole registered box.** The in-box optimum
is the box **floor**, α = 2.0, for `F_search` at every β ∈ [0.40, 0.70] and for `F_report` at
every β ∈ [0.40, 0.75]. That is exactly the finding's predicted `FAIL — RAILED`.

**Attack 4 (β is free) — the only attack with real force, and it still fails inside the gate.**
`ln sim = ln α + β·ln(product) + const`, and `mean(ln product) < 0` here, so raising β *lowers*
simulated flux and *raises* the implied α. Measured (9 full re-simulations, α = 11.8 throughout):

| β | geo-mean log-ratio → implied α | argmax `F_search` α | argmax `F_report` α | best in-box `F_report` (at α = 2.0) |
|---:|---:|---:|---:|---:|
| 0.40 | 0.0197 → 0.232 | 0.171 | 0.050 | −0.235 |
| **0.45** (G2.3 floor) | 0.0331 → 0.391 | 0.258 | 0.050 | −0.350 |
| 0.50 | — | 0.387 | 0.074 | −0.408 |
| 0.56 | 0.1026 → 1.211 | 0.625 | 0.117 | −0.350 |
| 0.60 | — | 0.858 | 0.156 | −0.324 |
| **0.65** (G2.3 ceiling) | 0.2556 → 3.016 | 1.289 | 0.325 | −0.305 |
| 0.70 | — | 1.969 | 0.629 | −0.300 |
| 0.75 (box ceiling) | 0.6962 → 8.215 | 3.062 | 1.168 | −0.307 |

Inside the **G2.3 hard gate β ∈ [0.45, 0.65]** the objective's free optimum is α = 0.26–1.29
(`F_search`) / 0.05–0.33 (`F_report`) — i.e. **below** the finding's own 0.85–1.14, not above it.
α only reaches the box floor when β is pushed to ≥ 0.70, which is itself a G2.3 hard stop.

**Attack 5 (aggregation) fails in the same direction:** the objective's argmax is *lower* than
the geometric mean the finding used, so the geometric-mean shortcut was generous to docs/43.

### The one thing the measurement adds that the finding did not claim
At the box floor the fit also **misses the bar**: `F_report(α = 2.0)` = −0.235 (β 0.40),
−0.350 (0.45), −0.350 (0.56), −0.305 (0.65) against the registered bar `[−0.26, 0.44]`. So for
every β inside G2.3 the predicted outcome is **FAIL — RAILED *and* FAIL — NUMERIC**, not one of
them. (The model *can* clear the bar — best attainable `F_report` at β = 0.56 is −0.027 — but
only at α ≈ 0.12, seventeen times below the box floor.)

### Where docs/43 is partly defended (the narrowing that survives)
docs/43 §2.1 assigns the level to **Π**, not to α. Π includes the LS level, and `docs/37` §4
candidate 0 measures our LS at **2.37×–3.00×** the source level. Crediting C4 with the *entire*
LS level error moves the implied α from 1.211 to **2.87–3.63** — over the box floor 2.0 but
**still under the `docs/35` hard stop 3.9**, and 3.63 is inside the 5 %-of-box-edge rail band
(α̂ must be ≥ 3.4 to clear it, so 2.87 is also railed). So the maximum re-partition of Π that
this project has actually measured does not rescue the fit either.

### Not established by the evidence offered
"the gap … is dominated by hillslope→station delivery" is an **attribution**, not a measurement.
Nothing here separates delivery from the LS level, the C level, the K unit system, the volume
convention, SSC event-undersampling or rating bias. The per-station implied α spans
**0.10–8.37** (β = 0.56, CAL, log estimand) — an 84× spread — which is `docs/43` §2.1 row 3's
own "still a defect" heterogeneity, not a single delivery ratio.

### DISCLOSURE OWED (important — flag to the orchestrator)
To test a claim *about C4's outcome* I had to evaluate C4's registered objective on C4's
registered fit set and window. `docs/45` §7.3 records that its own pass "does not launch a
search, fit anything, or produce a number that any gate here judges" — **this pass did produce
such numbers**. They are adversarial diagnostics, they live only in the session scratchpad
(`refute_alpha_cal_beta*.csv`, `refute_alpha_summary.json`, `refute_alpha_out.txt`,
`refute_gate_check.txt`) and in this journal, and **no repo artifact and no frozen artifact was
written or modified**. Whoever runs C4 must disclose that this profile existed beforehand.

## VERDICT
**NOT REFUTED.** Every attack I mounted failed, on the registered window with the registered
objective and estimator, behind two exact reproduction gates. The finding is *understated*: the
predicted outcome is FAIL–RAILED **and** FAIL–NUMERIC. Two clauses of it are not established —
the delivery attribution, and (strictly) the claim as an indictment of `docs/43` alone rather
than of `docs/43` §2.1 **combined with** `docs/45` §2.3's decision to fix `f_LS`, `C`, `P`, `FG`,
`f_K` and `f_vol` so that α is Π's only remaining handle.


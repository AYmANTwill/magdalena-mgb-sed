# Journal — agent `verify-d` (adversarial verification of H-D: blend arithmetic)

Role: **refute**, not agree. Date 2026-08-12. Repo `c:\dev\magdalena-mgb-sed`, branch `main`.
No commits, no adds, no pushes. No `docs/NN` file touched. All work in
`<scratchpad>/verify_d/`: `v1_decomp.py` → `v1_out.txt`, `v2_attack.py` → `v2_out.txt`,
`v3_loocv.py` → `v3_out.txt`, `v4_final.py` → `v4_out.txt`.

## 1. Method

I read `h2_harvest.py` in full for the column semantics **before** writing anything, and wrote
`v1_decomp.py` from those semantics alone — I deliberately did **not** open
`hd_blend_arith.py` / `hd_followup.py` until after my own numbers were on disk, so my
re-derivation is independent rather than a re-run. Only then did I read the report's scripts, to
locate the origin of the numbers I could not reproduce.

Semantics used (verified against `h2_harvest.py`): `sPA/sCrawA/sCmapA` are per-cell **day-sums
in mm** over subset A (`(~Cnan) & (~gap)`); `sPB/…` idem over B (`(~Cnan) & gap`, merged := Cmap);
`sPD` over D (`Cnan`, merged := P); `sP`/`sMerged` are all-day sums; `mmyr(x) =
(x·area).sum()/area.sum()/n_days·365.25`, `n_days = 3287`. Ledger integrity checks I ran and
that passed: `max|nA+nB+nD−ND| = 0`; `max|sPA+sPB+sPD−sP| = 7.3e-12`;
`max|sCmapA+sCmapB−sCmap_all| = 7.3e-12`; per-cell blend identity `max|LHS−RHS| = 1.24e-03 mm`
day-sum = **1.375e-04 mm/yr** (the report's journal quotes the mm/yr form — the conversion is
consistent, not a discrepancy).

## 2. What reproduced exactly (independent recomputation)

Every one of these matched the report to the last digit it printed:

* fields 2036.3927 / 2124.7205 / 2265.7574 / 2188.5404; surplus **+152.147692** (+7.4714 %).
* `E_area[w] = 0.403717`, `E_area[dA] = +229.326272`, product `+92.582966`,
  `cov_area(w, dA) = +59.526290`, blend term `+152.109256`, fallback `+0.038436`,
  total `+152.147692`, residual **+2.252e-08**; `product+cov−blend = −2.8e-14`.
* the 4-way: `+87.3022 / +64.8070 / +0.0086 / +0.0298`; `cov(w,Cmap−Craw) = +30.3667`,
  `cov(w,Craw−P) = +29.1596`.
* the whole §1 correlation table — all 24 entries and all six `E_area` values — plus
  `corr_a(d_nearest, Craw) = +0.4077`, `corr_a(elev, Craw) = −0.2739`, `corr_a(elev, w) = −0.1688`.
* constant-w counterfactual **2129.0141**, actual−constant `+59.526290` = cov to **−2.25e-08**;
  unweighted-w sensitivity 2129.4257 / `+59.1147`.
* `s = 0.937753`; (b) **2122.6282**; (c) **2072.0168**; cov under de-inflation **+50.611424**;
  residual under (c) **+35.624034**. All three FAIL [2016.0, 2056.8].
* w-band split `+0.003 / +54.200 / +97.944` at 25.84 / 57.07 / 17.09 % of area and
  0.00 / 35.62 / 64.37 % of surplus; w=1 = 1,496 cells, d_nearest 30.0–71.5 km, median 38.2.
* the full w-tenths table; Spearman(bin, mean dA) = **0.9273**; area-weighted OLS slope
  **+409.706**, intercept **+63.921**.
* the ladder: 59.5263 / 56.9974 / 35.6240 and 65.9122 / 50.6114 / 35.6240, both summing to
  +152.147692; brackets 33.26–39.12 %, 37.46–43.32 %, 23.41 %.
* `wmax = 0.088820` inside the band (using the published edge 2056.8), `w* = −0.000166` to hit
  2036.393, de-inflated `wmax = 0.231557`.
* gauge-pixel ratios: pair-weighted `+0.034 %`, simple `+0.350 %`, raw pair-wt `−2.519 %`
  (simple raw `−2.700 %`).
* the gate band **[2,016.0, 2,056.8]** is properly CITED — `docs/33`:116, `docs/18`:912,
  `docs/31`:396, and independently recomputed in `docs/39`:175. **No uncited band is load-bearing
  anywhere in this report.**

## 3. What I could NOT reproduce, and why — five defects

### 3.1 The "deciles" in §4 are not deciles (CRITICAL presentation defect)

Report: *"bottom decile contributes +18.14 (30.5 % of cov) … top decile +37.98 (63.8 %). The
middle 45 % of area contributes ~5 % net."*

Source located: `hd_followup_out.txt` block (ii). Those are the **fixed-width w bins**
`[0.0,0.1)` and `[0.9,1.0]` — **34.64 %** and **19.95 %** of area, i.e. 3.5× and 2× a decile. The
report's own three area shares sum to 100 % (34.64 + 45.4 + 19.95), which is impossible for two
deciles plus a 45 % middle — self-inconsistent on its face.

My equal-population deciles (`v3_out.txt`):

| construction | bottom | middle 8 | top |
|---|---|---|---|
| count-decile | +4.912 (8.25 %) | +19.386 (32.57 %) | +35.228 (59.18 %) |
| area-decile | +5.257 (8.83 %) | +18.647 (31.33 %) | +35.622 (59.84 %) |
| report ("decile") | +18.14 (30.5 %) | ~5 % | +37.98 (63.8 %) |

Worse, a decile of `w` is **not a well-defined object**: 2,213 cells (25.84 % of area) are tied at
exactly `w = 0` and 1,496 (17.09 %) at exactly `w = 1`, so the bottom ~2.5 deciles lie inside one
tie and membership is set by tie-break order. Over 100 random shuffles of the `w = 0` ties the
bottom count-decile ranges **+4.119 … +6.672** (spread 2.55 mm/yr, ±25 % of its own value).

Tie-free replacement I measured and recommend: cov contributions by band —
**w = 0: +13.972 (23.47 % of cov, 25.84 % of area) · 0 < w < 1: +10.529 (17.69 %, 57.07 %) ·
w = 1: +35.026 (58.84 %, 17.09 %)**. The report's *qualitative* two-tailed point survives under
this labelling; the numbers do not.

### 3.2 Four local inversions, not three

`mean_dA` = [95.4, 158.6, 153.0, 146.6, 198.0, 178.4, 257.8, 213.4, 307.1, 550.8]. Falls at
1-based rows **3, 4, 6, 8** — row 4 (146.56 < 152.98) is missed by the report's "bins 3, 6, 8".

### 3.3 The accusation against the brief is wrong (§2a) — REFUTED

Report: *"the brief's own trio does not close — 92.605 + 59.528 = 152.1330 vs the exact blend term
152.109256, off by +0.0237 … the brief's trio is internally inconsistent."*

The report correctly identified the brief's `d` as own-`nA` normalised (I get **229.381220**,
`E[w]·E[d] = 92.605149` — the brief's 229.381 / 92.605 exactly). But it never computed the
covariance under that same definition. I did:

```
cov_a(w, d_ownNA)  = 59.528320     <- the brief's 59.528, to 5 dp
E[w]E[d] + cov     = 152.133469
E_area[w·d_ownNA]  = 152.133469     residual +7.1e-15
```

The brief's trio **closes exactly, to 7e-15, on its own quantity.** It is internally consistent.
What is true — and all that is true — is that `E[w·d_ownNA] = 152.1335` is **not** the blend term
`152.1093`; the two differ by **+0.0242 mm/yr** because the identity needs the window-length (ND)
normalisation. The report converted a definitional difference into an accusation of arithmetic
error against another artefact. The measurement that would have prevented it (`cov` under
definition B) was one line away and was not run.

### 3.4 "Shapley avg" is not a Shapley value, and an order-free split exists

Only **two** interventions are defined (de-correlate, de-inflate); the third row is the *residual*
after both, so its "order-invariance" is true by construction, not measured. A 3-player Shapley
value needs 6 orderings; the report averages 2. The label should read "2-ordering average".

More usefully, an **exact order-free** decomposition exists — expand `dA = (Cmap−Craw) + (Craw−P)`
and `w = E[w] + w'`:

| term | mm/yr | share |
|---|---|---|
| `E[w]·E[Cmap−Craw]` (map inflation, mean part) | +56.9356 | 37.42 % |
| `E[w]·E[Craw−P]` (CHIRPS-vs-IDW, mean part) | +35.6474 | 23.43 % |
| `cov(w, Cmap−Craw)` | +30.3667 | 19.96 % |
| `cov(w, Craw−P)` | +29.1596 | 19.17 % |
| fallback `E[dB]` | +0.0384 | 0.03 % |
| **sum** | **+152.1477** | resid +2.25e-08 |

Blend-arithmetic (covariance) share, order-free: **39.12 %**, a single number. The report's
33.3–39.1 % bracket is an artefact of choosing a *multiplicative* de-inflation (which rescales the
covariance too); it is conservative rather than wrong, but the bracket should be attributed to that
choice, not to irreducible ambiguity.

Two labels in the §6 table are approximate but printed as identities:
`E[w] × map inflation` is +56.997 in the ladder vs **+56.936** exactly; the (c) residual +35.624 is
called `E[w] × (raw CHIRPS − gauge IDW basin gap)` = **+35.659** exactly (and `E[w]·E[Craw−P]` on
blend days = **+35.647**). Errors ≤ 0.07 mm/yr — immaterial, but write "≈".

### 3.5 "a floor no weight scheme can remove" — REFUTED

The +35.624 term is exactly proportional to `E[w]` (`v4_out.txt` block B):

```
constant w 0.4037 -> +35.62   areal 2072.02      constant w 0.10 -> +8.78   areal 2045.17
constant w 0.20   -> +17.62   areal 2054.01 (INSIDE the band)
constant w 0.00   ->  -0.06   areal 2036.33
```

It vanishes as `E[w] → 0`, and a de-inflated map at constant `w = 0.20` **passes the gate**. The
report's own §5 already says "with the map de-inflated, constant w up to 0.2316 passes" — so the
verdict paragraph contradicts its own §5. The claim is only true at **fixed** `E[w] = 0.4037`.

## 4. The headline negative is REFUTED: corr(w, error) IS identifiable, and has been measured

Report: *"correlation with error is **not identifiable from anything that exists** … so no
gauge-independent truth exists in the region carrying 64.4 % of the surplus … Recorded as **not
identifiable** — a publishable negative."*

`data/processed/merge_loocv_report_v2.csv` (291 rows, written by the same merge run, bit-identical
to the Aug-3 file per `docs/18` §15.5) carries per **held-out** gauge: `d_nearest_km`, `w_chirps`,
`bias_base_pct`, `bias_merged_pct`. That is leave-one-out, gauge-independent truth **with the
blend weight of the held-out cell on the x-axis** — precisely the axis corr(w, error) needs.

```
gauges with w_chirps == 1 (d_nearest > 30 km): 20      0 < w < 1: 169      w == 0: 98
LOOCV >30 km gauges: d_nearest 30.1 - 59.5 km (median 34.6)
w=1 CELLS          : d_nearest 30.0 - 71.5 km (median 38.2)
=> 96.1 % of the w=1 AREA lies inside the LOOCV-tested distance range
```

Measured (my `v3_out.txt`, reproducing `docs/18` §15.5 exactly):

| band | n | median bias_base | median bias_merged | median delta |
|---|---|---|---|---|
| w = 0 (<10 km) | 98 | +3.62 % | +2.98 % | **+0.00 pts** |
| 0<w<1 (10–30 km) | 169 | +0.29 % | +1.29 % | **+0.24 pts** |
| w = 1 (>30 km) | 20 | +3.86 % | +6.56 % | **+0.89 pts** |

Those three deltas are **already published** in `docs/18` §15.5: *"The per-band bias deltas say
the same thing monotonically: +0.00 pts below 10 km, +0.24 pts at 10-30 km, +0.89 pts beyond
30 km"*, alongside *"> 30 km loses a lot (0.343 -> 0.300, n=20)"* — which I reproduce
(r_base 0.343 → r_merged 0.300, n = 20).

**So the quantity is identifiable and was identified.** The report's own executed output
(`hd_gauge_out.txt`) even prints *"gauges >30 km from their nearest neighbour: 20 of 291"* — it had
the datum and drew the opposite conclusion. Its script block 6 is correctly scoped ("not estimable
**from this ledger**"); the *report* escalated that to "from anything that exists". The escalation
is the defect.

**And the null matters more than the negative.** When measured, the effect is not distinguishable
from zero:

```
corr(w_chirps, delta bias)  Pearson +0.0066   Spearman +0.0782   (n=287)
>30 km band: 11 of 20 deltas positive; Wilcoxon on the delta p = 0.956; mean delta -0.92 pts
             (median +0.89 -- mean and median disagree in SIGN at n=20)
all 287    : median delta +0.000, mean +0.187, Wilcoxon p = 0.395
```

The publishable result is therefore **not** "unmeasurable" but **"measured at point scale and
indistinguishable from zero (n = 20 in the w = 1 band, Wilcoxon p = 0.96)"** — which is a weak
*exculpation* of the blend and a stronger statement than the report's. The genuine residual
non-identifiability is narrower: point bias at gauge locations does not identify **areal** bias
over the ungauged 17 %, and gauge sites are not a random sample of ungauged terrain.

### 4.1 "+0.034 % — the map is validated where it is least used" is IN-SAMPLE

`h2_harvest.py` builds `mean_c_map` with `pools.fit(band_g[j], zone_g[j])`, its own comment
reading `# basin-field map (no holdout)`. Gauge *j*'s pairs are inside the pool that produced its
map, so `+0.034 %` is a **quantile-map fit residual**, not a validation — a monotone map carrying a
pool's CHIRPS marginal onto that pool's gauge marginal matches the pool mean by construction. The
per-pool table proves it: every pool with ≥4 gauges matches within ±0.5 %, and the only large
deviations are the pools with 1–2 gauges (`('z','Cesar')` −18.4 %, `('z','Medio Magdalena')`
−6.6 %, `('z','Sogamoso')` +11.4 %). "Validated" must become "fitted"; the out-of-sample substitute
is the LOOCV table above.

## 5. The elevation confound: the direction of the claim is over-stated

Report: *"this is **not** an orographic story. The remote-and-wet region is *low* and ungauged, not
high."*

Partial correlations (area-weighted) support the **first** half strongly:
`corr_a(w, Craw) = +0.371` → `+0.343` controlling elevation; `corr_a(w, dA) = +0.2225` → `+0.2148`
controlling elevation; and inside the w = 1 set `corr(elev, dA) = +0.007` — no elevation signal at
all. Good: the surplus is not orographic.

The **second** half is wrong as a description. Splitting the surplus by cell-elevation tercile
(<310 / 310–1460 / >1460 m):

```
whole basin : low 28.39 %  mid 50.24 %  high 21.37 % of the surplus (area 32/33/34 %)
w = 1 cells : low +27.04 (17.77 %) | mid +53.25 (35.00 %) | high +17.64 (11.60 %)
              aw elevation of those three blocks: 125 m / 796 m / 2,406 m
```

The plurality of the w = 1 block is **mid-elevation**, and 11.6 % of the whole surplus comes from
ungauged cells averaging **2,406 m**. `corr_a(elev, w) = −0.169` is weak. Publishable form: the
surplus tracks *ungaugedness*, not elevation — not "the wet region is low".

## 6. Two claims I attacked and could not break

* **"cov is structural, not an artefact of map inflation."** Confirmed and strengthenable:
  `cov(w, Craw−P) = +29.160` is **49.0 %** of `cov(w, dA)` and survives *any* mean-preserving map.
  Further, `cov_a(w, PA) = +83.691` — the **gauge-only** field carries the same w-geometry on its
  own, so no re-weighting removes it.
* **the gate-design flag** — arithmetically right (with the map as-is no constant `w ≥ 0.089`
  passes; `w* = −0.0002` hits the target) and the band is cited. But two corrections: (i) "no
  **positive** amount of CHIRPS influence can satisfy" is false — every `w ∈ (0, 0.0888]` passes;
  (ii) the inference "a statement about the target, not about the blend" must confront the
  registered design intent it contradicts. nb10 §5 **Decision** (`src/nbgen/make_nb10.py`:396,
  quoted in `docs/agents/journal_nb-banner-1011.md`:79/120 as A1) is *"**Gauges set the values;
  CHIRPS sets the spatial pattern between them.**"* Under that decision a volume gate anchored on
  the gauge field is the intended constraint, not an accident of gate design — the merge failing it
  means the merge violated its own charter. The flag is worth raising; it is not settled.

## 7. Minor, corroborated

`bounds_fields.csv` F5/F6 label "0.414" vs code/brief 0.4527 — real, and already found
independently by `journal_chirps-mundane.md`:32-33 (*"the **code** is 0.4527 … the **label** says
0.414"*), `journal_chirps-orographic.md`:57-58 and `journal_chirps-transfer.md`:51-52. Not novel;
still worth reconciling. Note 0.414 is itself a real published coefficient elsewhere
(`docs/18`:577, the inserted-day wet-rate ratio), which is probably how the label drifted.

## 8. What the report should have run and did not

1. `cov` under the brief's own `d` definition — would have retracted §2a's accusation (§3.3).
2. Equal-population deciles, or any tie-aware split, before writing the word "decile" (§3.1).
3. `merge_loocv_report_v2.csv` — the artefact that refutes its headline negative (§4). It is
   listed in `docs/18` §15.5 four paragraphs from the gate table the report cites.
4. Whether the map's `+0.034 %` is in-sample (§4.1) — one grep of its own harvest comment.
5. `E[w]`-scaling of the (c) residual before calling it a floor (§3.5).

## 9. Scope of my own work

I re-measured from `cell_ledger.csv`, `gauge_ledger.csv`, `bounds_fields.csv` and
`data/processed/merge_loocv_report_v2.csv` only. I did **not** rebuild the merged field (RAM
constraint honoured; peak use one 8,672-row frame plus a 291-row frame). I did not verify that the
ledger itself is faithful to `merge_chirps_gauges.py` beyond the harvest's own asserts and its
reproduction of 2188.5404 / 2219.1786 — if the ledger is wrong, everything above is wrong the same
way, and that risk is common to the report and to me.

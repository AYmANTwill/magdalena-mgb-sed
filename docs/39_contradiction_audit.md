# 39 — Contradiction audit of the project's own record

**Status:** AUDIT, 2026-08-11, by the `contradictions` agent
(`docs/agents/journal_contradictions.md`). **Read-only** with respect to every other file: this
document *reports* disagreements, it does not fix them. No committed number was edited anywhere.
No git operation was performed.

**Scope.** `CLAUDE.md`, `README.md`, `docs/00_INDEX.md`, `docs/06`, `docs/12`, `docs/13`,
`docs/16`–`docs/36`, `docs/PROGRESS.md`, `docs/progress_journal.md`, `docs/open_questions.md`,
and the `DATA` block of `progress_map.html` (lines 410–674). `docs/37` did not exist when this
was written (reserved by the concurrent C3-closure workflow).

**Method.** Every headline quantity appearing in more than one place was tabulated with its file
and line (§1). Every disagreement was then classified into one of four classes (§2–§5), following
the review protocol `docs/31` §"Review protocol" mandates. Where an artifact on disk could settle
a disagreement, it was read (read-only) and the settlement is recorded with the artifact path.

> **Caveat on live files.** Three files changed while this audit was reading them:
> `CLAUDE.md` (a newer on-disk version than the one carried in session context), `docs/13`
> (a `STATUS — HISTORICAL` header was added), and `docs/00_INDEX.md` (created mid-audit by a
> `consolidate` agent — it reserves number 39 for this document). Line references to those three
> are as of 2026-08-11 and may drift.

---

## 0 — Summary

| class | count | meaning |
|---|---:|---|
| **NEW-unverified** | **12** | a genuine conflict nobody has flagged — §2 |
| resolvable-now | 4 | settled here from an artifact on disk — §3 |
| known-open | 9 | already on a register; confirming is not a discovery — §4 |
| false-alarm | 6 | same name, legitimately different quantity — §5 |
| mis-citations / dead pointers | 6 | §6 |

The single most consequential finding is **N1**: the flow partition that motivates the whole of
stage C2b (`docs/33`) is not in the document it cites, and the number quoted as "51.3 % surface"
is the basin **runoff coefficient**. The true generated-surface share of local runoff is **62.6 %**,
computed here from the frozen drivers and equal to `docs/26` §A.6's own two numbers. No C2b verdict
depends on it — `docs/33` §2.2 explicitly attaches no threshold to it — but it is quoted three times
in `docs/33` and once in the live tracker as a measured property of the adopted model.

---

## 1 — The NUMBER LEDGER

Every quantity below appears in at least two places. `✔` = all sources agree. `≠` = disagreement,
with its classification in the right-hand column.

### 1.1 Skill by configuration and period

| quantity | values found (file:line) | verdict |
|---|---|---|
| VAL-all median KGE, attempt 1 (Config B) | **0.450** — `docs/18`:98, `docs/21`:23, `docs/24`:96, `docs/25`:54, `docs/26`:265 | ✔ |
| VAL-all KGE, attempt 2 (H1) | **0.421** — `docs/21`:24, `docs/24`:97, `docs/26`:266, `docs/26`:121 | ✔ |
| VAL-all KGE, attempt 3 (H2) | **0.346** — `docs/21`:25, `docs/24`:98, `docs/26`:267, `docs/26`:121 | ✔ |
| VAL-all KGE, attempt 4 (H2E) | **0.356** — `docs/24`:99, `docs/26`:268; artifact `metrics_fleet.csv` H2E/fit/VAL all = 0.35625 | ✔ |
| VAL-all NSE by attempt | 0.256 / 0.179 / 0.161 / **0.130** — `docs/26`:265-268; artifact agrees | ✔ (but see **N6**) |
| "ours is +0.16 to +0.26" (NSE) | `docs/24`:225-226 | ≠ **N6** — excludes the adopted H2E's 0.130 |
| El Niño KGE | Config B **0.193** (`docs/18`:100, `docs/22`:40, `docs/26`:120), H1 0.245, H2 0.207 (`docs/26`:120), H2E **0.200** (`docs/26`:290; artifact 0.20037) | ✔ |
| La Niña KGE | Config B **0.399** (`docs/18`:99, `docs/22`:39), H2E **0.344** (`docs/26`:289; artifact 0.34390) | ✔ |
| CAL 2012-14 r | **0.522** (`docs/18`:97, Config B) · **0.518** (`progress_map.html`:435, `docs/33`:414) · **0.5564** (`docs/33`:415, artifact `metrics_fleet.csv` H2E/fit/CAL = 0.55640) | ≠ known-open **K4** |
| El Niño daily r across 12 configs | **0.556–0.572** — `docs/22`:221, `docs/21`:59, `docs/24`:197, `docs/26`:273, `docs/30`:15, `docs/31`:27, `docs/33`:419 | ✔ |
| El Niño anomaly r | **0.476** — `docs/18`:186, `docs/21`:65, `docs/22`:229, `docs/24`:202 | ✔ |
| PBIAS by attempt (VAL all) | +6.83 / +6.36 / +7.34 / **+3.51** — `docs/26`:265-268; `docs/24`:96-99 rounds to +6.8/+6.4/+7.3/+3.5 | ✔ |
| Recession ratio by attempt | 2.98× / 0.96× / 1.01× / 0.98× — `docs/21`:23-25, `docs/24`:96-99, `docs/26`:265-268 | ✔ |
| Observed recession constant | **13.9 d** (`docs/18`:137, `docs/22`:110) vs **10.40 d** (`docs/26`:54) vs **9.5–11.9 d** (`docs/24`:118) vs **10.44 d** (`docs/33`:568) | ✔ false-alarm **F1** (different segment rules, stated in `docs/26` §2) |
| Skill over climatology, El Niño | Config B **+0.024** (`docs/22`:40, `docs/25`:54) · **−0.026** (`docs/24`:125, `docs/26`:118) · H1 **+0.026** · H2 **+0.006** · H2E **−0.0005** (`docs/26`:292,300; artifact −0.00053) | ≠ false-alarm **F2** + **N6** |
| Skill over climatology, La Niña | **+0.236** (`docs/22`:39, `docs/25`:54) · **+0.157** (Config B, `docs/26`:118) · **+0.126** (H1, `docs/26`:118 and `docs/24`:231) · **+0.106** (H2E, `docs/24`:135, `docs/26`:292) | ≠ **N6** (docs/24 mixes attempts) |
| Skill over climatology, VAL-all | +0.199 / +0.170 / +0.079 / **+0.089** — `docs/26`:265-268; artifact H2E = 0.08909 | ✔ |
| Overfitting excess | **+0.011** — `docs/18`:27,106, `docs/24`:82 | ✔ |
| Cal→val degradation | **−0.159** — `docs/18`:105, `docs/24`:82 | ✔ |

### 1.2 F values and the objective

| quantity | values found | verdict |
|---|---|---|
| F(prior) | **0.1276** — `docs/20`:157, `docs/24`:105, `docs/26`:47 | ✔ |
| F(random null) | **0.1729 / 0.173** — `docs/20`:157, `docs/24`:105 | ✔ |
| F(Config B) | **0.2429 / 0.243** — `docs/20`:157, `docs/24`:105, `docs/26`:76 | ✔ |
| F(H2E best seed) | **0.25931** / `0.25930593639066796` — `docs/20`:134, `docs/26`:203,218, `docs/29`:168, `docs/31`:24, `docs/33`:370; artifact `report_H2E.json` identical | ✔ |
| H1 / H2 mean F over 6 seeds | 0.23443 / 0.24358, gap 0.00915, spreads 0.05082 / 0.02298 — `docs/29`:173, `docs/31`:26; recomputed from `docs/29`'s own seed table: mean 0.234435 / 0.243580 | ✔ |
| H2E-S seed F (incumbent scale) | 0.22489 / 0.22984, mean 0.22737, Δ −0.0319 — `docs/33`:957, `docs/36`:60 | ✔ |
| F ceiling arithmetic | `c2m(0.518)=0.349` vs `c2m(0.5564)=0.386` — `docs/33`:414-415 | ≠ **K4** |

### 1.3 Peak signatures (C2b)

| quantity | values found | verdict |
|---|---|---|
| `R_AMS` fleet median | **0.820** — `docs/33`:721,753, `docs/35`:232, `docs/36`:31, `progress_map`:525 | ✔ |
| `R_Q1` | **0.847** — same four | ✔ |
| `R_Q5` | **0.975** — same four | ✔ |
| `R_POT` | **0.567** (`docs/33`:756, `docs/35`:236, `docs/36`:33) vs **0.5747** (`docs/36`:94, `progress_map`:598, artifact `peakgap/summary.json`) vs **0.575 fleet-wide** (`docs/33`:770) | ≠ known-open **K5** |
| POT counts | 1,285 sim / 2,236 obs — `docs/33`:770, `docs/35`:239, `docs/36`:40 | ✔ |
| "43 % of flood events missed" vs 81.8 % identity deficit | `docs/33`:774, `docs/35`:240 vs `docs/36`:101 | ≠ known-open **K6** |
| El Niño `R_AMS` | **0.686** — `docs/33`:815, `docs/35`:292, `docs/36`:32 | ✔ |
| Sediment propagation `R^0.56` | −10.5 % fleet, −19.0 % El Niño — `docs/33`:898-900, `docs/35`:232,275, `docs/36`:31-32 | ✔ |
| Contrast inflation | **≈ +10 %** (0.8875/0.8097 = 1.096) — `docs/35`:297, `docs/36`:229 | ✔ |
| Area-tercile population | n = **63**, large tercile 1,569–257,097 km² (`docs/33`:849) vs n = **62**, large tercile 1,563–54,035 km² (`docs/36`:145) | ≠ **N11** |

### 1.4 BFI (C2b.1)

| quantity | values found | verdict |
|---|---|---|
| fleet-median `BFI_obs` / `BFI_sim` | 0.7811 / 0.7965 — `docs/33`:587-588, `progress_map`:519 | ✔ |
| gate IQR(`BFI_obs`) | 0.02845, measured 0.01625 — `docs/33`:588-589, `progress_map`:519 | ✔ |
| gauges entering the statistic | **55 of 63** — `docs/33`:561, `progress_map`:516 | ✔ |
| model internal partition | **51.3 % surface / 29.2 % subsurface / 19.5 % baseflow** — `docs/33`:37,205,628, `progress_map`:262-264,664 | ≠ **N1 — PRIZE** |
| basin runoff coefficient | **0.5127** — `docs/26`:252; artifact `report_H2E.json` `runoff_coefficient` = 0.5126921499891222 | ✔ |
| generated surface vs local runoff | 650 vs 1,038 mm/yr — `docs/26`:330; recomputed here 650.1 / 1038.2 ⇒ share **0.6262** | ≠ **N1** |

### 1.5 Gauge counts

| set | value | sources | verdict |
|---|---:|---|---|
| discharge stations consolidated | 192 | `docs/17`:20,486 | ✔ |
| calibration-ready after QC | 80 of 192 | `docs/17`:23,406,511 | ✔ |
| v1 calibration set | **61** | `docs/18`:92, `docs/22`:85, `docs/26`:20; artifact `feasibility_H1.csv` = 61 rows | ✔ |
| v2 / H2E calibration set | **63** | `docs/18`:729, `docs/26`:21, `docs/31`:24, `docs/33`:247; artifacts `feasibility_H2.csv` 63 rows, `metrics_fleet.csv` VAL-all n = 63 | ✔ |
| H2 − H1 common gauges | **59** | `docs/21`:42, `docs/26`:88; recomputed here: |H1 ∩ H2| = 59 | ✔ |
| CAL-window gauges | **57** | artifact `metrics_fleet.csv` H2E CAL n = 57 | ✔ false-alarm **F3** |
| BFI-eligible gauges | **55** | `docs/33`:561 | ✔ false-alarm **F3** |
| El Niño-window gauges | 54 | `docs/26`:297; artifact n = 54 | ✔ |
| precip gauges | 294 → **291** after merge | `docs/16`:16, `docs/18`:687, `docs/23`:89 | ✔ |
| LOOCV gauge set | **287** | `docs/18`:696,838,910, `docs/33`:117 | ✔ |
| zero-suppression repair, v1 → v2 | 70 → **153** stations; 109,129 → **240,158** inferred-dry days | `docs/16`:82,144; `docs/18`:292,365,538; `docs/20`:61; `docs/24`:161 | ✔ |
| energy-floor failures | **18 → 14** (`docs/18`:609-611, `docs/23`:16, `docs/24`:163) vs **18 → 16** (`docs/26`:112) | ≠ resolvable **R2** |

### 1.6 SSC network

| quantity | values found | verdict |
|---|---|---|
| SSC stations total | **79** | `docs/19`:23, `docs/30`:48, `docs/31`:30, `docs/32`:23, `PROGRESS`:147 | ✔ |
| mapped to a minibacia | **28** | `docs/19`:27,306, `docs/31`:30, `docs/32`:16 | ✔ |
| calibration-safe (geometry+name screen) | **24** | `docs/19`:28,306, `docs/30`:48, `docs/32`:16 | ✔ |
| with coordinates | 33 | `docs/31`:30 | ✔ |
| unmapped | **46** no coords + **5** outside the domain | `docs/19`:27 says "46 lack coordinates, 51 lack a minibacia"; `docs/32`:296-303 splits 46 / 5 and calls it a "bookkeeping correction to C1.0" | ✔ (correction recorded in place) |
| C1 classification | 6 usable / 12 caveat / 61 excluded | `docs/32`:231-234, `docs/00_INDEX`:147, `progress_map`:484 | ✔ (sums check: 6+12+61 = 79; mapped 6+12+10 = 28) |
| stations usable in both ENSO windows | **7** | `docs/32`:256, `docs/34`:154 (18 stations × 4 windows) | ✔ |
| bridging stations, 2011 vs 2015-16 | **6** | `docs/19`:351,703, `docs/30`:38 | ✔ false-alarm **F4** (a different definition from C1's 7) |
| SSC station-days | 269,337 | `docs/19`:23,685, `docs/30`:47, `docs/31`:29, `docs/32`:21 | ✔ |
| clean paired SSC+Q days, safe-24 | 73,264 / 73,265 | `docs/19`:28,586,701 | ✔ (stated with both bases) |
| mainstem/tributary split of the 28 | 8 / 20 | `docs/32`:240 | ✔ |

### 1.7 Observed ENSO contrast (C2)

| quantity | values found | verdict |
|---|---|---|
| primary median rate ratio | (a) **4.62**, (b) **2.84** headline / 2.95 all | `docs/34`:208,210-211, `progress_map`:496 | ✔ |
| sensitivity median rate ratio | (a) **9.32**, (b) **6.40** | `docs/34`:212,215 | ✔ |
| headline range quoted | "**~3 to ~9×**" (`docs/34`:472), "**2.8×–4.6×** primary, **6.4×–9.3×** sensitivity" (`docs/35`:306, `docs/36`:301, `progress_map`:413) | ✔ false-alarm **F5** |
| unanimity | **22 of 22** station-ratios > 1; 16 of 22 CIs exclude 1 | `docs/34`:204,230, `progress_map`:496 | ≠ known-open **K7** |
| estimator disagreement | 8 of 38 = 21 % | `docs/34`:302,466 | ✔ |
| monotonicity | 0 violations of 40 | `docs/34`:352 | ✔ |
| Duan smearing factor | 1.080–1.832, median 1.478 | `docs/34`:199,345 | ✔ |
| ARRANCAPLUMAS annualised | 15.1 / 23.4 Mt/yr (P-LN); 13.3 / 23.9 (S-LN) | `docs/34`:406-409 | ✔ |
| literature anchor | **144 Mt/yr** (Restrepo & Kjerfve 2000) · **184 Mt/yr** (Restrepo & Escobar 2018) · "~145–169" (`docs/06`:9) · "~140–180" (`docs/31`:37) | ✔ resolved by `docs/34` §5.1 — but see **N9** |
| published basin area | **257,438 km²** (`docs/34`:391) vs our **257,097 km²** (everywhere) | ✔ (0.13 % apart, stated) |

### 1.8 Basin-scale forcing quantities

| quantity | values found | verdict |
|---|---|---|
| basin area / minibacias | 257,097 km² / 8,672 | `docs/16`:349, `docs/17`:68, `docs/19`:399, `docs/24`:26,51, `docs/34`:392, `report_H2E.json` 257,096.93 | ✔ |
| areal rainfall, v1 2009–2017 | **2,174.3 mm/yr** | `docs/18`:391,598, `docs/23`:48,95 | ✔ |
| areal rainfall, v1 2008–2018 | **2,206 mm/yr** | `docs/16`:352,372, `docs/17`:277,510, `docs/18`:390 | ✔ |
| areal rainfall, v2 2009–2017 | **2,035.6** unmerged / **2,036.4** merged | `docs/18`:598,691, `docs/23`:95 | ✔ (merge worth +0.8) |
| areal rainfall, v2 2008–2018 | **2,072.3** unmerged / **2,073.1** merged | `docs/18`:599,724, `docs/23`:96 | ✔ |
| gauge-mean annual | 2,904 → 2,304 → 2,327 mm/yr | `docs/16`:144,398 | ✔ |
| CHIRPS areal mean, 2009–2017 | **2,124.9** | `docs/18`:425,449 | ✔ |
| CHIRPS areal mean, 2008–2018 | **2,140** | `docs/18`:391,423 | ✔ |
| uncited reference | **~2,050 mm/yr** | `docs/18`:393,405, `docs/21`:82 | known-open (docs/21 §4 item 4) |
| PET | 3.40 mm/day / 1,255 mm/yr (v1) · 3.41 mm/day (v2) · basin PET **1,251.6 mm/yr** | `docs/16`:357-358, `docs/18`:694,726 | ✔ |
| radiation | **17.2 MJ/m²/day**, band widened to 15–22 | `docs/16`:359,377, `docs/17`:98, `docs/18`:693 | ✔ |
| CHIRPS gate — volume band | 2,036.4 ± 1 % = **[2,016.0, 2,056.8]** | `docs/33`:116, `docs/18`:912, `docs/31`:396 | ✔ (recomputed: 2016.04 / 2056.76) |
| CHIRPS gate — LOOCV bar | **0.429**; merged **0.447** | `docs/18`:696,839,911, `docs/21`:63,79, `docs/26`:180, `docs/31`:27-28, `docs/33`:117-119 | ✔ |
| CHIRPS volume result | **2,188.5 mm/yr**, +7.47 % (quoted as +7.5 %) | `docs/18`:840,912, `docs/33`:119 | ✔ |
| CHIRPS per-band r | <10 km 0.481→0.475 · 10–30 km 0.426→0.449 · >30 km 0.343→0.300 | `docs/18`:847-849,917 | ✔ |

### 1.9 Sediment engine / MUSLE (C3)

| quantity | values found | verdict |
|---|---|---|
| first uncalibrated basin total | **0.6844 Mt/yr** (`pixel_km2`), 9.0222 (`swat_mm_ha`), 32.7577 (`williams_m3`) | `docs/35`:508-510, `progress_map`:413,573 | ✔ |
| decade total | 6,843,119.50146461 t | `docs/35`:501, `progress_map`:566 | ✔ |
| `h2e_drivers.npz` size | **546 MB** (`docs/26`:314, `docs/20`:44) vs **521 MB** (`docs/33`:456, `docs/36`:83,384,691, `progress_map`:453,455,612) | ≠ resolvable **R1** |
| Qsur fleet total | 167.4 km³/yr = 651 mm/yr | `docs/35`:40,196 | ✔ (matches 650.1 recomputed here) |
| α, β Williams defaults | 11.8, 0.56 | `docs/31`:35, `docs/35`:31,336 | ✔ |
| α hard stop | > 35.4 or < 3.9 | `docs/35`:343-344, `progress_map`:562 | ✔ |
| β band | [0.45, 0.65] vs Fagundes' published 0.44–0.93 | `docs/35`:371 vs `progress_map`:563,607 | known-open **K8** |
| LS2D per-cell median | **12.77** (capped 12.49) vs published 2–10 | `progress_map`:550, `docs/00_INDEX`:180 | ✔ — now owned: `docs/37` §1 decision 4 retires the uncited 2–10 band; the *level* question it was probing is `docs/37` §4 **candidate 0** |
| LS **formulation** level vs the α = 11.8 reference | ours area-wtd **39.812** vs source-faithful **16.775** = **×0.421** (×0.333 with the Desmet–Govers `L`) ⇒ our LS is **2.37×–3.00×** high | `docs/agents/journal_decide-ls-resolution.md`:§1a,§3b; now in `docs/37`:§4 cand. 0 and `docs/35`:§9.3 | ✔ (measured on all 30,235,916 basin cells at 90 m) — **was absent from every numbered doc until 2026-08-11**, and it is the largest wrong-way term in C3: it takes 248.730 → 104.8/82.8 Mt/yr, implied SDR 1.37–2.22 |
| basin area-weighted C | 0.01082 | `progress_map`:553,555 | ✔ |
| sediment skill bar | KGE −0.26…0.44 (Fagundes) | `docs/19`:430,715, `docs/30`:101,119, `docs/31`:36 | ✔ |
| flux conversion | × **0.0864** | `docs/31`:34, `docs/34`:49, `docs/32`:99 | ✔ |

### 1.10 The outlet anchor (CALAMAR `29037020`)

| quantity | values found | verdict |
|---|---|---|
| upstream area | 257,097 km² | `docs/17`:68,499, `docs/19`:408 | ✔ |
| median Q | **6,954 m³/s** | `docs/17`:170,499, `docs/19`:408,707 | ✔ |
| mean Q | **7,433.4 m³/s** (`docs/18`:726) vs published **~7,100 m³/s** (`docs/34`:391) | ✔ false-alarm **F6** |
| specific runoff | **~880 mm/yr** (`docs/17`:68,499) vs **912.4 mm/yr** (`docs/18`:726) | ✔ **F6** (different periods/fields) |
| basin max flow | 14,909 m³/s | `docs/17`:341 | ✔ |
| SSC at the outlet | **none** | `docs/19`:408,707, `docs/32`:245 | ✔ |
| `R_AMS` at the outlet gauge | 1.690 | `docs/33`:860 | ✔ |

---

## 2 — NEW-unverified: genuine conflicts nobody has flagged

### N1 — `docs/33`'s "51.3 % surface" flow partition is the basin runoff coefficient, and it is not in the document it cites — **PRIZE**

**Claim A**, `docs/33_c2b_preregistration.md`:37-38 (repeated at :205 and :628):

> "- the model's internal partition is **51.3 % surface / 29.2 % subsurface / 19.5 % baseflow**
>   and was **never validated against observation** (docs/26 §A.3, RC 0.5127);"

**Claim B**, the cited source, `docs/26_phase3_refit.md`:251-253 (all of §A.3's balance sentence):

> "Engine run over 2008–2018, 2008 warm-up, 2009–2018 scored, 63 gauges. Mass-balance residual
> **9.66e-17** relative (bar < 1e-15); the negative-W guard never fired; RC 0.5127."

**Claim C**, `docs/26_phase3_refit.md`:330 (§A.6, the frozen-driver description):

> "Basin-mean 650 mm/yr generated surface runoff against 1,038 mm/yr total local runoff."

**The conflict.** `docs/26` §A.3 contains **no flow partition at all** — the only number it supplies
is `RC 0.5127`, which `data/processed/sim_calibrated_v2/report_H2E.json` names explicitly:
`"runoff_coefficient": 0.5126921499891222`, sitting beside `p_mm 22805.01`, `et_mm 11142.70`,
`runoff_mm 11691.95` — i.e. **total runoff ÷ precipitation over the whole record**, not a share of
runoff arriving by the surface path. `51.3 %` is `RC × 100`. The `29.2 %` and `19.5 %` figures
appear nowhere in `docs/26`, in `report_H2E.json`, or in any other numbered document; a repo-wide
grep finds the triple only in `docs/33` and in `progress_map.html` (which took it from `docs/33`).

**Resolution — measured here, read-only, from the frozen drivers.** Loading
`data/processed/sim_calibrated_v2/h2e_drivers.npz` and area-weighting by `own_area_km2`:

| quantity | value |
|---|---|
| generated surface runoff (`qsur_gen_mm`), area-weighted | **650.1 mm/yr** |
| total local runoff (`q_local_mm`), area-weighted | **1038.2 mm/yr** |
| **generated-surface share of local runoff** | **0.6262 = 62.6 %** |
| runoff coefficient (runoff ÷ P) | 0.5127 |

So the surface share is **62.6 %, not 51.3 %**, and the two numbers `docs/26` §A.6 already carried
(650 and 1,038) give exactly that. The remaining two components of the triple are unsourced.

**Why it matters, and why it is bounded.** The partition is one of the three stated motivations
for re-opening Phase B as stage C2b (`docs/33` §0), and it is re-used in `docs/33` §2.2 (:205) as
the "consistency check" and in §6.4 (:628-631) to compute a "**Gap: +0.602**" against `BFI_sim`
0.7965. Recomputed against the correct 62.6 %, that gap is +0.171 on the surface share, and the
0.195 baseflow figure it is compared against has no source at all. **No C2b verdict changes**:
`docs/33` §2.2 states "**No threshold attaches to this number**", §6.4 states "neither is a C2b
verdict", and both the H-BFI and H-PEAK gates read only paired filtered series. What changes is a
sentence quoted four times as a measured property of the adopted model.

**What would fully resolve it.** Recover, from whatever code produced the triple, what the 29.2 %
and 19.5 % denominators were; or re-derive all three from `h2e_drivers.npz` plus the engine's
internal `d_int`/`d_bas` terms and record them with an amendment note. **Do not silently edit**
`docs/33` — §1–§5 are frozen and §6/§7 are results; the correction belongs in a dated append.

---

### N2 — the "Phase C blocked" stale-prose register names the wrong documents

**Claim A**, `docs/31_phase_c_workplan.md`:480 (known-open register, entry 4):

> "| 4 | Older docs (12, 19, 21, 24, 25, 28) still carry \"Phase C blocked on mainstem SSC\" —
> superseded by docs/30 §1, not yet edited in place | docs/30 |"

(propagated verbatim to `docs/PROGRESS.md`:109 and `docs/00_INDEX.md`:209.)

**Claim B**, the documents themselves:

- `docs/19_sediment_qc_audit.md`:31 — "| **Phase C (sediment)** | **Unblocked as a data problem,
  bounded as a science problem.** The data exist; §3.9 states what they cannot answer |"
- `docs/21_project_state_and_handoff.md`:13 — "Phase C (sediment) is unblocked as a data problem
  and bounded as a science problem"
- `docs/12_sediment_data_status.md`:9 — "The sediment-data risk that was blocking Phase 3 is
  **largely resolved**"

and, **not on the register**:

- `docs/16_forcing_pipeline_audit.md`:26 — "Phase C (sediment) remains blocked on mainstem SSC data."
- `docs/16_forcing_pipeline_audit.md`:337 — "4. **Phase C sediment** — still blocked on mainstem SSC data."
- `docs/18_hydrology_journal.md`:35 — "| Phase C (sediment) | Still blocked — on mainstem SSC data
  and on the doc 19 `calibration_safe` gate |"

**The conflict.** Three of the six documents the register names say the *opposite* of what it
attributes to them, and the two documents CLAUDE.md calls "the knowledge base" and "the Phase B
record" — `docs/16` and `docs/18`, both marked `LIVE` in `docs/00_INDEX.md` — carry the stale line
and are not on the register. Only `docs/24`:36, `docs/25`:21 and `docs/28`:44 match the register's
description. A reader who trusts the register will clean the wrong files and leave the two
highest-traffic ones untouched.

**Resolution.** The register entry should read: **docs/16 (×2), docs/18, docs/24, docs/25,
docs/28**; and `docs/12`, `docs/19`, `docs/21` should be struck from it. Verified by
`grep -rn -i "phase c.*block|blocked on mainstem|still blocked" CLAUDE.md docs/` on 2026-08-11.
Note `docs/17`:28 carries a fourth-generation variant — "| **Phase B** | **Still blocked**" — which
is also stale and on no register.

---

### N3 — CLAUDE.md's and `docs/20`'s "non-negotiable" `_qc` file convention points at the superseded file

**Claim A**, `CLAUDE.md`:80-81 (under "Conventions and hard-won rules"):

> "- **Use the `_qc` files** (`precip_gauges_daily_qc.csv`, `precip_gauges_inventory_qc.csv`), never
>   the pre-repair ones, for any analysis. `approval == 'Inferido_seco'` marks inferred dry days."

restated at `docs/20_reproduction_guide.md`:109-111 under the heading "Non-negotiable conventions
on this chain":

> "- **Use the `_qc` files** (`precip_gauges_daily_qc.csv`, `precip_gauges_inventory_qc.csv`)
>   for any analysis; `approval == 'Inferido_seco'` marks inferred dry days."

**Claim B**, `docs/18_hydrology_journal.md`:489-490:

> "Outputs are written **alongside** v1 (`precip_gauges_daily_qc_v2.csv`,
> `precip_selectivity_report.csv`) so both remain available for attribution."

and `docs/18`:897-899:

> "`load_gauges()` reads `precip_gauges_daily_qc_v2.csv` - 926,910 rows, of which **240,158 are
> `Inferido_seco` zeros**"

**The conflict.** The file the two convention statements name is the **v1** repair output
(70 stations, 109,129 inferred-dry days, 686,752 station-days). The forcing the whole project runs
on is built from the **v2** file: `src/nbgen/make_nb11.py`:57 reads
`precip_gauges_daily_qc_v2.csv`, and `src/merge_chirps_gauges.py`:114 the same. Both files exist on
disk (`precip_gauges_daily_qc.csv` 30.0 MB, `precip_gauges_daily_qc_v2.csv` 34.3 MB). An analyst
following the stated rule reproduces the **2,174 mm/yr** v1 field instead of the **2,036 mm/yr** v2
field — a 6.4 % basin-rainfall difference, the exact quantity `docs/18` §10.5 reports as the
repair's headline effect. Only `src/nbgen/make_nb10.py`:38 legitimately still reads v1.

**Resolution.** The convention should name `precip_gauges_daily_qc_v2.csv` for anything downstream
of `src/repair_precip_selectivity.py`, and say explicitly that v1 is retained only for attribution
(`docs/18` §10) and for nb10's pre-repair comparison. Compounding it, `CLAUDE.md`'s "Pipeline
commands" block (:69-76) lists `repair_precip_zero_suppression.py` as "precip QC v2 (REQUIRED)" and
**omits `src/repair_precip_selectivity.py` entirely** — the step `docs/20`:61 calls "QC v3" and the
step that actually produces the shipped gauge file.

---

### N4 — CLAUDE.md still says the model period is bounded by ERA5; that was closed four sessions ago

**Claim A**, `CLAUDE.md`:87:

> "- Model period bounded by ERA5 (P∩PET); gauges span 2008–2018."

**Claim B**, `docs/18_hydrology_journal.md`:706-707 (§14.1):

> "**Open item 3 is closed.** PET now spans the full rainfall record, so the model period is no
> longer clipped to 2009–2017 by ERA5. That item had been open for four sessions."

and `docs/18`:288 (open-item table, item 3):

> "| 3 | ~~Extend the model period to 2008–2018~~ **DONE (§14)** — nb11 and nb12 executed; P and PET
> both span 2008-01-01..2018-12-31 (4,018 days)"

**The conflict.** The binding constraint on the model period is now the *gauge* record, not ERA5;
`CLAUDE.md`'s own next clause ("gauges span 2008–2018") is the operative one and contradicts the
first. The same sentence appears in `docs/16`:23 ("**Model period** | **2009-01-01 → 2017-12-31
(3287 days)** — bounded by ERA5, not rainfall"), which is correct *as of docs/16* but is the file
CLAUDE.md sends every new session to first. **Consequence measured elsewhere**: `docs/19` §3.8
(:391) still argues "2018 is a wasted harvest … entirely **outside** the 2009-2017 forcing window
(doc 16 §1, ERA5-bounded)" and `docs/19` §5.2 item 3 (:623-626) still lists extending the forcing
forward through 2018 as **blocking the sediment phase** — an open item that the 2008–2018 rebuild
already satisfied and that appears on no register as closed.

**Resolution.** Restate as: *model period 2008-01-01 → 2018-12-31 (4,018 days), 2008 warm-up,
2009–2018 scored; ERA5 no longer binds (docs/18 §14.1)*. Strike `docs/19` §5.2 item 3's
forward-extension half with a dated note.

---

### N5 — two different rationales are recorded for the same +4 gauges in the calibration set

**Claim A**, `docs/26_phase3_refit.md`:110-112:

> "Outside the matched comparison H2 gains 2018 as a validation year (KGE 0.235), **four gauges the
> co-located merge recovered**, and two fewer gauges below their energy floor (18 → 16)."

**Claim B**, `docs/18_hydrology_journal.md`:732-736 (§14.2):

> "**The calibration set grew to 63, and the prediction of 59 was wrong.** … But **extending the
> window to 2008–2018 gave gauges that previously failed the `n_window` gates enough record to
> qualify**, and that gain (+4 net) outweighed the exclusions. **A window change is not a filter on
> a fixed population; it changes the population.**"

**The conflict.** Both claim the same +4, and they attribute it to different causes: the co-located
*precipitation*-gauge merge (`docs/23` §11.2, three pairs merged) versus the *discharge*-record
window extension. These cannot both be the mechanism — the co-located merge touched rain gauges,
not discharge gauges, and `docs/23` §11.3 measures its effect as "+0.8 mm/yr (+0.04 %)" on areal
rainfall plus local changes at 542 minibacias; it has no path to a gauge's `n_window` eligibility.

**Resolution — the identities, from disk.** `feasibility_H1.csv` (61 codes) vs
`feasibility_H2.csv` (63 codes): the four added are `23087300, 26157080, 26187170, 26217050`; the
two dropped are `22017010, 23087200` — precisely the two gauges `docs/23` §12 triaged **EXCLUDE
D3**. That is the +4/−2 `docs/18` §14.2 describes, and it is the window/triage mechanism, not the
merge. `docs/26` §4's attribution appears to be wrong; it should be corrected with a dated note,
or restated as "four gauges the extended window qualified".

---

### N6 — `docs/24` slide 15 still quotes attempt-2 numbers after slides 8 and 9 were updated to attempt 4

**Claim A**, `docs/24_presentation_outline.md`:225-226 and :230-231 (slide 15, "What we cannot yet claim"):

> "- **Conventional adequacy is not reached.** Moriasi et al. (2007) put satisfactory *daily* NSE
>   above 0.50; **ours is +0.16 to +0.26**. …
> - **The ENSO asymmetry persists.** Skill over climatology is **+0.126** in La Niña against
>   **+0.026** in El Niño. We set out to halve that ratio; we have not."

**Claim B**, `docs/26_phase3_refit.md`:268 and :292 (the C0 addendum, dated 2026-08-10 — the same
date slide 8 was updated):

> "| **4 — H2E (v2 + new objective + FAO-56 ET)** | **0.356** | **0.130** | 0.591 | …"

> "| **skill over climatology** | **+0.106** | **−0.0005** | **+0.107** |"

**The conflict, inside one document.** `docs/24` slide 8 carries "*Table updated 2026-08-10 (Stage
C0) to add attempt 4*" (:90) and slide 9 carries an explicit "**Caveat added 2026-08-10 (Stage
C0), and it must be spoken, not skipped**" (:131). Slide 15, in the same file, was not touched: its
NSE range **+0.16 to +0.26** excludes the adopted configuration's **0.130**, and its ENSO-asymmetry
pair **+0.126 / +0.026** is `docs/26` §5's H1 (attempt 2) row, not H2E's **+0.106 / −0.0005**. The
"+0.026" is the very figure `docs/26` §A.5 (:300-305) warns "does **not** survive to the
configuration we adopted", and `progress_map.html`:452 records that warning against slide 9 only.

**Resolution.** Slide 15's two bullets need the same dated caveat slide 9 received; the honest
numbers for the adopted configuration are NSE 0.130 (VAL all) and skill-over-climatology
+0.106 / −0.0005. Slide 16 (:241-252) is in the same condition: items 2 ("Replace the ET stress
function with the FAO-56 threshold form") and 3 ("Add search seeds until the two forcing versions
separate") were both executed and reported in `docs/29`.

---

### N7 — `docs/33` registered, as H-CHIRPS, exactly the intervention `docs/31` B1 had already ruled insufficient — on the same day

**Claim A**, `docs/31_phase_c_workplan.md`:392-395 (background task B1, as corrected by review
finding F3 on 2026-08-10):

> "*The identified mechanism* of the +7.5 % volume failure is those 139 residual rain-selective
> stations transferred through reporting-day-conditioned maps (docs/18 §15.3) — **not** merely the
> absence of `Inferido_seco` days, which only dries already-repaired stations and would leave the
> volume gate failing."

**Claim B**, `docs/33_c2b_preregistration.md`:106-109 (H-CHIRPS, frozen 2026-08-10):

> "> Refitting the CHIRPS-gauge quantile maps on the **repaired** precipitation series —
> `precip_gauges_daily_qc.csv` with `approval == 'Inferido_seco'` days included, so the maps are no
> longer conditioned on reporting days only — brings the areal volume inside its pre-registered gate
> while retaining the LOOCV correlation gain."

**The conflict.** `docs/31` B1 states in advance that this exact change "would leave the volume gate
failing"; `docs/33` froze it as the hypothesis to test anyway, citing the diagnosis (`docs/18`
§15.3) that B1 had just corrected. `docs/30`:126-128 (§5.1) carries the same superseded spec
("refit quantile maps on the repaired series including inferred-dry days; rerun both gates").
The run then discovered something sharper — `docs/18`:898-902 (§15.5): "**The first thing the refit
found is that this was already the code's behaviour.**… those inferred zeros were in every pool
from the start: **240,115 of 926,268 paired station-days, 25.9 %**" — and reported it as a new
finding, without noting that `docs/31` B1 had predicted the null result. Note also that `docs/33`
names the **v1** file (`precip_gauges_daily_qc.csv`) while the code reads
`precip_gauges_daily_qc_v2.csv` (§N3).

**Resolution.** Nothing to recompute: the outcome (`docs/33` §7, `docs/18` §15.5) is consistent with
`docs/31` B1's prediction, and B1's re-spec — refit on **selectivity-passing** stations, or repair
the 139 residual stations first — is still the untried intervention. What is owed is a note in
`docs/33` §1 and `docs/30` §5.1 that B1 superseded the registered mechanism, so the next session
does not spend a third slot on the same no-op.

---

### N8 — `docs/33` §5.2's renumbering table is now wrong on two rows, and C4's pre-registration has no number

**Claim A**, `docs/33_c2b_preregistration.md`:484-489:

> "| content | docs/31 said | now |
> | C2b pre-registration (this file) | — | **33** |
> | C2 observed ENSO contrast | 33 | **34** |
> | **C4.2 sediment calibration pre-registration** | 34 | **35** |
> | C5.4 ENSO contrast results | 35 | **36** |"

**Claim B**, the disk: `docs/35_qpeak_preregistration.md` is the **C3.3 `q_peak`** registration
("**Stage:** C3.3 of `docs/31_phase_c_workplan.md`", :3), and `docs/36_peak_deficit_options.md` is
the peak-deficit adjudication.

**The conflict.** Row 4 was explicitly superseded — `docs/36`:9-11: "docs/33 §5.2 provisionally
reserved number 36 for 'C5.4 ENSO contrast results'. That reservation is superseded by this file…
**C5.4's results must take a later number (37+).**" **Row 3 was never corrected anywhere.** Number
35 is taken by the `q_peak` registration, so C4.2's sediment-calibration pre-registration — the
next pre-registration the project owes — has no assigned number in any document.
`progress_map.html`:577 handles it implicitly ("Writes docs/37+"), and `docs/00_INDEX.md`:124 says
"C4's and C5's write-ups take **37+**", but `docs/33` §5.2 is the table both `docs/31` and
`CLAUDE.md` point at. `CLAUDE.md`:45 propagates the superseded version outright: "…and it renumbers
the C2/C4/C5 docs to **34/35/36**." (`docs/00_INDEX.md` §7.6 flags the CLAUDE.md half only.)

**Resolution.** Add a dated amendment under `docs/33` §5.2 recording that rows 3 and 4 are
superseded, and that C4.2 and C5.4 take 37+ in the order they are written, checking
`docs/00_INDEX.md` §3 and `docs/agents/` for in-flight claims first.

---

### N9 — `docs/34` declares `docs/31` register item 5 closed; all three registers still list it open

**Claim A**, `docs/34_observed_enso_contrast.md`:394-396:

> "docs/06:9's \"~145–169 Mt/yr\" is therefore **confirmed as a plausible range but not as a single
> figure**: the two primary sources give 144 (1975–1995) and 184 (1980–2010) Mt/yr. **docs/31 open
> item 5 is closed by the two citations above.**"

**Claim B**, `docs/31_phase_c_workplan.md`:481:

> "| 5 | The Restrepo outlet-flux anchor (~140–180 Mt/yr) is unverified until C2.4 fetches the exact
> figure and citation | §0 table |"

and `docs/PROGRESS.md`:109 — "5. 🔴 Restrepo anchor unverified (→ C2.4)" — and
`progress_map.html`:634 — "docs/31 register — #1 railed-count RESOLVED ✅; kc_mult>1.2,
k_int_frac floor, **Restrepo anchor** open".

**The conflict.** C2.4 ran, the citations were fetched and verified against Crossref
(`docs/34` §5.1: Restrepo & Kjerfve 2000, *J. Hydrol.* 235(1–2):137–149,
doi 10.1016/S0022-1694(00)00269-9, **144 Mt/yr**; Restrepo & Escobar 2018, *Geomorphology* 302:76–91,
**184 Mt/yr**), and the closing document says so — but the register that owns the item, its
markdown ancestor and the live tracker all still show it open. `docs/00_INDEX.md`:151 repeats it a
fourth time ("the Restrepo anchor").

**Resolution.** Mark `docs/31` register item 5 **RESOLVED**, citing `docs/34` §5.1, and propagate
to `docs/PROGRESS.md`:109 and the tracker. Note the *derived* consequence stays open and is a
different item: `docs/34` §5.2 records a 6.0–13.8× shortfall of the observed network against those
anchors, and `docs/35` §9.1 / `progress_map`:635 record that the same anchors now sit against a
first-run erosion total that is 210× low under the registered unit convention.

---

### N10 — the tracker attributes an SNHT count to `docs/17` that `docs/17` does not contain

**Claim A**, `progress_map.html`:476 (C1.4 panel):

> "docs/17 found **25 SNHT breaks** inside 2009-2017,\n12 strong, shifts −65 % to +88 %."

**Claim B**, `docs/17_discharge_qc_audit.md`:233-235 (§3.8 heading and body):

> "### 3.8 SNHT: **24 strong discharge break candidates, 12 inside 2009–2017** — signal robust…
> 146/192 stations screenable … **82 exceed Tmax>25**, but … the **Tmax>50 tier (24 stations) is the
> action list**, and 12 of those break inside the calibration window, with neighbour-relative shifts
> of −65 % to +88 %."

**The conflict.** `docs/17` reports **24** strong candidates *in total*, of which **12** fall inside
2009–2017. The tracker reads it as 25 breaks *inside* the window of which 12 are strong. Neither
"25" nor "12 strong of 25" occurs in `docs/17`. The number matters downstream: `docs/32` §R4 (:212)
records "docs/17 names 24 Tmax > 50 candidates but only 7 station codes are recoverable in-repo and
no SNHT results file exists on disk", and `docs/34` §7.3 makes the incomplete break list a
first-order caveat on the only Magdalena-trunk rating.

**Resolution.** Trivial: the tracker panel should read "24 strong candidates (Tmax > 50), 12 inside
2009–2017". Flagged rather than edited — `progress_map.html` is inside the concurrent workflow's
blast radius.

---

### N11 — `docs/36` reports the peak/area analysis on 62 gauges where `docs/33` used 63, without saying which was dropped

**Claim A**, `docs/33_c2b_preregistration.md`:845-849 (§7.5 tercile table):

> "| large | 21 | **1,569 – 257,097** | 0.981 | 0.847 | 0.888 | 0.739 | 2.0 |"
> …with "| `R_AMS` | **+0.088** | 0.49 | **63** |" at :838.

**Claim B**, `docs/36_peak_deficit_options.md`:140-143 (§2.4(a)):

> "Per-gauge miss fraction vs log catchment area: Spearman ρ = **+0.018, p = 0.89, n = 62**. Area
> terciles: small (68–288 km², 21 gauges, 853 events) 79.2 % missed; mid (298–1,464 km²) 82.9 %;
> large (**1,563–54,035 km²**) 84.1 %."

**The conflict.** Both sections analyse "the per-gauge table" over the same fleet and the same
period, and the populations differ by one gauge: `docs/33`'s largest is 257,097 km² (CALAMAR
`29037020`), `docs/36`'s is 54,035 km² (ARRANCAPLUMAS `21237020`). `docs/36` never states that a
gauge was dropped or why, and its tercile boundaries shift accordingly (1,569 → 1,563; 288 vs 288
but 298–1,464 vs 298–1,563). The two statistics being compared are different (`R_AMS` vs miss
fraction), so this is not a contradiction of *result* — but it is an unexplained change of
population between the document that measured the deficit and the document that adjudicates it,
in the one section where the "no area gradient" refutation is stated (`docs/36` §2.7 leans on it).

**Resolution.** Read `data/processed/peakgap/per_gauge.csv` and state which gauge is absent and on
what rule (likeliest: the outlet gauge has no POT record under the same mask). One line in
`docs/36` §2.4.

---

### N12 — `docs/34` §3.3's caption says "four orders of magnitude"; its own numbers give 3.7

**Claim A**, `docs/34_observed_enso_contrast.md`:268-270 (§3.3, "Absolute levels"):

> "Wet-window mean daily flux spans **four orders of magnitude** across the fleet, 7.6 t/day
> (`26017060` PUENTE ARAGÓN, 152 km²) to 41,272 t/day (`21237020` ARRANCAPLUMAS, 54,035 km²) on
> estimator (a), P-LN."

**The conflict.** 41,272 ÷ 7.6 = **5,430**, i.e. **3.7** orders of magnitude, not four. This is the
"figure whose caption disagrees with its own numbers" class. It is cosmetic — no gate, ratio or
verdict reads it — but §3.3's whole purpose is to state absolute levels precisely, and the same
sentence is the one a reader quotes for the fleet's dynamic range.

**Resolution.** "more than three orders of magnitude (a factor of 5,400)". No committed number
changes.

---

## 3 — Resolvable-now: settled here from an artifact on disk

### R1 — `h2e_drivers.npz`: 546 MB and 521 MB are the same file in different units

`docs/26`:314 and `docs/20`:44 say **546 MB**; `docs/33`:456, `docs/36`:83/384/691 and
`progress_map.html`:453/455/612 say **521 MB**.

**Artifact:** `ls -l data/processed/sim_calibrated_v2/h2e_drivers.npz` → **546,366,478 bytes**.
546,366,478 / 10⁶ = **546 MB** (SI); / 2²⁰ = **521 MiB**. Both figures are correct; they are
decimal-MB and binary-MiB readings of one file. **Correct usage: 546 MB = 521 MiB.** Worth a single
parenthetical wherever it is quoted, because five documents currently look as if two files exist.
(`docs/31` C0.5 :88 predicted "~250 MB"; `docs/26` §A.6 :332 already explains the difference —
"larger than docs/31 C0.5's '~250 MB' estimate because that estimate assumed three fields, not
five".)

### R2 — energy-floor failures: 18 → 14 and 18 → 16 are both right, on different gauge sets

`docs/18`:609-611 and `docs/24`:163 say **18 → 14** ("of 61"); `docs/26`:112 says **18 → 16** (no
denominator).

**Artifacts:** `data/processed/sim_calibrated_v2/feasibility_H1.csv` (61 rows) → `energy_ok == False`
for **18**; `feasibility_H2.csv` (63 rows) → **16**.

| basis | failures |
|---|---:|
| H1 / v1 forcing, 61-gauge set (`docs/18` §10.6's fixed set) | **18** |
| H2 / v2 forcing, 63-gauge set (`docs/26` §4) | **16** |
| v2 forcing restricted to the 59 gauges common to both sets | **12** |
| of the 4 gauges present only in H2 (`23087300, 26157080, 26187170, 26217050`) | **4 — all fail** |

So the "18 → 14" figure is the standalone v1-vs-v2 comparison on a *fixed* 61-gauge set, and the
"18 → 16" figure is the H1-cell-vs-H2-cell comparison on *different* gauge sets that drop the two
`docs/23` §12 EXCLUDE gauges (`22017010`, `23087200`) and add four that all fail. **Neither
document states its denominator**, which is precisely the failure mode `docs/18` trap 23 warns
about ("Any 'N of 61' criterion written before a period change is stale"). Recommended phrasing:
*"18 of 61 → 14 of 61 on the fixed v1 set; 18 of 61 → 16 of 63 across the H1/H2 cells; 12 of the 59
common gauges."*

### R3 — the "CAL r" used in the F-ceiling arithmetic

`progress_map.html`:435 and the brief quoted at `docs/33`:433 use **0.518**; `docs/33`:415 and
`metrics_fleet.csv` (H2E, `fit`, CAL 2012-14) give **0.5564**.
**Artifact:** `data/processed/sim_calibrated_v2/metrics_fleet.csv` → `r = 0.5563967263058308`.
`docs/33` §4 already reports both and shows the verdict is identical (`F_max` 0.349 vs 0.386, both
far below 0.5), so nothing downstream moves — but **0.5564 is the on-disk value** and the tracker's
0.518 should carry that note. Listed under §4 as known-open **K4** because `docs/33` §4 flagged it
first.

### R4 — the C1 window gauge counts in `docs/13` vs `docs/32`

`docs/13`:12-19 gives, per station, "in 2011 / in 2015-16" counts (NEMIZAQUE 301/0, MATEGUADUA
109/0, PUENTE ARAGÓN 201/33); `docs/32` §R6.1 gives 302/0, 111/0, 207/34.
**Resolution:** `docs/13` counted raw common Q&SSC days; `docs/32` counted **QC'd valid samples**
after the C1 screens, on the registered windows. The offsets are +1…+6 and uniformly positive,
consistent with the different base. Not a conflict — but `docs/13` now carries a
`STATUS — HISTORICAL` header pointing at `docs/32` §R5, which is the right resolution and needs no
further action.

---

## 4 — Known-open: already on a register (confirming these is not a discovery)

| id | item | register entry |
|---|---|---|
| **K1** | `docs/24` slide 8 "3 of 10" vs `docs/26` §5 "2" railed parameters for attempt 3 | `docs/31` register #1 — **RESOLVED** in `docs/agents/review_2026-08-10_docs31.md` §3 (one 18-dim vector, two denominators); `docs/26` §A.2 and `docs/24` slide 8 both now state both |
| **K2** | `kc_mult` 1.662/1.836 off its rail but above the FAO-56 ≤ 1.2 bar | `docs/31` register #2; `docs/29` §Caveats |
| **K3** | `k_int_frac` on its 0.02 floor in 7 of 8 v2 seeds | `docs/31` register #3; background task B2 |
| **K4** | CAL r 0.518 vs 0.5564 in the F-ceiling arithmetic | flagged by `docs/33` §4's own boxed issue note ("Issue journalled, per the freeze rule"); tracker still uses 0.518 |
| **K5** | `R_POT` 0.567 (three documents) vs 0.5747 (artifact) | `docs/36` §7.3; `docs/00_INDEX` §7.2; tracker "New open items" #7. Locus worth naming: `docs/35` §5.2 quotes **both** in one section — table row "0.567" at :236 and "57.5 % of them" at :239 |
| **K6** | "43 % of flood events missed" is a count, not an identity, deficit (81.8 %) | `docs/36` §7.1 |
| **K7** | `docs/34`'s "22 of 22" is a pooled count across estimators and window pairs, not one artifact row | tracker "New open items" #3 (`progress_map.html`:498) |
| **K8** | registered β hard stop [0.45, 0.65] is narrower than Fagundes (2018) App. IV's published 0.44–0.93 | tracker "New open items" #6; `docs/35` §9's amendment procedure unused |
| **K9** | MUSLE area-unit convention (pixel km² / hectares / m³, 13.18× and 47.86× apart) | `docs/35` §9.1; tracker "Open registers" (`progress_map.html`:635) |

Also already recorded and not re-reported here: `README.md` stale (`docs/00_INDEX` §7.4),
`docs/PROGRESS.md` doc-index numbering stale (§7.1), `docs/open_questions.md` superseded
(`docs/00_INDEX` §3), `docs/progress_journal.md` stops 2026-08-03 (§5), `docs/31` C3.3's
"worst at the largest" peak-bias claim refuted (corrected in `docs/35` §5.2), C3.5 blocked
(`docs/35` §8 item 2, `docs/36` §7.4).

---

## 5 — False alarms: the same name, legitimately a different quantity

| id | apparent conflict | why it is not one |
|---|---|---|
| **F1** | observed recession constant 13.9 d / 10.40 d / 10.44 d / 9.5–11.9 d | Three estimators on three definitions, and each says so: `docs/22` §4.4 (≥3-day monotone declines below the 40th percentile, fleet median), `docs/26` §2 "Validation B" (reconstructed from prose — "Absolute constants differ … because the segment rule is reconstructed from a description. The **ratio** is what the objective and the criterion use"), `docs/33` §6.1 (master recession curve for the Eckhardt `a`). `docs/26` §A.3 additionally reports recession on **both** circulating definitions (ratio-of-medians vs median-of-ratios) because "they are not equivalent and picking one after the fact would be a choice" |
| **F2** | El Niño skill-over-climatology +0.024 vs −0.026 vs +0.026 vs +0.006 vs −0.0005 | Two axes at once: **which climatology benchmark** (`docs/26` §6 measures its own as "harder by +0.051 to +0.117 KGE" than `docs/22` §4.1's, and says so) and **which attempt** (Config B / H1 / H2 / H2E). Every value is correctly labelled at its own site. The residual risk is not the numbers but the deck quoting attempt 2's — see **N6** |
| **F3** | 63 / 61 / 59 / 57 / 55 / 54 gauges | 63 = H2E calibration-safe set; 61 = the v1 set; 59 = H1∩H2 for the matched comparison; **57, 54, 56 = gauges with enough record inside CAL 2012-14, El Niño 2015-16 and 2018 respectively** (`metrics_fleet.csv` `n` column); 55 = gauges clearing `docs/33` §2.1's ≥1,095-scored-day rule for the BFI statistic. All six are on disk and reconcile |
| **F4** | "6 bridging stations" (`docs/19`) vs "7 usable in both windows" (`docs/32`) | Different rules: `docs/19` §3.8 requires ≥30 clean paired SSC+Q days in both windows over the **safe-24** set; `docs/32` §R1 requires ≥ **N = 91** QC'd samples in both windows over the **28 mapped**. The sets are not nested and both are stated with their rule |
| **F5** | contrast "~3–9×" vs "2.8–4.6× / 6.4–9.3×" | The first is the honest combined range (`docs/34` §7); the second is the primary/sensitivity pair of headline medians quoted separately (`docs/34` §3.1: primary (b) 2.84 → (a) 4.62; sensitivity (b) 6.40 → (a) 9.32). `docs/34` §3.1 insists on the range form explicitly |
| **F6** | CALAMAR mean Q 7,433.4 m³/s vs published ~7,100; specific runoff 880 vs 912.4 mm/yr | Different records and windows: 7,433.4 / 912.4 are the v2 bundle's 3,992 valid days 2008–2018 (`docs/18` §14.2); ~880 is `docs/17`'s consolidation-era figure and ~7,100 is Restrepo & Kjerfve's 1975–1995 mean (`docs/34` §5.1). Median 6,954 is a third statistic. `docs/18` trap 9 ("no basin-mean figure means anything without its window attached") applies and is honoured at each site |

---

## 6 — Mis-citations and dead pointers found along the way

Not contradictions of fact, but each sends a reader to the wrong place.

| # | pointer | where | what is actually there |
|---|---|---|---|
| 1 | "docs/26 §A.3, RC 0.5127" cited for the flow partition | `docs/33`:38, :205 | §A.3 has no partition — see **N1** |
| 2 | "field LOOCV skill 0.429 (**docs/18 §12**, docs/26 §7…)" | `docs/31`:27 | `docs/18` §11–§13 were **moved to `docs/23`** (`docs/18`:661-663); `docs/23` §12 is the energy-floor triage. The 0.429 is `docs/18` **§14.1** (:696) |
| 3 | "**docs/32**, commit 542d5f6" cited for the CHIRPS-merge rejection | `docs/36`:343, :599 | `docs/32` is the SSC-quality gate and contains no CHIRPS content. The rejection is `docs/18` §15 (first) and `docs/33` §1/§7 + `docs/18` §15.5 (the refit). The commit id is correct |
| 4 | "the three pre-registered conditions (**§3.3**)" and the rule quoted as §3.3's | `docs/33`:952,960; `docs/36`:55 | The three success criteria and the quoted sentence ("Anything else is a failure of the refit…") are **§3.5** (:363-393). §3.3 is the cell specification |
| 5 | "fleet median R²(Qs vs Q) = 0.546 ✅ **as docs/13 expected**" | `progress_map.html`:480 | `docs/31` §0 (:33) established that "**docs/13** is the pairing-candidates doc — it carries **no R² values**"; the 0.54 / 33 pairs figure is `data/processed/rating_curves.csv`. The tracker reintroduces the attribution `docs/31` corrected |
| 6 | "docs/34_sediment_calibration.md" (C4.2 Out) and "docs/33, observed_enso_contrast.csv" (C2 paste-prompt) | `docs/31`:337, :241 | Both contradict `docs/31`'s **own** header note (:3-5), which assigns 34 = C2 observed contrast and 35 = C4 sediment calibration — itself now superseded (**N8**). `docs/33` §5.2 (:491) records that "docs/31 is not edited by this session" |

---

## 7 — What would resolve each NEW item, ranked by cost

| id | resolution | cost |
|---|---|---|
| **N1** | Re-derive the surface/subsurface/baseflow generation split from `h2e_drivers.npz` + the engine's internal terms; append a dated correction to `docs/33` (do not edit §1–§5) and to the tracker | ≤ ½ session; the surface number (62.6 %) is already measured here |
| **N2** | Rewrite `docs/31` register #4's document list from the grep; propagate to `docs/PROGRESS.md` and `docs/00_INDEX.md` §7.5 | minutes |
| **N3** | Change the `_qc` convention in `CLAUDE.md` and `docs/20` §3 to name `precip_gauges_daily_qc_v2.csv`, and add `src/repair_precip_selectivity.py` to `CLAUDE.md`'s pipeline block | minutes |
| **N4** | Restate `CLAUDE.md`'s model-period line; strike the forward-extension half of `docs/19` §5.2 item 3 with a dated note | minutes |
| **N5** | Correct `docs/26` §4's attribution (dated note): the +4/−2 is the window extension plus the `docs/23` §12 triage, verified from `feasibility_H1/H2.csv` | minutes |
| **N6** | Add the slide-9-style dated caveat to `docs/24` slides 15 and 16 | minutes |
| **N7** | Note in `docs/33` §1 and `docs/30` §5.1 that `docs/31` B1 superseded the registered mechanism | minutes |
| **N8** | Dated amendment under `docs/33` §5.2 (rows 3 and 4 superseded; C4.2/C5.4 take 37+); fix `CLAUDE.md`:45 | minutes |
| **N9** | Mark `docs/31` register #5 RESOLVED citing `docs/34` §5.1; propagate to `PROGRESS.md` and the tracker | minutes |
| **N10** | Fix the `progress_map.html` C1.4 panel to "24 strong candidates, 12 in-window" | minutes |
| **N11** | Read `data/processed/peakgap/per_gauge.csv`, name the dropped gauge and the rule, in `docs/36` §2.4 | minutes |
| **N12** | "more than three orders of magnitude (a factor of 5,400)" in `docs/34` §3.3 | minutes |

**Standing rule that applies to all twelve.** Several touch numbers that are committed or frozen
(`docs/33` §1–§5, `docs/34` §1, `docs/35` §4–§6, `docs/29` §1–§3). None of them may be edited
silently: every change needs a **dated amendment note** with its reason, per `docs/35` §9 and
`docs/33` §5.4. The two that touch a *frozen* section — **N1** (`docs/33` §0/§2.2) and **N7**
(`docs/33` §1) — must be appended as corrections, never overwritten.

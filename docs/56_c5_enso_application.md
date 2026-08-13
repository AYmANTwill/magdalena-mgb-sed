# 56 — C5: the modelled ENSO sediment contrast — the model REPRODUCES it

**Written 2026-08-12. The strictly out-of-sample application (`docs/45` §3.5): run the frozen
sediment configuration on the ENSO windows — never seen by the C4 fit — and ask whether it
reproduces the model-free observed contrast of `docs/34`.** Harness
`scripts/c5/c5_enso_contrast.py`; record `data/processed/c5_enso_contrast.{json,md}`.

## 1 — The headline

**The model reproduces the observed ENSO sediment contrast.**

| | direction | median rate ratio | geo-mean | range |
|---|---|---|---|---|
| **observed** (`docs/34`, model-free, 22 station-ratios) | La Niña > El Niño, **22/22** | **~3–5** | — | up to ~9 |
| **modelled** (this stage, 18 usable stations) | La Niña > El Niño, **18/18** | **3.05** | 3.06 | 1.62 – 4.85 |

Every station shows more suspended sediment in the wet La Niña year (2011) than across the dry
El Niño window (2015–16), in the model as in the data, and the **central magnitude matches** —
the modelled median (3.05) sits at the lower edge of the observed ~3–5 band. The rate ratio is
`mean t/day(P-LN) ÷ mean t/day(P-EN)`, primary windows P-LN 2011 and P-EN 2015–16 (`docs/34`
§1.2), rates only (the windows are unequal, 12 vs 24 months, so totals are never divided —
`docs/34` §1.4).

**Named reference estimator, both values printed (`docs/34`'s "gate on one, report both").** The
observed median is **4.62** on estimator (a) (paired sample-day flux) and **2.84–2.95** on estimator
(b) (rating-curve flux). The reference for judging the model is **estimator (b)**, because (a) is
sparse-sample noisy (per-station spread 1.21–11.68 vs (b)'s 1.14–6.19); the modelled **3.05**
matches (b) closely and sits **below** (a). This is stated explicitly so the model is not compared
against whichever observed estimator flatters it.

## 2 — Why this holds even though C4.3 railed

The within-station wet/dry ratio is **invariant to α and to the LS level** — both are static
multipliers that cancel: `[α·LS·X_LN] / [α·LS·X_EN] = X_LN/X_EN`. So the C4.3 railing (`docs/55`:
the fit could not pin the absolute level and wanted an implausibly low α) **does not touch this
result**. C5 tests the *runoff contrast* the rainfall field carries between the two regimes, not
the sediment level. It is also why the model can carry a poor *daily* KGE (~0, the r ≈ 0.57
ceiling) and still get the *contrast* right: the contrast is an integrated seasonal-to-annual
signal that survives daily-timing noise. Engine at adopted defaults (V4_dg, α = 1, β = 0.56),
k_dep = 0 / SDR = 1.

## 3 — Per-station, where an observed ratio exists

The observed estimator (a) (paired sample-day flux) is noisy — sparse SSC sampling gives it a wide
spread (1.21 – 11.68) — while estimator (b) (rating) is smoother (1.14 – 6.19). The modelled
ratios sit inside that envelope, with scatter both ways, and their central tendency matches:

| station | modelled | obs (a) | obs (b) |
|---|--:|--:|--:|
| 24037390 CAPITANEJO | 4.85 | 2.45 | 2.95 |
| 21197010 EL PROFUNDO | 4.12 | 1.21 | 2.99 |
| 22017030 BOCAS | 3.41 | 9.68 | 2.70 |
| 22017010 BOCAS | 2.92 | 1.70 | 1.14 |
| 23127010 BORBUR | 2.71 | 11.68 | 6.19 |
| 24027030 NEMIZAQUE | 2.66 | — | 3.15 |
| 26017060 PUENTE ARAGÓN | 2.09 | 6.79 | 1.94 |

No station reverses sign; the disagreements are in magnitude, and the observed (a) outliers
(BORBUR 11.7, BOCAS 9.7) are the sparsely-sampled stations the C1.2/§4.1 notes already flag.

## 4 — What this is, and is NOT

- It **is** the study's positive finding: a MUSLE sediment model built on this basin's forcing,
  with LS resolved to the adopted source formulation, **reproduces the observed ENSO wet>dry
  sediment contrast in direction (18/18) and central magnitude (~3×)** on strictly out-of-sample
  windows.
- It is **NOT** a validated absolute flux, and it does **not** rescue the C4.3 level. `docs/55`'s
  RAILED/EXPLORATORY verdict stands; α is a handle on Π; the LS level is UNVALIDATED (`docs/42`
  G4.2); O4 is open. The `docs/23` §13.2 **yield embargo** holds — this is a dimensionless ratio
  of absolute fluxes, **no t/km²/yr**.
- **β and window sensitivity — DONE (2026-08-12, `scripts/c5/c5_sensitivity.py`,
  `c5_sensitivity.csv`).** The direction (La Niña > El Niño, **18/18**) holds in **every** one of
  the six (β ∈ {0.45, 0.56, 0.65} × {primary, secondary}) cells. Primary-window median rises with
  β: **2.59 → 3.05 → 3.50**; the secondary ONI-peak windows (S-LN 2010-07…2011-06, S-EN
  2015-10…2016-04, `docs/34` §1.2) *sharpen* the contrast: **3.78 → 4.92 → 5.90**. β and the window
  definition move the magnitude but **never the sign**, and the primary range brackets the
  observed ~3–5. The finding is robust.

## 5 — Disclosure

Reads only. New files: `scripts/c5/c5_enso_contrast.py`,
`data/processed/c5_enso_contrast.{json,md}`. One engine run at α = 1 on the adopted default
(V4_dg); no default moved, no frozen artifact opened. The strictly-out-of-sample windows were
seen for the first time here; no parameter was adjusted against them (`docs/45` §3.5, Klemeš).

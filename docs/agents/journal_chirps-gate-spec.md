# journal — H-A: is the CHIRPS volume gate mis-specified?

**Agent:** `chirps-gate-spec`. **Date:** 2026-08-12. One of several parallel agents diagnosing
why the CHIRPS-gauge merge failed its volume gate at 2,188.5 mm/yr (+7.5 %).

**My assignment (paraphrased from the brief):** test H-A — *the gate is mis-specified*. Verify by
direct read what docs/18 §10.4 actually says about where the true basin areal mean lies; establish
what the gate target 2,036.4 mm/yr IS (and whether the uncited ~2,050 collaborator figure is
load-bearing in it); derive a defensible interval on the true 2009-2017 basin areal mean from
measurements this project holds, every leg cited; answer in/out for 2,188.5 with signed distance;
report the gate-width-to-knowledge-width ratio; draft (not enact) a registered gate revision, or
refuse with reasons. Also reconcile the direction-of-bias question across §9.4 / §10.4 / §10.6.

**Constraints I am operating under:** no commit/add/push; no edits to docs/18, docs/30, docs/33
(frozen), or docs/54 (synthesis agent owns it); no scripts in the repo (scratchpad only); no
rebuild of the merged field (RAM); verify from executed output.

---

## 1 — Reading log (direct reads, not from the brief)

Read in full, with line numbers captured:

- `docs/18_hydrology_journal.md` §9.1 (L317-336), §9.2 (L336-363), §9.3 (L363-382),
  §9.4 (L382-410), §9.5 (L410-456), §9.5b (L456-480), §10.1-10.7 (L480-661), §15.1-15.5 (L815-951).
- `docs/33_c2b_preregistration.md` §1 H-CHIRPS (L98-129) including the resolved-note (L100-104)
  and the frozen gate table (L114-117).
- `docs/21_project_state_and_handoff.md` §4 open items (L75-101) — item **4** (old 8) is the
  ~2,050 provenance item.
- `docs/40_sdr_evidence.md` header (L1-33) and §8 verdict + replacement clause (L514-600).

### Verbatim quotes I will rely on

`docs/18` §10.4, L584-586:
> "**The honest reading is that the true areal mean lies between the v2 and v1 figures, closer to
> v2** — a large step in the right direction with a bounded, measured over-correction, not an exact
> answer."

`docs/18` §10.5, L596-599 (the v1/v2 table): 2009-2017 v1 **2,174.3**, v2 **2,035.6**, change
−138.7 (−6.4 %); 2008-2018 v1 2,206.0, v2 2,072.3.

`docs/18` §10.5, L602-603:
> "v2 lands **0.7 % below the uncited ~2,050 reference**, which is notable but is not validation
> while that number has no citation (open item 8)."

`docs/18` §9.4, L406-409:
> "The ~2,050 reference is doing real work in this argument and its provenance is unverified.
> **Ask the collaborator for the citation before it is used as a validation target.**"

`docs/33` §1, L116 (frozen gate):
> "| volume | area-weighted basin areal mean, **2009–2017**, within **±1 %** of the gauge-only
> **2,036.4 mm/yr** → the interval **[2,016.0, 2,056.8] mm/yr** |"

`docs/40` §8.1 (the precedent, standing rule):
> "Per this run's standing rule — *an uncited plausibility band may not be used to pass **or** fail a
> gate* — the band is retired in **both** directions."

**Note on the precedent's shape:** docs/40 retires a band in BOTH directions. Whatever I conclude
about the ±1 % window, I may not use its retirement to ADOPT the merged field. Recorded here before
I measure anything, so it cannot be adjusted afterwards.

---

## 2 — What the gate target IS (executed measurement)

`src/merge_chirps_gauges.py:94-95`:
```
VOLUME_TARGET = 2036.4        # v2 gauge-only, area-weighted, 2009-2017
VOLUME_TOL = 0.01
```
`:484`  `vol_ok = abs(vol / VOLUME_TARGET - 1.0) <= VOLUME_TOL`.

So the gate is **self-referential**: the target is the merge's own gauge input volume, measured
with the same `areal_mean` (`:408-412`) on the same 8,672 centroids. It is **not** the uncited
~2,050 collaborator figure. `grep` for `2,050`/`2050` finds it nowhere in
`merge_chirps_gauges.py`. It reproduces: `bounds_fields.csv` F2 = **2036.3927** vs 2036.4 →
0.007 mm/yr (3e-4 %).

**The ~+0.8 mm/yr offset is identified and cited.** docs/18 §10.5 prints 2,035.6 / 2,174.3 on the
**294**-gauge set; `h3_bounds.py` runs `idwf.classify_colocated`+`merge_colocated` → **291**
gauges. docs/23 §11.3 L93-96 tabulates exactly this: "2009-2017 | 2,035.6 | 2,036.4 | **+0.8 mm/yr
(+0.04 %)**" and 2,072.2 → 2,073.1. My measurement: F2 rel offset **+0.0389 %**, F1 **+0.0399 %**
(2,174.3 → 2,175.167), F1's v1 case not tabulated in docs/23 but the same +0.04 %.
**VOLUME_TARGET is the POST-merge (291-gauge) value**, so the gate is like-for-like with the
merged field's own gauge handling. The offset is 2 orders below the ±1 % window and 3 below the
failure margin — it does not matter for any verdict. Recorded because the brief asked.

**The ±1 % WIDTH has no derivation anywhere.** `grep` across `docs/*.md`, `docs/agents/*.md`,
`src/*.py`: it appears only as an assertion — docs/18 §15.1 L833, §15.5 L912, docs/31 L396,
docs/33 §1 L116, `VOLUME_TOL = 0.01`, and `docs/agents/journal_chirps-merge.md` L6/L12/L65 where
it enters as the merge agent's *task Goal* with no argument. docs/18 §15.1 L831-832 is explicit
that it was "quoted from the task as registered in the run journal before any number existed".
**Pre-registered, yes. Derived, no.** Those are different properties and I will not conflate them.

## 3 — Executed measurements (scratchpad scripts, output verbatim in the logs)

- `h5_gate_arith.py` — re-derived from `cell_ledger.csv` alone: gauge-only **2036.3927**, raw
  CHIRPS **2124.7205**, mapped CHIRPS **2265.7574**, merged **2188.5404**; blend identity max
  |resid| 1.238e-3 mm; surplus decomposition +87.3022 / +64.8070 / +0.0086 / +0.0298 summing to
  +152.1477 with residual 2.25e-8. **Every brief figure reproduced.** No disagreement to report.
- `h4_credit.py` (background, exit 0, `h4_credit.log`) — three new gauge-only IDW fields:
  **F7 2128.046** (increment credited a flat 1.836 mm/day, docs/18 §10.4 verbatim),
  **F8 2143.623** (increment credited 0.4527 × the station's own ALL-DAY mean),
  **F9 2199.703** (ALL 240,115 inferred-dry days credited flat 1.836 — an *uncited* extension).
  Inferred-dry counts: v1 109,086, v2 240,115, increment **131,029 on 83 stations** — exactly
  docs/18 §10.4's "131,029 newly inserted days (83 stations)". Interpolator, centroid set and
  `areal_mean` identical to h3_bounds.py, so F1-F9 are like-for-like.

### Two things I found that the brief did not state

1. **F5's credit basis is wrong by a measured factor of 2.07.** On the 83 increment stations the
   mean reporting-day mean is **8.798 mm/day** against an all-day mean of **4.258** — ratio
   **2.066** (median 2.111). So `0.4527 × reporting-day mean` (F5 basis, median 3.753 mm/day)
   over-credits `0.4527 × all-day mean` (F8 basis, median **1.778** mm/day) 2.1×. F8's median
   credit agrees with §10.4's flat neighbour value **1.836 mm/day** to **3.2 %** — two
   independent bases converging. That is why F5 (2267.4) came out **above** F1 (2175.2): a
   "partial credit" larger than no repair at all is arithmetically incoherent. F5/F6 dropped.
2. **docs/18 §10.4 has an internal arithmetic inconsistency.** L575-577 print mean 1.836 mm/day
   on inserted days, 4.056 on all days, and "**ratio | 0.414**". But 1.836/4.056 = **0.4527**.
   0.414 is not the ratio of the two printed means (it may be a mean-of-per-station-ratios; I
   cannot settle that without re-running the selectivity test, and I did not). It does not move
   my verdict: F7 uses the mm/day figures directly and is immune; scaling F8's credit by
   0.414/0.4527 shifts F8−F2 from +107.230 to ≈ +98.1 → F8 ≈ **2134.5**, still OUTSIDE and
   further from the merged field. **Journalled as an unresolved defect in docs/18 §10.4, not
   fixed (docs/18 is off-limits to me).**

- `h6_map_volume.py` — the leg that decided the verdict. Basin-wide the map's TARGET volume is
  P = 2036.393 and its INPUT is Craw = 2124.720, so a working map moves CHIRPS **DOWN** by 88.328
  mm/yr. It moved it **UP by +141.037 (+6.638 %)**: |Cmap − P| = 229.365 against |Craw − P| =
  88.328, i.e. **2.597× further from its own target**. At the 291 fit points the map is almost
  exact (unweighted pooled Cmap/G − 1 = **+0.351 %**; n_pairs-weighted **+0.034 %**) while over
  the basin Cmap/P − 1 = **+11.263 %**. Fit-domain vs apply-domain, not a coding error.
  (My n_pairs-weighted pooled means are 5.0550 / 4.9276 / 5.0567; the brief's 5.1003 / 4.9626 /
  5.1182 are the **unweighted** means over the 291 gauges. Reconciled, no disagreement.)
- Per-stratum, `h6_map_volume.py`: **78.6 % of the surplus (86.2 % of the area) is in the 17
  strata that used their OWN (band × zone) pool**, several with 10-32 gauges and 30-99 k pairs.
  Only 21.4 % is in the 15 fallback-pool strata. **A "starved pool" explanation of the inflation
  is refuted by this table.** (Mechanism beyond H-A's remit — flagged for the other agents.)
- Local concentration (same script family): the rejected field's surplus is **+0.00 %** where
  w=0 (25.8 % of area), **+4.73 %** in the blend band (57.1 %), **+23.08 %** (+573.176 mm/yr) in
  the w=1 ≥30 km band (17.1 %).

## 4 — What I refused to claim

- **I did not use the ~2,050 collaborator figure in any leg.** docs/18 §9.4 L406-409 and docs/21
  §4 item 4 both say it is uncited on both sides; docs/40 §8.1's standing rule forbids it in
  either direction. It is also **not** in the gate: `VOLUME_TARGET` is 2036.4, an internal
  measurement. Anyone conflating the two would conclude the gate rests on an uncited number. It
  does not.
- **I did not use F4 (2330.489, no repair at all).** It asserts the whole repair is wrong; docs/18
  §10.4 L570-579 measures the opposite at 81 of 83 tested stations (2 wetter, 1 with ratio > 1.2)
  and §9.2/§10.3's dense-band null sits at 1.001/1.003 over 89 then 149 stations. F4 is a field
  the project's own falsification test refutes.
- **I did not use F5/F6.** Measured refutation in §3 above (basis 2.07× too wet; F5 > F1).
- **I did not let F9 (2199.703) set the interval**, even though it is the one construction that
  admits 2,188.5. It extends §10.4's 1.836 mm/day to v1's 109,086 insertions, which were **never
  falsification-tested** — `grep 109,129 docs/` finds no equivalent of §10.4 for them, and §10.1
  says v1's detectors (`dry_frac`, `ratio`) are different and looser statistics. An uncited leg
  cannot bound a gate (docs/40 §8.1). Reported as a sensitivity and labelled.
- **I did not claim the ±1 % width is "retired" by the docs/40 precedent.** docs/40 retires an
  uncited *plausibility band on a physical quantity*. ±1 % is an *engineering tolerance on a
  construction-fidelity check*. Different object; the rule does not transfer automatically. What I
  can say is that the width is underived — and that it is **not load-bearing**, because the
  failure is +7.471 %, 7.47× the tolerance.
- **I did not resolve** docs/18 §10.4's 0.414-vs-0.4527 ratio inconsistency (§3 above), nor the
  ~+0.9 mm/yr gap between my ledger's lag-aligned raw-CHIRPS centroid mean (2124.7205) and docs/18
  §9.5's E1 (2,123.8) — most likely the LAG = −1 window shift, but I did not measure it and it is
  0.04 %, so nothing here depends on it.

## 5 — Could not settle

- Whether the true 2009-2017 areal mean could be **below** F2. docs/18 §10.3's post-repair
  selectivity (sparse 1.040, n=81; mid 1.009, n=113) sits above its own 1.001 null, and §10.2
  left 33,953 days absent as outages that the IDW then fills from rain-selective neighbours. Both
  are measured evidence of a residual HIGH bias in v2 — but **nobody has converted either into
  mm/yr**, so I cannot put a number on the interval's lower end. Recorded as an open item.
- The mechanism of the map inflation (why a well-populated stratum pool inflates 6.6 % out of
  sample). Outside H-A; the per-stratum table above is handed to whoever owns it.

## 6 — Verdict and the draft I returned

**H-A is TRUE in its premise and FAILS to dissolve the problem, by 0.615 %.**

The premise holds: the ±1 % width is underived, and the project's own cited knowledge of the true
areal mean is **3.407× wider** (138.774 vs 40.728 mm/yr). But the widest interval every leg of
which is cited is **[2036.393, 2175.167]** (docs/18 §10.4's own v1/v2 bracket, on the 291-gauge
basis), and **2188.540 sits +13.374 mm/yr (+0.615 %) ABOVE its ceiling** — still OUTSIDE. The only
construction that admits it (F9, 2199.703) rests on an uncited extension to 109,086 never-tested
station-days.

And H-A rests on a category error I should name: the gate does **not** gate the true areal mean.
`VOLUME_TARGET` is the merge's own gauge input volume, so the gate is a **construction-fidelity**
check on the design property docs/18 §15 states in its own words — "gauges keep control of volume,
CHIRPS supplies structure". Re-specifying it as a plausibility band on the truth swaps a strong
test for a weaker one the merge never claimed to pass.

So I drafted a revision that goes the other way: keep the fidelity gate, make its target
self-computed rather than hard-coded, and **add a tolerance-free inequality derived from the map's
own stated purpose** — `|areal(Cmap) − areal(P)| ≤ |areal(Craw) − areal(P)|`. Zero uncited
constants. The rejected field fails it 229.365 vs 88.328 = **2.597×**. Full draft in the return
value for the synthesis agent to place in docs/54. I did not write docs/54 and did not edit
docs/18/30/33.

Scratchpad artefacts: `h4_credit.py` + `h4_credit.log` + `credit_fields.csv`, `h5_gate_arith.py`,
`h6_map_volume.py`.

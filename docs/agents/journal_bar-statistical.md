# journal — `bar-statistical` agent

**Task.** Propose ONE option for `docs/46`'s materiality bar, from the STATISTICAL angle:
if the bar should be a noise quantity, work out which noise quantity is defensible and derive
it properly from what is measured. Say plainly if no measured noise quantity is the right
comparator for a systematic formulation choice.

**Constraints I am operating under.**
- No edits to docs/46, 47, 48, 49, 50, 51. No git. No engine default changes.
- BLINDING: must not compute, estimate, or reason toward `Δ_shape`. Recorded below if I slip.

---

## Log

### 2026-08-11 — orientation
Read `docs/51` in full and `docs/48` in full.

Key facts carried forward (not re-measured yet):
- `σ_r = 0.465 ln` is an **observer-disagreement** statistic (`0.658/√2` between two observed-flux
  estimators). It is NOT a model−obs residual sd. `docs/48` §1 verifies the category error by
  reading, before computing.
- Measured residual sd, CAL 8, est (b): **1.9618 ln**; est (a): **1.3506 ln**. SE of fleet-mean
  level: **0.6936** / **0.4775**.
- `docs/48` §2.4 gives SEVEN admissible constructions, sd 1.2217 – 1.9618, SE 0.3054 – 0.6936.
- Station bootstrap (`docs/45` §4.2's registered interval convention) half-widths:
  est (a) ≈ 0.850 ln, est (b) ≈ 1.283 ln (from `docs/48` §5.3 column headers; §3.3 CI is
  asymmetric: (a) [−0.8279,+0.8721], (b) [−1.3163,+1.2503]).
- LOO range for the CAL 8 = **0.8602** = range(r_i)/(n−1) = 6.0214/7. Jackknife SE = sd/√n
  **identically** — measured 0.6936 both ways. So G12's LOO range is NOT an independent noise
  quantity; it is `range/(n−1)`, i.e. a different functional of the same 8 residuals.
- The residual heterogeneity is enormous: `I² 96–99.2 %`, `τ 2.03–3.40×` per station
  (`docs/47` §2.6 item 3, cited in `docs/48` §1).

Immediate structural observation to develop: **every** candidate noise quantity on offer is a
*sampling* quantity — dispersion of the fleet-mean **estimator** across resampled stations.
The thing the bar is applied to (`|ln f_A − ln f_B|`) is not an estimator at all: it is a
**deterministic** ratio of two field computations on the same terrain, with sampling variance
exactly ZERO. Need to work out whether comparing the two is defensible at all, or a category
error of the same shape as the one `docs/48` retired.

---

### 2026-08-11 — read `docs/46` §§1–10, `docs/47` §2.2, `docs/45` §4.2 (bootstrap convention)

Inventory of the ten bar uses, classified by **what kind of object the bar is applied to**:

| use | clause | object compared | sampling variance of that object |
|---|---|---|---|
| :138, :140-142 | the bar + its derivation | — | — |
| :189 | H-M **(R4)** `|ln f(V2b) − ln f(V2a)|` | two deterministic field computations | **0** |
| :217 | H-S **(R7)** per-cell `S` ratio spread | dispersion of a deterministic field | **0** |
| :240 | H-JOINT **(R10)** product vs joint | deterministic | **0** |
| :265 | H-L `|ln f(V5) − ln 0.790|` | deterministic vs a published prior computation | **0** |
| :490-491, :506, :538 | `Δ_shape` branch / Branch A precondition / **B1** | per-station erosion-weight perturbation | non-zero (it moves the residual vector) |

**Seven of the ten uses are on quantities with exactly zero sampling variance.** Three are the
`Δ_shape` discriminator. No single noise quantity can be the right comparator for both classes.

### Arithmetic I verified myself (nothing transcribed)

`0.658/√2 = 0.465276`; `0.465/√8 = 0.164402`; `range(r_i)/(n−1) = 6.0214/7 = 0.86020`;
`ln(0.43194/0.25146) = 0.541003`; `1/f = 2.315136 / 3.976776`; `|ln 0.431944| = 0.83953`;
`|ln 0.25146| = 1.38048`; `|ln 1.694054| = 0.52713`; `|ln 0.5807| = 0.54346`;
`|ln 0.517480| = 0.65879`; `|ln 0.362435| = 1.01497`.

**(R10) reproduced and its construction identified.** The 0.2983 in `docs/51` §5.5 uses the
**step** `V2b = 0.52204`, not the cap: `0.362435 × 0.52204 × 1.694054 = 0.320524`, and
`|ln(0.431944/0.320524)| = 0.298337`. With the cap it would be 0.307111. So R10's statistic is
`joint/product = ×1.34762`. Confirms `docs/51`; the arithmetic is not in question.

### MEASUREMENT 1 — (R10) fires on **every** admissible noise construction, not just est (b)

Ran all seven of `docs/48` §2.4's constructions against the statistics:

| construction | sd | SE | (R10) 0.2983 | levers immaterial (of the 4 big) | bracket width 0.5410 |
|---|---:|---:|---|---|---|
| CAL8/CALwin/(b) — `docs/42` §9 PRIMARY | 1.9618 | 0.6936 | **FIRES** | 3/4 (m-cap, S, L-form) | **IMMATERIAL** |
| CAL8/CALwin/(a) — `docs/45` §7.1 objective | 1.3506 | 0.4775 | **FIRES** | 0/4 | material |
| CAL7/CALwin/(a) C1.2-compliant | 1.3539 | 0.5117 | **FIRES** | 0/4 | material |
| CALwin-all n=10 /(b) | 1.8930 | 0.5986 | **FIRES** | 2/4 (S, L-form) | **IMMATERIAL** |
| all18/ENSOmed/(b) — the G1.2 basis | 1.4175 | 0.3544 | **FIRES** | 0/4 | material |
| all18/ENSOmed/(a) | 1.2217 | **0.3054** (min) | **FIRES** | 0/4 | material |
| CAL8/ENSOmed/(b) | 1.7159 | 0.6067 | **FIRES** | 2/4 (S, L-form) | **IMMATERIAL** |

Two findings:
- **The smallest admissible SE across every construction is 0.3054, and R10 = 0.2983 < 0.3054.**
  So "decide the levers as a set" is refuted by *any* honest rescaling. It is not an
  estimator-(b) artifact. The flip is unanimous.
- **The bracket-width verdict is not even construction-stable**: material on 4 of 7 equally
  admissible constructions, immaterial on 3. Two analysts obeying the same corrected rule reach
  opposite verdicts on the same number.

### MEASUREMENT 2 — the bar would have to be known to 2 % and is known to ±27 %

`sd(s)/s ≈ 1/√(2(n−1))`. At `n = 8` that is **0.267**; at `n = 16`, **0.183**.

| construction | SE | 95 % interval for the SE itself | is R10 = 0.2983 inside? |
|---|---:|---|---|
| CAL8/(b) | 0.6936 | [0.3303, 1.0569] | no |
| CAL8/(a) | 0.4775 | [0.2274, 0.7276] | **yes** |
| CAL7/(a) | 0.5117 | [0.2222, 0.8012] | **yes** |
| n=10/(b) | 0.5986 | [0.3221, 0.8751] | no |
| all18/(b) | 0.3544 | [0.2276, 0.4812] | **yes** |
| all18/(a) | 0.3054 | [0.1961, 0.4147] | **yes** |
| CAL8-ENSO/(b) | 0.6067 | [0.2889, 0.9245] | **yes** |

**R10's verdict is inside the sampling error of the threshold itself on 5 of the 7
constructions.** On the tightest construction the margin is `(0.3054 − 0.2983)/0.2983 = 2.4 %`
on a quantity whose own 95 % interval spans a factor of 2.1. A threshold that has to resolve a
2.4 % margin cannot be built from an estimate known to ±27 %.

*(Side confirmation of `docs/48` by an independent route: **0.1644 lies below the 95 % lower
bound of all seven constructions** — 0.1961 is the smallest. `docs/48`'s "no admissible
construction" holds not only as a point comparison but as a sampling-distribution rejection.)*

### The core statistical argument, worked out

**(1) Wrong error term — a paired contrast compared against an unpaired SE.**
`ln f_A − ln f_B` is a difference between two computations on *the same* DEM, *the same*
minibacias, *the same* stations, *the same* days. Under `docs/46` §6.1's own derivation, at
fixed shape the LS level multiplies every station's simulated flux by the same `f`, so the two
arms of the contrast share their entire residual vector. **The sampling variance of the paired
difference is identically zero.** `SE(fleet-mean level) = sd/√n` is the error term of an
*absolute, unpaired* level. Using it for a within-design contrast is the textbook wrong-error-term
error. It is the *same shape of category error* `docs/48` retired one level down (an
observation-side statistic used as a model-side one); here a sampling-side statistic is used for a
specification-side quantity.

**(2) The identifiability wall makes the draft's premise false.** The draft's stated derivation is
*"a difference in the LS level smaller than the standard error of the only fit that will ever
consume it cannot change any downstream statement."* But **the fit never consumes the LS level.**
`docs/46` §8.1: the uniform scalars' design matrix has condition number = **inf**; only
`Π = α·f_vol·f_K·f_LS·C_mult·P·FG` is identifiable. Swapping LS leaves `Π̂`, the objective value,
the residual vector and every residual statistic *identical*, and moves the implied `α̂` by exactly
`1/f` with no noise. The fit's detectability of an LS level change is **exactly zero at every
noise level** — so the SE does not bound it, and comparing to the SE implies a power calculation
that does not exist.

**(3) Non-composability, measured here.** At `docs/42` §9's registered primary construction
(SE 0.6936), R10 FIRES ⇒ `docs/46`'s own rule then says the levers are separable and may be
decided one at a time ⇒ decided one at a time, `S` (0.5271), the `L`-form (0.5435) and the `m`-cap
(0.6588) are each *immaterial* ⇒ no change is material ⇒ **yet their composition is 1.3805, a
factor of 3.98.** A decision rule that concludes "nothing here is material" about a ×3.98 change,
by three individually-immaterial steps, is internally inconsistent. Any aggregate noise quantity
has this property; only the falsified 0.1644 escaped it, and it escaped only because it was 4×
too small.

**(4) The one place a noise term is type-correct is vacuous in the other direction.** For *shape*
clauses the residual vector really does move, so an error term exists. But the type-correct one is
the **within-fit-set residual scatter** (1.2217 – 1.9618 ln), not the SE of the mean — the SE of
the mean is precisely the component a level absorption already removes. `docs/51` §5.4's
registered *bound* on the shape statistic is `ln 1.287 = 0.2523`, which is **0.21 of the smallest
admissible residual sd**. So on the type-correct shape error term, *every admissible value* of the
shape statistic is immaterial by construction — the test cannot fail, and a guard that cannot fire
is not a test (`docs/48` §5.4 makes the mirror-image point about guards that fire by
construction). **BLINDING NOTE:** this argument uses only the pre-registered *bound*, which
`docs/51` §5.4 publishes; it is an argument of the form "for ALL admissible values this bar gives
the same answer", never "the value will be X so choose Y". I did not compute, estimate or seek
`Δ_shape`, and I did not choose among candidate bars by where they would put it. See the
rejection below, which is the one place I had to be careful.

**Candidate I considered and REJECTED on principle, recorded because rejecting it mattered:**
using the per-station erosion-weighted LS ratio dispersion (`docs/47` §4.4) as the bar. It is
attractive — it is a within-object statistic of a deterministic field, not sampling noise. It is
**inadmissible** because it is the same quantity `docs/46` §6.1's pre-test measures, so defining
the bar from it makes §6.1 **circular** — exactly the defect `docs/48` §3.2 measured when it
rejected route 1 (defining the Π band from G12's own LOO quantities). Rejected on the project's
own precedent, without reference to any value.

**Also considered and rejected: an "analyst-choice" (multiverse) yardstick.** `σ_r` is not
sampling noise; it is the disagreement between two admissible *constructions* of the observed
flux, which is structurally the same kind of thing as a formulation choice. Measured directly on
the object that matters: the fleet-mean level is **+2.5772 ln under estimator (a) and +1.9240 ln
under (b) ⇒ a common-mode displacement of 0.6532 ln** (`docs/48` §3.3), consistent with the
pair-σ 0.658. Two reasons it fails: (i) a **systematic, common-mode** displacement does not shrink
with `n`, so the `/√8` in 0.1644 is wrong for this framing even before the numerator is corrected
— the type-correct value is ≈0.65, not 0.164; (ii) at ≈0.65 it lands in the non-composability
regime of (3). A bar built from one unresolved ambiguity licenses ignoring every other ambiguity
of similar size, and they compound rather than cancel.

**Conclusion of the statistical search.** The two error terms that are type-correct are **0** (for
level clauses) and **≥ 1.22 ln** (for shape clauses). Neither is usable as a materiality bar, and
nothing in between is derivable from a measured noise quantity. **The search terminates in a
negative, not in a value.** That is my proposal.

### What replaces the bar operationally (so the document stays freezable)

1. **Reading clauses** → decided by source text + `docs/46` §4.1 grade. No threshold. Empirically
   this is what actually happened: all four levers reached CITED (`docs/51` §1.2) and **the bar
   decided none of them.**
2. **Field clauses** → report the exact measured ratio at full precision; the clause text states
   what that licenses. `×1.0088`, `×1.0251`, `×1.34762`, `×1.7177` are more informative than
   "material"/"immaterial" and cannot be gamed by moving a threshold.
3. **Adoption** → `docs/46` §4.2's rule hierarchy (fidelity to the transposed method → cited
   deviation only → α band rescaled → ties toward the lower LS). **It contains no threshold and
   never did.**
4. **Reproduction/agreement gates keep their numeric tolerances** (the project's `1e-8`-style
   exactness gates, `docs/49`'s gate 2, `report_h2e.py`'s 1e-8). Those are *agreement* tolerances
   on quantities that should be identical, not materiality bars, and nothing here touches them.

### Why the two surviving bar-dependent conclusions dissolve anyway

- **(R10)** — with all four levers CITED and eq. 13 read verbatim on p. 47, the source formulation
  is a single object read whole. Whether the *arithmetic* is separable (×1.34762) is a reportable
  fact; **how to adopt is answered by the source, not by a threshold.** (R10) is no longer a
  question a statistical bar should answer at all.
- **bracket WIDTH** — `docs/51` §2.3: the span is not an uncertainty interval, it is the `L`-form
  lever, and the source names eq. 13. There is no width to adjudicate; there is a point and a
  documented hybrid retained for reproducibility.

Neither needs a number. The endpoints-vs-1.0 statements (0.8395, 1.3805) are robust at every
construction and are unaffected.

### Δ_shape and §6.1 under this proposal — stated so the blinding is auditable

I am **not** supplying a threshold for `Δ_shape`, and the reason is value-independent:
`docs/51` §5.4 records that the branch is already determined by **B2** (ADOPT is unreachable, so
Branch B is mandatory) *regardless* of `Δ_shape`. The threshold therefore has no decision content
left; what is owed is the **record**. So §6.1 should register `Δ_shape` as a **reported
diagnostic** with its exact discriminator stated — the fit is recoverable by rescaling `α̂` **iff
`Δ_shape = 0` exactly**, which is the mathematically true statement — and any positive number is
an approximation tolerance, not a branch. This removes a comparison that would otherwise have
produced a verdict; I flag that explicitly as the place a reviewer should push hardest, and it is
carried into the honest-weakness field of my return.

### Self-check against the forbidden move

- I never computed, estimated, simulated, or looked up `Δ_shape`. I used only the published bound
  `≤ 0.2523` from `docs/51` §5.4, and only in a for-all argument.
- I did not choose the proposal by where it puts `Δ_shape`. The proposal is "no number", which is
  the one choice that cannot be tuned to a side of `Δ_shape`.
- I rejected the one candidate bar (per-station LS ratio dispersion) that would have been derived
  from the same quantity, on circularity, before considering any value.

### Files written by this pass

`docs/agents/journal_bar-statistical.md` (this file) only. `docs/46` was **read, not edited**;
`docs/47`–`docs/51` read, not edited; no `data/` product opened for writing; no engine run, no
fit, no default changed, no git command.

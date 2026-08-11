# Journal — decide-ls-aggregation

## Goal
Determine (a) which LS2D statistic MUSLE requires when a fine-resolution LS grid is
aggregated to a coarser computational unit, and (b) at what spatial scale the MUSLE
equation should be APPLIED (per pixel then summed, vs once per URH/HRU). Both must be
decided from the algebra and from the source method — never from what makes the basin
total match the 144–184 Mt/yr outlet anchor.

## Discipline commitment
I will write the DECISION and its justification into this journal BEFORE computing or
looking up what it does to the basin total. "It makes the number match" is not evidence.

## Checklist
- [ ] 1. Read src/mgb_sediment.py to state exactly what is implemented now.
- [ ] 2. Read data/processed/peakgap/method_research.md + docs/33,35,36 for the source
      method's application scale.
- [ ] 3. Algebra half A: what aggregate LS reproduces sum_i(area_i * f * LS_i) exactly?
      Can the median ever be correct?
- [ ] 4. Algebra half B: general form of the pixel-sum vs unit-once ratio in n and beta.
- [ ] 5. WRITE DECISION HERE (both halves), justified, BEFORE any basin-total arithmetic.
- [ ] 6. Only then: quantify the multiplicative factor of recommended vs implemented.

## Log
### Step 0 — journal created
Starting. Nothing computed yet.

### Step 1 — what is implemented now (READ, not assumed)
- `src/mgb_sediment.py` L808-816 `cell_static_factor`: `(A_cell/a_p) * alpha * K*C*P*LS2D*FG`,
  with `LS2D = geom.cell_ls2d` = `urh_ls2d.csv:ls2d_hs` (L594-713 `load_geometry`,
  default `ls2d_column="ls2d_hs"`).
- `src/mgb_sediment.py` L830-841 `runoff_energy_term`: `(Qsur * (Qsur*a_p/86.4) * a_p * vf)^beta`
  evaluated ON THE PIXEL, `a_p = 0.0081 km2`.
- `scripts/c3/ls2d.py` docstring L110-115, verbatim: "`ls2d*` are AREA-WEIGHTED MEANS of the
  per-cell values inside the minibacia (weights = true cell area, which varies with
  latitude). `ls2d_median` / `ls2d_p90` are the EXACT per-cell median / 90th percentile of
  `ls2d` inside the minibacia".
  => **The column already in use, `ls2d_hs`, IS the area-weighted mean.** And `ls2d_median`
  is the median of the UNCAPPED `ls2d`, i.e. the "mean 30.6 vs median 16.6, factor 1.8"
  contrast in my brief compares two DIFFERENT variants (capped mean vs uncapped median), not
  two statistics of the same field. There is no per-cell median of `ls2d_hs` on disk at all.
- `data/processed/urh_ls2d.csv` header: `mini,urh,n_cells,area_km2,area_frac,ls2d,ls2d_hs,
  ls2d_mb86,ls2d_dg96` — confirms per-(minibacia,URH) rows, one LS value per cell, no
  quantile columns at URH level.

### Step 2 — the source method's application scale (repo evidence, quoted)
- `docs/35_qpeak_preregistration.md` §3(iii) L134-140, verbatim: "eq. 7: `qpico_{i,j}^k =
  Dsup_{i,j}^k · A_{i,j}^k / 86.4` preceded by: *'the peak rate of surface runoff in each
  pixel k is obtained considering a runoff volume uniform through the day.'* with **eq. 5**
  `SED = 11.8·(Qsup·qpico·A)^0.56 · K·C·P·LS·FG` applied **per DEM pixel** inside each URH of
  each minibacia (eq. 6)".
- `data/processed/peakgap/method_research.md` §1.1 confirms the same eq. 7 in Buarque (2015)
  p.59 and Fagundes (2018) eq. 12, "em cada pixel k".
- `method_research.md` §2.1: SWAT applies MUSLE **per HRU** with `q_peak` from the modified
  rational method — a different (coarser) application scale, and a different `q_peak`.
=> The source method for THIS transposition (MGB-SED) applies MUSLE per DEM pixel. Our
   implementation matches it. SWAT does not, and SWAT is not the method being transposed.

### Step 3 — ALGEBRA, half A: which LS statistic is the aggregation?
Let a computational unit U be built from sub-units i (DEM cells) of area `area_i`, and let
`f` denote every MUSLE factor other than LS. Within one (minibacia, URH) cell of THIS model
`f` is provably identical for all i: `Qsur` is stored per minibacia (frozen drivers), `K` is
per minibacia, `C`/`P` are per land class, `a_p` and `alpha`,`beta`,`FG` are constants. So

    Sed_U  =  sum_i ( area_i * f * LS_i )  =  f * sum_i ( area_i * LS_i )                (A1)

Now demand a single aggregate `LS_agg` that, applied once to the whole unit, reproduces (A1):

    f * ( sum_i area_i ) * LS_agg  =  f * sum_i ( area_i * LS_i )
    =>  LS_agg = sum_i(area_i * LS_i) / sum_i(area_i)                                    (A2)

which is the **area-weighted arithmetic mean**, and it is an IDENTITY, not an approximation.
It is unique: (A2) is the only solution of a linear equation in `LS_agg`.

Why no quantile can be correct. `sum_i area_i LS_i` is a *linear functional* of the LS
distribution. The only aggregate that preserves a linear functional under summation is the
corresponding weighted mean; a quantile is not linear (`median(X+Y) != median(X)+median(Y)`),
so it cannot reproduce (A1) except by coincidence. Concretely, for the right-skewed LS field
we have (log-normal-like, heavy upper tail from steep Andean cells) the median sits far below
the mean and the deficit is exactly the tail that carries most of the erosion. A median LS is
therefore not a different aggregation of the same quantity — it is a DIFFERENT QUANTITY
(a typical cell), and using it silently deletes mass.

The only honest argument for the median is ROBUSTNESS: that extreme per-cell LS values are
DEM artefacts. But that is a claim about the VALIDITY of the tail, not about aggregation, and
its correct remedy is to bound the tail at source with a stated physical reason — which
`ls2d_hs` already does (upslope area capped at the 1 km2 channel-initiation threshold,
Montgomery & Dietrich 1988/1992; `scripts/c3/ls2d.py` docstring). Replacing a valid mean with
a median because *some* of the tail may be artefact would also delete the *valid* part of the
tail, and would do so by an amount nobody can state.

Generalisation, recorded because it matters if `f` ever stops being uniform: if the sub-units
differ in the other factors too, the exact aggregate is the **f-weighted** mean,
`LS_agg = sum_i(area_i f_i LS_i) / sum_i(area_i f_i)`. It reduces to (A2) iff `f_i` is
constant, which is the present case. If a future version puts `Qsur` on the URH columns, (A2)
stops being exact within a MINIBACIA but stays exact within a URH cell.

### Step 4 — ALGEBRA, half B: the application-scale ratio
Split a unit of area `A` into `n` equal sub-units of area `a = A/n`, uniform `Qsur`, all other
factors uniform. With Buarque eq. 7, `q_peak(a) = c * Qsur * a`, `c = 1/86.4`:

    X(a) = Qsur * q_peak(a) * a * vf = vf*c * Qsur^2 * a^2          (the MUSLE argument)
    Sed(a) = alpha * X(a)^beta * K*C*P*LS

  (a) apply per sub-unit, then sum:
      S_fine  = n * alpha * (vf*c*Qsur^2*(A/n)^2)^beta * KCPLS
              = n^(1-2beta) * alpha * (vf*c*Qsur^2*A^2)^beta * KCPLS
  (b) apply once at unit scale:
      S_lump  = alpha * (vf*c*Qsur^2*A^2)^beta * KCPLS

    RATIO  R = S_lump / S_fine = n^(2*beta - 1)                                          (B1)

Equivalently, total load at application unit `a` scales as `a^(2beta-1)`: coarser unit, more
sediment, because `2beta-1 = 0.12 > 0` (i.e. because beta > 1/2).

General form: if the MUSLE argument scales as `X ∝ a^p`, then `R = n^(p*beta - 1)`. Here
`p = 2` — area enters TWICE, once explicitly as `A` and once inside `q_peak ∝ A`. This is why
the exponent is `2beta-1` and not `beta-1`: had `q_peak` been area-independent (`p=1`),
`R = n^(beta-1) = n^-0.44` and lumping would REDUCE the load. The sign of the scale effect is
a property of eq. 7, not of MUSLE alone.

Consequence worth stating before any number is looked at: the exponent is 0.12, so the
application scale is a **logarithmically weak lever**. To gain a factor 10 you would need
`n = 10^(1/0.12) = 10^8.33 = 2.2e8` sub-units lumped into one — more than the whole basin has
pixels. This bounds what half B can possibly contribute, independently of any measurement.

### Step 5 — DECISION (written BEFORE computing any factor or basin total)
I state here, and I confirm I have NOT yet computed the effect of either choice on the basin
total or on the 144-184 Mt/yr anchor:

**(a) LS aggregation = the AREA-WEIGHTED ARITHMETIC MEAN of the per-cell LS over the
computational unit.** Justification: eq. (A2) — it is the unique aggregate that reproduces
`sum_i(area_i * f * LS_i)` exactly, because MUSLE is LINEAR in LS. The per-cell median is
mathematically incapable of reproducing a linear functional and, on a right-skewed LS field,
systematically discards the tail that carries the erosion. This is what
`urh_ls2d.csv:ls2d_hs` already is, so **the implemented choice is already correct and I
recommend NO CHANGE.** (Direction note recorded in advance: switching to a median would LOWER
the total, i.e. move AWAY from the anchor — so this decision cannot be an artefact of
answer-chasing.)

**(b) Application scale = PER DEM PIXEL, summed** (`a_p = 0.0081 km2`, `A_cell/a_p` pixels
per URH cell). Justification: it is the source method verbatim — Buarque (2015) eq. 5-7
applied "per DEM pixel inside each URH of each minibacia", reproduced in Fagundes (2018)
eq. 11-12 and quoted in docs/35 §3(iii). It is also the scale at which the pre-registered
`alpha` band (11.8, hard stop 35.4) is defined. **The implemented choice matches the source
and I recommend NO CHANGE.**

**Therefore my recommended combination is IDENTICAL to what is implemented, and its
multiplicative factor versus the current implementation is exactly 1.000 x 1.000 = 1.000.**
Neither half of this task contributes anything to closing the order-of-magnitude gap. I am
recording that as the answer because it is what the algebra and the sources give, not because
it is useful.

**Caveat I must NOT resolve by convenience — the `alpha`-scale-consistency question.**
Eq. (B1) says the numerical value of `alpha` is meaningless without the application scale it
was fitted at: `alpha` transfers between scales as `alpha(a') = alpha(a) * (a/a')^(2beta-1)`.
Williams (1975) fitted `alpha = 11.8` on whole small experimental watersheds with ONE
`(V, q_p)` pair each — not on 0.0081 km2 pixels. If that is right, applying 11.8 per pixel is
a scale mismatch of `(A_Williams/a_p)^0.12`. I cannot settle this from the repo: neither
Williams (1975) nor the watershed areas he used are present here. I record it as UNRESOLVED
in §Findings and state what would resolve it, rather than adopting the reading that raises the
total. Counter-evidence already in the repo, which must be weighed against it:
`method_research.md` §1.2 reports Fagundes (2018) CALIBRATING alpha at this same pixel scale
against observed SSC on the 86,715 km2 Doce and recovering **6.93-18.86**, i.e. straddling
11.8 — which is what one would NOT see if pixel-scale application were badly scale-mismatched.

### Step 6 — verification computations (only now, after the decision above)

**6a. (A2) is exact in this repo's data, verified.** Rebuilding each minibacia's `ls2d_hs`
as `sum(area_cell * ls2d_hs_cell) / sum(area_cell)` over its URH cells and comparing to
`minibacia_ls2d.csv:ls2d_hs`: on the 7,382 minibacias with `urh_cover_frac == 1` the median
relative error is **7.4e-7** and the max **8.2e-6** (CSV print precision). The 1,290
partial-cover minibacias differ by a median 4.0 % — that residual is MISSING AREA (cells with
no URH code; 98.06 % of basin area is covered), not a wrong statistic. So the file's LS is
confirmed to be the area-weighted mean and the aggregation composes exactly.

**6b. What the LS numbers in my brief actually are** (correction). `ls2d_hs` median 30.605 is
the area-weighted MEAN of the CAPPED field; `ls2d_median` median 16.555 is the per-cell MEDIAN
of the UNCAPPED field. Not a like-for-like pair, so "factor 1.8" is not the mean/median gap.
Like-for-like on the one field that has both statistics (uncapped `ls2d`), basin
area-weighted: mean **104.90** vs mean-of-per-cell-medians **23.58**, ratio **4.449**. Per
minibacia the mean/median ratio has median **2.625** (p05 1.576, p95 31.09). Since MUSLE is
linear in LS, those ratios ARE erosion ratios. Adopting a median LS would therefore divide
basin erosion by roughly 2.6-4.4.

**6c. Half B verified against the engine, not just on paper.** Representative URH cell
(mini 6783, urh 31, area 4.7618 km2 = 588 pixels), real `K` 0.0302, `C` 0.0030, `P` 1.0,
`LS2D` 0.202, representative wet-day `Qsur` 1.3461 mm/d, through
`mgb_sediment.musle_load_tonnes`:
  - (a) per pixel then summed : 6.6193e-05 t/d
  - (b) once at URH scale     : 1.42274e-04 t/d
  - ratio (b)/(a) = **2.149383**; predicted `n^(2beta-1)` = **2.149383**; agreement
    **2.2e-16 relative** (bitwise, to float rounding).
  - Re-run at `Qsur` = 0.01 and 50.0 mm/d: ratio **2.149383** both times — Qsur-independent,
    exactly as eq. (B1) says it must be.

**6d. Scale-lever magnitudes across the real geometry** (32,782 URH cells, `a_p` 0.0081 km2,
`beta` 0.56; `R = n^0.12`):
  | lumping level | n (pixels) | R |
  |---|---|---|
  | median URH cell (4.366 km2) | 539 | **2.127** |
  | URH cells, weighted by their true decade contribution | — | **2.372** |
  | median minibacia (25.58 km2) | 3,158 | **2.630** |
  | whole basin as one unit (257,097 km2) — absurd, an upper bound | 3.17e7 | **7.947** |
Consistent with the pre-computed `a^(2beta-1)` prediction everywhere. So the ENTIRE
application-scale lever, taken to an indefensible extreme, is worth at most ~7.9x; at the
defensible SWAT-HRU-equivalent scale, 2.37x.

### Step 7 — FACTOR OF RECOMMENDED vs IMPLEMENTED
Recommended = (area-weighted mean LS) x (per-pixel application) = exactly what
`src/mgb_sediment.py` + `urh_ls2d.csv:ls2d_hs` already do.
**Multiplicative factor = 1.000 x 1.000 = 1.000. This run contributes NOTHING to closing the
gap.** Both alternatives I was asked to consider move the wrong way or are only weakly
available: a median LS would DIVIDE the total by 2.6-4.4; coarsening the application scale
would multiply it by at most 2.37x (URH) or 7.95x (whole basin), against a residual gap of
210-269x in the registered convention. Neither is the missing order of magnitude.

### Findings / UNRESOLVED
1. **UNRESOLVED — the scale at which Williams (1975) fitted `alpha` = 11.8.** By eq. (B1)
   `alpha` is only meaningful with its application scale attached, transferring as
   `alpha(a') = alpha(a)*(a/a')^(2beta-1)`. Neither Williams (1975) nor the drainage areas of
   his experimental watersheds are in this repo. What would resolve it: the watershed areas in
   Williams, J.R. (1975) "Sediment-yield prediction with universal equation using runoff
   energy factor" (ARS-S-40, pp. 244-252). Weighing against it, already in repo:
   `method_research.md` §1.2 — Fagundes (2018) calibrated `alpha` at this same pixel scale on
   the 86,715 km2 Doce and recovered 6.93-18.86, straddling 11.8. Also note the lever is weak:
   even a 1,000x scale error in `a` is only 1000^0.12 = 2.29x.
2. **Not a finding against us: our application scale MATCHES the source method.** SWAT's HRU
   scale is coarser, but SWAT is not the method being transposed, and its `q_peak` differs too
   (modified rational, `method_research.md` §2.1) — importing SWAT's scale without SWAT's
   `q_peak` would be mixing two methods.
3. `urh_cover_frac`: 98.06 % of basin area carries a valid URH code; 1,290 minibacias are
   partially covered. Erosion is only ever computed on covered area. Small, but it is a
   one-directional (downward) 1.9 % term nobody has listed.

### Checklist status
- [x] 1  - [x] 2  - [x] 3  - [x] 4  - [x] 5 (decision written before Step 6)  - [x] 6


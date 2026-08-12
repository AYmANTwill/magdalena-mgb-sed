"""MUSLE hillslope-erosion engine for the Magdalena basin (stage C3.4).

WHAT THIS IS
------------
A vectorised, importable implementation of **hillslope** (sheet + rill) soil loss with the
Modified Universal Soil Loss Equation, driven by the FROZEN H2E hydrology of Phase B.
It computes, per minibacia per day, the suspended-sediment load delivered from the
hillslopes to that minibacia's river reach, in **tonnes/day**.

It is NOT a channel model.  Advection, deposition and the Momposina floodplain sink are
stage C4 (``docs/31`` §C4.1) and deliberately absent here: this module's output is the
*input* to that step, so anything it produced downstream of the hillslope would be
double-counted later.

It re-runs NOTHING.  The hydrology is read from
``data/processed/sim_calibrated_v2/h2e_drivers.npz`` (546 MB, adopted cell H2E, FAO-56 ET,
``theta_crit`` 0.6, F 0.25931).  ``src/mgb_hydrology.py`` and that file are frozen twice
over (Phase B closed twice, docs/33 §8) and are opened read-only here.

THE EQUATION, AS PRE-REGISTERED (docs/35 §4, registered 2026-08-11) AND AS AMENDED
---------------------------------------------------------------------------------
::

    Sed_URH = (A_URH / a_p) * alpha * (Qsur * q_peak * a_p * f_vol)^beta
                            * (K * f_K) * C * P * (LS2D * f_LS) * FG
    q_peak  = Qsur * a_p / 86.4                        (Buarque 2015 eq. 7)
    a_p     = 0.0081 km2                               (COP90 pixel, the registered scale)
    f_vol   = 1000  (``volume_convention='williams_m3'``, DEFAULT since 2026-08-11)
    f_K     = 7.593014  (``k_unit_system='us_customary'``, DEFAULT since 2026-08-11)
    f_LS    = 1.0   (``ls2d_aggregation='area_weighted_mean'`` x ``ls2d_resolution='native_90m'``)

``f_vol`` and ``f_K`` are the two unit-system corrections adopted on 2026-08-11 (see
CONVENTION AMENDMENT below).  They are NOT calibration knobs: each is a fixed, derived
constant, and each is reversible by name.

i.e. MUSLE is evaluated **per DEM pixel** and multiplied by the number of pixels in the
URH cell, which is what keeps a fitted ``alpha`` comparable to Williams' 11.8 with no
scale correction (docs/35 §6.2: lumping ``N`` pixels inflates the load by ``N**(2*beta-1)``,
2.63x at the median minibacia).  ``q_peak`` is the registered proxy and is **not** a knob:
it comes from :mod:`scripts.c3.qpeak`, which this module imports rather than re-derives.

Every symbol, and where its number comes from:

===========  ===============================================  ==================================
symbol       meaning                                          source
===========  ===============================================  ==================================
``Qsur``     surface-runoff depth, mm/day                     ``h2e_drivers.npz:qsur_rel_mm``
``q_peak``   peak runoff rate, m3/s                           ``qpeak.qpeak_daily_mean`` (docs/35)
``a_p``      MUSLE application area, km2                      ``qpeak.COP90_PIXEL_AREA_KM2``
``A_URH``    URH cell area, km2                               ``urh_fractions.csv`` x ``minibacias.csv``
``K``        soil erodibility, per minibacia                  ``minibacia_soil_params.csv:K`` (nb09 §4)
``C``,``P``  cover / practice, per land class                 ``urh_cp_factors.csv`` (C3.2)
``LS2D``     2-D topographic factor, per URH cell             ``urh_ls2d.csv:ls2d_hs`` (C3.1)
``FG``       coarse-fragment factor                           1.0, see FG below
``alpha``    11.8                                             Williams (1975) - STARTING VALUE
``beta``     0.56                                             Williams (1975) - STARTING VALUE
===========  ===============================================  ==================================

``alpha`` and ``beta`` ARE NOT TUNED VALUES.  They are the published Williams (1975) pair,
adopted unchanged by Buarque (2015) eq. 5 *with this same daily-mean* ``q_peak``, and they
are here only so the module runs before stage C4 fits them.  C4's registered bands and hard
stops live in ``qpeak.check_musle_parameters`` - call it, do not retype the numbers.

CONVENTION AMENDMENT - 2026-08-11 - TWO DEFAULTS CHANGED, WITH THEIR REASONS
---------------------------------------------------------------------------
Stated here, at the top, because a silently changed default is the failure mode this module's
docstring exists to prevent.  Both changes are unit-system corrections resolved from source
derivations, and both are recorded as an amendment in docs/35 §9.2.

1. ``volume_convention``: ``'pixel_km2'`` -> ``'williams_m3'`` (x1000 product, x47.8630 load).
   REASON.  Williams' English-unit regression is ``Y[short ton] = 95 (Q[acre-ft] * q_p[cfs])^0.56
   K C P LS``.  Converting the dimensional quantities only (1 acre-ft = 1233.4818375 m3,
   1 cfs = 0.028316846592 m3/s, 1 short ton = 0.90718474 t) gives
   ``95 * 0.90718474 / (1233.4818375*0.028316846592)^0.56 = 95*0.90718474/34.92823^0.56 =
   11.7818``, i.e. **11.8 is the coefficient for runoff volume in m3 and q_peak in m3/s**
   (0.15 % from the published 11.8).  Read as ``mm*ha`` the same derivation gives 42.78, read
   as ``mm*km2`` it gives 563.95 - so neither ``swat_mm_ha`` nor the previously registered
   ``pixel_km2`` can carry ``alpha`` = 11.8.  Independently re-derived twice (a decision pass
   and an audit pass) with the same result.

2. ``k_unit_system``: NEW option, default ``'us_customary'`` (stored SI K x 7.593014).
   REASON.  The conversion in (1) leaves ``K``, ``C``, ``P`` and ``LS`` untouched, so
   ``alpha`` = 11.8 goes with the **US-customary NUMERIC** values of those factors.  But
   ``minibacia_soil_params.csv:K`` is stored in SI: ``notebooks/09_soil_parameters.ipynb`` §4
   says so in as many words - "mid-range Wischmeier & Smith (1978) class values **converted to
   SI (x0.1317)**", table Coarse 0.020 / Medium 0.045 / Fine 0.028 - and
   ``src/nbgen/make_nb12.py`` labels the array ``t.ha.h/ha/MJ/mm``.  Undoing the documented
   transform returns the textbook US-customary numbers it was built from
   (0.020/0.1317 = 0.1519 ~ sand 0.15; 0.045/0.1317 = 0.3417 ~ silt loam 0.34;
   0.028/0.1317 = 0.2126 ~ clay 0.21), which identifies the transform rather than inferring
   it.  Using SI K with ``alpha`` = 11.8 is therefore a dimensional error of exactly
   ``1/0.1317 = 7.593014``.  Stated imprecision: the SI table is rounded to three decimals, so
   the recovered US numerics carry <= 1.3 % rounding residue.  Not a fitted quantity.

   CONSEQUENCE FOR THE docs/35 §6.1 GUARD, spelled out because it cuts both ways: before this
   amendment a fitted ``alpha`` was being compared against Williams' 11.8 across two different
   unit systems, 363.42x apart, so the guard was **not meaningful** - it could not have fired
   for the right reason.  Under the adopted convention the comparison is like-for-like and the
   band (5.9 - 23.6, hard stops 3.9 and 35.4) is meaningful **for the first time**, unchanged.
   The §6.3 ``beta`` guard was never affected: a constant unit factor ``F`` moves ``alpha`` by
   ``F^beta`` and leaves ``beta`` untouched, so 0.45-0.65 stands as registered.  §6.2's
   scale rescaling ``N^(2*beta-1)`` is dimensionless and also stands.

3. NOT changed, and named so the absence is auditable: ``ls2d_aggregation`` and
   ``ls2d_resolution`` are new EXPLICIT options whose adopted values reproduce exactly what
   this module already did (factor 1.000 each).  See LS2D AGGREGATION AND RESOLUTION below.

INPUT AMENDMENT - 2026-08-11 - THE COVER FACTOR C (docs/41; a THIRD default moved)
---------------------------------------------------------------------------------
4. ``load_geometry(cp_revision=...)``: NEW option, default ``'cited_central_2026_08_11'``
   (x1.2043 on the basin total, 248.730 -> 299.539 Mt/yr).  This one is NOT a unit convention -
   it is the INPUT table, ``urh_cp_factors.csv``, re-sourced.  REASON.  docs/37 residual 1
   recorded that ``C`` was "a choice, and it is at the low end of its own range", with three
   classes carrying an uncited ASSUMED value.  docs/41 gives all 8 rows a source, a stated land
   condition and a low/central/high range.  The revision is a NET of Forest 0.003 -> 0.005
   (x1.243), Grassland 0.010 -> 0.015 (x1.137) and **Bare 1.00 -> 0.50 (x0.822)** - the
   largest single move in the table LOWERS the model, which is why the net is only x1.20 and
   not the x2-5 docs/37 candidate 1 estimated for itself.  The prior table stays reachable as
   ``cp_revision='prior_2026_08_11'``, and docs/41's band endpoints as
   ``cited_low_2026_08_11`` / ``cited_high_2026_08_11`` (the low end is REFUTED by mass
   balance).  Unlike (1) and (2) this is NOT a pure level shift: Bare and Forest move in
   opposite directions, so the spatial and land-class ATTRIBUTION changes too (docs/37
   Amendment A1 §3 re-runs both pattern gates on it).  The ENSO ratios are invariant - ``C``
   has no seasonality, so every window rescales identically.

UNITS - AND THE CONVENTION LADDER, STATED NOT HIDDEN
---------------------------------------------------
* ``Qsur`` mm/day, ``q_peak`` m3/s, areas km2, ``K`` as stored t.ha.h/(ha.MJ.mm) (converted at
  use, see (2) above), ``C``/``P``/``LS2D`` dimensionless, output **tonnes/day**.
* MUSLE is an empirical, dimensionally inhomogeneous regression: the tonne scale is set
  entirely by ``alpha`` *at one particular unit convention*.  **THREE** conventions exist in
  the literature for the ``(Qsur * q_peak * A)`` product; they differ only by a constant
  factor, and the derivation in (1) above is what selects among them:

  ``volume_convention='pixel_km2'`` (the ORIGINALLY registered one, docs/35 §4 - **no longer
  the default**, kept reachable so the first-run numbers stay reproducible)
      the product is ``Qsur[mm] * q_peak[m3/s] * a_p[km2]``, i.e. the area is carried in
      **km2**, the unit Buarque (2015) eq. 7 needs for ``q_pico = Dsup*A/86.4``.
      CORRECTED 2026-08-11 (this module previously asserted that Buarque's MUSLE ``A`` "is
      the same km2 area his eq. 7 uses" - that assertion is DELETED, because this project's
      own source review says the opposite).  Verbatim, from
      ``data/processed/peakgap/method_research.md`` §1.1, written 62 min before this module:

          "Unit check: 1 mm/day over 1 km² = 1000 m³/day = 0.011574 m³/s = 1/86.4, so
          ``Dsup`` is mm/day and ``A`` is km² in eq. 7/12 (both texts label the MUSLE area
          ``A`` in ha for the erosion equation itself - mind the mixed units when porting)."

      So the km2 area is established for the ``q_peak`` equation ONLY.  For the erosion
      equation the sources say **ha**, which is the next convention.

  ``volume_convention='swat_mm_ha'`` (non-default; the convention ``alpha`` = 11.8 is
  normally quoted with)
      SWAT's standard MUSLE form, and the reading the sentence above points to:
      ``Q_surf[mm] * q_peak[m3/s] * area[ha]``.  ``area[ha] = 100 * area[km2]``, so the
      product is exactly ``100`` times the registered one and the load exactly
      ``100**beta = 13.18x`` larger (at ``beta`` = 0.56).

  ``volume_convention='williams_m3'`` (**DEFAULT since 2026-08-11**)
      Williams (1975) writes ``Y = 11.8 (V * q_p)^0.56 K C P LS`` with ``V`` the runoff
      **volume in m3**.  ``V = 1000 * Qsur[mm] * A[km2]``, so this convention's product is
      exactly ``1000`` times the originally registered one and its load exactly
      ``1000**beta = 47.8630x`` larger (at ``beta`` = 0.56).  Adopted because the
      unit-by-unit conversion of Williams' English form lands on 11.78 here and on 42.78 /
      563.95 in the two alternatives - see CONVENTION AMENDMENT (1).

  ``k_unit_system`` is the second, independent unit ladder, and it multiplies ``K`` rather
  than the runoff product (so it is LINEAR, not raised to ``beta``):

  ``k_unit_system='us_customary'`` (**DEFAULT since 2026-08-11**)
      stored SI ``K`` x ``1/0.1317 = 7.593014``, the exact inverse of the conversion nb09 §4
      documents applying.  This is the numeric system Williams' 11.8 belongs to.
  ``k_unit_system='si_stored'``
      use ``minibacia_soil_params.csv:K`` as stored (x1.0).  This is what the module did before
      2026-08-11 and it is a dimensional error when paired with ``alpha`` = 11.8; kept
      reachable only so the pre-amendment numbers remain reproducible.

  MEASURED on this basin, 2009-2018, summed over hillslopes before any channel routing (C4) -
  and read the QUANTITY note below before calling that sum a "gross erosion", because that
  label is an ASSUMPTION, not a definition.  Rows 1-3 are the 2026-08-11 first run
  (``si_stored`` K, docs/35 §9.1); row 4 is the level docs/37 §2-§3 published; **row 5 is
  what this module actually returns today**, because the default now also carries the docs/41
  cover factor (``cp_revision='cited_central_2026_08_11'``, x1.2043).  A row is quoted with
  BOTH its unit conventions and its ``cp_revision``, never without:

  ================================================================  ==============  ====================
  convention @ ``cp_revision``                                      basin total     vs 144 / 184 Mt/yr
  ================================================================  ==============  ====================
  ``pixel_km2`` + ``si_stored`` @ ``prior``                          0.684 Mt/yr    210x / 269x below
  ``swat_mm_ha`` + ``si_stored`` @ ``prior``                         9.022 Mt/yr    16.0x / 20.4x below
  ``williams_m3`` + ``si_stored`` @ ``prior``                       32.758 Mt/yr    4.4x / 5.6x below
  ``williams_m3`` + ``us_customary`` @ ``prior_2026_08_11``        248.730 Mt/yr    1.35x / 1.73x ABOVE
  **``williams_m3`` + ``us_customary`` @ ``cited_central_2026_08_11``  299.539 Mt/yr  2.08x / 1.63x ABOVE  <- THE DEFAULT**
  ================================================================  ==============  ====================

  The anchor column is CONTEXT, not the selector.  The convention was chosen by the unit
  derivations above - ultimately by SWAT's own source code (docs/35 §9.2) - and rows 1-3 are
  ruled out there, not by being far from 144/184 Mt/yr.

  WHAT QUANTITY IS THIS SUM?  AND WHY THE SDR SENTENCE THAT USED TO STAND HERE IS DELETED
  (2026-08-11).  This docstring previously said the adopted row "implies a basin sediment
  delivery ratio of 0.58 - 0.74, where the published range for a basin of 257,097 km2 is
  roughly 0.05 - 0.3", and that C3 is OPEN "for exactly this reason".  All three parts of that
  are now wrong, and the correction is the point of docs/40:

  * **The 0.05 - 0.3 band is UNCITED and RETIRED** (docs/40 §2, §8; docs/37 A1.2).  A published
    SDR puts ALL water erosion in its denominator - gullies, valley trenches, streambanks -
    while this module computes sheet-and-rill only, so the ratio is a DIFFERENT quantity (an
    "apparent delivery ratio"), and USDA's own reference example has it at 1.7778 in a
    watershed whose true SDR is 0.6957.  Per this project's standing rule an uncited
    plausibility band may not be used to pass OR fail a gate, so it is retired in BOTH
    directions.  Do not reinstate it.
  * **C3 is not open for that reason.**  It is open on docs/37 A1.1 clauses 2 (the LS level -
    our LS sits 2.3151x-3.9768x above the level ``alpha`` = 11.8 is PAIRED with, and 3.9768x
    above the point now adopted; see below), 3 (the three 2026-08-11 decisions are unaudited)
    and 4'' (NOT ESTABLISHED, docs/37 A1.9).

    **THE LS FORMULATION IS NO LONGER "UNRESOLVED" - AND THE LEVEL IS STILL UNVALIDATED**
    (docs/37 **A3**, 2026-08-12, the C3.1 enactment under frozen docs/46).  Corrected here
    2026-08-12; this docstring previously read "the LS FORMULATION level is UNRESOLVED - our LS
    sits 2.37x-3.00x above ...", and BOTH halves of that were wrong:

    - the factor is **2.3151x - 3.9768x**, from the registered bracket ``f_LS`` in
      [0.25146, 0.43194] EROSION-weighted (area-weighted proxy
      **[0.2446790094097074, 0.42136300143291305]**, measured 2.5% low).  *Corrected
      2026-08-12: this docstring read the proxy as [0.24468, 0.42148]; 0.42148 is a correctly
      computed quantity on the ENGINE URH-fraction area support (257,096.93 km2), not
      docs/46 §3.3's per-cell basin one (30,235,916 cells, 256,702.36 km2), so it is not
      what §3.3 defines f_area to be.  Owning records docs/46 §10 amendment 2 and docs/51 §9
      amendment 1; expressed exactly as here by docs/43 §7 amendment 8.  ``f_ero`` is
      UNAFFECTED, so no bracket, alpha reference, hard stop or basin load moves.*
      The superseded "2.37x-3.00x" came from a x0.333 endpoint built on a x0.790
      that does NOT isolate the L form - it factorises as 0.852262 (L form) x 0.926925 (S swap)
      and was measured on the uncapped ``ls2d`` column, not on this module's ``ls2d_hs``
      (docs/50; docs/51 §2, §4).  The L-form ratio is FORMULATION-DEPENDENT (0.852262 uncapped
      / 0.769833 on ``ls2d_hs`` / 0.580685 inside the source formulation) and may not be
      composed across formulations as a scalar;
    - and the bracket is **not an uncertainty over readings of the source**.  All four levers
      are **CITED** with a single admissible reading each, so the source formulation read whole
      is a **POINT at f_LS = 0.25146** (``ls_formulation = 'buarque_2015_dg'``, docs/46 §3.1's
      ``V4_dg``), x0.43194 is a documented **HYBRID** (the source's three levers with OUR L),
      and the span between them, ln(0.43194/0.25146) = 0.5410, is the **L-form lever exactly** -
      a lever, not an error bar.  docs/46 §4.2's outcome exercised is **ADOPT-SOURCE**.

    **NOTHING IN THIS MODULE CHANGES BECAUSE OF A3, AND THAT IS DELIBERATE.**  A3's status is
    **DETERMINED and RECORDED, NOT YET EXERCISABLE**: it does not propose the engine-default
    switch, ``ls2d_column`` stays ``"ls2d_hs"`` and ``urh_ls2d`` stays ``"urh_ls2d.csv"``, and
    the switch is a separate, separately dated act that is not draftable until a gated
    ``V4_dg`` column exists as a committed product.  Enactment is a written amendment, not a
    code edit.  The LS **LEVEL** remains **UNVALIDATED** (docs/42 G4.2): a CITED formulation is
    not a validated level, and a fitted one is not either.  Clause 2 therefore stays NOT MET -
    also because it needs the LS **SHAPE** decision, which A3 does not touch - and C4.3 stays
    BLOCKED (docs/47).

    One related label correction, unconditional (docs/46 §1.1 Defect A, §2.2, §7.3 item 2;
    measured in docs/49): Buarque's **eq. 14 is a STEP FUNCTION** - m = 0.2 / 0.3 / 0.4 / 0.5
    on slope < 1% / 1-3% / 3-5% / >= 5%, with Sf in slope PERCENT - worth x0.522043
    erosion-weighted (x0.505092 area).  ``min(m_continuous, 0.5)`` is a **CAP**, x0.517480 ero
    (x0.502472 area); it is NOBODY'S published formulation and may never be graded CITED.  And
    per this project's standing rule, a product of single-lever factors is NEVER quoted as the
    joint factor: 0.362435 x 0.52204 x 1.694054 = 0.3205244 against a measured joint of
    0.431944, i.e. **joint / product = x1.34762** (docs/46 §1, docs/52 §1.1; carrying the m step
    to 0.522043 gives 0.3205263 and x1.347609 - the same measurement at a different printed
    precision, not a second number).
  * **And the "gross erosion" label itself is unresolved.**  SWAT's theoretical documentation
    for this exact equation (v2009, Section 4 Ch. 1, p. 252; quoted verbatim in docs/40 §0 and
    docs/37 A1.9.1) defines its output as "the sediment yield on a given day", whose runoff
    factor "represents energy used in detaching AND TRANSPORTING sediment" - which is why MUSLE
    "eliminates the need for delivery ratios".  Under that reading the residual's SIGN INVERTS
    (docs/37 A1.9.2: 2.03x-2.27x LOW as an erosion, 1.33x-1.49x HIGH as a yield), and a
    per-pixel sum over 30 M pixels is not cleanly either.  **The residual's direction is
    UNKNOWN.**

  **This module does not resolve that residual, and does not let ``alpha`` resolve it either**
  (docs/35 §6 RULE 0; docs/42 G5, which fires on any fit lacking a NAMED transport sink -
  note the yield-reading ``alpha`` of 7.92-8.86 sits just ABOVE G5's deposition-free band).
  *Corrected 2026-08-12 per docs/43 §7 amendment 5: this line read "overlaps G5's
  deposition-free 6.83-8.73".  6.83-8.73 is ``11.8 x {144, 184} / 248.730`` - the PRIOR
  ``cp_revision``'s basin total.  At the ADOPTED C (299.5387088405831 Mt/yr) the same
  arithmetic gives* **5.6727 - 7.2485**, *and the reading-B band 7.92-8.86 is already at the
  adopted C, so the two are* **DISJOINT** *with a gap of 0.6715 in alpha.  Never quote a load
  without its convention AND its* ``cp_revision``.  *What survives, on other grounds: G5's
  caution is retained because its NAMED-sink claim, not a numeric band, carries the weight
  (docs/43 §7 amendments 4 and 5).  Whether the disjointness changes docs/43 §3.4's "doubly
  load-bearing" conclusion is docs/47 open item O12 and is NOT decided here.*
  Switching a convention or a ``cp_revision`` default is an AMENDMENT with a date and a reason
  (done: docs/35 §9.2, docs/37 A1.3), never a quiet code change.

LS2D AGGREGATION AND RESOLUTION - NAMED, ADOPTED, AND FACTOR 1.000
------------------------------------------------------------------
Two more choices that could each have been an order-of-magnitude error were resolved on
2026-08-11 and both came out as what this module already did.  They are now explicit names on
:class:`SedParams` so that a future reader can see they were decided rather than defaulted:

* ``ls2d_aggregation='area_weighted_mean'`` (**adopted**, factor 1.000) - ``urh_ls2d.csv``'s
  ``ls2d_hs`` column IS the per-minibacia/per-URH area-weighted arithmetic mean of the
  per-cell LS2D, and MUSLE is applied per DEM pixel and summed, which is what an
  area-weighted mean of a LINEAR factor requires.  ``'per_cell_median'`` (factor 0.5410, the
  measured 16.555 / 30.605 basin-median ratio, ``docs/agents/journal_c31-ls2d.md`` §101/§133)
  is reachable as a DIAGNOSTIC ONLY: a median is not an admissible aggregate for a factor that
  enters linearly, because the sum of a linear factor over cells is its mean times the count,
  never its median times the count.
* ``ls2d_resolution='native_90m'`` (**adopted**, factor 1.000) - keep LS2D at the native COP90
  90 m resolution with no correction and no reference-resolution rescaling.
  ``'rescale_740m_ref'`` (factor 0.6008 = 7.51 / 12.5, the measured basin per-cell medians at
  740 m and 90 m) is reachable as a DIAGNOSTIC ONLY.  The "published mountainous LS of 2-10"
  comparison that motivated a rescale is UNCITED and is retired, not acted on.

Neither of these contributes to the order-of-magnitude gap: 1.000 x 1.000.
* No quantity in ``t/km2/yr`` is produced anywhere in this module, by design: per-area
  sediment yields are EMBARGOED (catchment areas disagree by >2x on 36 % of shared gauges,
  docs/23 §13.2).  Area enters only as the MUSLE application unit, and only as each
  minibacia's OWN area, which is the same number the frozen water balance used.

WHY THE DAILY TERM FACTORISES (an identity, not an approximation)
-----------------------------------------------------------------
``a_p`` is a constant and the frozen drivers carry ``Qsur`` per MINIBACIA, so within one
minibacia-day the runoff-energy term ``(Qsur * q_peak * a_p)^beta`` is the same number for
every URH cell.  Therefore::

    Sed_mini(t) = term(t, mini) * sum_over_cells[ (A_cell/a_p) * alpha * K*C*P*LS2D*FG ]
                = term(t, mini) * mini_factor(mini)

exactly, with the second factor static.  Two backends exploit this differently and the test
suite asserts they agree, the same two-implementation discipline the routing uses in
``mgb_hydrology.py``:

* ``backend='cells'``  - the reference: evaluate MUSLE on all 32,782 (minibacia, URH) cells
  every day through :func:`musle_load_tonnes` and ``bincount`` to the minibacia.  Obvious,
  and it gives per-cell output for free.
* ``backend='collapsed'`` - pre-sum the static per-cell factor once, then one multiply per
  minibacia-day.  Agrees with ``cells`` to float rounding only (different summation order, so
  agreement is asserted to 1e-12 relative, not bitwise).

MEASURED, and it changes why the second backend exists: the full basin-decade takes 2.0 s
with ``cells`` and 1.3 s with ``collapsed`` - only **1.5x**, because 32,782 cells x 3,652 days
is small.  So ``collapsed`` is NOT justified as an optimisation; it is justified as a second
independent implementation of the same identity, which is what the routing backends do in
``mgb_hydrology.py`` (test 5b there).  If the two ever disagree beyond rounding, one of them
has a bug and the test says so.

DOCUMENTED CONSEQUENCE - URH-level ``Qsur`` IS NOT RECOVERABLE.  The engine generated
surface runoff on the URH columns and area-weighted it to the minibacia before storing
(``h2e_drivers.npz`` field note for ``qsur_gen_mm``).  So all URHs of a minibacia share
their minibacia's ``Qsur`` here, and URH identity enters only through ``K``, ``C``, ``P``,
``LS2D`` and area.  A forest and a bare cell in the same minibacia therefore differ in
erodibility but not in runoff depth - which understates the contrast, because the bare cell
really does generate more runoff.  Un-mixing it would require re-running the frozen
hydrology with per-URH output, which is out of scope and forbidden here.

DELIVERY, AND THE MASS LEDGER (docs/35 §8 open item 4, answered)
---------------------------------------------------------------
Buarque (2015) delays each minibacia's sediment to the channel through a linear reservoir.
This module implements the same reservoir but **defaults its residence time to 0 days**::

    store += eroded
    delivered = store * (1 - exp(-dt/tau))     # tau = 0  =>  coefficient 1, pass-through
    store    -= delivered

Why ``tau_delivery_days = 0.0`` is the default: the registered ``Qsur`` is
``qsur_rel_mm``, the runoff **released by the minibacia's surface linear reservoir**
(engine ``q_sup``), not the runoff generated on the columns.  The lag Buarque applies to the
sediment has therefore already been applied to the water that drives it; adding a second
reservoir would double-count it.  The store is kept in the code and in the ledger anyway so
that (a) a non-zero ``tau`` is a one-line change if C4 wants one, and (b) the accounting is
structural rather than a lucky consequence of a default.

DOCUMENTED CONSEQUENCE of driving MUSLE with the *released* rather than the *generated*
runoff: the term is convex in ``Qsur`` (exponent ``2*beta`` = 1.12 > 1), so smoothing the
runoff before MUSLE yields less sediment than MUSLE-then-smooth.  Measured on the frozen
drivers, ``qsur_gen_mm`` gives 0.770 Mt/yr against ``qsur_rel_mm``'s 0.684, i.e. **1.125x**
- small, because the surface reservoir's residence time is short.  It is one more term in
the SAME direction as the registered
lower bound of docs/35 §5.3, and it is switchable via ``qsur_field`` for anyone who wants to
report the alternative - not silently averaged with it.

**Ledger.** ``eroded = delivered + stored`` exactly.  With the default pass-through the
identity is bitwise: ``tau = 0`` gives a release coefficient of exactly 1.0, so
``delivered`` is the same float as ``eroded`` and the store stays at exactly 0.0 for every
minibacia-day of the record; the reported residual is exactly ``0.0``, not a small number.
With ``tau > 0`` the daily arithmetic is still a structural partition (``store`` is defined
as ``S - delivered``, so no gram is created or dropped), and the cumulative totals are
accumulated with :func:`math.fsum` so the accounting adds no error of its own - the residual
then reflects only per-day float rounding (measured < 1e-15 relative).

INPUTS AND THE CAVEATS THEY BRING WITH THEM
-------------------------------------------
* ``K`` (``minibacia_soil_params.csv:K``) is per MINIBACIA, not per URH: 8,672 values,
  texture-derived (nb09 §4), 0 NaN, range 0.019-0.0495 **in SI** - i.e. 0.1443-0.3759 in the
  US-customary numerics MUSLE with ``alpha`` = 11.8 requires, which is the conversion
  ``k_unit_system`` performs (CONVENTION AMENDMENT (2)).  :class:`SedGeometry` stores the
  column AS READ, in SI; the conversion happens at use in :func:`effective_k`, so what the
  geometry tests assert against the CSV stays a straight comparison.  The same file's ``Wm_mm`` is a
  hydrological parameter and is NOT read here, mirroring the reverse warning in
  ``mgb_hydrology.py``: the two columns are numerically similar and confusing them runs
  without error and is silently wrong.
* ``C`` (C3.2) is per land class and is now a NAMED, REVERSIBLE choice, exactly like the unit
  conventions above: ``load_geometry(cp_revision=...)``, values in :data:`CP_REVISIONS`.
  **DEFAULT since 2026-08-11 is ``cited_central_2026_08_11``** (docs/41): every one of the 8
  rows carries a source, a stated land condition and a low/central/high range, and the
  basin area-weighted ``C`` is 0.013083 against the prior 0.010823, i.e. **x1.2043** on the
  basin total (248.730 -> 299.539 Mt/yr).  That is a NET of two opposing corrections - Forest
  0.003 -> 0.005 (x1.243) and Grassland 0.010 -> 0.015 (x1.137) up, **Bare 1.00 -> 0.50
  (x0.822) down**, which is the largest single revision in the table and it LOWERS the model.
  ``cp_revision='prior_2026_08_11'`` reproduces the pre-revision level and every number in
  docs/37 §2-§3 as first published.
  Three things that survive the revision and must still travel with any load:
  ``P`` = 1.0 basin-wide is an EXPLICIT assumption (AH-537 defines ``P`` for support
  PRACTICES and no practice layer exists for this basin), which makes the practice term an
  upper bound on erosion; the ``C`` **level** is confounded with ``alpha`` and can never be
  fitted (docs/42 §3.1), so it must be pinned from outside or printed UNVALIDATED; and
  ``Bare`` is still an interpolation (0.50 = sqrt(0.25 x 1.00)) applied above the treeline
  where the surface is rock, ash and ice, so with ``K`` non-zero everywhere the model still
  erodes bare rock, at half the former rate.  See ``urh_cp_factors.csv``'s own
  ``land_condition`` / ``source`` / ``note`` columns - they are loaded, not paraphrased.
* ``LS2D``: the default column is ``ls2d_hs``, the hillslope-limited variant (upslope area
  capped at a 1 km2 channel-initiation threshold).  ``scripts/c3/ls2d.py`` states in its own
  docstring that this is "the column MUSLE should use": the uncapped ``ls2d`` lets channel
  cells carry the entire upstream catchment into a *hillslope* equation, which is a
  domain-of-validity failure (area-weighted mean 104.9 uncapped vs 39.8 capped).  Measured
  through this engine: the uncapped column multiplies basin-total erosion by **2.225x** at a
  uniform ``Qsur``, so this is not a cosmetic choice.
* ``FG`` = 1.0, explicitly, because no coarse-fragment / rock-fragment layer exists for the
  basin (IGAC gives texture classes, not stone content).  ``FG <= 1`` always, so omitting it
  RAISES the simulated load - it is the only term found so far that points against the
  lower-bound direction of docs/35 §5.3, and docs/35 §8 item 3 requires it be said out loud
  rather than left silent.  It is a parameter, not a hardcoded 1.
* AREA CROSS-CHECK, recorded because it is a >2x disagreement on some cells: URH areas from
  ``urh_fractions.csv`` x ``minibacias.csv`` (used here) and from ``urh_ls2d.csv:area_km2``
  (the LS2D raster's own cell count) agree at the median (ratio 1.0021) but differ by >5 % on
  12.9 % of cells, up to 6.6x, and the LS2D raster totals 2.09 % less basin area (251,724 vs
  257,097 km2 - DEM nodata).  This module takes area from ``urh_fractions``, i.e. the same
  area the frozen water balance and ``h2e_drivers.npz:own_area_km2`` use, and treats
  ``ls2d_hs`` as an intensive per-cell mean.  :func:`load_geometry` re-measures the
  disagreement and warns; it does not silently pick the smaller number.

BIAS THIS MODULE INHERITS (measured, docs/33 §7 and docs/35 §5 - do not re-derive)
---------------------------------------------------------------------------------
The peak deficit is STRUCTURAL (docs/33 §8: the H2E-S refit that fixed peaks was rejected
on 2 of 3 pre-registered conditions).  Fleet-median ``R_AMS`` 0.820 (El Nino 0.686),
``R_POT`` 0.567 - the model produces 1,285 independent peaks-over-threshold against 2,236
observed, i.e. ~43 % of flood events are missing.  Through ``beta``, the magnitude channel
alone puts simulated flood-driven sediment at least 10.5 % low fleet-wide and 19.0 % low in
El Nino; with the missing events the bracket is -10 % to -45 %; adding the ``q_peak`` proxy's
own sub-daily assumption the total suppression is ~2.1x (bracket 1.4-4.8), and that last term
is method-consistent with Buarque/Fagundes and must be reported separately, never merged.
**Simulated sediment from this module is a LOWER BOUND**, and the simulated
La Nina : El Nino contrast is overstated by ~+10 % because the dry phase is suppressed
harder.  Nothing in this module corrects any of that.

REJECTED ALTERNATIVES
---------------------
* **Rejected - deriving ``q_peak`` from a unit hydrograph** (SCS triangular, docs/35 §3(ii)):
  needs a rainfall-excess duration ``D``, which does not exist in a model with no sub-daily
  rainfall, and a basin-wide slope field, which does not exist at all (the only processed DEM
  covers 17.4 % of minibacias and they are the flat ones).  Implemented in
  ``scripts/c3/qpeak.py`` as a sensitivity generator only.  Choosing it would be a tuned
  decision dressed as a physical one.
* **Rejected - applying MUSLE lumped at the minibacia (or URH) scale.**  It is cheaper and it
  is what a naive port does, but MUSLE is scale-dependent: lumping inflates the load by
  ``N**(2*beta-1)``, 2.63x at the median minibacia, and it silently invalidates the
  pre-registered ``alpha`` band (docs/35 §6.2 - the hard stop would point the wrong way).
  The pixel-scale form is one extra multiplication.  If C4 ever needs the lumped form, use
  ``qpeak.rescale_alpha_reference`` and say so in the same table as ``alpha``.
* **Rejected - a per-URH sediment delivery ratio (SDR) or a Renard-style routing factor.**
  Any SDR is another free multiplicative parameter sitting upstream of ``alpha``, i.e. a
  second knob for the same degree of freedom, and nothing measured in this project can
  identify it separately from ``alpha``.  Delivery is one named linear reservoir (above) and
  the channel step is C4.
* **Rejected - making ``K`` per URH by soil family.**  ``K`` in
  ``minibacia_soil_params.csv`` is already texture-derived per minibacia; splitting it by the
  URH's soil-family digit would re-derive the same texture information from the URH code and
  could disagree with the file.  One source of truth per factor.
* **Rejected - clipping or smoothing extreme cells** (the eight highest-``C`` minibacias are
  bare rock/ice above the treeline).  A clip would hide a known input problem inside the
  engine.  The engine reports where its load concentrates; the fix, if any, belongs in
  ``urh_cp_factors.csv`` with a written reason.
* **Rejected - defaulting ``qsur_field`` to ``qsur_gen_mm``** even though Buarque's eq. 7 uses
  generated runoff: docs/35 §1 registers ``qsur_rel_mm`` as ``Qsur``, and the registration
  predates this module.  Switching the default after the fact is exactly the ordering
  violation docs/35 exists to prevent.  Both fields are available and the difference is
  measured (~1.6x), not hidden.

PERFORMANCE
-----------
Loops over TIME ONLY, like ``mgb_hydrology.py``.  Full basin-decade (3,652 days x 8,672
minibacias, 32,782 URH cells), measured 2026-08-11: ``collapsed`` 1.3 s without the daily
output array and 1.5 s with it (126 MB, float32), ``cells`` 2.0 s.  Peak memory is dominated
by the inputs, not the loop: the ``Qsur`` field alone is 121 MB.
"""

from __future__ import annotations

import importlib.util
import math
import pathlib
import sys
import time
import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np

# Resolved from this file, never from the caller's cwd: nbconvert runs a notebook's kernel in
# notebooks/, so a relative "data/processed" default silently becomes notebooks/data/processed.
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PROCESSED_DIR = _REPO_ROOT / "data" / "processed"
DEFAULT_DRIVERS_PATH = DEFAULT_PROCESSED_DIR / "sim_calibrated_v2" / "h2e_drivers.npz"

__all__ = [
    "DEFAULT_PROCESSED_DIR",
    "DEFAULT_DRIVERS_PATH",
    "DT_DAYS",
    "COP90_PIXEL_AREA_KM2",
    "WILLIAMS_ALPHA",
    "WILLIAMS_BETA",
    "WILLIAMS_M3_PER_MM_KM2",
    "VOLUME_CONVENTIONS",
    "VOLUME_FACTORS",
    "DEFAULT_VOLUME_CONVENTION",
    "K_SI_PER_K_US",
    "K_US_PER_K_SI",
    "K_UNIT_FACTORS",
    "K_UNIT_SYSTEMS",
    "DEFAULT_K_UNIT_SYSTEM",
    "LS2D_AGGREGATION_FACTORS",
    "LS2D_AGGREGATIONS",
    "DEFAULT_LS2D_AGGREGATION",
    "LS2D_RESOLUTION_FACTORS",
    "LS2D_RESOLUTIONS",
    "DEFAULT_LS2D_RESOLUTION",
    "CP_REVISIONS",
    "CP_REVISION_NAMES",
    "DEFAULT_CP_REVISION",
    "QSUR_FIELDS",
    "effective_k",
    "effective_ls2d",
    "LAND_CLASS_NAMES",
    "SedGeometry",
    "SedParams",
    "SedState",
    "SedDrivers",
    "SedResult",
    "qpeak_daily_mean",
    "musle_load_tonnes",
    "build_geometry",
    "load_geometry",
    "load_drivers",
    "cell_static_factor",
    "mini_static_factor",
    "runoff_energy_term",
    "erode_day",
    "simulate_sediment",
    "check_musle_parameters",
]

DT_DAYS = 1.0


# ---------------------------------------------------------------------------
# the registered q_peak proxy, imported (never re-derived)
# ---------------------------------------------------------------------------


def _import_qpeak():
    """Import ``scripts/c3/qpeak.py`` by path.

    It lives in ``scripts/c3/`` and not ``src/`` on purpose (docs/35 §7): Phase B's engine
    directory is frozen and C3 code must not be mistakable for part of it.  ``src/`` is not
    a package, so a relative import is impossible; loading by path keeps the registered
    proxy a single source of truth instead of copying its constants in here, which is how
    a "registered" number quietly drifts.
    """
    if "qpeak" in sys.modules:
        return sys.modules["qpeak"]
    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "c3" / "qpeak.py"
    if not path.is_file():
        raise ImportError(
            f"the registered q_peak proxy is missing: {path}. It is pre-registered in "
            "docs/35 §4 and must not be re-implemented here."
        )
    spec = importlib.util.spec_from_file_location("qpeak", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["qpeak"] = module
    spec.loader.exec_module(module)
    return module


_QP = _import_qpeak()

#: The registered MUSLE application scale, 0.0081 km2 (docs/35 §4).  Re-exported, not copied.
COP90_PIXEL_AREA_KM2 = _QP.COP90_PIXEL_AREA_KM2
WILLIAMS_ALPHA = _QP.WILLIAMS_ALPHA        # 11.8  - starting value, NOT a fitted value
WILLIAMS_BETA = _QP.WILLIAMS_BETA          # 0.56  - starting value, NOT a fitted value
qpeak_daily_mean = _QP.qpeak_daily_mean
check_musle_parameters = _QP.check_musle_parameters

#: 1 mm of depth over 1 km2 is 1000 m3 - the whole difference between the two unit
#: conventions of the module docstring (``williams_m3`` = ``pixel_km2`` x 1000).
WILLIAMS_M3_PER_MM_KM2 = 1000.0

#: 1 km2 = 100 ha.  SWAT's standard MUSLE form carries the area in HECTARES
#: (``Q_surf[mm] * q_peak[m3/s] * area[ha]``), which is the form ``alpha`` = 11.8 is normally
#: quoted with, and the form ``method_research.md`` §1.1 says both source texts label
#: (see the module docstring's UNITS section).  ``swat_mm_ha`` = ``pixel_km2`` x 100.
SWAT_HA_PER_KM2 = 100.0

#: The product multiplier for each convention, in ascending order of magnitude.
VOLUME_FACTORS = {
    "pixel_km2": 1.0,
    "swat_mm_ha": SWAT_HA_PER_KM2,
    "williams_m3": WILLIAMS_M3_PER_MM_KM2,
}
VOLUME_CONVENTIONS = tuple(VOLUME_FACTORS)

#: The name of the adopted volume convention, as amended on 2026-08-11 (docs/35 §9.2).
#: Named rather than inlined so the default and the amendment cannot drift apart.
DEFAULT_VOLUME_CONVENTION = "williams_m3"

#: SI USLE K per US-customary USLE K.  ``notebooks/09_soil_parameters.ipynb`` §4 states that
#: the stored K was produced by multiplying Wischmeier & Smith (1978) US-customary class values
#: by this constant ("converted to SI (x0.1317)"), and undoing it returns the textbook numbers
#: (0.020 -> 0.1519 ~ sand 0.15; 0.045 -> 0.3417 ~ silt loam 0.34; 0.028 -> 0.2126 ~ clay 0.21).
#: It is the repository's OWN conversion constant, so undoing it exactly is the correct inverse
#: rather than an independent literature value.
K_SI_PER_K_US = 0.1317
#: 7.593014 - the factor MUSLE needs on the stored SI K for ``alpha`` = 11.8 to be Williams'
#: coefficient (his conversion left K/C/P/LS in US-customary numerics).  Not a knob.
K_US_PER_K_SI = 1.0 / K_SI_PER_K_US

#: Multiplier applied to the stored ``K`` for each named unit system.  ``us_customary`` is the
#: adopted default; ``si_stored`` reproduces the pre-2026-08-11 (dimensionally wrong) behaviour.
K_UNIT_FACTORS = {
    "si_stored": 1.0,
    "us_customary": K_US_PER_K_SI,
}
K_UNIT_SYSTEMS = tuple(K_UNIT_FACTORS)
DEFAULT_K_UNIT_SYSTEM = "us_customary"

#: Basin-median within-minibacia per-cell MEDIAN over the area-weighted MEAN of ``ls2d_hs``
#: (16.555 / 30.605, ``docs/agents/journal_c31-ls2d.md``).  The mean is the adopted aggregate;
#: this ratio exists only so the rejected alternative is reproducible and its size visible.
LS2D_MEDIAN_OVER_MEAN = 16.555 / 30.605
#: Basin per-cell median LS2D at 740 m over the same at 90 m (7.51 / 12.5).  Adopted choice is
#: NO rescaling; this ratio exists only to make the retired option reproducible.
LS2D_740M_OVER_90M = 7.51 / 12.5

#: LS2D aggregation choices.  Adopted: ``area_weighted_mean`` (factor 1.000 - the ``ls2d_hs``
#: column already is that mean, and MUSLE is applied per pixel and summed, which is what a
#: LINEAR factor requires).  ``per_cell_median`` is a DIAGNOSTIC: a median is not an admissible
#: aggregate for a linear factor.
LS2D_AGGREGATION_FACTORS = {
    "area_weighted_mean": 1.0,
    "per_cell_median": LS2D_MEDIAN_OVER_MEAN,
}
LS2D_AGGREGATIONS = tuple(LS2D_AGGREGATION_FACTORS)
DEFAULT_LS2D_AGGREGATION = "area_weighted_mean"

#: LS2D resolution treatment.  Adopted: ``native_90m`` (factor 1.000 - no correction, no
#: reference-resolution rescaling; the "mountainous 2-10" comparison that motivated one is
#: uncited and retired).  ``rescale_740m_ref`` is a DIAGNOSTIC only.
LS2D_RESOLUTION_FACTORS = {
    "native_90m": 1.0,
    "rescale_740m_ref": LS2D_740M_OVER_90M,
}
LS2D_RESOLUTIONS = tuple(LS2D_RESOLUTION_FACTORS)
DEFAULT_LS2D_RESOLUTION = "native_90m"

#: Named C/P revisions of ``urh_cp_factors.csv``.  Each name maps to the (C column, P column)
#: PAIR :func:`load_geometry` reads, so a change in the cover-factor LEVEL is a named,
#: reversible choice - the same pattern as ``volume_convention`` / ``k_unit_system`` - and the
#: prior level stays reachable by name rather than only in a spreadsheet column.
#:
#: * ``cited_central_2026_08_11`` (DEFAULT since 2026-08-11, docs/41): the loader-facing ``C``
#:   / ``P`` columns, which carry docs/41's cited-and-conditioned central values.  Basin
#:   area-weighted C 0.013083; **x1.2043** on the basin total (248.73 -> 299.54 Mt/yr).  It is
#:   a NET of two opposing corrections: Forest 0.003 -> 0.005 (x1.243) and Grassland 0.010 ->
#:   0.015 (x1.137) up, Bare 1.00 -> 0.50 (x0.822) down.
#: * ``prior_2026_08_11``: the pre-revision values, preserved in the CSV's own
#:   ``value_prior_2026_08_11`` / ``P_prior_2026_08_11`` columns.  Reproduces 248.730 Mt/yr
#:   and every number in docs/37 §2-§3 as first published.  Its provenance was
#:   Wischmeier & Smith (1978) / Roose (1977) with three classes ASSUMED and uncited.
#: * ``cited_low_2026_08_11`` / ``cited_high_2026_08_11``: docs/41's low/high band endpoints
#:   (x0.4315 / x7.6238).  DIAGNOSTIC ONLY.  The low end is REFUTED by mass balance - it
#:   implies an outlet-to-hillslope ratio of 1.34-1.72, i.e. the basin exporting more than it
#:   erodes (docs/41 §7).  The high end is not adopted because picking a C to close a residual
#:   is the failure mode docs/35 §6 RULE 0 forbids for ``alpha``.
#: * ``pacheco_practice_2026_08_11``: the cited C with the land-use-keyed P of
#:   Rengifo-Rengifo et al. (2022) Cuadro 5 after Pacheco et al. (2019).  DIAGNOSTIC ONLY and
#:   REJECTED as a category error (P is defined for support PRACTICES, not for land use, so it
#:   double-counts the cover effect C already carries - docs/41 §5).  Kept reachable because
#:   it is the measured direction: x0.542, i.e. any P < 1 LOWERS erosion and WIDENS the
#:   residual (docs/37 residual 4).
CP_REVISIONS = {
    "cited_central_2026_08_11": ("C", "P"),
    "prior_2026_08_11": ("value_prior_2026_08_11", "P_prior_2026_08_11"),
    "cited_low_2026_08_11": ("C_low", "P_central"),
    "cited_high_2026_08_11": ("C_high", "P_central"),
    "pacheco_practice_2026_08_11": ("C", "P_low"),
}
CP_REVISION_NAMES = tuple(CP_REVISIONS)
#: The adopted C/P revision, as of docs/41 (2026-08-11).  Named rather than inlined so the
#: default and the document that argues for it cannot drift apart.
DEFAULT_CP_REVISION = "cited_central_2026_08_11"
#: Frozen-driver fields that can play ``Qsur``.  ``qsur_rel_mm`` is the registered one.
QSUR_FIELDS = ("qsur_rel_mm", "qsur_gen_mm")

#: URH id = soil_family*10 + land_class (nb08 step 4); the land digit indexes C/P.
LAND_CLASS_NAMES = {
    1: "Forest", 2: "Shrub", 3: "Grassland", 4: "Cropland",
    5: "Urban", 6: "Bare", 7: "Water", 8: "Wetland",
}


def _finite_nonneg(name: str, arr: np.ndarray, *, positive: bool = False) -> np.ndarray:
    """Reject NaN/inf/negative (or non-positive) inputs loudly instead of coercing them."""
    a = np.asarray(arr, dtype=np.float64)
    if not np.all(np.isfinite(a)):
        n = int((~np.isfinite(a)).sum())
        raise ValueError(f"{name} has {n} non-finite entries")
    if positive:
        if np.any(a <= 0.0):
            raise ValueError(f"{name} must be > 0; min is {float(a.min())!r}")
    elif np.any(a < 0.0):
        raise ValueError(f"{name} must be >= 0; min is {float(a.min())!r}")
    return a


# ---------------------------------------------------------------------------
# the MUSLE primitive
# ---------------------------------------------------------------------------


def musle_load_tonnes(
    qsur_mm,
    qpeak_m3s,
    area_km2,
    k_usle,
    c_usle,
    p_usle,
    ls2d,
    *,
    alpha: float = WILLIAMS_ALPHA,
    beta: float = WILLIAMS_BETA,
    fg: float = 1.0,
    volume_factor: float = 1.0,
    validate: bool = True,
):
    """MUSLE soil loss for ONE application unit and one day, in tonnes.

    ``Sed = alpha * (Qsur * q_peak * A * volume_factor)^beta * K * C * P * LS2D * FG``

    This is the primitive every other function in the module goes through, and it takes
    ``q_peak`` **explicitly** rather than deriving it: the registered proxy makes ``q_peak``
    a function of ``Qsur`` (docs/35 §4), so a function that derived it internally could not
    be tested for monotonicity in ``q_peak`` alone.  Keeping the argument separate is what
    lets ``tests/test_sediment.py`` vary each of the seven factors independently.

    ``volume_factor`` is the unit convention of the module docstring: 1.0 for the registered
    ``pixel_km2`` form, :data:`SWAT_HA_PER_KM2` for SWAT's hectare form,
    :data:`WILLIAMS_M3_PER_MM_KM2` for the Williams-m3 form (see :data:`VOLUME_FACTORS`).
    It is a documented convention, not a calibration knob - see the docstring's UNITS
    section.

    All arguments broadcast.  Exact zero anywhere in the first three factors gives exactly
    0.0 tonnes (``0.0**beta`` is exactly 0.0 for ``beta`` > 0), so a dry day erodes nothing
    to the last bit rather than to within a tolerance.
    """
    if validate:
        qsur = _finite_nonneg("qsur_mm", qsur_mm)
        qpeak = _finite_nonneg("qpeak_m3s", qpeak_m3s)
        area = _finite_nonneg("area_km2", area_km2)
        k = _finite_nonneg("k_usle", k_usle)
        c = _finite_nonneg("c_usle", c_usle)
        p = _finite_nonneg("p_usle", p_usle)
        ls = _finite_nonneg("ls2d", ls2d)
        if not np.all(np.isfinite([alpha, beta, fg, volume_factor])):
            raise ValueError("alpha, beta, fg, volume_factor must be finite")
        if alpha < 0.0 or beta <= 0.0 or fg < 0.0 or volume_factor <= 0.0:
            raise ValueError(
                "need alpha >= 0, beta > 0 (beta <= 0 would make a dry day erode "
                "infinitely), fg >= 0, volume_factor > 0"
            )
    else:
        qsur, qpeak, area = qsur_mm, qpeak_m3s, area_km2
        k, c, p, ls = k_usle, c_usle, p_usle, ls2d
    product = qsur * qpeak * area * volume_factor
    return alpha * product ** beta * k * c * p * ls * fg


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SedGeometry:
    """Immutable static erosion geometry: one row per active (minibacia, URH) cell.

    Built once and reused for every parameter set, exactly like ``MgbTopology``: a C4
    calibration re-run must not re-read four CSVs per evaluation.  Nothing here depends on
    ``alpha``, ``beta``, ``FG`` or the pixel scale - those live in :class:`SedParams`.
    """

    mini_ids: np.ndarray         # (n,) int64   minibacia ids, in driver order
    mini_area_km2: np.ndarray    # (n,) float64 own area (== h2e_drivers own_area_km2)
    cell_mini: np.ndarray        # (N,) int64   internal minibacia index per cell
    cell_urh_code: np.ndarray    # (N,) int64   URH code 11..38
    cell_area_km2: np.ndarray    # (N,) float64
    cell_k: np.ndarray           # (N,) float64 erodibility (per minibacia, broadcast)
    cell_c: np.ndarray           # (N,) float64 cover factor (per land class)
    cell_p: np.ndarray           # (N,) float64 practice factor (1.0 basin-wide)
    cell_ls2d: np.ndarray        # (N,) float64
    ls2d_column: str = "ls2d_hs"
    area_source: str = "urh_fractions"
    audit: dict = field(default_factory=dict, repr=False)

    @property
    def n_mini(self) -> int:
        return int(self.mini_ids.size)

    @property
    def n_cells(self) -> int:
        return int(self.cell_mini.size)

    @property
    def covered_area_km2(self) -> float:
        """Area MUSLE is actually applied to = sum of cell areas."""
        return float(self.cell_area_km2.sum())

    def cell_land_class(self) -> np.ndarray:
        """Land digit of each cell's URH code (1 Forest .. 8 Wetland)."""
        return self.cell_urh_code % 10

    def index_of(self, ids: Sequence[int]) -> np.ndarray:
        """Internal indices of the given minibacia ids (raises on an unknown id)."""
        want = np.asarray(ids, dtype=np.int64)
        srt = np.argsort(self.mini_ids, kind="stable")
        sorted_ids = self.mini_ids[srt]
        loc = np.clip(np.searchsorted(sorted_ids, want), 0, sorted_ids.size - 1)
        ok = sorted_ids[loc] == want
        if not ok.all():
            raise KeyError(f"unknown minibacia ids: {want[~ok][:10].tolist()}")
        return srt[loc].astype(np.int64)


def build_geometry(
    mini_ids,
    mini_area_km2,
    cell_mini,
    cell_urh_code,
    cell_area_km2,
    mini_k,
    class_c,
    class_p,
    cell_ls2d,
    *,
    ls2d_column: str = "ls2d_hs",
    area_source: str = "urh_fractions",
    audit: Optional[dict] = None,
) -> SedGeometry:
    """Validate and pack the static factors.  ``class_c`` / ``class_p`` are dicts keyed 1..8.

    Every input is range-checked here rather than at use time, because a negative ``K`` or a
    NaN ``LS2D`` would otherwise surface 3,652 days later as a NaN in the output and cost a
    bisection to find.
    """
    ids = np.asarray(mini_ids, dtype=np.int64)
    n = ids.size
    if np.unique(ids).size != n:
        raise ValueError("duplicate minibacia ids")
    area_mini = _finite_nonneg("mini_area_km2", mini_area_km2, positive=True)
    if area_mini.shape != (n,):
        raise ValueError(f"mini_area_km2 must be ({n},), got {area_mini.shape}")
    cm = np.asarray(cell_mini, dtype=np.int64)
    cu = np.asarray(cell_urh_code, dtype=np.int64)
    ca = _finite_nonneg("cell_area_km2", cell_area_km2, positive=True)
    ls = _finite_nonneg("cell_ls2d", cell_ls2d, positive=True)
    if not (cm.shape == cu.shape == ca.shape == ls.shape) or cm.ndim != 1:
        raise ValueError("cell_* arrays must be 1-D and the same length")
    if cm.size and (cm.min() < 0 or cm.max() >= n):
        raise ValueError("cell_mini out of range for the given minibacia ids")
    k_mini = _finite_nonneg("mini_k", mini_k, positive=True)
    if k_mini.shape != (n,):
        raise ValueError(f"mini_k must be ({n},), got {k_mini.shape}")

    land = cu % 10
    unknown = sorted(set(land.tolist()) - set(class_c))
    if unknown:
        raise ValueError(f"no C factor for land class(es) {unknown}")
    unknown = sorted(set(land.tolist()) - set(class_p))
    if unknown:
        raise ValueError(f"no P factor for land class(es) {unknown}")
    c = _finite_nonneg("class_c", np.array([class_c[int(x)] for x in land]))
    p = _finite_nonneg("class_p", np.array([class_p[int(x)] for x in land]))
    return SedGeometry(
        mini_ids=ids,
        mini_area_km2=area_mini,
        cell_mini=cm,
        cell_urh_code=cu,
        cell_area_km2=ca,
        cell_k=k_mini[cm],
        cell_c=c,
        cell_p=p,
        cell_ls2d=ls,
        ls2d_column=str(ls2d_column),
        area_source=str(area_source),
        audit=dict(audit or {}),
    )


def load_geometry(
    processed_dir=DEFAULT_PROCESSED_DIR,
    *,
    minibacias: str = "minibacias.csv",
    urh_fractions: str = "urh_fractions.csv",
    soil_params: str = "minibacia_soil_params.csv",
    cp_factors: str = "urh_cp_factors.csv",
    cp_revision: str = DEFAULT_CP_REVISION,
    urh_ls2d: str = "urh_ls2d.csv",
    ls2d_column: str = "ls2d_hs",
    mini_ids: Optional[Sequence[int]] = None,
    area_tol_frac: float = 0.05,
) -> SedGeometry:
    """Assemble :class:`SedGeometry` from the four project CSVs.

    ``mini_ids`` orders the output (pass ``h2e_drivers.npz:minibacia_id`` so the geometry and
    the drivers share one column order - a mismatch there is a silent spatial scramble).

    ``ls2d_column`` defaults to ``ls2d_hs``, the hillslope-limited LS2D, because that is the
    column ``scripts/c3/ls2d.py`` states MUSLE should use; ``ls2d`` (uncapped) is available
    but lets channel cells carry the whole upstream catchment into a hillslope equation.

    ``cp_revision`` names WHICH pair of C/P columns is read (:data:`CP_REVISIONS`).  The
    default is docs/41's cited central revision; ``'prior_2026_08_11'`` reproduces the
    pre-revision level, and the band endpoints stay reachable as diagnostics.  The chosen name
    and the two column names are recorded in ``SedGeometry.audit`` so a load can never be
    quoted without its C provenance - the same discipline
    :meth:`SedParams.convention_summary` enforces for the unit conventions (docs/37 §5.3).

    Cell areas come from ``urh_fractions`` x ``minibacias``, NOT from ``urh_ls2d:area_km2``.
    The two disagree (see the module docstring); this function re-measures the disagreement
    on the spot and warns above ``area_tol_frac`` so the choice cannot rot silently.
    """
    import pandas as pd

    if cp_revision not in CP_REVISIONS:
        raise ValueError(f"cp_revision must be one of {CP_REVISION_NAMES}, got {cp_revision!r}")
    c_col, p_col = CP_REVISIONS[cp_revision]

    d = pathlib.Path(processed_dir)
    mb = pd.read_csv(d / minibacias)
    uf = pd.read_csv(d / urh_fractions)
    sp = pd.read_csv(d / soil_params)
    cp = pd.read_csv(d / cp_factors)
    ul = pd.read_csv(d / urh_ls2d)

    for name, df, cols in (
        (minibacias, mb, ("id", "area_km2")),
        (urh_fractions, uf, ("mini",)),
        (soil_params, sp, ("id", "K")),
        (cp_factors, cp, ("class_id", c_col, p_col)),
        (urh_ls2d, ul, ("mini", "urh", "area_km2", ls2d_column)),
    ):
        missing = [c for c in cols if c not in df.columns]
        if missing:
            hint = ""
            if df is cp:
                hint = (f" (cp_revision={cp_revision!r} reads {c_col!r} and {p_col!r}; a table "
                        "written before the docs/41 revision carries neither)")
            raise ValueError(f"{name} is missing column(s) {missing}{hint}")

    ids = mb.id.to_numpy(dtype=np.int64) if mini_ids is None else np.asarray(mini_ids, np.int64)
    mb = mb.set_index("id")
    unknown = set(ids.tolist()) - set(mb.index)
    if unknown:
        raise ValueError(f"{len(unknown)} requested minibacia ids are absent from "
                         f"{minibacias}, e.g. {sorted(unknown)[:5]}")
    area_mini = mb.loc[ids, "area_km2"].to_numpy(dtype=np.float64)

    codes = [c for c in uf.columns if c != "mini"]
    uf = uf.set_index("mini")
    missing_rows = set(ids.tolist()) - set(uf.index)
    if missing_rows:
        raise ValueError(f"{urh_fractions} has no row for {len(missing_rows)} minibacias, "
                         f"e.g. {sorted(missing_rows)[:5]}")
    frac = uf.loc[ids, codes].to_numpy(dtype=np.float64)
    if np.any(frac < 0) or not np.all(np.isfinite(frac)):
        raise ValueError(f"{urh_fractions} has negative or non-finite fractions")
    mi, ci = np.nonzero(frac > 0.0)
    cell_mini = mi.astype(np.int64)
    cell_code = np.asarray([int(codes[j]) for j in ci], dtype=np.int64)
    cell_area = frac[mi, ci] * area_mini[mi]

    sp = sp.set_index("id")
    missing_rows = set(ids.tolist()) - set(sp.index)
    if missing_rows:
        raise ValueError(f"{soil_params} has no row for {len(missing_rows)} minibacias")
    k_mini = sp.loc[ids, "K"].to_numpy(dtype=np.float64)

    cp = cp.set_index("class_id")
    class_c = {int(i): float(v) for i, v in cp[c_col].items()}
    class_p = {int(i): float(v) for i, v in cp[p_col].items()}
    # Drift guard: the DEFAULT revision reads the loader-facing ``C``/``P`` columns and CLAIMS
    # they hold docs/41's central values.  If the table also carries ``C_central``/``P_central``
    # and they disagree, the name and the number have come apart - say so rather than let the
    # audit record a provenance the file no longer has.
    if cp_revision == DEFAULT_CP_REVISION:
        for adopted, central in (("C", "C_central"), ("P", "P_central")):
            if central in cp.columns and not np.allclose(
                cp[adopted].to_numpy(dtype=np.float64),
                cp[central].to_numpy(dtype=np.float64),
                rtol=0.0, atol=1e-12,
            ):
                warnings.warn(
                    f"{cp_factors}: column {adopted!r} does not equal {central!r}, but "
                    f"cp_revision={cp_revision!r} names the central revision. The adopted "
                    f"column is used AS READ; fix the table or pass an explicit cp_revision.",
                    stacklevel=2,
                )

    ul_idx = ul.set_index(["mini", "urh"])
    want = list(zip(ids[cell_mini].tolist(), cell_code.tolist()))
    missing_cells = [key for key in want if key not in ul_idx.index]
    if missing_cells:
        raise ValueError(
            f"{urh_ls2d} has no LS2D for {len(missing_cells)} active (minibacia, URH) cells, "
            f"e.g. {missing_cells[:5]}. A missing LS2D must not become an implicit 0 - that "
            "would silently switch erosion off for those cells."
        )
    sub = ul_idx.loc[want]
    cell_ls2d = sub[ls2d_column].to_numpy(dtype=np.float64)
    ls_area = sub["area_km2"].to_numpy(dtype=np.float64)

    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(ls_area > 0, cell_area / ls_area, np.nan)
    frac_off = float(np.mean(np.abs(ratio - 1.0) > area_tol_frac))
    audit = {
        "n_cells": int(cell_mini.size),
        "area_ratio_median": float(np.nanmedian(ratio)),
        "area_ratio_p99": float(np.nanpercentile(ratio, 99)),
        "area_ratio_max": float(np.nanmax(ratio)),
        "frac_cells_area_off": frac_off,
        "area_total_urh_fractions_km2": float(cell_area.sum()),
        "area_total_urh_ls2d_km2": float(ls_area.sum()),
        "ls2d_column": ls2d_column,
        "cp_factors": cp_factors,
        "cp_revision": cp_revision,
        "cp_c_column": c_col,
        "cp_p_column": p_col,
        "class_c": {int(k): float(v) for k, v in class_c.items()},
        "class_p": {int(k): float(v) for k, v in class_p.items()},
    }
    if frac_off > 0.0:
        warnings.warn(
            f"URH cell areas from {urh_fractions} x {minibacias} and from "
            f"{urh_ls2d}:area_km2 differ by more than {area_tol_frac:.0%} on "
            f"{frac_off:.1%} of cells (median ratio {audit['area_ratio_median']:.4f}, max "
            f"{audit['area_ratio_max']:.2f}; basin totals "
            f"{audit['area_total_urh_fractions_km2']:.0f} vs "
            f"{audit['area_total_urh_ls2d_km2']:.0f} km2). This module uses the "
            f"{urh_fractions} area, i.e. the same area the frozen water balance used, and "
            "treats LS2D as an intensive per-cell mean.",
            stacklevel=2,
        )
    return build_geometry(
        ids, area_mini, cell_mini, cell_code, cell_area, k_mini,
        class_c, class_p, cell_ls2d,
        ls2d_column=ls2d_column, area_source=urh_fractions, audit=audit,
    )


# ---------------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SedParams:
    """Every tunable number, with the origin of its default stated.

    Frozen on purpose: a C4 search must construct a new instance per evaluation rather than
    mutate a shared one, so a half-updated parameter set cannot leak between evaluations.
    Nothing here is fitted.
    """

    #: MUSLE coefficient.  Williams (1975), adopted unchanged by Buarque (2015) eq. 5 with
    #: this same daily-mean q_peak.  A STARTING VALUE to be fitted in C4, not a tuned value;
    #: C4's registered band and hard stops are in ``qpeak.check_musle_parameters``.
    alpha: float = WILLIAMS_ALPHA
    #: MUSLE exponent.  Williams (1975).  STARTING VALUE; C4 hard stop outside [0.45, 0.65].
    beta: float = WILLIAMS_BETA
    #: Coarse-fragment factor.  EXPLICITLY 1.0: no rock-fragment layer exists for the basin
    #: (docs/35 §8 item 3).  FG <= 1 always, so 1.0 RAISES the load - the one term pointing
    #: against the docs/35 §5.3 lower-bound direction.  Stated, not silent.
    fg: float = 1.0
    #: MUSLE application area, km2.  The registered COP90 pixel (docs/35 §4).  Changing it
    #: invalidates the pre-registered alpha band unless the band is rescaled by
    #: ``qpeak.musle_scale_factor`` - see docs/35 §6.2.
    pixel_area_km2: float = COP90_PIXEL_AREA_KM2
    #: Delivery linear-reservoir residence time, days.  0.0 = pass-through, the default,
    #: because the registered Qsur (``qsur_rel_mm``) has ALREADY been through the engine's
    #: surface linear reservoir; a second one would double-count the lag (docs/35 §8 item 4).
    tau_delivery_days: float = 0.0
    #: Unit convention for the (Qsur * q_peak * A) product.  DEFAULT since 2026-08-11 is
    #: 'williams_m3', Williams' literal m3-volume form - the only one of the three whose
    #: unit-by-unit conversion of Y = 95 (Q[ac-ft] q_p[cfs])^0.56 lands on alpha = 11.8
    #: (11.7818; the mm*ha reading gives 42.78 and the mm*km2 reading 563.95).  'pixel_km2'
    #: (the originally registered form, docs/35 §4) and 'swat_mm_ha' are kept reachable so the
    #: pre-amendment numbers stay reproducible.  Changing this default is an amendment to
    #: docs/35 §9 (done: §9.2) plus a dated note in the module docstring - never a quiet edit.
    volume_convention: str = DEFAULT_VOLUME_CONVENTION
    #: Unit system of the K values fed to MUSLE.  DEFAULT since 2026-08-11 is 'us_customary':
    #: minibacia_soil_params.csv:K is stored in SI (nb09 §4 says it multiplied Wischmeier's
    #: US-customary values by 0.1317) while Williams' alpha = 11.8 requires the US-customary
    #: numerics, so the stored K must be multiplied by 1/0.1317 = 7.593014.  This factor is
    #: LINEAR in the load (it is not inside the ^beta term).  'si_stored' reproduces the
    #: pre-amendment behaviour and is a dimensional error when paired with alpha = 11.8.
    k_unit_system: str = DEFAULT_K_UNIT_SYSTEM
    #: How the per-cell LS2D field was aggregated to the (minibacia, URH) cell.  ADOPTED
    #: 'area_weighted_mean', factor 1.000 - what urh_ls2d.csv:ls2d_hs already is.
    #: 'per_cell_median' (x0.5410) is a diagnostic; a median is not admissible for a factor
    #: that enters linearly.
    ls2d_aggregation: str = DEFAULT_LS2D_AGGREGATION
    #: Resolution treatment of LS2D.  ADOPTED 'native_90m', factor 1.000 - no correction and no
    #: reference-resolution rescaling.  'rescale_740m_ref' (x0.6008) is a diagnostic only.
    ls2d_resolution: str = DEFAULT_LS2D_RESOLUTION

    def __post_init__(self) -> None:
        if self.volume_convention not in VOLUME_CONVENTIONS:
            raise ValueError(f"volume_convention must be one of {VOLUME_CONVENTIONS}")
        if self.k_unit_system not in K_UNIT_SYSTEMS:
            raise ValueError(f"k_unit_system must be one of {K_UNIT_SYSTEMS}")
        if self.ls2d_aggregation not in LS2D_AGGREGATIONS:
            raise ValueError(f"ls2d_aggregation must be one of {LS2D_AGGREGATIONS}")
        if self.ls2d_resolution not in LS2D_RESOLUTIONS:
            raise ValueError(f"ls2d_resolution must be one of {LS2D_RESOLUTIONS}")
        for name in ("alpha", "beta", "fg", "pixel_area_km2", "tau_delivery_days"):
            v = float(getattr(self, name))
            if not math.isfinite(v):
                raise ValueError(f"{name} must be finite")
        if self.alpha < 0.0:
            raise ValueError("alpha must be >= 0")
        if self.beta <= 0.0:
            raise ValueError(
                "beta must be > 0: with beta <= 0 a zero-runoff day would erode infinitely"
            )
        if self.fg < 0.0 or self.fg > 1.0:
            raise ValueError("fg is a fraction of erodible surface and must lie in [0, 1]")
        if self.pixel_area_km2 <= 0.0:
            raise ValueError("pixel_area_km2 must be > 0")
        if self.tau_delivery_days < 0.0:
            raise ValueError("tau_delivery_days must be >= 0")

    @property
    def volume_factor(self) -> float:
        """Multiplier on the ``(Qsur * q_peak * A)`` product for the chosen convention.

        This one sits INSIDE the ``^beta`` power, so it moves the load by
        ``volume_factor**beta``, not by ``volume_factor``.
        """
        return VOLUME_FACTORS[self.volume_convention]

    @property
    def k_factor(self) -> float:
        """Multiplier on the stored ``K`` for the chosen unit system (LINEAR in the load)."""
        return K_UNIT_FACTORS[self.k_unit_system]

    @property
    def ls2d_factor(self) -> float:
        """Multiplier on the stored ``LS2D`` = aggregation x resolution (LINEAR in the load).

        Both adopted choices are 1.0, so the adopted product is exactly 1.0 and neither
        contributes to the C3.6 magnitude gap.  The non-adopted names exist so the rejected
        alternatives are reproducible instead of merely asserted.
        """
        return (LS2D_AGGREGATION_FACTORS[self.ls2d_aggregation]
                * LS2D_RESOLUTION_FACTORS[self.ls2d_resolution])

    def convention_summary(self) -> dict:
        """Every named convention this parameter set carries, with its numeric factor.

        Meant to be printed beside any reported load: docs/35 §6.4 test T3 requires the
        application unit and the reference band in the same table as the number, and after the
        2026-08-11 amendment the unit CONVENTION belongs there too - a load without its
        convention is 363x ambiguous.
        """
        return {
            "volume_convention": self.volume_convention,
            "volume_factor": self.volume_factor,
            "volume_load_multiplier": float(self.volume_factor ** float(self.beta)),
            "k_unit_system": self.k_unit_system,
            "k_factor": self.k_factor,
            "ls2d_aggregation": self.ls2d_aggregation,
            "ls2d_resolution": self.ls2d_resolution,
            "ls2d_factor": self.ls2d_factor,
            "pixel_area_km2": float(self.pixel_area_km2),
            "alpha": float(self.alpha),
            "beta": float(self.beta),
        }

    @property
    def delivery_release_coef(self) -> float:
        """Fraction of the sediment store delivered in one day.

        ``1 - exp(-dt/tau)``, the analytic one-day solution of ``dS/dt = -S/tau`` - the same
        form ``mgb_hydrology._release_coef`` uses for water, for the same reason (bounded in
        (0, 1] for every tau >= 0, so the store can never go negative).  ``tau = 0`` gives
        exactly 1.0, i.e. bitwise pass-through.
        """
        tau = float(self.tau_delivery_days)
        return 1.0 if tau == 0.0 else float(-math.expm1(-DT_DAYS / tau))

    def check(self, area_km2: Optional[float] = None) -> dict:
        """Apply the pre-registered docs/35 §6 anti-compensation rule to (alpha, beta).

        Thin wrapper over ``qpeak.check_musle_parameters`` so C4 cannot forget it exists.
        ``area_km2`` is only needed if MUSLE was applied lumped rather than at the
        registered pixel scale.
        """
        return check_musle_parameters(float(self.alpha), float(self.beta), area_km2=area_km2)


# ---------------------------------------------------------------------------
# static factor and the daily runoff-energy term
# ---------------------------------------------------------------------------


def effective_k(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """``geom.cell_k`` in the unit system MUSLE is being evaluated in, ``(N,)``.

    The stored K is SI (``minibacia_soil_params.csv``, nb09 §4); ``alpha`` = 11.8 needs the
    US-customary numerics, hence the default x7.593014.  Kept as a named function, not inlined,
    so both backends and the reference cell path go through the SAME conversion - a factor
    applied in one path and not the other would show up only as a backend disagreement.
    """
    return geom.cell_k * params.k_factor


def effective_ls2d(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """``geom.cell_ls2d`` after the named aggregation/resolution choices, ``(N,)``.

    Both adopted choices are factor 1.0, so this returns the stored column times exactly 1.0
    by default (``x * 1.0`` is bitwise ``x`` for every finite float, so the adopted path adds
    no rounding).
    """
    return geom.cell_ls2d * params.ls2d_factor


def cell_static_factor(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """Per-cell part of MUSLE that does not depend on the day, ``(N,)``.

    ``(A_cell / a_p) * alpha * (K*f_K) * C * P * (LS2D*f_LS) * FG`` - the pixel count times
    every static factor.  Multiply by :func:`runoff_energy_term` to get tonnes/day.
    """
    n_pix = geom.cell_area_km2 / float(params.pixel_area_km2)
    return (n_pix * float(params.alpha) * effective_k(geom, params) * geom.cell_c
            * geom.cell_p * effective_ls2d(geom, params) * float(params.fg))


def mini_static_factor(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """:func:`cell_static_factor` summed to the minibacia, ``(n,)`` - the collapsed backend.

    Valid because the runoff-energy term is identical for every cell of a minibacia (the
    frozen drivers carry ``Qsur`` per minibacia and ``a_p`` is a constant), so the sum
    factorises exactly.  See the module docstring, WHY THE DAILY TERM FACTORISES.
    """
    return np.bincount(geom.cell_mini, weights=cell_static_factor(geom, params),
                       minlength=geom.n_mini)


def runoff_energy_term(qsur_mm, params: SedParams, *, validate: bool = True):
    """``(Qsur * q_peak * a_p * volume_factor)^beta`` at the registered pixel scale.

    ``q_peak`` comes from the registered proxy :func:`qpeak_daily_mean` evaluated on the
    pixel, i.e. ``Qsur * a_p / 86.4``; nothing here is free.  Exactly 0.0 where ``Qsur`` is
    0.0.
    """
    q = _finite_nonneg("qsur_mm", qsur_mm) if validate else qsur_mm
    a_p = float(params.pixel_area_km2)
    qpeak = q * a_p * _QP.MM_KM2_PER_DAY_TO_M3S
    return (q * qpeak * a_p * params.volume_factor) ** float(params.beta)


def erode_day(geom: SedGeometry, params: SedParams, qsur_mini_mm) -> np.ndarray:
    """Gross hillslope erosion for one day, per URH cell, in tonnes/day, ``(N,)``.

    ``qsur_mini_mm`` is ``(n_mini,)``: the minibacia's surface-runoff depth for the day.
    This is the reference path - it evaluates MUSLE cell by cell through
    :func:`musle_load_tonnes`, so what the tests check is what the run uses.
    """
    q = _finite_nonneg("qsur_mini_mm", qsur_mini_mm)
    if q.shape != (geom.n_mini,):
        raise ValueError(f"qsur_mini_mm must be ({geom.n_mini},), got {q.shape}")
    q_cell = q[geom.cell_mini]
    a_p = float(params.pixel_area_km2)
    qpeak_cell = qpeak_daily_mean(q_cell, a_p)
    per_pixel = musle_load_tonnes(
        q_cell, qpeak_cell, a_p,
        effective_k(geom, params), geom.cell_c, geom.cell_p, effective_ls2d(geom, params),
        alpha=float(params.alpha), beta=float(params.beta), fg=float(params.fg),
        volume_factor=params.volume_factor, validate=False,
    )
    return per_pixel * (geom.cell_area_km2 / a_p)


# ---------------------------------------------------------------------------
# state, drivers, result
# ---------------------------------------------------------------------------


@dataclass
class SedState:
    """Mutable state: tonnes held in each minibacia's delivery reservoir."""

    store_t: np.ndarray          # (n,) tonnes

    @classmethod
    def initial(cls, geom: SedGeometry) -> "SedState":
        """Cold start with an empty store.

        Unlike the water balance there is nothing to warm up: the store's only input is the
        day's erosion and, at the default ``tau`` = 0, it is empty at the end of every day.
        A non-zero ``tau`` fills it within a few ``tau``, which is why C4's spin-up note
        (docs/31 §C4.2) is about antecedent CHANNEL state, not about this store.
        """
        return cls(store_t=np.zeros(geom.n_mini, dtype=np.float64))

    def copy(self) -> "SedState":
        return SedState(store_t=self.store_t.copy())

    def stored_tonnes(self) -> float:
        return float(math.fsum(self.store_t.tolist()))


@dataclass(frozen=True)
class SedDrivers:
    """The frozen hydrology this module consumes, and nothing else."""

    qsur_mm: np.ndarray          # (ndays, n_mini) float32, mm/day
    dates: np.ndarray            # (ndays,) datetime64[D]
    mini_ids: np.ndarray         # (n_mini,) int64
    own_area_km2: np.ndarray     # (n_mini,) float64
    qsur_field: str
    meta: dict = field(default_factory=dict, repr=False)

    @property
    def ndays(self) -> int:
        return int(self.qsur_mm.shape[0])


def load_drivers(
    path=DEFAULT_DRIVERS_PATH,
    *,
    qsur_field: str = "qsur_rel_mm",
) -> SedDrivers:
    """Read ``Qsur`` (and geometry keys) out of the frozen H2E driver bundle, read-only.

    ``qsur_field`` defaults to the REGISTERED ``qsur_rel_mm`` (docs/35 §1).  ``qsur_gen_mm``
    (runoff generated on the URH columns, before the surface reservoir) is the field
    Buarque's eq. 7 uses and is available for the comparison the module docstring quantifies
    - but it is not the default, because the registration predates this module.

    Only the one requested field is materialised: each is 3652 x 8672 float32 = 121 MB and
    the file holds five of them.
    """
    if qsur_field not in QSUR_FIELDS:
        raise ValueError(f"qsur_field must be one of {QSUR_FIELDS}")
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(
            f"{p} not found. It is the frozen H2E driver bundle (546 MB, gitignored); "
            "rebuild it with src/build_h2e_drivers.py - do NOT re-run the hydrology by hand."
        )
    import json

    with np.load(p, allow_pickle=False) as z:
        if qsur_field not in z.files:
            raise KeyError(f"{p} has no field '{qsur_field}'; it holds {sorted(z.files)}")
        qsur = z[qsur_field]
        dates = z["dates"]
        ids = z["minibacia_id"].astype(np.int64)
        own_area = z["own_area_km2"].astype(np.float64)
        meta_raw = str(z["meta"][0]) if "meta" in z.files else "{}"
    try:
        meta = json.loads(meta_raw)
    except ValueError:
        meta = {"raw": meta_raw}
    if qsur.ndim != 2 or qsur.shape[1] != ids.size or qsur.shape[0] != dates.size:
        raise ValueError(
            f"{qsur_field} is {qsur.shape} but dates is {dates.shape} and minibacia_id is "
            f"{ids.shape} - the driver bundle is inconsistent; do not proceed"
        )
    return SedDrivers(qsur_mm=qsur, dates=dates, mini_ids=ids, own_area_km2=own_area,
                      qsur_field=qsur_field, meta=meta)


@dataclass
class SedResult:
    """Delivered load plus everything needed to audit the run."""

    dates: Optional[np.ndarray]
    record_ids: np.ndarray             # (m,) minibacia ids of the recorded columns
    delivered_t_day: Optional[np.ndarray]   # (ndays_rec, m) tonnes/day, or None
    series: dict                       # basin-total daily series, tonnes/day
    cell_eroded_t: np.ndarray          # (N,) period-total gross erosion per URH cell
    ledger: dict
    state: SedState
    params: SedParams
    backend: str
    wall_time_s: float

    def load_at(self, mini_id: int) -> np.ndarray:
        if self.delivered_t_day is None:
            raise ValueError("this run was made with store_daily=False")
        j = int(np.flatnonzero(self.record_ids == int(mini_id))[0])
        return self.delivered_t_day[:, j]

    def eroded_by_land_class(self, geom: SedGeometry) -> dict:
        """Period-total gross erosion (tonnes) grouped by land class - attribution, not yield."""
        land = geom.cell_land_class()
        return {LAND_CLASS_NAMES[int(k)]: float(self.cell_eroded_t[land == k].sum())
                for k in np.unique(land)}


# ---------------------------------------------------------------------------
# the driver loop
# ---------------------------------------------------------------------------


def _assemble_ledger(eroded_daily, delivered_daily, store_start: float,
                     store_end: float) -> dict:
    """Close the sediment budget: ``eroded = delivered + (store_end - store_start)``.

    Totals are summed with :func:`math.fsum` so the ACCOUNTING contributes no error of its
    own; whatever residual remains is the per-day float rounding of the reservoir update,
    and at the default ``tau`` = 0 it is exactly 0.0 because ``delivered`` is bitwise
    ``eroded``.  ``exact`` records which of those two situations the run was in, instead of
    letting a tolerance hide the difference.
    """
    eroded = math.fsum(eroded_daily)
    delivered = math.fsum(delivered_daily)
    residual = eroded - delivered - (store_end - store_start)
    scale = max(abs(eroded), 1.0)
    return {
        "eroded_t": eroded,
        "delivered_t": delivered,
        "store_start_t": store_start,
        "store_end_t": store_end,
        "residual_t": residual,
        "residual_relative": abs(residual) / scale,
        "exact": residual == 0.0,
        "ndays": len(eroded_daily),
    }


def simulate_sediment(
    geom: SedGeometry,
    params: SedParams,
    qsur_mm: np.ndarray,
    *,
    dates: Optional[Sequence] = None,
    record_ids: Optional[Sequence[int]] = None,
    state: Optional[SedState] = None,
    backend: str = "auto",
    store_daily: bool = True,
    dtype_out: type = np.float32,
) -> SedResult:
    """Run the hillslope-erosion model over ``qsur_mm`` ``(ndays, n_mini)``, mm/day.

    Parameters
    ----------
    qsur_mm
        Surface-runoff depth per minibacia-day, columns ordered like ``geom.mini_ids``.
        Get it from :func:`load_drivers`; NEVER from the wide forcing CSVs (pandas returns a
        silent truncated prefix on those - see ``src/forcing_npy.py``).
    record_ids
        Minibacia ids to write out; ``None`` records all (float32, 126 MB for the full
        basin-decade).  ``store_daily=False`` skips the array entirely and keeps only the
        basin series, the per-cell period totals and the ledger.
    backend
        ``'cells'`` = evaluate MUSLE on all 32,782 cells daily (reference);
        ``'collapsed'`` = pre-summed static factor, one multiply per minibacia-day - the
        same identity computed a different way, only 1.5x faster, kept as an independent
        second implementation; ``'auto'`` = collapsed.  ``tests/test_sediment.py`` asserts
        the two agree to 1e-12 relative on the synthetic case and on a real year.

    Returns
    -------
    SedResult
        ``delivered_t_day`` is the hillslope load delivered to each reach, in TONNES/DAY.
        It is a lower bound (module docstring, BIAS THIS MODULE INHERITS) and it is not a
        yield: nothing is divided by an area anywhere.
    """
    if backend == "auto":
        backend = "collapsed"
    if backend not in ("cells", "collapsed"):
        raise ValueError("backend must be 'cells', 'collapsed' or 'auto'")
    t0 = time.perf_counter()
    n = geom.n_mini
    q = np.asarray(qsur_mm)
    if q.ndim != 2 or q.shape[1] != n:
        raise ValueError(f"qsur_mm must be (ndays, {n}), got {q.shape}")
    ndays = int(q.shape[0])
    if dates is not None and len(dates) != ndays:
        raise ValueError(
            f"dates has {len(dates)} entries but qsur_mm has {ndays} days - a mismatch "
            "here silently mislabels the output time axis"
        )
    # One full-array screen up front: a NaN or a negative Qsur anywhere would otherwise
    # propagate into the load as a NaN and be found only by bisection.
    if not np.all(np.isfinite(q)):
        raise ValueError(f"qsur_mm has {int((~np.isfinite(q)).sum())} non-finite entries")
    if np.any(q < 0.0):
        raise ValueError("qsur_mm has negative entries - surface runoff cannot be negative")

    if record_ids is None:
        rec_idx = np.arange(n, dtype=np.int64)
        rec_ids = geom.mini_ids.copy()
    else:
        rec_idx = geom.index_of(record_ids)
        rec_ids = geom.mini_ids[rec_idx]
    out = (np.empty((ndays, rec_idx.size), dtype=dtype_out) if store_daily else None)

    st = SedState.initial(geom) if state is None else state.copy()
    if st.store_t.shape != (n,):
        raise ValueError("state does not match geometry")
    store_start = st.stored_tonnes()
    coef = params.delivery_release_coef

    static_cell = cell_static_factor(geom, params)
    static_mini = mini_static_factor(geom, params)
    cell_mini = geom.cell_mini
    ser = {k: np.zeros(ndays) for k in ("eroded", "delivered", "store_end")}
    eroded_daily = ser["eroded"]
    delivered_daily = ser["delivered"]
    cell_acc = np.zeros(geom.n_cells)
    term_sum_mini = np.zeros(n)

    for t in range(ndays):
        q_day = q[t].astype(np.float64, copy=False)
        term = runoff_energy_term(q_day, params, validate=False)
        if backend == "cells":
            cell_day = static_cell * term[cell_mini]
            cell_acc += cell_day
            eroded = np.bincount(cell_mini, weights=cell_day, minlength=n)
        else:
            term_sum_mini += term
            eroded = static_mini * term
        # delivery reservoir: a structural partition of the store, so no tonne is created
        # or dropped.  coef == 1.0 (tau = 0) makes this bitwise pass-through.
        s = st.store_t + eroded
        delivered = s * coef
        st.store_t = s - delivered
        eroded_daily[t] = eroded.sum()
        delivered_daily[t] = delivered.sum()
        ser["store_end"][t] = st.store_t.sum()
        if out is not None:
            out[t] = delivered[rec_idx]

    if backend != "cells":
        cell_acc = static_cell * term_sum_mini[cell_mini]
    ledger = _assemble_ledger(eroded_daily.tolist(), delivered_daily.tolist(),
                              store_start, st.stored_tonnes())
    return SedResult(
        dates=None if dates is None else np.asarray(dates),
        record_ids=rec_ids,
        delivered_t_day=out,
        series=ser,
        cell_eroded_t=cell_acc,
        ledger=ledger,
        state=st,
        params=params,
        backend=backend,
        wall_time_s=time.perf_counter() - t0,
    )

# journal_x59-refute-1

Role: REFUTER. Default posture: the finding is WRONG. Read-only except this file.

Target finding (from x59-lens-overclaim, HIGH):
"The narrowing to `K` ... is contradicted by R2's committed code, and its own open item X13 says so"
locator: docs/59_cross_implementation_comparison.md:121-125, :470, :501, :478-486, :1013

## Plan
1. Verify the quoted strings exist verbatim at the named locators in docs/59.
2. Independently re-run the greps in THEIR read-only clone at d055561.
3. Verify hash / bytes of minibacia_soil_params.csv and input_hashes.txt line 9.
4. Check whether docs/59 already discloses this (X13) => a disclosed weakness is not a defect.
5. Check for category errors and re-grade severity.

## 1. Locators and verbatim quotes in docs/59 — ALL ACCURATE

- `:121` "and — newly, at hash level — the **soil/K product**" ✔ verbatim
- `:122-123` "Of the four C4.3 over-production suspects named in `docs/35` §6.1, **`K` is now the one the argument reaches** (one input, byte-identical, two implementations)" ✔ verbatim
- `:463-464` "the net effect is that the argument now reaches **one** of the four C4.3 suspects instead of none." ✔ verbatim
- `:470` soils row: "`minibacia_soil_params.csv` — **BYTE-IDENTICAL**", sha256 6e5940…ae38b1, 398,698 bytes, "MANIFEST A9: *\"soil/K source as used\"*" ✔ verbatim
- `:501` K row R2 cell: "**the same file, byte-identical** (§5.1) — though aggregated onto 7,929 catchments × 12 HRUs rather than 8,672 × 24 URH, and their code also contains a SoilGrids/EPIC path (**X13**)"; verdict cell "**YES — the one suspect the argument reaches.** A code-difference argument cannot exonerate `K`: both implementations read the same numbers" ✔ verbatim
- `:483-486` "Two honest limits: a hash proves **the file is the same file**, not **which code path consumed it** … **X13** … this is **one** row of `input_hashes.txt` tested, not twenty (**X12**)." ✔ verbatim  → THE DOC DOES DISCLOSE
- `:1013` X13: "**Which soil/K code path R2's shipped run actually used.** … **Two of their own statements conflict at `d055561`.** … **This document quotes both and adjudicates neither.**" ✔ verbatim

No misquote. Every locator lands.

## 2. Re-ran the finding's greps in the read-only clone (HEAD d055561843d437419cc13d9fcbc45eefb0a2ffa9, Mon Aug 3 05:23:00 2026)

(a) `grep -rn minibacia_soil_params .` (all file types, .git excluded) → EXACTLY TWO hits:
    config/data_sources.yaml:17 ; scripts/14_integrate_data_final.py:97    → CONFIRMED
(b) `grep -rn data_sources --include=*.py .` → 14_integrate_data_final.py:25 (prose), :177
    (`--config-out config/data_sources.yaml`). That script WRITES the yaml. No model code reads it. → CONFIRMED
(c) only producer of BasinData.k_factor: src/mgbsed/preprocess/hru.py:185 build_k_factor
    (docstring: "K is computed cell-by-cell from the actual SoilGrids composition"), calling
    erodibility_sharpley_williams; invoked scripts/04_build_basin.py:383 on rasters from
    soil_mean_profile(Path(args.soil_dir), …), `--soil-dir` default `data/raw/soil`, pattern
    `soilgrids_{clay,silt,sand,soc}_{depth}_mean.tif` (:104, :234, :364-367); assembled :426;
    consumed model/simulate.py:368,604 → model/musle.py:341
    `yield_t = yield_t * k_factor * c_factor * params.p_factor * ls2d`. → CONFIRMED
(d) `grep -rnE "soil_params|read_csv\(.*soil|Wm" --include=*.py .` → no reader of any soil CSV
    anywhere (only 06_calibrate.py/16_load_discharge.py prose and soil_water.py maths). → CONFIRMED
    `grep -rni "igac" --include=*.py .` → hits ONLY in 14_integrate_data_final.py (the yaml writer). → CONFIRMED
(e) our file header: `id,Wm_mm,K,depth_cm,texture,drainage,area_km2,downstream`, 8,672 data rows. → CONFIRMED

## 3. Hash / bytes recomputed here
python3.10: data/processed/minibacia_soil_params.csv → 398,698 bytes,
sha256 6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1
`input_hashes.txt` line 9 = same hash for `02_basin_and_soils/minibacia_soil_params.csv`. → CONFIRMED.
Byte-identity is REAL. §5.1's R1-side K stats also re-verified from that file:
n 8672, median 0.03055, mean 0.03182408902214022, min 0.019, max 0.0495, CV 0.2289362876681507. ✔

## 4. The finding UNDERSTATED its own case, and mis-described one leg
The lens said R2 has "three mutually inconsistent statements". That count is wrong in two ways.
- `config/data_sources.yaml` does NOT contradict the MANIFEST: it says `soils.primary: IGAC national
  field survey`, `minibacia_params: …/minibacia_soil_params.csv`, and "SoilGrids is comparison and
  gap-fill only". That AGREES with the MANIFEST on canonicity (though it declares canonical DATA, not
  a consumed code path — and no model code reads the yaml). So the lens inverted this leg.
- But their committed README.md at d055561 says the opposite of the MANIFEST, five times:
  :108  "Soil erodibility **K** | EPIC formulation, 0.1317 SI conversion | Sharpley & Williams (1990)"
  :157  "Soil | ISRIC SoilGrids | 250 m | clay/silt/sand/SOC × 3 depths | 12 rasters"
  :158  "Soil (alternative) | **IGAC national field survey**"
  :926  (§11.1 "Decision points where independent teams diverge. Our value given for each.")
        "Soil | SoilGrids (**IGAC available, not yet used**) | SoilGrids classes 95% of the basin
         \"Fine\" against IGAC's 38%"
  :1020 (future-work list, item 5) "**IGAC soils instead of SoilGrids.** Documented disagreement:
         95% vs 38% \"Fine\". K depends on texture, so it propagates into sediment."
  plus :691-692 "the SoilGrids-derived storage capacities were about right".
=> The author's OWN ACCOUNT at d055561 says IGAC is NOT YET USED and lists adopting it as FUTURE
WORK. So Tier B does not resolve in favour of the CSV: the author contradicts the author. The single
statement supporting "as used" is MANIFEST.md:46, written 2026-08-13, ten days after d055561.
The lens's "rests on one line of author prose" is therefore CORRECT and stronger than it claimed.

## 5. Is this a disclosed weakness (=> not a defect)?
Partly. §5.1 :483-486 and the §5.3 R2 cell both flag X13, and §5.3 :506-508 drains the row
("produces **no positive evidence against** `K`"). But the doc still GRADES the row **YES**, still
asserts the unhedged "**both implementations read the same numbers**" (a consumption claim no
committed code path supports), and the top VERDICT block :119-127 prints the narrowing with NO X13
caveat and NO hedge. Disclosing a limit and then grading against it is not the same as disclosing it.
Category error present: CITED (an author line) treated as VALIDATED (a code path) — the exact
distinction docs/59 itself quotes at :441 ("cited is not validated").

## 6. Minor inaccuracy in the finding, not load-bearing
"the document's only new positive result" — the VERDICT/§8.2 also newly close X5 (184 m), X9
(R1's accusation withdrawn), X10 (grouped split 0.918→0.801 / 0.905→0.781), and record the
1,965 vs 2,036.4 mm/yr rainfall pair. "Only" is inaccurate; the rest of the finding stands.

## VERDICT: NOT REFUTED. Severity HIGH upheld.

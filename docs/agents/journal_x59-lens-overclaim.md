# journal: x59-lens-overclaim

Role: adversarial lens on docs/59_cross_implementation_comparison.md. READ-ONLY except this file.
Default posture: docs/59 takes credit it has not earned and flatters us.

## Log

### Step 0 — journal created

### Step 1 — read the artifact
`docs/59_cross_implementation_comparison.md`, 1,206 lines, read in full (4 Read calls).
`docs/agents/journal_x59-write.md` 278 lines (writer's process record) consulted for its
verification table (§1.3) and its list of four own-measurements.

### Step 2 — pin verification (PASSES)
```
$ sha256sum data/raw/refs/yben409_sediment_repo.bundle
adf7a1d1bf21d62057257de14bc8adf0584facfa1e37cfe1f5b7afafb551ca9e   <- matches docs/59 §0
$ (in their clone) git log -1 --format='%H %ad'
d055561843d437419cc13d9fcbc45eefb0a2ffa9 Mon Aug 3 05:23:00 2026 -0500  <- matches §0
```
Document is pinned to commit + bundle hash + date, and §0 states counterpart numbers will change.
NO FINDING on the pin.

### Step 3 — soil hash (file identity PASSES; the inference built on it does not — see Step 6)
```
$ sha256sum data/processed/minibacia_soil_params.csv
6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1  (398698 bytes)
$ grep -n -i soil data/raw/colleague_share/input_hashes.txt
9:6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1 ... 02_basin_and_soils/minibacia_soil_params.csv
$ head -1 data/processed/minibacia_soil_params.csv
id,Wm_mm,K,depth_cm,texture,drainage,area_km2,downstream
```
Byte-identity CONFIRMED.

### Step 4 — station containment, re-measured by me from both repos (PASSES)
python3.10 + pandas, int() normalisation of their 10-char zero-padded codes:
```
their sizes 21 13 90 | our79 79 our_dis 192
21 in our79: 21  only-theirs: []
13 in our79: 13  only-theirs: []
90 in our_dis: 90 only-theirs: []
```
Containment 1.000 in all three, ONLY-theirs empty. docs/59's central data-dependence claim is
correct as stated. (our79 = sediment_inventory_qc.csv; our_dis = discharge_inventory.csv 192 rows.)

### Step 5 — the SSC defect is independently verifiable in their committed code (STRENGTHENS §3.1)
`src/mgbsed/model/sediment.py` (advection block, ~L388-415):
```
state.channel[c.name] = np.maximum(new_mass, 0.0)
qss_t_s = outflow / dt_s
ssc = self.concentration_mg_l(new_mass, v_ch)      <- concentration from POST-EXPORT residual mass
```
Exactly the defect MANIFEST.md describes. So the VOID verdict does not rest only on their prose.
§9 does not claim this check was run; I ran it and it holds. NO FINDING — a corroboration.

### Step 6 — THE K NARROWING: contradicted by their committed code (FINDING 1)
```
$ grep -rn "minibacia_soil_params" .        (their clone, all file types)
config/data_sources.yaml:17
scripts/14_integrate_data_final.py:97
$ grep -rn "data_sources" --include=*.py .
scripts/14_integrate_data_final.py:25 (prose), :177 (--config-out) -- WRITES it; no model code reads it
$ grep -rn "k_factor" --include=*.py src/ | head
model/basin.py:61 k_factor: np.ndarray ; model/simulate.py:368,604 k_factor=basin.k_factor
preprocess/hru.py:185 def build_k_factor(...)
$ sed -n '370,395p;104p;234p;364,367p' scripts/04_build_basin.py
--soil-dir default data/raw/soil ; soilgrids_{clay,silt,sand,soc}_{depth}_mean.tif
k_factor = build_k_factor(catchment_id, texture_class, cover_class, sand, silt, clay, soc, n)
$ grep -n -A 30 "def build_k_factor" src/mgbsed/preprocess/hru.py
"K is computed cell-by-cell from the actual SoilGrids composition" -> erodibility_sharpley_williams
$ grep -rn "soil_params|read_csv.*soil|Wm" --include=*.py .   -> no reader anywhere
```
=> No committed code path carries the byte-identical file into their MUSLE `k_factor`. The only
K path is SoilGrids/EPIC. So "both implementations read the same numbers" (§5.3) and "K is now the
one the argument reaches" (VERDICT, §5.3) are NOT SUPPORTED; the honest grade is X13's own
UNRESOLVED, and the narrowing then reaches ZERO of the four suspects.

### Step 7 — score juxtaposition (FINDING 2)
docs/59:216 is a two-column comparison-table row: `F_report -0.118 (est. a) / +0.139 (est. b)`
opposite `stage2_median_kge_log 0.05461202762457862 ... both computed on defective simulated SSC`.
docs/59:250-254 (§3.1) forbids exactly this: "must not be compared to R1's -0.118 / +0.139. Not in
a table, not in a sentence, not in a figure, not with a caveat."
No ranking SENTENCE exists anywhere (grep for "better|outperform|higher score" -> none).

### Step 8 — the interiority / no-rail inference (FINDING 3)
docs/59:227-231 (§2.1) "This is a fact about their search geometry and it survives §3.1, because a
rail is a property of the box and the objective surface, not of the level of the score."
docs/59:340 (§3.5) "the constraint is exactly why R1 railed and R2 did not."
The argmax location is a property of the SAME defective objective surface. Their re-run already
moves the surface (stage 3 fires, 3 rules, +0.068 -> +0.087; ANSWERS C1).

### Step 9 — band / materiality check (FINDING 4, FINDING 5)
docs/59:780-786 table column header is literally "agreement"; four rows 4.3/3.5/3.6/1.0 %, one row
annotated "14 % - disagrees"; §6.5 text "Three of four agree to 3.5-4.3 %". §9 (:1149-1158) claims
"No threshold, tolerance, materiality bar or band is introduced anywhere".
Also :785 "product of means 3.928965 / 3.966659 / 1.0 %" sits inside the "What IS corroborated"
table although §6.4 (:772) grades the product of marginals NOT COMPARABLE.

### Step 10 — clean checks
```
$ grep -n -E "t/km|km2/yr|km²/yr" docs/59...md   -> 1 hit, line 1160, the embargo disclosure itself
$ grep -n -i replicat docs/59...md               -> :88,:89,:90,:1197 all PROHIBITIONS
$ sed -n '515,525p' src/mgb_transport.py         -> k_dep: object = 0.0 (docs/59 §8.3 correct)
$ grep -rn "condition number" docs/42...md       -> :115 inf (13-station design), :710 5,682
      (composition design after A-P1, "basin-total form still inf") -- §4.1 as stated is consistent
our-side numbers re-verified: docs/55:19 (-0.118, box floor alpha=2.0) and :109 (+0.139);
docs/43:16 + docs/45:490 (66.53 %, 199.29 of 299.54 Mt/yr, 801.1 km); docs/35:353 (f_LS 0.25146);
c5_enso_contrast.json median_ratio 3.046755091543662; docs/16:452 (2,073.1 / 2,036.4, 2,206 stale);
docs/35:1099 + docs/45:1288 (C revision 1.204272539864846).
arithmetic re-derived: 3.5061873895109055 %, 5.2144131976267385 %, x26.442009334002304,
x2.0611616793829812, +0.004409952544391804 -- all reproduce.
MANIFEST.md and ANSWERS_C1_C2_C3.md read in full; every quotation in docs/59 that I spot-checked
is verbatim and in context (SSC defect, metric warning, 0.918->0.801 / 0.905->0.781, 82 sites /
58 / 97 % / Taihu 113, 41 South American from 3 Brazilian sites / 0 Colombian, selectivity request,
TriggerSet last-match-wins, stage 3 = 3 rules +0.068->+0.087, 1,965 mm/yr, 88 gauges, 199 of 287).
Their in-script precip QC verified in code (15_build_forcing_v2.py load_gauge_precip: <80 % density
drop, no-coordinate drop, <20 gauge abort, 4.5/6.9/13.0 mm/day docstring); no precip_gauges_daily_qc
reference anywhere in their python. TriggerSet last-match-wins verified at musle.py:200-208.
```
No fit run, no engine default touched, no git command, nothing written outside this journal.

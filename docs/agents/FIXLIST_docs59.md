# FIXLIST — docs/59 post-verification repair

> Generated 2026-08-13 from workflow run `wf_5ecff859-6a3` (12 agents, 0 errors).
> Lens journals: `docs/agents/journal_x59-lens-overclaim.md`, `journal_x59-lens-numbers.md`.
> Refuter journals: `docs/agents/journal_x59-refute-1.md` … `-5.md`.
> **Every finding below has ALREADY been independently refuted or confirmed. Do not re-audit,
> do not re-measure, do not spawn agents. Apply, verify, report.**

**Context that survived the sweep, so you do not redo it:** the overclaim lens found its default
posture NOT SUSTAINED (no independent-replication claim, no ranking, no inflated shared-inputs
argument; the pin verifies on disk). The numbers lens re-derived ~218 figures and **211 are clean**.
`docs/59` is fundamentally sound — this is a repair pass, not a rewrite.

---

## A. CONFIRMED — survived independent refutation. APPLY ALL.

### A1 — [HIGH] The narrowing to `K` — the document's only new positive result — is contradicted by R2's committed code, and its own open item X13 says so

**Locator:** docs/59_cross_implementation_comparison.md:121-125 (VERDICT), :470 (§5.1 soils row), :501 (§5.3 `K` row verdict cell), :478-486, :1013 (X13)

**Finding (as confirmed by its refuter):**

CONFIRMED with an amended evidence base and one leg of the original evidence corrected.

Grade the §5.3 `K` row **UNRESOLVED (X13)**, not YES. Delete "both implementations read the same numbers", and delete the VERDICT clause "`K` is now the one the argument reaches (one input, byte-identical, two implementations)". Replace with: *a byte-identical soil/K table (`minibacia_soil_params.csv`, sha256 `6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1`, 398,698 bytes, `input_hashes.txt` line 9, recomputed here) was transferred — further evidence that the DATA is shared. But no committed R2 code path carries it into their MUSLE `k_factor`: it appears in exactly two files (`config/data_sources.yaml:17` and `scripts/14_integrate_data_final.py:97`, the script that writes that yaml), no model code reads that yaml, and the sole producer of `BasinData.k_factor` is `preprocess/hru.py:185 build_k_factor` computing K cell-by-cell from SoilGrids via `erodibility_sharpley_williams` (`scripts/04_build_basin.py:364-388`, `--soil-dir` default `data/raw/soil`) and passed unchanged to `musle.py:341`. Whether `K` is shared IN THE MODEL is UNRESOLVED (X13).*

Restate §5's headline (:463-464) and the VERDICT (:121-125) as: **the shared-inputs argument currently reaches NONE of the four C4.3 suspects**; it would reach `K` only if X13 resolves for the CSV. Keep the hash under data-dependence (§5.1), not under narrowing.

Amend X13 — do not restate it from the lens's version. Correct: `config/data_sources.yaml` does NOT contradict the MANIFEST (it declares `soils.primary: IGAC national field survey` and names the CSV as `minibacia_params`); it agrees on canonicity while declaring canonical DATA, not a consumed path. The real conflict is larger than "two statements": at `d055561` their own README says SoilGrids five times — `:108` "Soil erodibility **K** | EPIC formulation … Sharpley & Williams (1990)"; `:157/:158` inventory (SoilGrids as the soil, "Soil (alternative) | IGAC national field survey"); `:926`, under "Decision points where independent teams diverge. Our value given for each.", "Soil | SoilGrids (**IGAC available, not yet used**)"; and `:1020` future-work item 5 "**IGAC soils instead of SoilGrids** … K depends on texture, so it propagates into sediment". So the Tier-B rule cannot settle this row: the author's committed account at `d055561` contradicts the author's `MANIFEST.md:46` line of 2026-08-13. State that plainly, adjudicate none of it, and note the most likely benign reading — a soil switch made after `d055561`, consistent with §0's "mid-rewrite" — which is theirs to confirm and is not a defect of theirs.

Also note in §1.1 that this is the one place where the Tier-B override was applied against a code read that is cheap, checkable and contrary, and that the override is withdrawn on this row.

Two corrections to the finding as filed: (i) its "three mutually inconsistent statements" is wrong as stated — the yaml corroborates the MANIFEST; (ii) "the document's only new positive result" is inaccurate — X5 (184 m), X9 (R1's accusation withdrawn), X10 (0.918→0.801 / 0.905→0.781) and the 1,965 vs 2,036.4 mm/yr pair are also new. Neither correction rescues the `K` grade.

**Fix:**

Grade the `K` row **UNRESOLVED (X13)**, not YES. Delete "both implementations read the same numbers" and the VERDICT clause "`K` is now the one the argument reaches (one input, byte-identical, two implementations)"; replace with: *a byte-identical soil/K table was transferred, which is further evidence that the DATA is shared, but no committed R2 code path carries it into their MUSLE `k_factor` — their only K path is SoilGrids/EPIC (`hru.py:185`, `04_build_basin.py:383`), so whether `K` is shared IN THE MODEL is UNRESOLVED.* Restate §5's headline as: the shared-inputs argument currently reaches **none** of the four suspects, and would reach `K` only if X13 resolves for the CSV. Add the three-way inconsistency (MANIFEST vs `data_sources.yaml` vs `build_k_factor`) to X13, still adjudicating none of it. Keep the hash where it belongs — under data-dependence, not under narrowing.

---

### A2 — [MEDIUM] The bundle archive IS on this disk — §1.2's stated evidence limit is overstated, and three open items are settleable today

**Locator:** docs/59_cross_implementation_comparison.md §1.2 (lines 164-171), §9 (lines 1113-1116), §8.1 items X3/X4/X11 (lines 1006-1011)

**Finding (as confirmed by its refuter):**

§1.2 (docs/59 lines 164-171) understates what is readable, in one sentence. The clause "no bundle archive is present under `data/raw/`" is literally true but scoped to one directory: `magdalena_share_for_colleague.zip` (306,200,202 B) sits at the repository ROOT, invisible to `git status` only because `.gitignore:52` is `*.zip`, and §0 (line 38) already names it and quotes that exact byte count. Streamed read-only sha256 of every member against `input_hashes.txt` verifies 20/20 — the archive IS the bundle, and its data files open without extraction (observed_ssc_daily.parquet -> (3652, 59); observed_ssc_stations.csv -> (59, 10); basin_magdalena.pkl unpickles to BasinData, n_cat 7929, with ls2d mean 23.631671 / median 15.318151 and ls2d_trigger median 9036.8 / max 344389.6, reproducing their docstring's "median 9,037, max 344,390").

FIX (small, and confined to §1.2 and two X rows):
- Replace the "no bundle archive is present under `data/raw/`" clause and the "So ..." inference with: the archive is present at the repository root (gitignored, 306,200,202 B, 20 data files, all hash-verified against `input_hashes.txt`) and its data members were NOT OPENED by this pass — a choice about scope, not a limit on the evidence. Keep the true provenance sentence: every claim here about a bundle data file rests on the manifest text or on a hash.
- X3: re-grade to "resolvable from this disk today (Tier 1 is inside the root archive); not done."
- X11: SPLIT. The LS2D-mean half is resolvable today from `basin_magdalena.pkl` in that archive. The basin-sediment-level half is NOT — the bundle withholds `stage1_*`/`stage2_*` as mid-rewrite, so §4 item 5 ("no basin sediment load of theirs exists on this disk in any form") stands unchanged.

NOT part of the fix: X4 already reads "**Settleable now; not done.**" and X12 already reads "(cheap, not done)". §9 needs no change — "its 20 data files were not extracted into this repository and none was opened" is a true account of what the pass did, not a claim of absence. And there is no second copy of the archive in Downloads; exactly one copy exists.

Severity MEDIUM, not HIGH: no docs/59 number or conclusion changes, the mis-scoped sentence sits inside an explicitly self-limiting disclosure the document is required to print, and §0 supplies the counter-fact 126 lines earlier.

**Fix:**

Replace "no bundle archive is present under `data/raw/`" and the "never on a read of the file" inference with the true statement: the archive is present at the repository root (gitignored, 306,200,202 B, 20 data files) and was NOT OPENED by this pass — a choice, not a limit. Re-grade X3 and X4 from "not extracted here" to "resolvable from disk, not done", and split X11: the LS2D-mean half is inside `basin_magdalena.pkl` in that archive; only the sediment-level half needs a run they have not dumped. §9's disclosure should say the archive was not opened rather than implying it is absent.

---

### A3 — [MEDIUM] The Fagundes bar [−0.26, 0.44] is cited to `docs/45` §84, which contains no bar

**Locator:** docs/59_cross_implementation_comparison.md line 217 (§2 table, row "the bar")

**Finding (as confirmed by its refuter):**

docs/59:217 mis-locates the sediment KGE bar: it cites `docs/45` §84, which is the P1 α-search-box row of §2.1 (**[2.0, 30.0]** log-spaced) and states no KGE band; the bar is registered at `docs/45` line 307, inside §3.2, and that locator appears nowhere in docs/59 (the string "0.26" occurs exactly once in the whole document). §84 does contain "Fagundes (2018) §6.3.1" verbatim, so the pointer is misdirected rather than fabricated — and docs/59 uses §84 a second time, correctly, at line 336 for the α prior (not "two rows later" in the §2 table, which carries no citation). Compounding it, the cell's attribution of the band to Fagundes **(2018) §6.3.1** is unsupported by any artifact: every in-repo use of §6.3.1 concerns α/β calibratability or the MOCOM-UA prior [2.0, 25.0], while the band is sourced in-repo and in the counterpart's own metrics.py L7 to **Fagundes et al. (2026)**'s conclusions, and neither full text is on disk (docs/35:127, docs/36:761). Mitigating and capping severity at MEDIUM: the interval itself is correct and correctly registered in the cited document, the row's right-hand cell is verbatim-accurate against `src/mgbsed/calibration/metrics.py` L7 and L53–54, and docs/59:1157 already states the bar is used only as a "descriptive tall[y] against the CITED Fagundes band … not a new gate", so no verdict in the document turns on it.

**Fix:**

Change the bar's citation to `docs/45` §3.2 (line 307), and keep §84 for the α box only. Note also that §84's "Fagundes (2018)" conflicts with `docs/19`:428, `docs/30`:215 and `docs/31`:64, which all say Fagundes et al. **2026** — that is our inconsistency, not docs/59's, but the year should not be introduced into a new document without flagging it.

---

### A4 — [MEDIUM] The DEM-archive "genuinely SHARED" row cites `docs/15` L24/L31, which contain neither the archive filename nor the member

**Locator:** docs/59_cross_implementation_comparison.md line 471 (§5.1 table, row "DEM archive")

**Finding (as confirmed by its refuter):**

MEDIUM (was HIGH), CONFIRMED as a citation defect, not a substantive one. docs/59 line 471 (§5.1, row "DEM archive") cites `docs/15` L24/L31 for the archive filename `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, the member `output_hh.tif`, and the 0.000833° resolution. Those lines carry only the dataset (COP90) and the bbox (L24) and the target directory `data/raw/dem/` (L31) — not the filename, not the typo, not the member, not the resolution. The claim itself is true and independently reproducible on both sides (their `config/data_sources.yaml` L11-13; our archive contains exactly one member, `output_hh.tif`, 260,274,553 B, and that raster measures 5640x12000 at res 0.0008333333 with bounds −77.0004/1.4004 to −72.3004/11.4004), so the SHARED verdict and every downstream argument stand; only the pointer is misaddressed. Fix: cite `docs/35` L65-66 for the archive name, the typo and the member; cite `docs/37` L897 (or the raster itself, 5,640 x 12,000 @ 0.000833°) for the resolution; keep `docs/15` L24 for the dataset and bbox only (it is already the right citation for the adjacent "domain bbox" row). Do NOT import docs/35:66's "not extracted" — that is stale: the member is extracted at `%TEMP%\output_hh.tif` (260,274,553 B, 2026-07-30) and is consumed by `scripts/c3/ls2d.py:213-220` and `src/merge_chirps_gauges.py:82`. If a size is quoted for the §5.4 / X6 DEM-provenance item, distinguish member (260,274,553 B) from archive (249,137,558 B).

**Fix:**

Cite `docs/35` lines 65-66 for the archive name, the typo and the member; keep `docs/15` L24 for the dataset (COP90) and the bbox only. Also record from docs/35:66 that our copy is 260,274,553 B and "not extracted", which is directly relevant to the §5.4 / X6 DEM-provenance item.

---

## B. MEDIUM / LOW — raised but NEVER sent to a refuter.

Carry at the stated grade. **Do NOT promote.** Apply only where the locator and the replacement
are unambiguous on the artifact; where they are not, record as an open item in §8.1 and move on.

**B1 — [MEDIUM]** "Interior optimum, no rail" is presented as surviving the SSC defect, but it is the argmax of the same defective objective surface
  - locator: docs/59_cross_implementation_comparison.md:225-231 (§2.1), :340-347 (§3.5), :215 (§2 row "fitted values"), :413-414 (§4.3)
  - fix: In §2.1 delete "and it survives §3.1"; label the fitted position **PRE-FIX, SUSPENDED with the score (X14)**. In §2's "fitted values" row, add the same marker that :216 carries. Reduce §3.5's sentence to a design statement that does not depend on their optimum: *with C fixed and the α box narrow, an upstream over-production has nowhere to go and shows up as a rail; with `c_mult` free over two decades it can be absorbed. Whether R2's post-fix refit rails is unknown and this document does not guess.*

**B2 — [MEDIUM]** A table column headed "agreement", with one row annotated "disagrees", is an undeclared materiality cut against §9's own disclosure
  - locator: docs/59_cross_implementation_comparison.md:780-786 (§6.5 table), :788-790, against :1149-1158 (§9)
  - fix: Rename the column **difference** and drop both verdict words: "three of the four statistics differ by 3.5–4.3 %, the fourth (SSC median ratio) by 14 %, cause unidentified (X3)". Change "a genuine point in R2's favour" to name what is actually favourable — that their pooled marginals are reproducible on an independently QC'd copy of the same archive — without grading the size of the residual difference.

**B3 — [LOW]** The product of marginals — graded NOT COMPARABLE in §6.4 — reappears as a row inside §6.5's "What IS corroborated" table
  - locator: docs/59_cross_implementation_comparison.md:785 (§6.5 table row "product of means") against :751-774 (§6.4)
  - fix: Move the row into §6.4 under a heading such as *"their pooled estimator, reproduced on our data"*, or keep it in place with the cell annotated `NOT COMPARABLE as a flux statistic (§6.4) — reproduction check only`, and say in the prose why it is excluded from the count.

**B4 — [LOW]** "The first external corroboration that decision has ever had" credits R2's note with validating R1's choice, not the property it actually establishes
  - locator: docs/59_cross_implementation_comparison.md:388-389 (§4.2)
  - fix: "…and R2's note is the first external corroboration of the non-identifiability itself. It does not endorse either project's response to it: R2 fitted the level anyway and reported interior optima, and §4.4 item 2 governs what the shared finding may be used for."

**B5 — [MEDIUM]** 66.53 % / 199.29 of 299.54 Mt/yr is attributed to `docs/42` G9, which registers 63.9 % / 158.9 of 248.7 Mt/yr
  - locator: docs/59_cross_implementation_comparison.md §7.4 item 1 (line 945); same triple at §6.7 (line 843) and §8.1 X-item context
  - fix: In §7.4 (and anywhere the triple appears) cite `docs/45` §490/§67-68 for the numbers and `docs/42` G9 only for the disclosure obligation, adding one clause that G9's own registered figures (63.9 % / 158.9 of 248.7) are at the superseded prior-C level — otherwise a reader who checks docs/42 finds three different numbers and cannot tell which document is wrong.

**B6 — [MEDIUM]** "The four C4.3 over-production suspects named in `docs/35` §6.1" — §6.1 names five, including the delivery step
  - locator: docs/59_cross_implementation_comparison.md THE VERDICT (line 123), §3.5 (line 343), §5.3 table header (line 499)
  - fix: Either say "five candidates named in `docs/35` §6.1 (`Qsur`, `K`, `C`, `LS2D`, or the delivery step)" and state that the delivery step is excluded on the measured ground that NEITHER project fits one (our `k_dep` = 0.0 at `src/mgb_transport.py`:521 and `docs/45` §2.3's SDR = 1.0 claim; their `gamma` pinned 1.0), or keep "four" but add that exclusion in the same sentence. As written, the denominator does not match the cited section and the narrowing reads stronger than the registration supports.

**B7 — [MEDIUM]** §0 says `input_hashes.txt` lists 23 member hashes; it lists 20, and §1.2 says 20
  - locator: docs/59_cross_implementation_comparison.md §0 (lines 38-39) against §1.2 (line 166) and X12 (line 1012)
  - fix: Change §0 to "whose **20** member hashes are listed in `input_hashes.txt` (their MANIFEST says 23; the file has 20 — a discrepancy on their side, not ours)". This also removes an internal contradiction between §0, §1.2 and X12 that an auditor will hit immediately.

**B8 — [MEDIUM]** `docs/45` §2.3 is cited for "LS, C, K, f_vol, P, FG fixed, not fitted"; §2.3 registers only the deposition coefficient
  - locator: docs/59_cross_implementation_comparison.md line 211 (§2 table, row "free parameters, count")
  - fix: Cite `docs/45` §2.1 for the two free parameters and `docs/42` §3.1/G6 for the fixed factors; keep `docs/45` §2.3 for the `k_dep` = 0.0 / SDR = 1.0 row, where docs/59 already uses it correctly two rows down.

**B9 — [LOW]** ×1.3496976 is arithmetically wrong; the ratio is ×1.3497013
  - locator: docs/59_cross_implementation_comparison.md §5.5 (line 569)
  - fix: Print ×1.3497013 (or ×1.34970 at a sane precision). The finding it supports is unaffected — the carried figure is quoted to 8 significant figures and should be right at all of them.

**B10 — [LOW]** "est. (b) 2.948674885718534" is docs/34's non-headline (b) row; docs/34's flagged headline (b) is 2.84
  - locator: docs/59_cross_implementation_comparison.md §6.7 (lines 837-838)
  - fix: Write "est. (b), all rating stations (n = 7) 2.948674885718534; docs/34's headline (b), partial-rating excluded (n = 4), is 2.84" — or cite the JSON field name. As written it quotes a docs/34 number that docs/34 itself does not treat as its (b) headline.

**B11 — [LOW]** Two minor quotation/locator slips: `observations.py` L41–46 and the docs/26 §7 "only remaining lever" quote
  - locator: docs/59_cross_implementation_comparison.md §6.3 (line 712) and §5.8 / §10 item 7 (lines 642-643, 1203)
  - fix: (i) Cite L43-46. (ii) Either quote docs/26 §7 verbatim ("the only untried one") or attribute the "only remaining lever" phrasing to `docs/18`:357, where it is verbatim. Both are cosmetic; both are one grep from being right, and this document's whole method is that quotations are checkable.

---

## C. REFUTED — DO NOT APPLY, and do not let it be re-raised.

**§2's comparison table sets the two scores side by side in one row — precisely what §3.1 forbids "not in a table … not with a caveat"**

Why it failed:

The finding quotes accurately and its supporting facts are all real — I confirmed the defect in their committed sediment.py, the MANIFEST wording, the absence of any ranking sentence, and the exactness of every numeral in row 216. It still fails, on the reading of the prohibition it depends on.

THE KILL. The finding reads ":250-251" as a ban on the two numerals CO-OCCURRING. Under that reading the document violates its own rule in three prose places, one of which is the rule's own sentence: :250 reads "`0.05461202762457862` must not be compared to R1's `−0.118` / `+0.139`" — both numerals, one sentence. The VERDICT block at :99-100 does it again: "it must not be set beside our −0.118 (est. a) / +0.139 (est. b) in any table, sentence or figure" — a sentence that sets them beside each other while forbidding it. And :266-267 does it a third time. A reading that makes a rule self-violating three times over is the wrong reading of the rule, not evidence of three defects. The rule's own final clause names its object: "any statement that either project scores better is unsupported." The prohibited object is a comparative claim or a grade. Row 216 makes neither, and the finding itself verified that no such claim exists anywhere in the document.

CONTEXT TEST (the one the brief asks for). §2 is titled "The two configurations, side by side" and is a specification table — variable scored, estimator, transform, station universe, window, free-parameter count, search box, fitted values. "median score reported" is a field of the record. Three independent disclosures surround it: the R2 cell carries two in-cell disqualifiers; row 215 immediately above flags R1's own fit "NOT ADOPTED — RAILED", so the table does not present R1's number as an adoption either; and the paragraph at :221-224, immediately below the table, says of the bar row that it "is also the only row of this table on which a comparison of numbers would have been admissible if the numbers had been sound" — an explicit, in-section statement that no other row, the score row included, admits a comparison of numbers. §3.5:326 ("about design, not scores, so it survives §3.1 intact") and §9:1150-1156 (VOID describes validity, not a gate outcome) confirm the author's own usage. This is a disclosure the document already prints, not a defect it hides.

CATEGORY ERROR. The finding equates "table row" with "comparison instrument". But §2's table is the instrument that establishes incomparability: by row 216 the reader has already crossed :203 (FLUX t/day vs CONCENTRATION mg/L), :205 (different ε), :208 (21/13 vs 8 stations), :209 (730 d vs 1,096 d) and :211 (4 vs 2 free parameters). The rows that make the numbers incommensurable are in the same table, read by the same eye reading across.

THE FIX IS A NET LOSS. The numeral appears at :49 (the PIN), :99, :216, :250 and :407 — and :407 is itself a table. Withholding it from one table while it remains in another table and three prose sentences is cosmetic, and §0's pin rule ("Anyone quoting a number from this document must quote the commit and the date with it") requires the committed value to be on the record so the snapshot stays reproducible after their repo moves on. No figure or summary reproduces §2's table, so the fix's last sentence has no referent.

BEING FAIR TO THE FINDING. Something real survives: "not in a table … not with a caveat" is written more absolutely than the document obeys, so one clause needs a word for literal self-consistency. That is an editorial repair to §3.1's phrasing, not a defect of §2, and it moves no number and creates no overclaim. LOW.

One remnant I pass up separately because it is NOT what was filed and I did not verify it as a defect: the in-cell asymmetry. R2's cell is caveated in-cell; R1's RAILED/EXPLORATORY flag sits in the row above. A row quoted in isolation would read "theirs is broken, ours stands." Fairness-of-tone, LOW, and the cheap remedy is to add "(RAILED, EXPLORATORY — not adopted; docs/55 §1)" to the R1 cell rather than to strip the R2 cell.

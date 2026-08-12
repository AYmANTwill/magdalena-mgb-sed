# Journal - agent a3-enactment (T1: docs/37 amendment A3, the C3.1 enactment)

Started 2026-08-12. Slug: a3-enactment. I own ONLY:
- docs/37_c3_closure.md (append A3)
- docs/agents/journal_a3-enactment.md (this file)

No git commands. No engine default changes. No fits.

## Log

- [t0] Journal created as first action, per brief.

- [t1] Read CLAUDE.md context, docs/00_INDEX.md, docs/47 (full), docs/46 (full, 1400 lines).
  Key confirmations from docs/46 as frozen:
  - §4.2 outcome table: ADOPT-SOURCE condition = all four levers CITED (met) + (R6) not triggered
    (met) + §3.3 exact re-run completed AND REPORTED incl. stratified report + §4.3 forbidden
    evidence untouched. Licence = *proposing* the adopted variant as engine default in a SEPARATE
    dated amendment owned by whoever owns scripts/c3/ls2d.py and docs/37 -- docs/37 §A3.
  - §4.2 note 3: "Reachable != exercised." §3.3's full stratified report NOT discharged (slope
    terciles do not exist; per-station erosion-weighted LSbar only as ratios) -- required before
    ADOPT-SOURCE is EXERCISED, not before the freeze.
  - §3.1 V4_dg = buarque_2015_dg, f_ero 0.25146, f_area 0.2446790094097074.
  - §10 amendment 1: Delta_shape = 0.1299456916752905 => BRANCH B MANDATORY.
  - §7.3 item 5: enactment = docs/37 §A3, and THAT is docs/47's B1 event.
  - §4.4: honest ordering sentence prescribed verbatim.

- [t2] MEASURED ON DISK (read-only), not taken from the panel:
  * `head -1 data/processed/urh_ls2d_variants.csv` ->
    mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,V2b_m_step_eq14,
    V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd  -- **NO V4_dg column**.
  * `head -1 data/processed/urh_ls2d.csv` -> mini,urh,n_cells,area_km2,area_frac,ls2d,ls2d_hs,
    ls2d_mb86,ls2d_dg96 -- no V4_dg either; ls2d_dg96 is Defect B's confounded column.
  * buarque2015.pdf: 9,646,521 bytes, sha256 3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037
    -- MATCHES docs/38 §9.1's card.
  * B3 DISCHARGED: src/mgb_transport.py:908 `if not (m <= max_resid)` with the IEEE-754 comment at
    :902-907; NaN regression test tests/test_transport.py:232 + :274 (`assert math.isnan(...)`).
  * B4 DISCHARGED: docs/42 §9.1-§9.6 amendment log written (A-P1, A-P2, A-P3, A-P1.1); the §9 card
    cell now reads "THREE, all dated 2026-08-11 ... plus A-P1.1".
  * B2 / B5 / §5.5 NOT DISCHARGED: docs/45 §8 reads "Empty at registration"; docs/35 §9 carries
    only 9.1/9.2/9.3 (no alpha-box re-registration).
  * src/mgb_sediment.py: `ls2d_column: str = "ls2d_hs"` at :757, :801, :864; `urh_ls2d: str =
    "urh_ls2d.csv"` at :863.
  * docs/35 §6.1 read directly: reference 11.8; expected 5.9-23.6; watch 23.6-35.4; HARD STOP
    alpha > 35.4; HARD STOP alpha < 3.9.
  * slope terciles: grep across docs/ scripts/ src/ returns only DOCUMENTS that say they are OWED
    (46, 49, 50, 51 + agent journals). No artifact. CONFIRMED ABSENT.
- [t3] ARITHMETIC (python3.10, read-only, full precision):
    3.9*0.25146=0.9806940000000001 ; 5.9*f=1.4836140000000002 ; 11.8*f=2.9672280000000004 ;
    23.6*f=5.934456000000001 ; 35.4*f=8.901684 ; 2.0*f=0.50292 ; 30.0*f=7.543800000000001
    1/f=3.976775630318937 ; ln f=-1.3804713478171018
  On the exact 2nd reproduction f=0.2514648985839397: 0.9807131044773649 / 1.4836429016452444 /
    2.9672858032904887 / 5.9345716065809775 / 8.901857409871466 ; 1/f=3.9766981619750683
  Area proxy f=0.2446790094097074: 0.9542481366978589 / 1.443606155517274 / 2.887212311034548 /
    5.774424622069096 / 8.661636933103642 ; 1/f=4.08698728351287
  Hybrid V4 0.43194: 11.8f=5.096892 ; 35.4f=15.290676 ; 1/f=2.315136361531694
  proxy bias 0.25146/0.2446790094097074 = 1.0277138223121463 (docs/47 R7: 1.0278)
  L-form lever ln(0.43194/0.25146)=0.5410027585442313, ratio 1.7177284657599616
  299.5387088405831*0.2514648985839397 = 75.32347104056149
  joint/product 0.431944/(0.362435*0.522043*1.694054) = 1.347608646050708
  39.812/9.741 = 4.087054717174828 == 1/f_area 4.08698728351287 to 5 s.f.
- [t4] DEFECT FOUND in a file I do NOT own -> REPORT, do not fix: docs/46 §1.0 (and docs/51 §2.3)
  write "ln(0.43194/0.25146) = 0.5410 = -ln 0.580685". Measured: -ln(0.580685)=0.543546837831505
  vs ln(0.43194/0.25146)=0.5410027585442313. Gap 0.0025440792872737372 ln. exp(-0.5410027585)
  = 0.5821641894707599, so 0.5410 pairs with 0.58216, not 0.580685. Immaterial to every verdict
  (both constituents are separately correct); the IDENTITY as written is not exact.
- [t5] Found docs/agents/journal_c31-enactment.md (2026-08-11): a PRIOR session took the same
  task, reached the same decision ("outcome = the source formulation read whole (V4_dg) ...
  ADOPT-SOURCE DETERMINED but NOT EXERCISABLE"), and did NOT write A3 (grep 'A3' docs/37 -> none;
  last amendment A2.7). I do not write to that journal. I cite it as the ordering record.
- [t6] DECISION, taken before writing a word of A3: exercise ADOPT-SOURCE at V4_dg
  (buarque_2015_dg), f_ero 0.25146 / f_area 0.2446790094097074, DETERMINED-not-yet-EXERCISABLE,
  and A3 does NOT propose the default switch. C4.3 stays BLOCKED. Reasons in A3 itself.

## Resumed run, 2026-08-12 (process killed mid-flight in the prior pass)

- [t7] RESUME. Confirmed the state the orchestrator describes: `grep -c "A3" docs/37_c3_closure.md`
  and `grep -n "^## A3" docs/37_c3_closure.md` -> the in-place corrections ARE applied (A3.* pointers
  at lines 11, 111-121, 190, 205-207, 216-275, 329-357, 418, 677-712, 1006-1007, 1175) but NO `## A3`
  section body exists. docs/37 is 1331 lines. My job this run: verify a sample of the in-place edits,
  then APPEND the A3 body so all seven forward references resolve.
- [t8] VERIFIED THE PRIOR PASS'S IN-PLACE EDITS by reading each site (lines 11, 100-125, 185-290,
  325-360, 412-422, 670-716, 1006, 1175). All are the A2.7 strike-through + dated-pointer pattern,
  nothing deleted, every superseded string readable inside `~~...~~`. NO re-application needed.
  BUT the grep found THREE sites the interrupted pass MISSED, all live uses of superseded numbers:
    * line 289  "an LS that is 2.4 - 3.0x too high for its own alpha"  -> LIVE. FIXED this run.
    * line 753  "the LS correction lowers the model by 2.4 - 3.0x"     -> LIVE. FIXED this run.
    * line 209  "(0.502 x 1.714 x 0.351 = 0.302 != the joint 0.421)"   -> live use of x0.502 with
      no label pointer. FIXED this run with pointers to A3.3.1/A3.3.2 and the exact ero factors.
  While fixing 209 I FIRST WROTE THE WRONG PRODUCT and caught it by measuring:
    0.362435*0.517480*1.694054 = 0.3177246791318452  (the CAP)
    0.362435*0.522043*1.694054 = 0.3205262902296241  (the eq.-14 STEP) <- this is the one that
    pairs with the registered joint/product x1.347608646050708. Corrected in place before writing.
- [t9] RE-VERIFIED EVERY NUMBER with python3.10 this run (see A3.8's reproduction block for the
  full list). All match the prior pass. Additional measurements made this run:
    * 129.3840/299.5387088405831 = 0.43194417342854735 -- so the registered hybrid load 129.3840
      corresponds to f_ero 0.4319442, and "0.43194" is its 5 s.f. rounding. 299.5387088405831 *
      0.43194 = 129.38274989660147. A PRECISION NOTE, not a defect; recorded in A3.2.
    * 3.40*0.25146 = 0.8549640000000001 (the docs/45 5%-of-box rail band, rescaled).
    * 0.362435*0.517480*1.694054 vs *0.522043* (above).
- [t10] VERIFIED ON DISK THIS RUN, not carried from the panel:
    * B3: src/mgb_transport.py:908 `if not (m <= max_resid)`; tests/test_transport.py:274
      `assert math.isnan(res.ledger["max_node_residual_t"])`. DISCHARGED.
    * B4: docs/42 §9 amendment log at :616 with A-P1 (§9.2), A-P2 (§9.3), A-P3 (§9.4), A-P1.1
      (§9.5); the §9 card cell at :604 reads "THREE, all dated 2026-08-11 ... plus A-P1.1".
      DISCHARGED.
    * docs/45 §8 at :610-612 still reads "Empty at registration" -> B2, B5 and the §5.5
      disclosure have NOT landed as of my read. I state the C4.3 contract CONDITIONALLY on them.
    * docs/35 §9 carries 9.1 (:476), 9.2 (:551), 9.3 (:678) only -- no alpha-box re-registration.
    * docs/35 §9.3.2 item 1 read verbatim at :710-715: the registered default outcome is
      enumerated as THREE levers -- "slope length limited to one DEM pixel, m stepped and capped
      at 0.5 (his eq. 14), S = Wischmeier & Smith 1978 (his eq. 18)". L IS NOT NAMED. This is the
      SUPREMACY OBJECTION panellists 2 and 3 raised and panellist 1 MISSED. I adjudicate it in
      A3.1.3 and record the docs/35 §9 amendment as OWED, with the explicit conditional branch:
      if docs/35's owner declines it, docs/35 wins on its literal text and NEGATIVE - UNRESOLVED
      is the surviving outcome. Grounds for my adjudication, all read on disk: item 1's own
      stated rationale is LEVEL fidelity ("an LS level that differs from the source's passes
      one-for-one into alpha"), which our point-rate L violates by x1.7177; §9.3.1 at :700-702
      already records the L lever SEPARATELY as x0.790, so item 1's parenthetical is an inventory
      of levers then measured and not a definition; §9.3.4 item 4 pre-authorises supersession; and
      on a genuinely ambiguous reading it is a TIE, which §4.2 item 4 breaks toward the LOWER LS.
    * docs/47:369-371 confirms the formPRESED.exe "(0) standard method / (1) slope scaling method"
      finding -- panellist 1's ADOPT-BAND objection is real on the record. Addressed in A3.1.2's
      risk note: docs/46 §1.2's read-out that (R1) does not fire is FROZEN and in force, the
      plugin is a 2025 successor artifact and not the transposed source of record, and every
      branch of the objection points DOWN, so it threatens the recorded SHAPE (point vs band) and
      never licenses RETAIN-OURS.
    * docs/53:23-24, :134, :141, :143 confirm Delta_shape = 0.1299456916752905, argmax 24037390
      CAPITANEJO, smallest CAL station 26127010 EL ALAMBRADO AUT 0.0179854753, no CAL station
      invariant, CAL 8 f_s spread x1.250023.
    * docs/46:127 carries the defective identity. CONFIRMED. Reported in A3.7, NOT fixed.
- [t11] PANEL ADJUDICATION: all three panellists return ADOPT-SOURCE / DETERMINED-not-exercisable /
  C4.3 NO. I agree and exercise it. Two genuine disagreements I resolve in A3:
    (i) whether §4.2 item 3's rescaling obligation even attaches (panellist 3 reads item 3's
        antecedent narrowly -- it speaks of "a deviation adopted under (2)", and ADOPT-SOURCE is
        item 1's DEFAULT, not a deviation). Textually panellist 3 is right about item 3's
        antecedent, but §4.2's ADOPT-SOURCE licence CELL and §7.3 item 5 BOTH name "the alpha band
        rescaled per item 3" as owed by the enactment unconditionally. The obligation attaches.
        Substantively they are the same arithmetic in two coordinates and I print both, naming
        which coordinate each lives in.
    (ii) panellist 1 alone omits the docs/35 supremacy objection. That is the strongest objection
        on the record and A3 must not omit it. A3.1.3.
  Where all three are wrong: none of them names the three MISSED live sites at docs/37 lines 209,
  289 and 753 (they were reading the file mid-edit). I found and fixed them (t8).
- [t12] WRITING the A3 body now: A3 header, A3.1 (with A3.1.1-A3.1.6), A3.2, A3.3 (with A3.3.1,
  A3.3.2, A3.3.3), A3.4, A3.5 (with A3.5.1, A3.5.2), A3.6 disclosure, A3.7 cross-references,
  A3.8 reproduction. All seven forward references resolve, plus A3.4 which had none.
- [t13] A3 BODY APPENDED to docs/37_c3_closure.md. Structure written (all seven forward references
  RESOLVE, plus A3.4 which had none, plus A3.3.3/A3.6/A3.7/A3.8 which A3's own text introduces):
    1342 # AMENDMENT A3 (2026-08-12, after A2.7)
    1381 ## A3.1     1413 ### A3.1.1  1453 ### A3.1.2  1525 ### A3.1.3  1585 ### A3.1.4
                     1606 ### A3.1.5  1633 ### A3.1.6
    1691 ## A3.2     1771 ## A3.3     1783 ### A3.3.1  1853 ### A3.3.2  1873 ### A3.3.3
    1884 ## A3.4     2019 ## A3.5     2021 ### A3.5.1  2063 ### A3.5.2
    2098 ## A3.6 (disclosure)  2170 ## A3.7 (cross-refs)  2210 ## A3.8 (reproduction)
  Heading level: `###` for three-part numbers, matching the document's own A1.3.1-A1.3.4 precedent
  (A1.9.x uses `##`; the document is internally inconsistent, I followed A1.3.x).
- [t14] POST-WRITE VERIFICATION (all read-only):
  * `grep -o "A3\.[0-9]\(\.[0-9]\)\?"` -> every referenced subsection now has a heading. ZERO
    dangling cross-references.
  * Superseded strings STILL PRESENT and readable inside strike-throughs: "2.37× – 3.00×" x11,
    "2.37×–3.00×" x1, "×0.333 – ×0.421" x6, "2.4 – 3.0×" x4, "≈ 3.9 – 5.0" x2, "≈ 2.0 – 9.9" x2,
    "≈ 11.8 – 14.9" x1, "hard-capped at 0.5" x2. NOTHING DELETED.
  * Markdown table integrity: 9 tables in A3, all column-consistent (script check, 0 inconsistent).
  * Line endings: the file was mixed (1338 CRLF / 934 LF before my append). Normalised the WHOLE
    file to CRLF (2272 CRLF, 0 bare LF, 186,979 bytes) so the append does not introduce a mixed-EOL
    diff. This changes no character of content -- only line terminators.
  * docs/37 is now 2272 lines (was 1331 at resume). Sections A1, A1.9, A2 untouched; the headline
    verdict line untouched; §3 and §6 untouched.
- [t15] FINAL POSITION: outcome ADOPT-SOURCE; ls_formulation = buarque_2015_dg; f_ero 0.25146
  (exact 0.2514648985839397) / f_area 0.2446790094097074; FORMULATION CHOICE = CITED, LS LEVEL =
  UNVALIDATED; alpha reference 2.9672280000000004, band 1.4836140000000002-5.934456000000001,
  hard stop 8.901684, 1/f 3.976775630318937; C4.3 NOT UNBLOCKED; engine default owner = the C3.1
  owner in two separately dated acts, act 2 not draftable until a V4_dg column is committed.
  No git command was run. No engine default moved. No fit. No frozen artifact opened for writing.
  Files written: docs/37_c3_closure.md, docs/agents/journal_a3-enactment.md.

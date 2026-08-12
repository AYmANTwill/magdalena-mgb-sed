# journal — `sweep-phasec` (agent A5)

**Run 2026-08-12. READ-ONLY.** This agent wrote **this file and nothing else**. No doc, notebook,
source file or artifact was edited; no `git add`/`commit`/`push` was run; no frozen artifact under
`sim_calibrated_v2/` was opened.

**Scope swept:** `docs/32` … `docs/53` inclusive (no `docs/44` exists), plus the prose/markdown
content of `src/mgb_sediment.py`, `src/nbgen/make_nb18.py`, `src/nbgen/make_nb19.py`. `docs/00`–`31`
belong to agent A4 and were read only for orientation (`CLAUDE.md`, `docs/00_INDEX.md`).
**Working-tree state was read, not `HEAD`** — the uncommitted edits to `docs/35`, `37`, `42`, `43`,
`45`, `46`, `51`, `src/mgb_sediment.py` and both nbgen generators are treated as current.

**Method.** RULE 0 applied throughout: for a *fact*, the numbered doc that owns the topic wins; for
*status*, `progress_map.html` wins. Every finding names the owner and quotes it. Two numbers were
recomputed from disk rather than adjudicated by preference (§C).

---

## A — THE LEDGER

Sorted HIGH → MEDIUM → LOW. "Frozen?" = the remedy must be an **amendment in the document's own
amendment slot**, never a rewrite of registered text.

| # | sev | `file:line` | stale claim (quoted) | owning doc | what the owning doc actually says | proposed correction | frozen? |
|---|---|---|---|---|---|---|---|
| **1** | **HIGH** | `progress_map.html:575`, `:576`, `:882`, `:718`, `:364`, `:381`, `:483`, `:504` | *"C4 is no longer BLOCKED but is GATED by G1–G9"* (`:575`); *"**C4 MAY NOW START** (docs/37 A1.6)"* (`:576`); *"our LS is **2.37 – 3.00×** the level α = 11.8 is paired with"* (`:576`, `:381`, `:882`); *"248.730 Mt/yr — ADOPTED"* (`:364`, `:483`); *"×0.421 … 0.333 ⇒ 126.2 / 99.7 Mt/yr — still UNRESOLVED"* (`:504`) | `docs/47` (the block); `docs/37` A3 + `docs/51` (the bracket); `docs/37` A1.3.4 (the level) | `docs/47:14` — *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not start.**"*, re-affirmed by `docs/37:1884` (*"Is C4.3 thereby UNBLOCKED? **NO**"*), `docs/45:1064`, `docs/46:1318`, `docs/51:49`, `docs/52:403`, `docs/53:342`. `docs/51:22` — the bracket is *"`f_LS ∈ [0.25146, 0.43194]` … **2.3151× – 3.9768×** … This **supersedes ×0.333 – ×0.421 and \"2.37× – 3.00×\"**"* | Update the tracker's banner, `updated` string, factor-chain SVGs and the `2026-08-11 · docs/37 §4 cand. 0` discovery card. **Per RULE 0 the tracker is the status authority, so it is currently telling every reader the opposite of the verdict.** This is the single highest-value repair in the sweep. | no |
| **2** | **HIGH** | `docs/47:35`, `docs/47:675` | *"executed under the pre-registration drafted as `docs/46_ls_preregistration_DRAFT.md`, frozen"* (`:35`); cross-ref table row *"`docs/46_ls_preregistration_DRAFT.md` \| the LS pre-registration"* (`:675`) | `docs/46_ls_preregistration.md` | `docs/46:1` — *"# 46 — Resolving the LS **level**: pre-registration — **FROZEN (READ OUT)**"*; `:3` — *"⚠ FROZEN 2026-08-11. §1–§8 ARE IN FORCE. §10 IS THE AMENDMENT SLOT."* The `_DRAFT` file does not exist on disk. | Replace both pointers with `docs/46_ls_preregistration.md` and add *"FROZEN (READ OUT) 2026-08-11; §10 is its amendment slot; `Δ_shape` is recorded in §10 amendment 1"*. `docs/47` is not frozen — correct in place with a dated note. | no |
| **3** | **HIGH** | `docs/47:604-606`, `docs/47:629` | *"**`docs/46` §6.1's `Δ_shape` pre-test.** It is the registered Branch A/B discriminator, it has **not been run** (O6), and it costs minutes."* (`:604-606`); open item **O6** *"`docs/46` §6.1's `Δ_shape` pre-test **has not been run**"* (`:629`) | `docs/53_delta_shape_pretest.md` | `docs/53:1` — *"# 53 — The `Δ_shape` pre-test: **COMPUTED**, and the answer is Branch B"*; `docs/53:19` — *"`Δ_shape` = **0.1299456916752905**"*; `docs/53:24` — *"**VERDICT — `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY**"*; `docs/53:397` — *"`docs/47` **O6** … **CLOSED.** Value 0.1299456916752905; Branch B."* Recorded in `docs/46` §10 amendment 1. | Strike O6, mark **CLOSED 2026-08-11 → `docs/53`**, and strike the §6.3 bullet. Note that the answer removes Branch A entirely, which *strengthens* §5.4. | no |
| **4** | **HIGH** | `docs/47:187-217` (§2.3 D3, headed **BLOCKING**), `docs/47:571` (B3) | *"D3 — the per-node mass audit is blind to NaN and reports PASS on an all-NaN run **BLOCKING (one line)**"*; *"**Fix `src/mgb_transport.py:902`** (`if not (m <= max_resid)`) … `tests/test_transport.py:583` currently passes on an all-NaN run."* | `src/mgb_transport.py` (verified on disk this pass) | `src/mgb_transport.py:908` now reads `if not (m <= max_resid):` with the IEEE-754 rationale at `:902-907`; the NaN regression test is `tests/test_transport.py:246-275`, asserting `math.isnan(res.ledger["max_node_residual_t"])`, plus `:232` `test_a_nan_local_load_is_rejected_at_the_door`. `docs/37:1901` — *"**B3** … the NaN-safe form … The all-NaN run can no longer publish a false PASS."* Commit `a0d8afb` *"fix: the per-reach mass claim no longer survives a non-finite run"*. | Mark D3 **RESOLVED 2026-08-12** and B3 **DISCHARGED**, with the new line numbers (`:908`, test `:274`). Leave the finding's text intact — it is the provenance for the fix. | no |
| **5** | **HIGH** | `docs/47:219-237` (§2.4 D4, headed **BLOCKING**), `docs/47:572` (B4), `docs/47:672` | *"D4 — the `docs/42` §9 transcription is unperformed and C4 has already started"*; *"**Read directly this pass:** `docs/42` §9 still reads `\| Amendments \| none \|` and `\| Registered station sets \| CAL 13 … \|`, and §4.2's power table still prints the CAL-13 `k_min` as **0.0104 /km**"*; B4 *"they are unperformed"* | `docs/42_c4_guards.md` §9 | `docs/42:648` — *"⚠ **THREE, all dated 2026-08-11 — A-P1, A-P2, A-P3, plus A-P1.1 … Plus A-P4, dated 2026-08-12 (§9.7)**"*; `docs/42:660` — *"§9.1 — Amendment log: opened 2026-08-11, and it is late"*; `docs/42:644` — the station-set cell now carries *"the fitting set is **SUPERSEDED by amendment A-P1 (§9.2): it is the CAL 8**"*; `docs/42:901` **F5** — *"**`docs/47` §2.4 D4** (this transcription unperformed) **is discharged** by §9.1–§9.5. **D4 may be CLOSED.**"* | Mark D4 **CLOSED** and B4 **DISCHARGED 2026-08-11/12**, pointing at `docs/42` §9.1–§9.5 and §9.6 F5. | no |
| **6** | **HIGH** | `docs/47:14-36` (THE VERDICT), `docs/47:569` (B1) | *"The condition for unblocking is a single named event: **C3.1 lands**"* (`:34`); B1 *"**Land C3.1** — the LS-formulation decision"* (`:569`) | `docs/37_c3_closure.md` Amendment A3 | `docs/37:1342` — *"**AMENDMENT A3 (2026-08-12) — THE C3.1 ENACTMENT.** The LS *formulation* is DECIDED on source grounds: **ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`. **No engine default moves here. C3 stays OPEN. C4.3 stays BLOCKED.**"*; `docs/37:1893` — *"**B1 lands here, in the reduced form A3.1.6 permits**"*; `docs/37:1884` — the block **holds**, now resting on **B2 alone** (`docs/37:1908-1915`). | Add a dated banner to `docs/47`'s VERDICT box: **"B1 LANDED 2026-08-12 (`docs/37` A3). B3, B4, B5 and the §5.5 disclosure are DISCHARGED. The block now rests on B2 alone — the α box is still denominated at `f_LS` = 1."** Without this the title *"BLOCKED **UNTIL LS LANDS**"* reads as false: the LS **has** landed. | no |
| **7** | **HIGH** | `docs/43:1`, `docs/43:132`, `docs/43:165` | Title *"# 43 — The C3/C4 gate: **C3 STAYS OPEN · C4 PROCEEDS CONDITIONALLY**"*; verdict box *"`C3-STAYS-OPEN-C4-PROCEEDS-CONDITIONALLY`"*; section heading *"### 2.2 Why C4 is not BLOCKED"* followed by *"**No lens supports blocking**"* | `docs/47_c4_entry_verdict.md` | `docs/47:14-16` — *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not start.**"*; `docs/47:612-614` — *"**Not permitted:** any evaluation of `KGE_ln` against the α box; any consumption of the registered 5,482-evaluation budget…"*. `docs/43` itself concedes this at `:47` (*"C4.3 still BLOCKED — `docs/37` is that amendment's owner and its text wins over this pointer"*) — but only inside §1.1, 85 lines above §2's verdict box. | Add a dated pointer under the title **and** immediately under the §2 verdict box and the §2.2 heading: *"⚠ SUPERSEDED IN PART, 2026-08-11: `docs/47` blocks **C4.3** specifically (`C4.3-BLOCKED-UNTIL-LS-LANDS`). §2.2's reasoning applies to C4.1/C4.2, which ran; C4.3 may not."* A reader briefing an advisor from §2 today gets the opposite of the live verdict. | no (§7 is its open amendment slot) |
| **8** | **HIGH** | `docs/37:207`, `docs/37:1790` | `:207` (A3.3.1's **replacement** cell) — *"~~**0.421**~~ → **A3.3.1**: `f_ero` **0.431944** · `f_area` **0.421475** (`V4`, the documented **hybrid**)"*; `:1790` (the supersession table's *registered* column) — *"upper end ×0.421 \| **×0.43194** ero · ×0.421475 area"* | `docs/46` §10 Amendment 2 + `docs/51` §9 amendment 1 | `docs/46:1401` — *"**Amendment 2 — 2026-08-12 — `f_area(V4)` is 0.42136300143291305, not ×0.42148 / 0.421475**"*; `docs/46:1417` — the V4 row's cell *"`f_area` **0.421475**"* → *"**0.42136300143291305**"*. `docs/51:632` — *"`f_area(V4)` \| ×0.42148 / 0.42147514 \| **0.42136300143291305**"*. **Recomputation, §C below: the on-disk value is 0.42136300143291305.** | Replace both with **0.42136300143291305** (or ×0.42136), citing `docs/46` §10 amd 2. **This is the worst instance of the `f_area` defect** because these two cells are the *corrected* values other documents copy from. | no |
| **9** | **HIGH** | `docs/37:1258` (A2.4 item 2) | *"Π (the level) is identifiable with SE = 0.465/√8 = **0.1644 ln = ±38 % at 95 %**"* — printed live, un-struck, no pointer | `docs/42` §9.7 (A-P4) | `docs/42:962` — *"SE of the fleet-mean level, est (b) \| **0.1644 ln** \| **0.6936 ln** \| **×4.22**"*; `docs/42:964` — the band *"±38 % (×0.724 – ×1.380)"* → *"**×0.257 – ×3.894**"*; `docs/42:1037` names this exact site: *"**7 \| `docs/37`:1158 (A2.4) \| SE = `0.465/√8` = 0.1644 ln = ±38 % \| as row 1 — **OWED to `docs/37`'s owner**"* (the line has since drifted to `:1258`). | Strike in place with the `docs/37` A2.7 pattern (nothing deleted) and print the station-bootstrap band `Π̂ × [0.29, 3.73]` (`docs/45` §8 amd 1, `docs/43` §7 amd 1) plus the mandatory sentence *"the level is set by 8 stations whose residuals span a factor of 412"*. | no |
| **10** | MEDIUM | `docs/47:576` (B5), `docs/47:578` (§5.5 disclosure) | B5 *"**Replace the ±38 % Π band** … a `docs/45` §8 amendment"*; *"**Plus the disclosure of §5.5**, as a dated `docs/45` §8 amendment."* — both presented as owed | `docs/45` §8 | `docs/45:644` — *"**THREE, all dated 2026-08-12, all in §8** … **Amendment 1** — the ±38 % Π band **REPLACED** by the station bootstrap, and the `k` bound restated at **≈ 10× over ~342 km** (discharges `docs/47` §6.1 **B5**). **Amendment 2** — the **PRE-FIT DISCLOSURE** … (discharges `docs/47` §5.5)"*. `docs/42` §9.7 (A-P4) and `docs/43` §7 amd 1 enact the same repair in their files. | Mark B5 and the §5.5 disclosure **DISCHARGED 2026-08-12**; note `docs/47` **O9** (the governance question) is still open and explicitly undecided. | no |
| **11** | MEDIUM | `docs/47:590` (§6.2 item 4), `docs/47:262` (§2.6 item 2) | *"no first-order channel sink **stronger** than ~10× over 342 km is **detectable** on this fit set"* | `docs/42` §9.7 / `docs/43` §7 item 7 | `docs/43:631` — *"**the comparative is inverted.** `k_min` is a **detection floor** … with the verb **detectable** the true comparative is **weaker**."*; `docs/42:1007` states the same pairing. Separately, *"this fit set"* is wrong: the ≈10×/342 km figure is the **all-18 G1.2** form; the CAL-8 **fit-set** figure is `k_min` **0.0838 /km ⇒ ≈ 173× over 61.5 km** (`docs/45:137`, §8 amd 1). | Restate as *"no first-order channel sink **weaker** than ≈ 10× over ~342 km is detectable **on the all-18 G1.2 residual test**; on the CAL-8 fit set the floor is ≈ 173× over 61.5 km."* | no |
| **12** | MEDIUM | `docs/43:586` (inside Amendment 3's REGISTERED blockquote) | *"Area-weighted **proxy** [0.24468, **0.42148**], measured **2.51 % low** and never overriding (`docs/46` §3.3)."* | `docs/46` §10 amd 2 / `docs/51` §9 amd 1 | as finding 8. The registered value is **0.42136300143291305**; `docs/51:633` gives the bracket as *"**[0.2446790094097074, 0.42136300143291305]**"*. | Amend the blockquote's proxy to **[0.24468, 0.42136]**. (`docs/43`'s erosion-weighted bracket, which decides, is untouched.) | no (§7 slot) |
| **13** | MEDIUM | `docs/46:105`, `:109`, `:717`, `:1037` | `:105` *"Area-weighted proxy **[0.24468, 0.42148]**"*; `:109` *"upper end … ×0.42148 area"*; `:717` V4 row *"`f_area` **0.421475**"*; `:1037` *"area proxy ×0.24468 – ×0.42148"* — all printed as **live registered text** with no in-place pointer | `docs/46` §10 Amendment 2, in the same file | `docs/46:1415-1418` corrects exactly these four cells to **0.42136300143291305**, and heads the block *"site in §1–§8 (**unchanged there; corrected here**)"* | **The amendment already exists and is correct** — the gap is only that §1.0/§3.1/§6.2 carry no in-place pointer, so a reader who stops before §10 quotes the wrong number. Remedy: apply the `docs/37` **A2.7 / `docs/42` §9.7.7** precedent — strike-through + dated pointer **in place**, nothing deleted, **under Amendment 2's authority**. **Never rewrite the registered text.** | **YES — `docs/46` is FROZEN; only §10 may authorise the annotation** |
| **14** | MEDIUM | `docs/45:40`, `docs/45:643` | *"The `docs/42` §9 transcription **remains owed**."* (both sites) | `docs/42` §9 | as finding 5 — `docs/42:648`, `:660`, `:901` (F5: *"D4 may be **CLOSED**"*) | A `docs/45` §8 **Amendment 4**: *"the `docs/42` §9 transcription landed 2026-08-11/12 as A-P1, A-P2, A-P3, A-P1.1 and A-P4."* | **YES — amendment only** |
| **15** | MEDIUM | `docs/42:15`, `docs/42:330`, `docs/42:516` | `:15` — *"a fit that silently omits channel deposition now lands **α at 6.83 – 8.73**, inside the registered 'expected' band of 5.9 – 23.6 … **C4 must not run until a test that can catch it is registered. This is that test set.**"* (the document's founding rationale) | `docs/47` §2.5 **C1**; enacted in `docs/43` §7 amd 5 | `docs/47:246` — *"6.83–8.73 is `11.8 × {144,184} / 248.730` (**prior C**) … At the adopted C the deposition-free band is **5.67 – 7.25**, which is **disjoint** from 7.92–8.86 (gap 0.67)."*; `docs/43:652` — *"deposition-free fit, `11.8 × 144 / total` \| 6.8315 \| **5.6727**"*. `docs/42:1107` **F7** already registers `:15`, `:299`, `:472` as **OWED as a further `docs/42` amendment** — *"NOT corrected here"*. | The owed `docs/42` §9 amendment: strike in place and print **5.67 – 7.25 at the adopted C** beside the prior-C figure, with the convention and `cp_revision` named (`docs/37`'s own rule). Note `docs/47`'s line refs `:299`/`:472` have drifted; the live sites today are **`:15`, `:330`, `:516`**. | **YES — `docs/42` §9 slot** |
| **16** | MEDIUM | `docs/45:452` | *"a fit which **silently omits channel deposition lands α at 6.83–8.73, INSIDE `docs/35` §6.1's** …"* | as finding 15 | as finding 15 | A `docs/45` §8 amendment carrying the adopted-C band **5.67 – 7.25** and the disjointness. `docs/47` **O12** (whether disjointness changes the *"doubly load-bearing"* G5 conclusion) stays open. | **YES — amendment only** |
| **17** | MEDIUM | `docs/35:652` | *"an α fitted to make **gross** erosion equal the outlet load … lands at **α = 6.83 – 8.73**, comfortably *inside* the expected band"* | as finding 15 | as finding 15 | A `docs/35` §9 amendment (§9.5) re-basing this to the adopted C: **5.67 – 7.25**, disjoint from the reading-B 7.92–8.86. The §9.4 amendment already re-based `docs/35`'s *loads*; this α band was missed. | **YES — `docs/35` §9 slot** |
| **18** | MEDIUM | `docs/37:1006`, `docs/37:1263` | `:1006` — *"lands α at **6.83 – 8.73**. **These overlap.** So a fit …"*; `:1263` — *"the deposition-free α band (**6.83 – 8.73**) overlaps the reading-B α (**7.92 – 8.86**)"* | as finding 15 | as finding 15. **`docs/37` corrects this in one place and not the other**: `:355-359` carries *"→ **A3.3.1**: as arithmetic … `docs/47` §2.5 C1 records: 6.83 – 8.73 is `11.8 × {144,184} / 248.730`, i.e. at the PRIOR `C`; at the adopted `C` the deposition-free band is 5.67 – 7.25"*, while §A2 at `:1006`/`:1263` does not. | Apply the same A2.7 strike + pointer at `:1006` and `:1263`. | no |
| **19** | MEDIUM | `docs/40:116-117` | *"reading the α that reproduces Tan's converted level is **7.92 – 8.86**, which **overlaps** G5's deposition-free fit band of **6.83 – 8.73** — so a fit that 'works' under the yield reading is …"* (and the appendix at `:716`) | as finding 15 | as finding 15 — at the adopted C the bands are **disjoint**, gap 0.67 in α | Strike + pointer to `docs/43` §7 amd 5. The *caution* survives (safe direction); the *reasoning* does not. | no |
| **20** | MEDIUM | `docs/40:148`, `:152`, `:192`, `:356`, `:383`, `:393`, `:434`, `:681-691` | *"gross **hillslope** erosion, MUSLE, basin decade 2009–2018 \| **248.730 Mt/yr**"* and every ratio built on it (*"144/248.730 = 0.5789 · 184/248.730 = 0.7397"*, *"÷ our gross hillslope erosion 248.730 \| **0.7237** \| **1.0614**"*) printed as the live denominator | `docs/37` A1.3.4 | `docs/37:847` — *"**The 248.730 Mt/yr headline is superseded by 299.539 Mt/yr** wherever it is quoted"*; `docs/41:418` repeats it. `docs/00_INDEX:153` — *"The level is **299.539 Mt/yr** … which supersedes the 248.730 Mt/yr quoted in docs/35, 36, 37 §2–§3, **40** and 42"*. | `docs/40` is **partially** back-annotated already (`:130` and the appendix `:698-714` give the adopted-C figures), so the remedy is a per-site pointer, not a rewrite: add *"prior `cp_revision`; at the adopted C the level is 299.5387088405831 Mt/yr"* beside each. `docs/37`'s standing rule — *"never quote a load without its convention **and** its `cp_revision`"* — is what these sites break. | no |
| **21** | MEDIUM | `docs/39:192` | Table row marked **✔ verified**: *"ours area-wtd **39.812** vs source-faithful **16.775** = **×0.421** (×0.333 with the Desmet–Govers `L`) ⇒ our LS is **2.37×–3.00×** high … it takes 248.730 → 104.8/82.8 Mt/yr, implied SDR 1.37–2.22"* | `docs/47` §4.3 (measurement) + `docs/51` §2 | `docs/47:292` **R6** — *"×0.333 … **REFUTED by two independent agents**"*; `docs/47:396` — *"**`f_LS` ∈ [0.25146, 0.43194] erosion-weighted — our LS is 2.315× – 3.977× the source level**"*; `docs/51:22` — *"This **supersedes ×0.333 – ×0.421 and \"2.37× – 3.00×\"**"*. The *"implied SDR 1.37–2.22"* reading is retired outright (`docs/40`, `docs/37` A1.2). | `docs/39` is a dated audit (2026-08-11) but carries no supersession note and marks this row **✔**. Add a dated strike + pointer, or a header banner: *"§1.9's LS row is SUPERSEDED — see `docs/47` §4.3 and `docs/51` §2."* | no |
| **22** | MEDIUM | `src/mgb_sediment.py:223` | *"[0.25146, 0.43194] EROSION-weighted (area-weighted proxy **[0.24468, 0.42148]**, measured 2.5% low)"* | `docs/46` §10 amd 2 / `docs/51` §9 amd 1 | as finding 8: **0.42136300143291305** | Change to **[0.24468, 0.42136]**. The erosion-weighted bracket beside it is correct and must not move. | no |
| **23** | MEDIUM | `src/mgb_sediment.py:268` | *"note the yield-reading ``alpha`` of 7.92-8.86 overlaps G5's deposition-free 6.83-8.73"* | as finding 15 | as finding 15 | Restate at the adopted C: *"…the yield-reading alpha of 7.92-8.86 is **disjoint** from G5's deposition-free 5.67-7.25 at the adopted cp_revision (6.83-8.73 was the prior C); docs/47 §2.5 C1, docs/43 §7 amd 5, docs/47 O12 open."* | no |
| **24** | MEDIUM | `src/nbgen/make_nb18.py:1244`, `:1269`, `:1353` | `:1244` V4 row *"\| **0.431944** \| **0.421475** \|"*; `:1269` *"$0.3513\times0.505092\times1.7139 = 0.304112$ vs **0.421475**, **x1.38592**"*; `:1353` `F_HYB_ERO,  F_HYB_AREA = 0.431944, **0.421475**` | `docs/46` §10 amd 2 | as finding 8: **0.42136300143291305** | Set `F_HYB_AREA = 0.42136300143291305` and re-derive the `x1.38592` area-weighted ratio from it (the erosion-weighted `x1.34762` is unaffected), then regenerate and re-execute nb18. **Note:** the *same table* at `:1245` already prints the DG endpoint at full precision (`0.2446790094097074`), so the file is internally inconsistent. | no |
| **25** | MEDIUM | `src/nbgen/make_nb19.py:2435` | `F_HYB_E,  F_HYB_A  = 0.431944, **0.421475**    # V4     his 3 levers + OUR L  -> documented HYBRID` | `docs/46` §10 amd 2 | as finding 8 | as finding 24, then regenerate and re-execute nb19. | no |
| **26** | MEDIUM | `src/nbgen/make_nb19.py:1528`, `:1537`, `:1581`, `:1639` | `:1528` table row *"a fit that **silently omits channel deposition** lands at \| **6.83 - 8.73** \| `docs/35` section 9.2"*; `:1581` `shows=` prose *"**6.83-8.73 and 7.92-8.86 overlap**, and both lie inside 5.9-23.6"*; `:1639` a plotted `axhspan` labelled *"deposition-free fit 6.83-8.73"* | as finding 15 | as finding 15 — at the adopted C the two bands are **disjoint** | Re-base `DEPFREE` to (5.6727, 7.2483), restate the `shows=` sentence as *"they are **disjoint** at the adopted C (they overlapped at the prior C, which is where 6.83-8.73 comes from)"*, and re-label the plotted band. **This renders into a published notebook figure**, so it is the most visible surviving copy of C1. `make_nb18.py:2771` already prints both (*"6.83-8.73 (prior C) or 5.67-7.25"*) — nb19 did not get the same treatment. | no |
| **27** | MEDIUM | `docs/47:116` | *"Crediting C4 with the largest re-partition this project has measured — the LS level, `docs/37` §4 candidate 0 at its **registered** ×2.37–3.00 — lifts implied α only to **2.87 – 3.63**"* | `docs/47` §4.3, in the same document | `docs/47:396` registers *"**`f_LS` ∈ [0.25146, 0.43194]** … 2.315× – 3.977×"* and explicitly supersedes ×0.333 – ×0.421 as a measurement 280 lines later. §2.1's arithmetic is therefore run on the bracket its own §4.3 retires. | Re-derive at 2.3151× – 3.9768× (which *strengthens* the finding — the upper end rises) or mark the passage *"as the defence was mounted, on the then-registered bracket; superseded by §4.3"*. | no |
| **28** | MEDIUM | `docs/47:624` (O1), `docs/47:362-367` (§4.2 items 4–5), `docs/47:406-412` (§4.3 caveat) | O1 *"**Whether the LS levers can be settled from the literature at all.**"*; §4.3 *"**A different reading of p. 94 moves both rows.**"* | `docs/51` §1; `docs/46` §1.0/§2.5 | `docs/51:57` — *"**The PDF is obtainable, it was obtained, and it is on disk**"* (sha256 `3047624f…c0037`, 182 pp., `lume.ufrgs.br` handle `10183/129875`); `docs/51:73` — *"**(R6) — RESOLVED. `Sf` is slope PERCENT**"*; `docs/51:26` — *"with Buarque eq. 13 now read verbatim (§1), the source formulation read whole is a **POINT at ×0.25146**"*; `docs/46:119` — *"Every lever is **CITED** … there is no admissible reading in which `L` is our point-rate form."* | Narrow O1 to what is still true: **Desmet & Govers (1996)** and **Fagundes et al. (2026)** remain unobtained; **Buarque (2015) is obtained and all four levers are CITED**, and §4.3's *"a different reading of p. 94 moves both rows"* is **withdrawn** — the interval is an `L`-form lever, not a reading ambiguity. | no |
| **29** | MEDIUM | `docs/47:630` (O7) | *"**The 7 % method difference between the two `k_min` computations** — `docs/42` prints 0.0104 /km, the lens computed 0.0096 /km …"* | `docs/42` §9.5 (A-P1.1) | `docs/42:778` — *"AMENDMENT A-P1.1 · 2026-08-11 · §4.2's power table, corrected — and the **0.0096-vs-0.0104 discrepancy resolved**"*; `docs/42:803` — *"**CAL 13** \| 13 \| **0.009640** \| §4.2 prints 0.0104 \| — **does not reproduce**"*; `docs/43:688` — *"`docs/47` open item **O7** is thereby **CLOSED**"* | Mark O7 **CLOSED** → `docs/42` §9.5, `docs/43` §7 amd 6. | no |
| **30** | MEDIUM | `docs/43:41`, `docs/43:139` | `:41` — *"The pre-registered C3.1 comparison (`docs/35` §9.3) **has not been made**."* (un-struck); `:139` clause-2 cell — *"C3.1 (`docs/35` §9.3) **unmade**"* | `docs/37` A3 | `docs/37:1342` — ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`, 2026-08-12 | `:41` is immediately followed by an Amendment-3 note that says *"The C3.1 comparison **has since been made**"*, so it is half-repaired — strike the sentence itself. `:139` has **no** annotation and should get the same one as §2.1's SHAPE row (`:151`), which does carry it. | no (§7 slot) |
| **31** | MEDIUM | `docs/48:9`, `docs/48:587` | `:9` — *"They are frozen; **B5 is owed to them** as a `docs/45` §8 amendment, enacted by that document's owner."*; `:587` — cross-ref row *"`docs/46_ls_preregistration_DRAFT.md`"* | `docs/45` §8 amd 1; `docs/46` | as findings 10 and 2 | Add a dated closing note: *"B5 was enacted 2026-08-12 — `docs/45` §8 amd 1, `docs/42` §9.7 A-P4, `docs/43` §7 amd 1."* Fix the `_DRAFT` pointer. | no |
| **32** | LOW | `docs/49:5`, `:345`; `docs/50:5`, `:337`; `docs/52:6`, `:491` | *"`docs/46_ls_preregistration_DRAFT.md`"* (all six); `docs/50:337` explicitly — *"`docs/46` **is a DRAFT** and is the file that inherits these."* | `docs/46_ls_preregistration.md` | `docs/46:1`/`:3` — **FROZEN (READ OUT) 2026-08-11**; §10 is the amendment slot | These three were written **before** the freeze and are correct for their date, but nothing marks that. Add a one-line dated header note to each: *"`docs/46` was frozen 2026-08-11 as `docs/46_ls_preregistration.md`; the `_DRAFT` filename in this document is historical."* | no |
| **33** | LOW | `docs/37:1908-1915` (A3.4 item 2) | Heading *"**B2, B5 and the §5.5 disclosure have NOT landed**"*; body *"**Measured on disk in this pass:** `docs/45` §8 at :610–612 still reads ***'Empty at registration'***"* | `docs/45` §8 | `docs/45:644` — three amendments, all 2026-08-12 (B5 and the §5.5 disclosure discharged). **B2 alone is still owed** — `docs/45:101-108` confirms *"**The α box [2.0, 30.0] is NOT amended here** — re-expressing the gate is `docs/47` B2 and belongs to its owner."* | **Self-protecting and therefore near-harmless** — `docs/37:1917-1919` says *"Their landing is stated here as a CONDITION and is NOT claimed as a fact. A later reader must check `docs/45` §8 and `docs/35` §9 themselves."* Recommended: narrow the heading to *"**B2 has NOT landed**"*. | no |
| **34** | LOW | `docs/47:391` | §4.3 table, *source method, continuous L* row: area-weighted × = **0.42135** | `docs/46` §3.1 as amended | **0.42136300143291305** (§C below) | Print at the registered precision. A 1-in-the-last-digit truncation, not a different measurement — but it is a third distinct spelling of the same quantity in the corpus. | no |
| **35** | LOW | `docs/47:246` (C1's site list) | *"Propagated verbatim into **`docs/42:15, :299, :472`** and **`docs/45:404`**."* | the files themselves | Read this pass: `docs/42:299` is a C-class erosion-share table row and `:472` is G3.3's opening — **neither carries the band**; the live sites are `docs/42:15`, `:330`, `:516`. `docs/45:404` is inside §3.5's ONI clause; the live site is `docs/45:452`. Line numbers drifted when `docs/42` §9 and `docs/45` §8 were added. | Re-anchor the list, or quote the sentence instead of the line number. | no |
| **36** | LOW | `docs/47:332` | *"(Code defect found alongside: the `ls2d.py` docstring claims m 'runs … to ~0.5 on steep Andean slopes'; **measured median 0.5844, p90 0.7028, max 0.7501**.)"* | `scripts/c3/ls2d.py` | **Not verified this pass** — `scripts/c3/ls2d.py` is outside the assigned sweep scope. Flagged so it is not assumed fixed. | Someone with `scripts/c3/` in scope should confirm whether the docstring was corrected. | no |

---

## B — THE TWO CONFIRMED DEFECTS: exact residual state, site by site

### B.1 — `min(m, 0.5)` mislabelled *"Buarque eq. 14"*

**Owning rule:** `docs/46:512` — *"The **cap** — `min(m, 0.5)` — may **never** be graded CITED"*;
`docs/46:434` — *"Buarque's eq. 14 is the **step function** 0.2 / 0.3 / 0.4 / 0.5 on `Sf` < 1 / 1–3 /
3–5 / ≥ 5 **percent**"*; the units verified first-party at `docs/51:73` (*"onde `Sf` [%] é a
declividade do pixel"*, printed p. 47, corroborated p. 48).
**Owning measurement:** `docs/49:92` — step (**V2b**) ×0.505092 area / **×0.522043** erosion; cap
(**V2a**) ×0.502472 area / **×0.517480** erosion.

| the five named sites | state | evidence |
|---|---|---|
| **`docs/35` §9.3.1** — `:733` | **FIXED** | *"~~eq. 14, step function capped at **0.5**~~ **MISLABEL — STRUCK 2026-08-12, §9.4.1.**"* + the full §9.4.1 amendment at `:925`, `:944-966`, incl. the first-party p. 47 re-extraction at `:1224`. Struck, not deleted, with both objects named and both factors printed. |
| **`docs/37` §4 candidate 0** — `:205`, `:210`, `:225-230` | **FIXED** | `:205` *"~~his eq. 14, step function **hard-capped at 0.5**~~ → **A3.3.2**"*; the A3.3.2 block at `:1853-1869` names both objects and both factors. |
| **`docs/43` §1.4** — `:89-101` | **FIXED** | `:89` *"~~`m` cap ×0.502~~"* struck in place; Amendment 2 at `:524-555` gives *"**Buarque eq. 14 is a STEP FUNCTION** on slope **percent**, worth **×0.505092** area-weighted / **×0.522043** erosion-weighted"* and the never-CITED clause. |
| **`src/nbgen/make_nb18.py`** — `:1241`, `:1248-1262`, `:1352`, `:1371` | **FIXED** | `:1241` now reads *"**his eq. 14, printed p. 47: a STEP FUNCTION** … with $S_f$ in slope **percent** \| **0.522043** \| 0.505092"*; `:1248` carries a full *"A LABEL CORRECTION, and it is unconditional"* blockquote; `:1352` `M_CAP_ERO, M_CAP_AREA = 0.517480, 0.502472   # min(m, 0.5): the CAP.  NOBODY'S published form.`; `:1371` prints *"m as min(m,0.5) - the CAP, NOT eq. 14, nobody published it"*. |
| **`src/nbgen/make_nb19.py`** — `:2400`, `:2432-2433`, `:2447`, `:2454` | **FIXED** | `:2400` *"conflating two different objects. **Buarque's eq. 14 (printed p. 47) IS a step**"*; `:2432` `F_STEP_E, F_STEP_A = 0.522043, 0.505092    # V2b  eq. 14, the STEP function, Sf in slope PERCENT`; `:2433` the cap kept separate and labelled *"NOBODY'S published form"*; `:2454` prints the distinction. |

> **VERDICT: all five sites are FIXED. Zero live-stale instances remain.** `min(m, 0.5)` is nowhere
> graded CITED, and every surviving mention of ×0.502 in the corpus is either struck, labelled *the
> CAP*, or inside a supersession table. **This defect is closed and should not be re-litigated.**
>
> One residual note, not a mislabel: `docs/37:1533` and `docs/46:178` still contain the string
> *"`m` stepped and capped at 0.5 (his eq. 14)"* — both are **verbatim quotations of the superseded
> source text** inside their own correction blocks (`docs/37:1558` immediately says it *"conflates
> **two different objects**"*). Correctly handled; not findings.

### B.2 — `f_area(V4)`: `0.42136300143291305` vs `0.42147514`

**Owning amendments:** `docs/46` §10 **Amendment 2** (`:1401-1418`) and `docs/51` §9 **amendment 1**
(`:632-633`, `:664`). Both register **0.42136300143291305** as correct.
**Recomputed from disk this pass — see §C.** `docs/46:1467` and `docs/51:582` both stress that
0.42147514 *"is NOT an arithmetic error"* — it is the same quantity on the **wrong area support**
(`urh_fractions.csv` × `minibacias.csv`, 32,782 units, 257,096.93 km²), a legitimate number that is
simply not `f_area` as `docs/46` §3.3 defines it.

**Every remaining LIVE print of the superseded value, outside a supersession table:**

| # | site | printed as | ledger row |
|---|---|---|---|
| 1 | **`docs/37:207`** — A3.3.1's *replacement* cell | `f_area` **0.421475** | 8 (HIGH) |
| 2 | **`docs/37:1790`** — A3.3.1 supersession table, *registered* column | ×0.421475 area | 8 (HIGH) |
| 3 | **`docs/43:586`** — Amendment 3's REGISTERED blockquote | [0.24468, **0.42148**] | 12 |
| 4 | **`docs/46:105`** — §1.0 registered statement | [0.24468, **0.42148**] | 13 (frozen) |
| 5 | **`docs/46:109`** — §1.0 table, upper-end row | ×**0.42148** area | 13 (frozen) |
| 6 | **`docs/46:717`** — §3.1 V4 row | `f_area` **0.421475** | 13 (frozen) |
| 7 | **`docs/46:1037`** — §6.2 A2 run-card clause | area proxy ×0.24468 – ×**0.42148** | 13 (frozen) |
| 8 | **`src/mgb_sediment.py:223`** | [0.24468, **0.42148**] | 22 |
| 9 | **`src/nbgen/make_nb18.py:1244`** | **0.421475** | 24 |
| 10 | **`src/nbgen/make_nb18.py:1269`** | vs **0.421475**, x1.38592 | 24 |
| 11 | **`src/nbgen/make_nb18.py:1353`** | `F_HYB_AREA = 0.421475` | 24 |
| 12 | **`src/nbgen/make_nb19.py:2435`** | `F_HYB_A = 0.421475` | 25 |
| 13 | **`docs/47:391`** (variant spelling) | 0.42135 — a truncation, 1 ulp of print from correct | 34 (LOW) |

**Checked and NOT stale (do not re-open):**

- **`docs/47:338`** — *"joint **16.7754 / ×0.4214**"*. `16.7754 / 39.8123 = 0.4213617`, which rounds
  to **0.4214** — this is the **corrected** value at 4 d.p., not the superseded one (0.42147514
  rounds to 0.4215). Correct as printed.
- **`docs/50:299`** — *"**×0.4214** / ×0.43194"*. Same: correct at 4 d.p.
- **`docs/51:19`, `:135`, `:141`, `:167`** — all four struck in place with pointers to §9 amendment 1.
- **`docs/51:548-664`** and **`docs/46:1401-1490`** — the defect analyses themselves.
- **`docs/53:359-366`** — §7 *"Incidental, flagged not fixed"* explicitly reports the inconsistency
  and names the owner. Correctly handled.
- **`docs/45`, `docs/48`, `docs/49`, `docs/52`** — no live print of the superseded value found.
  `docs/49:121` already prints the **corrected** `f_area(V4)` = **0.421363**.

---

## C — RECOMPUTATION (measure before asserting)

Run read-only against `data/processed/`:

```
python3.10 -c "import json; ..."   # walk the three LS JSON artifacts

ls2d_variants_summary.json  variants.V4_buarque_2015.ratio_to_V0        = 0.42136300143291305
ls2d_defect_b.json          decomposition.V4_over_V0                    = 0.42136300143291344
ls_defect_a.json            variants.V4_buarque_2015.f_area_urhfrac_areas = 0.4214751420286394
ls_defect_a.json            variants.V4_buarque_2015.f_ero              = 0.43194417543884817
```

**Conclusion.** Two different area supports, two different numbers, both correctly computed. The
one `docs/46` §3.3 defines as `f_area` is the LS2D grid's own support ⇒
**`f_area(V4) = 0.42136300143291305`**. `0.4214751420286394` is the `urh_fractions × minibacias`
support, which `docs/51:589` shows differs because *"basin totals 257097 vs 251724 km²"*. The
erosion-weighted `f_ero(V4) = 0.43194417543884817` — the number that **decides** — is unaffected,
so **no registered bracket, no α reference, no hard stop and no basin load moves.** This matches
`docs/46:1430-1437` exactly.

Also verified on disk: `src/mgb_transport.py:908` = `if not (m <= max_resid):` (finding 4);
`tests/test_transport.py:246,274` = the NaN regression test; `docs/42:648`,`:660` = the §9
amendment log exists (finding 5); `docs/45:644` = three §8 amendments exist (finding 10).

---

## D — CHECKED AND **NOT** STALE (so nobody re-litigates these)

Repaired by a prior session, or correctly marked as historical. **None of these is a finding.**

1. **The eq.-14 mislabel — all five named sites.** See §B.1. Closed.
2. **`docs/35` §9.4** (`:480`, `:733`, `:744-745`, `:776-781`, `:816-830`, `:925-966`, `:1025`,
   `:1102`) — the mislabel, the superseded bracket and the 248.730-based loads are all struck in
   place with the re-derived values beside them, under the frozen doc's own §9 slot. Exemplary.
3. **`docs/37` A3.3.1 / A3.3.2** (`:1783-1830`) — the twelve-site enactment of the bracket
   supersession, including the honest note that *"three further live sites were found by grep in
   this pass … a reader auditing whether the enactment travelled needs to know the list was not
   complete on the first attempt."*
4. **The ±38 % / σ_r = 0.465 / 0.1644 ln defect** — enacted in `docs/42` §9.7 (A-P4), `docs/43` §7
   amd 1 + amd 4, `docs/45` §8 amd 1. `docs/42:940-948` correctly preserves what **survives**
   (σ_r as an estimator-disagreement statistic; G8's and G11's 0.465 firing thresholds; the
   `b_obs` IQR 0.464; SE(β) = 0.0199). Only `docs/37:1258` was missed (finding 9).
5. **CAL 13 → CAL 8** — correctly scoped everywhere checked: `docs/42:644` strikes it **for fitting
   only** and states *"The all-18 clause and the never-fit rule are **unchanged**"*. No document was
   found invoking CAL 13 for the all-18 clause. `docs/46:538`, `docs/47:429-431`, `docs/52:370`,
   `docs/53:108,228` use "CAL 13" for the **C1-usable tributary set**, a different object —
   `docs/53:368` already flags the naming collision. Not stale.
6. **`docs/47`'s BLOCKED verdict itself.** Confirmed still current by every downstream owner:
   `docs/37:1884` (*"Is C4.3 thereby UNBLOCKED? **NO**"*), `docs/45:1064`, `docs/46:1318`,
   `docs/51:49` (*"the BLOCKED verdict HOLDS, and is strengthened, not weakened"*), `docs/52:403`,
   `docs/53:342`. Only `progress_map.html` disagrees (finding 1).
7. **`docs/47` O12** (whether the disjoint bands change the G5 conclusion) — genuinely still open;
   `docs/43:735` carries it forward by name. Not stale.
8. **`docs/47` O8** (class-C detectability) — genuinely still open, and correctly refuses to offer a
   fourth number: `docs/43:630`, `docs/42:1047`, `docs/45:483`.
9. **`docs/47` O10 / §2.5 C5** (*"`docs/41` remains unaudited"*) — still true. No `docs/41` audit
   exists in `docs/agents/`; `docs/43:142` and `docs/37:1194` agree.
10. **`docs/45` §2.1's α box** — correctly **not** amended: `docs/45:106` states *"**The α box
    [2.0, 30.0] is NOT amended here** — re-expressing the gate is `docs/47` B2 and belongs to its
    owner."* B2 is genuinely outstanding; this is the one live leg of the block.
11. **`docs/42` §9.7 F7** — the 6.83–8.73 defect is *registered as owed* rather than silently
    carried, with an explicit refusal to smuggle an unrelated enactment into A-P4's slot. Correct
    process; the body sites remain (finding 15).
12. **`docs/32`, `docs/34`, `docs/38`** — clean. Pre-registrations and a transcription, each with an
    accurate status header and no forward reference that has since resolved.
13. **`docs/36`** — clean; its numbering note (33 §5.2's reservation of 36) is correctly resolved in
    place, and it decides nothing it does not own.
14. **`docs/33`** — clean; frozen 2026-08-10 with results appended, and its §5.2 number reservation
    is annotated by `docs/00_INDEX:111`.
15. **`src/mgb_sediment.py`'s docstring** — substantially current: it carries A3, the corrected
    bracket, the POINT/HYBRID distinction, the eq.-14 correction, the SDR retirement and the
    withdrawn direction. Only two lines are stale (findings 22, 23).
16. **`src/nbgen/make_nb18.py:2966`** — the *"what we got wrong"* table correctly states **both**
    the bracket and the eq.-14 errors and their corrections. Model back-annotation.
17. **`docs/53:359-372`** §7 — flags the `f_area` inconsistency and the CAL-13 naming collision
    rather than fixing them out of scope. Correctly handled.

---

## E — OWNER UNCLEAR

1. **`progress_map.html`.** RULE 0 makes it the authority for *status*, but no numbered document
   owns it and this run's scope note assigns it to no agent (A4 = docs/00–31, A5 = docs/32–53,
   A6 = the two confirmed defects). It is the **most stale artifact found** (finding 1) and it is
   the one a newcomer is told to open fifth (`docs/00_INDEX:46`). **Needs an explicit owner.**
2. **The 6.83 – 8.73 → 5.67 – 7.25 correction (`docs/47` §2.5 C1).** Enacted only in `docs/43`
   (§7 amd 5). `docs/47:246` says *"Correct in place at C5 **or** at the next `docs/42` amendment"*,
   and `docs/42:1107` F7 declines it as belonging to *"a different repair"*. So five files
   (`docs/35`, `docs/37`, `docs/40`, `docs/42`, `docs/45`, plus `src/mgb_sediment.py` and
   `make_nb19.py`) carry it with **no named owner and no deadline**. Two of the seven are frozen.
   **Recommend: name one owner and one dated pass, since three of the sites are frozen and need
   coordinated amendments.**
3. **`docs/39_contradiction_audit.md`'s status.** It is a dated read-only audit whose §1 tables are
   quoted as verified facts, but it carries no `STATUS: HISTORICAL` header and is absent from
   `docs/00_INDEX` §3's status table (which stops at 42). Finding 21 assumes it should be
   back-annotated; if the house convention is that audits freeze at their date, a header note
   saying so would settle it.
4. **`docs/00_INDEX` §3's Phase-C table stops at `docs/42`.** Documents **43, 45–53** have no status
   row and no owner assignment. Out of my scope (A4 owns the index) but flagged: the index cannot
   discharge RULE 0 for eleven of the corpus's most decision-bearing files. Note also that
   `docs/44` does not exist and nothing records why the number was skipped.
5. **`scripts/c3/ls2d.py`'s docstring** (finding 36) — outside every named sweep scope.

---

## F — DISCLOSURE

- **Files written by this pass:** `docs/agents/journal_sweep-phasec.md` (this file). **Nothing else.**
- Everything in `docs/32`–`docs/53`, `src/mgb_sediment.py`, `src/nbgen/make_nb18.py`,
  `src/nbgen/make_nb19.py` was **read and not edited**. `src/mgb_transport.py`,
  `tests/test_transport.py` and `progress_map.html` were read as evidence.
- **Two numbers were recomputed** rather than adjudicated (§C), from
  `data/processed/{ls2d_variants_summary,ls2d_defect_b,ls_defect_a}.json`, read-only. No artifact
  was written. No calibration or simulation was run. No git command was run.
- **No finding below HIGH was promoted** to make the list look decisive, and **17 checks that came
  back clean are recorded in §D** so a later session does not re-litigate them. Where a claim could
  not be verified inside my scope it says so (findings 36, §E.5) rather than assuming.

# Handoff — drafted fixes for the four surviving T6 findings

**Written 2026-08-12 by the orchestrating/thinking session. PROPOSED text only — NOT APPLIED.**
Each is a wording / dangling-reference / label fix; **none touches a canonical result number**
(299.5387 / 248.7298 stand). Apply each through its **owning doc's amendment slot**, respecting
one-agent-per-file. All four **survived their first refutation** (`refute-t6-1/4/6/2`); findings 2
and 3 are stated here in the **corrected** form the refuter returned, not the original. Verify each
locator on disk before editing — line numbers drift.

Standing rule this obeys: *enactment is a written amendment; an uncited band cannot pass or fail a
gate; verify from executed output.* Nothing here moves an engine default or opens a frozen artifact.

---

## Fix 1 — `docs/37`:241 — "exercised" overclaim (finding `refute-t6-1`, HIGH)

**Confirmed:** `docs/37` uses "exercised" for ADOPT-SOURCE at a live site, while `docs/46` §4.2
note 3 reserves *"exercised"* for the step gated on §3.3's full stratified report, and `docs/37`'s
own A3.1 status row says **"DETERMINED and RECORDED — not yet EXERCISABLE."** The refuter found the
**one substantive site is `:241`** — `:1394` and `:1423` use the verb in a defensible,
supersession-context sense, and `src/mgb_sediment.py:242` is mitigated two lines later, so **leave
those three**.

**Owner/slot:** `docs/37` (append-only via its amendment convention; the A3 author owns this line).

**Proposed edit:** at `:241`, replace the "exercised" phrasing with the A3.1 status-row language,
e.g. — *"ADOPT-SOURCE is **determined and recorded, not yet exercisable** (`docs/46` §4.2 note 3:
'exercised' is reserved for the §3.3-gated step; the stratified report is owed) — see A3.1.6."*
Add a one-line supersession note; do not silently overwrite.

---

## Fix 2 — `docs/51` §3/§4 (+ `:31`, `:258`, `:330`) — struck-bar verdict still live (finding `refute-t6-4`, HIGH)

**Confirmed:** `docs/51` §3/§4 verdict tables (and the FOUR-ANSWERS box `:31`, plus `:258`/`:330`)
print *"(R4) FIRES ⇒ field clause REFUTED"* in a **`bar` column at 0.1644** — the bar **struck** by
`docs/52` — with **no pointer to `docs/52`** at those sites, in a document the INDEX advertises as
executable. `docs/52` §8(d) says that verdict label is **owed to `docs/51`'s owner**.

**Owner/slot:** `docs/51` amendment slot (its owner). **Drop the "fourth retired band" wording**
that the finding originally carried — the refuter flagged that consequence as the overclaim.

**Proposed edit:** at each of the four locators, annotate the 0.1644 `bar` cell / verdict:
*"⚠ bar 0.1644 STRUCK by `docs/52`; this verdict was reached through a retired instrument — label
re-adjudication owed to this document's owner per `docs/52` §8(d). Not a live pass/fail."* Do **not**
delete the historical row; mark it superseded. **Do not** describe it as "a fourth retired band."

---

## Fix 3 — `docs/37` A3.1.3 `:1570–1573` — fallback-branch conflation + factor (finding `refute-t6-6`, HIGH)

**Confirmed, in corrected form.** The "THE HONEST LIMIT OF THIS ADJUDICATION" blockquote names the
fallback branch as *"NEGATIVE — UNRESOLVED on a documentary ground" with **V0 retained**,* which:
(i) extends a frozen row's entry conditions from another file; (ii) contradicts `docs/35` §9.4.3 and
`docs/37`'s own `:1536–1538`; (iii) is the **engine-state/outcome conflation** the A3.1.1 RETAIN-OURS
row (`:1422`) expressly rejects. **Refuter corrections to apply verbatim:**
- the fallback-vs-fallback gap is **×2.3151**, not ×1.7177;
- the locator **must include A3.7's `docs/35` row (a)**;
- the "V0 + bracket" pairing is **`docs/46`'s wording** — attribute it there.

**Owner/slot:** `docs/37` A3 author.

**Proposed edit:** correct the factor to **×2.3151**; strike the *"V0 retained"* engine-state phrasing
(it conflates outcome with default, which `:1422` forbids); add the `docs/35` row (a) + A3.7 locator;
attribute the V0+bracket pairing to `docs/46`. Keep the section's honest-limit intent; fix only the
mislabelled branch and the number.

---

## Fix 4 — `src/nbgen/make_nb19.py` + `notebooks/19_*.ipynb` — struck band still live (finding `refute-t6-2`, CRITICAL)

**Confirmed:** the retired **±38 % / 0.1644 ln** band is **alive in `make_nb19.py`** and in the
**executed** `notebooks/19_c3_gate_and_c4_setup.ipynb`, where it **passes an integrity assertion**;
`σ_r = 0.465` is still labelled a *per-station residual floor*. This is a dangling reference to a
struck number presented as current — the exact T6 lens.

**Do NOT fix by editing the generator in this track.** Per the refuter and the `docs/43` §7/§8 amd
precedent: **register `make_nb19.py` + nb19 as an OWED SITE** in an amendment now (this documentation
track), and **hand the regeneration to the notebook track** (editing the generator + re-executing is
a code edit; this run's rule is *enactment is a written amendment*).

**Owner/slot:** register in the C4-setup owner's amendment slot (e.g. `docs/45` §8 or `docs/43` §7/§8,
whichever owns nb19's C4 setup record). **Proposed registration text:** *"OWED SITE — `make_nb19.py`
and `notebooks/19_c3_gate_and_c4_setup.ipynb` still carry the STRUCK ±38 %/0.1644 ln band (`σ_r=0.465`
per-station-floor block) and assert on it. The struck instrument is `docs/52`; the station-bootstrap
replacement is `docs/45` §8 amd 1. Regeneration is owed to the notebook track — do not consume nb19's
band as current until regenerated. Canonical erosion (299.5387/248.7298) is unaffected."*

---

## After all four are applied
- Re-run the refuter pass on the *edited* text (each finding to a fresh "this fix is wrong" refuter),
  per the run's rule that a claim entering a document must survive refutation.
- These four are the open items `docs/54` §6/§7 carries; close them there once applied.

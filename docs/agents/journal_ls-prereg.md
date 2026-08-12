# Journal — ls-prereg

**Agent slug:** `ls-prereg`
**Started:** 2026-08-11
**Task:** DRAFT (not freeze, not adopt) a pre-registration for resolving the LS **level**,
written to `docs/46_ls_preregistration_DRAFT.md`, modelled on `docs/33` and `docs/35`.

**Deliverable written:** `c:\dev\magdalena-mgb-sed\docs\46_ls_preregistration_DRAFT.md`
(new file; nothing else in the repository was created or modified by this run).

## Binding constraints I restated to myself before starting

- I write a **DRAFT**. It is not in force. It says so on line 1, its registration card (§9)
  is deliberately blank, and its amendment slot (§10) is marked inactive. I did **not** edit
  `docs/00_INDEX.md`, `docs/31`, `docs/35`, `docs/37`, `docs/42`, `docs/43` or `docs/45`, and
  the draft records what those files are **owed** rather than enacting any of it.
- No git commands. No modification of adopted configuration (H2E, the frozen driver bundle,
  the adopted `cp_revision`, the LS column the engine reads). No calibration, no simulation.
- MEASURE BEFORE ASSERTING. Every number in the draft is either carried from a doc/journal
  with a citation, or is a three-line derivation from two published formulas that I ran and
  recorded here.
- AN UNCITED BAND CANNOT PASS OR FAIL A GATE. I introduced **no** new plausibility band. The
  one tolerance the draft uses (0.1644 ln = ±38 %) is the project's own registered level
  standard error (`docs/45` §2.2 / `docs/43` §3.2 lens 3, σ_r 0.465 ln over n = 8), reused
  with the derivation for why it is the right bar.

## Log

### Step 0 — orientation

Read, in order: `CLAUDE.md`; `docs/00_INDEX.md`; `docs/33` in full (form: frozen §1–§5,
results appended as §6–§8, issues journalled-and-followed); `docs/35` §1–§3 and §9.2–§9.3
(form: registration card up front, §9 the amendment slot, **§9.3 is already a frozen
pre-registration of the LS-formulation comparison**); `docs/agents/journal_decide-ls-
resolution.md` in full (the measurement that produced the three levers, and the *resolution*
decision that this draft does NOT re-open); `docs/37` §4 candidate 0, A1.6, A2.1, A2.2;
`docs/42` §3.1–§3.3, G4, §9; `docs/43` §2–§3; `docs/45` §0–§2.5, §6, §7; `docs/30` §1;
`docs/31` C4.3; `scripts/c3/ls2d.py`; the LS consumption path in `src/mgb_sediment.py`.

### Step 1 — the design problem, and how I solved it

**The trap:** the three lever factors (0.351 / 0.502 / 1.714 / joint 0.421) were measured on
2026-08-11 and are already quoted in five documents and two notebook generators. A
"hypothesis" that predicts them is a post-hoc dressed as a pre-registration — exactly the
failure mode this project's rules name. Writing that would have been worse than writing
nothing.

**Resolution:** §1 of the draft is an explicit *ordering disclosure* — it lists everything
already measured and declares it **out of scope as a hypothesis** — and §2's hypotheses are
built only on quantities that are genuinely **not** measured today:

1. the **erosion-weighted** factors (only *area-weighted* proxies exist; `docs/35` §9.3.3
   itself flags 104.8 Mt/yr as a proxy and demands the exact re-run, without stating a bound);
2. the **step-function** `m` variant (only the *cap* was measured — see Defect A below);
3. the **isolated `L`-form** lever (the published ×0.790 is confounded — Defect B below);
4. the per-cell / per-stratum **shape** of each lever;
5. whether the joint factor survives on the engine's own column with erosion weighting;
6. whether G4.1 fires.

Each hypothesis therefore has a **reading clause** (refutable by document evidence) and a
**field clause** (refutable by recomputation), and each names the evidence grade at stake.

### Step 2 — TWO DEFECTS I FOUND IN THE EXISTING EVIDENCE (both measured/derived, not asserted)

**Defect A — the ×0.502 row is a CAP; Buarque eq. 14 is a STEP FUNCTION. They differ.**
`journal_decide-ls-resolution` §3b labels the row *"+ m hard-capped at 0.5 (his eq. 14)"*,
while its own §1a records eq. 14 as the step 0.2 / 0.3 / 0.4 / 0.5 on slope classes
< 1 % / 1–3 % / 3–5 % / ≥ 5 %. `min(m_cont, 0.5)` equals that step only where our continuous
`m` already exceeds each step, which `scripts/c3/ls2d.py:slope_exponent_m` puts at
tan θ ≈ 0.09. Derived (recorded so it is reproducible):

```
python3.10 -c "
import math
def m_cont(t):
    s=t/math.sqrt(1+t*t); b=(s/0.0896)/(3*s**0.8+0.56); return b/(1+b)
def m_step(t):
    sf=t*100.0
    return 0.2 if sf<1 else (0.3 if sf<3 else (0.4 if sf<5 else 0.5))
au=185.2                                   # basin-median a_unit_hs at 90 m (same journal, step 2)
L=lambda m,a:(m+1)*(a/22.13)**m
for t in [0.005,0.02,0.05,0.1581,0.5]:
    mc=m_cont(t); print(t, mc, min(mc,0.5), m_step(t), L(m_step(t),au)/L(min(mc,0.5),au))
"
```

| tan θ | `m_cont` | `min(m,0.5)` (measured row) | eq. 14 step | L(step)/L(cap) at a_unit 185.2 m |
|---|---|---|---|---|
| 0.005 | 0.0847 | 0.0847 | 0.20 | **1.414** |
| 0.020 | 0.2441 | 0.2441 | 0.30 | 1.177 |
| 0.050 | 0.4009 | 0.4009 | 0.50 | 1.322 |
| 0.1581 | 0.5845 | 0.5000 | 0.50 | 1.000 |
| 0.500 | 0.7003 | 0.5000 | 0.50 | 1.000 |

⇒ eq. 14 is **less reducing** than the cap below ~9 % slope, so the joint **×0.421 is a
plausible over-statement** of the gap and the true "2.37×" may be smaller. **I did not
recompute the basin factor** (that needs the 30.2 M-cell pass, which would be doing the
measurement this document is supposed to pre-register). It is registered as H-M with a signed
prediction (`f(V2b) > f(V2a)`) and its own refutation conditions.

**Defect B — the ×0.790 "literal Desmet–Govers L" is confounded with an S swap.**
Read from the code, not inferred: `scripts/c3/ls2d.py:ls_variants` builds
`ls3 = l_dg * s_factor_mccool(...)` while the primary `ls1` uses `(sinθ/0.0896)^1.3`. So
`ls2d_dg96 / ls2d = [L_dg/L_cont] × [S_McCool87 / S_MB86]` — **two levers** — and it was
measured on the **uncapped** `ls2d`, not on `ls2d_hs`, which is what the engine reads
(`src/mgb_sediment.py:864`). The S-ratio is strongly slope-dependent, derived from the
published formulas alone:

| tan θ | W&S78 / MB86 | McCool87 / MB86 |
|---|---|---|
| 0.005 | 3.809 | 3.578 |
| 0.050 | 0.975 | 1.217 |
| 0.1581 | 1.152 | 1.031 |
| 0.500 | 1.878 | 0.867 |
| 1.500 | 2.712 | 0.744 |

⇒ the bracket's lower end (×0.333, the "3.00×" statement quoted in `docs/35` §9.3.1,
`docs/37` §4 candidate 0, `docs/43`, `docs/45` §2.1 and both notebook generators) rests on an
unisolated lever applied to a different column. Registered as **H-L** with variant `V5`
(literal D&G `L`, S held at ours) and a refutation bound.

Both defects are recorded in the draft as §1.1, and §9.1 requires a freezing session to
either resolve them or **explicitly inherit** them.

### Step 3 — the C4.3 gate, and the number that makes it decidable

Verified first that the question is live: `progress_map.html` says *"C4.3, the search itself,
has not started"*; `ls scripts/c4`, `ls data/processed/c4` and a repo-wide `find` for
`c4_grid*` all return nothing. So this is a real ordering decision, not a retrospective one.

**The gate's discriminator** (draft §6.1) is a cheap pre-test that costs minutes and decides
the branch *before either job runs*: the per-station upstream erosion weights `w_s` under V0
and V4, and `Δ_shape = max over the CAL 8 of |ln(w_s(V4)/w_s(V0))|` against the same 0.1644
bar. Derivation: LS is linear per cell and transport is linear in cell load, so a **uniform**
LS factor `f` moves the optimum to `α̂/f` and leaves Π̂, the objective value and every residual
statistic identical at that optimum — the surface is the same surface with a relabelled α
axis. Only a **relative** shift between stations makes the fit unrecoverable by rescaling.
That is `docs/37` A2.2's level/shape split made operational for one decision.

**The number that makes Branch A fail-able:** the registered α box is [2.0, 30.0]
(`docs/45` §2.1) and a later source-LS adoption multiplies α̂ by 1/f ∈ [2.375, 3.00]. So
`30.0/3.00 = 10.0` — **α̂ ≥ 10.0 blocks the verdict**, because the equivalent source-LS
optimum may lie outside its own registered box, and above `30.0/2.375 = 12.63` it certainly
does. A fit whose equivalent is outside its registered box needs a *new pre-registration*,
not a re-run. I also registered that the `docs/45` §6.1 **ADOPT** outcome is unreachable
before LS lands, because its conditions read α̂ against 3.9 / 35.4, which is an LS-conditional
band — phrased as *strictly more restrictive than* `docs/45`, never as an amendment to it,
since a frozen pre-registration is amended only by its own owner.

### Step 4 — things I deliberately did NOT do (dead ends and refusals)

- **Did not re-run `scripts/c3/ls2d.py`.** It writes the committed `minibacia_ls2d.csv` /
  `urh_ls2d.csv`; `journal_decide-ls-resolution` §2 records that trap and I inherited its
  discipline. The draft registers that variants go to a **new** file.
- **Did not compute any basin factor or load.** That is the measurement the document
  pre-registers; computing it first would destroy the ordering the document exists to
  guarantee.
- **Did not re-open the resolution question.** It is RESOLVED at native 90 m by D1–D6 of
  `journal_decide-ls-resolution`; the draft says so and lists `ls2d_aggregation` /
  `ls2d_resolution` among the immovable objects (`docs/42` G4.2).
- **Did not invent a tolerance.** My first instinct was a ±10 % proxy tolerance; I discarded
  it as an uncited band and used the project's registered 0.1644 ln level SE instead, with
  the derivation for why a difference below the fit's own standard error cannot change any
  downstream statement.
- **Did not use the "mountainous LS 2–10" coincidence** (source-formulation median 7.262 sits
  inside it) as evidence in any direction — `docs/35` §9.3.5 forbids it and the draft repeats
  the prohibition in §4.3.
- **Did not restate the C3 residual's direction.** It is UNKNOWN (`docs/37` A1.9); the
  "~2× under-erosive" claim is withdrawn and may not motivate an LS choice.

### Step 5 — consequential corrections the draft RECORDS AS OWED (it enacts none)

1. `docs/35` §9.3.3's expected consequence is based on the **prior** C level (248.730 Mt/yr);
   re-based to the adopted 299.5387 Mt/yr it is **≈ 126.1 Mt/yr** at ×0.421 and **≈ 99.7** at
   ×0.333 — still below the 144–184 anchors, so the registered "an unattractive total is not
   evidence" clause is unaffected in substance. Owed to `docs/35` §9.
2. If H-M survives, the label *"his eq. 14"* on the ×0.502 row is wrong in `docs/35` §9.3.1,
   `docs/37` §4 candidate 0, `docs/43` §1.4, `src/nbgen/make_nb18.py`, `make_nb19.py`.
3. If H-L survives, the ×0.790 / ×0.333 bracket and the "2.37×–3.00×", "α ref 3.9–5.0",
   "band 2.0–9.9", "hard stop 11.8–14.9" statements need re-deriving in the same places plus
   `docs/45` §2.1.
4. `docs/42` §9 still owes the P1/P2/P3 transcription from `docs/43` §3.1 (noted in
   `docs/45` §0; unrelated to LS but in the same slot).

### Step 6 — what a successor needs to know

- The draft's §9.1 lists the four things a freezing session must settle first; the hardest is
  whether Buarque (2015) can be re-obtained to verify eq. 14's `Sf` units. If it cannot, H-M's
  (R6) is unfalsifiable and the honest outcome for that lever is already the **NEGATIVE —
  UNRESOLVED** branch, which the draft pre-commits to publishing (§7, with the `docs/30` §1,
  `docs/33` §3.4, `docs/40` and `docs/29` precedents).
- The draft is subordinate to `docs/35` §9.3 by construction. If a freezing session wants it
  to *supersede* rather than *extend* that section, that is a `docs/35` amendment and is not
  in this document's gift.
- Nothing in the repository was measured, moved, executed or committed by this run.

## Closing state

- [x] Read `CLAUDE.md`, `docs/00_INDEX.md`, then `docs/33` and `docs/35` for form
- [x] Read the LS evidence chain: `journal_decide-ls-resolution`, `journal_c31-ls2d`,
      `docs/37` §4/A1.6/A2.1/A2.2, `docs/42` §3/G4, `docs/43` §2/§3, `docs/45`
- [x] (a) four hypotheses — one per lever + the joint cell (+ a fifth, H-L, for the
      confounded `L` form), each with named refuting statistics and bounds
- [x] (b) decision rule with the DERIVED / IDENTIFIED / CITED / ASSUMED / UNVALIDATED ladder
      and a three-outcome adoption table
- [x] (c) the immovable set: adopted `cp_revision`, both unit conventions, H2E, the frozen
      driver bundle, the aggregation/resolution scalars, the committed LS products, P/FG,
      the yield embargo, the four frozen pre-registrations
- [x] (d) the C4.3 gate, both branches, with a pre-test that decides the branch and an α̂ = 10.0
      stop derived from the registered α box
- [x] (e) pre-commitment to publishing the negative result, with this project's four precedents
- [x] (f) the Π confounding declaration and seven things the document cannot conclude
- [x] Two defects found in the existing evidence, with the arithmetic behind each
- [x] Journal written as I went; no repo artifact modified; no git command run

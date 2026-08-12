# journal — B4: transcribe P1/P2/P3 into `docs/42` §9, and resolve 0.0096 vs 0.0104

Agent: `debt-b4-transcription`. Opened 2026-08-11.
Task: bookkeeping repair of `docs/42`'s registration record (§9 amendment slot only), plus a
written resolution of the CAL-13 `k_min` discrepancy.

## Step 1 — verification by direct read (do not trust the brief)

Read `docs/42_c4_guards.md` in full (612 lines), `docs/43_c3_c4_gate.md` in full (360 lines),
`git log`, and grepped the repo for the four `k_min` numbers.

CONFIRMED, all three brief claims:

- `docs/42` §9 line 604: `| Amendments | none |` — verbatim, still says none.
- `docs/42` §9 line 600: `| Registered station sets | CAL 13 (docs/32 §R6 tributary set) for
  fitting; all 18 for every residual-structure guard, ... |` — still CAL 13.
- `docs/42` §4.2 line 230: `| slope over the CAL 13 only | 13 | 0.0104 | 3.06× ... | NO —
  underpowered |` — still 0.0104.
- Meanwhile `git log` shows `1e0843c` (c4.1 transport), `865f674` (c4.2 prereg freeze),
  `831bd0a`/`02e7e95` (nb19 written + executed), `608a39e` (tracker: C4 under way). So C4 has
  started against a registration record that says no amendment was ever made.

`docs/43` §3.1 P1 text, verbatim: *"Correct §4.2's power table with it: the fitted-set `k_min`
is 0.0209 /km, not 0.0096 /km."* — i.e. it attributes 0.0096 to `docs/42`, which prints 0.0104.
`docs/47` O7 (line 630) flags exactly this and assigns its resolution to B4.

## Step 2 — recomputation plan for the discrepancy

Both numbers claim to be the minimum detectable OLS slope of `r_i = c + k·Lw_i` at σ_r = 0.465
over the CAL 13 `Lw` values in `docs/42` §4.1. Candidate methods differ only in the multiplier
and the σ→SE step. Reproduce the all-18 anchor (0.00216, which BOTH documents agree on) first —
whichever method reproduces the anchor is the method, and that method's CAL-13 answer is the
right one. That is the decisive test and it needs no new data.

## Step 3 — the recomputation, and the verdict

Method recovered from `src/nbgen/make_nb19.py:1970` (`def k_min`), which is the lens's/nb19's:

```
k_min = 1.96 * sigma_r / sqrt(sum((Lw - mean(Lw))**2))
```

i.e. the smallest |slope| whose 95 % two-sided normal interval excludes 0 in `r_i = c + k·Lw_i`,
at the registered `sigma_r = 0.465` and `docs/42` §4.1's own `Lw` column.

Scratchpad scripts (wrote nothing into the repo):
`.../scratchpad/kmin_recompute.py`, `.../scratchpad/kmin_joint.py`.

Reproduces, at 1.96 / 0.465 / §4.1's Lw:

| set | n | recomputed | published | agrees? |
|---|---:|---:|---:|---|
| all 18 | 18 | **0.002158** | 0.00216 (`docs/42` §4.2 itself) | YES |
| CAL 8 | 8 | **0.020916** | 0.02092 (`docs/43` §3.2, nb19) | YES |
| CAL 8 + ARRANCAPLUMAS | 9 | **0.003031** | 0.00303 (`docs/43` P2) | YES |
| **CAL 13** | 13 | **0.009640** | **`docs/42` §4.2 prints 0.0104** | **NO** |

So the method that produces `docs/42`'s *own* all-18 cell produces 0.00964, not 0.0104, on the
CAL 13. Five attempts to reproduce 0.0104 and all five failed:

1. z: would need z = **2.115**, not 1.96 — and the all-18 cell would then be 0.00233, not 0.00216.
2. sigma: would need **0.5017**, not the registered 0.465.
3. t-critical instead of z: df = n-2 -> 0.01083; df = n-1 -> 0.01072. Neither is 0.0104, and
   either moves the all-18 cell off 0.00216.
4. a different 13 of the 18: exhaustive search of all C(18,13) = 8,568 subsets -> **zero** subsets
   give 0.0104 +- 5e-5.
5. the joint form of G1 note 3 (Lw residualised on §4.1's Grassland and Bare shares): CAL 13
   -> 0.01062 (2.1 % off), and it does NOT reproduce the CAL-8 0.02092 (gives 0.02529), so the
   lineage's numbers are univariate. Hypothesis rejected.

**Sixth and decisive check — `docs/43`'s own arithmetic runs on 0.00964, not on 0.0104.**
P1 claims losing the 5 stations costs a factor **2.2** and is **9.7×** worse than the all-18 guard.
0.020916/0.009640 = **2.170** (-> 2.2) and 0.020916/0.002158 = **9.693** (-> 9.7).
At 0.0104 the first factor would be **2.011** (-> 2.0), which is not what P1 prints.

VERDICT: **`docs/42` §4.2's CAL-13 cell is the wrong number.** Correct value 0.00964 /km.
`docs/43` P1's *number* (0.0096) is right; its *attribution* is wrong — it presents 0.0096 as what
`docs/42` printed. `journal_adj-c4-feasibility.md:167` called the gap "method rounding"; that
label is withdrawn — 7 % is far outside 1-dp rounding of any input and no method reproduces it.

Independent corroboration found after the fact: `docs/47` §2.2 states the same mechanism and the
same digits (all-18 **0.002157**, CAL-8 **0.02092**) from a different agent's recomputation.

Secondary, recorded not repaired: the CAL-13 cell's contrast column uses the max-min **span**
(exp(0.0104x107.8) = 3.068 -> "3.06") while the all-18 and 22-pair rows use the **max Lw**
(exp(0.00216x348.4) = 2.122 -> "2.12"; exp(0.00119x348.4) = 1.514 -> "1.51"). Corrected CAL-13
contrast: **2.83x** on its own stated span convention, **2.90x** on the other rows' convention.

**No verdict moves.** 0.00964 is still ~4.5x the all-18 figure, still outside the (uncited, and
gate-forbidden) 0.0020-0.0032 reference, so the CAL-13-only test stays underpowered and stays
rejected. The correction moves the number in the *more powerful* direction and rescues nothing.

## Step 4 — the station set actually in force

From `docs/45` (FROZEN 2026-08-11, C4.2), which discharged the substance of P1/P2/P3 in its own
frozen sections while recording that the `docs/42` §9 transcription "remains owed":
- fitting: the **CAL 8** (`docs/45` §0, §2.2) — P1;
- `21237020` ARRANCAPLUMAS **EVAL only**, with the other four (`docs/45` §2.4) — P2 decided;
- deposition `k` **FIXED at 0.0 /km**, reported as a bound, 2 free + 1 fixed (`docs/45` §2.3) — P3;
- G1.2 still runs on **all 18**, `k_min` **0.00216 /km** unchanged.

## Step 5 — written

Appended `docs/42` §9.1-§9.6 (amendment slot only). Two cells in §9's table gained pointers with
their original text preserved verbatim. **No threshold anywhere in `docs/42` was altered**;
§1-§8 untouched; `docs/43`, `docs/45`, `docs/47` not edited. Five items flagged to the
orchestrator in §9.6 rather than fixed here.

**Deliberately NOT done:** `sigma_r` = 0.465 is a registered threshold and `docs/47` §2.2 (D2)
measures it 3.9-4.2x too low. Every `k_min` here is proportional to it. Correcting it is
`docs/47` B5's job against `docs/45` §8, not this pass's — so the amendment corrects the CAL-13
number **at the registered sigma_r** and carries D2 as a mandatory pointer instead of silently
re-basing the table. Re-basing would have been the convenient move and would have changed a
frozen threshold under cover of a bookkeeping repair.

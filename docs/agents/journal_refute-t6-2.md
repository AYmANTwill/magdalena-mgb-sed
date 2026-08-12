# journal_refute-t6-2 — REFUTER, T6 lens-new-bar-costume

Date: 2026-08-12. Posture: the finding is WRONG until I cannot kill it.

## Target finding (restated)
CRITICAL: the retired ±38 % / 0.1644 ln level band is alive in `src/nbgen/make_nb19.py`
and in the executed `notebooks/19_c3_gate_and_c4_setup.ipynb`, where it PASSES an integrity
assertion; and σ_r = 0.465 is still labelled a *per-station residual floor*.

## Plan
1. Verify the quoted strings verbatim at the named locators (misquote ⇒ refutation).
2. Check surrounding context for supersession / strike-through / historical-record framing.
3. Verify from the EXECUTED notebook JSON (not exit code) that the outputs claimed are present.
4. Check whether this re-raises something already refuted/retired (0.1644 bar is RETIRED —
   but retired-as-a-MATERIALITY-BAR is not the same object as a level band; watch for a
   category error).
5. Recompute the arithmetic with python3.10.
6. Check severity even if it survives.

## Log

### Step 1 - do the quoted strings exist verbatim?

YES, all of them - but the LOCATORS ARE STALE by roughly +54 to +70 lines, because
`src/nbgen/make_nb19.py` was edited later this run (mtime 12:16) than the lens read it and than
the notebook was executed (`notebooks/19_c3_gate_and_c4_setup.ipynb` mtime 11:11).

Command: `grep -n 'per-station\*\* residual floor\|the level band at n=8\|13 stations would have given' src/nbgen/make_nb19.py`

    1897:| **stations** | **8** | the registered noise floor $\sigma_r$ = 0.465 ln is a **per-station** residual floor and does **not** average down within a station | **the binding one**, used for every spatial claim |
    1967:consequently **+/-38 %** (0.724x to 1.380x); 13 stations would have given +/-28.8 %.
    2956:    ('the level band at n=8 is +/-38 % at 95 %',

Command: `grep -n 'SE8\|SE13\|SIGMA_R' src/nbgen/make_nb19.py` (excerpt)

    1906:SIGMA_R = 0.465          # ln units, docs/42 section 4.2 - PER STATION, does not average down
    1920:SE8 = SIGMA_R / np.sqrt(8); SE13 = SIGMA_R / np.sqrt(13)
    2211:                   f'+/-{100*(np.exp(1.96*SE8)-1):.0f} % at 95 % (SE {SE8:.4f} ln, n=8)',
    2957:     abs(100 * (np.exp(1.96 * SE8) - 1) - 38) < 1.0),
    2958-2961: the two k_min assertions, against 0.00216 and 0.02092

Claimed :1843 / :1852 / :1866 / :2886-2891 -> actual :1897 / :1906 / :1920 / :2956-2961.
Content quoted correctly; line numbers wrong. STALE LOCATOR, NOT A MISQUOTE. Not a refutation.

### Step 2 - is the surrounding context a supersession / historical block?

NO. Section 4.2 of the notebook is a live methodological table choosing the binding denominator,
and cell 81 is a live integrity-assertion gate whose failure would `assert`. Searched the
generator and the executed notebook for any retirement marker:

`grep -n 'RETIRED\|0.6936\|1.9618\|9.7.2\|AMENDMENT\|bootstrap' src/nbgen/make_nb19.py` -> NO hit
for 0.6936, 1.9618, 9.7.2, A-P4. Its only `~~` strikes concern 6.83-8.73 (docs/35 section 9.2) and
0.421475 (f_area) - different objects.

Notebook JSON scan (82 cells): `1.9618` cells [], `0.6936` cells [], `A-P4` cells [],
`0.29, 3.73` cells [], `STALE` cells []. No banner anywhere. NOT a false positive on framing.

### Step 3 - verified FROM EXECUTED OUTPUT (parsed the .ipynb JSON, not an exit code)

All claimed output lines are present, verbatim:

    cell 53 OUT: SE of the fleet-mean LEVEL at n=8  : 0.1644 ln = +/-38 % at 95 %  (0.725x - 1.380x)
    cell 53 OUT: SE of the fleet-mean LEVEL at n=13 : 0.1290 ln = +/-28.8 %   (what docs/42 assumed)
    cell 60 OUT: Pi (the level) ... +/-38 % at 95 % (SE 0.1644 ln, n=8)
    cell 60 OUT: channel deposition k ... k_min 0.0209 /km on the fit set; 0.00216 /km on all 18
    cell 81 OUT:   PASS  the level band at n=8 is +/-38 % at 95 %
    cell 81 OUT:   PASS  k_min on all 18 reproduces the documented 0.00216 /km
    cell 81 OUT:   PASS  k_min on the CAL 8 reproduces the documented 0.0209 /km

Plus cell 52 markdown carries the "per-station residual floor" label, and cells 54 / 55 / 59 / 61
carry "+/-38 %". The notebook is git-MODIFIED this run, i.e. it was re-executed this run.

### Step 4 - arithmetic recomputed with python3.10

    0.465/sqrt(8) = 0.16440232662587229
    pct halfwidth n=8  = 38.02001987244472    -> the assertion's |x-38| = 0.0200 < 1.0, so it PASSES
    pct halfwidth n=13 = 28.759595562555006
    1.9618/sqrt(8) = 0.6936010416658844    1.3506/sqrt(8) = 0.4775092093352755
    0.6936/0.1644 = 4.2189247311827955 = 1.9618/0.465
    exp(+-1.96*0.6936) = 0.2568 - 3.8941

The lens's arithmetic holds exactly, including the x4.22.

### Step 5 - is the retirement real in the documents of record?

YES, three times over, all dated 2026-08-12:

- `docs/42` section 9.7 (A-P4) :906 and :945 - "`0.465/sqrt(n)` as the SE of a fitted level ...
  RETIRED - INVALID (wrong error term)"; the :960-964 table; the :1031-1038 ownership table.
- `docs/43` section 3.2 :209 struck with an amendment-1 pointer; section 7 amd 1 :432-444;
  :518-520 "a struck band does not revert to +-38 % by default".
- `docs/45` section 8.1 :135 struck; section 8.1.5 rows 1-6, 8, 14-16: k_min 0.0209 -> 0.0838,
  0.00216 -> 0.0065-0.0069, band -> the station bootstrap x0.29-x3.73 (a PROCEDURE, not a
  constant), and row 3 WITHDRAWS +-28.8 % with NO corrected value.

So nb19 prints, unbannered and as PASSING, the exact objects three frozen documents struck.

### Step 6 - is it a re-raise, or a category error?

NO on both.

- Not a re-raise: it does not reconstruct a materiality bar, quotes no alpha-hat, and does not
  re-litigate docs/52. It correctly keeps the two 0.1644 objects apart - the docs/46 MATERIALITY
  BAR (struck, docs/52, no replacement) versus the SE-OF-THE-LEVEL REUSE (retired by docs/42
  section 9.7.2 / docs/43 section 7 amd 1 / docs/45 section 8 amd 1).
- No category error on sigma_r either: docs/42 section 9.7 holds the estimator-disagreement
  statistic VALID and retires only its REUSE as a per-station residual sd. nb19 :1897 / :1906
  asserts the residual-floor provenance and then divides by sqrt(8). That IS the retired reuse.

### Partial defences considered and weighed

(i) The two k_min assertions are labelled "reproduces the documented ..." and are, as arithmetic,
    faithful reproductions of docs/42 section 4.2's printed digits at sigma_r = 0.465 - and
    docs/42 section 9.5 :800-801 CITES nb19 for exactly that reproduction, on purpose. So this
    half is weaker than the +-38 % half. But docs/45 section 8.1.5 rows 5-6 and docs/42 :715
    strike 0.00216 as the operative bound, so "the documented 0.00216" is no longer documented.
    Stale label, no pointer. Real, but MEDIUM in isolation.
(ii) The RATIOS in cells 56 / 58 ("a factor of 2.2 WORSE", "9.7x worse") explicitly SURVIVE
    unchanged (docs/42 section 9.7 :947; docs/45 section 8.1.5 "DOES NOT CHANGE" - sigma cancels
    in a ratio). The finding does not attack them, correctly. Nothing to trim there.
(iii) The finding's consequence sentence overclaims: "the claim 'the +-38 % band is retired' is
    false on disk". It IS retired on disk, in the three documents of record. What is true is that
    a regenerable derived artifact still asserts it as current and PASSING, with no pointer, and
    that no amendment ownership table registers nb19 as an owed site for THIS defect - grep for
    nb19 across docs/42/43/45/47 finds only docs/42 :787/:801 citing it as a reproduction source,
    and docs/43 section 7 amd 8 :841 owing it a correction for f_area 0.421475 only.

### VERDICT

NOT REFUTED. Strings verbatim, executed output confirmed, no supersession framing, arithmetic
exact, not a re-raise, no category error. Corrections owed to the finding: the locators are stale
by roughly +60 lines, and "false on disk" must be narrowed to the artifact.

Severity: HIGH, not CRITICAL. (a) nb19 is a regenerable derived artifact, not a project document,
not frozen, and gates nothing - C4 entry is gated by docs/47, the band by docs/45 section 8;
(b) the documents of record already carry the strike plus an explicit no-default-revert rule
(docs/43 :518-520), so the remedy is a pointer or a regeneration, not a decision reversal;
(c) docs/43 section 7 amendment 8 :841 already set this project's precedent for stale notebook
prints - "RESIDUAL, not this session's to fix", remedied by the notebook/verification track with a
dated correction followed by regeneration and re-execution; (d) one third of the offered evidence
(the k_min reproduction assertions) is a weaker staleness sub-claim. Not lower than HIGH: the
notebook is the executable C4 setup record, the project's own discipline is VERIFY FROM EXECUTED
OUTPUT, and nb19 is currently the only unregistered site.

Scope note for the parent: the proposed fix as written (edit the generator, re-execute) is a code
edit, and this run's standing rule is that ENACTMENT IS A WRITTEN AMENDMENT. The docs/43 section 7
amd 8 precedent is the right shape - register nb19 as an owed site in an amendment now, hand the
regeneration to the notebook track.

# journal x59-refute-4 (REFUTER)

Target finding (HIGH, lens x59-lens-numbers):
"The Fagundes bar [-0.26, 0.44] is cited to `docs/45` §84, which contains no bar"
locator: docs/59_cross_implementation_comparison.md line 217

Posture: default WRONG. Try to kill it.

## Log

### 1. Quoted string at docs/59:217 — exists VERBATIM
```
$ sed -n '217p' docs/59_cross_implementation_comparison.md
| **the bar** | **[-0.26, 0.44]**, Fagundes (2018) s6.3.1 (`docs/45` s84) | **the same bar**,
cited in `src/mgbsed/calibration/metrics.py` L7 as *"the KGE range quoted in its conclusions
(-0.26 to 0.44)"* |
```
No misquote. The finding's transcription of the claim is exact.

### 2. docs/45 line 84 — it is the alpha SEARCH BOX row, no KGE band
```
$ sed -n '84p' docs/45_c4_preregistration.md
| **P1** | **alpha** | ... | **[2.0, 30.0]**, log-spaced | union of `docs/31` sC4.2's registered
`alpha in [2, 30]` and Fagundes (2018) s6.3.1's own MOCOM-UA search prior **[2.0, 25.0]**
(`docs/43` s1.3 leg 1) | **11.8** | **Williams (1975)** ... |
```
```
$ grep -n "0\.26" docs/45_c4_preregistration.md
307, 581, 583, 637, 901, 1034, 1037, 1103, 1310, 1566, 1635, 1636, 1714   # 84 is NOT among them
```
Line 307 (registration): "> **THE SEDIMENT KGE BAR, registered: `F_report` in [-0.26, 0.44]** --
Fagundes' median log-flux KGE band, as `docs/31` sC4.2 registered and `docs/43` s3.1 forbids
relaxing."
Headings: s3.2 starts at line 297, s3.3 at line 316 -> line 307 IS inside s3.2. s2.1 spans
80-124 -> line 84 IS inside s2.1. CONFIRMED as the finding states.

### 3. Is "s84" a line number? YES - established, not assumed
docs/59 cites `docs/45` s302 (= line 302, the F_report row) and s311 (= line 311, the mean
predictor KGE = 1 - sqrt(2)); both verified by sed. docs/45 has no section numbered above 8.x
(`grep -n '^#\{1,4\} '`). The writer's own worksheet uses the repo's `doc`:line form:
```
docs/agents/journal_x59-write.md:58
| bar + no-skill | `docs/45`:84 (Fagundes 2018 s6.3.1), :311, :589 | bar [-0.26, 0.44]; mean
  predictor KGE = 1 - sqrt(2) = **-0.414** |
```
So s84 = line 84, and the writer's own note shows where the slip came from: :84 was collected for
the "Fagundes 2018 s6.3.1" ATTRIBUTION, :311/:589 for the no-skill statement -- and no locator
was ever collected for the bar's own registration at :307.

### 4. The finding's "two rows later" is WRONG - corrected, substance unaffected
```
$ grep -n 's84' docs/59_cross_implementation_comparison.md
217:| **the bar** | ... (`docs/45` s84) | ...
336:  pre-registered against Williams (1975) and Fagundes' own MOCOM-UA prior (`docs/45` s84).
```
The second, CORRECT use of s84 is at line 336 in prose (119 lines later), not "two rows later"
in the s2 table; the table's "search box" row carries no citation at all. The finding's point
that one locator does two jobs and is wrong for one stands; its locator for the second job is
imprecise.

### 5. docs/59 cites the bar ONCE, and never points at its registration
`grep -n "0\.26" docs/59...` returns line 217 only. So docs/45:307 / s3.2 appears nowhere in
docs/59: a reader cannot reach the registration of the bar from docs/59 at all.

### 6. NEW, and it strengthens the finding: "Fagundes (2018) s6.3.1" for the BAND is unsupported
`grep -rn "6\.3\.1" docs/*.md` -> docs/36:791, docs/37:1121, docs/43:67, docs/43:154, docs/45:84,
docs/59:217. Every in-repo use of s6.3.1 is about alpha/beta being adopted-vs-calibrated
("ora adotados como 11,8 e 0,56 ... ora calibrados automaticamente") or the MOCOM-UA prior.
NONE attaches the KGE band to s6.3.1.
The band's in-repo sourcing is a DIFFERENT work and a different location:
- docs/19:428 "**Fagundes et al. (2026) report SSC KGE from -0.26 to 0.44** -- with in-situ data
  and **25 years of calibration**"; docs/19:715; docs/31:64 "the source paper"; docs/39:194.
- docs/agents/review_2026-08-10_docs31.md item 9: '"Fagundes et al. 2026" and the -0.26...0.44
  band -- consistent everywhere in-repo ... Not externally checkable from here'.
- THEIR metrics.py L7: "the KGE range quoted in its **conclusions** (-0.26 to 0.44)"; L54 "the
  paper's -0.26 at Barca do Cai".
docs/35:127 records that Fagundes et al. (2026) "is **not in this repo** (no PDF)"; docs/36:761
records its full text could not be obtained. `find . -iname "*fagundes*"` -> nothing on disk
(the fagundes2018.txt cited by journal_verify-gate-logic.md:56 is gone/gitignored). So s6.3.1's
contents are NOT checkable from the artifact, and docs/59:217 merges the 2018 MSc thesis
(s6.3.1, the alpha prior) with the 2026 paper (conclusions, the KGE band).

### 7. The rest of the row SURVIVES (fairness check, their repo, read-only)
```
friend_repo/src/mgbsed/calibration/metrics.py
L7:  Figs. 6, 7 and 9 and to the KGE range quoted in its conclusions (-0.26 to 0.44).
L53:     ``beta = mean_sim/mean_obs`` (bias). Perfect = 1. Note KGE = -0.41, not 0,
L54:     is the "mean of observations" benchmark -- the paper's -0.26 at Barca do Cai
```
Both right-hand cells (L7 bar, L53-54 benchmark) are verbatim-correct. Nothing numeric in the row
is wrong: [-0.26, 0.44] IS the registered bar and IS in their code.

### 8. Disclosure check (docs/59 is required to print its own weaknesses)
docs/59:1157 already states the bar is used only descriptively: "Counts of 'n stations inside the
bar' are descriptive tallies against the **CITED** Fagundes band that both projects already use,
not a new gate." So no gate turns on this citation - a real mitigation. But the mis-pointer itself
is NOT disclosed anywhere, so it is not a disclosed weakness.

### VERDICT: NOT REFUTED. Core claim confirmed from the artifact.
Severity HIGH -> **MEDIUM**: the interval, the source document and the substance are all correct,
the right-hand cell is verbatim, and docs/59 explicitly declines to gate on the bar. What is
defective is the verification path plus an unsupported (2018) s6.3.1 attribution - above LOW
because in this project a mis-cited band is load-bearing (four bands retired on the citation
rule) and a reader following the pointer lands on an alpha box.

# journal_refute-t6-8 -- REFUTER, T6 finding #8
2026-08-12. Read-only agent. Task: try to kill the finding that nb18's equifinality
figure draws a superseded rescaled alpha band 2.0-9.9 and a superseded alpha reference 4.45.

Posture: default = the finding is WRONG.

## Step 1 - verbatim check of the quoted strings at the named locators

VERBATIM CHECK: PASSES for the finding (i.e. I could not kill it on a misquote).
- src/nbgen/make_nb18.py:2897  `                (4.45, r'like-for-like ref for OUR $LS$')]:`
- src/nbgen/make_nb18.py:2901  `ax[1].axvspan(2.0, 9.9, color=CB['amber'], alpha=0.14,`
- :2902  `              label='the SAME band rescaled for our $LS$ level')`
- :2916  reading `what=`: "the amber band is the same range rescaled for our measured topographic level"
- :2923-2924 reading `shows=`: "its rescaled counterpart (2.0-9.9) ... with the like-for-like
  reference for our own topographic level at about 4.45."
Executed copy notebooks/18_musle_construction.ipynb: lines 4471, 4475, 4503-4504; the cell's
iopub idle stamp is 2026-08-12T16:10:44 -> executed THIS run, not a stale artifact.

## Step 2 - provenance of 2.0-9.9 and 4.45 (python3.10, recomputed)
$ python3.10 -c "..."
registered bracket 11.8*f      : 2.9672280000000004 5.096892
registered 5.9-23.6 * bracket  : 1.4836140000000002 10.193784
registered 5.9-23.6 at POINT   : 1.4836140000000002 5.934456000000001
RETIRED bracket 5.9-23.6       : 1.9647000000000003 9.9356        <-- rounds to 2.0 - 9.9
RETIRED bracket 1/f            : 2.375296912114014 3.003003003003003  <-- the retired "2.37x-3.00x"
11.8*mean(retired)             : 4.4486                          <-- rounds to 4.45
11.8*geomean(retired)          : 4.418197972024342
4.45/11.8                      : 0.3771186440677966 = (0.333+0.421)/2

CONCLUSION of step 2: both drawn numbers are the RETIRED f_LS bracket [0.333, 0.421] -- the one
the measured state records as SUPERSEDED by [0.25146, 0.43194] ("1/f_LS = 2.3151x - 3.9768x
SUPERSEDES 2.37x-3.00x"). The lens's own reconstruction (geometric mean 4.4182) is slightly
WRONG: 4.45 is the ARITHMETIC mean of the retired endpoints (4.4486). This tightens the
provenance rather than loosening it -- correction to the evidence, not a refutation.

## Step 3 - is 2.0-9.9 / 4.45 a registered-superseded number? YES, explicitly STRUCK
docs/37_c3_closure.md:268-270 (section 4 candidate 0 bullet "On the alpha guard"):
  "The like-for-like alpha reference for **our** LS is therefore ~~**~ 3.9 - 5.0, not 11.8**~~; the
   docs/35 6.1 expected band 5.9 - 23.6 becomes ~~~ **2.0 - 9.9**~~ and the hard stop ... ~~**11.8 - 14.9**~~"
  followed by "AMENDMENT A3.3.1 + A3.2, 2026-08-12 - all four struck alpha numbers are superseded."
docs/37 A3.2 (line 1691+) registers the replacements at the adopted POINT:
  11.8*f = 2.9672280000000004 ; 5.9-23.6 * f = 1.4836140000000002 - 5.934456000000001 ;
  35.4*f = 8.901684 ; 1/f = 3.976775630318937.
docs/35 line 2287 lists "(d) 9.3.2 item 3's 'expected ~ 2.0 - 9.9, hard stop ~ 11.8 - 14.9'
  re-derived to A3.2's numbers" as an owed amendment.

PROVENANCE OF 4.45, CORRECTED against the lens: 4.45 is the ARITHMETIC MIDPOINT of docs/37's
STRUCK "~ 3.9 - 5.0" like-for-like reference band: 11.8*0.333 = 3.9294, 11.8*0.421 = 4.9678,
mean = 4.4486 -> 4.45. NOT the geometric mean 4.4182 the lens guessed. It is not derivable from
the current bracket: 11.8*[0.25146,0.43194] = [2.9672, 5.0969], amean 4.032, gmean 3.889.

## Step 4 - is the notebook context a supersession block / historical record?  NO.
No strike, no warning, no "superseded" marker anywhere in or around the section 7.2 figure cell.
The reading() text asserts them as CURRENT: "the amber band is the same range rescaled for our
measured topographic level" and "with the like-for-like reference for our own topographic level at
about 4.45." Meanwhile the SAME generator, section 3.6, line 1551, says in prose:
  "The earlier bracket **x0.333-x0.421 / '2.37x-3.00x' is superseded**"
and line 1456 prints "expected band 5.9-23.6*f: 1.4836 - 10.1939". Self-contradiction confirmed.

## Step 5 - is the finding a retired/already-refuted claim, or a category error?
No. It is not (R10), not the 0.1644 bar, not the SDR 0.05-0.30 band, not the mountainous LS 2-10
band. It is not f_ero/f_area confusion (2.0-9.9 does not reconstruct from the area bracket:
5.9*0.24468 = 1.4436, not 2.0). It is not tolerance-vs-materiality. It is exactly a dangling ref.

## Step 6 - git provenance (read-only)
$ git log --oneline -1 -S'axvspan(2.0, 9.9' -- src/nbgen/make_nb18.py
345299a 2026-08-11 notebooks: 15-18 document Phase C end to end ...
$ git show HEAD:src/nbgen/make_nb18.py | grep -c 'expected band 5.9-23.6\*f'  -> 0
$ grep -c 'expected band 5.9-23.6\*f' src/nbgen/make_nb18.py                 -> 1
=> the two stale lines PRE-DATE this run; the CORRECTING section-3.6 cells were ADDED this run;
the notebook was RE-EXECUTED this run (cell stamp 2026-08-12T16:10:44). So the contradiction was
CREATED this run, but the offending text is a STALE SURVIVOR, not newly authored. Framing
correction to the finding, not a refutation.

## Step 7 - the consequence claim
docs/37 line 353-362 performs the exact inversion the lens describes, and docs/37 5 item 1 does
literally call itself "the most important line in this document" (line 342-343) - so that phrase
is a quotation, not rhetoric. Two qualifications the lens omits:
 (a) the inversion holds against the ADOPTED-POINT band 1.4836-5.9345; against the bracket-wide
     form the same notebook prints three cells earlier (1.4836-10.1939), 6.83-8.73 still lands
     inside. docs/37 uses the POINT form, so the inversion is the documented reading.
 (b) 6.83-8.73 is itself a PRIOR-C number; docs/47 2.5 C1 gives 5.67-7.25 at the adopted C.
Neither qualification rescues 2.0-9.9 or 4.45, which are neither form.

## VERDICT: I COULD NOT KILL IT.  refuted = false.  Severity HIGH upheld.
Standing ceiling noted honestly: rescaled alpha numbers "pass and fail nothing" (docs/46 8.2
item 2, docs/37 A3.2's ceiling), so no gate outcome moves. The defect is a re-published figure and
its reading asserting two STRUCK numbers as current, contradicting cells in the same notebook -
which in this project is a significant quality defect, not a cosmetic one.
NOTE FOR THE PARENT: I own no file but this journal; I made no edit to make_nb18.py or the notebook.

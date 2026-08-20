# journal_x59-refute-3

Role: REFUTER. Target finding (HIGH, from x59-lens-numbers):
"The bundle archive IS on this disk - §1.2's stated evidence limit is overstated, and three open
items are settleable today"
Locator: docs/59_cross_implementation_comparison.md §1.2 (164-171), §9 (1113-1116), §8.1 X3/X4/X11 (1006-1011)

Default posture: the finding is WRONG. Try to kill it.

## Log

### 1. Quote check at the locator (verbatim?)

`docs/59` §1.2 lines 164-171 read (verbatim):

    And the bundle's **data** files are likewise not on this disk. `ls -la data/raw/colleague_share/`
    returns exactly **three** files -- `MANIFEST.md`, `ANSWERS_C1_C2_C3.md`, `input_hashes.txt`. The
    **20 data files** enumerated in `input_hashes.txt` ... were **not extracted into this
    repository**, and no bundle archive is present under `data/raw/`. **So every claim in this document
    about a bundle data file rests on the manifest text or on a hash, never on a read of the file** --
    with one exception, which is the one that matters most (§5.1).

=> The finding's two quoted strings ARE verbatim. But the finding CLIPS the trailing
   "-- with one exception, which is the one that matters most (§5.1)". Words quoted are exact;
   the sentence's force is trimmed.

### 2. Is the literal statement true?

    $ ls -la data/raw/colleague_share/     -> exactly 3 files (MANIFEST.md 6294, ANSWERS 7431, input_hashes 2699)
    $ ls -la data/raw/*.zip                -> No such file or directory
    $ ls -la *.zip                         -> magdalena_share_for_colleague.zip  306200202  Aug 13 05:16
    $ find /c/dev/magdalena-mgb-sed -maxdepth 3 -iname "*magdalena_share*"
      -> /c/dev/magdalena-mgb-sed/magdalena_share_for_colleague.zip   (ONE hit only)
    $ grep -n '^\*\.zip' .gitignore        -> 52:*.zip

=> "no bundle archive is present under `data/raw/`" is LITERALLY TRUE. The archive is at the
   repository ROOT, one directory up from the searched path.

### 3. The document already names the archive

    docs/59:38: "...plus the 2026-08-13 bundle `magdalena_share_for_colleague.zip` (306,200,202 bytes)
                 whose 23 member hashes are listed in `data/raw/colleague_share/input_hashes.txt`."

=> §0 (THE PIN) names the archive AND its exact byte count. The document does not assert the
   archive is absent; §1.2's clause is scoped to one directory. The finding is right that §0's
   byte count is obtainable only from the file itself.

### 4. Is the archive really the bundle? sha256 of all 20 members, read-only, streamed

    python3.10: zipfile.open(member) -> sha256, compared to data/raw/colleague_share/input_hashes.txt
    RESULT: ok 20  bad 0  missing 0  total 20

=> The archive on our disk IS the bundle, byte-for-byte on every hashed member. Its inner
   MANIFEST.md (6294 B) / ANSWERS (7431 B) / input_hashes.txt (2699 B) match the three extracted
   files exactly. 60 members (20 data files + 4 text/dir + __MACOSX resource forks).

### 5. Are X3 / X4 settleable today? (test by reading, in memory, no extraction)

    observed_ssc_daily.parquet   -> DataFrame (3652, 59)  index 2009-01-01.., columns = 59 station ids
    observed_ssc_stations.csv    -> (59, 10) ['station','lon','lat','reach','upstream_km2','mapping',
                                    'snap_km','n_days','name','plausible']

=> YES. Tier-1 reads fine. Note X4 ALREADY says "**Settleable now; not done.**" in the doc, and
   X12 already says "(cheap, not done)". X3 says "present in the bundle, not extracted here" --
   true, and not a claim of impossibility.

### 6. Is X11's LS2D half settleable today?

    PYTHONPATH=<their clone>/src  python3.10  pickle.loads(zip.read(basin_magdalena.pkl))
    -> mgbsed.model.basin.BasinData, n_cat 7929, fields incl. ls2d, ls2d_trigger, k_factor, hru_fraction
    ls2d          : sum 187375.516  mean 23.631671  median 15.318151  min 0.447208  max 1206.172
    ls2d_trigger  : median 9036.8   max 344389.6    mean 22169.8
    (their src/mgbsed/model/musle.py:133-134: "``ls2d`` (mean, for the equation) and
     ``ls2d_trigger`` (sum, for the thresholds)")

=> X11's premise is exactly right (only the SUM was published: scripts/21:30 "median 9,037, max
   344,390", reproduced here to 9036.8 / 344389.6 -- so the pkl IS that terrain). And the MEAN
   half IS resolvable today: mean 23.6317, median 15.3182. The LEVEL half is NOT: the bundle
   contains no sediment output (MANIFEST withholds stage1_*/stage2_* as mid-rewrite), so §4 item 5
   ("no basin sediment load of theirs exists on this disk in any form") stands unchanged.

### 7. One piece of the finding's evidence is FALSE

    $ ls /c/Users/knade.MSI_TWILL/Downloads | grep -i zip
      DDJ-400_v103_WIN(1).zip  DDJ-400_v103_WIN(2).zip  DDJ-400_v103_WIN(3).zip  DDJ-400_v103_WIN.zip
    $ find /c/Users -maxdepth 3 -iname magdalena_share_for_colleague.zip -> (nothing)

=> There is NO second copy in Downloads. Exactly ONE copy exists, at the repo root.

### 8. §9's disclosure is accurate as written

§9 says "its 20 data files were not extracted into this repository and none was opened". That is a
statement about what THIS PASS DID, and journal_x59-write.md (c) confirms it. It does not assert the
archive is absent. No defect at §9 -- the finding's §9 fix ("should say the archive was not opened
rather than implying it is absent") asks for a change the sentence already makes.

## VERDICT

NOT REFUTED on the core fact -- independently confirmed (20/20 hashes, files read, X11 half settled
in under a minute). But SEVERITY OVERSTATED: HIGH -> MEDIUM, and the finding's own statement needs
two corrections (no Downloads copy; §9 needs no fix; X11 only half-settleable, and its load-bearing
half is unaffected). Nothing in docs/59 changes numerically; the "never on a read of the file"
provenance sentence is TRUE and is a conservative self-limitation the doc is required to print.
The real defect is narrow: a section titled "What is, and is not, READABLE on this disk" scopes its
search to `data/raw/` and then draws a "So ..." inference that reads as unavailability where the
truth is a choice.

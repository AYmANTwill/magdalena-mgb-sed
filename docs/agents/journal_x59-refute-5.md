# journal_x59-refute-5

Role: REFUTER. Target finding (HIGH, from x59-lens-numbers):
docs/59 line 471, §5.1 table row "DEM archive" — claims our-side locator `docs/15` L24/L31
supports the archive filename `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, member `output_hh.tif`,
and the filename typo. Lens says the locator is wrong; correct locator is docs/35:65-66.

READ-ONLY except this file. No git. No writes to docs/59.

## Log

### 1. docs/59 line 471 quoted verbatim (locator correct)
```
$ sed -n '471p' docs/59_cross_implementation_comparison.md
| **DEM archive** | `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, member `output_hh.tif`, 0.000833deg | theirs `config/data_sources.yaml` L9-14; ours `docs/15` L24/L31 - **same archive, same member, same filename typo** |
```
Only two hits for "DEM archive" in docs/59: L120 (prose) and L471 (the table row). Locator OK.

### 2. docs/15 L24 and L31 - the cited lines
```
$ sed -n '24p' docs/15_domain_correction.md
| **DEM** (Copernicus GLO-90) | **re-download** on the new bbox | OpenTopography: dataset `COP90`, S=1.4 N=11.4 W=-77.0 E=-72.3 |
$ sed -n '31p' docs/15_domain_correction.md
3. Re-download **DEM** (COP90) and **SoilGrids** on the new bbox; drop them in `data/raw/dem/` and `data/raw/soils/`.
```
CONFIRMED: neither line contains the tarball name, the typo `Corrdinatzs`, the member
`output_hh.tif`, or `0.000833`. What they DO carry: dataset = COP90 (Copernicus GLO-90),
the bbox, and the directory `data/raw/dem/`. So the locator supports the *dataset* and the
*bbox* (i.e. it is the right citation for the NEXT row, "domain bbox"), not the three things
this row bolds.

### 3. Where our side actually says it
```
$ grep -rn "Corrdinatzs\|output_hh" docs/ src/ notebooks/ scripts/
docs/35_qpeak_preregistration.md:65-66   <- archive + member + size + "not extracted"
docs/35_qpeak_preregistration.md:465
docs/37_c3_closure.md:897                <- "corrected COP90 DEM (0.000833deg, 5,640 x 12,000...)"
src/merge_chirps_gauges.py:80,82 ; scripts/c3/ls2d.py:100-101,213-220
notebooks/07,08 (extract member from tar) ; several docs/agents journals
```
docs/35:65-66 verbatim:
> - **A whole-basin DEM is buildable but unbuilt.** `data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz`
>   contains one member, `output_hh.tif` (260,274,553 B, Copernicus GLO-90), not extracted.
Note: docs/35:65-66 does NOT contain `0.000833`. The resolution's our-side citation is
docs/37:897 (or the raster itself). The lens's proposed fix is therefore incomplete for the
third element of the row's shared-thing cell.

### 4. Independent recomputation from the primary artifacts (not from any doc)
```
$ ls -la data/raw/dem/
-rw-r--r-- 249137558 Jul 30 16:03 rasters_COP90_Correcte_Corrdinatzs.tar.gz   (also rasters_COP90.tar.gz, 214055442)
$ python3.10 -c "import tarfile; [print(repr(m.name), m.size, m.isfile()) for m in tarfile.open('data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz').getmembers()]"
'output_hh.tif' 260274553 True          # exactly ONE member; size matches docs/35 to the byte
$ python3.10 rasterio %TEMP%\output_hh.tif
size 5640 12000 float32 EPSG:4326
res (0.0008333333333333334, 0.0008333333333333334)
bounds (-77.0004167, 1.4004167) -> (-72.3004167, 11.4004167)
```
So all three elements of the shared-thing cell are TRUE and reproducible from our disk.

### 5. STALENESS the lens's fix would import
```
$ ls -la C:/Users/knade.MSI_TWILL/AppData/Local/Temp/output_hh.tif
-rw-r--r-- 260274553 Jul 30 16:01
```
docs/35:66's "not extracted" is STALE as of 2026-07-30: the member IS extracted (journals
c31-ls2d:20-21, c36-first-run:42,83, reverdict:97 all use it; scripts/c3/ls2d.py:213-220 and
src/merge_chirps_gauges.py:82 read it). The lens's fix asks docs/59 to record "not extracted"
- that would print a superseded statement. Also 260,274,553 B is the *member* size, not the
archive size (249,137,558 B); the fix text "our copy is 260,274,553 B" must say which.

### 6. Their side re-verified
```
$ cat -n friend_repo/config/data_sources.yaml | sed -n '9,14p'
 9  dem:
10    source: Copernicus COP90 via OpenTopography, corrected domain
11    archive: data_Final/02_dem/raw_cop90_opentopography/rasters_COP90_Correcte_Corrdinatzs.tar.gz
12    member: output_hh.tif
13    resolution_deg: 0.000833
14    note: the processed_cop30 GeoTIFFs are on the OLD domain and are quarantined
```
Their L9-14 citation is exact. Same archive basename, typo included; same member; same resolution.

### 7. Verdict
NOT REFUTED. The defect is real and I confirmed it independently: the our-side locator on the
DEM-archive row does not support the row's three bolded elements. But the CLAIM is true, the
verdict SHARED is untouched, no number and no conclusion moves, and a correct our-side citation
exists in the repo. Category check: this is a CITED-vs-nothing error, not concentration-vs-flux,
not pooled-vs-paired, not held-out-vs-in-sample. The row is a positive evidence cell in the
"genuinely SHARED" table, not a disclosure or a labelled limitation, so the "docs/59 must print
its weaknesses" exemption does not apply.
Severity: HIGH -> **MEDIUM**. Verifiability defect on one of seven rows of a load-bearing table;
misdirects an auditor, falsifies nothing.

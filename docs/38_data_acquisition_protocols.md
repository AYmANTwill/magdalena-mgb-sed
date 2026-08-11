# 38 — Data acquisition protocols (extracted from the Word/PDF hand-off documents)

**Written 2026-08-11** by the `hygiene` agent, so that six binary reference documents sitting in the
repository root can be retired without losing anything.

These documents were the *operator instructions* handed to the two data collectors (TWILL and Omar)
while Phase A was being assembled. They were never Markdown, never reviewed, and never linked from
`CLAUDE.md`. Most of what they say is already in `docs/08`, `docs/10`, `docs/11`, `docs/12`,
`docs/16` and `src/download_igac_soils.py`. **This file records only the parts that were NOT already
in the repository**, plus the contradictions the comparison exposed.

Every section names its source file. Nothing here has been re-derived or re-verified: it is a
faithful transcription of what those documents asserted, and it inherits their date and their
uncertainty. Where a claim conflicts with a later, measured document, the later document wins and
the conflict is flagged in §7.

Provenance note: `Protocolo_descarga_PRECIPITACION.docx` appeared as modified in the working tree at
the start of this session. It is not: `git hash-object` on the working-tree file returns
`cb9afdc26fa37f0337067eb3f19109cb2f75bbcc`, byte-identical to `HEAD`. The "M" was a stale stat-cache
entry (mtime touched, content unchanged). The extraction below is nevertheless taken from the
**working-tree** file, as instructed.

---

## 1 — Precipitation via DHIME: the parts no Markdown doc covers

*Source: `Protocolo_descarga_PRECIPITACION.docx` (working-tree version) and
`Protocolo_descarga_PRECIPITACION_OMAR.docx`.*

`docs/16 §2` starts the precipitation pipeline at *"DHIME downloads (two collaborators, by
department)"* — the acquisition step itself was undocumented. This is it.

### 1.1 Portal settings (precipitation)

| Field | Value |
|---|---|
| Portal | `http://dhime.ideam.gov.co/atencionciudadano/` → **Consulta de Datos**. **Use `http`, not `https`** (the OMAR document is explicit about this). |
| Variable | *Precipitación* → parameter *Precipitación Total Diaria*, frequency *Diaria* (PTPM, mm accumulated to 07:00) |
| Station categories | Pluviométrica, Pluviográfica, Climatológica Ordinaria, Climatológica Principal |
| Basin filter | *Área hidrográfica = "Magdalena Cauca"* (station codes 21–29) — or filter by **Departamento** and take every station returned |
| Period | one query `2008-01-01 → 2018-12-31` |
| Output | keep DHIME's `.zip` **zipped**; save to `data/raw/observed/precip/dhime/` |

**Query-size limit (precipitation).** An 11-year query is rejected for the largest departments
(Cundinamarca and Huila were named in advance). Split the dates into `2008–2013` and `2014–2018` and
save two zips (`huila_2008-2013.zip`, `huila_2014-2018.zip`). The delivered folder shows this was
needed far more widely than predicted — Antioquia arrived as 11 numbered parts, Cauca as 6.

### 1.2 The two selection strategies actually used

Two different strategies were issued, in sequence, and both are visible in the delivered data:

1. **Curated target list (Cauca side, TWILL).** `data/raw/observed/precip/dhime_target_stations.csv`
   — **684 stations**, selected as: **at most 2 stations per 0.25° cell**, **installed before 2011**,
   ranked by category and operating status, with columns `priority` and `assigned_to`. This yielded
   the ~157 clean Cauca-side stations.
2. **Department sweep (Magdalena side, Omar).** No per-station selection at all — filter by
   `Departamento`, select every station DHIME returns, one zip per department. Paste-ready code lists
   for cross-checking: `OMAR_magdalena_codes.txt`, `OMAR_all_codes.txt`, `TWILL_all_codes.txt`
   (all in `data/raw/observed/precip/`).

> **Why this matters and is worth keeping.** The station-selection *rule* (≤2 per 0.25° cell,
> pre-2011 install) is the only record of why the gauge network has the spatial structure it has —
> and that structure is exactly what `docs/23_gauge_geometry.md` audits (co-located gauges,
> energy-floor triage) and what caps `r ≈ 0.57` in `docs/22`. The list files themselves live under
> `data/raw/`, which is **gitignored** — so before this file, the rule existed nowhere in version
> control.

### 1.3 The work split (why coverage is uneven)

*From the precipitation protocol, Table 2 — the priority ordering was driven by a viability check on
the automatic network:*

| Person | Priority | Hydrographic zones | Stations |
|---|---|---|---|
| TWILL | 1 — GAP (automatic network empty here) | Cauca · Nechí · Bajo Magdalena-Cauca-San Jorge | 217 |
| Omar | 1 — GAP (automatic network empty here) | Cesar · Bajo Magdalena | 128 |
| Omar | 2 — has automatic backup | Alto Magdalena · Medio Magdalena · Sogamoso · Saldaña | 339 |

Omar's department list, with the catalogue upper bound on station count (the document warns the
actual yield is far lower because *"most catalogue stations have no conventional daily series"*):

| # | Department | ~catalogue stations | Main zone(s) | Save as |
|---|---|---:|---|---|
| 1 | Cundinamarca | ~416 | Alto / Medio Magdalena | `cundinamarca_2008-2018.zip` |
| 2 | Huila | ~223 | Alto Magdalena | `huila_2008-2018.zip` |
| 3 | Cesar | ~198 | Cesar, Medio Magdalena | `cesar_2008-2018.zip` |
| 4 | Boyacá | ~185 | Sogamoso, Medio Magdalena | `boyaca_2008-2018.zip` |
| 5 | Bogotá D.C. | ~155 | Alto Magdalena | `bogota_2008-2018.zip` |
| 6 | Magdalena | ~102 | Bajo Magdalena, Cesar | `magdalena_2008-2018.zip` |
| 7 | Atlántico | ~75 | Bajo Magdalena | `atlantico_2008-2018.zip` |
| 8 | La Guajira | ~21 | Cesar (edge) | `laguajira_2008-2018.zip` |
| 9 | Norte de Santander | ~7 | Medio Magdalena | `nortedesantander_2008-2018.zip` |

*(La Guajira was later excluded from the soil/URH domain — it drains to the Caribbean, not to
Magdalena-Cauca; see `notebooks/05` `SKIP_DEPTS` and `src/build_soil_layer.py`.)*

### 1.4 Why conventional daily and not the automatic network

The automatic 10-minute network (Socrata dataset **`s54a-sgyg`**, pulled by
`src/download_precip_automatic.py`) is scriptable but **raw/unvalidated and sparse in 2011**. The
viability check found it *only covers the Magdalena main stem* — it passes the ENSO wet/dry test
there but has almost no stations in the Cauca system or the lowlands. DHIME conventional daily was
therefore prioritised **exactly where the automatic network is empty**. (The `s54a-sgyg` route was
re-verified live and re-costed much later, in `docs/36 §sub-daily`.)

### 1.5 Quality instructions issued to the collectors

- Daily totals in mm; **blanks and sentinels (e.g. `-999`) are missing, not zero.**
- Record per-station completeness (days present out of 365/731).
- Prefer stations covering **both** 2011 and 2015–16, and still *Activa*; but **keep the spatial
  spread** — *"don't drop a whole cell, even a mediocre gauge beats an empty gap. Good spatial
  spread matters more than raw count: a correction is only as good as its coverage of the ungauged
  gaps."*

> ⚠ **This instruction is the origin of a defect.** "Blanks are missing, not zero" was correct for
> the *values*, but nobody was told to check for **absent rows**. `docs/16 §4.1` later found
> **70 of 294 stations contained only rain days** — DHIME never exported their dry days at all. The
> per-station completeness check requested above cannot see that; only the neighbour-ratio test in
> `src/repair_precip_zero_suppression.py` can. Keep the two failure modes distinct.

---

## 2 — Suspended sediment via DHIME: the parts no Markdown doc covers

*Source: `Protocolo_descarga_SEDIMENTOS.docx`.*

`docs/12_sediment_data_status.md` records the *outcome* (which departments, which stations, which
years). These are the *operating limits* that produced it:

- **The variable.** Descripción → **"Concentración media diaria" (Kg/m³)**. **NOT "Concentración
  superficial promedio diario"** — that product is almost empty and misses the study years
  (independently measured and written up in `docs/10`, *Finding 2026-07-28*).
- **Per-download limits (Diario type): ~50 stations and ~30 years.** Over either limit, split into
  batches `ssc_<dep>_1.csv`, `ssc_<dep>_2.csv`.
- **Pre-1990 records need a second batch.** Standard window is `1990-01-01 → 2018-12-31`. If a
  station has data before 1990, run a second pass `1970-01-01 → 1989-12-31`:
  *"el histórico antiguo es muy valioso para las curvas de gasto sólido."* This is why files like
  `ssc_santander_1968_2014.csv` and `ssc_bolivar_1979_1984.csv` exist.
- **Row filter in the station table:** select all, then deselect (a) códigos not starting 21–29 and
  (b) **rows with a blank `FechaFin`**.
- **Non-basin códigos to expect per department:** Cundinamarca and Boyacá 3× Orinoco;
  Norte de Santander 16× Catatumbo; Cauca / Valle del Cauca 5× Pacífico.
- **Do not open the CSV in Excel** — *"Conservar el CSV tal como lo entrega el portal"*. Excel
  corrupts dates and separators. (`docs/12` confirms the delivered files kept `.` decimals and were
  not Excel-damaged; the `DD/MM/YYYY` layout in Cundinamarca is a **portal** quirk, not Excel.)

**Assignment (11 remaining departments).** *Already downloaded and explicitly not to be redone:*
Huila, Cauca, Caldas, Antioquia, Santander, Bolívar, Valle del Cauca.

| # | Department | Owner | Expected file |
|---|---|---|---|
| 1–5 | Tolima, Quindío, Risaralda, Cundinamarca, Boyacá | TWILL | `ssc_tolima.csv` … `ssc_boyaca.csv` |
| 6–11 | Norte de Santander, Cesar, Córdoba, Sucre, Magdalena, Atlántico | Omar | `ssc_nsantander.csv` … `ssc_atlantico.csv` |

*(Outcome per `docs/12`: N. de Santander had no 21–29 stations, Sucre was not in the dropdown, and
Atlántico was never delivered.)*

---

## 3 — Discharge via DHIME: what differs from `docs/11`

*Source: `Protocolo_descarga_IDEAM_Magdalena.docx`.*

`docs/11_discharge_download_tracker.md` supersedes this document on every operational point and adds
the per-department results. Only three things are not in `docs/11`:

1. **The date window originally issued was `1980-01-01 → 2018-12-31`** ("39 years, under the ~50-year
   limit of the Diario type"). `docs/11` uses `1990-01-01 → 2018-12-31` and states the cap as **~30
   years, with 40/50 rejected**. See §7 — the two disagree, and `docs/11` is the one written from
   observed portal rejections.
2. **The rationale for pulling the full history rather than only 2011 / 2015–16:** calibration and
   validation use all observations, and the discharge record later feeds the solid-transport rating
   curves `Qs = a·Q^b` used to reconstruct sediment in the study years.
3. **The zone-29 warning, stated as the single most important thing not to forget:** *"⚠ No olvidar
   las zonas 28 (Cesar) y 29 (Bajo Magdalena) — la zona 29 contiene Calamar, la estación de salida de
   toda la cuenca, la más importante."* `docs/11` carries the zone table with Calamar marked, so this
   survives.

The 18-department TWILL/Omar split in this document is reproduced, with results, in `docs/11`'s
department table. Nothing is lost.

---

## 4 — IGAC soils: what differs from `docs/08` and `src/download_igac_soils.py`

*Source: `Guia_descarga_suelos_IGAC.docx`.*

The QGIS click-path in that document is **superseded** by `src/download_igac_soils.py`, which hits
`https://mapas.igac.gov.co/server/rest/services/agrologia/{svc}/MapServer/0/query` directly, pages at
the service `maxRecordCount` of 2000, and carries the **exact, server-verified** service names (the
document only had guesses, warning that *"the article de/del varies"* — the script also records the
one real trap, `...departamentodeSantander` with a capital S). `docs/08 §3` already has the manual
QGIS/ArcGIS-REST route and the EPSG:9377 note.

Three things were only in the document:

### 4.1 The quantitative reason SoilGrids was rejected

> *"SoilGrids (250 m global model) is far too uniform for this basin: cross-checked against the IGAC
> field survey it agrees only **49 %** of the time and labels **~99 %** of the area 'Fine', erasing
> the real **Coarse (19 %)** and **Medium (32 %)** soils IGAC maps."*

`notebooks/05_landcover_soils_reclass.ipynb` states this qualitatively (*"collapses the great
majority of the basin into a single 'Fine' class — kept only as a gap-fill where IGAC has no
coverage"*) and `figures/igac_vs_soilgrids.png` shows it. The four percentages appear nowhere else in
the repository. **They are transcribed, not re-derived** — treat them as the document's claim, and
re-measure from notebook 05 before quoting them in a report.

### 4.2 The one acceptance check on a downloaded layer

Open the exported layer's attribute table and confirm the column **`CARACTERÍSTICAS_SUELOS`** exists
and is populated — it is the free-text texture field (*"arcillosa"*, *"texturas medias y finas"*,
*"gruesa"*…). If it is empty you added the wrong layer: pick the **soil-units (UCS) polygon** layer,
not a raster or an index layer. Export with **all** fields kept.
*(The field name is in the `src/download_igac_soils.py` docstring; the check as an acceptance
criterion was only in the document.)*

### 4.3 Fallback source and department status

- **Fallback if the ArcGIS REST route stalls:** **Colombia en Mapas**
  (`colombiaenmapas.gov.co`) also serves IGAC soils for download; the §4.2 attribute check still
  applies. This URL appears nowhere else in the repository.
- **Already downloaded (northern basin), not to be redone:** Antioquia, Bolívar, Córdoba, Magdalena,
  Cesar, Sucre, Atlántico. **To download (Andean upper basin, where soils vary most):** Huila,
  Tolima, Cauca, Cundinamarca, Boyacá, Caldas, Risaralda, Quindío, Valle del Cauca, Norte de
  Santander — the same ten that `src/download_igac_soils.py` now automates (plus Santander).
- IGAC delivers **EPSG:9377 (MAGNA-SIRGAS Origen-Nacional)**; leave it, the pipeline reprojects.

---

## 5 — `Explanation_script_MGB_SA_Magdalena.pdf` — KEEP, do not delete

*8 pages, gitignored, untracked, generated from `notebooks/06_data_inventory.ipynb` (which **is**
tracked). Every distinctive number in it — 1,130,236 clean discharge rows / 167 stations, 269,305
sediment rows / 77 stations, the +1.70σ / −1.02σ / −0.64σ ENSO anomalies over 102 long-record
stations, the 33 paired rating curves with median R² ≈ 0.5 — traces to that notebook and to
`docs/17`, `docs/19`, `docs/34`.*

It is nevertheless **an active citation** in a live pre-registration and must stay on disk:

- `docs/35_qpeak_preregistration.md` cites it twice, load-bearingly: for *"30 m over the whole basin
  exceeds the tool's cell limit"* (why the 30 m DEM is only a lower-Magdalena window) and for
  *"slope feeds the MUSLE LS factor"* (evidence that slope's intended role is LS2D / C3.1 and never
  `q_peak`).
- `docs/agents/journal_c32-cp.md` and `journal_c33-qpeak.md` record it as *the only PDF in the repo*
  — the negative result that Fagundes et al. (2026) is not available locally.

Its own content is otherwise **superseded**: it predates the domain correction (`docs/15`), still
describes soils as SoilGrids (replaced by IGAC, §4 above) and lists the eastern domain box as the one
open item. Do not cite it for anything except the two sentences `docs/35` already quotes.

---

## 6 — Adjudication summary

| File | Tracked | Unique knowledge found | Extracted to | Disposition |
|---|---|---|---|---|
| `Protocolo_descarga_PRECIPITACION.docx` | tracked | precipitation portal settings; ≤2-per-0.25°-cell / pre-2011 selection rule; 684-station target list; TWILL/Omar priority split; `s54a-sgyg` viability rationale | §1 | propose removal |
| `Protocolo_descarga_PRECIPITACION_OMAR.docx` | untracked (gitignored) | `http`-not-`https` portal quirk; department sweep + zip names; 11-year query split rule; catalogue-vs-actual warning | §1.1, §1.3 | propose removal (no-op in git; delete on disk in a later session) |
| `Protocolo_descarga_SEDIMENTOS.docx` | tracked | ~50-station / ~30-year Diario limits; the 1970–1989 second-batch rule; blank-`FechaFin` filter; non-basin código counts per department; the do-not-open-in-Excel rule; the 7 already-done departments | §2 | propose removal |
| `Protocolo_descarga_IDEAM_Magdalena.docx` | tracked | 1980–2018 window + "~50-year cap" claim (conflicts with `docs/11`); full-history rationale; zone-29/Calamar warning | §3, §7 | propose removal |
| `Guia_descarga_suelos_IGAC.docx` | untracked (gitignored) | SoilGrids-vs-IGAC 49 % / 99 % / 19 % / 32 %; `CARACTERÍSTICAS_SUELOS` acceptance check; `colombiaenmapas.gov.co` fallback; already-done department list | §4 | propose removal (no-op in git; delete on disk in a later session) |
| `Explanation_script_MGB_SA_Magdalena.pdf` | untracked (gitignored) | none unique — but **actively cited** by `docs/35` | §5 | **KEEP on disk** |

---

## 7 — Contradictions surfaced by the comparison

Both are **new** and unresolved; neither is resolved by this document.

**(a) The DHIME Diario date-range cap.**
`Protocolo_descarga_IDEAM_Magdalena.docx` §3: *"Ajustar Fechas = 1980-01-01 → 2018-12-31 (39 años,
bajo el límite de ~50 años del tipo Diario)"*.
`docs/11_discharge_download_tracker.md` line 31: *"`1990-01-01 → 2018-12-31` (29 yr — the Daily type
caps at **~30 years**; 40/50 are rejected)"*.
`Protocolo_descarga_SEDIMENTOS.docx` sides with `docs/11` (*"~30 años por descarga"*), and the
delivered filenames (`caudal_*.csv` at 1990–2018, `ssc_santander_1968_2014.csv` split at 1990) are
consistent with a ~30-year cap. **Resolution:** `docs/11` is authoritative — it was written from
observed portal rejection messages; the 50-year figure in the .docx was an untested assumption issued
before the first download. No committed number changes.

**(b) Which sediment parameter to request.**
`docs/10_ideam_download_recipe.md` (lines 11, 26) instructs: *Descripción → "Transporte medio diario
**a partir de la CM**"*.
`Protocolo_descarga_IDEAM_Magdalena.docx` §5 instructs the opposite: *"Evitar los parámetros «a
partir de la CM» (producto derivado, casi vacío)"*.
**Resolution:** neither was the variable finally used. `docs/12` and `docs/19_sediment_qc_audit.md`
(the DHIME variable/units rule box) establish that the
project runs on **CM = "Concentración media diaria" (Kg/m³)**, the *measured* depth-averaged
concentration — not on any *"a partir de la CM"* derived transport product and not on *"Concentración
superficial promedio diario"*. `docs/10`'s instruction is stale and predates the CM breakthrough; the
.docx's warning is right in spirit but names the wrong villain. **Recommendation for a later
session:** add a one-line dated amendment at the top of `docs/10` pointing at `docs/12`. Not done
here — `docs/10` is outside this agent's remit and the fix should be reviewed, not slipped in.

---

## 8 — Files these protocols refer to that are gitignored

Listed so a future reader knows the referenced artifacts exist on disk but not in version control:

- `data/raw/observed/precip/dhime_target_stations.csv` (the 684-station curated list, with `priority`
  and `assigned_to`)
- `data/raw/observed/precip/{TWILL,OMAR}_all_codes.txt`, `OMAR_magdalena_codes.txt`,
  `twill_priority1_codes.txt` and their `_stations.csv` counterparts
- `data/raw/observed/precip/dhime/*.zip` (the department downloads, many split into numbered parts)
- `data/raw/observed/caudal/caudal_<dept>.csv`, `data/raw/observed/sedimento/ssc_<dept>.csv`
- `data/raw/soils/suelos_<dept>.gpkg`

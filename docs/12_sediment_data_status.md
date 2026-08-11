# Sediment data status — BREAKTHROUGH (variable CM)

> **STATUS — SUPERSEDED.** The "variable CM" discovery below stands, but every coverage claim here has been replaced by measurement: QC and the honest ceiling in [docs/19](19_sediment_qc_audit.md), and **which stations are actually usable** in [docs/32 §R6](32_ssc_qc_audit.md) (79 classified · 28 mapped · 6 usable + 12 with caveat). Its "Phase C blocked" framing is superseded by [docs/30 §1](30_phase_c_plan.md). Entry point: [docs/00_INDEX.md](00_INDEX.md).

A colleague retrieved IDEAM sediment as the variable **CM = "Concentración media diaria" (kg/m³)** — the *mean daily
suspended-sediment concentration*. This is far richer than the earlier "Concentración superficial promedio diario"
(which was sparse and did not cover the study years). Files live in `data/raw/observed/sedimento/`.

## Why this matters

The sediment-data risk that was blocking Phase 3 is **largely resolved**: we now have observed daily sediment
concentration in **both study years**, across several sub-basins, at tributary stations — exactly what the
tributary-calibration / rating-curve plan needs. The lower-Magdalena mainstem still lacks sediment (known limitation),
but tributary coverage is now good.

## Coverage by study year

**2011 (La Niña):**
- `ssc_santander_1968_2014.csv` — **9 stations, all cover 2011** (Sogamoso/Opón: EL JORDAN, LA CEIBA, NEMIZAQUE,
  PUENTE CABRA, PUENTE ARCO, SAN BENITO, PUENTE NACIONAL, PUERTO ARAUJO, PUENTE FERROCARRIL). 57 680 rows.
- `ssc_cauca_2001_2015.csv` — JULUMITO (…2011), PUENTE ARAGÓN (…2015) — upper Cauca.
- `ssc_valledelcauca_hist.csv` — MATEGUADUA (…2011).

**2015–2016 (El Niño):**
- `ssc_huila_2015_2018.csv` — 8 stations cover 2015/16 (upper Magdalena headwaters).
- `ssc_caldas_2015_2018.csv` — IRRA, PAILA, PUENTE NEGRO (Cauca).
- `ssc_antioquia_2015_2018.csv` — 5 stations incl. BOLOMBOLO (Cauca mainstem).
- `ssc_cauca_2001_2015.csv` — PUENTE ARAGÓN (2015).
- `ssc_santander_2015_2018.csv` — some stations reach 2016.

**Historic only (for rating curves, any year):** `ssc_bolivar_1979_1984.csv` (LAS VARAS), Valle JUANCHITO/LA VICTORIA.

## Stations with BOTH discharge and sediment (ideal for rating curves Qs–Q)

Several sediment stations are also in our caudal files → direct rating-curve fitting, e.g.:
- **21147030 CARRASPOSO** (Huila) — caudal + ssc
- **26167070 IRRA** (Caldas) — caudal + ssc
- **26017020 JULUMITO**, **26017060 PUENTE ARAGÓN** (Cauca) — caudal + ssc
- Santander Sogamoso stations (24037360 EL JORDAN, 24017640 LA CEIBA, …) — match against Omar's Santander caudal.

## Update (download completed by TWILL + Omar)

Additional departments downloaded with the correct **CM** variable, all códigos catalog-verified (21-29):

| dept | file | stations | 2011 | 2015-16 | note |
|------|------|---------:|:----:|:-------:|------|
| Tolima | ssc_tolima.csv | 9 | ✓ | ✓ | 5 overlap Tolima caudal (rating curves) |
| Quindío | ssc_quindio.csv | 1 | ✓ | ✓ | EL ALAMBRADO — also in caudal |
| Risaralda | ssc_risaralda.csv | 2 | ✓ | ✓ | incl. LA VIRGINIA (Cauca mainstem) |
| Cundinamarca | ssc_cundinamarca.csv | 6 | ✓ | ✓ | ⚠ dates in **DD/MM/YYYY** (portal quirk, not Excel; values OK) |
| Boyacá | ssc_boyaca.csv | 7 | ✓ | ✓ | Sogamoso headwaters |
| Cesar | ssc_cesar.csv | 3 | – | – | historic only (→2000/2014) |
| Córdoba | ssc_cordoba.csv | 2 | – | – | historic only |
| Magdalena | ssc_magdalena.csv | 8 | ✓ | – | lower-basin, cover 2011 |

**Empty / no basin stations (skip):** Norte de Santander (no 21-29), Sucre (not in dropdown).
**Pending:** Atlántico (Omar reports ~3 stations; file not yet delivered).

> Processing note: sediment CSVs mix two date formats — `YYYY-MM-DD` (most) and `DD/MM/YYYY` (Cundinamarca). Parse
> robustly. Valor uses `.` decimals throughout (no Excel corruption).

## To do
- Match sediment stations to discharge stations basin-wide; list pairs usable for rating curves.
- (Optional) also pull the same CM variable for the remaining departments for completeness.
- All códigos are basin (21-29); no non-basin found in the sediment set.

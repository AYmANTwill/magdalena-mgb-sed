# IDEAM discharge download tracker — Caudal medio diario

Goal: daily discharge (`Caudal medio diario`) for **every station in the Magdalena-Cauca basin**, full
historical record, to calibrate/validate MGB-SA hydrology (split-sample) and to feed the sediment rating curves.

Portal: **DHIME** (https://atencionciudadano.ideam.gov.co/). Manual, one department at a time. Reload (F5) between
departments so the portal stays responsive.

## The basin filter — código 21-29

A station belongs to the Magdalena-Cauca basin if its **código starts with 21-29** (Área Hidrográfica 2):

| zona | name | zona | name |
|----|------|----|------|
| 21 | Alto Magdalena | 26 | Cauca |
| 22 | Saldaña | 27 | Nechí |
| 23 | Medio Magdalena | 28 | Cesar |
| 24 | Sogamoso | 29 | Bajo Magdalena (**Calamar / outlet**) |
| 25 | Bajo Magdalena-Cauca-San Jorge | | |

Some border departments (Boyacá, Cundinamarca, Santander, N. de Santander, Cauca) also have stations draining to
the **Orinoco (3x)** or **Catatumbo (16x)** — **discard any código NOT starting 21-29**.

## Recipe (repeat per department)

1. **Consultar** → Variable = **Caudal medio diario**.
2. **Descripción** → the daily parameter (usually one).
3. **Datos Estación**: Departamento = *[dept]*, Municipio = **Todo**, Nombre = **Todo** → **Filtrar**.
4. In the station table, select all → then **deselect** (a) rows whose **código does not start 21-29** and
   (b) rows with a **blank FechaFin**.
5. **Descargar** → **Ajustar Fechas** = `1990-01-01 → 2018-12-31` (29 yr — the Daily type caps at **~30 years**; 40/50 are rejected) → **CSV**.
6. Save into `data/raw/observed/caudal/` as **`caudal_<depto>.csv`** (e.g. `caudal_santander.csv`).
7. F5, next department.

> **Station-count limit (~50 per download, Daily type).** DHIME rejects a daily request with too many stations
> ("Ha superado el límite: Número de estaciones ... Ingresó NN Estaciones"). If a department has >~50 stations,
> split into batches of ~25-26 and save as `caudal_<depto>_1.csv`, `caudal_<depto>_2.csv` (merged on ingest).
> Same idea if a big request stalls: split by stations, or by date windows (1990-2003 / 2004-2018).

## Departments (ordered roughly upstream → downstream)

| # | Department | Status | File | Notes (n stations kept) |
|---|-----------|--------|------|-------------------------|
| 1 | Huila | ✅ | caudal_huila.csv | 52 selected → 6 with 1990-2018 data (rest empty in range). **+ CALAMAR [29037020] outlet captured here (bonus)** |
| 2 | Tolima | ✅ | caudal_tolima.csv | 2 real batches, **18 stations** (código 21/22/23), all verified Tolima. Cover 2011:12 2015:11 2016:11 |
| 3 | Cauca | ✅ | caudal_cauca.csv | Redone correctly: 2 batches, 17 stations (código 21+26), all verified Cauca/Magdalena-Cauca |
| 4 | Valle del Cauca | ✅ | caudal_valle.csv | Redone: 5 stations (código 26), verified Valle/Magdalena-Cauca |
| 5 | Caldas | ✅ | caudal_caldas.csv | 9 stations (all código 26 = Cauca), verified all officially Caldas |
| 6 | Risaralda | ✅ | caudal_risaralda.csv | 7 stations (código 26), verified all officially Risaralda; disjoint from Caldas |
| 7 | Quindío | ✅ | caudal_quindio.csv | 2 stations (código 26), verified officially Quindío / Magdalena-Cauca |
| 8 | Cundinamarca | ✅ | caudal_cundinamarca.csv | Redone: 9 stations (21/23/24), verified Cundinamarca/Magdalena-Cauca |
| 9 | Boyacá | ✅ | caudal_boyaca.csv | 2 batches, 16 stations (código 23/24), verified Boyacá/Magdalena-Cauca. Dropped `24017720` (código 24 but officially **Orinoco** in catalog — code heuristic fooled, catalog is authority) |
| 10 | Antioquia | ✅ (Omar) | caudal_antioquia.csv | 3 batches → 24 stations (23/25/26/27), all verified Antioquia/Magdalena-Cauca. Cover 2011:12 15/16:12 |
| 11 | Santander | ✅ (Omar) | caudal_santander.csv | 3 batches → 25 stations (23/24). Dropped `37017010` (Orinoco). Covers 2011:10, 15/16:10 |
| 12 | Norte de Santander | ✅ (Omar) | caudal_nsantander.csv | 1 station (23) — most of N.Santander drains to Catatumbo, so few basin stations |
| 13 | Cesar | ✅ (Omar) | caudal_cesar.csv | 8 stations (23/25/28) |
| 14 | Córdoba | ✅ (Omar) | caudal_cordoba.csv | 3 stations (25) |
| 15 | Sucre | ❌ MISSING | | **Not in Omar's folder — still to download** (código 25) |
| 16 | Bolívar | ✅ (Omar) | caudal_bolivar.csv | 8 stations (25/29), all cover both study years |
| 17 | Magdalena | ✅ (Omar) | caudal_magdalena.csv | 8 stations (25/28/29) |
| 18 | Atlántico | ✅ (Omar) | caudal_atlantico.csv | 1 station (29 = Calamar outlet) — Atlántico has few basin caudal stations |

Tick a box, drop the file in `caudal/`, and I verify coverage (esp. 2011 & 2015-16) after each one.

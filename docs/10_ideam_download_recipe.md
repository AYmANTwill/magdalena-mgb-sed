# IDEAM / DHIME download recipe (discharge + sediment)

Portal: **https://atencionciudadano.ideam.gov.co/** (accept the terms once). The portal is heavy and freezes after a
full cycle — **reload (F5) between departments** to keep it responsive. It is not reliably automatable; do it by hand
(the flow is fast once you know it — validated below).

## The recipe (repeat per department)

1. **Consultar** tab → Serie de Tiempo = **Estándar**.
2. **Variable** → type in the search box to filter → pick the variable (see list below).
3. **Descripción** → pick the daily parameter (for sediment: **"Transporte medio diario a partir de la CM"**).
4. **Datos Estación**: Departamento = *[department]*, Municipio = **Todo**, Nombre = Todo → **Filtrar**.
5. If stations appear under **"Seleccione las estaciones a descargar"** → click the **header checkbox** (top-left of the
   table) to select **all** of them. (If the table is empty, that department has no station for this variable — skip it.)
6. **Descargar** tab → set **Periodo** to the full range (e.g. `1970-01-01` → `2018-12-31`) → format **CSV** → **Descargar**.
7. Move the file from your browser **Downloads** folder into `data/raw/observed/`, renamed clearly
   (e.g. `sedimentos_transporte_santander.csv`).
8. Reload the page (F5) and do the next department.

> Speed tip: **"Agregar Otros"** on the Descargar tab lets you accumulate several department/variable selections into a
> single CSV before downloading — fewer files. But per-department downloads are safer if the portal stalls.

## Variables to download

**Sediment (priority — the limiting data):**
- **Transporte de sedimentos** → "Transporte medio diario a partir de la CM"
- **Concentración de sedimentos en suspensión** (some stations have this but not transport)

**Discharge:**
- **Caudal medio diario**

## Departments to iterate

**Sediment** (only these tend to have stations — the rest are empty, skip fast):
Santander *(key — Sogamoso/Lebrija, records to 2018: EL JORDAN, LA CEIBA, MERIDA, NEMIZAQUE, PUENTE ARCO, PUENTE CABRA
— cover 2011 & 2015–16)*, Antioquia, Cesar, Magdalena, Boyacá, Cundinamarca, Tolima, Huila, Cauca, Valle del Cauca.

**Discharge** (all basin departments): Huila, Tolima, Cundinamarca, Caldas, Antioquia, Santander, Boyacá, Cesar,
Bolívar, Magdalena, Atlántico, Sucre, Córdoba, Cauca, Valle del Cauca, Risaralda, Quindío, Norte de Santander.

## Finding (2026-07-28): daily sediment series is too sparse for the study years

Downloaded **"Concentración superficial promedio diario de sedimentos"** for Santander (1990–2018).
The result is a **derived daily product** that IDEAM computed only for scattered station-years: the whole
Santander batch returned **275 rows total** — EL JORDAN 2017-01→08 (continuous), MONAS 2004-02, CARARE 1999-08,
NEMIZAQUE 2018-01. A targeted test (EL JORDAN, 2011) returned **"no hay información"** → the daily series does
**not** cover 2011 (nor, likely, 2015–16).

Also: the Consultar **"Cantidad Probable"** column is *not* a record count — it is the day-span between FechaIni
and FechaFin (EL JORDAN 1974→2021 ≈ 17 270 days ≈ the "17272" shown). It says nothing about actual data volume.

**Consequence:** direct daily-sediment validation in the study years is not available from this product — this is
the known sediment-data limitation already escalated to the advisor. Sediment calibration will instead rely on a
**rating curve Qs–Q** built from whatever aforos exist (all years). **Hydrology (discharge) is calibrated first**,
so priority pivots to **Caudal medio diario**. Keep the sparse concentration file (`concentracion_diaria_santander.csv`)
for the rating curve. Resume the sediment dig after the advisor confirms the calibration path.

## Why full records (not just 2011 & 2015–16)

Calibration uses **all** available observations, not only the comparison years. The complete series (1990s→2018) gives a
robust calibration/validation record and keeps both study-year options open. See `docs/09` / journal.

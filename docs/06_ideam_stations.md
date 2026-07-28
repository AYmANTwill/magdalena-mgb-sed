# IDEAM sediment & discharge stations — Magdalena (Q1 findings)

Findings from a literature scan on 2026-07-27. Data are downloaded from the IDEAM **DHIME** portal.

## Key stations

- **Calamar** — downstream reference gauge, **112 km upstream of the Caribbean mouth** (~10.25° N). The integrating
  outlet for basin sediment flux. Long records: discharge from **1942**; suspended sediment used in the literature for
  **1975–1995** and **1990–2010**. Mean annual suspended sediment load **~145–169 Mt/yr**. The reference station in the
  Magdalena sediment literature (Restrepo, Higgins, Kjerfve).
- **Puerto Berrío** — mid-basin, two IDEAM stations (codes **23095010** and **23090110**); suspended sediment measured
  (e.g. 2004–2005 in one study). Natural candidate for the **pilot outlet**.
- **Network** — IDEAM holds daily discharge + suspended-sediment concentration + transport for many stations; the
  literature cites **30–40+ sediment sites** across the sub-basins of the Magdalena-Cauca system.

## Data source: DHIME

- **DHIME** (Sistema para la Gestión de Datos Hidrológicos y Meteorológicos), live since Oct 2018: free consultation and
  download of IDEAM time series — level, discharge, **sediment concentration & transport**, granulometry, cross-section
  profiles, rating curves.
- **Catálogo Nacional de Estaciones del IDEAM** (on datos.gov.co): full station list with coordinates, type and
  operating period → use it to shortlist sediment stations by location and record length.

## Q1 assessment

- **Good news:** an extensive IDEAM suspended-sediment network exists; Calamar has a long, well-documented record; data
  are free to download via DHIME. The "no data → no project" risk drops from red to roughly green.
- **Still to verify (the real remaining check):** temporal coverage for the **study years** — confirm that Calamar (and a
  mid-basin station such as Puerto Berrío) have **suspended-sediment** records for **2011** (La Niña) and **2015–2017**
  (El Niño). Sediment is sampled less often than discharge, so this must be checked directly on DHIME.

## Relevant sediment literature (Magdalena)

- Restrepo et al. — *Sediment load trends in the Magdalena River basin (1980–2010): anthropogenic and climate-induced causes.*
- Higgins et al. — *Suspended sediment transport in the Magdalena River: hydrologic regime, rating parameters, effective discharge.*
- Restrepo & Kjerfve — *Magdalena River: interannual variability (1975–1995), revised water discharge and sediment load estimates.*
- *Efectos naturales y antrópicos en la producción de sedimentos de la cuenca del río Magdalena* (Rev. Acad. Colomb. Cienc.).

## Magdalena mainstem stations (catalogue sweep, 2026-07-28)

Decision taken: **stay on the Magdalena** (Paths A/B only). Full mainstem gauge chain pulled from the IDEAM catalogue
(`corriente = MAGDALENA`, source→mouth). Realistic **suspended-sediment candidate stations** (major, historically
monitored) to check in DHIME for record coverage:

| Station | Code | ~Lat | Notes |
|---|---|---|---|
| Puerto Salgar | 23037010 | 5.47 | Cundinamarca, mid basin |
| Puerto Berrío | 23097030 | 6.49 | Antioquia, mid basin — classic sediment gauge |
| Barrancabermeja | 23157030 | 7.06 | Santander, mid basin — classic sediment gauge |
| Gamarra | 23217080 | 8.28 | Cesar, lower-mid |
| El Banco | 25027020 | 8.99 | Magdalena dept, lower (near Cauca junction) |
| Plato | 25027450 | 9.79 | Magdalena dept, lower |
| Calamar | 29037020 | 10.24 | lower — **discharge only, no sediment (confirmed)** |

**Still to determine (DHIME, per-station):** which of these has a suspended-sediment record, and its FechaIni/FechaFin.
Literature (Restrepo, Higgins) suggests strong records but many ending ~2010 → if so, **Path B** (a pre-2010 ENSO pair)
becomes the realistic route; if any reaches 2015–2016, **Path A** with current years stays open.

## Next action

On DHIME: open the station catalogue, filter to the Magdalena for **sediment (transporte de sedimentos / concentración)**,
locate Calamar + candidate mid-basin stations, and record their **available years** vs 2011 and 2015–2017.

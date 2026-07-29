# Discharge ↔ sediment station pairing (for calibration / rating curves)

Cross-match of all `caudal/*.csv` (143 discharge stations) against `sedimento/*.csv` (39 sediment stations,
variable CM = daily mean concentration, kg/m³). "Common days" = dates where the station has BOTH a discharge value
and a concentration value — the points usable to fit an empirical rating curve.

## A. Stations with BOTH discharge and sediment (10) — direct rating-curve candidates

| código | name | common Q&Sed days | in 2011 | in 2015-16 |
|--------|------|------------------:|--------:|-----------:|
| 24027030 | NEMIZAQUE | 6449 | 301 | 0 |
| 26107130 | MATEGUADUA | 3075 | 109 | 0 |
| 26017060 | PUENTE ARAGÓN | 2568 | 201 | 33 |
| 26107070 | LA VICTORIA | 1703 | 0 | 0 |
| 26017020 | JULUMITO | 1367 | 0 | 0 |
| 26167070 | IRRA | 993 | 0 | 304 |
| 26067010 | JUANCHITO | 925 | 0 | 0 |
| 26167060 | PAILA LA | 551 | 0 | 360 |
| 24027070 | MERIDA | 342 | 0 | 0 |
| 21147030 | CARRASPOSO | 214 | 0 | 214 |

All 10 have ≥30 common days (enough to fit Qs = a·Q^b). Study-year rating curves: **2011** → NEMIZAQUE, MATEGUADUA,
PUENTE ARAGÓN; **2015-16** → PUENTE ARAGÓN, IRRA, PAILA, CARRASPOSO.

## B. Key point — most sediment is usable WITHOUT co-located discharge

MGB-SED outputs suspended-sediment **concentration**, and our observations are **concentration (kg/m³)** too. So the
model can be validated by **direct concentration comparison** at every sediment station — no discharge needed at that
station. Co-located discharge (section A) only enables *independent* empirical rating curves (a bonus/cross-check).

## C. Sediment stations lacking discharge but covering a study year (21) — optional targeted Caudal download

If we want independent rating curves at these too, download `Caudal medio diario` for these specific station codes.

**Cover 2011 (Sogamoso/Opón — La Niña):** 23127020 PUERTO ARAUJO, 23147020 PUENTE FERROCARRIL, 24017570 SAN BENITO,
24017590 PUENTE NACIONAL, 24017640 LA CEIBA, 24027040 PUENTE CABRA, 24027060 PUENTE ARCO, 24037360 EL JORDAN.

**Cover 2015-16 (upper Magdalena / Cauca — El Niño):** 21027010 PERICONGO, 21037010 PUENTE GARCES, 21057060 PAICOL,
21087040 HIDROELECTRICA, 21087080 HACIENDA VENECIA, 21097070 PUENTE SANTANDER, 21147050 PUENTE VENADO,
23057140 SAN MIGUEL, 23087210 CANTERAS, 26147140 PUENTE NEGRO, 26187110 LA PINTADA, 26207080 BOLOMBOLO, 26237020 PENALTA.

> Note: some of these may simply not publish daily Caudal at IDEAM; where discharge is unavailable, use the
> calibrated model's simulated Q. Not a blocker for calibration.

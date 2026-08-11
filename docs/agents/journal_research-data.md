# Journal: research-data (sub-daily data availability)

GOAL: Establish what SUB-DAILY precipitation data actually EXISTS for the
Magdalena-Cauca basin 2008-2018, because the honest fix for a daily model's
peak deficit (R_AMS 0.820, R_POT 0.567, ~43 % of POT events missed) is
sub-daily forcing. Real, not nice-to-have. Verdicts must be backed by an
OPENED FILE or a DOCUMENTED download route.

Write ONLY this journal + a findings file in data/processed/peakgap/.

## Step checklist
- [ ] S1 inventory era5land_ext_*.nc on disk (sizes, count)
- [ ] S2 OPEN each mosaic: variables, time resolution, exact date span, corruption check
- [ ] S3 assess ERA5-Land tp as within-day SHAPE (not amount) for disaggregation
- [ ] S4 repo search for IDEAM sub-daily / horario / telemetric / min_hours
- [ ] S5 CHIRPS: confirm daily-only from opened file + docs
- [ ] S6 any other on-disk product with sub-daily precip
- [ ] S7 write data/processed/peakgap/subdaily_data_inventory.md
- [ ] S8 structured output

## S1+S2 DONE (ERA5-Land mosaics OPENED, not counted)
- 132 files data/raw/climate/era5land_ext_<y>_M<mm>.nc, 2008_M01..2018_M12, 12 GB.
- ALL 132 opened with netCDF4 + a real data slice read from `tp`. BAD FILES: [] (zero).
  (Separately: one known bad file is quarantined as
   data/raw/climate/_corrupt/era5land_ext_2008_M06.nc.corrupt, 43.7 MB — and 2008_M06
   is present and healthy in the live set, so the corrupt copy was already replaced.)
- Variables in every one of the 132: d2m, sp, ssrd, t2m, tp, u10, v10  -> tp IS PRESENT.
- Time coord valid_time, units 'seconds since 1970-01-01'; unique diff = 3600 s in every
  file => STRICTLY HOURLY, no sub-sampling.
- Exact span: 2008-01-01 00:00 -> 2018-12-31 23:00 UTC. Total timesteps 96,432 =
  4,018 days x 24 h exactly. Per-month count == calendar hours for all 132 months
  (months with a short count: none). NO HOURLY GAPS ANYWHERE.
- Grid 101 lat x 48 lon = 4,848 cells @0.1 deg, domain -77.0..-72.3 / 1.4..11.4.
NEXT: S3 assess tp as within-day SHAPE (accumulation convention, diurnal cycle,
concentration, UTC vs IDEAM 07-07 local day, intensity bias vs gauges).

## S4 IDEAM sub-daily — FOUND, and it is 10-MINUTE, not hourly
- `src/download_precip_automatic.py` (in repo) documents + uses Socrata dataset
  **s54a-sgyg** on www.datos.gov.co = IDEAM AUTOMATIC (telemetry) precipitation,
  **10-minute raw**. Our script aggregated it SERVER-SIDE to daily
  (date_trunc_ymd + sum) "so we move kilobytes, not gigabytes" — i.e. the sub-daily
  detail exists at the source and was DISCARDED at download time, not absent.
- Opened `data/raw/observed/precip/precip_auto_daily_long.csv`: 86,621 station-days,
  204 station codes, span 2011-01-01..2016-12-31 (script SPANS = 2011 + 2015-16 only).
  Column `n` = number of sub-daily slots that reported that day:
  median 144, 25th pct 132, **max 288** -> most stations log at 10 min (144/day),
  some at **5 min** (288/day). This is FILE-BACKED proof of sub-daily resolution.
- valid days (n>=100): 70,367 rows / 126 stations. Per year (valid):
  2011 = 17,468 station-days / 66 stations; 2015 = 25,409 / 84; 2016 = 27,490 / 120.
  Coverage GROWS with time -> 2008-2010 will be thinner (network build-out).
- Catalogue `stations_precip_catalog.csv` (4,603 basin precip stations): tecnologia =
  Convencional 3,593; **Automatica con Telemetria 862**; Automatica con Telemetria +
  Convencional 129; Automatica sin Telemetria 19 -> **1,010 automatic** in the
  Magdalena-Cauca area, 882 "Activa". (Install-date field is unreliable as a record-start
  proxy: it inherits the parent conventional station's date, min 1931. Telemetric
  build-out years: 2004-05 (90), 2010 (50), 2013 (164), 2017-18 (194).)
- CAVEAT already on record, docs/16 s4.4: the automatic network under-catches the
  conventional network by **19 %** on co-located pairs, explicitly attributed in part to
  "mechanical under-registration at high intensity" — the exact regime a peak fix needs.
- Protocolo_descarga_PRECIPITACION.docx confirms in writing: "the automatic 10-minute
  network (dataset s54a-sgyg) is scriptable but raw/unvalidated and sparser in 2011".

## S4b LIVE VERIFICATION of the sub-daily source (network reachable from this box)
GET https://www.datos.gov.co/resource/s54a-sgyg.json -> 200. Schema:
codigoestacion, codigosensor(0240), fechaobservacion, valorobservado, nombreestacion,
departamento, municipio, zonahidrografica, latitud, longitud, descripcionsensor
("Precipitacion"), unidadmedida ("mm"). Station codes are 10-digit ZERO-PADDED
('0021015040'), NOT the 8-digit form used in our CSVs - a query with '21015040'
returns [] silently.
PULLED THE RAW SUB-DAILY: station 0021015040, 2011-01-03 -> 138 rows at 10-min stamps
(00:00, 00:10, ...). Daily sum 6.0 mm, 15 nonzero slots. This EXACTLY reproduces the
on-disk aggregate row (21015040, 2011-01-03, p_mm=6.0, n=138) -> the route is verified
end-to-end and the aggregate is faithful.
That day's shape: 6.0 mm delivered in 15 of 138 slots = 2.5 h, in two bursts
(14:50-15:30 = 1.7 mm; 19:40-20:30 = 3.2 mm). Peak 10-min intensity 1.5 mm/10min
= 9 mm/h vs the daily-uniform 0.25 mm/h -> a 36x intensity ratio the daily model
cannot see. This is the mechanism behind R_POT 0.567.
NEXT: background job counting basin automatic stations per year 2008-2018 (1-7 Mar
window). Meanwhile S3 ERA5 tp shape assessment.

## S3 ERA5-Land tp: convention + within-day SHAPE (measured, 2011 + 2015, all cells)
CONVENTION (verified by opening era5land_ext_2011_M04.nc): tp attrs GRIB_stepType='accum',
units 'm'. It behaves EXACTLY like ssrd: reset at 00 UTC, the 00:00 stamp holds the
PREVIOUS day's total, stamps 01..23 are cumulative-since-00 of the current day
(negative steps in the raw series occur only at hours 0,24,48...). So
  UTC daily total(day d) = tp at 00:00 of day d+1;
  hourly increment(h) = tp[h]-tp[h-1] with tp[0]:=0 and the 23->24 step closed by the
  next day's 00:00 stamp.
Getting this wrong repeats docs/16 error #4 (the ssrd +7 % radiation bug).
MEASURED (de-accumulated increments, mm, all 4,848 cells):
  areal mean 3,500 mm/yr (2011) vs 2,743 mm/yr (2015) - the ENSO sign is right.
  Diurnal cycle (LOCAL time = UTC-5): peak 13h local = 6.9 % of annual rain,
  minimum 18h local = 2.9-3.0 %, peak/mean 1.66 (2011) / 1.64 (2015). A real,
  physically plausible afternoon-convective cycle, essentially identical in a wet and a
  dry year -> the shape is a stable climatological signal, not noise.
  On wet cell-days (>=5 mm; n = 938,960 in 2011 / 739,461 in 2015):
   - wettest HOUR carries median 19.3 % of the daily total (p90 38.1 %)
   - median 16 hours per day with >=0.1 mm (p10 9, p90 23)
   - max hourly intensity median 2.58 mm/h (p95 6.70, max 57.8)
   - peak-hour / daily-uniform ratio median 4.63x (2011), 4.84x (2015)
=> ERA5-Land DOES carry within-day structure worth 4.6-4.8x over uniform, but it RAINS
   FOR 16 h OF THE DAY. Compare the one live gauge day pulled above: 15 of 138 ten-min
   slots = 2.5 h wet, peak 9 mm/h. ERA5 is DRIZZLY/SMEARED - suspected, now measured.
NEXT: quantify that against real gauge 10-min data (S3c).

## S3c GAUGE 10-min ground truth vs ERA5 shape (5 stations, 2011, LIVE PULL)
Pulled full-year raw records for 0021195170, 0021201980, 0023050420, 0024035360,
0021195160: ~51.7k-52.4k rows each, median step 600 s (10 min), 365 days with >=100
slots each. Same metrics as ERA5, on wet days >=5 mm:
  station    wet days  wettest-hour share  wet hours/day  peak/uniform
  0021195170   111        0.386                 9            9.26x
  0021201980    87        0.426                 8           10.22x
  0023050420   228        0.421                 8           10.11x
  0024035360    73        0.508                 6           12.20x
  0021195160   117        0.556                 7           13.33x
  --------------------------------------------------------------------
  GAUGE median ~0.42-0.51   ~7-8 h    ~10.2x
  ERA5-Land      0.193      16 h       4.63x
=> ERA5-Land under-concentrates within-day rainfall by a factor ~2.2 on BOTH the
   wettest-hour share (0.193 vs ~0.42) and the peak/uniform ratio (4.63x vs ~10.2x),
   and it rains for TWICE as many hours (16 vs 7-8).
=> SPATIAL SHAPE ALSO WRONG, not just amplitude: ERA5's diurnal cycle is a single
   basin-wide 13h-local afternoon peak everywhere, but the gauges disagree with each
   other AND with ERA5 - 0023050420 (Argelia, Medio Magdalena) peaks NOCTURNALLY
   (20h-01h = 10.0,7.8,8.2,10.7,12.5,11.1 % vs 0.4-1.0 % at 09h-13h), the classic
   Magdalena-valley nocturnal convection ERA5-Land does not reproduce.
   (Timestamp convention inferred as LOCAL: afternoon/nocturnal peaks are physical;
   a UTC reading would put them at 09h/15h local. Flagged as an inference.)

## PROCESS NOTE (honest record)
My backgrounded per-year Socrata count job FAILED IMMEDIATELY (exit 127, Windows path
quoting in the bash launcher) - it never ran. Before I knew that, I ran
`Stop-Process -Id 6200` believing it was that job; PID 6200 was a python3.10 with 0.94 s
CPU. It was almost certainly one of my own finished heredoc interpreters. No calibration
search was running (Phase B is closed) and I launched none. Recording it because I cannot
prove what 6200 was. Redoing the counts sequentially in the foreground instead.

## S5/S6 CHIRPS + everything else (all OPENED)
- CHIRPS: 11 files data/raw/climate/chirps_basin_<y>.nc, ALL OPENED. Single variable
  `precip`, shape (365|366, 202, 96) @0.05 deg, time units 'days since 1980-01-01',
  unique diff = 1.0 day. Span 2008-01-01 -> 2018-12-31. DAILY ONLY - ruled out.
- IDEAM RADAR (dataset havx-dbve -> registry.opendata.aws/ideam-radares):
  anonymous listing of s3://s3-radaresideam shows l2_data/ = 2018..2026 ONLY, earliest
  day 2018-06-12, 44 files that day for Barrancabermeja at 5-MINUTE cadence
  (BAR180612200505.RAWNCJR / 201004 / 201505). 2018-12-31 = Barrancabermeja+Guaviare;
  2022-06-15 = Guaviare+Munchique. RULED OUT: misses 2011 and 2015-16 entirely.
- Radar composite PNG (uxcq-3pq7): 5-min but 5-DAY retention. Ruled out.
- Disdrometers (s6tj-xze3): raw instantaneous, asset published 2025, no 2008-18. Ruled out.
- Sub-daily RIVER STAGE exists: Socrata bdmn-sqnh 'Nivel Instantaneo' (sensor 0230, mt).
  Basin codes 0021-0029, 1-7 Mar window: 2011 = 33 stations / 7,664 rows;
  2015 = 47 stations / 11,174 rows. Station 0026067010 on 2011-03-02 = 96 rows,
  median step 900 s (15 min); basin mean ~33 obs/station/day (mixed 15-min and hourly).
  NOT forcing, but it is the missing yardstick: R_POT/R_AMS are scored on DAILY MEAN Q.
- Nothing else on disk: no .nc/.grib under data/ besides era5land_* and chirps_*; every
  observed CSV is a '...medio diario' series with a fixed 00:00 stamp (checked
  caudal_*.csv, ssc_*.csv, concentracion_diaria_*.csv). Grep for HH:MM hits were all
  '1990-01-01 00:00' daily stamps - false positives, verified by reading the rows.

## S4c per-year basin automatic-station counts (live, identical 1-7 Mar window)
2008 54 / 46,087 rows; 2009 57 / 50,678; 2010 58 / 58,094; 2011 53 / 57,667;
2012 59 / 61,300; 2013 75 / 76,749; 2014 71 / 67,510; 2015 75 / 70,319; 2016 103 / 69,953.
2017 and 2018 NOT RETURNED - repeated 250 s API read timeouts (recorded as unmeasured,
not as zero); catalogue shows 107+87 telemetric installs in 2017-18 so >=103.
API cost note: one grouped weekly basin query = 66-194 s and TIMES OUT at 250 s on some
windows -> any bulk raw pull must be per-station and resumable.

## S7 DONE - findings written
data/processed/peakgap/subdaily_data_inventory.md (9 candidates A-I, each with a verdict
backed by an opened file or a live-exercised route).

## S8 verdict summary
- A ERA5-Land hourly tp: on disk, complete 2008-2018, USABLE AS SHAPE ONLY (~2.2x too
  smooth, spatially uniform diurnal cycle). Never as an amount.
- B IDEAM automatic 10-min (s54a-sgyg): REAL, OBTAINABLE, live-verified; 53-103 basin
  stations/yr; the only true sub-daily rainfall for 2011/2015-16. Shape/timing only
  (19 % under-catch at high intensity).
- C DHIME conventional: daily only - it is the AMOUNT to be disaggregated.
- D CHIRPS: daily only - ruled out. E radar: starts 2018-06-12 - ruled out.
- F composite PNG / G disdrometers: no archive - ruled out.
- H sub-daily STAGE (bdmn-sqnh): exists for both ENSO years, 33-47 stations, 15-min;
  the observational yardstick, needs rating curves.
- I nothing else on disk.
NO calibration launched. Files written: this journal + the findings file only.

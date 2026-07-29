# ERA5-Land download checklist (whole-basin study, 90 m)

**Domain:** whole Magdalena-Cauca basin — box `N 11.4, W −77.0, S 1.4, E −72.9`.
**Files:** 108 monthly NetCDFs (2009–2017 × 12), named **`era5land_basin_<year>_M<mm>.nc`**, in `data/raw/climate/`.
**Script:** `src/download_era5.py` (already set to this box + naming). Run: `python src/download_era5.py` — resumable.

> ⚠️ The old `era5land_<year>_M<mm>.nc` files (78 present) are the **lower-Magdalena box** — a *different* extent.
> They are superseded **only if** the whole-basin domain is confirmed. **Keep them until the advisor confirms Q3.**
> Do not delete them yet.

Status: **0 / 108** whole-basin files downloaded (fresh start once the domain is locked).

| Year | M01 | M02 | M03 | M04 | M05 | M06 | M07 | M08 | M09 | M10 | M11 | M12 |
|------|----|----|----|----|----|----|----|----|----|----|----|----|
| 2009 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2010 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2011 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2012 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2013 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2014 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2015 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2016 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2017 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

To refresh status at any time, list `data/raw/climate/era5land_basin_*.nc` (or ask me to scan the folder and tick the boxes).

## Launch sequence (once the advisor confirms whole-basin)
1. `Remove-Item data\raw\climate\era5land_2*_M*.nc`   ← delete the old small-box files
2. `python src/download_era5.py`                       ← downloads the 108 basin files (resumable)

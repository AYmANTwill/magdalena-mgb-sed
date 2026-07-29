# Notebooks

Didactic notebooks that derive the maths behind each MGB-SA preprocessing step, by hand and in simple Python,
on a 6x6 toy DEM one can verify by hand. They explain *what the QGIS plugins do*; they do not replace them.

- `01_dem.ipynb` — DEM → minibacias: ASCII/NODATA, pit filling (Planchon-Darboux), D8 flow
  direction, flow accumulation, stream definition, segmentation, watershed/catchment delineation.
- `02_urh.ipynb` — URH: soil × land-cover crossing, Fréchet bounds, per-minibacia composition,
  link to the MGB water balance.
- `03_hydrology.ipynb` — MGB-SA hydrology: daily soil water balance, saturation-excess runoff
  (variable contributing area, `b`), linear-reservoir recession (`K_bas`), a full one-URH daily simulation, and routing.

Real-data notebooks (run on the downloaded data in `data/`):

- `04_real_dem_eda.ipynb` — exploring the real Copernicus DEM: inspection, terrain hillshade, flow-accumulation attempt,
  and *why* the lower-Magdalena box can't be delineated (upstream basin off-map + flat delta) → threshold EDA needs the
  full-basin DEM.
- `05_landcover_soils_reclass.ipynb` — reclassifying WorldCover land cover and IGAC soils into hydrological classes,
  aligning to the DEM grid, and crossing them into the real URH map (the real-data version of notebook 02).

Run: open in Jupyter / VS Code (Jupyter extension), select a Python 3 kernel, "Run All".
Requires `numpy`, `matplotlib` (see `../requirements.txt`).

# Notebooks

Didactic notebooks that derive the maths behind each MGB-SA preprocessing step, by hand and in simple Python,
on a 6x6 toy DEM one can verify by hand. They explain *what the QGIS plugins do*; they do not replace them.

- `01_dem.ipynb` — DEM → minibacias: ASCII/NODATA, pit filling (Planchon-Darboux), D8 flow
  direction, flow accumulation, stream definition, segmentation, watershed/catchment delineation.
- `02_urh.ipynb` — URH: soil × land-cover crossing, Fréchet bounds, per-minibacia composition,
  link to the MGB water balance.
- `03_hydrology.ipynb` — MGB-SA hydrology: daily soil water balance, saturation-excess runoff
  (variable contributing area, `b`), linear-reservoir recession (`K_bas`), a full one-URH daily simulation, and routing.

Run: open in Jupyter / VS Code (Jupyter extension), select a Python 3 kernel, "Run All".
Requires `numpy`, `matplotlib` (see `../requirements.txt`).

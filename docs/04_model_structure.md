# Model structure

## Overview

MGB-SED couples a hydrological/hydrodynamic core (**MGB-SA**) with a sediment module (**MGB-SED**).
Crucially, the sediment module consumes the **outputs of the hydrology** (runoff volume, peak flow), so the two
must be calibrated in order: hydrology first, sediments second.

## Input → sub-model → output flow

```mermaid
flowchart TD
    DEM[DEM / MNT<br/>ALOS or Copernicus]
    SOIL[Soil map<br/>IGAC]
    LU[Land cover<br/>WorldCover / IDEAM]
    CLIM[Climate forcing<br/>ERA5 + IDEAM]

    MINI[Minibacias and network<br/>slopes, drainage areas]
    URH[URH<br/>soil x land cover fractions]

    DEM --> MINI
    SOIL --> URH
    LU --> URH

    MGBSA[[MGB-SA — hydrology<br/>discharge, runoff, peak flow]]
    MINI --> MGBSA
    URH --> MGBSA
    CLIM --> MGBSA

    MGBSED[[MGB-SED — sediments<br/>MUSLE + Exner routing]]
    MGBSA --> MGBSED
    MINI --> MGBSED

    OUT[Suspended sediment flux<br/>concentration, load]
    MGBSED --> OUT

    QOBS[(Observed discharge<br/>IDEAM)]
    SOBS[(Observed sediment<br/>IDEAM / DHIME)]
    QOBS -. calibrates .-> MGBSA
    SOBS -. calibrates .-> MGBSED
```

## Preprocessing chain (DEM → minibacias)

One rule, repeated: water follows the steepest descent, cell by cell.

```mermaid
flowchart LR
    A[DEM .asc<br/>NODATA -9999] --> B[Sink and Destroy<br/>pit filling]
    B --> C[Flow Direction<br/>D8]
    C --> D[Flow Accumulation]
    D --> E[Stream Definition<br/>threshold 1000 cells]
    E --> F[Stream Segmentation]
    F --> G[Watershed and<br/>Catchment Delineation]
    G --> H[Minibacias<br/>mini.gtb]
```

Each transformation is derived by hand, with the maths and simple Python, in
`notebooks/01_dem.ipynb`. The URH layer (the other structural input) is in
`notebooks/02_urh.ipynb`.

## Reference scheme

The canonical MGB-SED AS scheme (hydrology in blue, sediment in brown; inputs, structure, processes, outputs)
is given in Fagundes et al. (*Sediment Flows in South America…*), figure set. See `01_scientific_background.md`.

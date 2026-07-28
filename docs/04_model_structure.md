# Model structure

## Overview

MGB-SED couples a hydrological/hydrodynamic core (**MGB-SA**) with a sediment module (**MGB-SED**).
Crucially, the sediment module consumes the **outputs of the hydrology** (runoff volume, peak flow), so the two
must be calibrated in order: hydrology first, sediments second.

## Full model graph (inputs → preprocessing → structure → sub-models → outputs)

Dashed arrows = calibration data.

```mermaid
flowchart TB
    subgraph IN["Input data"]
        DEM["DEM<br/>ALOS / Copernicus 30 m"]
        SOIL["Soil map<br/>IGAC"]
        LU["Land cover<br/>WorldCover / IDEAM"]
        CLIM["Climate forcing<br/>ERA5 + IDEAM (daily)"]
    end

    subgraph PREP["Preprocessing — IPH-HydroTools"]
        direction LR
        FILL["Sink & Destroy"] --> FDIR["Flow direction D8"] --> FACC["Flow accumulation"]
        FACC --> STR["Stream definition"] --> SEG["Segmentation"] --> CATd["Catchment delineation"]
    end

    subgraph STR2["Basin structure"]
        MINI["Minibacias<br/>+ upstream-downstream topology"]
        URH["URH<br/>soil x land cover fractions"]
    end

    subgraph SA["MGB-SA — hydrology"]
        WB["Soil water balance<br/>per URH"]
        WB --> DSUP["Surface runoff<br/>saturation-excess (b)"]
        WB --> DINT["Interflow"]
        WB --> DBAS["Baseflow<br/>recession (Kbas)"]
        DSUP --> ROUT["Channel routing<br/>local-inertial + floodplain"]
        DINT --> ROUT
        DBAS --> ROUT
    end

    subgraph SED["MGB-SED — sediments"]
        MUSLE["Hillslope erosion<br/>MUSLE (K, LS, C, P, alpha, beta)"]
        EXNER["Channel transport<br/>Exner + 1D equations"]
        MUSLE --> EXNER
    end

    OUTQ["Discharge hydrograph"]
    OUTS["Suspended sediment<br/>concentration and load"]

    DEM --> FILL
    CATd --> MINI
    SOIL --> URH
    LU --> URH
    MINI --> WB
    URH --> WB
    CLIM --> WB
    ROUT --> OUTQ
    OUTQ --> MUSLE
    MINI --> MUSLE
    EXNER --> OUTS

    QOBS[("IDEAM discharge")] -. calibrates .-> ROUT
    SOBS[("IDEAM sediment<br/>DHIME")] -. calibrates .-> EXNER
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

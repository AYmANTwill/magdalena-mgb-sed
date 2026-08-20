# Objectives and hypotheses

## Scientific context

Suspended sediment flux is a first-order control on river morphology, reservoir siltation, nutrient and
contaminant transport, and delta stability. In the tropical Andes, sediment production is strongly modulated by
**ENSO** (El Niño–Southern Oscillation): La Niña years tend to be wetter over much of Colombia (more runoff,
more erosion), while El Niño years tend to be drier. The **Magdalena** is the main Colombian river draining the
Andes to the Caribbean and carries one of the largest specific sediment yields in South America
(**published figures, not ours**: Restrepo & Syvitski 2006; Restrepo A. 2015, which reports the
continent's highest specific yield at Calamar — see [docs/40](40_sdr_evidence.md) §4.1 M4/M10.
Our own t/km²/yr is embargoed until the catchment areas get an external arbiter,
[docs/23](23_gauge_geometry.md) §13.2, so this basin-scale framing is *theirs*.)

This work asks whether a **physically based, spatially distributed** model (MGB-SED) can reproduce and explain
the difference in suspended sediment transport between two contrasting ENSO years, transposing the methodology
of **Fagundes et al.** (southern Brazil) to the Magdalena.

## Main objective

Quantify and physically interpret the **difference in suspended sediment fluxes** between a **La Niña** year (2011)
and an **El Niño** year (2015–2016 or 2017, TBC) in the Magdalena basin, using a calibrated MGB-SED model.

## Specific objectives

1. Build the physical structure of the basin from a DEM (minibacias, drainage network) and land data (URH).
2. Force the model with corrected climate data (Copernicus ERA5, bias-corrected against IDEAM).
3. **Calibrate hydrology first** (discharge, IDEAM), then **calibrate sediments** (MUSLE α, β) using the
   rain/slope threshold technique of Fagundes et al.
4. Run and compare the two ENSO scenarios; attribute the difference to hydro-climatic drivers.

## Hypotheses (testable)

- **H1 — Detectability.** The two ENSO phases produce a difference in basin sediment output that is **larger than
  model/observation uncertainty** (i.e., not washed out by calibration error).
- **H2 — Reproducibility.** An MGB-SED calibrated on IDEAM discharge and sediment records **reproduces observed
  suspended sediment loads** within acceptable performance metrics (e.g., NSE, KGE, PBIAS) at gauged stations.
- **H3 — Method transfer.** The **rain/slope threshold** approach of Fagundes et al., developed for southern
  Brazilian floods, **transfers to the Andean-Magdalena context** for identifying erosive events.
- **H4 — Forcing bias.** ERA5 reanalysis is **biased over mountainous terrain** (noted in Briceño et al.), so
  **bias correction against IDEAM stations is required** before the hydrological signal — and therefore the
  sediment signal — is trustworthy.

## Success criteria

- A calibrated hydrological model (discharge) at one or more IDEAM stations on the Magdalena.
- A calibrated sediment model at one or more IDEAM **sediment** stations.
- A defensible, uncertainty-aware comparison of La Niña vs El Niño sediment fluxes.

## Known risks

- **No usable IDEAM sediment station ⇒ no sediment calibration ⇒ no project.** This is the dominant risk and the
  first open question (see `open_questions.md`).
- Full-basin 30 m preprocessing exceeds IPH-HydroTools' ~250 M cell limit (scale decision needed).
- ERA5 bias over the Andes (mitigated by H4 bias correction).

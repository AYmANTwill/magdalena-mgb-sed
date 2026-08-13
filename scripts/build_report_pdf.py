#!/usr/bin/env python3.10
"""Build the complete explanatory report PDF for the MGB-SED ENSO study.

Dual-level: plain-language narrative first, then the rigorous mathematics, with every technical
term defined in a glossary.  Equations are rendered with matplotlib mathtext and embedded.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
                                Table, TableStyle, HRFlowable)

OUT = Path("/sessions/epic-sleepy-mendel/mnt/magdalena-mgb-sed/MGB-SED_complete_report.pdf")
EQD = Path("/sessions/epic-sleepy-mendel/mnt/magdalena-mgb-sed/_eq"); EQD.mkdir(exist_ok=True)

NAVY = HexColor("#1a3a5c"); STEEL = HexColor("#2e6b8a"); RUST = HexColor("#a8481f")
LIGHT = HexColor("#eef3f7"); GREY = HexColor("#555555")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=17,
                    textColor=NAVY, spaceBefore=18, spaceAfter=8, leading=20)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13,
                    textColor=STEEL, spaceBefore=12, spaceAfter=5, leading=16)
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=10.3, leading=15.2,
                      alignment=TA_JUSTIFY, spaceAfter=7, textColor=HexColor("#1b1b1b"))
SIMPLE = ParagraphStyle("SIMPLE", parent=BODY, backColor=LIGHT, borderColor=STEEL,
                        borderWidth=0, leftIndent=8, rightIndent=8, spaceBefore=4,
                        spaceAfter=8, borderPadding=8)
TERM = ParagraphStyle("TERM", parent=BODY, fontSize=9.6, leading=13.5, leftIndent=12,
                      spaceAfter=4, textColor=HexColor("#333333"))
CAP = ParagraphStyle("CAP", parent=BODY, fontSize=9, textColor=GREY, alignment=TA_CENTER,
                     spaceBefore=2, spaceAfter=10)
TITLE = ParagraphStyle("TITLE", parent=ss["Title"], fontSize=23, textColor=NAVY, leading=27)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=12.5, textColor=STEEL,
                     alignment=TA_CENTER, spaceAfter=4)


def eq(latex, name, fs=17):
    p = EQD / f"{name}.png"
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", ha="center", va="center", fontsize=fs, color="#14243a")
    fig.savefig(p, dpi=220, bbox_inches="tight", pad_inches=0.12, transparent=True)
    plt.close(fig)
    w, h = PILImage.open(p).size
    tw = min(15 * cm, w / 220 * 2.54 * cm / 2.54)
    tw = min(tw, 15 * cm)
    return Image(str(p), width=tw, height=tw * h / w, hAlign="CENTER")


FIGDIR = Path("/sessions/epic-sleepy-mendel/mnt/magdalena-mgb-sed/figures/report")


def figimg(name, w=15.6 * cm):
    p = FIGDIR / name
    iw, ih = PILImage.open(p).size
    return Image(str(p), width=w, height=w * ih / iw, hAlign="CENTER")


def simple(txt):
    return Paragraph("<b>In plain terms.</b> " + txt, SIMPLE)


def term(name, defn):
    return Paragraph(f"<b>{name}</b> — {defn}", TERM)


def tbl(data, widths, header=True):
    t = Table(data, colWidths=widths, hAlign="CENTER")
    sty = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.6),
           ("TEXTCOLOR", (0, 0), (-1, -1), HexColor("#1b1b1b")),
           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
           ("LINEBELOW", (0, 0), (-1, -1), 0.4, HexColor("#c8d4de")),
           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f4f8fb")])]
    if header:
        sty += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
                ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY)]
    t.setStyle(TableStyle(sty))
    return t


S = []  # story


def rule():
    S.append(Spacer(1, 3)); S.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#c8d4de")))
    S.append(Spacer(1, 3))


# ============================================================ TITLE
S += [Spacer(1, 3.2 * cm),
      Paragraph("Modelling Suspended-Sediment Transport in the Magdalena–Cauca Basin", TITLE),
      Spacer(1, 0.5 * cm),
      Paragraph("Does El Niño–La Niña (ENSO) change how much sediment the rivers carry?", SUB),
      Paragraph("A physically-based model, its honest calibration, and what the data can and cannot tell us", SUB),
      Spacer(1, 1.2 * cm),
      Paragraph("MGB-SED / MUSLE study · UMNG internship", CAP),
      Paragraph("This document explains the whole study twice: first in plain language, then with the "
                "full mathematics. Every technical term is defined in simple words where it first "
                "appears and again in the glossary at the end.", CAP),
      PageBreak()]

# ============================================================ EXECUTIVE SUMMARY
S.append(Paragraph("Executive summary", H1))
S.append(Paragraph(
    "We built a physically-based computer model to simulate how much suspended sediment (mud and "
    "silt carried in the water) the rivers of the Magdalena–Cauca basin in Colombia move each "
    "day, and we asked whether the El Niño / La Niña climate cycle changes that amount. "
    "The study reaches two honest conclusions that sit at different levels.", BODY))
S.append(Paragraph(
    "<b>First, the model cannot predict the exact daily tonnage of sediment very accurately</b> — "
    "and, importantly, we can prove that <i>no</i> model could, with the data available. Sediment is "
    "carried by water, and the rainfall records for this basin only let us reconstruct the day-to-day "
    "river flow to about 57% accuracy (a correlation of r ≈ 0.57). You cannot know when the "
    "sediment moved more precisely than you know when the water moved. We measured this ceiling and, "
    "in this study, closed the last remaining idea for lifting it: it would raise accuracy by at most "
    "0.006, so it is a true limit of the observations, not a flaw in the model.", BODY))
S.append(Paragraph(
    "<b>Second — and this is the study's positive result — the model correctly reproduces the "
    "ENSO effect.</b> In the wet La Niña year the model produces about three times more sediment "
    "than in the dry El Niño years, at every one of the 18 river stations tested (18 out of 18 in "
    "the right direction), matching independent measurements (~3–5×). This works precisely "
    "<i>because</i> a wet-versus-dry ratio cancels out the parts of the model we cannot pin down. So "
    "the scientific question the study set out to answer — does ENSO change sediment transport, "
    "and by how much — is answered clearly, even though the absolute daily prediction is weak.", BODY))
rule()

# ============================================================ PART I
S.append(Paragraph("Part I — The study in plain language", H1))

S.append(Paragraph("1. The question", H2))
S.append(Paragraph(
    "The Magdalena–Cauca is Colombia's largest river basin. It carries an enormous load of "
    "suspended sediment — fine soil washed off the hillslopes by rain — which shapes farmland, "
    "reservoirs, ports and ecosystems downstream. The El Niño–Southern Oscillation (ENSO) is "
    "a natural climate swing: La Niña years are unusually wet here, El Niño years unusually "
    "dry. Our question: how much does this wet/dry swing change the amount of sediment the rivers "
    "carry? We compare the very wet La Niña of 2011 against the dry El Niño of 2015–16.", BODY))

S.append(Paragraph("2. What we built", H2))
S.append(Paragraph(
    "We did not guess. We built a <i>physically-based</i> model — one that computes sediment from "
    "the actual physics of erosion, not from a statistical fit. Rain falls, some runs off the surface, "
    "that runoff detaches soil from the hillslopes according to how steep the land is, what grows on "
    "it, and how erodible the soil is; the detached soil is delivered to the river. The model does "
    "this for 8,672 small sub-catchments across the whole basin, every day for ten years.", BODY))

S.append(Paragraph("3. What we found, and the honest catch", H2))
S.append(Paragraph(
    "When we tuned the model against real sediment measurements at the river gauges (this tuning is "
    "called <i>calibration</i>), it could only match the day-to-day amounts weakly. The reason is not "
    "the sediment part of the model — it is the rainfall. Sediment follows water, and our "
    "reconstructed water flow is only about 57% right, because Colombia's rain-gauge network is sparse "
    "and, in dry years especially, the rainfall is hard to reconstruct. If you don't know exactly when "
    "the water moved, you can't know exactly when the sediment moved. So the weak daily accuracy is "
    "inherited from the rainfall data; it is a limit of what was measured, and we proved it cannot be "
    "meaningfully improved with the data that exists.", BODY))
S.append(Paragraph(
    "But the wet-versus-dry <i>contrast</i> is a much easier, coarser question than the exact daily "
    "amount — and there the model succeeds. It reproduces the observed ENSO effect (about three "
    "times more sediment in the wet year) at all 18 stations. That contrast is robust because it is a "
    "ratio: the parts of the model we cannot pin down appear on both the top and the bottom of the "
    "fraction and cancel out.", BODY))
S.append(simple(
    "The model is like a thermometer that can't tell you the exact temperature each hour (the rainfall "
    "'signal' is too fuzzy for that) but <i>can</i> reliably tell you that summer is hotter than winter. "
    "The 'summer vs winter' question here is 'La Niña vs El Niño', and the model gets it right."))
rule()

# ============================================================ PART II
S.append(PageBreak())
S.append(Paragraph("Part II — The science in detail", H1))
S.append(Paragraph(
    "This part states the mathematics precisely. Every symbol is defined the first time it appears, "
    "and a plain-terms box follows each equation.", BODY))

# --- 4 MUSLE
S.append(Paragraph("4. The erosion model (MUSLE)", H2))
S.append(Paragraph(
    "The engine is the Modified Universal Soil Loss Equation (MUSLE). For each model cell it computes "
    "the mass of sediment produced on a given day as:", BODY))
S.append(eq(r"\mathrm{Sed} \;=\; \alpha \,\left(Q_{sur}\cdot q_{peak}\cdot A\right)^{\beta}\; K\cdot C\cdot P\cdot LS", "musle"))
S.append(Paragraph("where the symbols mean:", BODY))
for n, d in [
    ("Sed", "the sediment mass eroded that day, in tonnes."),
    ("Q<sub>sur</sub>", "surface runoff — the depth of rainwater (in mm) that runs off the surface rather than soaking in. This is the link to the hydrology, and the source of the ceiling discussed in §5."),
    ("q<sub>peak</sub>", "the peak runoff rate — how fast the water leaves at its fastest moment. Fast water carries more soil."),
    ("A", "the area of the cell."),
    ("α (alpha)", "a multiplier that sets the overall level of erosion. The reference physical value is α = 11.8 (Williams, 1975). This is the main knob we try to calibrate."),
    ("β (beta)", "an exponent (a power) that controls how strongly big rain events dominate. Reference value β = 0.56."),
    ("K", "soil erodibility — how easily the soil washes away (from soil maps)."),
    ("C", "the cover factor — how much the vegetation protects the soil (forest protects, bare ground does not)."),
    ("P", "the practice factor — soil-conservation practices; set to 1 (no data) meaning 'no protection assumed'."),
    ("LS", "the topographic factor — how steepness and slope length increase erosion. Steeper, longer slopes erode more. This factor is the subject of §6."),
]:
    S.append(term(n, d))
S.append(simple(
    "This formula says: the amount of soil eroded equals a level knob (α) times the erosive power "
    "of the day's runoff (raised to a power β), multiplied by four properties of the land — how "
    "erodible the soil is (K), how well plants cover it (C), whether it is protected (P), and how steep "
    "it is (LS)."))

# --- 5 hydrology ceiling
S.append(Paragraph("5. The hydrology, and the rainfall ceiling", H2))
S.append(Paragraph(
    "The runoff Q<sub>sur</sub> that drives erosion comes from a calibrated water-balance model of the "
    "basin (the adopted configuration is called H2E). Its skill is measured by the <i>correlation</i> "
    "between simulated and observed daily river flow.", BODY))
S.append(term("Correlation (r)", "a number between −1 and +1 measuring how well two time-series rise "
              "and fall together. r = 1 is perfect agreement in timing; r = 0 is no relationship. Here it "
              "measures whether the model puts the high-flow and low-flow days on the right dates."))
S.append(Paragraph(
    "The best achievable correlation for this basin is <b>r ≈ 0.57</b>. This is not a tuning failure: "
    "three competing explanations were tested and refuted, and the limit was traced to the rainfall "
    "input itself — a sparse gauge network that, in dry years, cannot reconstruct the timing of the "
    "rain. In the dry El Niño phase the model's skill over simply guessing the long-term average is "
    "essentially zero (measured at −0.0005). Because sediment is a function of runoff, this "
    "correlation ceiling propagates directly into the sediment model.", BODY))
S.append(simple(
    "'Correlation' is a score from −1 to +1 for how well two wiggly lines move together. Our water "
    "model scores about 0.57 — decent but far from perfect — and that is the best the rainfall "
    "data allows. Everything the sediment model does is capped by this number."))

# --- 6 LS
S.append(Paragraph("6. Resolving the topographic factor LS", H2))
S.append(Paragraph(
    "The LS factor turned out to be the single largest uncertainty. Our original way of computing it "
    "gave values about four times larger than the published source formulation (Buarque, 2015) intends. "
    "We re-derived LS strictly from the source method (a variant labelled V4_dg) and measured, on our "
    "own terrain, the ratio between the two:", BODY))
S.append(eq(r"f_{LS} \;=\; \frac{\overline{LS}_{\,\mathrm{V4dg\;(adopted)}}}{\overline{LS}_{\,\mathrm{V0\;(original)}}} \;=\; 0.25146", "fls"))
S.append(term("f<sub>LS</sub>", "the ratio of the adopted LS field to the original one. A value of 0.25 "
              "means the corrected topography factor is one-quarter of what we first used — our "
              "original erosion-from-slope was about 4× too high."))
S.append(Paragraph(
    "Crucially, this was measured to be a <i>shape</i> change, not a uniform rescaling: the reduction is "
    "stronger on steep, high terrain (ratio ≈ 0.235) than on gentle lowlands (≈ 0.30). Because "
    "erosion concentrates exactly where the reduction is largest (68% of erosion occurs above 1000 m), "
    "the correction genuinely changes the spatial pattern, not just the total. The basin-total gross "
    "hillslope erosion at the reference parameters is 299.54 million tonnes per year.", BODY))
S.append(simple(
    "The 'slope' ingredient of the erosion formula was about four times too strong. We fixed it to match "
    "the published method, and the fix cuts hardest exactly on the steep ground that produces most of the "
    "erosion — so it reshapes the map, not just the grand total."))

# --- 7 calibration KGE
S.append(PageBreak())
S.append(Paragraph("7. Calibrating the sediment model", H2))
S.append(Paragraph(
    "Calibration means adjusting the free parameters (here α and β) so the simulated sediment "
    "matches observations at gauging stations. We measured the match with the Kling–Gupta "
    "Efficiency on the logarithm of sediment flux (KGE), computed per station over its measured days:", BODY))
S.append(eq(r"\mathrm{KGE} \;=\; 1 - \sqrt{\,(r-1)^2 + (v-1)^2 + (m-1)^2\,}", "kge"))
S.append(Paragraph("built from three components comparing simulated (y) and observed (x) log-flux:", BODY))
S.append(eq(r"r=\mathrm{corr}(x,y)\quad\; v=\frac{\mathrm{sd}(y)}{\mathrm{sd}(x)}\quad\; m=\frac{\mathrm{mean}(y)}{\mathrm{mean}(x)}", "kgec"))
for n, d in [
    ("KGE", "a skill score. KGE = 1 is a perfect match. Higher is better."),
    ("r", "correlation — is the <i>timing</i> right? (defined in §5)."),
    ("v", "the variability ratio — is the <i>spread</i> (ups and downs) the right size?"),
    ("m", "the mean ratio — is the <i>average level</i> right? The α knob mainly moves this term."),
    ("log flux", "we compare the logarithm of sediment flux because flux spans a factor of thousands "
     "between small and large rivers; logarithms put them on a comparable footing."),
    ("flux", "sediment discharge = water discharge × concentration × 0.0864, in tonnes/day."),
]:
    S.append(term(n, d))
S.append(Paragraph(
    "Two facts make the outcome computable in advance. (1) The knob α only shifts the mean term m by "
    "a constant, so the whole α-search is closed-form arithmetic on the station statistics — no "
    "blind search is needed. (2) The parameters are <i>non-identifiable</i>: α multiplies together "
    "with K, C, P and LS, so the data can only constrain the product, never α alone (the design "
    "matrix has an infinite condition number). α is therefore a handle on a bundled quantity, never a "
    "physically separable number.", BODY))
S.append(term("Non-identifiable", "when several unknowns only ever appear multiplied together, the data "
              "can pin down their product but not each one separately — like knowing 6 = 2×3 "
              "tells you the product, not that the factors were 2 and 3 rather than 1 and 6."))

# --- 8 the result
S.append(Paragraph("8. The calibration result: railed / exploratory", H2))
S.append(Paragraph(
    "Run on the corrected LS field (a genuine first run, required because the LS change is a shape "
    "change and cannot be faked by rescaling), the search produced:", BODY))
S.append(tbl([
    ["Quantity", "Result", "Meaning"],
    ["Best KGE within the allowed α range [2, 30]", "−0.118 (at α = 2, the floor)", "the search rails at the edge"],
    ["α the data actually wants (unconstrained)", "≈ 0.48", "below the plausible floor"],
    ["Best KGE, dropping the flow-biased station (G12)", "+0.197", "verdict does not flip"],
    ["Robustness check on a rating-curve estimator (b)", "+0.139", "same sign → not indeterminate"],
    ["KGE of simply guessing the average every day", "−0.414", "the 'no-skill' reference line"],
    ["Registered 'usable' band (Fagundes, for sediment)", "[−0.26, 0.44]", "the pre-agreed target"],
], [7.2 * cm, 4.6 * cm, 4.4 * cm]))
S.append(Spacer(1, 6))
S.append(Paragraph(
    "The fit <b>rails</b>: the data wants α ≈ 0.48, far below the physical value (11.8) and below "
    "the plausible floor. In the pre-registered scheme this is read as a diagnostic — an α that "
    "wants to be very small signals mild over-production somewhere upstream — not a number to adopt. "
    "So the sediment model is reported as <b>exploratory (not calibrated for adoption)</b> and runs on the "
    "physical Williams parameters. Notably, several individual stations fit genuinely well where their "
    "runoff happens to be predictable (El Profundo KGE 0.76 with r 0.79; Borbur 0.50; Capitanejo 0.32), "
    "and the per-station KGE tracks the per-station correlation almost exactly — direct proof that "
    "the runoff-timing ceiling, not the sediment model, sets the score.", BODY))
S.append(figimg("fig2_kge_alpha_rail.png", 13.6 * cm))
S.append(Paragraph("Fig 2. Median sediment KGE versus the level knob α (β = 0.56, logarithmic axis). "
    "The score rises as α falls toward the value the data prefers (≈ 0.48), which lies below the "
    "plausible floor — so within the allowed range [2, 30] the fit rails at the floor (α = 2). At the "
    "physical Williams value (11.8) the score is −0.42, right at the no-skill line.", CAP))

# --- 9 why not 1
S.append(Paragraph("9. Why the KGE cannot be near 1 — the ceiling, mathematically", H2))
S.append(Paragraph(
    "A KGE near 1 requires r near 1: the timing must be nearly perfect. But timing is inherited from "
    "runoff, capped at r ≈ 0.57. Substituting the best possible r into the KGE formula, with perfect "
    "variability and mean (v = m = 1):", BODY))
S.append(eq(r"\mathrm{KGE}_{\max} \;=\; 1-\sqrt{(0.57-1)^2+0+0}\;=\;1-0.43\;\approx\;0.57", "kgemax"))
S.append(Paragraph(
    "So ~0.57 is the absolute best this basin could give even with a flawless model, and the campaign-"
    "sampled, rating-curve sediment observations (log-scatter ≈ 0.8) push the realistic figure lower. "
    "A KGE near 1 was never physically attainable — and a model that <i>did</i> score near 1 would be "
    "a warning sign of having accidentally fitted the rating curve, which the design deliberately avoids.", BODY))
S.append(simple(
    "The best possible score is set by the timing correlation. Ours is capped at 0.57, so even a perfect "
    "sediment model tops out around 0.57 in this basin — and daily sediment realistically scores near "
    "zero. That is the ceiling, not a failure."))
S.append(figimg("fig3_kge_vs_r.png", 11.6 * cm))
S.append(Paragraph("Fig 3. Each point is one calibration station: its sediment KGE (vertical) against "
    "its runoff-timing correlation r (horizontal). They line up — stations whose runoff is predictable "
    "score well, those whose runoff is not score badly, with the same model and the same α. This is "
    "direct evidence that the runoff-timing ceiling, not the sediment physics, sets the score.", CAP))

# --- 10 gauges
S.append(Paragraph("10. The observation limit: only 18 usable gauges", H2))
S.append(Paragraph(
    "Sediment flux needs discharge × concentration measured on the same day at the same place. Of 79 "
    "sediment stations, only 18 also gauge discharge and are usable; 8 of those (covering 5.4% of the "
    "basin) enter the fit. We recovered coordinates for the 46 unmapped stations from the national "
    "catalogue, but confirmed that none of them gauge discharge at all — they are sediment-only sites, "
    "so the calibratable set cannot grow past ~18. This is a physical limit of the monitoring network. "
    "The study's strength therefore rests not on gauge count but on the agreement of three independent "
    "lines of evidence (below).", BODY))

# --- 11 ENSO contrast
S.append(PageBreak())
S.append(Paragraph("11. Out-of-sample design and the climate windows", H2))
S.append(Paragraph(
    "The ENSO years were deliberately held out of the calibration (a Klemeš differential split-sample "
    "test): the model is tuned only on the neutral window and then scored on the wet and dry extremes "
    "it never saw. We verified the window classifications against the NOAA CPC Oceanic Niño Index (ONI), "
    "fetched 2026-08-13.", BODY))
S.append(term("ONI (Oceanic Niño Index)", "NOAA's official ENSO thermometer; El Niño / La Niña are "
              "declared when it stays above +0.5 / below −0.5 °C for five overlapping 3-month seasons."))
S.append(figimg("fig5_oni_windows.png", 15.6 * cm))
S.append(Paragraph("Fig 5. The ONI across the study period. The calibration window (2012–2014, grey) "
    "is ENSO-neutral at its core — all of 2013 lies within ±0.45 — but its edges catch weak signals: a "
    "La Niña tail in early 2012 and the onset of the 2015–16 El Niño in the last quarter of 2014 "
    "(ONI +0.5 to +0.8). The out-of-sample design is therefore strong but not perfectly clean, and we "
    "state it that way rather than overclaiming a strictly out-of-phase split.", CAP))
S.append(Paragraph("12. The ENSO contrast — the study's headline result", H2))
S.append(Paragraph(
    "The scientific target is the wet/dry ratio of sediment rate between La Niña and El Niño. "
    "For a station this is:", BODY))
S.append(eq(r"R \;=\; \frac{\overline{\mathrm{Sed}}_{\;\mathrm{LaNina}}}{\overline{\mathrm{Sed}}_{\;\mathrm{ElNino}}}"
           r"\;=\;\frac{\alpha\,LS\,\overline{X}_{\,\mathrm{LaNina}}}{\alpha\,LS\,\overline{X}_{\,\mathrm{ElNino}}}"
           r"\;=\;\frac{\overline{X}_{\,\mathrm{LaNina}}}{\overline{X}_{\,\mathrm{ElNino}}}", "ratio"))
S.append(Paragraph(
    "The badly-constrained factors α and LS appear identically top and bottom and <b>cancel</b>. So "
    "the contrast is immune to the calibration railing and to the LS-level uncertainty — it depends "
    "only on the runoff contrast the rainfall carries between the two regimes. The results:", BODY))
S.append(tbl([
    ["", "Direction (wet > dry)", "Median ratio", "Range"],
    ["Observed (measurements, model-free)", "22 of 22 stations", "~3–5×", "up to ~9×"],
    ["Modelled (this study, 18 stations)", "18 of 18 stations", "3.05×", "1.6–4.9×"],
    ["Modelled, sensitivity (β & window)", "18 of 18, every case", "2.6–5.9×", "—"],
], [6.6 * cm, 4.2 * cm, 3.0 * cm, 2.4 * cm]))
S.append(Spacer(1, 6))
S.append(figimg("fig1_enso_contrast.png", 15.6 * cm))
S.append(Paragraph("Fig 1. Modelled wet/dry sediment ratio (bars) at all 18 stations, sorted, with the "
    "two observed estimators overlaid where they exist. The named reference is estimator <b>(b)</b>: the "
    "modelled median (3.05) sits close to (b)'s 2.84–2.95 and below (a)'s 4.62 — both observed values "
    "are shown here, following the project's 'report both' rule, so the model is not silently compared "
    "against whichever estimator flatters it. Every bar exceeds 1.", CAP))
S.append(Paragraph(
    "Every station, in the model and in the data, shows more sediment in the wet year; the model's median "
    "(3.05×) sits squarely inside the observed 3–5× and matches the smoother rating-based estimator (b) "
    "closely. The direction never reverses across three values of β and two window definitions. This is "
    "an out-of-sample test: the ENSO years were never used in the calibration (with the mild edge caveat "
    "of §11).", BODY))
S.append(simple(
    "The one thing we most want to know — does the wet/dry climate swing change sediment, and by how "
    "much — comes out as a <i>ratio</i>, and ratios cancel the parts of the model we're unsure about. "
    "The model says 'about 3× more in the wet year, at every station', and the measurements agree."))

# --- 12 ceiling bound
S.append(Paragraph("13. Can the ceiling be lifted? A quantified no", H2))
S.append(Paragraph(
    "The one surviving idea for improving the rainfall was to repair 139 gauges that under-report dry days "
    "and thereby enable a satellite-rainfall blend. We bounded the best possible gain using the project's "
    "own cross-validation: the blend helps only at intermediate gauge-distance (+0.023 in r over 57% of "
    "the basin) and actively hurts far from gauges (−0.043 over 17%). Area-weighted, the net is:", BODY))
S.append(eq(r"\Delta r_{\text{basin}} \;=\; (0.258)(0)+(0.571)(+0.023)+(0.171)(-0.043)\;\approx\;+0.006", "bound"))
S.append(Paragraph(
    "So even a perfect repair lifts the correlation from ~0.57 to only ~0.576 — and the discharge gain "
    "would be smaller still. The r ≈ 0.57 ceiling is therefore structural: the information simply is "
    "not in the observations. This turns the last open question into a closed, quantified finding.", BODY))
S.append(figimg("fig4_ceiling_bound.png", 15.0 * cm))
S.append(Paragraph("Fig 4. Why the last rainfall lever cannot help. Left: how the basin splits by "
    "distance to the nearest rain gauge. Right: each band's contribution to the basin-average change in "
    "correlation if the satellite blend were adopted — the gain in the middle band is almost exactly "
    "cancelled by the loss in the far band, netting only +0.006.", CAP))
rule()

# ============================================================ PART III
S.append(Paragraph("Part III — Conclusions", H1))
S.append(Paragraph(
    "The study delivers an honest two-level result. At the level of <b>absolute daily prediction</b>, the "
    "sediment model is weak (KGE near zero) and rails under calibration — not because of the sediment "
    "physics, but because the rainfall data caps the runoff timing at r ≈ 0.57, a ceiling we proved "
    "cannot be lifted with available data. At the level of the <b>ENSO contrast</b> — the question the "
    "study exists to answer — the model succeeds: it reproduces the observed ~3× wet/dry sediment "
    "ratio at 18 of 18 stations, robustly, out of sample, because the contrast cancels the unconstrained "
    "parts of the model.", BODY))
S.append(Paragraph(
    "The conclusion rests on the convergence of three independent lines — observed flux contrast "
    "(22/22), observed concentration contrast (weaker, same direction), and modelled contrast (18/18) — "
    "which is more robust than any single larger dataset would be. Absolute sediment yields (tonnes per "
    "km² per year) are deliberately not reported, because the catchment areas are unreliable and are "
    "under embargo; all results are stated as ratios or as basin-internal fluxes.", BODY))
S.append(simple(
    "We cannot say precisely how many tonnes moved on a given day — nobody could, with this rainfall "
    "data, and we proved it. But we can say clearly and reliably that La Niña moves about three times "
    "more sediment than El Niño, everywhere we can check. That is the finding."))
rule()

# ============================================================ GLOSSARY
S.append(PageBreak())
S.append(Paragraph("Glossary — every term in simple words", H1))
gloss = [
    ("Suspended sediment", "fine soil (silt and clay) carried along inside river water, rather than rolling on the bed."),
    ("Basin / catchment", "the whole area of land whose rain drains into a given river."),
    ("ENSO / El Niño / La Niña", "a natural Pacific climate cycle. Here La Niña = wetter than normal, El Niño = drier."),
    ("Physically-based model", "a model that computes results from physical laws (erosion, water balance), not from a statistical curve fit."),
    ("MUSLE", "Modified Universal Soil Loss Equation — the physics formula that turns runoff and land properties into eroded soil mass."),
    ("Runoff (Q<sub>sur</sub>)", "the part of rainfall that flows over the surface instead of soaking in; it does the eroding."),
    ("Discharge", "the volume of water flowing past a point per second (cubic metres per second)."),
    ("Flux (sediment)", "the mass of sediment passing a point per day = discharge × concentration × 0.0864 (tonnes/day)."),
    ("Concentration", "how much sediment is in the water, in milligrams per litre."),
    ("Calibration", "adjusting a model's free numbers so its output matches real measurements."),
    ("Validation", "checking a calibrated model against data it was not fitted to."),
    ("Parameter", "an adjustable number in the model (here α and β)."),
    ("α (alpha)", "the level knob for erosion; physical reference value 11.8."),
    ("β (beta)", "the exponent controlling how much big storms dominate; reference 0.56."),
    ("LS factor", "how slope steepness and length increase erosion."),
    ("Correlation (r)", "a −1-to-+1 score for how well two time-series move together; 1 = perfect timing."),
    ("KGE", "Kling–Gupta Efficiency — a skill score combining timing, spread and average; 1 = perfect."),
    ("Log / logarithm", "a way of compressing numbers that span huge ranges so small and large rivers compare fairly."),
    ("Non-identifiable", "when unknowns only appear multiplied together, so only their product can be found, not each one."),
    ("Rails / railing", "when a search hits the edge of the allowed range because the data wants to go beyond it."),
    ("Exploratory (result)", "a result reported honestly as not good enough to adopt as final — a legitimate scientific outcome."),
    ("Out-of-sample", "tested on data (here the ENSO years) that were deliberately kept out of the calibration."),
    ("Ceiling (r ≈ 0.57)", "the best accuracy the rainfall data allows; a hard limit, not a tuning failure."),
    ("Contrast / ratio", "the wet-year value divided by the dry-year value; robust because shared errors cancel."),
    ("Gauge / station", "a fixed site where river flow and/or sediment are measured."),
]
for n, d in gloss:
    S.append(term(n, d))

S.append(Spacer(1, 10))
S.append(Paragraph(
    "<i>Prepared as a complete, self-contained explanation of the MGB-SED ENSO study. Numbers are drawn "
    "from the project's committed results (H2E hydrology, the LS resolution, the C4.3 calibration, the C5 "
    "ENSO application, and the rainfall-ceiling bound).</i>", CAP))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#c8d4de")); canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.4 * cm, A4[0] - 2 * cm, 1.4 * cm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1.0 * cm, "MGB-SED · Magdalena–Cauca ENSO sediment study")
    canvas.drawRightString(A4[0] - 2 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm,
                        leftMargin=2 * cm, rightMargin=2 * cm,
                        title="MGB-SED ENSO sediment study — complete explanation")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)

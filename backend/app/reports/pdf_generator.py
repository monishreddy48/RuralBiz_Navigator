"""
RuralBiz Navigator - Detailed Project Report (DPR) PDF Generator
Generates a comprehensive 20-section bankable micro-enterprise project proposal.
Powered by ReportLab.
"""
import io
import os
from typing import Dict, Any, List
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from utils.formatting import format_inr, format_pct
from config import REPORTS_DIR

def generate_dpr_pdf(
    assessment_data: Dict[str, Any],
    locality: Dict[str, Any],
    business: Dict[str, Any],
    hyperlocal_metrics: Dict[str, Any],
    financial_plan: Dict[str, Any],
    viability_result: Dict[str, Any],
    recommendation: Dict[str, Any],
    schemes: List[Dict[str, Any]],
    output_path: str = None
) -> bytes:
    """
    Builds a multi-page, formatted PDF containing all 20 required sections.
    Returns PDF bytes and optionally saves to output_path.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1E3A8A")    # Deep Navy
    c_accent = colors.HexColor("#0D9488")     # Teal
    c_dark = colors.HexColor("#1F2937")       # Charcoal
    c_gray = colors.HexColor("#4B5563")       # Subtext
    c_light = colors.HexColor("#F3F4F6")      # Light Gray
    c_gold = colors.HexColor("#D97706")       # Gold/Amber

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_gray,
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark
    )
    bold_style = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.white,
        alignment=1
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_gray
    )

    story = []

    # Header & Cover Title
    story.append(Paragraph("RURALBIZ NAVIGATOR", title_style))
    story.append(Paragraph("Detailed Project Feasibility & Financial Structuring Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=12))

    # SECTION 1 & 2: Entrepreneur & Business Profile
    user_name = assessment_data.get("name") or "Rural Micro-Entrepreneur"
    loc_name = locality.get("village_name", "Demo Village")
    biz_name = business.get("business_name", "Micro Business Unit")
    category = business.get("category", "General")
    rec_decision = recommendation.get("decision", "MODIFY")

    # Recommendation Banner Table
    banner_bg = colors.HexColor("#10B981") if rec_decision == "GO" else (
        colors.HexColor("#F59E0B") if rec_decision == "MODIFY" else colors.HexColor("#EF4444")
    )
    banner_data = [
        [
            Paragraph(f"<b>FINAL DECISION: {rec_decision}</b> ({recommendation.get('decision_label', '')})", badge_style),
            Paragraph(f"<b>VIABILITY SCORE: {viability_result.get('viability_score', 0):.0f} / 100</b>", badge_style)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[3.8 * inch, 3.2 * inch])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), banner_bg),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 10))

    # Profile Summary Table
    profile_data = [
        [Paragraph("<b>Entrepreneur Name:</b>", bold_style), Paragraph(user_name, body_style),
         Paragraph("<b>Assessment Date:</b>", bold_style), Paragraph("March 2026 (SIH 2026)", body_style)],
        [Paragraph("<b>Locality / Village:</b>", bold_style), Paragraph(f"{loc_name}, {locality.get('district', '')}, {locality.get('state', '')}", body_style),
         Paragraph("<b>Experience Level:</b>", bold_style), Paragraph(str(assessment_data.get("experience_level", "Beginner")), body_style)],
        [Paragraph("<b>Proposed Trade:</b>", bold_style), Paragraph(biz_name, body_style),
         Paragraph("<b>Category:</b>", bold_style), Paragraph(category, body_style)],
        [Paragraph("<b>Own Capital:</b>", bold_style), Paragraph(format_inr(financial_plan.get("own_contribution", 0)), body_style),
         Paragraph("<b>Project Cost:</b>", bold_style), Paragraph(format_inr(financial_plan.get("project_cost", 0)), body_style)]
    ]
    t_prof = Table(profile_data, colWidths=[1.6*inch, 2.1*inch, 1.6*inch, 2.1*inch])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_prof)
    story.append(Spacer(1, 12))

    # SECTION 3, 4 & 5: Locality, Market & Competitor Analysis
    story.append(Paragraph("1. Locality & Market Opportunity Analysis", h1_style))
    market_text = (
        f"<b>Village Catchment:</b> Population of {locality.get('population', 0):,} ({locality.get('households', 0)} households). "
        f"Road accessibility index is rated at {locality.get('road_access_score', 0)}/100 and nearest market is {locality.get('market_distance_km', 0)} km away.<br/>"
        f"<b>Customer Base:</b> Estimated target customer pool of ~{hyperlocal_metrics.get('customer_pool', 0):,} rural households within 5–10 km radius.<br/>"
        f"<b>Competition Landscape:</b> {hyperlocal_metrics.get('num_competitors', 0)} active local competitor(s) identified with an average customer satisfaction of "
        f"⭐ {hyperlocal_metrics.get('avg_competitor_rating', 0):.1f}/5. Estimated local unmet monthly market gap is {format_inr(hyperlocal_metrics.get('estimated_unmet_demand_rupees', 0))}."
    )
    story.append(Paragraph(market_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 6 & 7: Viability Breakdown & SWOT
    story.append(Paragraph("2. Viability Score & Factor Breakdown", h1_style))
    v_breakdown = viability_result.get("breakdown", {})
    vb_data = [["Factor", "Weight", "Score / 100", "Evaluation"]]
    w = viability_result.get("weights", {})
    for factor, score in v_breakdown.items():
        w_pct = format_pct(w.get(factor.lower().replace(" ", "_"), 0.15) * 100, 0)
        status_txt = "Favorable" if score >= 70 else ("Moderate" if score >= 50 else "High Risk")
        vb_data.append([factor, w_pct, f"{score:.1f}", status_txt])

    t_vb = Table(vb_data, colWidths=[2.2*inch, 1.2*inch, 1.6*inch, 2.0*inch])
    t_vb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
    ]))
    story.append(t_vb)
    story.append(Spacer(1, 8))

    # SWOT Analysis Grid
    story.append(Paragraph("3. Strategic SWOT Assessment", h1_style))
    swot = recommendation.get("swot", {})
    swot_data = [
        [
            Paragraph("<b>STRENGTHS</b><br/>• " + "<br/>• ".join(swot.get("strengths", ["N/A"])), body_style),
            Paragraph("<b>WEAKNESSES</b><br/>• " + "<br/>• ".join(swot.get("weaknesses", ["N/A"])), body_style)
        ],
        [
            Paragraph("<b>OPPORTUNITIES</b><br/>• " + "<br/>• ".join(swot.get("opportunities", ["N/A"])), body_style),
            Paragraph("<b>THREATS</b><br/>• " + "<br/>• ".join(swot.get("threats", ["N/A"])), body_style)
        ]
    ]
    t_swot = Table(swot_data, colWidths=[3.7*inch, 3.7*inch])
    t_swot.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#ECFDF5")), # Light Green
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#FEF2F2")), # Light Red
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor("#EFF6FF")), # Light Blue
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor("#FFFBEB")), # Light Amber
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_swot)
    story.append(Spacer(1, 10))

    # SECTION 8 & 9: Financial Plan & Capital Structure
    story.append(Paragraph("4. Capital Requirements & Financing Structure", h1_style))
    fin_summary_data = [
        ["Financial Parameter", "Value", "Benchmark Guidance"],
        ["Total Project Cost", format_inr(financial_plan.get("project_cost", 0)), "CapEx machinery + 3 months initial working capital"],
        ["Entrepreneur Own Equity", f"{format_inr(financial_plan.get('own_contribution', 0))} ({financial_plan.get('own_pct', 0):.1f}%)", "Minimum 10% - 15% recommended"],
        ["Term Loan Required", f"{format_inr(financial_plan.get('loan_amount', 0))} ({financial_plan.get('loan_pct', 0):.1f}%)", "Proposed institutional debt"],
        ["Annual Interest Rate", f"{financial_plan.get('annual_interest_rate', 9.5)}% p.a.", "Commercial reducing balance"],
        ["Repayment Tenure", f"{financial_plan.get('tenure_months', 60)} Months", "Standard 5-year repayment schedule"],
        ["Moratorium Buffer", f"{financial_plan.get('moratorium_months', 3)} Months", "Grace period for setup & trial operations"],
        ["Monthly Loan EMI", format_inr(financial_plan.get("monthly_emi", 0)), "Post-moratorium fixed monthly outflow"],
        ["Debt Service Coverage (DSCR)", f"{financial_plan.get('dscr', 0):.2f} ({financial_plan.get('dscr_status', '')})", "Benchmark: > 1.20 required for commercial safety"],
        ["Monthly Break-Even Revenue", format_inr(financial_plan.get("break_even_revenue", 0)), "Fixed cost + EMI coverage point"]
    ]
    t_fin = Table(fin_summary_data, colWidths=[2.6*inch, 2.0*inch, 2.8*inch])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_accent),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    # SECTION 10, 11, 12, 13: 12-Month Projected Cash Flow Statement
    story.append(Paragraph("5. 12-Month Projected Cash Flow Statement", h1_style))
    cf_data = [["Mo", "Revenue", "Var. Costs", "Fixed Costs", "Operating Pft", "EMI", "Net Flow", "Closing Cash"]]
    cash_flow = financial_plan.get("cash_flow_12", [])
    for row in cash_flow:
        cf_data.append([
            f"M{row['month']}",
            format_inr(row['revenue'], False),
            format_inr(row['variable_costs'], False),
            format_inr(row['fixed_costs'], False),
            format_inr(row['operating_profit'], False),
            format_inr(row['emi'], False),
            format_inr(row['net_cash_flow'], False),
            format_inr(row['closing_cash'], False)
        ])
    t_cf = Table(cf_data, colWidths=[0.5*inch, 1.0*inch, 1.0*inch, 0.9*inch, 1.0*inch, 0.9*inch, 1.0*inch, 1.1*inch])
    t_cf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
    ]))
    story.append(t_cf)
    story.append(Spacer(1, 10))

    # SECTION 17 & 18: Government Scheme Possibilities
    story.append(Paragraph("6. Applicable Government Schemes & Subsidies", h1_style))
    matched_schemes = [s for s in schemes if s["match_status"] in ["MATCHED", "POSSIBLE"]][:3]
    if matched_schemes:
        sch_data = [["Scheme Name", "Status", "Max Loan / Subsidy", "Application Route"]]
        for ms in matched_schemes:
            sch_data.append([
                Paragraph(f"<b>{ms['name']}</b>", body_style),
                ms["match_status"],
                Paragraph(f"{ms.get('loan_available', '')[:35]}...<br/><b>Subsidy:</b> {ms.get('subsidy_available', '')[:30]}", body_style),
                Paragraph(ms.get("application_route", "")[:50] + "...", body_style)
            ])
        t_sch = Table(sch_data, colWidths=[2.2*inch, 1.0*inch, 2.2*inch, 2.0*inch])
        t_sch.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_gold),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ]))
        story.append(t_sch)
    story.append(Spacer(1, 10))

    # SECTION 19 & 20: Grounded Reasons & Formal Disclaimer
    story.append(Paragraph("7. Advisory Conclusion & Evidence-Grounded Reasons", h1_style))
    reasons_bullets = "<br/>• " + "<br/>• ".join(recommendation.get("reasons", ["No specific conditions noted."]))
    story.append(Paragraph(reasons_bullets, body_style))
    story.append(Spacer(1, 12))

    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#9CA3AF"), spaceAfter=6))
    story.append(Paragraph("<b>LEGAL & FINANCIAL DISCLAIMER:</b>", bold_style))
    story.append(Paragraph(
        "RuralBiz Navigator is an informational and decision-support tool created for Smart India Hackathon 2026. "
        "All calculations are generated deterministically based on standard financial formulas and prototype demographic models. "
        "Locality indices, customer estimates, and competitor records are simulated prototype data for demonstration only. "
        "This report does not constitute official lending approval, legal counsel, or financial guarantee. "
        "Final loan sanction, interest rates, and scheme subsidies depend solely on the discretion of official lending institutions and authorities.",
        disclaimer_style
    ))

    # Build Document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Save to disk if requested
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes

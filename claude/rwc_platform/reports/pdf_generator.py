"""
RWC Operations Intelligence Platform
PDF Report Generator — Executive Report Export
"""

import io
from datetime import datetime


def generate_pdf_report(kpis: dict, projects_df, briefing_text: str) -> bytes:
    """
    Generate a professional PDF executive report.
    Uses reportlab if available, falls back to a formatted bytes payload.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter,
            leftMargin=0.75*inch, rightMargin=0.75*inch,
            topMargin=0.75*inch, bottomMargin=0.75*inch,
        )

        BG = colors.HexColor("#0A0E1A")
        ACCENT = colors.HexColor("#F97316")
        WHITE = colors.HexColor("#F1F5F9")
        MUTED = colors.HexColor("#64748B")
        RED = colors.HexColor("#EF4444")
        GREEN = colors.HexColor("#10B981")
        YELLOW = colors.HexColor("#F59E0B")
        DARK = colors.HexColor("#111827")

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("Title", parent=styles["Title"],
            fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,
            backColor=BG, spaceAfter=4, alignment=TA_CENTER)
        subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, textColor=MUTED, alignment=TA_CENTER, spaceAfter=16)
        section_style = ParagraphStyle("Section", parent=styles["Heading2"],
            fontName="Helvetica-Bold", fontSize=13, textColor=ACCENT, spaceBefore=16, spaceAfter=6)
        body_style = ParagraphStyle("Body", parent=styles["Normal"],
            fontName="Helvetica", fontSize=9, textColor=WHITE, leading=14, spaceAfter=8)
        kpi_label = ParagraphStyle("KPILabel", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=8, textColor=MUTED)
        kpi_value = ParagraphStyle("KPIValue", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=18, textColor=ACCENT)

        date_str = datetime.today().strftime("%B %d, %Y")
        story = []

        # Header
        story.append(Paragraph("RWC CONSTRUCTION MANAGEMENT GROUP", title_style))
        story.append(Paragraph(f"Executive Operations Intelligence Report  |  {date_str}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=2, color=ACCENT))
        story.append(Spacer(1, 12))

        # KPI Summary Table
        story.append(Paragraph("PORTFOLIO KPI SUMMARY", section_style))
        kpi_data = [
            ["METRIC", "VALUE", "STATUS"],
            ["Active Projects", str(kpis.get("active_projects", "—")), "●"],
            ["Delayed Projects", str(kpis.get("delayed_projects", "—")), "⚠"],
            ["Total Workforce", str(kpis.get("total_workforce", "—")), "●"],
            ["Workforce Utilization", f"{kpis.get('workforce_utilization', '—')}%", "●"],
            ["Open Safety Risks", str(kpis.get("open_safety_risks", "—")), "⚠"],
            ["Material Delays", str(kpis.get("material_delays", "—")), "⚠"],
            ["Cost Exposure", f"${kpis.get('cost_exposure', 0):,.0f}", "⚠"],
            ["Efficiency Score", f"{kpis.get('efficiency_score', '—')}/100", "●"],
        ]
        kpi_table = Table(kpi_data, colWidths=[3*inch, 2*inch, 0.8*inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#0F1929"), colors.HexColor("#111827")]),
            ("TEXTCOLOR", (0, 1), (-1, -1), WHITE),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E2D45")),
            ("PADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 12))

        # Projects Table
        story.append(Paragraph("PROJECT STATUS OVERVIEW", section_style))
        proj_headers = ["Project Name", "Supervisor", "Progress", "Risk", "Confidence", "Status"]
        proj_data = [proj_headers]
        for _, row in projects_df.iterrows():
            proj_data.append([
                row["name"][:28],
                row["supervisor"],
                f"{row['progress']}%",
                row["schedule_risk"],
                f"{row['confidence']}%",
                row["status"],
            ])
        proj_table = Table(proj_data, colWidths=[2.1*inch, 1.3*inch, 0.7*inch, 0.8*inch, 0.9*inch, 1.0*inch])
        proj_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#0F1929"), colors.HexColor("#111827")]),
            ("TEXTCOLOR", (0, 1), (-1, -1), WHITE),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E2D45")),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(proj_table)
        story.append(Spacer(1, 12))

        # Briefing
        story.append(Paragraph("AI-GENERATED EXECUTIVE BRIEFING", section_style))
        clean_briefing = briefing_text.replace("**", "").replace("━", "—").replace("🔴", "[CRITICAL]").replace("🟠", "[HIGH]").replace("🟡", "[MEDIUM]").replace("✅", "[OK]")
        for para in clean_briefing.split("\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))

        # Footer
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=1, color=MUTED))
        footer_style = ParagraphStyle("Footer", parent=styles["Normal"],
            fontName="Helvetica", fontSize=7, textColor=MUTED, alignment=TA_CENTER)
        story.append(Paragraph(
            f"CONFIDENTIAL — RWC Operations Intelligence Platform | Generated {date_str} | AI-Assisted Analysis",
            footer_style
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    except ImportError:
        # Fallback: return a plain text "PDF" placeholder
        content = f"RWC EXECUTIVE REPORT\n{'='*60}\nGenerated: {datetime.today().strftime('%B %d, %Y')}\n\n"
        content += f"NOTE: Install 'reportlab' for full PDF generation.\n\npip install reportlab\n\n"
        content += f"KPI SUMMARY\n{'-'*40}\n"
        for k, v in kpis.items():
            content += f"{k.replace('_', ' ').title()}: {v}\n"
        content += f"\n\nEXECUTIVE BRIEFING\n{'-'*40}\n"
        content += briefing_text.replace("**", "").replace("━", "=")
        return content.encode("utf-8")

"""
PDF report generator.
FR-9.1: Generate PDF report with inputs, recommendations, estimates, compliance, disclaimers.
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib import colors


def generate_report(
    inputs: dict,
    recommendations: list[dict],
    compliance: dict,
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("PackSmart Recommendation Report", styles["Title"]))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Input Parameters", styles["Heading2"]))
    input_data = [
        ["Parameter", "Value"],
        ["Commodity", inputs.get("commodity_name", "N/A")],
        ["Shelf Life Target", f"{inputs.get('shelf_life_target_days', 'N/A')} days"],
        ["Pack Size", f"{inputs.get('pack_size_g', 'N/A')} g"],
        ["Storage Temperature", f"{inputs.get('storage_temp_c', 'N/A')} °C"],
        ["Storage Humidity", f"{inputs.get('storage_humidity_pct', 'N/A')} %"],
        ["Transport Mode", inputs.get("transport_mode", "N/A")],
        ["Budget per Unit", f"Rs. {inputs.get('budget_per_unit', 'N/A')}"],
    ]
    t = Table(input_data, colWidths=[120, 340])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Recommendations", styles["Heading2"]))
    for i, rec in enumerate(recommendations[:3], 1):
        elements.append(Paragraph(
            f"<b>Rank {i}: {rec.get('material_name', 'N/A')}</b> "
            f"(Score: {rec.get('score', 0):.2f})",
            styles["Heading3"]
        ))
        sl = rec.get("shelf_life", {})
        elements.append(Paragraph(
            f"Estimated Shelf Life: {sl.get('min_days', '?')}-{sl.get('max_days', '?')} days "
            f"({sl.get('model_used', 'N/A')})",
            styles["Normal"]
        ))
        cost = rec.get("cost_per_unit", 0)
        elements.append(Paragraph(
            f"Estimated Cost: Rs. {cost:.1f} per unit",
            styles["Normal"]
        ))
        elements.append(Paragraph(
            f"<i>{rec.get('explanation', '')}</i>",
            styles["Normal"]
        ))
        warnings = rec.get("warnings", [])
        if warnings:
            for w in warnings:
                elements.append(Paragraph(f"Warning: {w}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Compliance Notes", styles["Heading2"]))
    for note in compliance.get("warnings", []):
        elements.append(Paragraph(
            f"Warning: {note.get('message', '')} "
            f"({note.get('citation', '')})",
            styles["Normal"]
        ))
    for note in compliance.get("info_notes", []):
        elements.append(Paragraph(
            f"Info: {note.get('message', '')} "
            f"({note.get('citation', '')})",
            styles["Normal"]
        ))

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        compliance.get("disclaimer", "Results are estimates only."),
        styles["Normal"]
    ))

    doc.build(elements)
    return buffer.getvalue()

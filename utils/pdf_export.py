"""
PDF export — generates a beautifully formatted travel itinerary PDF using ReportLab.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

TEAL       = colors.HexColor("#0D9488")
TEAL_LIGHT = colors.HexColor("#CCFBF1")
NAVY       = colors.HexColor("#0F172A")
SLATE      = colors.HexColor("#475569")
WHITE      = colors.white
GREY_BG    = colors.HexColor("#F8FAFC")
BORDER     = colors.HexColor("#E2E8F0")

CATEGORY_COLORS = {
    "Sightseeing":      colors.HexColor("#3B82F6"),
    "Food":             colors.HexColor("#F59E0B"),
    "Food & Sightseeing": colors.HexColor("#F59E0B"),
    "Adventure":        colors.HexColor("#10B981"),
    "Entertainment":    colors.HexColor("#8B5CF6"),
    "Culture & Art":    colors.HexColor("#EC4899"),
    "Nightlife":        colors.HexColor("#6366F1"),
    "Shopping":         colors.HexColor("#F97316"),
    "Nature":           colors.HexColor("#22C55E"),
}
DEFAULT_CAT = colors.HexColor("#64748B")

TIME_EMOJI = {
    "Morning":   "🌅",
    "Lunch":     "🍽️",
    "Afternoon": "☀️",
    "Evening":   "🌆",
    "Dinner":    "🍷",
    "Night":     "🌙",
}


def _s():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Normal"],
            fontSize=24, textColor=WHITE, fontName="Helvetica-Bold",
            alignment=TA_CENTER, spaceAfter=2),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
            fontSize=11, textColor=TEAL_LIGHT, fontName="Helvetica",
            alignment=TA_CENTER),
        "day_hdr": ParagraphStyle("day_hdr", parent=base["Normal"],
            fontSize=13, textColor=WHITE, fontName="Helvetica-Bold", leftIndent=6),
        "day_cost": ParagraphStyle("day_cost", parent=base["Normal"],
            fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
            alignment=TA_RIGHT),
        "slot_time": ParagraphStyle("slot_time", parent=base["Normal"],
            fontSize=8.5, textColor=SLATE, fontName="Helvetica-Bold", leftIndent=4),
        "slot_act": ParagraphStyle("slot_act", parent=base["Normal"],
            fontSize=11, textColor=NAVY, fontName="Helvetica-Bold", leftIndent=4),
        "slot_det": ParagraphStyle("slot_det", parent=base["Normal"],
            fontSize=9, textColor=SLATE, fontName="Helvetica", leftIndent=4),
        "tip": ParagraphStyle("tip", parent=base["Normal"],
            fontSize=8.5, textColor=colors.HexColor("#166534"),
            fontName="Helvetica-Oblique", leftIndent=8,
            backColor=colors.HexColor("#F0FDF4"), borderPad=3),
        "sec_hdr": ParagraphStyle("sec_hdr", parent=base["Normal"],
            fontSize=12, textColor=TEAL, fontName="Helvetica-Bold",
            spaceAfter=4, spaceBefore=8),
        "body": ParagraphStyle("body", parent=base["Normal"],
            fontSize=9.5, textColor=NAVY, fontName="Helvetica",
            spaceAfter=3, leading=14),
        "chk": ParagraphStyle("chk", parent=base["Normal"],
            fontSize=9.5, textColor=NAVY, fontName="Helvetica",
            leftIndent=10, spaceAfter=2),
        "footer": ParagraphStyle("footer", parent=base["Normal"],
            fontSize=8, textColor=SLATE,
            fontName="Helvetica-Oblique", alignment=TA_CENTER),
    }


def generate_pdf(itinerary: dict, trip_name: str = "My Trip") -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"{trip_name} — Travel Itinerary")

    S = _s()
    story = []
    destination = itinerary.get("destination", trip_name)
    days        = itinerary.get("days", [])
    currency    = itinerary.get("currency", "USD")
    total_cost  = itinerary.get("total_estimated_cost_usd", 0)
    W = doc.width

    # Cover header
    hdr = Table([[Paragraph(f"✈  {destination}", S["title"])]],
                colWidths=[W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), TEAL),
        ("TOPPADDING",    (0,0),(-1,-1), 14),
        ("BOTTOMPADDING", (0,0),(-1,-1), 14),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.2*cm))

    sub = Table([[Paragraph(
        f"{trip_name}  |  {len(days)}-Day Adventure  |  Est. ${total_cost:,} USD",
        S["subtitle"])]],
        colWidths=[W])
    sub.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
    ]))
    story.append(sub)
    story.append(Spacer(1, 0.5*cm))

    # Days
    for day_data in days:
        day_num   = day_data.get("day", "?")
        theme     = day_data.get("theme", "")
        daily_tot = day_data.get("daily_total_usd", 0)
        slots     = day_data.get("slots", [])

        day_bar = Table(
            [[Paragraph(f"Day {day_num}  ·  {theme}", S["day_hdr"]),
              Paragraph(f"${daily_tot} USD", S["day_cost"])]],
            colWidths=[W*0.78, W*0.22])
        day_bar.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), TEAL),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("ALIGN",         (1,0),(1,0), "RIGHT"),
            ("RIGHTPADDING",  (1,0),(1,0), 8),
        ]))
        story.append(KeepTogether([day_bar, Spacer(1, 0.1*cm)]))

        for slot in slots:
            ts       = slot.get("time_slot", "")
            activity = slot.get("activity", "")
            location = slot.get("location", "")
            dur      = slot.get("duration_hrs", 0)
            cost     = slot.get("cost_usd", 0)
            cat      = slot.get("category", "")
            tip      = slot.get("tip", "")
            emoji    = TIME_EMOJI.get(ts, "•")
            cat_col  = CATEGORY_COLORS.get(cat, DEFAULT_CAT)

            badge = Table(
                [[Paragraph(f" {cat} ", ParagraphStyle("b", fontSize=7,
                    textColor=WHITE, fontName="Helvetica-Bold",
                    alignment=TA_CENTER))]],
                colWidths=[max(len(cat)*5+12, 40)])
            badge.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), cat_col),
                ("TOPPADDING",    (0,0),(-1,-1), 2),
                ("BOTTOMPADDING", (0,0),(-1,-1), 2),
                ("LEFTPADDING",   (0,0),(-1,-1), 4),
                ("RIGHTPADDING",  (0,0),(-1,-1), 4),
            ]))

            elems = [
                Paragraph(f"{emoji}  {ts}", S["slot_time"]),
                Paragraph(activity, S["slot_act"]),
                Paragraph(f"📍 {location}   ⏱ {dur}h   💰 ${cost} USD", S["slot_det"]),
            ]
            if tip:
                elems.append(Paragraph(f"💡 {tip}", S["tip"]))

            card = Table([[elems, badge]], colWidths=[W*0.84, W*0.16])
            card.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), GREY_BG),
                ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
                ("TOPPADDING",    (0,0),(-1,-1), 6),
                ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                ("LEFTPADDING",   (0,0),(-1,-1), 6),
                ("VALIGN",        (0,0),(-1,-1), "TOP"),
                ("ALIGN",         (1,0),(1,0), "CENTER"),
            ]))
            story.append(KeepTogether([card, Spacer(1, 0.12*cm)]))

        story.append(Spacer(1, 0.35*cm))

    # Cost summary
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("💰  Estimated Cost Summary", S["sec_hdr"]))
    rows = [["Day", "Theme", "Estimated Cost"]]
    for d in days:
        rows.append([f"Day {d.get('day','?')}", d.get("theme",""),
                     f"${d.get('daily_total_usd',0):,} USD"])
    rows.append(["", "TOTAL", f"${total_cost:,} USD"])
    ct = Table(rows, colWidths=[W*0.1, W*0.67, W*0.23])
    ct.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0), TEAL),
        ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
        ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",       (0,0),(-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1),(-1,-2), [WHITE, GREY_BG]),
        ("BACKGROUND",     (0,-1),(-1,-1), NAVY),
        ("TEXTCOLOR",      (0,-1),(-1,-1), WHITE),
        ("FONTNAME",       (0,-1),(-1,-1), "Helvetica-Bold"),
        ("ALIGN",          (2,0),(2,-1), "RIGHT"),
        ("BOX",            (0,0),(-1,-1), 0.5, BORDER),
        ("INNERGRID",      (0,0),(-1,-1), 0.25, BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.4*cm))

    # Packing checklist
    packing = itinerary.get("packing_tips", [])
    if packing:
        story.append(Paragraph("🎒  Packing Checklist", S["sec_hdr"]))
        for t in packing:
            story.append(Paragraph(f"☐  {t}", S["chk"]))
        story.append(Spacer(1, 0.4*cm))

    # Emergency contacts
    emergency = itinerary.get("emergency_contacts", {})
    if emergency:
        story.append(Paragraph("🚨  Emergency Contacts", S["sec_hdr"]))
        for k, v in emergency.items():
            story.append(Paragraph(f"<b>{k.replace('_',' ').title()}:</b>  {v}", S["body"]))
        story.append(Spacer(1, 0.4*cm))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Generated by Personalized Travel Itinerary Planner · Powered by Gemini AI",
        S["footer"]))

    doc.build(story)
    return buf.getvalue()

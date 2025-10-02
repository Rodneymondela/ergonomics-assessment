from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from flask import send_file
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def assessments_list_pdf(rows: list[dict]) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 15 * mm
    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, "Ergonomics Assessments")
    y -= 8 * mm
    c.setFont("Helvetica-Bold", 10)
    headers = ["ID", "Date", "Job Role", "RULA", "REBA", "NIOSH LI", "Risk"]
    col_widths = [15*mm, 25*mm, 65*mm, 18*mm, 18*mm, 22*mm, 22*mm]
    x = x_margin
    for h, w in zip(headers, col_widths):
        c.drawString(x, y, h); x += w
    y -= 6 * mm; c.setFont("Helvetica", 10)
    for r in rows:
        if y < 20 * mm:
            c.showPage(); y = height - 20 * mm
            c.setFont("Helvetica-Bold", 10); x = x_margin
            for h, w in zip(headers, col_widths): c.drawString(x, y, h); x += w
            y -= 6 * mm; c.setFont("Helvetica", 10)
        x = x_margin
        values = [str(r.get("id","")), r.get("date",""), r.get("job_title","")[:45], str(r.get("rula","")), str(r.get("reba","")), str(r.get("niosh_li","")), r.get("risk","")]
        for v, w in zip(values, col_widths):
            c.drawString(x, y, v); x += w
        y -= 6 * mm
    c.showPage(); c.save(); buffer.seek(0)
    return buffer.getvalue()

def send_assessments_pdf(rows: list[dict]):
    pdf_bytes = assessments_list_pdf(rows)
    return send_file(BytesIO(pdf_bytes), mimetype="application/pdf", as_attachment=True, download_name="assessments.pdf")

def assessment_detail_pdf(a: dict, media_paths: list[str], logo_path: str | None = None) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 15 * mm; y = height - 20 * mm
    if logo_path:
        try:
            img = ImageReader(logo_path)
            c.drawImage(img, x_margin, y-10*mm, width=25*mm, height=10*mm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin + (30*mm if logo_path else 0), y, "Ergonomics Assessment Report")
    y -= 12 * mm
    meta = [
        ["Assessment ID", str(a.get("id","")), "Date", a.get("date","")],
        ["Assessor", a.get("assessor",""), "Job Role", a.get("job_title","")],
        ["Company", a.get("company",""), "Site", a.get("site","")],
    ]
    t = Table(meta, colWidths=[28*mm, 62*mm, 20*mm, 60*mm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.grey),("INNERGRID",(0,0),(-1,-1),0.25,colors.grey),("BACKGROUND",(0,0),(-1,0),colors.whitesmoke),("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(0,0),(-1,-1),"LEFT")]))
    w, h = t.wrapOn(c, width - 2*x_margin, y); t.drawOn(c, x_margin, y - h); y -= (h + 8*mm)
    c.setFont("Helvetica-Bold", 12); c.drawString(x_margin, y, "Scores"); y -= 6*mm
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, f"RULA: {a.get('rula','')}"); c.drawString(x_margin + 35*mm, y, f"REBA: {a.get('reba','')}"); c.drawString(x_margin + 70*mm, y, f"NIOSH LI: {a.get('niosh_li','')} (RWL {a.get('rwl','')} kg)"); c.drawString(x_margin + 135*mm, y, f"Risk: {a.get('risk','')}"); y -= 10*mm
    obs = a.get("observation","") or ""
    c.setFont("Helvetica-Bold", 12); c.drawString(x_margin, y, "Observation"); y -= 6*mm
    c.setFont("Helvetica", 10)
    for line in (obs.replace("\r","").split("\n")):
        if y < 25*mm: c.showPage(); y = height - 20*mm; c.setFont("Helvetica", 10)
        c.drawString(x_margin, y, line[:140]); y -= 5*mm
    y -= 4*mm
    if media_paths:
        c.setFont("Helvetica-Bold", 12)
        if y < 50*mm: c.showPage(); y = height - 20*mm
        c.drawString(x_margin, y, "Media Evidence"); y -= 6*mm
        thumb_w, thumb_h, gap = 45*mm, 32*mm, 6*mm
        x = x_margin; row_h = thumb_h + 10
        for p in media_paths:
            if y < (thumb_h + 30*mm): c.showPage(); y = height - 20*mm; x = x_margin
            try:
                c.drawImage(ImageReader(p), x, y - thumb_h, width=thumb_w, height=thumb_h, preserveAspectRatio=True, mask='auto')
                c.rect(x, y - thumb_h, thumb_w, thumb_h, stroke=1, fill=0)
            except Exception:
                c.setFont("Helvetica", 8); c.drawString(x, y - 10, f"(couldn't render: {p})")
            x += thumb_w + gap
            if x + thumb_w > width - x_margin:
                x = x_margin; y -= row_h
        y -= 8*mm
    if y < 40*mm: c.showPage(); y = height - 20*mm
    c.setFont("Helvetica-Bold", 12); c.drawString(x_margin, y, "Sign-off"); y -= 8*mm
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, "Assessor Signature: ________________________________       Date: _____________"); y -= 8*mm
    c.drawString(x_margin, y, "Client/Responsible Person: _________________________       Date: _____________"); y -= 8*mm
    c.showPage(); c.save(); buffer.seek(0)
    return buffer.getvalue()

def send_assessment_pdf(a: dict, media_paths: list[str], logo_path: str | None = None):
    pdf_bytes = assessment_detail_pdf(a, media_paths, logo_path)
    return send_file(BytesIO(pdf_bytes), mimetype="application/pdf", as_attachment=True, download_name=f"assessment_{a.get('id','')}.pdf")

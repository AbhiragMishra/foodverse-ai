from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import os

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(self._pagesize[0] - 36, 20, page_str)
        self.drawString(36, 20, "FoodVerse AI — AI/ML & Generative AI Track Project Deliverable")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 30, self._pagesize[0] - 36, 30)
        self.restoreState()

def get_theme_styles():
    styles = getSampleStyleSheet()
    
    body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b")
    )
    
    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )
    
    th_style = ParagraphStyle(
        'CustomTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )
    
    h1 = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    
    h2 = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=8,
        spaceAfter=4
    )

    desc_style = ParagraphStyle(
        'CustomDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8
    )

    return {
        'body': body,
        'body_bold': body_bold,
        'th': th_style,
        'h1': h1,
        'h2': h2,
        'desc': desc_style
    }

def create_rubric_header(title, max_marks="3 Marks", date="15 March 2026", team_id="FV-AI-2026-X1", project_name="FoodVerse AI"):
    """Builds the exact evaluation header matching Ravi Teja's template sheets."""
    styles = get_theme_styles()
    
    header_data = [
        [
            Paragraph(f"<b>Template:</b> {title}", styles['body_bold']),
            Paragraph(f"<b>Maximum Marks:</b> {max_marks}", styles['body_bold'])
        ],
        [
            Paragraph(f"<b>Date:</b> {date}", styles['body']),
            Paragraph(f"<b>Team ID:</b> {team_id}", styles['body'])
        ],
        [
            Paragraph(f"<b>Project Name:</b> {project_name}", styles['body_bold']),
            Paragraph("<b>Track:</b> AI/ML & Generative AI", styles['body'])
        ]
    ]
    
    t = Table(header_data, colWidths=[320, 220])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def make_table(headers, rows, col_widths, is_header=True):
    styles = get_theme_styles()
    data = []
    if is_header:
        data.append([Paragraph(h, styles['th']) if isinstance(h, str) else h for h in headers])
    
    for row in rows:
        formatted_row = []
        for cell in row:
            if isinstance(cell, str):
                formatted_row.append(Paragraph(cell, styles['body']))
            else:
                formatted_row.append(cell)
        data.append(formatted_row)
        
    t = Table(data, colWidths=col_widths, repeatRows=1 if is_header else 0)
    
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f766e")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0f766e")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]
    
    for r in range(1, len(data)):
        if r % 2 == 0:
            style.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor("#f8fafc")))
        else:
            style.append(('BACKGROUND', (0, r), (-1, r), colors.white))
            
    t.setStyle(TableStyle(style))
    return t

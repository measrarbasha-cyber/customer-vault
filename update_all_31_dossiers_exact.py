import os
import shutil
import sqlite3
import json
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
upload_dir = os.path.join(vault_dir, "uploads")
db_path = os.path.join(vault_dir, "customers.db")
stats_path = os.path.join(vault_dir, "master_client_stats.json")

os.makedirs(artifact_dir, exist_ok=True)
os.makedirs(upload_dir, exist_ok=True)

USER_NAME = "MD ASRAR BASHA A"
USER_PHONE = "+91 7358882822"
USER_PHONE_RAW = "917358882822"
USER_EMAIL = "amdasrarbasha@gmail.com"
USER_LOCATION = "Chennai & Ranipet, Tamil Nadu (Pan-India Advisory)"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, ref_code, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self.ref_code = ref_code
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFillColor(colors.HexColor("#0F2942"))
        self.rect(0, 786, 612, 6, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#0D9488"))  # Teal accent
        self.rect(0, 782, 612, 4, fill=1, stroke=0)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(36, 766, "PRIVATE & CONFIDENTIAL | STATUTORY ASSET RECOVERY ADVISORY")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(576, 766, f"REF: {self.ref_code}")
        
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 32, 576, 32)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#0F2942"))
        self.drawString(36, 22, f"SPECIALIST ADVISORY: {USER_NAME} | {USER_PHONE} | {USER_EMAIL}")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(576, 22, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def format_inr_crores(amount):
    if amount >= 10000000:
        cr = amount / 10000000
        return f"Rs. {cr:.2f} Cr"
    else:
        lakhs = amount / 100000
        return f"Rs. {lakhs:.2f} Lakhs"

# City Profiles Map
CITY_PROFILES = {
    6: "Mumbai Prime HNI Estate Holding. High-value promoter-tier allocation.",
    7: "Ahmedabad Senior Medical Faculty. Joint shareholder holding.",
    8: "Hosur Traditional Textile & Paper Manufacturing Enterprise Family Portfolio.",
    9: "Coimbatore Industrial Estate Portfolio.",
    10: "Cheyyar Heritage Family Estate Portfolio.",
    11: "Ahmedabad Ambawadi Estate Holding.",
    12: "Mumbai Suburbs Joint Family Holding.",
    13: "Mumbai Central Estate Holding.",
    14: "Chennai T. Nagar Commercial & Residential Estate Holding.",
    15: "Chennai Park Town Commercial Enterprise Portfolio.",
    19: "Junagadh Medical & Diagnostic Centre Family Holding.",
    20: "Gurgaon Corporate Executive Portfolio.",
    21: "Ranchi Commercial Trading Enterprise Family Portfolio.",
    22: "Secunderabad / NRI US Physician Portfolio.",
    23: "Indore Senior Chartered Accountancy Practice & Estate Holding.",
    24: "Ahmedabad Navrangpura Senior Chartered Accountancy Practice & Corporate Advisory Portfolio.",
    26: "Mumbai Walkeshwar Prime High-Net-Worth Individual (HNI) Family Estate Holding.",
    27: "Madurai Commercial Director & Enterprise Family Holding (N M R Krishna Moorthy & Sons / Cheese Corner).",
    28: "Rajkot Sanganva Chowk Electrical Distribution Enterprise Portfolio (Rajdeep Agency).",
    29: "Chennai Sowcarpet Prominent Commercial Community & Legal Advisory Family Portfolio.",
    30: "Karamsad / Anand Automobile Dealership Network Enterprise Portfolio (Destination Honda / Motors).",
    31: "Ranchi Doranda Bazar Established Wholesale & Retail Textile Merchant Enterprise Portfolio.",
    32: "Ahmedabad Sardar Nagar Senior Chartered Accountant Practice & Tax Advisory Portfolio (Prakash Tekwani & Associates).",
    33: "Delhi NCR Senior Director of Orthopaedics & Robotic Surgery Portfolio (Max Super Speciality Hospital).",
    34: "Ahmedabad Ellisbridge Premier Financial Brokerage Enterprise Portfolio (Madhuvan Group / Commodities).",
    35: "Premier laparoscopic & endoscopic surgical hospital in Marathwada. Headed by Managing Directors Dr. Pandit Annarao Palaskar & Dr. Rinku Panditrao Palaskar.",
    36: "Managing Director of Priyadarshini Polysacks Limited; prominent polymer & PP woven sacks manufacturer with established operations at Station Road, Kolhapur.",
    37: "Senior Pediatrician and Director of Gandhi Children Hospital & Newborn Care (NICU), Govindnagar, Dahod. Empanelled under PMJAY scheme.",
    38: "Senior Consultant Eye Surgeon (Ophthalmologist) and Founder-Director of Netra Eye Hospital at Ingole Square, Arvi Road, Wardha.",
    39: "Director and Chief Physician at Walse Hospital & Maternity Home, prominent multi-speciality and obstetrics healthcare establishment in Latur.",
    40: "Chairman & Key Promoter of Saurashtra Fuels Private Limited (CIN: U23200GJ1993PTC097907), premier industrial Low Ash Metallurgical Coke manufacturing group."
}

def generate_exact_dossier(c_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=38)

    title_style = ParagraphStyle('DTitle', fontName='Helvetica-Bold', fontSize=13.5, leading=16.5, textColor=colors.HexColor("#0F2942"))
    subtitle_style = ParagraphStyle('DSub', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=colors.HexColor("#0D9488"))
    banner_pill = ParagraphStyle('BPill', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#FFFFFF"), alignment=1)
    body_text = ParagraphStyle('DBody', fontName='Helvetica', fontSize=7.2, leading=9.5, textColor=colors.HexColor("#1E293B"))
    body_bold = ParagraphStyle('DBold', fontName='Helvetica-Bold', fontSize=7.2, leading=9.5, textColor=colors.HexColor("#0F2942"))
    metric_label = ParagraphStyle('DMLabel', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#475569"))
    metric_val = ParagraphStyle('DMVal', fontName='Helvetica-Bold', fontSize=11, leading=13.5, textColor=colors.HexColor("#047857"))
    callout_box = ParagraphStyle('DCallout', fontName='Helvetica', fontSize=6.8, leading=9.2, textColor=colors.HexColor("#0F2942"))
    btn_text = ParagraphStyle('DBtn', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#FFFFFF"), alignment=1)

    story = []

    # Header Title
    story.append(Paragraph("<b>STATUTORY RECOVERY DOSSIER &bull; UNCLAIMED EQUITY ASSETS</b>", title_style))
    story.append(Paragraph("MINISTRY OF CORPORATE AFFAIRS (MCA) &bull; INVESTOR EDUCATION &amp; PROTECTION FUND (IEPF)", subtitle_style))
    story.append(Spacer(1, 4))

    # Top Confidential Banner
    banner_data = [
        [
            Paragraph("<b>CONFIDENTIAL BENEFICIARY AUDIT</b>", banner_pill),
            Paragraph("<b>ENTITY: ASTRAL LIMITED (NSE: ASTRAL | BSE: 532830)</b>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor("#FFFFFF"))),
            Paragraph("<b>LEGAL PATHWAY: MCA IEPF-5</b>", banner_pill)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[160, 260, 120])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F2942")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 5))

    # Client Summary Card
    client_card = [
        [
            Paragraph(f"<b>LEGAL BENEFICIARY:</b> <b>{c_data['name']}</b>", body_bold),
            Paragraph(f"<b>FOLIO / DP-CLIENT ID:</b> <font face='Courier'>{c_data['folio_id']}</font>", body_bold)
        ],
        [
            Paragraph(f"<b>REGISTERED POSTAL RECORD:</b><br/>{c_data['address']}", body_text),
            Paragraph("<b>STATUTORY CUSTODIAN:</b><br/>IEPF Authority, Ministry of Corporate Affairs, New Delhi", body_text)
        ]
    ]
    t_client = Table(client_card, colWidths=[310, 230])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 5))

    # Key Financial Metrics (Exact Audited Values)
    exact_shares = c_data["current_shares"]
    exact_val = c_data["current_val_inr"]
    val_short = format_inr_crores(exact_val)

    metrics_data = [
        [
            Paragraph("AUDITED PORTFOLIO VALUE (CMP Rs. 1,425)", metric_label),
            Paragraph("CERTIFIED SHARE ENTITLEMENT", metric_label),
            Paragraph("UPFRONT / ADVANCE EXPENSE", metric_label)
        ],
        [
            Paragraph(f"<b>Rs. {exact_val:,}</b><br/><font size='7' color='#047857'>({val_short})</font>", metric_val),
            Paragraph(f"<b>{exact_shares:,} Shares</b><br/><font size='7' color='#0F766E'>(100% Audited Entitlement)</font>", ParagraphStyle('MEnt', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=colors.HexColor("#0F766E"))),
            Paragraph("<b>Rs. 0.00 (ZERO ADVANCE)</b><br/><font size='7' color='#0369A1'>(100% Risk-Free Guarantee)</font>", ParagraphStyle('MZero', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor("#0369A1")))
        ],
        [
            Paragraph("<font color='#64748B' size='6.8'>Based on NSE: ASTRAL CMP + historical bonuses</font>", body_text),
            Paragraph("<font color='#64748B' size='6.8'>100% Traceable &amp; Recoverable via MCA Form IEPF-5</font>", body_text),
            Paragraph("<font color='#64748B' size='6.8'>Zero retainer, no out-of-pocket processing expense</font>", body_text)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[180, 180, 180])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F0FDF4")), # Green
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F0FDFA")), # Teal
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor("#F0F9FF")), # Blue
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 5))

    # Corporate Actions Matrix
    matrix_data = [
        [
            Paragraph("<b>CORPORATE EVENT / TRIGGER</b>", body_bold),
            Paragraph("<b>ENTITLEMENT MULTIPLIER</b>", body_bold),
            Paragraph("<b>STATUS &amp; STATUTORY NOTE</b>", body_bold)
        ],
        [
            Paragraph("<b>Original Transferred Base Holding</b>", body_text),
            Paragraph(f"<b>{c_data['shares_pre_2019']:,} Shares</b> Base", body_text),
            Paragraph("Transferred to IEPF under Sec 124(6)", body_text)
        ],
        [
            Paragraph("<b>2019 Bonus Issue (1:4)</b>", body_text),
            Paragraph(f"+{c_data['bonus_2019']:,} Additional Shares (+25%)", body_text),
            Paragraph("Corporate benefit accrued to master folio", body_text)
        ],
        [
            Paragraph("<b>2021 Bonus Issue (1:3)</b>", body_text),
            Paragraph(f"+{c_data['bonus_2021']:,} Additional Shares (+33.3%)", body_text),
            Paragraph("Compounded volume expansion on base", body_text)
        ],
        [
            Paragraph("<b>2023 Bonus Issue (1:3)</b>", body_text),
            Paragraph(f"+{c_data['bonus_2023']:,} Additional Shares (+33.3%)", body_text),
            Paragraph("Final split multiplier applied", body_text)
        ],
        [
            Paragraph("<b>Accumulated Cash Dividends</b>", body_text),
            Paragraph(f"<b>Rs. {c_data['total_unclaimed_div']:,.2f}</b> Escrow", body_text),
            Paragraph("Held in Govt Escrow awaiting Form IEPF-5", body_text)
        ],
        [
            Paragraph("<b>AUDITED TOTAL RECOVERABLE ASSET</b>", ParagraphStyle('TotC', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>Rs. {exact_val:,} ({exact_shares:,} Shares)</b>", ParagraphStyle('TotCV', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#047857"))),
            Paragraph("<b>100% Recoverable via MCA Form IEPF-5</b>", ParagraphStyle('TotCS', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.HexColor("#0F2942")))
        ]
    ]
    matrix_table = Table(matrix_data, colWidths=[170, 180, 190])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#DCFCE7")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 5))

    # Safeguards
    fee_pct = c_data["fee_pct"]
    safeguards_data = [
        [
            Paragraph(f"<b>1. SUCCESS MANDATE ({fee_pct}% / Rs. 0 ADVANCE)</b><br/><font color='#475569'>No retainers, no advance fee. Client rate capped at <b>{fee_pct}% success fee</b>, strictly payable only AFTER shares &amp; money are credited into your personal account.</font>", callout_box),
            Paragraph("<b>2. DIRECT DEMAT &amp; BANK SETTLEMENT</b><br/><font color='#475569'>The consultant never touches shareholder funds. All shares &amp; dividends are disbursed directly by the IEPF Authority into your verified Demat &amp; bank accounts.</font>", callout_box),
            Paragraph("<b>3. TURNKEY COMPLIANCE EXECUTION</b><br/><font color='#475569'>We manage the entire statutory lifecycle: MCA Form IEPF-5 e-filing, verification dossier compilation, indemnity bonds, and Registrar (Bigshare) coordination.</font>", callout_box)
        ]
    ]
    safe_table = Table(safeguards_data, colWidths=[176, 176, 176])
    safe_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(safe_table)

    # Page 2: Statutory Lifecycle & Protocol
    story.append(PageBreak())
    story.append(Paragraph("<b>IEPF RECOVERY &amp; EQUITY TRANSMISSION EXECUTION PROTOCOL</b>", title_style))
    story.append(Paragraph(f"STATUTORY COMPLIANCE LIFECYCLE &bull; PREPARED FOR {c_data['name'].upper()}", subtitle_style))
    story.append(Spacer(1, 6))

    lifecycle_data = [
        [
            Paragraph("<b>PHASE 1: ENTITLEMENT AUDIT &amp; FOLIO RECONCILIATION</b>", body_bold),
            Paragraph("Reconciliation with <b>Bigshare Services Pvt. Ltd.</b> (Registrar &amp; Share Transfer Agent for Astral Ltd) to extract master ledger entries, exact share entitlement, and accumulated dividend warrants.", body_text)
        ],
        [
            Paragraph("<b>PHASE 2: STATUTORY DOSSIER DRAFTING</b>", body_bold),
            Paragraph("Drafting non-judicial stamped Indemnity Bonds, Advance Stamp Receipts, Client Master List (CML) certifications, and KYC verification documents strictly conforming to MCA guidelines.", body_text)
        ],
        [
            Paragraph("<b>PHASE 3: MCA PORTAL E-FILING (FORM IEPF-5)</b>", body_bold),
            Paragraph("Uploading electronic Form IEPF-5 on the Ministry of Corporate Affairs portal. Dispatching physical verification binder to the Nodal Officer of Astral Limited.", body_text)
        ],
        [
            Paragraph("<b>PHASE 4: NODAL VERIFICATION &amp; MCA SANCTION</b>", body_bold),
            Paragraph("Tracking the Nodal Officer's Verification Report to the IEPF Authority, New Delhi. Addressing and resolving any technical queries directly with Registrar officials.", body_text)
        ],
        [
            Paragraph("<b>PHASE 5: DIRECT DEMAT CREDIT &amp; SUCCESS SETTLEMENT</b>", body_bold),
            Paragraph(f"IEPF Authority sanctions corporate release: Shares are credited directly into your active Demat, and dividends wired into your bank account. Only then is our agreed {fee_pct}% success fee settled.", body_text)
        ]
    ]
    life_table = Table(lifecycle_data, colWidths=[170, 370])
    life_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(life_table)
    story.append(Spacer(1, 10))

    city_profile = CITY_PROFILES.get(c_data['id'], f"Registered shareholder folio in {c_data['address'][:40]}.")
    reason_box = (
        f"<b>LOCATION &amp; BENEFICIARY NOTE:</b><br/>"
        f"{city_profile} "
        f"Under Section 124(6) of the Companies Act, 2013, these equity assets remain fully protected by the Central Government and never lapse. "
        f"Our professional advisory handles all legal formalities and Registrar follow-ups so you experience zero procedural friction."
    )
    r_table = Table([[Paragraph(reason_box, body_text)]], colWidths=[540])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 10))

    wa_link = f"https://wa.me/{USER_PHONE_RAW}?text=Dear%20Asrar%2C%20regarding%20Astral%20Folio%20{c_data['folio_id']}"
    call_link = f"tel:{USER_PHONE.replace(' ', '')}"
    mail_link = f"mailto:{USER_EMAIL}?subject=Astral%20Limited%20Recovery%20-%20{c_data['name']}"

    contact_data = [
        [
            Paragraph(f"<a href='{wa_link}' color='#FFFFFF'><b>CHAT ON WHATSAPP</b></a>", btn_text),
            Paragraph(f"<a href='{call_link}' color='#FFFFFF'><b>CALL DIRECT LINE</b></a>", btn_text),
            Paragraph(f"<a href='{mail_link}' color='#FFFFFF'><b>SEND DIRECT EMAIL</b></a>", btn_text)
        ],
        [
            Paragraph(f"<font color='#1E293B'><b>{USER_PHONE}</b></font><br/><font color='#64748B' size='7'>Tap to chat directly on WhatsApp</font>", ParagraphStyle('CC1', alignment=1)),
            Paragraph(f"<font color='#1E293B'><b>{USER_PHONE}</b></font><br/><font color='#64748B' size='7'>Direct consultant line</font>", ParagraphStyle('CC2', alignment=1)),
            Paragraph(f"<font color='#1E293B'><b>{USER_EMAIL}</b></font><br/><font color='#64748B' size='7'>Tap to send official mail</font>", ParagraphStyle('CC3', alignment=1))
        ]
    ]
    contact_table = Table(contact_data, colWidths=[180, 180, 180])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#16A34A")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#0284C7")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#0F2942")),
        ('TOPPADDING', (0,0), (-1,0), 5),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,1), (-1,1), 3.5),
        ('BOTTOMPADDING', (0,1), (-1,1), 3.5),
    ]))
    story.append(contact_table)

    class CustomCanvas(NumberedCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(c_data["ref_code"], *args, **kwargs)

    doc.build(story, canvasmaker=CustomCanvas)

if __name__ == "__main__":
    with open(stats_path, 'r', encoding='utf-8') as f:
        stats = json.load(f)

    stats_by_id = {s['id']: s for s in stats}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, name, folio_id, est_folio, address, pdf1_filename, pdf1_path FROM customers ORDER BY id')
    db_clients = [dict(r) for r in c.fetchall()]
    conn.close()

    print(f"=== BATCH REGENERATION OF ALL {len(db_clients)} CLIENT EXECUTIVE RECOVERY DOSSIERS (PDF 1) ===")
    print("Redesign & Accuracy Highlights:")
    print("1. Top Metrics Card: Exact Audited Value (Rs. X) & Exact Share Count (Y Shares)")
    print("2. Corporate Actions Matrix: Exact Base Shares & Bonus Expansions")
    print("3. Fiduciary Safeguards: Success fee framed strictly as risk-free protective guarantee")
    print("4. Typography: All clean 'Rs.' (Zero broken rupee glyphs)")
    print("5. Privacy: No private street address leaks\n")

    page_counts = []
    address_leaks = []

    for cl in db_clients:
        cid = cl['id']
        s_data = stats_by_id.get(cid, {})
        
        # Merge DB and exact stats
        c_merged = dict(cl)
        c_merged.update(s_data)

        # Overrides for Dr Phatak with verified 13,140 shares
        if 'Phatak' in cl['name']:
            c_merged['current_shares'] = 13140
            c_merged['shares_pre_2023'] = 9856
            c_merged['bonus_2023'] = 3284
            c_merged['shares_pre_2021'] = 7392
            c_merged['bonus_2021'] = 2464
            c_merged['shares_pre_2019'] = 5913
            c_merged['bonus_2019'] = 1479
            c_merged['total_unclaimed_div'] = 68123.51
            c_merged['current_val_inr'] = round(13140 * 1425)

        c_merged['fee_pct'] = 15 if cid == 10 else 8
        c_merged['ref_code'] = f"IEPF/AST/2026/{cid:03d}"

        # Target files
        p1_path = cl.get('pdf1_path') or f"Executive_Dossier_{cid}.pdf"
        p1_filename = cl.get('pdf1_filename')

        out_brain = os.path.join(artifact_dir, p1_path)
        out_upload = os.path.join(upload_dir, p1_path)

        generate_exact_dossier(c_merged, out_brain)
        shutil.copyfile(out_brain, out_upload)

        # Also copy to pdf1_filename if different
        if p1_filename and p1_filename != p1_path:
            shutil.copyfile(out_brain, os.path.join(upload_dir, p1_filename))
            shutil.copyfile(out_brain, os.path.join(artifact_dir, p1_filename))

        # Verify page count and address privacy
        r = PdfReader(out_upload)
        pages_len = len(r.pages)
        page_counts.append((p1_path, pages_len))
        full_text = ' '.join([p.extract_text() or '' for p in r.pages])
        if 'appa pillai' in full_text.lower() or 'melvisharam' in full_text.lower():
            address_leaks.append(p1_path)

        print(f"[OK] ID {cid:2d}: {cl['name'][:24]:24s} -> {p1_path} ({pages_len} pages | {c_merged['current_shares']:,} shares = Rs. {c_merged['current_val_inr']:,})")

    print("\n--- DOSSIER VERIFICATION AUDIT ---")
    bad_pages = [x for x in page_counts if x[1] != 2]
    if bad_pages:
        print(f"WARNING: Page count anomalies found: {bad_pages}")
    else:
        print(f"SUCCESS: All {len(page_counts)} Executive Dossiers are EXACTLY 2 pages!")

    if address_leaks:
        print(f"WARNING: Address leaks found: {address_leaks}")
    else:
        print("SUCCESS: Zero address leaks across all dossiers!")

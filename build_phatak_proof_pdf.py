import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pymupdf

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                self.setStrokeColor(colors.HexColor('#0f172a'))
                self.setLineWidth(1)
                self.rect(20, 20, 555.28, 801.89)
                
                self.setFont('Helvetica-Bold', 7)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawString(30, 28, 'OFFICIAL STATUTORY AUDIT DOSSIER')
                self.setFont('Helvetica', 7)
                self.drawString(205, 28, '|  STRICTLY CONFIDENTIAL — FOR BENEFICIARY REVIEW ONLY')
                page_str = f'Page {self._pageNumber} of {num_pages}'
                self.drawRightString(565, 28, page_str)
                self.restoreState()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def generate_pdf():
    pdf_path = 'uploads/Dr_Sanjeev_Phatak_Sanu_Phatak_Official_Shares_Calculation_and_Gazette_Proof.pdf'
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=22,
        rightMargin=22,
        topMargin=22,
        bottomMargin=26
    )
    
    styles = getSampleStyleSheet()
    
    c_navy = colors.HexColor('#0f172a')
    c_blue = colors.HexColor('#0284c7')
    c_dark = colors.HexColor('#1e293b')
    c_slate = colors.HexColor('#475569')
    c_bg = colors.HexColor('#f8fafc')
    c_green = colors.HexColor('#15803d')
    c_red = colors.HexColor('#b91c1c')
    
    p_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=10, leading=12.5, textColor=c_navy)
    p_note = ParagraphStyle('DocNote', fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=c_dark)
    
    story = []
    
    # =========================================================================
    # PAGE 1: Audited Calculation & Bonus Breakdown
    # =========================================================================
    story.append(RLImage('uploads/phatak_official_shares_calculation_ss.png', width=525, height=742))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: Folio IN30034310432238 (Dr. Sanjeev Ratnakar Phatak - Gazette Page 29)
    # =========================================================================
    h2_table = [
        [
            Paragraph('<b>ASTRAL LIMITED • STATUTORY IEPF TRANSFER GAZETTE RECORD</b><br/>'
                      '<font color="#0284c7"><b>Folio ID: IN30034310432238 | Certified Transfer under Section 124(6) of Companies Act, 2013</b></font>', p_title),
            Paragraph('<b>STATUTORY AUDIT</b><br/>'
                      '<b>REGISTRAR:</b> Bigshare Services<br/>'
                      '<b>CUSTODIAN:</b> IEPF Authority, MCA', ParagraphStyle('R2', fontName='Helvetica', fontSize=6.8, leading=8.8, alignment=2, textColor=c_slate))
        ]
    ]
    t_h2 = Table(h2_table, colWidths=[380, 163])
    t_h2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_h2)
    story.append(Spacer(1, 4))
    
    b2_bar = [
        [
            Paragraph('<b>VERIFIED BENEFICIARY:</b> DR SANJEEV RATNAKAR PHATAK (SOLO HOLDING)<br/>'
                      '<b>REGISTERED ADDRESS:</b> 1, TEJDHARA BUNGLOWS PART-II 100FT. ROAD, B/H RAHUL TOWER SATELLITE, AHMEDABAD - 380015<br/>'
                      '<b>AUDITED STATUS:</b> <font color="#b91c1c"><b>TRANSFERRED TO IEPF (03-Sep-2026)</b></font> | <b>UNCLAIMED WARRANT:</b> Rs. 570.66 (9 Cumulative Tranches: Rs. 10,368.31)', p_note)
        ]
    ]
    t_b2 = Table(b2_bar, colWidths=[543])
    t_b2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86efac')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_b2)
    story.append(Spacer(1, 6))
    
    # img2 is 2312 x 1896 -> aspect 1.22 -> width=520, height=426
    story.append(RLImage('uploads/phatak_folio_IN30034310432238_p29_official_ss.png', width=520, height=415))
    story.append(Spacer(1, 6))
    
    note2 = [
        [
            Paragraph('<b>STATUTORY PRIVACY & VERIFICATION NOTICE:</b><br/>'
                      'In strict compliance with statutory data privacy standards, identifiable street addresses and folio numbers of unrelated third-party shareholders have been redacted. The highlighted entry in red confirms your certified registered shareholding and unclaimed dividend record in Astral Limited transferred into the Investor Education and Protection Fund (IEPF) Demat Account of the Government of India under Section 124(6). Total folio entitlement: 1,682 equity shares (~Rs. 23.97 Lakhs). This holding is 100% valid, intact, and fully reclaimable via MCA e-Form IEPF-5.', p_note)
        ]
    ]
    t_n2 = Table(note2, colWidths=[543])
    t_n2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_n2)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: Folio IN30034310432220 (Mrs. Sanu Sanjeev Phatak - Gazette Page 30)
    # =========================================================================
    h3_table = [
        [
            Paragraph('<b>ASTRAL LIMITED • STATUTORY IEPF TRANSFER GAZETTE RECORD</b><br/>'
                      '<font color="#0284c7"><b>Folio ID: IN30034310432220 | Certified Transfer under Section 124(6) of Companies Act, 2013</b></font>', p_title),
            Paragraph('<b>STATUTORY AUDIT</b><br/>'
                      '<b>REGISTRAR:</b> Bigshare Services<br/>'
                      '<b>CUSTODIAN:</b> IEPF Authority, MCA', ParagraphStyle('R3', fontName='Helvetica', fontSize=6.8, leading=8.8, alignment=2, textColor=c_slate))
        ]
    ]
    t_h3 = Table(h3_table, colWidths=[380, 163])
    t_h3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_h3)
    story.append(Spacer(1, 4))
    
    b3_bar = [
        [
            Paragraph('<b>VERIFIED BENEFICIARY:</b> SANU SANJEEV PHATAK (FAMILY / PRIMARY HOLDING)<br/>'
                      '<b>REGISTERED ADDRESS:</b> 1, TEJDHARA BUNGLOWS PART-II 100FT. ROAD, B/H RAHUL TOWER SATELLITE, AHMEDABAD - 380015<br/>'
                      '<b>AUDITED STATUS:</b> <font color="#b91c1c"><b>TRANSFERRED TO IEPF (03-Sep-2026)</b></font> | <b>UNCLAIMED WARRANT:</b> Rs. 856.00 (8 Cumulative Tranches: Rs. 57,755.20)', p_note)
        ]
    ]
    t_b3 = Table(b3_bar, colWidths=[543])
    t_b3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86efac')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_b3)
    story.append(Spacer(1, 6))
    
    # img3 is 2312 x 2146 -> aspect 1.08 -> width=520, height=435
    story.append(RLImage('uploads/phatak_folio_IN30034310432220_p30_official_ss.png', width=520, height=420))
    story.append(Spacer(1, 6))
    
    note3 = [
        [
            Paragraph('<b>STATUTORY PRIVACY & VERIFICATION NOTICE:</b><br/>'
                      'Non-beneficiary shareholder details have been blurred for data security compliance. The highlighted entry in red confirms the primary family shareholding and recurring dividend warrants registered under Folio IN30034310432220 in Astral Limited. Under Section 124(6), all cumulative corporate bonuses (2019, 2021, 2023) and cash warrants combine into your certified master family holding of 11,458 shares (~Rs. 1.63 Cr). Combined with Dr. Phatak\'s folio, the total claim is 13,140 equity shares (~Rs. 1.87 Cr), legally protected and fully recoverable through a consolidated MCA IEPF-5 petition.', p_note)
        ]
    ]
    t_n3 = Table(note3, colWidths=[543])
    t_n3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_n3)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 4: Statutory Proof Card & Recovery Mandate
    # =========================================================================
    h4_table = [
        [
            Paragraph('<b>IEPF AUTHORITY DEMAT TRANSFER CONFIRMATION & ENTITLEMENT AUDIT</b><br/>'
                      '<font color="#0284c7"><b>Official Central Government Recovery Protocol | Astral Limited (NSE: ASTRAL)</b></font>', p_title),
            Paragraph('<b>MANDATE AUDIT</b><br/>'
                      '<b>FEE:</b> 100% Contingent<br/>'
                      '<b>ADVANCE:</b> Rs. 0 Upfront', ParagraphStyle('R4', fontName='Helvetica', fontSize=6.8, leading=8.8, alignment=2, textColor=c_slate))
        ]
    ]
    t_h4 = Table(h4_table, colWidths=[380, 163])
    t_h4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_h4)
    story.append(Spacer(1, 4))
    
    # img4 is 1696 x 455 -> width=543 -> height = 145 pt
    story.append(RLImage('uploads/proof_cards/client_7_iepf_proof.png', width=543, height=145))
    story.append(Spacer(1, 6))
    
    # Master Reconciliation Table
    summary_data = [
        [
            Paragraph('<b>AUDITED PARAMETER</b>', ParagraphStyle('SH', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white)),
            Paragraph('<b>STATUTORY DETAILS & LEGAL CERTIFICATION</b>', ParagraphStyle('SH2', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white)),
            Paragraph('<b>STATUS</b>', ParagraphStyle('SH3', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1))
        ],
        [
            Paragraph('<b>Legal Beneficiaries</b>', p_note),
            Paragraph('Dr. Sanjeev Ratnakar Phatak & Mrs. Sanu Sanjeev Phatak<br/>'
                      '<font color="#64748b">1, Tejdhara Bunglows Part-II, 100ft. Road, Behind Rahul Tower, Satellite, Ahmedabad, Gujarat - 380015</font>', p_note),
            Paragraph('<b>VERIFIED</b>', ParagraphStyle('V1', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_green, alignment=1))
        ],
        [
            Paragraph('<b>Folios Included</b>', p_note),
            Paragraph('<b>Folio 1:</b> IN30034310432238 (Dr. Sanjeev Phatak - 1,682 Shares)<br/>'
                      '<b>Folio 2:</b> IN30034310432220 (Sanu Phatak - 11,458 Shares)', p_note),
            Paragraph('<b>AUDITED</b>', ParagraphStyle('V2', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_blue, alignment=1))
        ],
        [
            Paragraph('<b>Total Equity Holding</b>', p_note),
            Paragraph('<b>13,140 Shares</b> (5,913 Base + 1,479 [2019 Bonus] + 2,464 [2021 Bonus] + 3,284 [2023 Bonus])', p_note),
            Paragraph('<b>13,140 SHARES</b>', ParagraphStyle('V3', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_navy, alignment=1))
        ],
        [
            Paragraph('<b>Current Valuation</b>', p_note),
            Paragraph('<b>Rs. 1,87,24,500.00 (~Rs. 1.87 Crore)</b> (Based on NSE: ASTRAL CMP ~Rs. 1,425)', p_note),
            Paragraph('<b>~Rs. 1.87 CR</b>', ParagraphStyle('V4', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_green, alignment=1))
        ],
        [
            Paragraph('<b>Accumulated Dividends</b>', p_note),
            Paragraph('<b>Rs. 68,123.51</b> across 17 historical warrant cycles in Central Government Escrow (PFMS/DBT Direct Transfer)', p_note),
            Paragraph('<b>PFMS CREDIT</b>', ParagraphStyle('V5', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_blue, alignment=1))
        ],
        [
            Paragraph('<b>Statutory Custody</b>', p_note),
            Paragraph('IEPF Authority Demat Custodian Account, Ministry of Corporate Affairs (MCA), New Delhi', p_note),
            Paragraph('<b>IN ESCROW</b>', ParagraphStyle('V6', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_red, alignment=1))
        ],
        [
            Paragraph('<b>Advisory Mandate</b>', p_note),
            Paragraph('<b>100% Contingent Success-Fee Model:</b> Rs. 0 advance fees. Payable only after shares are credited in Demat.', p_note),
            Paragraph('<b>Rs. 0 ADVANCE</b>', ParagraphStyle('V7', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=c_green, alignment=1))
        ]
    ]
    t_sum = Table(summary_data, colWidths=[120, 333, 90])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 5))
    
    # Practice Contact Block
    contact_data = [
        [
            Paragraph(
                '<b>CORPORATE ASSET RECOVERY & IEPF ADVISORY PRACTICE</b><br/>'
                '<b>Lead Fiduciary Counsel:</b> MD ASRAR BASHA A<br/>'
                'Direct Phone / WhatsApp: <b>+91 7358882822</b> | Official Practice Email: <b>amdasrarbasha@gmail.com</b><br/>'
                'Physical Liaison: Mumbai (Bigshare Services Pvt Ltd) & New Delhi (IEPF Authority, MCA)',
                p_note
            )
        ]
    ]
    t_con = Table(contact_data, colWidths=[543])
    t_con.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_con)
    story.append(Spacer(1, 4))
    
    fiduciary_bar = [
        [
            Paragraph('<b>LEGAL FIDUCIARY COVENANT:</b> We never touch client equity shares or monetary disbursements. '
                      'The Government of India credits all shares directly into your certified personal Demat account. Zero financial liability prior to visible Demat credit.',
                      ParagraphStyle('FB', fontName='Helvetica', fontSize=6, leading=7.8, alignment=1, textColor=c_slate))
        ]
    ]
    t_fid = Table(fiduciary_bar, colWidths=[543])
    t_fid.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fid)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'Successfully created: {pdf_path}')
    
    # Copy to brain artifacts
    brain_dir = r'C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99'
    brain_pdf = os.path.join(brain_dir, os.path.basename(pdf_path))
    shutil.copyfile(pdf_path, brain_pdf)
    print(f'Copied to brain artifacts: {brain_pdf}')

if __name__ == '__main__':
    generate_pdf()

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
PDF_PATH = os.path.join(UPLOAD_DIR, "Corporate_IEPF_Team_Profile_and_Capability_Statement.pdf")
BRAIN_DIR = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"

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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, 808, "CORPORATE IEPF ASSET RESTITUTION PRACTICE | PRACTICE PROFILE & CAPABILITY STATEMENT")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(40, 802, 555, 802)

        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        
        self.drawString(40, 30, "CONFIDENTIAL & PROPRIETARY — PREPARED FOR SHAREHOLDER FIDUCIARY REVIEW")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(555, 30, page_str)
        self.restoreState()

def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0369a1'),
        spaceAfter=14
    )
    sec_heading = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0f172a')
    )
    role_title = ParagraphStyle(
        'RoleTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0284c7')
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        firstLineIndent=-12
    )

    story = []

    # ==================== PAGE 1 ====================
    # Header Banner Table
    header_data = [
        [
            Paragraph("<b>CORPORATE IEPF ASSET RESTITUTION PRACTICE</b><br/><font size=8.5 color='#64748b'>Fiduciary Shareholder Advisory & Investor Education and Protection Fund (IEPF) Representation</font>", title_style),
            Paragraph("<b>PRACTICE CREDENTIALS</b><br/><font size=7.5 color='#0369a1'>Section 124(6) & 125(3)<br/>Companies Act, 2013<br/>MCA / RTA Restitution</font>", ParagraphStyle('RHead', fontName='Helvetica', fontSize=8, leading=11, alignment=2, textColor=colors.HexColor('#0f172a')))
        ]
    ]
    t_hdr = Table(header_data, colWidths=[380, 135])
    t_hdr.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_hdr)
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=10))

    # Executive Summary Card
    summary_text = (
        "<b>Executive Overview:</b> Our specialized corporate practice operates exclusively at the intersection of "
        "<b>Corporate Law, SEBI Investor Protection Regulations, and MCA Statutory Governance</b>. We provide full-lifecycle "
        "fiduciary representation to High-Net-Worth Individuals (HNIs), chartered accountants, medical practitioners, family trusts, "
        "and corporate bodies whose long-term equity shares and accumulated dividend assets have matured past the 7-year "
        "unclaimed period and statutorily transitioned into the custody of the <b>Investor Education and Protection Fund (IEPF) "
        "Authority, Ministry of Corporate Affairs (Government of India)</b>. We maintain a 100% contingent, risk-free mandate."
    )
    t_sum = Table([[Paragraph(summary_text, body_style)]], colWidths=[515])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 10))

    # Core Leadership & Multi-Disciplinary Practice Team
    story.append(Paragraph("1. PRACTICE LEADERSHIP & MULTI-DISCIPLINARY STRUCTURE", sec_heading))

    team_data = [
        [
            Paragraph("<b>MD ASRAR BASHA A</b><br/><font color='#0284c7'><b>Practice Head & Lead Fiduciary Counsel</b></font>", role_title),
            Paragraph(
                "• Directs strategic statutory interventions, high-value corporate mandates, and client representation before the IEPF Authority.<br/>"
                "• Formulates legal restitution roadmaps across Section 124(6), Section 125(3), and Rule 7 of the IEPF Rules, 2016.<br/>"
                "• Direct liaison with Astral Limited Corporate Legal Desk, Bigshare Services Mumbai, and Nodal Officers at MCA New Delhi.<br/>"
                "• <i>Direct Line:</i> +91 7358882822 | <i>Email:</i> amdasrarbasha@gmail.com",
                body_style
            )
        ],
        [
            Paragraph("<b>Corporate Secretarial & MCA Governance Team</b><br/><font color='#475569'><b>FCS / ACS Domain Specialists</b></font>", role_title),
            Paragraph(
                "• Specializes in end-to-end statutory drafting, verification, and filing of digital <b>e-Form IEPF-5</b> on the MCA21 V3 Portal.<br/>"
                "• Resolves complex compliance hurdles including SEBI Circular ISR-1 (KYC), ISR-2 (Banker Attestation), and ISR-3/4.<br/>"
                "• Ensures zero-deficiency filings to bypass the 80%+ bureaucratic rejection bottleneck common in self-filed applications.",
                body_style
            )
        ],
        [
            Paragraph("<b>Forensic Equity & Bonus Reconciliation Desk</b><br/><font color='#475569'><b>Chartered Accountants & Equity Analysts</b></font>", role_title),
            Paragraph(
                "• Conducts mathematical equity reconstructions for bonus issues (e.g. Astral Limited 1:1, 1:2 historical bonus tranches).<br/>"
                "• Reconciles cumulative multi-year unpaid dividend warrants, fractional share entitlements, and TDS Form 16A credits.<br/>"
                "• Audits RTA register extracts against demat Client Master Lists (CML) to guarantee 100% exact restitution parity.",
                body_style
            )
        ],
        [
            Paragraph("<b>RTA & Nodal Authority Physical Liaison Unit</b><br/><font color='#475569'><b>Mumbai & New Delhi Operations Desk</b></font>", role_title),
            Paragraph(
                "• Physical representation and docket delivery at <b>Registrar Bigshare Services Pvt Ltd</b> (Andheri East, Mumbai).<br/>"
                "• Hand-carries original verification dockets to Astral Limited Secretarial Headquarters (Ahmedabad) for company verification.<br/>"
                "• Expedites Company Verification Reports (CVRs) and monitors Nodal Officer approvals through to final Demat credit.",
                body_style
            )
        ]
    ]

    t_team = Table(team_data, colWidths=[165, 350])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 10))

    # Core Practice Capabilities Box
    story.append(Paragraph("2. CORE PRACTICE CAPABILITIES & COMPLEX RESOLUTIONS", sec_heading))

    cap_data = [
        [
            Paragraph("<b>Dematerialization & Legacy Physical Folio Conversion:</b> Full conversion of physical share certificates into Demat format via SEBI Form ISR-4.", body_style),
            Paragraph("<b>Bank Signature Variation Rectification:</b> Official Form ISR-2 execution with Bank Manager seal, employee code, and CBS verification.", body_style)
        ],
        [
            Paragraph("<b>Transmission & Legal Heir Succession:</b> Execution of Succession Certificates, Probate of Will, Legal Heirship affidavits, and Family NOCs.", body_style),
            Paragraph("<b>Gazette Name & Address Reconciliations:</b> Rectification of spelling variations and address shifts via state gazette notifications and notarized affidavits.", body_style)
        ]
    ]
    t_cap = Table(cap_data, colWidths=[255, 260])
    t_cap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cap)

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    story.append(Paragraph("3. 100% RISK-FREE FIDUCIARY FRAMEWORK & CLIENT SAFEGUARDS", sec_heading))
    story.append(Paragraph("To ensure the utmost confidence and institutional protection for our clients, our practice functions under three strict ethical covenants:", body_style))
    story.append(Spacer(1, 6))

    covenants_data = [
        [
            Paragraph("<b>1. ZERO ADVANCE FEE<br/>(100% Contingent Model)</b>", role_title),
            Paragraph("We do <b>not charge a single rupee upfront</b>. Our professional remuneration is strictly contingent upon success, payable exclusively <b>AFTER</b> the shares and dividend warrants are visibly credited into your verified Demat and bank accounts. If there is no recovery, you owe nothing.", body_style)
        ],
        [
            Paragraph("<b>2. DIRECT GOVERNMENT SETTLEMENT<br/>(Non-Possessory Mandate)</b>", role_title),
            Paragraph("Our practice operates on a strictly non-possessory basis. The IEPF Authority and Central Government execute a <b>direct Corporate Action transfer</b> into your personal Demat account (CDSL/NSDL), and dividend funds are credited directly to your bank account via PFMS/DBT. <b>We never touch client assets or funds.</b>", body_style)
        ],
        [
            Paragraph("<b>3. INSTITUTIONAL DATA PRIVACY<br/>(Masked KYC Protocol)</b>", role_title),
            Paragraph("Under our strict data hygiene protocol, we only request <b>Masked Aadhaar</b> (with the first 8 digits blacked out) and cancelled cheques stamped <i>'FOR ASTRAL IEPF RESTITUTION KYC ONLY'</i>. We never request OTPs, Demat trading passwords, netbanking credentials, or power of attorney.", body_style)
        ]
    ]
    t_cov = Table(covenants_data, colWidths=[165, 350])
    t_cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 12))

    # Proven 5-Phase Restitution Lifecycle
    story.append(Paragraph("4. SYSTEMATIC 5-PHASE RESTITUTION LIFECYCLE", sec_heading))

    lifecycle_data = [
        ["Phase", "Milestone Action", "Statutory Stakeholder", "Estimated Timeline"],
        [
            "Phase 1",
            "Forensic Holding Verification & Gazette Audit\n• Reconstruct historical bonus shares & unpaid dividends\n• Cross-verify Bigshare RTA ledger and MCA Gazette records",
            "Astral Limited\nBigshare Services Pvt Ltd",
            "Days 1 – 3"
        ],
        [
            "Phase 2",
            "SEBI ISR Standardization & Dossier Compilation\n• Form ISR-1 (KYC), ISR-2 (Banker Attestation), ISR-3/4\n• Client Master List (CML) demat mapping & indemnity drafting",
            "Shareholder Bank\nLegal Counsel",
            "Days 4 – 10"
        ],
        [
            "Phase 3",
            "Digital e-Form IEPF-5 Filing on MCA21 V3 Portal\n• Generation of official SRN (Service Request Number)\n• Compilation of statutory physical verification docket",
            "Ministry of Corporate Affairs\n(MCA New Delhi)",
            "Days 11 – 15"
        ],
        [
            "Phase 4",
            "Company Verification Report (CVR) Issuance\n• Submission of physical verification docket to Astral Limited\n• Astral Nodal Officer audit and transmission of CVR to MCA",
            "Astral Limited Secretarial Desk\n(Ahmedabad)",
            "Days 16 – 40"
        ],
        [
            "Phase 5",
            "IEPF Authority Order & Direct Corporate Action Credit\n• IEPF Authority approval order passed\n• Direct credit of equity shares to Demat & dividends via PFMS",
            "IEPF Authority\n(Ministry of Corporate Affairs)",
            "Days 41 – 75"
        ]
    ]

    t_life = Table(lifecycle_data, colWidths=[55, 235, 140, 85])
    t_life.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#ffffff')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffffff')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,1), (-1,-1), 5),
    ]))
    story.append(t_life)
    story.append(Spacer(1, 14))

    # Practice Credentials & Contact Information
    story.append(Paragraph("5. DIRECT PRACTICE DESK & ENGAGEMENT CONTACT", sec_heading))

    contact_data = [
        [
            Paragraph(
                "<b>PRACTICE HEAD:</b><br/>"
                "<b>MD ASRAR BASHA A</b><br/>"
                "Senior Fiduciary Counsel & Restitution Lead<br/>"
                "Corporate IEPF Advisory Practice",
                body_style
            ),
            Paragraph(
                "<b>DIRECT ENGAGEMENT CONTACT:</b><br/>"
                "• <b>Direct Phone / WhatsApp:</b> +91 7358882822<br/>"
                "• <b>Official Email:</b> amdasrarbasha@gmail.com<br/>"
                "• <b>Digital Client Portal:</b> https://customer-vault.onrender.com",
                body_style
            )
        ]
    ]
    t_con = Table(contact_data, colWidths=[240, 275])
    t_con.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#0284c7')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_con)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")

    # Copy to brain artifacts directory
    brain_pdf = os.path.join(BRAIN_DIR, "Corporate_IEPF_Team_Profile_and_Capability_Statement.pdf")
    try:
        import shutil
        shutil.copyfile(PDF_PATH, brain_pdf)
        print(f"Copied to brain artifacts: {brain_pdf}")
    except Exception as e:
        print(f"Brain copy note: {e}")

if __name__ == "__main__":
    generate_pdf()

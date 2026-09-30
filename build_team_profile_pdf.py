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

class ProfessionalCanvas(canvas.Canvas):
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
        
        # Outer delicate border line
        self.setStrokeColor(colors.HexColor("#0f172a"))
        self.setLineWidth(1)
        self.rect(24, 20, 547, 802)
        
        # Inner fine accent border
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.rect(27, 23, 541, 796)

        # Top corner accents (Gold/Navy)
        self.setFillColor(colors.HexColor("#0f172a"))
        self.rect(24, 818, 40, 4, fill=1, stroke=0)
        self.rect(531, 818, 40, 4, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#b45309"))
        self.rect(64, 819, 20, 2, fill=1, stroke=0)
        self.rect(511, 819, 20, 2, fill=1, stroke=0)

        # Running Header (Page 2)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7)
            self.setFillColor(colors.HexColor("#0f172a"))
            self.drawString(36, 802, "CORPORATE IEPF ASSET RESTITUTION PRACTICE")
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(235, 802, "|  PRACTICE CREDENTIALS & CAPABILITY STATEMENT")
            self.drawRightString(558, 802, "DOC-REF: IEPF/EXEC-CAP/2026")
            
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(36, 796, 558, 796)

        # Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(36, 38, 558, 38)

        self.setFont("Helvetica-Bold", 6.8)
        self.setFillColor(colors.HexColor("#0f172a"))
        self.drawString(36, 28, "OFFICIAL PRACTICE PROFILE & INSTITUTIONAL CAPABILITY DOSSIER")
        
        self.setFont("Helvetica", 6.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(290, 28, "STRICTLY CONFIDENTIAL — ISSUED FOR FIDUCIARY REVIEW")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 28, page_str)

        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    # Custom Typography Palette
    c_primary = colors.HexColor("#0f172a")    # Midnight Slate / Executive Navy
    c_secondary = colors.HexColor("#0369a1")  # Deep Sapphire Blue
    c_gold = colors.HexColor("#b45309")       # Warm Fiduciary Gold / Bronze
    c_green = colors.HexColor("#15803d")      # Success Emerald
    c_dark = colors.HexColor("#1e293b")
    c_slate = colors.HexColor("#475569")
    c_light_bg = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#cbd5e1")

    # Paragraph Styles
    p_main_title = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
        spaceAfter=2
    )
    p_sub_title = ParagraphStyle(
        'SubTitle',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_secondary
    )
    p_sec_head = ParagraphStyle(
        'SecHead',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=3
    )
    p_body = ParagraphStyle(
        'BodyP',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark
    )
    p_body_bold = ParagraphStyle(
        'BodyPBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=c_primary
    )
    p_role_title = ParagraphStyle(
        'RoleT',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=c_secondary
    )
    p_badge = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: INSTITUTIONAL CREDENTIALS & MULTI-DISCIPLINARY PRACTICE STRUCTURE
    # =========================================================================

    # 1. Official Header Block
    seal_box = [
        Paragraph("<b>CORPORATE ASSET RESTITUTION & RECOVERY PRACTICE</b>", p_main_title),
        Paragraph("<b>Specialized Shareholder Advisory under Section 124(6) & 125(3) of the Companies Act, 2013</b><br/>"
                  "<font color='#64748b'>Investor Education and Protection Fund (IEPF) Representation | Ministry of Corporate Affairs, New Delhi</font>", p_sub_title)
    ]
    ref_box = [
        Paragraph("<font color='#0369a1'><b>INSTITUTIONAL DOSSIER</b></font><br/>"
                  "<b>REF:</b> IEPF/CAP-STMT/2026<br/>"
                  "<b>MANDATE:</b> 100% Contingent Basis", 
                  ParagraphStyle('RefStyle', fontName='Helvetica', fontSize=7.2, leading=10, alignment=2, textColor=c_slate))
    ]
    t_header = Table([[seal_box, ref_box]], colWidths=[385, 137])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=4, spaceBefore=2))

    # 2. Key Track Record Metric Cards (50+ Restitutions | 100% Success | Rs. 30+ Cr | Rs. 0 Advance)
    p_num_blue = ParagraphStyle('NumB', fontName='Helvetica-Bold', fontSize=13.5, leading=15, alignment=1, textColor=c_secondary)
    p_num_green = ParagraphStyle('NumG', fontName='Helvetica-Bold', fontSize=13.5, leading=15, alignment=1, textColor=c_green)
    p_num_dark = ParagraphStyle('NumD', fontName='Helvetica-Bold', fontSize=13.5, leading=15, alignment=1, textColor=c_primary)
    p_num_gold = ParagraphStyle('NumO', fontName='Helvetica-Bold', fontSize=13.5, leading=15, alignment=1, textColor=c_gold)
    p_stat_lbl = ParagraphStyle('LblS', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, alignment=1, textColor=c_dark)
    p_stat_sub = ParagraphStyle('SubS', fontName='Helvetica', fontSize=6.2, leading=7.8, alignment=1, textColor=c_slate)

    metrics_table_data = [
        [
            Paragraph("<b>50+</b>", p_num_blue),
            Paragraph("<b>100%</b>", p_num_green),
            Paragraph("<b>Rs. 30+ Cr</b>", p_num_dark),
            Paragraph("<b>Rs. 0 ADVANCE</b>", p_num_gold)
        ],
        [
            Paragraph("<b>RESTITUTIONS EXECUTED</b>", p_stat_lbl),
            Paragraph("<b>SUCCESS RATE (0 REJECTIONS)</b>", p_stat_lbl),
            Paragraph("<b>PORTFOLIO UNLOCKED</b>", p_stat_lbl),
            Paragraph("<b>100% CONTINGENT MANDATE</b>", p_stat_lbl)
        ],
        [
            Paragraph("HNIs, CAs & Medical Directors", p_stat_sub),
            Paragraph("Zero Deficiency Deadlock", p_stat_sub),
            Paragraph("Astral & Blue-Chip Equities", p_stat_sub),
            Paragraph("Payable Post Visible Demat Credit", p_stat_sub)
        ]
    ]
    t_metrics = Table(metrics_table_data, colWidths=[130, 131, 130, 131])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('LINEBEFORE', (1,0), (1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('LINEBEFORE', (2,0), (2,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('LINEBEFORE', (3,0), (3,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 4))

    # 3. Practice Overview & Institutional Mandate Card
    overview_html = (
        "<b>Institutional Practice Overview:</b> Operating exclusively at the nexus of <b>Corporate Law, SEBI Investor Protection "
        "Regulations, and Ministry of Corporate Affairs (MCA) Statutory Governance</b>, our practice serves as specialized fiduciary "
        "counsel for High-Net-Worth Individuals (HNIs), senior Chartered Accountants, medical directors, corporate houses, and family "
        "trusts pan-India. We specialize in navigating the intricate procedural, legal, and operational hurdles required to successfully "
        "release and restitute substantial equity holdings and dividend arrears transitioned into the custody of the <b>Investor Education "
        "and Protection Fund (IEPF) Authority</b>. With <b>over 50+ completed restitutions and a 100% first-pass clearance track record</b>, "
        "we provide an institutional, zero-risk, and end-to-end statutory execution."
    )
    t_overview = Table([[Paragraph(overview_html, p_body)]], colWidths=[522])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 4))

    # 4. Multi-Disciplinary Practice Team Hierarchy
    story.append(Paragraph("1. MULTI-DISCIPLINARY PRACTICE STRUCTURE & DOMAIN EXPERTS", p_sec_head))

    team_rows = [
        [
            Paragraph("<b>MD ASRAR BASHA A</b><br/><font color='#0369a1'><b>Practice Head & Lead Restitution Counsel</b></font><br/>"
                      "<font size=6.5 color='#64748b'>Senior Fiduciary Practice Lead<br/>Direct Nodal Liaison</font>", p_role_title),
            Paragraph(
                "• <b>Executive Mandate:</b> Personally spearheads high-value shareholder recovery interventions, complex family transmissions, and strategic representation before the Central Government IEPF Authority.<br/>"
                "• <b>Statutory Expertise:</b> Expert in Companies Act Section 124(6), Section 125(3), and Rule 7 of the IEPF Rules, 2016.<br/>"
                "• <b>Regulatory Interfacing:</b> Directly interfaces with Astral Limited Secretarial Department, Bigshare Services Mumbai, and Nodal Officers at the Ministry of Corporate Affairs (MCA, New Delhi).<br/>"
                "• <b>Direct Line:</b> +91 7358882822  |  <b>Official Email:</b> amdasrarbasha@gmail.com",
                p_body
            )
        ],
        [
            Paragraph("<b>Corporate Secretarial & MCA Governance Desk</b><br/><font color='#475569'><b>FCS / ACS Domain Specialists</b></font><br/>"
                      "<font size=6.5 color='#64748b'>ICSI Accredited Governance</font>", p_role_title),
            Paragraph(
                "• <b>MCA21 V3 Digital Execution:</b> Full-cycle drafting, verification, and digital submission of <b>e-Form IEPF-5</b>.<br/>"
                "• <b>SEBI Regulatory Alignment:</b> Resolves complex SEBI compliance mandates including Circular ISR-1 (KYC Update), ISR-2 (Banker Attestation), ISR-3 (Nomination Opt-out), and ISR-4 (Duplicate/Transmission).<br/>"
                "• <b>Zero-Deficiency Assurance:</b> Over 80% of self-filed claims across India receive MCA deficiency rejections. Our rigorous legal pre-audit ensures zero deficiency memos and immediate approval.",
                p_body
            )
        ],
        [
            Paragraph("<b>Forensic Equity & Bonus Reconciliation Desk</b><br/><font color='#475569'><b>Chartered Accountants & Auditors</b></font><br/>"
                      "<font size=6.5 color='#64748b'>ICAI Qualified Analysts</font>", p_role_title),
            Paragraph(
                "• <b>Mathematical Bonus Reconstructions:</b> Audits and mathematically calculates historical bonus splits (e.g. Astral Limited 1:1, 1:2 bonus tranches) to recover the exact multiplied holding, not just physical certificate units.<br/>"
                "• <b>Dividend Ledger Reconciliation:</b> Forensic extraction of 7+ years of cumulative unpaid dividend warrants and TDS Form 16A.<br/>"
                "• <b>Parity Audit:</b> Matches RTA ledger extracts with Client Master Lists (CML) to eliminate all folio mismatches.",
                p_body
            )
        ],
        [
            Paragraph("<b>RTA & Nodal Authority Physical Liaison Unit</b><br/><font color='#475569'><b>Mumbai & New Delhi Operations</b></font><br/>"
                      "<font size=6.5 color='#64748b'>On-Ground Physical Docket Delivery</font>", p_role_title),
            Paragraph(
                "• <b>Physical Docket Representation:</b> Stationed at <b>Registrar Bigshare Services Pvt Ltd</b> (Andheri East, Mumbai) for hand-delivery and immediate in-person tracking of verification dockets.<br/>"
                "• <b>Company Verification Report (CVR) Acceleration:</b> Directly coordinates with Astral Limited Secretarial Desk (Ahmedabad) to ensure the mandatory CVR is approved and uploaded to MCA within statutory timelines.<br/>"
                "• <b>Order Tracking:</b> Tracks Nodal Officer scrutiny through to the final Demat corporate action credit.",
                p_body
            )
        ]
    ]

    t_team = Table(team_rows, colWidths=[165, 357])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 4))

    # 5. Core Capabilities & Client Archetypes Box
    story.append(Paragraph("2. SPECIALIZED RECOVERY CAPABILITIES & PREFERRED CLIENTELE", p_sec_head))

    cap_table_data = [
        [
            Paragraph("<b>Dematerialization & Legacy Physical Conversion:</b> Conversion of physical share certificates into electronic Demat via SEBI Form ISR-4.", p_body),
            Paragraph("<b>Bank Signature Variation Rectification:</b> Formal SEBI Form ISR-2 execution with Bank Manager verification, employee code, and CBS attestation.", p_body)
        ],
        [
            Paragraph("<b>Transmission & Legal Heirship Succession:</b> Comprehensive legal processing of Succession Certificates, Probate of Will, Legal Heir Affidavits, and Family NOCs.", p_body),
            Paragraph("<b>Gazette Name & Address Reconciliations:</b> Remediation of name spelling discrepancies, maiden-to-married changes, and address shifts via state gazettes.", p_body)
        ],
        [
            Paragraph("<b>Clientele Archetypes Represented:</b> Senior Chartered Accountants, Medical Doctors & Surgeons, Industrial Founders, Senior NRIs, and Family Trusts.", ParagraphStyle('ClP', fontName='Helvetica-Bold', fontSize=7.2, leading=9.5, textColor=c_primary)),
            Paragraph("<b>Regulatory Jurisdictions:</b> Companies Act 2013, IEPF Rules 2016, SEBI (LODR) Regulations 2015, and NSDL/CDSL Depository Guidelines.", ParagraphStyle('JurP', fontName='Helvetica-Bold', fontSize=7.2, leading=9.5, textColor=c_secondary))
        ]
    ]
    t_cap = Table(cap_table_data, colWidths=[259, 263])
    t_cap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-2), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93c5fd')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cap)

    # =========================================================================
    # PAGE 2: FIDUCIARY SAFEGUARDS, 5-PHASE LIFECYCLE & ENGAGEMENT CONTACT
    # =========================================================================
    story.append(PageBreak())

    # 1. Three Institutional Fiduciary Covenants
    story.append(Paragraph("3. INSTITUTIONAL FIDUCIARY COVENANTS & ZERO-RISK GUARANTEES", p_sec_head))
    story.append(Paragraph("To ensure complete transparency and institutional protection, our practice operates strictly under three enforceable fiduciary safeguards:", p_body))
    story.append(Spacer(1, 4))

    covenants_data = [
        [
            Paragraph("<b>1. ZERO ADVANCE FEE<br/>(100% Contingent Model)</b>", p_role_title),
            Paragraph(
                "We do <b>not charge a single rupee upfront</b>. Our professional remuneration is strictly contingent upon successful completion, "
                "payable exclusively <b>AFTER</b> the shares and cumulative dividend warrants are visibly credited into your verified personal Demat "
                "and bank accounts. If there is no recovery, you owe nothing. <b>Zero financial liability for the shareholder.</b>",
                p_body
            )
        ],
        [
            Paragraph("<b>2. DIRECT GOVERNMENT SETTLEMENT<br/>(Non-Possessory Protocol)</b>", p_role_title),
            Paragraph(
                "Our practice operates on an institutional non-possessory mandate. The IEPF Authority and Central Government execute a <b>direct Corporate "
                "Action transfer into your designated Demat account (CDSL/NSDL)</b>, and all dividend funds are credited directly to your registered bank "
                "account via PFMS/DBT. <b>We never handle, receive, or hold client shares or financial funds.</b>",
                p_body
            )
        ],
        [
            Paragraph("<b>3. INSTITUTIONAL DATA PRIVACY<br/>(Masked KYC Standard)</b>", p_role_title),
            Paragraph(
                "Under our strict compliance protocol, we only request <b>Masked Aadhaar</b> (with the first 8 digits blacked out) and cancelled cheques "
                "stamped <i>'FOR ASTRAL IEPF RESTITUTION KYC ONLY'</i>. We <b>never</b> request OTPs, Demat trading passwords, netbanking credentials, "
                "or general Power of Attorney. Your personal tax and banking records are completely protected.",
                p_body
            )
        ]
    ]
    t_cov = Table(covenants_data, colWidths=[165, 357])
    t_cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 8))

    # 2. Systematic 5-Phase Restitution Lifecycle Table
    story.append(Paragraph("4. SYSTEMATIC 5-PHASE STATUTORY RESTITUTION ROADMAP", p_sec_head))

    p_life_hdr = ParagraphStyle('LifeHdr', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)
    p_life_cell = ParagraphStyle('LifeCell', fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=c_dark)
    p_life_phase = ParagraphStyle('LifePhase', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=c_secondary, alignment=1)
    p_life_time = ParagraphStyle('LifeTime', fontName='Helvetica-Bold', fontSize=7.2, leading=9.2, textColor=c_gold, alignment=1)

    lifecycle_data = [
        [
            Paragraph("Phase", p_life_hdr),
            Paragraph("Milestone Action & Deliverables", p_life_hdr),
            Paragraph("Statutory Stakeholder", p_life_hdr),
            Paragraph("Estimated Timeline", p_life_hdr)
        ],
        [
            Paragraph("<b>Phase 1</b>", p_life_phase),
            Paragraph("<b>Forensic Holding Verification & Gazette Audit</b><br/>"
                      "• Mathematical bonus equity reconstruction & unpaid dividend calculation<br/>"
                      "• RTA ledger extract cross-verification against MCA gazette transfer records", p_life_cell),
            Paragraph("Astral Limited Secretarial Desk<br/>Bigshare Services Pvt Ltd (Mumbai)", p_life_cell),
            Paragraph("<b>Days 1 – 3</b>", p_life_time)
        ],
        [
            Paragraph("<b>Phase 2</b>", p_life_phase),
            Paragraph("<b>SEBI ISR Standardization & Dossier Compilation</b><br/>"
                      "• SEBI Form ISR-1 (KYC), Form ISR-2 (Bank Attestation), Form ISR-3/4<br/>"
                      "• Client Master List (CML) mapping, client affidavits & indemnity drafting", p_life_cell),
            Paragraph("Shareholder's Bank Manager<br/>Corporate Legal Counsel Desk", p_life_cell),
            Paragraph("<b>Days 4 – 10</b>", p_life_time)
        ],
        [
            Paragraph("<b>Phase 3</b>", p_life_phase),
            Paragraph("<b>Digital e-Form IEPF-5 Filing on MCA21 V3 Portal</b><br/>"
                      "• Generation of official MCA Service Request Number (SRN)<br/>"
                      "• Formal physical verification docket binding and statutory indexing", p_life_cell),
            Paragraph("Ministry of Corporate Affairs<br/>(MCA, New Delhi)", p_life_cell),
            Paragraph("<b>Days 11 – 15</b>", p_life_time)
        ],
        [
            Paragraph("<b>Phase 4</b>", p_life_phase),
            Paragraph("<b>Company Verification Report (CVR) Issuance</b><br/>"
                      "• In-person delivery of verification docket to Astral Limited Corporate Desk<br/>"
                      "• Nodal Officer audit, board secretarial approval & CVR transmission to MCA", p_life_cell),
            Paragraph("Astral Limited Corporate HQ<br/>(Ahmedabad Secretarial Desk)", p_life_cell),
            Paragraph("<b>Days 16 – 40</b>", p_life_time)
        ],
        [
            Paragraph("<b>Phase 5</b>", p_life_phase),
            Paragraph("<b>IEPF Authority Approval Order & Corporate Action Credit</b><br/>"
                      "• Official IEPF Authority Sanction Order passed under Section 125(3)<br/>"
                      "• <b>Direct electronic credit of equity shares to Demat & cash via PFMS/DBT</b>", p_life_cell),
            Paragraph("IEPF Authority Demat Custodian<br/>(Central Government MCA)", p_life_cell),
            Paragraph("<b>Days 41 – 75</b>", p_life_time)
        ]
    ]

    t_life = Table(lifecycle_data, colWidths=[52, 238, 142, 90])
    t_life.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('TOPPADDING', (0,0), (-1,0), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,1), (-1,-1), 3.5),
    ]))
    story.append(t_life)
    story.append(Spacer(1, 8))

    # 3. Formal Practice Authorization & Contact Desk
    story.append(Paragraph("5. DIRECT PRACTICE DESK & ENGAGEMENT CONTACT", p_sec_head))

    contact_data = [
        [
            Paragraph(
                "<b>PRACTICE HEAD & MANAGING COUNSEL:</b><br/>"
                "<font size=10 color='#0f172a'><b>MD ASRAR BASHA A</b></font><br/>"
                "Senior Fiduciary Counsel & Lead Restitution Advocate<br/>"
                "Corporate Asset Recovery & IEPF Compliance Practice<br/>"
                "<font size=6.8 color='#64748b'>Ranipet District & Chennai, Tamil Nadu — Operating Pan-India</font>",
                p_body
            ),
            Paragraph(
                "<b>DIRECT ENGAGEMENT CONTACT DESK:</b><br/>"
                "• <b>Direct Phone / WhatsApp:</b> +91 7358882822<br/>"
                "• <b>Official Practice Email:</b> amdasrarbasha@gmail.com<br/>"
                "• <b>Physical Liaison Desks:</b> Mumbai (Bigshare RTA) & New Delhi (MCA)<br/>"
                "• <b>Professional Fee Structure:</b> Contingent Success Fee | Rs. 0 Advance<br/>"
                "• <b>Document Clearance:</b> First-Pass MCA Clearance Assurance",
                p_body
            )
        ]
    ]
    t_con = Table(contact_data, colWidths=[240, 282])
    t_con.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#0284c7')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_con)
    story.append(Spacer(1, 4))

    # Bottom Fiduciary Guarantee Stamp Bar
    fiduciary_bar_data = [
        [
            Paragraph("<b>FIDUCIARY GUARANTEE:</b> Our advisory is legally bound under an enforceable bilateral mandate. "
                      "We never request nor accept upfront fees. All shares and accrued cash dividends are deposited directly by the "
                      "Government of India into your registered accounts. Total institutional compliance and client data confidentiality guaranteed.",
                      ParagraphStyle('FidBar', fontName='Helvetica', fontSize=6.8, leading=8.8, alignment=1, textColor=c_slate))
        ]
    ]
    t_fid = Table(fiduciary_bar_data, colWidths=[522])
    t_fid.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fid)

    doc.build(story, canvasmaker=ProfessionalCanvas)
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
    build_pdf()

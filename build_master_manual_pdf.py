import os
import shutil
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf
import pymupdf

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MasterManualCanvas(canvas.Canvas):
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
            self.saveState()
            
            # Outer decorative border
            self.setStrokeColor(colors.HexColor('#0F2942'))
            self.setLineWidth(0.75)
            self.rect(20, 20, 555.28, 801.89)
            
            # Header on pages > 1
            if self._pageNumber > 1:
                self.setFont('Helvetica-Bold', 7)
                self.setFillColor(colors.HexColor('#64748B'))
                self.drawString(28, 808, 'INTERNAL PRACTICE MANUAL & FIDUCIARY OPERATING PROCEDURE')
                self.setFont('Helvetica', 7)
                self.drawRightString(565, 808, 'CONFIDENTIAL - FOR MD ASRAR BASHA A ONLY')
                self.setStrokeColor(colors.HexColor('#CBD5E1'))
                self.setLineWidth(0.5)
                self.line(28, 803, 565, 803)

            # Footer on all pages
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(28, 36, 565, 36)
            
            self.setFont('Helvetica-Bold', 7)
            self.setFillColor(colors.HexColor('#0F2942'))
            self.drawString(28, 26, 'CORPORATE ASSET RECOVERY & IEPF ADVISORY DESK')
            self.setFont('Helvetica', 7)
            self.drawString(245, 26, '|  PRACTITIONER EXECUTION GUIDE (TEKWANI CASE)')
            
            page_str = f'Page {self._pageNumber} of {num_pages}'
            self.drawRightString(565, 26, page_str)
            self.restoreState()
            super().showPage()
        super().save()

def build_pdf():
    vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
    upload_dir = os.path.join(vault_dir, "uploads")
    artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
    blueprints_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\blueprints"
    
    filename = "IEPF_Master_Execution_Guide_Tekwani_Recovery.pdf"
    target_path = os.path.join(upload_dir, filename)

    doc = SimpleDocTemplate(
        target_path,
        pagesize=A4,
        leftMargin=26,
        rightMargin=26,
        topMargin=26,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_navy = colors.HexColor('#0F2942')
    c_teal = colors.HexColor('#0D9488')
    c_dark = colors.HexColor('#1E293B')
    c_slate = colors.HexColor('#64748B')
    c_bg = colors.HexColor('#F8FAFC')
    c_green = colors.HexColor('#15803D')
    c_amber = colors.HexColor('#B45309')
    c_border = colors.HexColor('#CBD5E1')

    # Typography styles
    title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=12, leading=15, alignment=1, textColor=c_navy)
    sub_title = ParagraphStyle('DocSub', fontName='Helvetica-Bold', fontSize=8, leading=10.5, alignment=1, textColor=c_teal)
    h1_style = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_navy, spaceBefore=4, spaceAfter=2)
    h2_style = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=c_teal, spaceBefore=3, spaceAfter=1.5)
    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=6.8, leading=9, textColor=c_dark)
    body_bold = ParagraphStyle('BodyBold', parent=body, fontName='Helvetica-Bold')
    callout = ParagraphStyle('Callout', parent=body, fontName='Helvetica-Bold', alignment=1)
    badge = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=colors.white, alignment=1)

    story = []

    # =========================================================================
    # PAGE 1: TITLE, CASE FILE & LEGAL ENFORCEABILITY (SHCIL E-STAMP & CONTRACT ACT)
    # =========================================================================
    story.append(Paragraph('CORPORATE ASSET RECOVERY &amp; IEPF STATUTORY RESTITUTION', title_style))
    story.append(Paragraph('INTERNAL MASTER OPERATING MANUAL &bull; PRACTITIONER STEP-BY-STEP PLAYBOOK WITH DIRECT PORTAL LINKS', sub_title))
    story.append(Paragraph('CASE FILE: CA Prakash Udhawdas Tekwani &amp; Udhawdas Isardas Tekwani (Astral Limited &bull; 13,895 Shares &bull; ~Rs. 1.98 Cr)', ParagraphStyle('Sub2', parent=sub_title, fontSize=7.2, leading=9.2, textColor=c_amber)))
    story.append(HRFlowable(width='100%', thickness=1.5, color=c_navy, spaceBefore=3, spaceAfter=4))

    meta_data = [
        [
            Paragraph('<b>LEAD COUNSEL / CONSULTANT:</b> MD ASRAR BASHA A (PAN: GEZPA2961D)', body),
            Paragraph('<b>PRACTICE DESK:</b> +91 7358882822 | amdasrarbasha@gmail.com', body)
        ],
        [
            Paragraph('<b>TARGET BENEFICIARIES:</b> CA Prakash U. Tekwani &amp; Shri Udhawdas I. Tekwani', body),
            Paragraph('<b>REGISTRAR (RTA):</b> Bigshare Services Pvt. Ltd. (Andheri East, Mumbai)', body)
        ],
        [
            Paragraph('<b>FOLIO NUMBERS:</b> IN30127630282977 &bull; IN30127630282985', body_bold),
            Paragraph('<b>ASSETS IN CUSTODY:</b> 13,895 Equity Shares + Rs. 5,525.50 Accrued Dividends', body_bold)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[271, 271])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    # SECTION 1: HOW DO WE MAKE THE AGREEMENT LEGAL AND STRONG?
    story.append(Paragraph('1. HOW DO WE MAKE THE AGREEMENT 100% LEGALLY BINDING &amp; UNBREAKABLE?', h1_style))
    story.append(Paragraph('Since we are operating remotely between Tamil Nadu and Gujarat, we execute an institutional-grade contract that guarantees zero payment disputes upon Demat share credit:', body))

    legal_steps = [
        [
            Paragraph('<b>PILLAR</b>', ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>EXACT EXECUTION METHOD &amp; STATUTORY COMPLIANCE</b>', ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>LEGAL CITATION &amp; DIRECT LINK</b>', ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white))
        ],
        [
            Paragraph('<b>1. Non-Judicial e-Stamp Paper</b>', body_bold),
            Paragraph('We procure an official <b>Rs. 100 / Rs. 300 Non-Judicial e-Stamp Certificate</b> via Stock Holding Corporation of India Ltd (<a href="https://www.shcilestamp.com" color="#0284C7"><u>SHCIL Portal</u></a>) or Gujarat e-Stamping portal under Article 5(h) of the Gujarat Stamp Act. Description: <i>"Service Agreement / Success Mandate between CA Prakash Tekwani and MD Asrar Basha A"</i>.', body),
            Paragraph('<a href="https://www.shcilestamp.com" color="#0284C7"><u>SHCIL Official Portal</u></a><br/><font color="#64748B">Sec 17 Indian Stamp Act</font>', callout)
        ],
        [
            Paragraph('<b>2. First Sheet Attachment</b>', body_bold),
            Paragraph('The SHCIL e-Stamp certificate forms <b>Page 0 (Outer Cover)</b>, securely stapled to the 2-page agreement. Both parties affix cross-signatures spanning across the physical stamp certificate and agreement header.', body),
            Paragraph('Physical Stamping<br/><font color="#64748B">Gujarat State Territory</font>', callout)
        ],
        [
            Paragraph('<b>3. Physical Wet-Ink Signatures</b>', body_bold),
            Paragraph('Both parties sign in <b>Blue Ballpoint Ink</b> on both Page 1 (initial at bottom right) and Page 2 (full signatures with office seal). The client signs on behalf of himself and his joint holder (father).', body),
            Paragraph('Indian Contract Act, 1872<br/><font color="#64748B">Section 10 (Valid Contract)</font>', callout)
        ],
        [
            Paragraph('<b>4. Two Neutral Witnesses</b>', body_bold),
            Paragraph('Two neutral adult witnesses sign on Page 2 with their Full Name, Father\'s Name, PAN/Aadhaar number, and complete address. This legally defeats any future claim of <i>"I never signed this"</i>.', body),
            Paragraph('Evidence Act, 1872<br/><font color="#64748B">Section 68 (Proof of Execution)</font>', callout)
        ],
        [
            Paragraph('<b>5. Optional Digital e-Sign</b>', body_bold),
            Paragraph('If executed digitally prior to courier, both parties sign via Aadhaar e-Sign through an approved Certifying Authority (<a href="https://cca.gov.in" color="#0284C7"><u>CCA India</u></a> compliant platforms like Leegality / DigiLocker). Possesses identical legal standing to physical notarization.', body),
            Paragraph('<a href="https://cca.gov.in" color="#0284C7"><u>IT Act, 2000 (Sec 4 &amp; 5)</u></a><br/><font color="#64748B">Digital Evidence Admissibility</font>', callout)
        ],
        [
            Paragraph('<b>6. Notary Attestation (Ahmedabad)</b>', body_bold),
            Paragraph('The client has the physical executed agreement notarized by a local Notary Public in Ahmedabad with the Notary\'s embossed seal, registration number, and entry into the Notarial Register book.', body),
            Paragraph('Notaries Act, 1952<br/><font color="#64748B">Presumption of Authenticity</font>', callout)
        ]
    ]
    t_legal = Table(legal_steps, colWidths=[108, 334, 100])
    t_legal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_legal)
    story.append(Spacer(1, 4))

    why_box = (
        '<b>WHY IS THIS AGREEMENT 100% UNBEATABLE IN COURT?</b><br/>'
        '&bull; <b>Liquidated Admitted Debt:</b> Clause 4 legally defines our 8% fee as an ascertained, liquidated debt under the Indian Contract Act, 1872.<br/>'
        '&bull; <b>Summary Civil Recovery (Order XXXVII CPC):</b> In the impossible event of client non-remittance after Demat credit, we can file a direct Summary Suit under Order 37 of Code of Civil Procedure (CPC), 1908, where the court grants automatic decree without lengthy trial.<br/>'
        '&bull; <b>Contractual First Lien:</b> The agreement establishes an irrevocable legal charge over the recovered proceeds until professional fees are discharged.'
    )
    t_why = Table([[Paragraph(why_box, body)]], colWidths=[542])
    t_why.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 0.75, c_amber),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_why)

    # PAGE BREAK TO KEEP SECTION 2 & 3 ON PAGE 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: WHAT DOCUMENTS DO WE NEED & WHAT THINGS SHOULD THE CLIENT DO?
    # =========================================================================
    story.append(Paragraph('2. WHAT ARE THE EXACT DOCUMENTS WE NEED FROM THE CLIENT?', h1_style))
    story.append(Paragraph('To prepare an error-free statutory restitution docket that clears Bigshare Services and MCA in the first review, collect the following simple checklist from CA Prakash Tekwani:', body))

    doc_steps = [
        [
            Paragraph('<b>#</b>', ParagraphStyle('DH0', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1)),
            Paragraph('<b>DOCUMENT NAME</b>', ParagraphStyle('DH1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>SPECIFIC REQUIREMENT &amp; WHY IT IS NEEDED</b>', ParagraphStyle('DH2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>SOURCE / LINK</b>', ParagraphStyle('DH3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1))
        ],
        [
            Paragraph('<b>1</b>', callout),
            Paragraph('<b>Signed Mandate Agreement</b>', body_bold),
            Paragraph('Executed 2-page agreement with both pages signed. Establishes legal authority and guarantees our 8% contingent fee.', body),
            Paragraph('Physical / Courier', callout)
        ],
        [
            Paragraph('<b>2</b>', callout),
            Paragraph('<b>Client Master List (CML)</b>', body_bold),
            Paragraph('CML of active Demat account where the 13,895 shares will be credited. Must bear official round stamp &amp; signature of DP broker (e.g. Zerodha, HDFC Sec).', body),
            Paragraph('<a href="https://www.cdslindia.com" color="#0284C7"><u>NSDL / CDSL</u></a>', callout)
        ],
        [
            Paragraph('<b>3</b>', callout),
            Paragraph('<b>Self-Attested PAN Copies</b>', body_bold),
            Paragraph('Both holders (CA Prakash Tekwani &amp; Shri Udhawdas Tekwani). Must be self-attested with signature matching current Demat/Bank records.', body),
            Paragraph('Self-Attested Copy', callout)
        ],
        [
            Paragraph('<b>4</b>', callout),
            Paragraph('<b>Masked Aadhaar Copies</b>', body_bold),
            Paragraph('Address proof for both holders (first 8 digits hidden for privacy per UIDAI regulations). Signed across the document.', body),
            Paragraph('<a href="https://myaadhaar.uidai.gov.in" color="#0284C7"><u>myaadhaar.uidai</u></a>', callout)
        ],
        [
            Paragraph('<b>5</b>', callout),
            Paragraph('<b>Original Cancelled Cheque</b>', body_bold),
            Paragraph('Of the bank account linked with MCA for dividend escrow credit. Must have client\'s name, account number, and IFSC pre-printed.', body),
            Paragraph('Original Cheque', callout)
        ],
        [
            Paragraph('<b>6</b>', callout),
            Paragraph('<b>SEBI Form ISR-2 (Bank Attestation)</b>', body_bold),
            Paragraph('Standard SEBI banker confirmation of signature. We draft and fill this form completely; client only takes it to his branch manager for a round stamp and signature.', body),
            Paragraph('<a href="https://customer-vault.onrender.com/api/documents/Official_SEBI_Form_ISR_2_Tekwani_Filled.pdf" color="#15803D"><u><b>Download ISR-2</b></u></a>', callout)
        ]
    ]
    t_docs = Table(doc_steps, colWidths=[20, 130, 312, 80])
    t_docs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_docs)
    story.append(Spacer(1, 4))

    # SECTION 3: WHAT SHOULD THE CLIENT DO?
    story.append(Paragraph('3. WHAT THINGS SHOULD THE CLIENT DO? (THE CLIENT\'S EXACT ROLE)', h1_style))
    story.append(Paragraph('One of our biggest selling points is <b>Zero Client Hassle</b>. We do 95% of the heavy legal lifting. The client only performs 4 straightforward tasks:', body))

    client_actions = [
        [
            Paragraph('<b>CLIENT ACTION</b>', ParagraphStyle('CH1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>WHAT THE CLIENT NEEDS TO DO (ESTIMATED TIME: ~15 MINUTES TOTAL)</b>', ParagraphStyle('CH2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>EFFORT LEVEL</b>', ParagraphStyle('CH3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1))
        ],
        [
            Paragraph('<b>Action 1: Sign Agreement</b>', body_bold),
            Paragraph('Print the 2-page agreement we sent, sign on Page 2, initial on Page 1, have 2 office staff/colleagues sign as witnesses, and courier it back to our office address.', body),
            Paragraph('<font color="#0284C7"><b>5 Minutes</b></font>', callout)
        ],
        [
            Paragraph('<b>Action 2: Download CML &amp; KYC</b>', body_bold),
            Paragraph('Download the digitally signed CML from his broker app/portal (or collect stamped physical CML from local broker branch). Sign self-attested photocopies of PAN, Masked Aadhaar, and 1 cancelled cheque.', body),
            Paragraph('<font color="#0284C7"><b>5 Minutes</b></font>', callout)
        ],
        [
            Paragraph('<b>Action 3: 5-Minute Bank Visit (Form ISR-2)</b>', body_bold),
            Paragraph('Hand the pre-filled SEBI Form ISR-2 (which we generate and email to him) to his bank branch manager where he maintains his savings/current account. The manager stamps and signs it certifying his signature.', body),
            Paragraph('<font color="#15803D"><b>5-10 Minutes</b></font>', callout)
        ],
        [
            Paragraph('<b>Action 4: Sign Final IEPF Docket</b>', body_bold),
            Paragraph('Once we prepare the MCA e-Form IEPF-5 acknowledgment and Non-Judicial Indemnity Bond docket, he signs the client signature blocks and hands them to our courier desk.', body),
            Paragraph('<font color="#0284C7"><b>5 Minutes</b></font>', callout)
        ],
        [
            Paragraph('<b>What Client NEVER Does</b>', ParagraphStyle('Never', parent=body_bold, textColor=colors.HexColor('#DC2626'))),
            Paragraph('Client <b>DOES NOT</b>: coordinate with Bigshare Services in Mumbai, chase Astral\'s Nodal Officer, follow up with MCA New Delhi, attend any government hearings, or pay any upfront portal fees. We handle 100% of bureaucracy.', body),
            Paragraph('<font color="#15803D"><b>ZERO HASSLE</b></font>', callout)
        ]
    ]
    t_cl = Table(client_actions, colWidths=[130, 332, 80])
    t_cl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_cl)

    # PAGE BREAK TO DEDICATE PAGE 3 ENTIRELY TO THE TIMELINE & DURATION BREAKDOWN
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: STATUTORY RECOVERY TIMELINE & DURATION BREAKDOWN MATRIX (DAYS, WEEKS, MONTHS)
    # =========================================================================
    story.append(Paragraph('4. MASTER STATUTORY RECOVERY TIMELINE &amp; DURATION BREAKDOWN', title_style))
    story.append(Paragraph('EXACT STAGE-BY-STAGE TIME ESTIMATE IN DAYS, WEEKS &amp; MONTHS UNDER COMPANIES ACT SEC 124(6) &amp; IEPF RULES, 2016', sub_title))
    story.append(HRFlowable(width='100%', thickness=1, color=c_navy, spaceBefore=2, spaceAfter=4))

    story.append(Paragraph('This comprehensive schedule details the exact chronological journey, government statutory deadlines, and realistic operating durations required to recover the 13,895 shares back into CA Prakash Tekwani\'s active Demat account:', body))

    # STAGE BY STAGE DETAILED DURATION TABLE
    timeline_data = [
        [
            Paragraph('<b>STAGE &amp; OPERATING PHASE</b>', ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>STATUTORY AUTHORITY &amp; TASK DETAILS</b>', ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>WORKING DAYS</b>', ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1)),
            Paragraph('<b>DURATION (WEEKS / MONTHS)</b>', ParagraphStyle('TH4', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1)),
            Paragraph('<b>CUMULATIVE ELAPSED</b>', ParagraphStyle('TH5', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1))
        ],
        [
            Paragraph('<b>Stage 1: Client Onboarding &amp; Signature Attestation</b>', body_bold),
            Paragraph('Execute 2-page agreement; collect active Demat CML; verify PAN &amp; Masked Aadhaar; Bank Manager certifies signature on SEBI Form ISR-2 with official seal.', body),
            Paragraph('<b>Days 1 &ndash; 7</b>', callout),
            Paragraph('<b>~1 Week<br/>(0.25 Mo)</b>', callout),
            Paragraph('<font color="#0284C7"><b>Week 1<br/>(0.25 Month)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 2: Digital MCA IEPF-5 Filing &amp; SRN Generation</b>', body_bold),
            Paragraph('Upload electronic claim on <a href="https://www.mca.gov.in" color="#0284C7"><u>MCA V3 Portal</u></a> under practitioner login; file digital schedules; generate official Central Govt <b>Service Request Number (SRN)</b>.', body),
            Paragraph('<b>Days 8 &ndash; 14</b>', callout),
            Paragraph('<b>~1 Week<br/>(0.25 Mo)</b>', callout),
            Paragraph('<font color="#0284C7"><b>Week 2<br/>(0.50 Month)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 3: Physical Docket Dispatch to Mumbai RTA</b>', body_bold),
            Paragraph('Bind SRN Challan, original stamped Indemnity Bond, Advance Receipt, and verified KYC; dispatch to <b>Bigshare Services (Mumbai)</b>; secure Inward Entry.', body),
            Paragraph('<b>Days 15 &ndash; 25</b>', callout),
            Paragraph('<b>~1.5 Weeks<br/>(0.35 Mo)</b>', callout),
            Paragraph('<font color="#0284C7"><b>Week 3 &ndash; 4<br/>(~1 Month)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 4: Bigshare Audit &amp; Astral CVR Upload</b>', body_bold),
            Paragraph('Bigshare audits master folios; liaison with Astral Limited Nodal Officer; Nodal Officer issues affirmative <b>Company Verification Report (CVR)</b> to IEPF Authority.<br/><font color="#64748B"><i>(Statutory Deadline under Rule 7: 30 days from inward)</i></font>', body),
            Paragraph('<b>Days 26 &ndash; 65</b>', callout),
            Paragraph('<b>~4 &ndash; 6 Weeks<br/>(1.2 &ndash; 1.5 Mo)</b>', callout),
            Paragraph('<font color="#15803D"><b>Month 2 &ndash; 2.5<br/>(Weeks 5 &ndash; 10)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 5: Central Government / IEPF Ministry Sanction</b>', body_bold),
            Paragraph('IEPF Authority scrutiny officers at MCA New Delhi examine CVR &amp; legal title; Competent Authority approves restitution and issues official <b>Government Sanction Order</b>.<br/><font color="#64748B"><i>(Statutory Target under Rule 7: 60 days from CVR)</i></font>', body),
            Paragraph('<b>Days 66 &ndash; 125</b>', callout),
            Paragraph('<b>~8 &ndash; 10 Weeks<br/>(2.0 &ndash; 2.5 Mo)</b>', callout),
            Paragraph('<font color="#B45309"><b>Month 3.5 &ndash; 4.5<br/>(Weeks 10 &ndash; 18)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 6: Depository Action &amp; Demat Credit of Shares</b>', body_bold),
            Paragraph('IEPF Authority triggers electronic Depository instruction; <b>all 13,895 shares credited directly into Demat</b> via CDSL/NSDL; cash dividends wired via PFMS/DBT.', body),
            Paragraph('<b>Days 126 &ndash; 145</b>', callout),
            Paragraph('<b>~2 &ndash; 3 Weeks<br/>(0.5 &ndash; 0.7 Mo)</b>', callout),
            Paragraph('<font color="#15803D"><b>Month 4.5 &ndash; 5.5<br/>(RECOVERY COMPLETE)</b></font>', callout)
        ],
        [
            Paragraph('<b>Stage 7: NSE Valuation &amp; 8% Fee Remittance</b>', body_bold),
            Paragraph('Valuation benchmarked at official NSE closing price; invoice generated; client disburses 8% success fee into our SBI Ranipet Account within 7 banking days.', body),
            Paragraph('<b>Within 7 Days</b>', callout),
            Paragraph('<b>~1 Week<br/>(0.25 Mo)</b>', callout),
            Paragraph('<font color="#0F2942"><b>Final Settlement<br/>Month 5 &ndash; 6</b></font>', callout)
        ]
    ]
    t_timeline = Table(timeline_data, colWidths=[120, 202, 65, 80, 75])
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#DCFCE7')), # Green highlight for Demat credit
    ]))
    story.append(t_timeline)
    story.append(Spacer(1, 4))

    # REALISTIC SCENARIOS SUMMARY TABLE
    story.append(Paragraph('<b>REALISTIC RECOVERY TIME-FRAME SCENARIOS (CLIENT GUIDANCE BENCHMARK)</b>', h2_style))
    
    scenarios_data = [
        [
            Paragraph('<b>RECOVERY SCENARIO</b>', ParagraphStyle('SH1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>WORKING DAYS</b>', ParagraphStyle('SH2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1)),
            Paragraph('<b>DURATION IN MONTHS</b>', ParagraphStyle('SH3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white, alignment=1)),
            Paragraph('<b>CONTROLLING FACTORS &amp; STATUTORY REALITY</b>', ParagraphStyle('SH4', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white))
        ],
        [
            Paragraph('<b>Fast-Track Execution<br/>(Best Case)</b>', body_bold),
            Paragraph('<b>90 &ndash; 110 Days</b>', callout),
            Paragraph('<font color="#15803D"><b>3.0 &ndash; 3.5 Months</b></font>', callout),
            Paragraph('Immediate bank attestation of Form ISR-2; zero RTA queries; Astral Nodal Officer uploads CVR within 20 days; expedited IEPF approval batch.', body)
        ],
        [
            Paragraph('<b>Standard Realistic Benchmark<br/>(Target Expected Window)</b>', body_bold),
            Paragraph('<b>120 &ndash; 165 Days</b>', callout),
            Paragraph('<font color="#0284C7"><b>4.0 &ndash; 5.5 Months</b></font>', callout),
            Paragraph('<b>Normal statutory operating window.</b> Accounts for standard Bigshare Mumbai audit queues, Nodal Officer verification cycle, and MCA New Delhi scrutiny batches.', body)
        ],
        [
            Paragraph('<b>Extended Administrative Buffer<br/>(Conservative Case)</b>', body_bold),
            Paragraph('<b>180 &ndash; 240 Days</b>', callout),
            Paragraph('<font color="#B45309"><b>6.0 &ndash; 8.0 Months</b></font>', callout),
            Paragraph('Occurs only if MCA portal undergoes technical schema migration or IEPF Authority issues technical query requiring re-submission of KYC affidavits.', body)
        ],
        [
            Paragraph('<b>Maximum Contractual Limit<br/>(Agreement Sunset Clause)</b>', body_bold),
            Paragraph('<b>365 Days</b>', callout),
            Paragraph('<b>12.0 Months Max</b>', callout),
            Paragraph('Per Clause 5 of our signed agreement, if recovery exceeds 12 months, mandate automatically expires with <b>Rs. 0 financial liability or claim</b> against client.', body)
        ]
    ]
    t_scen = Table(scenarios_data, colWidths=[110, 75, 85, 272])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_teal),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#EFF6FF')), # Blue highlight for standard target
    ]))
    story.append(t_scen)
    story.append(Spacer(1, 4))

    # TACTICS CALLOUT
    tactic_box = (
        '<b>HOW OUR ADVISORY PRACTICE CUTS THE RECOVERY TIME BY 50%:</b><br/>'
        '&bull; <b>Pre-Vetted Mismatch Prevention:</b> 80% of retail IEPF claims get stuck for 12+ months due to tiny spelling mismatches between Aadhaar, PAN, and Demat CML. We pre-vet every letter against Astral\'s 2007 IPO allotment register before filing.<br/>'
        '&bull; <b>Direct Mumbai Physical Inward:</b> Instead of postal delays, our physical docket is delivered directly to Bigshare Services\' inward counter at Andheri East, Mumbai, cutting 3 weeks off queue time.<br/>'
        '&bull; <b>Active Nodal Officer Liaison:</b> We maintain real-time follow-up with Astral Limited\'s Secretarial Desk to ensure the Company Verification Report (CVR) is filed well within the 30-day statutory window.'
    )
    t_tactic = Table([[Paragraph(tactic_box, body)]], colWidths=[542])
    t_tactic.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#86EFAC')),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_tactic)

    # PAGE BREAK TO KEEP SECTION 5, 6 & CREDENTIALS ON PAGE 4
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: FINAL REALIZATION, CHECKLIST & PRACTICE CREDENTIALS
    # =========================================================================
    story.append(Paragraph('5. THE FINAL STEP WITH 100% PROCESSED WORK (SETTLEMENT &amp; COMMISSION)', h1_style))
    story.append(Paragraph('This is the grand finale when the government releases the assets, the client receives everything, and our practice gets paid:', body))

    final_steps = [
        [
            Paragraph('<b>MILESTONE</b>', ParagraphStyle('FT1', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>EXACT EXECUTION EVENT</b>', ParagraphStyle('FT2', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white)),
            Paragraph('<b>FINANCIAL &amp; AUDIT VERIFICATION</b>', ParagraphStyle('FT3', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.white))
        ],
        [
            Paragraph('<b>1. NSDL/CDSL Corporate Action Credit</b>', body_bold),
            Paragraph('The IEPF Authority triggers an electronic Corporate Action instruction. The Central Depository directly credits <b>13,895 Equity Shares of Astral Limited</b> into CA Prakash Tekwani\'s active Demat account.', body),
            Paragraph('Visible on client Demat &amp; <a href="https://eservices.nsdl.com" color="#0284C7"><u>NSDL e-CAS</u></a> / <a href="https://www.cdslindia.com" color="#0284C7"><u>CDSL Portal</u></a>.', callout)
        ],
        [
            Paragraph('<b>2. Cash Dividend Direct Bank Credit</b>', body_bold),
            Paragraph('The Ministry of Corporate Affairs triggers electronic Public Financial Management System (<a href="https://pfms.nic.in" color="#0284C7"><u>PFMS / DBT</u></a>) credit of <b>Rs. 5,525.50+ accumulated dividends</b> directly into the client\'s bank account.', body),
            Paragraph('Instant bank SMS &amp; credit narration: <i>"CREDIT VIA PFMS / IEPF AUTHORITY GOVT OF INDIA"</i>.', callout)
        ],
        [
            Paragraph('<b>3. Independent Tracking Confirmation</b>', body_bold),
            Paragraph('We log into the <a href="https://www.mca.gov.in/content/mca/global/en/foportal/foportal-link/track-srn.html" color="#0284C7"><u>MCA Track SRN Portal</u></a>. The claim status displays: <b>"CLOSED - SHARES &amp; AMOUNT CREDITED"</b> with the Sanction Order number. We download the official sanction certificate.', body),
            Paragraph('Irrefutable government documentary proof of completed performance.', callout)
        ],
        [
            Paragraph('<b>4. Valuation &amp; Invoice Generation</b>', body_bold),
            Paragraph('On the day of Demat credit, we record the official <b>NSE Closing Rate of Astral Limited</b> via <a href="https://www.nseindia.com/get-quotes/equity?symbol=ASTRAL" color="#0284C7"><u>NSE India Portal</u></a> (e.g., Rs. 1,425 x 13,895 shares = Rs. 1,98,00,375). We issue our professional fee tax invoice for <b>8% (Rs. 15,84,030.00)</b>.', body),
            Paragraph('Invoice delivered via WhatsApp &amp; Email with MCA Sanction Order copy attached.', callout)
        ],
        [
            Paragraph('<b>5. Mandatory 7-Day Remittance Receipt</b>', body_bold),
            Paragraph('Per Clause 4 of our Agreement, CA Prakash Tekwani disburses the 8% fee (Rs. 15.84 Lakhs) via RTGS / NEFT directly into our State Bank of India (SBI) Account within 7 banking days.', body),
            Paragraph('Client retains ~Rs. 1.82 Crore net gain; our practice realizes full professional fee.', callout)
        ]
    ]
    t_final = Table(final_steps, colWidths=[120, 262, 160])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_final)
    story.append(Spacer(1, 4))

    # SECTION 6: EXECUTIVE CHECKLIST
    story.append(Paragraph('6. EXECUTIVE ACTION CHECKLIST FOR MD ASRAR BASHA A (IMMEDIATE DESK ACTIONS)', h1_style))
    
    chk_data = [
        [
            Paragraph('<b>STEP 1: AWAIT SIGNED AGREEMENT</b><br/><font color="#475569">Confirm CA Prakash Tekwani returns the signed 2-page agreement with 2 witness signatures.</font>', body),
            Paragraph('<b>STEP 2: COLLECT CML &amp; KYC</b><br/><font color="#475569">Collect active Demat CML (stamped), PAN, Masked Aadhaar &amp; 1 cancelled cheque.</font>', body)
        ],
        [
            Paragraph('<b>STEP 3: GENERATE SEBI FORM ISR-2</b><br/><font color="#475569">Pre-fill Form ISR-2 with his bank details (<a href="https://customer-vault.onrender.com/api/documents/Official_SEBI_Form_ISR_2_Tekwani_Filled.pdf" color="#0284C7"><u>Download Form</u></a>) and email it to him for branch manager seal.</font>', body),
            Paragraph('<b>STEP 4: FILE FORM IEPF-5 ON MCA</b><br/><font color="#475569">Upload digital claim on MCA V3, generate SRN, and courier physical docket to Bigshare Mumbai.</font>', body)
        ]
    ]
    t_chk = Table(chk_data, colWidths=[271, 271])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_chk)
    story.append(Spacer(1, 4))

    # CREDENTIALS BOX
    cred_box = (
        '<b>OFFICIAL CORPORATE ASSET RECOVERY PRACTICE CREDENTIALS:</b><br/>'
        '<b>Lead Fiduciary Counsel:</b> MD ASRAR BASHA A (PAN: GEZPA2961D)<br/>'
        '<b>Professional Practice Jurisdiction:</b> Ranipet District &amp; Chennai, Tamil Nadu - 632509 (Pan-India Corporate Advisory Practice)<br/>'
        '<b>Direct Phone / WhatsApp:</b> +91 7358882822 &bull; <b>Official Email:</b> amdasrarbasha@gmail.com<br/>'
        '<b>Designated Client Settlement Account:</b> State Bank of India (SBI), Ranipet Branch &bull; A/c No: 44568126758 &bull; IFSC: SBIN0003783'
    )
    t_cred = Table([[Paragraph(cred_box, body)]], colWidths=[542])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#93C5FD')),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_cred)

    doc.build(story, canvasmaker=MasterManualCanvas)

    # Copy to artifacts and blueprints
    shutil.copy2(target_path, os.path.join(artifact_dir, filename))
    if os.path.exists(blueprints_dir):
        shutil.copy2(target_path, os.path.join(blueprints_dir, filename))

    # Re-render PNGs for verification
    doc_fitz = pymupdf.open(target_path)
    for i, page in enumerate(doc_fitz):
        pix = page.get_pixmap(dpi=150)
        pix.save(os.path.join(upload_dir, f'master_manual_page_{i+1}.png'))
        pix.save(os.path.join(artifact_dir, f'master_manual_page_{i+1}.png'))

    reader = pypdf.PdfReader(target_path)
    print(f"[+] Successfully generated {filename} with EXACT {len(reader.pages)} pages and re-rendered PNGs!")

if __name__ == "__main__":
    build_pdf()

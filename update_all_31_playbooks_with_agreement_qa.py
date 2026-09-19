import os
import shutil
import sqlite3
import json
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
upload_dir = os.path.join(vault_dir, "uploads")
db_path = os.path.join(vault_dir, "customers.db")

USER_NAME = "MD ASRAR BASHA A"
USER_PAN = "GEZPA2961D"
USER_ADDRESS = "Ranipet District & Chennai, Tamil Nadu - 632509 (Pan-India Corporate Advisory Practice)"
USER_PHONE = "+91 7358882822"
USER_EMAIL = "amdasrarbasha@gmail.com"
USER_PORTAL = "https://customer-vault.onrender.com"

class PlaybookCanvas(canvas.Canvas):
    def __init__(self, target_name, *args, **kwargs):
        super(PlaybookCanvas, self).__init__(*args, **kwargs)
        self.target_name = target_name
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(PlaybookCanvas, self).showPage()
        super(PlaybookCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFillColor(colors.HexColor("#0F2942"))
        self.rect(0, 786, 612, 6, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#0D9488"))
        self.rect(0, 782, 612, 4, fill=1, stroke=0)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(36, 766, "EXECUTIVE CALL PLAYBOOK | STATUTORY CONVERSION MASTER SCRIPT")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(576, 766, f"TARGET: {self.target_name.upper()}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 760, 576, 760)
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.line(36, 36, 576, 36)
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawString(36, 26, f"{USER_NAME} | Corporate IEPF Advisory Practice | Phone/WhatsApp: {USER_PHONE}")
        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(576, 26, f"Page {self._pageNumber} of {page_count} | 100% Success-Only Mandate")
        self.restoreState()

def build_playbook_pdf(client, lang, filepath):
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('PBTitle', fontName='Helvetica-Bold', fontSize=13, leading=15.5, textColor=colors.HexColor("#0F2942"))
    subtitle_style = ParagraphStyle('PBSub', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0D9488"))
    h1_style = ParagraphStyle('PBH1', fontName='Helvetica-Bold', fontSize=8.5, leading=10.5, textColor=colors.HexColor("#0F2942"))
    body_text = ParagraphStyle('PBBT', fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor("#334155"))
    body_bold = ParagraphStyle('PBBB', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.HexColor("#0F2942"))
    script_quote = ParagraphStyle('PBSQ', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#0F2942"))
    label_amber = ParagraphStyle('PBLA', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.HexColor("#92400E"))
    label_blue = ParagraphStyle('PBLB', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.HexColor("#1E40AF"))
    label_emerald = ParagraphStyle('PBLE', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.HexColor("#065F46"))
    label_purple = ParagraphStyle('PBLP', fontName='Helvetica-Bold', fontSize=7, leading=8.8, textColor=colors.HexColor("#5B21B6"))

    story = []

    # =========================================================================
    # PAGE 1: TITLE, SNAPSHOT, CORE PSYCHOLOGY & OPENING SCRIPT
    # =========================================================================
    lang_name = "ENGLISH (DIRECTOR / CA / HNI EDITION)" if lang == "EN" else ("TANGLISH (TAMIL NADU HNI CONVERSATION)" if lang == "TN" else "HINGLISH (HINDI BELT HNI CONVERSATION)")
    story.append(Paragraph("<b>HIGH-STAKES CLIENT CONVERSATION PLAYBOOK &bull; 11 PROTOCOL MASTER SCRIPT</b>", title_style))
    story.append(Paragraph(f"VERBATIM SPOKEN SCRIPT &bull; FORENSIC AUDIT HANDLERS &bull; LANGUAGE: <b>{lang_name}</b>", subtitle_style))
    story.append(Spacer(1, 4))

    fee_pct = client.get('fee_pct', 8)
    est_val = client.get('est_folio', '₹ 1.00 Cr')
    my_est_val = client.get('my_est_value', f'{fee_pct}% Success Fee')
    current_shares = client.get('current_shares', 5000)

    client_card = [
        [
            Paragraph(f"<b>TARGET BENEFICIARY:</b> {client['name']}", body_bold),
            Paragraph(f"<b>DEMAT FOLIO ID:</b> <font face='Courier'>{client['folio_id']}</font>", body_bold),
            Paragraph("<b>TARGET ASSET:</b> Astral Limited", body_bold)
        ],
        [
            Paragraph(f"<b>LOCATION:</b> {client['address'][:65]}...", body_text),
            Paragraph(f"<b>PORTFOLIO VALUE:</b> {est_val}", ParagraphStyle('CV1', fontName='Helvetica-Bold', fontSize=7, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>SUCCESS FEE ({fee_pct}%):</b> {my_est_val}", ParagraphStyle('CV2', fontName='Helvetica-Bold', fontSize=7, textColor=colors.HexColor("#B45309")))
        ]
    ]
    t_client = Table(client_card, colWidths=[200, 180, 160])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>CORE PSYCHOLOGY: HOW TO CONDUCT THIS CALL</b>", h1_style))
    mindset_text = (
        "<b>1. Total Authority & Zero Neediness:</b> You are bringing news of a multi-crore unclaimed family fortune sitting in government custody. You are an expert forensic auditor.<br/>"
        f"<b>2. The Golden Anchor:</b> Always repeat: <i>'We charge Rs. 0 in advance. All shares and cash flow 100% directly from Government to your own account. You only pay our {fee_pct}% fee AFTER assets are in your hands.'</i><br/>"
        "<b>3. Direct Demat & Bank Settlement:</b> Emphasize that the consultant never handles client funds or shares."
    )
    story.append(Paragraph(mindset_text, body_text))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>PHASE 1: THE FIRST 60 SECONDS (OPENING DIALOGUE)</b>", h1_style))
    story.append(Spacer(1, 2))

    salutation = client.get('salutation', client['name'].split()[0])

    if lang == "EN":
        open_script = (
            f"<i>\"Good day {salutation}. My name is <b>{USER_NAME}</b>. I am calling from Corporate IEPF Asset Recovery Practice regarding a statutory compliance matter.<br/>"
            f"I know you are exceptionally busy, so I will take exactly 60 seconds. We have recently audited the statutory registers of <b>Astral Limited</b> under Section 124(6) of the Companies Act.<br/>"
            f"We identified a high-value equity holding registered under your name at <b>{client['address'][:50]}</b> (Demat Folio: <font face='Courier'><b>{client['folio_id']}</b></font>).<br/>"
            f"Due to historical 1:4 and 1:3 bonus expansions, this portfolio has accumulated to approximately <b>{current_shares:,} shares valued at {est_val}</b> plus accumulated cash dividends sitting in government escrow. "
            f"I am calling to formally assist your family in securing 100% direct recovery back to your active Demat account with <b>zero advance fee</b>.\"</i>"
        )
    elif lang == "TN":
        open_script = (
            f"<i>\"Vanakkam {salutation}. En peyar <b>{USER_NAME}</b>. Naan Corporate IEPF Asset Recovery Practice-lendhu pesaren.<br/>"
            f"Unga business/work naduvula oru 60 seconds mattum pesalaama sir? Astral Limited company-oda official shareholder register audit pannumbodhu, unga peyarla irukkum high-value equity folio-vai identify pannirukom.<br/>"
            f"Unga Demat Folio: <font face='Courier'><b>{client['folio_id']}</b></font>, address: <b>{client['address'][:45]}</b>.<br/>"
            f"Astral company pottirukra 1:4 matrum 1:3 bonus shares moolamaaga, ungaloda holding ippo sumaar <b>{current_shares:,} shares</b>, adhaavathu <b>{est_val}</b> madhippulla asset-a valarndhirukku.<br/>"
            f"Indha shares and dividend escrows-a 100% ungaloda sontha Demat account-ku direct-ah meedkedukka dhaan naanga assist panrom, <b>advance fee edhuvum illaamal</b>.\"</i>"
        )
    else: # Hinglish
        open_script = (
            f"<i>\"Namaskar {salutation}. Mera naam <b>{USER_NAME}</b> hai. Main Corporate IEPF Asset Recovery Practice se call kar raha hoon ek statutory matter ke silsile mein.<br/>"
            f"Aapke busy schedule mein se sirf 60 seconds loonga. Humne <b>Astral Limited</b> ke shareholder register ka forensic audit kiya hai, jismein aapke registered folio (Folio: <font face='Courier'><b>{client['folio_id']}</b></font>) par unclaimed equity shares identify hue hain.<br/>"
            f"Astral ke repeated 1:4 aur 1:3 bonus issues ke chalte aapki holding expand hokar lagbhag <b>{current_shares:,} shares</b> ho chuki hai, jiski current market value <b>{est_val}</b> hai, saath mein cash dividends bhi escrow mein hain.<br/>"
            f"Hum aapko yeh 100% shares seedha aapke active Demat account mein recover karwane mein assist karte hain, woh bhi <b>zero advance fee</b> par.\"</i>"
        )

    t_open = Table([[Paragraph(f"<b>STEP 1: PERMISSION &amp; VALUE HOOK</b>", label_blue)], [Paragraph(open_script, script_quote)]], colWidths=[540])
    t_open.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_open)

    # =========================================================================
    # PAGE 2: OBJECTIONS 1 TO 5
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: OBJECTION HANDLING &amp; CORE FAQS (PART 1)</b>", h1_style))
    story.append(Spacer(1, 3))

    if lang == "EN":
        q1_title = "OBJECTION 1: \"I will go directly to the company office and handle it myself.\""
        q1_text = (
            f"<i>\"That is a natural first reaction. However, under <b>Section 124(6) of the Companies Act, 2013</b>, once shares remain unclaimed for 7 consecutive years, Astral Limited loses legal jurisdiction over them.<br/>"
            f"The company cannot issue shares or cash to you directly. The assets are in the statutory custody of the <b>IEPF Authority under the Ministry of Corporate Affairs in New Delhi</b>, managed via Registrar <b>Bigshare Services in Mumbai</b>.<br/>"
            f"Visiting the registered office will only redirect you to file digital <b>Form IEPF-5</b>, which requires exact legal affidavits, indemnity bonds, and reconciliation. That exact turnkey process is what we manage with zero upfront risk.\"</i>"
        )
        q2_title = "QUESTION 2: \"Who is your organization and where are you located?\""
        q2_text = (
            f"<i>\"We are an institutional IEPF Advisory &amp; Transmission Consultancy headed by <b>{USER_NAME}</b>, operating from Tamil Nadu (Chennai &amp; Ranipet) and serving clients pan-India.<br/>"
            f"We specialize exclusively in high-net-worth recovery under MCA rules. All interactions are governed by a legally binding service agreement and tracked live on our portal <b>{USER_PORTAL}</b>.\"</i>"
        )
        q3_title = "QUESTION 3: \"How did you get my Demat / Folio ID and contact information?\""
        q3_text = (
            f"<i>\"Under Rule 5(8) of the IEPF Rules, listed companies are legally required to publish the Gazette list of unclaimed shareholders with Folio IDs. "
            f"Our forensic compliance desk cross-referenced Astral Limited's gazette records with public registries to trace eligible legal owners. We respect complete privacy and use verified public records solely for investor restitution.\"</i>"
        )
        q4_title = "QUESTION 4: \"What is my exact portfolio and share quantity?\""
        q4_text = (
            f"<i>\"In your registered Folio <font face='Courier'><b>{client['folio_id']}</b></font>, company records certify a holding of approximately <b>{current_shares:,} equity shares</b> plus uncashed cash dividends of <b>Rs. {client.get('total_unclaimed_div', 0):,.2f}</b>. "
            f"At Astral's current share price (~Rs. 1,425), this folio is worth approximately <b>{est_val}</b>.\"</i>"
        )
        q5_title = "QUESTION 5: \"How did my investment become so huge?\""
        q5_text = (
            f"<i>\"Astral Limited is one of India's biggest compounders. On top of massive share appreciation, Astral declared repeated bonus issues: <b>1:4 bonus in September 2019</b>, <b>1:3 bonus in March 2021</b>, and <b>1:3 bonus in March 2023</b>. "
            f"Even if your starting shares were modest, the bonus shares compounded by 2.22x and expanded into this fortune!\"</i>"
        )
    elif lang == "TN":
        q1_title = "OBJECTION 1: \"Naan direct-ah company office-ke poi pesikiren.\""
        q1_text = (
            f"<i>\"Sir, unga instinct puriyudhu. Aana <b>Companies Act 2013 Section 124(6)</b> padi, 7 years continuous-ah claim pannala-na, company-ku andha shares mela direct authority irukaadhu.<br/>"
            f"Astral company office-la ungalukku shares thara mudiyaadhu. Idhu Central Government-oda <b>IEPF Authority (New Delhi)</b> custody-la irukku, idhoda RTA <b>Bigshare Services (Mumbai)</b>.<br/>"
            f"Neenga company office-ku ponaalum, avanga ungalai MCA portal-la digital <b>Form IEPF-5</b> file panna dhaan solvanga. Andha legal documentation and verification-a 100% guarantee-yoda naanga zero advance-la panni tharom.\"</i>"
        )
        q2_title = "QUESTION 2: \"Neenga yaaru? Unga office enga irukku?\""
        q2_text = (
            f"<i>\"Naanga specialized Corporate IEPF Advisory firm. En peyar <b>{USER_NAME}</b>, Tamil Nadu (Chennai &amp; Ranipet) lendhu operate panrom. Pan-India level-la clients represent panrom.<br/>"
            f"Industrialists, business owners, and HNI families-oda complex share transmission and government claims dhaan enga core expertise. Engaloda transparency portal <b>{USER_PORTAL}</b>-la details track pannalaam.\"</i>"
        )
        q3_title = "QUESTION 3: \"Ennoda Demat Folio ID and phone number ungalukku eppadi theriyum?\""
        q3_text = (
            f"<i>\"Sir, Central Government IEPF Rules padi, 7 varusham unclaimed dividends irukra shareholders list-a companies statutory Gazette-la publish pannanum. "
            f"Engaloda compliance research team Astral Limited gazette filings-a verified public records-oda match panni, genuine shareholders-ku idhai communicate panrom.\"</i>"
        )
        q4_title = "QUESTION 4: \"Ennoda exact portfolio and share count evlo?\""
        q4_text = (
            f"<i>\"Sir, ungaloda Folio <font face='Courier'><b>{client['folio_id']}</b></font>-la, total-ah sumaar <b>{current_shares:,} equity shares</b> certified aagirukku, koodave <b>Rs. {client.get('total_unclaimed_div', 0):,.2f}</b> cash dividend escrow-la irukku. "
            f"Current market price (~Rs. 1,425)-la idhoda value <b>{est_val}</b>.\"</i>"
        )
        q5_title = "QUESTION 5: \"Ivlo periya amount eppadi aachu?\""
        q5_text = (
            f"<i>\"Astral Limited India-la oru mega wealth creator. Stock price eri irukardhu mattum illaama, company 3 thadava bonus shares thandhirukaanga: <b>2019-la 1:4 bonus</b>, <b>2021-la 1:3 bonus</b>, and <b>2023-la 1:3 bonus</b>. "
            f"Idhanaala unga original shares 2.22x multiply aagi ivlo periya crorepati portfolio-va maari irukku!\"</i>"
        )
    else: # Hinglish
        q1_title = "OBJECTION 1: \"Main seedha company office jakar baat kar lunga.\""
        q1_text = (
            f"<i>\"Sir, aapka aisa sochna bilkul natural hai. Lekin <b>Companies Act Section 124(6)</b> ke mutabiq, jab 7 saal tak shares unclaimed rehte hain toh company ka legal control khatam ho jata hai.<br/>"
            f"Astral company chahe bhi toh aapko direct shares release nahi kar sakti. Yeh assets Central Government ki <b>IEPF Authority (New Delhi)</b> ke paas hain, jiska record Registrar <b>Bigshare Services (Mumbai)</b> maintain karti hai.<br/>"
            f"Company office jane par bhi woh aapko online <b>Form IEPF-5</b> bharne ko kahenge. Wahi technical reconciliation hum zero advance par handle karte hain.\"</i>"
        )
        q2_title = "QUESTION 2: \"Aapka organization kya hai aur aap kahan located hain?\""
        q2_text = (
            f"<i>\"Hum corporate IEPF advisory practice hain jise <b>{USER_NAME}</b> lead karte hain. Humara primary office Tamil Nadu (Chennai/Ranipet) mein hai aur hum pan-India HNI investors ko represent karte hain.<br/>"
            f"Hum legal agreements ke tahat transparently kaam karte hain aur aap hamare central portal <b>{USER_PORTAL}</b> par record dekh sakte hain.\"</i>"
        )
        q3_title = "QUESTION 3: \"Aapko mera Demat / Folio ID aur contact details kahan se mila?\""
        q3_text = (
            f"<i>\"Sir, Central Government IEPF Rules ke tahat har listed company ko 7 saal se unpaid shareholders ki official list gazette karni hoti hai. "
            f"Hamari forensic audit team Astral Limited ke gazette records ko verified corporate directories ke saath match karke legal investors tak restitution deliver karti hai.\"</i>"
        )
        q4_title = "QUESTION 4: \"Mera exact portfolio aur share quantity kitna hai?\""
        q4_text = (
            f"<i>\"Sir, aapke Folio <font face='Courier'><b>{client['folio_id']}</b></font> mein company records ke mutabiq lagbhag <b>{current_shares:,} equity shares</b> hain aur saath hi <b>Rs. {client.get('total_unclaimed_div', 0):,.2f}</b> ka unpaid cash dividend hai. "
            f"Current Astral share price (~Rs. 1,425) par aapke portfolio ki valuation lagbhag <b>{est_val}</b> hai.\"</i>"
        )
        q5_title = "QUESTION 5: \"Itna chhota investment itna bada kaise ban gaya?\""
        q5_text = (
            f"<i>\"Astral Limited share market ka historic multibagger stock hai. Price growth ke alawa company ne 3 baar bonus shares announce kiye: <b>2019 mein 1:4 bonus</b>, <b>2021 mein 1:3 bonus</b>, aur <b>2023 mein 1:3 bonus</b>. "
            f"Is compounding ke chalte aapke shares 2.22x multiply ho chuke hain!\"</i>"
        )

    for q_t, q_b, col in [(q1_title, q1_text, colors.HexColor("#FFFBEB")), (q2_title, q2_text, colors.HexColor("#F8FAFC")), (q3_title, q3_text, colors.HexColor("#FFFBEB")), (q4_title, q4_text, colors.HexColor("#F8FAFC")), (q5_title, q5_text, colors.HexColor("#FFFBEB"))]:
        t_q = Table([[Paragraph(f"<b>{q_t}</b>", label_amber if col == colors.HexColor("#FFFBEB") else label_blue)], [Paragraph(q_b, script_quote)]], colWidths=[540])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), col),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D") if col == colors.HexColor("#FFFBEB") else colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_q)
        story.append(Spacer(1, 2.5))

    # =========================================================================
    # PAGE 3: STATUTORY FORENSICS & THE 2 CRITICAL NEW QUESTIONS (Q6, Q9, Q10)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: STATUTORY FORENSICS &amp; TRUST SAFEGUARDS (PART 2)</b>", h1_style))
    story.append(Spacer(1, 3))

    if lang == "EN":
        q6_title = "QUESTION 6: \"Where can I see my shares and the exact amount?\""
        q6_text = (
            f"<i>\"You do not have to take our word for it. You can independently verify your shares in 3 official places:<br/>"
            f"1. <b>Astral Limited Official Portal (astralpipes.com):</b> Investor Relations &rarr; 'Transfer to IEPF' gazette lists your Folio <font face='Courier'><b>{client['folio_id']}</b></font>.<br/>"
            f"2. <b>Ministry of Corporate Affairs Portal (iepf.gov.in):</b> 'Search Unclaimed / Unpaid Amounts' under company 'Astral Limited'.<br/>"
            f"3. <b>Registrar Bigshare Services (bigshareonline.com):</b> Investor service desk for Astral Limited under ISIN INE006I01046.\"</i>"
        )
        q9_title = "QUESTION 9: \"My Demat account has not moved into IEPF, it is a current active account?\""
        q9_text = (
            f"<i>\"You are 100% correct! A Demat account is held with your Depository Participant and <b>never moves to IEPF</b>. "
            f"Under Section 124(6) of the Companies Act, when dividends on a specific company (Astral) fail to reach your bank for 7 consecutive years, the company is legally required to execute a corporate action debit transferring <b>only the specific Astral shares</b> to the IEPF Authority Demat account.<br/>"
            f"Your active Demat account is the <b>best possible news</b>: if the shares are still showing in your Demat (under current transfer schedule), filing Form ISR-1/2 with Bigshare Services <b>halts the transfer immediately</b> and releases your cash dividends; if debit has occurred, your active Demat is required so Form IEPF-5 credits 100% of the recovered shares directly back to you!\"</i>"
        )
        q10_title = "QUESTION 10: \"Why should we trust to do KYC to you?\""
        q10_text = (
            f"<i>\"Entrusting KYC is a serious matter. Our practice operates on 5 unbreakable fiduciary safeguards:<br/>"
            f"1. <b>Zero Financial Risk:</b> Rs. 0 advance fee. Our {fee_pct}% fee is payable strictly AFTER shares and cash are in your Demat and bank.<br/>"
            f"2. <b>Direct Demat Credit:</b> We never touch client funds. Central Government credits 100% directly to your accounts.<br/>"
            f"3. <b>Standard SEBI Forms Only:</b> We collect only Form ISR-1/ISR-2. We never ask for passwords, OTPs, or blank cheques.<br/>"
            f"4. <b>Masked KYC Security:</b> You provide masked Aadhaar (first 8 digits hidden) and cheque crossed 'FOR ASTRAL KYC ONLY'.<br/>"
            f"5. <b>Stamped Legal Agreement:</b> We execute an official Rs. 100 stamp paper agreement with full SBI bank details protecting you.\"</i>"
        )
    elif lang == "TN":
        q6_title = "QUESTION 6: \"Ennoda shares matrum exact amount-ai naan enga direct-ah paarkka mudiyum?\""
        q6_text = (
            f"<i>\"Neenga engala mattum namba thevaiye illa sir. 3 official direct sources-la ungaloda shares-a verify pannalaam:<br/>"
            f"1. <b>Astral Limited Official Website (astralpipes.com):</b> 'Investor Relations &rarr; IEPF Transferred Shares' section-la unga Folio <font face='Courier'><b>{client['folio_id']}</b></font> irukkum.<br/>"
            f"2. <b>MCA Government Portal (iepf.gov.in):</b> 'Search Unclaimed Amounts' tab-la Astral Limited select panni paarkkalaam.<br/>"
            f"3. <b>Bigshare Services (bigshareonline.com):</b> Astral-oda official Registrar portal-la unga folio details verify pannalaam.\"</i>"
        )
        q9_title = "QUESTION 9: \"Ennoda Demat account active-ah dhaan irukku, idhu IEPF-ku pola-ye?\""
        q9_text = (
            f"<i>\"Neenga solradhu 100% sari sir! Demat account eppodhume IEPF-ku pogaadhu. Andha account ungaloda Depository Participant kitta ungaloda sontha account-ah dhaan irukkum.<br/>"
            f"Companies Act Section 124(6) padi, 7 years continuous-ah dividend claim aagala-na, Astral company andha specific shares-a mattum corporate action valiyaaga IEPF account-ku transfer panna legal obligation irukku.<br/>"
            f"Ungaloda Demat account active-ah irukkaradhu romba nalla vishayam: transfer innum mudiyala-na, Form ISR-1/ISR-2 pottu shares transfer aagama thaduthu dividend-a release pannalaam; or transfer aagi irundhaalum, MCA Form IEPF-5 valiyaaga 100% shares ungaloda active Demat-ke direct-ah credit aagidum!\"</i>"
        )
        q10_title = "QUESTION 10: \"Naanga ungalukku KYC documents thara yen nambanum?\""
        q10_text = (
            f"<i>\"Idhu romba mukkiyamaana kelvi sir. Engaloda practice 5 strict legal protections-la dhaan operate aagudhu:<br/>"
            f"1. <b>Zero Financial Risk:</b> Advance fee Rs. 0. Shares matrum panam ungaloda account-la vandha apram dhaan {fee_pct}% success fee.<br/>"
            f"2. <b>Direct Settlement:</b> Engalukku ungaloda shares-o panamo varaadhu&mdash;Central Government direct-ah unga Demat &amp; Bank-ku anupum.<br/>"
            f"3. <b>Standard SEBI Forms Mattum:</b> Form ISR-1 matrum ISR-2 mattum dhaan thevai. Password, PIN, OTP edhuvum kekka maatom.<br/>"
            f"4. <b>Masked KYC Security:</b> Aadhaar-la first 8 digits mask panni, cancelled cheque-la 'FOR KYC ONLY' nu ezhudhi kudunga.<br/>"
            f"5. <b>Stamped Legal Agreement:</b> Rs. 100 stamp paper-la formal agreement execute panni, SBI bank details transparent-ah koduthu ungalukku full legal indemnity tharom.\"</i>"
        )
    else: # Hinglish
        q6_title = "QUESTION 6: \"Main apne shares aur exact amount kahan dekh aur verify kar sakta hoon?\""
        q6_text = (
            f"<i>\"Aapko hamari baat par aankh band karke vishwas karne ki zaroorat nahi hai. Aap khud 3 official jagah verify kar sakte hain:<br/>"
            f"1. <b>Astral Limited Official Website (astralpipes.com):</b> Investor Relations &rarr; 'Transfer to IEPF' section mein aapka Folio <font face='Courier'><b>{client['folio_id']}</b></font> registered hai.<br/>"
            f"2. <b>MCA Government Portal (iepf.gov.in):</b> 'Search Unclaimed / Unpaid Amounts' par Astral Limited search karke dekh sakte hain.<br/>"
            f"3. <b>Registrar Bigshare Services (bigshareonline.com):</b> Astral ke official Registrar portal par investor tracking uplabdh hai.\"</i>"
        )
        q9_title = "QUESTION 9: \"Mera Demat account toh active hai, yeh IEPF mein nahi gaya hai?\""
        q9_text = (
            f"<i>\"Aapka yeh observation 100% sahi hai sir! Demat account kabhi bhi IEPF mein nahi jata. Demat account aapka private account hota hai jo aapke broker ke paas active rehta hai.<br/>"
            f"Companies Act Section 124(6) ke mutabiq, jab 7 saal tak dividend uncashed rehta hai, toh company sirf us specific stock (Astral Limited) ke shares ko corporate debit karke IEPF Authority ke account mein transfer karti hai.<br/>"
            f"Aapka Demat account active hona sabse acchi baat hai: agar transfer complete nahi hua hai, toh Bigshare Services mein Form ISR-1/2 dekar transfer roka ja sakta hai aur dividend release ho jayega; aur agar transfer ho bhi chuka hai, toh MCA Form IEPF-5 se 100% shares seedha aapke active Demat account mein hi credit honge!\"</i>"
        )
        q10_title = "QUESTION 10: \"Hum aapko KYC documents dene par trust kyun karein?\""
        q10_text = (
            f"<i>\"Yeh bilkul laazmi sawaal hai sir. Hamari advisory 5 unbreakable legal safeguards par kaam karti hai:<br/>"
            f"1. <b>Zero Financial Risk:</b> Advance fee Rs. 0. Humara {fee_pct}% fee tabhi payable hai jab shares aur cash dividend aapke Demat aur bank account mein credit ho jayein.<br/>"
            f"2. <b>Direct Government Settlement:</b> Hum kisi bhi client ke paise ya shares ko touch nahi karte&mdash;sab kuch Government of India se direct aapke account mein aata hai.<br/>"
            f"3. <b>Sirf SEBI Forms:</b> Hum sirf standard SEBI Form ISR-1 aur ISR-2 use karte hain. Hum koi password, OTP ya blank cheque nahi maangte.<br/>"
            f"4. <b>Masked KYC Protocol:</b> Aap masked Aadhaar (pehli 8 digits chhipa kar) aur cheque par 'FOR ASTRAL KYC ONLY' likh kar dete hain.<br/>"
            f"5. <b>Legal Stamped Agreement:</b> Hum Rs. 100 stamp paper par legally binding agreement execute karte hain jismein SBI bank details aur full legal protection hoti hai.\"</i>"
        )

    for q_t, q_b, col in [(q6_title, q6_text, colors.HexColor("#F8FAFC")), (q9_title, q9_text, colors.HexColor("#EFF6FF")), (q10_title, q10_text, colors.HexColor("#F0FDF4"))]:
        border_col = colors.HexColor("#3B82F6") if col == colors.HexColor("#EFF6FF") else (colors.HexColor("#10B981") if col == colors.HexColor("#F0FDF4") else colors.HexColor("#CBD5E1"))
        t_q = Table([[Paragraph(f"<b>{q_t}</b>", label_blue if col == colors.HexColor("#EFF6FF") else (label_emerald if col == colors.HexColor("#F0FDF4") else label_purple))], [Paragraph(q_b, script_quote)]], colWidths=[540])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), col),
            ('BOX', (0,0), (-1,-1), 1, border_col),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_q)
        story.append(Spacer(1, 3))

    # =========================================================================
    # PAGE 4: DOCUMENTS REQUIRED, AGREEMENT EXPLANATION, SUCCESS FEE & CLOSING
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: DOCUMENT REQUIREMENTS, SERVICE AGREEMENT &amp; CLOSING (PART 3)</b>", h1_style))
    story.append(Spacer(1, 2))

    if lang == "EN":
        q7_title = "QUESTION 7: \"What documents do you need from me to file the claim?\""
        q7_text = (
            f"<i>\"We require only standard statutory identification documents to file Form IEPF-5 with MCA:<br/>"
            f"1. <b>Client Master List (CML)</b> from your active Demat broker with DP stamp and signature.<br/>"
            f"2. Self-attested copy of <b>PAN Card and Masked Aadhaar Card</b> (first 8 digits masked).<br/>"
            f"3. Original <b>Cancelled Cheque leaf</b> carrying your name, linked to your Demat bank account.<br/>"
            f"4. Our drafted <b>Non-Judicial Stamp Paper Indemnity Bond &amp; Advance Receipt</b> signed by you.\"</i>"
        )
        
        q_agr_title = "QUESTION 8: \"What is there in this Service Agreement? What are the key terms?\""
        q_agr_text = (
            f"<i>\"Our Service Agreement is a simple 3-pillar legal framework created entirely for your fiduciary protection:<br/>"
            f"1. <b>Statutory Scope:</b> It formally authorises our practice to liaise with Astral Limited, Registrar Bigshare Services, and the IEPF Authority (MCA) to draft and process your Form IEPF-5 claim.<br/>"
            f"2. <b>Rs. 0 Advance / Zero Risk:</b> You pay <b>Rs. 0 upfront</b>. There is zero retainer, no out-of-pocket processing cost, and no hidden legal fee.<br/>"
            f"3. <b>Direct Asset Delivery &amp; Success Fee:</b> 100% of recovered equity shares and accumulated cash dividends are credited <b>directly by the Government into your own active Demat and Bank account</b>. Our {fee_pct}% advisory fee is payable strictly AFTER assets are safely credited in your hands.<br/>"
            f"4. <b>Confidentiality:</b> All KYC and financial details are strictly confidential under fiduciary law and cannot be used for any other purpose.\"</i>"
        )

        q8_title = "QUESTION 9: \"Why should I pay a success fee when you operate from Tamil Nadu?\""
        q8_text = (
            f"<i>\"Under the Ministry of Corporate Affairs, IEPF restitution is a centralized digital process coordinated between MCA (New Delhi) and Bigshare Services (Mumbai). Physical geography has zero bearing.<br/>"
            f"A single discrepancy in name spelling, affidavit format, or RTA verification results in summary rejection by the Government. "
            f"Our <b>100% Contingent Model ({fee_pct}% fee, Rs. 0 Advance)</b> guarantees zero financial risk. You only compensate our practice after 100% of your shares are safely in your own Demat account.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"{salutation}, I have audited your entire Astral holding and prepared your formal <b>Executive Recovery Dossier</b> along with the <b>Statutory Share Certificate &amp; Agreement</b>.<br/>"
            f"I have sent both documents to your WhatsApp and email. Kindly review with your family or Chartered Accountant, and let us initiate the formal Bigshare reconciliation today.\"</i>"
        )
    elif lang == "TN":
        q7_title = "QUESTION 7: \"Claim file panna ennoda kitta irundhu enna documents thevai?\""
        q7_text = (
            f"<i>\"Sir, Central Government MCA portal-la Form IEPF-5 file panna simple basic KYC documents mattum podhum:<br/>"
            f"1. Ungaloda active Demat account-oda <b>Client Master List (CML)</b> copy (bank seal-oda).<br/>"
            f"2. <b>PAN Card matrum Masked Aadhaar Card</b> self-attested copies.<br/>"
            f"3. Ungaloda peyar print aana <b>Original Cancelled Cheque leaf</b> ('FOR KYC ONLY' nu ezhudhalaam).<br/>"
            f"4. Naanga draft panni anupum <b>Stamp Paper Indemnity Bond &amp; Advance Receipt</b>-la unga signature.\"</i>"
        )
        
        q_agr_title = "QUESTION 8: \"Indha Service Agreement-la enna irukku? Key terms enna?\""
        q_agr_text = (
            f"<i>\"Sir, indha Service Agreement ungaloda 100% legal safety-kaga simple-ah 3 core terms-la create pannirukom:<br/>"
            f"1. <b>Legal Authorization:</b> Astral Limited, Registrar Bigshare Services, matrum Central Government IEPF Authority kitta ungalukkaga Form IEPF-5 claim file panna formal authorization tharudhu.<br/>"
            f"2. <b>Zero Advance Fee:</b> Neenga <b>oru rupai kooda advance thara thevaiyilla (Rs. 0 Advance)</b>. Upfront fee, processing charge edhuvum kidayadhu.<br/>"
            f"3. <b>Direct Demat Delivery &amp; Success Fee:</b> Central Government ungaloda shares matrum uncashed dividend-a <b>direct-ah ungaloda sontha Demat &amp; Bank account-ke credit pannum</b>. Ungalukku assets vandha apram dhaan engaloda {fee_pct}% success fee neenga pay panna poreenga.<br/>"
            f"4. <b>Confidentiality:</b> Ungaloda KYC documents IEPF claim processing-ku mattume use aagum, full statutory safety guarantee.\"</i>"
        )

        q8_title = "QUESTION 9: \"Neenga Tamil Nadu-la irukinga, naan ungalukku success fee yen tharanum?\""
        q8_text = (
            f"<i>\"Sir, IEPF recovery enbadhu New Delhi Central Government MCA digital portal matrum Mumbai RTA Bigshare Services valiyaaga nadakkum federal process. Geographical distance oru thadaye illa.<br/>"
            f"Single document mistake irundhaalum Government reject pannidum. Adhai legal precision-oda complete panna dhaan engaloda <b>100% Success-Only Model ({fee_pct}% fee, Rs. 0 Advance)</b>. Shares Demat-la vandha apram dhaan neenga fee thara poreenga.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"Sir, ungaloda complete share calculations and bonus history-a audit panni <b>Executive Recovery Dossier</b> and <b>Share Audit Certificate</b> ready panniten.<br/>"
            f"Indha rendaiyum ungaloda WhatsApp-ku ippo anupuren. Unga family-oda review pannitu sollunga sir, innaike formal process initiate pannidalaam.\"</i>"
        )
    else: # Hinglish
        q7_title = "QUESTION 7: \"Claim file karne ke liye mujhse kya documents chahiye?\""
        q7_text = (
            f"<i>\"Sir, MCA portal par Form IEPF-5 file karne ke liye sirf standard statutory documents lagte hain:<br/>"
            f"1. Aapke active Demat broker se certified <b>Client Master List (CML)</b> copy (DP seal ke saath).<br/>"
            f"2. <b>PAN Card aur Masked Aadhaar Card</b> ki self-attested photocopy.<br/>"
            f"3. Name printed <b>Original Cancelled Cheque</b> (crossed 'FOR ASTRAL KYC ONLY').<br/>"
            f"4. Humare dwara draft kiya gaya <b>Non-Judicial Stamp Paper Indemnity Bond</b> par aapke signature.\"</i>"
        )

        q_agr_title = "QUESTION 8: \"Is Service Agreement mein kya likha hai? Iske main terms kya hain?\""
        q_agr_text = (
            f"<i>\"Sir, humara Service Agreement ekdam transparent aur simple 3 core pillars par bana hai jo poori tarah aapki safety ke liye hai:<br/>"
            f"1. <b>Legal Scope:</b> Yeh humein Astral Limited, Registrar Bigshare Services aur MCA ke IEPF portal par aapke behalf par legal Form IEPF-5 file karne ki official authorization deta hai.<br/>"
            f"2. <b>Zero Advance (100% Risk-Free):</b> Aapko <b>ek bhi rupiya advance nahi dena hai (Rs. 0 Advance)</b>. Koi retainer ya processing fee nahi hai.<br/>"
            f"3. <b>Direct Delivery &amp; Success Fee:</b> Central Government saare shares aur uncashed cash dividends <b>seedha aapke apne Demat aur Bank account mein transfer karti hai</b>. Humara {fee_pct}% success fee tabhi payable hai jab shares aur paisa aapke account mein safely credit ho jayein.<br/>"
            f"4. <b>Data Confidentiality:</b> Aapke KYC documents (Aadhaar/PAN/CML) strictly IEPF claim filing ke liye hi use hote hain under complete fiduciary trust.\"</i>"
        )

        q8_title = "QUESTION 9: \"Aap Tamil Nadu se hain, main aapko success commission kyun doon?\""
        q8_text = (
            f"<i>\"Sir, IEPF recovery New Delhi Central Government MCA portal aur Mumbai RTA Bigshare Services ke through hone wala centralized legal process hai. Distance se koi farq nahi padta.<br/>"
            f"Sabse important hai documentation error-free hona taaki claim reject na ho. Humara model <b>100% Contingent Success-Only ({fee_pct}% fee, Rs. 0 Advance)</b> hai. Jab tak shares aapke Demat mein nahi aate, aapko ek rupiya nahi dena.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"Sir, aapki complete audit aur bonus details ke saath maine aapka personalized <b>Executive Recovery Dossier</b> aur <b>Share Certificate</b> prepare kar liya hai.<br/>"
            f"Main dono documents abhi aapke verified WhatsApp par bhej raha hoon. Aap review kijiye, aur hum turant documentation start karte hain.\"</i>"
        )

    t_q7 = Table([[Paragraph(f"<b>{q7_title}</b>", label_amber)], [Paragraph(q7_text, script_quote)]], colWidths=[540])
    t_q7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q7)
    story.append(Spacer(1, 2.5))

    t_q_agr = Table([[Paragraph(f"<b>{q_agr_title}</b>", label_purple)], [Paragraph(q_agr_text, script_quote)]], colWidths=[540])
    t_q_agr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F3FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C4B5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q_agr)
    story.append(Spacer(1, 2.5))

    t_q8 = Table([[Paragraph(f"<b>{q8_title}</b>", label_blue)], [Paragraph(q8_text, script_quote)]], colWidths=[540])
    t_q8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q8)
    story.append(Spacer(1, 2.5))

    t_close = Table([[Paragraph(f"<b>{close_title}</b>", label_emerald)], [Paragraph(close_text, script_quote)]], colWidths=[540])
    t_close.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_close)

    class CustomCanvas(PlaybookCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(client['name'], *args, **kwargs)

    doc.build(story, canvasmaker=CustomCanvas)

if __name__ == "__main__":
    stats_path = os.path.join(vault_dir, 'master_client_stats.json')
    with open(stats_path, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, name, folio_id, address, est_folio, my_est_value, pdf3_path, pdf4_path FROM customers ORDER BY id')
    db_rows = {r['id']: dict(r) for r in c.fetchall()}
    conn.close()

    print(f"Regenerating all {len(clients)} Client Playbooks with Agreement Q&A (EN, TN, HI)...")

    page_counts = []
    address_leaks = []

    for client in clients:
        cid = client['id']
        db_info = db_rows.get(cid, {})
        client['pdf3_path'] = db_info.get('pdf3_path')
        client['pdf4_path'] = db_info.get('pdf4_path')
        client['salutation'] = client['name'].split()[0]
        client['fee_pct'] = 15 if cid == 10 else 8

        # Dr Phatak exact shares override
        if "Phatak" in client['name']:
            client['current_shares'] = 13140

        # Build English Playbook (PDF 3)
        p3_file = client['pdf3_path']
        if p3_file:
            p3_out_brain = os.path.join(artifact_dir, p3_file)
            p3_out_upload = os.path.join(upload_dir, p3_file)
            build_playbook_pdf(client, "EN", p3_out_brain)
            shutil.copyfile(p3_out_brain, p3_out_upload)
            
            # verify
            r = PdfReader(p3_out_upload)
            page_counts.append((p3_file, len(r.pages)))
            text = ' '.join([p.extract_text() or '' for p in r.pages])
            if 'appa pillai' in text.lower() or 'melvisharam' in text.lower():
                address_leaks.append(p3_file)

        # Build Regional Playbook (PDF 4)
        p4_file = client['pdf4_path']
        if p4_file:
            is_tn = client.get('is_tn', False)
            lang = "TN" if is_tn else "HI"
            p4_out_brain = os.path.join(artifact_dir, p4_file)
            p4_out_upload = os.path.join(upload_dir, p4_file)
            build_playbook_pdf(client, lang, p4_out_brain)
            shutil.copyfile(p4_out_brain, p4_out_upload)

            # verify
            r = PdfReader(p4_out_upload)
            page_counts.append((p4_file, len(r.pages)))
            text = ' '.join([p.extract_text() or '' for p in r.pages])
            if 'appa pillai' in text.lower() or 'melvisharam' in text.lower():
                address_leaks.append(p4_file)

        print(f"[OK] Client {cid}: {client['name']} -> {p3_file} & {p4_file}")

    print("\n--- PLAYBOOK VERIFICATION AUDIT ---")
    bad_pages = [x for x in page_counts if x[1] != 4]
    if bad_pages:
        print(f"WARNING: Page count anomalies found: {bad_pages}")
    else:
        print(f"SUCCESS: All {len(page_counts)} playbooks are EXACTLY 4 pages!")

    if address_leaks:
        print(f"WARNING: Address leaks found: {address_leaks}")
    else:
        print("SUCCESS: Zero address leaks across all playbooks!")

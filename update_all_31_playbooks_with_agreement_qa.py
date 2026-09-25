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
db_path = os.path.join(vault_dir, "uploads", "customers.db")
db_root_path = os.path.join(vault_dir, "customers.db")

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

    title_style = ParagraphStyle('PBTitle', fontName='Helvetica-Bold', fontSize=12, leading=14.5, textColor=colors.HexColor("#0F2942"))
    subtitle_style = ParagraphStyle('PBSub', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.HexColor("#0D9488"))
    h1_style = ParagraphStyle('PBH1', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#0F2942"))
    body_text = ParagraphStyle('PBBT', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#334155"))
    body_bold = ParagraphStyle('PBBB', fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.HexColor("#0F2942"))
    script_quote = ParagraphStyle('PBSQ', fontName='Helvetica', fontSize=6.2, leading=8.0, textColor=colors.HexColor("#0F2942"))
    label_amber = ParagraphStyle('PBLA', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#92400E"))
    label_blue = ParagraphStyle('PBLB', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#1E40AF"))
    label_emerald = ParagraphStyle('PBLE', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#065F46"))
    label_purple = ParagraphStyle('PBLP', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#5B21B6"))
    label_rose = ParagraphStyle('PBLR', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#9F1239"))

    story = []

    # =========================================================================
    # PAGE 1: TITLE, BENEFICIARY CARD, CORE PSYCHOLOGY & PRE-TRANSFER HOOK
    # =========================================================================
    lang_name = "ENGLISH (DIRECTOR / CA / HNI EDITION)" if lang == "EN" else ("TANGLISH (TAMIL NADU HNI CONVERSATION)" if lang == "TN" else "HINGLISH (HINDI BELT HNI CONVERSATION)")
    story.append(Paragraph("<b>HIGH-STAKES CLIENT CONVERSATION PLAYBOOK &bull; 13 PROTOCOL MASTER SCRIPT</b>", title_style))
    story.append(Paragraph(f"STATUTORY PRE-TRANSFER NOTICE &bull; VERBATIM CONVERSATION PROTOCOL &bull; LANGUAGE: <b>{lang_name}</b>", subtitle_style))
    story.append(Spacer(1, 3))

    fee_pct = client.get('fee_pct', 8)
    est_val = client.get('est_folio', '₹ 1.00 Cr')
    my_est_val = client.get('my_est_value', f'{fee_pct}% Success Fee')
    current_shares = client.get('current_shares', 5000)
    unclaimed_div = client.get('total_unclaimed_div', 0)

    client_card = [
        [
            Paragraph(f"<b>BENEFICIARY:</b> {client['name']}", body_bold),
            Paragraph(f"<b>FOLIO ID:</b> <font face='Courier'>{client['folio_id']}</font>", body_bold),
            Paragraph("<b>TARGET ASSET:</b> Astral Limited", body_bold)
        ],
        [
            Paragraph(f"<b>REGISTERED ADDRESS:</b> {client['address'][:65]}...", body_text),
            Paragraph(f"<b>PORTFOLIO VALUE:</b> {est_val}", ParagraphStyle('CV1', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>CONTINGENT SUCCESS FEE ({fee_pct}%):</b> {my_est_val}", ParagraphStyle('CV2', fontName='Helvetica-Bold', fontSize=6.8, textColor=colors.HexColor("#B45309")))
        ]
    ]
    t_client = Table(client_card, colWidths=[200, 180, 160])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>CORE PSYCHOLOGY &amp; STATUTORY POSITIONING</b>", h1_style))
    mindset_text = (
        "<b>1. Pre-Transfer Warning Position:</b> Never claim shares are already gone. The client's folio is currently listed on Astral's statutory schedule for <b>upcoming transfer to IEPF</b> under Section 124(6). You are alerting them before the final cut-off.<br/>"
        "<b>2. Share Protection Guarantee:</b> Under Section 124(6) proviso, claiming even 1 dividend or updating KYC legally halts transfer and de-lists the folio. Clients keep 100% of shares in their Demat undisturbed.<br/>"
        f"<b>3. The Golden Anchor:</b> Always repeat: <i>'We charge Rs. 0 in advance. Central Govt / RTA credits 100% directly to your accounts. You only pay our {fee_pct}% fee AFTER assets are safely in your possession.'</i>"
    )
    story.append(Paragraph(mindset_text, body_text))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>PHASE 1: THE FIRST 60 SECONDS (OPENING DIALOGUE)</b>", h1_style))
    story.append(Spacer(1, 2))

    salutation = client.get('salutation', client['name'].split()[0])

    if lang == "EN":
        open_script = (
            f"<i>\"Good day {salutation}. My name is <b>{USER_NAME}</b>. I am calling from Corporate IEPF Asset Recovery Practice regarding an urgent statutory compliance notice.<br/>"
            f"I know you are exceptionally busy, so I will take exactly 60 seconds. In our audit of Astral Limited's statutory regulatory filings under Section 124 of the Companies Act, "
            f"we identified that your equity folio (<font face='Courier'><b>{client['folio_id']}</b></font>) registered at <b>{client['address'][:45]}</b> is <b>officially listed on Astral's schedule for upcoming transfer to the IEPF (Investor Education and Protection Fund)</b>.<br/>"
            f"Due to historical 1:4 and 1:3 bonus expansions, your holding has compounded to approximately <b>{current_shares:,} shares valued at {est_val}</b>, plus <b>Rs. {unclaimed_div:,.2f}</b> in accumulated cash dividends sitting in statutory escrow.<br/>"
            f"Your folio is currently in the <b>statutory pre-transfer warning stage</b>. If action is not taken before the final corporate action cut-off, these shares will be debited from your Demat and surrendered to the Central Government IEPF Authority in New Delhi. "
            f"I am calling to formally assist your family in <b>de-listing your folio, protecting your shares in your Demat, and releasing your cash dividends</b> with <b>zero advance fee</b>.\"</i>"
        )
    elif lang == "TN":
        open_script = (
            f"<i>\"Vanakkam {salutation}. En peyar <b>{USER_NAME}</b>. Naan Corporate IEPF Asset Recovery Practice-lendhu oru mukkiyamaana statutory compliance notice vishayamaaga pesaren.<br/>"
            f"Unga busy work naduvula oru 60 seconds mattum pesalaama sir? Astral Limited company-oda official statutory compliance filings audit pannumbodhu, ungaloda Demat folio (<font face='Courier'><b>{client['folio_id']}</b></font>, address: <b>{client['address'][:40]}</b>) "
            f"<b>Central Government IEPF-ku transfer aaga koodiya official statutory schedule-la list aagirukradhai identify pannirukom</b>.<br/>"
            f"Astral company pottirukra bonus shares moolamaaga ungaloda holding <b>{current_shares:,} shares</b>, adhaavathu <b>{est_val}</b> madhippulla asset-a valarndhirukku, koodave <b>Rs. {unclaimed_div:,.2f}</b> cash dividend escrow-la irukku.<br/>"
            f"Ungaloda folio ippo <b>pre-transfer warning stage</b>-la irukku: statutory deadline-kulla regularise pannala-na, indha shares Demat-lendhu debit aagi New Delhi IEPF Authority custody-ku surrender aagidum. "
            f"Indha shares IEPF-ku pogamal thaduthu, unga Demat-laye safe-ah protect panni, cash dividends-ai direct-ah unga bank account-ke meedkedukka dhaan naanga assist panrom, <b>advance fee edhuvum illaamal</b>.\"</i>"
        )
    else: # Hinglish
        open_script = (
            f"<i>\"Namaskar {salutation}. Mera naam <b>{USER_NAME}</b> hai. Main Corporate IEPF Asset Recovery Practice se call kar raha hoon ek urgent statutory compliance notice ke silsile mein.<br/>"
            f"Aapke busy schedule mein se sirf 60 seconds loonga. Humne <b>Astral Limited</b> ke statutory filings ka compliance audit kiya hai, jismein aapka folio (<font face='Courier'><b>{client['folio_id']}</b></font>, registered address: <b>{client['address'][:40]}</b>) "
            f"<b>Central Government IEPF mein transfer hone ke official statutory schedule par listed paya gaya hai</b>.<br/>"
            f"Astral ke 1:4 aur 1:3 bonus issues ke chalte aapki holding expand hokar lagbhag <b>{current_shares:,} shares</b> ho chuki hai, jiski current market valuation <b>{est_val}</b> hai, saath hi <b>Rs. {unclaimed_div:,.2f}</b> ka cash dividend bhi escrow mein hai.<br/>"
            f"Aapka folio abhi <b>pre-transfer warning stage</b> par hai: agar statutory cut-off se pehle action nahi liya gaya, toh yeh valuable shares debited hokar Ministry of Corporate Affairs, IEPF Authority New Delhi ke paas surrender ho jayenge. "
            f"Hum aapko yeh shares IEPF mein jaane se rokne, Demat mein safe retain karne, aur cash dividends seedha aapke bank account mein release karwane mein assist karte hain, woh bhi <b>zero advance fee</b> par.\"</i>"
        )

    t_open = Table([[Paragraph(f"<b>STEP 1: PERMISSION, PRE-TRANSFER WARNING &amp; VALUE HOOK</b>", label_blue)], [Paragraph(open_script, script_quote)]], colWidths=[540])
    t_open.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_open)

    # =========================================================================
    # PAGE 2: OBJECTIONS 1 TO 5 (DIRECT COMPANY, ROLE/WHY NOT SELF, ORG, LEAK, VALUE)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: OBJECTION HANDLING &amp; CORE FAQS (PART 1 &bull; PROCEDURAL OBJECTIONS)</b>", h1_style))
    story.append(Spacer(1, 2.5))

    if lang == "EN":
        q1_title = "OBJECTION 1: \"I will go directly to Astral's corporate office and withdraw my funds / shares myself.\""
        q1_text = (
            f"<i>\"That is a natural first reaction. However, <b>Astral Limited is an industrial piping manufacturer, not a bank or financial intermediary</b>. Under SEBI regulations, company headquarters cannot entertain direct payout requests or issue shares across the counter.<br/>"
            f"All shareholder folios, unpaid dividends, and IEPF statutory transfers are delegated to their Registrar &amp; Transfer Agent (RTA), <b>Bigshare Services Pvt. Ltd. (Mumbai)</b>.<br/>"
            f"Visiting Astral's registered office in Ahmedabad will only result in them directing you to Bigshare under SEBI's strict investor service circulars (Form ISR-1/2). That exact complex reconciliation is what we handle turnkey with zero upfront risk.\"</i>"
        )
        q2_title = "OBJECTION 2: \"What is your role? Why do I need your help instead of doing it by myself?\""
        q2_text = (
            f"<i>\"While you legally have the right to approach the RTA, doing it yourself carries 4 severe procedural hazards where over 80% of self-filed claims get stuck or rejected:<br/>"
            f"1. <b>Signature &amp; Name Mismatch:</b> Over 7-10 years, signatures evolve and bank records change. A minor variance triggers an official RTA 'Deficiency Memo', freezing your folio for months.<br/>"
            f"2. <b>Form ISR-2 Bank Manager Attestation:</b> SEBI strictly mandates Form ISR-2 certified by a nationalized bank branch manager with their employee code, branch seal, and original cancelled cheque. Getting bank compliance without errors is a major bottleneck.<br/>"
            f"3. <b>The 7-Year Statutory Clock:</b> While a self-filer exchanges correspondence with the RTA, the 7-year clock does not pause. If the statutory deadline expires during delays, your shares get debited to IEPF Authority in New Delhi, converting a simple RTA de-listing into a multi-year MCA legal battle.<br/>"
            f"4. <b>100% Success-Based Protection:</b> We charge <b>Rs. 0 advance</b>. We handle all drafting, bank branch liaising, and Bigshare coordination. You only pay after assets are safely credited in your hands.\"</i>"
        )
        q3_title = "QUESTION 3: \"Who is your organization and where are you located?\""
        q3_text = (
            f"<i>\"We are an institutional IEPF Advisory &amp; Transmission Consultancy headed by <b>{USER_NAME}</b>, operating from Tamil Nadu (Chennai &amp; Ranipet) and serving clients pan-India.<br/>"
            f"We specialize exclusively in high-net-worth recovery under MCA rules. All interactions are governed by a legally binding service agreement and tracked live on our portal <b>{USER_PORTAL}</b>.\"</i>"
        )
        q4_title = "QUESTION 4: \"How did you get my Demat / Folio ID and contact information?\""
        q4_text = (
            f"<i>\"Under Section 124(6) and Rule 5(8) of the IEPF Rules, listed companies are legally required to publish the Gazette list of unclaimed shareholders with Folio IDs. "
            f"Our forensic compliance desk cross-referenced Astral Limited's gazette records with public registries to trace eligible legal owners. We respect complete privacy and use verified public records solely for investor restitution.\"</i>"
        )
        q5_title = "QUESTION 5: \"What is my exact portfolio and share quantity? How did it become so huge?\""
        q5_text = (
            f"<i>\"In your registered Folio <font face='Courier'><b>{client['folio_id']}</b></font>, company records certify a holding of approximately <b>{current_shares:,} equity shares</b> plus uncashed cash dividends of <b>Rs. {unclaimed_div:,.2f}</b>. "
            f"At Astral's current share price (~Rs. 1,425), this folio is worth approximately <b>{est_val}</b>.<br/>"
            f"Astral declared repeated bonus issues: <b>1:4 bonus in 2019</b>, <b>1:3 bonus in 2021</b>, and <b>1:3 bonus in 2023</b>. Even if your starting shares were modest, the bonus shares compounded by 2.22x and expanded into this fortune!\"</i>"
        )
    elif lang == "TN":
        q1_title = "OBJECTION 1: \"Naan direct-ah Astral company office-ke poi ennoda panam / shares-a vangikiren.\""
        q1_text = (
            f"<i>\"Sir, unga instinct puriyudhu, aana <b>Astral Limited oru manufacturing company, bank kidayadhu</b>. SEBI rules padi company headquarters-la direct-ah panamo shares-o thara legal authority illa.<br/>"
            f"Ella shareholder claims and dividend issues-aiyum company-oda official Registrar (RTA) aana <b>Bigshare Services Pvt. Ltd. (Mumbai)</b> dhaan manage panranga.<br/>"
            f"Neenga Ahmedabad office-ku ponaalum, avanga Bigshare RTA kitta SEBI Form ISR-1/2 submit panna dhaan solvanga. Andha legal documentation and verification-a 100% precision-oda naanga zero advance-la panni tharom.\"</i>"
        )
        q2_title = "OBJECTION 2: \"Unga role enna? Naane direct-ah panna koodaadha? Unga help yen thevai?\""
        q2_text = (
            f"<i>\"Sir, neengale direct-ah RTA kitta approach panna legal right irukku. Aana individual-ah pannumbodhu 80% claims reject aaga 4 mukkiyamaana risk irukku:<br/>"
            f"1. <b>Signature &amp; Bank Mismatch:</b> 7-10 varushathula signature matrum bank account maari irukkum. Chinna difference irundhaalum RTA 'Deficiency Memo' pottu reject pannidum.<br/>"
            f"2. <b>Form ISR-2 Bank Manager Attestation:</b> SEBI rule padi Form ISR-2-la nationalized bank branch manager seal, sign matrum original cancelled cheque crt-ah vanganum. Idhu romba periya challenge.<br/>"
            f"3. <b>7-Varusha Statutory Clock:</b> Neenga RTA kitta pesum podhu 7-year statutory clock nikaadhu. Deadline mudinjaal shares IEPF Authority New Delhi-ku transfer aagidum, apram periya MCA legal process aaidum.<br/>"
            f"4. <b>Zero Risk / Success Model:</b> Advance fee <b>Rs. 0</b>. Shares unga Demat-la safe-aagi, cash unga bank-ku vandha apram dhaan fee.\"</i>"
        )
        q3_title = "QUESTION 3: \"Neenga yaaru? Unga office enga irukku?\""
        q3_text = (
            f"<i>\"Naanga specialized Corporate IEPF Advisory firm. En peyar <b>{USER_NAME}</b>, Tamil Nadu (Chennai &amp; Ranipet) lendhu operate panrom. Pan-India level-la clients represent panrom.<br/>"
            f"Industrialists, business owners, and HNI families-oda complex share transmission and government claims dhaan enga core expertise. Engaloda transparency portal <b>{USER_PORTAL}</b>-la details track pannalaam.\"</i>"
        )
        q4_title = "QUESTION 4: \"Ennoda Demat Folio ID and phone number ungalukku eppadi theriyum?\""
        q4_text = (
            f"<i>\"Sir, Companies Act Section 124(6) padi, 7 varusham unclaimed dividends irukra shareholders list-a companies statutory Gazette-la publish pannanum. "
            f"Engaloda compliance research team Astral Limited gazette filings-a verified public records-oda match panni, genuine shareholders-ku idhai communicate panrom.\"</i>"
        )
        q5_title = "QUESTION 5: \"Ennoda exact portfolio evlo? Ivlo periya amount eppadi aachu?\""
        q5_text = (
            f"<i>\"Sir, ungaloda Folio <font face='Courier'><b>{client['folio_id']}</b></font>-la, total-ah sumaar <b>{current_shares:,} equity shares</b> certified aagirukku, koodave <b>Rs. {unclaimed_div:,.2f}</b> cash dividend escrow-la irukku. Valuation <b>{est_val}</b>.<br/>"
            f"Astral company 3 thadava bonus shares thandhirukaanga: <b>2019-la 1:4 bonus</b>, <b>2021-la 1:3 bonus</b>, and <b>2023-la 1:3 bonus</b>. Original shares 2.22x multiply aagi ivlo periya crorepati portfolio-va maari irukku!\"</i>"
        )
    else: # Hinglish
        q1_title = "OBJECTION 1: \"Main seedha Astral corporate office jakar apne shares / paise khud nikal lunga.\""
        q1_text = (
            f"<i>\"Sir, aapka aisa sochna bilkul natural hai, lekin <b>Astral Limited ek industrial manufacturing company hai, koi bank nahi</b>. SEBI regulations ke mutabiq corporate office direct cash payout ya shares hand-over nahi kar sakti.<br/>"
            f"Aapke saare claims, unpaid dividends aur IEPF records unke Registrar <b>Bigshare Services Pvt. Ltd. (Mumbai)</b> ke through SEBI Form ISR-1/2 ke tahat process hote hain.<br/>"
            f"Astral office jane par bhi woh aapko Bigshare ke paas compliance complete karne ko kahenge. Wahi technical reconciliation aur RTA follow-up hum zero advance par manage karte hain.\"</i>"
        )
        q2_title = "OBJECTION 2: \"Aapka role kya hai? Main khud kyun nahi kar sakta? Mujhe aapki kya zaroorat hai?\""
        q2_text = (
            f"<i>\"Sir, legally aapko khud RTA ke paas jane ka poora adhikaar hai. Lekin direct khud try karne par 80% applications in 4 major risks ke chalte reject ya freeze ho jati hain:<br/>"
            f"1. <b>Signature &amp; Bank Mismatch:</b> 7-10 saal purane records mein signature ya address mismatch hote hi RTA 'Deficiency Memo' issue karke claim freeze kar deta hai.<br/>"
            f"2. <b>Form ISR-2 Bank Manager Attestation:</b> SEBI ke mutabiq Form ISR-2 par nationalized bank branch manager ke exact seal, sign aur original cancelled cheque verification mein bohot delay hota hai.<br/>"
            f"3. <b>7-Saal Ka Statutory Clock:</b> RTA se correspondence ke dauran 7 saal ki statutory deadline ruki nahi rehti. Deadline khatam hote hi shares IEPF Authority New Delhi chale jayenge, fir lambi MCA legal process ban jayegi.<br/>"
            f"4. <b>Zero Advance / 100% Risk-Free:</b> Humara fee <b>Rs. 0 advance</b> hai. Saara documentation hum karte hain. Assets aapke account mein aane ke baad hi success fee payable hai.\"</i>"
        )
        q3_title = "QUESTION 3: \"Aapka organization kya hai aur aap kahan located hain?\""
        q3_text = (
            f"<i>\"Hum corporate IEPF advisory practice hain jise <b>{USER_NAME}</b> lead karte hain. Humara primary office Tamil Nadu (Chennai/Ranipet) mein hai aur hum pan-India HNI investors ko represent karte hain.<br/>"
            f"Hum legal agreements ke tahat transparently kaam karte hain aur aap hamare central portal <b>{USER_PORTAL}</b> par record dekh sakte hain.\"</i>"
        )
        q4_title = "QUESTION 4: \"Aapko mera Demat / Folio ID aur contact details kahan se mila?\""
        q4_text = (
            f"<i>\"Sir, Companies Act Section 124(6) ke tahat har listed company ko 7 saal se unpaid shareholders ki official list gazette karni hoti hai. "
            f"Hamari forensic audit team Astral Limited ke gazette records ko verified corporate directories ke saath match karke legal investors tak restitution deliver karti hai.\"</i>"
        )
        q5_title = "QUESTION 5: \"Mera exact portfolio kitna hai aur yeh itna bada kaise ban gaya?\""
        q5_text = (
            f"<i>\"Sir, aapke Folio <font face='Courier'><b>{client['folio_id']}</b></font> mein company records ke mutabiq <b>{current_shares:,} equity shares</b> hain aur saath hi <b>Rs. {unclaimed_div:,.2f}</b> ka unpaid cash dividend hai. Current valuation <b>{est_val}</b> hai.<br/>"
            f"Astral ne 3 baar bonus shares announce kiye: <b>2019 mein 1:4 bonus</b>, <b>2021 mein 1:3 bonus</b>, aur <b>2023 mein 1:3 bonus</b>. Is compounding ke chalte aapke shares 2.22x multiply ho chuke hain!\"</i>"
        )

    for q_t, q_b, col in [(q1_title, q1_text, colors.HexColor("#FFFBEB")), (q2_title, q2_text, colors.HexColor("#FEF2F2")), (q3_title, q3_text, colors.HexColor("#F8FAFC")), (q4_title, q4_text, colors.HexColor("#FFFBEB")), (q5_title, q5_text, colors.HexColor("#F8FAFC"))]:
        border_c = colors.HexColor("#FCD34D") if col == colors.HexColor("#FFFBEB") else (colors.HexColor("#FCA5A5") if col == colors.HexColor("#FEF2F2") else colors.HexColor("#CBD5E1"))
        t_q = Table([[Paragraph(f"<b>{q_t}</b>", label_amber if col == colors.HexColor("#FFFBEB") else (label_rose if col == colors.HexColor("#FEF2F2") else label_blue))], [Paragraph(q_b, script_quote)]], colWidths=[540])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), col),
            ('BOX', (0,0), (-1,-1), 1, border_c),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_q)
        story.append(Spacer(1, 2))

    # =========================================================================
    # PAGE 3: STATUTORY FORENSICS, SHARE RETENTION, PAYMENT STRUCTURE & VERIFY
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: STATUTORY FORENSICS &amp; TRUST SAFEGUARDS (PART 2 &bull; COMPLIANCE &amp; RETENTION)</b>", h1_style))
    story.append(Spacer(1, 2.5))

    if lang == "EN":
        q6_title = "QUESTION 6: \"My Demat account is active and has not moved to IEPF. Why is my folio listed?\""
        q6_text = (
            f"<i>\"You are 100% correct! A Demat account is held with your Depository Participant and <b>never moves to IEPF</b>.<br/>"
            f"Under Section 124(6) of the Companies Act, when dividends on a specific company (Astral) fail to reach your bank for 7 consecutive years, the company is legally required to execute a corporate action debit transferring <b>only the specific Astral shares</b> to the IEPF Authority Demat account.<br/>"
            f"Your active Demat account is the <b>best possible news</b>: because you have an active Demat, regularizing your KYC (Form ISR-1/2) with Bigshare Services <b>halts the transfer immediately</b>, protects your shares, and releases all accumulated cash dividends directly to your linked bank!\"</i>"
        )
        q7_title = "QUESTION 7: \"Can I keep my shares in my Demat without selling them? Can we de-list from IEPF?\""
        q7_text = (
            f"<i>\"<b>Yes, 100%! You do not have to sell a single share.</b> Under the <b>proviso to Section 124(6) of the Companies Act, 2013</b>, if a shareholder regularizes KYC and claims even <b>one single unpaid dividend</b>, the statutory 7-year clock is legally reset to ZERO.<br/>"
            f"Astral Limited immediately de-lists your folio from the IEPF transfer schedule. Your <b>{current_shares:,} shares remain 100% untouched in your Demat account</b>, continuing to compound and earn future dividends and bonus shares undisturbed.\"</i>"
        )
        q8_title = "QUESTION 8: \"If I keep my shares and don't sell them, how do you get paid?\""
        q8_text = (
            f"<i>\"Our fee structure is completely aligned with your financial safety:<br/>"
            f"1. <b>Paid from Cash Dividend Arrears:</b> Your folio has accumulated <b>Rs. {unclaimed_div:,.2f}</b> in unpaid cash dividends. When Bigshare releases this cash directly into your bank, our advisory fee can be settled from these newly recovered funds.<br/>"
            f"2. <b>Direct Consulting Invoice:</b> If the cash dividend does not cover the full fee, we raise a formal consulting invoice payable via NEFT/Cheque strictly <b>AFTER</b> you receive written confirmation from Bigshare that your folio is de-listed and your shares are safe. You pay Rs. 0 advance.\"</i>"
        )
        q9_title = "QUESTION 9: \"Where can I independently verify my shares and listing?\""
        q9_text = (
            f"<i>\"You do not have to take our word for it. You can independently verify your shares in 3 official places:<br/>"
            f"1. <b>Astral Limited Official Portal (astralltd.com):</b> Investor Relations &rarr; Investor Services &rarr; 'Unpaid Dividend &amp; IEPF Transfer Schedule' lists your Folio <font face='Courier'><b>{client['folio_id']}</b></font>.<br/>"
            f"2. <b>Registrar Bigshare Services (bigshareonline.com):</b> Investor service desk for Astral Limited under ISIN INE006I01046.<br/>"
            f"3. <b>Ministry of Corporate Affairs Portal (iepf.gov.in):</b> 'Search Unclaimed / Unpaid Amounts' under company 'Astral Limited'.\"</i>"
        )
        q10_title = "QUESTION 10: \"Why should we trust you with our KYC documents?\""
        q10_text = (
            f"<i>\"Entrusting KYC is a serious matter. Our practice operates on 5 unbreakable fiduciary safeguards:<br/>"
            f"1. <b>Zero Financial Risk:</b> Rs. 0 advance fee. Our {fee_pct}% fee is payable strictly AFTER shares and cash are in your Demat and bank.<br/>"
            f"2. <b>Direct Demat Credit:</b> We never touch client funds. Central Government / RTA credits 100% directly to your accounts.<br/>"
            f"3. <b>Standard SEBI Forms Only:</b> We collect only Form ISR-1/ISR-2. We never ask for passwords, OTPs, or blank cheques.<br/>"
            f"4. <b>Masked KYC Security:</b> You provide masked Aadhaar (first 8 digits hidden) and cheque crossed 'FOR ASTRAL KYC ONLY'.<br/>"
            f"5. <b>Stamped Legal Agreement:</b> We execute an official Rs. 100 stamp paper agreement with full SBI bank details protecting you.\"</i>"
        )
    elif lang == "TN":
        q6_title = "QUESTION 6: \"Ennoda Demat account active-ah dhaan irukku, idhu IEPF-ku pola-ye? Folio yen list aachu?\""
        q6_text = (
            f"<i>\"Neenga solradhu 100% sari sir! Demat account eppodhume IEPF-ku pogaadhu. Andha account ungaloda Depository Participant kitta ungaloda sontha account-ah dhaan irukkum.<br/>"
            f"Companies Act Section 124(6) padi, 7 years continuous-ah dividend uncashed-ah irundha, Astral company andha specific shares-a mattum corporate action valiyaaga IEPF account-ku transfer panna schedule ready pannum.<br/>"
            f"Ungaloda Demat account active-ah irukkaradhu romba nalla vishayam: Bigshare Services kitta Form ISR-1/ISR-2 regularise panninaal, <b>transfer udane stop aagi unga shares safe aagidum</b>, cash dividend-um direct-ah bank-ku release aagidum!\"</i>"
        )
        q7_title = "QUESTION 7: \"Ennoda shares-a vikkaama Demat-laye safe-ah vechuka mudiyuma? IEPF list-lendhu neekkalaama?\""
        q7_text = (
            f"<i>\"<b>Kandippa sir, 100%! Neenga oru share kooda vikka thevaiye illa.</b> Companies Act Section 124(6) statutory proviso padi, oru shareholder KYC update panni oru single unpaid dividend claim panninaal kooda, 7-year clock zero-ku reset aagidum.<br/>"
            f"Astral company ungaloda folio-vai IEPF transfer schedule-lendhu permanently de-list pannidum. Ungaloda <b>{current_shares:,} shares unga Demat-laye safe-ah retain aagum</b>, future bonus &amp; compounding uninterrupted-ah continue aagum.\"</i>"
        )
        q8_title = "QUESTION 8: \"Shares-a naan vikkala-na, ungalukku advisory fee eppadi pay aagum?\""
        q8_text = (
            f"<i>\"Engaloda fee payment romba transparent:<br/>"
            f"1. <b>Cash Dividend Arrears Moolam:</b> Unga folio-la shares mattum illaama, <b>Rs. {unclaimed_div:,.2f}</b> uncashed cash dividend irukku. Idhu unga bank account-ku direct-ah credit aagumbodhu, indha panathilendhe engaloda fee settle pannalaam.<br/>"
            f"2. <b>Post-Confirmation Invoice:</b> Bigshare kitta irundhu unga shares de-list aagi safe-aagirukku endra written confirmation vandhadhukku apram dhaan formal invoice raise panrom. Advance fee <b>Rs. 0</b> dhaan.\"</i>"
        )
        q9_title = "QUESTION 9: \"Ennoda shares matrum exact listing-ai naan enga direct-ah paarkka mudiyum?\""
        q9_text = (
            f"<i>\"Neenga engala mattum namba thevaiye illa sir. 3 official direct sources-la verify pannalaam:<br/>"
            f"1. <b>Astral Limited Official Portal (astralltd.com):</b> 'Investor Relations &rarr; Investor Services &rarr; Unclaimed Dividend &amp; IEPF Schedule'-la unga Folio <font face='Courier'><b>{client['folio_id']}</b></font> irukkum.<br/>"
            f"2. <b>Bigshare Services (bigshareonline.com):</b> Astral-oda official Registrar portal-la unga folio details verify pannalaam.<br/>"
            f"3. <b>MCA Government Portal (iepf.gov.in):</b> 'Search Unclaimed Amounts' tab-la Astral Limited select panni paarkkalaam.\"</i>"
        )
        q10_title = "QUESTION 10: \"Naanga ungalukku KYC documents thara yen nambanum?\""
        q10_text = (
            f"<i>\"Idhu romba mukkiyamaana kelvi sir. Engaloda practice 5 strict legal protections-la dhaan operate aagudhu:<br/>"
            f"1. <b>Zero Financial Risk:</b> Advance fee Rs. 0. Shares matrum panam ungaloda account-la vandha apram dhaan {fee_pct}% success fee.<br/>"
            f"2. <b>Direct Settlement:</b> Engalukku ungaloda shares-o panamo varaadhu&mdash;Central Government / RTA direct-ah unga Demat &amp; Bank-ku anupum.<br/>"
            f"3. <b>Standard SEBI Forms Mattum:</b> Form ISR-1 matrum ISR-2 mattum dhaan thevai. Password, PIN, OTP edhuvum kekka maatom.<br/>"
            f"4. <b>Masked KYC Security:</b> Aadhaar-la first 8 digits mask panni, cancelled cheque-la 'FOR KYC ONLY' nu ezhudhi kudunga.<br/>"
            f"5. <b>Stamped Legal Agreement:</b> Rs. 100 stamp paper-la formal agreement execute panni ungalukku full legal indemnity tharom.\"</i>"
        )
    else: # Hinglish
        q6_title = "QUESTION 6: \"Mera Demat account active hai, yeh IEPF mein nahi gaya hai. Toh folio kyun listed hai?\""
        q6_text = (
            f"<i>\"Aapka yeh observation 100% sahi hai sir! Demat account kabhi bhi IEPF mein nahi jata. Demat account aapka private account hota hai jo aapke broker ke paas active rehta hai.<br/>"
            f"Companies Act Section 124(6) ke mutabiq, jab 7 saal tak dividend uncashed rehta hai, toh company sirf us specific stock (Astral Limited) ke shares ko IEPF Authority ko transfer karne ka schedule banati hai.<br/>"
            f"Aapka Demat account active hona sabse acchi baat hai: Bigshare Services mein Form ISR-1/2 dekar KYC regularize karte hi <b>transfer turant ruk jata hai</b>, folio schedule se hat jata hai aur cash dividend bank mein release ho jata hai!\"</i>"
        )
        q7_title = "QUESTION 7: \"Kya main apne shares bina beche Demat mein safe rakh sakta hoon? Kya IEPF transfer ruk sakta hai?\""
        q7_text = (
            f"<i>\"<b>Haan bilkul 100%! Aapko ek bhi share bechne ki zaroorat nahi hai.</b> Companies Act Section 124(6) ke statutory proviso ke mutabiq, agar investor apna KYC regularize karke ek bhi unpaid dividend claim kar leta hai, toh 7 saal ka clock zero par reset ho jata hai.<br/>"
            f"Astral company aapke folio ko IEPF schedule se permanently de-list kar deti hai. Aapke <b>{current_shares:,} shares aapke Demat account mein hi safe rahenge</b> aur future compounding aur bonus ka faayda milta rahega.\"</i>"
        )
        q8_title = "QUESTION 8: \"Agar main shares nahi bechta, toh aapko fees kaise pay hogi?\""
        q8_text = (
            f"<i>\"Humara payment process 100% transparent aur client-friendly hai:<br/>"
            f"1. <b>Unpaid Cash Dividends Se Payment:</b> Shares ke saath-saath aapke folio mein <b>Rs. {unclaimed_div:,.2f}</b> ka unpaid cash dividend jama hai. Jab yeh cash dividend direct aapke bank account mein credit ho jata hai, tab aap usi recovered amount se humari advisory fee pay kar sakte hain.<br/>"
            f"2. <b>Post-Success Consulting Invoice:</b> Baki advisory fee ke liye hum official invoice raise karte hain jo tabhi payable hoti hai jab Bigshare Services se folio de-listing aur Demat security ka written confirmation aa jaye. Zero advance fee.\"</i>"
        )
        q9_title = "QUESTION 9: \"Main apne shares aur listing kahan independently verify kar sakta hoon?\""
        q9_text = (
            f"<i>\"Aapko hamari baat par aankh band karke vishwas karne ki zaroorat nahi hai. Aap khud 3 official jagah verify kar sakte hain:<br/>"
            f"1. <b>Astral Limited Official Portal (astralltd.com):</b> Investor Relations &rarr; Investor Services &rarr; 'Unpaid Dividend &amp; IEPF Transfer Schedule' par aapka Folio <font face='Courier'><b>{client['folio_id']}</b></font> listed hai.<br/>"
            f"2. <b>Registrar Bigshare Services (bigshareonline.com):</b> Astral ke official Registrar portal par investor tracking uplabdh hai.<br/>"
            f"3. <b>MCA Government Portal (iepf.gov.in):</b> 'Search Unclaimed / Unpaid Amounts' par Astral Limited search karke dekh sakte hain.\"</i>"
        )
        q10_title = "QUESTION 10: \"Hum aapko KYC documents dene par trust kyun karein?\""
        q10_text = (
            f"<i>\"Yeh bilkul laazmi sawaal hai sir. Hamari advisory 5 unbreakable legal safeguards par kaam karti hai:<br/>"
            f"1. <b>Zero Financial Risk:</b> Advance fee Rs. 0. Humara {fee_pct}% fee tabhi payable hai jab shares aur cash dividend aapke Demat aur bank account mein credit ho jayein.<br/>"
            f"2. <b>Direct Settlement:</b> Hum kisi bhi client ke paise ya shares ko touch nahi karte&mdash;sab kuch Central Govt / RTA se direct aapke account mein aata hai.<br/>"
            f"3. <b>Sirf SEBI Forms:</b> Hum sirf standard SEBI Form ISR-1 aur ISR-2 use karte hain. Hum koi password, OTP ya blank cheque nahi maangte.<br/>"
            f"4. <b>Masked KYC Protocol:</b> Aap masked Aadhaar (pehli 8 digits chhipa kar) aur cheque par 'FOR ASTRAL KYC ONLY' likh kar dete hain.<br/>"
            f"5. <b>Legal Stamped Agreement:</b> Hum Rs. 100 stamp paper par legally binding agreement execute karte hain full legal protection ke saath.\"</i>"
        )

    for q_t, q_b, col in [(q6_title, q6_text, colors.HexColor("#EFF6FF")), (q7_title, q7_text, colors.HexColor("#F0FDF4")), (q8_title, q8_text, colors.HexColor("#FFFBEB")), (q9_title, q9_text, colors.HexColor("#F8FAFC")), (q10_title, q10_text, colors.HexColor("#F5F3FF"))]:
        border_c = colors.HexColor("#3B82F6") if col == colors.HexColor("#EFF6FF") else (colors.HexColor("#10B981") if col == colors.HexColor("#F0FDF4") else (colors.HexColor("#FCD34D") if col == colors.HexColor("#FFFBEB") else (colors.HexColor("#C4B5FD") if col == colors.HexColor("#F5F3FF") else colors.HexColor("#CBD5E1"))))
        lbl_c = label_blue if col == colors.HexColor("#EFF6FF") else (label_emerald if col == colors.HexColor("#F0FDF4") else (label_amber if col == colors.HexColor("#FFFBEB") else (label_purple if col == colors.HexColor("#F5F3FF") else label_blue)))
        t_q = Table([[Paragraph(f"<b>{q_t}</b>", lbl_c)], [Paragraph(q_b, script_quote)]], colWidths=[540])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), col),
            ('BOX', (0,0), (-1,-1), 1, border_c),
            ('TOPPADDING', (0,0), (-1,-1), 1.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_q)
        story.append(Spacer(1, 2))

    # =========================================================================
    # PAGE 4: DOCUMENTS REQUIRED, SERVICE AGREEMENT, SUCCESS COMMISSION & CLOSING
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>PHASE 2: DOCUMENT REQUIREMENTS, SERVICE AGREEMENT &amp; CLOSING (PART 3)</b>", h1_style))
    story.append(Spacer(1, 2))

    if lang == "EN":
        q11_title = "QUESTION 11: \"What documents do you need from me to regularize KYC and stop the IEPF transfer?\""
        q11_text = (
            f"<i>\"We require only standard statutory identification documents to submit Form ISR-1 and ISR-2 to Bigshare Services:<br/>"
            f"1. <b>Client Master List (CML)</b> from your active Demat broker with DP stamp and signature.<br/>"
            f"2. Self-attested copy of <b>PAN Card and Masked Aadhaar Card</b> (first 8 digits masked).<br/>"
            f"3. Original <b>Cancelled Cheque leaf</b> carrying your name, linked to your active bank account.<br/>"
            f"4. <b>Form ISR-2 Bank Confirmation</b> attested by your bank manager (we provide the pre-filled format).\"</i>"
        )
        
        q12_title = "QUESTION 12: \"What is there in this Service Agreement? What are the key terms?\""
        q12_text = (
            f"<i>\"Our Service Agreement is a simple 4-pillar legal framework created entirely for your fiduciary protection:<br/>"
            f"1. <b>Statutory Scope:</b> It formally authorises our practice to liaise with Astral Limited and Registrar Bigshare Services to de-list your folio, update KYC, and claim uncashed dividends.<br/>"
            f"2. <b>Rs. 0 Advance / Zero Risk:</b> You pay <b>Rs. 0 upfront</b>. There is zero retainer, no out-of-pocket processing cost, and no hidden legal fee.<br/>"
            f"3. <b>Direct Asset Delivery:</b> 100% of recovered cash dividends and shares remain <b>directly in your own active Demat and Bank account</b>. Our {fee_pct}% advisory fee is payable strictly AFTER assets and confirmations are in your hands.<br/>"
            f"4. <b>Confidentiality:</b> All KYC and financial details are strictly confidential under fiduciary law and cannot be used for any other purpose.\"</i>"
        )

        q13_title = "QUESTION 13: \"Why should I pay a success fee when you operate from Tamil Nadu?\""
        q13_text = (
            f"<i>\"Under SEBI and MCA regulations, investor restitution is a centralized digital process coordinated between MCA (New Delhi) and Bigshare Services (Mumbai). Physical geography has zero bearing.<br/>"
            f"A single discrepancy in name spelling, bank attestation, or RTA verification results in official rejection. "
            f"Our <b>100% Contingent Model ({fee_pct}% fee, Rs. 0 Advance)</b> guarantees zero financial risk. You only compensate our practice after your shares and dividends are safely confirmed.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"{salutation}, I have audited your entire Astral holding and prepared your formal <b>Executive Recovery Dossier</b> along with the <b>Statutory Share Certificate &amp; Service Agreement</b>.<br/>"
            f"I have sent both documents to your WhatsApp and email. Kindly review with your family or Chartered Accountant, and let us submit Form ISR-1/2 to Bigshare to de-list your folio today.\"</i>"
        )
    elif lang == "TN":
        q11_title = "QUESTION 11: \"KYC regularise panni transfer thadukka ennoda kitta irundhu enna documents thevai?\""
        q11_text = (
            f"<i>\"Sir, Bigshare Services kitta Form ISR-1 matrum ISR-2 submit panna simple basic KYC documents mattum podhum:<br/>"
            f"1. Ungaloda active Demat account-oda <b>Client Master List (CML)</b> copy (broker seal-oda).<br/>"
            f"2. <b>PAN Card matrum Masked Aadhaar Card</b> self-attested copies.<br/>"
            f"3. Ungaloda peyar print aana <b>Original Cancelled Cheque leaf</b> ('FOR KYC ONLY' nu ezhudhalaam).<br/>"
            f"4. <b>Form ISR-2 Bank Confirmation</b> (unga bank branch manager seal &amp; sign-oda, format naangale pre-fill panni tharom).\"</i>"
        )
        
        q12_title = "QUESTION 12: \"Indha Service Agreement-la enna irukku? Key terms enna?\""
        q12_text = (
            f"<i>\"Sir, indha Service Agreement ungaloda 100% legal safety-kaga simple-ah 4 core terms-la create pannirukom:<br/>"
            f"1. <b>Legal Scope:</b> Astral Limited matrum Registrar Bigshare Services kitta ungalukkaga KYC update panni, folio de-list panna formal authorization.<br/>"
            f"2. <b>Zero Advance Fee:</b> Neenga <b>oru rupai kooda advance thara thevaiyilla (Rs. 0 Advance)</b>. Upfront fee, processing charge edhuvum kidayadhu.<br/>"
            f"3. <b>Direct Settlement &amp; Success Fee:</b> Ungaloda shares Demat-laye safe-ah irukkum, dividend direct-ah unga Bank-ku credit aagum. Assets safe aana apram dhaan {fee_pct}% fee.<br/>"
            f"4. <b>Confidentiality:</b> Ungaloda KYC documents claim processing-ku mattume use aagum, full statutory safety guarantee.\"</i>"
        )

        q13_title = "QUESTION 13: \"Neenga Tamil Nadu-la irukinga, naan ungalukku success fee yen tharanum?\""
        q13_text = (
            f"<i>\"Sir, share restitution enbadhu New Delhi Central Government MCA digital portal matrum Mumbai RTA Bigshare Services valiyaaga nadakkum federal process. Geographical distance oru thadaye illa.<br/>"
            f"Single document mistake irundhaalum RTA reject pannidum. Adhai legal precision-oda complete panna dhaan engaloda <b>100% Success-Only Model ({fee_pct}% fee, Rs. 0 Advance)</b>. Folio safe aagi confirmation vandha apram dhaan neenga fee thara poreenga.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"Sir, ungaloda complete share calculations and bonus history-a audit panni <b>Executive Recovery Dossier</b> and <b>Share Audit Certificate</b> ready panniten.<br/>"
            f"Indha rendaiyum ungaloda WhatsApp-ku ippo anupuren. Unga family-oda review pannitu sollunga sir, innaike Bigshare kitta Form ISR-1/2 initiate pannidalaam.\"</i>"
        )
    else: # Hinglish
        q11_title = "QUESTION 11: \"KYC regularize karne aur transfer rokne ke liye mujhse kya documents chahiye?\""
        q11_text = (
            f"<i>\"Sir, Bigshare Services mein Form ISR-1 aur ISR-2 file karne ke liye sirf standard statutory documents lagte hain:<br/>"
            f"1. Aapke active Demat broker se certified <b>Client Master List (CML)</b> copy (DP seal ke saath).<br/>"
            f"2. <b>PAN Card aur Masked Aadhaar Card</b> ki self-attested photocopy.<br/>"
            f"3. Name printed <b>Original Cancelled Cheque</b> (crossed 'FOR ASTRAL KYC ONLY').<br/>"
            f"4. <b>Form ISR-2 Bank Confirmation</b> (bank manager ke seal aur sign ke saath, format hum pre-fill karke denge).\"</i>"
        )

        q12_title = "QUESTION 12: \"Is Service Agreement mein kya likha hai? Iske main terms kya hain?\""
        q12_text = (
            f"<i>\"Sir, humara Service Agreement ekdam transparent aur simple 4 core pillars par bana hai jo poori tarah aapki safety ke liye hai:<br/>"
            f"1. <b>Legal Scope:</b> Yeh humein Astral Limited aur Registrar Bigshare Services ke saath aapke behalf par KYC update aur de-listing karne ki official authorization deta hai.<br/>"
            f"2. <b>Zero Advance (100% Risk-Free):</b> Aapko <b>ek bhi rupiya advance nahi dena hai (Rs. 0 Advance)</b>. Koi retainer ya processing fee nahi hai.<br/>"
            f"3. <b>Direct Asset Delivery:</b> Shares aapke Demat mein hi safe rahenge aur cash dividend <b>seedha aapke bank account mein aayega</b>. Humara {fee_pct}% fee tabhi payable hai jab confirmation mil jaye.<br/>"
            f"4. <b>Data Confidentiality:</b> Aapke KYC documents strictly is compliance ke liye hi use hote hain under complete fiduciary trust.\"</i>"
        )

        q13_title = "QUESTION 13: \"Aap Tamil Nadu se hain, main aapko success commission kyun doon?\""
        q13_text = (
            f"<i>\"Sir, share regularization New Delhi Central Government MCA portal aur Mumbai RTA Bigshare Services ke through hone wala centralized process hai. Distance se koi farq nahi padta.<br/>"
            f"Sabse important hai documentation error-free hona taaki RTA reject na kare. Humara model <b>100% Contingent Success-Only ({fee_pct}% fee, Rs. 0 Advance)</b> hai. Jab tak shares safe nahi hote, aapko ek rupiya nahi dena.\"</i>"
        )
        close_title = "PHASE 3: THE HIGH-CONVERSION CLOSING SCRIPT"
        close_text = (
            f"<i>\"Sir, aapki complete audit aur bonus details ke saath maine aapka personalized <b>Executive Recovery Dossier</b> aur <b>Share Certificate</b> prepare kar liya hai.<br/>"
            f"Main dono documents abhi aapke verified WhatsApp par bhej raha hoon. Aap review kijiye, aur hum turant Bigshare reconciliation start karte hain.\"</i>"
        )

    t_q11 = Table([[Paragraph(f"<b>{q11_title}</b>", label_amber)], [Paragraph(q11_text, script_quote)]], colWidths=[540])
    t_q11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q11)
    story.append(Spacer(1, 2))

    t_q12 = Table([[Paragraph(f"<b>{q12_title}</b>", label_purple)], [Paragraph(q12_text, script_quote)]], colWidths=[540])
    t_q12.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F3FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C4B5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q12)
    story.append(Spacer(1, 2))

    t_q13 = Table([[Paragraph(f"<b>{q13_title}</b>", label_blue)], [Paragraph(q13_text, script_quote)]], colWidths=[540])
    t_q13.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q13)
    story.append(Spacer(1, 2))

    t_close = Table([[Paragraph(f"<b>{close_title}</b>", label_emerald)], [Paragraph(close_text, script_quote)]], colWidths=[540])
    t_close.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
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

    # Read from uploads/customers.db if exists, fallback to customers.db
    target_db = db_path if os.path.exists(db_path) else db_root_path
    conn = sqlite3.connect(target_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, name, folio_id, address, est_folio, my_est_value, pdf3_path, pdf4_path FROM customers ORDER BY id')
    db_rows = {r['id']: dict(r) for r in c.fetchall()}
    conn.close()

    print(f"Regenerating all {len(clients)} Client Playbooks with Updated Statutory Pre-Transfer Protocol (EN, TN, HI)...")

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
        print(f"WARNING: Page count anomalies found ({len(bad_pages)}): {bad_pages[:5]}")
    else:
        print(f"SUCCESS: All {len(page_counts)} playbooks are EXACTLY 4 pages!")

    if address_leaks:
        print(f"WARNING: Address leaks found: {address_leaks}")
    else:
        print("SUCCESS: Zero address leaks across all playbooks!")

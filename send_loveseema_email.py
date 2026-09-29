#!/usr/bin/env python3
"""
send_loveseema_email.py
-----------------------
Dispatches the formal Statutory Restitution Notice & Audit Dossier email
with PDF attachment to CA Loveseema Kukreja (ca.loveseema@gmail.com).
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "uploads", "CA_Loveseema_Kukreja_IEPF_Transfer_Notice_and_Recovery_Guide.pdf")

# SMTP Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = "amdasrarbasha@gmail.com"
SENDER_PASSWORD = "zenqaefujramczmo"

RECIPIENT_EMAIL = "ca.loveseema@gmail.com"
SUBJECT = "Statutory Compliance Notice: Restitution of Transferred Astral Limited Equity (32,000 Shares / ₹4.56 Cr) | Folio: IN30296010013727"

def build_plain_text():
    return """Respected CA Loveseema Kukreja ma'am,

Subject: Formal Compliance Audit Notice regarding statutory debit and transfer of Astral Limited equity holdings to the IEPF Authority under Section 124(6) of the Companies Act, 2013.

I am writing to bring an urgent corporate action matter regarding your long-term equity investment in Astral Limited to your professional attention.

Following a statutory forensic audit of Astral Limited's regulatory gazette filings, we have identified that your registered holding has matured past the 7-year unpaid dividend threshold and was statutorily transferred to the Central Government IEPF Authority Demat Account (Ministry of Corporate Affairs, New Delhi).

--------------------------------------------------------------------------------
1. AUDITED PORTFOLIO SUMMARY (CERTIFIED MCA RECORD)
--------------------------------------------------------------------------------
• Target Company: Astral Limited (CIN: L25200GJ1996PLC029134 | ISIN: INE006I01046)
• Registered Folio / Client ID: IN30296010013727
• Registered Address: G-707, Rashmi Apartments, Harsh Vihar, Pitampura, Delhi - 110034
• Total Equity Shares: 32,000 Equity Shares (expanded via 1:4 and 1:3 corporate bonus issues)
• Current Market Valuation (@ ₹1,425): ₹4,56,00,000.00 (~₹4.56 Crores)
• Accrued Cash Dividends: ₹9,586.16 (Initial transfer executed on 25-Sep-2025, Page 18)
• Current Custody: IEPF Authority Demat Account (Central Government)

--------------------------------------------------------------------------------
2. THE ADMINISTRATIVE FREEZE & INACTION RISK
--------------------------------------------------------------------------------
As a fellow finance professional and Chartered Accountant, you are well aware that the Central Government acts strictly as a statutory custodian under Section 125(3). The government will NEVER automatically release or credit shares back into your Demat account.

Without timely, error-free intervention:
1. The 80%+ Rejection Trap: According to MCA annual data, over 80% of self-filed IEPF claims get stuck in bureaucratic deadlock or receive formal 'Deficiency Memos' from Registrar Bigshare Services due to legacy signature variations and SEBI Form ISR-1/2 attestation technicalities.
2. Permanent Administrative Lock-in: Unresolved claims remain frozen in government custody for years. Astral Limited headquarters is legally prohibited from releasing these assets across the counter.

--------------------------------------------------------------------------------
3. INDEPENDENT VERIFICATION (CHECK IN 2 MINUTES)
--------------------------------------------------------------------------------
You do not have to rely solely on our advisory communication. You can verify your statutory transfer directly across official portals:
1. MCA IEPF Authority Portal: https://www.iepf.gov.in -> Services -> Search Unclaimed / Transferred Amounts (Search: Astral Limited | Folio: IN30296010013727).
2. Astral Limited Official Investor Desk: https://www.astralltd.com/investor_relations/key-financial-figures/ -> Gazette File: ASTRAL_UNPAID_DIVIDEND_2025-26.pdf (Pages 18, 23 & 30).
3. Registrar (Bigshare Services Mumbai): Official Investor Desk at 022-62638200 / investor@bigshareonline.com.

--------------------------------------------------------------------------------
4. OUR 100% RISK-FREE FIDUCIARY MANDATE
--------------------------------------------------------------------------------
Our corporate practice specializes exclusively in executing Section 125(3) IEPF-5 restitutions for high-net-worth individuals, directors, and professionals pan-India:
• ₹0 Advance Fee (Zero Financial Risk): We do not charge a single rupee upfront. Our contingent success fee (8%) is payable strictly AFTER your 32,000 shares are visibly credited in your active Demat account.
• Direct Government Settlement: The Central Government executes a direct Corporate Action transfer into your own Demat account, and credits cash dividends directly to your bank account via PFMS/DBT. We never touch client funds.
• Strict Privacy Protocol: We require only Masked Aadhaar (first 8 digits hidden) and a cheque crossed "FOR ASTRAL IEPF KYC ONLY". We never request passwords, Demat credentials, or OTPs.

--------------------------------------------------------------------------------
NEXT STEPS
--------------------------------------------------------------------------------
Please find attached our complete 3-Page Statutory Restitution Notice & Holding Audit (CA_Loveseema_Kukreja_IEPF_Transfer_Notice_and_Recovery_Guide.pdf), including high-resolution official gazette screenshots and the complete step-by-step reclamation roadmap.

Could we schedule a brief 5-minute introductory call today at your convenience to discuss filing your e-Form IEPF-5?

Respectfully yours,

MD ASRAR BASHA A
Practice Head — Corporate IEPF Asset Restitution
Phone / WhatsApp: +91 7358882822
Email: amdasrarbasha@gmail.com
Live Practice Portal: https://customer-vault.onrender.com
"""

def build_html():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a202c; max-width: 680px; margin: 0 auto; padding: 20px; }
  .header-box { background: #0f172a; color: #ffffff; padding: 20px 24px; border-radius: 8px; margin-bottom: 24px; }
  .header-box h2 { margin: 0 0 6px 0; font-size: 19px; letter-spacing: 0.5px; color: #f8fafc; }
  .header-box p { margin: 0; font-size: 13px; color: #94a3b8; }
  .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; margin-bottom: 20px; }
  .stat-grid { width: 100%; border-collapse: collapse; margin-top: 10px; }
  .stat-grid td { padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
  .stat-grid td.label { font-weight: 600; color: #475569; width: 38%; }
  .stat-grid td.val { color: #0f172a; font-weight: 700; }
  .stat-grid td.highlight { color: #0284c7; font-weight: 800; font-size: 15px; }
  .section-title { font-size: 16px; font-weight: 700; color: #0f172a; margin: 24px 0 10px 0; border-left: 4px solid #0284c7; padding-left: 10px; }
  .bullet-list { margin: 0; padding-left: 20px; }
  .bullet-list li { margin-bottom: 8px; font-size: 14px; }
  .alert-box { background: #fffbeb; border-left: 4px solid #d97706; padding: 14px 16px; border-radius: 4px; margin: 18px 0; font-size: 13.5px; color: #92400e; }
  .badge { background: #dbeafe; color: #1e40af; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
  .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #e2e8f0; font-size: 13.5px; color: #475569; }
</style>
</head>
<body>

<div class="header-box">
  <h2>STATUTORY ASSET RESTITUTION NOTICE</h2>
  <p>Companies Act, 2013 | Section 124(6) & Section 125(3) Audit</p>
</div>

<p>Respected <strong>CA Loveseema Kukreja ma'am</strong>,</p>

<p><strong>Subject: Formal Compliance Audit Notice regarding statutory debit and transfer of Astral Limited equity holdings to the IEPF Authority under Section 124(6) of the Companies Act, 2013.</strong></p>

<p>I am writing to bring an urgent corporate action matter regarding your long-term equity investment in <strong>Astral Limited</strong> to your professional attention.</p>

<p>Following a statutory forensic audit of Astral Limited's regulatory gazette filings, we have identified that your registered holding has matured past the 7-year unpaid dividend threshold and was <strong>statutorily transferred to the Central Government IEPF Authority Demat Account (Ministry of Corporate Affairs, New Delhi)</strong>.</p>

<div class="section-title">1. Audited Portfolio Summary (Certified MCA Record)</div>
<div class="card">
  <table class="stat-grid">
    <tr>
      <td class="label">Target Company</td>
      <td class="val">Astral Limited (CIN: L25200GJ1996PLC029134)</td>
    </tr>
    <tr>
      <td class="label">Registered Folio / Client ID</td>
      <td class="val"><code>IN30296010013727</code></td>
    </tr>
    <tr>
      <td class="label">Registered Address</td>
      <td class="val">G-707, Rashmi Apartments, Harsh Vihar, Pitampura, Delhi - 110034</td>
    </tr>
    <tr>
      <td class="label">Total Equity Shares</td>
      <td class="highlight">32,000 Equity Shares <span class="badge">Expanded via 1:4 & 1:3 Bonus</span></td>
    </tr>
    <tr>
      <td class="label">Current Market Valuation (@ ₹1,425)</td>
      <td class="highlight" style="color: #15803d;">₹4,56,00,000.00 (~₹4.56 Crores)</td>
    </tr>
    <tr>
      <td class="label">Accrued Cash Dividends</td>
      <td class="val">₹9,586.16 (Initial transfer executed 25-Sep-2025, Page 18)</td>
    </tr>
    <tr>
      <td class="label">Current Custody</td>
      <td class="val" style="color: #b91c1c;">IEPF Authority Demat Account (Central Government)</td>
    </tr>
  </table>
</div>

<div class="section-title">2. The Administrative Freeze & Inaction Risk</div>
<p>As a fellow finance professional and Chartered Accountant, you are well aware that the Central Government acts strictly as a statutory custodian under Section 125(3). <strong>The government will NEVER automatically release or credit shares back into your Demat account.</strong></p>

<div class="alert-box">
  <strong>Key Regulatory Hurdles:</strong><br>
  • <strong>The 80%+ Rejection Trap:</strong> According to MCA annual data, over 80% of self-filed IEPF claims get stuck in bureaucratic deadlock or receive formal <em>'Deficiency Memos'</em> from Registrar Bigshare Services due to legacy signature variations and SEBI Form ISR-1/2 attestation technicalities.<br>
  • <strong>Permanent Administrative Lock-in:</strong> Unresolved claims remain frozen in government custody for years. Astral Limited corporate office is legally prohibited from releasing these assets across the counter.
</div>

<div class="section-title">3. Independent Verification (Check in 2 Minutes)</div>
<p>You can independently verify your statutory transfer directly across official government portals:</p>
<ul class="bullet-list">
  <li><strong>MCA IEPF Authority Portal:</strong> <a href="https://www.iepf.gov.in">www.iepf.gov.in</a> &rarr; <em>Services</em> &rarr; <em>Search Unclaimed / Transferred Amounts</em> (Company: <strong>Astral Limited</strong> | Folio: <code>IN30296010013727</code>).</li>
  <li><strong>Astral Limited Official Investor Desk:</strong> <a href="https://www.astralltd.com/investor_relations/key-financial-figures/">Astral Investor Relations</a> &rarr; Gazette File: <code>ASTRAL_UNPAID_DIVIDEND_2025-26.pdf</code> (Pages 18, 23 & 30).</li>
  <li><strong>Registrar (Bigshare Services Mumbai):</strong> Official Investor Desk at <code>022-62638200</code> / <a href="mailto:investor@bigshareonline.com">investor@bigshareonline.com</a>.</li>
</ul>

<div class="section-title">4. Our 100% Risk-Free Fiduciary Mandate</div>
<p>Our corporate practice specializes exclusively in executing Section 125(3) IEPF-5 restitutions for high-net-worth individuals, directors, and professionals pan-India:</p>
<ul class="bullet-list">
  <li><strong>₹0 Advance Fee (Zero Financial Risk):</strong> We do not charge a single rupee upfront. Our contingent success fee (8%) is payable strictly <strong>AFTER</strong> your 32,000 shares are visibly credited in your active Demat account.</li>
  <li><strong>Direct Government Settlement:</strong> The Central Government executes a direct Corporate Action transfer into your own Demat account, and credits cash dividends directly to your bank account via PFMS/DBT. We never touch client funds.</li>
  <li><strong>Strict Privacy Protocol:</strong> We require only <strong>Masked Aadhaar</strong> (first 8 digits hidden) and a cheque crossed <em>"FOR ASTRAL IEPF KYC ONLY"</em>. We never request passwords, Demat credentials, or OTPs.</li>
</ul>

<div class="section-title">Next Steps</div>
<p>Please find attached our complete <strong>3-Page Statutory Restitution Notice & Holding Audit</strong> (<code>CA_Loveseema_Kukreja_IEPF_Transfer_Notice_and_Recovery_Guide.pdf</code>), including high-resolution official gazette screenshots and the complete step-by-step reclamation roadmap.</p>

<p>Could we schedule a brief 5-minute introductory call today at your convenience to discuss filing your <strong>e-Form IEPF-5</strong>?</p>

<div class="footer">
  <strong>Respectfully yours,</strong><br><br>
  <strong>MD ASRAR BASHA A</strong><br>
  Practice Head &mdash; Corporate IEPF Asset Restitution<br>
  📞 <strong>Phone / WhatsApp:</strong> +91 7358882822<br>
  ✉️ <strong>Email:</strong> amdasrarbasha@gmail.com<br>
  🌐 <strong>Live Practice Portal:</strong> <a href="https://customer-vault.onrender.com">https://customer-vault.onrender.com</a>
</div>

</body>
</html>"""

def send_email():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")
    
    print(f"[1/4] Preparing email for: {RECIPIENT_EMAIL}")
    print(f"      Subject: {SUBJECT}")
    print(f"      Attachment: {os.path.basename(PDF_PATH)} ({os.path.getsize(PDF_PATH)} bytes)")

    msg = MIMEMultipart("mixed")
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = SUBJECT

    # Alternative part for plain text and HTML
    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(build_plain_text(), "plain", "utf-8"))
    alt_part.attach(MIMEText(build_html(), "html", "utf-8"))
    msg.attach(alt_part)

    # Attach PDF
    with open(PDF_PATH, "rb") as f:
        pdf_attachment = MIMEApplication(f.read(), Name=os.path.basename(PDF_PATH))
        pdf_attachment["Content-Disposition"] = f'attachment; filename="{os.path.basename(PDF_PATH)}"'
        msg.attach(pdf_attachment)

    print(f"[2/4] Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT} via SSL...")
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    
    print("[3/4] Authenticating with Gmail SMTP...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    print(f"[4/4] Sending message to {RECIPIENT_EMAIL}...")
    server.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
    server.quit()
    
    print(">>> SUCCESS: Email has been dispatched successfully to CA Loveseema Kukreja!")

if __name__ == "__main__":
    send_email()

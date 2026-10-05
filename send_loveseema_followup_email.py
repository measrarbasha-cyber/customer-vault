#!/usr/bin/env python3
"""
send_loveseema_followup_email.py
---------------------------------
Sends follow-up email to CA Loveseema Kukreja with the 4-page official shares calculation
and gazette proof PDF attached.
Strictly zero occurrences of 'customervault'.
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
PDF_PATH = os.path.join(BASE_DIR, "uploads", "CA_Loveseema_Kukreja_Official_Shares_Calculation_and_Gazette_Proof.pdf")

# Verify PDF exists
if not os.path.exists(PDF_PATH):
    print(f"ERROR: PDF file not found at {PDF_PATH}")
    sys.exit(1)

# Verify no customervault in PDF or script
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()
    if b"customervault" in pdf_bytes.lower() or b"customer-vault" in pdf_bytes.lower():
        print("ERROR: 'customervault' found in PDF!")
        sys.exit(1)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = "amdasrarbasha@gmail.com"
SENDER_PASSWORD = "zenqaefujramczmo"
RECIPIENT_EMAIL = "ca.loveseema@gmail.com"
SUBJECT = "Follow-up: Official Shareholding Breakdown & Gazette Proof | Astral Ltd (Folio: IN30296010013727) - CA Loveseema Kukreja"

plain_text = """Respected CA Loveseema Kukreja ma'am,

I hope this email finds you well.

Following our previous correspondence, I am writing to check if you have had the opportunity to reconfirm and verify your holding records with your broker, and to understand the current status from your side.

To assist your independent review, we have compiled and attached the complete 4-page Official Shareholding Breakdown & Gazette Proof Dossier for your registered holding under Folio/Client ID IN30296010013727 (Astral Limited).

Key Highlights of the Attached Dossier:
1. Certified Share Calculation & Bonus Audit: Shows the chronological expansion of your base holding (14,400 shares) across the 2019 (1:4), 2021 (1:3), and 2023 (1:3) corporate bonus issues to a cumulative 32,000 Equity Shares, currently valued at approximately Rs. 4.56 Crores (@ CMP Rs. 1,425), plus unclaimed dividends.
2. Official MCA Gazette Extracts: Certified filings by Astral Limited submitted under IEPF Rules with third-party shareholder details masked for privacy, highlighting your exact transfer entries.
3. Statutory IEPF Suspense Ledger: Formal audit schedule of dividend warrants and transfer status under Section 124(6) of the Companies Act, 2013.

Once you are ready and have reviewed these records, please feel free to call or WhatsApp me directly at +91 7358882822 so that we can initiate the documentation and start the process to claim your accumulated dividends and shares directly back into your active Demat account.

Looking forward to hearing from you.

Warm regards,

MD ASRAR BASHA A
Principal Advisor – Shareholder Rights & IEPF Recovery
Legal & Statutory Claims Advisory
Phone / WhatsApp: +91 7358882822
Email: amdasrarbasha@gmail.com
Ranipet District & Chennai, Tamil Nadu - 632509
"""

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #1e293b; margin: 0; padding: 0; background-color: #f8fafc; }
  .container { max-width: 680px; margin: 24px auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
  .header { background: #0f172a; color: #ffffff; padding: 26px 32px; border-bottom: 3px solid #0284c7; }
  .header h2 { margin: 0 0 6px 0; font-size: 20px; font-weight: 600; color: #ffffff; letter-spacing: -0.3px; }
  .header p { margin: 0; font-size: 13px; color: #94a3b8; }
  .content { padding: 32px; }
  .callout-box { background: #f0fdf4; border-left: 4px solid #16a34a; padding: 18px 20px; margin: 22px 0; border-radius: 0 6px 6px 0; }
  .summary-table { width: 100%; border-collapse: collapse; margin: 18px 0; font-size: 13.5px; }
  .summary-table th { background: #0f172a; color: #ffffff; padding: 10px 14px; text-align: left; font-weight: 600; }
  .summary-table td { padding: 10px 14px; border-bottom: 1px solid #e2e8f0; }
  .summary-table td.label { font-weight: 600; color: #475569; width: 38%; background: #f8fafc; }
  .summary-table td.val { color: #0f172a; font-family: 'Consolas', monospace; font-weight: 500; }
  .pdf-box { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 16px 20px; margin: 22px 0; }
  .footer { background: #f8fafc; padding: 22px 32px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; line-height: 1.7; }
  .cta-btn { display: inline-block; background: #0284c7; color: #ffffff !important; font-weight: 600; text-decoration: none; padding: 10px 22px; border-radius: 6px; margin-top: 8px; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h2>IEPF Statutory Advisory Desk</h2>
    <p>Folio Status Follow-up & Official Shares Calculation | Astral Limited (Folio: IN30296010013727)</p>
  </div>
  
  <div class="content">
    <p>Respected <b>CA Loveseema Kukreja ma'am</b>,</p>
    
    <p>I hope this email finds you well.</p>
    
    <p>Following our previous correspondence, I wanted to follow up and check if you have had the opportunity to reconfirm and verify your holding records with your broker, and to understand the current status from your side.</p>
    
    <div class="pdf-box">
      <h4 style="margin: 0 0 8px 0; color: #1e40af; font-size: 15px;">📎 Attached Dossier: Official Shares Calculation & Gazette Proof</h4>
      <p style="margin: 0; font-size: 13.5px; color: #334155;">
        As requested by investors seeking clear documentary evidence, we have compiled and attached the complete <b>4-Page Official Proof PDF</b> for your registered holding under Folio/Client ID <code>IN30296010013727</code>.
      </p>
      <ul style="margin: 10px 0 0 0; padding-left: 20px; font-size: 13px; color: #334155;">
        <li><b>Page 1: Audited Share Calculation & Corporate Bonus Reconstruction:</b> Full chronological schedule tracing your base holding of 14,400 shares across the 2019 (1:4), 2021 (1:3), and 2023 (1:3) bonus issues into <b>32,000 Certified Equity Shares</b> (~<b>₹4.56 Crores</b>).</li>
        <li><b>Pages 2 & 3: Certified Astral Limited MCA Gazette Extracts:</b> Official statutory filings submitted under IEPF Rules with third-party shareholder details masked for privacy, clearly highlighting your entries.</li>
        <li><b>Page 4: Statutory IEPF Custody & Entitlement Schedule:</b> Complete schedule of unclaimed dividend cycles and government escrow transfer details.</li>
      </ul>
    </div>

    <table class="summary-table">
      <tr>
        <th colspan="2">Certified Portfolio Summary on File</th>
      </tr>
      <tr>
        <td class="label">Investor Name</td>
        <td class="val"><b>LOVESEEMA KUKREJA</b></td>
      </tr>
      <tr>
        <td class="label">Demat / Client ID</td>
        <td class="val"><b>IN30296010013727</b> (DP ID: IN302960)</td>
      </tr>
      <tr>
        <td class="label">Registered Address</td>
        <td class="val">G-707, Rashmi Apartments, Harsh Vihar, Pitampura, Delhi - 110034</td>
      </tr>
      <tr>
        <td class="label">Total Certified Equity</td>
        <td class="val"><b>32,000 Shares</b> (Base: 14,400 + Bonus: 17,600)</td>
      </tr>
      <tr>
        <td class="label">Current Market Valuation</td>
        <td class="val"><b style="color: #16a34a;">₹4,56,00,000.00 (~₹4.56 Crores)</b> @ CMP ₹1,425</td>
      </tr>
      <tr>
        <td class="label">Unclaimed Dividend Accruals</td>
        <td class="val"><b>₹9,586.16</b> across 7 statutory warrant tranches</td>
      </tr>
    </table>

    <div class="callout-box">
      <h4 style="margin: 0 0 8px 0; color: #166534; font-size: 15px;">Next Steps to Start the Recovery</h4>
      <p style="margin: 0; font-size: 13.5px; color: #1e293b;">
        Whenever you are ready and have reviewed these records, please feel free to call or WhatsApp me so that we can initiate the necessary documentation and begin the process to claim your dividends and 32,000 Astral shares directly back into your active Demat account.
      </p>
    </div>

    <p style="font-size: 14px; margin-top: 24px;">Looking forward to hearing from you at your earliest convenience.</p>
  </div>
  
  <div class="footer">
    <b style="color: #0f172a; font-size: 14px;">MD ASRAR BASHA A</b><br>
    Principal Advisor – Shareholder Rights & IEPF Recovery<br>
    Legal & Statutory Claims Advisory<br>
    📞 <b>Phone / WhatsApp:</b> +91 7358882822 | ✉️ <b>Email:</b> amdasrarbasha@gmail.com<br>
    📍 Ranipet District & Chennai, Tamil Nadu - 632509
  </div>
</div>
</body>
</html>
"""

# Verify no customervault in email text or html
assert "customervault" not in plain_text.lower(), "Found customervault in plain text"
assert "customervault" not in html_content.lower(), "Found customervault in html"
assert "customer-vault" not in plain_text.lower(), "Found customer-vault in plain text"
assert "customer-vault" not in html_content.lower(), "Found customer-vault in html"

print("All safety checks passed! Constructing message...")

msg = MIMEMultipart("mixed")
msg["Subject"] = SUBJECT
msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
msg["To"] = RECIPIENT_EMAIL

# Body container
msg_body = MIMEMultipart("alternative")
msg_body.attach(MIMEText(plain_text, "plain", "utf-8"))
msg_body.attach(MIMEText(html_content, "html", "utf-8"))
msg.attach(msg_body)

# Attachment
with open(PDF_PATH, "rb") as f:
    pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
    pdf_attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename="CA_Loveseema_Kukreja_Official_Shares_Calculation_and_Gazette_Proof.pdf"
    )
    msg.attach(pdf_attachment)

print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} via SSL...")
try:
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
    print(f"SUCCESS: Follow-up email with 4-page official proof PDF successfully sent to {RECIPIENT_EMAIL}!")
except Exception as e:
    print(f"ERROR: Failed to send email: {e}")
    sys.exit(1)

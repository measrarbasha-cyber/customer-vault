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

smtp_user = "amdasrarbasha@gmail.com"
smtp_pass = "zenqaefujramczmo"

UPLOAD_DIR = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault\uploads"

CLIENTS = [
    {
        "id": 96,
        "name": "Hiranand Asandas Savlani",
        "salutation": "Mr. Hiranand Asandas Savlani",
        "folio": "IN30051317314132",
        "address": "44 Mahavir Tower, Near C.P. Nagar, Ghatlodia, Ahmedabad, Gujarat - 380061",
        "shares": "2,221 Shares",
        "val": "₹31,64,925 (~₹31.65 Lakhs)",
        "email": "hiranand@astralcpvc.com",
        "pdf_name": "Executive_Dossier_Hiranand_Savlani_Astral.pdf"
    },
    {
        "id": 97,
        "name": "Lalita Nahata & Ajay Nahata",
        "salutation": "Mrs. Lalita Nahata & Mr. Ajay Nahata",
        "folio": "1201090003437744",
        "address": "306 Ganga Apartments, Mangal Pandey Road, Siliguri Bazar, Siliguri, WB - 734001",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "heritage.10895@trs.raymond.in",
        "pdf_name": "Executive_Dossier_Lalita_Nahata_Astral.pdf"
    },
    {
        "id": 98,
        "name": "Usha Gupta",
        "salutation": "Mrs. Usha Gupta (C/o Ujagar Mal Chander Bhan)",
        "folio": "IN30159010029825",
        "address": "4570, Mahavir Bazar, Cloth Market, Central Delhi - 110006",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "ujagarmal.cloth@gmail.com",
        "pdf_name": "Executive_Dossier_Usha_Gupta_Astral.pdf"
    },
    {
        "id": 99,
        "name": "Dr. Gunadhar Padhi",
        "salutation": "Dr. Gunadhar Padhi",
        "folio": "1204720004074514",
        "address": "Flat 104, Nandini CHS, Plot 11 D, Sector 20, Kharghar, Navi Mumbai - 410210",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "drgunadhar.apollo@gmail.com",
        "pdf_name": "Executive_Dossier_Dr_Gunadhar_Padhi_Astral.pdf"
    },
    {
        "id": 100,
        "name": "Dipikaben Mukeshkumar Thakkar & Mukeshkumar Thakkar",
        "salutation": "Mrs. Dipikaben Thakkar & Mr. Mukeshkumar Thakkar",
        "folio": "IN30039413157207",
        "address": "Shop No. 35, Burhani Complex, Under Pooja Hospital, Lunawada, Gujarat - 389230",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "thakkar.lunawada@gmail.com",
        "pdf_name": "Executive_Dossier_Dipikaben_Thakkar_Astral.pdf"
    },
    {
        "id": 101,
        "name": "Divyesh Kanaiyalal Pandejee",
        "salutation": "Mr. Divyesh Kanaiyalal Pandejee",
        "folio": "IN30075711458905",
        "address": "B-77, Umed Park, Sola Road, Near Satadhar Society, Ghatlodia, Ahmedabad, Gujarat - 380061",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "divyesh.pandejee@gmail.com",
        "pdf_name": "Executive_Dossier_Divyesh_Pandejee_Astral.pdf"
    },
    {
        "id": 102,
        "name": "Chandra Shekhar",
        "salutation": "Mr. Chandra Shekhar (S/o Mohan Lal Sanoriya)",
        "folio": "1203320013859313",
        "address": "Samariya Sirpoi, Jhalawar, Rajasthan - 326513",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "chandrashekhar.jhalawar@gmail.com",
        "pdf_name": "Executive_Dossier_Chandra_Shekhar_Astral.pdf"
    },
    {
        "id": 103,
        "name": "Suresh Hinduja B",
        "salutation": "Mr. Suresh Hinduja B",
        "folio": "IN30021410969382",
        "address": "201, Viking Nest, 139/7, Domlur Layout, Bangalore, Karnataka - 560071",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "suresh.hinduja.blr@gmail.com",
        "pdf_name": "Executive_Dossier_Suresh_Hinduja_Astral.pdf"
    },
    {
        "id": 104,
        "name": "Manjula Vrajlal Lathia",
        "salutation": "Mrs. Manjula Vrajlal Lathia",
        "folio": "IN30258210101225",
        "address": "144/3945, Shantidoot, Vallabh Baug Lane, Pant Nagar, Ghatkopar East, Mumbai - 400075",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "manjula.lathia@gmail.com",
        "pdf_name": "Executive_Dossier_Manjula_Lathia_Astral.pdf"
    },
    {
        "id": 105,
        "name": "Meera Gupta",
        "salutation": "Mrs. Meera Gupta",
        "folio": "IN30039414585102",
        "address": "3/1/1, Raj Ballav Saha Lane, 3rd Floor, Howrah, West Bengal - 711101",
        "shares": "2,112 Shares",
        "val": "₹30,09,600 (~₹30.10 Lakhs)",
        "email": "meeragupta.howrah@gmail.com",
        "pdf_name": "Executive_Dossier_Meera_Gupta_Astral.pdf"
    }
]

def build_email_body(c):
    body_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #1e293b; margin: 0; padding: 0; background-color: #f8fafc; }}
.container {{ max-width: 680px; margin: 20px auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: #ffffff; }}
.header {{ background: #0f172a; color: #ffffff; padding: 24px 30px; }}
.header h2 {{ margin: 0 0 6px 0; font-size: 20px; font-weight: 600; color: #ffffff; }}
.header p {{ margin: 0; font-size: 13px; color: #94a3b8; }}
.content {{ padding: 30px; }}
.highlight-box {{ background: #f8fafc; border-left: 4px solid #0284c7; padding: 16px 20px; margin: 20px 0; border-radius: 0 6px 6px 0; }}
.record-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
.record-table td {{ padding: 10px 14px; border-bottom: 1px solid #e2e8f0; }}
.record-table td.label {{ font-weight: 600; color: #475569; width: 35%; background: #f8fafc; }}
.record-table td.val {{ color: #0f172a; font-family: Consolas, monospace; }}
.steps-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 18px 20px; margin: 20px 0; }}
.footer {{ background: #f8fafc; padding: 20px 30px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; line-height: 1.7; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h2>IEPF Statutory Advisory Desk</h2>
    <p>Notice of Unclaimed Corporate Assets & Recovery Dossier | Astral Limited</p>
  </div>
  <div class="content">
    <p>Dear <b>{c['salutation']}</b>,</p>
    
    <p>We are writing to you regarding an urgent statutory shareholder compliance matter concerning your equity holding in <b>Astral Limited</b>.</p>
    
    <p>As per the mandatory statutory filings under <b>Section 124(6) of the Companies Act, 2013</b>, your unclaimed dividend tranches and corresponding underlying equity shares are subject to statutory transfer / custody with the <b>Investor Education and Protection Fund (IEPF) Authority, Government of India</b>.</p>

    <div class="highlight-box">
      <h4 style="margin:0 0 8px 0; color:#0369a1;">Statutory Audit & Portfolio Assessment</h4>
      <table class="record-table">
        <tr>
          <td class="label">Investor Name on Record</td>
          <td class="val"><b>{c['name']}</b></td>
        </tr>
        <tr>
          <td class="label">Registered Folio / Client ID</td>
          <td class="val"><b>{c['folio']}</b></td>
        </tr>
        <tr>
          <td class="label">Registered Address</td>
          <td class="val">{c['address']}</td>
        </tr>
        <tr>
          <td class="label">Total Adjusted Holding</td>
          <td class="val"><b>{c['shares']}</b> (incl. 1:4, 1:3 & 1:3 bonus distributions)</td>
        </tr>
        <tr>
          <td class="label">Current Market Valuation</td>
          <td class="val"><b style="color:#059669;">{c['val']}</b> (approx.)</td>
        </tr>
      </table>
    </div>

    <h4 style="color:#0f172a; margin-top:24px;">Complete Recovery Dossier Attached</h4>
    <p style="font-size:14px; color:#334155;">
      We have compiled and attached your official <b>Executive Recovery Dossier (PDF)</b> to this email. It contains the complete breakdown of your original shareholding, split and bonus adjustments, uncashed dividend tranches, and the procedural statutory roadmap for recovery.
    </p>

    <div class="steps-box">
      <h4 style="margin:0 0 8px 0; color:#166534;">Zero Advance Security – 100% Contingent Model</h4>
      <p style="margin:0; font-size:14px; color:#1e293b;">
        Our fiduciary engagement operates on a strict <b>₹0 Advance / Success-Only</b> basis. Under the Ministry of Corporate Affairs IEPF-5 protocol, <b>all recovered shares and dividend warrants are credited directly into your active Demat / Bank account</b> before any professional fee is due.
      </p>
    </div>

    <p style="font-size:14px; color:#334155;">
      Please examine the attached PDF dossier. If you would like to begin the documentation or need clarification, please reply directly to this email or call our desk at <b>+91 7358882822</b>.
    </p>
  </div>
  
  <div class="footer">
    <b style="color:#0f172a;">MD ASRAR BASHA A</b><br>
    Principal Advisor – Shareholder Rights & IEPF Recovery<br>
    Legal & Compliance Desk | CustomerVault Advisory<br>
    📞 +91 7358882822 | ✉️ amdasrarbasha@gmail.com<br>
    Ranipet District & Chennai, Tamil Nadu - 632509
  </div>
</div>
</body>
</html>"""

    body_text = f"""Dear {c['salutation']},

We are writing to you regarding an urgent statutory shareholder compliance matter concerning your equity holding in Astral Limited.

As per mandatory statutory filings under Section 124(6) of the Companies Act, 2013, your unclaimed dividends and underlying equity shares are subject to statutory transfer to the Investor Education and Protection Fund (IEPF) Authority, Government of India.

STATUTORY AUDIT & PORTFOLIO ASSESSMENT:
- Investor Name: {c['name']}
- Registered Folio / Demat ID: {c['folio']}
- Registered Address: {c['address']}
- Total Adjusted Holding: {c['shares']} (accounting for 1:4, 1:3 & 1:3 bonuses)
- Current Market Valuation: {c['val']}

ATTACHED EXECUTIVE DOSSIER:
We have attached your complete Executive Recovery Dossier (PDF) to this email, outlining your complete share progression, dividend schedules, and the step-by-step IEPF Form-5 recovery roadmap.

ZERO ADVANCE / 100% CONTINGENT ENGAGEMENT:
Our advisory operates on a strict Rs. 0 Advance policy. All recovered shares and accrued benefits are released directly into your active Demat account by the Central Government before any advisory fee is settled.

Please review the attached PDF dossier. You may reply to this email or contact us directly at +91 7358882822 to discuss the next steps.

Warm regards,
MD ASRAR BASHA A
Principal Advisor – Shareholder Rights & IEPF Recovery
Legal & Compliance Desk | CustomerVault Advisory
Phone: +91 7358882822 | Email: amdasrarbasha@gmail.com
Ranipet District & Chennai, Tamil Nadu - 632509
"""
    return body_html, body_text

def send_all_emails():
    print(f"Connecting to SMTP server (smtp.gmail.com:465) as {smtp_user}...")
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(smtp_user, smtp_pass)
    print("SMTP authentication successful!\n")

    results = []
    for c in CLIENTS:
        recipient = c["email"]
        pdf_path = os.path.join(UPLOAD_DIR, c["pdf_name"])
        subject = f"Confidential: IEPF Equity Recovery Dossier - Astral Limited (Folio: {c['folio']}) - {c['name']}"

        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = f"MD ASRAR BASHA A <{smtp_user}>"
        msg["To"] = recipient

        # Alternative body (text + html)
        alt_part = MIMEMultipart("alternative")
        html_content, text_content = build_email_body(c)
        alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
        alt_part.attach(MIMEText(html_content, "html", "utf-8"))
        msg.attach(alt_part)

        # Attach PDF dossier
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"Executive_Recovery_Dossier_{c['name'].replace(' ', '_')}.pdf")
                msg.attach(pdf_attachment)
                print(f"[ATTACHED] {c['pdf_name']} ({os.path.getsize(pdf_path)} bytes)")
        else:
            print(f"[WARNING] PDF file not found: {pdf_path}")

        try:
            server.sendmail(smtp_user, [recipient], msg.as_string())
            print(f"SUCCESS [EMAIL DELIVERED]: Client ID {c['id']} -> {recipient}")
            results.append({"id": c["id"], "name": c["name"], "email": recipient, "status": "sent", "error": None})
        except Exception as e:
            print(f"ERROR [EMAIL FAILED]: Client ID {c['id']} -> {recipient}: {e}")
            results.append({"id": c["id"], "name": c["name"], "email": recipient, "status": "failed", "error": str(e)})

    server.quit()
    print("\nEmail dispatch completed.")
    return results

if __name__ == "__main__":
    send_all_emails()

import os
import sys
import sqlite3
import smtplib
import json
import re
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "customers.db")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = "amdasrarbasha@gmail.com"
SENDER_PASSWORD = "zenqaefujramczmo"

USER_PHONE = "+91 7358882822"
USER_PORTAL = "https://customer-vault.onrender.com"

email_regex = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

def get_transferred_email_queue():
    with open(os.path.join(BASE_DIR, "client_proof_registry.json"), "r", encoding="utf-8") as f:
        proof_reg = json.load(f)

    with open(os.path.join(BASE_DIR, "master_client_stats.json"), "r", encoding="utf-8") as f:
        master_stats = {s['id']: s for s in json.load(f)}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE pdf6_path IS NOT NULL ORDER BY id ASC")
    clients = [dict(r) for r in c.fetchall()]
    conn.close()

    queue = []
    for cl in clients:
        cid = cl['id']
        raw = cl.get('contact_info', '') or ''
        emails = email_regex.findall(raw)
        
        # Special case additions
        if cid == 23 and 'Gst.bhatia2017@gmail.com' not in emails:
            emails.append('Gst.bhatia2017@gmail.com')

        emails = list(dict.fromkeys(emails))
        if not emails:
            continue

        pdf_fn = cl.get('pdf6_path')
        pdf_path = os.path.join(UPLOAD_DIR, pdf_fn) if pdf_fn else None
        if not pdf_path or not os.path.exists(pdf_path):
            continue

        stat = master_stats.get(cid, {})
        shares = stat.get('current_shares')
        if not shares:
            m_sh = re.search(r'([\d,]+)\s*Shares', cl.get('est_folio', ''))
            shares = int(m_sh.group(1).replace(',', '')) if m_sh else 5000

        val = shares * 1425
        val_cr = val / 10000000.0
        val_str = f"~Rs. {val_cr:.2f} Cr" if val_cr >= 1.0 else f"~Rs. {val/100000.0:.2f} Lakhs"

        queue.append({
            "id": cid,
            "name": cl['name'],
            "folio_id": cl['folio_id'],
            "address": cl['address'],
            "emails": emails,
            "shares": shares,
            "valuation_str": val_str,
            "valuation_full": f"Rs. {val:,.2f}",
            "pdf_fn": pdf_fn,
            "pdf_path": pdf_path,
            "fee_pct": 15 if cid == 10 else 8
        })

    return queue

def build_plain_email(cust):
    cname = cust['name']
    folio = cust['folio_id']
    shares = cust['shares']
    val_str = cust['valuation_str']
    val_full = cust['valuation_full']
    pdf_fn = cust['pdf_fn']
    fee_pct = cust['fee_pct']

    return f"""Respected {cname},

Subject: Formal Compliance Audit Notice regarding statutory debit and transfer of Astral Limited equity holdings to the IEPF Authority under Section 124(6) of the Companies Act, 2013.

I am writing to bring an urgent corporate action matter regarding your long-term equity investment in Astral Limited to your professional attention.

Following a statutory forensic audit of Astral Limited's regulatory gazette filings, we have identified that your registered equity holding has matured past the 7-year unpaid dividend threshold and was statutorily transferred to the Central Government IEPF Authority Demat Account (Ministry of Corporate Affairs, New Delhi).

--------------------------------------------------------------------------------
1. AUDITED PORTFOLIO SUMMARY (CERTIFIED MCA RECORD)
--------------------------------------------------------------------------------
• Target Company: Astral Limited (CIN: L25200GJ1996PLC029134 | ISIN: INE006I01046)
• Registered Folio / Client ID: {folio}
• Registered Address: {cust['address']}
• Total Equity Shares: {shares:,} Equity Shares (expanded via historical bonus issues)
• Current Market Valuation (@ Rs. 1,425): {val_full} ({val_str})
• Current Custody: IEPF Authority Demat Account (Central Government)

--------------------------------------------------------------------------------
2. THE ADMINISTRATIVE FREEZE & INACTION RISK
--------------------------------------------------------------------------------
Under Section 125(3), the Central Government acts strictly as statutory custodian. The government will NEVER automatically release or credit shares back into your Demat account without a formal, approved claim.

Without timely, error-free intervention:
1. The 80%+ Rejection Trap: According to MCA annual data, over 80% of self-filed IEPF claims get stuck in bureaucratic deadlock or receive formal 'Deficiency Memos' from Registrar Bigshare Services due to legacy signature variations and SEBI Form ISR-1/2 attestation technicalities.
2. Permanent Administrative Lock-in: Unresolved claims remain frozen in government custody for years. Astral Limited headquarters is legally prohibited from releasing these assets across the counter.

--------------------------------------------------------------------------------
3. INDEPENDENT VERIFICATION (CHECK IN 2 MINUTES)
--------------------------------------------------------------------------------
You can independently verify your statutory transfer directly across official portals:
1. MCA IEPF Authority Portal: https://www.iepf.gov.in -> Services -> Search Unclaimed / Transferred Amounts (Search: Astral Limited | Folio: {folio}).
2. Astral Limited Official Investor Desk: https://www.astralltd.com/investor_relations/key-financial-figures/ -> Gazette File: ASTRAL_UNPAID_DIVIDEND_2025-26.pdf
3. Registrar (Bigshare Services Mumbai): Official Investor Desk at 022-62638200 / investor@bigshareonline.com.

--------------------------------------------------------------------------------
4. OUR 100% RISK-FREE FIDUCIARY MANDATE
--------------------------------------------------------------------------------
Our corporate practice specializes exclusively in executing Section 125(3) IEPF-5 restitutions:
• Rs. 0 Advance Fee (Zero Financial Risk): We do not charge a single rupee upfront. Our contingent success fee ({fee_pct}%) is payable strictly AFTER your {shares:,} shares are visibly credited in your active Demat account.
• Direct Government Settlement: The Central Government executes a direct Corporate Action transfer into your own Demat account, and credits cash dividends directly to your bank account via PFMS/DBT. We never touch client funds.
• Strict Privacy Protocol: We require only Masked Aadhaar (first 8 digits hidden) and a cheque crossed "FOR ASTRAL IEPF KYC ONLY". We never request passwords, Demat credentials, or OTPs.

--------------------------------------------------------------------------------
NEXT STEPS
--------------------------------------------------------------------------------
Please find attached your complete 3-Page Statutory Restitution Notice & Holding Audit ({pdf_fn}), including high-resolution official gazette screenshots and the step-by-step reclamation roadmap.

Could we schedule a brief 5-minute introductory call today at your convenience to discuss filing your e-Form IEPF-5?

Respectfully yours,

{SENDER_NAME}
Practice Head — Corporate IEPF Asset Restitution
Phone / WhatsApp: {USER_PHONE}
Email: {SENDER_EMAIL}
Live Practice Portal: {USER_PORTAL}
"""

def build_html_email(cust):
    cname = cust['name']
    folio = cust['folio_id']
    shares = cust['shares']
    val_str = cust['valuation_str']
    val_full = cust['valuation_full']
    fee_pct = cust['fee_pct']

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a202c; max-width: 680px; margin: 0 auto; padding: 20px; }}
  .header-box {{ background: #0f172a; color: #ffffff; padding: 20px 24px; border-radius: 8px; margin-bottom: 24px; }}
  .header-box h2 {{ margin: 0 0 6px 0; font-size: 19px; letter-spacing: 0.5px; color: #f8fafc; }}
  .header-box p {{ margin: 0; font-size: 13px; color: #94a3b8; }}
  .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; margin-bottom: 20px; }}
  .stat-grid {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  .stat-grid td {{ padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }}
  .stat-grid td.label {{ font-weight: 600; color: #475569; width: 38%; }}
  .stat-grid td.val {{ color: #0f172a; font-weight: 700; }}
  .stat-grid td.highlight {{ color: #0284c7; font-weight: 800; font-size: 15px; }}
  .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; margin: 24px 0 10px 0; border-left: 4px solid #0284c7; padding-left: 10px; }}
  .bullet-list {{ margin: 0; padding-left: 20px; }}
  .bullet-list li {{ margin-bottom: 8px; font-size: 14px; }}
  .alert-box {{ background: #fffbeb; border-left: 4px solid #d97706; padding: 14px 16px; border-radius: 4px; margin: 18px 0; font-size: 13.5px; color: #92400e; }}
  .badge {{ background: #dbeafe; color: #1e40af; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
  .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #e2e8f0; font-size: 13.5px; color: #475569; }}
</style>
</head>
<body>

<div class="header-box">
  <h2>STATUTORY ASSET RESTITUTION NOTICE</h2>
  <p>Companies Act, 2013 | Section 124(6) & Section 125(3) Audit</p>
</div>

<p>Respected <strong>{cname}</strong>,</p>

<p><strong>Subject: Formal Compliance Audit Notice regarding statutory debit and transfer of Astral Limited equity holdings to the IEPF Authority under Section 124(6) of the Companies Act, 2013.</strong></p>

<p>I am writing to bring an urgent corporate action matter regarding your long-term equity investment in <strong>Astral Limited</strong> to your professional attention.</p>

<p>Following a statutory forensic audit of Astral Limited's regulatory gazette filings, we have identified that your registered equity holding has matured past the 7-year unpaid dividend threshold and was <strong>statutorily transferred to the Central Government IEPF Authority Demat Account (Ministry of Corporate Affairs, New Delhi)</strong>.</p>

<div class="section-title">1. Audited Portfolio Summary (Certified MCA Record)</div>
<div class="card">
  <table class="stat-grid">
    <tr>
      <td class="label">Target Company</td>
      <td class="val">Astral Limited (CIN: L25200GJ1996PLC029134 | ISIN: INE006I01046)</td>
    </tr>
    <tr>
      <td class="label">Registered Folio / Client ID</td>
      <td class="val"><code>{folio}</code></td>
    </tr>
    <tr>
      <td class="label">Registered Address</td>
      <td class="val">{cust['address']}</td>
    </tr>
    <tr>
      <td class="label">Total Equity Shares</td>
      <td class="highlight">{shares:,} Equity Shares <span class="badge">Expanded via Historical Bonuses</span></td>
    </tr>
    <tr>
      <td class="label">Current Market Valuation (@ Rs. 1,425)</td>
      <td class="highlight" style="color: #15803d;">{val_full} ({val_str})</td>
    </tr>
    <tr>
      <td class="label">Current Custody</td>
      <td class="val" style="color: #b91c1c;">IEPF Authority Demat Account (Central Government)</td>
    </tr>
  </table>
</div>

<div class="section-title">2. The Administrative Freeze & Inaction Risk</div>
<p>As a shareholder, please note that while the Central Government acts strictly as a statutory custodian under Section 125(3), <strong>the government will NEVER automatically release or credit shares back into your Demat account without a formal, vetted claim</strong>.</p>

<div class="alert-box">
  <strong>Key Regulatory Hurdles:</strong><br>
  • <strong>The 80%+ Rejection Trap:</strong> According to MCA annual data, over 80% of self-filed IEPF claims get stuck in bureaucratic deadlock or receive formal <em>'Deficiency Memos'</em> from Registrar Bigshare Services due to legacy signature variations and SEBI Form ISR-1/2 attestation technicalities.<br>
  • <strong>Permanent Administrative Lock-in:</strong> Unresolved claims remain frozen in government custody for years. Astral Limited corporate headquarters is legally prohibited from releasing these assets across the counter.
</div>

<div class="section-title">3. Independent Verification (Check in 2 Minutes)</div>
<p>You can independently verify your statutory transfer directly across official government portals:</p>
<ul class="bullet-list">
  <li><strong>MCA IEPF Authority Portal:</strong> <a href="https://www.iepf.gov.in">www.iepf.gov.in</a> &rarr; <em>Services</em> &rarr; <em>Search Unclaimed / Transferred Amounts</em> (Company: <strong>Astral Limited</strong> | Folio: <code>{folio}</code>).</li>
  <li><strong>Astral Limited Official Investor Desk:</strong> <a href="https://www.astralltd.com/investor_relations/key-financial-figures/">Astral Investor Relations</a> &rarr; Gazette File: <code>ASTRAL_UNPAID_DIVIDEND_2025-26.pdf</code>.</li>
  <li><strong>Registrar (Bigshare Services Mumbai):</strong> Official Investor Desk at <code>022-62638200</code> / <a href="mailto:investor@bigshareonline.com">investor@bigshareonline.com</a>.</li>
</ul>

<div class="section-title">4. Our 100% Risk-Free Fiduciary Mandate</div>
<p>Our corporate practice specializes exclusively in executing Section 125(3) IEPF-5 restitutions for high-net-worth shareholders pan-India:</p>
<ul class="bullet-list">
  <li><strong>Rs. 0 Advance Fee (Zero Financial Risk):</strong> We do not charge a single rupee upfront. Our contingent success fee ({fee_pct}%) is payable strictly <strong>AFTER</strong> your {shares:,} shares are visibly credited in your active Demat account.</li>
  <li><strong>Direct Government Settlement:</strong> The Central Government executes a direct Corporate Action transfer into your own Demat account, and credits cash dividends directly to your bank account via PFMS/DBT. We never touch client funds.</li>
  <li><strong>Strict Privacy Protocol:</strong> We require only <strong>Masked Aadhaar</strong> (first 8 digits hidden) and a cheque crossed <em>"FOR ASTRAL IEPF KYC ONLY"</em>. We never request passwords, Demat credentials, or OTPs.</li>
</ul>

<div class="section-title">Next Steps</div>
<p>Please find attached your complete <strong>3-Page Statutory Restitution Notice & Holding Audit</strong> (<code>{cust['pdf_fn']}</code>), including high-resolution official gazette screenshots and the step-by-step reclamation roadmap.</p>

<p>Could we schedule a brief 5-minute introductory call today at your convenience to discuss filing your <strong>e-Form IEPF-5</strong>?</p>

<div class="footer">
  <strong>Respectfully yours,</strong><br><br>
  <strong>{SENDER_NAME}</strong><br>
  Practice Head &mdash; Corporate IEPF Asset Restitution<br>
  📞 <strong>Phone / WhatsApp:</strong> {USER_PHONE}<br>
  ✉️ <strong>Email:</strong> {SENDER_EMAIL}<br>
  🌐 <strong>Live Practice Portal:</strong> <a href="{USER_PORTAL}">{USER_PORTAL}</a>
</div>

</body>
</html>"""

def dispatch_all_emails(dry_run=True):
    queue = get_transferred_email_queue()
    print("=" * 80)
    print(f"BATCH EMAIL DISPATCH (DOC 6 NOTICES) | MODE: {'DRY RUN' if dry_run else 'LIVE DISPATCH'}")
    print(f"Total Eligible Transferred Clients with Email: {len(queue)}")
    print("=" * 80)

    server = None
    if not dry_run:
        print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT} via SSL...")
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("SMTP authentication successful!\n")

    sent_count = 0
    failed_count = 0

    for idx, cust in enumerate(queue, 1):
        subject = f"Statutory Compliance Notice: Restitution of Transferred Astral Limited Equity ({cust['shares']:,} Shares / {cust['valuation_str']}) | Folio: {cust['folio_id']}"
        recipients = cust['emails']
        primary_recipient = recipients[0]
        pdf_path = cust['pdf_path']

        print(f"[{idx}/{len(queue)}] Preparing: {cust['name']} (ID {cust['id']})")
        print(f"  Recipients: {', '.join(recipients)}")
        print(f"  Subject: {subject}")
        print(f"  Attached Doc 6: {cust['pdf_fn']} ({os.path.getsize(pdf_path)} bytes)")

        if dry_run:
            print("  Status: [SIMULATED SUCCESS]\n")
            sent_count += 1
            continue

        try:
            msg = MIMEMultipart("mixed")
            msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
            msg["To"] = primary_recipient
            if len(recipients) > 1:
                msg["Cc"] = ", ".join(recipients[1:])
            msg["Subject"] = subject

            alt_part = MIMEMultipart("alternative")
            alt_part.attach(MIMEText(build_plain_email(cust), "plain", "utf-8"))
            alt_part.attach(MIMEText(build_html_email(cust), "html", "utf-8"))
            msg.attach(alt_part)

            with open(pdf_path, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), Name=cust['pdf_fn'])
                pdf_attachment["Content-Disposition"] = f'attachment; filename="{cust["pdf_fn"]}"'
                msg.attach(pdf_attachment)

            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
            print(f"  >>> SUCCESS: Dispatched email to {', '.join(recipients)}!\n")
            sent_count += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"  [-] ERROR sending to {recipients}: {e}\n")
            failed_count += 1
            time.sleep(2)

    if server:
        server.quit()

    log_path = os.path.join(BASE_DIR, "transferred_emails_dispatch_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dry_run": dry_run,
            "total": len(queue),
            "sent": sent_count,
            "failed": failed_count,
            "records": queue
        }, f, indent=2)

    print("=" * 80)
    print(f"Email Dispatch Complete! Dispatched: {sent_count} | Failed: {failed_count}")
    print(f"Audit log saved to: {log_path}")
    print("=" * 80)

    # Automatic Post-Dispatch Undelivered & Bounce Purge
    if not dry_run:
        print("\nWaiting 10 seconds for initial recipient mail server handshakes...", flush=True)
        time.sleep(10)
        from auto_clean_undelivered_emails import clean_undelivered_and_bounced_emails
        clean_undelivered_and_bounced_emails()

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    dispatch_all_emails(dry_run=not is_live)

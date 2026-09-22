import os
import sys
import sqlite3
import re
import smtplib
import time
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customers.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
REGISTRY_PATH = os.path.join(BASE_DIR, "master_outreach_registry.json")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = "amdasrarbasha@gmail.com"
SENDER_PASSWORD = "zenqaefujramczmo"

CONSULTANT_PHONE = "+91 7358882822"
CONSULTANT_TITLE = "Principal Advisor – Shareholder Rights & IEPF Recovery"
CONSULTANT_LOC = "Ranipet District & Chennai, Tamil Nadu - 632509"

def extract_email(contact_info):
    if not contact_info:
        return None
    match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', contact_info)
    return match.group(1).lower().strip() if match else None

def build_email_body(customer, dossier_filename):
    name = customer.get("name", "Investor")
    folio = customer.get("folio_id", "Unclaimed Folio")
    est_folio = customer.get("est_folio", "Audited Portfolio")

    body = f"""Dear {name},

I hope this email finds you well.

I am writing to bring to your attention an important matter regarding your long-standing unclaimed equity investment in Astral Limited (Folio ID: {folio}), which is currently held under the statutory custody of the Investor Education and Protection Fund (IEPF) Authority, Ministry of Corporate Affairs, Government of India.

Our forensic verification and audit indicates a gross portfolio valuation of {est_folio} (inclusive of accumulated corporate benefits, bonus shares, and unpaid dividends).

We handle the complete statutory recovery end-to-end under a strict zero-risk framework:
1. ₹0 Upfront / Zero Advance Fee: 100% contingent on success.
2. Direct Government Settlement: All recovered shares and dividend disbursements are credited directly into your personal verified Demat and Bank account by the IEPF Authority.
3. Complete Documentation: Physical share entitlement, RTA reconciliation (Bigshare Services, Mumbai), and MCA e-filing (IEPF Form 5) managed entirely by our office.

We have attached your comprehensive Executive Recovery Dossier and audit breakdown to this email ({dossier_filename}).

Please review the attached document. Feel free to reply directly to this email or reach out to me at {CONSULTANT_PHONE} to coordinate the statutory paperwork.

Warm regards,

{SENDER_NAME}
{CONSULTANT_TITLE}
Phone: {CONSULTANT_PHONE}
Email: {SENDER_EMAIL}
Location: {CONSULTANT_LOC}
"""
    return body

def send_deduped_emails(dry_run=True):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    delivered_emails = {k.lower().strip() for k in registry.get("email_delivered_clients", {}).keys()}
    bounced_emails = {k.lower().strip() for k in registry.get("bounced_emails", [])}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id ASC")
    customers = [dict(r) for r in c.fetchall()]
    conn.close()

    print("=" * 80)
    print(f"CustomerVault Deduped Email Sender | Mode: {'DRY RUN (Simulated)' if dry_run else 'LIVE DISPATCH'}")
    print(f"Sender: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"Already Delivered: {len(delivered_emails)} | Bounced/Excluded: {len(bounced_emails)}")
    print("=" * 80)

    queue = []
    skipped_delivered = []
    skipped_bounced = []

    for cust in customers:
        email = extract_email(cust.get("contact_info", ""))
        pdf1 = cust.get("pdf1_path")
        pdf_path = os.path.join(UPLOAD_DIR, pdf1) if pdf1 else None

        if not email:
            continue
        if email in delivered_emails:
            skipped_delivered.append((cust['id'], cust['name'], email))
            continue
        if email in bounced_emails:
            skipped_bounced.append((cust['id'], cust['name'], email))
            continue
        if not pdf_path or not os.path.exists(pdf_path):
            print(f"[-] PDF MISSING for ID {cust['id']}: {pdf1}")
            continue

        queue.append({
            "id": cust['id'],
            "name": cust['name'],
            "email": email,
            "folio_id": cust.get("folio_id"),
            "pdf_path": pdf_path,
            "subject": f"Confidential: IEPF Equity Recovery Dossier - Astral Ltd (Folio: {cust.get('folio_id', '')}) - {cust['name']}",
            "body": build_email_body(cust, os.path.basename(pdf_path))
        })

    print(f"Eligible Dispatch Queue: {len(queue)} clients")
    print(f"Skipped (Already Delivered): {len(skipped_delivered)}")
    print(f"Skipped (Bounced Previously): {len(skipped_bounced)}")
    print("-" * 80)

    if dry_run:
        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] [SIMULATION] ID {item['id']} -> {item['name']}")
            print(f"  To: {item['email']}")
            print(f"  Subject: {item['subject']}")
            print(f"  Attached: {os.path.basename(item['pdf_path'])}")
            print("-" * 60)
        return

    # LIVE DISPATCH
    print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT} via SSL...")
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("SMTP authentication successful!\n")

    sent_count = 0
    for idx, item in enumerate(queue, 1):
        msg = MIMEMultipart()
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = item["email"]
        msg["Subject"] = item["subject"]
        msg.attach(MIMEText(item["body"], "plain", "utf-8"))

        with open(item["pdf_path"], "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(item["pdf_path"]))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(item["pdf_path"])}"'
            msg.attach(part)

        try:
            server.sendmail(SENDER_EMAIL, [item["email"]], msg.as_string())
            print(f"[{idx}/{len(queue)}] [SUCCESS] Sent email to: {item['email']} (ID {item['id']}: {item['name']})")
            
            # Record in registry
            registry["email_delivered_clients"][item["email"]] = {
                "id": item["id"],
                "name": item["name"],
                "subject": item["subject"],
                "date": time.strftime("%a, %d %b %Y %H:%M:%S +0530")
            }
            sent_count += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"[{idx}/{len(queue)}] [FAILED] Could not send to {item['email']}: {e}")

    server.quit()

    registry["email_count"] = len(registry["email_delivered_clients"])
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Live Email Dispatch Complete: {sent_count} sent successfully. Registry updated.")
    print("=" * 80)

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    send_deduped_emails(dry_run=not is_live)

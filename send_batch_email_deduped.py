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
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(UPLOAD_DIR, "customers.db") if os.path.exists(os.path.join(UPLOAD_DIR, "customers.db")) else os.path.join(BASE_DIR, "customers.db")
AUDIT_PATH = os.path.join(BASE_DIR, "email_delivery_audit.json")
REGISTRY_PATH = os.path.join(BASE_DIR, "master_outreach_registry.json")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = "amdasrarbasha@gmail.com"
SENDER_PASSWORD = "zenqaefujramczmo"

CONSULTANT_PHONE = "+91 7358882822"
CONSULTANT_TITLE = "Principal Advisor – Shareholder Rights & IEPF Recovery Practice"
CONSULTANT_LOC = "Ranipet District & Chennai, Tamil Nadu - 632509 (Pan-India Advisory)"

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

I am writing to bring to your attention an urgent statutory compliance notice regarding your equity holding in Astral Limited (Folio ID: {folio}), which is officially listed on Astral Limited's statutory schedule for upcoming transfer to the Investor Education and Protection Fund (IEPF) Authority under Section 124(6) of the Companies Act, 2013.

Your folio is currently in the pre-transfer warning stage due to consecutive uncashed dividend tranches. Our forensic audit indicates a portfolio valuation of {est_folio} (inclusive of historical 1:4 and 1:3 bonus share expansions and accumulated cash dividends).

Under Section 124(6) proviso, regularizing your KYC records and claiming your uncashed dividend legally resets the statutory clock, permanently halts the IEPF transfer, and keeps your shares safe in your active Demat account without selling them.

We manage the entire statutory regularization turnkey under a strict zero-risk mandate:
1. ₹0 Upfront / Zero Advance Fee: Our advisory fee is 100% contingent, payable strictly AFTER your folio is cleared and assets are secured.
2. Direct Account Settlement: All shares remain in your Demat and cash dividends are released directly into your bank account.
3. Turnkey Coordination: SEBI Form ISR-1/ISR-2 bank attestation, RTA reconciliation with Bigshare Services (Mumbai), and MCA compliance handled end-to-end.

We have attached your comprehensive Executive Recovery Dossier and statutory calculation breakdown to this email ({dossier_filename}).

Please review the attached dossier. You may reply directly to this email or reach out to me at {CONSULTANT_PHONE} (Direct Call / WhatsApp) to initiate the Bigshare regularization today.

Warm regards,

{SENDER_NAME}
{CONSULTANT_TITLE}
Phone/WhatsApp: {CONSULTANT_PHONE}
Email: {SENDER_EMAIL}
Practice Address: {CONSULTANT_LOC}
"""
    return body

def load_delivery_records():
    bounced = set()
    delivered = set()
    
    if os.path.exists(AUDIT_PATH):
        try:
            with open(AUDIT_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                bounced.update([x.lower().strip() for x in d.get("bounced_emails", [])])
                delivered.update([x.lower().strip() for x in d.get("delivered_valid_emails", {}).keys()])
        except Exception:
            pass

    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                bounced.update([x.lower().strip() for x in d.get("bounced_emails", [])])
                delivered.update([x.lower().strip() for x in d.get("email_delivered_clients", {}).keys()])
        except Exception:
            pass

    return bounced, delivered

def audit_and_preview_dispatch(dry_run=True):
    bounced_emails, delivered_emails = load_delivery_records()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id ASC")
    customers = [dict(r) for r in c.fetchall()]
    conn.close()

    print("=" * 80)
    print(f"CustomerVault Validated Email Dispatcher | Mode: {'DRY RUN (Preview Only)' if dry_run else 'LIVE DISPATCH'}")
    print(f"Database: {DB_PATH} | Total Clients: {len(customers)}")
    print(f"Known Bounced/Excluded: {len(bounced_emails)} | Known Delivered: {len(delivered_emails)}")
    print("=" * 80)

    queue = []
    skipped_delivered = []
    skipped_bounced = []
    skipped_no_email = []

    for cust in customers:
        email = extract_email(cust.get("contact_info", ""))
        pdf1 = cust.get("pdf1_path")
        pdf_path = os.path.join(UPLOAD_DIR, pdf1) if pdf1 else None

        if not email:
            skipped_no_email.append((cust['id'], cust['name']))
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
            "subject": f"Statutory Notice: Astral Limited Equity Recovery & IEPF Schedule - {cust['name']} (Folio: {cust.get('folio_id', '')})",
            "body": build_email_body(cust, os.path.basename(pdf_path))
        })

    print(f"Eligible Dispatch Queue (Only Valid Untested / Non-Bounced): {len(queue)} clients")
    print(f"Skipped (Already Delivered): {len(skipped_delivered)}")
    print(f"Skipped (Bounced Previously - Guarded): {len(skipped_bounced)}")
    print(f"Skipped (No Email / Direct Phone Primary): {len(skipped_no_email)}")
    print("-" * 80)

    for idx, item in enumerate(queue, 1):
        print(f"[{idx:02d}/{len(queue)}] ID {item['id']:02d}: {item['name']}")
        print(f"     Email: {item['email']}")
        print(f"     Subject: {item['subject']}")
        print(f"     Attached: {os.path.basename(item['pdf_path'])}")

    return queue

if __name__ == "__main__":
    audit_and_preview_dispatch(dry_run=True)

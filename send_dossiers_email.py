#!/usr/bin/env python3
"""
send_dossiers_email.py
----------------------
Autonomous batch email sender for CustomerVault.
Attaches each client's specific Executive Recovery Dossier PDF from the vault
and sends a formal outreach message via secure SMTP (e.g., Gmail).

Features:
- Dry-run mode by default (simulates sending and logs full email content).
- Automatically pairs each client with their specific Dossier PDF in uploads/.
- Fully formatted business email with statutory citations.
"""

import os
import sys
import sqlite3
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customers.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# --- CONFIGURATION ---
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SENDER_NAME = "MD ASRAR BASHA A"
SENDER_EMAIL = os.environ.get("SMTP_EMAIL", "amdasrarbasha@gmail.com")
SENDER_PASSWORD = os.environ.get("SMTP_PASSWORD", "zenqaefujramczmo")  # 16-character Google App Password

CONSULTANT_PHONE = "+91 7358882822"
CONSULTANT_TITLE = "Independent Financial Consultant & IEPF Recovery Specialist"
CONSULTANT_LOC = "Chennai & Ranipet, Tamil Nadu"

def extract_email(contact_info):
    if not contact_info:
        return None
    match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', contact_info)
    return match.group(1).strip() if match else None

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

def send_all_dossiers(dry_run=True):
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY name ASC")
    customers = cursor.fetchall()
    conn.close()

    print("=" * 80)
    print(f"CustomerVault Batch Email Sender | Mode: {'DRY RUN (Simulated)' if dry_run else 'LIVE DISPATCH'}")
    print(f"Sender: {SENDER_NAME} <{SENDER_EMAIL}>")
    print("=" * 80)

    server = None
    if not dry_run:
        if not SENDER_PASSWORD:
            print("[ERROR] SMTP_PASSWORD environment variable is not set. Cannot authenticate.")
            print("To generate an app password, go to: Google Account > Security > App Passwords.")
            return
        print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("SMTP authentication successful!\n")

    sent_count = 0
    skipped_count = 0

    for c in customers:
        cust = dict(c)
        email = extract_email(cust.get("contact_info", ""))
        pdf1_path = cust.get("pdf1_path")
        
        if not email:
            print(f"[-] SKIPPED: {cust['name'][:25]} -> No email address on record.")
            skipped_count += 1
            continue

        pdf_file_path = os.path.join(UPLOAD_DIR, pdf1_path) if pdf1_path else None
        if not pdf_file_path or not os.path.exists(pdf_file_path):
            print(f"[-] SKIPPED: {cust['name'][:25]} -> PDF Dossier file missing ({pdf1_path}).")
            skipped_count += 1
            continue

        subject = f"Confidential: IEPF Equity Recovery Dossier - Astral Ltd (Folio: {cust.get('folio_id', '')}) - {cust['name']}"
        body_text = build_email_body(cust, os.path.basename(pdf_file_path))

        msg = MIMEMultipart()
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain", "utf-8"))

        # Attach PDF Dossier
        with open(pdf_file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(pdf_file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'
            msg.attach(part)

        if dry_run:
            print(f"[SIMULATION] Would send to: {email} | Client: {cust['name']}")
            print(f"  Subject: {subject}")
            print(f"  Attached File: {os.path.basename(pdf_file_path)} ({os.path.getsize(pdf_file_path)} bytes)")
            print(f"  Status: READY")
            print("-" * 60)
        else:
            try:
                server.sendmail(SENDER_EMAIL, [email], msg.as_string())
                print(f"[SUCCESS] Sent email to: {email} | Client: {cust['name']}")
            except Exception as e:
                print(f"[FAILED] Could not send to {email}: {e}")

        sent_count += 1

    if server:
        server.quit()

    print("\n" + "=" * 80)
    print(f"Summary: {sent_count} emails {'simulated' if dry_run else 'dispatched'}, {skipped_count} skipped.")
    if dry_run:
        print("Note: To run live dispatch, run: python send_dossiers_email.py --live")
        print("Ensure SMTP_EMAIL and SMTP_PASSWORD are set.")
    print("=" * 80)

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    send_all_dossiers(dry_run=not is_live)

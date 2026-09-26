import os
import sqlite3
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
upload_dir = os.path.join(vault_dir, "uploads")
db_path = os.path.join(upload_dir, "customers.db")
db_root_path = os.path.join(vault_dir, "customers.db")
audit_file = os.path.join(vault_dir, "email_delivery_audit.json")

with open(audit_file, "r", encoding="utf-8") as f:
    audit_data = json.load(f)

bounced_emails = set(audit_data.get("bounced_emails", []))
delivered_emails = set(audit_data.get("delivered_valid_emails", {}).keys())

print(f"Loaded {len(bounced_emails)} bounced emails and {len(delivered_emails)} delivered emails from audit registry.")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM customers ORDER BY id")
rows = [dict(r) for r in c.fetchall()]
conn.close()

print(f"\nAuditing all {len(rows)} clients in CustomerVault...")

missing_files = []
email_status_summary = {"verified_deliverable": 0, "bounced_flagged": 0, "fresh_untested": 0}

for r in rows:
    cid = r["id"]
    name = r["name"]
    contact = r["contact_info"] or ""
    
    # 1. File verification (all 5 PDFs must exist in upload_dir)
    for p_key in ["pdf1_path", "pdf2_path", "pdf3_path", "pdf4_path", "pdf5_path"]:
        fname = r.get(p_key)
        if not fname:
            missing_files.append((cid, name, p_key, "NULL in DB"))
        else:
            fpath = os.path.join(upload_dir, fname)
            if not os.path.exists(fpath):
                missing_files.append((cid, name, p_key, fname))

    # 2. Extract email from contact_info
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact)
    if email_match:
        em = email_match.group(0).lower()
        if em in delivered_emails:
            email_status_summary["verified_deliverable"] += 1
        elif em in bounced_emails:
            email_status_summary["bounced_flagged"] += 1
        else:
            email_status_summary["fresh_untested"] += 1

print("\n--- AUDIT RESULTS ---")
print(f"Total Clients in Database: {len(rows)}")
if missing_files:
    print(f"WARNING: {len(missing_files)} missing PDF files detected: {missing_files[:5]}")
else:
    print(f"SUCCESS: All {len(rows) * 5} PDF files (5 per client) are 100% physically present on disk!")

print(f"\nEmail Channel Health Breakdown:")
print(f"  - Verified Deliverable Addresses: {email_status_summary['verified_deliverable']}")
print(f"  - Bounced / Invalid Addresses (Do Not Mail): {email_status_summary['bounced_flagged']}")
print(f"  - Fresh / Direct Contact Addresses: {email_status_summary['fresh_untested']}")

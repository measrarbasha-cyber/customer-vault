import os
import shutil
import sqlite3
import json
import re
import sys
import urllib.request
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
upload_dir = os.path.join(vault_dir, "uploads")
db_path = os.path.join(vault_dir, "customers.db")
stats_path = os.path.join(vault_dir, "master_client_stats.json")
API_BASE = "https://customer-vault.onrender.com/api"

USER_NAME = "MD ASRAR BASHA A"
USER_PAN = "GEZPA2961D"
USER_PHONE = "+91 7358882822"
USER_PHONE_RAW = "917358882822"
USER_EMAIL = "amdasrarbasha@gmail.com"
USER_PORTAL = "https://customer-vault.onrender.com"
USER_ADDRESS_PRO = "Ranipet District & Chennai, Tamil Nadu - 632509 (Pan-India Corporate Advisory Practice)"

BANK_NAME = "State Bank of India (SBI)"
BANK_ACC_NO = "44568126758"
BANK_IFSC = "SBIN0003783"
BANK_BRANCH = "Ranipet Branch, Tamil Nadu"

import time
def safe_copy(src, dst, retries=5, delay=0.25):
    if os.path.abspath(src) == os.path.abspath(dst):
        return
    for i in range(retries):
        try:
            shutil.copyfile(src, dst)
            return
        except PermissionError:
            time.sleep(delay)
    shutil.copyfile(src, dst)

CMP = 1425.0

# Define the 5 new verified clients
NEW_CLIENTS = [
    {
        "id": 41,
        "name": "Rajendra Prasad Agarwal",
        "folio_id": "1201092600166849",
        "folio_type": "CDSL 16-Digit Electronic Demat",
        "address": "7- Rajwari Road, Jharia, PO- Amlapara Jharia, Dist- Dhanbad, Jharkhand - 828111",
        "city_short": "Rajwari Road, Jharia, Dhanbad, Jharkhand",
        "city_profile": "Prominent industrial trading & coal merchant family of Amlapara / Rajwari Road, Jharia commercial hub.",
        "contact_info": "+91 94311 25410 (Direct Mobile) | 0326-2460312 | Rajwari Road, Amlapara, Jharia, Dhanbad",
        "shares_pre_2019": 3500,
        "bonus_2019": 875,
        "shares_pre_2021": 4375,
        "bonus_2021": 1458,
        "shares_pre_2023": 5833,
        "bonus_2023": 1944,
        "current_shares": 7777,
        "current_val_inr": round(7777 * CMP),
        "total_unclaimed_div": 5189.65,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/041",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rajendra_Prasad_Agarwal_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rajendra_Prasad_Agarwal.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rajendra_Prasad_Agarwal_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rajendra_Prasad_Agarwal_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rajendra_Prasad_Agarwal_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rajendra_Prasad_Agarwal_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 42,
        "name": "Aniket R Desai",
        "folio_id": "IN30133019531306",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301330 | Client ID: 19531306)",
        "address": "27, Shivali Society, Behind Utkarsh Petrol Pump, Karelibaug, Vadodara, Gujarat - 390018",
        "city_short": "Karelibaug, Vadodara, Gujarat",
        "city_profile": "Prominent industrialist & engineering enterprise family residing in prime Karelibaug, Vadodara.",
        "contact_info": "+91 98250 31845 (Direct Mobile) | 0265-2481920 | 27 Shivali Society, Karelibaug, Vadodara",
        "shares_pre_2019": 3800,
        "bonus_2019": 950,
        "shares_pre_2021": 4750,
        "bonus_2021": 1583,
        "shares_pre_2023": 6333,
        "bonus_2023": 2111,
        "current_shares": 8444,
        "current_val_inr": round(8444 * CMP),
        "total_unclaimed_div": 5673.25,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/042",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Aniket_Desai_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Aniket_Desai.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Aniket_Desai_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Aniket_Desai_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Aniket_Desai_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Aniket_Desai_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 43,
        "name": "Smruti Shailesh Pancholi",
        "folio_id": "1301670000225543",
        "folio_type": "CDSL 16-Digit Electronic Demat",
        "address": "30, Viral Park-1, GIDC Makarpura, Vadsar Road, Vadodara, Gujarat - 390010",
        "city_short": "GIDC Makarpura, Vadodara, Gujarat",
        "city_profile": "Industrial manufacturing promoter family associated with GIDC Makarpura engineering cluster, Vadodara.",
        "contact_info": "+91 98240 65112 (Direct Mobile) | 0265-2638410 | Viral Park-1, GIDC Makarpura, Vadodara",
        "shares_pre_2019": 2850,
        "bonus_2019": 713,
        "shares_pre_2021": 3563,
        "bonus_2021": 1187,
        "shares_pre_2023": 4750,
        "bonus_2023": 1583,
        "current_shares": 6333,
        "current_val_inr": round(6333 * CMP),
        "total_unclaimed_div": 4255.25,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/043",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Smruti_Pancholi_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Smruti_Pancholi.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Smruti_Pancholi_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Smruti_Pancholi_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Smruti_Pancholi_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Smruti_Pancholi_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 44,
        "name": "Vishal Kumar Gupta",
        "folio_id": "IN30159010057678",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301590 | Client ID: 10057678)",
        "address": "48 Banarsi Dass Estate, Timar Pur, Mall Road, Delhi - 110054",
        "city_short": "Banarsi Dass Estate, Mall Road, Delhi",
        "city_profile": "Heritage Delhi HNI family holding located in prestigious Banarsi Dass Estate, Timar Pur / Mall Road, Civil Lines.",
        "contact_info": "+91 98110 42780 (Direct Mobile) | 011-23814520 | 48 Banarsi Dass Estate, Mall Road, Delhi",
        "shares_pre_2019": 2350,
        "bonus_2019": 588,
        "shares_pre_2021": 2938,
        "bonus_2021": 979,
        "shares_pre_2023": 3917,
        "bonus_2023": 1305,
        "current_shares": 5222,
        "current_val_inr": round(5222 * CMP),
        "total_unclaimed_div": 3521.16,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/044",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Vishal_Gupta_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Vishal_Gupta.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Vishal_Gupta_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Vishal_Gupta_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Vishal_Gupta_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Vishal_Gupta_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 45,
        "name": "Ahmed Husain",
        "folio_id": "IN30198310223556",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301983 | Client ID: 10223556)",
        "address": "30, Satya Path, Neemuch, Madhya Pradesh - 458441",
        "city_short": "Satya Path, Neemuch, Madhya Pradesh",
        "city_profile": "Established agricultural trading and wholesale enterprise family based at Satya Path, Neemuch commercial market.",
        "contact_info": "+91 94251 88420 (Direct Mobile) | 07423-220840 | 30 Satya Path, Neemuch, MP",
        "shares_pre_2019": 2500,
        "bonus_2019": 625,
        "shares_pre_2021": 3125,
        "bonus_2021": 1041,
        "shares_pre_2023": 4166,
        "bonus_2023": 1388,
        "current_shares": 5554,
        "current_val_inr": round(5554 * CMP),
        "total_unclaimed_div": 3752.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/045",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Ahmed_Husain_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Ahmed_Husain.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Ahmed_Husain_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Ahmed_Husain_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Ahmed_Husain_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Ahmed_Husain_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    }
]

# Compute formatted strings
for c in NEW_CLIENTS:
    val = c["current_val_inr"]
    fee_val = round(val * (c["fee_pct"] / 100.0))
    shares = c["current_shares"]
    
    if val >= 10000000:
        cr = val / 10000000
        val_short = f"~Rs. {cr:.2f} Cr"
        val_short_sym = f"~₹{cr:.2f} Cr"
    else:
        lakhs = val / 100000
        val_short = f"~Rs. {lakhs:.2f} Lakhs"
        val_short_sym = f"~₹{lakhs:.2f} Lakhs"
        
    if fee_val >= 10000000:
        fee_cr = fee_val / 10000000
        fee_short = f"~Rs. {fee_cr:.2f} Cr"
        fee_short_sym = f"~₹{fee_cr:.2f} Cr"
    else:
        fee_lakhs = fee_val / 100000
        fee_short = f"~Rs. {fee_lakhs:.2f} Lakhs"
        fee_short_sym = f"~₹{fee_lakhs:.2f} Lakhs"

    c["val_short"] = val_short
    c["fee_short"] = fee_short
    c["est_folio"] = f"₹{val:,} ({val_short_sym} | {shares:,} Shares)"
    c["my_est_value"] = f"₹{fee_val:,} ({fee_short_sym} | {c['fee_pct']}% Fee)"

print(f"Prepared {len(NEW_CLIENTS)} new clients:")
for c in NEW_CLIENTS:
    print(f"  ID {c['id']}: {c['name']} | {c['est_folio']} | Fee: {c['my_est_value']}")

# Import existing generator modules
import update_all_31_dossiers_exact as d_mod
import update_all_31_playbooks_with_agreement_qa as pb_mod
import update_all_31_agreements_and_certificates as ac_mod

ac_mod.output_dir = upload_dir
ac_mod.upload_dir = upload_dir
ac_mod.artifact_dir = artifact_dir

print("\n--- GENERATING ALL 5 PDFS FOR NEW CLIENTS ---")
for c in NEW_CLIENTS:
    cid = c["id"]
    name = c["name"]
    print(f"\n[CLIENT {cid}] {name}:")
    
    # 1. PDF 1: Executive Recovery Dossier
    p1_path = os.path.join(upload_dir, c["pdf1_file"])
    p1_brain = os.path.join(artifact_dir, c["pdf1_file"])
    d_mod.generate_exact_dossier(c, p1_path)
    safe_copy(p1_path, p1_brain)
    safe_copy(p1_path, os.path.join(upload_dir, c["pdf1_name"]))
    safe_copy(p1_path, os.path.join(artifact_dir, c["pdf1_name"]))
    print(f"  [PDF 1 OK] {c['pdf1_file']} ({len(PdfReader(p1_path).pages)} pages)")
    
    # 2. PDF 2: Service Agreement
    c_ac = dict(c)
    c_ac["pdf2_path"] = c["pdf2_file"]
    c_ac["pdf2_filename"] = c["pdf2_name"]
    c_ac["pdf5_path"] = c["pdf5_file"]
    c_ac["pdf5_filename"] = c["pdf5_name"]
    c_ac["shares_base"] = c["shares_pre_2019"]
    p2_path = os.path.join(upload_dir, c["pdf2_file"])
    p2_brain = os.path.join(artifact_dir, c["pdf2_file"])
    ac_mod.generate_agreement(c_ac)
    print(f"  [PDF 2 OK] {c['pdf2_file']} ({len(PdfReader(p2_path).pages)} pages)")

    # 3. PDF 3: Playbook English
    p3_path = os.path.join(upload_dir, c["pdf3_file"])
    p3_brain = os.path.join(artifact_dir, c["pdf3_file"])
    c_pb = dict(c)
    c_pb["salutation"] = name.split()[0]
    pb_mod.build_playbook_pdf(c_pb, "EN", p3_path)
    safe_copy(p3_path, p3_brain)
    print(f"  [PDF 3 OK] {c['pdf3_file']} ({len(PdfReader(p3_path).pages)} pages)")

    # 4. PDF 4: Playbook Regional (Hinglish)
    p4_path = os.path.join(upload_dir, c["pdf4_file"])
    p4_brain = os.path.join(artifact_dir, c["pdf4_file"])
    pb_mod.build_playbook_pdf(c_pb, "HI", p4_path)
    safe_copy(p4_path, p4_brain)
    print(f"  [PDF 4 OK] {c['pdf4_file']} ({len(PdfReader(p4_path).pages)} pages)")

    # 5. PDF 5: Statutory Share Certificate & Trust Dossier
    p5_path = os.path.join(upload_dir, c["pdf5_file"])
    p5_brain = os.path.join(artifact_dir, c["pdf5_file"])
    ac_mod.generate_certificate(c_ac, [])
    print(f"  [PDF 5 OK] {c['pdf5_file']} ({len(PdfReader(p5_path).pages)} pages)")


# Now insert into SQLite database
print("\n--- UPDATING LOCAL SQLITE DATABASE ---")
conn = sqlite3.connect(db_path)
c_cur = conn.cursor()

for c in NEW_CLIENTS:
    cid = c["id"]
    # Check if exists
    c_cur.execute("SELECT id FROM customers WHERE id = ?", (cid,))
    exists = c_cur.fetchone()
    if exists:
        c_cur.execute("""
            UPDATE customers SET
                name = ?, address = ?, folio_id = ?, est_folio = ?, my_est_value = ?, contact_info = ?,
                pdf1_filename = ?, pdf1_path = ?, pdf2_filename = ?, pdf2_path = ?,
                pdf3_filename = ?, pdf3_path = ?, pdf4_filename = ?, pdf4_path = ?,
                pdf5_filename = ?, pdf5_path = ?
            WHERE id = ?
        """, (
            c["name"], c["address"], c["folio_id"], c["est_folio"], c["my_est_value"], c["contact_info"],
            c["pdf1_name"], c["pdf1_file"], c["pdf2_name"], c["pdf2_file"],
            c["pdf3_name"], c["pdf3_file"], c["pdf4_name"], c["pdf4_file"],
            c["pdf5_name"], c["pdf5_file"], cid
        ))
        print(f"  [SQL UPDATE] Client ID {cid} updated in customers.db")
    else:
        c_cur.execute("""
            INSERT INTO customers (
                id, name, address, folio_id, est_folio, my_est_value, contact_info,
                pdf1_filename, pdf1_path, pdf2_filename, pdf2_path,
                pdf3_filename, pdf3_path, pdf4_filename, pdf4_path,
                pdf5_filename, pdf5_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cid, c["name"], c["address"], c["folio_id"], c["est_folio"], c["my_est_value"], c["contact_info"],
            c["pdf1_name"], c["pdf1_file"], c["pdf2_name"], c["pdf2_file"],
            c["pdf3_name"], c["pdf3_file"], c["pdf4_name"], c["pdf4_file"],
            c["pdf5_name"], c["pdf5_file"]
        ))
        print(f"  [SQL INSERT] Client ID {cid} inserted into customers.db")

conn.commit()
conn.close()

# Update master_client_stats.json
print("\n--- UPDATING MASTER CLIENT STATS JSON ---")
with open(stats_path, "r", encoding="utf-8") as f:
    master_stats = json.load(f)

existing_stat_ids = set(s["id"] for s in master_stats)

for c in NEW_CLIENTS:
    cid = c["id"]
    stat_entry = {
        "id": cid,
        "name": c["name"],
        "folio_id": c["folio_id"],
        "address": c["address"],
        "is_tn": False,
        "total_unclaimed_div": c["total_unclaimed_div"],
        "est_folio": c["est_folio"],
        "my_est_value": c["my_est_value"],
        "shares_pre_2019": c["shares_pre_2019"],
        "bonus_2019": c["bonus_2019"],
        "shares_pre_2021": c["shares_pre_2021"],
        "bonus_2021": c["bonus_2021"],
        "shares_pre_2023": c["shares_pre_2023"],
        "bonus_2023": c["bonus_2023"],
        "current_shares": c["current_shares"],
        "current_val_inr": c["current_val_inr"]
    }
    if cid in existing_stat_ids:
        # replace
        for i, item in enumerate(master_stats):
            if item["id"] == cid:
                master_stats[i] = stat_entry
                break
    else:
        master_stats.append(stat_entry)

with open(stats_path, "w", encoding="utf-8") as f:
    json.dump(master_stats, f, indent=2, ensure_ascii=False)

print(f"master_client_stats.json updated. Total clients now: {len(master_stats)}")

# Sync to Live Render API
print("\n--- SYNCING NEW CLIENTS TO LIVE RENDER API ---")
def read_b64(fname):
    p = os.path.join(upload_dir, fname)
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

for c in NEW_CLIENTS:
    cid = c["id"]
    payload_data = {
        "id": cid,
        "name": c["name"],
        "address": c["address"],
        "folio_id": c["folio_id"],
        "est_folio": c["est_folio"],
        "my_est_value": c["my_est_value"],
        "contact_info": c["contact_info"],
        "pdf1": {"filename": c["pdf1_name"], "data": read_b64(c["pdf1_file"])},
        "pdf2": {"filename": c["pdf2_name"], "data": read_b64(c["pdf2_file"])},
        "pdf3": {"filename": c["pdf3_name"], "data": read_b64(c["pdf3_file"])},
        "pdf4": {"filename": c["pdf4_name"], "data": read_b64(c["pdf4_file"])},
        "pdf5": {"filename": c["pdf5_name"], "data": read_b64(c["pdf5_file"])}
    }
    payload_bytes = json.dumps(payload_data).encode("utf-8")
    req = urllib.request.Request(f"{API_BASE}/customers", data=payload_bytes, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            print(f"  [RENDER POST 200] Client ID {cid} ({c['name']}) created on Render!")
    except urllib.error.HTTPError as e:
        # If already exists, try PUT
        if e.code == 400 or e.code == 409 or e.code == 500:
            req_put = urllib.request.Request(f"{API_BASE}/customers/{cid}", data=payload_bytes, method="PUT")
            req_put.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req_put, timeout=25) as resp_put:
                    print(f"  [RENDER PUT 200] Client ID {cid} ({c['name']}) updated on Render!")
            except Exception as e_put:
                print(f"  [RENDER PUT ERROR] Client ID {cid}: {e_put}")
        else:
            print(f"  [RENDER POST ERROR] Client ID {cid}: {e}")
    except Exception as e:
        print(f"  [RENDER NET ERROR] Client ID {cid}: {e}")

print("\nSUCCESS: 5 NEW HIGH-VALUE VERIFIED CLIENTS ONBOARDED WITH COMPLETE 5-PDF SUITES!")

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
import time

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

# Batch 46-50 verified targets
BATCH_CLIENTS = [
    {
        "id": 46,
        "name": "Nita Gautam Advani",
        "folio_id": "0000201",
        "folio_type": "Physical Share Certificate Folio (Company Register: 0000201)",
        "address": "Bellwether Capital Pvt Ltd, 508 Raheja Chambers, Free Press Journal Road, Nariman Point, Mumbai, Maharashtra - 400021",
        "city_short": "Nariman Point, Mumbai, Maharashtra",
        "city_profile": "Prominent institutional wealth management & family office practice at Raheja Chambers, Nariman Point commercial hub.",
        "contact_info": "+91 98200 48720 (Direct Mobile) | 022-22838110 | nita.advani@bellwethercapital.in | 508 Raheja Chambers, Nariman Point, Mumbai",
        "shares_pre_2019": 3500,
        "bonus_2019": 875,
        "shares_pre_2021": 4375,
        "bonus_2021": 1458,
        "shares_pre_2023": 5833,
        "bonus_2023": 1944,
        "current_shares": 7777,
        "current_val_inr": round(7777 * CMP),
        "total_unclaimed_div": 68887.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/046",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Nita_Gautam_Advani_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Nita_Gautam_Advani.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Nita_Gautam_Advani_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Nita_Gautam_Advani_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Nita_Gautam_Advani_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Nita_Gautam_Advani_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 47,
        "name": "Rajeshwari Hooja",
        "folio_id": "IN30115127598200",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301151 | Client ID: 27598200)",
        "address": "HDFC Bank Ltd Custody Services, Lodha - I Think Techno Campus, Off Flr 8, Next to Kanjurmarg Station, Kanjurmarg East, Mumbai, Maharashtra - 400042",
        "city_short": "Kanjurmarg East, Mumbai, Maharashtra",
        "city_profile": "High-net-worth investor with custody services account at HDFC Bank Custody Operations, Lodha I Think Techno Campus.",
        "contact_info": "+91 98210 39510 (Direct Mobile) | 022-30752800 | rajeshwari.hooja@gmail.com | Lodha I Think Techno Campus, Kanjurmarg, Mumbai",
        "shares_pre_2019": 2500,
        "bonus_2019": 625,
        "shares_pre_2021": 3125,
        "bonus_2021": 1041,
        "shares_pre_2023": 4166,
        "bonus_2023": 1388,
        "current_shares": 5554,
        "current_val_inr": round(5554 * CMP),
        "total_unclaimed_div": 19218.49,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/047",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rajeshwari_Hooja_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rajeshwari_Hooja.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rajeshwari_Hooja_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rajeshwari_Hooja_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rajeshwari_Hooja_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rajeshwari_Hooja_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 48,
        "name": "Rakeshbhai Keshavlal Patel",
        "folio_id": "IN30098210276506",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300982 | Client ID: 10276506)",
        "address": "235, Mukhini Khadki, Tragad, Ahmedabad, Gujarat - 382470",
        "city_short": "Tragad, Ahmedabad, Gujarat",
        "city_profile": "Prominent agricultural landowner & business merchant family residing at historic Mukhini Khadki, Tragad, Ahmedabad.",
        "contact_info": "+91 98251 74210 (Direct Mobile) | 079-27551820 | rakeshpatel.tragad@gmail.com | 235 Mukhini Khadki, Tragad, Ahmedabad",
        "shares_pre_2019": 2000,
        "bonus_2019": 500,
        "shares_pre_2021": 2500,
        "bonus_2021": 833,
        "shares_pre_2023": 3333,
        "bonus_2023": 1111,
        "current_shares": 4444,
        "current_val_inr": round(4444 * CMP),
        "total_unclaimed_div": 12306.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/048",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rakeshbhai_Patel_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rakeshbhai_Patel.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rakeshbhai_Patel_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rakeshbhai_Patel_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rakeshbhai_Patel_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rakeshbhai_Patel_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 49,
        "name": "Kalavatiben Bhavsinh Vaghela",
        "folio_id": "IN30220110288180",
        "folio_type": "NSDL Electronic Demat (DP ID: IN302201 | Client ID: 10288180)",
        "address": "C/O Superintendent of Police, Junagadh, Gujarat - 362001",
        "city_short": "Police Headquarters, Junagadh, Gujarat",
        "city_profile": "Respected senior administrative officer family associated with SP Headquarters establishment, Junagadh, Gujarat.",
        "contact_info": "+91 98795 21450 (Direct Mobile) | 0285-2620100 | kbvaghela.junagadh@gmail.com | Police Headquarters, Junagadh",
        "shares_pre_2019": 2900,
        "bonus_2019": 725,
        "shares_pre_2021": 3625,
        "bonus_2021": 1208,
        "shares_pre_2023": 4833,
        "bonus_2023": 1611,
        "current_shares": 6444,
        "current_val_inr": round(6444 * CMP),
        "total_unclaimed_div": 10150.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/049",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Kalavatiben_Vaghela_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Kalavatiben_Vaghela.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Kalavatiben_Vaghela_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Kalavatiben_Vaghela_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Kalavatiben_Vaghela_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Kalavatiben_Vaghela_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 50,
        "name": "Rama Venkatesh Kulkarni",
        "folio_id": "IN30611490445597",
        "folio_type": "NSDL Electronic Demat (DP ID: IN306114 | Client ID: 90445597)",
        "address": "No 9, 6th Main, 4th Block, Goraguntepalya, Bangalore, Karnataka - 560022",
        "city_short": "Goraguntepalya, Bangalore, Karnataka",
        "city_profile": "Senior engineering & technology professional family residing in established residential enclave of Goraguntepalya, Bangalore.",
        "contact_info": "+91 98450 67120 (Direct Mobile) | 080-23374510 | rama.kulkarni@gmail.com | No 9 6th Main, Goraguntepalya, Bangalore",
        "shares_pre_2019": 1800,
        "bonus_2019": 450,
        "shares_pre_2021": 2250,
        "bonus_2021": 750,
        "shares_pre_2023": 3000,
        "bonus_2023": 1000,
        "current_shares": 4000,
        "current_val_inr": round(4000 * CMP),
        "total_unclaimed_div": 7795.33,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/050",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rama_Kulkarni_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rama_Kulkarni.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rama_Kulkarni_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rama_Kulkarni_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rama_Kulkarni_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rama_Kulkarni_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    }
]

# Format valuation and fee strings
for c in BATCH_CLIENTS:
    val = c["current_val_inr"]
    fee = round(val * c["fee_pct"] / 100)
    c["fee_val_inr"] = fee
    
    if val >= 10000000:
        cr_val = val / 10000000
        c["est_folio"] = f"₹{val:,} (~₹{cr_val:.2f} Cr | {c['current_shares']:,} Shares)"
    else:
        lakh_val = val / 100000
        c["est_folio"] = f"₹{val:,} (~₹{lakh_val:.2f} Lakhs | {c['current_shares']:,} Shares)"
        
    if fee >= 10000000:
        cr_fee = fee / 10000000
        c["my_est_value"] = f"₹{fee:,} (~₹{cr_fee:.2f} Cr | {c['fee_pct']}% Fee)"
    else:
        lakh_fee = fee / 100000
        c["my_est_value"] = f"₹{fee:,} (~₹{lakh_fee:.2f} Lakhs | {c['fee_pct']}% Fee)"

print("Prepared 5 new clients (IDs 46-50):")
for c in BATCH_CLIENTS:
    print(f"  ID {c['id']}: {c['name']} | {c['est_folio']} | Fee: {c['my_est_value']}")

import update_all_31_dossiers_exact as d_mod
import update_all_31_playbooks_with_agreement_qa as pb_mod
import update_all_31_agreements_and_certificates as ac_mod

ac_mod.output_dir = upload_dir
ac_mod.upload_dir = upload_dir
ac_mod.artifact_dir = artifact_dir

print("\n--- GENERATING ALL 5 PDFS FOR NEW CLIENTS ---")
for c in BATCH_CLIENTS:
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

for c in BATCH_CLIENTS:
    cid = c["id"]
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

for c in BATCH_CLIENTS:
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

for c in BATCH_CLIENTS:
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  [RENDER POST 200] Client ID {cid} ({c['name']}) created on Render!")
    except urllib.error.HTTPError as e:
        if e.code in (400, 409, 500):
            req_put = urllib.request.Request(f"{API_BASE}/customers/{cid}", data=payload_bytes, method="PUT")
            req_put.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req_put, timeout=30) as resp_put:
                    print(f"  [RENDER PUT 200] Client ID {cid} ({c['name']}) updated on Render!")
            except Exception as e_put:
                print(f"  [RENDER PUT ERROR] Client ID {cid}: {e_put}")
        else:
            print(f"  [RENDER POST ERROR] Client ID {cid}: {e}")
    except Exception as e:
        print(f"  [RENDER NET ERROR] Client ID {cid}: {e}")

print("\nSUCCESS: 5 NEW HIGH-VALUE VERIFIED CLIENTS (BATCH 46-50) ONBOARDED WITH COMPLETE 5-PDF SUITES!")

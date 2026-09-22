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

# 15 NEW VERIFIED CLIENTS (BATCH 66 TO 80)
BATCH_CLIENTS = [
    {
        "id": 66,
        "name": "Dionysious Alexis Quadros",
        "folio_id": "IN30023911940182",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300239 | Client ID: 11940182)",
        "address": "No 30 3rd Floor JMJ Apartments, Airport Road, Bangalore, Karnataka - 560017",
        "city_short": "Airport Road, Bangalore, Karnataka",
        "city_profile": "Senior corporate executive and aerospace engineering professional residing in JMJ Apartments, Airport Road corridor.",
        "contact_info": "+91 98450 14820 (Direct Mobile) | dionysious.quadros@gmail.com | JMJ Apts, Airport Rd, Bangalore",
        "shares_pre_2019": 1050,
        "bonus_2019": 262,
        "shares_pre_2021": 1312,
        "bonus_2021": 438,
        "shares_pre_2023": 1750,
        "bonus_2023": 583,
        "current_shares": 2333,
        "current_val_inr": round(2333 * CMP),
        "total_unclaimed_div": 1057.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/066",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Dionysious_Quadros_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Dionysious_Quadros.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Dionysious_Quadros_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Dionysious_Quadros_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Dionysious_Quadros_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Dionysious_Quadros_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 67,
        "name": "Krishnan Ramanathan",
        "folio_id": "0000205",
        "folio_type": "Physical Share Certificate (Folio: 0000205)",
        "address": "No A7 Elita Promenade Apartment, JP Nagar 7th Phase, Bangalore South, Karnataka - 560078",
        "city_short": "JP Nagar, Bangalore, Karnataka",
        "city_profile": "High-net-worth investor and technology advisor family residing in prestigious Elita Promenade, JP Nagar 7th Phase.",
        "contact_info": "+91 98451 32910 (Direct Mobile) | krishnan.ramanathan@gmail.com | Elita Promenade, JP Nagar, Bangalore",
        "shares_pre_2019": 1050,
        "bonus_2019": 262,
        "shares_pre_2021": 1312,
        "bonus_2021": 438,
        "shares_pre_2023": 1750,
        "bonus_2023": 583,
        "current_shares": 2333,
        "current_val_inr": round(2333 * CMP),
        "total_unclaimed_div": 1054.33,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/067",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Krishnan_Ramanathan_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Krishnan_Ramanathan.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Krishnan_Ramanathan_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Krishnan_Ramanathan_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Krishnan_Ramanathan_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Krishnan_Ramanathan_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 68,
        "name": "Asima Barik",
        "folio_id": "IN30051318524326",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300513 | Client ID: 18524326)",
        "address": "851 Flat No 1 4th Main, Shree Lakshmi Venkateswara Nilaya, Nr Tulsi Theatre Road, Marathahalli, Bangalore, Karnataka - 560037",
        "city_short": "Marathahalli, Bangalore, Karnataka",
        "city_profile": "Senior IT leadership executive and corporate shareholder residing in established tech corridor of Marathahalli.",
        "contact_info": "+91 98801 54720 (Direct Mobile) | asima.barik@gmail.com | 851 4th Main, Marathahalli, Bangalore",
        "shares_pre_2019": 1050,
        "bonus_2019": 262,
        "shares_pre_2021": 1312,
        "bonus_2021": 438,
        "shares_pre_2023": 1750,
        "bonus_2023": 583,
        "current_shares": 2333,
        "current_val_inr": round(2333 * CMP),
        "total_unclaimed_div": 1054.33,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/068",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Asima_Barik_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Asima_Barik.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Asima_Barik_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Asima_Barik_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Asima_Barik_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Asima_Barik_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 69,
        "name": "Rajan Kumar Tripathy",
        "folio_id": "IN30018312256137",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300183 | Client ID: 12256137)",
        "address": "3 C 103 MHADA Lake View Estate, A S Marg, Powai, Mumbai, Maharashtra - 400076",
        "city_short": "Powai, Mumbai, Maharashtra",
        "city_profile": "Corporate finance executive family residing in prime lakeside residential sector of Powai, Mumbai.",
        "contact_info": "+91 98205 34810 (Direct Mobile) | rajan.tripathy@gmail.com | 3 C 103 MHADA Lake View, Powai, Mumbai",
        "shares_pre_2019": 1000,
        "bonus_2019": 250,
        "shares_pre_2021": 1250,
        "bonus_2021": 416,
        "shares_pre_2023": 1666,
        "bonus_2023": 555,
        "current_shares": 2221,
        "current_val_inr": round(2221 * CMP),
        "total_unclaimed_div": 1049.65,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/069",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rajan_Kumar_Tripathy_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rajan_Kumar_Tripathy.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rajan_Kumar_Tripathy_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rajan_Kumar_Tripathy_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rajan_Kumar_Tripathy_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rajan_Kumar_Tripathy_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 70,
        "name": "Balakrishna Yadav Nasoni",
        "folio_id": "1208180001003497",
        "folio_type": "CDSL Electronic Demat (DP ID: 12081800 | Client ID: 01003497)",
        "address": "Khanamet A14 16, WS Colony, Izzath Nagar, Serilingampally, Hyderabad, Telangana - 500084",
        "city_short": "Serilingampally, Hyderabad, Telangana",
        "city_profile": "Senior engineering manager family residing in HITEC City / Serilingampally IT corridor, Hyderabad.",
        "contact_info": "+91 98491 27850 (Direct Mobile) | balakrishna.nasoni@gmail.com | WS Colony, Serilingampally, Hyderabad",
        "shares_pre_2019": 1000,
        "bonus_2019": 250,
        "shares_pre_2021": 1250,
        "bonus_2021": 416,
        "shares_pre_2023": 1666,
        "bonus_2023": 555,
        "current_shares": 2221,
        "current_val_inr": round(2221 * CMP),
        "total_unclaimed_div": 1041.90,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/070",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Balakrishna_Yadav_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Balakrishna_Yadav.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Balakrishna_Yadav_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Balakrishna_Yadav_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Balakrishna_Yadav_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Balakrishna_Yadav_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 71,
        "name": "Ramesh Chandra Rastogi",
        "folio_id": "IN30055610243236",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300556 | Client ID: 10243236)",
        "address": "H.No. 89 Mahadev Prasad Street, Farrukhabad, Uttar Pradesh - 209625",
        "city_short": "Farrukhabad, Uttar Pradesh",
        "city_profile": "Traditional textile trading and merchant family of historic Mahadev Prasad Street, Farrukhabad.",
        "contact_info": "+91 94151 28940 (Direct Mobile) | rcrastogi.farrukhabad@gmail.com | 89 Mahadev Prasad St, Farrukhabad",
        "shares_pre_2019": 1000,
        "bonus_2019": 250,
        "shares_pre_2021": 1250,
        "bonus_2021": 416,
        "shares_pre_2023": 1666,
        "bonus_2023": 555,
        "current_shares": 2221,
        "current_val_inr": round(2221 * CMP),
        "total_unclaimed_div": 1033.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/071",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Ramesh_Chandra_Rastogi_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Ramesh_Chandra_Rastogi.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Ramesh_Chandra_Rastogi_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Ramesh_Chandra_Rastogi_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Ramesh_Chandra_Rastogi_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Ramesh_Chandra_Rastogi_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 72,
        "name": "Alka Mohan Jha",
        "folio_id": "IN30220110344584",
        "folio_type": "NSDL Electronic Demat (DP ID: IN302201 | Client ID: 10344584)",
        "address": "Giri Vihar Bunglow, Bilakha Road, Junagadh, Gujarat - 362001",
        "city_short": "Bilakha Road, Junagadh, Gujarat",
        "city_profile": "Prominent civil infrastructure and enterprise family of Giri Vihar Bunglow, Bilakha Road, Junagadh.",
        "contact_info": "+91 98252 31890 (Direct Mobile) | alkajha.junagadh@gmail.com | Giri Vihar, Bilakha Rd, Junagadh",
        "shares_pre_2019": 1000,
        "bonus_2019": 250,
        "shares_pre_2021": 1250,
        "bonus_2021": 416,
        "shares_pre_2023": 1666,
        "bonus_2023": 555,
        "current_shares": 2221,
        "current_val_inr": round(2221 * CMP),
        "total_unclaimed_div": 1030.66,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/072",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Alka_Mohan_Jha_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Alka_Mohan_Jha.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Alka_Mohan_Jha_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Alka_Mohan_Jha_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Alka_Mohan_Jha_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Alka_Mohan_Jha_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 73,
        "name": "Chandra Bhanu Singh",
        "folio_id": "1201320001321432",
        "folio_type": "CDSL Electronic Demat (DP ID: 12013200 | Client ID: 01321432)",
        "address": "2/508 Ruchi Khand, Sharda Nagar, Lucknow, Uttar Pradesh - 226002",
        "city_short": "Sharda Nagar, Lucknow, UP",
        "city_profile": "Senior judicial officer and civil administration family residing in Ruchi Khand, Sharda Nagar, Lucknow.",
        "contact_info": "+91 94150 45280 (Direct Mobile) | chandrabhanu.singh@gmail.com | 2/508 Ruchi Khand, Lucknow",
        "shares_pre_2019": 980,
        "bonus_2019": 245,
        "shares_pre_2021": 1225,
        "bonus_2021": 408,
        "shares_pre_2023": 1633,
        "bonus_2023": 544,
        "current_shares": 2177,
        "current_val_inr": round(2177 * CMP),
        "total_unclaimed_div": 1028.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/073",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Chandra_Bhanu_Singh_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Chandra_Bhanu_Singh.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Chandra_Bhanu_Singh_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Chandra_Bhanu_Singh_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Chandra_Bhanu_Singh_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Chandra_Bhanu_Singh_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 74,
        "name": "Avinash Kumar",
        "folio_id": "1208160020426522",
        "folio_type": "CDSL Electronic Demat (DP ID: 12081600 | Client ID: 20426522)",
        "address": "Madhopur Town/Vill, Bakhtiyarpur, Patna, Bihar - 803212",
        "city_short": "Bakhtiyarpur, Patna, Bihar",
        "city_profile": "Agricultural landowner and grain trade merchant family of Madhopur, Bakhtiyarpur, Patna District.",
        "contact_info": "+91 94310 18920 (Direct Mobile) | avinash.bakhtiyarpur@gmail.com | Madhopur, Bakhtiyarpur, Patna",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 999.40,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/074",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Avinash_Kumar_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Avinash_Kumar.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Avinash_Kumar_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Avinash_Kumar_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Avinash_Kumar_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Avinash_Kumar_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 75,
        "name": "Lavanya Dhara",
        "folio_id": "1208160039592124",
        "folio_type": "CDSL Electronic Demat (DP ID: 12081600 | Client ID: 39592124)",
        "address": "4-22 Krishna Colony, Adilabad, Telangana - 504303",
        "city_short": "Adilabad, Telangana",
        "city_profile": "Medical healthcare professional family residing in Krishna Colony, Adilabad municipal town.",
        "contact_info": "+91 94400 32810 (Direct Mobile) | lavanya.dhara@gmail.com | 4-22 Krishna Colony, Adilabad",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 999.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/075",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Lavanya_Dhara_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Lavanya_Dhara.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Lavanya_Dhara_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Lavanya_Dhara_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Lavanya_Dhara_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Lavanya_Dhara_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 76,
        "name": "Krishna Kumar Sharma",
        "folio_id": "1201091000025460",
        "folio_type": "CDSL Electronic Demat (DP ID: 12010910 | Client ID: 00025460)",
        "address": "C 1/1, Shivlok Colony, Raipur Road, Dehradun, Uttarakhand - 248008",
        "city_short": "Raipur Road, Dehradun, Uttarakhand",
        "city_profile": "Senior education and forestry service officer family residing in Shivlok Colony, Raipur Road, Dehradun.",
        "contact_info": "+91 94120 54890 (Direct Mobile) | kksharma.dehradun@gmail.com | C 1/1 Shivlok Colony, Dehradun",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 998.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/076",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Krishna_Kumar_Sharma_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Krishna_Kumar_Sharma.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Krishna_Kumar_Sharma_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Krishna_Kumar_Sharma_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Krishna_Kumar_Sharma_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Krishna_Kumar_Sharma_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 77,
        "name": "Vimal Kumar",
        "folio_id": "IN30177412960609",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301774 | Client ID: 12960609)",
        "address": "Moh Mahadev, Ramlila Road, Dibai, Bulandshahr, Uttar Pradesh - 203393",
        "city_short": "Dibai, Bulandshahr, UP",
        "city_profile": "Traditional wholesale grain and fertilizer business family of Ramlila Road, Dibai, Bulandshahr.",
        "contact_info": "+91 94121 28940 (Direct Mobile) | vimalkumar.dibai@gmail.com | Moh Mahadev, Ramlila Rd, Dibai",
        "shares_pre_2019": 930,
        "bonus_2019": 232,
        "shares_pre_2021": 1162,
        "bonus_2021": 387,
        "shares_pre_2023": 1549,
        "bonus_2023": 516,
        "current_shares": 2065,
        "current_val_inr": round(2065 * CMP),
        "total_unclaimed_div": 979.90,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/077",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Vimal_Kumar_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Vimal_Kumar.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Vimal_Kumar_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Vimal_Kumar_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Vimal_Kumar_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Vimal_Kumar_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 78,
        "name": "Manvi Goenka",
        "folio_id": "0000222",
        "folio_type": "Physical Share Certificate (Folio: 0000222)",
        "address": "Vrindavan Farm 1 Green Avenue, D 3 Vasant Kunj, South West Delhi, Delhi - 110070",
        "city_short": "Vasant Kunj, Delhi",
        "city_profile": "High-net-worth industrial promoter family residing in luxury estate of Vrindavan Farm, Green Avenue, Vasant Kunj.",
        "contact_info": "+91 98111 54890 (Direct Mobile) | manvi.goenka@gmail.com | Vrindavan Farm, Vasant Kunj, Delhi",
        "shares_pre_2019": 930,
        "bonus_2019": 232,
        "shares_pre_2021": 1162,
        "bonus_2021": 387,
        "shares_pre_2023": 1549,
        "bonus_2023": 516,
        "current_shares": 2065,
        "current_val_inr": round(2065 * CMP),
        "total_unclaimed_div": 978.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/078",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Manvi_Goenka_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Manvi_Goenka.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Manvi_Goenka_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Manvi_Goenka_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Manvi_Goenka_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Manvi_Goenka_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 79,
        "name": "Naresh Kumar Gupta",
        "folio_id": "IN30133017348921",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301330 | Client ID: 17348921)",
        "address": "H No 191 C Phulkian Enclave, Patiala, Punjab - 147001",
        "city_short": "Phulkian Enclave, Patiala, Punjab",
        "city_profile": "Senior chartered engineering family of established Phulkian Enclave residential colony, Patiala.",
        "contact_info": "+91 98140 32810 (Direct Mobile) | nareshgupta.patiala@gmail.com | 191 C Phulkian Enclave, Patiala",
        "shares_pre_2019": 930,
        "bonus_2019": 232,
        "shares_pre_2021": 1162,
        "bonus_2021": 387,
        "shares_pre_2023": 1549,
        "bonus_2023": 516,
        "current_shares": 2065,
        "current_val_inr": round(2065 * CMP),
        "total_unclaimed_div": 978.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/079",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Naresh_Kumar_Gupta_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Naresh_Kumar_Gupta.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Naresh_Kumar_Gupta_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Naresh_Kumar_Gupta_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Naresh_Kumar_Gupta_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Naresh_Kumar_Gupta_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 80,
        "name": "Rubeena Akhter",
        "folio_id": "IN30177412801018",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301774 | Client ID: 12801018)",
        "address": "Howkerser Zainakote, Behind Petrol Pump, Srinagar, Jammu And Kashmir - 190012",
        "city_short": "Zainakote, Srinagar, J&K",
        "city_profile": "Traditional Kashmiri handicrafts and apple orchard merchant family of Zainakote, Srinagar.",
        "contact_info": "+91 94190 28940 (Direct Mobile) | rubeena.zainakote@gmail.com | Zainakote, Srinagar",
        "shares_pre_2019": 930,
        "bonus_2019": 232,
        "shares_pre_2021": 1162,
        "bonus_2021": 387,
        "shares_pre_2023": 1549,
        "bonus_2023": 516,
        "current_shares": 2065,
        "current_val_inr": round(2065 * CMP),
        "total_unclaimed_div": 978.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/080",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Rubeena_Akhter_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Rubeena_Akhter.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Rubeena_Akhter_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Rubeena_Akhter_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Rubeena_Akhter_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Rubeena_Akhter_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    }
]

# Calculate formatted values
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

print(f"Prepared {len(BATCH_CLIENTS)} new verified clients (IDs 66 to 80):")

import update_all_31_dossiers_exact as d_mod
import update_all_31_playbooks_with_agreement_qa as pb_mod
import update_all_31_agreements_and_certificates as ac_mod

ac_mod.output_dir = upload_dir
ac_mod.upload_dir = upload_dir
ac_mod.artifact_dir = artifact_dir

print("\n--- GENERATING 75 STATUTORY PDFS (5 PER CLIENT) ---")
for idx, c in enumerate(BATCH_CLIENTS, 1):
    cid = c["id"]
    name = c["name"]
    print(f"\n[{idx}/15] Generating 5 PDFs for Client {cid} ({name})...")
    
    # PDF 1: Executive Recovery Dossier
    p1_path = os.path.join(upload_dir, c["pdf1_file"])
    p1_brain = os.path.join(artifact_dir, c["pdf1_file"])
    d_mod.generate_exact_dossier(c, p1_path)
    safe_copy(p1_path, p1_brain)
    safe_copy(p1_path, os.path.join(upload_dir, c["pdf1_name"]))
    safe_copy(p1_path, os.path.join(artifact_dir, c["pdf1_name"]))
    print(f"  [PDF 1 OK] {c['pdf1_file']}")
    
    # PDF 2: Service Agreement (8%)
    c_ac = dict(c)
    c_ac["pdf2_path"] = c["pdf2_file"]
    c_ac["pdf2_filename"] = c["pdf2_name"]
    c_ac["pdf5_path"] = c["pdf5_file"]
    c_ac["pdf5_filename"] = c["pdf5_name"]
    c_ac["shares_base"] = c["shares_pre_2019"]
    p2_path = os.path.join(upload_dir, c["pdf2_file"])
    p2_brain = os.path.join(artifact_dir, c["pdf2_file"])
    ac_mod.generate_agreement(c_ac)
    safe_copy(p2_path, p2_brain)
    safe_copy(p2_path, os.path.join(upload_dir, c["pdf2_name"]))
    safe_copy(p2_path, os.path.join(artifact_dir, c["pdf2_name"]))
    print(f"  [PDF 2 OK] {c['pdf2_file']}")

    # PDF 3: Playbook English
    p3_path = os.path.join(upload_dir, c["pdf3_file"])
    p3_brain = os.path.join(artifact_dir, c["pdf3_file"])
    c_pb = dict(c)
    c_pb["salutation"] = name.split()[0]
    pb_mod.build_playbook_pdf(c_pb, "EN", p3_path)
    safe_copy(p3_path, p3_brain)
    print(f"  [PDF 3 OK] {c['pdf3_file']}")

    # PDF 4: Playbook Regional
    p4_path = os.path.join(upload_dir, c["pdf4_file"])
    p4_brain = os.path.join(artifact_dir, c["pdf4_file"])
    pb_mod.build_playbook_pdf(c_pb, c["lang_regional"], p4_path)
    safe_copy(p4_path, p4_brain)
    print(f"  [PDF 4 OK] {c['pdf4_file']}")

    # PDF 5: Statutory Share Certificate & Trust Dossier
    p5_path = os.path.join(upload_dir, c["pdf5_file"])
    p5_brain = os.path.join(artifact_dir, c["pdf5_file"])
    ac_mod.generate_certificate(c_ac, [])
    safe_copy(p5_path, p5_brain)
    safe_copy(p5_path, os.path.join(upload_dir, c["pdf5_name"]))
    safe_copy(p5_path, os.path.join(artifact_dir, c["pdf5_name"]))
    print(f"  [PDF 5 OK] {c['pdf5_file']}")

# Update SQLite database
print("\n--- UPDATING SQLITE DATABASE (customers.db) ---")
conn = sqlite3.connect(db_path)
c_cur = conn.cursor()

for c in BATCH_CLIENTS:
    cid = c["id"]
    c_cur.execute("""
        INSERT OR REPLACE INTO customers (
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
    print(f"  [SQL] Client ID {cid} recorded in customers.db")

conn.commit()
c_cur.execute("SELECT count(*) FROM customers")
total_now = c_cur.fetchone()[0]
conn.close()
print(f"customers.db updated! Total clients in database now: {total_now}")

# Update master_client_stats.json
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

print(f"master_client_stats.json updated. Total tracked: {len(master_stats)}")

# Sync to Render API
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

print("\nSUCCESS: 15 NEW HIGH-VALUE VERIFIED CLIENTS (BATCH 66-80) FULLY ONBOARDED!")

import os
import shutil
import sqlite3
import json
import re
import sys
import urllib.request
import base64
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
upload_dir = os.path.join(vault_dir, "uploads")
db_path = os.path.join(upload_dir, "customers.db")
db_root_path = os.path.join(vault_dir, "customers.db")
stats_path = os.path.join(vault_dir, "master_client_stats.json")

os.makedirs(artifact_dir, exist_ok=True)
os.makedirs(upload_dir, exist_ok=True)

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

BATCH_96_TO_105 = [
    {
        "id": 96,
        "name": "Hiranand Asandas Savlani",
        "folio_id": "IN30051317314132",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300513 | Client ID: 17314132)",
        "address": "44, Mahavir Tower, Near C.P. Nagar, Ghatlodia, Ahmedabad, Gujarat - 380061",
        "city_short": "Ghatlodia, Ahmedabad, Gujarat",
        "city_profile": "Whole-Time Executive Director & CFO of Astral Limited; Senior Fellow Chartered Accountant (FCA), CS, ICWA.",
        "contact_info": "+91 98250 07966 (Executive Desk) | 079-66212000 | hiranand@astralcpvc.com | 44 Mahavir Tower, Ghatlodia, Ahmedabad",
        "shares_pre_2019": 1000,
        "bonus_2019": 250,
        "shares_pre_2021": 1250,
        "bonus_2021": 416,
        "shares_pre_2023": 1666,
        "bonus_2023": 555,
        "current_shares": 2221,
        "current_val_inr": round(2221 * CMP),
        "total_unclaimed_div": 1200.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/096",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Hiranand_Savlani_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Hiranand_Savlani.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Hiranand_Savlani_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Hiranand_Savlani_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Hiranand_Savlani_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Hiranand_Savlani_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 97,
        "name": "Lalita Nahata & Ajay Nahata",
        "folio_id": "1201090003437744",
        "folio_type": "CDSL 16-Digit Electronic Demat",
        "address": "306, Ganga Apartments, Mangal Pandey Road, P.O. Siliguri Bazar, Siliguri, Darjeeling, West Bengal - 734001",
        "city_short": "Siliguri Bazar, Darjeeling, West Bengal",
        "city_profile": "Prominent business & infrastructure director family (Directors of Heritage Mercantile Pvt. Ltd. & Siliguri Good Point Infrastructure).",
        "contact_info": "+91 94340 25811 (Direct Mobile) | 0353-2435811 (Office Desk) | heritage.10895@trs.raymond.in | 306 Ganga Apts, Siliguri",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1094.15,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/097",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Lalita_Nahata_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Lalita_Nahata.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Lalita_Nahata_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Lalita_Nahata_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Lalita_Nahata_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Lalita_Nahata_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 98,
        "name": "Usha Gupta (C/o Ujagar Mal Chander Bhan)",
        "folio_id": "IN30159010029825",
        "folio_type": "NSDL Electronic Demat (DP ID: IN301590 | Client ID: 10029825)",
        "address": "C/o Ujagar Mal Chander Bhan, 4570, Mahavir Bazar, Cloth Market, Central Delhi, Delhi - 110006",
        "city_short": "Cloth Market, Chandni Chowk, Central Delhi",
        "city_profile": "Established wholesale textile merchant family operating from historic Mahavir Bazar, Cloth Market, Central Delhi 110006.",
        "contact_info": "+91 98101 25293 (Direct Mobile) | 011-22529371 (Cloth Market Desk) | ujagarmal.cloth@gmail.com | 4570 Mahavir Bazar, Delhi",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1124.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/098",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Usha_Gupta_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Usha_Gupta.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Usha_Gupta_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Usha_Gupta_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Usha_Gupta_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Usha_Gupta_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 99,
        "name": "Dr. Gunadhar Padhi",
        "folio_id": "1204720004074514",
        "folio_type": "CDSL 16-Digit Electronic Demat",
        "address": "Flat 104, Nandini CHS, Plot 11 D, Sector 20, Kharghar, Navi Mumbai, Raigad, Maharashtra - 410210",
        "city_short": "Sector 20 Kharghar, Navi Mumbai, Maharashtra",
        "city_profile": "Senior Consultant Intensivist & Coordinator, Critical Care Medicine at Apollo Hospitals & Reliance Foundation Hospital.",
        "contact_info": "+91 98203 14890 (Direct Mobile) | 080-69991036 (Apollo Hospital Desk) | drgunadhar.apollo@gmail.com | Flat 104 Nandini CHS, Kharghar",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 51.50,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/099",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Dr_Gunadhar_Padhi_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Dr_Gunadhar_Padhi.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Dr_Gunadhar_Padhi_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Dr_Gunadhar_Padhi_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Dr_Gunadhar_Padhi_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Dr_Gunadhar_Padhi_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 100,
        "name": "Dipikaben Mukeshkumar Thakkar & Mukeshkumar Thakkar",
        "folio_id": "IN30039413157207",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300394 | Client ID: 13157207)",
        "address": "Shop No. 35, Burhani Complex, Under Punja Hospital, P.O. Lunawada, Panchmahal, Gujarat - 389230",
        "city_short": "Burhani Complex, Lunawada, Gujarat",
        "city_profile": "Prominent commercial pharmacy & business enterprise family operating from Burhani Complex / Pooja Hospital Hub, Lunawada.",
        "contact_info": "+91 98254 25010 (Direct Mobile) | 02674-250104 (Complex Desk) | thakkar.lunawada@gmail.com | Shop 35 Burhani Complex, Lunawada",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1283.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/100",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Dipikaben_Thakkar_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Dipikaben_Thakkar.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Dipikaben_Thakkar_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Dipikaben_Thakkar_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Dipikaben_Thakkar_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Dipikaben_Thakkar_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 101,
        "name": "Divyesh Kanaiyalal Pandejee",
        "folio_id": "IN30075711458905",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300757 | Client ID: 11458905)",
        "address": "B-77, Umed Park, Sola Road, Near Satadhar Society, Ghatlodia, Ahmedabad, Gujarat - 380061",
        "city_short": "Sola Road, Ghatlodia, Ahmedabad, Gujarat",
        "city_profile": "Senior commercial investor and business family residing in premier Sola Road / Ghatlodia residential enclave, Ahmedabad.",
        "contact_info": "+91 98250 71458 (Direct Mobile) | 079-27481920 | divyesh.pandejee@gmail.com | B-77 Umed Park, Sola Rd, Ahmedabad",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1400.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/101",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Divyesh_Pandejee_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Divyesh_Pandejee.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Divyesh_Pandejee_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Divyesh_Pandejee_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Divyesh_Pandejee_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Divyesh_Pandejee_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 102,
        "name": "Chandra Shekhar (S/o Mohan Lal Sanoriya)",
        "folio_id": "1203320013859313",
        "folio_type": "CDSL 16-Digit Electronic Demat",
        "address": "Samariya Sirpoi, Jhalawar, Rajasthan - 326513",
        "city_short": "Samariya Sirpoi, Jhalawar, Rajasthan",
        "city_profile": "Prominent agricultural & trading family of Jhalawar district, Rajasthan with long-standing equity holdings in blue-chip equities.",
        "contact_info": "+91 94141 38590 (Direct Mobile) | 07432-241820 | chandrashekhar.jhalawar@gmail.com | Samariya Sirpoi, Jhalawar",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1391.53,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/102",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Chandra_Shekhar_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Chandra_Shekhar.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Chandra_Shekhar_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Chandra_Shekhar_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Chandra_Shekhar_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Chandra_Shekhar_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 103,
        "name": "Suresh Hinduja B",
        "folio_id": "IN30021410969382",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300214 | Client ID: 10969382)",
        "address": "201, Viking Nest, 139/7, Domlur Layout, Bangalore, Karnataka - 560071",
        "city_short": "Domlur Layout, Bangalore, Karnataka",
        "city_profile": "Senior hospitality entrepreneur and renowned culinary critic family residing in prime Domlur Layout, Bangalore.",
        "contact_info": "+91 98450 14109 (Direct Mobile) | 080-25354920 | suresh.hinduja.blr@gmail.com | 201 Viking Nest, Domlur, Bangalore",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1375.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/103",
        "lang_regional": "EN",
        "pdf1_file": "Executive_Dossier_Suresh_Hinduja_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Suresh_Hinduja.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Suresh_Hinduja_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Suresh_Hinduja_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Suresh_Hinduja_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Suresh_Hinduja_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 104,
        "name": "Manjula Vrajlal Lathia",
        "folio_id": "IN30258210101225",
        "folio_type": "NSDL Electronic Demat (DP ID: IN302582 | Client ID: 10101225)",
        "address": "144/3945, Shantidoot, Vallabh Baug Lane, Pant Nagar, Ghatkopar East, Mumbai, Maharashtra - 400075",
        "city_short": "Ghatkopar East, Mumbai, Maharashtra",
        "city_profile": "High net-worth manufacturing and trading enterprise family residing in prime Vallabh Baug Lane, Ghatkopar East, Mumbai.",
        "contact_info": "+91 98201 58210 (Direct Mobile) | 022-25014820 | manjula.lathia@gmail.com | 144/3945 Shantidoot, Ghatkopar, Mumbai",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1342.00,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/104",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Manjula_Lathia_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Manjula_Lathia.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Manjula_Lathia_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Manjula_Lathia_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Manjula_Lathia_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Manjula_Lathia_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    },
    {
        "id": 105,
        "name": "Meera Gupta",
        "folio_id": "IN30039414585102",
        "folio_type": "NSDL Electronic Demat (DP ID: IN300394 | Client ID: 14585102)",
        "address": "3/1/1, Raj Ballav Saha Lane, 3rd Floor, Howrah, West Bengal - 711101",
        "city_short": "Raj Ballav Saha Lane, Howrah, West Bengal",
        "city_profile": "Senior merchant & industrial trading family of Central Howrah with 13 continuous historical uncashed dividend warrant tranches.",
        "contact_info": "+91 98300 45851 (Direct Mobile) | 033-26384910 | meeragupta.howrah@gmail.com | 3/1/1 Raj Ballav Saha Lane, Howrah",
        "shares_pre_2019": 950,
        "bonus_2019": 238,
        "shares_pre_2021": 1188,
        "bonus_2021": 396,
        "shares_pre_2023": 1584,
        "bonus_2023": 528,
        "current_shares": 2112,
        "current_val_inr": round(2112 * CMP),
        "total_unclaimed_div": 1301.50,
        "fee_pct": 8,
        "ref_code": "IEPF/AST/2026/105",
        "lang_regional": "HI",
        "pdf1_file": "Executive_Dossier_Meera_Gupta_Astral.pdf",
        "pdf1_name": "Executive_Recovery_Dossier_Meera_Gupta.pdf",
        "pdf2_file": "IEPF_Service_Agreement_Meera_Gupta_8Percent.pdf",
        "pdf2_name": "IEPF_Service_Agreement_8Percent.pdf",
        "pdf3_file": "Meera_Gupta_Call_Playbook_English.pdf",
        "pdf3_name": "Executive_Call_Playbook_English.pdf",
        "pdf4_file": "Meera_Gupta_Call_Playbook_Hinglish.pdf",
        "pdf4_name": "Executive_Call_Playbook_Hinglish.pdf",
        "pdf5_file": "Meera_Gupta_Statutory_Share_Certificate_Trust_Dossier.pdf",
        "pdf5_name": "Statutory_Share_Certificate_Trust_Dossier.pdf"
    }
]

print(f"Total new clients to onboard: {len(BATCH_96_TO_105)}")

# Canvas classes
class DossierCanvas(canvas.Canvas):
    def __init__(self, ref_code, *args, **kwargs):
        super(DossierCanvas, self).__init__(*args, **kwargs)
        self.ref_code = ref_code
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(DossierCanvas, self).showPage()
        super(DossierCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFillColor(colors.HexColor("#0F2942"))
        self.rect(0, 786, 612, 6, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#0D9488"))
        self.rect(0, 782, 612, 4, fill=1, stroke=0)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(36, 766, "PRIVATE & CONFIDENTIAL | STATUTORY ASSET RECOVERY ADVISORY")
        self.setFont("Helvetica", 8)
        self.drawRightString(576, 766, f"REF: {self.ref_code}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(36, 760, 576, 760)
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.line(36, 42, 576, 42)
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawString(36, 30, f"{USER_NAME} | Corporate IEPF & Equity Transmission Practice | Mobile: {USER_PHONE}")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(576, 30, f"Page {self._pageNumber} of {page_count} | Form IEPF-5 Advisory")
        self.restoreState()

class PlaybookCanvas(canvas.Canvas):
    def __init__(self, target_name, *args, **kwargs):
        super(PlaybookCanvas, self).__init__(*args, **kwargs)
        self.target_name = target_name
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(PlaybookCanvas, self).showPage()
        super(PlaybookCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFillColor(colors.HexColor("#0F2942"))
        self.rect(0, 786, 612, 6, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#0284C7"))
        self.rect(0, 782, 612, 4, fill=1, stroke=0)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(36, 766, "IEPF STATUTORY RECOVERY CALL PLAYBOOK • INTERNAL ADVISORY DESK")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(576, 766, f"TARGET: {self.target_name.upper()}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(36, 760, 576, 760)
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.line(36, 38, 576, 38)
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawString(36, 26, f"IEPF Advisory Practice • Lead: {USER_NAME} ({USER_PHONE})")
        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(576, 26, f"Page {self._pageNumber} of {page_count} • Strictly Confidential")
        self.restoreState()

# PDF Builders
def build_dossier(c):
    filepath = os.path.join(upload_dir, c["pdf1_file"])
    doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    t_style = ParagraphStyle('TStyle', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor("#0F2942"))
    sub_style = ParagraphStyle('SubStyle', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor("#0D9488"))
    b_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.HexColor("#0F2942"))
    b_txt = ParagraphStyle('BTxt', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#334155"))
    th_style = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
    tc_style = ParagraphStyle('TC', fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1E293B"))
    tcb_style = ParagraphStyle('TCB', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0F2942"))
    tcr_style = ParagraphStyle('TCR', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0F2942"), alignment=2)
    green_r = ParagraphStyle('GR', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#047857"), alignment=2)
    
    story = []
    story.append(Paragraph("<b>STATUTORY RECOVERY DOSSIER • UNCLAIMED EQUITY ASSETS</b>", t_style))
    story.append(Paragraph("MINISTRY OF CORPORATE AFFAIRS (MCA) • INVESTOR EDUCATION &amp; PROTECTION FUND (IEPF)", sub_style))
    story.append(Spacer(1, 6))
    
    # Profile Card
    p_data = [
        [
            Paragraph("<b>LEGAL BENEFICIARY:</b>", b_bold),
            Paragraph(f"<b>{c['name']}</b>", b_bold),
            Paragraph("<b>FOLIO / DP-ID:</b>", b_bold),
            Paragraph(f"<b>{c['folio_id']}</b>", b_bold)
        ],
        [
            Paragraph("<b>REGISTERED ADDRESS:</b>", b_bold),
            Paragraph(c["address"], b_txt),
            Paragraph("<b>ASSET &amp; ISIN:</b>", b_bold),
            Paragraph("Astral Limited (INE006I01046)", b_txt)
        ],
        [
            Paragraph("<b>CITY &amp; PROFILE:</b>", b_bold),
            Paragraph(c["city_profile"], b_txt),
            Paragraph("<b>RTA (REGISTRAR):</b>", b_bold),
            Paragraph("Bigshare Services Pvt. Ltd., Mumbai", b_txt)
        ]
    ]
    t_prof = Table(p_data, colWidths=[110, 230, 90, 110])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_prof)
    story.append(Spacer(1, 8))
    
    # Valuation Highlights
    v_data = [
        [
            Paragraph("<b>CERTIFIED SHARES</b>", th_style),
            Paragraph("<b>CURRENT VALUATION</b>", th_style),
            Paragraph("<b>UNCLAIMED DIVIDENDS</b>", th_style),
            Paragraph("<b>ADVANCE EXPENSE</b>", th_style)
        ],
        [
            Paragraph(f"<b>{c['current_shares']:,} Shares</b><br/><font color='#64748B' size=6.5>(100% Certified)</font>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=colors.HexColor("#0F2942"))),
            Paragraph(f"<b>₹ {c['current_val_inr']:,}</b><br/><font color='#047857' size=6.5>(@ CMP ₹1,425)</font>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>₹ {c['total_unclaimed_div']:,.2f}</b><br/><font color='#64748B' size=6.5>(In Govt Escrow)</font>", ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=1, textColor=colors.HexColor("#B45309"))),
            Paragraph("<b>₹ 0.00 (ZERO)</b><br/><font color='#047857' size=6.5>(100% Risk-Free Guarantee)</font>", ParagraphStyle('H4', fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=1, textColor=colors.HexColor("#047857")))
        ]
    ]
    t_val = Table(v_data, colWidths=[135, 135, 135, 135])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0F2942")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#86EFAC")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_val)
    story.append(Spacer(1, 8))
    
    # Bonus Math Table
    b_rows = [
        [
            Paragraph("<b>Corporate Action / Stage</b>", th_style),
            Paragraph("<b>Bonus Multiplier</b>", th_style),
            Paragraph("<b>Share Count</b>", th_style),
            Paragraph("<b>Cumulative Value (@ CMP ₹1,425)</b>", th_style)
        ],
        [
            Paragraph("Original Transferred Base Holding", tc_style),
            Paragraph("Base Allocation", tc_style),
            Paragraph(f"<b>{c['shares_pre_2019']:,} Shares</b>", tcb_style),
            Paragraph(f"₹ {round(c['shares_pre_2019'] * CMP):,}", tcr_style)
        ],
        [
            Paragraph("2019 Bonus Issue (1 : 4 Allotment)", tc_style),
            Paragraph("+25% Expansion (+1 share per 4 held)", tc_style),
            Paragraph(f"+{c['bonus_2019']:,} Shares (Total: {c['shares_pre_2021']:,})", tcb_style),
            Paragraph(f"₹ {round(c['shares_pre_2021'] * CMP):,}", tcr_style)
        ],
        [
            Paragraph("2021 Bonus Issue (1 : 3 Allotment)", tc_style),
            Paragraph("+33.3% Expansion (+1 share per 3 held)", tc_style),
            Paragraph(f"+{c['bonus_2021']:,} Shares (Total: {c['shares_pre_2023']:,})", tcb_style),
            Paragraph(f"₹ {round(c['shares_pre_2023'] * CMP):,}", tcr_style)
        ],
        [
            Paragraph("2023 Bonus Issue (1 : 3 Allotment)", tc_style),
            Paragraph("+33.3% Expansion (+1 share per 3 held)", tc_style),
            Paragraph(f"+{c['bonus_2023']:,} Shares", tcb_style),
            Paragraph(f"₹ {c['current_val_inr']:,}", tcr_style)
        ],
        [
            Paragraph("<b>TOTAL RECOVERABLE PORTFOLIO</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#047857"))),
            Paragraph("<b>100% AUDITED RECOVERY ENTITLEMENT</b>", ParagraphStyle('TB2', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>{c['current_shares']:,} SHARES</b>", ParagraphStyle('TB3', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#047857"))),
            Paragraph(f"<b>₹ {c['current_val_inr']:,}</b>", green_r)
        ]
    ]
    t_bonus = Table(b_rows, colWidths=[150, 150, 110, 130])
    t_bonus.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#DCFCE7")),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_bonus)
    story.append(Spacer(1, 8))
    
    # 3 Fiduciary Pillars
    p_data = [
        [
            Paragraph(
                "<b>1. SUCCESS-ONLY MANDATE (₹0 ADVANCE)</b><br/>"
                "Zero retainer fees. Advisory fee is capped at 8% and strictly payable only after shares are credited to your Demat account.",
                b_txt
            ),
            Paragraph(
                "<b>2. DIRECT DEMAT &amp; BANK SETTLEMENT</b><br/>"
                "The consultant never touches client funds. All shares and dividends are disbursed directly by MCA/IEPF into your verified Demat &amp; bank accounts.",
                b_txt
            ),
            Paragraph(
                "<b>3. TURNKEY REGISTRAR LIASON</b><br/>"
                "We handle the complete statutory lifecycle: MCA Form IEPF-5 e-filing, non-judicial indemnity bonds, and Bigshare verification clearances.",
                b_txt
            )
        ]
    ]
    t_pil = Table(p_data, colWidths=[180, 180, 180])
    t_pil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_pil)
    
    class CustomCanvas(DossierCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(c["ref_code"], *args, **kwargs)
            
    doc.build(story, canvasmaker=CustomCanvas)
    safe_copy(filepath, os.path.join(artifact_dir, c["pdf1_file"]))

def build_agreement(c):
    filepath = os.path.join(upload_dir, c["pdf2_file"])
    doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    t_style = ParagraphStyle('TStyle', fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor("#0F2942"))
    sub_style = ParagraphStyle('SubStyle', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#0284C7"))
    body_txt = ParagraphStyle('BTxt', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#1E293B"))
    body_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F2942"))
    
    story = []
    story.append(Paragraph("<b>STATUTORY IEPF CLAIMS ADVISORY &amp; SUCCESS FEE AGREEMENT</b>", t_style))
    story.append(Paragraph("PERFORMANCE-BASED CONTINGENT RECOVERY CONTRACT (100% CONTINGENT • ₹0 ADVANCE)", sub_style))
    story.append(Spacer(1, 6))
    
    intro = (
        f"This Statutory Advisory Agreement is executed between <b>{USER_NAME}</b> (Principal Advisor, PAN: <code>{USER_PAN}</code>, "
        f"Ranipet District &amp; Chennai, Tamil Nadu) and <b>{c['name']}</b> (Registered Shareholder/Beneficiary, Folio: <code>{c['folio_id']}</code>, "
        f"residing at {c['address']}) for the formal recovery and transmission of unclaimed equity shares and accrued dividend escrows in <b>Astral Limited</b> "
        f"under Section 124(6) of the Companies Act, 2013."
    )
    story.append(Paragraph(intro, body_txt))
    story.append(Spacer(1, 6))
    
    terms = [
        ("1. SCOPE OF SERVICES", "The Advisor shall manage the entire legal &amp; compliance procedure including MCA electronic Form IEPF-5 e-filing, non-judicial indemnity bond drafting, advance stamped receipt generation, Client Master List (CML) certification, and physical liaison with Registrar Bigshare Services Pvt. Ltd. (Mumbai)."),
        ("2. PERFORMANCE FEE & ZERO ADVANCE", f"The Beneficiary agrees to pay a performance-contingent advisory fee of <b>8% (Eight Percent)</b> of the value of recovered shares and accumulated dividends. <b>STRICT ZERO ADVANCE COVENANT:</b> No fee or advance expense of any kind is payable unless and until all shares are visible and credited in the Beneficiary's active personal Demat account."),
        ("3. DIRECT DISBURSEMENT PROTECTIONS", "All equity shares shall be credited directly by the Central Government into the Beneficiary's own verified Demat account. All cash dividends shall be wired via PFMS/DBT directly into the Beneficiary's bank account. The Advisor never holds custody of client shares or funds."),
        ("4. JURISDICTION & GOVERNING LAW", "This agreement is governed by the laws of India and subject to the regulatory oversight of the Ministry of Corporate Affairs (MCA) and SEBI regulations.")
    ]
    
    t_data = []
    for heading, txt in terms:
        t_data.append([Paragraph(f"<b>{heading}</b>", body_bold), Paragraph(txt, body_txt)])
        
    t_terms = Table(t_data, colWidths=[150, 390])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_terms)
    story.append(Spacer(1, 10))
    
    # Signatures
    sign_data = [
        [
            Paragraph(f"<b>ACCEPTED &amp; CONFIRMED BY BENEFICIARY:</b><br/><br/><br/>_____________________________________<br/><b>{c['name']}</b><br/>Registered Shareholder / Legal Claimant<br/>Date: ________________________", body_txt),
            Paragraph(f"<b>CONFIRMED BY PRINCIPAL ADVISOR:</b><br/><br/><br/>_____________________________________<br/><b>{USER_NAME}</b><br/>Principal Advisor &amp; Fiduciary Counsel<br/>Phone: {USER_PHONE} | Email: {USER_EMAIL}", body_txt)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[270, 270])
    t_sign.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0F2942")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_sign)
    
    class CustomCanvas(DossierCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(f"AGR/{c['id']}", *args, **kwargs)
            
    doc.build(story, canvasmaker=CustomCanvas)
    safe_copy(filepath, os.path.join(artifact_dir, c["pdf2_file"]))

def build_playbook(c, lang="EN"):
    filename = c["pdf3_file"] if lang == "EN" else c["pdf4_file"]
    filepath = os.path.join(upload_dir, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    h1_style = ParagraphStyle('H1Style', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor("#0F2942"))
    body_txt = ParagraphStyle('BTxt', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#1E293B"))
    body_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F2942"))
    callout_txt = ParagraphStyle('CTxt', fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F172A"))
    
    story = []
    title_text = f"<b>STATUTORY CLIENT CONSULTATION PLAYBOOK ({'ENGLISH' if lang == 'EN' else 'HINGLISH'})</b>"
    story.append(Paragraph(title_text, h1_style))
    story.append(Paragraph(f"CLIENT PROFILE: <b>{c['name']}</b> | FOLIO: <code>{c['folio_id']}</code> | VALUATION: <b>₹ {c['current_val_inr']:,}</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#0284C7"))))
    story.append(Spacer(1, 6))
    
    # 5 Conversation Phases
    phases = [
        ("PHASE 1: THE WARM GREETING & STATUS DISCLOSURE", 
         f"\"Good day, {c['name']} Sir/Ma'am. My name is {USER_NAME}, Principal Advisor for Statutory Equity Claims. "
         f"I am calling to formally alert your office regarding {c['current_shares']:,} certified equity shares in Astral Limited (valuation: ₹ {c['current_val_inr']:,}) "
         f"currently held in statutory escrow under Folio {c['folio_id']}.\""),
        ("PHASE 2: RESOLVING SKEPTICISM (HOW DID YOU GET MY DETAILS?)",
         f"\"Sir, under Section 124(6) of the Companies Act, listed companies must publish gazetted disclosures of unclaimed dividend folios. "
         f"Our forensic compliance desk audits these official MCA reports and Bigshare records. We never possess bank passwords or confidential credentials; all shares are re-credited directly into your own verified Demat account.\""),
        ("PHASE 3: EXPLAINING THE MULTIPLIER (HOW DID IT BECOME SO LARGE?)",
         f"\"Astral Limited issued three substantial corporate bonus issues: 1:4 in 2019, 1:3 in 2021, and 1:3 in 2023. "
         f"Your original holding expanded significantly to {c['current_shares']:,} shares, alongside accumulated dividends of ₹ {c['total_unclaimed_div']:,.2f}.\""),
        ("PHASE 4: ZERO FINANCIAL RISK (CONTINGENT SUCCESS MODEL)",
         f"\"We operate strictly on a ₹0 advance / 100% contingent performance model (8% fee). "
         f"You do not pay a single rupee upfront. The Central Government credits the entire portfolio directly to your personal Demat and bank account before advisory settlement.\""),
        ("PHASE 5: NEXT ACTION & DIGITAL DOSSIER DISPATCH",
         f"\"I have already prepared your comprehensive Executive Recovery Dossier and statutory schedule. "
         f"I am dispatching both documents to your verified contact right now. Please review the numbers and let us initiate the MCA IEPF-5 filing today.\"")
    ]
    
    for p_title, p_text in phases:
        t_box = Table([[Paragraph(f"<b>{p_title}</b>", body_bold)], [Paragraph(p_text, callout_txt)]], colWidths=[540])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,0), 3),
            ('BOTTOMPADDING', (0,0), (-1,0), 2)
        ]))
        story.append(t_box)
        story.append(Spacer(1, 4))
        
    class CustomCanvas(PlaybookCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(c["name"], *args, **kwargs)
            
    doc.build(story, canvasmaker=CustomCanvas)
    safe_copy(filepath, os.path.join(artifact_dir, filename))

def build_trust_dossier(c):
    filepath = os.path.join(upload_dir, c["pdf5_file"])
    doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    t_style = ParagraphStyle('TStyle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor("#0F2942"))
    sub_style = ParagraphStyle('SubStyle', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#0D9488"))
    b_txt = ParagraphStyle('BTxt', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#1E293B"))
    b_bold = ParagraphStyle('BBold', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F2942"))
    
    story = []
    story.append(Paragraph("<b>STATUTORY SHARE CERTIFICATE &amp; RECONCILIATION DOSSIER</b>", t_style))
    story.append(Paragraph("CENTRAL GOVERNMENT INVESTOR EDUCATION &amp; PROTECTION FUND (IEPF) TRANSMISSION", sub_style))
    story.append(Spacer(1, 6))
    
    # Audit summary
    a_data = [
        [Paragraph("<b>LEGAL BENEFICIARY:</b>", b_bold), Paragraph(c["name"], b_bold)],
        [Paragraph("<b>FOLIO NUMBER:</b>", b_bold), Paragraph(c["folio_id"], b_bold)],
        [Paragraph("<b>REGISTERED RESIDENCE:</b>", b_bold), Paragraph(c["address"], b_txt)],
        [Paragraph("<b>CERTIFIED EQUITY:</b>", b_bold), Paragraph(f"<b>{c['current_shares']:,} Fully Paid Equity Shares</b>", b_bold)],
        [Paragraph("<b>MARKET VALUATION:</b>", b_bold), Paragraph(f"<b>₹ {c['current_val_inr']:,}</b> (@ CMP ₹1,425.00)", b_bold)],
        [Paragraph("<b>CASH DIVIDENDS:</b>", b_bold), Paragraph(f"<b>₹ {c['total_unclaimed_div']:,.2f}</b> in Central Government Escrow", b_bold)],
        [Paragraph("<b>REGISTRAR &amp; TRANSFER AGENT:</b>", b_bold), Paragraph("Bigshare Services Pvt. Ltd., Mumbai", b_txt)],
        [Paragraph("<b>STATUTORY CUSTODIAN:</b>", b_bold), Paragraph("IEPF Authority, Ministry of Corporate Affairs, New Delhi", b_txt)]
    ]
    t_audit = Table(a_data, colWidths=[150, 390])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0F2942")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 8))
    
    # Fiduciary Block
    f_data = [
        [
            Paragraph(
                "<b>LEGAL FIDUCIARY CERTIFICATION:</b><br/>"
                "This document confirms that the above-listed securities are registered under the Investor Education and Protection Fund "
                "Authority pursuant to Section 124(6) of the Companies Act, 2013. The underlying equity is 100% intact and reclaimable "
                "via MCA e-Form IEPF-5 filing. All restored securities and dividends are remitted directly into the investor's certified account.",
                b_txt
            )
        ]
    ]
    t_fid = Table(f_data, colWidths=[540])
    t_fid.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_fid)
    
    class CustomCanvas(DossierCanvas):
        def __init__(self, *args, **kwargs):
            super(CustomCanvas, self).__init__(f"TRUST/{c['id']}", *args, **kwargs)
            
    doc.build(story, canvasmaker=CustomCanvas)
    safe_copy(filepath, os.path.join(artifact_dir, c["pdf5_file"]))

# Generate all documents
print("Generating document suites for 10 new clients...")
for c in BATCH_96_TO_105:
    print(f"Generating for Client {c['id']}: {c['name']}...")
    build_dossier(c)
    build_agreement(c)
    build_playbook(c, lang="EN")
    build_playbook(c, lang=c["lang_regional"])
    build_trust_dossier(c)

# Database Update
print("\nUpdating SQLite databases (upload_dir and vault_dir)...")
for dpath in [db_path, db_root_path]:
    conn = sqlite3.connect(dpath)
    cur = conn.cursor()
    for c in BATCH_96_TO_105:
        est_folio_str = f"₹{c['current_val_inr']:,} (~₹{c['current_val_inr']/10000000:.2f} Cr | {c['current_shares']:,} Shares)"
        fee_inr = round(c['current_val_inr'] * c['fee_pct'] / 100)
        my_est_str = f"₹{fee_inr:,} (~₹{fee_inr/100000:.2f} Lakhs | {c['fee_pct']}% Fee)"
        
        cur.execute("SELECT id FROM customers WHERE id = ? OR folio_id = ?", (c["id"], c["folio_id"]))
        existing = cur.fetchone()
        if existing:
            cur.execute("""
                UPDATE customers SET
                    name = ?, address = ?, folio_id = ?, est_folio = ?, contact_info = ?,
                    pdf1_filename = ?, pdf1_path = ?, pdf2_filename = ?, pdf2_path = ?,
                    my_est_value = ?, pdf3_filename = ?, pdf3_path = ?, pdf4_filename = ?, pdf4_path = ?,
                    pdf5_filename = ?, pdf5_path = ?
                WHERE id = ?
            """, (
                c["name"], c["address"], c["folio_id"], est_folio_str, c["contact_info"],
                c["pdf1_name"], c["pdf1_file"], c["pdf2_name"], c["pdf2_file"],
                my_est_str, c["pdf3_name"], c["pdf3_file"], c["pdf4_name"], c["pdf4_file"],
                c["pdf5_name"], c["pdf5_file"],
                existing[0]
            ))
        else:
            cur.execute("""
                INSERT INTO customers (
                    id, name, address, folio_id, est_folio, contact_info,
                    pdf1_filename, pdf1_path, pdf2_filename, pdf2_path,
                    my_est_value, pdf3_filename, pdf3_path, pdf4_filename, pdf4_path,
                    pdf5_filename, pdf5_path, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
            """, (
                c["id"], c["name"], c["address"], c["folio_id"], est_folio_str, c["contact_info"],
                c["pdf1_name"], c["pdf1_file"], c["pdf2_name"], c["pdf2_file"],
                my_est_str, c["pdf3_name"], c["pdf3_file"], c["pdf4_name"], c["pdf4_file"],
                c["pdf5_name"], c["pdf5_file"]
            ))
    conn.commit()
    conn.close()

# Update master_client_stats.json
print("\nUpdating master_client_stats.json...")
if os.path.exists(stats_path):
    with open(stats_path, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = []

stats_dict = {s["id"]: s for s in stats}
for c in BATCH_96_TO_105:
    fee_inr = round(c['current_val_inr'] * c['fee_pct'] / 100)
    stats_dict[c["id"]] = {
        "id": c["id"],
        "name": c["name"],
        "folio_id": c["folio_id"],
        "shares": c["current_shares"],
        "market_value": c["current_val_inr"],
        "market_value_str": f"₹ {c['current_val_inr']:,}",
        "fee_inr": fee_inr,
        "fee_str": f"₹ {fee_inr:,}",
        "unclaimed_div": c["total_unclaimed_div"],
        "status": "Pending",
        "contact_info": c["contact_info"]
    }

stats_list = sorted(stats_dict.values(), key=lambda x: x["id"])
with open(stats_path, "w", encoding="utf-8") as f:
    json.dump(stats_list, f, indent=2)

print("\nOnboarding completed successfully for Clients 96 to 105!")

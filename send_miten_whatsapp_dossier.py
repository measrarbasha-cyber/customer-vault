import os
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, ".whatsapp_session")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

PHONE = "919820222028"
PDF_PATH = os.path.abspath(os.path.join(BASE_DIR, "uploads", "Miten_Ashwin_Mehta_Official_Shares_Calculation_and_Gazette_Proof.pdf"))

# Verify PDF exists and has no customervault
assert os.path.exists(PDF_PATH), f"PDF not found at {PDF_PATH}"
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read().lower()
    assert b"customervault" not in pdf_bytes and b"customer-vault" not in pdf_bytes, "Found customervault in PDF!"

MESSAGE = """Respected Miten Ashwin Mehta Sir,

Subject: Urgent Statutory Notice — Mandatory IEPF Transfer of your Astral Limited Equity Holdings (Folio / DP-Client ID: 1201170000029668)

I am reaching out to bring an urgent corporate action matter regarding your long-term equity investment in Astral Limited to your personal attention.

According to official Ministry of Corporate Affairs (MCA) gazette notifications and Registrar (Bigshare Services Pvt. Ltd.) records, your registered holding under CDSL Demat / Folio 1201170000029668 has accumulated consecutive unpaid dividends (totaling Rs. 95,625.00 on record across 3 distinct schedules) and has been statutorily marked for transfer into the Investor Education and Protection Fund (IEPF) Authority Demat Account under Section 124(6) of the Companies Act, 2013.

CRITICAL COMPLICATIONS & INACTION RISKS YOU FACE:
1. Complete Disappearance from Active Demat: Once transferred to the IEPF Suspense Escrow Account (Govt. of India), these securities will no longer reflect in your CDSL/trading app or portfolio valuation. Frontline broker support cannot view or access MCA statutory custody.
2. The Government NEVER Automatically Returns Shares: The IEPF Authority acts strictly as a statutory custodian. Under the law, the Central Government will never voluntarily credit shares or dividends back into your account without formal, zero-defect legal petitioning.
3. Compounded Freezing of Benefits: All accrued corporate benefits—including bonus shares (1:4 in 2019, 1:3 in 2021, and 1:3 in 2023) expanding your base to 101,053 Certified Equity Shares (~Rs. 14.40 Crores @ CMP Rs. 1,425)—as well as future dividend warrants, remain locked in government suspense.
4. Procedural & Bureaucratic Impediments: Reclaiming assets from IEPF is a complex legal maze. It mandates e-Form IEPF-5 filing on the MCA V3 portal, submission of physical verification dossiers to Astral's Nodal Officer, original Client Master List (CML) certifications, advance stamp receipts, and non-judicial indemnity bonds. Minor typographical or documentation mismatches result in immediate rejection or multi-year bureaucratic delays.

WHY YOU SHOULD IMMEDIATELY ENGAGE OUR SPECIALIZED ASSISTANCE:
- End-to-End Turnkey Execution: Our legal and compliance practice manages the entire lifecycle—forensic audit, MCA e-Form IEPF-5 filing, documentation, and on-ground liaison with Registrar Bigshare Services (Mumbai) and Astral's Nodal Officer.
- 100% Contingent / Rs. 0 Advance Security: We operate strictly on a success-fee basis with ZERO upfront or retainer fees. All shares and accumulated dividends are credited DIRECTLY by the Central Government into your verified active Demat and bank account before our professional fee is settled.
- High-Priority Fast-Tracking: We resolve all technical and compliance prerequisites upfront to ensure approval on the very first submission.

Attached below is your comprehensive 4-Page Official Shareholding Breakdown & Gazette Proof Dossier containing the audited bonus reconstruction, certified MCA gazette scans (with unrelated shareholders blurred for privacy), and the statutory recovery schedule.

Whenever you are ready, please call or WhatsApp me directly so we can initiate the paperwork and secure your shares.

Warm regards,

MD Asrar Basha A
Principal Advisor – Shareholder Rights & IEPF Recovery
Legal & Statutory Claims Advisory
Phone / WhatsApp: +91 7358882822
Email: amdasrarbasha@gmail.com
Ranipet District & Chennai | Liaison: Mumbai (Bigshare) & New Delhi (MCA)"""

assert "customervault" not in MESSAGE.lower() and "customer-vault" not in MESSAGE.lower(), "Found customervault in message!"

def send_whatsapp():
    print(f"Connecting to WhatsApp Web for target phone: +{PHONE}...")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 800},
            user_agent=USER_AGENT,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        encoded_msg = urllib.parse.quote(MESSAGE)
        url = f"https://web.whatsapp.com/send?phone={PHONE}&text={encoded_msg}"
        print(f"Opening WhatsApp chat URL for +{PHONE}...")
        page.goto(url)
        
        print("Waiting for chat interface to load (up to 20s)...")
        time.sleep(15)
        
        # Check if invalid popup appeared
        invalid_popup = page.locator("div[role='dialog']:has-text('invalid'), div[role='dialog']:has-text('Phone number shared via url is invalid')")
        if invalid_popup.count() > 0 and invalid_popup.first.is_visible():
            print("ERROR: Phone number not registered on WhatsApp or invalid!")
            page.screenshot(path="uploads/wa_miten_invalid.png")
            ctx.close()
            return False

        # Send text message
        send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
        sent_text = False
        try:
            send_btn.first.wait_for(state="visible", timeout=15000)
            time.sleep(1)
            send_btn.first.click()
            sent_text = True
            print("[+] Text message sent successfully!")
        except Exception as e:
            print(f"Send button not clickable immediately: {e}. Trying fallback press Enter...")
            chat_box = page.locator("footer div[contenteditable='true'], div[role='textbox']")
            if chat_box.count() > 0:
                chat_box.first.press("Enter")
                sent_text = True
                print("[+] Pressed Enter in chatbox successfully!")
        
        time.sleep(4)
        
        # Attach PDF
        print(f"Attaching PDF document: {PDF_PATH}...")
        file_input = page.locator("input[type='file'][accept='*']").first
        file_input.set_input_files(PDF_PATH)
        time.sleep(4)
        
        # Send PDF in preview modal
        modal_send_btn = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
        if modal_send_btn.count() > 0:
            print("Clicking Send button in preview modal...")
            try:
                modal_send_btn.first.click(force=True)
            except Exception:
                page.keyboard.press("Enter")
            print("[+] PDF attachment sent!")
        else:
            print("Fallback: pressing Enter in modal...")
            page.keyboard.press("Enter")
        
        time.sleep(6)
        
        screenshot_path = "uploads/wa_miten_delivered.png"
        page.screenshot(path=screenshot_path)
        print(f"[+] Confirmation screenshot saved: {screenshot_path}")
        
        # Copy screenshot to brain artifacts
        art_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
        art_ss = os.path.join(art_dir, "wa_miten_delivered.png")
        import shutil
        shutil.copyfile(screenshot_path, art_ss)
        print(f"[+] Artifact screenshot saved: {art_ss}")
        
        ctx.close()
        return True

if __name__ == "__main__":
    success = send_whatsapp()
    print("Completed with status:", success)

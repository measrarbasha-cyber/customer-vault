import os
import sys
import time
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

assert os.path.exists(PDF_PATH), f"PDF not found at {PDF_PATH}"
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read().lower()
    assert b"customervault" not in pdf_bytes and b"customer-vault" not in pdf_bytes, "Found customervault in PDF!"

def attach_pdf_to_miten():
    print(f"Connecting to WhatsApp Web to attach PDF for +{PHONE}...")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 800},
            user_agent=USER_AGENT,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        # Navigate to existing chat
        url = f"https://web.whatsapp.com/send?phone={PHONE}"
        print(f"Opening chat: {url}...")
        page.goto(url)
        time.sleep(15)
        
        # Check if chat loaded
        print("Looking for attach button...")
        attach_btn = page.locator("[data-icon='plus'], [aria-label='Attach'], div[title='Attach'], button[title='Attach']").first
        attach_btn.wait_for(state="visible", timeout=20000)
        attach_btn.click()
        time.sleep(2)
        
        print("Opening file chooser for Document...")
        with page.expect_file_chooser(timeout=10000) as fc_info:
            doc_btn = page.locator("[aria-label='Document'], li:has-text('Document')").first
            doc_btn.click()

        file_chooser = fc_info.value
        print(f"Uploading file: {PDF_PATH}...")
        file_chooser.set_files(PDF_PATH)
        time.sleep(4)
        
        # Click send in preview modal
        print("Looking for send button in preview modal...")
        modal_send = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']").first
        try:
            modal_send.wait_for(state="visible", timeout=10000)
            modal_send.click(force=True)
            print("[+] Clicked Send button in modal!")
        except Exception as e:
            print(f"Send button wait error: {e}. Pressing Enter...")
            page.keyboard.press("Enter")
            
        time.sleep(7)
        
        screenshot_path = "uploads/wa_miten_delivered.png"
        page.screenshot(path=screenshot_path)
        print(f"[+] Confirmation screenshot saved: {screenshot_path}")
        
        # Copy to brain artifacts
        art_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
        art_ss = os.path.join(art_dir, "wa_miten_delivered.png")
        import shutil
        shutil.copyfile(screenshot_path, art_ss)
        print(f"[+] Artifact screenshot saved: {art_ss}")
        
        ctx.close()
        return True

if __name__ == "__main__":
    success = attach_pdf_to_miten()
    print("Attachment status:", success)

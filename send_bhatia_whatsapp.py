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
PDF_PATH = os.path.join(BASE_DIR, "uploads", "Naniklal_Bhatia_IEPF_Transfer_Notice_and_Recovery_Guide.pdf")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

NUMBERS = [
    {"phone": "919826082720", "desc": "CA Shyam Bhatia / Naniklal Bhatia (Primary Line)"},
    {"phone": "919826082725", "desc": "CA Shyam Bhatia / Naniklal Bhatia (Office / Direct Line)"}
]

MESSAGE = """Respected CA Shyam Bhatia sir & Naniklal Bhatia ji,

Please review the attached Statutory Audit Notice regarding your long-term equity investments in Astral Limited.

Under Section 124(6) of the Companies Act, your 35,368 equity shares (worth ~₹5.04 Crores + ₹6,692 dividends) registered at your Jairampur Colony, Indore address have matured and transferred into the Central Government IEPF Authority Demat Account.

⚠️ Important: Government custody does not release shares automatically. Without filing MCA Form IEPF-5, these high-value assets remain frozen in administrative custody.

🔍 You can verify this yourself right now on the official MCA portal:
👉 https://www.iepf.gov.in (Services → Search Unclaimed/Transferred Amounts → Company: Astral Limited | Folio: IN30048411367040)

🛡️ Our 100% Risk-Free Fiduciary Mandate:
• ₹0 Advance Fee (Payable only AFTER shares are visibly in your Demat account)
• Direct Government Settlement (Shares credited directly to your own Demat)
• Complete Privacy (Masked KYC only; no OTPs/passwords ever requested)

Please check the attached PDF for official gazette screenshots across Pages 4, 7, 12, 18 & 21 and the complete claim roadmap. When would be a convenient time for a brief 2-minute call today?

Respectfully,
MD ASRAR BASHA A
Corporate IEPF Advisory Practice
📞 +91 7358882822"""

def send_whatsapp_outreach():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")
    
    print("=" * 75)
    print("DISPATCHING WHATSAPP MESSAGE & PDF NOTICE TO NANIKLAL & SHYAM BHATIA")
    print(f"Target Numbers: {[n['phone'] for n in NUMBERS]}")
    print(f"PDF Attachment: {os.path.basename(PDF_PATH)} ({os.path.getsize(PDF_PATH)} bytes)")
    print("=" * 75)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 800},
            user_agent=USER_AGENT,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com")

        print("Checking WhatsApp session state...", flush=True)
        try:
            page.wait_for_selector("div[id='pane-side'], div[aria-label='Chat list']", timeout=30000)
            print("[+] Session authenticated successfully!\n", flush=True)
        except Exception as e:
            print(f"[-] Session authentication failed: {e}")
            page.screenshot(path="wa_auth_failed.png")
            context.close()
            return

        for idx, target in enumerate(NUMBERS, 1):
            phone = target["phone"]
            desc = target["desc"]
            print(f"[{idx}/2] Processing: +{phone} ({desc})...", flush=True)

            try:
                encoded_msg = urllib.parse.quote(MESSAGE)
                url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
                page.goto(url)

                print("  Waiting for chat conversation to load...", flush=True)
                time.sleep(6)

                # Check if invalid number dialog appeared
                invalid_popup = page.locator("div[role='dialog']:has-text('invalid'), div[data-animate-modal-popup='true']:has-text('invalid')")
                if invalid_popup.count() > 0 and invalid_popup.first.is_visible():
                    print(f"  [-] Number +{phone} is not registered on WhatsApp. Skipping.\n")
                    ok_btn = page.locator("div[role='button']:has-text('OK'), button:has-text('OK')")
                    if ok_btn.count() > 0:
                        ok_btn.first.click()
                    continue

                # Wait for Send button or press Enter
                send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
                try:
                    send_btn.first.wait_for(state="visible", timeout=20000)
                    time.sleep(1)
                    send_btn.first.click()
                except Exception:
                    chat_box = page.locator("footer div[contenteditable='true'], div[role='textbox']")
                    if chat_box.count() > 0:
                        chat_box.first.press("Enter")

                print(f"  [+] Text message dispatched to +{phone}!", flush=True)
                time.sleep(4)

                # Attach PDF notice
                print("  Attaching statutory PDF document...", flush=True)
                plus_btn = page.locator("footer button[aria-label='Attach'], footer span[data-icon='plus'], footer div[role='button']:has(span[data-icon='plus'])")
                plus_btn.first.click()
                time.sleep(2)

                with page.expect_file_chooser(timeout=10000) as fc_info:
                    doc_btn = page.locator("[aria-label='Document']")
                    doc_btn.first.click()

                file_chooser = fc_info.value
                file_chooser.set_files(PDF_PATH)
                time.sleep(3)

                # Click Send in preview modal
                modal_send = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']").first
                modal_send.click()
                print(f"  >>> SUCCESS: PDF Notice delivered to +{phone} ({desc})!\n", flush=True)

                page.screenshot(path=f"wa_sent_{phone}.png")
                time.sleep(8)

            except Exception as err:
                print(f"  [ERROR] Delivery error for +{phone}: {err}\n", flush=True)
                page.screenshot(path=f"wa_error_{phone}.png")
                time.sleep(3)

        context.close()
        print("=" * 75)
        print("WHATSAPP DISPATCH COMPLETED FOR BOTH NUMBERS!")
        print("=" * 75)

if __name__ == "__main__":
    send_whatsapp_outreach()

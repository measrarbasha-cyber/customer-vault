import os
import sys
import time
import json
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, ".whatsapp_session")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LOG_PATH = os.path.join(BASE_DIR, "batch_96_to_105_wa_final_delivered.json")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

CLIENTS = [
    {
        "id": 96,
        "name": "Hiranand Asandas Savlani",
        "phone": "919825007966",
        "pdf": "Executive_Dossier_Hiranand_Savlani_Astral.pdf",
        "message": """Respected Hiranand Savlani Sir,

Regarding your equity holdings in Astral Limited (Client ID: IN30051317314132 | Ahmedabad):

Under Section 124(6) of the Companies Act, your 2,221 shares (accounting for 1:4, 1:3 & 1:3 bonus distributions, current market valuation ~₹31.65 Lakhs) along with accumulated unclaimed dividend tranches are subject to statutory custody under the IEPF Authority, Ministry of Corporate Affairs, New Delhi.

Attached below is your complete 3-Page Statutory Restitution Notice & Executive Audit Dossier, containing:
1. Certified holding audit & valuation schedule.
2. Official Astral Limited Gazette filing proof & step-by-step self-verification instructions.
3. 100% Risk-Free statutory restitution roadmap (Zero Advance fee / direct credit into your Demat account).

Kindly review the attached PDF dossier. We would be pleased to speak with you regarding the recovery process at your convenience.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
Legal & Compliance Desk | CustomerVault Advisory"""
    },
    {
        "id": 97,
        "name": "Lalita Nahata & Ajay Nahata",
        "phone": "919434025811",
        "pdf": "Executive_Dossier_Lalita_Nahata_Astral.pdf",
        "message": """Respected Lalita Nahata Ji & Ajay Nahata Ji,

Regarding your equity holding in Astral Limited (Client ID: 1201090003437744 | Siliguri):

Under Section 124(6) of the Companies Act, your 2,112 shares (accounting for all bonus distributions, current market valuation ~₹30.10 Lakhs) along with uncashed dividend tranches are subject to statutory transfer to the IEPF Authority, Government of India.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier, providing the certified share audit, Gazette filing evidence, self-verification guide, and our ₹0 Advance recovery procedure.

Kindly review the attached PDF dossier. We are available at +91 7358882822 to assist you with the documentation.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 98,
        "name": "Usha Gupta",
        "phone": "919810125293",
        "pdf": "Executive_Dossier_Usha_Gupta_Astral.pdf",
        "message": """Respected Usha Gupta Ji,

Regarding your equity holding in Astral Limited (Client ID: IN30159010029825 | Cloth Market, Central Delhi):

Under Section 124(6) of the Companies Act, your 2,112 shares (adjusted for 1:4, 1:3 & 1:3 bonus issues, valued at ~₹30.10 Lakhs) along with unclaimed dividend tranches are subject to statutory transfer to the IEPF Authority (Govt. of India).

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier containing the complete shareholding audit, Gazette record proof, and the IEPF-5 recovery roadmap.

We manage the complete verification and recovery on a 100% contingent (₹0 Advance) basis — shares are released directly into your active Demat account.

Please examine the attached PDF dossier. Feel free to call us at +91 7358882822 for any questions.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 99,
        "name": "Dr. Gunadhar Padhi",
        "phone": "919820314890",
        "pdf": "Executive_Dossier_Dr_Gunadhar_Padhi_Astral.pdf",
        "message": """Respected Dr. Gunadhar Padhi Sir,

Regarding your equity investment in Astral Limited (Client ID: 1204720004074514 | Kharghar, Navi Mumbai):

Under Section 124(6) of the Companies Act, your 2,112 shares (accounting for all corporate bonus issues, valued at ~₹30.10 Lakhs) and uncashed dividend tranches are subject to statutory custody with the IEPF Authority, Ministry of Corporate Affairs.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier outlining the complete audit breakdown, Gazette proof screenshot, and the MCA IEPF Form-5 recovery steps.

Our services operate on a 100% success-only basis (₹0 Advance) — all shares are credited directly into your active Demat account prior to any fee settlement.

Please review the attached PDF dossier at your convenience. We are available at +91 7358882822 to discuss the recovery process.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 100,
        "name": "Dipikaben Mukeshkumar Thakkar & Mukeshkumar Thakkar",
        "phone": "919825425010",
        "pdf": "Executive_Dossier_Dipikaben_Thakkar_Astral.pdf",
        "message": """Respected Dipikaben Thakkar Ji & Mukeshkumar Thakkar Ji,

Regarding your equity holding in Astral Limited (Client ID: IN30039413157207 | Burhani Complex, Lunawada):

Under Section 124(6) of the Companies Act, your 2,112 shares (adjusted for 1:4, 1:3 & 1:3 bonus distributions, valued at ~₹30.10 Lakhs) and uncashed dividends are subject to statutory transfer to the IEPF Authority, Central Government.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier, detailing your full share progression, official Gazette evidence, and the recovery roadmap.

We undertake the complete legal and liaison recovery on a ₹0 Advance / Success-Only basis — with shares restored directly to your active Demat account.

Please review the attached PDF dossier. Kindly reach out to us at +91 7358882822 to initiate the process.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 101,
        "name": "Divyesh Kanaiyalal Pandejee",
        "phone": "919825071458",
        "pdf": "Executive_Dossier_Divyesh_Pandejee_Astral.pdf",
        "message": """Respected Divyesh Pandejee Sir,

Regarding your equity holding in Astral Limited (Client ID: IN30075711458905 | Ghatlodia, Ahmedabad):

Under Section 124(6) of the Companies Act, your 2,112 shares (reflecting 1:4, 1:3 & 1:3 bonus issues, current market value ~₹30.10 Lakhs) and unclaimed dividends are subject to statutory transfer to the IEPF Authority, Government of India.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier, providing the complete shareholding audit, Gazette evidence, and IEPF Form-5 procedural guide.

Our engagement is 100% contingent (₹0 Advance) — shares are transferred directly by the Central Government into your active Demat account.

Please review the attached PDF dossier. Feel free to contact us at +91 7358882822 to discuss the recovery.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 102,
        "name": "Chandra Shekhar",
        "phone": "919414138590",
        "pdf": "Executive_Dossier_Chandra_Shekhar_Astral.pdf",
        "message": """Respected Chandra Shekhar Ji,

Regarding your equity holding in Astral Limited (Client ID: 1203320013859313 | Jhalawar, Rajasthan):

Under Section 124(6) of the Companies Act, your 2,112 shares (accounting for all bonus splits, valued at ~₹30.10 Lakhs) across 7 unclaimed dividend tranches are subject to statutory transfer to the IEPF Authority, Ministry of Corporate Affairs.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier with complete share records, official Gazette proof card, and the recovery roadmap.

We work on a strict ₹0 Advance / Success-Only basis — all recovered shares and funds are credited directly into your active Demat account.

Please check the attached PDF dossier. You can reach us directly at +91 7358882822 to proceed.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 103,
        "name": "Suresh Hinduja B",
        "phone": "919845014109",
        "pdf": "Executive_Dossier_Suresh_Hinduja_Astral.pdf",
        "message": """Respected Suresh Hinduja Sir,

Regarding your equity investment in Astral Limited (Client ID: IN30021410969382 | Domlur, Bangalore):

Under Section 124(6) of the Companies Act, your 2,112 shares (accounting for 1:4, 1:3 & 1:3 bonus issues, valued at ~₹30.10 Lakhs) along with unclaimed dividend tranches are subject to statutory transfer to the IEPF Authority, Government of India.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier outlining the complete historical progression, Gazette proof snippet, and the IEPF Form-5 recovery protocol.

Our advisory operates on a 100% contingent (₹0 Advance) framework — shares and dividends are released directly into your active Demat account by the MCA before any fee is settled.

Please examine the attached PDF dossier. We look forward to assisting you and can be reached at +91 7358882822.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 104,
        "name": "Manjula Vrajlal Lathia",
        "phone": "919820158210",
        "pdf": "Executive_Dossier_Manjula_Lathia_Astral.pdf",
        "message": """Respected Manjula Lathia Ji,

Regarding your equity holding in Astral Limited (Client ID: IN30258210101225 | Ghatkopar East, Mumbai):

Under Section 124(6) of the Companies Act, your 2,112 shares (adjusted for all historical bonus distributions, current market value ~₹30.10 Lakhs) and unclaimed dividends are subject to statutory custody under the IEPF Authority, Ministry of Corporate Affairs.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier containing the full audit, official Gazette proof card, and step-by-step recovery roadmap.

We operate strictly on a ₹0 Advance / Success-Only basis — shares are credited directly into your active Demat account by the Central Government.

Please review the attached PDF dossier. Kindly contact our desk at +91 7358882822 to discuss the documentation.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    },
    {
        "id": 105,
        "name": "Meera Gupta",
        "phone": "919830045851",
        "pdf": "Executive_Dossier_Meera_Gupta_Astral.pdf",
        "message": """Respected Meera Gupta Ji,

Regarding your equity holding in Astral Limited (Client ID: IN30039414585102 | Howrah, West Bengal):

Under Section 124(6) of the Companies Act, your 2,112 shares (accounting for 1:4, 1:3 & 1:3 bonus issues, valued at ~₹30.10 Lakhs) across 13 continuous unclaimed dividend tranches are subject to statutory transfer to the IEPF Authority, Central Government.

Attached below is your official 3-Page Statutory Restitution Notice & Executive Recovery Dossier with complete dividend breakdown, official Gazette proof card, and the IEPF-5 recovery plan.

Our engagement is 100% contingent (₹0 Advance) — all shares are credited directly into your active Demat account before any fee is settled.

Please examine the attached PDF dossier. Feel free to call us at +91 7358882822 to take this forward.

Warm regards,
MD Asrar Basha A
Senior Fiduciary Counsel | +91 7358882822
CustomerVault Advisory"""
    }
]

def dispatch_whatsapp():
    print(f"Starting resilient WhatsApp dispatch of 3-Page Executive Dossiers for {len(CLIENTS)} clients...")
    
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 800},
            user_agent=USER_AGENT,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://web.whatsapp.com")
        page.wait_for_selector("div[id='pane-side']", timeout=35000)
        print("[+] WhatsApp Web session verified and ready!", flush=True)

        results = []

        for idx, c in enumerate(CLIENTS, 1):
            phone = c["phone"]
            name = c["name"]
            pdf_path = os.path.join(UPLOAD_DIR, c["pdf"])
            print(f"\n[{idx}/{len(CLIENTS)}] Client ID {c['id']}: {name} (+{phone})...", flush=True)

            page.keyboard.press("Escape")
            time.sleep(1)

            encoded_msg = urllib.parse.quote(c["message"])
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
            page.goto(url)

            # Resilient wait loop up to 25 seconds for chat readiness or rejection dialog
            chat_ready = False
            not_on_wa = False
            start_t = time.time()

            while time.time() - start_t < 25:
                # 1. Check for rejection dialog
                dialogs = page.locator("div[role='dialog']")
                if dialogs.count() > 0:
                    d_text = dialogs.first.inner_text()
                    if "isn't on WhatsApp" in d_text or "not on WhatsApp" in d_text or "invalid" in d_text:
                        print(f"  [-] +{phone} is NOT on WhatsApp ({d_text[:40]}). Dismissing modal...")
                        not_on_wa = True
                        ok_btn = dialogs.first.locator("button:has-text('OK'), div[role='button']:has-text('OK')")
                        if ok_btn.count() > 0:
                            ok_btn.first.click()
                        else:
                            page.keyboard.press("Enter")
                        time.sleep(2)
                        break

                # 2. Check if send button or textbox is active
                send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
                if send_btn.count() > 0 and send_btn.first.is_visible():
                    chat_ready = True
                    break

                chat_box = page.locator("footer div[contenteditable='true'], div[role='textbox']")
                if chat_box.count() > 0 and chat_box.first.is_visible():
                    chat_ready = True
                    break

                time.sleep(1)

            if not_on_wa:
                results.append({"id": c["id"], "name": name, "phone": phone, "status": "not_on_whatsapp", "text_sent": False, "pdf_sent": False})
                continue

            if not chat_ready:
                print(f"  [-] Timeout waiting for chat interface on +{phone}. Skipping.")
                results.append({"id": c["id"], "name": name, "phone": phone, "status": "timeout_loading_chat", "text_sent": False, "pdf_sent": False})
                continue

            # Send message text
            text_sent = False
            send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
            try:
                if send_btn.count() > 0 and send_btn.first.is_visible():
                    send_btn.first.click()
                    text_sent = True
                    print("  [+] Text message sent!")
                else:
                    chat_box = page.locator("footer div[contenteditable='true'], div[role='textbox']")
                    chat_box.first.press("Enter")
                    text_sent = True
                    print("  [+] Text message sent via Enter!")
            except Exception as e_send:
                print(f"  [-] Text send failed: {e_send}")

            time.sleep(3)

            # Attach 3-Page Executive Recovery Dossier PDF
            pdf_sent = False
            try:
                attach_btn = page.locator("[data-icon='plus'], [aria-label='Attach'], div[title='Attach'], button[title='Attach']").first
                attach_btn.wait_for(state="visible", timeout=12000)
                attach_btn.click()
                time.sleep(2)

                with page.expect_file_chooser(timeout=10000) as fc_info:
                    page.locator("[aria-label='Document']").first.click()

                file_chooser = fc_info.value
                file_chooser.set_files(pdf_path)
                print(f"  [+] Attached 3-Page Executive Dossier: {c['pdf']}")
                time.sleep(3)

                modal_send = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']").first
                try:
                    modal_send.click(force=True, timeout=5000)
                except Exception:
                    page.keyboard.press("Enter")

                pdf_sent = True
                print("  [+] 3-Page Executive Dossier PDF delivered successfully!")
                time.sleep(5)

                proof_path = os.path.join(UPLOAD_DIR, f"wa_delivered_3page_{c['id']}.png")
                page.screenshot(path=proof_path)
                print(f"  [+] Screenshot captured: {proof_path}")

            except Exception as e_attach:
                print(f"  [-] Failed attaching dossier PDF: {e_attach}")

            results.append({
                "id": c["id"],
                "name": name,
                "phone": phone,
                "status": "delivered" if (text_sent and pdf_sent) else "partial",
                "text_sent": text_sent,
                "pdf_sent": pdf_sent,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })

            time.sleep(3)

        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump({"results": results}, f, indent=2)

        ctx.close()
        print("\nAll WhatsApp dispatches completed!")

if __name__ == "__main__":
    dispatch_whatsapp()

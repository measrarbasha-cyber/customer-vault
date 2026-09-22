import os
import sys
import re
import time
import json
import sqlite3
import urllib.parse
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customers.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
SESSION_DIR = os.path.join(BASE_DIR, ".whatsapp_session")
REGISTRY_PATH = os.path.join(BASE_DIR, "master_outreach_registry.json")

USER_NAME = "MD ASRAR BASHA A"
USER_PHONE = "+91 7358882822"
USER_TITLE = "Principal Advisor – Shareholder Rights & IEPF Recovery"
USER_FIRM = "Legal & Compliance Desk | CustomerVault Advisory"
USER_LOC = "Ranipet District & Chennai, Tamil Nadu - 632509"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def extract_mobile_number(contact_info):
    if not contact_info:
        return None
    matches = re.findall(r'(?:(?:\+?91)[\s-]?)?([6-9]\d{4}[\s-]?\d{5})', contact_info)
    if matches:
        clean = re.sub(r'\D', '', matches[0])
        return f"91{clean}"
    return None

def build_whatsapp_message(cust):
    name = cust.get("name", "Investor")
    folio = cust.get("folio_id", "Unclaimed Folio")
    est_folio = cust.get("est_folio", "Audited Portfolio")
    
    # STRICT ZERO-LINK POLICY: No URLs or HTTP links anywhere
    msg = (
        f"Namaste {name} ji,\n\n"
        f"I am writing to bring to your attention an important statutory matter regarding your unclaimed equity shares "
        f"in *Astral Limited* (Folio / Demat ID: *{folio}*), currently held under the statutory custody of the Investor Education and "
        f"Protection Fund (IEPF) Authority, Ministry of Corporate Affairs, Government of India.\n\n"
        f"📊 *Audited Valuation Summary:*\n"
        f"• Total Portfolio Value: *{est_folio}*\n"
        f"• Terms: *Rs. 0 Advance Fee* (100% contingent on credit)\n"
        f"• Settlement: Shares & accrued dividends are credited *directly by Central Govt* into your personal Demat & Bank A/C.\n\n"
        f"📄 *Official Executive Recovery Dossier:*\n"
        f"I have attached your official Executive Recovery Dossier PDF directly to this message for your review.\n\n"
        f"Please review the attached document. You may reply directly here on WhatsApp or call me at {USER_PHONE} to coordinate the recovery paperwork.\n\n"
        f"Warm regards,\n"
        f"*{USER_NAME}*\n"
        f"{USER_TITLE}\n"
        f"{USER_FIRM}\n"
        f"Phone: {USER_PHONE}\n"
        f"Location: {USER_LOC}"
    )
    return msg

def dispatch_whatsapp(dry_run=True, batch_only=True):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    wa_delivered_ids = {c['id'] for c in registry.get("whatsapp_delivered_clients", [])}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id ASC")
    customers = [dict(r) for r in c.fetchall()]
    conn.close()

    print("=" * 80, flush=True)
    print(f"CustomerVault Batch WhatsApp Sender | Mode: {'DRY RUN (Simulated)' if dry_run else 'LIVE DISPATCH'}", flush=True)
    print(f"Sender Phone: {USER_PHONE} ({USER_NAME})", flush=True)
    print(f"Policy: NO external URL links | Direct PDF Dossier Attachments Only", flush=True)
    print(f"Already Delivered Clients: {len(wa_delivered_ids)}", flush=True)
    print("=" * 80, flush=True)

    queue = []
    skipped = []

    for cust in customers:
        cid = cust['id']
        phone = extract_mobile_number(cust.get("contact_info", ""))
        pdf1 = cust.get("pdf1_path") or cust.get("pdf1_filename")
        pdf_path = os.path.join(UPLOAD_DIR, pdf1) if pdf1 else None

        if cid in wa_delivered_ids:
            skipped.append((cid, cust['name'], "Already delivered previously"))
            continue

        # If batch_only is set, only target the fresh batch (IDs 66 to 80)
        if batch_only and cid < 66:
            skipped.append((cid, cust['name'], "Pre-batch 66 client"))
            continue

        if not phone:
            skipped.append((cid, cust['name'], "No mobile number on record"))
            continue

        if not pdf_path or not os.path.exists(pdf_path):
            skipped.append((cid, cust['name'], f"Dossier PDF missing ({pdf1})"))
            continue

        queue.append({
            "id": cid,
            "name": cust['name'],
            "phone": phone,
            "folio_id": cust.get("folio_id"),
            "est_folio": cust.get("est_folio"),
            "pdf_path": pdf_path,
            "message": build_whatsapp_message(cust)
        })

    print(f"Ready for WhatsApp dispatch: {len(queue)} clients | Skipped / Already Sent: {len(skipped)}", flush=True)
    print("-" * 80, flush=True)

    if dry_run:
        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] [SIMULATION] Client: {item['name']} (ID {item['id']})", flush=True)
            print(f"  Target WhatsApp: +{item['phone']}", flush=True)
            print(f"  Direct PDF Attachment: {os.path.basename(item['pdf_path'])}", flush=True)
            print(f"  Message contains link: {'YES (ERROR)' if 'http' in item['message'] else 'NO (Clean)'}", flush=True)
            print("-" * 60, flush=True)
        return

    # LIVE DISPATCH WITH PLAYWRIGHT
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

        print("Verifying WhatsApp Web active session...", flush=True)
        try:
            page.wait_for_selector("div[id='pane-side'], div[aria-label='Chat list']", timeout=30000)
            print("Session authenticated successfully!\n", flush=True)
        except Exception:
            print("[ERROR] WhatsApp session not authenticated.", flush=True)
            context.close()
            return

        sent_count = 0
        failed_count = 0

        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] Processing: {item['name']} (+{item['phone']})...", flush=True)

            try:
                # 1. Navigate to chat with personalized message (no links)
                encoded_msg = urllib.parse.quote(item['message'])
                url = f"https://web.whatsapp.com/send?phone={item['phone']}&text={encoded_msg}"
                page.goto(url)

                time.sleep(4)
                invalid_popup = page.locator("div[role='dialog']:has-text('invalid'), div[data-animate-modal-popup='true']:has-text('invalid')")
                if invalid_popup.count() > 0 and invalid_popup.first.is_visible():
                    print(f"  [-] Phone number +{item['phone']} is not active on WhatsApp. Skipping.\n", flush=True)
                    ok_btn = page.locator("div[role='button']:has-text('OK'), button:has-text('OK')")
                    if ok_btn.count() > 0:
                        ok_btn.first.click()
                    failed_count += 1
                    time.sleep(2)
                    continue

                # Wait for Send button and transmit text message
                send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
                send_btn.first.wait_for(state="visible", timeout=25000)
                time.sleep(2)
                send_btn.first.click()
                print(f"  [+] Text message delivered to {item['name']} (+{item['phone']})", flush=True)
                time.sleep(3)

                # 2. Attach and send official PDF Dossier
                plus_btn = page.locator("footer button[aria-label='Attach'], footer span[data-icon='plus'], footer div[role='button']:has(span[data-icon='plus'])")
                plus_btn.first.click()
                time.sleep(2)

                with page.expect_file_chooser(timeout=10000) as fc_info:
                    doc_btn = page.locator("button[aria-label='Document']")
                    doc_btn.first.click()

                file_chooser = fc_info.value
                file_chooser.set_files(item['pdf_path'])
                time.sleep(4)

                # Click Send in preview modal
                modal_send = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
                modal_send.first.click()
                pdf_name = os.path.basename(item['pdf_path'])
                print(f"  [SUCCESS] Attached & Delivered PDF Dossier ({pdf_name}) to {item['name']} (+{item['phone']})!\n", flush=True)
                sent_count += 1

                # Record in registry immediately
                registry["whatsapp_delivered_clients"].append({
                    "id": item['id'],
                    "name": item['name'],
                    "phone": item['phone'],
                    "pdf": pdf_name
                })
                registry["whatsapp_count"] = len(registry["whatsapp_delivered_clients"])
                with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                    json.dump(registry, f, indent=2)

                time.sleep(12)

            except Exception as err:
                print(f"  [ERROR] Failed to send to {item['name']} (+{item['phone']}): {err}\n", flush=True)
                failed_count += 1
                time.sleep(3)

        context.close()
        print("=" * 80, flush=True)
        print(f"WhatsApp Dispatch Complete! Total Delivered: {sent_count} | Failed: {failed_count}", flush=True)
        print("=" * 80, flush=True)

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    dispatch_whatsapp(dry_run=not is_live, batch_only=True)

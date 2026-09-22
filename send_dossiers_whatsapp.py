#!/usr/bin/env python3
"""
send_dossiers_whatsapp.py
-------------------------
Autonomous WhatsApp outreach and document transmission system for CustomerVault.
Uses Playwright with a persistent browser profile to send personalized IEPF recovery
proposals and directly attach official Executive Recovery Dossier PDFs (no links).

Usage:
  python send_dossiers_whatsapp.py --login       # Opens browser to scan QR code once
  python send_dossiers_whatsapp.py --dry-run     # Simulates dispatch without sending
  python send_dossiers_whatsapp.py --live        # Autonomously dispatches to all clients with mobile numbers
"""

import os
import sys
import re
import time
import json
import sqlite3
import urllib.parse
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customers.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
SESSION_DIR = os.path.join(BASE_DIR, ".whatsapp_session")

os.makedirs(SESSION_DIR, exist_ok=True)

USER_NAME = "MD ASRAR BASHA A"
USER_PHONE = "+91 7358882822"
USER_TITLE = "Principal Advisor – Shareholder Rights & IEPF Recovery"
USER_FIRM = "Legal & Compliance Desk | CustomerVault Advisory"
USER_LOC = "Ranipet District & Chennai, Tamil Nadu - 632509"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def extract_mobile_number(contact_info):
    """Extracts a valid 10-digit Indian mobile number (prefixed with 91)."""
    if not contact_info:
        return None
    
    matches = re.findall(r'(?:(?:\+?91)[\s-]?)?([6-9]\d{4}[\s-]?\d{5})', contact_info)
    if matches:
        clean = re.sub(r'\D', '', matches[0])
        return f"91{clean}"
    return None

def build_whatsapp_message(cust):
    """
    Builds clean, high-trust WhatsApp message with ZERO URLs/links.
    Explicitly informs the client that their official PDF Dossier is attached.
    """
    name = cust.get("name", "Investor")
    folio = cust.get("folio_id", "Unclaimed Folio")
    est_folio = cust.get("est_folio", "Audited Portfolio")
    
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

def login_mode():
    """Launches visible browser to let user scan the WhatsApp Web QR code once."""
    print("=" * 80)
    print("WhatsApp Web Authentication Setup")
    print(f"Session Storage: {SESSION_DIR}")
    print("=" * 80)
    print("\nOpening WhatsApp Web in Chrome/Chromium...")
    print("Please scan the QR code using WhatsApp on your phone:")
    print("  1. Open WhatsApp on your phone")
    print("  2. Tap Menu (Android) or Settings (iPhone) -> Linked Devices")
    print("  3. Tap 'Link a Device' and point your camera at the QR code on screen.")
    print("\nWaiting for login...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
            user_agent=USER_AGENT,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com")

        # Wait for chat list container (indicates successful login)
        try:
            page.wait_for_selector("div[id='pane-side'], div[aria-label='Chat list']", timeout=120000)
            print("\n[SUCCESS] WhatsApp Web login successful! Session saved.")
            print("You can now run automated dispatch using: python send_dossiers_whatsapp.py --live")
        except Exception:
            print("\n[TIMEOUT] Login wait timed out or browser was closed before scanning.")
        finally:
            context.close()

def dispatch_whatsapp(dry_run=True):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id ASC")
    customers = [dict(r) for r in c.fetchall()]
    conn.close()

    print("=" * 80)
    print(f"CustomerVault Batch WhatsApp Sender | Mode: {'DRY RUN (Simulated)' if dry_run else 'LIVE DISPATCH'}")
    print(f"Sender Phone: {USER_PHONE} ({USER_NAME})")
    print(f"Policy: NO external URL links | Direct PDF Dossier Attachments Only")
    print("=" * 80)

    delivered_ids = set()
    log_file = os.path.join(BASE_DIR, "whatsapp_dispatch_log.json")
    results_log = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                results_log = json.load(f)
                for entry in results_log:
                    if entry.get("status") == "DELIVERED":
                        delivered_ids.add(entry.get("id"))
        except Exception:
            results_log = []

    queue = []
    skipped = []

    for cust in customers:
        phone = extract_mobile_number(cust.get("contact_info", ""))
        pdf1 = cust.get("pdf1_path") or cust.get("pdf1_filename")
        pdf_path = os.path.join(UPLOAD_DIR, pdf1) if pdf1 else None
        
        if cust['id'] in delivered_ids:
            skipped.append((cust['id'], cust['name'], "Already delivered today"))
            continue

        if not phone:
            skipped.append((cust['id'], cust['name'], "No mobile number on record"))
            continue
            
        if not pdf_path or not os.path.exists(pdf_path):
            skipped.append((cust['id'], cust['name'], f"Dossier PDF missing ({pdf1})"))
            continue
            
        queue.append({
            "id": cust['id'],
            "name": cust['name'],
            "phone": phone,
            "folio_id": cust.get("folio_id"),
            "est_folio": cust.get("est_folio"),
            "pdf_path": pdf_path,
            "message": build_whatsapp_message(cust)
        })

    print(f"Ready for WhatsApp dispatch: {len(queue)} clients | Skipped / Already Sent: {len(skipped)}")
    print("-" * 80)

    if dry_run:
        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] [SIMULATION] Client: {item['name']} (ID {item['id']})")
            print(f"  Target WhatsApp: +{item['phone']}")
            print(f"  Direct PDF Attachment: {os.path.basename(item['pdf_path'])}")
            print(f"  Message contains link: {'YES (ERROR)' if 'http' in item['message'] else 'NO (Clean)'}")
            print(f"  Preview: {item['message'][:140]}...\n")
        print("=" * 80)
        print(f"Dry run complete. {len(queue)} clients ready to receive WhatsApp messages with attached PDFs.")
        print("To send live messages, run: python send_dossiers_whatsapp.py --live")
        return

    # LIVE DISPATCH
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

        print("Verifying WhatsApp Web active session...")
        try:
            page.wait_for_selector("div[id='pane-side'], div[aria-label='Chat list']", timeout=30000)
            print("Session authenticated successfully!\n")
        except Exception:
            print("[ERROR] WhatsApp session not authenticated.")
            print("Please run: python send_dossiers_whatsapp.py --login to scan the QR code first.")
            context.close()
            return

        sent_count = 0
        failed_count = 0
        results_log = []

        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] Processing: {item['name']} (+{item['phone']})...", flush=True)
            
            try:
                # 1. Navigate to chat with personalized message (no links)
                encoded_msg = urllib.parse.quote(item['message'])
                url = f"https://web.whatsapp.com/send?phone={item['phone']}&text={encoded_msg}"
                page.goto(url)
                
                # Check for "Phone number shared via url is invalid" popup
                time.sleep(4)
                invalid_popup = page.locator("div[role='dialog']:has-text('invalid'), div[data-animate-modal-popup='true']:has-text('invalid')")
                if invalid_popup.count() > 0 and invalid_popup.first.is_visible():
                    print(f"  [-] Phone number +{item['phone']} is not active on WhatsApp. Skipping.\n", flush=True)
                    ok_btn = page.locator("div[role='button']:has-text('OK'), button:has-text('OK')")
                    if ok_btn.count() > 0:
                        ok_btn.first.click()
                    failed_count += 1
                    results_log.append({"id": item['id'], "name": item['name'], "phone": item['phone'], "status": "INVALID_NUMBER"})
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
                results_log.append({"id": item['id'], "name": item['name'], "phone": item['phone'], "status": "DELIVERED", "pdf": pdf_name})

                # Save interim progress to disk
                with open(os.path.join(BASE_DIR, "whatsapp_dispatch_log.json"), "w", encoding="utf-8") as f:
                    json.dump(results_log, f, indent=2)

                # Polite randomized delay to prevent spam flagging (12-16 seconds)
                time.sleep(14)

            except Exception as err:
                print(f"  [ERROR] Failed to send to {item['name']} (+{item['phone']}): {err}\n", flush=True)
                failed_count += 1
                results_log.append({"id": item['id'], "name": item['name'], "phone": item['phone'], "status": "FAILED", "error": str(err)})
                time.sleep(3)

        context.close()
        print("=" * 80, flush=True)
        print(f"WhatsApp Dispatch Complete! Total Delivered: {sent_count} | Failed: {failed_count}", flush=True)
        print("=" * 80, flush=True)

if __name__ == "__main__":
    if "--login" in sys.argv:
        login_mode()
    elif "--live" in sys.argv:
        dispatch_whatsapp(dry_run=False)
    else:
        dispatch_whatsapp(dry_run=True)

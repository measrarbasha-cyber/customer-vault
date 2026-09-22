#!/usr/bin/env python3
"""
send_dossiers_whatsapp.py
-------------------------
Autonomous WhatsApp outreach and document transmission system for CustomerVault.
Uses Playwright with a persistent browser profile to send personalized IEPF recovery
proposals and attach official Executive Recovery Dossier PDFs.

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
USER_TITLE = "Independent Financial Consultant & IEPF Recovery Specialist"
USER_LOC = "Chennai & Ranipet, Tamil Nadu"

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
    name = cust.get("name", "Investor")
    folio = cust.get("folio_id", "Unclaimed Folio")
    est_folio = cust.get("est_folio", "Audited Portfolio")
    
    msg = (
        f"Namaste {name} ji,\n\n"
        f"I am writing to bring to your attention an important statutory matter regarding your unclaimed equity shares "
        f"in *Astral Limited* (Folio / Demat ID: *{folio}*), currently held under the custody of the Investor Education and "
        f"Protection Fund (IEPF) Authority, Ministry of Corporate Affairs, Government of India.\n\n"
        f"📊 *Audited Valuation Summary:*\n"
        f"• Total Portfolio Value: *{est_folio}*\n"
        f"• Terms: *Rs. 0 Advance Fee* (100% contingent on credit)\n"
        f"• Settlement: Shares & accrued dividends are credited *directly by Central Govt* into your personal Demat & Bank A/C.\n\n"
        f"I have attached your official *Executive Recovery Dossier & Audit Breakdown PDF* for your review.\n\n"
        f"Please review the attached dossier. You may reply directly here or call me at {USER_PHONE} to coordinate the recovery paperwork.\n\n"
        f"Warm regards,\n"
        f"*{USER_NAME}*\n"
        f"{USER_TITLE}\n"
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
    print("=" * 80)

    queue = []
    skipped = []

    for cust in customers:
        phone = extract_mobile_number(cust.get("contact_info", ""))
        pdf1 = cust.get("pdf1_path") or cust.get("pdf1_filename")
        pdf_path = os.path.join(UPLOAD_DIR, pdf1) if pdf1 else None
        
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

    print(f"Ready for WhatsApp dispatch: {len(queue)} clients | Skipped: {len(skipped)}")
    print("-" * 80)

    if dry_run:
        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] [SIMULATION] Client: {item['name']} (ID {item['id']})")
            print(f"  Target WhatsApp: +{item['phone']}")
            print(f"  Attached Dossier: {os.path.basename(item['pdf_path'])}")
            print(f"  Preview: {item['message'][:120]}...\n")
        print("=" * 80)
        print(f"Dry run complete. {len(queue)} clients ready to receive WhatsApp messages.")
        print("To send live messages, run: python send_dossiers_whatsapp.py --live")
        return

    # LIVE DISPATCH
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
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

        for idx, item in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] Processing: {item['name']} (+{item['phone']})...")
            
            try:
                # Encode message into direct chat URL
                encoded_msg = urllib.parse.quote(item['message'])
                url = f"https://web.whatsapp.com/send?phone={item['phone']}&text={encoded_msg}"
                page.goto(url)
                
                # Wait for chat input box or send button
                time.sleep(5)
                
                # Look for Send button
                send_btn = page.locator("span[data-icon='send'], button[aria-label='Send']")
                send_btn.wait_for(state="visible", timeout=20000)
                send_btn.click()
                print(f"  -> Message text sent successfully!")
                time.sleep(3)

                # Attach PDF Document
                # Click the attach '+' icon
                attach_btn = page.locator("span[data-icon='plus'], button[aria-label='Attach'], span[data-icon='attach-menu-plus']")
                if attach_btn.is_visible():
                    attach_btn.click()
                    time.sleep(1)

                # Upload document via file input
                file_input = page.locator("input[type='file']")
                if file_input.count() > 0:
                    file_input.first.set_input_files(item['pdf_path'])
                    time.sleep(3)
                    
                    # Click send button in media preview
                    doc_send_btn = page.locator("span[data-icon='send'], div[aria-label='Send']")
                    doc_send_btn.wait_for(state="visible", timeout=15000)
                    doc_send_btn.click()
                    print(f"  -> Attached & sent: {os.path.basename(item['pdf_path'])}")
                    time.sleep(4)

                sent_count += 1
                print(f"  [COMPLETED] Successfully delivered to {item['name']} (+{item['phone']})\n")

                # Polite delay to prevent spam flagging
                time.sleep(8)

            except Exception as err:
                print(f"  [ERROR] Failed to send to {item['name']} (+{item['phone']}): {err}\n")
                failed_count += 1
                time.sleep(3)

        context.close()
        print("=" * 80)
        print(f"WhatsApp Dispatch Complete! Total Sent: {sent_count} | Failed: {failed_count}")
        print("=" * 80)

if __name__ == "__main__":
    if "--login" in sys.argv:
        login_mode()
    elif "--live" in sys.argv:
        dispatch_whatsapp(dry_run=False)
    else:
        dispatch_whatsapp(dry_run=True)

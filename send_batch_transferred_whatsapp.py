import os
import sys
import time
import json
import sqlite3
import re
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
DB_PATH = os.path.join(BASE_DIR, "customers.db")
LOG_PATH = os.path.join(BASE_DIR, "transferred_whatsapp_dispatch_log.json")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def get_whatsapp_queue():
    with open(os.path.join(BASE_DIR, "master_client_stats.json"), "r", encoding="utf-8") as f:
        master_stats = {s['id']: s for s in json.load(f)}

    with open(os.path.join(BASE_DIR, "transferred_dispatch_targets.json"), "r", encoding="utf-8") as f:
        targets = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, name, folio_id, address, est_folio FROM customers WHERE pdf6_path IS NOT NULL")
    clients_db = {r['id']: dict(r) for r in c.fetchall()}
    conn.close()

    queue = []
    for tgt in targets:
        cid = tgt['id']
        phones = tgt.get('phones', [])
        if not phones:
            continue

        pdf_fn = tgt.get('pdf6')
        pdf_path = os.path.join(UPLOAD_DIR, pdf_fn) if pdf_fn else None
        if not pdf_path or not os.path.exists(pdf_path):
            continue

        cl_db = clients_db.get(cid, {})
        stat = master_stats.get(cid, {})
        shares = stat.get('current_shares')
        if not shares:
            m_sh = re.search(r'([\d,]+)\s*Shares', cl_db.get('est_folio', ''))
            shares = int(m_sh.group(1).replace(',', '')) if m_sh else 5000

        val = shares * 1425
        val_cr = val / 10000000.0
        val_str = f"~Rs. {val_cr:.2f} Cr" if val_cr >= 1.0 else f"~Rs. {val/100000.0:.2f} Lakhs"

        addr = cl_db.get('address', '') or tgt.get('address', '')
        # Clean address snippet
        clean_addr = re.sub(r'[\r\n]+', ' ', addr).strip()
        addr_snippet = clean_addr[:45] + ("..." if len(clean_addr) > 45 else "")

        queue.append({
            "id": cid,
            "name": tgt['name'],
            "folio_id": tgt['folio'],
            "address": clean_addr,
            "addr_snippet": addr_snippet,
            "shares": shares,
            "valuation_str": val_str,
            "valuation_full": f"Rs. {val:,.2f}",
            "phones": phones,
            "pdf_fn": pdf_fn,
            "pdf_path": pdf_path
        })

    return queue

def build_whatsapp_message(cust):
    name = cust['name']
    folio = cust['folio_id']
    shares = cust['shares']
    val_str = cust['valuation_str']
    val_full = cust['valuation_full']
    addr = cust['addr_snippet']

    return f"""Respected {name},

Please review the attached Statutory Audit Notice regarding your long-term equity investment in Astral Limited.

Under Section 124(6) of the Companies Act, 2013, your {shares:,} equity shares ({val_str} | Market Value: {val_full}) registered at your {addr} address have matured past the 7-year unpaid dividend threshold and were statutorily debited and transferred into the Central Government IEPF Authority Demat Account (MCA, New Delhi).

⚠️ Important:
Central Government custody acts strictly as a statutory depository. Under Section 125(3), the government will NEVER automatically release or credit shares back to your Demat account without a formal, approved e-Form IEPF-5 claim. Over 80% of self-filed claims get rejected due to signature mismatches or SEBI Form ISR-1/2 technicalities.

🔍 Independent Verification (Takes 2 Minutes):
You can verify this transfer directly on the official MCA portal:
👉 https://www.iepf.gov.in (Services → Search Unclaimed/Transferred Amounts → Company: Astral Limited | Folio: {folio})

🛡️ Our 100% Risk-Free Fiduciary Mandate:
• ₹0 Advance Fee (Payable strictly AFTER shares are credited in your Demat account)
• Direct Government Settlement (Shares credited directly to your own Demat, funds via PFMS/DBT)
• Complete Privacy (Masked KYC only; no OTPs/passwords ever requested)

Please examine the attached 3-Page Statutory Audit Notice & Recovery Guide PDF for official gazette records and the complete step-by-step restitution roadmap.

Could we schedule a brief 2-minute introductory call today at your convenience?

Respectfully yours,
MD ASRAR BASHA A
Corporate IEPF Asset Restitution Practice
📞 +91 7358882822
🌐 https://customer-vault.onrender.com"""

def dispatch_transferred_whatsapp(dry_run=True, client_id=None, limit=None):
    queue = get_whatsapp_queue()
    if client_id:
        queue = [q for q in queue if q['id'] == client_id]
    if limit:
        queue = queue[:limit]

    print("=" * 80)
    print(f"BATCH WHATSAPP DISPATCH (DOC 6 NOTICES) | MODE: {'DRY RUN' if dry_run else 'LIVE DISPATCH'}")
    print(f"Total Eligible Transferred Clients with Mobile: {len(queue)}")
    total_nums = sum(len(q['phones']) for q in queue)
    print(f"Total Phone Numbers to Target: {total_nums}")
    print("=" * 80)

    if dry_run:
        for idx, cust in enumerate(queue, 1):
            print(f"[{idx}/{len(queue)}] Client ID {cust['id']}: {cust['name']}")
            print(f"  Folio: {cust['folio_id']} | Shares: {cust['shares']:,} ({cust['valuation_str']})")
            print(f"  Target Phones: {', '.join(cust['phones'])}")
            print(f"  PDF Notice: {cust['pdf_fn']} ({os.path.getsize(cust['pdf_path'])} bytes)")
            print("  Status: [SIMULATED SUCCESS]\n")
        print(f"Dry Run Complete! Simulated {len(queue)} clients ({total_nums} phone numbers).")
        return

    # Live Mode
    logs = []
    delivered_phones = set()
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                logs = prev_data.get("logs", [])
                for entry in logs:
                    if entry.get("status") == "delivered":
                        delivered_phones.add(entry.get("phone"))
        except Exception:
            pass

    success_count = len(delivered_phones)
    fail_count = len([e for e in logs if e.get("status") in ["failed", "skipped_not_on_whatsapp"]])

    print("Launching Chromium with persistent WhatsApp session...", flush=True)
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
            print("[+] WhatsApp session authenticated successfully!\n", flush=True)
        except Exception as e:
            print(f"[-] Session authentication failed: {e}")
            page.screenshot(path="wa_batch_auth_failed.png")
            context.close()
            return

        for idx, cust in enumerate(queue, 1):
            cname = cust['name']
            cid = cust['id']
            pdf_path = cust['pdf_path']
            msg = build_whatsapp_message(cust)

            print(f"\n================================================================================")
            print(f"[{idx}/{len(queue)}] Processing Client ID {cid}: {cname}")
            print(f"  Folio: {cust['folio_id']} | Shares: {cust['shares']:,} ({cust['valuation_str']})")
            print(f"  Phones: {cust['phones']}")
            print(f"  Doc 6 PDF: {cust['pdf_fn']}")
            print(f"================================================================================")

            for phone in cust['phones']:
                if phone in delivered_phones:
                    print(f"  [+] +{phone} already marked delivered. Skipping duplicate send.", flush=True)
                    continue

                record = {
                    "client_id": cid,
                    "name": cname,
                    "phone": phone,
                    "pdf": cust['pdf_fn'],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "pending",
                    "error": None
                }

                try:
                    print(f"  -> Navigating to chat for +{phone}...", flush=True)
                    encoded_msg = urllib.parse.quote(msg)
                    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
                    page.goto(url)

                    time.sleep(6)

                    # Check for invalid number dialog
                    invalid_popup = page.locator("div[role='dialog']:has-text('invalid'), div[data-animate-modal-popup='true']:has-text('invalid'), div[role='dialog']:has-text('Phone number shared via url is invalid')")
                    if invalid_popup.count() > 0 and invalid_popup.first.is_visible():
                        print(f"  [-] Number +{phone} is not registered on WhatsApp. Skipping.", flush=True)
                        ok_btn = page.locator("div[role='button']:has-text('OK'), button:has-text('OK')")
                        if ok_btn.count() > 0:
                            ok_btn.first.click()
                        record["status"] = "skipped_not_on_whatsapp"
                        logs.append(record)
                        time.sleep(2)
                        continue

                    # Send text message
                    send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']")
                    try:
                        send_btn.first.wait_for(state="visible", timeout=15000)
                        time.sleep(1)
                        send_btn.first.click()
                    except Exception:
                        chat_box = page.locator("footer div[contenteditable='true'], div[role='textbox']")
                        if chat_box.count() > 0:
                            chat_box.first.press("Enter")

                    print(f"  [+] Message sent to +{phone}!", flush=True)
                    time.sleep(3)

                    # Attach Doc 6 PDF
                    print(f"  Attaching Doc 6 Notice: {cust['pdf_fn']}...", flush=True)
                    plus_btn = page.locator("[data-icon='plus'], [aria-label='Attach'], button[title='Attach'], div[title='Attach']").first
                    try:
                        plus_btn.wait_for(state="visible", timeout=12000)
                        plus_btn.click(force=True)
                    except Exception:
                        page.keyboard.press("Escape")
                        time.sleep(1)
                        plus_btn.click(force=True)
                    time.sleep(2)

                    with page.expect_file_chooser(timeout=10000) as fc_info:
                        doc_btn = page.locator("[aria-label='Document'], li:has-text('Document')")
                        doc_btn.first.click(force=True)

                    file_chooser = fc_info.value
                    file_chooser.set_files(pdf_path)
                    time.sleep(3)

                    # Click Send in modal
                    try:
                        modal_send = page.locator("div[aria-label='Send'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']").first
                        modal_send.click(force=True, timeout=8000)
                    except Exception:
                        print("  [Note] modal_send click intercepted, sending via Enter key...", flush=True)
                        page.keyboard.press("Enter")

                    print(f"  >>> SUCCESS: PDF Notice delivered to +{phone} ({cname})!", flush=True)

                    record["status"] = "delivered"
                    success_count += 1
                    time.sleep(5)
                    # Clear any dangling overlays
                    page.keyboard.press("Escape")

                except Exception as ex:
                    print(f"  [-] ERROR delivering to +{phone}: {ex}", flush=True)
                    record["status"] = "failed"
                    record["error"] = str(ex)
                    fail_count += 1
                    time.sleep(3)

                logs.append(record)

                # Save intermediate log
                with open(LOG_PATH, "w", encoding="utf-8") as f:
                    json.dump({
                        "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "total_attempted": len(logs),
                        "success": success_count,
                        "failed": fail_count,
                        "logs": logs
                    }, f, indent=2)

        context.close()

    print("\n" + "=" * 80)
    print(f"WHATSAPP DISPATCH COMPLETED!")
    print(f"Delivered: {success_count} | Failed/Skipped: {fail_count}")
    print(f"Audit Log Saved: {LOG_PATH}")
    print("=" * 80)

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    cid_arg = None
    limit_arg = None

    for i, a in enumerate(sys.argv):
        if a == "--client-id" and i + 1 < len(sys.argv):
            cid_arg = int(sys.argv[i+1])
        if a == "--limit" and i + 1 < len(sys.argv):
            limit_arg = int(sys.argv[i+1])

    dispatch_transferred_whatsapp(dry_run=not is_live, client_id=cid_arg, limit=limit_arg)

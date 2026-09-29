import imaplib
import email
from email.header import decode_header
import re
import json
import os
import sys
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "amdasrarbasha@gmail.com"
EMAIL_PASS = "zenqaefujramczmo"

def clean_undelivered_and_bounced_emails():
    print("=" * 80, flush=True)
    print("GMAIL AUTOMATIC UNDELIVERED & BOUNCE CLEANUP", flush=True)
    print(f"Account: {EMAIL_USER}", flush=True)
    print("=" * 80, flush=True)

    try:
        import socket
        socket.setdefaulttimeout(15)
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)
        mail.login(EMAIL_USER, EMAIL_PASS)
        print("[+] Logged into Gmail IMAP successfully.", flush=True)
    except Exception as e:
        print(f"[-] IMAP Authentication failed: {e}", flush=True)
        return {"bounced": [], "deleted_sent": 0}

    # 1. Check INBOX for bounce notifications
    mail.select("INBOX")
    
    # Search mailer-daemon, delivery status notification
    search_queries = [
        '(FROM "mailer-daemon@googlemail.com")',
        '(SUBJECT "Delivery Status Notification (Failure)")'
    ]
    
    bounce_msg_ids = set()
    for q in search_queries:
        try:
            status, msgs = mail.search(None, q)
            if status == "OK" and msgs[0]:
                for mid in msgs[0].split():
                    bounce_msg_ids.add(mid)
        except Exception:
            pass

    print(f"Total bounce notifications identified in INBOX: {len(bounce_msg_ids)}")

    bounced_addresses = set()
    inbox_deleted_count = 0

    for mid in bounce_msg_ids:
        try:
            res, msg_data = mail.fetch(mid, "(RFC822)")
            if res != "OK":
                continue
            for part in msg_data:
                if isinstance(part, tuple):
                    msg = email.message_from_bytes(part[1])
                    body = ""
                    if msg.is_multipart():
                        for p in msg.walk():
                            if p.get_content_type() == "text/plain":
                                try:
                                    body += p.get_payload(decode=True).decode("utf-8", errors="ignore")
                                except Exception:
                                    pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except Exception:
                            pass

                    # Extract target bounced emails from notification body
                    # Matches "wasn't delivered to ...", "550 5.1.1 ...", or standard recipient emails
                    found = re.findall(r"(?:wasn't delivered to|failed to reach|550[\s-].*?|to\s*:?)\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", body, re.IGNORECASE)
                    for addr in found:
                        clean_addr = addr.lower().strip()
                        if clean_addr != EMAIL_USER.lower() and "google" not in clean_addr:
                            bounced_addresses.add(clean_addr)
            
            # Mark bounce notice for deletion from INBOX
            mail.store(mid, "+FLAGS", "\\Deleted")
            inbox_deleted_count += 1
        except Exception as ex:
            print(f"  [-] Error parsing bounce msg {mid}: {ex}")

    mail.expunge()
    if inbox_deleted_count > 0:
        print(f"[+] Purged {inbox_deleted_count} bounce notification emails from INBOX.")

    print(f"\nIdentified Bounced / Undelivered Addresses: {len(bounced_addresses)}")
    for b in sorted(bounced_addresses):
        print(f"  [-] Bounced Address: {b}")

    # 2. Find and permanently DELETE sent emails to these addresses from [Gmail]/Sent Mail
    deleted_sent_count = 0
    if bounced_addresses:
        # Determine Sent folder name
        sent_folder = '"[Gmail]/Sent Mail"'
        mail.select(sent_folder)

        for b_addr in bounced_addresses:
            try:
                status, msgs = mail.search(None, f'(TO "{b_addr}")')
                if status == "OK" and msgs[0]:
                    sent_ids = msgs[0].split()
                    for s_id in sent_ids:
                        mail.store(s_id, "+FLAGS", "\\Deleted")
                        deleted_sent_count += 1
                        print(f"  [x] Deleted from Sent Mail: email sent to undelivered address <{b_addr}>")
            except Exception as e:
                print(f"  [-] Error searching sent for {b_addr}: {e}")

        mail.expunge()
        print(f"\n[+] Successfully deleted {deleted_sent_count} undelivered emails from Sent Mail!")

        # 3. Also purge from [Gmail]/Trash
        try:
            mail.select('"[Gmail]/Trash"')
            status, trash_msgs = mail.search(None, "ALL")
            if status == "OK" and trash_msgs[0]:
                for t_id in trash_msgs[0].split():
                    mail.store(t_id, "+FLAGS", "\\Deleted")
                mail.expunge()
                print("[+] Emptied Trash to ensure permanently clean state.")
        except Exception:
            pass
    else:
        print("[+] No bounced or undelivered emails detected. All sent emails were accepted by recipient mail servers!")

    mail.logout()
    print("=" * 80)
    print("CLEANUP ROUTINE COMPLETE")
    print("=" * 80)

    return {
        "bounced": list(bounced_addresses),
        "deleted_sent": deleted_sent_count
    }

if __name__ == "__main__":
    clean_undelivered_and_bounced_emails()

import imaplib
import email
import sys

sys.stdout.reconfigure(encoding='utf-8')

IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "amdasrarbasha@gmail.com"
EMAIL_PASS = "zenqaefujramczmo"

mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)
mail.login(EMAIL_USER, EMAIL_PASS)

# Select Sent Mail
mail.select('"[Gmail]/Sent Mail"')
status, msgs = mail.search(None, 'ALL')
ids = msgs[0].split()
print(f"Total verified messages in Sent Mail: {len(ids)}")

print("\n--- RECENT SENT MESSAGES CURRENTLY IN SENT FOLDER ---")
for i in ids[-25:]:
    res, data = mail.fetch(i, '(BODY[HEADER.FIELDS (TO SUBJECT DATE)])')
    for part in data:
        if isinstance(part, tuple):
            m = email.message_from_bytes(part[1])
            to_h = m.get('To', '').strip()
            subj = m.get('Subject', '').strip()
            date = m.get('Date', '').strip()
            print(f"  [SENT OK] To: {to_h:<35} | Subj: {subj[:45]}")

mail.logout()

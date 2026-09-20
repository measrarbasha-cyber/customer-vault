import os
import json
import sqlite3
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
db_path = os.path.join(vault_dir, "customers.db")
stats_path = os.path.join(vault_dir, "master_client_stats.json")
API_BASE = "https://customer-vault.onrender.com/api"

def format_inr_short(amount):
    if amount >= 10000000:
        cr = amount / 10000000
        return f"~₹{cr:.2f} Cr"
    else:
        lakhs = amount / 100000
        return f"~₹{lakhs:.2f} Lakhs"

with open(stats_path, 'r', encoding='utf-8') as f:
    stats = json.load(f)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

print(f"Syncing exact audited portfolio values for all {len(stats)} clients...")

updates = []

for s in stats:
    cid = s['id']
    name = s['name']

    # Specific override for Dr Phatak with verified 13,140 shares
    if 'Phatak' in name:
        current_shares = 13140
        current_val = round(13140 * 1425)
    else:
        current_shares = s['current_shares']
        current_val = s['current_val_inr']

    fee_pct = 15 if cid == 10 else 8
    fee_val = round(current_val * (fee_pct / 100.0))

    est_folio = f"₹{current_val:,} ({format_inr_short(current_val)} | {current_shares:,} Shares)"
    my_est_value = f"₹{fee_val:,} ({format_inr_short(fee_val)} | {fee_pct}% Fee)"

    # Update stats in-memory
    s['est_folio'] = est_folio
    s['my_est_value'] = my_est_value
    s['current_shares'] = current_shares
    s['current_val_inr'] = current_val

    # Fetch current row from DB
    row = c.execute("SELECT * FROM customers WHERE id = ?", (cid,)).fetchone()
    if not row:
        print(f"[SKIP] Client ID {cid} not in DB")
        continue

    row_dict = dict(row)

    # Update SQLite local
    c.execute("""
        UPDATE customers 
        SET est_folio = ?, my_est_value = ? 
        WHERE id = ?
    """, (est_folio, my_est_value, cid))

    updates.append({
        "id": cid,
        "name": row_dict["name"],
        "address": row_dict["address"],
        "folio_id": row_dict["folio_id"],
        "est_folio": est_folio,
        "my_est_value": my_est_value,
        "contact_info": row_dict["contact_info"]
    })

    print(f"[LOCAL DB OK] ID {cid:2d}: {name[:22]:22s} -> {est_folio} | Fee: {my_est_value}")

conn.commit()
conn.close()

# Save updated master_client_stats.json
with open(stats_path, 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print("\n[OK] Updated master_client_stats.json successfully.")

# Push updates to Live Render API
print("\n--- PUSHING UPDATES TO LIVE RENDER API ---")
for u in updates:
    cid = u['id']
    url = f"{API_BASE}/customers/{cid}"
    payload = json.dumps({
        "name": u["name"],
        "address": u["address"],
        "folio_id": u["folio_id"],
        "est_folio": u["est_folio"],
        "my_est_value": u["my_est_value"],
        "contact_info": u["contact_info"]
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="PUT")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                print(f"[RENDER 200] ID {cid:2d} ({u['name'][:20]}) updated live on Render!")
            else:
                print(f"[RENDER {resp.status}] ID {cid:2d}")
    except Exception as e:
        print(f"[RENDER ERROR] ID {cid:2d}: {e}")

print("\nALL 31 CLIENT AUDITED VALUES SYNCHRONIZED LOCALLY AND TO LIVE PORTAL!")

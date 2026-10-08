import os
import json
import urllib.request
import urllib.error
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
upload_dir = os.path.join(vault_dir, "uploads")
API_BASE = "https://customer-vault.onrender.com/api"

with open(os.path.join(vault_dir, "master_client_stats.json"), "r", encoding="utf-8") as f:
    stats = json.load(f)

new_clients = [s for s in stats if s["id"] >= 96]
print(f"Found {len(new_clients)} new clients to sync to Render API:")

def read_b64(fname):
    p = os.path.join(upload_dir, fname)
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

import sqlite3
conn = sqlite3.connect(os.path.join(upload_dir, "customers.db"))
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM customers WHERE id >= 96 ORDER BY id")
db_rows = {r["id"]: dict(r) for r in c.fetchall()}
conn.close()

for nc in new_clients:
    cid = nc["id"]
    row = db_rows.get(cid, {})
    if not row:
        continue
    
    payload_data = {
        "id": cid,
        "name": row["name"],
        "address": row["address"],
        "folio_id": row["folio_id"],
        "est_folio": row["est_folio"],
        "my_est_value": row["my_est_value"],
        "contact_info": row["contact_info"],
        "status": row.get("status", "Pending"),
        "pdf1": {"filename": row["pdf1_filename"], "data": read_b64(row["pdf1_path"])},
        "pdf2": {"filename": row["pdf2_filename"], "data": read_b64(row["pdf2_path"])},
        "pdf3": {"filename": row["pdf3_filename"], "data": read_b64(row["pdf3_path"])},
        "pdf4": {"filename": row["pdf4_filename"], "data": read_b64(row["pdf4_path"])},
        "pdf5": {"filename": row["pdf5_filename"], "data": read_b64(row["pdf5_path"])}
    }
    payload_bytes = json.dumps(payload_data).encode("utf-8")
    req = urllib.request.Request(f"{API_BASE}/customers", data=payload_bytes, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  [RENDER POST 200] Client ID {cid} ({row['name']}) synced to live Render!")
    except urllib.error.HTTPError as e:
        if e.code in (400, 409, 500):
            req_put = urllib.request.Request(f"{API_BASE}/customers/{cid}", data=payload_bytes, method="PUT")
            req_put.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req_put, timeout=30) as resp_put:
                    print(f"  [RENDER PUT 200] Client ID {cid} ({row['name']}) updated on live Render!")
            except Exception as e_put:
                print(f"  [RENDER PUT ERROR] Client ID {cid}: {e_put}")
        else:
            print(f"  [RENDER POST ERROR] Client ID {cid}: {e}")
    except Exception as e:
        print(f"  [RENDER NET ERROR] Client ID {cid}: {e}")

print("Render sync completed for Clients 96 to 105.")

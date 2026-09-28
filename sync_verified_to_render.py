import os
import sys
import json
import sqlite3
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
API_BASE = "https://customer-vault.onrender.com/api"

# 25 Verified Customer IDs
VERIFIED_IDS = [6, 7, 12, 19, 20, 21, 22, 23, 24, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 44, 46, 67, 78]

def sync_verified():
    conn = sqlite3.connect(os.path.join(vault_dir, "customers.db"))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f"SELECT * FROM customers WHERE id IN ({','.join(map(str, VERIFIED_IDS))})")
    rows = {r["id"]: dict(r) for r in c.fetchall()}
    conn.close()

    print(f"Loaded {len(rows)} verified client records from local customers.db")

    for cid in VERIFIED_IDS:
        row = rows.get(cid)
        if not row:
            print(f"Skipping ID {cid} (not found in local DB)")
            continue

        # Get existing remote record to make sure we don't clobber any remote pdf links
        remote_cust = None
        try:
            get_req = urllib.request.Request(f"{API_BASE}/customers/{cid}")
            with urllib.request.urlopen(get_req, timeout=30) as resp:
                remote_cust = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  [GET ERROR] ID {cid}: {e}")

        payload = {
            "name": row["name"],
            "address": row["address"],
            "folio_id": row["folio_id"],
            "est_folio": row["est_folio"],
            "my_est_value": row["my_est_value"],
            "contact_info": row["contact_info"],
            "status": row.get("status") or (remote_cust.get("status") if remote_cust else "Pending")
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        put_req = urllib.request.Request(f"{API_BASE}/customers/{cid}", data=data_bytes, method="PUT")
        put_req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(put_req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                print(f"  [SUCCESS 200] ID {cid:2d} ({row['name'][:25]}): {row['contact_info'][:60]}...")
        except urllib.error.HTTPError as e:
            print(f"  [HTTP ERROR] ID {cid}: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"  [NET ERROR] ID {cid}: {e}")

    print("\nVerifying updated contacts on Render...")
    try:
        req = urllib.request.Request(f"{API_BASE}/customers/7")
        with urllib.request.urlopen(req, timeout=30) as resp:
            cust7 = json.loads(resp.read().decode("utf-8"))
            print(f"Verification Check ID 7:")
            print(f"  Name: {cust7.get('name')}")
            print(f"  Contact: {cust7.get('contact_info')}")
            print(f"  Status: {cust7.get('status')}")
    except Exception as e:
        print(f"Verification error: {e}")

if __name__ == "__main__":
    sync_verified()

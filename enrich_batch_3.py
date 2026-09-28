import sqlite3
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

API_BASE = "https://customer-vault.onrender.com/api"

BATCH_3 = {
    92: "+91 90328 82838 (Hotel Minerva & Building Desk) | 3rd Floor, 11/25/18 KT Road, Opp Hindu High School, Vijayawada",
    94: "+91 22 2367 4972 | vkakar@kaplegal.com (3rd Floor Desk, Jethalal Mansion) | Bank Street Cross Lane, Fort, Mumbai",
    64: "+91 97400 89897 | 0836-2265620 | 0836-2362645 | KDO Mansion Estate & Admin Desk, Kusugal Rd, Keshwapur, Hubli",
    60: "joshappliances@rediffmail.com | Milind & Manish Shete (Directors, Josh Equipments) | 10 Talathi Colony, MERI, Nashik"
}

def update_local(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for cid, cinfo in BATCH_3.items():
        c.execute("UPDATE customers SET contact_info = ? WHERE id = ?", (cinfo, cid))
    conn.commit()
    conn.close()
    print(f"Updated local {db_path} with {len(BATCH_3)} verified contacts.")

def sync_render():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f"SELECT * FROM customers WHERE id IN ({','.join(map(str, BATCH_3.keys()))})")
    rows = {r["id"]: dict(r) for r in c.fetchall()}
    conn.close()

    for cid, cinfo in BATCH_3.items():
        row = rows.get(cid)
        if not row: continue
        payload = {
            "name": row["name"],
            "address": row["address"],
            "folio_id": row["folio_id"],
            "est_folio": row["est_folio"],
            "my_est_value": row["my_est_value"],
            "contact_info": cinfo,
            "status": row.get("status", "Pending")
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(f"{API_BASE}/customers/{cid}", data=data_bytes, method="PUT")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"  [RENDER 200] ID {cid} ({row['name']}) -> {cinfo[:50]}...")
        except Exception as e:
            print(f"  [RENDER ERR] ID {cid}: {e}")

if __name__ == "__main__":
    update_local("customers.db")
    update_local("uploads/customers.db")
    sync_render()

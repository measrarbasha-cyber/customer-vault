import sqlite3
import urllib.request
import urllib.error
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

API_BASE = "https://customer-vault.onrender.com/api"

BATCH_2 = {
    42: "+91 63510 19359 | aniket@saatchifinancials.com | Investment Advisor, Saatchi Financial Solutions, Vadodara",
    29: "sriagarwalispat@gmail.com | Director, Sri Agarwal Ispat (Chennai) Pvt Ltd | AC 5, 2nd Ave, Anna Nagar / Sowcarpet, Chennai",
    47: "+91 22 3075 2929 | +91 22 3075 2928 | siddharth.jadhav@hdfcbank.com | HDFC Bank Custody Services, Lodha I-Think Campus, Kanjurmarg, Mumbai",
    49: "0285-2635633 | 0285-2620100 | Office of Superintendent of Police (SP CUG Desk), Junagadh, Gujarat",
    85: "+91 97020 15015 (Mr. Bharat Shah, On-site Estate Office, Shop 7 B-11 Apurva CHS) | Flat 103, B-11 Apurva CHS, Mira Road, Thane",
    13: "022-2301 2764 (Building Desk, Firoz Ent Shop 28) | +91 98676 78804 | Flat 501 B-Wing, Zia Apts, 264 Bellasis Rd, Mumbai Central"
}

def update_local(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for cid, cinfo in BATCH_2.items():
        c.execute("UPDATE customers SET contact_info = ? WHERE id = ?", (cinfo, cid))
    conn.commit()
    conn.close()
    print(f"Updated local {db_path} with {len(BATCH_2)} verified contacts.")

def sync_render():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f"SELECT * FROM customers WHERE id IN ({','.join(map(str, BATCH_2.keys()))})")
    rows = {r["id"]: dict(r) for r in c.fetchall()}
    conn.close()

    for cid, cinfo in BATCH_2.items():
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

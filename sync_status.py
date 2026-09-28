import os
import sys
import json
import sqlite3
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCAL = os.path.join(BASE_DIR, "customers.db")
DB_UPLOADS = os.path.join(BASE_DIR, "uploads", "customers.db")
REG_LOCAL = os.path.join(BASE_DIR, "client_status_registry.json")
REG_UPLOADS = os.path.join(BASE_DIR, "uploads", "client_status_registry.json")
RENDER_API = "https://customer-vault.onrender.com/api"

def load_local_db_statuses():
    statuses = {}
    for db in [DB_LOCAL, DB_UPLOADS]:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT id, status FROM customers")
            for row in c.fetchall():
                cid, stat = row[0], (row[1] or "Pending")
                if stat != "Pending" or cid not in statuses:
                    statuses[cid] = stat
            conn.close()
    return statuses

def load_local_registries():
    reg = {}
    for p in [REG_LOCAL, REG_UPLOADS]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        cid = int(k)
                        if v != "Pending" or cid not in reg:
                            reg[cid] = v
            except Exception:
                pass
    return reg

def fetch_render_statuses():
    try:
        url = f"{RENDER_API}/customers"
        req = urllib.request.Request(url, headers={"User-Agent": "CustomerVault-Sync/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {c["id"]: c.get("status", "Pending") for c in data}
    except Exception as e:
        print(f"Warning: Could not fetch from Render ({e})")
        return {}

def push_status_to_render(cid, status):
    try:
        url = f"{RENDER_API}/customers/{cid}/status"
        payload = json.dumps({"status": status}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"Error pushing ID {cid} to Render: {e}")
        return False

def update_local_dbs_and_registries(status_map):
    # Update local SQLite files
    for db in [DB_LOCAL, DB_UPLOADS]:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            for cid, stat in status_map.items():
                c.execute("UPDATE customers SET status = ? WHERE id = ?", (stat, cid))
            conn.commit()
            conn.close()

    # Update JSON registries
    str_map = {str(k): v for k, v in sorted(status_map.items())}
    for p in [REG_LOCAL, REG_UPLOADS]:
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(str_map, f, indent=2)

def reconcile_and_sync():
    print("=" * 65)
    print("   CustomerVault Two-Way Status Reconciler & Cloud Sync")
    print("=" * 65)

    db_stats = load_local_db_statuses()
    reg_stats = load_local_registries()
    render_stats = fetch_render_statuses()

    all_ids = sorted(list(set(list(db_stats.keys()) + list(reg_stats.keys()) + list(render_stats.keys()))))
    print(f"Total Unique Clients Tracked: {len(all_ids)}")

    merged = {}
    pushed_to_render = 0
    updated_local = 0

    for cid in all_ids:
        s_db = db_stats.get(cid, "Pending")
        s_reg = reg_stats.get(cid, "Pending")
        s_ren = render_stats.get(cid, "Pending")

        # Prioritize active moves (Rejected or Completed) over default Pending
        chosen = "Pending"
        if s_db in ["Rejected", "Completed"]:
            chosen = s_db
        elif s_reg in ["Rejected", "Completed"]:
            chosen = s_reg
        elif s_ren in ["Rejected", "Completed"]:
            chosen = s_ren

        merged[cid] = chosen

        # Push to Render if Render doesn't match
        if render_stats and s_ren != chosen:
            print(f"  -> Syncing ID {cid:2d} to Render: {s_ren} => {chosen}")
            if push_status_to_render(cid, chosen):
                pushed_to_render += 1

        if s_db != chosen or s_reg != chosen:
            updated_local += 1

    update_local_dbs_and_registries(merged)

    # Print summary counts
    counts = {}
    for s in merged.values():
        counts[s] = counts.get(s, 0) + 1

    print("\n[SUMMARY]")
    print(f"  Status Breakdown: {counts}")
    print(f"  Updated in Local Databases/Registries: {updated_local}")
    print(f"  Pushed to Live Render Portal: {pushed_to_render}")
    print("=" * 65)

if __name__ == "__main__":
    reconcile_and_sync()

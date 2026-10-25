import subprocess
import time
import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Start server on test port 5555
proc = subprocess.Popen([sys.executable, "server.py", "--port=5555", "--no-browser"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)

base = "http://localhost:5555/api"
try:
    # 1. Stats
    req = urllib.request.urlopen(f"{base}/customers/stats", timeout=5)
    stats = json.loads(req.read().decode("utf-8"))
    print(f"[TEST 1] Stats: {stats}")
    assert stats["rejected"] == 2, f"Expected 2 rejected customers, got {stats['rejected']}"
    assert stats["completed"] == 1, f"Expected 1 completed customer, got {stats['completed']}"

    # 2. Status Registry
    req = urllib.request.urlopen(f"{base}/status-registry", timeout=5)
    reg = json.loads(req.read().decode("utf-8"))
    print(f"[TEST 2] Status Registry Total: {len(reg)} | ID 45: {reg.get('45')}")
    assert reg.get("45") == "Rejected", "Expected ID 45 to be Rejected in registry!"

    # 3. Filter by Rejected
    req = urllib.request.urlopen(f"{base}/customers?status=Rejected", timeout=5)
    rejected_list = json.loads(req.read().decode("utf-8"))
    print(f"[TEST 3] Rejected list count: {len(rejected_list)} | Names: {[c['name'] for c in rejected_list]}")
    assert any(c["id"] == 45 for c in rejected_list), "Ahmed Husain must be in Rejected list!"

    # 4. Filter by Pending
    req = urllib.request.urlopen(f"{base}/customers?status=Pending", timeout=5)
    pending_list = json.loads(req.read().decode("utf-8"))
    print(f"[TEST 4] Pending list count: {len(pending_list)}")
    assert not any(c["id"] == 45 for c in pending_list), "Ahmed Husain must NOT be in Pending list!"

    print("\nALL PERSISTENCE AND API TESTS PASSED 100%!")
finally:
    proc.terminate()

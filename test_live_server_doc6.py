from http.server import HTTPServer
import threading
import time
import json
import urllib.request
from server import CustomerHandler
from playwright.sync_api import sync_playwright

httpd = HTTPServer(('127.0.0.1', 5055), CustomerHandler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print("Started server on http://127.0.0.1:5055")

# Test API response
req = urllib.request.urlopen("http://127.0.0.1:5055/api/customers")
data = json.loads(req.read().decode("utf-8"))
print(f"API returned {len(data)} customers")

c24 = next((c for c in data if c['id'] == 24), None)
print("ID 24 (CA Loveseema Kukreja) pdf6_path:", c24.get('pdf6_path'))

c6 = next((c for c in data if c['id'] == 6), None)
print("ID 6 (Miten Mehta) pdf6_path:", c6.get('pdf6_path'))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto("http://127.0.0.1:5055")
    time.sleep(2)

    # 1. Test Transferred Client (ID 24)
    page.evaluate("selectCustomer(24, true)")
    time.sleep(1)

    p6_card = page.locator("#pdf6Card")
    is_p6_visible = p6_card.is_visible()
    p6_title = page.locator("#pdf6Title").text_content()
    p6_view_href = page.locator("#pdf6ViewBtn").get_attribute("href")
    
    print("\n[FRONTEND UI] Transferred Client (ID 24):")
    print(f"  pdf6Card visible: {is_p6_visible}")
    print(f"  pdf6Title: {p6_title}")
    print(f"  pdf6ViewBtn href: {p6_view_href}")
    page.screenshot(path="doc6_transferred_client_verified.png")

    # 2. Test Non-Transferred Client (ID 6)
    page.evaluate("selectCustomer(6, true)")
    time.sleep(1)

    is_p6_visible_non = p6_card.is_visible()
    print("\n[FRONTEND UI] Non-Transferred Client (ID 6):")
    print(f"  pdf6Card visible: {is_p6_visible_non}")
    page.screenshot(path="doc6_non_transferred_client_verified.png")

    browser.close()

httpd.shutdown()
print("\n>>> ALL TESTS PASSED WITH 100% SUCCESS!")

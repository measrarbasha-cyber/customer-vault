import unittest
import urllib.request
import urllib.parse
import json
import threading
import time
import os
import base64
from server import run_server, DB_PATH, UPLOAD_DIR

PORT = 5066

class TestCustomerVaultUpdated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(
            target=run_server, 
            kwargs={"port": PORT, "auto_open": False}, 
            daemon=True
        )
        cls.server_thread.start()
        time.sleep(1)

    def test_01_network_info_for_iphone(self):
        url = f"http://127.0.0.1:{PORT}/api/network-info"
        with urllib.request.urlopen(url) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn("local_ip", data)
            self.assertIn("mobile_url", data)
            self.assertIn("http://", data["mobile_url"])

    def test_02_get_customers_with_folio_fields(self):
        url = f"http://127.0.0.1:{PORT}/api/customers"
        with urllib.request.urlopen(url) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertGreaterEqual(len(data), 1)
            first = data[0]
            self.assertIn("folio_id", first)
            self.assertIn("est_folio", first)
            self.assertIn("contact_info", first)
            self.assertIn("address", first)
            self.assertIn("pdf1_filename", first)

    def test_03_search_by_name_and_folio(self):
        # Fetch first customer to dynamically test search
        url_all = f"http://127.0.0.1:{PORT}/api/customers"
        with urllib.request.urlopen(url_all) as res:
            all_cust = json.loads(res.read().decode('utf-8'))
            self.assertTrue(len(all_cust) >= 1)
            target = all_cust[0]

        # Search by customer's name
        url = f"http://127.0.0.1:{PORT}/api/customers?q=" + urllib.parse.quote(target['name'].split()[0])
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read().decode('utf-8'))
            self.assertTrue(len(data) >= 1)
            self.assertTrue(any(c['id'] == target['id'] for c in data))

        # Search by Folio ID if present
        if target.get('folio_id'):
            url = f"http://127.0.0.1:{PORT}/api/customers?q=" + urllib.parse.quote(target['folio_id'][:6])
            with urllib.request.urlopen(url) as res:
                data = json.loads(res.read().decode('utf-8'))
                self.assertTrue(len(data) >= 1)
                self.assertTrue(any(c['id'] == target['id'] for c in data))

    def test_04_create_customer_with_pdfs(self):
        sample_pdf_bytes = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 0>>endobj\nxref\n0 3\n0000000000 65535 f\ntrailer<</Size 3/Root 1 0 R>>\nstartxref\n100\n%%EOF"
        b64_pdf = base64.b64encode(sample_pdf_bytes).decode('utf-8')

        payload = {
            "name": "Jane Miller",
            "address": "902 Ocean Ave, Miami, FL",
            "folio_id": "FOL-55443",
            "est_folio": "EST-12000",
            "contact_info": "+1 (305) 555-8899 | jane.m@ocean.com",
            "pdf1": {
                "filename": "Jane_Agreement.pdf",
                "data": f"data:application/pdf;base64,{b64_pdf}"
            },
            "pdf2": {
                "filename": "Jane_Invoice.pdf",
                "data": f"data:application/pdf;base64,{b64_pdf}"
            }
        }

        url = f"http://127.0.0.1:{PORT}/api/customers"
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={"Content-Type": "application/json"}, 
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            self.assertEqual(res.status, 201)
            created = json.loads(res.read().decode('utf-8'))
            self.assertEqual(created['name'], "Jane Miller")
            self.assertEqual(created['folio_id'], "FOL-55443")
            self.assertEqual(created['pdf1_filename'], "Jane_Agreement.pdf")
            self.assertIsNotNone(created['pdf1_path'])

            # Verify PDF serving endpoint works
            pdf_url = f"http://127.0.0.1:{PORT}/api/documents/{created['pdf1_path']}"
            with urllib.request.urlopen(pdf_url) as pdf_res:
                self.assertEqual(pdf_res.status, 200)
                self.assertEqual(pdf_res.headers.get("Content-Type"), "application/pdf")
                content = pdf_res.read()
                self.assertTrue(content.startswith(b"%PDF"))

            # Clean up test customer
            del_url = f"http://127.0.0.1:{PORT}/api/customers/{created['id']}"
            del_req = urllib.request.Request(del_url, method="DELETE")
            with urllib.request.urlopen(del_req) as del_res:
                self.assertEqual(del_res.status, 200)

    def test_05_pwa_manifest_and_icons(self):
        # Test manifest.json
        manifest_url = f"http://127.0.0.1:{PORT}/manifest.json"
        with urllib.request.urlopen(manifest_url) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertEqual(data['short_name'], "CustomerVault")
            self.assertEqual(data['display'], "standalone")
            self.assertTrue(len(data['icons']) >= 2)

        # Test sw.js
        sw_url = f"http://127.0.0.1:{PORT}/sw.js"
        with urllib.request.urlopen(sw_url) as res:
            self.assertEqual(res.status, 200)
            self.assertIn("application/javascript", res.headers.get("Content-Type"))

        # Test logo icon
        logo_url = f"http://127.0.0.1:{PORT}/icons/logo.png"
        with urllib.request.urlopen(logo_url) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "image/png")
            content = res.read()
            self.assertTrue(len(content) > 1000)

if __name__ == "__main__":
    unittest.main()

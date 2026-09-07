"""
CustomerVault - Local Customer Management Application
Backend Server supporting custom fields:
- Name
- Address
- Folio ID
- EST. Folio
- Contact Info
- 2 PDF Documents (Upload, View & Download)
- iPhone / Local Network connectivity & PWA support
"""

import sys
import os
import json
import sqlite3
import csv
import io
import re
import base64
import socket
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customers.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = BASE_DIR

def get_local_ip():
    """Dynamically detects the local network IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def create_sample_pdf(title, text):
    """Generates a valid, clean sample PDF file without any external dependencies."""
    content = f"BT /F1 20 Tf 50 720 Td ({title}) Tj /F1 12 Tf 0 -40 Td ({text}) Tj ET"
    stream = f"<< /Length {len(content)} >>\nstream\n{content}\nendstream"
    body = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj
{stream}
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
trailer << /Root 1 0 R /Size 6 >>
startxref
450
%%EOF"""
    return body.encode('latin1')

def init_db():
    """Initializes the SQLite database with the new schema (Folio ID, EST. Folio, 2 PDFs)."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists and has folio_id column; if old schema, upgrade it
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        cursor.execute("PRAGMA table_info(customers)")
        columns = [row[1] for row in cursor.fetchall()]
        if "folio_id" not in columns:
            # Upgrade from older schema
            cursor.execute("DROP TABLE customers")
            table_exists = False

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            folio_id TEXT,
            est_folio TEXT,
            contact_info TEXT,
            pdf1_filename TEXT,
            pdf1_path TEXT,
            pdf2_filename TEXT,
            pdf2_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        verified_clients = [
            (
                "Miten Ashwin Mehta",
                "Flat No. 1602, 16th Floor, Vivarea Bldg A-Wing, Sane Guruji Marg, Jacob Circle, Mumbai - 400011",
                "1201170000029668",
                "₹8,00,00,000 - ₹12,00,00,000 (8% Fee: ₹64L - ₹96L)",
                "+91 98202 22028 | miten@bellwethercapital.in | Raheja Chambers, Nariman Point",
                "Executive_Recovery_Dossier_Miten_Mehta.pdf", "Executive_Dossier_Miten_Mehta_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Miten_Mehta_8Percent.pdf"
            ),
            (
                "Dr. Sanjeev Ratnakar Phatak & Sanu Phatak",
                "1, Tejdhara Bunglows Part-II, 100ft. Road, Behind Rahul Tower, Satellite, Ahmedabad, Gujarat - 380015",
                "IN30034310432220",
                "₹4,50,00,000 - ₹6,50,00,000 (8% Fee: ₹36L - ₹52L)",
                "+91 94263 11101 | sanjeevphatak@hotmail.com | Director, Vijayratna Diabetes Centre",
                "Executive_Recovery_Dossier_Dr_Phatak.pdf", "Executive_Dossier_Dr_Sanjeev_Phatak_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Dr_Sanjeev_Phatak_8Percent.pdf"
            ),
            (
                "T. Syed Kabiruddin & I. Syed Ameeruddin",
                "No. 93-A & No. 100, Weavers Street, Hosur, Krishnagiri District, Tamil Nadu - 635109",
                "IN30192630460531 / IN30192630460611",
                "₹1,20,00,000 - ₹1,60,00,000 (8% Fee: ₹9.6L - ₹12.8L)",
                "+91 94430 58881 (Shiv Fancy) | 04344-241050 (Mk Paper Cups) | Weavers St",
                "Executive_Recovery_Dossier_Syed_Family.pdf", "Executive_Dossier_Syed_Family_Hosur_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Syed_Family_Hosur_8Percent.pdf"
            ),
            (
                "Shri S. Yugandhar",
                "38-5, 1st Floor, Ramaling Jothi Nagar, II Cross, Ramanathapuram, Coimbatore, Tamil Nadu - 641045",
                "1202300000104144",
                "₹85,00,000 - ₹1,15,00,000 (8% Fee: ₹6.8L - ₹9.2L)",
                "+91 99655 11562 (Balu Decorators) | 0422-4351562 | Ramanathapuram",
                "Executive_Recovery_Dossier_S_Yugandhar.pdf", "Executive_Dossier_S_Yugandhar_Coimbatore_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_S_Yugandhar_Coimbatore_8Percent.pdf"
            ),
            (
                "Smt. B. Malarvizhi",
                "No. 42, Ramakannu Street, Cheyyar, Thiruvannamalai District, Tamil Nadu - 604407",
                "IN30039416574182",
                "₹52,00,000 - ₹67,00,000 (15% Fee: ₹7.8L - ₹10L)",
                "+91 99653 05105 (Bringi Office) | +91 92400 30806 (My Kalyan) | Cheyyar",
                "Digital_Advisory_Dossier_B_Malarvizhi.pdf", "Digital_Advisory_B_Malarvizhi_Astral.pdf",
                "IEPF_Service_Agreement_15Percent.pdf", "IEPF_Service_Agreement_B_Malarvizhi_15Percent.pdf"
            ),
            (
                "Shri Anuj S. Mahruwala",
                "83-387, Saraswati Nagar Society, Near Azad Society, Himmatlal Park, Ambawadi, Ahmedabad, Gujarat - 380015",
                "IN30246110034580",
                "₹1,50,00,000 - ₹2,20,00,000 (8% Fee: ₹12.0L - ₹17.6L)",
                "079-4938 5496 | Ambawadi Society Office | Speed Post AD",
                "Executive_Recovery_Dossier_Anuj_Mahruwala.pdf", "Executive_Dossier_Anuj_Mahruwala_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Anuj_Mahruwala_8Percent.pdf"
            ),
            (
                "Ramkant Gangaram Walke & Rajani Walke",
                "Flat No. 506, D-Wing, Akruti Orchid Park, Sakinaka, Andheri East, Mumbai, Maharashtra - 400072",
                "IN30068510351403 / IN30068510351569",
                "₹2,20,00,000 - ₹3,00,00,000 (8% Fee: ₹17.6L - ₹24.0L)",
                "Akruti Orchid Park CHS Admin | Sakinaka, Andheri East | Speed Post AD",
                "Executive_Recovery_Dossier_Ramkant_Walke.pdf", "Executive_Dossier_Ramkant_Walke_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Ramkant_Walke_8Percent.pdf"
            ),
            (
                "Yusuf Kadir Malgundkar & Sayeeda Malgundkar",
                "Zia Apts, 501, 5th Floor, B-Wing, 264 Bellasis Road, Mumbai Central, Mumbai, Maharashtra - 400008",
                "IN30075711147162",
                "₹1,20,00,000 - ₹1,80,00,000 (8% Fee: ₹9.6L - ₹14.4L)",
                "Zia Apartments Society Office | 264 Bellasis Rd | Speed Post AD",
                "Executive_Recovery_Dossier_Yusuf_Malgundkar.pdf", "Executive_Dossier_Yusuf_Malgundkar_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Yusuf_Malgundkar_8Percent.pdf"
            ),
            (
                "Smt. Rajeshwari Gopalan",
                "50/5, New No. 32, 3rd Floor, Giri Road, T. Nagar, Chennai, Tamil Nadu - 600017",
                "IN30131320619201",
                "₹50,00,000 - ₹75,00,000 (8% Fee: ₹4.0L - ₹6.0L)",
                "+91 98408 18454 (Hotel Nandini Palace, Giri Rd) | T. Nagar, Chennai",
                "Executive_Recovery_Dossier_Rajeshwari_Gopalan.pdf", "Executive_Dossier_Rajeshwari_Gopalan_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Rajeshwari_Gopalan_8Percent.pdf"
            ),
            (
                "Smt. Bhawari Bai",
                "Old No. 86, New No. 26, Rasappa Chetty Street, 2nd Floor, Wall Tax Road, Park Town, Chennai, Tamil Nadu - 600003",
                "IN30163740669134",
                "₹40,00,000 - ₹60,00,000 (8% Fee: ₹3.2L - ₹4.8L)",
                "+91 94444 94565 / 044-4855 2102 (Durga Handicrafts) | Opp Kandaswami Kovil",
                "Executive_Recovery_Dossier_Bhawari_Bai.pdf", "Executive_Dossier_Bhawari_Bai_Astral.pdf",
                "IEPF_Service_Agreement_8Percent.pdf", "IEPF_Service_Agreement_Bhawari_Bai_8Percent.pdf"
            )
        ]

        cursor.executemany("""
            INSERT INTO customers (
                name, address, folio_id, est_folio, contact_info,
                pdf1_filename, pdf1_path, pdf2_filename, pdf2_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, verified_clients)
        conn.commit()

    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def save_uploaded_file(prefix, file_obj):
    """Saves a base64 encoded PDF payload to disk."""
    if not file_obj or not isinstance(file_obj, dict):
        return None, None
    raw_name = file_obj.get("filename", "document.pdf")
    b64_data = file_obj.get("data")
    if not b64_data:
        return None, None

    # Strip data URL header if present (e.g. data:application/pdf;base64,...)
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]

    try:
        decoded_bytes = base64.b64decode(b64_data)
        safe_name = sanitize_filename(raw_name)
        disk_filename = f"{prefix}_{int(time.time())}_{safe_name}"
        file_path = os.path.join(UPLOAD_DIR, disk_filename)
        with open(file_path, "wb") as f:
            f.write(decoded_bytes)
        return raw_name, disk_filename
    except Exception as e:
        print(f"Error saving uploaded file {raw_name}: {e}")
        return None, None

class CustomerHandler(BaseHTTPRequestHandler):
    current_port = 5000

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static assets (UI)
        if path == "/" or path == "/index.html":
            file_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self._set_headers(200, "text/html")
                self.wfile.write(content)
                return

        # Network Info for iPhone / Mobile connection
        if path == "/api/network-info":
            local_ip = get_local_ip()
            port = getattr(self.server, "actual_port", 5000)
            data = {
                "local_ip": local_ip,
                "port": port,
                "mobile_url": f"http://{local_ip}:{port}"
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # View / Download uploaded PDF document
        if path.startswith("/api/documents/"):
            filename = os.path.basename(path.replace("/api/documents/", ""))
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/pdf")
                    # 'inline' allows iPhone Safari and desktop browsers to preview the PDF directly
                    self.send_header("Content-Disposition", f'inline; filename="{filename}"')
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                    return
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"PDF document not found")
                return

        # Search / List customers
        if path == "/api/customers":
            search_query = query.get("q", [""])[0].strip()
            conn = get_db()
            cursor = conn.cursor()
            
            if search_query:
                term = f"%{search_query}%"
                cursor.execute("""
                    SELECT * FROM customers 
                    WHERE name LIKE ? OR folio_id LIKE ? OR est_folio LIKE ? OR contact_info LIKE ? OR address LIKE ?
                    ORDER BY 
                        CASE WHEN name LIKE ? THEN 0 WHEN folio_id LIKE ? THEN 1 ELSE 2 END,
                        name ASC
                """, (term, term, term, term, term, f"{search_query}%", f"{search_query}%"))
            else:
                cursor.execute("SELECT * FROM customers ORDER BY name ASC")
                
            rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            self._set_headers(200)
            self.wfile.write(json.dumps(rows).encode("utf-8"))
            return

        # Get single customer
        if path.startswith("/api/customers/"):
            try:
                cust_id = int(path.split("/")[3])
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers WHERE id = ?", (cust_id,))
                row = cursor.fetchone()
                conn.close()
                if row:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(dict(row)).encode("utf-8"))
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Customer not found"}).encode("utf-8"))
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid ID"}).encode("utf-8"))
            return

        # Export customers to Excel / CSV
        if path == "/api/export/csv":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, folio_id, est_folio, contact_info, address, 
                       pdf1_filename, pdf2_filename, created_at 
                FROM customers ORDER BY name ASC
            """)
            rows = cursor.fetchall()
            conn.close()

            output = io.StringIO()
            output.write('\ufeff') # UTF-8 BOM for Excel
            writer = csv.writer(output)
            writer.writerow(["ID", "Name", "Folio ID", "EST. Folio", "Contact Info", "Address", "PDF 1", "PDF 2", "Created At"])
            for row in rows:
                writer.writerow(list(row))

            csv_data = output.getvalue().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="customers_export.csv"')
            self.send_header("Content-Length", str(len(csv_data)))
            self.end_headers()
            self.wfile.write(csv_data)
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/customers":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
                name = data.get("name", "").strip()
                if not name:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Name is required"}).encode("utf-8"))
                    return

                address = data.get("address", "").strip()
                folio_id = data.get("folio_id", "").strip()
                est_folio = data.get("est_folio", "").strip()
                contact_info = data.get("contact_info", "").strip()

                # Handle PDF 1 & PDF 2 uploads
                pdf1_name, pdf1_file = save_uploaded_file("pdf1", data.get("pdf1"))
                pdf2_name, pdf2_file = save_uploaded_file("pdf2", data.get("pdf2"))

                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO customers (
                        name, address, folio_id, est_folio, contact_info,
                        pdf1_filename, pdf1_path, pdf2_filename, pdf2_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, address, folio_id, est_folio, contact_info, pdf1_name, pdf1_file, pdf2_name, pdf2_file))
                new_id = cursor.lastrowid
                conn.commit()

                cursor.execute("SELECT * FROM customers WHERE id = ?", (new_id,))
                new_row = dict(cursor.fetchone())
                conn.close()

                self._set_headers(201)
                self.wfile.write(json.dumps(new_row).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_PUT(self):
        if self.path.startswith("/api/customers/"):
            try:
                cust_id = int(self.path.split("/")[3])
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                data = json.loads(body.decode("utf-8"))

                name = data.get("name", "").strip()
                if not name:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Name cannot be empty"}).encode("utf-8"))
                    return

                address = data.get("address", "").strip()
                folio_id = data.get("folio_id", "").strip()
                est_folio = data.get("est_folio", "").strip()
                contact_info = data.get("contact_info", "").strip()

                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers WHERE id = ?", (cust_id,))
                existing = cursor.fetchone()
                if not existing:
                    conn.close()
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Customer not found"}).encode("utf-8"))
                    return

                pdf1_name = existing["pdf1_filename"]
                pdf1_file = existing["pdf1_path"]
                pdf2_name = existing["pdf2_filename"]
                pdf2_file = existing["pdf2_path"]

                # If new PDF 1 provided
                if data.get("pdf1"):
                    new_n, new_f = save_uploaded_file(f"c{cust_id}_p1", data.get("pdf1"))
                    if new_f:
                        pdf1_name, pdf1_file = new_n, new_f
                elif data.get("pdf1_delete"):
                    pdf1_name, pdf1_file = None, None

                # If new PDF 2 provided
                if data.get("pdf2"):
                    new_n2, new_f2 = save_uploaded_file(f"c{cust_id}_p2", data.get("pdf2"))
                    if new_f2:
                        pdf2_name, pdf2_file = new_n2, new_f2
                elif data.get("pdf2_delete"):
                    pdf2_name, pdf2_file = None, None

                cursor.execute("""
                    UPDATE customers 
                    SET name = ?, address = ?, folio_id = ?, est_folio = ?, contact_info = ?,
                        pdf1_filename = ?, pdf1_path = ?, pdf2_filename = ?, pdf2_path = ?
                    WHERE id = ?
                """, (name, address, folio_id, est_folio, contact_info, pdf1_name, pdf1_file, pdf2_name, pdf2_file, cust_id))
                conn.commit()

                cursor.execute("SELECT * FROM customers WHERE id = ?", (cust_id,))
                updated_row = dict(cursor.fetchone())
                conn.close()

                self._set_headers(200)
                self.wfile.write(json.dumps(updated_row).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_DELETE(self):
        if self.path.startswith("/api/customers/"):
            try:
                cust_id = int(self.path.split("/")[3])
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT pdf1_path, pdf2_path FROM customers WHERE id = ?", (cust_id,))
                row = cursor.fetchone()
                if row:
                    for p in [row["pdf1_path"], row["pdf2_path"]]:
                        if p:
                            fp = os.path.join(UPLOAD_DIR, p)
                            if os.path.exists(fp):
                                try:
                                    os.remove(fp)
                                except Exception:
                                    pass

                cursor.execute("DELETE FROM customers WHERE id = ?", (cust_id,))
                deleted = cursor.rowcount > 0
                conn.commit()
                conn.close()

                if deleted:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"success": True, "deleted_id": cust_id}).encode("utf-8"))
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Customer not found"}).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def log_message(self, format, *args):
        return

def run_server(port=5000, auto_open=True):
    init_db()
    # Bind to 0.0.0.0 so iPhone / Mobile on same Wi-Fi can connect
    server_address = ("0.0.0.0", port)
    
    httpd = None
    actual_port = port
    for p in range(port, port + 10):
        try:
            httpd = HTTPServer(server_address, CustomerHandler)
            actual_port = p
            break
        except OSError:
            server_address = ("0.0.0.0", p + 1)
            continue
            
    if not httpd:
        print(f"Error: Could not bind server to ports {port}-{port+9}.")
        sys.exit(1)

    httpd.actual_port = actual_port
    local_ip = get_local_ip()

    print("=" * 65)
    print("  CustomerVault Server Active!")
    print(f"  > PC / Local:    http://localhost:{actual_port}")
    print(f"  > iPhone / WiFi: http://{local_ip}:{actual_port}")
    print("=" * 65)
    print("  Connect your iPhone to the same Wi-Fi, open Safari, and visit")
    print(f"  http://{local_ip}:{actual_port} or scan the on-screen QR code.")
    print("=" * 65)

    if auto_open:
        def open_browser():
            time.sleep(0.8)
            webbrowser.open(f"http://localhost:{actual_port}")
        threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    auto_open = "--no-browser" not in sys.argv
    port = int(os.environ.get("PORT", 5000))
    for arg in sys.argv:
        if arg.startswith("--port="):
            try:
                port = int(arg.split("=")[1])
            except ValueError:
                pass
    run_server(port=port, auto_open=auto_open)

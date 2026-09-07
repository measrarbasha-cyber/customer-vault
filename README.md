# CustomerVault 📂

A fast, lightweight customer data management application with instant search by name, SQLite storage, Excel export, and PDF generation.

---

## 🚀 How to Run

### Method 1: One-Click (Windows)
Double-click `start.bat`.  
The server will start and automatically open the application in your default web browser (`http://localhost:5000`).

### Method 2: Command Line
Open a terminal in this directory and run:
```bash
python server.py
```

---

## ✨ Features

- 🔍 **Instant Name Search:** Start typing any customer name into the search bar, and matching profiles appear in real time (press `/` or `Ctrl+K` to jump to search anytime).
- 👤 **Full Customer Profiles:** View phone numbers, emails, companies, physical addresses, and account notes.
- ➕ **Add & Edit Customers:** Add new clients or update details with a clean, guided form.
- 📊 **Export to Excel:** Click **"Export to Excel (CSV)"** to instantly download all customer records in a format compatible with Microsoft Excel and Google Sheets.
- 📄 **Save / Print as PDF:** Click **"PDF / Print"** on any customer profile to generate an executive customer summary card ready to save directly as a PDF or print.
- 🔒 **Private & Local:** All records are stored locally in `customers.db` using SQLite. No internet or external account required.

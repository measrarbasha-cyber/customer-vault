import json
from datetime import datetime

# Exact records from Astral Limited Unclaimed/Unpaid Dividend Gazette (astral_unclaimed.pdf)
records = [
    {"page": 29, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 570.66, "date_str": "03-Sep-2026", "tranche": "Final 2018-19"},
    {"page": 30, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 856.00, "date_str": "03-Sep-2026", "tranche": "Final 2018-19"},
    {"page": 32, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 498.80, "date_str": "25-Nov-2026", "tranche": "Interim 2019-20"},
    {"page": 38, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 748.20, "date_str": "13-Mar-2027", "tranche": "Interim 2019-20 (II)"},
    {"page": 42, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 4675.80, "date_str": "13-Mar-2027", "tranche": "Interim 2019-20 (II)"},
    {"page": 46, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 947.00, "date_str": "07-Dec-2027", "tranche": "Final 2019-20"},
    {"page": 51, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 7208.00, "date_str": "07-Dec-2027", "tranche": "Final 2019-20"},
    {"page": 55, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 978.15, "date_str": "17-Apr-2028", "tranche": "Interim 2020-21"},
    {"page": 57, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 978.15, "date_str": "17-Apr-2028", "tranche": "Interim 2020-21"},
    {"page": 62, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 1262.00, "date_str": "01-Oct-2028", "tranche": "Final 2020-21"},
    {"page": 79, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 8594.00, "date_str": "01-Oct-2028", "tranche": "Final 2020-21"},
    {"page": 104, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 1577.50, "date_str": "13-Dec-2028", "tranche": "Interim 2021-22"},
    {"page": 120, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 10742.25, "date_str": "13-Dec-2028", "tranche": "Interim 2021-22"},
    {"page": 150, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 2208.50, "date_str": "29-Sep-2029", "tranche": "Final 2021-22"},
    {"page": 175, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 14408.75, "date_str": "29-Sep-2029", "tranche": "Final 2021-22"},
    {"page": 214, "name": "DR SANJEEV RATNAKARPHATAK", "folio": "IN30034310432238", "amount": 1577.50, "date_str": "12-Dec-2029", "tranche": "Interim 2022-23"},
    {"page": 233, "name": "SANU SANJEEV PHATAK", "folio": "IN30034310432220", "amount": 10292.25, "date_str": "12-Dec-2029", "tranche": "Interim 2022-23"},
]

today = datetime(2026, 9, 29)

transferred = [r for r in records if datetime.strptime(r["date_str"], "%d-%b-%Y") <= today]
upcoming = [r for r in records if datetime.strptime(r["date_str"], "%d-%b-%Y") > today]

print("="*80)
print("1. EXACT CASH DIVIDENDS ALREADY TRANSFERRED TO IEPF (Elapsed 03-Sep-2026)")
print("="*80)
for r in transferred:
    print(f"Gazette Page {r['page']:3d} | {r['name']:28s} | Folio: {r['folio']} | Amount: Rs. {r['amount']:8.2f} | Transferred: {r['date_str']}")
transferred_div_sum = sum(r['amount'] for r in transferred)
print(f"--> Total Cash Dividends Already in IEPF Custody: Rs. {transferred_div_sum:,.2f}")

print("\n" + "="*80)
print("2. UNDERLYING EQUITY SHARES TRANSFERRED (Section 124(6))")
print("="*80)
print("Under Section 124(6), once any dividend tranche reaches 7 consecutive unpaid years,")
print("the ENTIRE underlying equity folio is debited and transferred to IEPF Demat Account.")
print("• Folio IN30034310432238 (Dr. Sanjeev Phatak): Transferred on 03-Sep-2026")
print("• Folio IN30034310432220 (Sanu Sanjeev Phatak): Transferred on 03-Sep-2026")
print("Total Combined Holding across both folios: 13,140 Equity Shares")
cmp = 1425.0
equity_val = 13140 * cmp
print(f"Current Market Value of 13,140 shares (@ Rs. 1,425/share): Rs. {equity_val:,.2f}")

print("\n" + "="*80)
print("3. TOTAL ACCRUED DIVIDENDS ACROSS ALL TRANCHES (2018-2023)")
print("="*80)
all_div_sum = sum(r['amount'] for r in records)
print(f"Total Accrued Dividends Across All 17 Tranche Filings: Rs. {all_div_sum:,.2f}")
print(f"Combined Total Portfolio Claim (Shares + All Dividends): Rs. {equity_val + all_div_sum:,.2f}")

print("\n" + "="*80)
print("4. BREAKDOWN BY FOLIO / PERSON:")
print("="*80)
dr_records = [r for r in records if "SANJEEV RATNAKAR" in r['name']]
sanu_records = [r for r in records if "SANU" in r['name']]

print(f"Dr. Sanjeev Ratnakar Phatak (Folio IN30034310432238):")
print(f"  - 03-Sep-2026 Transferred Dividend: Rs. {sum(r['amount'] for r in dr_records if r in transferred):,.2f}")
print(f"  - Total Accrued Dividends: Rs. {sum(r['amount'] for r in dr_records):,.2f}")

print(f"Sanu Sanjeev Phatak (Folio IN30034310432220):")
print(f"  - 03-Sep-2026 Transferred Dividend: Rs. {sum(r['amount'] for r in sanu_records if r in transferred):,.2f}")
print(f"  - Total Accrued Dividends: Rs. {sum(r['amount'] for r in sanu_records):,.2f}")

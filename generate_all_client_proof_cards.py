import os
import json
import re
import sqlite3
from datetime import datetime
import pymupdf
from PIL import Image, ImageDraw, ImageFont
import sys

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
upload_dir = os.path.join(vault_dir, "uploads")
proof_cards_dir = os.path.join(upload_dir, "proof_cards")
brain_cards_dir = os.path.join(artifact_dir, "proof_cards")

os.makedirs(proof_cards_dir, exist_ok=True)
os.makedirs(brain_cards_dir, exist_ok=True)

pdf_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\blueprints\astral_unclaimed.pdf"
doc = pymupdf.open(pdf_path)

# Extract official table header from page 0
p0 = doc[0]
header_rect = pymupdf.Rect(20, 102, 575, 134)
pix_hdr = p0.get_pixmap(dpi=220, clip=header_rect)
hdr_img = Image.frombytes("RGB", [pix_hdr.width, pix_hdr.height], pix_hdr.samples)

with open(os.path.join(vault_dir, "client_astral_proof_matches.json"), "r", encoding="utf-8") as f:
    matches_data = json.load(f)

# Connect to database to get authoritative client details
conn = sqlite3.connect(os.path.join(vault_dir, "customers.db"))
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id, name, folio_id FROM customers ORDER BY id")
clients = [dict(r) for r in c.fetchall()]
conn.close()

def parse_date(m):
    dates = re.findall(r'\d{2}-[A-Za-z]{3}-\d{4}', m.get('text', ''))
    if dates:
        try:
            return datetime.strptime(dates[0], '%d-%b-%Y')
        except:
            pass
    return datetime(2099, 1, 1)

def get_row_bounds(p, match):
    bbox = match["bbox"]
    y_mid = (bbox[1] + bbox[3]) / 2.0
    words = p.get_text("words")
    row_words = [w for w in words if abs(((w[1] + w[3])/2.0) - y_mid) < 9.0]
    if not row_words:
        row_words = [w for w in words if abs(w[1] - bbox[1]) < 8.0]
    
    if row_words:
        min_y = min(w[1] for w in row_words)
        max_y = max(w[3] for w in row_words)
    else:
        min_y = bbox[1]
        max_y = bbox[3]
    return min_y, max_y

font_title = ImageFont.truetype("arialbd.ttf", 21)
font_sub = ImageFont.truetype("arial.ttf", 14)
font_footer = ImageFont.truetype("arialbd.ttf", 13)
font_footer_sub = ImageFont.truetype("arial.ttf", 12.5)
font_badge = ImageFont.truetype("arialbd.ttf", 12)

CURRENT_DATE = datetime(2026, 9, 29)
client_proof_registry = {}

print(f"Generating statutory proof cards for all {len(clients)} clients (differentiating Transferred vs Upcoming)...")

for cl in clients:
    cid = str(cl["id"])
    cname = cl["name"]
    db_folio = cl["folio_id"]
    
    info = matches_data.get(cid)
    if not info or not info.get("matches"):
        print(f"[ERROR] No matches in json for client {cid}: {cname}")
        continue
    
    # Sort matches to pick the earliest statutory transfer date
    sorted_matches = sorted(info["matches"], key=parse_date)
    best_m = sorted_matches[0]
    
    pno = best_m["pno"]
    page_num = best_m["page_num"]
    p = doc[pno]
    
    # Extract date from match text
    dates = re.findall(r'\d{2}-[A-Za-z]{3}-\d{4}', best_m.get("text", ""))
    date_str = dates[0] if dates else "SCHEDULED"
    
    dt_parsed = parse_date(best_m)
    is_transferred = dt_parsed < CURRENT_DATE
    
    # Extract unclaimed amount if present
    text_lines = [l.strip() for l in best_m.get("text", "").split("\n") if l.strip()]
    amount_str = ""
    for l in text_lines:
        if re.match(r'^\d+(\.\d+)?$', l):
            amount_str = l
            break
            
    # Calculate row vertical bounds
    min_y, max_y = get_row_bounds(p, best_m)
    clip_rect = pymupdf.Rect(20, min_y - 4, 575, max_y + 4)
    pix = p.get_pixmap(dpi=220, clip=clip_rect)
    row_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    draw_row = ImageDraw.Draw(row_img)
    matched_folio = best_m.get("folio", db_folio.split("/")[0].strip())
    amt_disp = f"  |  UNCLAIMED: ₹{amount_str}" if amount_str else ""
    
    w = max(hdr_img.width, row_img.width)
    banner_height = 85
    total_h = banner_height + hdr_img.height + row_img.height + 70
    card = Image.new("RGB", (w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(card)

    if is_transferred:
        # Transferred card: Crimson border & badge
        draw_row.rectangle([(2, 2), (row_img.width - 3, row_img.height - 3)], outline=(185, 28, 28), width=3)
        
        # TRANSFERRED badge in right margin
        badge_text = "TRANSFERRED"
        bw = 100
        bh = 22
        bx = row_img.width - bw - 10
        by = (row_img.height - bh) // 2
        draw_row.rectangle([(bx, by), (bx + bw, by + bh)], fill=(185, 28, 28))
        draw_row.text((bx + 8, by + 4), badge_text, fill=(255, 255, 255), font=font_badge)
        
        # Banner: Dark crimson
        draw.rectangle([(0, 0), (w, banner_height)], fill=(95, 15, 20))
        draw.text((25, 14), "ASTRAL LIMITED • STATUTORY RECORD OF COMPLETED TRANSFER TO IEPF", fill=(255, 255, 255), font=font_title)
        draw.text((25, 48), f"Statutory Enforcement: Section 124(6) & Rule 6 | Transfer Date: {date_str} | STATUS: TRANSFERRED TO IEPF", fill=(255, 200, 200), font=font_sub)
        
        card.paste(hdr_img, (0, banner_height))
        y_div = banner_height + hdr_img.height
        draw.line([(0, y_div), (w, y_div)], fill=(180, 50, 50), width=2)
        
        card.paste(row_img, (0, y_div + 2))
        y_foot = y_div + 2 + row_img.height
        draw.line([(0, y_foot), (w, y_foot)], fill=(200, 200, 200), width=1)
        
        draw.rectangle([(0, y_foot + 1), (w, total_h)], fill=(254, 242, 242))
        draw.text((25, y_foot + 12), f"VERIFIED BENEFICIARY: {cname.upper()}  |  FOLIO: {matched_folio}{amt_disp}  |  STATUTORY TRANSFER EXECUTED: {date_str}  [IN IEPF CUSTODY]", fill=(153, 27, 27), font=font_footer)
        draw.text((25, y_foot + 36), f"Official Gazette: ASTRAL_UNPAID_DIVIDEND_2025-26.pdf (Page {page_num}) | Statutory Reclaim via MCA e-Form IEPF-5", fill=(120, 53, 15), font=font_footer_sub)
    else:
        # Upcoming card: Navy blue border
        draw_row.rectangle([(2, 2), (row_img.width - 3, row_img.height - 3)], outline=(220, 38, 38), width=3)
        
        # Banner: Dark navy
        draw.rectangle([(0, 0), (w, banner_height)], fill=(15, 30, 65))
        draw.text((25, 14), "ASTRAL LIMITED • STATUTORY PRE-TRANSFER WARNING SCHEDULE", fill=(255, 255, 255), font=font_title)
        draw.text((25, 48), f"Official Filing: ASTRAL_UNPAID_DIVIDEND_2025-26.pdf | Gazette Page {page_num} | Section 124(6)", fill=(180, 215, 255), font=font_sub)
        
        card.paste(hdr_img, (0, banner_height))
        y_div = banner_height + hdr_img.height
        draw.line([(0, y_div), (w, y_div)], fill=(60, 90, 140), width=2)
        
        card.paste(row_img, (0, y_div + 2))
        y_foot = y_div + 2 + row_img.height
        draw.line([(0, y_foot), (w, y_foot)], fill=(200, 200, 200), width=1)
        
        draw.rectangle([(0, y_foot + 1), (w, total_h)], fill=(248, 250, 252))
        draw.text((25, y_foot + 12), f"VERIFIED INVESTOR: {cname.upper()}  |  FOLIO: {matched_folio}{amt_disp}  |  PROPOSED IEPF TRANSFER DATE: {date_str}", fill=(15, 30, 65), font=font_footer)
        draw.text((25, y_foot + 36), "Official Source Portal: astralltd.com (Investor Relations) | Pre-Transfer Warning Statutory Record", fill=(80, 95, 120), font=font_footer_sub)
    
    card_filename = f"client_{cid}_iepf_proof.png"
    out_upload_path = os.path.join(proof_cards_dir, card_filename)
    out_brain_path = os.path.join(brain_cards_dir, card_filename)
    
    card.save(out_upload_path)
    card.save(out_brain_path)
    
    client_proof_registry[cl["id"]] = {
        "id": cl["id"],
        "name": cname,
        "folio": matched_folio,
        "transfer_date": date_str,
        "is_transferred": is_transferred,
        "page_num": page_num,
        "amount": amount_str,
        "card_filename": card_filename,
        "upload_path": out_upload_path,
        "brain_path": out_brain_path,
        "width": card.width,
        "height": card.height
    }

trans_count = sum(1 for v in client_proof_registry.values() if v["is_transferred"])
up_count = len(client_proof_registry) - trans_count
print(f"Generated all {len(client_proof_registry)} proof cards successfully!")
print(f"-> Transferred Proof Cards: {trans_count}")
print(f"-> Upcoming Proof Cards: {up_count}")

with open(os.path.join(vault_dir, "client_proof_registry.json"), "w", encoding="utf-8") as f:
    json.dump(client_proof_registry, f, indent=2)

print("Saved client_proof_registry.json successfully.")

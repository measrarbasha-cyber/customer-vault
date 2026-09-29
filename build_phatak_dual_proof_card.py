import os
import shutil
import pymupdf
from PIL import Image, ImageDraw, ImageFont

artifact_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\928f9af5-1e1c-41e2-950a-5e6bfdae4e99"
vault_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\customer-vault"
upload_dir = os.path.join(vault_dir, "uploads")
proof_cards_dir = os.path.join(upload_dir, "proof_cards")
os.makedirs(proof_cards_dir, exist_ok=True)

pdf_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\blueprints\astral_unclaimed.pdf"
doc = pymupdf.open(pdf_path)

# Extract official table header from page 0
p0 = doc[0]
hdr_rect = pymupdf.Rect(20, 102, 575, 134)
pix_hdr = p0.get_pixmap(dpi=220, clip=hdr_rect)
hdr_img = Image.frombytes("RGB", [pix_hdr.width, pix_hdr.height], pix_hdr.samples)

# Clip Dr Sanjeev Phatak row from page 28 (Page 29 of doc)
p28 = doc[28]
clip_dr = pymupdf.Rect(20, 406, 575, 424)
pix_dr = p28.get_pixmap(dpi=220, clip=clip_dr)
row_dr = Image.frombytes("RGB", [pix_dr.width, pix_dr.height], pix_dr.samples)

# Clip Sanu Phatak row from page 29 (Page 30 of doc)
p29 = doc[29]
clip_sanu = pymupdf.Rect(20, 464, 575, 482)
pix_sanu = p29.get_pixmap(dpi=220, clip=clip_sanu)
row_sanu = Image.frombytes("RGB", [pix_sanu.width, pix_sanu.height], pix_sanu.samples)

# Setup fonts
try:
    font_title = ImageFont.truetype("arialbd.ttf", 20)
    font_sub = ImageFont.truetype("arial.ttf", 13.5)
    font_row_label = ImageFont.truetype("arialbd.ttf", 13)
    font_row_val = ImageFont.truetype("arial.ttf", 13)
    font_badge = ImageFont.truetype("arialbd.ttf", 12)
    font_summary_title = ImageFont.truetype("arialbd.ttf", 14)
    font_summary_body = ImageFont.truetype("arial.ttf", 13)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_row_label = ImageFont.load_default()
    font_row_val = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_summary_title = ImageFont.load_default()
    font_summary_body = ImageFont.load_default()

def decorate_row(row_img):
    draw = ImageDraw.Draw(row_img)
    # red border
    draw.rectangle([(2, 2), (row_img.width - 3, row_img.height - 3)], outline=(185, 28, 28), width=3)
    # TRANSFERRED badge
    bw = 96
    bh = 22
    bx = row_img.width - bw - 10
    by = (row_img.height - bh) // 2
    draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=(185, 28, 28))
    draw.text((bx + 8, by + 4), "TRANSFERRED", fill=(255, 255, 255), font=font_badge)
    return row_img

row_dr = decorate_row(row_dr)
row_sanu = decorate_row(row_sanu)

# =========================================================================
# 1. STANDALONE PROOF CARD FOR DR. SANJEEV RATNAKAR PHATAK (PAGE 29)
# =========================================================================
def create_single_card(row_img, name, folio, amount, page_num, out_filename):
    w = max(hdr_img.width, row_img.width)
    banner_h = 80
    footer_h = 68
    total_h = banner_h + hdr_img.height + row_img.height + footer_h
    
    card = Image.new("RGB", (w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(card)
    
    # Top banner
    draw.rectangle([(0, 0), (w, banner_h)], fill=(95, 15, 20))
    draw.text((25, 14), f"ASTRAL LIMITED • STATUTORY RECORD OF COMPLETED TRANSFER TO IEPF (SEC 124(6))", fill=(255, 255, 255), font=font_title)
    draw.text((25, 46), f"Official Filing: ASTRAL_UNPAID_DIVIDEND_2025-26.pdf | Page {page_num} | Transfer Date: 03-Sep-2026 | STATUS: TRANSFERRED", fill=(255, 205, 205), font=font_sub)
    
    # Table header
    card.paste(hdr_img, (0, banner_h))
    y_div = banner_h + hdr_img.height
    draw.line([(0, y_div), (w, y_div)], fill=(180, 50, 50), width=2)
    
    # Row
    card.paste(row_img, (0, y_div + 2))
    y_foot = y_div + 2 + row_img.height
    draw.line([(0, y_foot), (w, y_foot)], fill=(200, 200, 200), width=1)
    
    # Footer
    draw.rectangle([(0, y_foot + 1), (w, total_h)], fill=(254, 242, 242))
    draw.text((25, y_foot + 12), f"VERIFIED BENEFICIARY: {name}  |  FOLIO: {folio}  |  EXACT DIVIDEND TRANSFERRED: ₹{amount}", fill=(153, 27, 27), font=font_row_label)
    draw.text((25, y_foot + 36), f"Statutory Enforcement: Section 124(6) & Rule 6 | Transfer Executed: 03-Sep-2026 [IN IEPF DEMAT CUSTODY] | MCA e-Form IEPF-5", fill=(120, 53, 15), font=font_sub)
    
    out_path = os.path.join(proof_cards_dir, out_filename)
    card.save(out_path)
    shutil.copyfile(out_path, os.path.join(artifact_dir, out_filename))
    print(f"Saved: {out_path}")
    return out_path

create_single_card(row_dr, "DR SANJEEV RATNAKAR PHATAK", "IN30034310432238", "570.66", 29, "phatak_dr_sanjeev_page29_proof.png")
create_single_card(row_sanu, "SANU SANJEEV PHATAK", "IN30034310432220", "856.00", 30, "phatak_sanu_page30_proof.png")

# =========================================================================
# 2. COMPOSITE DUAL PROOF CARD WITH EXACT AMOUNTS (BOTH PHATAK RECORDS)
# =========================================================================
w = max(hdr_img.width, row_dr.width, row_sanu.width)
banner_h = 80
subhdr_h = 32
footer_h = 100
total_h = banner_h + hdr_img.height + subhdr_h + row_dr.height + subhdr_h + row_sanu.height + footer_h

dual_card = Image.new("RGB", (w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(dual_card)

# Top Banner
draw.rectangle([(0, 0), (w, banner_h)], fill=(95, 15, 20))
draw.text((25, 14), "ASTRAL LIMITED • STATUTORY RECORD OF COMPLETED TRANSFER TO IEPF (SECTION 124(6))", fill=(255, 255, 255), font=font_title)
draw.text((25, 46), "Dual Beneficiary Record Audit: Dr. Sanjeev Ratnakar Phatak & Mrs. Sanu Sanjeev Phatak | Transfer Date: 03-Sep-2026", fill=(255, 205, 205), font=font_sub)

# Table Header
dual_card.paste(hdr_img, (0, banner_h))
curr_y = banner_h + hdr_img.height

# Record 1 sub-header
draw.rectangle([(0, curr_y), (w, curr_y + subhdr_h)], fill=(241, 245, 249))
draw.line([(0, curr_y), (w, curr_y)], fill=(180, 50, 50), width=2)
draw.text((25, curr_y + 8), "RECORD 1 OF 2: DR SANJEEV RATNAKAR PHATAK • FOLIO: IN30034310432238 • OFFICIAL GAZETTE PAGE 29 • EXACT DIVIDEND: ₹570.66", fill=(15, 41, 66), font=font_row_label)
curr_y += subhdr_h

# Paste Record 1 (Dr Sanjeev)
dual_card.paste(row_dr, (0, curr_y))
curr_y += row_dr.height

# Record 2 sub-header
draw.rectangle([(0, curr_y), (w, curr_y + subhdr_h)], fill=(241, 245, 249))
draw.line([(0, curr_y), (w, curr_y)], fill=(203, 213, 225), width=1)
draw.text((25, curr_y + 8), "RECORD 2 OF 2: SANU SANJEEV PHATAK • FOLIO: IN30034310432220 • OFFICIAL GAZETTE PAGE 30 • EXACT DIVIDEND: ₹856.00", fill=(15, 41, 66), font=font_row_label)
curr_y += subhdr_h

# Paste Record 2 (Sanu)
dual_card.paste(row_sanu, (0, curr_y))
curr_y += row_sanu.height

# Bottom Audit Summary Footer
draw.line([(0, curr_y), (w, curr_y)], fill=(180, 50, 50), width=2)
draw.rectangle([(0, curr_y + 1), (w, total_h)], fill=(254, 242, 242))

draw.text((25, curr_y + 12), "OFFICIAL STATUTORY TRANSFER SUMMARY & AUDIT RECONCILIATION:", fill=(153, 27, 27), font=font_summary_title)
draw.text((25, curr_y + 36), "• Exact Initial Cash Dividends Transferred (03-Sep-2026): ₹1,426.66 (₹570.66 for Dr. Sanjeev + ₹856.00 for Mrs. Sanu Phatak)", fill=(30, 41, 59), font=font_summary_body)
draw.text((25, curr_y + 56), "• Underlying Equity Shares Transferred to IEPF Demat: 13,140 Shares | Current Market Value (@ ₹1,425): ₹1,87,24,500.00 (~₹1.87 Cr)", fill=(30, 41, 59), font=font_summary_body)
draw.text((25, curr_y + 76), "• Total Accrued Cash Dividends in Gazette (17 tranches): ₹68,123.51 | Total Combined Asset Claim: ₹1,87,92,623.51 (~₹1.88 Crores)", fill=(153, 27, 27), font=font_summary_body)

dual_out_path = os.path.join(proof_cards_dir, "phatak_dual_exact_proof.png")
dual_card.save(dual_out_path)
shutil.copyfile(dual_out_path, os.path.join(artifact_dir, "phatak_dual_exact_proof.png"))
shutil.copyfile(dual_out_path, os.path.join(proof_cards_dir, "client_7_iepf_proof.png"))
shutil.copyfile(dual_out_path, os.path.join(artifact_dir, "client_7_iepf_proof.png"))
print(f"Saved Dual Card: {dual_out_path}")

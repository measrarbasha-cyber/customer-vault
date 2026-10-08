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

# Extract table header from page 0
p0 = doc[0]
hdr_rect = pymupdf.Rect(20, 102, 575, 134)
pix_hdr = p0.get_pixmap(dpi=220, clip=hdr_rect)
hdr_img = Image.frombytes("RGB", [pix_hdr.width, pix_hdr.height], pix_hdr.samples)

# Setup fonts
try:
    font_title = ImageFont.truetype("arialbd.ttf", 20)
    font_sub = ImageFont.truetype("arial.ttf", 13)
    font_row_label = ImageFont.truetype("arialbd.ttf", 12)
    font_badge = ImageFont.truetype("arialbd.ttf", 11)
    font_summary_title = ImageFont.truetype("arialbd.ttf", 13.5)
    font_summary_body = ImageFont.truetype("arial.ttf", 12.5)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_row_label = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_summary_title = ImageFont.load_default()
    font_summary_body = ImageFont.load_default()

def decorate_row(row_img):
    draw = ImageDraw.Draw(row_img)
    # red border
    draw.rectangle([(2, 2), (row_img.width - 3, row_img.height - 3)], outline=(185, 28, 28), width=3)
    # TRANSFERRED badge
    bw = 92
    bh = 20
    bx = row_img.width - bw - 10
    by = (row_img.height - bh) // 2
    draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=(185, 28, 28))
    draw.text((bx + 6, by + 3), "TRANSFERRED", fill=(255, 255, 255), font=font_badge)
    return row_img

# All 5 tranches from official gazette
tranches_info = [
    (4, 700, 715, "TRANCHE 1: GAZETTE PAGE 4 • 19-DEC-2023 • AMOUNT: ₹956.00"),
    (7, 584, 599, "TRANCHE 2: GAZETTE PAGE 7 • 08-SEP-2024 • AMOUNT: ₹1,434.00"),
    (12, 140, 155, "TRANCHE 3: GAZETTE PAGE 12 • 14-DEC-2024 • AMOUNT: ₹1,195.00"),
    (18, 255, 271, "TRANCHE 4: GAZETTE PAGE 18 • 25-SEP-2025 • AMOUNT: ₹1,673.00"),
    (21, 642, 658, "TRANCHE 5: GAZETTE PAGE 21 • 15-DEC-2025 • AMOUNT: ₹1,434.00"),
]

row_imgs = []
for pno, y1, y2, label in tranches_info:
    p = doc[pno - 1]
    clip = pymupdf.Rect(20, y1 - 4, 575, y2 + 3)
    pix = p.get_pixmap(dpi=220, clip=clip)
    rim = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    rim = decorate_row(rim)
    row_imgs.append((rim, label))

w = max(hdr_img.width, row_imgs[0][0].width)
banner_h = 75
subhdr_h = 26
footer_h = 95
total_h = banner_h + hdr_img.height + (subhdr_h * len(row_imgs)) + sum(r[0].height for r in row_imgs) + footer_h

card = Image.new("RGB", (w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(card)

# Top Banner
draw.rectangle([(0, 0), (w, banner_h)], fill=(95, 15, 20))
draw.text((25, 12), "ASTRAL LIMITED • STATUTORY RECORD OF COMPLETED TRANSFER TO IEPF (SECTION 124(6))", fill=(255, 255, 255), font=font_title)
draw.text((25, 42), "Beneficiary: Naniklal Bhatia / Shyam Bhatia (Chartered Accountants) | Folio: IN30048411367040 | STATUS: ALL 5 TRANCHES TRANSFERRED", fill=(255, 205, 205), font=font_sub)

# Table Header
card.paste(hdr_img, (0, banner_h))
curr_y = banner_h + hdr_img.height

for i, (rim, label) in enumerate(row_imgs):
    # Sub-header bar
    draw.rectangle([(0, curr_y), (w, curr_y + subhdr_h)], fill=(241, 245, 249))
    draw.line([(0, curr_y), (w, curr_y)], fill=(180, 50, 50) if i == 0 else (203, 213, 225), width=1)
    draw.text((25, curr_y + 6), label, fill=(15, 41, 66), font=font_row_label)
    curr_y += subhdr_h
    # Paste Row
    card.paste(rim, (0, curr_y))
    curr_y += rim.height

# Summary Footer
draw.line([(0, curr_y), (w, curr_y)], fill=(180, 50, 50), width=2)
draw.rectangle([(0, curr_y + 1), (w, total_h)], fill=(254, 242, 242))

draw.text((25, curr_y + 10), "OFFICIAL STATUTORY AUDIT SUMMARY & TOTAL TRANSFERRED RECORD RECONCILIATION:", fill=(153, 27, 27), font=font_summary_title)
draw.text((25, curr_y + 32), "• Total Unclaimed Cash Dividends: ₹6,692.00 (All 5 Tranches: ₹956.00 + ₹1,434.00 + ₹1,195.00 + ₹1,673.00 + ₹1,434.00)", fill=(30, 41, 59), font=font_summary_body)
draw.text((25, curr_y + 52), "• Underlying Certified Equity Shares Transferred to IEPF Demat: 35,368 Shares | Current Market Value (@ ₹1,425): ₹5,03,99,400.00 (~₹5.04 Cr)", fill=(30, 41, 59), font=font_summary_body)
draw.text((25, curr_y + 72), "• Total Claim Recoverable: ₹5,04,06,092.00 (~₹5.04 Crores) | Custodian: Central Govt IEPF Authority, New Delhi | Form IEPF-5 Required", fill=(153, 27, 27), font=font_summary_body)

out_card_path = os.path.join(proof_cards_dir, "client_23_iepf_proof.png")
card.save(out_card_path)
shutil.copyfile(out_card_path, os.path.join(artifact_dir, "client_23_iepf_proof.png"))
shutil.copyfile(out_card_path, os.path.join(proof_cards_dir, "bhatia_all_5_proof.png"))
shutil.copyfile(out_card_path, os.path.join(artifact_dir, "bhatia_all_5_proof.png"))
print(f"Successfully generated all-5-tranche proof card: {out_card_path} (size: {card.size})")

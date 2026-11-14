# -*- coding: utf-8 -*-
"""
extract_and_align.py
Extracts translation text from PDF and aligns it with manga/manhwa raw chapter images.
Also generates composite contact sheets (6 panels each) for fast multimodal inspection.
"""

import os
import sys
import glob
import re
import json
import argparse
from PIL import Image

def get_page_number(filepath):
    base = os.path.basename(filepath)
    # Match trailing number before file extension (e.g. IMAG01_12.JPEG -> 12)
    m = re.search(r'(\d+)\.[^.]+$', base)
    if m:
        return int(m.group(1))
    return 999999

def extract_pdf_pages(pdf_path):
    import pypdf
    reader = pypdf.PdfReader(pdf_path)
    pages = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({
            "pdf_page_index": idx + 1,
            "text": text.strip()
        })
    return pages

def find_chapter_images(img_dir):
    exts = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.WEBP')
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(img_dir, ext)))
    # Deduplicate in case case-insensitive filesystems match twice
    files = list(set(files))
    # Sort by exact panel number
    files = sorted(files, key=get_page_number)
    return files

def generate_contact_sheets(image_files, output_dir, max_per_sheet=6):
    os.makedirs(output_dir, exist_ok=True)
    sheets = []
    
    # Process in batches of 6 (3 cols x 2 rows)
    for sheet_idx, i in enumerate(range(0, len(image_files), max_per_sheet), start=1):
        batch = image_files[i:i + max_per_sheet]
        if not batch:
            continue
            
        imgs = [Image.open(p) for p in batch]
        # Standardize cell size
        cell_w = 690
        cell_h = 1600
        cols = min(3, len(imgs))
        rows = (len(imgs) + cols - 1) // cols
        
        sheet = Image.new('RGB', (cell_w * cols, cell_h * rows), (255, 255, 255))
        for idx, im in enumerate(imgs):
            c = idx % cols
            r = idx // cols
            im_resized = im.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            sheet.paste(im_resized, (c * cell_w, r * cell_h))
            
        sheet_path = os.path.join(output_dir, f'contact_sheet_{sheet_idx:02d}.jpg')
        sheet.save(sheet_path, quality=80)
        sheets.append({
            "sheet_index": sheet_idx,
            "path": sheet_path,
            "images": [os.path.basename(p) for p in batch]
        })
        
    return sheets

def main():
    parser = argparse.ArgumentParser(description="Extract PDF and align with raw chapter images.")
    parser.add_argument("images_dir", help="Path to raw images folder")
    parser.add_argument("pdf_path", help="Path to client translation PDF")
    parser.add_argument("--out-dir", default=None, help="Output directory for intermediate data")
    args = parser.parse_args()

    img_dir = os.path.abspath(args.images_dir)
    pdf_path = os.path.abspath(args.pdf_path)
    out_dir = os.path.abspath(args.out_dir) if args.out_dir else os.path.join(img_dir, "_rawfix_workspace")
    os.makedirs(out_dir, exist_ok=True)

    print(f"[*] Scanning images in: {img_dir}")
    images = find_chapter_images(img_dir)
    print(f"[*] Found {len(images)} images.")

    print(f"[*] Extracting PDF text from: {pdf_path}")
    pdf_pages = extract_pdf_pages(pdf_path)
    print(f"[*] Extracted {len(pdf_pages)} PDF pages.")

    print(f"[*] Generating contact sheets for fast vision inspection...")
    contact_sheets = generate_contact_sheets(images, out_dir)
    print(f"[*] Generated {len(contact_sheets)} contact sheets in: {out_dir}")

    manifest = {
        "images_dir": img_dir,
        "pdf_path": pdf_path,
        "total_images": len(images),
        "total_pdf_pages": len(pdf_pages),
        "images": [os.path.basename(f) for f in images],
        "pdf_pages": pdf_pages,
        "contact_sheets": contact_sheets
    }

    manifest_path = os.path.join(out_dir, "alignment_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[+] Manifest created at: {manifest_path}")

if __name__ == "__main__":
    main()

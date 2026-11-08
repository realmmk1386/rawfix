# -*- coding: utf-8 -*-
"""
compile_script_pdf.py
Compiles structured manga/manhwa script data into a clean, unadorned typesetter PDF
and an accompanying plain text (.txt) file using headless Chromium / Edge.
"""

import os
import sys
import json
import subprocess
import shutil
import argparse

def find_browser():
    """Dynamically finds Edge, Chrome, Chromium, or Brave across Windows, macOS, and Linux."""
    # 1. Check PATH
    for name in ["msedge", "google-chrome", "chrome", "chromium", "chromium-browser", "brave"]:
        p = shutil.which(name)
        if p:
            return p

    # 2. Windows standard locations
    if sys.platform == "win32":
        candidates = [
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    # 3. macOS standard locations
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    # 4. Linux standard locations
    elif sys.platform.startswith("linux"):
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/usr/bin/microsoft-edge-stable",
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    return None

def build_html(title, chapter_name, pages_data, notes_header=""):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      font-family: sans-serif;
      color: #777;
    }}
    @top-right {{
      content: "{title}";
      font-size: 8pt;
      font-family: sans-serif;
      color: #999;
    }}
  }}
  body {{
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    color: #222;
    background: #fff;
    font-size: 10.5pt;
    line-height: 1.45;
    margin: 0;
    padding: 0;
  }}
  .doc-header {{
    border-bottom: 2px solid #333;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }}
  .doc-title {{
    font-size: 18pt;
    font-weight: bold;
    margin: 0 0 4px 0;
    color: #111;
  }}
  .doc-subtitle {{
    font-size: 9.5pt;
    color: #555;
    margin: 0;
  }}
  .info-box {{
    background-color: #f7f7f9;
    border-left: 4px solid #4a6fa5;
    padding: 8px 12px;
    margin-bottom: 16px;
    font-size: 9pt;
    color: #333;
  }}
  .page-block {{
    margin-bottom: 12px;
    padding: 8px 10px;
    border: 1px solid #e2e4e8;
    border-radius: 4px;
    page-break-inside: avoid;
  }}
  .page-header {{
    font-size: 11pt;
    font-weight: bold;
    color: #1a365d;
    background-color: #edf2f7;
    padding: 4px 8px;
    margin: -8px -10px 8px -10px;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    border-bottom: 1px solid #cbd5e0;
    display: flex;
    justify-content: space-between;
  }}
  .item-row {{
    margin-bottom: 6px;
    padding-left: 4px;
  }}
  .tag {{
    display: inline-block;
    font-weight: bold;
    font-size: 8.5pt;
    padding: 1px 6px;
    border-radius: 3px;
    margin-right: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .tag-bubble {{ background: #e3f2fd; color: #0d47a1; border: 1px solid #bbdefb; }}
  .tag-box {{ background: #fff3e0; color: #e65100; border: 1px solid #ffe0b2; }}
  .tag-sfx {{ background: #fce4ec; color: #c2185b; border: 1px solid #f8bbd0; }}
  .tag-text {{ background: #f3e5f5; color: #6a1b9a; border: 1px solid #e1bee7; }}
  .tag-title {{ background: #e8f5e9; color: #1b5e20; border: 1px solid #c8e6c9; }}
  .tag-notice {{ background: #fff9c4; color: #f57f17; border: 1px solid #fff59d; }}
  .tag-note {{ background: #eceff1; color: #455a64; border: 1px solid #cfd8dc; }}

  .text-content {{
    font-weight: 600;
    color: #111;
  }}
  .orig-content {{
    font-size: 8.5pt;
    color: #666;
    margin-top: 2px;
    margin-left: 20px;
    font-style: italic;
  }}
  .note-content {{
    font-size: 8.5pt;
    color: #888;
    margin-top: 1px;
    margin-left: 20px;
  }}
</style>
</head>
<body>

<div class="doc-header">
  <div class="doc-title">{title}</div>
  <div class="doc-subtitle">Clean Typesetting & Verification Script | Grammar Corrections, Missing SFX & Image Alignment</div>
</div>
'''
    if notes_header:
        html += f'''
<div class="info-box">
  {notes_header}
</div>
'''

    for page in pages_data:
        img_lbl = f"Image {page.get('img', '')}"
        pdf_lbl = f"PDF Page {page.get('pdf_page', '')}" if page.get('pdf_page') else ""
        
        html += f'<div class="page-block">\n'
        html += f'  <div class="page-header"><span>{img_lbl}</span><span style="font-weight:normal; font-size:9.5pt; color:#4a5568;">{pdf_lbl}</span></div>\n'
        
        for item in page.get("items", []):
            itype = item.get("type", "Bubble")
            tag_class = "tag-bubble"
            if "Box" in itype: tag_class = "tag-box"
            elif "SFX" in itype: tag_class = "tag-sfx"
            elif "Text" in itype: tag_class = "tag-text"
            elif "Title" in itype: tag_class = "tag-title"
            elif "Notice" in itype: tag_class = "tag-notice"
            elif "Note" in itype: tag_class = "tag-note"
            
            text_formatted = item.get('text', '').replace('\n', '<br/>')
            html += f'  <div class="item-row">\n'
            html += f'    <span class="tag {tag_class}">[{itype.upper()}]</span><span class="text-content">{text_formatted}</span>\n'
            if "orig" in item and item["orig"]:
                html += f'    <div class="orig-content">↳ Original: "{item["orig"]}"</div>\n'
            if "note" in item and item["note"]:
                html += f'    <div class="note-content">↳ Note: {item["note"]}</div>\n'
            html += f'  </div>\n'
        
        html += f'</div>\n'

    html += '''
</body>
</html>
'''
    return html

def build_txt(title, pages_data, notes_header=""):
    txt = "=" * 80 + "\n"
    txt += f"{title.upper()}\n"
    txt += "Clean Typesetting & Verification Script\n"
    txt += "=" * 80 + "\n\n"
    if notes_header:
        clean_notes = re.sub(r'<[^>]+>', '', notes_header).strip()
        txt += f"NOTES:\n{clean_notes}\n\n"
    txt += "TAGS: [BUBBLE] | [BOX] | [SFX] | [TEXT ON PROP / IMAGE] | [NOTE]\n\n"

    for page in pages_data:
        img_lbl = f"IMAGE {page.get('img', '')}"
        pdf_lbl = f"PDF Page {page.get('pdf_page', '')}" if page.get('pdf_page') else ""
        txt += "-" * 80 + "\n"
        txt += f"--- {img_lbl} ({pdf_lbl}) ---\n"
        txt += "-" * 80 + "\n"
        for item in page.get("items", []):
            txt += f"[{item.get('type', 'BUBBLE').upper()}]: {item.get('text', '')}\n"
            if "orig" in item and item["orig"]:
                txt += f"   [Original]: \"{item['orig']}\"\n"
            if "note" in item and item["note"]:
                txt += f"   [Note]: {item['note']}\n"
        txt += "\n"
    return txt

def main():
    parser = argparse.ArgumentParser(description="Compile script JSON into PDF and TXT.")
    parser.add_argument("script_json", help="Path to input script JSON file")
    parser.add_argument("output_dir", help="Destination folder for PDF and TXT")
    parser.add_argument("--pdf-name", default="Typesetting_Script.pdf", help="Output PDF filename")
    parser.add_argument("--txt-name", default="Typesetting_Script.txt", help="Output TXT filename")
    args = parser.parse_args()

    with open(args.script_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Typesetting Script")
    chapter_name = data.get("chapter_name", "")
    pages_data = data.get("pages", [])
    notes_header = data.get("notes_header", "")

    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    # 1. Output TXT
    txt_path = os.path.join(out_dir, args.txt_name)
    txt_content = build_txt(title, pages_data, notes_header)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)
    print(f"[+] TXT script generated: {txt_path}")

    # 2. Output HTML
    html_content = build_html(title, chapter_name, pages_data, notes_header)
    temp_html = os.path.join(out_dir, "_temp_script.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 3. Compile PDF via headless browser
    pdf_path = os.path.join(out_dir, args.pdf_name)
    browser_bin = find_browser()
    if browser_bin:
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            temp_html
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(pdf_path):
            print(f"[+] PDF generated successfully: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        else:
            print(f"[!] Warning: Browser exited with code {res.returncode}. PDF may not have generated.")
    else:
        print("[!] No compatible browser (Edge/Chrome/Chromium) found for PDF export.")

    # Clean up temp HTML
    if os.path.exists(temp_html):
        try:
            os.remove(temp_html)
        except Exception:
            pass

if __name__ == "__main__":
    main()

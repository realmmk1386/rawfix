---
name: rawfix
description: Use when the user invokes /rawfix or asks to process manga/manhwa raw chapter images and client translation files, align page numbering, fix grammar, translate missing SFX and dialogue, and generate a clean typesetter-ready PDF and TXT script.
---

# RawFix — Manga/Manhwa Raw Chapter & Translation Processing

## Overview
Automates the full pipeline of reviewing, grammar-checking, and completing raw manga/manhwa chapters against client translations. Identifies skipped/mismatched page numbering, translates missing SFX and background text, categorizes speech bubbles vs rectangular narration boxes, and generates a clean, unadorned PDF and companion TXT script for typesetters.

## Invocation
The user can trigger this workflow with:
```text
/rawfix "<images_path>" "<translation_path>"
```
or by asking in natural language to inspect/align raw chapter images with a translation file.

---

## Standard Workflow

### Step 1: Run Extraction & Alignment Scaffolding
Execute the bundled helper script [`scripts/extract_and_align.py`](./scripts/extract_and_align.py):
```bash
python scripts/extract_and_align.py "<images_path>" "<translation_path>"
```
*(If calling from outside the repository/skill folder, use the absolute path to `extract_and_align.py` within your installed skill directory).*

This utility automatically:
1. Extracts text from the client's PDF page by page (`pypdf`).
2. Scans and naturally sorts all raw image files in `<images_path>`.
3. Creates composite contact sheets (6 panels per sheet in a 3x2 grid) inside `<images_path>/_rawfix_workspace/`.
4. Outputs `alignment_manifest.json` containing the page-to-image mapping.

### Step 2: Detect Page Number Offsets & Typo Skips
Compare the client's PDF page count against the raw image count.
* Common issue: Translators frequently skip page numbers (e.g. typing `Page 40` directly after `Page 30`).
* Calculate the formula: `Image Number = PDF Page Number ± Offset`.
* Clearly state both numbers in the output (e.g. `Image 31 (PDF Page 40)`).

### Step 3: Visual Inspection via Contact Sheets
Use `read_file` to inspect the generated `contact_sheet_X.jpg` files:
* Reviewing 6 panels at once significantly cuts down token usage and avoids API timeouts.
* Verify every speech bubble, rectangular narration box, sound effect (SFX), and text on props/drawings.

### Step 4: Linguistic & Typesetting Standards
1. **Grammar & Typo Correction**:
   * Fix common errors: `your` vs `you're`, `there` vs `their`, `to` vs `too`, `seargent` vs `sergeant`, `cuz` vs `because of`, missing apostrophes, run-on punctuation.
   * Maintain the character's voice and tone.
2. **Preserve Client's Original Text**:
   * Whenever a line is modified or corrected, always include the original version underneath:
     `↳ Original: "..."`
3. **Translate Missing Elements**:
   * Identify untranslated Korean SFX (e.g. `콱` = *THUNK* / *DIG*, `쿨럭` = *COUGH*, `소근` = *WHISPER*, `글썽` = *WELLING UP*, `쿵쿵` = *BONK!* *BONK!*, `꿀꺽` = *GULP*).
   * Translate text on signs, food packets, and background calligraphy.
4. **Tag Every Entry**:
   * `[BUBBLE]` — Dialogue and thought balloons.
   * `[BOX]` — Rectangular narration, title, or system choice boxes.
   * `[SFX]` — Sound effects.
   * `[TEXT ON PROP / IMAGE]` — In-world environmental text.
   * `[NOTE]` — Action-only panels with no dialogue.

### Step 5: Compile Final PDF & TXT Script
Prepare the final script JSON file and compile it using [`scripts/compile_script_pdf.py`](./scripts/compile_script_pdf.py):
```bash
python scripts/compile_script_pdf.py "<workspace_json>" "<output_directory>" --pdf-name "Typesetting_Script.pdf" --txt-name "Typesetting_Script.txt"
```
* **PDF**: Generated via headless Chromium/Edge with print styling. Produces a clean, black-and-white/subtle-tint, unadorned document with semantic color tags, avoiding page breaks inside dialogue blocks.
* **TXT**: Companion plain-text file for fast copy-pasting directly into Photoshop/typesetting tools.

### Step 6: Final Output to User
Provide clickable links to both output files:
* `[Typesetting_Script.pdf](file:///...)`
* `[Typesetting_Script.txt](file:///...)`
Highlight any crucial findings (e.g., page number jumps or significant mistranslations).
When replying in Persian, always wrap the response in `<div dir="rtl">...</div>`.

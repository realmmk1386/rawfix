---
description: Process manga/manhwa raw chapter images and client translation files, fix grammar, translate missing SFX, and compile clean typesetter PDF and TXT.
arguments:
  - name: images_path
    description: Absolute or relative path to the directory containing raw chapter images
    required: true
  - name: translation_path
    description: Absolute or relative path to the client translation PDF or text file
    required: true
---

# RawFix Slash Command

Execute the raw chapter QA and typesetting script generation:

1. Run the alignment pre-processor:
   ```bash
   python scripts/extract_and_align.py "$ARG_IMAGES_PATH" "$ARG_TRANSLATION_PATH"
   ```

2. Inspect the contact sheets created in `_rawfix_workspace/` to verify dialogue, narration boxes, missing SFX, and text on images.

3. Fix grammatical and punctuation issues in the translation. Keep the original text underneath any edited line (`↳ Original: "..."`).

4. Tag entries using: `[BUBBLE]`, `[BOX]`, `[SFX]`, and `[TEXT ON PROP / IMAGE]`.

5. Compile the final typesetting PDF and TXT scripts:
   ```bash
   python scripts/compile_script_pdf.py "$ARG_IMAGES_PATH/_rawfix_workspace/script.json" "$ARG_IMAGES_PATH"
   ```

6. Output direct links to `Typesetting_Script.pdf` and `Typesetting_Script.txt`.

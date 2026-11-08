# Claude Code Instructions — RawFix

This repository provides the **RawFix** skill and slash command for Claude Code.

## Purpose
RawFix automates the end-to-end processing of raw manga/manhwa chapters and client translation documents. It aligns raw page images with client translation files, identifies and calculates page numbering offsets, checks grammar and typos while preserving original text, translates missing Korean sound effects (SFX) and background signage, and compiles clean, unadorned typesetter PDFs and companion TXT files.

## Claude Code Slash Command
Claude Code can invoke this tool directly via:
```text
/rawfix "<images_path>" "<translation_path>"
```
Defined in `.claude/commands/rawfix.md`.

## Execution Workflow
When `/rawfix` is triggered:
1. Run the extraction utility:
   ```bash
   python scripts/extract_and_align.py "<images_path>" "<translation_path>"
   ```
2. Inspect the generated 6-panel contact sheets in `<images_path>/_rawfix_workspace/` to verify dialogue, SFX, and narration boxes against images.
3. Detect any translation numbering jumps (e.g. page skips) and calculate offsets:
   $$\text{Image Number} = \text{PDF Page Number} \pm \text{Offset}$$
4. Fix grammar errors, typo issues, and mistranslations without losing character voice. If any line is edited, keep the original line as `↳ Original: "..."`.
5. Tag all entries clearly: `[BUBBLE]`, `[BOX]`, `[SFX]`, `[TEXT ON PROP / IMAGE]`, `[NOTE]`.
6. Compile the final PDF and TXT script:
   ```bash
   python scripts/compile_script_pdf.py "<script_json>" "<output_directory>"
   ```
7. Provide the user with direct clickable paths to the output files.

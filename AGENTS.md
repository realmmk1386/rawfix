# AGENTS.md — RawFix Universal Agent Specification

This specification defines the instructions and workflows for AI coding agents (OpenAI Codex, Cursor, Antigravity, Claude Code) working on manga/manhwa chapter processing and translation QA.

## Skill Overview
- **Name:** rawfix
- **Primary Function:** Align raw comic panel images with client translation files, resolve page numbering offsets, verify grammar, translate missing SFX/props, and export typesetter-ready PDF & TXT scripts.
- **Invocation Trigger:** `/rawfix <images_path> <translation_path>` or explicit natural language instruction.

## Behavioral Requirements
1. **Preserve Client Text:** Never silently discard or completely rewrite client translations. If modifying grammar or typos, always record the client's initial translation in a companion `Original:` field.
2. **Handle Page Skips Systematically:** Translators frequently skip page numbers (e.g. typing `Page 40` immediately after `Page 30`). Never assume image index $N$ equals PDF page $N$. Always check and calculate the offset formula.
3. **Sound Effects (SFX) & In-World Text:** Scrutinize visual sound effects (onomatopoeia like `콱`, `쿨럭`, `소근`, `쿵쿵`, `꿀꺽`) and in-panel text (signs, items, food packets). If missing from the client document, translate and categorize them.
4. **Structural Categorization:**
   - `[BUBBLE]` — Dialogue balloons, speech spikes, thought clouds, whispering.
   - `[BOX]` — Rectangular boxes for narration, chapter titles, system messages, choices.
   - `[SFX]` — Sound effects and environmental audio cues.
   - `[TEXT ON PROP / IMAGE]` — In-world signs, prop packaging, background text.
   - `[NOTE]` — Action-only panels without text.

## Execution Tools
- Extraction & Alignment: `python scripts/extract_and_align.py "<images_path>" "<translation_path>"`
- PDF & TXT Compiler: `python scripts/compile_script_pdf.py "<script_json>" "<output_directory>"`

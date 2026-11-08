# RawFix — Manga & Manhwa Raw Chapter QA & Typesetting Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Antigravity | Claude Code | Codex](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20Code%20%7C%20Codex-purple.svg)](#multi-agent-support)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)

**RawFix** is an AI agent skill and command pipeline designed for manga, manhwa, and webtoon scanlation workflows. It bridges the gap between raw comic panel images (`.jpg`, `.png`, `.webp`) and client translation documents (`.pdf`, `.docx`, `.txt`), guaranteeing typesetter-ready precision, grammatical accuracy, and full sound effect (SFX) coverage.

---

## 🌟 Key Features

1. **Automatic Page Number Alignment & Skip Detection**:
   * Translators frequently make pagination typos (e.g. jumping from Page 30 directly to Page 40).
   * RawFix naturally sorts raw chapter image filenames (`IMAG01_1.jpg` ... `IMAG01_75.jpg`), calculates page number offsets, and links both IDs throughout the script:
     $$\text{Image Number} = \text{PDF Page Number} \pm \text{Offset}$$
2. **Context-Optimized Contact Sheet Generation**:
   * Stitches raw panels into compact 6-panel contact sheets (3x2 grid) so multimodal AI models can visually inspect entire chapters without stream timeouts or token bloat.
3. **Sound Effect (SFX) & In-World Prop Translation**:
   * Scans visual art for omitted Korean/Japanese onomatopoeia (`콱` *THUNK*, `쿨럭` *COUGH*, `소근` *WHISPER*, `쿵쿵` *BONK*, `꿀꺽` *GULP*) and in-world packaging/calligraphy.
4. **Grammar & Typo Correction with Client Preservation**:
   * Fixes common grammatical errors (`your` $\to$ `you're`, `there` $\to$ `their`, `to` $\to$ `too`, punctuation, capitalization) while preserving character voice.
   * **Never overwrites silently:** Every modified line explicitly shows the client's version underneath:
     `↳ Original: "..."`
5. **Typesetting Category Tagging**:
   * `[BUBBLE]` — Speech balloons, thought clouds, whispering.
   * `[BOX]` — Rectangular narration, system menus, chapter titles.
   * `[SFX]` — Sound effects and environmental audio cues.
   * `[TEXT ON PROP / IMAGE]` — In-world signs, items, food packets.
   * `[NOTE]` — Action-only panels without text.
6. **Dual Typesetter Deliverables**:
   * **Clean Typesetting PDF (`Typesetting_Script.pdf`):** Unadorned, professional black-and-white print styling rendered via headless Chromium/Edge with proper page headers and anti-break layout.
   * **Companion Text Script (`Typesetting_Script.txt`):** Plain text formatted for rapid copy-pasting directly into Adobe Photoshop or InDesign.

---

## 🤖 Multi-Agent Support

RawFix is built from the ground up to support three major AI coding agents within the same repository:

| AI Agent | Integration File | Invocation Command |
| :--- | :--- | :--- |
| **Google Antigravity** | `SKILL.md` | `/rawfix "<images_path>" "<translation_path>"` |
| **Anthropic Claude Code** | `CLAUDE.md`, `.claude/commands/rawfix.md` | `/rawfix "<images_path>" "<translation_path>"` |
| **OpenAI Codex / Cursor** | `AGENTS.md` | Universal Agent Skill / Prompt |

---

## 🚀 Quick Installation

### Windows (PowerShell)

Clone the repository and run the PowerShell installer:

```powershell
git clone https://github.com/realmmk1386/rawfix.git
cd rawfix
.\install.ps1 -Target All
```

* Options for `-Target`: `All` (default), `Antigravity`, `Claude`, or `Codex`.

### Linux / macOS (Bash)

```bash
git clone https://github.com/realmmk1386/rawfix.git
cd rawfix
chmod +x install.sh
./install.sh All
```

### Manual Installation

- **Antigravity**: Copy `SKILL.md` and the `scripts/` directory to:
  - Windows: `%USERPROFILE%\.gemini\config\skills\rawfix\`
  - Linux/macOS: `~/.gemini/config/skills/rawfix/`
- **Claude Code**: Copy the skill to `~/.claude/skills/rawfix/` and copy `.claude/commands/rawfix.md` to `~/.claude/commands/rawfix.md`.
- **Codex / Universal**: Copy to `~/.codex/skills/rawfix/` or link `AGENTS.md` in your project root.

---

## 📖 Usage

### Slash Command

In your AI chat session, run:

```text
/rawfix "/path/to/chapter_images" "/path/to/translations.pdf"
```

Or ask the agent in plain language:

> *"Please use rawfix to align and process the raw chapter images at `/path/to/chapter_images` with the translation at `/path/to/translations.pdf`."*

### What Happens Next

1. The agent executes `scripts/extract_and_align.py` to extract PDF text, sort the raw images, and create contact sheets in `_rawfix_workspace/`.
2. The agent detects any page numbering offset between the PDF and the images.
3. The agent reviews each panel, fixes grammar, translates missing SFX, and classifies entries.
4. The agent compiles and delivers `Typesetting_Script.pdf` and `Typesetting_Script.txt` directly inside the chapter folder.

---

## 🛠 Prerequisites

- **Python 3.8+**
- Python packages:
  ```bash
  pip install pypdf pillow
  ```
- **Microsoft Edge** or **Google Chrome** (used headlessly to render pixel-perfect PDFs from styled HTML).

---

## 📁 Repository Structure

```text
rawfix/
├── .claude/
│   └── commands/
│       └── rawfix.md            # Claude Code custom slash command
├── examples/
│   └── sample_script.json       # Sample JSON data schema
├── scripts/
│   ├── extract_and_align.py     # PDF extractor & 6-panel contact-sheet generator
│   └── compile_script_pdf.py    # Headless Edge PDF & TXT compiler
├── AGENTS.md                    # Universal agent guidelines (Codex/Cursor)
├── CLAUDE.md                    # Claude Code configuration
├── SKILL.md                     # Antigravity skill specification
├── install.ps1                  # Windows one-click installer
├── install.sh                   # Linux/macOS one-click installer
├── LICENSE                      # MIT License
└── README.md                    # English documentation and user guide
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Created and maintained by [realmmk1386](https://github.com/realmmk1386).

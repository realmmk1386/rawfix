#!/usr/bin/env bash
# Install RawFix Skill for Antigravity, Claude Code, and Codex (Linux / macOS)

set -e

TARGET="${1:-All}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=================================================="
echo " Installing RawFix Skill for AI Coding Agents     "
echo " Target: $TARGET                                  "
echo "=================================================="

# Check Python dependencies
echo "[*] Checking Python dependencies..."
python3 -c "import pypdf, PIL" 2>/dev/null || {
    echo "[!] Installing pypdf and pillow..."
    pip install pypdf pillow
}

install_to() {
    local dest_dir="$1"
    local agent_name="$2"
    echo "[*] Installing for $agent_name -> $dest_dir"
    mkdir -p "$dest_dir/scripts"
    cp "$SCRIPT_DIR/SKILL.md" "$dest_dir/"
    cp -r "$SCRIPT_DIR/scripts/"* "$dest_dir/scripts/"
    echo "[+] Done for $agent_name."
}

# 1. Antigravity
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Antigravity" ]; then
    install_to "$HOME/.gemini/config/skills/rawfix" "Antigravity"
fi

# 2. Claude Code
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Claude" ]; then
    install_to "$HOME/.claude/skills/rawfix" "Claude Code"
    mkdir -p "$HOME/.claude/commands"
    cp "$SCRIPT_DIR/.claude/commands/rawfix.md" "$HOME/.claude/commands/rawfix.md"
    echo "[+] Installed Claude Code command at $HOME/.claude/commands/rawfix.md"
fi

# 3. Codex
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Codex" ]; then
    install_to "$HOME/.codex/skills/rawfix" "Codex / Universal Agent"
fi

echo ""
echo "[✓] RawFix installation complete! You can now use /rawfix in your chats."

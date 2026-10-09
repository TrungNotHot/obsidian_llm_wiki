#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# LLM Wiki Project Setup Script
# Copies the .agents skills and docs/ scaffold into a target project repository.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-target-project>"
    echo "Example: $0 /home/tdtr/workspace/code/crm-pipeline"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist."
    exit 1
fi

echo "🚀 Scaffolding LLM Wiki into: $TARGET_DIR"

# 1. Copy .agents directory (Skills & Plugins)
echo "📦 Copying .agents (Skills)..."
mkdir -p "$TARGET_DIR/.agents"
cp -rn "$SCRIPT_DIR/.agents/"* "$TARGET_DIR/.agents/"

# 1b. Claude Code: standalone .claude/skills
echo "📦 Copying .claude (Claude Code skills)..."
mkdir -p "$TARGET_DIR/.claude"
cp -rn "$SCRIPT_DIR/.claude/"* "$TARGET_DIR/.claude/"
[ -f "$SCRIPT_DIR/.agents/.agentignore" ] && [ ! -f "$TARGET_DIR/.agents/.agentignore" ] && cp "$SCRIPT_DIR/.agents/.agentignore" "$TARGET_DIR/.agents/"

# 1c. Copy AGENTS.md workspace guidelines if not present
if [ -f "$SCRIPT_DIR/AGENTS.md" ] && [ ! -f "$TARGET_DIR/AGENTS.md" ]; then
    echo "📋 Copying AGENTS.md guidelines..."
    cp "$SCRIPT_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
fi

# 2. Copy docs directory (Vault scaffold)
echo "📚 Copying docs/ (Constitutional schema, index, concepts, entities)..."
mkdir -p "$TARGET_DIR/docs"
cp -rn "$SCRIPT_DIR/docs/"* "$TARGET_DIR/docs/"

# Copy hidden .obsidian folder if not already present
if [ ! -d "$TARGET_DIR/docs/.obsidian" ] && [ -d "$SCRIPT_DIR/docs/.obsidian" ]; then
    cp -r "$SCRIPT_DIR/docs/.obsidian" "$TARGET_DIR/docs/"
fi

# 3. Ensure scripts are executable
for f in "$TARGET_DIR"/.agents/skills/kb-health/scripts/check_health.py \
         "$TARGET_DIR"/.claude/skills/kb-health/scripts/check_health.py \
         "$TARGET_DIR"/.agents/skills/kb-compile/scripts/parse_document.py \
         "$TARGET_DIR"/.claude/skills/kb-compile/scripts/parse_document.py; do
    [ -f "$f" ] && chmod +x "$f"
done

# 4. Ensure target .gitignore covers binary sources & Obsidian state
if [ -f "$TARGET_DIR/.gitignore" ]; then
    if ! grep -q "docs/raw/binary" "$TARGET_DIR/.gitignore"; then
        echo "📝 Appending LLM Wiki ignore rules to target .gitignore..."
        cat << 'EOF' >> "$TARGET_DIR/.gitignore"

# LLM Wiki binary documents & Obsidian local workspace state
docs/raw/binary/*
!docs/raw/binary/.gitkeep
docs/raw/superpowers/**/*
!docs/raw/superpowers/**/
!docs/raw/superpowers/**/.gitkeep
!docs/raw/superpowers/**/README.md
docs/.obsidian/workspace.json
docs/.obsidian/workspace-mobile.json
EOF
    fi
fi

echo ""
echo "✅ LLM Wiki successfully scaffolded!"
echo ""
echo "👉 Next Steps:"
echo "  1. Edit Part 2 of '$TARGET_DIR/docs/SCHEMA.md' to customize your project scope and tags."
echo "  2. Open '$TARGET_DIR/docs' in Obsidian as a Vault."
echo "  3. Use /kb-compile, /kb-report, /kb-index, or /kb-health with your AI agent!"
echo ""

#!/bin/bash
# GHS Setup Script - Sets up the vector search environment for a project
# Usage: bash tools/setup.sh [/path/to/project]

set -e

PROJECT_PATH="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR"

echo "🚀 GHS Vector Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Project: $PROJECT_PATH"

# 1. Create .ai-index directory
echo ""
echo "📁 Creating .ai-index directory..."
mkdir -p "$PROJECT_PATH/.ai-index"

# 2. Add .ai-index to .gitignore (vector data should not be committed)
if [ -f "$PROJECT_PATH/.gitignore" ]; then
    if ! grep -q ".ai-index" "$PROJECT_PATH/.gitignore"; then
        echo ".ai-index/" >> "$PROJECT_PATH/.gitignore"
        echo "  ✅ Added .ai-index/ to .gitignore"
    else
        echo "  ✅ .ai-index/ already in .gitignore"
    fi
else
    echo ".ai-index/" > "$PROJECT_PATH/.gitignore"
    echo "  ✅ Created .gitignore with .ai-index/"
fi

# 3. Check for virtual environment
if [ ! -d "$PROJECT_PATH/.venv" ]; then
    echo ""
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv "$PROJECT_PATH/.venv"
    echo "  ✅ Virtual environment created at .venv/"
fi

# 4. Install ChromaDB
echo ""
echo "📦 Installing ChromaDB..."
source "$PROJECT_PATH/.venv/bin/activate"
pip install chromadb --quiet
echo "  ✅ ChromaDB installed"

# 5. Copy tools to project
echo ""
echo "🔧 Copying GHS tools to project..."
mkdir -p "$PROJECT_PATH/tools"
cp "$TOOLS_DIR/indexer.py" "$PROJECT_PATH/tools/"
cp "$TOOLS_DIR/search.py" "$PROJECT_PATH/tools/"
echo "  ✅ indexer.py and search.py copied to tools/"

# 6. Run initial indexing
echo ""
echo "🔍 Running initial indexing..."
cd "$PROJECT_PATH"
source .venv/bin/activate
python3 tools/indexer.py --project-path "$PROJECT_PATH"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Setup complete!"
echo ""
echo "Available commands:"
echo "  source .venv/bin/activate"
echo "  python3 tools/search.py \"your query\"           # Human-friendly output"
echo "  python3 tools/search.py \"your query\" --json    # AI-agent output"
echo "  python3 tools/indexer.py                       # Re-index after changes"

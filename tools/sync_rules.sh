# GHS Rule Synchronizer
# Consolidates modular rules from both local and global .agents/rules/ 
# into root .cursorrules and .gemini_rules

PROJECT_ROOT=$(pwd)
LOCAL_RULES_DIR="$PROJECT_ROOT/.agents/rules"
GLOBAL_RULES_DIR="$PROJECT_ROOT/../.agents/rules"

CURSOR_RULES="$PROJECT_ROOT/.cursorrules"
GEMINI_RULES="$PROJECT_ROOT/.gemini_rules"

# Function to collect rules
collect_rules() {
    DIR=$1
    if [ -d "$DIR" ]; then
        echo "  Reading rules from $DIR..."
        for rule in "$DIR"/*.md; do
            if [ -f "$rule" ]; then
                FILENAME=$(basename "$rule")
                echo "    Adding $FILENAME..."
                echo -e "\n#### 📝 Rule [$DIR]: $FILENAME" >> "$TARGET_FILE"
                # Remove frontmatter if present
                sed '1,/^-*$/d' "$rule" >> "$TARGET_FILE"
            fi
        done
    fi
}

# Function to sync a specific file
sync_file() {
    TARGET_FILE=$1
    echo "Updating $TARGET_FILE..."
    
    MARKER="### 🧩 MODULAR RULES (AUTO-SYNCED by GHS)"
    
    if grep -q "$MARKER" "$TARGET_FILE"; then
        sed -i '' "/$MARKER/,\$d" "$TARGET_FILE"
    fi
    
    echo -e "\n$MARKER" >> "$TARGET_FILE"
    echo -e "---" >> "$TARGET_FILE"
    
    # Collect Local then Global
    collect_rules "$LOCAL_RULES_DIR"
    collect_rules "$GLOBAL_RULES_DIR"
}

# Sync both files if they exist
[ -f "$CURSOR_RULES" ] && sync_file "$CURSOR_RULES"
[ -f "$GEMINI_RULES" ] && sync_file "$GEMINI_RULES"

echo "✅ Rules synchronized successfully (Local + Global)."

# Sync both files if they exist
[ -f "$CURSOR_RULES" ] && sync_file "$CURSOR_RULES"
[ -f "$GEMINI_RULES" ] && sync_file "$GEMINI_RULES"

echo "✅ Rules synchronized successfully."

---
description: Synchronize modular rules from .agents/rules/ into root .cursorrules and .gemini_rules.
---

# Workflow: Modular Rule Synchronization

This workflow ensures that all project-specific and global modular rules are visible to the IDE.

1.  **Identify Rules**:
    - Check for new or modified rules in `.agents/rules/*.md`.
    - Also check for global rules in `../.agents/rules/*.md`.

2.  **Consolidate Rules**:
    - **Sync**: Run the [sync_rules.sh](file:///Users/mac/Documents/GIT/git-history-standard/tools/sync_rules.sh) script.
// turbo
```bash
bash tools/sync_rules.sh
```

3.  **Verify**:
    - Open `.cursorrules` or `.gemini_rules` to confirm that the new rules were appended under the `### 🧩 MODULAR RULES` marker.

4.  **Documentation**:
    - Mention the rule update in `HISTORY.md` using the `#ai-sync` tag if requested.

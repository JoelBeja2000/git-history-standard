---
name: GitHub Board Integration
description: Rules for syncing local bugs and status with GitHub Issues and Projects.
---

# 🐙 GitHub Integration Rules

- **Trigger**: Use `#ai-sync` to start a full synchronization.
- **Bugs to Issues**: Every entry in `BUGS.md` should have a corresponding GitHub Issue.
- **Dev Status Issue**: Maintain a single "GHS Development Status" issue (Issue #1 by default) updated with active branches and stashes.
- **Safety**: Never upload local vector stores (`.ai-index/`) or local environment variables (`.env`) to GitHub.

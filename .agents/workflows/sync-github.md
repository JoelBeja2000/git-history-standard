---
description: Synchronize BUGS.md and Development Status (Branches/Stashes) with GitHub.
---

# Workflow: GitHub Synchronization

This workflow ensures that the local GHS state is reflected in the GitHub repository.

1.  **Check Configuration**:
    - Verify that `github: enabled: true` is set in `.agents/skills/git-history/SKILL.md`.
    - Check if `gh` CLI is authenticated: `gh auth status`.

2.  **Sync Bugs**:
    - Parse `BUGS.md` and identify active/new bugs.
    - **Sync**: Call [github_sync.py](file:///Users/mac/Documents/GIT/git-history-standard/tools/github_sync.py) with `--bugs`.
// turbo
```bash
python3 tools/github_sync.py --bugs
```

3.  **Sync Dev Status**:
    - Identify current branches and stashed changes.
    - **Sync**: Call [github_sync.py](file:///Users/mac/Documents/GIT/git-history-standard/tools/github_sync.py) with `--dev`.
// turbo
```bash
python3 tools/github_sync.py --dev
```

4.  **Confirmation**:
    - Provide the user with links to the updated GitHub Issues or Project cards.

---
description: How to maintain the Project History (HISTORY.md) and Bug Registry.
---

# Workflow: Project History Maintenance

1.  **Analyze Context & Trigger Tags**:
    - **Identify Environment**: Run `git branch --show-current` and `git log --oneline -n 10`.
    - **Check for Tags**: Look for `#ai-history`, `#ai-bug`, or `#ai-catchup` in commit messages.
    - If a tag is found, prioritize a full history sync.
    - Compare with the existing `HISTORY.md`.

2.  **Update History**:
    - If new commits or branches were merged, append them to the "Full Commit Log" table in `HISTORY.md`.
    - **Language**: All entries must be in **English only** to maintain a professional global repository.
    - Maintain the table structure: `Commit | Author | Description | Screenshots | Technical Details`.

3.  **Handle Bugs (If applicable)**:
    - If a bug was fixed, add it to the `BUGS.md` file.
    - Maintain the structure: `Bug ID | Author | Description | Fix Details`.
    - Content must be in **English**.

4.  **Verify Visuals**:
    - Check if new UI screenshots need to be added to the `assets/screenshots/` folder and linked in the `HISTORY.md` using Markdown syntax: `![Alt Text](path)`.

5.  **Tag Replacement & Sync**:
    - **Replace Tag**: If tags were found, replace them with `[documented]` in the commit message using `git commit --amend` to keep the history clean.
    - **Sync**: `git push origin [current-branch] --force-with-lease` (to update the commit message on GitHub).
    - **Confirm**: Notify the user that the synchronization is complete and the project context is up to date.

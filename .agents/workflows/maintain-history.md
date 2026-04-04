---
description: How to maintain the Project History (HISTORY.md) and Bug Registry.
---

# Workflow: Project History Maintenance

1.  **Analyze Context & Trigger Tags**:
    - Run `git branch -a` and `git log --oneline -n 10`.
    - **Check for Tags**: Look for `#ai-history` or `#ai-bug` in the latest commit messages.
    - If a tag is found, prioritize a full history sync regardless of how "stale" it is.
    - Compare with the existing `HISTORY.md`.

2.  **Update History**:
    - If new commits or branches were merged, append them to the "Full Commit Log" table in `HISTORY.md`.
    - Ensure all messages are bilingual (EN/ES).

3.  **Handle Bugs (If applicable)**:
    - If a bug was fixed, add it to the `BUGS.md` or the "Bug Registry" section of `HISTORY.md`.
    - Include: `Symptom | Branch Introduced | Branch Fixed | Commit | Date`.

4.  **Verify Visuals**:
    - Check if new UI screenshots need to be added to the `screenshots/` folder and linked in the `README.md`.

5.  **Tag Replacement & Sync**:
    - **Replace Tag**: If `#ai-history` or `#ai-bug` was found, replace it with `[documented]` in the commit message using `git commit --amend` or similar.
    - **Sync**: `git push origin [current-branch] --force-with-lease` (to update the commit message on GitHub).
    - **Verify**: Confirm with the user that the synchronization is complete.

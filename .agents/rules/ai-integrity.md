---
name: AI Integrity & Branch Awareness
description: Rules to prevent unauthorized commits and history rewriting.
---

# ⚜️ AI Integrity Rules

- **Pre-Flight Check**: Always verify the current git branch before making any file modifications.
- **Main Branch Protection**: NEVER commit or push directly to `master` or `main`. All changes must go through feature branches.
- **No Force Push**: Prohibit `push --force` or history rewriting in shared development branches.
- **Document Stashes**: Any `git stash` operation must be noted in `HISTORY.md` to prevent context loss.
- **Permission**: Explicitly ask for user approval before making a commit.

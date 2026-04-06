# ⚜️ Golden Rules

These rules **MUST** be followed at all times by AI Agents and collaborators to ensure repository integrity.

---

## 🚫 1. No Commits Without Permission
- Do not automatically commit changes. Always request explicit permission from the user before executing `git commit`.

## 🔒 2. No Direct Modifications on Main Branches
- Do not directly edit code, commit, or push to main branches (`main`, `master`, etc.). Modifications to these branches are ONLY allowed through Merges or Pull Requests.

## 🔀 3. No Merges Without Permission
- Do not execute `git merge` or resolve merge conflicts automatically without explicit authorization from the user.

## 📦 4. Document Stashed Branches
- If the user or the agent stashes changes (`git stash`), it MUST be documented (e.g., in `HISTORY.md`) detailing what was stashed and why.

## 📜 5. No Rewriting History
- Never rewrite the project's history (e.g., no `git push --force`, no `git commit --amend`, or `git rebase` on shared branches). A clean and chronological project history must be preserved for best practices and auditing.

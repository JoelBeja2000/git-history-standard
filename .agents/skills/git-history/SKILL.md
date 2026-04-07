---
name: git-history
description: Maintain a project history, branch index, and bug registry.
config:
  languages: ["en"]
  history_file: "HISTORY.md"
  bug_file: "BUGS.md"
  ai_tags:
    history: "#ai-history"
    bug: "#ai-bug"
    catch_up: "#ai-catchup"
  include_author: true # Whether to include the Git Author in the history/bug files
  security:
    share_index: false # [IMPORTANT] Set to true ONLY for private repos if you want to share the vector cache
    share_env: false   # [CRITICAL] NEVER set to true unless you are in a local, air-gapped environment
  screenshots:
    enabled: true
    path: "assets/screenshots/" # RECOGNIZED BY AI: The agent will use this path to save/load captures.
    auto_index: true # AI will automatically index image alt-text into vectors.
    analyze_images: true # Allow AI to use vision to describe the contents.
    auto_upload: true # AI instruction: Always 'git add' images in this path during synchronization.
  vector_store:
    provider: "qdrant" # EXTENSIBLE: "chroma" (local), "qdrant" (server), or any custom provider
    url: "http://localhost:6333"
    collection_history: "ghs_history"
    collection_code: "ghs_code"
  github:
    enabled: true # Set to false to disable GitHub Issues/Projects synchronization

# AI Vision Protocol
# When an agent encounters a screenshot path in HISTORY.md or BUGS.md:
# 1. Use `view_file` on the image path to analyze the visual changes.
# 2. Compare the visual state with the technical description.
# 3. If on a different branch, use `git show branch:path` to retrieve the image.
---

# Git History Management Skill

This skill enables the agent to maintain a high-quality, professional history for any Git project.

## Core Responsibilities
1.  **Chronological Indexing**: Maintain a `HISTORY.md` file that captures every major milestone, branch evolution, and **Author/Actor identity (AI vs Human)**.
2.  **Multi-language Support**: All documentation and commit messages must be provided in the user's preferred language(s) (e.g., English, Spanish, French, etc.).
3.  **Visual Documentation**: Integrate and caption screenshots in the `README.md` and `HISTORY.md`.
4.  **Issue Tracking**: Maintain a `BUGS.md` or a "Bug Registry" section to prevent regressions.
5.  **GitHub Synchronization**: Synchronize `BUGS.md` with GitHub Issues and maintain a "Development Status" (branches, stash) on the GitHub repository using `#ai-sync`.
6.  **Rule Management**: Maintain modular AI rules in `.agents/rules/` and synchronize them with root `.cursorrules`/`.gemini_rules` using `tools/sync_rules.sh`.
7.  **Semantic Context (Vector RAG)**: (Level 2) Support codebase indexing using vector databases to provide instant semantic search.

## Operating Procedures
- **Pre-Flight Check (MANDATORY)**: 
  1. **Check Git Environment**: You MUST run `git branch --show-current` BEFORE reading or touching any files. If you are on `main` or `master` and changes are requested, do NOT make them. You MUST ask the user to indicate that a new branch should be created. NEVER edit files directly on main branches.
  2. **Verify History**: Check for `HISTORY.md`, `BUGS.md`, and `.vectors/` index.
- **Search Strategy**: Use GHS for chronology and Vector Search for technical implementation context.
- **Post-task**: Update the history files with new work. Execute synchronization if applicable using `python3 tools/github_sync.py`.
- **Alerting**: If the history becomes "stale" (more than 3-5 commits without update), notify the user and offer an automatic update.
- **Synchronization**: At the end of a milestone or when a bug is registered, use `#ai-sync` to push updates to GitHub Issues/Projects.
- **Rule Sync**: After adding or modifying rules in `.agents/rules/`, execute `bash tools/sync_rules.sh` to update IDE-visible files.

## File Templates
- `HISTORY.md`: [Execution Summary, Branch Map, Full Commit Log].
- `BUGS.md`: [Bug Description, Origin, Fix, Date].

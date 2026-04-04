---
name: git-history
description: Maintain a project history, branch index, and bug registry in the user's preferred language(s).
config:
  languages: ["en", "es"]
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
  vector_store:
    provider: "qdrant" # Options: "chroma" (local), "qdrant" (server)
    url: "http://localhost:6333"
    collection_history: "ghs_history"
    collection_code: "ghs_code"
---

# Git History Management Skill

This skill enables the agent to maintain a high-quality, professional history for any Git project.

## Core Responsibilities
1.  **Chronological Indexing**: Maintain a `HISTORY.md` file that captures every major milestone, branch evolution, and **Author/Actor identity (AI vs Human)**.
2.  **Multi-language Support**: All documentation and commit messages must be provided in the user's preferred language(s) (e.g., English, Spanish, French, etc.).
3.  **Visual Documentation**: Integrate and caption screenshots in the `README.md` and `HISTORY.md`.
4.  **Issue Tracking**: Maintain a `BUGS.md` or a "Bug Registry" section to prevent regressions.
5.  **Semantic Context (Vector RAG)**: (Level 2) Support codebase indexing using vector databases to provide instant semantic search.

## Operating Procedures
- **Pre-task**: Check for `HISTORY.md`, `BUGS.md`, and `.vectors/` index.
- **Search Strategy**: Use GHS for chronology and Vector Search for technical implementation context.
- **Post-task**: Update the history files with new work.
- **Alerting**: If the history becomes "stale" (more than 3-5 commits without update), notify the user and offer an automatic update.

## File Templates
- `HISTORY.md`: [Execution Summary, Branch Map, Full Commit Log].
- `BUGS.md`: [Bug Description, Origin, Fix, Date].

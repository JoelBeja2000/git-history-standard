# 🧠 Level 2: Vector Context (RAG) / Nivel 2: Contexto Vectorial (RAG)

This methodology complements the **Git History Standard (GHS)** by providing the AI with "Semantic Memory" of the entire codebase. While GHS provides the *intent* (Why), Vector Context provides the *content* (How).

---

## 🛰️ How it Works / Cómo funciona

1.  **Chunking**: The codebase is split into small, logical pieces (functions, classes).
2.  **Embedding**: These pieces are converted into mathematical vectors (embeddings).
3.  **Storage**: Vectors are stored in a database (ChromaDB, Pinecone, or local FAISS).
4.  **Querying**: When you ask "Where is the login logic?", the AI searches the vector space and "feels" the relevant code instantly.

---

## 🛠️ Implementation Strategy / Estrategia de Implementación

### 1. AST-Aware Chunking / Fragmentación Inteligente
Instead of splitting code every 500 characters, we use **tree-sitter** or similar tools to split by **function** or **class**.
- **Rule**: Never split a function in the middle.
- **Metadata**: Each chunk MUST include the file path and line numbers.

### 2. The `.vectors/` cache
To keep the standard portable, we propose a `.vectors/` directory (ignored by Git, but maintained by the AI) that stores a local index of the codebase.

### 3. Automated Update Hook / Hook de Actualización
Add a `post-push` or `post-commit` hook that triggers the re-indexing of only the modified files.

## 📜 Vectorizing Git History & Documentation / Vectorizando la Historia y Documentación de Git
To achieve "Ultra-Fast" context, the AI must index not only the code but also the **Project Memory** itself:

1.  **History Indexing (`HISTORY.md`)**: Each commit entry is vectorized with its **Intent**, **Author**, and **Bilingual Message**.
    - *Benefit*: Querying "When did we fix the keyboard rendering?" returns the exact commit and context in milliseconds.
2.  **Bug Registry Indexing (`BUGS.md`)**: Symptoms and solutions are indexed semantically.
    - *Benefit*: If a new bug appears with symptoms like "lag in input," the AI scans the vector store for similar past issues and identifies the solution instantly.
3.  **Cross-Language Retrieval**: Using **Multilingual Embeddings** (e.g., `multilingual-e5`), a search in Spanish can retrieve the relevant history even if it was originally written in English (and vice versa).

---

## 📂 The `.ai-index/` Folder Structure
To standardize this across all IDEs and Agents:
- `.ai-index/manifest.json`: Tracks which versions of `HISTORY.md` and `BUGS.md` are indexed.
- `.ai-index/history_vectors.db`: The specialized vector store for the project's evolution.
- `.ai-index/code_vectors.db`: The semantic map of the source code.

---

## 🚀 AI Agent Performance (The "Ultra-Fast" Rule)
When an agent (Antigravity, Claude, etc.) enters a project with an `.ai-index/`, it MUST:
1.  **Sync the Index**: Check the manifest and re-index any updated history since the last push.
2.  **Prioritize Semantic Retrieval**: Use the vector store to answer "What has been done?" instead of reading the entire `HISTORY.md` linearly.

---
*Research Branch: feature/vector-context-research*

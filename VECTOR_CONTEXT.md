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

---

## 🤖 AI Instructions (Advanced)
If a project has Vector Context enabled, the AI MUST:
- **Semantic Search**: Use vector queries for broad questions ("How does the auth work?").
- **GHS Check**: Use `#ai-history` to link the semantic search with the chronological evolution.

---
*Research Branch: feature/vector-context-research*

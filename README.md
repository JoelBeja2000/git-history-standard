# 📜 Git History Standard (GHS)
### by Oveja 🐑

🇪🇸 [Leer en Español](README.es.md)

**Git History Standard (GHS)** is a documentation convention + a set of scripts that automate your project's history so any AI agent can understand it instantly.

**It's not a replacement for `git log`.** It's a structured layer on top that turns atomic commits into searchable semantic context.

---

## 📦 What Does This Install in My Repo?

GHS adds these files to your project root:

```
your-project/
├── .agents/skills/git-history/SKILL.md  ← Central config (YAML)
├── HISTORY.md                           ← Structured history (table)
├── BUGS.md                              ← Known bugs registry
├── tools/
│   ├── indexer.py                       ← Semantic indexer (ChromaDB/Qdrant)
│   ├── search.py                        ← Natural language search
│   └── setup.sh                         ← Python environment setup
├── assets/screenshots/                  ← Visual captures (optional)
├── docker-compose.yml                   ← For Qdrant (Level 3)
└── .gitignore                           ← Pre-configured to exclude sensitive data
```

> [!NOTE]
> No global dependencies are installed. Everything lives inside your repo and a local `.venv`.

---

## 🔒 Security & Privacy

First things first: GHS generates a local database (`.ai-index/`) that contains fragments of your code in plain text. **It should never be pushed to a public repository.**

The included `.gitignore` blocks by default:
- **`.ai-index/`** — Local vector database
- **`.env`** — API keys
- **`.venv/`** — Python environment

You can control this behavior in `SKILL.md`:

```yaml
security:
  share_index: false  # Only true for private team repos
  share_env: false    # Never true unless air-gapped
```

---

## 🆚 How Is This Different From a Good CHANGELOG.md?

A `CHANGELOG.md` is a static document a human reads top to bottom. GHS is a **living context system** designed to be queried, searched, and understood by an AI.

The fundamental difference: **all GHS information is vectorized.**

| | CHANGELOG.md | GHS |
|:---|:---|:---|
| **Search** | Ctrl+F (exact text) | Semantic natural language |
| **Query** | Linear, top to bottom | By concept, author, date or component |
| **AI Context** | AI reads it entirely every time | AI retrieves only what's relevant |
| **Scalability** | Becomes unreadable over time | Vector index grows without degradation |

### Concrete Example: Before vs After

**Without GHS** — The AI receives your history like this:
```
commit 7accc32 - Update payment module
commit eaeaa75 - Fix bug
commit 4311cec - Refactor auth
commit 195bcee - WIP
```
Your AI doesn't know what bug was fixed, why auth was refactored, or what "WIP" means. It has to read thousands of diff lines to guess.

**With GHS** — The AI doesn't just read a structured table: it *queries it semantically.*

| Commit | Author | Description | Technical Details |
| :--- | :--- | :--- | :--- |
| `7accc32` | @dev1 | Migrate payments to Stripe | Replace PayPal SDK with Stripe.js v3. Change webhook endpoint. |
| `eaeaa75` | @dev2 | Fix: Invoice rounding | Float precision error in `invoice.py:L45`. Apply `Decimal`. |
| `4311cec` | @dev1 | Refactor auth to JWT | Remove server-side sessions. Add middleware in `auth/jwt.py`. |

The AI now knows **what**, **who**, **why** and **where**. But the important thing isn't just the format — it can *ask about it*:

```bash
# Instead of searching "Stripe" with Ctrl+F...
python3 tools/search.py "when did we change the payment system?"

# → Returns commit 7accc32 with full technical context,
#   even though the commit doesn't mention "payment" in those exact words.
```

With a 500-entry `CHANGELOG.md`, that question is impossible. With GHS, it takes milliseconds.

---

## 🏷️ How It Works

The core of the standard is **Trigger Tags** in your commit messages:

- **`#ai-history`** — AI updates `HISTORY.md` with a technical summary of the change.
- **`#ai-bug`** — AI registers the bug and its fix in `BUGS.md`.
- **`#ai-catchup`** — AI scans all undocumented commits and generates a batch summary.

> [!IMPORTANT]
> **Forgot to add tags?** No problem. The `#ai-catchup` tag exists precisely to catch up with previously undocumented commits. It's the system's safety net.

If you don't add any tag, the commit is treated normally — GHS doesn't interfere.

> [!TIP]
> **Branch Awareness**: The standard requires AI agents to verify your current Git branch before any update. This ensures that the "Branch Map" in `HISTORY.md` is always accurate and prevents documenting changes in the wrong environment.

---

## ⚙️ Who Executes the AI?

This is the key question: you put `#ai-history` in your commit... then what?

GHS is a **convention**, not a service. The AI that executes the tasks depends on your environment. There are 3 models:

### 1. IDE-Integrated Agent (Automatic)
If you use an editor with built-in AI (Cursor, Windsurf, Kilo Code, Antigravity), the agent detects the `SKILL.md` when opening the project and responds to tags in real time. **You don't have to do anything extra.**

```
# You commit normally:
git commit -m "Migrate payments to Stripe #ai-history"

# → Your IDE agent reads the tag, opens HISTORY.md and updates it.
```

### 2. Manual CLI Execution (On demand)
If you use an AI with terminal access (Claude CLI, GitHub Copilot CLI), simply ask it to review recent commits:

```bash
# You tell your AI:
"Review commits with #ai-history and update HISTORY.md"
```

### 3. CI/CD Automation (No humans)
For teams, you can set up a **GitHub Action** that runs a script after each push to `master`. The script reads new commits, detects tags and updates files automatically.

> [!NOTE]
> GHS doesn't enforce any of these models. You choose how and when the AI runs based on your workflow.

---

## ⚡ Installation

```bash
# 1. Clone the standard
git clone https://github.com/JoelBeja2000/git-history-standard.git

# 2. Copy the structure to your project
cp -r git-history-standard/.agents /path/to/your/project/
cp git-history-standard/HISTORY.md /path/to/your/project/
cp git-history-standard/BUGS.md /path/to/your/project/
cp -r git-history-standard/tools /path/to/your/project/
cp git-history-standard/docker-compose.yml /path/to/your/project/  # Optional (Level 3)
```

Once copied, any compatible AI agent will detect the `SKILL.md` file and follow the rules automatically.

---

## 🛠️ Configuration & Agnostic Design

GHS is designed to be **storage and provider agnostic**. You can change any path or database provider in `.agents/skills/git-history/SKILL.md`.

Everything is defined in the YAML frontmatter:

```yaml
config:
  # ...
  screenshots:
    path: "assets/screenshots/" # Use any local or shared path
  vector_store:
    provider: "chroma"  # EXTENSIBLE: supports local or any cloud DB (Qdrant, Pinecone, etc.)
```
  languages: ["en", "es"]
  history_file: "HISTORY.md"
  bug_file: "BUGS.md"
  ai_tags:
    history: "#ai-history"
    bug: "#ai-bug"
    catch_up: "#ai-catchup"
  include_author: true
  screenshots:
    enabled: true
    path: "assets/screenshots/"
    auto_index: true
    analyze_images: true  # false = save vision tokens
  security:
    share_index: false
    share_env: false
  vector_store:
    provider: "chroma"  # Options: "chroma" (local) or "qdrant" (server)
```

---

## 🧠 Semantic Search (Levels)

GHS has 3 adoption levels. You don't need the highest to get started:

| Level | Requirements | Activation Command | Description |
| :--- | :--- | :--- | :--- |
| **1. Plain Text** | None | *Automatic* | Just `HISTORY.md` + `BUGS.md`. AI reads them directly. |
| **2. Local** | Python | `bash tools/setup.sh` | Local vector indexing using ChromaDB. |
| **3. Enterprise** | Docker | `docker-compose up -d` | Shared server for teams using Qdrant. |

### 🚀 How to Enable

#### Level 1: Ready to go
Just copy the files. Any AI agent (Antigravity, Cursor, etc.) will detect the `SKILL.md` and read the history files as standard text.

#### Level 2: Local Search (ChromaDB)
1. Ensure you have Python installed.
2. Run: `bash tools/setup.sh`
3. The script will create a `.venv`, install dependencies, and index your project.

#### Level 3: Team Search (Qdrant)
1. Ensure Docker is running.
2. Run: `docker-compose up -d`
3. Edit `.agents/skills/git-history/SKILL.md` to set `vector_store.provider: "qdrant"`.
4. Run: `python3 tools/indexer.py`


---

### 📸 Advanced: Custom Screenshots & Storage

GHS allows you to store your project's visual history anywhere:

1. **Change the Path**: Edit `.agents/skills/git-history/SKILL.md` and update `screenshots.path`. The AI agent will immediately start saving and looking for images in that new directory.
2. **AI-Driven Uploads**: When you ask an agent to "Sync History", it will automatically:
   - Identify new images in your custom path.
   - Run `git add` for those images.
   - Embed them in `HISTORY.md` using the new path.
3. **Semantic Discovery**: Our `indexer.py` scans your history for Markdown images (`![alt](path)`). The `alt-text` is indexed into your vector database (Chroma/Qdrant), making your UI changes searchable by description.


#### 🔗 Universal Database & API Support (Agnostic Design)
GHS is a **universal protocol**. You can link **any database** (PostgreSQL, MongoDB, Redis, custom DBs in Rust/Go/C++, or cloud buckets):
- **Universal References**: Use custom URIs in your `HISTORY.md` like `![Alt](my-db://image_id)` or `![Capture](https://api.your-app.com/v1/storage/123)`.
- **Custom Bridges**: If your DB is private, create a small "bridge" script in `tools/`. The AI will follow the rules in `SKILL.md` and know how to query that bridge to retrieve or upload information.
- **Total Independence**: GHS doesn't care where you store your data, only how you label it.

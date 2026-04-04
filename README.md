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

## 🛠️ Configuration

Everything is defined in `.agents/skills/git-history/SKILL.md` (YAML frontmatter):

```yaml
config:
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

| Level | Requirements | Description |
| :--- | :--- | :--- |
| **1. Plain Text** | None | Just `HISTORY.md` + `BUGS.md`. The AI reads them directly. |
| **2. Local (ChromaDB)** | Python + `.venv` | Local vector indexing for semantic search. |
| **3. Enterprise (Qdrant)** | Docker | Shared server for teams. Collective memory. |

### Level 2: Local Search
```bash
bash tools/setup.sh           # Install ChromaDB in .venv
source .venv/bin/activate
python3 tools/indexer.py       # Index your project
python3 tools/search.py "authentication" --collection all
```

### Level 3: Shared Server (Docker)
```bash
docker-compose up -d           # Start Qdrant on port 6333
```
Then change `provider: "qdrant"` in your `SKILL.md`.

---

## 🖼️ Visual Documentation

GHS lets you attach screenshots to commits so reviewers can see changes directly on GitHub.

**Flow:**
1. Save your screenshot in `assets/screenshots/` (or your configured folder).
2. Reference it in the "Screenshots" column of `HISTORY.md`:

| Commit | Author | Description | Screenshots |
| :--- | :--- | :--- | :--- |
| `fe30d72` | @dev1 | Sidebar redesign | ![Sidebar v2](assets/screenshots/sidebar_v2.png) |

> [!NOTE]
> Images **must** be pushed to Git (unlike the vector index). It's the only way they'll be visible on GitHub/GitLab during Code Reviews.

Image alt-text is indexed in the vector database, enabling visual change search by concept (*"when did we change the sidebar?"*).

---

## 👥 Team Usage

GHS scales from a solo developer to large teams:

- **Shared server**: Point all team `SKILL.md` files to the same Qdrant to share a common project memory.
- **CI/CD**: Set up a GitHub Action that runs `tools/indexer.py` on every merge to `master`.
- **Traceability**: The "Author" column in `HISTORY.md` and `BUGS.md` makes it clear who made each change and which AI documented it.

---

## 🤖 AI Agent Integration

### Example: Using it with Antigravity, Cursor or Windsurf
When you use a sophisticated AI agent that has file system access (like Antigravity or Cursor), the experience is completely seamless.

1. You create a commit with the tag: `git commit -m "Update login flow #ai-history"`
2. You ask your agent: *"I just made a commit with #ai-history, please execute the standard."*
3. **The Magic:** The agent will automatically find the `.agents/skills/git-history/SKILL.md` file in your repository, read the exact rules on how to document history, read your `git diff`, and update `HISTORY.md` perfectly without you needing to explain *how* to do it.

Any agent can consume context in two ways:

### Direct Reading
Tell your AI to read `SKILL.md` and `HISTORY.md`. Being semantically structured, the AI will understand the project instantly.

### Terminal Integration
If your AI has terminal access, use the `--json` flag for machine-readable context:
```bash
python3 tools/search.py "error context" --json
```

### 🪄 Bonus: Hands-Free Git Workflow
Did you know you can instruct your AI to handle all your Git and GitHub commands automatically using the `gh` CLI?  
🔗 **[Read the Automated Git Workflow Guide](docs/automated-git-workflow.md)**

---

## 🖥️ Compatibility

GHS works with **any** Git client (SourceTree, GitKraken, VS Code, Terminal). It relies on standard commit messages — no extensions or plugins required.

---

## 📄 License

This project is under the MIT License — see [LICENSE](LICENSE) for details.

---
*Created by [Oveja](https://github.com/JoelBeja2000) — Simplifying Human-AI collaboration.*

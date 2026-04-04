# 📜 Git History Standard (GHS) / Estándar de Historia de Git

**[EN]** The **Git History Standard (GHS)** is a powerful documentation framework designed to automate project indexing and optimize AI-agent collaboration. By using structured `.agents` skills and workflows, it allows developers to trigger professional documentation directly from their Git commit messages.

**[ES]** El **Estándar de Historia de Git (GHS)** es un potente marco de trabajo de documentación diseñado para automatizar la indexación de proyectos y optimizar la colaboración con agentes de IA. Mediante el uso de habilidades y flujos de trabajo estructurados en la carpeta `.agents`, permite a los desarrolladores activar la documentación profesional directamente desde sus mensajes de commit de Git.

---

## 🏷️ AI-Triggered Documentation / Documentación Activada por IA

The core of this standard is the use of **Trigger Tags** in your commit messages. When an AI agent detects these tags, it automatically performs the required documentation tasks:

- **`#ai-history`**: Signals the AI to update the `HISTORY.md` and `README.md` based on recent code changes. The AI will then mark the commit as `[documented]`.
- **`#ai-bug`**: Signals that the commit contains a bug fix. The AI will automatically log the issue in the **Bug Registry** (`BUGS.md`) to prevent future regressions.

---

## 🚀 Key Features / Características Clave

- **⚡ Instant Context / Contexto Instantáneo**: Optimized for AI agents (Claude, GPT, Gemini) to understand the project's evolution in seconds.
- **🐛 Bug Registry / Registro de Errores**: Integrated tracking to document solutions and avoid repeating past mistakes.
- **📂 Incremental Indexing / Indexación Incremental**: Maintains a clean, chronological `HISTORY.md` that serves as a master index for the entire codebase.
- **🌍 Bilingual Support (Optional) / Soporte Bilingüe (Opcional)**: Easily configurable to maintain all history and documentation in both English and Spanish.

---

## 📦 Installation / Instalación

To adopt this standard, simply copy the `.agents` folder into your repository root:

```bash
# Clone the standard repo
git clone https://github.com/JoelBeja2000/git-history-standard.git

# Copy the agent configuration to your project
cp -r git-history-standard/.agents /path/to/your/project/
```

Once installed, any compatible AI agent will recognize the `git-history` skill and respond to your `#tags` automatically.

---

## 🛠️ Components / Componentes

- **`.agents/skills/git-history/SKILL.md`**: Defines how the AI should handle history and bug documentation.
- **`.agents/workflows/maintain-history.md`**: The step-by-step procedure for tag detection and documentation syncing.
- **`HISTORY.md`**: Your project's master index (Commits, Branches, Milestones).
- **`BUGS.md`**: Documentation of solved issues and troubleshooting.

---

## 📄 License / Licencia

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by [Oveja](https://github.com/JoelBeja2000) - Simplifying AI-Human collaboration.*

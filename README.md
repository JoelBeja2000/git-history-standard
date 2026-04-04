# 📜 Git History Standard (BGHS) / Estándar de Historia Bilingüe de Git

**[EN]** The **Bilingual Git History Standard (BGHS)** is a framework designed to professionalize project documentation and optimize AI-agent collaboration. By using structured `.agents` skills and workflows, it ensures that your project's evolution is capture in both English and Spanish, with an automated bug registry and context-aware trigger tags.

**[ES]** El **Estándar de Historia Bilingüe de Git (BGHS)** es un marco de trabajo diseñado para profesionalizar la documentación de proyectos y optimizar la colaboración con agentes de IA. Mediante el uso de habilidades y flujos de trabajo estructurados en la carpeta `.agents`, asegura que la evolución de tu proyecto se capture tanto en inglés como en español, con un registro de errores automatizado y etiquetas de activación inteligentes.

---

## 🚀 Key Features / Características Clave

- **🌍 100% Bilingual / 100% Bilingüe**: All commits and documentation are mirrored in EN/ES.
- **🤖 AI-Native / Nativo para IA**: Optimized for AI agents (Claude, GPT, Gemini) to understand project context in seconds.
- **🏷️ Trigger Tags / Etiquetas Activadoras**: Use `#ai-history` in your commits to trigger automatic documentation.
- **🐛 Bug Registry / Registro de Errores**: Integrated tracking to prevent regressions and document solutions.

---

## 📦 Installation / Instalación

To adopt this standard in your project, simply copy the `.agents` folder into your repository root:

```bash
# Clone this standard
git clone https://github.com/JoelBeja2000/git-history-standard.git

# Copy the agent configuration to your project
cp -r git-history-standard/.agents /path/to/your/project/
```

Once installed, any compatible AI agent will recognize the `git-history` skill and follow the maintenance workflows automatically.

---

## 🛠️ Components / Componentes

- **`.agents/skills/git-history/SKILL.md`**: Defines the AI's capabilities and bilingual requirements.
- **`.agents/workflows/maintain-history.md`**: Step-by-step instructions for history synchronization.
- **`HISTORY.md`**: The master index of the project's evolution.
- **`BUGS.md`**: The registry for tracking and solving recurring issues.

---

## 📄 License / Licencia

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by [Oveja](https://github.com/JoelBeja2000) - Building the future of AI-assisted development.*

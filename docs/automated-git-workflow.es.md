# 🤖 Flujo de Git Automatizado por IA

Mientras que **GHS** se centra en documentar el historial de tu proyecto, puedes llevar tu flujo de trabajo al siguiente nivel dejando que tu agente de IA controle las operaciones de Git y GitHub por completo.

Si usas un agente con acceso a terminal (como Antigravity, Cursor o Claude CLI), puedes instruirle para que gestione tus repositorios de forma automática.

## Requisitos
- Git instalado.
- [GitHub CLI (gh)](https://cli.github.com/) instalado y autenticado (`gh auth login`).

## El Flujo de Trabajo "Sin Manos"

En lugar de escribir comandos de Git manualmente, dale instrucciones de alto nivel a tu IA.

### 1. Inicializar y Crear un Repositorio
Al empezar un proyecto nuevo, dile a tu IA:
> *"Inicializa esta carpeta como un repositorio git, crea un repo público en mi GitHub usando gh CLI, y haz el push del primer commit."*

La IA ejecutará:
```bash
git init
git add .
git commit -m "Initial commit"
gh repo create mi-proyecto --public --source=. --remote=origin
git push -u origin master
```

### 2. Commits Diarios con GHS
Cuando termines una funcionalidad, dile a tu IA:
> *"Revisa mis cambios actuales, haz un commit usando el tag #ai-history con un mensaje relevante, ejecuta el estándar GHS para actualizar el HISTORY.md, y súbelo al repositorio (push)."*

La IA se encargará del `git add`, escribirá el mensaje de commit, actualizará los archivos de seguimiento de GHS, lo unificará todo en un commit y hará el push.

### 3. Crear Pull Requests
Si estás trabajando en una rama, pídele a tu IA:
> *"Sube esta rama y crea un PR a master usando gh CLI. Resume mis cambios en el cuerpo del PR."*

---

## ⚡ Bonus: Integración con NotebookLM
Si quieres crear un **NotebookLM** (Google) personalizado con el conocimiento de tu proyecto, hemos incluido una herramienta de exportación:

1. Ejecuta el script: `python3 tools/export_notebooklm.py`
2. Esto creará el archivo `ghs_context_for_notebooklm.txt`.
3. Arrastra y suelta ese archivo en el panel de fuentes de NotebookLM.

Ahora puedes chatear con tu proyecto o generar un podcast técnico sobre tu propio código.

---

> [!TIP]
> **La Lección Clave**: Trata a tu IA como un ingeniero de infraestructura. Ya no necesitas escribir comandos en la terminal. Solo explica el evento que quieres desencadenar (crear repo, guardar trabajo, abrir PR), y deja que el agente se encargue de la sintaxis de Git/GitHub.

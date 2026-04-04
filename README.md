# 📜 Git History Standard (GHS) / Estándar de Historia de Git

El **Estándar de Historia de Git (GHS)** es un marco de trabajo de documentación universal diseñado para automatizar la indexación de proyectos y optimizar la colaboración con agentes de IA. Es **agnóstico al idioma** y se adapta a las preferencias del usuario, permitiendo activar documentación profesional directamente desde los mensajes de commit.

---

## 🏷️ Documentación Activada por IA

El núcleo de este estándar es el uso de **Etiquetas de Activación (Trigger Tags)** en tus mensajes de commit. Cuando un agente de IA detecta estas etiquetas, realiza de forma automática las tareas de documentación:

- **`#ai-history`**: Indica a la IA que actualice el historial del proyecto (`HISTORY.md`) basándose en los últimos cambios de código.
- **`#ai-bug`**: Indica que el commit contiene la corrección de un error. La IA registrará automáticamente el problema en el **Registro de Errores** (`BUGS.md`) para evitar regresiones futuras.

> [!IMPORTANT]
> ### 🔄 Modo "Catch up" (Ponerse al día)
> ¿Has olvidado poner etiquetas en tus últimos commits? No te preocupes. 
> Usa la etiqueta **`#ai-catchup`** (configurable) para que la IA escanee todos los commits no documentados desde la última entrada del historial y genere un resumen profesional de golpe. ¡Es la red de seguridad del estándar GHS!

---

## 🚀 Características Clave

- **⚡ Contexto Instantáneo**: Optimizado para que agentes de IA (Claude, GPT, Gemini) entiendan la evolución del proyecto en segundos.
- **🐛 Registro de Errores**: Seguimiento integrado para documentar soluciones y evitar repetir errores pasados.
- **📂 Indexación Incremental**: Mantiene un archivo `HISTORY.md` limpio y cronológico que sirve como índice maestro de todo el código.
- **🌍 Soporte Multi-idioma**: Se adapta a cualquier idioma (español, inglés, francés, etc.) definido por el usuario.
- **🧠 Nivel 2: Contexto Semántico (Vector RAG)**: Soporte integrado para indexación y búsqueda semántica de código usando ChromaDB.

---

## 📦 Instalación

Para adoptar este estándar, simplemente copia la carpeta `.agents` en la raíz de tu repositorio:

```bash
# Clona el repositorio del estándar
git clone https://github.com/JoelBeja2000/git-history-standard.git

# Copia la configuración del agente a tu proyecto
cp -r git-history-standard/.agents /ruta/a/tu/proyecto/
```

Una vez instalado, cualquier agente de IA compatible reconocerá la habilidad `git-history` y responderá a tus `#tags` automáticamente.

---

## 🛠️ Configuración (Tuneado)

Puedes personalizar el estándar editando el archivo `.agents/skills/git-history/SKILL.md`. En la sección de cabecera (YAML), puedes ajustar:

```yaml
config:
  languages: ["es", "en"]      # Idiomas preferidos
  history_file: "HISTORY.md"   # Nombre del archivo de historial
  bug_file: "BUGS.md"         # Nombre del registro de errores
  ai_tags:
    history: "#ai-history"     # Tags personalizados
    bug: "#ai-bug"
```

---

## 🧠 Búsqueda Semántica (Vector RAG)

Usa las herramientas incluidas para indexar y buscar en tu código con inteligencia artificial:

### 1. Preparación
```bash
# Configura el entorno (crea .venv e instala ChromaDB)
bash tools/setup.sh
```

### 2. Uso de herramientas
```bash
# Activa el entorno
source .venv/bin/activate

# Buscar contexto (ej: "¿cómo se gestiona la autenticación?")
python3 tools/search.py "autenticación" --collection all

# Re-indexar tras cambios importantes
python3 tools/indexer.py
```

---

## 🏗️ Modo Pro: Integración con Docker y Qdrant

Para proyectos de gran escala o equipos que requieren una base de datos de vectores robusta (similar a la que usan extensiones como **Kilo Pass**), GHS soporta **Qdrant** a través de Docker.

### 1. Levantar el Servidor
```bash
# Inicia Qdrant en el puerto 6333
docker-compose up -d
```

### 2. Configurar el Proveedor
En `.agents/skills/git-history/SKILL.md`, cambia el proveedor a `qdrant`:
```yaml
vector_store:
  provider: "qdrant"
  url: "http://localhost:6333"
```

### 3. Ventajas del Modo Pro
- **Persistencia Aislada**: Los datos de vectores se gestionan fuera del código fuente.
- **Rendimiento**: Búsquedas semánticas optimizadas para miles de archivos.
- **Compatibilidad**: Listo para integrarse con herramientas que consumen APIs de Qdrant.

---

## 🆚 ¿Por qué GHS?

A diferencia de estándares como **Conventional Commits**, GHS está diseñado específicamente para la "Colaboración en Vivo" entre humanos e IA:

| Commit | Author / Autor | Description / Descripción | Details / Detalles Técnicos |
| :--- | :--- | :--- | :--- |
| `7accc32` | @JoelBeja2000 | [AI] Update README with Vector Context | Generalize multi-language support and add RAG docs. |

---

## 🖥️ Compatibilidad Universal

GHS funciona con **CUALQUIER** cliente de Git porque se basa en metadatos estándar. Puedes usar SourceTree, GitKraken, VS Code o la Terminal. La IA detectará el mensaje del commit sin importar cómo se haya creado.

---

## 🔒 Seguridad y Privacidad (Configurable)

El uso de herramientas de IA y bases de datos vectoriales requiere precaución. GHS te permite configurar qué quieres compartir en el archivo `.agents/skills/git-history/SKILL.md`:

```yaml
security:
  share_index: false # Controla si se debe subir el índice (.ai-index/)
  share_env: false   # Controla si se deben subir secretos (.env)
```

> [!IMPORTANT]
> **Por defecto, todo lo sensible está BLOQUEADO en el `.gitignore`.** 
> Si decides cambiar estos valores a `true` en la configuración para compartirlos en un repositorio PRIVADO de equipo, recuerda que debes eliminar manualmente las líneas correspondientes del archivo `.gitignore` de la raíz.

### ¿Por qué es importante?
- **`.ai-index/`**: Contiene fragmentos de tu código en texto plano dentro de la base de datos de vectores. **Subirlo a un repo público es un riesgo de seguridad.**
- **`.env`**: Contiene tus API Keys. **Subirlo es entregar las llaves de tu cuenta de IA a cualquiera.**

---

## 🖼️ Documentación Visual (Capturas de Pantalla)

GHS permite adjuntar pruebas visuales a tus commits para que los revisores en GitHub vean el cambio sin ejecutar el código.

### 1. Configuración
Activa el soporte en `.agents/skills/git-history/SKILL.md`:
```yaml
screenshots:
  enabled: true
  path: "assets/screenshots/"
  auto_index: true # Indexa el texto alternativo para búsqueda semántica
```

### 2. Cómo usarlo
Cuando realices un cambio visual, añade la captura a la carpeta configurada y menciónala en el `HISTORY.md`:

| Commit | Autor | Descripción | Screenshots / Capturas |
| :--- | :--- | :--- | :--- |
| `a1b2c3d` | @user | Nuevo diseño del Header | ![Header v2](assets/screenshots/header_v2.png) |

> [!TIP]
> **Indexación Visual**: El texto alternativo (`Header v2`) será indexado en la base de datos de vectores. Si buscas "header", la IA encontrará tanto el código como la captura visual asociada.

### 👁️ Análisis de IA (Visión)
Este estándar instruye a los agentes de IA para que, al encontrar una ruta de imagen en el historial, utilicen sus herramientas de visión (como `view_file`) para inspeccionar el cambio. Esto permite que la IA te diga: *"He analizado la captura y el botón de 'Aceptar' ahora cumple con el diseño solicitado"*.

---

## 👥 Colaboración en Equipo (Enterprise Mode)

GHS está diseñado para escalar desde un desarrollador solo hasta grandes equipos de ingeniería. Aquí te explicamos cómo usarlo de forma profesional:

### 1. Servidor de Vectores Compartido
En lugar de que cada desarrollador tenga su propia base de datos local, el equipo puede levantar un único servidor de **Qdrant** (en un VPS o servidor interno) y apuntar todos sus `SKILL.md` a la misma URL para compartir la **misma memoria del proyecto**.

### 2. Automatización con CI/CD
Puedes configurar un **GitHub Action** para que ejecute `tools/indexer.py` automáticamente cada vez que se apruebe un Pull Request en `master`. Así, el índice semántico estará siempre actualizado para todos.

### 3. Trazabilidad Total
Gracias a la columna **Author / Autor** en el `HISTORY.md` y `BUGS.md`, el equipo siempre sabrá qué compañero hizo un cambio y qué IA lo documentó.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤖 Integración Universal de IA (Claude, GPT, Antigravity)

Este estándar es "AI-First". Cualquier agente de IA puede consumir este contexto de dos formas:

### 1. Lectura Directa
Simplemente indica a tu IA que lea los archivos `.agents/skills/git-history/SKILL.md` y `HISTORY.md`. Al estar estructurados semánticamente, la IA entenderá el proyecto al instante.

### 2. Integración por Terminal (Modo Agente)
Si usas una IA con acceso a terminal (como Claude CLI o Antigravity), puedes pedirle que ejecute la búsqueda con el flag `--json`:

```bash
# La IA obtendrá un objeto JSON procesable con todo el contexto
python3 tools/search.py "contexto del error" --json
```

---

---
*Creado por [Oveja](https://github.com/JoelBeja2000) - Simplificando la colaboración Humano-IA.*

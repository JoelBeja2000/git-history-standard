# 📜 Git History Standard (GHS) / Estándar de Historia de Git

El **Estándar de Historia de Git (GHS)** es un marco de trabajo de documentación universal diseñado para automatizar la indexación de proyectos y optimizar la colaboración con agentes de IA. Es **agnóstico al idioma** y se adapta a las preferencias del usuario, permitiendo activar documentación profesional directamente desde los mensajes de commit.

---

## 🏷️ Documentación Activada por IA

El núcleo de este estándar es el uso de **Etiquetas de Activación (Trigger Tags)** en tus mensajes de commit. Cuando un agente de IA detecta estas etiquetas, realiza de forma automática las tareas de documentación:

- **`#ai-history`**: Indica a la IA que actualice el historial del proyecto (`HISTORY.md`) basándose en los últimos cambios de código.
- **`#ai-bug`**: Indica que el commit contiene la corrección de un error. La IA registrará automáticamente el problema en el **Registro de Errores** (`BUGS.md`) para evitar regresiones futuras.

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

| Característica | Estándar GHS | Conventional Commits |
| :--- | :--- | :--- |
| **Activador en Tiempo Real** | Sí (#tags) | No (Estructura estática) |
| **Multi-idioma** | Nativo (Configurable) | Manual / Post-proceso |
| **Registro de Errores** | Integrado (BUGS.md) | Gestor externo |
| **Contexto para IA** | Indexación Profesional | Solo basado en Diffs |

---

## 🖥️ Compatibilidad Universal

GHS funciona con **CUALQUIER** cliente de Git porque se basa en metadatos estándar. Puedes usar SourceTree, GitKraken, VS Code o la Terminal. La IA detectará el mensaje del commit sin importar cómo se haya creado.

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

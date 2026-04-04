# 📜 Git History Standard (GHS)
### by Oveja 🐑

🇬🇧 [Read in English](README.md)

El **Git History Standard (GHS)** es una convención de documentación + un conjunto de scripts que automatizan el historial de tu proyecto para que cualquier agente de IA lo entienda al instante.

**No es un reemplazo de `git log`.** Es una capa estructurada por encima que convierte commits atómicos en contexto semántico buscable.

---

## 📦 ¿Qué instala exactamente en mi repo?

GHS añade estos archivos a la raíz de tu proyecto:

```
tu-proyecto/
├── .agents/skills/git-history/SKILL.md  ← Configuración central (YAML)
├── HISTORY.md                           ← Historial estructurado (tabla)
├── BUGS.md                              ← Registro de errores conocidos
├── tools/
│   ├── indexer.py                       ← Indexador semántico (ChromaDB/Qdrant)
│   ├── search.py                        ← Búsqueda por lenguaje natural
│   └── setup.sh                         ← Instalación del entorno Python
├── assets/screenshots/                  ← Capturas visuales (opcional)
├── docker-compose.yml                   ← Para Qdrant (Nivel 3)
└── .gitignore                           ← Pre-configurado para excluir datos sensibles
```

> [!NOTE]
> No instala dependencias globales. Todo vive dentro de tu repositorio y un `.venv` local.

---

## 🔒 Seguridad y Privacidad

Antes de nada: GHS genera una base de datos local (`.ai-index/`) que contiene fragmentos de tu código en texto plano. **Nunca debe subirse a un repositorio público.**

El `.gitignore` incluido bloquea por defecto:
- **`.ai-index/`** — Base de datos de vectores local
- **`.env`** — Claves de API
- **`.venv/`** — Entorno de Python

Puedes controlar este comportamiento en `SKILL.md`:

```yaml
security:
  share_index: false  # Solo true en repos privados de equipo
  share_env: false    # Nunca true salvo entornos air-gapped
```

---

## 🆚 ¿En qué se diferencia de un buen CHANGELOG.md?

Un `CHANGELOG.md` es un documento estático que un humano lee de arriba a abajo. GHS es un **sistema de contexto vivo** diseñado para que una IA lo consulte, lo busque y lo entienda.

La diferencia fundamental: **toda la información de GHS está vectorizada.**

| | CHANGELOG.md | GHS |
|:---|:---|:---|
| **Búsqueda** | Ctrl+F (texto exacto) | Lenguaje natural semántico |
| **Consulta** | Lineal, de arriba a abajo | Por concepto, autor, fecha o componente |
| **Contexto para IA** | La IA lo lee entero cada vez | La IA recupera solo lo relevante |
| **Escalabilidad** | Se vuelve ilegible con el tiempo | El índice vectorial crece sin degradarse |

### Ejemplo concreto: Antes vs Después

**Sin GHS** — La IA recibe tu historial así:
```
commit 7accc32 - Update payment module
commit eaeaa75 - Fix bug
commit 4311cec - Refactor auth
commit 195bcee - WIP
```
Tu IA no sabe qué bug se arregló, por qué se refactorizó auth, ni qué significa "WIP". Tiene que leer miles de líneas de diff para adivinar.

**Con GHS** — La IA no solo lee una tabla estructurada: la *consulta semánticamente.*

| Commit | Author | Description | Technical Details |
| :--- | :--- | :--- | :--- |
| `7accc32` | @dev1 | Migrar pagos a Stripe | Reemplazar PayPal SDK por Stripe.js v3. Cambiar webhook endpoint. |
| `eaeaa75` | @dev2 | Fix: Redondeo en facturas | Error de precisión float en `invoice.py:L45`. Aplicar `Decimal`. |
| `4311cec` | @dev1 | Refactorizar auth a JWT | Eliminar sesiones server-side. Añadir middleware en `auth/jwt.py`. |

La IA ahora sabe **qué**, **quién**, **por qué** y **dónde**. Pero lo importante no es solo el formato — es que puede *preguntarlo*:

```bash
# En lugar de buscar "Stripe" con Ctrl+F...
python3 tools/search.py "¿cuándo cambiamos el sistema de pagos?"

# → Devuelve commit 7accc32 con todo su contexto técnico,
#   aunque el commit no mencione "pagos" con esa palabra exacta.
```

Con un `CHANGELOG.md` de 500 entradas, esa pregunta es imposible. Con GHS, tarda milisegundos.

---

## 🏷️ Cómo Funciona

El núcleo del estándar son **Etiquetas de Activación** en tus mensajes de commit:

- **`#ai-history`** — La IA actualiza `HISTORY.md` con un resumen técnico del cambio.
- **`#ai-bug`** — La IA registra el error y su solución en `BUGS.md`.
- **`#ai-catchup`** — La IA escanea todos los commits no documentados y genera un resumen en lote.

> [!IMPORTANT]
> **¿Has olvidado poner etiquetas?** No pasa nada. El tag `#ai-catchup` existe precisamente para ponerse al día con commits pasados sin documentar. Es la red de seguridad del sistema.

Si no pones ninguna etiqueta, el commit se trata de forma normal — GHS no interfiere.

> [!TIP]
> **Conciencia de Ramas**: El estándar obliga a los agentes de IA a verificar tu rama de Git actual antes de cualquier actualización. Esto asegura que el "Mapa de Ramas" en `HISTORY.md` sea siempre preciso y evita documentar cambios en el entorno equivocado.

---

## ⚙️ ¿Quién ejecuta la IA?

Esta es la pregunta clave: pones `#ai-history` en tu commit... ¿y luego qué?

GHS es una **convención**, no un servicio. La IA que ejecuta las tareas depende de tu entorno. Hay 3 modelos:

### 1. Agente integrado en el IDE (Automático)
Si usas un editor con IA integrada (Cursor, Windsurf, Kilo Code, Antigravity), el agente detecta el `SKILL.md` al abrir el proyecto y responde a los tags en tiempo real. **No tienes que hacer nada extra.**

```
# Haces tu commit normalmente:
git commit -m "Migrar pagos a Stripe #ai-history"

# → Tu agente de IDE lee el tag, abre HISTORY.md y lo actualiza.
```

### 2. Ejecución manual por CLI (Bajo demanda)
Si usas una IA con acceso a terminal (Claude CLI, GitHub Copilot CLI), simplemente le pides que revise los últimos commits:

```bash
# Le dices a tu IA:
"Revisa los commits con #ai-history y actualiza HISTORY.md"
```

### 3. Automatización CI/CD (Sin humanos)
Para equipos, puedes configurar un **GitHub Action** que ejecute un script tras cada push a `master`. El script lee los commits nuevos, detecta los tags y actualiza los archivos automáticamente.

> [!NOTE]
> GHS no impone ninguno de estos modelos. Tú eliges cómo y cuándo se ejecuta la IA según tu flujo de trabajo.

---

## ⚡ Instalación

```bash
# 1. Clona el estándar
git clone https://github.com/JoelBeja2000/git-history-standard.git

# 2. Copia la estructura a tu proyecto
cp -r git-history-standard/.agents /ruta/a/tu/proyecto/
cp git-history-standard/HISTORY.md /ruta/a/tu/proyecto/
cp git-history-standard/BUGS.md /ruta/a/tu/proyecto/
cp -r git-history-standard/tools /ruta/a/tu/proyecto/
cp git-history-standard/docker-compose.yml /ruta/a/tu/proyecto/  # Opcional (Nivel 3)
```

Una vez copiado, cualquier agente de IA compatible detectará el archivo `SKILL.md` y seguirá las reglas automáticamente.

---

## 🛠️ Configuración y Diseño Agnóstico

GHS está diseñado para ser **agnóstico al almacenamiento y al proveedor**. Puedes cambiar cualquier ruta o base de datos en `.agents/skills/git-history/SKILL.md`.

Todo se define en el frontmatter YAML:

```yaml
config:
  # ...
  screenshots:
    path: "assets/screenshots/" # Usa cualquier ruta local o compartida
  vector_store:
    provider: "chroma"  # EXTENSIBLE: soporta local o cualquier nube (Qdrant, Pinecone, etc.)
```
  languages: ["es", "en"]
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
    analyze_images: true  # false = ahorra tokens de visión
  security:
    share_index: false
    share_env: false
  vector_store:
    provider: "chroma"  # Opciones: "chroma" (local) o "qdrant" (servidor)
```

---

## 🧠 Búsqueda Semántica (Niveles)

GHS tiene 3 niveles de adopción. No necesitas el nivel más alto para empezar:

| Nivel | Requisitos | Comando de Activación | Descripción |
| :--- | :--- | :--- | :--- |
| **1. Texto Plano** | Ninguno | *Automático* | Solo `HISTORY.md` + `BUGS.md`. La IA los lee directamente. |
| **2. Local** | Python | `bash tools/setup.sh` | Indexación local usando ChromaDB. |
| **3. Enterprise** | Docker | `docker-compose up -d` | Servidor compartido para equipos usando Qdrant. |

### 🚀 Cómo Activar

#### Nivel 1: Listo para usar
Solo copia los archivos. Cualquier agente de IA (Antigravity, Cursor, etc.) detectará el `SKILL.md` y leerá los archivos de historial como texto estándar.

#### Nivel 2: Búsqueda Local (ChromaDB)
1. Asegúrate de tener Python instalado.
2. Ejecuta: `bash tools/setup.sh`
3. El script creará un `.venv`, instalará dependencias e indexará tu proyecto.

#### Nivel 3: Búsqueda de Equipo (Qdrant)
1. Asegúrate de tener Docker abierto.
2. Ejecuta: `docker-compose up -d`
3. Edita `.agents/skills/git-history/SKILL.md` para poner `vector_store.provider: "qdrant"`.
4. Ejecuta: `python3 tools/indexer.py`

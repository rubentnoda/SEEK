# AgenticSeek - Documentación Completa

## Índice

1. [Instalación](#instalación)
2. [Configuración](#configuración)
3. [Proveedores LLM](#proveedores-llm)
4. [Ejecución](#ejecución)
5. [Configuración Avanzada](#configuración-avanzada)
6. [Solución de Problemas](#solución-de-problemas)

---

## Instalación

### Requisitos Previos

- Python 3.10
- Docker y Docker Compose
- Google Chrome
- ChromeDriver (compatible con tu versión de Chrome)

### Pasos de Instalación

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
cp .env.example .env
```

#### 2. Crear Entorno Virtual

```bash
python3 -m venv agentic_seek_env
source agentic_seek_env/bin/activate
# En Windows: agentic_seek_env\Scripts\activate
```

#### 3. Instalar Dependencias

**Linux:**
```bash
sudo apt update
sudo apt install -y alsa-utils portaudio19-dev python3-pyaudio libgtk-3-dev libnotify-dev libgconf-2-4 libnss3 libxss1 chromium-chromedriver
pip3 install -r requirements.txt
```

**macOS:**
```bash
brew update
brew install --cask chromedriver
brew install portaudio
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

**Windows:**
```bash
pip install pyreadline3
# Instalar portaudio manualmente (vcpkg o binarios precompilados)
# Luego: pip install pyaudio
# Descargar ChromeDriver de https://sites.google.com/chromium.org/driver/
# Agregar al PATH del sistema
pip3 install -r requirements.txt
```

---

## Configuración

### Archivo `config.ini`

El archivo de configuración principal se encuentra en la raíz del proyecto:

```ini
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:14b
provider_server_address = 127.0.0.1:11434
agent_name = Jarvis
recover_last_session = False
save_session = False
speak = False
listen = False
work_dir = /ruta/a/tu/directorio
jarvis_personality = False
languages = en

[BROWSER]
headless_browser = True
stealth_mode = False
```

### Parámetros de Configuración

#### Sección [MAIN]

| Parámetro | Descripción | Valores |
|-----------|-------------|---------|
| `is_local` | Ejecutar LLM localmente | `True` / `False` |
| `provider_name` | Proveedor LLM a utilizar | Ver tabla de proveedores |
| `provider_model` | Modelo LLM específico | Depende del proveedor |
| `provider_server_address` | Dirección del servidor | IP:Puerto |
| `agent_name` | Nombre del asistente | Texto libre |
| `recover_last_session` | Recuperar sesión anterior | `True` / `False` |
| `save_session` | Guardar sesión actual | `True` / `False` |
| `speak` | Habilitar texto a voz | `True` / `False` |
| `listen` | Habilitar voz a texto | `True` / `False` |
| `work_dir` | Directorio de trabajo | Ruta absoluta |
| `jarvis_personality` | Personalidad JARVIS | `True` / `False` |
| `languages` | Idiomas soportados | ej: `en`, `en zh` |

#### Sección [BROWSER]

| Parámetro | Descripción | Valores |
|-----------|-------------|---------|
| `headless_browser` | Ejecutar navegador sin interfaz | `True` / `False` |
| `stealth_mode` | Modo sigiloso (evita detección) | `True` / `False` |

---

## Proveedores LLM

### Proveedores Locales

| Proveedor | Descripción |
|-----------|-------------|
| `ollama` | Ejecutar LLMs localmente con Ollama |
| `lm-studio` | Ejecutar LLMs localmente con LM Studio |
| `server` | Ejecutar LLM en un servidor remoto |
| `openai` | Usar API compatible con OpenAI (ej: llama.cpp) |

### Proveedores en la Nube

| Proveedor | Descripción | Variable de Entorno |
|-----------|-------------|---------------------|
| `openai` | ChatGPT API | `OPENAI_API_KEY` |
| `deepseek` | Deepseek API | `DEEPSEEK_API_KEY` |
| `google` | Google Gemini API | `GOOGLE_API_KEY` |
| `huggingface` | HuggingFace API | `HUGGINGFACE_API_KEY` |
| `together` | Together AI API | `TOGETHER_API_KEY` |
| `openrouter` | OpenRouter API | `OPENROUTER_API_KEY` |

### Configuración de Proveedor

**Ejemplo para Ollama (local):**
```ini
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:14b
provider_server_address = 127.0.0.1:11434
```

**Ejemplo para API externa:**
```ini
[MAIN]
is_local = False
provider_name = google
provider_model = gemini-2.0-flash
provider_server_address = 127.0.0.1:5000
```
Luego exportar la API key:
```bash
export GOOGLE_API_KEY="tu-api-key-aqui"
```

---

## Ejecución

### 1. Iniciar Servicios

```bash
# Linux/macOS
sudo ./start_services.sh

# Windows
start ./start_services.cmd
```

Esto inicia:
- SearxNG (motor de búsqueda)
- Redis (requerido por SearxNG)
- Frontend (interfaz web)

### 2. Ejecutar la Aplicación

**Modo CLI:**
```bash
python3 cli.py
```

**Modo Web:**
```bash
python3 api.py
# Acceder a http://localhost:3000/
```

---

## Configuración Avanzada

### Ejecutar LLM en Servidor Remoto

1. En el servidor:
```bash
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek/llm_server/
pip3 install -r requirements.txt
python3 app.py --provider ollama --port 3333
```

2. En el cliente (`config.ini`):
```ini
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:70b
provider_server_address = 192.168.x.x:3333
```

### Voz y Audio

**Habilitar Text-to-Speech:**
```ini
speak = True
```

**Habilitar Speech-to-Text:**
```ini
listen = True
```

El reconocimiento de voz usa el nombre del agente como palabra de activación. Ejemplo con `agent_name = Friday`:
- Di "Friday" para activar
- Tu consulta
- Confirma con "do it", "go ahead", etc.

---

## Solución de Problemas

### ChromeDriver Mismatch

Error: `session not created: This version of ChromeDriver only supports Chrome version XX`

Solución: Descargar ChromeDriver compatible desde:
- https://developer.chrome.com/docs/chromedriver/downloads
- Para Chrome 115+: https://googlechromelabs.github.io/chrome-for-testing/

### Error de Conexión con LM-Studio

Error: `No connection adapters were found for '127.0.0.1:11434/v1/chat/completions'`

Solución: Añadir `http://` al inicio de la dirección:
```ini
provider_server_address = http://127.0.0.1:1234
```

### SearxNG No Configurado

Error: `SearxNG base URL must be provided`

Solución:
```bash
export SEARXNG_BASE_URL="http://127.0.0.1:8080"
```

---

## Requisitos de Hardware

| Tamaño Modelo | VRAM GPU | Recomendación |
|---------------|----------|---------------|
| 7B | 8GB | No recomendado |
| 14B | 12GB (RTX 3060) | Usable para tareas simples |
| 32B | 24+GB (RTX 4090) | Bueno para la mayoría |
| 70B+ | 48+GB | Excelente |

---

## Contribuciones

Ver [CONTRIBUTING.md](./docs/CONTRIBUTING.md) para guía de contribuciones.

## Licencia

GPL-3.0 - Ver [LICENSE](./LICENSE)
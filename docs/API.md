# API Documentation - AgenticSeek

## Índice

1. [Información General](#información-general)
2. [Endpoints](#endpoints)
3. [Modelos de Datos](#modelos-de-datos)
4. [Proveedores LLM](#proveedores-llm)
5. [Configuración de Proveedores](#configuración-de-proveedores)
6. [CORS](#cors)

---

## Información General

La API de AgenticSeek está construida con FastAPI y corre en el puerto **8000** por defecto.

**URL Base:** `http://localhost:8000`

**Título:** AgenticSeek API

**Versión:** 0.1.0

---

## Endpoints

### Health Check

Verifica el estado de la API.

```
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

### Procesar Consulta

Envía una consulta al sistema de agentes.

```
POST /query
```

**Cuerpo de la Solicitud:**
```json
{
  "query": "Tu consulta aquí"
}
```

**Respuesta:**
```json
{
  "done": "true",
  "answer": "Respuesta del agente",
  "reasoning": "Razonamiento del modelo",
  "agent_name": "Planner",
  "success": "true",
  "blocks": {
    "0": {
      "tool_type": "web_search",
      "output": "Resultado de la búsqueda",
      "success": true
    }
  },
  "status": "Ready",
  "uid": "uuid-unico"
}
```

**Códigos de Estado:**
- `200`: Éxito
- `400`: Error en la consulta
- `429`: Otra consulta en proceso

---

### Obtener Última Respuesta

Obtiene la respuesta más reciente del agente.

```
GET /latest_answer
```

**Respuesta (si hay respuesta):**
```json
{
  "done": "false",
  "answer": "Respuesta actual",
  "reasoning": "Razonamiento",
  "agent_name": "Browser",
  "success": "true",
  "blocks": {},
  "status": "Thinking...",
  "uid": "uuid"
}
```

**Respuesta (si no hay respuesta):**
```json
{
  "error": "No answer available"
}
```

---

### Captura de Pantalla

Obtiene la captura de pantalla actual del navegador.

```
GET /screenshot
```

**Respuesta:**
- Archivo de imagen PNG
- Código `404` si no hay captura disponible

---

### Verificar Estado Activo

Verifica si hay una operación en curso.

```
GET /is_active
```

**Respuesta:**
```json
{
  "is_active": false
}
```

---

### Detener Operación

Detiene la operación actual en curso.

```
GET /stop
```

**Respuesta:**
```json
{
  "status": "stopped"
}
```

---

## Modelos de Datos

### QueryRequest

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `query` | string | La consulta del usuario |

### QueryResponse

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `done` | string | Estado de completitud ("true"/"false") |
| `answer` | string | Respuesta del agente |
| `reasoning` | string | Razonamiento del modelo |
| `agent_name` | string | Nombre del agente que procesó |
| `success` | string | Éxito de la operación |
| `blocks` | dict | Resultados de herramientas ejecutadas |
| `status` | string | Estado actual del agente |
| `uid` | string | Identificador único de la respuesta |

---

## Proveedores LLM

AgenticSeek soporta múltiples proveedores de LLM.

### Proveedores Locales

| Proveedor | Nombre en Config | Puerto Default | Descripción |
|-----------|------------------|----------------|-------------|
| Ollama | `ollama` | 11434 | Ejecutar LLMs localmente |
| LM Studio | `lm-studio` | 1234 | Interfaz local para LLMs |
| Server Remoto | `server` | configurable | LLM en servidor remoto |
| OpenAI Compatible | `openai` | configurable | API compatible con OpenAI |

### Proveedores en la Nube

| Proveedor | Nombre en Config | Variable de Entorno | Descripción |
|-----------|------------------|---------------------|-------------|
| OpenAI | `openai` | `OPENAI_API_KEY` | ChatGPT API |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | DeepSeek API |
| Google Gemini | `google` | `GOOGLE_API_KEY` | Google Gemini API |
| HuggingFace | `huggingface` | `HUGGINGFACE_API_KEY` | HuggingFace Inference API |
| Together AI | `together` | `TOGETHER_API_KEY` | Together AI API |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | Agregador de LLMs |

---

## Configuración de Proveedores

### Ollama (Local)

```ini
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:14b
provider_server_address = 127.0.0.1:11434
```

Iniciar Ollama:
```bash
ollama serve
```

Instalar modelo:
```bash
ollama pull deepseek-r1:14b
```

---

### LM Studio (Local)

```ini
[MAIN]
is_local = True
provider_name = lm-studio
provider_model = deepseek-r1-14b
provider_server_address = http://127.0.0.1:1234
```

**Nota:** Incluir `http://` en la dirección.

---

### Servidor Remoto

```ini
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:70b
provider_server_address = 192.168.1.100:3333
```

---

### OpenAI API

```ini
[MAIN]
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```

```bash
export OPENAI_API_KEY="tu-api-key"
```

---

### DeepSeek API

```ini
[MAIN]
is_local = False
provider_name = deepseek
provider_model = deepseek-chat
provider_server_address = 127.0.0.1:5000
```

```bash
export DEEPSEEK_API_KEY="tu-api-key"
```

---

### Google Gemini API

```ini
[MAIN]
is_local = False
provider_name = google
provider_model = gemini-2.0-flash
provider_server_address = 127.0.0.1:5000
```

```bash
export GOOGLE_API_KEY="tu-api-key"
```

---

### OpenRouter API

```ini
[MAIN]
is_local = False
provider_name = openrouter
provider_model = qwen/qwen3-coder-14b
provider_server_address = 127.0.0.1:5000
```

```bash
export OPENROUTER_API_KEY="tu-api-key"
```

---

### HuggingFace API

```ini
[MAIN]
is_local = False
provider_name = huggingface
provider_model = meta-llama/Llama-3.3-70B-Instruct
provider_server_address = 127.0.0.1:5000
```

```bash
export HUGGINGFACE_API_KEY="tu-api-key"
```

---

### Together AI API

```ini
[MAIN]
is_local = False
provider_name = together
provider_model = meta-llama/Llama-3.3-70B-Instruct
provider_server_address = 127.0.0.1:5000
```

```bash
export TOGETHER_API_KEY="tu-api-key"
```

---

## CORS

La API está configurada con los siguientes orígenes permitidos:

- `http://localhost`
- `http://localhost:3000`

---

## Notas Importantes

1. **Advertencia de Privacidad**: Al usar proveedores en la nube (no locales), los datos se envían a servidores externos.

2. **Recomendación**: Se recomienda usar modelos de razonamiento como DeepSeek R1 o Qwen para mejor rendimiento en navegación web y planificación de tareas.

3. **Rate Limiting**: El endpoint `/query` solo permite una solicitud a la vez. Retorna `429` si hay otra consulta en proceso.

4. **Sesiones**: La sesión se guarda automáticamente si `save_session = True` en `config.ini`.
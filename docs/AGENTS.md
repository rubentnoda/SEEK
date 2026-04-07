# Documentación de Agentes - AgenticSeek

## Índice

1. [概要](#概要)
2. [Agentes Disponibles](#agentes-disponibles)
3. [Sistema de Enrutamiento](#sistema-de-enrutamiento)
4. [Detalles de Cada Agente](#detalles-de-cada-agente)
5. [Herramientas Disponibles](#herramientas-disponibles)

---

## Resumen

AgenticSeek utiliza un sistema de múltiples agentes especializados que trabajan juntos para completar tareas complejas. El sistema selecciona automáticamente el agente apropiado basándose en la consulta del usuario.

### Tipos de Agentes

| Agente | Rol | Función Principal |
|--------|-----|------------------|
| CasualAgent | chat | Conversación casual |
| CoderAgent | code | Escritura y ejecución de código |
| FileAgent | files | Operaciones con archivos |
| BrowserAgent | web | Navegación web autónoma |
| PlannerAgent | planification | Planificación y coordinación de tareas |
| McpAgent | mcp | Integración con herramientas MCP |

---

## Agentes Disponibles

### 1. CasualAgent (Asistente Conversacional)

**Archivo:** `sources/agents/casual_agent.py`

**Propósito:** Manejar conversaciones casuales y consultas rápidas que no requieren herramientas específicas.

**Características:**
- Comunicación natural en lenguaje humano
- Respuestas contextuales
- No ejecuta operaciones complejas

**Prompt:** `prompts/base/casual_agent.txt` / `prompts/jarvis/casual_agent.txt`

**Cuándo usarlo:**
- Saludos y despedidas
- Preguntas generales
- Conversación informal

---

### 2. CoderAgent (Agente de Programación)

**Archivo:** `sources/agents/code_agent.py`

**Propósito:** Escribir, ejecutar y depurar código en múltiples lenguajes de programación.

**Características:**
- Soporte para Python, C, Go, Java, Bash
- Ejecución de código en sandbox
- Depuración automática
- Persistencia de memoria entre ejecuciones

**Herramientas:**
- PyInterpreter (Python)
- CInterpreter (C)
- GoInterpreter (Go)
- JavaInterpreter (Java)
- BashInterpreter (Bash/Shell)

**Prompt:** `prompts/base/coder_agent.txt` / `prompts/jarvis/coder_agent.txt`

**Cuándo usarlo:**
- "Crear un programa en Python que..."
- "Escribir un script para..."
- "Implementar una función en Go..."
- "Compilar y ejecutar código C"

---

### 3. FileAgent (Agente de Archivos)

**Archivo:** `sources/agents/file_agent.py`

**Propósito:** Gestionar archivos y directorios en el sistema local.

**Características:**
- Búsqueda de archivos
- Creación, lectura, escritura de archivos
- Renombrado y movimiento de archivos
- Listado de directorios
- Trabajo en directorio de trabajo configurado

**Herramientas:**
- FileFinder (búsqueda de archivos)
- BashInterpreter (operaciones de shell)

**Prompt:** `prompts/base/file_agent.txt` / `prompts/jarvis/file_agent.txt`

**Cuándo usarlo:**
- "Buscar archivos en la carpeta..."
- "Crear un archivo llamado..."
- "Renombrar archivos..."
- "Listar contenido de directorio..."

---

### 4. BrowserAgent (Agente de Navegación Web)

**Archivo:** `sources/agents/browser_agent.py`

**Propósito:** Navegar la web de forma autónoma para buscar y extraer información.

**Características:**
- Búsqueda web via SearxNG
- Navegación autónoma por páginas
- Extracción de información
- Llenado de formularios web
- Capturas de pantalla
- Historial de navegación

**Herramientas:**
- searxSearch (búsqueda en SearxNG)
- Browser (Selenium para navegación)

**Acciones del Agente:**
- SEARCH: Realizar búsqueda web
- NAVIGATE: Navegar a una URL
- GO_BACK: Volver a resultados anteriores
- FORM_FILLED: Completar formularios
- REQUEST_EXIT: Finalizar navegación

**Prompt:** `prompts/base/browser_agent.txt` / `prompts/jarvis/browser_agent.txt`

**Cuándo usarlo:**
- "Buscar información sobre..."
- "Navegar a un sitio web..."
- "Encontrar los mejores..."
- "Investigar empresas en..."

---

### 5. PlannerAgent (Agente Planificador)

**Archivo:** `sources/agents/planner_agent.py`

**Propósito:** Dividir tareas complejas en pasos y coordinar múltiples agentes para completarlas.

**Características:**
- Planificación de tareas en formato JSON
- Coordinación de múltiples agentes
- Paso de información entre agentes
- Replanificación automática en caso de errores
- Actualización dinámica del plan

**Agentes Coordinados:**
- CoderAgent (coder)
- FileAgent (file)
- BrowserAgent (web)
- CasualAgent (casual)

**Prompt:** `prompts/base/planner_agent.txt` / `prompts/jarvis/planner_agent.txt`

**Estructura del Plan:**

```json
{
  "plan": [
    {
      "agent": "Web",
      "id": "1",
      "need": null,
      "task": "Tarea a realizar"
    },
    {
      "agent": "File",
      "id": "2",
      "need": ["1"],
      "task": "Tarea que usa resultado del agente 1"
    }
  ]
}
```

**Cuándo usarlo:**
- Tareas multi-paso
- Investigación que requiere múltiples fuentes
- Tasks complejos que necesitan diferentes herramientas
- "Investigar X y luego crear un archivo con..."

---

### 6. McpAgent (Agente MCP)

**Billboard:** `sources/agents/mcp_agent.py`

**Propósito:** Integración con herramientas externas MCP (Model Context Protocol).

**Características:**
- Conexión a servidores MCP externos
- Ejecución de herramientas definidas en el servidor
- Extensibilidad através de protocolos MCP

**Prompt:** `prompts/base/mcp_agent.txt` / `prompts/jarvis/mcp_agent.txt`

---

## Sistema de Enrutamiento

### Selección Automática de Agentes

El sistema de enrutamiento determina automáticamente qué agente usar basándose en la consulta del usuario.

**Flujo de Selección:**

```
Consulta del Usuario
        |
        v
Router (sources/router.py)
        |
        v
Clasificación de Tarea
        |
        v
Selección de Agente
        |
        v
Procesamiento
```

### Clasificación de Tareas

| Palabras Clave | Agente Asignado |
|--------------|----------------|
| "buscar", "busqueda", "web", "navegar" | BrowserAgent |
| "codigo", "programa", "script", "python", "java", "crear" | CoderAgent |
| "archivo", "carpeta", "directorio", "buscar archivos" | FileAgent |
| Tarea compleja, múltiples pasos | PlannerAgent |
| Conversación simple | CasualAgent |

---

## Detalles de Cada Agente

### Clase Base: Agent

**Archivo:** `sources/agents/agent.py`

La clase `Agent` es la clase base de la cual heredan todos los agentes.

**Propiedades:**
- `agent_name`: Nombre del agente
- `role`: Rol (web, code, files, planification)
- `type`: Tipo de agente
- `memory`: Memoria conversacional
- `tools`: Herramientas disponibles
- `blocks_result`: Resultados de ejecuciones

**Métodos Principales:**
- `process(prompt, speech_module)`: Procesar una consulta
- `llm_request()`: Realizar solicitud al LLM
- `execute_modules(answer)`: Ejecutar herramientas
- `request_stop()`: Detener procesamiento

---

## Herramientas Disponibles

### Herramientas Web

| Herramienta | Descripción |
|-------------|-------------|
| searxSearch | Búsqueda web via SearxNG |
| webSearch | Búsqueda general en la web |

### Herramientas de Código

| Herramienta | Lenguaje | Descripción |
|------------|----------|-------------|
| PyInterpreter | Python | Ejecutar código Python |
| CInterpreter | C | Compilar y ejecutar C |
| GoInterpreter | Go | Ejecutar código Go |
| JavaInterpreter | Java | Compilar y ejecutar Java |
| BashInterpreter | Bash | Ejecutar comandos de shell |

### Herramientas de Archivos

| Herramienta | Descripción |
|-------------|-------------|
| FileFinder | Buscar archivos en el sistema |

### Utilidades

| Herramienta | Descripción |
|-------------|-------------|
| Tools | Framework general para herramientas |
| safety | Verificaciones de seguridad |

---

## Personalidades

AgenticSeek soporta dos personalidades:

### Base (Predeterminada)

Prompt: `prompts/base/`

Comportamiento: Enfocado en tareas, direto, eficiente.

### Jarvis

Prompt: `prompts/jarvis/`

Comportamiento: Estilo JARVIS de Iron Man, más conversacional y con personalidad definida.

**Activación en config.ini:**
```ini
[MAIN]
jarvis_personality = True
```

---

## Notas de Implementación

1. **Memoria**: Cada agente tiene su propia instancia de `Memory` para mantener contexto de la conversación.

2. **Bloques de Código**: Los agentes generan "bloques" de código que son ejecutados por las herramientas correspondientes.

3. **Expresión de Razonamiento**: Los modelos de razonamiento (como DeepSeek R1) incluyen bloques de razonamiento que son extraídos antes de procesar la respuesta.

4. **Manejo de Errores**: El PlannerAgent puede re-planificar automáticamente si un agente falla en su tarea.

5. **Session Recovery**: La recuperación de sesión está manejada por la clase `Interaction`, no por los agentes individualmente.
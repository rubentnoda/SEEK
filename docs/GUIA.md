# Guía de Uso - AgenticSeek

## Índice

1. [Inicio Rápido](#inicio-rápido)
2. [Interfaz de Línea de Comandos (CLI)](#interfaz-de-línea-de-comandos-cli)
3. [Interfaz Web](#interfaz-web)
4. [Ejemplos de Uso](#ejemplos-de-uso)
5. [Comandos de Voz](#comandos-de-voz)
6. [Gestión de Sesiones](#gestión-de-sesiones)

---

## Inicio Rápido

### 1. Activar el Entorno Virtual

```bash
source agentic_seek_env/bin/activate
```

### 2. Iniciar los Servicios

```bash
# Linux/macOS
sudo ./start_services.sh

# Windows
start ./start_services.cmd
```

### 3. Ejecutar AgenticSeek

**Opción A - CLI:**
```bash
python3 cli.py
```

**Opción B - Web:**
```bash
python3 api.py
# Abrir http://localhost:3000/ en el navegador
```

---

## Interfaz de Línea de Comandos (CLI)

Al ejecutar `python3 cli.py`, you'll see un prompt donde puedes escribir tus consultas.

### Comandos Especiales

| Comando | Descripción |
|---------|-------------|
| `goodbye` / `exit` | Salir de la aplicación |
| `help` | Mostrar ayuda |
| `restart` | Reiniciar la sesión |

### Flujo de Trabajo

1. Escribe tu consulta o tarea
2. El sistema automáticamente会选择 el agente apropiado
3. Observa el progreso en la terminal
4. Recibe la respuesta final

---

## Interfaz Web

La interfaz web está disponible en `http://localhost:3000/`.

### Características

- **Historial de Conversaciones**: Guarda tus interacciones previas
- **Capturas de Pantalla**: Ver el estado actual del navegador
- **Estado en Tiempo Real**: Monitorea el progreso de las tareas
- **Detener Tareas**: Botón para cancelar operaciones en curso

---

## Ejemplos de Uso

### Búsqueda Web

> *Buscar los mejores cafés en Rennes, Francia, y guardar una lista con sus direcciones en rennes_cafes.txt*

```
Request: Search the web for top cafes in Rennes, France, and save a list of three with their addresses in rennes_cafes.txt
```

### Programación

> *Crear un juego de serpiente en Python*

```
Request: Make a snake game in python!
```

> *Escribir un programa en Go para calcular el factorial*

```
Request: Write a Go program to calculate the factorial of a number, save it as factorial.go in your workspace
```

### Gestión de Archivos

> *Buscar archivos JPG en summer_pictures y renombrarlos con la fecha actual*

```
Request: Search my summer_pictures folder for all JPG files, rename them with today's date, and save a list of renamed files in photos_list.txt
```

### Tareas Complejas (Multi-Agente)

> *Investigar startups de IA en Osaka y Tokio, luego crear un archivo con los resultados*

```
Request: Search the web for AI startups in Osaka and Tokyo, then create a research file with the findings
```

> *Buscar una API de precios de acciones gratuita, registrar una cuenta, y crear un script para obtener precios de Tesla*

```
Request: Search the web for a free stock price API, register with my email, then write a Python script to fetch daily prices for Tesla
```

---

## Comandos de Voz

### Configuración

Para habilitar el reconocimiento de voz, configura en `config.ini`:

```ini
[MAIN]
listen = True
agent_name = Friday
```

### Cómo Usar

1. Habla el nombre del agente (ej: "Friday") para activar
2. Expresa tu consulta claramente
3. Usa una frase de confirmación para ejecutar:
   - "do it"
   - "go ahead"
   - "execute"
   - "run"
   - "start"
   - "thanks"
   - "please"

### Text-to-Speech

Para habilitar la voz del asistente:

```ini
[MAIN]
speak = True
```

---

## Gestión de Sesiones

### Guardar Sesión

```ini
[MAIN]
save_session = True
```

Guarda automáticamente el estado de la conversación.

### Recuperar Sesión

```ini
[MAIN]
recover_last_session = True
```

Carga la sesión anterior al iniciar.

---

## Recomendaciones

### Para Mejor Resultados

1. **Sé explícito en tus consultas**: En lugar de "¿Conoces buenos países para viajar solo?", usa "Haz una búsqueda web y encuentra los mejores países para viajar solo"

2. **Especifica el formato de salida**: "Guarda los resultados en un archivo llamado X"

3. **Para tareas complejas**: El PlannerAgent divide la tarea en pasos manejables

### Limitaciones Conocidas

- El llenado de formularios web está en fase experimental
- El reconocimiento de voz solo funciona en inglés actualmente
- Modelos pequeños (7B) pueden tener dificultades con planificación de tareas

---

## Solución de Problemas快速

### La aplicación no responde

1. Verificar que los servicios de Docker estén activos
2. Comprobar que el proveedor LLM esté ejecutándose
3. Reiniciar los servicios: `./start_services.sh`

### Error de conexión con el navegador

1. Verificar ChromeDriver instalado
2. Confirmar versión de Chrome compatible
3. Probar con `headless_browser = False` para debugging

### Sin respuesta del LLM

1. Verificar que Ollama/LM-Studio esté ejecutándose
2. Confirmar el modelo esté descargado
3. Revisar la configuración en `config.ini`

---

## Próximos Pasos

- Revisar [README.md](./README.md) para instalación detallada
- Consultar [API.md](./API.md) para documentación de endpoints
- Leer [AGENTS.md](./AGENTS.md) para entender los agentes disponibles
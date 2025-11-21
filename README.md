# FastEvents API 🎉

Sistema de gestión de eventos, usuarios e inscripciones con caché integrado.

## 📋 Descripción

FastEvents API es una API REST desarrollada con Flask que permite:
- Gestionar eventos (crear, listar, actualizar, eliminar)
- Administrar usuarios
- Registrar inscripciones de usuarios a eventos
- Sistema de caché en memoria para optimizar consultas

## 🏗️ Arquitectura

El proyecto sigue una arquitectura limpia y modular:

```
SistemeMiniEventos/
├── src/
│   ├── events/          # Módulo de eventos
│   ├── users/           # Módulo de usuarios
│   ├── attendance/      # Módulo de inscripciones
│   ├── cache/           # Sistema de caché
│   └── database/        # Conexión a BD
├── tests/               # Pruebas unitarias e integración
├── app.py              # Aplicación principal
└── requirements.txt    # Dependencias
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd SistemeMiniEventos
```

### 2. Crear entorno virtual (recomendado)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## ▶️ Ejecución

### Iniciar el servidor

```powershell
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📚 Endpoints de la API

### Eventos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/events` | Listar todos los eventos |
| POST | `/events` | Crear un nuevo evento |
| GET | `/events/{id}` | Obtener evento por ID |
| PUT | `/events/{id}` | Actualizar evento |
| DELETE | `/events/{id}` | Eliminar evento |

**Ejemplo - Crear evento:**
```json
POST /events
{
  "nombre": "Conferencia Tech 2025",
  "fecha": "2025-12-25",
  "capacidad": 100
}
```

### Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/users` | Listar todos los usuarios |
| POST | `/users` | Crear un nuevo usuario |
| GET | `/users/{id}` | Obtener usuario por ID |

**Ejemplo - Crear usuario:**
```json
POST /users
{
  "nombre": "Ana García",
  "email": "ana@example.com"
}
```

### Inscripciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/attendance` | Inscribir usuario a evento |

**Ejemplo - Inscribir usuario:**
```json
POST /attendance
{
  "userId": 1,
  "eventId": 5
}
```

## 🗄️ Base de Datos

El sistema utiliza **SQLite** con 3 tablas:

### Tabla `events`
- `id` INTEGER PRIMARY KEY
- `nombre` TEXT NOT NULL
- `fecha` TEXT NOT NULL
- `capacidad` INTEGER NOT NULL
- `inscritos` INTEGER DEFAULT 0

### Tabla `users`
- `id` INTEGER PRIMARY KEY
- `nombre` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL

### Tabla `attendance`
- `id` INTEGER PRIMARY KEY
- `user_id` INTEGER (FK → users)
- `event_id` INTEGER (FK → events)
- UNIQUE(user_id, event_id)

La base de datos se crea automáticamente al iniciar la aplicación: `fastevents.db`

## 💾 Sistema de Caché

El sistema implementa un caché en memoria para eventos:

**Funcionalidad:**
- Almacena el último evento consultado por ID
- Se invalida automáticamente cuando:
  - El evento se actualiza
  - El evento se elimina
  - Cambia la cantidad de inscritos

**Implementación:**
- Clase `CacheService` en `src/cache/cache_service.py`
- Integrado en `EventService`

## ✅ Reglas de Negocio

### Eventos
- ✅ No puede tener capacidad negativa
- ✅ No puede eliminarse si tiene inscritos

### Usuarios
- ✅ No se permiten correos repetidos

### Inscripciones
- ✅ No inscribir si el evento está lleno
- ✅ No inscribir si el usuario ya está inscrito
- ✅ Al inscribir: se incrementa el contador de inscritos

## 🧪 Pruebas

### Ejecutar todas las pruebas

```powershell
pytest
```

### Ejecutar con cobertura

```powershell
pytest --cov=src --cov-report=html
```

### Ejecutar pruebas específicas

```powershell
# Pruebas de eventos
pytest tests/test_event_service.py

# Pruebas de inscripciones
pytest tests/test_attendance_service.py

# Pruebas de caché
pytest tests/test_cache.py

# Pruebas de integración
pytest tests/test_integration.py
```

### Pruebas Implementadas

#### Pruebas Unitarias (3 archivos):

**`test_event_service.py`** (7 pruebas)
- ✅ Crear evento exitosamente
- ✅ No permitir capacidad negativa
- ✅ Obtener evento por ID
- ✅ Actualizar evento
- ✅ Eliminar evento sin inscritos
- ✅ No permitir eliminar evento con inscritos

**`test_attendance_service.py`** (6 pruebas)
- ✅ Inscribir usuario exitosamente
- ✅ No permitir doble inscripción
- ✅ No permitir inscripción en evento lleno
- ✅ No permitir inscribir usuario inexistente
- ✅ No permitir inscribir a evento inexistente
- ✅ Verificar incremento de inscritos

**`test_cache.py`** (6 pruebas)
- ✅ Almacenar y recuperar del caché
- ✅ Obtener clave inexistente
- ✅ Invalidar caché
- ✅ Limpiar caché completo
- ✅ Verificar existencia de clave
- ✅ Sobrescribir valor en caché

#### Pruebas de Integración (1 archivo):

**`test_integration.py`** (6 pruebas)
- ✅ Flujo completo: crear evento, usuario e inscribir
- ✅ Obtener lista de eventos
- ✅ Evento no encontrado (404)
- ✅ Actualizar evento
- ✅ No eliminar evento con inscritos
- ✅ Verificar funcionamiento del caché

**Total: 19 pruebas automatizadas**

## 📊 Ejemplos de Uso

### 1. Crear evento y usuario

```bash
# Crear evento
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Workshop Python","fecha":"2025-12-15","capacidad":30}'

# Crear usuario
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","email":"juan@test.com"}'
```

### 2. Inscribir usuario a evento

```bash
curl -X POST http://localhost:5000/attendance \
  -H "Content-Type: application/json" \
  -d '{"userId":1,"eventId":1}'
```

### 3. Consultar eventos

```bash
# Listar todos
curl http://localhost:5000/events

# Obtener por ID (usa caché)
curl http://localhost:5000/events/1
```

## 🛠️ Tecnologías Utilizadas

- **Flask 3.0.0** - Framework web
- **SQLite** - Base de datos
- **pytest 7.4.3** - Framework de pruebas
- **pytest-cov 4.1.0** - Cobertura de código

## 📝 Notas de Desarrollo

### Estructura Modular

Cada módulo (events, users, attendance) sigue el patrón:
- **Model**: Representa la entidad
- **Repository**: Acceso a datos (CRUD)
- **Service**: Lógica de negocio
- **Controller**: Endpoints HTTP

### Inyección de Dependencias

Los servicios reciben repositorios como dependencias, facilitando:
- Testing con mocks
- Flexibilidad para cambiar implementaciones
- Bajo acoplamiento

### Testing

Las pruebas usan bases de datos separadas (`test_*.db`) que se eliminan automáticamente después de cada ejecución.

## 🎯 Cumplimiento de Requerimientos

✅ API REST con endpoints claros
✅ Código modular y arquitectura limpia
✅ Base de datos con 3 tablas relacionadas
✅ Sistema de caché funcional
✅ 3+ pruebas unitarias (19 en total)
✅ Pruebas de integración
✅ README completo con documentación

## 👨‍💻 Autor

Proyecto desarrollado como ejercicio práctico de preparación para parcial.

## 📄 Licencia

Proyecto educativo - Uso libre para fines académicos.

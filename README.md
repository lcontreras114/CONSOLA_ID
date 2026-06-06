# 🔐 AUDITSA — Consola de Gestión de IDs

**AUDITSA Digital Audit** — Sistema de gestión de IDs de detección para broadcasting.

---

## ⚡ Inicio Rápido

### 1. Requisitos

- Python 3.10+
- Windows / macOS / Linux
- VS Code (recomendado)

### 2. Instalación

```bash
# Clona o descarga el proyecto
cd auditsa

# Crea entorno virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Instala dependencias
pip install -r requirements.txt
```

### 3. Configuración

```bash
# Copia el archivo de variables de entorno
cp .env.example .env
# Edita .env si necesitas cambiar SECRET_KEY u otras variables
```

### 4. Ejecutar

**Opción A — Windows doble clic:**
```
start.bat
```

**Opción B — Manual (dos terminales):**

Terminal 1 — Backend:
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — Frontend:
```bash
streamlit run frontend/app.py
```

Luego abre: **http://localhost:8501**

---

## 🏗️ Arquitectura

```
Streamlit Frontend
      ↓ HTTP (Bearer JWT)
FastAPI Backend
      ↓
Repository Layer
      ↓
Google Sheets (CSV público)
```

### Estructura del proyecto

```
auditsa/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Settings & env vars
│   ├── models/
│   │   └── __init__.py          # Pydantic models
│   ├── repositories/
│   │   ├── ids_repository.py    # Google Sheets IDs
│   │   ├── users_repository.py  # Google Sheets Usuarios + bcrypt
│   │   ├── channels_repository.py # Google Sheets Canales
│   │   └── audit_repository.py  # Auditoría + Historial
│   ├── services/
│   │   ├── auth_service.py      # JWT + autenticación
│   │   └── ids_service.py       # Lógica de negocio IDs
│   ├── routers/
│   │   ├── auth_router.py       # /auth/login, /logout, /me
│   │   ├── ids_router.py        # /ids/search, /new, /validate
│   │   ├── channels_router.py   # /canales/
│   │   ├── audit_router.py      # /audit/log, /history
│   │   └── users_router.py      # /users/
│   └── middleware/
│       └── auth_middleware.py   # JWT dependency injection
├── frontend/
│   ├── app.py                   # Streamlit entry point
│   ├── api_client.py            # HTTP client → FastAPI
│   ├── components/
│   │   ├── tab_buscar.py        # Tab 1: Buscar AAEE
│   │   ├── tab_nuevo_id.py      # Tab 2: Nuevo ID
│   │   ├── tab_canales.py       # Tab 3: IDs x Canal
│   │   └── tab_admin.py         # Tab 4: Admin Panel
│   └── utils/
│       ├── session.py           # Session state helpers
│       └── styles.py            # CSS + branding
├── assets/
│   └── logo.png
├── .streamlit/
│   └── config.toml              # Streamlit dark theme
├── .env.example
├── .gitignore
├── requirements.txt
├── start.bat                    # Windows launcher
└── README.md
```

---

## 🔑 Autenticación

- **JWT** con expiración configurable (default: 8 horas)
- **bcrypt** para contraseñas (compatible con texto plano legacy en Google Sheets)
- Cookies `HttpOnly`, `SameSite=Lax`
- Renovación automática vía `/auth/refresh`
- Logout real con limpieza de cookie

### Roles

| Rol | Permisos |
|-----|----------|
| `adm` | Todo: buscar, crear IDs, validar, admin panel, log |
| `regular` | Buscar + crear IDs (van a validación) |
| `capa` | Solo buscar |

---

## 📡 API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Login → JWT |
| POST | `/auth/logout` | Logout |
| GET | `/auth/me` | Usuario actual |
| GET | `/ids/search` | Buscar IDs |
| POST | `/ids/new` | Crear ID (pending) |
| GET | `/ids/pending` | IDs pendientes (ADM) |
| POST | `/ids/validate` | Validar/rechazar ID (ADM) |
| GET | `/canales/` | Lista de canales |
| GET | `/canales/mis-canales` | Canales del usuario |
| GET | `/canales/{canal}/info` | Info del canal |
| GET | `/canales/{canal}/ids` | IDs del canal |
| GET | `/audit/log` | Log de auditoría (ADM) |
| GET | `/audit/history` | Historial del usuario |
| POST | `/audit/history` | Agregar al historial |
| DELETE | `/audit/history` | Limpiar historial |

Documentación interactiva: **http://127.0.0.1:8000/docs**

---

## 🔒 Seguridad

- Cambiar `SECRET_KEY` en `.env` antes de producción
- En producción: activar `secure=True` en cookies (requiere HTTPS)
- Los orígenes CORS están restringidos al frontend local

---

## 📦 Deploy en la nube

Para desplegar en internet (Railway, Render, Fly.io):

1. Sube el repositorio a GitHub
2. Configura las variables de entorno del `.env` en la plataforma
3. Comando de inicio backend: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Para el frontend Streamlit: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`
5. Actualiza `BACKEND_URL` en `.env` con la URL pública del backend

---

## 🛠️ Desarrollado por

**AUDITSA Digital Audit** — Sistema interno de gestión de IDs.

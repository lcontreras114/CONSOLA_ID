"""
AUDITSA - Backend FastAPI
=========================
Run with:
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routers import auth_router, ids_router, channels_router, audit_router, users_router
from backend.config import APP_TITLE

app = FastAPI(
    title=APP_TITLE,
    version="2.0.0",
    description="API Backend para la Consola de IDs - AUDITSA Digital Audit",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Allow the Streamlit frontend (any localhost port during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(ids_router.router)
app.include_router(channels_router.router)
app.include_router(audit_router.router)
app.include_router(users_router.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "app": APP_TITLE}


@app.get("/", tags=["system"])
def root():
    return {"message": f"Bienvenido a {APP_TITLE} API v2.0"}

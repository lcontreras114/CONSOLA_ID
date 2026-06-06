import os
from dotenv import load_dotenv

load_dotenv()

# ── Google Sheets URLs ──────────────────────────────────────────────────────
SHEET_IDS_URL = os.getenv(
    "SHEET_IDS_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJNg51LW2DbTBSEOOSPOTHR0dc4xCF1lTZqLq_z_R9LkfMHO7CzyrI45eGhbApkyGtcBwX4ibmRtZd/pub?gid=1166538171&single=true&output=csv",
)
SHEET_CANALES_URL = os.getenv(
    "SHEET_CANALES_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJNg51LW2DbTBSEOOSPOTHR0dc4xCF1lTZqLq_z_R9LkfMHO7CzyrI45eGhbApkyGtcBwX4ibmRtZd/pub?gid=2126304715&single=true&output=csv",
)
SHEET_IDS_CANAL_URL = os.getenv(
    "SHEET_IDS_CANAL_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJNg51LW2DbTBSEOOSPOTHR0dc4xCF1lTZqLq_z_R9LkfMHO7CzyrI45eGhbApkyGtcBwX4ibmRtZd/pub?gid=1906691236&single=true&output=csv",
)
SHEET_USUARIOS_URL = os.getenv(
    "SHEET_USUARIOS_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJNg51LW2DbTBSEOOSPOTHR0dc4xCF1lTZqLq_z_R9LkfMHO7CzyrI45eGhbApkyGtcBwX4ibmRtZd/pub?gid=447315811&single=true&output=csv",
)
SHEET_USUARIO_CANAL_URL = os.getenv(
    "SHEET_USUARIO_CANAL_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJNg51LW2DbTBSEOOSPOTHR0dc4xCF1lTZqLq_z_R9LkfMHO7CzyrI45eGhbApkyGtcBwX4ibmRtZd/pub?gid=2019399218&single=true&output=csv",
)

# ── Security ────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "auditsa-super-secret-key-change-in-production-2024")
SESSION_EXPIRE_HOURS = int(os.getenv("SESSION_EXPIRE_HOURS", "8"))
ALGORITHM = "HS256"

# ── Fallback credentials (hashed at startup if present) ────────────────────
FALLBACK_USER = os.getenv("FALLBACK_USER", "LContreras")
FALLBACK_PASS = os.getenv("FALLBACK_PASS", "shanks1324")
FALLBACK_ROL  = os.getenv("FALLBACK_ROL", "adm")

# ── Cache TTL ───────────────────────────────────────────────────────────────
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))

# ── App ─────────────────────────────────────────────────────────────────────
APP_TITLE   = "Consola de IDs - AUDITSA"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

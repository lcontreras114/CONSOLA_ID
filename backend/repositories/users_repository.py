import pandas as pd
import bcrypt
import time
import threading
from typing import Optional, Tuple
from backend.config import SHEET_USUARIOS_URL, CACHE_TTL_SECONDS, FALLBACK_USER, FALLBACK_PASS, FALLBACK_ROL

_cache_df: Optional[pd.DataFrame] = None
_cache_ts: float = 0.0
_cache_lock = threading.Lock()

VALID_ROLES = {"adm", "regular", "capa"}

# Pre-hash the fallback password once at import time
_FALLBACK_HASH = bcrypt.hashpw(FALLBACK_PASS.encode(), bcrypt.gensalt()).decode()


def _load_from_sheets() -> pd.DataFrame:
    df = pd.read_csv(SHEET_USUARIOS_URL, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.upper()
    return df


def _get_df() -> pd.DataFrame:
    global _cache_df, _cache_ts
    with _cache_lock:
        now = time.time()
        if _cache_df is None or (now - _cache_ts) > CACHE_TTL_SECONDS:
            try:
                _cache_df = _load_from_sheets()
                _cache_ts = now
            except Exception:
                if _cache_df is None:
                    _cache_df = pd.DataFrame(columns=["USUARIO", "CONTRASEÑA", "RANGO"])
    return _cache_df.copy()


def verify_user(username: str, password: str) -> Tuple[bool, str]:
    """
    Returns (success, rol).
    Supports both plain-text passwords (legacy Google Sheets) and bcrypt hashes.
    Falls back to hardcoded credential if sheet is unavailable.
    """
    df = _get_df()

    if not df.empty and "USUARIO" in df.columns and "CONTRASEÑA" in df.columns:
        match = df[df["USUARIO"].astype(str).str.strip() == username.strip()]
        if not match.empty:
            row = match.iloc[0]
            stored = str(row.get("CONTRASEÑA", "")).strip()
            rol = str(row.get("RANGO", "")).lower().strip()

            if rol not in VALID_ROLES:
                return False, ""

            # Support bcrypt hash (starts with $2b$) or legacy plain text
            try:
                if stored.startswith("$2b$"):
                    ok = bcrypt.checkpw(password.encode(), stored.encode())
                else:
                    # Legacy plain text comparison (still supported for existing sheets)
                    ok = stored == password
            except Exception:
                ok = False

            return ok, rol

    # Fallback credentials
    if username == FALLBACK_USER and password == FALLBACK_PASS:
        return True, FALLBACK_ROL

    return False, ""


def get_all_users() -> list:
    """Return list of user dicts (without passwords)."""
    df = _get_df()
    if df.empty:
        return []
    result = []
    for _, row in df.iterrows():
        result.append({
            "usuario": str(row.get("USUARIO", "")).strip(),
            "rol": str(row.get("RANGO", "")).lower().strip(),
        })
    return result


def hash_password(plain: str) -> str:
    """Utility: hash a plain password with bcrypt."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

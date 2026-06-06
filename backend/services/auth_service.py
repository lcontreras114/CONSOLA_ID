"""
Auth Service
------------
Handles JWT creation/verification and session cookie helpers.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
from backend.config import SECRET_KEY, ALGORITHM, SESSION_EXPIRE_HOURS
from backend.repositories import users_repository, audit_repository


def create_access_token(username: str, rol: str) -> Tuple[str, int]:
    """Returns (token, expires_in_seconds)."""
    expire = datetime.utcnow() + timedelta(hours=SESSION_EXPIRE_HOURS)
    expires_in = SESSION_EXPIRE_HOURS * 3600
    payload = {
        "sub": username,
        "rol": rol,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expires_in


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT. Returns payload dict or None on failure."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login(username: str, password: str, ip: str = "") -> Optional[dict]:
    """
    Authenticate user.
    Returns dict with token info or None if auth fails.
    """
    ok, rol = users_repository.verify_user(username, password)
    if not ok:
        audit_repository.log_event(username, "LOGIN_FAILED", f"IP:{ip}", ip)
        return None

    token, expires_in = create_access_token(username, rol)
    audit_repository.log_event(username, "LOGIN", f"rol={rol}", ip)
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": username,
        "rol": rol,
        "expires_in": expires_in,
    }


def logout(username: str, ip: str = ""):
    audit_repository.log_event(username, "LOGOUT", "", ip)


def get_current_user(token: str) -> Optional[dict]:
    """Extract user info from token. Returns None if invalid/expired."""
    payload = decode_token(token)
    if payload is None:
        return None
    return {
        "username": payload.get("sub"),
        "rol": payload.get("rol"),
    }

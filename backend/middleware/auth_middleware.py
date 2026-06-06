"""
Auth Middleware
---------------
FastAPI dependency that validates the JWT token from the
Authorization header OR from the session cookie.
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.services.auth_service import get_current_user

security = HTTPBearer(auto_error=False)


def _extract_token(request: Request, credentials: Optional[HTTPAuthorizationCredentials]) -> Optional[str]:
    """Try Bearer header first, then fall back to cookie."""
    if credentials and credentials.credentials:
        return credentials.credentials
    # Cookie fallback
    return request.cookies.get("auditsa_token")


def get_token_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    Returns the current authenticated user dict {username, rol}.
    Raises 401 if invalid/missing.
    """
    token = _extract_token(request, credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Por favor, inicia sesión.",
        )
    user = get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión expirada o token inválido.",
        )
    return user


def require_adm(user: dict = Depends(get_token_user)) -> dict:
    if user.get("rol") != "adm":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores.",
        )
    return user


def require_regular_or_adm(user: dict = Depends(get_token_user)) -> dict:
    if user.get("rol") not in ("adm", "regular"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido.",
        )
    return user

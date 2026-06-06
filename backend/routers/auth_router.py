from fastapi import APIRouter, Response, Request, HTTPException, status, Depends
from backend.models import LoginRequest, TokenResponse
from backend.services import auth_service
from backend.middleware.auth_middleware import get_token_user
from backend.config import SESSION_EXPIRE_HOURS

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE_NAME = "auditsa_token"
COOKIE_MAX_AGE = SESSION_EXPIRE_HOURS * 3600


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, response: Response):
    ip = request.client.host if request.client else ""
    result = auth_service.login(body.username, body.password, ip=ip)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
        )
    # Set HttpOnly, SameSite=Lax cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=result["access_token"],
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=False,  # Set True in production with HTTPS
    )
    return TokenResponse(**result)


@router.post("/logout")
def logout(request: Request, response: Response, user: dict = Depends(get_token_user)):
    ip = request.client.host if request.client else ""
    auth_service.logout(user["username"], ip=ip)
    response.delete_cookie(COOKIE_NAME)
    return {"message": "Sesión cerrada correctamente."}


@router.get("/me")
def me(user: dict = Depends(get_token_user)):
    return user


@router.post("/refresh")
def refresh(user: dict = Depends(get_token_user), response: Response = None):
    """Issue a fresh token with a new expiry."""
    from backend.services.auth_service import create_access_token
    token, expires_in = create_access_token(user["username"], user["rol"])
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"],
        "rol": user["rol"],
        "expires_in": expires_in,
    }

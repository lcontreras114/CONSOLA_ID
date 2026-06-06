from fastapi import APIRouter, Depends, HTTPException
from backend.repositories import channels_repository
from backend.middleware.auth_middleware import get_token_user

router = APIRouter(prefix="/canales", tags=["canales"])


@router.get("/")
def get_canales(user: dict = Depends(get_token_user)):
    return {"canales": channels_repository.get_all_canal_names()}


@router.get("/mis-canales")
def mis_canales(user: dict = Depends(get_token_user)):
    assigned = channels_repository.get_canales_for_user(user["username"])
    # Validate they exist in the canales list
    all_names = channels_repository.get_all_canal_names()
    valid = [c for c in assigned if c in all_names]
    return {"canales": valid}


@router.get("/{canal}/info")
def canal_info(canal: str, user: dict = Depends(get_token_user)):
    info = channels_repository.get_canal_info(canal)
    if info is None:
        raise HTTPException(status_code=404, detail=f"Canal '{canal}' no encontrado.")
    return info


@router.get("/{canal}/ids")
def canal_ids(canal: str, user: dict = Depends(get_token_user)):
    return {"ids": channels_repository.get_ids_for_canal(canal)}

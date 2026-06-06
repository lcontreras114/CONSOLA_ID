from fastapi import APIRouter, Depends
from backend.repositories import users_repository
from backend.middleware.auth_middleware import require_adm, get_token_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users(user: dict = Depends(require_adm)):
    return {"users": users_repository.get_all_users()}

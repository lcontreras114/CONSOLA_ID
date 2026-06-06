from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from backend.repositories import audit_repository
from backend.middleware.auth_middleware import get_token_user, require_adm

router = APIRouter(prefix="/audit", tags=["audit"])


# ── Audit Log (ADM only) ──────────────────────────────────────────────────

@router.get("/log")
def get_audit_log(
    limit: int = Query(200, le=1000),
    user: dict = Depends(require_adm),
):
    return {"log": audit_repository.get_audit_log(limit=limit)}


# ── Per-user history ──────────────────────────────────────────────────────

@router.get("/history")
def get_history(user: dict = Depends(get_token_user)):
    return {"items": audit_repository.get_history(user["username"])}


@router.post("/history")
def add_history(item: dict, user: dict = Depends(get_token_user)):
    audit_repository.add_history_item(user["username"], item)
    audit_repository.log_event(user["username"], "COPIAR_ID", f"ID={item.get('id','')}")
    return {"ok": True}


@router.delete("/history")
def clear_history(user: dict = Depends(get_token_user)):
    audit_repository.clear_history(user["username"])
    return {"ok": True}


@router.delete("/history/{id_value}")
def remove_history_item(id_value: str, user: dict = Depends(get_token_user)):
    audit_repository.remove_history_item(user["username"], id_value)
    return {"ok": True}

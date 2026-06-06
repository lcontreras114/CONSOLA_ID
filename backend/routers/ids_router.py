from fastapi import APIRouter, Request, Depends, HTTPException, Query
from typing import List, Optional
from backend.models import NuevoIDRequest, ValidarIDRequest, SearchRequest
from backend.services import ids_service
from backend.middleware.auth_middleware import get_token_user, require_adm, require_regular_or_adm

router = APIRouter(prefix="/ids", tags=["ids"])


@router.get("/search")
def search_ids(
    q: Optional[str] = Query("", description="Texto libre de búsqueda"),
    tipos: Optional[List[str]] = Query(None, description="Lista de tipos cortos"),
    rtc: Optional[bool] = Query(False),
    user: dict = Depends(get_token_user),
):
    results = ids_service.search_ids(query=q, tipos_cortos=tipos or [], rtc=rtc)
    return {"results": results, "total": len(results)}


@router.get("/pending")
def get_pending(user: dict = Depends(require_adm)):
    return {"pending": ids_service.get_pending_ids()}


@router.post("/new")
def create_id(
    body: NuevoIDRequest,
    request: Request,
    user: dict = Depends(require_regular_or_adm),
):
    ip = request.client.host if request.client else ""
    try:
        result = ids_service.create_id(body.model_dump(), user["username"], ip=ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "ID enviado a validación.", "record": result}


@router.post("/validate")
def validate_id(
    body: ValidarIDRequest,
    request: Request,
    user: dict = Depends(require_adm),
):
    ip = request.client.host if request.client else ""
    ok = ids_service.validate_id(
        body.id_deteccion, body.accion, body.comentario or "", user["username"], ip=ip
    )
    if not ok:
        raise HTTPException(status_code=404, detail="ID no encontrado en pendientes.")
    return {"message": f"ID {body.id_deteccion} procesado ({body.accion})."}


@router.get("/distinct/{column}")
def distinct_values(column: str, user: dict = Depends(get_token_user)):
    allowed = {"Compañía", "Marca", "Submarca", "Producto", "VersiOn", "Tipo"}
    if column not in allowed:
        raise HTTPException(status_code=400, detail="Columna no permitida.")
    return {"values": ids_service.get_distinct_values(column)}

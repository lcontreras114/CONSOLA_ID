from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Rol(str, Enum):
    adm = "adm"
    regular = "regular"
    capa = "capa"


class EstadoID(str, Enum):
    pendiente = "PENDIENTE"
    validado = "VALIDADO"
    rechazado = "RECHAZADO"
    confiable = "Confiable"
    no_validado = "NO VALIDADO"


# ── Auth ─────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    rol: str
    expires_in: int  # seconds


class UserInfo(BaseModel):
    username: str
    rol: str


# ── IDs ──────────────────────────────────────────────────────────────────────

class IDRecord(BaseModel):
    compania: str = Field("", alias="Compañía")
    marca: str = Field("", alias="Marca")
    submarca: str = Field("", alias="Submarca")
    producto: str = Field("", alias="Producto")
    version: str = Field("", alias="VersiOn")
    tipo: str = Field("", alias="Tipo")
    id_deteccion: str = Field("", alias="ID")
    estado: str = Field("Confiable", alias="Estado")

    class Config:
        populate_by_name = True


class NuevoIDRequest(BaseModel):
    compania: str
    marca: str
    submarca: Optional[str] = ""
    producto: Optional[str] = ""
    version: Optional[str] = ""
    tipo: Optional[str] = ""
    id_deteccion: str


class ValidarIDRequest(BaseModel):
    id_deteccion: str
    accion: str  # "validar" | "rechazar"
    comentario: Optional[str] = ""


# ── Canales ──────────────────────────────────────────────────────────────────

class CanalRecord(BaseModel):
    canal: str = ""
    station_id: str = ""
    tag_autopromos: str = ""
    grilla_web: str = ""
    server: str = ""


class IDCanalRecord(BaseModel):
    canal: str = ""
    codigo_hash: str = ""
    tipo: str = ""
    descripcion: str = ""
    id_value: str = ""


# ── Usuarios ─────────────────────────────────────────────────────────────────

class UsuarioRecord(BaseModel):
    usuario: str
    rol: str


class UsuarioCanalRecord(BaseModel):
    usuario: str
    canal: str


# ── Auditoría ────────────────────────────────────────────────────────────────

class AuditEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    username: str
    accion: str
    detalle: Optional[str] = ""
    ip: Optional[str] = ""


# ── Historial ────────────────────────────────────────────────────────────────

class HistorialItem(BaseModel):
    id: str
    desc: str
    version: str = ""
    tipo: str = ""
    count: int = 1
    timestamp: Optional[str] = ""


class HistorialResponse(BaseModel):
    items: List[HistorialItem]


# ── Search ───────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: Optional[str] = ""
    tipos: Optional[List[str]] = []
    rtc: Optional[bool] = False


class SearchResponse(BaseModel):
    results: List[IDRecord]
    total: int

"""
IDs Service
-----------
Business logic for creating, searching, and validating IDs.
"""

import re
from typing import Optional
from backend.repositories import ids_repository, audit_repository


TIPO_MAP = {
    "MENCION": "MENCIÓN",
    "SUPERIMPO": "SUPERIMPOSICION",
    "VIRTUAL": "VIRTUAL",
    "RTC": "RTC",
    "PATROCINIO": "PATROCINIO",
    "B.PATROCINADO": "BLOQUE PATROCINADO",
    "F. DE GOL": "FESTEJO DE GOL",
    "MULTIPATRO": "MULTIPATROCINIO",
    "I.ACTIVA": "I. ACTIVA",
    "I.AMBIENTAL": "I. AMBIENTAL",
    "C. COMERCIAL": "CORTINILLA COMERCIAL",
    "A.ESPECIAL": "ACCIÓN ESPECIAL",
}

# Reverse map: full name → short key
TIPO_MAP_REV = {v: k for k, v in TIPO_MAP.items()}


def search_ids(query: str = "", tipos_cortos: list = None, rtc: bool = False) -> list:
    """
    Search IDs. Accepts short tipo keys (from the filter matrix) and translates them.
    Returns list of dicts.
    """
    tipos_largos = []
    if tipos_cortos:
        for t in tipos_cortos:
            if t in TIPO_MAP:
                tipos_largos.append(TIPO_MAP[t])
            else:
                tipos_largos.append(t)

    df = ids_repository.search_ids(query=query, tipos=tipos_largos, rtc=rtc)
    return df.to_dict(orient="records")


def create_id(record: dict, username: str, ip: str = "") -> dict:
    """
    Validate and enqueue a new ID for admin review.
    Raises ValueError on validation failure.
    """
    id_value = str(record.get("id_deteccion", "")).strip()

    if not re.match(r"^\d{8}$", id_value):
        raise ValueError("El ID debe contener exactamente 8 dígitos numéricos.")

    if not record.get("compania") or not record.get("marca"):
        raise ValueError("Compañía y Marca son obligatorios.")

    new_entry = {
        "Compañía": record.get("compania", ""),
        "Marca": record.get("marca", ""),
        "Submarca": record.get("submarca", ""),
        "Producto": record.get("producto", ""),
        "VersiOn": record.get("version", ""),
        "Tipo": record.get("tipo", ""),
        "ID": id_value,
        "Estado": "PENDIENTE",
        "creado_por": username,
    }

    ids_repository.add_pending_id(new_entry)
    audit_repository.log_event(username, "CREAR_ID", f"ID={id_value} Marca={record.get('marca','')}", ip)

    return new_entry


def validate_id(id_deteccion: str, accion: str, comentario: str, username: str, ip: str = "") -> bool:
    """Admin validates or rejects a pending ID."""
    ok = ids_repository.validate_pending_id(id_deteccion, accion)
    if ok:
        evento = "VALIDAR_ID" if accion == "validar" else "RECHAZAR_ID"
        audit_repository.log_event(
            username, evento, f"ID={id_deteccion} comentario={comentario}", ip
        )
    return ok


def get_pending_ids() -> list:
    return ids_repository.get_pending_ids()


def get_distinct_values(column: str) -> list:
    return ids_repository.get_distinct_values(column)

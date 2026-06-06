import pandas as pd
import time
import threading
from typing import Optional, List
from backend.config import SHEET_IDS_URL, CACHE_TTL_SECONDS

# ── In-memory store for new IDs (pending validation) ──────────────────────
_pending_lock = threading.Lock()
_pending_ids: List[dict] = []

# ── Cache ──────────────────────────────────────────────────────────────────
_cache_df: Optional[pd.DataFrame] = None
_cache_ts: float = 0.0
_cache_lock = threading.Lock()

COLUMN_MAP = {
    "COMPAÑIA": "Compañía", "COMPAÑÍA": "Compañía",
    "MARCA": "Marca", "SUBMARCA": "Submarca", "PRODUCTO": "Producto",
    "SUB TIPO DE SPOT": "Tipo", "SUBTIPO DE SPOT": "Tipo",
    "VERSION": "VersiOn", "VERSIÓN": "VersiOn",
    "ID DETECCION": "ID", "ID DETECCIÓN": "ID", "ID": "ID",
    "VERIFICACION": "Estado", "VERIFICACIÓN": "Estado", "ESTADO": "Estado",
}


def _load_from_sheets() -> pd.DataFrame:
    """Fetch and normalize the IDs sheet from Google Sheets."""
    df = pd.read_csv(SHEET_IDS_URL, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.upper()
    df = df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns})

    if "ID" in df.columns:
        df["ID"] = (
            df["ID"].astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.replace("nan", "", regex=False)
            .str.strip()
        )

    if "Estado" not in df.columns:
        df["Estado"] = "Confiable"

    # Deduplicate: keep first ID per key group
    key_cols = [c for c in ["Compañía", "Marca", "Submarca", "Producto", "VersiOn", "Tipo"] if c in df.columns]
    if key_cols and "ID" in df.columns:
        df["ID"] = df.groupby(key_cols)["ID"].transform("first")
        df = df.drop_duplicates(subset=key_cols).reset_index(drop=True)

    return df


def _get_base_df() -> pd.DataFrame:
    global _cache_df, _cache_ts
    with _cache_lock:
        now = time.time()
        if _cache_df is None or (now - _cache_ts) > CACHE_TTL_SECONDS:
            try:
                _cache_df = _load_from_sheets()
                _cache_ts = now
            except Exception as e:
                if _cache_df is None:
                    _cache_df = pd.DataFrame()
    return _cache_df.copy()


def invalidate_cache():
    global _cache_df, _cache_ts
    with _cache_lock:
        _cache_df = None
        _cache_ts = 0.0


def get_all_ids() -> pd.DataFrame:
    """Return base + pending IDs merged."""
    base = _get_base_df()
    with _pending_lock:
        if _pending_ids:
            pending_df = pd.DataFrame(_pending_ids)
            return pd.concat([pending_df, base], ignore_index=True)
    return base


def search_ids(query: str = "", tipos: list = None, rtc: bool = False) -> pd.DataFrame:
    df = get_all_ids()
    if df.empty:
        return df

    if query:
        search_cols = [c for c in ["Compañía", "Marca", "Submarca", "Producto", "VersiOn", "ID"] if c in df.columns]
        mask = df[search_cols].astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        df = df[mask]

    if rtc:
        df = df[df.get("VersiOn", pd.Series(dtype=str)).astype(str).str.contains("RTC CLASIFICACION", case=False, na=False)]

    if tipos:
        df = df[df.get("Tipo", pd.Series(dtype=str)).astype(str).str.upper().str.strip().isin(tipos)]

    return df.reset_index(drop=True)


def add_pending_id(record: dict):
    """Add a new ID to the pending in-memory list (awaiting admin validation)."""
    with _pending_lock:
        # Prevent duplicates
        existing = [p["ID"] for p in _pending_ids]
        if record.get("ID") and record["ID"] in existing:
            raise ValueError(f"ID {record['ID']} ya existe en pendientes.")
        # Also check base
        base = _get_base_df()
        if not base.empty and "ID" in base.columns:
            if record.get("ID") in base["ID"].values:
                raise ValueError(f"ID {record['ID']} ya existe en la base principal.")
        _pending_ids.append(record)


def get_pending_ids() -> List[dict]:
    with _pending_lock:
        return list(_pending_ids)


def validate_pending_id(id_deteccion: str, accion: str) -> bool:
    """Promote or reject a pending ID."""
    global _cache_df
    with _pending_lock:
        idx = next((i for i, p in enumerate(_pending_ids) if p.get("ID") == id_deteccion), None)
        if idx is None:
            return False
        record = _pending_ids.pop(idx)

    if accion == "validar":
        record["Estado"] = "Confiable"
        with _cache_lock:
            if _cache_df is not None:
                new_row = pd.DataFrame([record])
                _cache_df = pd.concat([new_row, _cache_df], ignore_index=True)
    # If rechazar, just remove from pending (already done above)
    return True


def get_distinct_values(column: str) -> list:
    df = get_all_ids()
    if column in df.columns:
        return sorted(df[column].dropna().astype(str).unique().tolist())
    return []

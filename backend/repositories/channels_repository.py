import pandas as pd
import time
import threading
from typing import Optional
from backend.config import SHEET_CANALES_URL, SHEET_IDS_CANAL_URL, SHEET_USUARIO_CANAL_URL, CACHE_TTL_SECONDS

# ── Canales cache ─────────────────────────────────────────────────────────
_cache_canales: Optional[pd.DataFrame] = None
_cache_ids_canal: Optional[pd.DataFrame] = None
_cache_usuario_canal: Optional[pd.DataFrame] = None
_cache_ts: float = 0.0
_cache_lock = threading.Lock()


def _load_all():
    global _cache_canales, _cache_ids_canal, _cache_usuario_canal, _cache_ts

    df_canales = pd.read_csv(SHEET_CANALES_URL, encoding="utf-8-sig")
    df_canales.columns = df_canales.columns.str.strip()

    df_ids_canal = pd.read_csv(SHEET_IDS_CANAL_URL, encoding="utf-8-sig")
    df_ids_canal.columns = df_ids_canal.columns.str.strip().str.upper()
    if "ID" in df_ids_canal.columns:
        df_ids_canal["ID"] = (
            df_ids_canal["ID"].astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.replace("nan", "", regex=False)
            .str.strip()
        )

    df_uc = pd.read_csv(SHEET_USUARIO_CANAL_URL, encoding="utf-8-sig")
    df_uc.columns = df_uc.columns.str.strip().str.upper()

    _cache_canales = df_canales
    _cache_ids_canal = df_ids_canal
    _cache_usuario_canal = df_uc
    _cache_ts = time.time()


def _ensure_cache():
    global _cache_canales, _cache_ts
    with _cache_lock:
        now = time.time()
        if _cache_canales is None or (now - _cache_ts) > CACHE_TTL_SECONDS:
            try:
                _load_all()
            except Exception as e:
                if _cache_canales is None:
                    _cache_canales = pd.DataFrame()
                if _cache_ids_canal is None:
                    _cache_ids_canal = pd.DataFrame()
                if _cache_usuario_canal is None:
                    _cache_usuario_canal = pd.DataFrame()


def get_all_canales() -> pd.DataFrame:
    _ensure_cache()
    return _cache_canales.copy()


def get_canal_info(canal: str) -> Optional[dict]:
    df = get_all_canales()
    if df.empty or "CANAL" not in df.columns:
        return None
    match = df[df["CANAL"] == canal]
    if match.empty:
        return None

    row = match.iloc[0]

    def gv(col):
        for k in row.index:
            if str(k).strip().lower() == str(col).strip().lower():
                val = str(row[k]).replace("nan", "N/A").strip()
                return val
        return "N/A"

    station_id = gv("stationid")
    tag_auto = gv("tag de autopromos")
    grilla = gv("grilla web /dish")
    server = gv("server")

    return {
        "canal": canal,
        "station_id": station_id,
        "tag_autopromos": tag_auto,
        "grilla": grilla,
        "server": server,
    }


def get_ids_for_canal(canal: str) -> list:
    _ensure_cache()
    df = _cache_ids_canal.copy()
    if df.empty or "CANAL" not in df.columns:
        return []

    ids_c = df[df["CANAL"] == canal]
    results = []
    for _, row in ids_c.iterrows():
        results.append({
            "canal": canal,
            "codigo_hash": str(row.get("CODIGO HASH", "")),
            "tipo": str(row.get("TIPO", "")),
            "descripcion": str(row.get("DESCRIPCION", "")),
            "id_value": str(row.get("ID", "")).split(".")[0],
        })
    return results


def get_canales_for_user(username: str) -> list:
    _ensure_cache()
    df = _cache_usuario_canal.copy()
    if df.empty or "USUARIO" not in df.columns or "CANAL" not in df.columns:
        return []

    user_upper = username.strip().upper()
    canales_df = df[df["USUARIO"].astype(str).str.strip().str.upper() == user_upper]
    return canales_df["CANAL"].dropna().unique().tolist()


def get_all_canal_names() -> list:
    df = get_all_canales()
    if df.empty or "CANAL" not in df.columns:
        return []
    return sorted(df["CANAL"].dropna().unique().tolist())

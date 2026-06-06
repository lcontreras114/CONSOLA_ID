"""
API Client
----------
All HTTP calls from Streamlit to the FastAPI backend go through here.
Reads the token from st.session_state.token and sends it as Bearer header.
"""

import requests
import streamlit as st
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # reuse config

BASE = BACKEND_URL.rstrip("/")
TIMEOUT = 10


def _headers() -> dict:
    token = st.session_state.get("token", "")
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _handle(resp: requests.Response) -> dict:
    try:
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        try:
            detail = resp.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"Error {resp.status_code}: {detail}")
        return {}
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return {}


# ── Auth ──────────────────────────────────────────────────────────────────────

def login(username: str, password: str) -> dict:
    try:
        r = requests.post(
            f"{BASE}/auth/login",
            json={"username": username, "password": password},
            timeout=TIMEOUT,
        )
        return _handle(r)
    except Exception as e:
        st.error(f"No se pudo conectar con el backend: {e}")
        return {}


def logout_api() -> dict:
    try:
        r = requests.post(f"{BASE}/auth/logout", headers=_headers(), timeout=TIMEOUT)
        return _handle(r)
    except Exception:
        return {}


def get_me() -> dict:
    try:
        r = requests.get(f"{BASE}/auth/me", headers=_headers(), timeout=TIMEOUT)
        return _handle(r)
    except Exception:
        return {}


# ── IDs ───────────────────────────────────────────────────────────────────────

def search_ids(query: str = "", tipos: list = None, rtc: bool = False) -> dict:
    params = {"q": query, "rtc": str(rtc).lower()}
    if tipos:
        params["tipos"] = tipos
    try:
        r = requests.get(
            f"{BASE}/ids/search",
            headers=_headers(),
            params=params,
            timeout=TIMEOUT,
        )
        return _handle(r)
    except Exception as e:
        st.error(f"Error buscando IDs: {e}")
        return {}


def get_pending_ids() -> dict:
    try:
        r = requests.get(f"{BASE}/ids/pending", headers=_headers(), timeout=TIMEOUT)
        return _handle(r)
    except Exception:
        return {}


def create_id(payload: dict) -> dict:
    try:
        r = requests.post(f"{BASE}/ids/new", headers=_headers(), json=payload, timeout=TIMEOUT)
        return _handle(r)
    except Exception as e:
        st.error(f"Error creando ID: {e}")
        return {}


def validate_id(id_deteccion: str, accion: str, comentario: str = "") -> dict:
    try:
        r = requests.post(
            f"{BASE}/ids/validate",
            headers=_headers(),
            json={"id_deteccion": id_deteccion, "accion": accion, "comentario": comentario},
            timeout=TIMEOUT,
        )
        return _handle(r)
    except Exception as e:
        st.error(f"Error validando ID: {e}")
        return {}


def get_distinct_values(column: str) -> list:
    try:
        r = requests.get(
            f"{BASE}/ids/distinct/{column}", headers=_headers(), timeout=TIMEOUT
        )
        data = _handle(r)
        return data.get("values", [])
    except Exception:
        return []


# ── Canales ───────────────────────────────────────────────────────────────────

def get_all_canales() -> list:
    try:
        r = requests.get(f"{BASE}/canales/", headers=_headers(), timeout=TIMEOUT)
        return _handle(r).get("canales", [])
    except Exception:
        return []


def get_mis_canales() -> list:
    try:
        r = requests.get(f"{BASE}/canales/mis-canales", headers=_headers(), timeout=TIMEOUT)
        return _handle(r).get("canales", [])
    except Exception:
        return []


def get_canal_info(canal: str) -> dict:
    try:
        r = requests.get(
            f"{BASE}/canales/{requests.utils.quote(canal, safe='')}/info",
            headers=_headers(),
            timeout=TIMEOUT,
        )
        return _handle(r)
    except Exception:
        return {}


def get_canal_ids(canal: str) -> list:
    try:
        r = requests.get(
            f"{BASE}/canales/{requests.utils.quote(canal, safe='')}/ids",
            headers=_headers(),
            timeout=TIMEOUT,
        )
        return _handle(r).get("ids", [])
    except Exception:
        return []


# ── History ───────────────────────────────────────────────────────────────────

def get_history() -> list:
    try:
        r = requests.get(f"{BASE}/audit/history", headers=_headers(), timeout=TIMEOUT)
        return _handle(r).get("items", [])
    except Exception:
        return []


def add_history(item: dict) -> dict:
    try:
        r = requests.post(
            f"{BASE}/audit/history", headers=_headers(), json=item, timeout=TIMEOUT
        )
        return _handle(r)
    except Exception:
        return {}


def clear_history_api() -> dict:
    try:
        r = requests.delete(f"{BASE}/audit/history", headers=_headers(), timeout=TIMEOUT)
        return _handle(r)
    except Exception:
        return {}


# ── Audit log ─────────────────────────────────────────────────────────────────

def get_audit_log(limit: int = 200) -> list:
    try:
        r = requests.get(
            f"{BASE}/audit/log",
            headers=_headers(),
            params={"limit": limit},
            timeout=TIMEOUT,
        )
        return _handle(r).get("log", [])
    except Exception:
        return []


# ── Users ─────────────────────────────────────────────────────────────────────

def get_users() -> list:
    try:
        r = requests.get(f"{BASE}/users/", headers=_headers(), timeout=TIMEOUT)
        return _handle(r).get("users", [])
    except Exception:
        return []

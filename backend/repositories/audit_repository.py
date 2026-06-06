"""
Audit & History Repository
--------------------------
Persists audit events and per-user copy history IN MEMORY (process lifetime).
In production, swap the storage backend for Redis or a DB.
"""

import threading
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

_audit_lock = threading.Lock()
_history_lock = threading.Lock()

# Global audit log: list of dicts
_audit_log: List[dict] = []

# Per-user history: {username: [HistorialItem dicts]} sorted by count desc
_user_history: Dict[str, List[dict]] = defaultdict(list)

MAX_HISTORY_PER_USER = 30
MAX_AUDIT_ENTRIES = 5000


# ── Audit ─────────────────────────────────────────────────────────────────

def log_event(username: str, accion: str, detalle: str = "", ip: str = ""):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "accion": accion,
        "detalle": detalle,
        "ip": ip,
    }
    with _audit_lock:
        _audit_log.append(entry)
        if len(_audit_log) > MAX_AUDIT_ENTRIES:
            _audit_log.pop(0)


def get_audit_log(limit: int = 200) -> List[dict]:
    with _audit_lock:
        return list(reversed(_audit_log[-limit:]))


# ── History ───────────────────────────────────────────────────────────────

def add_history_item(username: str, item: dict):
    """
    item = {id, desc, version, tipo, count, timestamp}
    If id already exists for user: increment count and re-sort.
    Otherwise prepend.
    """
    with _history_lock:
        hist = _user_history[username]
        existing = next((h for h in hist if h.get("id") == item.get("id")), None)
        if existing:
            existing["count"] = existing.get("count", 0) + 1
        else:
            item.setdefault("count", 1)
            item.setdefault("timestamp", datetime.utcnow().isoformat())
            hist.insert(0, item)

        # Sort by count desc
        hist.sort(key=lambda x: x.get("count", 0), reverse=True)

        # Trim
        _user_history[username] = hist[:MAX_HISTORY_PER_USER]


def get_history(username: str) -> List[dict]:
    with _history_lock:
        return list(_user_history.get(username, []))


def clear_history(username: str):
    with _history_lock:
        _user_history[username] = []


def remove_history_item(username: str, id_value: str):
    with _history_lock:
        hist = _user_history.get(username, [])
        _user_history[username] = [h for h in hist if h.get("id") != id_value]

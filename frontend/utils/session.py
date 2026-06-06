"""
Session State Manager
---------------------
Centralised helpers for reading/writing Streamlit session state.
"""

import streamlit as st


def init_session():
    defaults = {
        "logged_in": False,
        "token": "",
        "username": "",
        "rol": "",
        "history_loaded": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def get_user() -> str:
    return st.session_state.get("username", "")


def get_rol() -> str:
    return st.session_state.get("rol", "")


def set_session(token: str, username: str, rol: str):
    st.session_state.logged_in = True
    st.session_state.token = token
    st.session_state.username = username
    st.session_state.rol = rol
    st.session_state.history_loaded = False


def clear_session():
    st.session_state.logged_in = False
    st.session_state.token = ""
    st.session_state.username = ""
    st.session_state.rol = ""
    st.session_state.history_loaded = False

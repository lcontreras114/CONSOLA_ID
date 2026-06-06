"""
AUDITSA - Frontend Streamlit
============================
Run with:
    streamlit run frontend/app.py
"""

import streamlit as st
import streamlit.components.v1 as components

# Page config MUST be first Streamlit call
st.set_page_config(
    page_title="Consola de IDs — AUDITSA",
    page_icon="🔎",
    layout="wide"
)
# ── Internal imports (after page config) ─────────────────────────────────────
from utils.session import init_session, is_logged_in, set_session, clear_session, get_user, get_rol
from utils.styles import AUDITSA_CSS, get_header_html
import api_client
from components import tab_buscar, tab_nuevo_id, tab_canales, tab_admin

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(AUDITSA_CSS, unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
init_session()

MATRIZ_FILTROS = [
    "MENCION", "SUPERIMPO", "VIRTUAL", "RTC",
    "PATROCINIO", "B.PATROCINADO", "F. DE GOL", "MULTIPATRO",
    "I.ACTIVA", "I.AMBIENTAL", "C. COMERCIAL", "A.ESPECIAL",
]

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not is_logged_in():
    # Centered login card
    st.markdown("<br>", unsafe_allow_html=True)
    _, c_centro, _ = st.columns([1, 1.4, 1])

    with c_centro:
        # Logo / title block
        st.markdown(
            """
            <div style="
                text-align:center; 
                background: linear-gradient(135deg, #0F3460, #1E5FA8);
                border-radius: 16px; padding: 30px 20px 20px;
                border: 1px solid #1E3A5F;
                box-shadow: 0 10px 40px rgba(15,52,96,0.6);
                margin-bottom: 16px;
            ">
                <div style="
                    font-family:'Rajdhani',sans-serif; font-size:38px; font-weight:700;
                    color:#F1F5F9; letter-spacing:4px; margin-bottom:2px;
                ">AUDITSA</div>
                <div style="
                    font-family:'Rajdhani',sans-serif; font-size:12px; font-weight:600;
                    color:#F47B20; letter-spacing:6px;
                ">DIGITAL AUDIT</div>
                <div style="
                    margin-top:16px; font-family:'Inter',sans-serif;
                    font-size:13px; color:#64748B;
                ">Consola de Gestión de IDs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("form_login", clear_on_submit=False):
            user_input = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            pwd_input = st.text_input("Contraseña", type="password", placeholder="••••••••")

            submitted = st.form_submit_button("🔐 Entrar", type="primary", use_container_width=True)

            if submitted:
                if not user_input or not pwd_input:
                    st.error("Completa usuario y contraseña.")
                else:
                    with st.spinner("Autenticando..."):
                        result = api_client.login(user_input, pwd_input)

                    if result and result.get("access_token"):
                        set_session(
                            token=result["access_token"],
                            username=result["username"],
                            rol=result["rol"],
                        )
                        st.rerun()
                    elif result:
                        st.error("Usuario o contraseña incorrectos.")
                    # Error already shown by api_client if connection failed

    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP (authenticated)
# ══════════════════════════════════════════════════════════════════════════════
token = st.session_state.get("token", "")
username = get_user()
rol = get_rol()

# ── Header ────────────────────────────────────────────────────────────────────
col_titulo, col_filtros, col_logout = st.columns([2.5, 7, 1.5])

with col_titulo:
    st.markdown(
        "<div style='font-family:Rajdhani,sans-serif;font-size:20px;font-weight:700;"
        "color:#F1F5F9;margin-top:4px;letter-spacing:1px;'>🛠️ Consola de Gestión</div>",
        unsafe_allow_html=True,
    )

# ── Filter matrix (identical logic to original) ───────────────────────────────
with col_filtros:
    # Init filter state
    if "filtro_todo" not in st.session_state:
        st.session_state.filtro_todo = True
    for t in MATRIZ_FILTROS:
        if f"filtro_{t}" not in st.session_state:
            st.session_state[f"filtro_{t}"] = False

    def _cb_todo():
        if st.session_state.filtro_todo:
            for t in MATRIZ_FILTROS:
                st.session_state[f"filtro_{t}"] = False
        else:
            if not any(st.session_state.get(f"filtro_{t}", False) for t in MATRIZ_FILTROS):
                st.session_state.filtro_todo = True

    def _cb_tipo():
        if any(st.session_state.get(f"filtro_{t}", False) for t in MATRIZ_FILTROS):
            st.session_state.filtro_todo = False
        else:
            st.session_state.filtro_todo = True

    st.markdown('<span id="anchor-filtros"></span>', unsafe_allow_html=True)
    st.checkbox("TODO", key="filtro_todo", on_change=_cb_todo)

    r1 = st.columns(4)
...

with c_todo:
    st.markdown('<span id="chip-todo"></span>', unsafe_allow_html=True)
    st.checkbox("TODO", key="filtro_todo", on_change=_cb_todo)

with c_grilla:
    r1 = st.columns(4)
    for j, item in enumerate(MATRIZ_FILTROS[0:4]):
        with r1[j]:
            st.checkbox(item, key=f"filtro_{item}", on_change=_cb_tipo)
    r2 = st.columns(4)
    for j, item in enumerate(MATRIZ_FILTROS[4:8]):
        with r2[j]:
            st.checkbox(item, key=f"filtro_{item}", on_change=_cb_tipo)
    r3 = st.columns(4)
    for j, item in enumerate(MATRIZ_FILTROS[8:12]):
        with r3[j]:
            st.checkbox(item, key=f"filtro_{item}", on_change=_cb_tipo)

with col_logout:
    st.markdown(
        f"<div style='text-align:right;color:#F47B20;font-weight:600;"
        f"font-size:12px;margin-top:4px;font-family:Inter,sans-serif;'>"
        f"👤 {username}<br><span style='color:#64748B;font-size:10px;'>{rol.upper()}</span></div>",
        unsafe_allow_html=True,
    )
    if st.button("Cerrar Sesión", use_container_width=True):
        api_client.logout_api()
        clear_session()
        st.rerun()

st.divider()

# ── Tab configuration (role-based) ────────────────────────────────────────────
pestanas = ["🔍 Buscar AAEE"]

if rol in ("regular", "adm"):
    pestanas.append("📥 Nuevo ID")

pestanas.append("📺 IDs x Canal")

if rol == "adm":
    pestanas.append("🛡️ Validación Admin")

tabs = st.tabs(pestanas)
idx = 0

# ── Tab 1: Buscar AAEE ────────────────────────────────────────────────────────
with tabs[idx]:
    tab_buscar.render(token)
idx += 1

# ── Tab 2: Nuevo ID (regular + adm) ──────────────────────────────────────────
if rol in ("regular", "adm"):
    with tabs[idx]:
        tab_nuevo_id.render(token)
    idx += 1

# ── Tab 3: IDs x Canal ────────────────────────────────────────────────────────
with tabs[idx]:
    tab_canales.render(token, username)
idx += 1

# ── Tab 4: Admin ──────────────────────────────────────────────────────────────
if rol == "adm":
    with tabs[idx]:
        tab_admin.render(token)

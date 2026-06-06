"""
Tab: Nuevo ID
-------------
Form for REGULAR and ADM users to submit new IDs for validation.
"""

import re
import streamlit as st
import api_client
from utils.session import get_user


def _selector_o_manual(label: str, opciones: list, sufijo_key: str) -> str:
    opc = ["-- Seleccionar --", "INGRESAR NUEVO (MANUAL)"] + sorted(
        [o for o in opciones if o and str(o) != "nan"]
    )
    sel = st.selectbox(f"{label}:", opc, key=f"sel_{sufijo_key}")
    if sel == "INGRESAR NUEVO (MANUAL)":
        return st.text_input(f"Escriba {label}:", key=f"txt_{sufijo_key}").upper()
    return sel if sel != "-- Seleccionar --" else ""


def _aplicar_reglas_marca(texto: str) -> str:
    if not texto:
        return ""
    t = str(texto).upper().replace("&", "Y").replace("'", "").replace("´", "").replace("`", "")
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9\-\s]", "", t)).strip()


def render(token: str):
    st.markdown(
        "<div style='font-family:Rajdhani,sans-serif;font-size:20px;font-weight:700;"
        "color:#F47B20;letter-spacing:1px;margin-bottom:12px;'>Sugerir Nuevo Registro</div>",
        unsafe_allow_html=True,
    )

    # Load distinct values for dropdowns
    cias = api_client.get_distinct_values("Compañía")
    marcas = api_client.get_distinct_values("Marca")
    submarcas = api_client.get_distinct_values("Submarca")
    productos = api_client.get_distinct_values("Producto")
    tipos = api_client.get_distinct_values("Tipo")

    c1, c2 = st.columns(2)

    with c1:
        n_cia = _selector_o_manual("Compañía", cias, "cia")
        n_mar = _selector_o_manual("Marca", marcas, "mar")
        n_sub = _selector_o_manual("Submarca", submarcas, "sub")

    with c2:
        n_pro = _selector_o_manual("Producto", productos, "pro")
        n_ver = st.text_input(
            "Versión",
            value=_aplicar_reglas_marca(n_mar),
            key="txt_version",
        ).upper()
        n_id = st.text_input("ID Detección (8 dígitos)", key="txt_id_nuevo")
        n_tipo = _selector_o_manual("Tipo de Spot", tipos, "tipo")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("📤 Enviar a Validación", type="primary", use_container_width=False):
        if not n_cia or not n_mar or not n_id:
            st.error("⚠️ Campos obligatorios: Compañía, Marca e ID.")
        elif not re.match(r"^\d{8}$", n_id.strip()):
            st.error("⚠️ El ID debe contener exactamente 8 números.")
        else:
            result = api_client.create_id({
                "compania": n_cia,
                "marca": n_mar,
                "submarca": n_sub,
                "producto": n_pro,
                "version": n_ver,
                "tipo": n_tipo,
                "id_deteccion": n_id.strip(),
            })
            if result:
                st.success(
                    f"✅ ID **{n_id}** enviado a validación correctamente. "
                    "Aparecerá con 🟡 hasta que el administrador lo valide."
                )

"""
Tab: Admin Panel (ADM only)
---------------------------
- Validate / reject pending IDs
- View full ID base
- Audit log
- User list
"""

import streamlit as st
import pandas as pd
import api_client


def render(token: str):
    st.markdown(
        "<div style='font-family:Rajdhani,sans-serif;font-size:20px;font-weight:700;"
        "color:#F47B20;letter-spacing:1px;margin-bottom:8px;'>🛡️ Panel Admin</div>",
        unsafe_allow_html=True,
    )

    sub_tabs = st.tabs(["⏳ Validación de IDs", "📚 Base de IDs", "📋 Log de Auditoría", "👥 Usuarios"])

    # ── Subtab 1: Validación ──────────────────────────────────────────────
    with sub_tabs[0]:
        data = api_client.get_pending_ids()
        pending = data.get("pending", [])

        if pending:
            st.markdown(
                f"<div style='color:#FBBF24;font-weight:600;margin-bottom:10px;font-size:13px;'>"
                f"⏳ {len(pending)} ID(s) pendiente(s) de validación</div>",
                unsafe_allow_html=True,
            )
            for row in pending:
                id_val = row.get("ID", "")
                marca = row.get("Marca", "")
                cia = row.get("Compañía", "")
                tipo = row.get("Tipo", "")
                creado_por = row.get("creado_por", "—")

                c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
                c1.markdown(
                    f"<div style='background:#1A2235;border:1px solid #92400E;border-radius:8px;"
                    f"padding:10px 14px;'>"
                    f"<span style='color:#FBBF24;font-weight:700;'>🟡 {id_val}</span>"
                    f"<br><span style='font-size:12px;color:#94A3B8;'>"
                    f"<b>Marca:</b> {marca} &nbsp;|&nbsp; <b>Cía:</b> {cia} &nbsp;|&nbsp;"
                    f"<b>Tipo:</b> {tipo} &nbsp;|&nbsp; <b>Creado por:</b> {creado_por}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if c3.button("✅ Validar", key=f"val_{id_val}", use_container_width=True):
                    result = api_client.validate_id(id_val, "validar")
                    if result:
                        st.success(f"ID {id_val} validado.")
                        st.rerun()
                if c4.button("❌ Rechazar", key=f"rej_{id_val}", use_container_width=True):
                    result = api_client.validate_id(id_val, "rechazar")
                    if result:
                        st.warning(f"ID {id_val} rechazado y eliminado.")
                        st.rerun()
        else:
            st.success("✅ Todo validado. No hay IDs pendientes.")

    # ── Subtab 2: Base de IDs ─────────────────────────────────────────────
    with sub_tabs[1]:
        data = api_client.search_ids(query="")
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            show_cols = [c for c in ["Compañía", "Marca", "Submarca", "Producto", "VersiOn", "Tipo", "ID", "Estado"] if c in df.columns]
            if show_cols:
                st.dataframe(
                    df[show_cols].fillna(""),
                    hide_index=True,
                    use_container_width=True,
                )
                st.caption(f"Total: {len(df)} registros")
        else:
            st.info("No hay datos disponibles.")

    # ── Subtab 3: Audit Log ───────────────────────────────────────────────
    with sub_tabs[2]:
        limit = st.number_input("Mostrar últimas N entradas:", min_value=10, max_value=1000, value=100, step=10)
        if st.button("🔄 Actualizar Log", use_container_width=False):
            st.rerun()

        log = api_client.get_audit_log(limit=int(limit))
        if log:
            df_log = pd.DataFrame(log)
            show_cols = [c for c in ["timestamp", "username", "accion", "detalle", "ip"] if c in df_log.columns]
            st.dataframe(
                df_log[show_cols].fillna(""),
                hide_index=True,
                use_container_width=True,
            )
            st.caption(f"Total entradas cargadas: {len(df_log)}")
        else:
            st.info("No hay entradas en el log de auditoría.")

    # ── Subtab 4: Usuarios ────────────────────────────────────────────────
    with sub_tabs[3]:
        users = api_client.get_users()
        if users:
            df_users = pd.DataFrame(users)
            st.dataframe(
                df_users.fillna(""),
                hide_index=True,
                use_container_width=True,
            )
            st.caption(f"Total usuarios: {len(df_users)}")
        else:
            st.info("No se pudieron cargar los usuarios.")

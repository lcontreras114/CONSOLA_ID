"""
Tab: IDs x Canal
----------------
Shows assigned channels + manual search.
Each channel has a copy card (monitor text, tag autopromos, grilla button).
"""

import re
import streamlit as st
import streamlit.components.v1 as components
import api_client


def _renderizar_canal(canal: str, info: dict, ids_canal: list):
    st_id = info.get("station_id", "N/A")
    tag_auto = info.get("tag_autopromos", "N/A")
    grilla = info.get("grilla", "N/A")
    server = info.get("server", "N/A")

    if server not in ("N/A", "None", "", "nan"):
        texto_monitor = f"{canal} - {st_id} - {server}"
    else:
        texto_monitor = f"{canal} - {st_id} - MONITOR"

    tm_js = texto_monitor.replace("'", "\\'")
    ta_js = str(tag_auto).replace("'", "\\'")

    btn_grilla = ""
    g = str(grilla)
    if g not in ("N/A", "", "nan", "None"):
        if "http" in g.lower():
            btn_grilla = f'<a href="{g}" target="_blank" class="btn-grilla">🌐 Ver Grilla Web<br><span style="font-size:10px;">Abrir enlace</span></a>'
        elif "carta" in g.lower():
            ruta = r"\\192.168.148.80\Casos\MonDedicado\Programacion"
            ruta_js = ruta.replace("\\", "\\\\")
            btn_grilla = f'<button class="btn-grilla" onclick="navigator.clipboard.writeText(\'{ruta_js}\');this.innerHTML=\'✓ Ruta copiada\';setTimeout(()=>this.innerHTML=\'📁 Carta Oficial\',2000)">📁 Carta Oficial<br><span style="font-size:10px;">Copiar ruta</span></button>'
        else:
            btn_grilla = f'<a href="https://secciones.dish.com.mx/guiadeprogramacion.html" target="_blank" class="btn-grilla">📡 Grilla Dish<br><span style="font-size:11px;">({g})</span></a>'

    uid = re.sub(r"\W+", "", canal)

    html = f"""
    <style>
        :root {{--bg:#111827;--text:#F1F5F9;--btn-dark:#0F3460;}}
        body{{margin:0;padding:0;background:transparent;font-family:'Inter',sans-serif;overflow:hidden;}}
        .wrapper{{display:flex;flex-direction:row;flex-wrap:nowrap;gap:8px;width:100%;height:110px;
                  box-sizing:border-box;align-items:stretch;}}
        .card{{flex:2;min-width:0;display:flex;justify-content:space-between;align-items:center;
               background:var(--bg);border:2px dashed #1E5FA8;border-radius:10px;
               padding:8px 12px;cursor:pointer;color:var(--text);transition:all 0.2s;}}
        .card:hover{{border-color:#F47B20;background:#1A2235;}}
        .info-txt{{font-size:11px;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
        .info-txt b{{color:#F47B20;}}
        .btn-grilla,.btn-promo{{flex:1;min-width:0;background:#1E5FA8;color:white;border-radius:10px;
                                font-size:11px;font-weight:700;cursor:pointer;text-decoration:none;
                                display:flex;flex-direction:column;align-items:center;
                                justify-content:center;text-align:center;border:none;transition:all 0.2s;}}
        .btn-grilla:hover{{background:#3B82F6;}}
        .btn-promo{{background:var(--btn-dark);}}
        .btn-promo:hover{{background:#1E3A5F;}}
        .toast{{position:fixed;bottom:5px;right:5px;background:#065F46;color:#6EE7B7;
                padding:8px 15px;border-radius:5px;font-size:12px;display:none;z-index:1000;}}
    </style>
    <script>
        function cop_{uid}(txt,msg='✓ Copiado'){{
            navigator.clipboard.writeText(txt);
            let t=document.getElementById('t_{uid}');
            t.style.display='block';t.innerHTML=msg;
            setTimeout(()=>{{t.style.display='none'}},2000);
        }}
    </script>
    <div class="wrapper">
        <div class="card" onclick="cop_{uid}('{tm_js}')">
            <div class="info-txt">
                <b>{canal}</b><br>
                ID: {st_id} | Server: {server}
            </div>
        </div>
        {btn_grilla}
        <button class="btn-promo" onclick="cop_{uid}('{ta_js}')">TAG:<br>{tag_auto}</button>
    </div>
    <div id="t_{uid}" class="toast"></div>
    """
    components.html(html, height=125, scrolling=False)

    # Expandable IDs table
    if ids_canal:
        with st.expander(f"📂 Ver IDs — {canal}"):
            from itertools import groupby
            ids_por_hash = {}
            for row in ids_canal:
                h = row.get("codigo_hash", "—")
                ids_por_hash.setdefault(h, []).append(row)

            for h, rows in ids_por_hash.items():
                st.markdown(f"**{h}**")
                html_i = """
                <style>
                    :root{--bg:#111827;--text:#F1F5F9;--border:#1E3A5F;}
                    body{margin:0;font-family:'Inter',sans-serif;background:transparent;}
                    table{width:100%;border-collapse:collapse;font-size:13px;background:var(--bg);}
                    th,td{border:1px solid var(--border);padding:8px;text-align:left;color:var(--text);}
                    th{background:#0F3460;color:#F1F5F9;font-size:11px;}
                    .btn-i{width:100%;cursor:pointer;font-weight:700;background:#1A2235;
                           border:1px solid #2D4A6B;border-radius:4px;padding:4px;
                           color:#F1F5F9;transition:0.2s;font-size:12px;}
                    .btn-i:hover{background:#243555;border-color:#3B82F6;}
                </style>
                <table><tr><th>Tipo</th><th>Descripción</th><th>ID</th></tr>
                """
                for r in rows:
                    v_id = str(r.get("id_value", "")).split(".")[0]
                    html_i += (
                        f"<tr><td>{r.get('tipo','')}</td>"
                        f"<td>{r.get('descripcion','')}</td>"
                        f"<td><button class='btn-i' "
                        f"onclick=\"navigator.clipboard.writeText('{v_id}');"
                        f"this.innerHTML='✓ Ok!';setTimeout(()=>this.innerHTML='{v_id}',1000)\">"
                        f"{v_id}</button></td></tr>"
                    )
                html_i += "</table>"
                components.html(html_i, height=60 + len(rows) * 52, scrolling=False)


def render(token: str, username: str):
    # ── Canales asignados al usuario ──────────────────────────────────────
    mis_canales = api_client.get_mis_canales()

    if mis_canales:
        st.markdown(
            f"<div style='font-family:Rajdhani,sans-serif;font-size:18px;font-weight:700;"
            f"color:#F1F5F9;margin-bottom:10px;'>📋 Canales Asignados ({len(mis_canales)})</div>",
            unsafe_allow_html=True,
        )
        for i in range(0, len(mis_canales), 2):
            cols = st.columns(2)
            for j, canal in enumerate(mis_canales[i : i + 2]):
                info = api_client.get_canal_info(canal)
                ids_c = api_client.get_canal_ids(canal)
                with cols[j]:
                    with st.container(border=True):
                        _renderizar_canal(canal, info, ids_c)
        st.divider()

    # ── Buscador manual ───────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Rajdhani,sans-serif;font-size:18px;font-weight:700;"
        "color:#F1F5F9;margin-bottom:10px;'>🔍 Buscar Canal</div>",
        unsafe_allow_html=True,
    )
    todos_canales = api_client.get_all_canales()
    c_sel = st.selectbox(
        "Canal:",
        ["-- Seleccionar --"] + todos_canales,
        label_visibility="collapsed",
    )
    if c_sel != "-- Seleccionar --":
        info = api_client.get_canal_info(c_sel)
        ids_c = api_client.get_canal_ids(c_sel)
        with st.container(border=True):
            _renderizar_canal(c_sel, info, ids_c)

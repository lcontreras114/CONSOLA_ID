"""
Tab: Buscar AAEE
----------------
Search + filter matrix + results table + history sidebar.
"""

import streamlit as st
import streamlit.components.v1 as components
import api_client
from utils.session import get_user

MATRIZ_FILTROS = [
    "MENCION", "SUPERIMPO", "VIRTUAL", "RTC",
    "PATROCINIO", "B.PATROCINADO", "F. DE GOL", "MULTIPATRO",
    "I.ACTIVA", "I.AMBIENTAL", "C. COMERCIAL", "A.ESPECIAL",
]


def _init_filtros():
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


def _build_resultado_html(resultados: list) -> str:
    html = """
    <style>
        :root {
            --bg:#111827; --text:#F1F5F9; --border:#1E3A5F;
            --th-bg:#0F3460; --th-text:#F1F5F9; --row-alt:#1A2235;
            --btn-bg:#1E2D45; --btn-border:#2D4A6B; --btn-hover:#243555;
            --hover-hl:rgba(244,123,32,0.15);
        }
        body{margin:0;font-family:'Inter',sans-serif;background:transparent;}
        table{width:100%;border-collapse:collapse;font-size:13px;background:var(--bg);}
        th,td{border:1px solid var(--border);padding:9px 10px;text-align:left;color:var(--text);}
        th{background:var(--th-bg);color:var(--th-text);text-align:center;font-weight:600;font-size:11px;letter-spacing:0.5px;}
        tr:nth-child(even) td{background:var(--row-alt);}
        tr:hover td{background:var(--hover-hl)!important;}
        .btn-c{background:var(--btn-bg);border:1px solid var(--btn-border);color:var(--text);
            cursor:pointer;width:100%;font-weight:700;border-radius:5px;padding:6px 4px;
            font-size:12px;transition:all 0.2s;font-family:'Inter',sans-serif;}
        .btn-c:hover{background:var(--btn-hover);transform:scale(1.02);border-color:#3B82F6;}
        .btn-c.copiado{background:#065F46!important;color:#6EE7B7!important;border-color:#059669!important;}
        .btn-c.warn{background:#451A03;border-color:#92400E;color:#FCD34D;}
        .btn-c.warn:hover{background:#78350F;}
        .semaforo{font-size:14px;}
    </style>
    <script>
        function copiarID(id, desc, version, tipo, boton) {
            navigator.clipboard.writeText(id);
            let txtOrig = boton.innerHTML;
            boton.innerHTML = '✓ Copiado';
            boton.classList.add('copiado');
            setTimeout(()=>{boton.innerHTML=txtOrig; boton.classList.remove('copiado');}, 1400);
            fetch('/audit/history', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({id:id,desc:desc,version:version,tipo:tipo,count:1})
            }).catch(()=>{});
        }
    </script>
    <table>
    <tr>
        <th style="width:4%">Est.</th>
        <th>Compañía</th><th>Marca</th><th>Submarca</th>
        <th>Producto</th><th>Versión</th><th>Tipo</th><th style="width:12%">ID</th>
    </tr>
    """
    for f in resultados:
        id_t = str(f.get("ID", f.get("id_deteccion", ""))).split(".")[0]
        estado = str(f.get("Estado", f.get("estado", "Confiable"))).upper()
        if estado in ("NO VALIDADO", "PENDIENTE"):
            luz, clase = "🟡", "btn-c warn"
        elif estado in ("RECHAZADO",):
            luz, clase = "🔴", "btn-c"
        else:
            luz, clase = "🟢", "btn-c"

        def esc(v):
            return str(v).replace("nan", "N/A").replace("'", "\\'").replace('"', "&quot;")

        cia = f.get("Compañía", f.get("compania", ""))
        marca = f.get("Marca", f.get("marca", ""))
        sub = f.get("Submarca", f.get("submarca", ""))
        prod = f.get("Producto", f.get("producto", ""))
        ver = f.get("VersiOn", f.get("version", ""))
        tipo = f.get("Tipo", f.get("tipo", ""))
        desc_txt = f"{esc(marca)} | {esc(sub)} | {esc(prod)}"

        html += (
            f"<tr>"
            f"<td style='text-align:center'>{luz}</td>"
            f"<td>{cia}</td><td>{marca}</td><td>{sub}</td>"
            f"<td>{prod}</td><td>{ver}</td><td>{tipo}</td>"
            f"<td><button class='{clase}' onclick=\"copiarID('{id_t}','{desc_txt}','{esc(ver)}','{esc(tipo)}',this)\">{id_t}</button></td>"
            f"</tr>"
        )
    html += "</table>"
    return html


def _build_history_html(items: list) -> str:
    items_js = []
    for it in items:
        items_js.append({
            "id": str(it.get("id", "")),
            "desc": str(it.get("desc", "")),
            "version": str(it.get("version", "")),
            "tipo": str(it.get("tipo", "")),
            "count": it.get("count", 1),
        })
    import json
    items_json = json.dumps(items_js)

    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        :root {{--bg:#111827;--text:#F1F5F9;--border:#1E3A5F;--btn-bg:#1A2235;--btn-hover:#243555;}}
        body{{margin:0;padding:0;background:transparent;font-family:'Inter',sans-serif;overflow:hidden;}}
        .hc{{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:12px;
             height:86vh;max-height:900px;overflow-y:auto;}}
        .ht{{font-size:13px;font-weight:600;color:#94A3B8;margin-bottom:10px;
             border-bottom:2px solid var(--border);padding-bottom:6px;
             position:sticky;top:0;background:var(--bg);z-index:10;
             display:flex;justify-content:space-between;align-items:center;}}
        .btn-del{{background:transparent;border:none;cursor:pointer;font-size:16px;
                  padding:2px 5px;border-radius:4px;transition:0.2s;}}
        .btn-del:hover{{background:rgba(239,68,68,0.15);transform:scale(1.1);}}
        .bh{{display:block;width:100%;background:var(--btn-bg);
             border:1px solid #1E3A5F;padding:8px 7px;margin-bottom:7px;
             border-radius:8px;cursor:pointer;color:var(--text);transition:all 0.2s;
             overflow:hidden;box-shadow:0 2px 8px rgba(30,95,168,0.15);}}
        .bh:hover{{background:var(--btn-hover);transform:translateY(-2px);
                   border-color:#3B82F6;box-shadow:0 4px 12px rgba(59,130,246,0.2);}}
        .bh.copiado{{background:#065F46!important;border-color:#059669!important;}}
        .hd{{font-size:10px;color:#64748B;text-align:center;padding-bottom:3px;
             border-bottom:1px solid #1E3A5F;margin-bottom:3px;
             white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-transform:uppercase;}}
        .hv{{font-size:13px;color:#F47B20;font-weight:700;text-align:center;
             padding-bottom:3px;border-bottom:1px solid #1E3A5F;margin-bottom:3px;
             text-transform:uppercase;letter-spacing:0.5px;}}
        .hti{{font-size:11px;color:#94A3B8;text-align:center;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-transform:uppercase;}}
        .empty{{font-size:12px;color:#4B5563;text-align:center;padding:20px 5px;}}
    </style>
    <script>
        var _items = {items_json};
        
        function render() {{
            var c = document.getElementById('hl');
            if (!_items || _items.length === 0) {{
                c.innerHTML = "<div class='empty'>Copia un ID para empezar.</div>";
                return;
            }}
            var h = "";
            _items.forEach(function(it) {{
                h += "<button class='bh' onclick=\\"copy(\\'"+it.id+"\\',\\'"+it.desc+"\\',this)\\" title=\\""+it.desc+"\\">"
                   + "<div class='hd'>"+it.desc+"</div>"
                   + "<div class='hv'>"+it.id+"</div>"
                   + "<div class='hti'>"+it.version+" · "+it.tipo+"</div>"
                   + "</button>";
            }});
            c.innerHTML = h;
        }}
        
        function copy(id, desc, btn) {{
            navigator.clipboard.writeText(id);
            btn.classList.add('copiado');
            var idx = _items.findIndex(function(x){{return x.id===id;}});
            if(idx>-1) {{ _items[idx].count = (_items[idx].count||0)+1; }}
            _items.sort(function(a,b){{return (b.count||0)-(a.count||0);}});
            setTimeout(function(){{btn.classList.remove('copiado'); render();}}, 1200);
        }}
        
        function clearAll() {{
            if(confirm("¿Eliminar todo el historial?")) {{
                _items = [];
                render();
                fetch('/audit/history', {{method:'DELETE'}}).catch(()=>{{}});
            }}
        }}
        
        window.onload = render;
    </script>
    <div class='hc'>
        <div class='ht'>
            <span>🕒 Historial</span>
            <button class='btn-del' onclick='clearAll()' title='Borrar todo'>🗑️</button>
        </div>
        <div id='hl'></div>
    </div>
    """
    return html


def render(token: str):
    _init_filtros()

    col_main, col_hist = st.columns([3.5, 1.2])

    with col_main:
        busqueda = st.text_input(
            "🔍 Buscar (Compañía, Marca, Producto, ID...):",
            placeholder="Ej: Caliente, 12345678...",
            key="search_universal",
        )

        mostrar_tabla = False
        resultados = []

        if busqueda or not st.session_state.filtro_todo:
            tipos_activos = [t for t in MATRIZ_FILTROS if t != "RTC" and st.session_state.get(f"filtro_{t}", False)]
            rtc_activo = st.session_state.get("filtro_RTC", False)

            data = api_client.search_ids(
                query=busqueda,
                tipos=tipos_activos,
                rtc=rtc_activo,
            )
            resultados = data.get("results", [])
            mostrar_tabla = True

        if mostrar_tabla:
            if resultados:
                st.markdown(
                    f"<div style='color:#F47B20;font-weight:600;margin:8px 0;font-family:Inter,sans-serif;font-size:13px;'>"
                    f"Resultados encontrados: {len(resultados)}</div>",
                    unsafe_allow_html=True,
                )
                html_tabla = _build_resultado_html(resultados)
                components.html(html_tabla, height=60 + len(resultados) * 52, scrolling=False)
            else:
                st.info("No se encontraron coincidencias.")

    with col_hist:
        # Load history from backend
        history_items = api_client.get_history()
        html_hist = _build_history_html(history_items)
        components.html(html_hist, height=950, scrolling=False)

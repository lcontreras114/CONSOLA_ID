"""
Global CSS and theming for AUDITSA frontend.
"""

AUDITSA_CSS = """
<style>
/* ─── Google Fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ─── CSS Variables ─────────────────────────────────────────────── */
:root {
    --blue-primary: #1E5FA8;
    --blue-dark: #0F3460;
    --blue-light: #3B82F6;
    --orange: #F47B20;
    --orange-light: #FB923C;
    --bg-main: #0B0F1A;
    --bg-card: #111827;
    --bg-card2: #1A2235;
    --border: #1E3A5F;
    --border-light: #2D4A6B;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --pending: #FBBF24;
    --font-display: 'Rajdhani', sans-serif;
    --font-body: 'Inter', sans-serif;
}

/* ─── Reset / Base ──────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { 
    padding: 1rem 1.5rem 1rem !important; 
    max-width: 100% !important;
}

/* ─── Streamlit chrome ──────────────────────────────────────────── */
.stApp {
    background: var(--bg-main) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ─── Tabs ──────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px 10px 0 0;
    border-bottom: 2px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-display) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 18px !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    color: var(--orange) !important;
    background: rgba(244, 123, 32, 0.08) !important;
    border-bottom: 3px solid var(--orange) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--bg-card) !important;
    border-radius: 0 0 10px 10px;
    border: 1px solid var(--border);
    border-top: none;
    padding: 16px !important;
}

/* ─── Inputs ────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: var(--font-body) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--blue-light) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}
.stTextInput > label, .stSelectbox > label { 
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ─── Buttons ───────────────────────────────────────────────────── */
.stButton > button {
    background: var(--bg-card2) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 6px !important;
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--blue-light) !important;
    background: rgba(59,130,246,0.1) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--blue-primary), var(--blue-light)) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--blue-dark), var(--blue-primary)) !important;
    box-shadow: 0 4px 15px rgba(30,95,168,0.4) !important;
}

/* ─── Divider ───────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ─── Checkboxes (filter matrix) ───────────────────────────────── */
div[data-testid="stCheckbox"] div[data-baseweb="checkbox"] > div:first-child { 
    display: none !important; 
}
div[data-testid="stCheckbox"] label { 
    background: var(--bg-card2) !important;
    border: 1px solid var(--border-light) !important; 
    border-radius: 4px !important;
    padding: 0px !important; 
    cursor: pointer !important; 
    transition: all 0.15s ease !important; 
    margin: 0 !important; 
    display: flex; align-items: center; justify-content: center;
    height: 28px !important; 
    width: 100% !important;
}
div[data-testid="stCheckbox"] p { 
    font-size: 10px !important;
    font-weight: 600 !important; 
    font-family: var(--font-display) !important;
    color: var(--text-secondary) !important;
    margin: 0 !important;
    letter-spacing: 0.3px !important; 
    text-align: center; width: 100%; 
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
div[data-testid="stCheckbox"] label:hover { 
    background: rgba(59,130,246,0.08) !important; 
    border-color: var(--blue-light) !important;
}
div[data-testid="stCheckbox"]:has(input:checked) label { 
    background: rgba(244, 123, 32, 0.12) !important; 
    border-color: var(--orange) !important; 
    border-width: 2px !important;
}
div[data-testid="stCheckbox"]:has(input:checked) p { 
    color: var(--orange) !important; 
}
div:has(> div > span#chip-todo) + div[data-testid="stVerticalBlock"] label {
    height: 88px !important;
}
div:has(> div > span#chip-todo) + div[data-testid="stVerticalBlock"] p {
    font-size: 12px !important;
}
div:has(> div > span#anchor-filtros) div[data-testid="stHorizontalBlock"] { 
    gap: 2px !important; align-items: start !important; 
}
div:has(> div > span#anchor-filtros) div[data-testid="column"] { 
    padding: 0 !important; min-width: 0 !important; 
}
div:has(> div > span#anchor-filtros) .stCheckbox { margin-bottom: 2px !important; }

/* ─── Alerts ────────────────────────────────────────────────────── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
}

/* ─── Expander ──────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

/* ─── Dataframe ─────────────────────────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ─── Container border ──────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
}

/* ─── Form ──────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
</style>
"""

# Header HTML with logo
def get_header_html(username: str, rol: str) -> str:
    return f"""
    <div style="
        display:flex; align-items:center; justify-content:space-between;
        background: linear-gradient(135deg, #0F3460 0%, #1E5FA8 50%, #0F3460 100%);
        border-radius: 12px; padding: 10px 20px; margin-bottom: 4px;
        border: 1px solid #1E3A5F; box-shadow: 0 4px 20px rgba(15,52,96,0.5);
    ">
        <div style="display:flex; align-items:center; gap:14px;">
            <div style="
                font-family:'Rajdhani',sans-serif; font-size:22px; font-weight:700;
                color:#F1F5F9; letter-spacing:2px;
            ">AUDITSA</div>
            <div style="
                font-family:'Rajdhani',sans-serif; font-size:11px; font-weight:500;
                color:#F47B20; letter-spacing:4px; padding-top:2px;
            ">DIGITAL AUDIT</div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="
                background: rgba(244,123,32,0.15); border: 1px solid rgba(244,123,32,0.3);
                border-radius: 6px; padding: 4px 12px;
                font-family:'Inter',sans-serif; font-size:12px; font-weight:500; color:#FB923C;
            ">
                👤 {username} &nbsp;·&nbsp; {rol.upper()}
            </div>
        </div>
    </div>
    """

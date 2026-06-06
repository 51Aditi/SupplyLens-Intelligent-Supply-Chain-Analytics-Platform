"""Shared CSS, theme, chart utilities — premium BI dashboard."""
import streamlit as st


# ── Colour palette ─────────────────────────────────────────────────────────────
BG       = "#0B1120"
CARD     = "#1E293B"
SIDEBAR  = "#0F172A"
BORDER   = "#334155"
ACCENT   = "#38BDF8"
SUCCESS  = "#22C55E"
WARNING  = "#F59E0B"
DANGER   = "#EF4444"
TEXT     = "#FFFFFF"
TEXT2    = "#CBD5E1"
MUTED    = "#94A3B8"

# Chart-only restored colors
CHART_BG       = "white"
CHART_PLOT_BG  = "white"
CHART_TEXT     = "#0F172A"
CHART_GRID     = "#E2E8F0"
CHART_LINE     = "#CBD5E1"
CHART_HOVER_BG = "white"


# ── Per-chart palettes ─────────────────────────────────────────────────────────
P1    = ["#38BDF8", "#0EA5E9", "#0284C7", "#0369A1", "#075985"]
P2    = ["#22C55E", "#16A34A", "#15803D", "#166534", "#14532D"]
P3    = ["#F97316", "#EA580C", "#C2410C", "#9A3412", "#7C2D12"]
P4    = ["#A855F7", "#9333EA", "#7E22CE", "#6B21A8", "#581C87"]
P5    = ["#EC4899", "#DB2777", "#BE185D", "#9D174D", "#831843"]
P6    = ["#FACC15", "#EAB308", "#CA8A04", "#A16207", "#854D0E"]
MIXED = ["#38BDF8", "#A855F7", "#22C55E", "#F97316", "#EC4899",
         "#FACC15", "#06B6D4", "#8B5CF6", "#10B981", "#F43F5E"]


# ── Global Plotly theme ────────────────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor=CHART_BG,
    plot_bgcolor=CHART_PLOT_BG,
    font=dict(size=14, color=CHART_TEXT, family="Inter, sans-serif"),
    title_font=dict(size=16, color=CHART_TEXT, family="Inter, sans-serif"),
    xaxis=dict(
        gridcolor=CHART_GRID,
        linecolor=CHART_LINE,
        tickcolor=CHART_TEXT,
        zerolinecolor=CHART_LINE,
        tickfont=dict(size=13, color=CHART_TEXT),
        title_font=dict(size=14, color=CHART_TEXT),
    ),
    yaxis=dict(
        gridcolor=CHART_GRID,
        linecolor=CHART_LINE,
        tickcolor=CHART_TEXT,
        zerolinecolor=CHART_LINE,
        tickfont=dict(size=13, color=CHART_TEXT),
        title_font=dict(size=14, color=CHART_TEXT),
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor=CHART_LINE,
        borderwidth=1,
        font=dict(size=13, color=CHART_TEXT),
        title=dict(font=dict(color=CHART_TEXT)),
    ),
    margin=dict(t=60, b=50, l=60, r=30),
    hoverlabel=dict(
        bgcolor=CHART_HOVER_BG,
        bordercolor=CHART_LINE,
        font=dict(color=CHART_TEXT, size=13),
    ),
    transition=dict(duration=300, easing="cubic-in-out"),
    coloraxis_colorbar=dict(
        tickfont=dict(color=CHART_TEXT, size=12),
        title_font=dict(color=CHART_TEXT, size=13),
    ),
)


def pl(fig, h=420):
    """Apply global Plotly theme to any figure."""
    fig.update_layout(height=h, **PLOTLY_BASE)
    fig.update_annotations(font_color=CHART_TEXT, font_size=13)
    def pl(fig, h=420):
     fig.update_layout(
        height=h,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=CHART_TEXT)
    )
    return fig
    def pl(fig, h=420):
     fig.update_layout(
        height=h,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=CHART_TEXT)
    )
    return fig


def pie_style(fig, h=380):
    """Style for Pie / Donut charts — dark labels on white background."""
    fig.update_traces(
        textinfo="percent+label",
        textfont=dict(size=14, color=CHART_TEXT),
        textposition="outside",
        outsidetextfont=dict(size=13, color=CHART_TEXT),
        insidetextfont=dict(size=13, color=CHART_TEXT),
    )
    fig.update_layout(
        height=h,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=dict(size=14, color=CHART_TEXT, family="Inter, sans-serif"),
        title_font=dict(size=16, color=CHART_TEXT, family="Inter, sans-serif"),
        legend=dict(
            font=dict(size=13, color=CHART_TEXT),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=CHART_LINE,
            borderwidth=1,
            title=dict(font=dict(color=CHART_TEXT)),
        ),
        margin=dict(t=60, b=40, l=20, r=20),
    )
    fig.update_annotations(font_color=CHART_TEXT, font_size=13)
    return fig


def heatmap_style(fig, h=500):
    """Style for heatmap charts — white/light chart area with dark text."""
    fig.update_layout(
        height=h,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=dict(size=13, color=CHART_TEXT, family="Inter, sans-serif"),
        title_font=dict(size=16, color=CHART_TEXT, family="Inter, sans-serif"),
        xaxis=dict(
            tickfont=dict(size=12, color=CHART_TEXT),
            title_font=dict(size=14, color=CHART_TEXT),
            tickangle=-40,
            gridcolor=CHART_GRID,
            linecolor=CHART_LINE,
            zerolinecolor=CHART_LINE,
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=CHART_TEXT),
            title_font=dict(size=14, color=CHART_TEXT),
            gridcolor=CHART_GRID,
            linecolor=CHART_LINE,
            zerolinecolor=CHART_LINE,
        ),
        margin=dict(t=60, b=80, l=160, r=30),
    )
    fig.update_annotations(font_color=CHART_TEXT, font_size=13)
    return fig


# ── Master CSS ─────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ROOT */
html,body,[class*="css"]{ font-family:'Inter',sans-serif !important; }
.main         { background:#0B1120 !important; }
.block-container { padding:1.4rem 2rem !important; max-width:100% !important; }
#MainMenu,footer,header      { visibility:hidden !important; }
[data-testid="stSidebarNav"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }


/* SIDEBAR */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0F172A 0%,#111827 100%) !important;
    border-right:1px solid #1E3A5F !important;
    min-width:268px !important; max-width:268px !important;
}
[data-testid="stSidebar"] * { color:#F1F5F9 !important; }
.sb-brand { padding:0 0 14px; border-bottom:1px solid #1E3A5F; margin-bottom:10px; }
.sb-brand h2{ font-size:1.05rem; font-weight:700; color:#38BDF8 !important; margin:5px 0 2px; }
.sb-brand p { font-size:0.72rem; color:#94A3B8 !important; margin:0; }
.nav-lbl {
    font-size:10px; font-weight:700; letter-spacing:1.6px;
    text-transform:uppercase; color:#475569 !important; padding:10px 4px 4px;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] {
    border-radius:10px !important; padding:3px 8px !important;
    margin:2px 0 !important; transition:all .2s !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
    background:rgba(56,189,248,.12) !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] {
    background:rgba(56,189,248,.18) !important;
    border-left:3px solid #38BDF8 !important;
    box-shadow:0 0 14px rgba(56,189,248,.2) !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] p,
[data-testid="stSidebar"] [data-testid="stPageLink"] span {
    font-size:14px !important; font-weight:600 !important; color:#E2E8F0 !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] p,
[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] span {
    color:#38BDF8 !important;
}
[data-testid="stSidebar"] hr{ border-color:#1E3A5F !important; margin:8px 0 !important; }
[data-testid="stSidebar"] [data-baseweb="select"]>div {
    background:#1E293B !important; border:1px solid #334155 !important;
    border-radius:10px !important; color:#F1F5F9 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"]>div:hover { border-color:#38BDF8 !important; }
[data-baseweb="popover"]>div { background:#1E293B !important; border:1px solid #334155 !important; }
[data-baseweb="option"]:hover { background:rgba(56,189,248,.15) !important; }
[data-testid="stSidebar"] .stSelectbox label {
    font-size:11px !important; color:#475569 !important;
    font-weight:700 !important; text-transform:uppercase; letter-spacing:.6px;
}
[data-testid="stSidebar"] .stRadio label {
    background:#1E293B !important; border:1px solid #334155 !important;
    border-radius:8px !important; padding:6px 12px !important;
    font-size:13px !important; color:#CBD5E1 !important; cursor:pointer !important;
    transition:all .2s !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    border-color:#38BDF8 !important; color:#38BDF8 !important;
}


/* HERO BANNER */
.hero {
    background:linear-gradient(135deg,#0B1120 0%,#1E293B 55%,#0B1120 100%);
    border:1px solid #1E3A5F; border-radius:18px;
    padding:30px 36px; text-align:center; margin-bottom:20px;
    position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,#38BDF8,#A855F7,#22C55E,#F97316);
}
.hero h1 { color:#FFFFFF !important; font-size:1.75rem; font-weight:800; margin:4px 0; }
.hero p  { color:#94A3B8 !important; font-size:.9rem; margin:6px 0 0; }
.hero .badge {
    display:inline-block; background:#1E3A5F;
    border:1px solid #38BDF8; border-radius:20px;
    padding:3px 14px; font-size:.72rem; color:#7DD3FC; margin-top:8px;
}


/* KPI CARDS */
.kpi-card {
    background:linear-gradient(145deg,#1E293B 0%,#162032 100%);
    border:1px solid #334155; border-radius:14px;
    padding:18px 12px; text-align:center;
    transition:all .3s; position:relative; overflow:hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,#38BDF8,#A855F7);
    border-radius:14px 14px 0 0;
}
.kpi-card:hover { transform:translateY(-3px); box-shadow:0 10px 28px rgba(56,189,248,.2); border-color:#38BDF8; }
.kpi-icon   { font-size:1.4rem; margin-bottom:3px; }
.kpi-value  { font-size:1.6rem; font-weight:800; color:#38BDF8; margin:3px 0; }
.kpi-label  { font-size:.68rem; color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:.6px; }
.kpi-sub    { font-size:.68rem; color:#4ADE80;  margin-top:4px; font-weight:500; }
.kpi-warn   { font-size:.68rem; color:#F59E0B;  margin-top:4px; font-weight:500; }
.kpi-danger { font-size:.68rem; color:#F87171;  margin-top:4px; font-weight:500; }


/* SECTION HEADER */
.sec-hdr {
    display:flex; align-items:center; gap:10px;
    background:linear-gradient(90deg,#1E293B,rgba(30,41,59,0));
    border-left:4px solid #38BDF8; color:#FFFFFF !important;
    padding:9px 18px; border-radius:0 10px 10px 0;
    font-size:.92rem; font-weight:700; margin:20px 0 12px; letter-spacing:.2px;
}


/* ── INSIGHT CARDS — SOLID HIGH-CONTRAST ─────────────────────────────────── */
.ins-obs {
    background:#E0F2FE;
    border-left:5px solid #0284C7;
    border-radius:0 10px 10px 0;
    padding:14px 18px; margin:8px 0;
}
.ins-obs b, .ins-obs strong {
    display:block; color:#0C4A6E !important;
    font-size:14px !important; font-weight:700 !important; margin-bottom:6px;
}
.ins-obs, .ins-obs span, .ins-obs li {
    color:#082F49 !important; font-size:14px !important;
    font-weight:500 !important; line-height:1.65 !important;
}


.ins-impact {
    background:#FFF7ED;
    border-left:5px solid #EA580C;
    border-radius:0 10px 10px 0;
    padding:14px 18px; margin:8px 0;
}
.ins-impact b, .ins-impact strong {
    display:block; color:#9A3412 !important;
    font-size:14px !important; font-weight:700 !important; margin-bottom:6px;
}
.ins-impact, .ins-impact span, .ins-impact li {
    color:#7C2D12 !important; font-size:14px !important;
    font-weight:500 !important; line-height:1.65 !important;
}


.ins-rec {
    background:#F0FDF4;
    border-left:5px solid #16A34A;
    border-radius:0 10px 10px 0;
    padding:14px 18px; margin:8px 0;
}
.ins-rec b, .ins-rec strong {
    display:block; color:#166534 !important;
    font-size:14px !important; font-weight:700 !important; margin-bottom:6px;
}
.ins-rec, .ins-rec span, .ins-rec li {
    color:#14532D !important; font-size:14px !important;
    font-weight:500 !important; line-height:1.65 !important;
}


/* SELECTOR CARDS */
.sel-wrap { display:flex; gap:8px; flex-wrap:wrap; margin:8px 0 16px; }
.sel-card {
    background:#1E293B; border:1.5px solid #334155; border-radius:10px;
    padding:8px 15px; font-size:12px; font-weight:600;
    color:#94A3B8; white-space:nowrap; cursor:default;
}
.sel-card.active {
    background:#1E3A5F; border-color:#38BDF8;
    color:#38BDF8; box-shadow:0 0 14px rgba(56,189,248,.2);
}


/* STAT CARD */
.stat-card {
    background:#1E293B; border:1px solid #334155; border-radius:10px;
    padding:14px; text-align:center;
}
.stat-card:hover { border-color:#38BDF8; }


/* MGMT CARD */
.mgmt-card {
    background:linear-gradient(145deg,#1E293B,#162032);
    border:1px solid #334155; border-radius:12px;
    padding:18px; margin:8px 0; transition:all .25s;
}
.mgmt-card:hover { border-color:#38BDF8; box-shadow:0 4px 18px rgba(56,189,248,.1); }
.mgmt-title { font-size:.88rem; font-weight:700; margin-bottom:8px; color:#F1F5F9; }


/* QUICK INSIGHT PANEL */
.qi-panel {
    background:#1E293B; border:1px solid #334155;
    border-radius:12px; padding:16px 20px; margin:6px 0;
}
.qi-panel h4 {
    color:#38BDF8 !important; font-size:.82rem; font-weight:700;
    text-transform:uppercase; letter-spacing:.8px; margin:0 0 10px;
}
.qi-item {
    display:flex; align-items:flex-start; gap:8px;
    color:#CBD5E1 !important; font-size:.88rem; font-weight:500;
    line-height:1.5; margin:6px 0;
}
.qi-dot { font-size:1rem; flex-shrink:0; }


/* DATAFRAME */
[data-testid="stDataFrame"] { border-radius:10px !important; overflow:hidden; }


/* EXPANDER */
[data-testid="stExpander"] {
    background:#1E293B !important; border:1px solid #334155 !important;
    border-radius:10px !important;
}
[data-testid="stExpander"] summary { color:#F1F5F9 !important; font-weight:600 !important; }


/* SCROLLBAR */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#0B1120; }
::-webkit-scrollbar-thumb { background:#334155; border-radius:2px; }
::-webkit-scrollbar-thumb:hover { background:#38BDF8; }
</style>
"""


def apply_styles():
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_nav():
    with st.sidebar:
        st.markdown("""
        <div class='sb-brand'>
            <div style='font-size:1.8rem'>📦</div>
            <h2>Supply Chain</h2>
            <p>Loss Analysis Dashboard</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='nav-lbl'>Pages</div>", unsafe_allow_html=True)
        st.page_link("app.py",                  label="🏠  Home")
        st.page_link("pages/1_Univariate.py",   label="📊  Univariate Analysis")
        st.page_link("pages/2_Bivariate.py",    label="📈  Bivariate Analysis")
        st.page_link("pages/3_Multivariate.py", label="🔥  Multivariate Analysis")
        st.page_link("pages/4_Dashboard.py",    label="🎯  Executive Dashboard")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            "<small style='color:#475569;font-size:11px;'>"
            "📁 supply_chain_cleaned.csv<br>"
            "📌 180,519 records · 45 columns</small>",
            unsafe_allow_html=True)


def kpi(icon, label, value, sub, cls="kpi-sub"):
    safe = sub.replace("<", "&#60;").replace(">", "&#62;")
    return (f"<div class='kpi-card'>"
            f"<div class='kpi-icon'>{icon}</div>"
            f"<div class='kpi-value'>{value}</div>"
            f"<div class='kpi-label'>{label}</div>"
            f"<div class='{cls}'>{safe}</div></div>")


def sec(icon, title):
    return f"<div class='sec-hdr'><span>{icon}</span><span>{title}</span></div>"


def ins(kind, heading, body):
    icons = {"obs": "📊", "impact": "🔥", "rec": "✅"}
    return (f"<div class='ins-{kind}'>"
            f"<b>{icons[kind]} {heading}</b>"
            f"<span>{body}</span>"
            f"</div>")


def quick_insights(title, items, dots):
    """Compact insight panel — items & dots are parallel lists."""
    rows = "".join(
        f"<div class='qi-item'><span class='qi-dot'>{d}</span><span>{t}</span></div>"
        for d, t in zip(dots, items)
    )
    return f"<div class='qi-panel'><h4>{title}</h4>{rows}</div>"


def sel_cards(options, active):
    parts = []
    for o in options:
        cls = "sel-card active" if o == active else "sel-card"
        parts.append(f"<div class='{cls}'>{o}</div>")
    return "<div class='sel-wrap'>" + "".join(parts) + "</div>"
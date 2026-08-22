"""
ProStartup Idea Validator — Streamlit Frontend
==============================================
Frontend redesign only.
Backend agents, prompts, LLM config, pipeline, schemas,
PDF generator, and conversational-agent logic are UNCHANGED.
"""

import sys
import os
import base64

# Ensure root directory is on sys.path for backend imports
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

import streamlit as st
import json
import uuid

# ─────────────────────────────────────────────────────────────────────────────
# BACKEND IMPORTS — DO NOT MODIFY
# ─────────────────────────────────────────────────────────────────────────────
from agents.web_search_agent import run_web_search_agent
from agents.market_analysis_agent import run_market_agent
from agents.competitor_agent import run_competitor_agent
from agents.swot_risk_agent import run_swot_agent
from agents.mvp_recommendation_agent import run_mvp_agent
from agents.gtm_strategy_agent import run_gtm_agent
from agents.report_agent import run_report_agent
from agents.conversational_advisor import run_conversational_advisor
from pdf_generator.generate_pdf import generate_pdf


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProStartup — AI Startup Idea Validator",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults: dict = {
    "page": "landing",
    "startup": "",
    "domain": "",
    "location": "",
    "report_result": None,
    "pdf_path": None,
    "web_result": None,
    "market_result": None,
    "competitor_result": None,
    "swot_result": None,
    "mvp_result": None,
    "gtm_result": None,
    "chat_open": False,
    "chat_messages": [],
    "chat_thread_id": str(uuid.uuid4()),
    "chat_initialized": False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─────────────────────────────────────────────────────────────────────────────
# ASSETS
# ─────────────────────────────────────────────────────────────────────────────
_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_HERO_IMG_PATH = os.path.join(_ASSETS_DIR, "prostartup_hero.png")


@st.cache_data(show_spinner=False)
def _img_to_base64(path: str) -> str:
    """Read an image file from disk and return a base64 data URI (cached)."""
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(path)[1].lstrip(".").lower() or "png"
        return f"data:image/{ext};base64,{encoded}"
    except Exception:
        return ""


_HERO_IMG_DATA_URI = _img_to_base64(_HERO_IMG_PATH)

# Small tiled honeycomb pattern as a data-URI background (used on the dashboard header)
_HONEYCOMB_PATTERN_SVG = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(
        b"""<svg xmlns='http://www.w3.org/2000/svg' width='64' height='74' viewBox='0 0 64 74'>
<g fill='none' stroke='%23F4B942' stroke-opacity='0.35' stroke-width='1.4'>
<polygon points='32,2 60,18 60,50 32,66 4,50 4,18'/>
</g>
</svg>""".replace(b"%23", b"#")
    ).decode("utf-8")
)


# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE FONTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — HONEY BEE THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>

/* ── RESET & BASE ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFF9EE !important;
    font-family: 'Manrope', sans-serif !important;
}

.block-container {
    padding-top: 0.6rem !important;
    max-width: 1080px !important;
}

/* Hide default Streamlit chrome */
header[data-testid="stHeader"]  { display: none !important; }
footer                           { display: none !important; }
#MainMenu                        { display: none !important; }

/* Tighten default Streamlit vertical gaps between blocks */
[data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
div.element-container { margin-bottom: 0 !important; }

/* ── TYPOGRAPHY ───────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 800;
    color: #202433 !important;
}
p, span, li, div {
    font-family: 'Manrope', sans-serif !important;
}
.stMarkdown p, .stMarkdown li {
    color: #2B2B2B;
    line-height: 1.65;
}

/* ── PRIMARY BUTTON (Honey Gold, pill) ───────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #F4B942 0%, #e8a832 100%) !important;
    color: #202433 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 13px 32px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    font-family: 'Manrope', sans-serif !important;
    cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(244, 185, 66, 0.38) !important;
    transition: all 0.22s cubic-bezier(.4,0,.2,1) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(244, 185, 66, 0.55) !important;
    background: linear-gradient(135deg, #FFD978 0%, #F4B942 100%) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── RECTANGULAR SAAS ACTION BUTTONS (Ask Hive AI / New Idea) ──
   Targeted via marker-div + adjacent-sibling trick so we don't
   have to touch every pill CTA button on the page.               */
.rect-btn-ask + div .stButton > button,
.rect-btn-new + div .stButton > button {
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-size: 13.5px !important;
    box-shadow: none !important;
    letter-spacing: 0 !important;
}
.rect-btn-ask + div .stButton > button {
    background: #FFF3CD !important;
    border: 1.5px solid #F4B942 !important;
    color: #202433 !important;
}
.rect-btn-ask + div .stButton > button:hover {
    background: #FFE9A8 !important;
    transform: none !important;
    box-shadow: 0 2px 8px rgba(244,185,66,0.35) !important;
}
.rect-btn-new + div .stButton > button {
    background: #FFFDF7 !important;
    border: 1.5px solid #E4DBC4 !important;
    color: #202433 !important;
}
.rect-btn-new + div .stButton > button:hover {
    background: #FFF9EE !important;
    border-color: #C9BC93 !important;
    transform: none !important;
    box-shadow: 0 2px 8px rgba(32,36,51,0.10) !important;
}

/* ── BACK BUTTON (cute rounded square icon) ───────────────── */
.back-btn-marker + div .stButton > button {
    border-radius: 12px !important;
    padding: 8px 12px !important;
    font-size: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    background: #FFFFFF !important;
    border: 1.5px solid #EDD9A3 !important;
    color: #202433 !important;
    min-width: 38px !important;
    line-height: 1 !important;
}
.back-btn-marker + div .stButton > button:hover {
    background: #FFF3CD !important;
    border-color: #F4B942 !important;
    transform: none !important;
    box-shadow: 0 4px 12px rgba(244,185,66,0.25) !important;
}

/* ── BACK BUTTON (cute rounded square icon) ───────────────── */
.back-btn-marker + div .stButton > button {
    border-radius: 12px !important;
    padding: 8px 12px !important;
    font-size: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    background: #FFFFFF !important;
    border: 1.5px solid #EDD9A3 !important;
    color: #202433 !important;
    min-width: 38px !important;
    line-height: 1 !important;
}
.back-btn-marker + div .stButton > button:hover {
    background: #FFF3CD !important;
    border-color: #F4B942 !important;
    transform: none !important;
    box-shadow: 0 4px 12px rgba(244,185,66,0.25) !important;
}

/* ── DASHBOARD CARDS ──────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, #1a1d2b 0%, #202433 55%, #2d3450 100%);
    border-radius: 20px;
    padding: 22px 30px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(32,36,51,0.25);
}
.dash-header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;
    position: relative;
    z-index: 1;
}
.dash-header-left {
    min-width: 240px;
}
.dash-header-left p {
    color: #F4B942;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    font-family: Manrope, sans-serif;
    margin: 0 0 4px;
}
.dash-header-left h1 {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.15;
    font-family: Manrope, sans-serif;
    margin: 0;
}
.dash-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.dash-meta-item {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    padding: 8px 16px;
    min-width: 110px;
}
.dash-meta-item.gold {
    background: rgba(244,185,66,0.16);
    border: 1px solid rgba(244,185,66,0.35);
}
.dash-meta-item p:first-child {
    margin: 0;
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-family: Manrope, sans-serif;
}
.dash-meta-item p:last-child {
    margin: 2px 0 0;
    font-size: 13px;
    font-weight: 700;
    color: #FFFFFF;
    font-family: Manrope, sans-serif;
}
.dash-meta-item.gold p:first-child {
    color: #FFD978;
}

.report-card {
    background: white;
    border-radius: 24px;
    padding: 32px 38px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border: 1px solid rgba(244,185,66,0.15);
    margin-bottom: 16px;
}
.report-title {
    font-size: 24px;
    font-weight: 800;
    color: #202433;
    font-family: Manrope, sans-serif;
    margin-bottom: 20px;
}

.section-card {
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.section-card.overview {
    background: linear-gradient(135deg, #FFF9EE, #FFF3CD);
    border: 1px solid rgba(244,185,66,0.15);
}
.section-card.market {
    background: linear-gradient(135deg, #F5F9FF, #EDF4FF);
    border: 1px solid rgba(66,133,244,0.12);
}
.section-card.competitor {
    background: linear-gradient(135deg, #FFF9EE, #FFF3CD);
    border: 1px solid rgba(244,185,66,0.15);
}
.section-card.swot {
    background: white;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.section-card.mvp {
    background: linear-gradient(135deg, #F0FDF4, #E8F5E9);
    border: 1px solid rgba(76,175,80,0.15);
}
.section-card.gtm {
    background: linear-gradient(135deg, #F3E5F5, #EDE7F6);
    border: 1px solid rgba(156,39,176,0.10);
}
.section-card.final {
    background: linear-gradient(135deg, #FFF9EE, #FFF3CD);
    border: 1px solid rgba(244,185,66,0.40);
    box-shadow: 0 8px 24px rgba(244,185,66,0.18);
}
.section-label {
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 14px;
    font-family: Manrope, sans-serif;
}
.section-label.overview { color: #6B4E0E; }
.section-label.market { color: #1a73e8; }
.section-label.competitor { color: #6B4E0E; }
.section-label.swot { color: #202433; }
.section-label.mvp { color: #2E7D32; }
.section-label.gtm { color: #4527A0; }
.section-label.final { color: #7A5A0E; }

/* ── DOWNLOAD BUTTON (Deep Navy) ─────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #202433 0%, #2d3450 100%) !important;
    color: #FFF9EE !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 36px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    font-family: 'Manrope', sans-serif !important;
    box-shadow: 0 4px 16px rgba(32, 36, 51, 0.35) !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(32, 36, 51, 0.45) !important;
}

/* ── FORM INPUTS ──────────────────────────────────────────── */
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 2px solid #EDD9A3 !important;
    border-radius: 16px !important;
    color: #202433 !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #F4B942 !important;
    box-shadow: 0 0 0 3px rgba(244, 185, 66, 0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 2px solid #EDD9A3 !important;
    border-radius: 14px !important;
    color: #202433 !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    height: 50px !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #F4B942 !important;
    box-shadow: 0 0 0 3px rgba(244, 185, 66, 0.15) !important;
}
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 2px solid #EDD9A3 !important;
    border-radius: 14px !important;
    font-family: 'Manrope', sans-serif !important;
    min-height: 50px !important;
    transition: border-color 0.2s ease !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #F4B942 !important;
    box-shadow: 0 0 0 3px rgba(244, 185, 66, 0.15) !important;
}
.stTextArea label,
.stTextInput label,
.stSelectbox label {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    color: #202433 !important;
    font-size: 14px !important;
}

/* ── PROGRESS BAR ─────────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, #F4B942, #FFD978) !important;
    border-radius: 100px !important;
}
.stProgress > div {
    background: #F0E6C8 !important;
    border-radius: 100px !important;
}

/* ── SPINNER ──────────────────────────────────────────────── */
.stSpinner > div { color: #F4B942 !important; }

/* ── ALERTS ───────────────────────────────────────────────── */
.stAlert { border-radius: 14px !important; font-family: 'Manrope', sans-serif !important; }

/* ── FORM SUBMIT BUTTON (chat send) ──────────────────────── */
.stForm .stButton > button {
    padding: 10px 18px !important;
    font-size: 18px !important;
    border-radius: 12px !important;
}

/* ── ANIMATIONS ───────────────────────────────────────────── */
@keyframes beeBob {
    0%, 100% { transform: translateY(0) rotate(-4deg); }
    50%       { transform: translateY(-10px) rotate(4deg); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseSoft {
    0%, 100% { opacity: 0.07; }
    50%       { opacity: 0.13; }
}
@keyframes glowPulse {
    0%, 100% { opacity: 0.16; }
    50%       { opacity: 0.30; }
}

</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# ROBUST DEEP-SEARCH HELPERS (for TAM / SAM / SOM extraction)
# ─────────────────────────────────────────────────────────────────────────────
def _key_matches(key: str, keywords: list) -> bool:
    kl = str(key).lower().replace(" ", "_").replace("-", "_")
    for kw in keywords:
        kwn = kw.lower().replace(" ", "_")
        if kl == kwn or kl.startswith(kwn + "_") or kl.endswith("_" + kwn) or f"_{kwn}_" in f"_{kl}_":
            return True
    return False


def _stringify_value(v):
    """Turn a scalar or a small dict/list into a short display string."""
    if v is None:
        return None
    if isinstance(v, (str, int, float)):
        s = str(v).strip()
        return s if s else None
    if isinstance(v, dict):
        for subk in ("value", "amount", "size", "total", "estimate", "figure"):
            if subk in v and isinstance(v[subk], (str, int, float)):
                return str(v[subk]).strip()
        return None
    return None


def _deep_find(obj, keywords: list, _depth: int = 0):
    """Recursively search a nested dict/list for the first key matching
    `keywords` and return a short display-ready value. Returns None if
    nothing matches anywhere in the structure."""
    if _depth > 8 or obj is None:
        return None
    if isinstance(obj, dict):
        # First pass: direct key match at this level (shallowest wins)
        for k, v in obj.items():
            if _key_matches(k, keywords):
                s = _stringify_value(v)
                if s:
                    return s
        # Second pass: recurse into children
        for v in obj.values():
            found = _deep_find(v, keywords, _depth + 1)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _deep_find(item, keywords, _depth + 1)
            if found:
                return found
    return None


def _get_tam_sam_som() -> dict:
    """Search every result object we have (market_result, report_result,
    and its nested summaries) for TAM / SAM / SOM values, however the
    backend happens to have nested them."""
    sources = [
        st.session_state.market_result,
        (st.session_state.report_result or {}).get("market_analysis"),
        st.session_state.report_result,
    ]
    keyword_map = {
        "TAM": ["tam", "total_addressable_market"],
        "SAM": ["sam", "serviceable_addressable_market"],
        "SOM": ["som", "serviceable_obtainable_market"],
    }
    out = {}
    for label, kws in keyword_map.items():
        val = None
        for src in sources:
            val = _deep_find(src, kws)
            if val:
                break
        out[label] = val or "—"
    return out


def _extract_score(final: dict):
    """Try to pull a numeric-ish overall score (e.g. '8/10', '82%', '7.5')."""
    raw = final.get("overall_score", "")
    if not raw:
        return None, None
    raw_str = str(raw).strip()
    try:
        if "/" in raw_str:
            num, den = raw_str.split("/")
            pct = max(0, min(100, float(num.strip()) / float(den.strip()) * 100))
            return raw_str, pct
        if "%" in raw_str:
            pct = max(0, min(100, float(raw_str.replace("%", "").strip())))
            return raw_str, pct
        val = float(raw_str)
        pct = max(0, min(100, val * 10 if val <= 10 else val))
        return raw_str, pct
    except Exception:
        return raw_str, None


# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION HELPER
# ─────────────────────────────────────────────────────────────────────────────
def go(page: str) -> None:
    st.session_state.page = page
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SHARED COMPONENT — NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_navbar(show_back: bool = False) -> None:
    c_logo, c_gap, c_btn = st.columns([2, 7, 1])
    with c_logo:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:9px;padding:10px 0 6px;">'
            '<span style="font-size:26px;">🐝</span>'
            '<span style="font-size:19px;font-weight:800;color:#202433;'
            'letter-spacing:-0.3px;font-family:Manrope,sans-serif;">PROSTARTUP</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    if show_back:
        with c_btn:
            st.markdown(
                '<div class="back-btn-marker"></div>',
                unsafe_allow_html=True,
            )
            if st.button("←", key="nav_back_btn", help="Back to home"):
                go("landing")


# ─────────────────────────────────────────────────────────────────────────────
# SHARED COMPONENT — BEE MASCOT (fixed, always visible)
# ─────────────────────────────────────────────────────────────────────────────
def render_bee_mascot() -> None:
    st.markdown(
        """
<style>
.bee-mascot-wrap {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 9999;
    animation: beeBob 2.8s ease-in-out infinite;
    cursor: default;
    user-select: none;
}
.bee-mascot-body {
    width: 58px;
    height: 58px;
    background: linear-gradient(145deg, #F4B942, #e8a832);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 6px 24px rgba(244,185,66,0.55);
    border: 3px solid rgba(255,255,255,0.85);
}
.bee-mascot-tooltip {
    position: absolute;
    bottom: 68px;
    right: 0;
    background: #202433;
    color: white !important;
    padding: 7px 14px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    box-shadow: 0 4px 14px rgba(0,0,0,0.22);
    font-family: Manrope, sans-serif;
}
.bee-mascot-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    right: 16px;
    border: 6px solid transparent;
    border-top-color: #202433;
}
.bee-mascot-wrap:hover .bee-mascot-tooltip { opacity: 1; }
</style>
<div class="bee-mascot-wrap">
    <div class="bee-mascot-body">🐝</div>
    <div class="bee-mascot-tooltip">Need help? Ask Hive AI 🐝</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# INLINE HELPER — bullet list item
# ─────────────────────────────────────────────────────────────────────────────
def _bullet(text: str, dot_color: str = "#F4B942", border: bool = True) -> str:
    border_style = "border-bottom:1px solid #F5EDD4;" if border else ""
    return (
        f'<div style="display:flex;align-items:flex-start;gap:10px;'
        f'padding:6px 0;{border_style}">'
        f'<div style="width:7px;height:7px;min-width:7px;background:{dot_color};'
        f'border-radius:50%;margin-top:7px;"></div>'
        f'<p style="font-size:14px;color:#2B2B2B;margin:0;line-height:1.55;'
        f'font-family:Manrope,sans-serif;">{text}</p>'
        f'</div>'
    )


def _section_header(icon: str, title: str) -> str:
    return (
        f'<div style="border-left:4px solid #F4B942;padding-left:20px;margin-bottom:16px;">'
        f'<h3 style="font-size:17px;font-weight:800;color:#202433;'
        f'font-family:Manrope,sans-serif;margin-bottom:10px;">{icon} {title}</h3>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — LANDING
# ─────────────────────────────────────────────────────────────────────────────
def render_landing() -> None:
    render_navbar()

    # ── Hero ──────────────────────────────────────────────────────────────────
    col_text, col_svg = st.columns([1, 1], gap="large")

    with col_text:
        st.markdown(
            """
<div style="padding:30px 0 22px;animation:fadeInUp 0.55s ease;">

  <div style="
    display:inline-flex;align-items:center;gap:8px;
    background:#FFF3CD;border:1.5px solid #F4B942;border-radius:100px;
    padding:8px 22px;font-size:14px;font-weight:700;color:#8B6914;
    margin-bottom:26px;letter-spacing:0.3px;font-family:Manrope,sans-serif;
  ">🐝 AI-Powered Startup Validation</div>

  <h1 style="
    font-size:62px;font-weight:800;color:#202433;
    line-height:1.08;margin-bottom:24px;font-family:Manrope,sans-serif;
  ">Make Your<br>Idea <span style="color:#F4B942;">Buzz.</span></h1>

  <p style="
    font-size:19px;color:#666;line-height:1.72;
    max-width:520px;margin-bottom:38px;font-family:Manrope,sans-serif;
  ">
    Validate your startup idea with AI-powered market intelligence,
    competitive insights, strategic analysis and actionable recommendations.
  </p>

</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("✨  Validate My Idea", key="hero_cta", use_container_width=True):
            go("input")

    with col_svg:
        if _HERO_IMG_DATA_URI:
            st.markdown(
                f'<div style="padding:12px 0;text-align:center;">'
                f'<img src="{_HERO_IMG_DATA_URI}" alt="ProStartup — AI startup idea validator"'
                f' style="max-width:480px;width:100%;height:auto;display:inline-block;'
                f'filter:drop-shadow(0 18px 34px rgba(244,185,66,0.30));" />'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            # Fallback if the asset can't be located on disk
            st.image(_HERO_IMG_PATH, use_container_width=True)

    render_bee_mascot()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — USER INPUT
# ─────────────────────────────────────────────────────────────────────────────
def render_input() -> None:
    render_navbar(show_back=True)

    # Subtle corner honeycomb decoration
    st.markdown(
        """
<div style="position:fixed;top:0;right:0;opacity:0.055;pointer-events:none;z-index:0;">
<svg width="220" height="220" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
  <polygon points="110,12 158,40 158,96 110,124 62,96 62,40"
           fill="none" stroke="#F4B942" stroke-width="5"/>
  <polygon points="165,46 213,74 213,130 165,158 117,130 117,74"
           fill="none" stroke="#F4B942" stroke-width="5"/>
  <polygon points="55,46 103,74 103,130 55,158 7,130 7,74"
           fill="none" stroke="#F4B942" stroke-width="5"/>
</svg>
</div>
""",
        unsafe_allow_html=True,
    )

    # Page header
    st.markdown(
        """
<div style="text-align:center;padding:18px 20px 10px;max-width:620px;
    margin:0 auto;animation:fadeInUp 0.5s ease;">
  <h1 style="font-size:33px;font-weight:800;color:#202433;
    line-height:1.2;margin-bottom:8px;font-family:Manrope,sans-serif;">
    Let's Put Your Idea in the Hive. 🐝
  </h1>
  <p style="font-size:16px;color:#777;line-height:1.65;
    font-family:Manrope,sans-serif;">
    Drop your idea here and let the magic happen. ✨
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # STARTUP IDEA INPUT CARD
    # ─────────────────────────────────────────────────────────────────────────

    _l, _c, _r = st.columns([0.5, 5, 0.5])

    with _c:

        # Use a real Streamlit container instead of an HTML div
        with st.container(border=True):

            startup_val = st.text_area(
                "💡 Your Startup Idea",
                placeholder="Describe your startup idea in a few sentences...",
                height=160,
                value=st.session_state.startup,
                key="input_startup",
                label_visibility="visible",
            )

            st.markdown(
                "<div style='height:8px'></div>",
                unsafe_allow_html=True,
            )

            clicked = st.button(
                "🍯  Start Validation",
                key="start_validation",
                use_container_width=True,
            )

    if clicked:
        _err = None
        if not startup_val.strip():
            _err = "🐝 We need your startup idea before sending it to the Hive."

        if _err:
            _el, _ec, _er = st.columns([0.5, 5, 0.5])
            with _ec:
                st.markdown(
                    f'<div style="background:#FFF3CD;border:1.5px solid #F4B942;'
                    f'border-radius:13px;padding:13px 18px;font-size:14px;font-weight:600;'
                    f'color:#8B6914;margin-top:10px;font-family:Manrope,sans-serif;">{_err}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.session_state.startup = startup_val.strip()
            if not st.session_state.domain:
                st.session_state.domain = "General"
            if not st.session_state.location:
                st.session_state.location = "Global"
            go("dashboard")

    render_bee_mascot()


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE RUNNER  (calls all existing backend agents, unchanged)
# ─────────────────────────────────────────────────────────────────────────────
def run_pipeline() -> bool:
    startup  = st.session_state.startup
    domain   = st.session_state.domain
    location = st.session_state.location

    _slot = st.empty()

    def _show(icon: str, msg: str, pct: int) -> None:
        _slot.markdown(
            f"""
<div style="background:white;border-radius:24px;padding:50px 40px;text-align:center;
    box-shadow:0 8px 32px rgba(0,0,0,0.08);border:1px solid rgba(244,185,66,0.18);
    max-width:520px;margin:40px auto;">
  <div style="font-size:54px;animation:beeBob 1.6s ease-in-out infinite;
    display:inline-block;margin-bottom:18px;">{icon}</div>
  <h2 style="font-size:21px;font-weight:800;color:#202433;
    font-family:Manrope,sans-serif;margin-bottom:8px;">Analyzing Your Startup</h2>
  <p style="font-size:14px;color:#999;font-family:Manrope,sans-serif;margin-bottom:26px;">
    {msg}
  </p>
  <div style="background:#F0E6C8;border-radius:100px;height:8px;overflow:hidden;margin-bottom:14px;">
    <div style="width:{pct}%;height:100%;
      background:linear-gradient(90deg,#F4B942,#FFD978);
      border-radius:100px;transition:width 0.5s ease;"></div>
  </div>
  <p style="font-size:12px;color:#bbb;font-family:Manrope,sans-serif;">
    This usually takes 1–3 minutes. Please don't close this window.
  </p>
</div>
""",
            unsafe_allow_html=True,
        )

    try:
        _show("🐝", "Gathering startup intelligence from the web...", 10)
        web_result = run_web_search_agent(startup)
        st.session_state.web_result = web_result

        _show("📊", "Analyzing the market landscape...", 28)
        market_result = run_market_agent(web_result)
        st.session_state.market_result = market_result

        _show("🏆", "Mapping the competitive landscape...", 45)
        competitor_result = run_competitor_agent(market_result)
        st.session_state.competitor_result = competitor_result

        _show("⚡", "Running SWOT & risk analysis...", 60)
        swot_result = run_swot_agent(competitor_result)
        st.session_state.swot_result = swot_result

        _show("🛠️", "Designing your MVP roadmap...", 72)
        mvp_result = run_mvp_agent(swot_result)
        st.session_state.mvp_result = mvp_result

        _show("📢", "Building your go-to-market strategy...", 83)
        gtm_result = run_gtm_agent(mvp_result)
        st.session_state.gtm_result = gtm_result

        _show("🧠", "Connecting the insights and generating report...", 93)
        report_result = run_report_agent(
            market_result, competitor_result,
            swot_result, mvp_result, gtm_result,
        )
        report_result["user_input"] = {
            "startup_idea": startup,
            "domain": domain,
            "location": location,
        }
        st.session_state.report_result = report_result

        _show("📄", "Generating your PDF report...", 98)
        pdf_path = generate_pdf(report_result)
        st.session_state.pdf_path = pdf_path

        _slot.empty()
        return True

    except Exception as exc:
        _slot.empty()
        st.error(
            f"🐝 Something went wrong while analyzing your idea. Please try again.\n\n**Error:** {exc}"
        )
        return False


# ─────────────────────────────────────────────────────────────────────────────
# CHAT HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _extract_advisor_text(response) -> str:
    """Pull plain text from run_conversational_advisor response."""
    try:
        content = response["messages"][-1].content
        if isinstance(content, list):
            content = " ".join(
                item["text"] if isinstance(item, dict) and "text" in item else str(item)
                for item in content
            )
        return str(content).strip()
    except Exception:
        return "I'm having trouble responding right now. Please try again."


def _init_chat() -> None:
    """Send startup context to the advisor and store its opening greeting."""
    if st.session_state.chat_initialized:
        return
    report_json = (
        json.dumps(st.session_state.report_result, indent=2)
        if st.session_state.report_result
        else "(analysis not yet available)"
    )
    init_msg = (
        f"I've just received a startup analysis. Here's the context:\n\n"
        f"Startup Idea: {st.session_state.startup}\n"
        f"Domain: {st.session_state.domain}\n"
        f"Location: {st.session_state.location}\n\n"
        f"Analysis Report Summary:\n{report_json}\n\n"
        f"Please briefly introduce yourself as Hive AI and confirm you're ready to help "
        f"me explore these results. Keep it friendly and concise (2-3 sentences)."
    )
    try:
        resp = run_conversational_advisor(init_msg, st.session_state.chat_thread_id)
        greeting = _extract_advisor_text(resp)
    except Exception:
        greeting = (
            "Hi! I'm Hive AI. 🐝 "
            "I've finished analyzing your startup — what would you like to explore?"
        )
    st.session_state.chat_messages = [{"role": "ai", "text": greeting}]
    st.session_state.chat_initialized = True


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD SUB-COMPONENTS — VISUAL CHARTS (real backend data only)
# ─────────────────────────────────────────────────────────────────────────────
def _render_tam_sam_som_funnel(tam: str, sam: str, som: str) -> None:
    """Three-tier funnel using real TAM/SAM/SOM values pulled from the backend."""
    _rows = [
        ("TAM", "Total Addressable Market", tam, "100%", "#202433", "#F4B942"),
        ("SAM", "Serviceable Addressable Market", sam, "72%", "#2d3450", "#FFD978"),
        ("SOM", "Serviceable Obtainable Market", som, "46%", "#3a4166", "#FFE9A8"),
    ]
    _html = '<div style="display:flex;flex-direction:column;align-items:center;gap:6px;margin:4px 0 6px;">'
    for _label, _sub, _val, _width, _bg, _text_c in _rows:
        _html += (
            f'<div style="width:{_width};background:{_bg};border-radius:12px;'
            f'padding:14px 18px;text-align:center;box-shadow:0 4px 14px rgba(32,36,51,0.14);">'
            f'<p style="margin:0;font-size:11px;font-weight:700;letter-spacing:0.6px;'
            f'color:{_text_c};text-transform:uppercase;font-family:Manrope,sans-serif;">{_label} · {_sub}</p>'
            f'<p style="margin:2px 0 0;font-size:19px;font-weight:800;color:white;'
            f'font-family:Manrope,sans-serif;">{_val}</p>'
            f'</div>'
        )
    _html += "</div>"
    st.markdown(_html, unsafe_allow_html=True)


def _render_score_gauge(display_val: str, pct) -> None:
    """A prominent circular score/viability gauge driven by real backend data."""
    if pct is None:
        pct = 70  # neutral fill when the score isn't numeric-parseable, label still shows real value
    _deg = max(0, min(360, pct * 3.6))
    st.markdown(
        f"""
<div style="text-align:center;">
  <div style="
      width:128px;height:128px;border-radius:50%;margin:0 auto 8px;
      background:conic-gradient(#F4B942 {_deg}deg, #EFE6D0 {_deg}deg 360deg);
      display:flex;align-items:center;justify-content:center;
      box-shadow:0 6px 20px rgba(244,185,66,0.30);">
    <div style="width:100px;height:100px;border-radius:50%;background:white;
        display:flex;flex-direction:column;align-items:center;justify-content:center;">
      <span style="font-size:22px;font-weight:800;color:#202433;font-family:Manrope,sans-serif;">{display_val}</span>
      <span style="font-size:10px;font-weight:700;color:#999;text-transform:uppercase;
        letter-spacing:0.5px;font-family:Manrope,sans-serif;">Score</span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — VALIDATION DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def render_dashboard() -> None:

    # Guard — if no startup text somehow, redirect to input
    if not st.session_state.startup:
        go("input")
        return

    # ── Run pipeline when no report yet ───────────────────────────────────────
    if st.session_state.report_result is None:
        render_navbar(show_back=True)
        success = run_pipeline()
        if not success:
            _bl, _bc, _br = st.columns([2, 2, 2])
            with _bc:
                if st.button("← Go back and try again", key="retry_btn"):
                    go("input")
            return
        st.rerun()

    report = st.session_state.report_result

    # ── Top nav ───────────────────────────────────────────────────────────────
    _nl, _ng, _nr = st.columns([2, 5, 3])
    with _nl:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:9px;padding:10px 0 6px;">'
            '<span style="font-size:24px;">🐝</span>'
            '<span style="font-size:18px;font-weight:800;color:#202433;'
            'font-family:Manrope,sans-serif;">PROSTARTUP</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    with _nr:
        _b1, _b2 = st.columns(2)
        with _b1:
            st.markdown('<div class="rect-btn-ask"></div>', unsafe_allow_html=True)
            if st.button("💬 Ask Hive AI", key="toggle_chat"):
                st.session_state.chat_open = not st.session_state.chat_open
                if st.session_state.chat_open:
                    _init_chat()
                st.rerun()
        with _b2:
            st.markdown('<div class="rect-btn-new"></div>', unsafe_allow_html=True)
            if st.button("+ New Idea", key="new_idea_btn"):
                for _k in [
                    "report_result", "pdf_path", "web_result", "market_result",
                    "competitor_result", "swot_result", "mvp_result", "gtm_result",
                    "chat_messages", "chat_initialized",
                ]:
                    st.session_state[_k] = [] if _k == "chat_messages" else None
                st.session_state.chat_open = False
                st.session_state.chat_initialized = False
                st.session_state.chat_thread_id = str(uuid.uuid4())
                go("input")

    # ── Dashboard header card ──────────────────────────────────────────────────
    st.markdown(
        f'<div class="dash-header">'
        f'<div class="dash-header-inner">'
        f'<div class="dash-header-left">'
        f'<p>🐝 PROSTARTUP</p>'
        f'<h1>AI Startup Validation Report</h1>'
        f'</div>'
        f'<div class="dash-meta">'
        f'<div class="dash-meta-item">'
        f'<p>Startup Idea</p>'
        f'<p>{st.session_state.startup[:70] + ("…" if len(st.session_state.startup) > 70 else "")}</p>'
        f'</div>'
        f'<div class="dash-meta-item gold">'
        f'<p>Domain</p>'
        f'<p>{st.session_state.domain}</p>'
        f'</div>'
        f'<div class="dash-meta-item">'
        f'<p>Location</p>'
        f'<p>{st.session_state.location}</p>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Unified AI Validation Report card ─────────────────────────────────────
    st.markdown(
        '<div class="report-card">'
        '<div class="report-title">🍯 AI Validation Report</div>',
        unsafe_allow_html=True,
    )

    # ── Section 1: Startup Overview ───────────────────────────────────────────
    overview = report.get("startup_overview", {})
    st.markdown('<div class="section-card overview">', unsafe_allow_html=True)
    st.markdown('<div class="section-label overview">🚀 Startup Overview</div>', unsafe_allow_html=True)
    if overview.get("idea_summary"):
        st.markdown(
            f'<p style="font-size:15px;color:#2B2B2B;line-height:1.7;'
            f'font-family:Manrope,sans-serif;margin-bottom:10px;">'
            f'{overview["idea_summary"]}</p>',
            unsafe_allow_html=True,
        )
    if overview.get("problem_statement"):
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;line-height:1.65;'
            f'font-family:Manrope,sans-serif;margin-bottom:8px;">'
            f'<strong>Problem:</strong> {overview["problem_statement"]}</p>',
            unsafe_allow_html=True,
        )
    if overview.get("target_users"):
        _users = overview["target_users"]
        _users_str = ", ".join(_users) if isinstance(_users, list) else str(_users)
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;'
            f'font-family:Manrope,sans-serif;margin-bottom:0;">'
            f'<strong>Target Users:</strong> {_users_str}</p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 2: Market Analysis ─────────────────────────────────────────────
    market_summary = report.get("market_analysis", {})
    _tss = _get_tam_sam_som()
    st.markdown('<div class="section-card market">', unsafe_allow_html=True)
    st.markdown('<div class="section-label market">📊 Market Analysis</div>', unsafe_allow_html=True)
    _render_tam_sam_som_funnel(_tss["TAM"], _tss["SAM"], _tss["SOM"])
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if market_summary.get("market_opportunity"):
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;line-height:1.65;'
            f'font-family:Manrope,sans-serif;margin-bottom:10px;">'
            f'<strong>Market Opportunity:</strong> {market_summary["market_opportunity"]}</p>',
            unsafe_allow_html=True,
        )
    if market_summary.get("customer_demand"):
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;line-height:1.65;'
            f'font-family:Manrope,sans-serif;margin-bottom:10px;">'
            f'<strong>Customer Demand:</strong> {market_summary["customer_demand"]}</p>',
            unsafe_allow_html=True,
        )
    if market_summary.get("key_trends"):
        st.markdown(
            '<p style="font-size:13px;font-weight:700;color:#202433;'
            'font-family:Manrope,sans-serif;margin-bottom:8px;">Key Trends</p>',
            unsafe_allow_html=True,
        )
        _trends_html = "".join(
            _bullet(t) for t in market_summary["key_trends"]
        )
        st.markdown(_trends_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Competitor Analysis ─────────────────────────────────────────
    comp = report.get("competitor_analysis", {})
    st.markdown('<div class="section-card competitor">', unsafe_allow_html=True)
    st.markdown('<div class="section-label competitor">🏆 Competitive Landscape</div>', unsafe_allow_html=True)
    if comp.get("competitors"):
        _cards = ""
        for _c in comp["competitors"]:
            if isinstance(_c, dict):
                _name = _c.get("name", "")
                _desc = _c.get("description", _c.get("weakness", _c.get("strength", "")))
            else:
                _name, _desc = str(_c), ""
            _cards += (
                f'<div style="background:#FFFDF7;border:1px solid #EDD9A3;'
                f'border-radius:14px;padding:14px 16px;">'
                f'<p style="font-size:14px;font-weight:800;color:#202433;margin:0 0 4px;'
                f'font-family:Manrope,sans-serif;">🏢 {_name}</p>'
                f'<p style="font-size:12.5px;color:#666;margin:0;line-height:1.5;'
                f'font-family:Manrope,sans-serif;">{_desc}</p>'
                f'</div>'
            )
        st.markdown(
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));'
            f'gap:10px;">{_cards}</div>',
            unsafe_allow_html=True,
        )

    if comp.get("competitive_advantages"):
        st.markdown(
            '<p style="font-size:13px;font-weight:700;color:#202433;'
            'font-family:Manrope,sans-serif;margin:14px 0 8px;">Your Competitive Advantages</p>',
            unsafe_allow_html=True,
        )
        for _adv in comp["competitive_advantages"]:
            st.markdown(
                f'<div style="background:#E2F4EA;border-radius:10px;'
                f'padding:9px 14px;margin-bottom:7px;font-size:13px;'
                f'color:#2E7D32;font-weight:600;font-family:Manrope,sans-serif;">✓ {_adv}</div>',
                unsafe_allow_html=True,
            )
    if comp.get("market_gaps"):
        st.markdown(
            '<p style="font-size:13px;font-weight:700;color:#202433;'
            'font-family:Manrope,sans-serif;margin:14px 0 8px;">Market Gaps</p>',
            unsafe_allow_html=True,
        )
        for _gap in comp["market_gaps"]:
            st.markdown(
                f'<div style="background:#EDE7F6;border-radius:10px;'
                f'padding:9px 14px;margin-bottom:7px;font-size:13px;'
                f'color:#4527A0;font-weight:600;font-family:Manrope,sans-serif;">◆ {_gap}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 4: SWOT Analysis ───────────────────────────────────────────────
    swot = report.get("swot_analysis", {})
    st.markdown('<div class="section-card swot">', unsafe_allow_html=True)
    st.markdown('<div class="section-label swot">⚡ SWOT Analysis</div>', unsafe_allow_html=True)
    _sw1, _sw2 = st.columns(2, gap="medium")
    _swot_rows = [
        [
            (_sw1, "💪 Strengths",     swot.get("strengths", []),     "#E2F4EA", "#2E7D32"),
            (_sw2, "⚠️ Weaknesses",    swot.get("weaknesses", []),    "#FDE8E8", "#C62828"),
        ],
        [
            (_sw1, "🚀 Opportunities", swot.get("opportunities", []), "#EDE7F6", "#4527A0"),
            (_sw2, "🔥 Threats",       swot.get("threats", []),       "#FFF3E0", "#E65100"),
        ],
    ]
    for _row_pair in _swot_rows:
        for _col, _label, _items, _bg, _color in _row_pair:
            with _col:
                _li_html = "".join(
                    f'<li style="font-size:13px;color:#2B2B2B;padding:3px 0 3px 4px;'
                    f'font-family:Manrope,sans-serif;line-height:1.5;">{_it}</li>'
                    for _it in _items
                )
                st.markdown(
                    f'<div style="background:{_bg};border-radius:14px;'
                    f'padding:14px 18px;margin-bottom:10px;">'
                    f'<p style="font-size:11.5px;font-weight:800;color:{_color};'
                    f'text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;'
                    f'font-family:Manrope,sans-serif;">{_label}</p>'
                    f'<ul style="list-style:none;padding:0;margin:0;">{_li_html}</ul>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 5: MVP Recommendation ─────────────────────────────────────────
    mvp = report.get("mvp_recommendation", {})
    st.markdown('<div class="section-card mvp">', unsafe_allow_html=True)
    st.markdown('<div class="section-label mvp">🛠️ MVP Recommendation</div>', unsafe_allow_html=True)
    if mvp.get("development_focus"):
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;line-height:1.65;'
            f'font-family:Manrope,sans-serif;margin-bottom:12px;">'
            f'<strong>Development Focus:</strong> {mvp["development_focus"]}</p>',
            unsafe_allow_html=True,
        )
    _mv1, _mv2 = st.columns(2, gap="medium")
    with _mv1:
        st.markdown(
            '<p style="font-size:12px;font-weight:800;color:#2E7D32;'
            'text-transform:uppercase;letter-spacing:0.5px;'
            'font-family:Manrope,sans-serif;margin-bottom:8px;">✅ Core Features</p>',
            unsafe_allow_html=True,
        )
        for _f in mvp.get("core_features", []):
            st.markdown(_bullet(str(_f), dot_color="#4CAF50"), unsafe_allow_html=True)
    with _mv2:
        st.markdown(
            '<p style="font-size:12px;font-weight:800;color:#E65100;'
            'text-transform:uppercase;letter-spacing:0.5px;'
            'font-family:Manrope,sans-serif;margin-bottom:8px;">⏳ Defer to Later</p>',
            unsafe_allow_html=True,
        )
        for _f in mvp.get("features_to_delay", []):
            st.markdown(_bullet(str(_f), dot_color="#FF9800"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 6: Go-To-Market ───────────────────────────────────────────────
    gtm = report.get("go_to_market", {})
    st.markdown('<div class="section-card gtm">', unsafe_allow_html=True)
    st.markdown('<div class="section-label gtm">📢 Go-To-Market Strategy</div>', unsafe_allow_html=True)
    if gtm.get("positioning"):
        st.markdown(
            f'<p style="font-size:14px;color:#2B2B2B;line-height:1.65;'
            f'font-family:Manrope,sans-serif;margin-bottom:12px;">'
            f'<strong>Positioning:</strong> {gtm["positioning"]}</p>',
            unsafe_allow_html=True,
        )
    _g1, _g2 = st.columns(2, gap="medium")
    with _g1:
        if gtm.get("acquisition_channels"):
            st.markdown(
                '<p style="font-size:12px;font-weight:800;color:#4527A0;'
                'text-transform:uppercase;letter-spacing:0.5px;'
                'font-family:Manrope,sans-serif;margin-bottom:8px;">📣 Acquisition Channels</p>',
                unsafe_allow_html=True,
            )
            for _ch in gtm["acquisition_channels"]:
                st.markdown(
                    f'<div style="background:#EDE7F6;border-radius:10px;'
                    f'padding:9px 14px;margin-bottom:7px;font-size:13px;'
                    f'color:#4527A0;font-weight:600;font-family:Manrope,sans-serif;">→ {_ch}</div>',
                    unsafe_allow_html=True,
                )
    with _g2:
        if gtm.get("launch_strategy"):
            st.markdown(
                '<p style="font-size:12px;font-weight:800;color:#E65100;'
                'text-transform:uppercase;letter-spacing:0.5px;'
                'font-family:Manrope,sans-serif;margin-bottom:8px;">🚀 Launch Strategy</p>',
                unsafe_allow_html=True,
            )
            for _step in gtm["launch_strategy"]:
                st.markdown(_bullet(str(_step)), unsafe_allow_html=True)
    if gtm.get("customer_segments"):
        st.markdown(
            '<p style="font-size:12px;font-weight:800;color:#202433;'
            'text-transform:uppercase;letter-spacing:0.5px;'
            'font-family:Manrope,sans-serif;margin:12px 0 6px;">Target Segments</p>',
            unsafe_allow_html=True,
        )
        _segs_html = " ".join(
            f'<span style="display:inline-block;background:#FFF3CD;'
            f'border:1px solid #F4B942;border-radius:100px;padding:5px 14px;'
            f'font-size:12px;font-weight:600;color:#8B6914;margin:4px;'
            f'font-family:Manrope,sans-serif;">{_s}</span>'
            for _s in gtm["customer_segments"]
        )
        st.markdown(_segs_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 7: Final Recommendation ────────────────────────────────────────
    final = report.get("final_recommendation", {})
    st.markdown('<div class="section-card final">', unsafe_allow_html=True)
    st.markdown('<div class="section-label final">🎯 Final Recommendation</div>', unsafe_allow_html=True)
    _fr_l, _fr_r = st.columns([3, 1])
    with _fr_l:
        if final.get("startup_viability"):
            st.markdown(
                f'<p style="font-size:14px;color:#2B2B2B;line-height:1.7;'
                f'font-family:Manrope,sans-serif;margin-bottom:12px;">'
                f'{final["startup_viability"]}</p>',
                unsafe_allow_html=True,
            )
        if final.get("next_steps"):
            st.markdown(
                '<p style="font-size:12px;font-weight:800;color:#7A5A0E;'
                'text-transform:uppercase;letter-spacing:0.5px;'
                'font-family:Manrope,sans-serif;margin-bottom:10px;">Next Steps</p>',
                unsafe_allow_html=True,
            )
            for _i, _step in enumerate(final.get("next_steps", []), 1):
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;gap:10px;'
                    f'padding:8px 0;border-bottom:1px solid #F0E6C8;">'
                    f'<div style="width:24px;height:24px;min-width:24px;'
                    f'background:linear-gradient(135deg,#F4B942,#FFD978);'
                    f'border-radius:8px;display:flex;align-items:center;'
                    f'justify-content:center;font-size:11px;font-weight:800;'
                    f'color:#202433;font-family:Manrope,sans-serif;">{_i}</div>'
                    f'<p style="font-size:13px;color:#2B2B2B;margin:3px 0 0;'
                    f'font-family:Manrope,sans-serif;line-height:1.5;">{_step}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    with _fr_r:
        _display_val, _pct = _extract_score(final)
        if _display_val:
            _render_score_gauge(_display_val, _pct)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close main report card

    # ── Download PDF ──────────────────────────────────────────────────────────
    if st.session_state.pdf_path:
        _dl1, _dl2, _dl3 = st.columns([1, 2, 1])
        with _dl2:
            try:
                with open(st.session_state.pdf_path, "rb") as _pdf_file:
                    st.download_button(
                        label="⬇  Download Validation Report (PDF)",
                        data=_pdf_file,
                        file_name="Startup_Validation_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_pdf_btn",
                    )
            except Exception as _pdf_err:
                st.warning(f"PDF generated but could not be opened: {_pdf_err}")

    # ── Hive AI Chat Panel ────────────────────────────────────────────────────
    if st.session_state.chat_open:
        render_chat_panel()

    render_bee_mascot()


# ─────────────────────────────────────────────────────────────────────────────
# CHAT PANEL  (wired to existing run_conversational_advisor)
# ─────────────────────────────────────────────────────────────────────────────
def render_chat_panel() -> None:
    # Panel chrome
    st.markdown(
        """
<div style="background:linear-gradient(135deg,#202433,#2d3450);
    border-radius:18px 18px 0 0;padding:16px 22px;
    display:flex;align-items:center;gap:13px;max-width:680px;margin:10px auto 0;">
  <div style="width:40px;height:40px;
    background:linear-gradient(135deg,#F4B942,#FFD978);
    border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-size:22px;flex-shrink:0;">🐝</div>
  <div>
    <p style="color:white;font-size:15px;font-weight:700;
      font-family:Manrope,sans-serif;margin:0;">Hive AI</p>
    <p style="color:rgba(255,255,255,0.5);font-size:12px;
      font-family:Manrope,sans-serif;margin:0;">Your startup analysis assistant</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Messages
    _chat_wrap_l, _chat_wrap_c, _chat_wrap_r = st.columns([1, 6, 1])
    with _chat_wrap_c:
        st.markdown(
            '<div style="background:#FAFAFA;border:1px solid #EEE;'
            'border-top:none;padding:16px 20px;min-height:160px;max-height:340px;'
            'overflow-y:auto;">',
            unsafe_allow_html=True,
        )
        for _msg in st.session_state.chat_messages:
            if _msg["role"] == "ai":
                st.markdown(
                    f'<div style="background:#F5F5F5;border-radius:16px 16px 16px 4px;'
                    f'padding:11px 15px;margin:6px 0;display:inline-block;max-width:88%;'
                    f'font-size:14px;color:#202433;line-height:1.6;'
                    f'font-family:Manrope,sans-serif;">{_msg["text"]}</div><br>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="text-align:right;">'
                    f'<div style="background:linear-gradient(135deg,#F4B942,#FFD978);'
                    f'border-radius:16px 16px 4px 16px;'
                    f'padding:11px 15px;margin:6px 0;display:inline-block;max-width:80%;'
                    f'font-size:14px;color:#202433;line-height:1.6;'
                    f'font-family:Manrope,sans-serif;">{_msg["text"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # Input form
        with st.form("hive_chat_form", clear_on_submit=True):
            _inp_col, _btn_col = st.columns([6, 1])
            with _inp_col:
                _user_msg = st.text_input(
                    "chat_input_label",
                    placeholder="Ask anything about your startup...",
                    key="chat_text_input",
                    label_visibility="collapsed",
                )
            with _btn_col:
                _send = st.form_submit_button("→", use_container_width=True)

        if _send and _user_msg.strip():
            st.session_state.chat_messages.append(
                {"role": "user", "text": _user_msg.strip()}
            )
            with st.spinner("Hive AI is thinking... 🐝"):
                try:
                    _resp = run_conversational_advisor(
                        _user_msg.strip(),
                        st.session_state.chat_thread_id,
                    )
                    _ai_text = _extract_advisor_text(_resp)
                except Exception as _e:
                    _ai_text = f"Sorry, I encountered an issue. Please try again. ({_e})"
            st.session_state.chat_messages.append(
                {"role": "ai", "text": _ai_text}
            )
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
_page = st.session_state.page

if _page == "landing":
    render_landing()
elif _page == "input":
    render_input()
elif _page == "dashboard":
    render_dashboard()
else:
    render_landing()
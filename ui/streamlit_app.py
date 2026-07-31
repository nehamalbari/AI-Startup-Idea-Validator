import streamlit as st
import time

from agents.web_search_agent import run_web_search
from agents.market_analysis_agent import run_market_analysis

st.set_page_config(
    page_title="AI Startup Idea Validator",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for Professional Purple & White Theme with Perfect Background
st.markdown("""
<style>
    /* Main Background - Soft Lavender Gray */
    .stApp {
        background: #F8F6FC;
    }
    
    /* Gradient Purple Header */
    .header-gradient {
        background: linear-gradient(135deg, #4A148C 0%, #7B1FA2 40%, #9C27B0 70%, #AB47BC 100%);
        padding: 40px 30px 30px 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(74, 20, 140, 0.25);
    }
    
    .header-gradient h1 {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    
    .header-gradient p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.1rem !important;
        margin: 8px 0 0 0 !important;
        opacity: 0.9;
    }
    
    /* White Cards with Purple Accents */
    .card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 2px 16px rgba(74, 20, 140, 0.06);
        border: 1px solid rgba(74, 20, 140, 0.06);
        transition: all 0.2s ease;
        margin-bottom: 20px;
    }
    
    .card:hover {
        box-shadow: 0 4px 24px rgba(74, 20, 140, 0.1);
        border-color: rgba(74, 20, 140, 0.12);
    }
    
    .card-title {
        color: #4A148C;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Purple Metric Cards */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        border: 1px solid rgba(74, 20, 140, 0.08);
        box-shadow: 0 2px 12px rgba(74, 20, 140, 0.05);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4A148C, #9C27B0);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(74, 20, 140, 0.12);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #4A148C;
        margin: 8px 0 4px 0;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        color: #6A1B9A;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-sub {
        color: #9E9E9E;
        font-size: 12px;
        margin-top: 4px;
    }
    
    /* Purple Input Fields */
    .stTextInput > div > div > input {
        background: #FAF8FF;
        border: 2px solid #E8E0F0;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 15px;
        color: #1A1A1A;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7B1FA2;
        box-shadow: 0 0 0 4px rgba(123, 31, 162, 0.08);
        background: white;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #BDBDBD;
    }
    
    /* Purple Select Boxes */
    .stSelectbox > div > div {
        background: #FAF8FF;
        border: 2px solid #E8E0F0;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #7B1FA2;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #7B1FA2;
        box-shadow: 0 0 0 4px rgba(123, 31, 162, 0.08);
    }
    
    /* Purple Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6A1B9A 0%, #4A148C 100%);
        color: white;
        border: none;
        padding: 14px 32px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.2s ease;
        width: 100%;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 16px rgba(74, 20, 140, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(74, 20, 140, 0.3);
        background: linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Purple Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F5F0FA;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #E8E0F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        color: #6A1B9A;
        font-weight: 500;
        transition: all 0.2s ease;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(74, 20, 140, 0.06);
        color: #4A148C;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #4A148C !important;
        box-shadow: 0 2px 12px rgba(74, 20, 140, 0.1);
    }
    
    /* Purple Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9C27B0, #4A148C);
        border-radius: 8px;
    }
    
    .stProgress > div {
        background: #F0EBF5;
        border-radius: 8px;
    }
    
    /* Status Alerts with Purple */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #7B1FA2;
    }
    
    .stAlert > div {
        background: #FAF8FF !important;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #1A1A1A;
        font-weight: 600;
    }
    
    h3 {
        color: #4A148C;
        font-weight: 600;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #9C27B0, transparent);
        margin: 28px 0;
    }
    
    /* Purple Success Box */
    .success-box {
        background: #FAF8FF;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #7B1FA2;
        margin: 8px 0;
        color: #1A1A1A;
    }
    
    /* Purple Tags */
    .tag {
        display: inline-block;
        background: #F3E8FF;
        color: #4A148C;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 4px 4px 4px 0;
    }
    
    /* Segment Cards */
    .segment-card {
        background: #FAF8FF;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #F0EBF5;
        margin: 10px 0;
        transition: all 0.2s ease;
    }
    
    .segment-card:hover {
        background: #F5F0FA;
        border-color: #D4C4E8;
        transform: translateX(4px);
    }
    
    .segment-card strong {
        color: #4A148C;
        font-size: 16px;
    }
    
    .segment-card p {
        color: #4A4A4A;
        margin: 6px 0 0 0;
        font-size: 14px;
    }
    
    /* Trend Items */
    .trend-item {
        display: flex;
        align-items: center;
        padding: 10px 16px;
        margin: 6px 0;
        border-radius: 10px;
        background: white;
        border: 1px solid #F0EBF5;
        transition: all 0.2s ease;
    }
    
    .trend-item:hover {
        background: #FAF8FF;
        border-color: #D4C4E8;
        transform: translateX(4px);
    }
    
    .trend-bullet {
        color: #7B1FA2;
        margin-right: 12px;
        font-weight: 700;
        font-size: 18px;
    }
    
    /* Location Badge */
    .location-badge {
        background: linear-gradient(135deg, #7B1FA2, #4A148C);
        padding: 10px 24px;
        border-radius: 12px;
        display: inline-block;
        color: white;
        font-weight: 500;
        font-size: 16px;
        box-shadow: 0 4px 16px rgba(74, 20, 140, 0.2);
    }
    
    /* Info Boxes */
    .info-box {
        background: #FAF8FF;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #F0EBF5;
    }
    
    .info-box-label {
        color: #6A1B9A;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .info-box-value {
        color: #1A1A1A;
        font-size: 24px;
        font-weight: 600;
        margin-top: 4px;
    }
    
    /* Labels */
    .field-label {
        color: #4A148C;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
        display: block;
    }
    
    /* Main Container Padding */
    .main > div {
        padding: 0px 10px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F0EBF5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #9C27B0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7B1FA2;
    }
    
    /* Success message styling */
    .stSuccess {
        background: #F0EBF5 !important;
        border-radius: 12px !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background: #FFF8F0 !important;
        border-radius: 12px !important;
        border-left: 4px solid #FF9800 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="header-gradient">
    <h1>🚀 Startup Validator</h1>
    <p>AI-powered multi-agent analysis for your startup idea</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #

st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<span class="field-label">💡 Your Startup Idea</span>', unsafe_allow_html=True)
    startup = st.text_input(
        "",
        placeholder="e.g., AI Resume Builder, Smart Parking System",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<span class="field-label">🎯 Target Market</span>', unsafe_allow_html=True)
    
    col_industry, col_location = st.columns(2)
    
    with col_industry:
        industry = st.selectbox(
            "Industry",
            ["AI", "Healthcare", "FinTech", "Education", "Agriculture", "E-Commerce", "Other"],
            index=0,
            label_visibility="collapsed"
        )
    
    with col_location:
        location = st.selectbox(
            "Location",
            ["India", "USA", "Europe", "Global"],
            index=0,
            label_visibility="collapsed"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYZE BUTTON ---------------- #

analyze = st.button("🔍 Analyze Startup Idea", use_container_width=True)

# ---------------- ANALYSIS ---------------- #

if analyze:
    if startup == "":
        st.warning("⚠️ Please enter a startup idea to validate.")
        st.stop()
    
    # Progress
    st.markdown('<div class="card">', unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    steps = [
        ("🌐 Searching web for insights...", 25),
        ("📊 Analyzing market data...", 50),
        ("🧠 Generating AI recommendations...", 75),
        ("✅ Analysis complete!", 100)
    ]
    
    for step_text, progress_value in steps:
        status_placeholder.info(step_text)
        progress_bar.progress(progress_value)
        time.sleep(0.3)
    
    status_placeholder.empty()
    progress_bar.empty()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Execute agents
    with st.spinner("Processing your request..."):
        web_result =  run_web_search(startup)
        market_result = run_market_analysis(startup, industry, location)
    
    st.success("✅ Analysis complete! Check the results below.")
    st.divider()
    
    # ---------------- TABS ---------------- #
    
    tab1, tab2 = st.tabs(["🌐 Web Search Insights", "📈 Market Analysis Report"])
    
    # ---------------- WEB SEARCH TAB ---------------- #
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="card-title">🌐 Web Search Insights</span>', unsafe_allow_html=True)
        st.markdown("### 📈 Market Trends")
        for trend in web_result.market_trends:
            st.markdown(f" {trend}")

        st.divider()

        st.markdown("### 😟 Customer Pain Points")

        for pain in web_result.customer_pain_points:
            st.markdown(f" {pain}")

        st.divider()

        st.markdown("### 📰 Latest News")

        for news in web_result.latest_news:
            st.markdown(f" {news}")

        st.divider()

        st.markdown("### 💡 Industry Insights")

        for insight in web_result.industry_insights:
            st.markdown(f"💡 {insight}")

        st.markdown("</div>", unsafe_allow_html=True)


    
    # ---------------- MARKET ANALYSIS TAB ---------------- #
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Location
        st.markdown("### 📍 Target Location")
        st.markdown(f'<span class="location-badge">{market_result.location}</span>', unsafe_allow_html=True)
        
        st.divider()
        
        # Metrics
        st.markdown("### 📊 Market Size Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TAM</div>
                <div class="metric-value">{market_result.tam}</div>
                <div class="metric-sub">Total Addressable Market</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">SAM</div>
                <div class="metric-value">{market_result.sam}</div>
                <div class="metric-sub">Serviceable Addressable Market</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">SOM</div>
                <div class="metric-value">{market_result.som}</div>
                <div class="metric-sub">Serviceable Obtainable Market</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Growth & Maturity
        st.markdown("### 📈 Market Dynamics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-box-label">📊 Growth Rate</div>
                <div class="info-box-value">{market_result.growth_rate}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-box-label">📈 Market Maturity</div>
                <div class="info-box-value">{market_result.market_maturity}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Customer Segments
        st.markdown("### 👥 Customer Segments")
        
        for segment in market_result.customer_segments:
            st.markdown(f"""
            <div class="segment-card">
                <strong>{segment.name}</strong>
                <p>{segment.description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Key Trends
        st.markdown("### 🔥 Key Market Trends")
        
        for trend in market_result.key_trends:
            st.markdown(f"""
            <div class="trend-item">
                <span class="trend-bullet">✦</span>
                <span style="color: #1A1A1A;">{trend}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
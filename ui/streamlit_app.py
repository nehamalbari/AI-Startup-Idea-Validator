import streamlit as st
import time

from agents.web_search_agent import run_web_search
from agents.market_analysis_agent import run_market_analysis
from agents.swot_risk_agent import run_swot_analysis

st.set_page_config(
    page_title="AI Startup Idea Validator",
    page_icon="🚀",
    layout="wide"
)

# ==================== PROFESSIONAL LAVENDER & WHITE THEME ====================
st.markdown("""
<style>
    /* ----- BASE ----- */
    .stApp {
        background: #f3edf9;
    }
    
    /* ----- GLASS HEADER ----- */
    .header-gradient {
        background: linear-gradient(145deg, #4a1a7a, #7b2fbe, #9c4dcc, #b87ad4);
        padding: 2rem 2.8rem;
        border-radius: 32px;
        margin-bottom: 1.5rem;
        box-shadow: 0 16px 40px -12px rgba(74, 20, 140, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .header-gradient h1 {
        color: white !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .header-gradient p {
        color: rgba(255, 255, 255, 0.92) !important;
        font-size: 1.15rem !important;
        margin: 4px 0 0 0 !important;
        font-weight: 400;
    }
    
    .header-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(4px);
        padding: 0.5rem 1.6rem;
        border-radius: 60px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ----- GLASS CARDS ----- */
    .card {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 1.5rem 1.8rem;
        box-shadow: 0 8px 28px -8px rgba(74, 20, 140, 0.07), 0 0 0 1px rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 1.2rem;
        transition: all 0.25s ease;
    }
    
    .card:hover {
        box-shadow: 0 16px 36px -12px rgba(74, 20, 140, 0.12);
        border-color: rgba(106, 27, 154, 0.12);
    }
    
    .card-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #3b0b6e;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
    }
    
    /* ----- INPUTS ----- */
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e8e0f0;
        border-radius: 16px;
        padding: 0.9rem 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.2s;
        color: #1c1b1e;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7b1fa2;
        box-shadow: 0 0 0 4px rgba(123, 31, 162, 0.08);
        background: white;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #b0a8b8;
        font-weight: 400;
    }
    
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e8e0f0;
        border-radius: 16px;
        transition: all 0.2s;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        padding: 0.1rem 0.3rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #7b1fa2;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #7b1fa2;
        box-shadow: 0 0 0 4px rgba(123, 31, 162, 0.08);
    }
    
    .stSelectbox > div > div > div {
        font-size: 1rem;
        font-weight: 500;
    }
    
    .field-label {
        display: block;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #4a148c;
        margin-bottom: 6px;
    }
    
    /* ----- BUTTON ----- */
    .stButton > button {
        background: linear-gradient(145deg, #6a1b9a, #4a148c) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2.4rem !important;
        border-radius: 60px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.4px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 8px 24px -6px rgba(74, 20, 140, 0.35) !important;
        width: 100% !important;
        height: auto !important;
        line-height: 1.5 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 16px 36px -8px rgba(74, 20, 140, 0.45) !important;
        background: linear-gradient(145deg, #7b1fa2, #4a148c) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button:active {
        transform: scale(0.97) !important;
    }
    
    .stButton > button:focus {
        border: none !important;
        outline: none !important;
    }
    
    /* ----- METRIC CARDS ----- */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 0.6rem 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 1.4rem 0.8rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(74, 20, 140, 0.04);
        border: 1px solid rgba(106, 27, 154, 0.06);
        transition: all 0.2s;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #7b1fa2, #b87ad4);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px -10px rgba(74, 20, 140, 0.12);
        border-color: rgba(106, 27, 154, 0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #3b0b6e;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 700;
        color: #6a1b9a;
        letter-spacing: 0.6px;
        margin-top: 6px;
    }
    
    .metric-sub {
        font-size: 0.72rem;
        color: #9e9e9e;
        margin-top: 2px;
        font-weight: 500;
    }
    
    /* ----- INFO BOXES ----- */
    .info-box {
        background: #f8f4ff;
        border-radius: 18px;
        padding: 1rem 1.6rem;
        border: 1px solid #ede6f6;
    }
    
    .info-box-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #6a1b9a;
        font-weight: 700;
        letter-spacing: 0.4px;
    }
    
    .info-box-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1c1b1e;
        margin-top: 2px;
    }
    
    /* ----- LOCATION BADGE ----- */
    .location-badge {
        background: linear-gradient(145deg, #7b1fa2, #4a148c);
        padding: 0.6rem 2rem;
        border-radius: 60px;
        display: inline-block;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 8px 18px -6px rgba(74, 20, 140, 0.25);
        letter-spacing: 0.3px;
    }
    
    /* ----- SEGMENT & TREND ITEMS ----- */
    .segment-card, .trend-item {
        background: white;
        border-radius: 16px;
        padding: 0.9rem 1.4rem;
        margin: 0.5rem 0;
        border: 1px solid #f0ebf5;
        transition: all 0.15s;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        font-size: 1rem;
    }
    
    .segment-card:hover, .trend-item:hover {
        background: #faf8ff;
        border-color: #d4c4e8;
        transform: translateX(4px);
    }
    
    .segment-card strong {
        color: #4a148c;
        font-size: 1.05rem;
        font-weight: 700;
    }
    
    .segment-card p {
        color: #3a3a3a;
        font-size: 0.95rem;
        margin-top: 4px;
    }
    
    .trend-bullet {
        color: #7b1fa2;
        font-weight: 700;
        font-size: 1.2rem;
        line-height: 1.4;
        min-width: 28px;
    }
    
    .trend-item span {
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* ----- TAGS ----- */
    .tag {
        background: #f0e8fa;
        color: #4a148c;
        padding: 0.3rem 1.4rem;
        border-radius: 60px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.3px;
    }
    
    /* ----- PROGRESS BAR ----- */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9c27b0, #4a148c);
        border-radius: 60px;
        height: 8px !important;
    }
    
    .stProgress > div {
        background: #ede6f6;
        border-radius: 60px;
        height: 8px !important;
    }
    
    /* ----- ALERTS ----- */
    .stAlert {
        border-radius: 16px;
        border-left: 5px solid #7b1fa2;
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(4px);
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
    }
    
    .stAlert > div {
        font-size: 1rem !important;
    }
    
    .stSuccess {
        background: rgba(240, 248, 240, 0.92) !important;
        border-radius: 16px !important;
        border-left: 5px solid #2e7d32 !important;
        font-size: 1rem !important;
    }
    
    .stWarning {
        background: rgba(255, 248, 225, 0.92) !important;
        border-radius: 16px !important;
        border-left: 5px solid #f57c00 !important;
        font-size: 1rem !important;
    }
    
    /* ----- TABS (modern pill) ----- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1ebf7;
        padding: 6px;
        border-radius: 60px;
        border: 1px solid #e4dcee;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 60px;
        padding: 0.7rem 2rem;
        color: #5a2d7a;
        font-weight: 600;
        font-size: 0.95rem;
        background: transparent;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(74, 20, 140, 0.04);
        color: #3b0b6e;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #3b0b6e !important;
        box-shadow: 0 4px 16px -4px rgba(74, 20, 140, 0.08);
        font-weight: 700;
    }
    
    /* ----- DIVIDER ----- */
    .divider-light {
        height: 1px;
        background: linear-gradient(90deg, transparent, #b69ac9, transparent);
        margin: 1.2rem 0;
        opacity: 0.35;
        border: none;
    }
    
    /* ----- HEADINGS ----- */
    h1, h2, h3, h4 {
        color: #1c1b1e;
        font-weight: 700;
    }
    
    h3 {
        color: #4a148c;
        font-weight: 700;
        font-size: 1.3rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* ----- RESPONSIVE ----- */
    @media (max-width: 700px) {
        .header-gradient {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
            padding: 1.5rem;
        }
        .header-gradient h1 { font-size: 1.8rem !important; }
        .card { padding: 1rem; }
    }
    
    /* ----- SCROLLBAR ----- */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f0ebf5;
    }
    ::-webkit-scrollbar-thumb {
        background: #9c27b0;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #7b1fa2;
    }
    
    /* ----- SPACING FIXES ----- */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    
    .row-widget.stSelectbox {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="column"] {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="header-gradient">
    <div>
        <h1>🚀 Startup Validator</h1>
        <p>AI-powered multi-agent analysis for your startup idea</p>
    </div>
    <div class="header-badge">
        <span style="color: #b9f6ca; font-size: 0.6rem;">●</span> active · v2.0
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== INPUT SECTION ====================
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns([2.2, 1.8])

with col1:
    st.markdown('<span class="field-label">💡 Your Startup Idea</span>', unsafe_allow_html=True)
    startup = st.text_input(
        "",
        placeholder="e.g., AI Resume Builder, Smart Parking System, LegalTech Assistant",
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

# ==================== ANALYZE BUTTON ====================
analyze = st.button("🔍 Analyze Startup Idea", use_container_width=True)

# ==================== ANALYSIS ====================
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
        web_result = run_web_search(startup)
        market_result = run_market_analysis(startup, industry, location)
        swot_result = run_swot_analysis(startup)
    
    st.success("✅ Analysis complete! Check the results below.")
    st.divider()
    
    # ==================== TABS ====================
    tab1, tab2, tab3 = st.tabs(["🌐 Web Search Insights", "📈 Market Analysis Report", "⚔ SWOT & Risk Analysis"])
    
    # ==================== WEB SEARCH TAB ====================
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="card-title">🌐 Web Search Insights</span>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Market Trends")
            for trend in web_result.market_trends:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">✦</span>
                    <span>{trend}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Customer Pain Points")
            for pain in web_result.customer_pain_points:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">•</span>
                    <span>{pain}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📰 Latest News")
            for news in web_result.latest_news:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">📰</span>
                    <span>{news}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Industry Insights")
            for insight in web_result.industry_insights:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">💡</span>
                    <span>{insight}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== MARKET ANALYSIS TAB ====================
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Location
        st.markdown("### 📍 Target Location")
        st.markdown(f'<span class="location-badge">{market_result.location}</span>', unsafe_allow_html=True)
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
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
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
        # Growth & Maturity
        st.markdown("### 📈 Market Dynamics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-box-label">Growth Rate</div>
                <div class="info-box-value">{market_result.growth_rate}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <div class="info-box-label">Market Maturity</div>
                <div class="info-box-value">{market_result.market_maturity}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
        # Customer Segments
        st.markdown("### 👥 Customer Segments")
        
        for segment in market_result.customer_segments:
            st.markdown(f"""
            <div class="segment-card">
                <strong>{segment.name}</strong>
                <p>{segment.description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
        # Key Trends
        st.markdown("### 🔥 Key Market Trends")
        
        for trend in market_result.key_trends:
            st.markdown(f"""
            <div class="trend-item">
                <span class="trend-bullet">✦</span>
                <span>{trend}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== SWOT & RISK TAB (MINIMAL EMOJIS - PROFESSIONAL) ====================
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="card-title">⚔ SWOT & Risk Analysis</span>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Strengths")
            for item in swot_result.strengths:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">✓</span>
                    <span>{item}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Weaknesses")
            for item in swot_result.weaknesses:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">✗</span>
                    <span>{item}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Opportunities")
            for item in swot_result.opportunities:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">→</span>
                    <span>{item}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Threats")
            for item in swot_result.threats:
                st.markdown(f"""
                <div class="trend-item">
                    <span class="trend-bullet">!</span>
                    <span>{item}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
        # Risk Categories
        st.markdown("### Risk Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<span class="tag">Market Risks</span>', unsafe_allow_html=True)
            for item in swot_result.market_risks:
                st.markdown(f"• {item}")
        
        with col2:
            st.markdown('<span class="tag">Technical Risks</span>', unsafe_allow_html=True)
            for item in swot_result.technical_risks:
                st.markdown(f"• {item}")
        
        with col3:
            st.markdown('<span class="tag">Financial Risks</span>', unsafe_allow_html=True)
            for item in swot_result.financial_risks:
                st.markdown(f"• {item}")
        
        st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("### Recommendations")
        for item in swot_result.recommendations:
            st.markdown(f"""
            <div class="trend-item">
                <span class="trend-bullet">▶</span>
                <span>{item}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
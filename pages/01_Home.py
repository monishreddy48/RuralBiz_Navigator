"""
RuralBiz Navigator - Home / Dashboard
Modern Fintech & Analytics Interface for Rural Micro-Entrepreneurs.
SIH 2026 Problem Statement SIH26091 / PS 91
"""
import streamlit as st
from utils.ui_components import (
    load_custom_css,
    render_sidebar,
    render_disclaimer_footer,
    _apply_scenario_to_state
)
from utils.demo_scenarios import load_scenario
from i18n.translations import t
from database.db import init_db

# Page config
st.set_page_config(
    page_title="RuralBiz Navigator - Home",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database safely & inject CSS
init_db()
load_custom_css()
render_sidebar(current_page="Home")

lang = st.session_state.get("language", "en")

# Ensure session state has a default scenario loaded so initial visits have data to explore immediately
if "assessment_data" not in st.session_state:
    _apply_scenario_to_state(load_scenario("demo_1"))

# ==============================================================================
# SECTION A: Welcome / Hero Section
# ==============================================================================
st.markdown(
    """
    <div class="hero-box-v2">
        <div class="hero-badge">🌾 SIH 2026 &bull; PS 91 &bull; Micro-Enterprise Intelligence</div>
        <div class="hero-title-v2">Build a smarter business, starting in your village.</div>
        <div class="hero-desc-v2">
            Discover opportunities, understand your local market, calculate financial feasibility, and make confident business decisions with AI-powered guidance.
        </div>
        <div class="hero-stats-row">
            <div class="hero-stat-item">
                <span class="hero-stat-value">5–10 km</span>
                <span class="hero-stat-label">Catchment Radius</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">0–100</span>
                <span class="hero-stat-label">Viability Index</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">Reducing-Balance</span>
                <span class="hero-stat-label">EMI &amp; DSCR Math</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">8 Official</span>
                <span class="hero-stat-label">Govt Schemes Mapped</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hero CTAs
col_hero_cta1, col_hero_cta2, col_hero_spacer = st.columns([1.5, 1.5, 3.0])
with col_hero_cta1:
    if st.button("🚀 Start Business Assessment", use_container_width=True, type="primary"):
        st.switch_page("pages/02_Business_Feasibility.py")
with col_hero_cta2:
    if st.button("🔍 Explore Opportunities", use_container_width=True):
        st.switch_page("pages/07_Business_Alternatives.py")

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION B: Business Assessment Journey (Connected Stepper)
# ==============================================================================
st.markdown(
    """
    <div class="journey-container">
        <div class="journey-header">
            <div>
                <div class="journey-title">🧭 Intelligent Business Assessment Journey</div>
                <div class="journey-subtitle">Structured, deterministic evaluation guiding your decision from location to final recommendation.</div>
            </div>
            <span class="context-chip context-chip-highlight">8 Sequential Stages</span>
        </div>
        <div class="stepper-track">
            <div class="step-node completed">
                <div class="step-circle">1</div>
                <div class="step-label">Your Location</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node completed">
                <div class="step-circle">2</div>
                <div class="step-label">Your Capital</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node completed">
                <div class="step-circle">3</div>
                <div class="step-label">Business Idea</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node active">
                <div class="step-circle">4</div>
                <div class="step-label">Local Market<br/>(5–10 km)</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node">
                <div class="step-circle">5</div>
                <div class="step-label">Business<br/>Viability</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node">
                <div class="step-circle">6</div>
                <div class="step-label">Financial Plan<br/>&amp; EMI</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node">
                <div class="step-circle">7</div>
                <div class="step-label">Scheme<br/>Routing</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-node">
                <div class="step-circle">8</div>
                <div class="step-label">Final Decision<br/>(GO / MODIFY / AVOID)</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# SECTION C: Quick Actions
# ==============================================================================
st.subheader("⚡ Quick Actions")
st.caption("Jump straight into an assessment, explore potential micro-ventures, or load pre-built demo scenarios.")

qa_col1, qa_col2, qa_col3 = st.columns(3)

with qa_col1:
    st.markdown(
        """
        <div class="action-card">
            <div>
                <div class="action-card-icon">🚀</div>
                <div class="action-card-title">Start Business Assessment</div>
                <div class="action-card-desc">
                    Enter your village location, budget, and venture idea to get a rigorous 0–100 viability score, local market analysis, and GO/MODIFY/AVOID verdict.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Begin Assessment &rarr;", key="qa_btn_assess", use_container_width=True, type="primary"):
        st.switch_page("pages/02_Business_Feasibility.py")

with qa_col2:
    st.markdown(
        """
        <div class="action-card">
            <div>
                <div class="action-card-icon">🔍</div>
                <div class="action-card-title">Explore Business Opportunities</div>
                <div class="action-card-desc">
                    Not sure what to start? Enter your available capital to rank all 10 rural enterprise categories based on local demand and competition.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Explore Alternatives &rarr;", key="qa_btn_explore", use_container_width=True):
        st.switch_page("pages/07_Business_Alternatives.py")

with qa_col3:
    st.markdown(
        """
        <div class="action-card">
            <div>
                <div class="action-card-icon">⚡</div>
                <div class="action-card-title">Load Demo Entrepreneur</div>
                <div class="action-card-desc">
                    Instantly load verified SIH judging cases: Agri Food Processing (GO), Coastal Tailoring (MODIFY), or Peri-Urban Retail Store (AVOID).
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Load Scenario 1 (Food Processing) &rarr;", key="qa_btn_demo1", use_container_width=True):
        _apply_scenario_to_state(load_scenario("demo_1"))
        st.toast("Loaded Scenario 1: Food Processing in Agri Hub!", icon="🌾")
        st.switch_page("pages/02_Business_Feasibility.py")

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION D: Decision-Support Pillars
# ==============================================================================
st.subheader("💡 Decision-Support Pillars")
st.caption("Eight integrated intelligence modules built on deterministic financial engineering and verified rural benchmarks.")

pillars = [
    {
        "icon": "📊",
        "title": "1. Business Feasibility",
        "desc": "Understand whether a business idea is practical with a 0–100 weighted viability score, 3–5 grounded reasons, and strategic SWOT analysis.",
        "page": "pages/02_Business_Feasibility.py",
        "btn": "View Feasibility"
    },
    {
        "icon": "📍",
        "title": "2. Hyperlocal Market",
        "desc": "Discover local demand and competition within a 5–10 km catchment zone, population demographics, and unmet spending gaps.",
        "page": "pages/03_Hyper_Local_Market.py",
        "btn": "Explore Market"
    },
    {
        "icon": "💳",
        "title": "3. Financial Planning",
        "desc": "Estimate investment, profit, expenses, and reducing-balance EMI schedule with 12-month dynamic P&L and DSCR coverage.",
        "page": "pages/04_Financial_Calculator.py",
        "btn": "Plan Finances"
    },
    {
        "icon": "📉",
        "title": "4. What-If Simulation",
        "desc": "Explore different stress scenarios: volume drops, price wars, raw material inflation, or interest rate shocks to test business survival.",
        "page": "pages/05_What_If_Simulator.py",
        "btn": "Simulate Shocks"
    },
    {
        "icon": "🏛️",
        "title": "5. Government Schemes",
        "desc": "Discover potentially relevant support schemes (PMEGP, MUDRA, PMFME, Stand-Up India) with verified subsidy rules and ceilings.",
        "page": "pages/06_Scheme_Navigator.py",
        "btn": "Find Schemes"
    },
    {
        "icon": "🤖",
        "title": "6. AI Business Assistant",
        "desc": "Get natural language assistance with business questions in English, Hindi, Telugu, or Kannada, grounded in your real calculations.",
        "page": "pages/08_AI_Assistant.py",
        "btn": "Ask Assistant"
    },
    {
        "icon": "💡",
        "title": "7. Business Alternatives",
        "desc": "Discover alternative business opportunities ranked by viability for your specific budget and locality with one-click adoption.",
        "page": "pages/07_Business_Alternatives.py",
        "btn": "Compare Sectors"
    },
    {
        "icon": "📄",
        "title": "8. DPR Generation",
        "desc": "Generate structured, 20-section Detailed Project Reports (DPR) compiled into bank-ready PDFs for formal loan applications.",
        "page": "pages/09_DPR_Report.py",
        "btn": "Generate DPR"
    }
]

p_col1, p_col2, p_col3, p_col4 = st.columns(4)
for idx, pil in enumerate(pillars):
    target_col = [p_col1, p_col2, p_col3, p_col4][idx % 4]
    with target_col:
        st.markdown(
            f"""
            <div class="pillar-card">
                <div class="pillar-card-header">
                    <div class="pillar-card-icon">{pil['icon']}</div>
                    <div class="pillar-card-title">{pil['title']}</div>
                </div>
                <div class="pillar-card-desc">{pil['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(pil['btn'], key=f"pil_btn_{idx}", use_container_width=True):
            st.switch_page(pil['page'])
        st.markdown("<br/>", unsafe_allow_html=True)

render_disclaimer_footer(lang)

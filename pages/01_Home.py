"""
RuralBiz Navigator - Home / Dashboard
SIH 2026 Problem Statement SIH26091 / PS 91
"""
import streamlit as st
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer, _apply_scenario_to_state
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

# Initialize database safely
init_db()
load_custom_css()
render_sidebar()

lang = st.session_state.get("language", "en")

# Ensure session state has a default scenario loaded so initial visits have data to explore immediately
if "assessment_data" not in st.session_state:
    _apply_scenario_to_state(load_scenario("demo_1"))

# Hero Section
st.markdown(
    f"""
    <div class="hero-box">
        <div class="hero-title">🌾 {t('app_title', lang)}</div>
        <div class="hero-tagline">"{t('tagline', lang)}"</div>
        <div class="hero-desc">
            AI-powered hyper-local business advisory and financial structuring for rural micro-entrepreneurs.
            Understand whether a business venture fits your specific village ecosystem, budget, and competition <b>before borrowing money</b>.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Workflow Breadcrumb Banner
st.markdown(
    """
    <div class="workflow-container">
        <span class="workflow-step">📍 YOUR LOCATION</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">💰 YOUR CAPITAL</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">💡 BUSINESS IDEA</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">🛒 LOCAL MARKET (5-10 km)</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">📊 VIABILITY (0-100)</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">💳 FINANCIAL PLAN &amp; EMI</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step">🏛️ SCHEME ROUTING</span>
        <span class="workflow-arrow">&rarr;</span>
        <span class="workflow-step" style="background:#10B981; color:white;">🎯 GO / MODIFY / AVOID</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Action Callouts
col_cta1, col_cta2, col_demo = st.columns([1.5, 1.5, 2.0])
with col_cta1:
    if st.button("🚀 " + t("cta_start_assessment", lang), use_container_width=True, type="primary"):
        st.switch_page("pages/02_Business_Feasibility.py")

with col_cta2:
    if st.button("🔍 " + t("cta_explore_opps", lang), use_container_width=True):
        st.switch_page("pages/07_Business_Alternatives.py")

with col_demo:
    if st.button("⚡ " + t("btn_load_demo", lang) + " (Food Processing ₹3L)", use_container_width=True):
        _apply_scenario_to_state(load_scenario("demo_1"))
        st.toast("Loaded Scenario 1: Food Processing in Agri Hub!", icon="🌾")
        st.rerun()

st.markdown("---")

# Key Pillars Section
st.subheader("💡 Decision-Support Pillars")
st.caption("Grounded in verified local benchmarks, reducing-balance debt mathematics, and official schemes.")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-card-title">📍 {t('card_market_opp', lang)}</div>
            <div class="feature-card-desc">{t('card_market_opp_desc', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-card-title">💳 {t('card_fin_readiness', lang)}</div>
            <div class="feature-card-desc">{t('card_fin_readiness_desc', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-card-title">🏛️ {t('card_funding_options', lang)}</div>
            <div class="feature-card-desc">{t('card_funding_options_desc', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-card-title">📉 {t('card_business_risk', lang)}</div>
            <div class="feature-card-desc">{t('card_business_risk_desc', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# Differentiation Highlight Banner
st.info(
    """
    **🌟 The RuralBiz Differentiation:**
    Most government and banking portals help entrepreneurs *after* they decide to borrow—to register, draft a loan application, or seek subsidies.
    **RuralBiz Navigator focuses on the critical decision BEFORE borrowing:**
    *"Should I start this business HERE, with MY budget, given MY local market?"*
    """
)

# Active Snapshot Section if assessment exists
if "viability_result" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Current Assessment Snapshot")
    
    loc = st.session_state.get("locality", {})
    biz = st.session_state.get("business", {})
    viab = st.session_state.get("viability_result", {})
    rec = st.session_state.get("recommendation", {})
    fin = st.session_state.get("financial_plan", {})
    
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("Location", loc.get("village_name", "Village"))
    col_m2.metric("Business", biz.get("category", "Trade"))
    col_m3.metric("Viability Score", f"{viab.get('viability_score', 0):.0f} / 100", viab.get("classification", ""))
    col_m4.metric("Recommendation", rec.get("decision", "N/A"), rec.get("decision_label", ""))
    col_m5.metric("DSCR Buffer", f"{fin.get('dscr', 0):.2f}", fin.get("dscr_badge", ""))

render_disclaimer_footer(lang)

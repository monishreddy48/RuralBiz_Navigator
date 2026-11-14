"""
RuralBiz Navigator - Common UI Layout & Sidebar Components
Modern Fintech / Analytics Dashboard Component Library.
"""
import streamlit as st
from pathlib import Path
from i18n.translations import t
from config import SUPPORTED_LANGUAGES, BASE_DIR
from ai.router import get_active_provider
from utils.demo_scenarios import load_scenario
from utils.formatting import format_inr

def load_custom_css():
    """Injects custom CSS from assets/style.css."""
    css_path = BASE_DIR / "assets" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_sidebar(current_page: str = ""):
    """
    Renders the modern fintech-styled sidebar across all pages:
    - Brand identity with tagline: 'Smarter decisions. Stronger rural businesses.'
    - Structured navigation groups:
        * OVERVIEW
        * BUSINESS INTELLIGENCE
        * FINANCIAL TOOLS
        * GOVERNMENT SUPPORT
        * AI SUPPORT
        * ADDITIONAL
    - Quick Demo Scenario Loaders (Cases 1, 2, 3)
    - Active Assessment Status Widget
    - AI Provider Status
    - Language Selector at the bottom
    - Institutional Disclaimer
    """
    if "language" not in st.session_state:
        st.session_state["language"] = "en"
        
    lang = st.session_state["language"]

    with st.sidebar:
        # 1. Brand Logo & Tagline
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="sidebar-logo-icon">🌾</div>
                <div>
                    <div class="sidebar-brand-name">RuralBiz Navigator</div>
                    <div class="sidebar-brand-tagline">Smarter decisions. Stronger rural businesses.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 2. Structured Navigation Groups
        nav_groups = [
            {
                "group": "OVERVIEW",
                "items": [
                    {"label": "Home", "icon": "🏠", "page": "pages/01_Home.py", "key": "Home"}
                ]
            },
            {
                "group": "BUSINESS INTELLIGENCE",
                "items": [
                    {"label": "Business Feasibility", "icon": "📊", "page": "pages/02_Business_Feasibility.py", "key": "Feasibility"},
                    {"label": "Hyperlocal Market", "icon": "📍", "page": "pages/03_Hyper_Local_Market.py", "key": "Market"},
                    {"label": "Business Alternatives", "icon": "💡", "page": "pages/07_Business_Alternatives.py", "key": "Alternatives"}
                ]
            },
            {
                "group": "FINANCIAL TOOLS",
                "items": [
                    {"label": "Financial Calculator", "icon": "💳", "page": "pages/04_Financial_Calculator.py", "key": "Financial"},
                    {"label": "What-If Simulator", "icon": "📉", "page": "pages/05_What_If_Simulator.py", "key": "WhatIf"},
                    {"label": "DPR Report", "icon": "📄", "page": "pages/09_DPR_Report.py", "key": "DPR"}
                ]
            },
            {
                "group": "GOVERNMENT SUPPORT",
                "items": [
                    {"label": "Scheme Navigator", "icon": "🏛️", "page": "pages/06_Scheme_Navigator.py", "key": "Schemes"}
                ]
            },
            {
                "group": "AI SUPPORT",
                "items": [
                    {"label": "AI Assistant", "icon": "🤖", "page": "pages/08_AI_Assistant.py", "key": "AI"}
                ]
            },
            {
                "group": "ADDITIONAL",
                "items": [
                    {"label": "About & Architecture", "icon": "ℹ️", "page": "pages/10_About.py", "key": "About"}
                ]
            }
        ]

        for grp in nav_groups:
            st.markdown(f'<div class="nav-group-label">{grp["group"]}</div>', unsafe_allow_html=True)
            for item in grp["items"]:
                is_active = (current_page == item["key"] or current_page == item["label"])
                btn_type = "primary" if is_active else "secondary"
                btn_text = f"{item['icon']} {item['label']}"
                if is_active:
                    btn_text = f"● {btn_text}"
                if st.button(btn_text, key=f"nav_btn_{item['key']}", use_container_width=True, type=btn_type):
                    if not is_active:
                        st.switch_page(item["page"])

        st.markdown("---")

        # 3. Quick Demo Scenarios
        st.markdown('<div class="nav-group-label">⚡ DEMO SCENARIOS</div>', unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🟢 Case 1: GO", use_container_width=True, help="Agri Food Processing (₹3L Capital): High viability"):
                scenario_data = load_scenario("demo_1")
                _apply_scenario_to_state(scenario_data)
                st.toast("Loaded Scenario 1: Strong Opportunity (GO)!", icon="✅")
                st.rerun()
                
        with col_d2:
            if st.button("🟡 Case 2: MODIFY", use_container_width=True, help="Tailoring Unit (₹30k Capital): Borderline viability"):
                scenario_data = load_scenario("demo_2")
                _apply_scenario_to_state(scenario_data)
                st.toast("Loaded Scenario 2: Borderline Opportunity (MODIFY)!", icon="⚠️")
                st.rerun()

        if st.button("🔴 Case 3: AVOID (High Risk)", use_container_width=True, help="Saturated Retail Kirana: High debt & competitor risk"):
            scenario_data = load_scenario("demo_3")
            _apply_scenario_to_state(scenario_data)
            st.toast("Loaded Scenario 3: High-Risk Saturated Market (AVOID)!", icon="🛑")
            st.rerun()

        # 4. Active Assessment Summary Card
        if "assessment_data" in st.session_state and st.session_state["assessment_data"]:
            ad = st.session_state["assessment_data"]
            loc = st.session_state.get("locality", {})
            biz = st.session_state.get("business", {})
            rec = st.session_state.get("recommendation", {})
            viab = st.session_state.get("viability_result", {})
            
            st.markdown("---")
            st.markdown('<div class="nav-group-label">📊 ACTIVE ASSESSMENT</div>', unsafe_allow_html=True)
            
            score = viab.get("viability_score", 0)
            decision = rec.get("decision", "N/A")
            decision_color = rec.get("decision_color", "#10B981")
            
            st.markdown(
                f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:10px 12px; font-size:0.8rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                    <div style="font-weight:700; color:#111827; margin-bottom:2px;">{biz.get('business_name', 'Venture')}</div>
                    <div style="color:#6B7280; margin-bottom:6px;">📍 {loc.get('village_name', 'N/A')} &bull; ₹{ad.get('own_capital', 0):,.0f}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:{decision_color};">Score: {score:.0f}/100</span>
                        <span style="background:{decision_color}; color:white; font-size:0.7rem; font-weight:800; padding:2px 7px; border-radius:4px;">{decision}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 5. AI Engine Badge
        st.markdown("---")
        _, provider_status = get_active_provider()
        if "Demo Mode" in provider_status:
            st.markdown(
                """
                <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:8px 10px; font-size:0.75rem; color:#166534;">
                    <b>🤖 AI Engine:</b> Demo Mode<br/>
                    <span style="color:#047857; font-size:0.7rem;">Deterministic offline advisor</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:8px 10px; font-size:0.75rem; color:#065F46;">
                    <b>⚡ AI Engine:</b> Connected<br/>
                    <span style="font-size:0.7rem;">{provider_status}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 6. Language Selector at the Bottom
        st.markdown("---")
        lang_keys = list(SUPPORTED_LANGUAGES.keys())
        lang_labels = list(SUPPORTED_LANGUAGES.values())
        curr_idx = lang_keys.index(lang) if lang in lang_keys else 0
        
        selected_lang_label = st.selectbox(
            "🌐 " + ("Language / भाषा / భాష / ಭಾಷೆ"),
            options=lang_labels,
            index=curr_idx,
            key="sb_lang_selector"
        )
        selected_key = lang_keys[lang_labels.index(selected_lang_label)]
        if selected_key != st.session_state["language"]:
            st.session_state["language"] = selected_key
            st.rerun()

        # 7. SIH & Disclaimer Note
        st.caption("🔒 **SIH 2026 Problem Statement 91**")
        st.caption("Simulated benchmark data for demonstration.")

def render_page_header(category: str, title: str, description: str):
    """Renders standardized fintech-style page title header."""
    st.markdown(
        f"""
        <div class="page-header-box">
            <div class="page-category-label">{category}</div>
            <div class="page-title-text">{title}</div>
            <div class="page-desc-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_context_bar():
    """Renders active assessment context chip bar if assessment data exists."""
    if "assessment_data" in st.session_state and st.session_state["assessment_data"]:
        loc = st.session_state.get("locality", {})
        biz = st.session_state.get("business", {})
        fin = st.session_state.get("financial_plan", {})
        rec = st.session_state.get("recommendation", {})
        viab = st.session_state.get("viability_result", {})
        
        score = viab.get("viability_score", 0)
        decision = rec.get("decision", "GO")
        
        st.markdown(
            f"""
            <div class="context-chip-bar">
                <span style="color:#6B7280; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Context:</span>
                <span class="context-chip">📍 <b>{loc.get('village_name', 'Village')}</b> ({loc.get('state', '')})</span>
                <span class="context-chip">💼 <b>{biz.get('business_name', 'Enterprise')}</b></span>
                <span class="context-chip">💰 Budget: <b>{format_inr(fin.get('project_cost', 0))}</b></span>
                <span class="context-chip context-chip-highlight">📊 Viability: <b>{score:.0f}/100</b> ({decision})</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def _apply_scenario_to_state(scenario_data: dict):
    """Populates session state from a scenario dict."""
    st.session_state["assessment_data"] = scenario_data["user_inputs"]
    st.session_state["locality"] = scenario_data["locality"]
    st.session_state["business"] = scenario_data["business"]
    st.session_state["competitors_df"] = scenario_data["competitors_df"]
    st.session_state["hyperlocal_metrics"] = scenario_data["hyperlocal_metrics"]
    st.session_state["financial_plan"] = scenario_data["financial_plan"]
    st.session_state["viability_result"] = scenario_data["viability_result"]
    st.session_state["recommendation"] = scenario_data["recommendation"]
    st.session_state["schemes"] = scenario_data["schemes"]

def render_disclaimer_footer(lang: str = "en"):
    """Renders prominent disclaimer block at the bottom of pages."""
    st.markdown(
        f"""
        <div class="disclaimer-card">
            <b>⚖️ Institutional Disclaimer:</b> {t('disclaimer_text', lang)}<br/>
            <span class="prototype-tag">{t('prototype_data_note', lang)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

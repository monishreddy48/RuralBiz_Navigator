"""
RuralBiz Navigator - Common UI Layout & Sidebar Components
Ensures consistent header, language switcher, AI status indicator, and demo scenario loaders.
"""
import streamlit as st
from pathlib import Path
from i18n.translations import t
from config import SUPPORTED_LANGUAGES, BASE_DIR
from ai.router import get_active_provider
from utils.demo_scenarios import load_scenario

def load_custom_css():
    """Injects custom CSS from assets/style.css."""
    css_path = BASE_DIR / "assets" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_sidebar():
    """
    Renders standardized sidebar across all pages:
    - Language Selector
    - AI Provider Status
    - Demo Scenario Quick Loader (Scenarios 1, 2, 3)
    - Active Assessment Mini Status
    - Official Disclaimer Note
    """
    # Initialize default language
    if "language" not in st.session_state:
        st.session_state["language"] = "en"
        
    lang = st.session_state["language"]

    with st.sidebar:
        st.markdown("### 🌾 **RuralBiz Navigator**")
        st.caption(t("tagline", lang))
        st.markdown("---")

        # 1. Language Selector
        lang_keys = list(SUPPORTED_LANGUAGES.keys())
        lang_labels = list(SUPPORTED_LANGUAGES.values())
        curr_idx = lang_keys.index(lang) if lang in lang_keys else 0
        
        selected_lang_label = st.selectbox(
            "🌐 " + ("Select Language / भाषा चुनें"),
            options=lang_labels,
            index=curr_idx,
            key="sb_lang_selector"
        )
        selected_key = lang_keys[lang_labels.index(selected_lang_label)]
        if selected_key != st.session_state["language"]:
            st.session_state["language"] = selected_key
            st.rerun()

        # 2. AI Assistant Provider Badge
        _, provider_status = get_active_provider()
        if "Demo Mode" in provider_status:
            st.info(f"🤖 **{provider_status}**\n\n*Deterministic offline engine active. No API key required.*")
        else:
            st.success(f"🤖 **{provider_status}**")

        st.markdown("---")

        # 3. Demo Scenario Quick-Loader
        st.markdown("#### ⚡ **Quick Demo Scenarios**")
        st.caption("Load pre-configured entrepreneur cases for SIH judging:")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🟢 Case 1 (GO)", use_container_width=True, help="Food Processing in Agri Hub: High viability"):
                scenario_data = load_scenario("demo_1")
                _apply_scenario_to_state(scenario_data)
                st.toast("Loaded Scenario 1: Strong Opportunity (GO)!", icon="✅")
                st.rerun()
                
        with col_d2:
            if st.button("🟡 Case 2 (MODIFY)", use_container_width=True, help="Tailoring Unit: Borderline viability"):
                scenario_data = load_scenario("demo_2")
                _apply_scenario_to_state(scenario_data)
                st.toast("Loaded Scenario 2: Borderline Opportunity (MODIFY)!", icon="⚠️")
                st.rerun()

        if st.button("🔴 Case 3 (AVOID / High Risk)", use_container_width=True, help="Saturated Retail Kirana: High debt & competitor risk"):
            scenario_data = load_scenario("demo_3")
            _apply_scenario_to_state(scenario_data)
            st.toast("Loaded Scenario 3: High-Risk (AVOID)!", icon="🛑")
            st.rerun()

        st.markdown("---")

        # 4. Active Assessment Summary Widget
        if "assessment_data" in st.session_state and st.session_state["assessment_data"]:
            ad = st.session_state["assessment_data"]
            loc = st.session_state.get("locality", {})
            biz = st.session_state.get("business", {})
            rec = st.session_state.get("recommendation", {})
            viab = st.session_state.get("viability_result", {})
            
            st.markdown("#### 📊 **Active Assessment**")
            st.markdown(f"**Locality:** {loc.get('village_name', 'N/A')}")
            st.markdown(f"**Business:** {biz.get('business_name', 'N/A')}")
            st.markdown(f"**Capital:** ₹{ad.get('own_capital', 0):,.0f}")
            
            score = viab.get("viability_score", 0)
            decision = rec.get("decision", "N/A")
            badge_color = rec.get("decision_color", "#3B82F6")
            
            st.markdown(
                f"<div style='background-color: {badge_color}; color: white; padding: 6px 12px; border-radius: 6px; text-align: center; font-weight: bold;'>"
                f"SCORE: {score:.0f}/100 &bull; {decision}</div>",
                unsafe_allow_html=True
            )
            st.markdown("---")

        # 5. Prototype Disclaimer
        st.caption("🔒 **SIH 2026 Problem Statement 91**")
        st.caption("Prototype data is simulated for demonstration.")

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
            <b>⚖️ Disclaimer:</b> {t('disclaimer_text', lang)}<br/>
            <span class="prototype-tag">{t('prototype_data_note', lang)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

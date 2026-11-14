"""
RuralBiz Navigator - Business Alternatives Recommender
Ranks all 10 rural enterprise categories against user locality and budget.
"""
import streamlit as st
import pandas as pd
from utils.ui_components import (
    load_custom_css,
    render_sidebar,
    render_page_header,
    render_context_bar,
    render_disclaimer_footer
)
from i18n.translations import t
from core.alternative_engine import evaluate_business_alternatives
from utils.formatting import format_inr
from database.db import get_localities, get_business_by_category, get_competitors
from core.hyperlocal_engine import calculate_hyperlocal_metrics
from core.financial_engine import calculate_financial_plan
from core.viability_engine import calculate_viability_score
from core.recommendation_engine import generate_business_recommendation
from core.scheme_engine import evaluate_schemes

st.set_page_config(
    page_title="RuralBiz Navigator - Business Alternatives",
    page_icon="💡",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="Alternatives")
lang = st.session_state.get("language", "en")

render_page_header(
    category="BUSINESS INTELLIGENCE",
    title="💡 " + t("nav_alternatives", lang),
    description="Evaluate and rank all 10 rural micro-enterprise categories to discover higher viability opportunities suited to your available budget."
)

render_context_bar()

locality = st.session_state.get("locality")
current_inputs = st.session_state.get("assessment_data", {})
active_category = current_inputs.get("category", "Food Processing")

if not locality:
    localities_df = get_localities()
    locality = localities_df.iloc[0].to_dict()
    st.session_state["locality"] = locality

# ==============================================================================
# SECTION 1: Capital Budget Filter
# ==============================================================================
col_f1, col_f2 = st.columns([2, 3])
with col_f1:
    default_budget = float(st.session_state.get("budget_search_capital", current_inputs.get("own_capital", 300000.0)))
    budget_input = st.number_input(
        "Available Capital for Deployment (₹)",
        min_value=10000.0,
        max_value=2000000.0,
        value=default_budget,
        step=25000.0
    )
with col_f2:
    st.markdown(
        f"""
        <div class="surface-card" style="padding:14px 18px; margin-top:24px;">
            <div style="font-size:0.75rem; color:#6B7280; font-weight:700; text-transform:uppercase;">Target Locality Context</div>
            <div style="font-size:1.05rem; font-weight:700; color:#111827; margin-top:2px;">
                📍 {locality.get('village_name', 'Village')}, {locality.get('state', '')}
            </div>
            <div style="font-size:0.84rem; color:#6B7280;">
                Population: {locality.get('population', 0):,} &bull; Road Index: {locality.get('road_access_score', 0):.0f}/100
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Evaluate all 10 alternative businesses deterministically
alternatives = evaluate_business_alternatives(
    locality=locality,
    available_capital=budget_input,
    current_business_category=active_category
)

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 2: Top-Ranked Opportunity Highlight
# ==============================================================================
st.subheader("🏆 Ranked Micro-Enterprise Opportunities")
st.caption("Ranked deterministically by composite Viability Score (Market Demand, Competition Saturation, Financial Feasibility, and Risk).")

top_alt = alternatives[0]
st.markdown(
    f"""
    <div class="surface-card" style="border: 2px solid #10B981; background: #F0FDF4;">
        <div style="font-size:0.75rem; color:#065F46; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">🥇 Top-Ranked Opportunity for Your Budget</div>
        <div style="font-size:1.6rem; font-weight:800; color:#064E3B; margin:4px 0;">{top_alt['business_name']} ({top_alt['category']})</div>
        <div style="color:#047857; font-size:0.92rem; margin-bottom:10px;">
            Viability Score: <b>{top_alt['viability_score']:.0f} / 100</b> ({top_alt['classification']}) &bull;
            Est. Monthly Net Profit: <b>{format_inr(top_alt['monthly_net_profit'])}</b> &bull;
            DSCR: <b>{top_alt['dscr']:.2f}</b>
        </div>
        <div style="color:#065F46; font-size:0.86rem; line-height:1.4;">
            <b>Why it is a superior fit:</b> {' &bull; '.join(top_alt['highlights'])}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: Comparison Table
# ==============================================================================
table_rows = []
for idx, alt in enumerate(alternatives, 1):
    table_rows.append({
        "Rank": f"#{idx}",
        "Business Category": alt["category"],
        "Viability Score": f"{alt['viability_score']:.0f} / 100",
        "Total Project Cost": format_inr(alt["project_cost"]),
        "Debt Required": format_inr(alt["loan_required"]),
        "Monthly Net Profit": format_inr(alt["monthly_net_profit"]),
        "DSCR": f"{alt['dscr']:.2f}",
        "Demand Score": f"{alt['market_demand_score']:.0f}",
        "Competition Score": f"{alt['competition_score']:.0f}",
        "Key Advantage": " • ".join(alt["highlights"][:2])
    })

df_table = pd.DataFrame(table_rows)
st.dataframe(df_table, use_container_width=True, hide_index=True)

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 4: One-Click Adoption
# ==============================================================================
st.subheader("🔄 Switch Active Business Assessment")
st.caption("Want to analyze one of these higher-ranked alternatives in detail? Adopt it with one click:")

col_sel, col_act = st.columns([3, 1])
with col_sel:
    selectable_cats = [a["category"] for a in alternatives]
    new_cat = st.selectbox("Select Alternative Category to Adopt", options=selectable_cats, index=0)
with col_act:
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("Adopt Alternative &rarr;", type="primary", use_container_width=True):
        new_biz = get_business_by_category(new_cat)
        competitors_df = get_competitors(locality_id=locality.get("village_id"), business_type=new_cat)
        hl_metrics = calculate_hyperlocal_metrics(locality, new_biz, competitors_df)
        
        proj_cost = float(new_biz["typical_capex"]) + float(new_biz["typical_working_capital"])
        own_cap = min(proj_cost, budget_input)
        
        fin_plan = calculate_financial_plan(
            project_cost=proj_cost,
            own_contribution=own_cap,
            monthly_sales=float(new_biz["typical_monthly_sales"]),
            variable_cost_ratio=float(new_biz["variable_cost_ratio"]),
            monthly_fixed_cost=float(new_biz["monthly_fixed_cost"]),
            unit_price=float(new_biz.get("unit_price_estimate", 100))
        )
        viability = calculate_viability_score(hl_metrics, fin_plan, new_biz, locality)
        rec = generate_business_recommendation(viability, fin_plan, hl_metrics, new_biz, locality)
        schemes = evaluate_schemes(proj_cost, new_cat, ["General", "Rural"])
        
        # Save to state
        st.session_state["business"] = new_biz
        st.session_state["competitors_df"] = competitors_df
        st.session_state["hyperlocal_metrics"] = hl_metrics
        st.session_state["financial_plan"] = fin_plan
        st.session_state["viability_result"] = viability
        st.session_state["recommendation"] = rec
        st.session_state["schemes"] = schemes
        if "assessment_data" not in st.session_state or not isinstance(st.session_state["assessment_data"], dict):
            st.session_state["assessment_data"] = {}
        st.session_state["assessment_data"]["category"] = new_cat
        st.session_state["assessment_data"]["expected_investment"] = proj_cost
        st.session_state["assessment_data"]["own_capital"] = own_cap
        
        st.toast(f"Switched active assessment to {new_cat}!", icon="🎯")
        st.switch_page("pages/02_Business_Feasibility.py")

render_disclaimer_footer(lang)

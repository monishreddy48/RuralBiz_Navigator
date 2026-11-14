"""
RuralBiz Navigator - Business Feasibility & Recommendation
Evaluates user inputs, calculates deterministic viability score, and renders GO/MODIFY/AVOID decision.
"""
import streamlit as st
import plotly.graph_objects as go
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer
from i18n.translations import t
from database.db import get_localities, get_businesses, get_competitors, save_assessment
from core.hyperlocal_engine import calculate_hyperlocal_metrics
from core.financial_engine import calculate_financial_plan
from core.viability_engine import calculate_viability_score
from core.recommendation_engine import generate_business_recommendation
from core.scheme_engine import evaluate_schemes
from utils.validation import validate_assessment_inputs
from utils.formatting import format_inr

st.set_page_config(
    page_title="RuralBiz Navigator - Feasibility Assessment",
    page_icon="📊",
    layout="wide"
)

load_custom_css()
render_sidebar()
lang = st.session_state.get("language", "en")

st.title("📊 " + t("nav_feasibility", lang))
st.caption("Complete the assessment form to evaluate your rural enterprise viability and generate a decision recommendation.")

localities_df = get_localities()
businesses_df = get_businesses()

# Active default values from session state
current_inputs = st.session_state.get("assessment_data", {})
current_loc = st.session_state.get("locality", {})
current_biz = st.session_state.get("business", {})

with st.expander("📝 **Entrepreneur & Project Input Form**", expanded=True):
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        user_name = st.text_input("Entrepreneur Name (Optional)", value=current_inputs.get("name", "Demo Entrepreneur"))
        
        # Locality Selection
        loc_options = {row["village_name"]: row["village_id"] for _, row in localities_df.iterrows()}
        default_loc_idx = 0
        if current_loc and current_loc.get("village_name") in loc_options:
            default_loc_idx = list(loc_options.keys()).index(current_loc["village_name"])
            
        selected_loc_name = st.selectbox(
            t("lbl_select_locality", lang),
            options=list(loc_options.keys()),
            index=default_loc_idx
        )
        selected_village_id = loc_options[selected_loc_name]
        selected_locality = localities_df[localities_df["village_id"] == selected_village_id].iloc[0].to_dict()

        # Business Category Selection
        biz_options = {row["business_name"]: row["category"] for _, row in businesses_df.iterrows()}
        default_biz_idx = 2  # Food Processing default
        if current_biz and current_biz.get("business_name") in biz_options:
            default_biz_idx = list(biz_options.keys()).index(current_biz["business_name"])
            
        selected_biz_name = st.selectbox(
            t("lbl_select_business", lang),
            options=list(biz_options.keys()),
            index=default_biz_idx
        )
        selected_category = biz_options[selected_biz_name]
        selected_business = businesses_df[businesses_df["business_name"] == selected_biz_name].iloc[0].to_dict()

        is_existing = st.radio(
            t("lbl_existing_biz", lang),
            options=["No (New Greenfield Venture)", "Yes (Existing Unit Expansion)"],
            index=1 if current_inputs.get("is_existing") else 0
        ) == "Yes (Existing Unit Expansion)"

    with col_f2:
        default_capex = float(selected_business.get("typical_capex", 180000))
        default_wc = float(selected_business.get("typical_working_capital", 35000))
        benchmark_cost = default_capex + default_wc

        expected_investment = st.number_input(
            t("lbl_expected_investment", lang),
            min_value=10000.0,
            max_value=5000000.0,
            value=float(current_inputs.get("expected_investment", benchmark_cost)),
            step=10000.0,
            help=f"Benchmark project cost for {selected_category} is {format_inr(benchmark_cost)}"
        )

        own_capital = st.number_input(
            t("lbl_own_capital", lang),
            min_value=0.0,
            max_value=5000000.0,
            value=float(min(expected_investment, float(current_inputs.get("own_capital", 300000.0)))),
            step=10000.0,
            help="Your own savings or family contribution towards project cost."
        )

        col_exp, col_risk = st.columns(2)
        with col_exp:
            experience = st.selectbox(
                t("lbl_experience", lang),
                options=["Beginner (< 1 yr)", "Intermediate (1-3 yrs)", "Experienced (3+ yrs)"],
                index=1
            )
        with col_risk:
            risk_tolerance = st.selectbox(
                t("lbl_risk_tolerance", lang),
                options=["Conservative", "Moderate", "Aggressive"],
                index=1
            )

        monthly_income = st.number_input(
            "Monthly Household Income (₹, Optional)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_inputs.get("monthly_income", 30000.0)),
            step=5000.0
        )

    col_btn, col_alt_btn = st.columns([2, 2])
    with col_btn:
        run_btn = st.button("🔍 " + t("btn_run_assessment", lang), type="primary", use_container_width=True)
    with col_alt_btn:
        if st.button("💡 What business can I start with this budget?", use_container_width=True):
            st.session_state["budget_search_capital"] = own_capital
            st.switch_page("pages/07_Business_Alternatives.py")

# Run or re-calculate assessment
if run_btn or "viability_result" not in st.session_state or st.session_state.get("business", {}).get("category") != selected_category:
    errors = validate_assessment_inputs(own_capital, expected_investment)
    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
    else:
        # Perform calculation
        competitors_df = get_competitors(locality_id=selected_village_id, business_type=selected_category)
        hl_metrics = calculate_hyperlocal_metrics(selected_locality, selected_business, competitors_df)
        
        # Financial Plan
        fin_plan = calculate_financial_plan(
            project_cost=expected_investment,
            own_contribution=own_capital,
            monthly_sales=float(selected_business.get("typical_monthly_sales", 65000)),
            variable_cost_ratio=float(selected_business.get("variable_cost_ratio", 0.48)),
            monthly_fixed_cost=float(selected_business.get("monthly_fixed_cost", 7500)),
            unit_price=float(selected_business.get("unit_price_estimate", 80))
        )
        
        # Viability
        viability = calculate_viability_score(hl_metrics, fin_plan, selected_business, selected_locality)
        
        # Recommendation
        rec = generate_business_recommendation(viability, fin_plan, hl_metrics, selected_business, selected_locality)
        
        # Schemes
        schemes = evaluate_schemes(expected_investment, selected_category, ["General", "Rural"], is_existing)
        
        # Update session state
        st.session_state["assessment_data"] = {
            "name": user_name,
            "village_id": selected_village_id,
            "category": selected_category,
            "own_capital": own_capital,
            "expected_investment": expected_investment,
            "experience": experience,
            "is_existing": is_existing,
            "risk_tolerance": risk_tolerance,
            "monthly_income": monthly_income
        }
        st.session_state["locality"] = selected_locality
        st.session_state["business"] = selected_business
        st.session_state["competitors_df"] = competitors_df
        st.session_state["hyperlocal_metrics"] = hl_metrics
        st.session_state["financial_plan"] = fin_plan
        st.session_state["viability_result"] = viability
        st.session_state["recommendation"] = rec
        st.session_state["schemes"] = schemes
        
        # Save to SQLite
        save_assessment({
            "locality_id": selected_village_id,
            "business_id": selected_business["business_id"],
            "own_capital": own_capital,
            "expected_investment": expected_investment,
            "experience_level": experience,
            "is_existing_business": is_existing,
            "monthly_household_income": monthly_income,
            "risk_tolerance": risk_tolerance,
            "viability_score": viability["viability_score"],
            "recommendation": rec["decision"]
        })

# Render Results
if "viability_result" in st.session_state:
    st.markdown("---")
    
    viab = st.session_state["viability_result"]
    rec = st.session_state["recommendation"]
    fin = st.session_state["financial_plan"]
    hl = st.session_state["hyperlocal_metrics"]
    loc = st.session_state["locality"]
    biz = st.session_state["business"]

    # Top Recommendation Banner
    col_dec, col_score = st.columns([3, 2])
    
    with col_dec:
        badge_class = f"badge-{rec['decision'].lower()}"
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:1.2rem; border-radius:12px;">
                <div style="font-size:0.85rem; color:#64748B; font-weight:700; text-transform:uppercase;">Final Decision Recommendation</div>
                <div style="display:flex; align-items:center; gap:12px; margin:8px 0;">
                    <span class="{badge_class}">{rec['decision']}</span>
                    <span style="font-size:1.2rem; font-weight:700; color:#1E293B;">{rec['decision_label']}</span>
                </div>
                <div style="color:#4B5563; font-size:0.9rem;">Confidence: <b>{rec['confidence']}</b> &bull; Source: <i>{rec['source']}</i></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_score:
        score_val = viab["viability_score"]
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:1.2rem; border-radius:12px; text-align:center;">
                <div style="font-size:0.85rem; color:#64748B; font-weight:700; text-transform:uppercase;">Viability Score</div>
                <div style="font-size:2.8rem; font-weight:800; color:{viab['status_color']};">{score_val:.0f} <span style="font-size:1.2rem; color:#94A3B8;">/ 100</span></div>
                <div style="font-weight:600; color:{viab['status_color']};">{viab['classification']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # Grounded Bullet Reasons
    st.markdown("#### 🎯 Key Grounded Decision Reasons")
    for r in rec["reasons"]:
        st.markdown(f"• {r}")

    # Evidence Panel
    st.markdown(
        f"""
        <div class="evidence-box">
            <b>🔍 Evidence Summary:</b> {rec['evidence']}<br/>
            <small><i>Note: {rec['disclaimer']}</i></small>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Factor Breakdown Visualization (Horizontal Bars & Radar)
    st.subheader("📈 Viability Factor Breakdown")
    
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        # Horizontal Bar Chart
        categories = list(viab["breakdown"].keys())
        scores = list(viab["breakdown"].values())
        
        colors_list = ["#10B981" if s >= 75 else ("#3B82F6" if s >= 60 else ("#F59E0B" if s >= 50 else "#EF4444")) for s in scores]
        
        fig_bar = go.Figure(go.Bar(
            x=scores,
            y=categories,
            orientation='h',
            marker_color=colors_list,
            text=[f"{s:.1f}" for s in scores],
            textposition='auto',
        ))
        fig_bar.update_layout(
            title="Factor Viability Scores (0 - 100)",
            xaxis=dict(range=[0, 100], title="Score"),
            yaxis=dict(autorange="reversed"),
            template="plotly_white",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        # Radar Chart
        radar_cats = categories + [categories[0]]
        radar_scores = scores + [scores[0]]
        
        fig_radar = go.Figure(go.Scatterpolar(
            r=radar_scores,
            theta=radar_cats,
            fill='toself',
            fillcolor='rgba(15, 118, 110, 0.25)',
            line=dict(color='#0F766E', width=2),
            name="Viability Profile"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Factor Radar Footprint",
            template="plotly_white",
            height=320,
            margin=dict(l=30, r=30, t=40, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # SWOT Framework
    st.subheader("🧭 Strategic SWOT Analysis")
    swot = rec.get("swot", {})
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("##### 🟢 **Strengths**")
        for s in swot.get("strengths", []):
            st.markdown(f"• {s}")
            
        st.markdown("##### 🔵 **Opportunities**")
        for o in swot.get("opportunities", []):
            st.markdown(f"• {o}")

    with sc2:
        st.markdown("##### 🟡 **Weaknesses**")
        for w in swot.get("weaknesses", []):
            st.markdown(f"• {w}")
            
        st.markdown("##### 🔴 **Threats**")
        for th in swot.get("threats", []):
            st.markdown(f"• {th}")

render_disclaimer_footer(lang)

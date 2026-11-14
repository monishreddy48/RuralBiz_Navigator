"""
RuralBiz Navigator - What-If Scenario Stress Testing
Simulates adverse economic shocks (sales declines, inflation, rate hikes) and tests enterprise survival.
"""
import streamlit as st
import plotly.graph_objects as go
from utils.ui_components import (
    load_custom_css,
    render_sidebar,
    render_page_header,
    render_context_bar,
    render_disclaimer_footer
)
from i18n.translations import t
from core.scenario_engine import run_stress_scenario
from utils.formatting import format_inr

st.set_page_config(
    page_title="RuralBiz Navigator - What-If Simulator",
    page_icon="📉",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="WhatIf")
lang = st.session_state.get("language", "en")

render_page_header(
    category="FINANCIAL TOOLS",
    title="📉 " + t("nav_whatif", lang),
    description="Test the resilience of your venture against real-world rural shocks: demand drops, input price spikes, or interest rate increases."
)

render_context_bar()

fin = st.session_state.get("financial_plan")
hl = st.session_state.get("hyperlocal_metrics")
biz = st.session_state.get("business")
loc = st.session_state.get("locality")

if not fin or not biz or not loc or not hl:
    st.warning("⚠️ Please initialize or load an assessment from the Home or Feasibility page first.")
    st.stop()

# ==============================================================================
# SECTION 1: Scenario Shock Controls
# ==============================================================================
st.subheader("🎛️ Configure Market & Operational Shocks")
st.caption("Adjust adverse stress factors to test whether your venture can withstand severe rural market disruptions.")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown("##### 🛒 Demand & Price Shocks")
    sales_vol_shock = st.slider(
        "Sales Volume Shock (%)",
        min_value=-50,
        max_value=50,
        value=-20,
        step=5,
        help="Simulate drought, reduced footfall, or local competition"
    )
    price_shock = st.slider(
        "Selling Price Shock (%)",
        min_value=-30,
        max_value=30,
        value=-5,
        step=5,
        help="Simulate price war or deflationary market pressure"
    )

with col_s2:
    st.markdown("##### 📦 Operating Cost Shocks")
    var_cost_shock = st.slider(
        "Raw Material / Input Cost Shock (%)",
        min_value=-20,
        max_value=50,
        value=15,
        step=5,
        help="Simulate feed, diesel, packaging, or spice inflation"
    )
    fixed_cost_shock = st.slider(
        "Fixed Overhead / Rent Shock (%)",
        min_value=-20,
        max_value=50,
        value=10,
        step=5,
        help="Simulate commercial rent increase or utility tariff spike"
    )

with col_s3:
    st.markdown("##### 💳 Debt & Financing Shocks")
    rate_shock = st.slider(
        "Interest Rate Shift (% Points)",
        min_value=-3.0,
        max_value=5.0,
        value=1.5,
        step=0.5,
        help="Simulate RBI repo rate hike or lender risk premium"
    )
    loan_delta = st.slider(
        "Loan Size Revision (%)",
        min_value=-40,
        max_value=40,
        value=0,
        step=5,
        help="Simulate scaling setup machinery up or down"
    )

# Compute Stress Results Deterministically
scenario_results = run_stress_scenario(
    base_plan=fin,
    hyperlocal_metrics=hl,
    business=biz,
    locality=loc,
    sales_vol_delta_pct=sales_vol_shock,
    price_delta_pct=price_shock,
    var_cost_delta_pct=var_cost_shock,
    fixed_cost_delta_pct=fixed_cost_shock,
    interest_rate_delta=rate_shock,
    loan_amount_delta_pct=loan_delta
)

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 2: Survival Verdict Banner
# ==============================================================================
st.subheader("🛡️ Enterprise Survival Verdict")
surv_status = scenario_results["survival_status"]
surv_color = scenario_results["survival_color"]
surv_text = scenario_results["survival_verdict"]

badge_style = "badge-go" if "SURVIVES" in surv_status else ("badge-avoid" if "FAILS" in surv_status else "badge-modify")

st.markdown(
    f"""
    <div class="surface-card" style="border-left: 6px solid {surv_color};">
        <div style="font-size:0.75rem; color:#6B7280; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">Would This Business Still Survive?</div>
        <div style="display:flex; align-items:center; gap:12px; margin:8px 0;">
            <span class="{badge_style}">{surv_status}</span>
        </div>
        <div style="font-size:1.05rem; font-weight:600; color:#111827; line-height:1.4;">{surv_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: Side-by-Side Comparison (Base vs Stress)
# ==============================================================================
st.subheader("⚖️ Base Case vs. Stress Case Comparison")

base = scenario_results["base_case"]
stress = scenario_results["stress_case"]

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Monthly Revenue",
    format_inr(stress["monthly_sales"]),
    f"{((stress['monthly_sales'] - base['monthly_sales'])/base['monthly_sales'])*100:+.1f}% vs Base"
)
c2.metric(
    "Monthly Net Profit",
    format_inr(stress["monthly_net_profit"]),
    f"{format_inr(stress['monthly_net_profit'] - base['monthly_net_profit'])} delta"
)
c3.metric(
    "Debt Coverage (DSCR)",
    f"{stress['dscr']:.2f}",
    f"{stress['dscr'] - base['dscr']:+.2f} shift"
)
c4.metric(
    "Break-Even Revenue",
    format_inr(stress["break_even_revenue"]),
    f"{((stress['break_even_revenue'] - base['break_even_revenue'])/base['break_even_revenue'])*100:+.1f}%"
)

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 4: Comparative Bar Chart
# ==============================================================================
fig_comp = go.Figure()

metrics_labels = ["Gross Revenue", "Operating Profit", "Monthly Net Flow", "Monthly EMI"]
base_vals = [base["monthly_sales"], fin["monthly_operating_profit"], base["monthly_net_profit"], base["monthly_emi"]]
stress_vals = [
    stress["monthly_sales"],
    stress["stress_plan"]["monthly_operating_profit"],
    stress["monthly_net_profit"],
    stress["monthly_emi"]
]

fig_comp.add_trace(go.Bar(
    x=metrics_labels,
    y=base_vals,
    name="Base Plan",
    marker=dict(color="#0F5132", line=dict(color="#FFFFFF", width=1)),
    text=[format_inr(v) for v in base_vals],
    textposition="auto"
))

fig_comp.add_trace(go.Bar(
    x=metrics_labels,
    y=stress_vals,
    name="Stress Case",
    marker=dict(color="#DC2626" if stress["monthly_net_profit"] < 0 else "#D97706", line=dict(color="#FFFFFF", width=1)),
    text=[format_inr(v) for v in stress_vals],
    textposition="auto"
))

fig_comp.update_layout(
    title="Financial Resilience: Base Case vs Stress Case (₹ / Month)",
    barmode="group",
    template="plotly_white",
    height=380,
    yaxis=dict(title="Rupees (₹)", gridcolor="#F3F4F6"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 5: Advisory Takeaways
# ==============================================================================
st.subheader("💡 Stress Mitigation Guidance")

if stress["monthly_net_profit"] < 0:
    st.markdown(
        """
        <div class="surface-card" style="border-left: 4px solid #DC2626;">
            <b style="color:#991B1B;">⚠️ Critical Capital Action Required:</b><br/>
            Under this adverse shock, the unit incurs operating deficits. Consider negotiating flexible vendor payment cycles or maintaining at least <b>4 months of fixed operating expenses</b> in liquid reserve before launch.<br/><br/>
            <b style="color:#991B1B;">💳 Debt Restructuring Recommended:</b><br/>
            Explore subsidized interest schemes (e.g. DAY-NRLM or PM Vishwakarma at 5% interest subvention) to reduce debt service burden.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="surface-card" style="border-left: 4px solid #0F5132;">
            <b style="color:#065F46;">✅ Resilient Financial Buffer:</b><br/>
            The venture retains positive net cash flow under simulated stress. Your operating margins are sufficiently broad to absorb normal rural seasonality.<br/><br/>
            <b style="color:#065F46;">🛡️ Best Practice:</b><br/>
            Retain <b>20% of peak monthly surplus</b> in a liquid bank sweep account to protect against unexpected localized commodity price volatility.
        </div>
        """,
        unsafe_allow_html=True
    )

render_disclaimer_footer(lang)

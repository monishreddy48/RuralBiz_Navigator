"""
RuralBiz Navigator - Financial Calculator & Debt Structuring
Implements reducing-balance EMI, 12-month cash flows, break-even analysis, and DSCR.
Pure deterministic mathematics.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer
from i18n.translations import t
from core.financial_engine import calculate_financial_plan
from utils.formatting import format_inr, format_pct

st.set_page_config(
    page_title="RuralBiz Navigator - Financial Calculator",
    page_icon="💳",
    layout="wide"
)

load_custom_css()
render_sidebar()
lang = st.session_state.get("language", "en")

st.title("💳 " + t("nav_financial", lang))
st.caption("Deterministic loan structuring, reducing-balance EMI, cash flow simulation, and break-even analysis.")

# Fetch active assessment state
fin = st.session_state.get("financial_plan")
biz = st.session_state.get("business")

if not fin or not biz:
    st.warning("⚠️ Please initialize an assessment from the Home or Feasibility page.")
    st.stop()

# Interactive Financial Assumptions Bar
with st.expander("⚙️ **Adjust Financing & Operating Assumptions**", expanded=True):
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    
    with col_a1:
        cost_val = st.number_input(
            "Project Cost (₹)",
            min_value=10000.0,
            max_value=5000000.0,
            value=float(fin.get("project_cost", 215000.0)),
            step=10000.0
        )
        own_pct_slider = st.slider(
            "Own Contribution (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(fin.get("own_pct", 25.0)),
            step=5.0
        )
        own_cap_calc = round(cost_val * (own_pct_slider / 100.0), 2)
        
    with col_a2:
        interest_rate = st.number_input(
            "Interest Rate (% p.a.)",
            min_value=0.0,
            max_value=24.0,
            value=float(fin.get("annual_interest_rate", 9.5)),
            step=0.25,
            help="Commercial MSME rate or subsidized rate"
        )
        tenure_months = st.slider(
            "Tenure (Months)",
            min_value=6,
            max_value=84,
            value=int(fin.get("tenure_months", 60)),
            step=6
        )

    with col_a3:
        moratorium_months = st.slider(
            "Moratorium (Months)",
            min_value=0,
            max_value=12,
            value=int(fin.get("moratorium_months", 3)),
            step=1,
            help="Grace period before principal repayment begins"
        )
        monthly_sales = st.number_input(
            t("lbl_monthly_sales", lang) + " (₹)",
            min_value=5000.0,
            max_value=1000000.0,
            value=float(fin.get("monthly_sales", 65000.0)),
            step=5000.0
        )

    with col_a4:
        var_cost_pct = st.slider(
            "Variable Cost / COGS (%)",
            min_value=10,
            max_value=85,
            value=int(float(biz.get("variable_cost_ratio", 0.48)) * 100),
            step=2
        )
        fixed_costs = st.number_input(
            "Monthly Fixed Costs (₹)",
            min_value=1000.0,
            max_value=200000.0,
            value=float(fin.get("monthly_fixed_costs", 7500.0)),
            step=1000.0,
            help="Rent, shop electricity, basic maintenance"
        )

# Re-compute financial plan with adjusted sliders
fin = calculate_financial_plan(
    project_cost=cost_val,
    own_contribution=own_cap_calc,
    annual_interest_rate=interest_rate,
    tenure_months=tenure_months,
    moratorium_months=moratorium_months,
    monthly_sales=monthly_sales,
    variable_cost_ratio=var_cost_pct / 100.0,
    monthly_fixed_cost=fixed_costs,
    unit_price=float(biz.get("unit_price_estimate", 80))
)
st.session_state["financial_plan"] = fin

st.markdown("---")

# Key Metrics Row
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Total Project Cost", format_inr(fin["project_cost"]), f"Loan: {format_inr(fin['loan_amount'])}")
col_m2.metric(t("lbl_monthly_emi", lang), format_inr(fin["monthly_emi"]), f"{fin['tenure_months']} mos @ {fin['annual_interest_rate']}%")
col_m3.metric(t("lbl_net_profit", lang), format_inr(fin["monthly_net_profit"]), f"Margin: {fin['net_margin_pct']}%")
col_m4.metric(t("lbl_break_even", lang), format_inr(fin["break_even_revenue"]), f"Safety: {fin['margin_of_safety_pct']}%")
col_m5.metric(t("lbl_dscr", lang), f"{fin['dscr']:.2f}", fin["dscr_badge"])

# DSCR Health Warning
if fin["dscr"] < 1.2 and fin["loan_amount"] > 0:
    st.error(f"⚠️ **High Debt Risk Notice:** DSCR is {fin['dscr']:.2f}. Commercial lenders require a minimum DSCR of 1.20 to approve credit.")
elif fin["dscr"] >= 1.5:
    st.success(f"✅ **Healthy Debt Capacity:** DSCR is {fin['dscr']:.2f}. Your operating cash flows provide a substantial buffer against default.")

st.markdown("<br/>", unsafe_allow_html=True)

# Visual Charts: Capital Donut & 12-Month Cash Flow
col_c1, col_c2 = st.columns([2, 3])

with col_c1:
    st.subheader("🥧 Capital Structure")
    fig_donut = go.Figure(go.Pie(
        labels=["Entrepreneur Equity (Own)", "Institutional Debt (Loan)"],
        values=[fin["own_contribution"], fin["loan_amount"]],
        hole=0.55,
        marker=dict(colors=["#10B981", "#3B82F6"])
    ))
    fig_donut.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_c2:
    st.subheader("📈 12-Month Dynamic Cash Flow Projection")
    df_cf = pd.DataFrame(fin["cash_flow_12"])
    
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Scatter(
        x=[f"M{m}" for m in df_cf["month"]],
        y=df_cf["revenue"],
        mode="lines+markers",
        name="Gross Revenue",
        line=dict(color="#10B981", width=2.5)
    ))
    fig_cf.add_trace(go.Scatter(
        x=[f"M{m}" for m in df_cf["month"]],
        y=df_cf["operating_profit"],
        mode="lines+markers",
        name="Operating Profit (EBITDA)",
        line=dict(color="#3B82F6", width=2)
    ))
    fig_cf.add_trace(go.Scatter(
        x=[f"M{m}" for m in df_cf["month"]],
        y=df_cf["net_cash_flow"],
        mode="lines+markers",
        name="Net Cash Flow (After EMI)",
        line=dict(color="#D97706", width=2, dash="dash")
    ))
    fig_cf.add_trace(go.Scatter(
        x=[f"M{m}" for m in df_cf["month"]],
        y=df_cf["closing_cash"],
        mode="lines",
        name="Closing Cash Balance",
        line=dict(color="#8B5CF6", width=2),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.08)"
    ))
    fig_cf.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(title="Amount (₹)"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_cf, use_container_width=True)

st.markdown("---")

# Break-Even Summary Box
st.subheader("⚖️ Break-Even Economics")
b1, b2, b3 = st.columns(3)
b1.info(f"**Monthly Break-Even Sales:** {format_inr(fin['break_even_revenue'])}\n\n*Required monthly revenue to cover all fixed costs & loan EMI.*")
b2.info(f"**Break-Even Units:** {fin['break_even_units']:,} units / month\n\n*Assuming unit price of ₹{biz.get('unit_price_estimate', 80):.0f}.*")
b3.info(f"**Safety Margin:** {fin['margin_of_safety_pct']:.1f}%\n\n*Sales can fall by this percentage before the business breaches break-even.*")

st.markdown("---")

# Loan Amortization Schedule Table
st.subheader("📋 Reducing-Balance Amortization Schedule")
st.caption("Month-by-month principal and interest breakdown with 3-month moratorium buffer.")

if fin["amortization_schedule"]:
    df_amort = pd.DataFrame(fin["amortization_schedule"])
    df_amort_view = df_amort[["month", "opening_balance", "emi", "interest", "principal", "closing_balance", "is_moratorium"]].copy()
    df_amort_view.rename(columns={
        "month": "Month",
        "opening_balance": "Opening Bal (₹)",
        "emi": "EMI Paid (₹)",
        "interest": "Interest (₹)",
        "principal": "Principal (₹)",
        "closing_balance": "Closing Bal (₹)",
        "is_moratorium": "Grace Period?"
    }, inplace=True)
    
    st.dataframe(df_amort_view.head(24), use_container_width=True, hide_index=True)
    st.caption(f"Showing first 24 months of total {fin['tenure_months']} months schedule.")

render_disclaimer_footer(lang)

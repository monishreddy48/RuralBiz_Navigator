"""
RuralBiz Navigator - Detailed Project Report (DPR) Generator
Generates bankable 20-section project proposal and provides instant PDF download.
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
from reports.pdf_generator import generate_dpr_pdf
from utils.formatting import format_inr
from config import REPORTS_DIR

st.set_page_config(
    page_title="RuralBiz Navigator - DPR Generator",
    page_icon="📄",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="DPR")
lang = st.session_state.get("language", "en")

render_page_header(
    category="FINANCIAL TOOLS",
    title="📄 " + t("nav_dpr", lang),
    description="Generate a professional, bank-ready Detailed Project Report (DPR) combining market data, debt schedules, SWOT matrix, and scheme options."
)

render_context_bar()

assessment_data = st.session_state.get("assessment_data", {})
loc = st.session_state.get("locality")
biz = st.session_state.get("business")
hl = st.session_state.get("hyperlocal_metrics")
fin = st.session_state.get("financial_plan")
viab = st.session_state.get("viability_result")
rec = st.session_state.get("recommendation")
schemes = st.session_state.get("schemes", [])

if not loc or not biz or not fin or not viab:
    st.warning("⚠️ Please complete or load an assessment first to compile your DPR.")
    st.stop()

# ==============================================================================
# SECTION 1: Report Metadata & KPIs
# ==============================================================================
st.subheader("📑 Report Specification & Key Metrics")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Project Title", biz.get("business_name", "Enterprise"))
c2.metric("Total Outlay", format_inr(fin.get("project_cost", 0)))
c3.metric("Viability Score", f"{viab.get('viability_score', 0):.0f} / 100", viab.get("classification"))
c4.metric("Advisory Recommendation", rec.get("decision", "MODIFY"), rec.get("decision_label"))

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 2: PDF Download & 20-Section Framework
# ==============================================================================
col_gen, col_info = st.columns([1.5, 2.5])

with col_gen:
    st.markdown("#### 📥 Instant PDF Download")
    pdf_filename = "RuralBiz_Navigator_Business_Report.pdf"
    
    with st.spinner("Compiling bankable ReportLab PDF with 20 sections..."):
        pdf_bytes = generate_dpr_pdf(
            assessment_data=assessment_data,
            locality=loc,
            business=biz,
            hyperlocal_metrics=hl,
            financial_plan=fin,
            viability_result=viab,
            recommendation=rec,
            schemes=schemes,
            output_path=str(REPORTS_DIR / pdf_filename)
        )
        
    st.download_button(
        label="📄 Download Official DPR Report (PDF)",
        data=pdf_bytes,
        file_name=pdf_filename,
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    st.markdown(
        """
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:10px 12px; font-size:0.84rem; color:#166534; margin-top:12px;">
            ✅ <b>PDF compiled successfully!</b> Ready for submission to District Task Force Committees (PMEGP), Lead District Managers (LDM), and commercial bank branch managers.
        </div>
        """,
        unsafe_allow_html=True
    )

with col_info:
    st.markdown("#### 📋 20-Section Bankable Framework")
    st.markdown(
        """
        Your generated DPR PDF contains the following standard institutional sections:
        
        1. **Entrepreneur Profile & KYC Declaration**
        2. **Business Activity & Unit Benchmarks**
        3. **Locality Catchment & Connectivity Indices**
        4. **Hyper-Local Market & Customer Pool (5–10 km)**
        5. **Competitor Mapping & Demand Gap Analysis**
        6. **Weighted Viability Scoring (0–100)**
        7. **Deterministic Strategic SWOT Framework**
        8. **CapEx & Working Capital Structuring**
        9. **Institutional Debt & Equity Contribution**
        10. **12-Month Revenue & Operating Projections**
        11. **Cost of Goods Sold (COGS) & Fixed Overheads**
        12. **Reducing-Balance EMI Amortization Schedule**
        13. **12-Month Dynamic Cash Flow Statement**
        14. **Break-Even Analysis (Revenue & Units)**
        15. **Debt Service Coverage Ratio (DSCR) Audit**
        16. **What-If Sensitivity & Stress Test Matrix**
        17. **Government Schemes & Subsidy Eligibility**
        18. **Operational & Supply Chain Risks**
        19. **Final GO / MODIFY / AVOID Recommendation**
        20. **Legal, Statutory & Prototype Data Disclaimer**
        """
    )

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 3: Quick Preview of Report Data
# ==============================================================================
with st.expander("👀 **Preview Key DPR Tables (Amortization & Cash Flow)**"):
    t1, t2 = st.tabs(["12-Month P&L Cash Flow", "Repayment Amortization Schedule"])
    
    with t1:
        df_cf = pd.DataFrame(fin.get("cash_flow_12", []))
        st.dataframe(df_cf, use_container_width=True, hide_index=True)
        
    with t2:
        df_amort = pd.DataFrame(fin.get("amortization_schedule", []))
        st.dataframe(df_amort.head(12), use_container_width=True, hide_index=True)

render_disclaimer_footer(lang)

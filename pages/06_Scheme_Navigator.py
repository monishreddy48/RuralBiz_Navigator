"""
RuralBiz Navigator - Government Scheme Navigator
Rule-based matching against verified Indian government micro-enterprise schemes.
NO fabricated benefits.
"""
import streamlit as st
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer
from i18n.translations import t
from core.scheme_engine import evaluate_schemes
from utils.formatting import format_inr

st.set_page_config(
    page_title="RuralBiz Navigator - Scheme Navigator",
    page_icon="🏛️",
    layout="wide"
)

load_custom_css()
render_sidebar()
lang = st.session_state.get("language", "en")

st.title("🏛️ " + t("nav_schemes", lang))
st.caption("Verified rule-based routing for Central & State credit-linked subsidies and micro-finance programmes.")

fin = st.session_state.get("financial_plan")
biz = st.session_state.get("business")
user_inputs = st.session_state.get("assessment_data", {})

project_cost = float(fin.get("project_cost", 215000.0)) if fin else 215000.0
category = biz.get("category", "Food Processing") if biz else "Food Processing"

# Beneficiary Category Filters
st.subheader("🎯 Applicant Profile & Scheme Matching Filters")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    cost_override = st.number_input(
        "Project Budget (₹)",
        min_value=10000.0,
        max_value=10000000.0,
        value=project_cost,
        step=25000.0
    )
with col_f2:
    selected_tags = st.multiselect(
        "Beneficiary Profile Tags",
        options=["General", "Rural", "Women Entrepreneur", "SC / ST Category", "OBC", "Traditional Artisan / Craftsman", "SHG Member"],
        default=["General", "Rural"]
    )
with col_f3:
    is_existing = st.checkbox("Existing Enterprise (Upgrade / Expansion)", value=user_inputs.get("is_existing", False))

# Re-evaluate schemes
matched_schemes = evaluate_schemes(cost_override, category, selected_tags, is_existing)
st.session_state["schemes"] = matched_schemes

st.markdown("---")

# Summary Badges
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
matched_count = sum(1 for s in matched_schemes if s["match_status"] == "MATCHED")
possible_count = sum(1 for s in matched_schemes if s["match_status"] == "POSSIBLE")
verify_count = sum(1 for s in matched_schemes if s["match_status"] == "VERIFICATION REQUIRED")

col_b1.metric("Fully Matched Schemes", matched_count, "Top Priority")
col_b2.metric("Potential Alternate Schemes", possible_count, "Review Criteria")
col_b3.metric("Verification Required", verify_count, "Ceiling Review")
col_b4.metric("Total Database Schemes", len(matched_schemes), "Verified Rules")

st.markdown("<br/>", unsafe_allow_html=True)

# Scheme Detail Cards
st.subheader("📋 Matched Schemes & Guidelines")

for s in matched_schemes:
    status = s["match_status"]
    status_color = s["status_color"]
    
    with st.container():
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left: 6px solid {status_color}; border-radius:10px; padding:1.2rem; margin-bottom:1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div style="font-size:1.15rem; font-weight:700; color:#1E293B;">{s['name']}</div>
                    <span style="background:{status_color}; color:white; font-size:0.8rem; font-weight:800; padding:4px 10px; border-radius:6px; letter-spacing:0.5px;">
                        {status}
                    </span>
                </div>
                <div style="color:#64748B; font-size:0.88rem; margin:6px 0;">{s['description']}</div>
                <div style="background:#F8FAFC; padding:8px 12px; border-radius:6px; font-size:0.85rem; color:#1E3A8A; margin:8px 0;">
                    <b>Why it may fit:</b> {s['fit_reason']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(f"🔍 View Eligibility Checks, Required Documents & Application Route ({s['name'][:35]}...)"):
            col_d1, col_d2 = st.columns([1.2, 1.0])
            
            with col_d1:
                st.markdown("##### 📌 **Financing & Terms**")
                st.markdown(f"• **Loan Amount Available:** {s.get('loan_available', 'N/A')}")
                st.markdown(f"• **Subsidy Available:** {s.get('subsidy_available', 'N/A')}")
                if s.get("estimated_subsidy_rupees", 0) > 0:
                    st.markdown(f"• **Potential Subsidy Value:** ~{format_inr(s['estimated_subsidy_rupees'])}")
                st.markdown(f"• **Beneficiary Margin Contribution:** {s.get('margin_requirement', 'N/A')}")
                st.markdown(f"• **Interest Rate Policy:** {s.get('interest_notes', 'N/A')}")
                st.markdown(f"• **Collateral Security:** {s.get('collateral_notes', 'N/A')}")
                st.markdown(f"• **Application Route:** {s.get('application_route', 'N/A')}")
                st.markdown(f"• **Official Source Portal:** [Click to Visit Official Portal]({s.get('source_url', '#')})")
                st.caption(f"Last Verified Date: {s.get('last_verified_date', '2026-01-01')} &bull; Status: {s.get('verification_status')}")

            with col_d2:
                st.markdown("##### ✅ **Eligibility Checklist**")
                for chk in s.get("eligibility_checks", []):
                    icon = "✅" if chk["passed"] else "⚠️"
                    st.markdown(f"{icon} **{chk['criterion']}**  \n<small style='color:#6B7280;'>{chk['detail']}</small>", unsafe_allow_html=True)
                
                st.markdown("##### 📄 **Mandatory Documents**")
                for doc in s.get("documents", []):
                    st.markdown(f"• {doc}")

render_disclaimer_footer(lang)

"""
RuralBiz Navigator - Government Scheme Navigator
Rule-based matching against verified Indian government micro-enterprise schemes.
NO fabricated benefits.
"""
import streamlit as st
from utils.ui_components import (
    load_custom_css,
    render_sidebar,
    render_page_header,
    render_context_bar,
    render_disclaimer_footer
)
from i18n.translations import t
from core.scheme_engine import evaluate_schemes
from utils.formatting import format_inr

st.set_page_config(
    page_title="RuralBiz Navigator - Scheme Navigator",
    page_icon="🏛️",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="Schemes")
lang = st.session_state.get("language", "en")

render_page_header(
    category="GOVERNMENT SUPPORT",
    title="🏛️ " + t("nav_schemes", lang),
    description="Verified rule-based routing for Central & State credit-linked subsidies, collateral-free credit guarantees, and micro-enterprise programmes."
)

render_context_bar()

fin = st.session_state.get("financial_plan")
biz = st.session_state.get("business")
user_inputs = st.session_state.get("assessment_data", {})

project_cost = float(fin.get("project_cost", 215000.0)) if fin else 215000.0
category = biz.get("category", "Food Processing") if biz else "Food Processing"

# ==============================================================================
# SECTION 1: Beneficiary Profile Filters
# ==============================================================================
with st.expander("🎯 **Applicant Profile & Scheme Matching Criteria**", expanded=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cost_override = st.number_input(
            "Target Project Outlay (₹)",
            min_value=10000.0,
            max_value=10000000.0,
            value=project_cost,
            step=25000.0
        )
    with col_f2:
        selected_tags = st.multiselect(
            "Beneficiary Profile Attributes",
            options=["General", "Rural", "Women Entrepreneur", "SC / ST Category", "OBC", "Traditional Artisan / Craftsman", "SHG Member"],
            default=["General", "Rural"]
        )
    with col_f3:
        is_existing = st.checkbox("Existing Enterprise (Upgrade / Expansion)", value=user_inputs.get("is_existing", False))

# Re-evaluate schemes deterministically
matched_schemes = evaluate_schemes(cost_override, category, selected_tags, is_existing)
st.session_state["schemes"] = matched_schemes

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: Summary Metrics
# ==============================================================================
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
matched_count = sum(1 for s in matched_schemes if s["match_status"] == "MATCHED")
possible_count = sum(1 for s in matched_schemes if s["match_status"] == "POSSIBLE")
verify_count = sum(1 for s in matched_schemes if s["match_status"] == "VERIFICATION REQUIRED")

col_b1.metric("Fully Matched Schemes", matched_count, "Highest Alignment")
col_b2.metric("Potential Alternatives", possible_count, "Review Criteria")
col_b3.metric("Verification Required", verify_count, "Ceiling Review")
col_b4.metric("Total Database Schemes", len(matched_schemes), "Verified Rules")

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 3: Scheme Cards & Details
# ==============================================================================
st.subheader("📋 Matched Government Schemes & Guidelines")
st.caption("Official schemes matched deterministically against your project outlay, business classification, and demographic eligibility criteria.")

for s in matched_schemes:
    status = s["match_status"]
    status_color = s["status_color"]
    
    status_badge_class = "badge-go" if status == "MATCHED" else ("badge-modify" if status == "POSSIBLE" else "badge-avoid")
    
    with st.container():
        st.markdown(
            f"""
            <div class="surface-card" style="border-left: 6px solid {status_color}; margin-bottom: 0.75rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div style="font-size:1.15rem; font-weight:800; color:#111827;">{s['name']}</div>
                    <span style="background:{status_color}; color:white; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:4px; letter-spacing:0.04em;">
                        {status}
                    </span>
                </div>
                <div style="color:#6B7280; font-size:0.88rem; margin:6px 0 10px 0; line-height:1.4;">{s['description']}</div>
                <div style="background:#F0FDF4; border:1px solid #DCFCE7; padding:8px 12px; border-radius:6px; font-size:0.85rem; color:#065F46;">
                    <b>Why it matches:</b> {s['fit_reason']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(f"🔍 View Full Terms, Checklist & Application Route for {s['name'][:35]}..."):
            col_d1, col_d2 = st.columns([1.2, 1.0])
            
            with col_d1:
                st.markdown("##### 📌 Financing & Terms")
                st.markdown(f"• **Loan Amount Available:** {s.get('loan_available', 'N/A')}")
                st.markdown(f"• **Subsidy Available:** {s.get('subsidy_available', 'N/A')}")
                if s.get("estimated_subsidy_rupees", 0) > 0:
                    st.markdown(f"• **Potential Subsidy Value:** ~{format_inr(s['estimated_subsidy_rupees'])}")
                st.markdown(f"• **Beneficiary Margin Contribution:** {s.get('margin_requirement', 'N/A')}")
                st.markdown(f"• **Interest Rate Policy:** {s.get('interest_notes', 'N/A')}")
                st.markdown(f"• **Collateral Security:** {s.get('collateral_notes', 'N/A')}")
                st.markdown(f"• **Application Route:** {s.get('application_route', 'N/A')}")
                st.markdown(f"• **Official Source Portal:** [Click to Visit Official Portal]({s.get('source_url', '#')})")
                st.caption(f"Last Verified: {s.get('last_verified_date', '2026-01-01')} &bull; Status: {s.get('verification_status')}")

            with col_d2:
                st.markdown("##### ✅ Eligibility Checklist")
                for chk in s.get("eligibility_checks", []):
                    icon = "✅" if chk["passed"] else "⚠️"
                    st.markdown(f"{icon} **{chk['criterion']}**  \n<small style='color:#6B7280;'>{chk['detail']}</small>", unsafe_allow_html=True)
                
                st.markdown("##### 📄 Required Documentation")
                for doc in s.get("documents", []):
                    st.markdown(f"• {doc}")
        
        st.markdown("<br/>", unsafe_allow_html=True)

render_disclaimer_footer(lang)

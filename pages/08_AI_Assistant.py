"""
RuralBiz Navigator - Multilingual AI Advisory Assistant
Grounds natural-language queries in deterministic calculation facts.
Outputs explainable structured advice: ANSWER, WHY, EVIDENCE, FINANCIAL IMPACT, RISK, NEXT STEP.
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
from ai.router import ask_advisory_assistant, get_active_provider

st.set_page_config(
    page_title="RuralBiz Navigator - AI Assistant",
    page_icon="🤖",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="AI")
lang = st.session_state.get("language", "en")

render_page_header(
    category="AI SUPPORT",
    title="🤖 " + t("nav_ai", lang),
    description="Ask natural-language questions about your business viability, financial plan, EMI structure, or matched government schemes in English, Hindi, Telugu, or Kannada."
)

render_context_bar()

# Provider Status Banner
_, provider_status = get_active_provider()
if "Demo Mode" in provider_status:
    st.markdown(
        """
        <div class="surface-card" style="border-left: 4px solid #10B981; padding:10px 14px; margin-bottom:1rem;">
            <b>🤖 Active AI Engine:</b> Demo Mode (Deterministic Local Knowledge Base) &bull; <i>No external API keys or cloud dependencies required.</i>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class="surface-card" style="border-left: 4px solid #0F5132; padding:10px 14px; margin-bottom:1rem;">
            <b>⚡ Active AI Engine:</b> {provider_status} &bull; <i>Live API Connected.</i>
        </div>
        """,
        unsafe_allow_html=True
    )

# Extract active context
loc = st.session_state.get("locality", {})
biz = st.session_state.get("business", {})
viab = st.session_state.get("viability_result", {})
fin = st.session_state.get("financial_plan", {})
rec = st.session_state.get("recommendation", {})
schemes = st.session_state.get("schemes", [])

matched_scheme_names = [s["name"] for s in schemes if s.get("match_status") in ["MATCHED", "POSSIBLE"]]

context_package = {
    "locality_name": loc.get("village_name", "Demo Village"),
    "locality_population": loc.get("population", 3000),
    "locality_district": loc.get("district", "District"),
    "business_name": biz.get("business_name", "Micro Business"),
    "category": biz.get("category", "General"),
    "viability_score": viab.get("viability_score", 78),
    "classification": viab.get("classification", "Promising"),
    "recommendation": rec.get("decision", "GO"),
    "decision_label": rec.get("decision_label", "Proceed"),
    "project_cost": fin.get("project_cost", 215000),
    "own_capital": fin.get("own_contribution", 300000),
    "loan_amount": fin.get("loan_amount", 50000),
    "monthly_sales": fin.get("monthly_sales", 65000),
    "monthly_profit": fin.get("monthly_net_profit", 18500),
    "monthly_emi": fin.get("monthly_emi", 3500),
    "dscr": fin.get("dscr", 1.45),
    "break_even_revenue": fin.get("break_even_revenue", 42000),
    "margin_of_safety_pct": fin.get("margin_of_safety_pct", 35.0),
    "matched_schemes": matched_scheme_names
}

# Quick Prompt Suggestions
st.markdown("#### 💡 Quick Inquiry Prompts")
st.caption("Click any prompt below to query the advisory assistant based on your loaded assessment facts:")

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    if st.button("❓ Why is this business recommended?", use_container_width=True):
        st.session_state["pending_prompt"] = f"Why did you give {biz.get('business_name', 'this business')} a viability score of {viab.get('viability_score', 78)}?"
    if st.button("💳 How much EMI will I pay?", use_container_width=True):
        st.session_state["pending_prompt"] = f"How much loan and EMI will I pay for {biz.get('business_name', 'this business')}?"
with col_p2:
    if st.button("📉 What happens if sales fall 20%?", use_container_width=True):
        st.session_state["pending_prompt"] = "What happens if sales fall by 20%? Will my business still survive?"
    if st.button("🏛️ Which government scheme may fit me?", use_container_width=True):
        st.session_state["pending_prompt"] = "Which government scheme and subsidy fits my business setup?"
with col_p3:
    if st.button("💰 What business can I start with ₹2 lakh?", use_container_width=True):
        st.session_state["pending_prompt"] = "What business can I start with ₹2 lakh capital in my locality?"
    if st.button("🌐 Explain this in Hindi / हिंदी", use_container_width=True):
        st.session_state["pending_prompt"] = "Explain this recommendation and loan calculation in Hindi."

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {
            "role": "assistant",
            "content": f"Namaste! I am your RuralBiz Advisor for **{loc.get('village_name', 'your village')}**. I have analyzed your proposed **{biz.get('business_name', 'business')}** (Viability: {viab.get('viability_score', 78):.0f}/100, Recommendation: **{rec.get('decision', 'GO')}**). Ask me any question about your local market, cash flow, EMI, or government subsidies!"
        }
    ]

# Render existing chat
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle User Input
user_query = st.chat_input("Ask a question about your market, EMI, or schemes...")

if "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
    user_query = st.session_state.pop("pending_prompt")

if user_query:
    # Append user question
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Determine response language: if prompt contains 'hindi', respond in 'hi', etc.
    q_lower = user_query.lower()
    resp_lang = lang
    if "hindi" in q_lower or "हिंदी" in q_lower:
        resp_lang = "hi"
    elif "telugu" in q_lower or "తెలుగు" in q_lower:
        resp_lang = "te"
    elif "kannada" in q_lower or "ಕನ್ನಡ" in q_lower:
        resp_lang = "kn"

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing facts & structuring advisory response..."):
            answer_text, _ = ask_advisory_assistant(user_query, context_package, resp_lang)
            st.markdown(answer_text)
            st.session_state["chat_history"].append({"role": "assistant", "content": answer_text})

render_disclaimer_footer(lang)

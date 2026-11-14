"""
RuralBiz Navigator - About & Disclaimer
Explains Problem Statement 91, Hybrid Architecture, Mathematical Engines, and Prototype Disclaimers.
"""
import streamlit as st
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer
from i18n.translations import t

st.set_page_config(
    page_title="RuralBiz Navigator - About & Disclaimer",
    page_icon="ℹ️",
    layout="wide"
)

load_custom_css()
render_sidebar()
lang = st.session_state.get("language", "en")

st.title("ℹ️ " + t("nav_about", lang))
st.caption("Smart India Hackathon 2026 &bull; Problem Statement SIH26091 / PS 91")

st.markdown(
    """
    ### 🎯 **Smart India Hackathon 2026 Problem Statement**
    **Problem Statement ID:** SIH26091 / PS 91  
    **Title:** *AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs*  
    **Tagline:** *"Know your market. Know your money. Make a better business decision."*
    
    ---
    
    ### 🏗️ **Hybrid Architecture Principle**
    A fundamental design mandate of RuralBiz Navigator is the strict separation between conversational explanation and mathematical execution:
    """
)

col_arc1, col_arc2, col_arc3 = st.columns(3)

with col_arc1:
    st.markdown(
        """
        <div style="background:#F0FDF4; border:1px solid #10B981; border-radius:10px; padding:1rem; height:100%;">
            <div style="font-weight:700; color:#065F46; font-size:1.05rem;">🤖 Natural Language AI Layer</div>
            <div style="color:#047857; font-size:0.88rem; margin-top:6px;">
                • Multilingual user intent parsing<br/>
                • Natural language advisory explanations<br/>
                • Conversational context injection<br/>
                • Structured output format (ANSWER, WHY, EVIDENCE, FINANCIAL IMPACT, RISK, NEXT STEP)<br/>
                <i>*Zero mathematical formulas executed by LLM.*</i>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_arc2:
    st.markdown(
        """
        <div style="background:#EFF6FF; border:1px solid #3B82F6; border-radius:10px; padding:1rem; height:100%;">
            <div style="font-weight:700; color:#1E3A8A; font-size:1.05rem;">⚙️ Deterministic Python Engine</div>
            <div style="color:#1D4ED8; font-size:0.88rem; margin-top:6px;">
                • Standard reducing-balance EMI formula<br/>
                • Month-by-month loan amortization schedule<br/>
                • 12-month dynamic P&L and cash flow projection<br/>
                • Break-even point (revenue & volume)<br/>
                • Debt Service Coverage Ratio (DSCR)<br/>
                • Weighted Viability Scoring (0-100)<br/>
                • What-If shock sensitivity simulation
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_arc3:
    st.markdown(
        """
        <div style="background:#FFFBEB; border:1px solid #F59E0B; border-radius:10px; padding:1rem; height:100%;">
            <div style="font-weight:700; color:#92400E; font-size:1.05rem;">📂 Verified Data Layer</div>
            <div style="color:#B45309; font-size:0.88rem; margin-top:6px;">
                • SQLite relational persistence (`app.db`)<br/>
                • 10 micro-enterprise benchmark models<br/>
                • 7 representative rural demographic profiles<br/>
                • Hyper-local competitor mapping<br/>
                • Verified Indian Central & State schemes (PMEGP, MUDRA, PMFME, DAY-NRLM, Vishwakarma)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Architectural Flowchart
st.subheader("📐 System Workflow Diagram")
st.code(
    """
                        User Interface (Streamlit)
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
  AI Advisory Assistant                               Assessment Engine
  (Natural Language & Multilingual)                          |
         |                                                   v
  AI Provider Router                                  Hyper-Local Engine
  (Groq -> Gemini -> OpenAI -> Mock Fallback)                |
         |                                                   v
         +-------------------------+                     Data Layer
                                   |              (Localities, Competitors, Benchmarks)
                                   v                         |
                         Financial Math Engine               v
                         (Reducing-balance EMI,       Scheme Rule Engine
                          DSCR, Break-Even, P&L)      (PMEGP, MUDRA, PMFME, etc.)
                                   |                         |
                                   +------------+------------+
                                                |
                                                v
                                    Viability & Recommendation
                                    (0-100 Score & GO / MODIFY / AVOID)
                                                |
                                                v
                                    Downloadable DPR (ReportLab PDF)
    """,
    language="text"
)

st.markdown("---")

# Privacy and Security
st.subheader("🔒 Privacy, Security & Data Handling")
st.markdown(
    """
    - **No PII Mandate:** User name and household income are entirely optional. No Aadhaar, PAN, or bank credentials are ever collected or stored.
    - **Local Processing:** Financial simulations run locally on the server in Python.
    - **No Secret Leakage:** API keys are never exposed in frontend bundles and are loaded strictly from server-side environment variables.
    - **Graceful Offline Mode:** The application is architected to operate 100% reliably in Demo Mode without requiring any external cloud API connection.
    """
)

st.markdown("---")

# Legal & Institutional Disclaimer
st.subheader("⚖️ Legal & Institutional Disclaimer")
st.warning(
    """
    **Notice to Evaluators and Users:**  
    1. **Not Financial or Investment Advice:** RuralBiz Navigator provides informational and decision-support estimates based on available data and prototype assumptions. It does not constitute financial, legal, investment, or commercial lending advice.
    2. **No Success Guarantee:** The system does not guarantee business profitability, customer footfall, scheme eligibility, or bank loan approval. Final credit decisions are made solely by commercial lending institutions.
    3. **Synthetic Prototype Data:** Locality coordinates, customer catchment numbers, and competitor profiles in this prototype are synthetically constructed for demonstration purposes.
    4. **Verified Schemes:** Government scheme parameters (PMEGP, MUDRA, PMFME, Vishwakarma) reflect official Ministry guidelines, but terms and interest subventions are subject to official policy updates.
    """
)

render_disclaimer_footer(lang)

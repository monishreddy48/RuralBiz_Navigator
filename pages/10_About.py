"""
RuralBiz Navigator - About & Disclaimer
Explains Problem Statement 91, Hybrid Architecture, Mathematical Engines, and Prototype Disclaimers.
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

st.set_page_config(
    page_title="RuralBiz Navigator - About & Disclaimer",
    page_icon="ℹ️",
    layout="wide"
)

load_custom_css()
render_sidebar(current_page="About")
lang = st.session_state.get("language", "en")

render_page_header(
    category="ADDITIONAL",
    title="ℹ️ " + t("nav_about", lang),
    description="Smart India Hackathon 2026 &bull; Problem Statement SIH26091 / PS 91 &bull; Architecture, Computational Engine & Transparency Guidelines."
)

render_context_bar()

# ==============================================================================
# SECTION 1: SIH 2026 Problem Statement
# ==============================================================================
st.markdown(
    """
    <div class="surface-card" style="border-left: 6px solid #0F5132;">
        <div style="font-size:0.75rem; color:#0F5132; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">Problem Statement Overview</div>
        <div style="font-size:1.35rem; font-weight:800; color:#111827; margin:6px 0;">
            SIH26091 / PS 91: AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs
        </div>
        <div style="color:#047857; font-weight:600; font-size:0.95rem; margin-bottom:8px;">
            "Know your market. Know your money. Make a better business decision."
        </div>
        <div style="color:#4B5563; font-size:0.88rem; line-height:1.5;">
            Most government portals assist entrepreneurs <i>after</i> borrowing (registration, subsidy disbursement). 
            <b>RuralBiz Navigator fills the critical gap BEFORE borrowing:</b> determining whether an enterprise idea is viable in a specific village ecosystem given real catchment demand, competitor density, reducing-balance debt math, and verified scheme eligibility.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 2: Hybrid Architecture Principle
# ==============================================================================
st.subheader("🏗️ Hybrid Architecture Principle")
st.caption("A fundamental architectural boundary: strict separation between conversational explanation and mathematical execution.")

col_arc1, col_arc2, col_arc3 = st.columns(3)

with col_arc1:
    st.markdown(
        """
        <div class="surface-card" style="border-top: 4px solid #10B981; height: 100%;">
            <div style="font-weight:800; color:#065F46; font-size:1.05rem; margin-bottom:8px;">🤖 Natural Language AI Layer</div>
            <div style="color:#374151; font-size:0.86rem; line-height:1.55;">
                • Multilingual user intent parsing (EN, HI, TE, KN)<br/>
                • Natural language advisory explanations<br/>
                • Conversational context injection<br/>
                • Structured output format (ANSWER, WHY, EVIDENCE, FINANCIAL IMPACT, RISK, NEXT STEP)<br/>
                <i style="color:#047857; font-weight:600;">*Zero mathematical formulas executed by LLM.*</i>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_arc2:
    st.markdown(
        """
        <div class="surface-card" style="border-top: 4px solid #3B82F6; height: 100%;">
            <div style="font-weight:800; color:#1E3A8A; font-size:1.05rem; margin-bottom:8px;">⚙️ Deterministic Python Engine</div>
            <div style="color:#374151; font-size:0.86rem; line-height:1.55;">
                • Standard reducing-balance EMI formula<br/>
                • Month-by-month loan amortization schedule<br/>
                • 12-month dynamic P&amp;L and cash flow projection<br/>
                • Break-even point (revenue &amp; volume)<br/>
                • Debt Service Coverage Ratio (DSCR)<br/>
                • Weighted Viability Scoring (0–100)<br/>
                • What-If shock sensitivity simulation
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_arc3:
    st.markdown(
        """
        <div class="surface-card" style="border-top: 4px solid #F59E0B; height: 100%;">
            <div style="font-weight:800; color:#92400E; font-size:1.05rem; margin-bottom:8px;">📂 Verified Data Layer</div>
            <div style="color:#374151; font-size:0.86rem; line-height:1.55;">
                • SQLite relational persistence (<code>app.db</code>)<br/>
                • 10 micro-enterprise benchmark models<br/>
                • 7 representative rural demographic profiles<br/>
                • Hyper-local competitor mapping<br/>
                • Verified Indian Central &amp; State schemes (PMEGP, MUDRA, PMFME, DAY-NRLM, Vishwakarma)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 3: System Workflow Diagram
# ==============================================================================
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

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 4: Privacy, Security & Data Handling
# ==============================================================================
st.subheader("🔒 Privacy, Security & Data Handling")
st.markdown(
    """
    <div class="surface-card">
        <ul style="margin:0; padding-left:1.2rem; color:#374151; font-size:0.88rem; line-height:1.6;">
            <li><b>Zero PII Mandate:</b> User name and household income are entirely optional. No Aadhaar, PAN, or bank credentials are ever requested or stored.</li>
            <li><b>Deterministic Local Processing:</b> All financial computations and score engines execute strictly on the local Python runtime.</li>
            <li><b>No Secret Leakage:</b> API keys are never bundled in frontend assets and are resolved exclusively from server-side environment configurations.</li>
            <li><b>100% Offline Capability:</b> The platform operates reliably in Demo Mode without requiring any active internet connection or third-party cloud API keys.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# SECTION 5: Legal & Institutional Disclaimer
# ==============================================================================
st.subheader("⚖️ Legal & Institutional Disclaimer")
st.warning(
    """
    **Notice to Evaluators and Users:**  
    1. **Informational Decision-Support Only:** RuralBiz Navigator provides financial engineering models and prototype demographic indices. It does not constitute formal legal, investment, or banking advice.
    2. **No Profit or Sanction Guarantee:** The platform does not guarantee enterprise profitability, footfall, subsidy sanction, or loan approval. Final lending decisions rest with authorized financial institutions.
    3. **Synthetic Demographic Baseline:** Village coordinates, competitor ratings, and customer footfall metrics in this prototype are synthetically constructed for evaluation.
    4. **Verified Scheme Guidelines:** Scheme slabs (PMEGP, MUDRA, PMFME, Vishwakarma) reflect official guidelines but are subject to Ministry revisions.
    """
)

render_disclaimer_footer(lang)

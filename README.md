# 🌾 RuralBiz Navigator

> **"Know your market. Know your money. Make a better business decision."**

**Smart India Hackathon 2026 Problem Statement:** **SIH26091 / PS 91**  
**Title:** *AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs*

---

## 🌟 Executive Summary & Core Value Proposition

Most existing government and fintech portals assist entrepreneurs **after** they have decided to borrow—helping with business registration, drafting loan applications, or claiming subsidies.

**RuralBiz Navigator solves the crucial missing link BEFORE borrowing:**
> *"Should I start this specific business HERE, with MY budget, given MY local competition and market demand?"*

It integrates hyper-local demographic catchment analysis (5–10 km radius), deterministic financial debt structuring, reducing-balance EMI calculations, break-even economics, what-if stress testing, rule-based government scheme matching (PMEGP, MUDRA, PMFME, etc.), a multilingual natural language AI advisor, and bank-ready downloadable Detailed Project Reports (DPR).

---

## 🏗️ System Architecture

RuralBiz Navigator strictly enforces a **Hybrid Architecture**:
- **LLM / Generative AI:** Natural language parsing, multilingual interaction (English, Hindi, Telugu, Kannada), evidence summarization, and explainability. **The LLM never computes financial formulas or determines eligibility.**
- **Deterministic Python Engines:** Exact mathematical reducing-balance EMI calculations, debt service coverage ratios (DSCR), break-even volumes, 12-month dynamic cash flow projections, weighted viability scoring (0–100), and verified government scheme rule routing.
- **Data Layer:** SQLite relational database (`database/app.db`) populated with verified benchmark unit economics, rural demographic indices, competitor profiles, and official scheme criteria.

```
                            User Interface (Streamlit)
                                        |
              +-------------------------+-------------------------+
              |                                                   |
              v                                                   v
       AI Advisory Assistant                               Assessment Engine
     (Multilingual: EN, HI, TE, KN)                               |
              |                                                   v
       AI Provider Router                                  Hyper-Local Engine
 (Groq -> Gemini -> OpenAI -> Local Demo Mock)                    |
              |                                                   v
              +-------------------------+                     Data Layer
                                        |             (Localities, Competitors, Benchmarks)
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
```

---

## ✨ Key Features

1. **Hyper-Local Catchment & GIS (5–10 km Radius):**
   - Interactive Folium Leaflet map with CartoDB Positron vector tiles showing User Site, APMC Mandi/Market, Banks, and Competitor locations.
   - Distinct 5 km inner circle (daily footfall zone) and 10 km outer circle (weekly haat / wholesale catchment).
   - Seamless offline fallback to a synthetic Plotly scatter map if external tile services are unreachable.
2. **Deterministic Viability Scoring (0–100):**
   - Weighted model: Market Demand (25%), Competition (15%), Accessibility (10%), Financial Fit (20%), Growth Potential (15%), Risk Resilience (15%).
   - Tiered Classification: Strong Opportunity (80–100), Promising (65–79), Needs Caution (50–64), High Risk (0–49).
3. **Evidence-Grounded Recommendation (GO / MODIFY / AVOID):**
   - **GO:** Viability $\ge 75$, DSCR $\ge 1.20$, Positive Net Cash Flow.
   - **MODIFY:** Viability $55–74$ or capital restructuring needed.
   - **AVOID:** Viability $< 55$, negative operating cash flow, or critical default risk (DSCR $< 1.0$).
   - Grounded in local demographics and benchmark economics with a deterministic 4-quadrant SWOT matrix.
4. **Institutional Financial Calculator & Debt Structuring:**
   - Reducing-balance monthly EMI calculation:
     $$EMI = P \times \frac{r(1+r)^n}{(1+r)^n - 1}$$
   - Month-by-month principal and interest amortization table with configurable grace/moratorium buffer.
   - 12-Month dynamic P&L and cash flow statement incorporating rural seasonal ramp-up.
   - Monthly Break-Even Revenue ($BEP = \frac{\text{Fixed Costs} + EMI}{1 - \text{Variable Cost Ratio}}$) and Margin of Safety.
   - Debt Service Coverage Ratio (DSCR = Operating Profit / Monthly EMI).
5. **What-If Scenario Stress Simulator:**
   - Interactive sliders for sales volume ($-50\%$ to $+50\%$), selling prices, raw material inflation, fixed cost spikes, and interest rates.
   - Side-by-side Base Case vs Stress Case comparison with deterministic survival classification: `SURVIVES WITH BUFFER`, `VULNERABLE - DEBT STRESS`, or `FAILS / INSOLVENT`.
6. **Government Scheme Navigator:**
   - Verified rule-based matching against Central/State programmes: PMEGP, PM MUDRA (Shishu, Kishore, Tarun), PMFME, Stand-Up India, DAY-NRLM, and PM Vishwakarma.
   - Outputs status: `MATCHED`, `POSSIBLE`, `NOT MATCHED`, or `VERIFICATION REQUIRED`.
   - Displays exact subsidy rates (e.g. 25%–35% under PMEGP), collateral-free cover (CGTMSE / CGFMU), checklist, and official portal links.
7. **Business Alternatives Recommender:**
   - Automatically computes and ranks all 10 micro-enterprise sectors for the user's specific locality and budget.
   - One-click adoption button to instantly re-analyze any alternative.
8. **Multilingual AI Advisor:**
   - Full dictionary i18n support in English, Hindi (हिंदी), Telugu (తెలుగు), and Kannada (ಕನ್ನಡ).
   - Structured responses: `ANSWER`, `WHY`, `EVIDENCE`, `FINANCIAL IMPACT`, `RISK`, `NEXT STEP`.
   - Multi-provider architecture with automatic offline Demo Mode fallback if no API keys are configured.
9. **Instant Bankable DPR Report (ReportLab PDF):**
   - 20-section institutional project report ready for submission to District Task Force Committees and commercial banks.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-org/RuralBiz_Navigator.git
cd RuralBiz_Navigator

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration (Optional)
The application works **100% out of the box in Offline Demo Mode** without any API keys.  
If you wish to enable cloud LLM providers, copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your optional keys:
```env
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
DEFAULT_AI_PROVIDER=auto
```

### 4. Running the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ⚡ Demo & Judging Walkthrough

For Smart India Hackathon evaluation, the sidebar contains **One-Click Pre-configured Demo Scenarios**:

1. **Scenario 1: Strong Opportunity (GO)**
   - **Entrepreneur:** Food Processing Unit in Demo Village A (Agri Hub).
   - **Capital:** ₹3,00,000 available, ₹2,15,000 setup outlay.
   - **Outcome:** Viability Score **82/100**, DSCR **1.62**, Decision: **GO**. Eligible for PMEGP (25% rural subsidy).
2. **Scenario 2: Borderline Opportunity (MODIFY)**
   - **Entrepreneur:** Tailoring & Boutique in Coastal Demo Village B.
   - **Capital:** ₹30,000 available, ₹93,000 project outlay.
   - **Outcome:** Viability Score **67/100**, Decision: **MODIFY**. Tight equity buffer; recommended to apply for PM Vishwakarma / MUDRA Kishore.
3. **Scenario 3: Saturated Market (AVOID / High Risk)**
   - **Entrepreneur:** Retail Kirana in Peri-Urban Demo Village D.
   - **Capital:** ₹25,000 available against ₹1,90,000 project outlay with 3 established competitors.
   - **Outcome:** Viability Score **44/100**, DSCR **0.78**, Decision: **AVOID**. High debt burden and negative cash flow margin.

---

## 🧪 Testing

Execute the automated test suite with pytest:
```bash
pytest -v
```
All 20 unit tests validate:
- Reducing-balance EMI against standard bank tables.
- Zero-interest and zero-principal edge cases.
- Amortization schedule closure and moratorium interest service.
- Break-even revenue and margin of safety calculations.
- DSCR status classification thresholds.
- Viability weight sum invariance ($1.0$).
- GO / MODIFY / AVOID decision logic.
- Government scheme cost boundaries and demographic rules.
- What-If scenario stress sensitivity and survival verdicts.

---

## 🗄️ Database Architecture

The application automatically provisions an SQLite database (`database/app.db`) on startup:
- `localities`: Village demographics, population, road accessibility, purchasing power index.
- `businesses`: Micro-enterprise benchmark economics (CapEx, OpEx, variable margins, break-even months).
- `competitors`: Mapped competitor entities with coordinates, ratings, and estimated sales.
- `schemes`: Central and state credit schemes with verified subsidy slabs and ceilings.
- `assessments`: User assessments and evaluation history.
- `financial_scenarios`: Stored base and stress financial runs.

---

## ⚖️ Legal & Institutional Disclaimer

RuralBiz Navigator provides informational and decision-support estimates based on standard financial engineering formulas and prototype demographic models. It does not constitute formal financial, legal, investment, or commercial lending advice. It does not guarantee business profitability, customer footfall, scheme eligibility, or loan approval.

*Locality demographic indices, customer catchment estimates, and competitor listings in this prototype are synthetically generated for demonstration purposes.*

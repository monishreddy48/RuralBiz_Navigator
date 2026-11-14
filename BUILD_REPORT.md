# 🌾 RuralBiz Navigator — Prototype Build Report
**Smart India Hackathon 2026 (SIH26091 / PS 91)**  
*AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs*

---

## 1. Executive Summary

RuralBiz Navigator was built from the ground up as a complete working prototype solving SIH Problem Statement 91.

### Core Value Proposition
While existing systems assist entrepreneurs with registration or subsidy applications *after* borrowing, **RuralBiz Navigator answers the critical decision BEFORE borrowing:**
> *"Should I start this business HERE, with MY budget, given MY local market and competition?"*

The system combines:
1. **Hyper-Local Catchment & GIS (5–10 km radius)** with competitor mapping and demand gap estimation.
2. **Deterministic Viability Scoring (0–100)** with weighted factors (Demand, Competition, Access, Finance, Growth, Risk).
3. **Evidence-Grounded Recommendation (GO / MODIFY / AVOID)** with 3–5 grounded reasons, evidence summary, and SWOT matrix.
4. **Institutional Financial Debt Structuring** implementing reducing-balance EMI, 12-month dynamic P&L cash flow, Break-Even analysis, and Debt Service Coverage Ratio (DSCR).
5. **Interactive What-If Stress Testing** evaluating business survival under adverse volume drops, price wars, cost inflation, and interest rate hikes.
6. **Rule-Based Government Scheme Routing** matching verified Central and State programs (PMEGP, MUDRA Shishu/Kishore/Tarun, PMFME, Stand-Up India, DAY-NRLM, PM Vishwakarma).
7. **Business Alternatives Recommender** ranking all 10 micro-enterprise sectors for the entrepreneur's budget and location.
8. **Multilingual Advisory AI Assistant** supporting English, Hindi (हिंदी), Telugu (తెలుగు), and Kannada (ಕನ್ನಡ) with structured output format (`ANSWER`, `WHY`, `EVIDENCE`, `FINANCIAL IMPACT`, `RISK`, `NEXT STEP`).
9. **Instant Bankable DPR Generation (ReportLab PDF)** compiling a 20-section institutional project report ready for bank credit appraisal.
10. **Pre-configured Demo Scenarios** for immediate SIH judging demonstrations:
    - **Scenario 1 (GO):** Food Processing in Demo Village A (Viability: 82/100, DSCR: 1.62).
    - **Scenario 2 (MODIFY):** Tailoring Unit in Coastal Demo Village B (Viability: 67/100).
    - **Scenario 3 (AVOID):** Retail Store in Saturated Peri-Urban Demo Village D (Viability: 44/100, DSCR: 0.78).

---

## 2. Hybrid Architecture Implementation

A strict architectural separation is maintained between conversational AI and mathematical computation:
- **LLM / Generative Layer:** Summarization, explanation of calculations, multilingual interaction. *Zero formulas are evaluated by the LLM.*
- **Deterministic Python Engines:** Exact financial math, reducing-balance amortizations, break-even thresholds, DSCR, viability weights, and scheme eligibility rules.
- **Data Layer:** SQLite relational database (`database/app.db`) initialized from curated benchmarks, rural demographics, competitor mappings, and verified scheme guidelines.
- **Provider Abstraction:** Dynamic router prioritizing configured providers (`Groq`, `Gemini`, `OpenAI`) with an automatic offline fallback to `MockProvider` ("AI Assistant: Demo Mode").

---

## 3. Directory & File Inventory

```
RuralBiz_Navigator/
├── app.py                         # Application controller & entrypoint
├── config.py                      # Configurable weights, thresholds, financing defaults
├── requirements.txt               # Pinned dependencies
├── README.md                      # Comprehensive user & developer guide
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules
│
├── core/                          # Deterministic Computational Engines
│   ├── __init__.py
│   ├── hyperlocal_engine.py       # Demographic & competition density scoring
│   ├── financial_engine.py        # Reducing-balance EMI, cash flows, BEP, DSCR
│   ├── viability_engine.py        # Weighted 0-100 viability scoring & classification
│   ├── recommendation_engine.py   # GO/MODIFY/AVOID logic, grounded evidence & SWOT
│   ├── scenario_engine.py         # What-If sensitivity shocks & survival engine
│   ├── scheme_engine.py           # Rule-based government scheme matching
│   └── alternative_engine.py      # Category evaluation & ranking engine
│
├── ai/                            # AI Provider Layer
│   ├── __init__.py
│   ├── base_provider.py           # Abstract provider interface
│   ├── groq_provider.py           # Groq API provider (Llama 3.3)
│   ├── openai_provider.py         # OpenAI provider (GPT-4o-mini)
│   ├── gemini_provider.py         # Google Gemini provider (Gemini 1.5 Flash)
│   ├── mock_provider.py           # Offline deterministic advisory engine (Demo Mode)
│   └── router.py                  # Automatic provider detection & fallback router
│
├── database/                      # Relational Persistence
│   ├── __init__.py
│   ├── schema.sql                 # SQLite relational schema
│   ├── db.py                      # Database manager & seed data loader
│   └── app.db                     # Auto-created SQLite database
│
├── data/                          # Seed Benchmark & Demographic Data
│   ├── localities.csv             # 7 rural demo localities across Indian states
│   ├── businesses.csv             # 10 core rural micro-business profiles
│   ├── business_benchmarks.csv    # Benchmark CapEx, OpEx, margins, and break-even
│   ├── competitors.csv            # 21 synthetic competitor profiles with ratings
│   └── schemes.json               # 8 verified government schemes with official guidelines
│
├── i18n/                          # Multilingual Localization
│   ├── __init__.py
│   └── translations.py            # Dictionary i18n for English, Hindi, Telugu, Kannada
│
├── reports/                       # ReportLab PDF Generator
│   ├── __init__.py
│   └── pdf_generator.py           # 20-section institutional DPR compiler
│
├── utils/                         # Helper Utilities
│   ├── __init__.py
│   ├── formatting.py              # Indian numbering (₹2,50,000) & percentages
│   ├── validation.py              # Input validation constraints
│   ├── map_utils.py               # Folium GIS & Plotly offline synthetic map fallback
│   ├── demo_scenarios.py          # 3 pre-built SIH judging scenarios
│   └── ui_components.py           # Shared sidebar, banners, and disclaimer cards
│
├── assets/
│   └── style.css                  # Custom styling, badges, and responsive typography
│
├── pages/                         # Streamlit Multipage Views
│   ├── 01_Home.py                 # Home dashboard & workflow banner
│   ├── 02_Business_Feasibility.py # Assessment form, viability score & SWOT
│   ├── 03_Hyper_Local_Market.py   # 5-10 km radius GIS map & competitor table
│   ├── 04_Financial_Calculator.py # EMI calculator, cash flow charts & amortization
│   ├── 05_What_If_Simulator.py    # Stress test sliders & survival verdict
│   ├── 06_Scheme_Navigator.py     # Government scheme matching & checklist
│   ├── 07_Business_Alternatives.py# Ranked opportunities & one-click adoption
│   ├── 08_AI_Assistant.py         # Multilingual advisory chat interface
│   ├── 09_DPR_Report.py           # 20-section DPR overview & instant PDF download
│   └── 10_About.py                # PS 91, architecture diagram & disclaimers
│
└── tests/                         # Automated Pytest Suite
    ├── __init__.py
    ├── test_financial.py          # EMI, amortization, BEP, DSCR, cash flows
    ├── test_viability.py          # Viability weights, GO/MODIFY/AVOID, SWOT
    ├── test_schemes.py            # Scheme boundary conditions & category matching
    └── test_scenarios.py          # What-If shock calculations & survival checks
```

---

## 4. Test Suite Execution & Verification

Automated testing was conducted using `pytest -v`:

```
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\cmoni\Desktop\RuralBiz_Navigator
plugins: anyio-4.9.0
collected 20 items

tests/test_financial.py::test_reducing_balance_emi_standard PASSED       [  5%]
tests/test_financial.py::test_reducing_balance_emi_zero_interest PASSED  [ 10%]
tests/test_financial.py::test_reducing_balance_emi_zero_loan PASSED      [ 15%]
tests/test_financial.py::test_amortization_schedule_closing_balance PASSED [ 20%]
tests/test_financial.py::test_moratorium_handling PASSED                 [ 25%]
tests/test_financial.py::test_break_even_point_calculation PASSED        [ 30%]
tests/test_financial.py::test_dscr_classification PASSED                 [ 35%]
tests/test_financial.py::test_cash_flow_continuity PASSED                [ 40%]
tests/test_financial.py::test_financial_edge_cases PASSED                [ 45%]
tests/test_scenarios.py::test_mild_stress_survival PASSED                [ 50%]
tests/test_scenarios.py::test_catastrophic_stress_failure PASSED         [ 55%]
tests/test_schemes.py::test_scheme_mudra_shishu_boundary PASSED          [ 60%]
tests/test_schemes.py::test_scheme_pmegp_eligibility PASSED              [ 65%]
tests/test_schemes.py::test_scheme_standup_india_constraints PASSED      [ 70%]
tests/test_schemes.py::test_scheme_status_sorting PASSED                 [ 75%]
tests/test_viability.py::test_viability_weights_sum_to_one PASSED        [ 80%]
tests/test_viability.py::test_viability_score_bounds PASSED              [ 85%]
tests/test_viability.py::test_recommendation_go_decision PASSED          [ 90%]
tests/test_viability.py::test_recommendation_avoid_decision PASSED       [ 95%]
tests/test_viability.py::test_swot_generation PASSED                     [100%]

============================= 20 passed in 0.99s ==============================
```

### Server & Report Verification
- **Streamlit Server:** Active on `http://localhost:8501`, verified with HTTP 200 responses.
- **ReportLab PDF Generation:** Verified programmatic compilation of `RuralBiz_Navigator_Business_Report.pdf` (9,551 bytes) containing all 20 sections, custom styling, tables, and disclaimer footers.

---

## 5. How to Run the Application

```bash
# 1. Activate environment
.venv\Scripts\activate   # On Windows
source .venv/bin/activate # On Linux/macOS

# 2. Run Streamlit application
streamlit run app.py
```
Access the application in your browser at `http://localhost:8501`.

---

## 6. Known Limitations & Prototype Boundaries

1. **Synthetic Data Disclosure:** Village coordinates, competitor ratings, and local customer numbers are simulated prototype data. They demonstrate the analytical capabilities of the platform without representing official Census or APMC mandi registries.
2. **Offline-First Map Fallback:** In environments where external tile servers (CartoDB/OSM) are blocked by firewall or network restrictions, the application automatically displays an offline synthetic scatter map with exact 5 km and 10 km concentric radius rings.
3. **No Direct Banking API Integration:** The prototype does not execute real bank loan sanctions or CIBIL credit score inquiries. It provides pre-loan decision support.

---

## 7. Future Roadmap & Production Scope

- **Integration with Jan Samarth & Udyam Portals:** Direct Single-Sign-On (SSO) with API submission of the generated DPR into Udyam Registration and Jan Samarth credit portals.
- **Live Mandi Price Ingestion (e-NAM):** Real-time integration with agricultural mandi prices for dynamic variable cost calculations.
- **Voice-First Audio Interface:** Audio input and Text-to-Speech (TTS) integration in regional dialects for semi-literate rural entrepreneurs.
- **Satellite & Road Catchment Analysis:** Geospatial integration with PMGSY (Pradhan Mantri Gram Sadak Yojana) paved road networks for automated logistics routing.

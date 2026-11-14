# 🌾 RuralBiz Navigator

> **"Know your market. Know your money. Make a better business decision."**

**Smart India Hackathon 2026 Problem Statement:** **SIH26091 / PS 91**  
**Title:** *AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs*  
**Repository:** [https://github.com/monishreddy48/RuralBiz_Navigator](https://github.com/monishreddy48/RuralBiz_Navigator)

---

## 🌟 Executive Summary & Core Value Proposition

Most existing government and fintech portals assist entrepreneurs **after** they have decided to borrow—helping with business registration, drafting loan applications, or claiming subsidies.

**RuralBiz Navigator solves the crucial missing link BEFORE borrowing:**
> *"Should I start this specific business HERE, with MY budget, given MY local competition and market demand?"*

It integrates hyper-local demographic catchment analysis (5–10 km radius), deterministic financial debt structuring, reducing-balance EMI calculations, break-even economics, what-if stress testing, rule-based government scheme matching (PMEGP 35% subsidy, MUDRA, PMFME), a conversational **Gemini Live AI Voice Business Advisor** in **Kannada, Telugu, Hindi, and English**, and bank-ready institutional Detailed Project Reports (DPR).

---

## 🏗️ Modern Full-Stack System Architecture

RuralBiz Navigator is built on a high-performance decoupled architecture designed for scale and enterprise reliability:

```
                            [ Web Browser / Mobile ]
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
         [ Next.js 14 Frontend ]                 [ Firebase Authentication ]
    (TypeScript + Tailwind CSS + Lucide)        (Email/Password, Google OAuth,
    Port 3000 | Responsive UI & Audio Waveform        Role & Profile Store)
                   |                                       |
                   | REST API & Live WebSockets            | JWT Verification
                   v                                       v
    +-------------------------------------------------------------+
    |                    FastAPI Backend Engine                   |
    |                         (Port 8000)                         |
    +-------------------------------------------------------------+
         |                     |                      |
         v                     v                      v
  [ AI Voice Relay ]   [ Deterministic Math ]   [ Data Layer ]
  Gemini 3.8 Live API  Reducing-Balance EMI     SQLite (app.db) /
  WebSockets (/live)   DSCR, Cash Flow, BEP     PostgreSQL (Production)
  PCM Audio 16kHz      Govt Scheme Rules        Localities, Benchmarks,
  kn-IN, te-IN, hi, en 20-Section PDF DPR       Competitors & Schemes
```

---

## ✨ Key Capabilities & Modules

1. **Public SaaS Landing Page (`/`)**:
   - Deep forest green and warm ivory editorial visual identity.
   - Diverse rural micro-entrepreneur representation across trades (retail, food processing, textiles, agro, fabrication, services).
   - Responsive design with zero generic placeholders.

2. **Firebase Authentication & Onboarding (`/login`, `/register`, `/complete-profile`)**:
   - Live Email/Password & Google Sign-In.
   - Multi-step entrepreneur onboarding (State, District, Village, Business Category, Existing vs New Plan).
   - Route-level security protecting all dashboard sub-modules.

3. **Entrepreneur Cockpit & SIH Judging Presets (`/dashboard`)**:
   - Real-time KPI summaries, profile completeness, and quick assessment launcher.
   - **1-Click Pre-configured SIH Demo Cases**:
     - **Case 1: GO** — Agro-Processing Unit in Tumakuru (Score: 82/100, Safe DSCR 1.65x, 35% PMEGP subsidy).
     - **Case 2: MODIFY** — Small Manufacturing Unit (Score: 58/100, requires equity buffer injection).
     - **Case 3: AVOID** — Saturated Village Kirana (Score: 44/100, 8 competitors in 1 km, DSCR < 1.0).

4. **8 Dedicated Business Intelligence Engines**:
   - **Business Feasibility (`/dashboard/feasibility`)**: 6-factor radar model (Demand, Saturation, Access, Fit, Growth, Resilience) and 4-quadrant SWOT matrix.
   - **Hyperlocal Market Intelligence (`/dashboard/market`)**: Interactive SVG Catchment Radar mapping 5 km walk-in footfall vs 10 km weekly mandi wholesale radius.
   - **Financial Calculator & Debt Structuring (`/dashboard/financial`)**: Reducing-balance monthly EMI, 60-month amortization, dynamic cash flow, and DSCR.
   - **What-If Scenario Simulator (`/dashboard/simulator`)**: Adverse demand drops (-20%), deflation, inflation, and interest rate spikes with survival classifications (`SURVIVES`, `VULNERABLE`, `INSOLVENT`).
   - **Government Scheme Navigator (`/dashboard/schemes`)**: Rule-based matching against PMEGP, MUDRA Shishu/Kishore/Tarun, PMFME, and Stand-Up India.
   - **Business Alternatives (`/dashboard/alternatives`)**: Comparing and ranking all 10 rural trades matched to your savings.
   - **AI Voice Business Advisor (`/dashboard/assistant`)**: Live microphone conversational AI powered by **Gemini Live API** with canvas audio waveforms in **Kannada, Telugu, Hindi, and English**.
   - **Institutional DPR Generator (`/dashboard/dpr`)**: 1-click generation of the bank-ready 20-section Detailed Project Report PDF powered by ReportLab.

---

## 🚀 Quick Start Guide

### Option A: 1-Click Launch (Recommended for Windows)

Double-click **`start_all.bat`** (or run `start_all.ps1` in PowerShell) in the root directory.  
This automatically boots both servers and opens your browser:
- **Next.js Web Portal:** [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend & Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option B: Manual Command Line Startup

#### 1. Start the Python FastAPI Backend (Terminal 1)
```powershell
# From project root
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Start the Next.js Frontend (Terminal 2)
```powershell
cd frontend
npm run dev
# OR for optimized production build:
# npm run build
# npm start
```
Then visit **[http://localhost:3000](http://localhost:3000)**.

---

### Option C: Docker Containerization (Production)
```bash
docker-compose up --build
```
Orchestrates both frontend (port 3000) and backend (port 8000) inside isolated production containers.

---

## 🧪 Automated Testing Suite (100% Passing)

Run the full pytest suite across computational engines and voice APIs:
```bash
python -m pytest tests/ -v
```
**25 / 25 automated tests pass in ~1.8 seconds**, covering:
- Reducing-balance EMI math and amortization balance closure.
- DSCR threshold classifications and break-even bounds.
- 5 km catchment demand multipliers.
- PMEGP 35% subsidy eligibility and MUDRA ceilings.
- What-If stress test survival boundaries.
- Multilingual voice grounding across Kannada, Telugu, Hindi, and English.

---

## 🗄️ Database & Multi-User Roadmap

- **Prototype & Local Evaluation**: SQLite 3 (`database/app.db`) with pre-seeded datasets (`data/localities.csv`, `data/businesses.csv`, `data/competitors.csv`, `data/schemes.json`).
- **State-Wide Production Migration**: Detailed in [database/DATABASE_MIGRATION.md](database/DATABASE_MIGRATION.md) for deploying to managed **PostgreSQL (Google Cloud SQL / Supabase)** with Row-Level Security (RLS) and connection pooling.

---

## ⚖️ Legal & Institutional Disclaimer

RuralBiz Navigator provides informational and decision-support guidance based on standard financial engineering formulas and verified rural economic models. It does not constitute formal commercial lending approval or legal advice. Final credit sanction is governed by lending institutions under RBI guidelines.

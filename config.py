"""
RuralBiz Navigator - Configuration
SIH 2026 Problem Statement SIH26091 / PS 91
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "app.db"
REPORTS_DIR = BASE_DIR / "reports"

# Application Metadata
APP_NAME = "RuralBiz Navigator"
TAGLINE = "Know your market. Know your money. Make a better business decision."
PROBLEM_STATEMENT = "SIH26091 / PS 91: AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs"
VERSION = "1.0.0-prototype"

# Viability Scoring Weights (Configurable, must sum to 1.0)
VIABILITY_WEIGHTS = {
    "market_demand": 0.25,
    "competition": 0.15,
    "accessibility": 0.10,
    "financial_fit": 0.20,
    "growth_potential": 0.15,
    "risk": 0.15
}

# Viability Classification Thresholds
VIABILITY_THRESHOLDS = {
    "strong": 80,       # 80-100: Strong Opportunity
    "promising": 65,    # 65-79: Promising
    "caution": 50,      # 50-64: Needs Caution
    "high_risk": 0      # 0-49: High Risk
}

# DSCR (Debt Service Coverage Ratio) Thresholds
DSCR_THRESHOLDS = {
    "strong": 1.5,
    "acceptable": 1.2,
    "caution": 1.0
}

# Recommendation Decision Rules
DECISION_THRESHOLDS = {
    "go_viability": 75,
    "modify_viability": 55
}

# Financing Defaults (Prototype assumptions when no scheme overrides)
DEFAULT_FINANCING = {
    "default_margin_percent": 15.0,     # Own contribution %
    "default_interest_rate": 9.5,       # Annual interest rate %
    "default_tenure_months": 60,        # 5 years
    "default_moratorium_months": 3,     # 3 months grace
    "max_loan_percent": 85.0
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "te": "తెలుగు (Telugu)",
    "kn": "ಕನ್ನಡ (Kannada)"
}

# AI Provider API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "auto")

# Map Configuration
MAP_DEFAULT_ZOOM = 13
MAP_RADIUS_INNER_KM = 5
MAP_RADIUS_OUTER_KM = 10
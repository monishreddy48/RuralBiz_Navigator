"""
RuralBiz Navigator - Backend Configuration & Settings
FastAPI Backend settings, paths, and financial engineering thresholds.
"""
import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load root .env if present
load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BACKEND_DIR.parent
DATA_DIR = ROOT_DIR / "data"
DATABASE_DIR = ROOT_DIR / "database"
DB_PATH = DATABASE_DIR / "app.db"
REPORTS_DIR = ROOT_DIR / "reports"

# API Settings
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "RuralBiz Navigator API"
VERSION = "1.0.0"

# CORS Allowed Origins
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8501", # Allow Streamlit fallback
]

# Viability Scoring Weights (Configurable, must sum to 1.0)
VIABILITY_WEIGHTS: Dict[str, float] = {
    "market_demand": 0.25,
    "competition": 0.15,
    "accessibility": 0.10,
    "financial_fit": 0.20,
    "growth_potential": 0.15,
    "risk": 0.15
}

# Viability Classification Thresholds
VIABILITY_THRESHOLDS: Dict[str, float] = {
    "strong": 80.0,       # 80-100: Strong Opportunity
    "promising": 65.0,    # 65-79: Promising
    "caution": 50.0,      # 50-64: Needs Caution
    "high_risk": 0.0      # 0-49: High Risk
}

# DSCR Thresholds
DSCR_THRESHOLDS: Dict[str, float] = {
    "strong": 1.5,
    "acceptable": 1.2,
    "caution": 1.0
}

# Recommendation Decision Rules
DECISION_THRESHOLDS: Dict[str, float] = {
    "go_viability": 75.0,
    "modify_viability": 55.0
}

# Financing Defaults
DEFAULT_FINANCING = {
    "default_margin_percent": 15.0,
    "default_interest_rate": 9.5,
    "default_tenure_months": 60,
    "default_moratorium_months": 3,
    "max_loan_percent": 85.0
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada"
}

# AI & Cloud Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "auto")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")


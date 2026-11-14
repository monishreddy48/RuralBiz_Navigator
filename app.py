"""
RuralBiz Navigator - Main Application Entry Point
Smart India Hackathon 2026 Problem Statement SIH26091 / PS 91
"""
import streamlit as st
from database.db import init_db
from utils.demo_scenarios import load_scenario
from utils.ui_components import _apply_scenario_to_state, load_custom_css

# Page configuration
st.set_page_config(
    page_title="RuralBiz Navigator",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize SQLite database & styles
init_db()
load_custom_css()

# Initialize session state with Scenario 1 (Food Processing in Agri Hub)
if "assessment_data" not in st.session_state:
    _apply_scenario_to_state(load_scenario("demo_1"))

if "language" not in st.session_state:
    st.session_state["language"] = "en"

# Seamlessly switch to Home Dashboard
try:
    st.switch_page("pages/01_Home.py")
except Exception:
    import runpy
    runpy.run_path("pages/01_Home.py")

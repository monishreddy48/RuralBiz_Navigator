"""
Unit Tests for RuralBiz Navigator - Viability & Recommendation Engine
Tests factor weights, boundary limits, classification, GO/MODIFY/AVOID rules, and SWOT.
"""
import pytest
import math
from config import VIABILITY_WEIGHTS, VIABILITY_THRESHOLDS, DECISION_THRESHOLDS
from core.viability_engine import calculate_viability_score
from core.recommendation_engine import generate_business_recommendation, generate_swot_analysis

def test_viability_weights_sum_to_one():
    """Configured viability weights must sum precisely to 1.0 (100%)."""
    total_weight = sum(VIABILITY_WEIGHTS.values())
    assert math.isclose(total_weight, 1.0, rel_tol=1e-5)

def test_viability_score_bounds():
    """Score must strictly reside within [0, 100]."""
    mock_hl = {"market_demand_score": 85.0, "competition_score": 75.0, "accessibility_score": 80.0}
    mock_fin = {"financial_fit_score": 80.0, "dscr": 1.6}
    mock_biz = {"growth_potential": "High", "risk_level": "Low"}
    mock_loc = {"purchasing_power_index": 80.0}

    result = calculate_viability_score(mock_hl, mock_fin, mock_biz, mock_loc)
    score = result["viability_score"]
    
    assert 0.0 <= score <= 100.0
    assert result["classification"] in ["Strong Opportunity", "Promising", "Needs Caution", "High Risk"]

def test_recommendation_go_decision():
    """High viability + DSCR >= 1.2 + positive profit must trigger GO."""
    viab = {"viability_score": 82.0}
    fin = {
        "dscr": 1.55,
        "monthly_net_profit": 18000.0,
        "margin_of_safety_pct": 28.0,
        "own_pct": 35.0,
        "loan_amount": 50000.0
    }
    hl = {"num_competitors": 1, "customer_pool": 450, "estimated_unmet_demand_rupees": 25000}
    biz = {"typical_capex": 180000, "typical_margin": 0.28, "growth_potential": "High"}
    loc = {"village_name": "Demo Village A", "population": 4200, "purchasing_power_index": 80}

    rec = generate_business_recommendation(viab, fin, hl, biz, loc)
    assert rec["decision"] == "GO"
    assert len(rec["reasons"]) >= 3
    assert rec["confidence"] == "High"

def test_recommendation_avoid_decision():
    """Low viability or negative profit must trigger AVOID."""
    viab = {"viability_score": 42.0}
    fin = {
        "dscr": 0.65,
        "monthly_net_profit": -4500.0,
        "margin_of_safety_pct": -20.0,
        "own_pct": 10.0,
        "loan_amount": 150000.0
    }
    hl = {"num_competitors": 4, "customer_pool": 200, "estimated_unmet_demand_rupees": 0}
    biz = {"typical_capex": 200000, "typical_margin": 0.12}
    loc = {"village_name": "Demo Village D", "population": 3000}

    rec = generate_business_recommendation(viab, fin, hl, biz, loc)
    assert rec["decision"] == "AVOID"
    assert any("negative" in r.lower() or "default" in r.lower() or "viability" in r.lower() for r in rec["reasons"])

def test_swot_generation():
    """SWOT framework must produce all four quadrants."""
    hl = {"market_demand_score": 75, "num_competitors": 2, "estimated_unmet_demand_rupees": 30000}
    fin = {"own_pct": 30.0, "loan_pct": 70.0, "dscr": 1.4, "margin_of_safety_pct": 22.0}
    biz = {"skill_requirement": "Moderate"}
    loc = {"road_access_score": 80, "bank_access_score": 70}

    swot = generate_swot_analysis(hl, fin, biz, loc)
    assert "strengths" in swot and len(swot["strengths"]) > 0
    assert "weaknesses" in swot and len(swot["weaknesses"]) > 0
    assert "opportunities" in swot and len(swot["opportunities"]) > 0
    assert "threats" in swot and len(swot["threats"]) > 0

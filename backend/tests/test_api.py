"""
Comprehensive API Tests for RuralBiz Navigator FastAPI Backend
Validates all endpoints, request validation, and deterministic math integrity.
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["api_v1"] == "/api/v1"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

def test_financial_calculate_api():
    payload = {
        "project_cost": 215000.0,
        "own_contribution": 53750.0, # 25%
        "annual_interest_rate": 9.5,
        "tenure_months": 60,
        "moratorium_months": 3,
        "monthly_sales": 65000.0,
        "variable_cost_ratio": 0.48,
        "monthly_fixed_cost": 7500.0,
        "unit_price": 80.0
    }
    res = client.post("/api/v1/financial/calculate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["loan_amount"] == 161250.0
    assert data["monthly_emi"] > 0
    assert data["break_even_revenue"] > 0
    assert data["dscr"] > 1.2
    assert len(data["amortization_schedule"]) > 0
    assert len(data["cash_flow_12"]) == 12

def test_feasibility_evaluate_api():
    payload = {
        "village_id": "VIL_001",
        "category": "Food Processing",
        "expected_investment": 215000.0,
        "own_capital": 300000.0,
        "experience_level": "Intermediate",
        "is_existing": False,
        "monthly_income": 30000.0,
        "risk_tolerance": "Moderate"
    }
    res = client.post("/api/v1/feasibility/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["viability_score"] >= 75.0
    assert data["recommendation"]["decision"] in ["GO", "MODIFY", "AVOID"]
    assert len(data["recommendation"]["reasons"]) > 0
    assert "swot" in data["recommendation"]
    assert data["assessment_id"] is not None

def test_market_catchment_api():
    res = client.get("/api/v1/market/catchment/VIL_001?category=Food%20Processing")
    assert res.status_code == 200
    data = res.json()
    assert data["locality"]["village_id"] == "VIL_001"
    assert data["customer_pool"] > 0
    assert data["market_demand_score"] > 0
    assert isinstance(data["competitors"], list)

def test_schemes_match_api():
    payload = {
        "project_cost": 215000.0,
        "business_category": "Food Processing",
        "target_group_tags": ["General", "Rural"],
        "is_existing": False
    }
    res = client.post("/api/v1/schemes/match", json=payload)
    assert res.status_code == 200
    schemes = res.json()
    assert len(schemes) > 0
    statuses = [s["match_status"] for s in schemes]
    assert "MATCHED" in statuses

def test_alternatives_rank_api():
    res = client.get("/api/v1/alternatives/rank?village_id=VIL_001&available_capital=200000")
    assert res.status_code == 200
    alts = res.json()
    assert len(alts) == 10
    # Must be sorted descending by viability score
    scores = [a["viability_score"] for a in alts]
    assert scores == sorted(scores, reverse=True)

def test_simulator_stress_api():
    payload = {
        "village_id": "VIL_001",
        "category": "Food Processing",
        "project_cost": 215000.0,
        "own_capital": 300000.0,
        "sales_vol_delta_pct": -20.0,
        "price_delta_pct": -5.0,
        "var_cost_delta_pct": 15.0,
        "fixed_cost_delta_pct": 10.0,
        "interest_rate_delta": 1.5,
        "loan_amount_delta_pct": 0.0
    }
    res = client.post("/api/v1/simulator/stress", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "survival_status" in data
    assert "base_case" in data
    assert "stress_case" in data

def test_ai_chat_api():
    payload = {
        "question": "Why is this business recommended?",
        "language": "en",
        "context": {
            "locality_name": "Demo Village A",
            "business_name": "Food Processing",
            "viability_score": 82,
            "recommendation": "GO",
            "monthly_profit": 18500,
            "monthly_emi": 3200,
            "dscr": 1.62
        }
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "ANSWER" in data["answer"]
    assert data["provider"] is not None

def test_reports_dpr_download_api():
    payload = {
        "user_name": "Ramesh Patel",
        "village_id": "VIL_001",
        "category": "Food Processing",
        "expected_investment": 215000.0,
        "own_capital": 300000.0
    }
    res = client.post("/api/v1/reports/dpr/download", json=payload)
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 5000 # Valid PDF bytes
    assert res.content[:4] == b"%PDF"

def test_auth_verify_api():
    payload = {
        "id_token": "demo_guest_token_12345",
        "preferred_language": "hi"
    }
    res = client.post("/api/v1/auth/verify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["preferred_language"] == "hi"
    assert "uid" in data


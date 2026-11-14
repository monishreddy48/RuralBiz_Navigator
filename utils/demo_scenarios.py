"""
RuralBiz Navigator - Pre-configured Demo Scenarios
Provides 3 curated judging scenarios: Strong, Borderline, and High-Risk opportunities.
"""
from typing import Dict, Any
from database.db import get_locality_by_id, get_business_by_category, get_competitors
from core.hyperlocal_engine import calculate_hyperlocal_metrics
from core.financial_engine import calculate_financial_plan
from core.viability_engine import calculate_viability_score
from core.recommendation_engine import generate_business_recommendation
from core.scheme_engine import evaluate_schemes

DEMO_SCENARIOS = {
    "demo_1": {
        "title": "Scenario 1: Strong Opportunity (GO)",
        "description": "Food Processing unit in Agri Hub (Village A) with ₹3,00,000 own capital.",
        "village_id": "VIL_001",
        "category": "Food Processing",
        "own_capital": 300000.0,
        "expected_investment": 215000.0,
        "experience": "Intermediate",
        "is_existing": False,
        "risk_tolerance": "Moderate",
        "monthly_income": 35000.0,
        "target_group_tags": ["General", "Rural", "Agri Producer"]
    },
    "demo_2": {
        "title": "Scenario 2: Borderline Opportunity (MODIFY)",
        "description": "Tailoring & Boutique in Coastal Village (Village B) with ₹30,000 own capital.",
        "village_id": "VIL_002",
        "category": "Tailoring",
        "own_capital": 30000.0,
        "expected_investment": 93000.0,
        "experience": "Beginner",
        "is_existing": False,
        "risk_tolerance": "Conservative",
        "monthly_income": 18000.0,
        "target_group_tags": ["Women", "Rural", "Artisan"]
    },
    "demo_3": {
        "title": "Scenario 3: High-Risk Saturated Market (AVOID)",
        "description": "Retail Kirana in Peri-Urban (Village D) with tight ₹25,000 capital and 3 strong competitors.",
        "village_id": "VIL_004",
        "category": "Retail / General Store",
        "own_capital": 25000.0,
        "expected_investment": 190000.0,
        "experience": "Beginner",
        "is_existing": False,
        "risk_tolerance": "High",
        "monthly_income": 15000.0,
        "target_group_tags": ["General", "Rural"]
    }
}

def load_scenario(scenario_key: str = "demo_1") -> Dict[str, Any]:
    """
    Executes full pipeline for chosen scenario and returns state dictionary.
    """
    cfg = DEMO_SCENARIOS.get(scenario_key, DEMO_SCENARIOS["demo_1"])
    locality = get_locality_by_id(cfg["village_id"])
    business = get_business_by_category(cfg["category"])
    competitors = get_competitors(locality_id=cfg["village_id"], business_type=cfg["category"])
    
    # 1. Hyper-local
    hl_metrics = calculate_hyperlocal_metrics(locality, business, competitors)
    
    # 2. Financials
    proj_cost = cfg["expected_investment"]
    own_cap = min(proj_cost, cfg["own_capital"])
    
    fin_plan = calculate_financial_plan(
        project_cost=proj_cost,
        own_contribution=own_cap,
        monthly_sales=float(business.get("typical_monthly_sales", 65000)),
        variable_cost_ratio=float(business.get("variable_cost_ratio", 0.48)),
        monthly_fixed_cost=float(business.get("monthly_fixed_cost", 7500)),
        unit_price=float(business.get("unit_price_estimate", 80))
    )
    
    # 3. Viability
    viability = calculate_viability_score(hl_metrics, fin_plan, business, locality)
    
    # 4. Recommendation & SWOT
    rec = generate_business_recommendation(viability, fin_plan, hl_metrics, business, locality)
    
    # 5. Schemes
    schemes = evaluate_schemes(proj_cost, cfg["category"], cfg["target_group_tags"], cfg["is_existing"])

    return {
        "scenario_key": scenario_key,
        "scenario_title": cfg["title"],
        "locality": locality,
        "business": business,
        "competitors_df": competitors,
        "hyperlocal_metrics": hl_metrics,
        "financial_plan": fin_plan,
        "viability_result": viability,
        "recommendation": rec,
        "schemes": schemes,
        "user_inputs": {
            "name": "Demo Entrepreneur",
            "village_id": cfg["village_id"],
            "category": cfg["category"],
            "own_capital": cfg["own_capital"],
            "expected_investment": cfg["expected_investment"],
            "experience": cfg["experience"],
            "is_existing": cfg["is_existing"],
            "risk_tolerance": cfg["risk_tolerance"],
            "monthly_income": cfg["monthly_income"],
            "target_group_tags": cfg["target_group_tags"]
        }
    }

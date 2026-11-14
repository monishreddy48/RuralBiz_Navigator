"""
Unit Tests for RuralBiz Navigator - What-If Scenario Stress Engine
Tests sensitivity to shocks in sales volume, input prices, interest rates, and survival determination.
"""
import pytest
from core.financial_engine import calculate_financial_plan
from core.scenario_engine import run_stress_scenario

@pytest.fixture
def base_context():
    biz = {
        "business_name": "Food Processing Unit",
        "category": "Food Processing",
        "typical_capex": 180000,
        "typical_working_capital": 35000,
        "typical_monthly_sales": 65000,
        "variable_cost_ratio": 0.48,
        "monthly_fixed_cost": 7500,
        "unit_price_estimate": 80
    }
    loc = {
        "village_id": "VIL_001",
        "village_name": "Demo Village A",
        "population": 4200,
        "purchasing_power_index": 80
    }
    hl = {
        "market_demand_score": 82.0,
        "competition_score": 78.0,
        "accessibility_score": 80.0
    }
    plan = calculate_financial_plan(
        project_cost=215000,
        own_contribution=75000,
        monthly_sales=65000,
        variable_cost_ratio=0.48,
        monthly_fixed_cost=7500,
        annual_interest_rate=9.5,
        tenure_months=60
    )
    return plan, hl, biz, loc

def test_mild_stress_survival(base_context):
    """Mild shock (Sales -10%, Costs +5%) should result in SURVIVES WITH BUFFER."""
    plan, hl, biz, loc = base_context
    res = run_stress_scenario(
        base_plan=plan,
        hyperlocal_metrics=hl,
        business=biz,
        locality=loc,
        sales_vol_delta_pct=-10.0,
        var_cost_delta_pct=5.0
    )
    assert res["survival_status"] in ["SURVIVES WITH BUFFER", "VULNERABLE - DEBT STRESS"]
    assert res["stress_case"]["monthly_sales"] < plan["monthly_sales"]

def test_catastrophic_stress_failure(base_context):
    """Severe shock (Sales -50%, Variable Costs +40%) must trigger FAILS / INSOLVENT."""
    plan, hl, biz, loc = base_context
    res = run_stress_scenario(
        base_plan=plan,
        hyperlocal_metrics=hl,
        business=biz,
        locality=loc,
        sales_vol_delta_pct=-50.0,
        var_cost_delta_pct=40.0,
        fixed_cost_delta_pct=30.0
    )
    assert res["survival_status"] == "FAILS / INSOLVENT"
    assert res["stress_case"]["monthly_net_profit"] < 0

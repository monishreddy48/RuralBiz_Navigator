"""
FastAPI Router for What-If Scenario Stress Simulator
"""
from fastapi import APIRouter, HTTPException
from backend.app.models.market import SimulatorRequest, SimulatorResponse
from backend.app.db.database import get_locality_by_id, get_business_by_category, get_competitors_df
from backend.app.core.hyperlocal_engine import calculate_hyperlocal_metrics
from backend.app.core.financial_engine import calculate_financial_plan
from backend.app.core.scenario_engine import run_stress_scenario

router = APIRouter(prefix="/simulator", tags=["What-If Simulator"])

@router.post("/stress", response_model=SimulatorResponse)
async def simulate_stress(req: SimulatorRequest):
    village_id = req.village_id or "VIL_001"
    category = req.category or "Food Processing"
    project_cost = float(req.project_cost if req.project_cost is not None else 215000.0)
    own_capital = float(req.own_capital if req.own_capital is not None else (req.own_contribution if req.own_contribution is not None else 53750.0))

    locality = get_locality_by_id(village_id) or get_locality_by_id("VIL_001")
    business = get_business_by_category(category) or get_business_by_category("Food Processing")
        
    comp_df = get_competitors_df(locality_id=village_id, business_type=category)
    hl = calculate_hyperlocal_metrics(locality, business, comp_df)
    
    base_plan = calculate_financial_plan(
        project_cost=project_cost,
        own_contribution=own_capital,
        monthly_sales=float(business.get("typical_monthly_sales", 65000.0)),
        variable_cost_ratio=float(business.get("variable_cost_ratio", 0.48)),
        monthly_fixed_cost=float(business.get("monthly_fixed_cost", 7500.0)),
        unit_price=float(business.get("unit_price_estimate", 80.0))
    )
    
    results = run_stress_scenario(
        base_plan=base_plan,
        hyperlocal_metrics=hl,
        business=business,
        locality=locality,
        sales_vol_delta_pct=req.sales_vol_delta_pct,
        price_delta_pct=req.price_delta_pct,
        var_cost_delta_pct=req.var_cost_delta_pct,
        fixed_cost_delta_pct=req.fixed_cost_delta_pct,
        interest_rate_delta=req.interest_rate_delta,
        loan_amount_delta_pct=req.loan_amount_delta_pct
    )
    
    return SimulatorResponse(
        survival_status=results["survival_status"],
        survival_verdict=results["survival_verdict"],
        survival_color=results["survival_color"],
        base_case=results["base_case"],
        stress_case=results["stress_case"],
        shocks_applied=results.get("shocks") or results.get("shocks_applied") or {}
    )


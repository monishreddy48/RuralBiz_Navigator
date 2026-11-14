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
    locality = get_locality_by_id(req.village_id)
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
        
    business = get_business_by_category(req.category)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    comp_df = get_competitors_df(locality_id=req.village_id, business_type=req.category)
    hl = calculate_hyperlocal_metrics(locality, business, comp_df)
    
    base_plan = calculate_financial_plan(
        project_cost=req.project_cost,
        own_contribution=req.own_capital,
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
        shocks_applied=results["shocks_applied"]
    )


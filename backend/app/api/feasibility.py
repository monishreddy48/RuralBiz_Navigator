"""
FastAPI Router for Business Feasibility Assessment
"""
from fastapi import APIRouter, HTTPException
from backend.app.models.feasibility import FeasibilityRequest, FeasibilityResponse
from backend.app.db.database import (
    get_locality_by_id, get_business_by_category, get_competitors_df, save_assessment_record
)
from backend.app.core.hyperlocal_engine import calculate_hyperlocal_metrics
from backend.app.core.financial_engine import calculate_financial_plan
from backend.app.core.viability_engine import calculate_viability_score
from backend.app.core.recommendation_engine import generate_business_recommendation

router = APIRouter(prefix="/feasibility", tags=["Business Feasibility"])

@router.post("/evaluate", response_model=FeasibilityResponse)
async def evaluate_feasibility(req: FeasibilityRequest):
    locality = get_locality_by_id(req.village_id)
    if not locality:
        raise HTTPException(status_code=404, detail=f"Locality with ID '{req.village_id}' not found.")
        
    business = get_business_by_category(req.category)
    if not business:
        raise HTTPException(status_code=404, detail=f"Business category '{req.category}' not found.")
        
    competitors_df = get_competitors_df(locality_id=req.village_id, business_type=req.category)
    
    # 1. Hyperlocal calculations
    hl_metrics = calculate_hyperlocal_metrics(locality, business, competitors_df)
    
    # 2. Financial planning
    fin_sales = float(req.monthly_sales) if (req.monthly_sales and req.monthly_sales > 0) else float(business.get("typical_monthly_sales", 65000.0))
    fin_plan = calculate_financial_plan(
        project_cost=req.expected_investment,
        own_contribution=req.own_capital,
        annual_interest_rate=float(req.annual_interest_rate or 9.5),
        tenure_months=int(req.tenure_months or 60),
        moratorium_months=int(req.moratorium_months if req.moratorium_months is not None else 3),
        monthly_sales=fin_sales,
        variable_cost_ratio=float(business.get("variable_cost_ratio", 0.48)),
        monthly_fixed_cost=float(business.get("monthly_fixed_cost", 7500.0)),
        unit_price=float(business.get("unit_price_estimate", 80.0))
    )
    
    # 3. Viability Scoring
    viability = calculate_viability_score(hl_metrics, fin_plan, business, locality)
    
    # 4. Recommendation & SWOT
    recommendation = generate_business_recommendation(viability, fin_plan, hl_metrics, business, locality)
    recommendation["verdict"] = recommendation["decision"]

    factor_mapping = [
        (("Market Demand", "market_demand"), "Market Demand", 0.25),
        (("Competition", "competition"), "Competition Saturation", 0.15),
        (("Accessibility", "accessibility"), "Infrastructure & Road Access", 0.10),
        (("Financial Fit", "financial_fit"), "Financial Fit & Debt Coverage", 0.20),
        (("Growth Potential", "growth_potential"), "Growth Potential", 0.15),
        (("Risk Resilience", "risk_resilience"), "Risk Resilience", 0.15),
    ]
    factor_scores = []
    breakdown_normalized = {}
    for keys, label, weight in factor_mapping:
        score = 70.0
        for k in keys:
            if k in viability.get("breakdown", {}):
                score = float(viability["breakdown"][k])
                break
        factor_scores.append({
            "factor": label,
            "score": round(score, 1),
            "weight": weight,
            "contribution": round(score * weight, 1)
        })
        breakdown_normalized[keys[1]] = round(score, 1)
    
    # 5. Persist to DB
    assessment_id = save_assessment_record({
        "locality_id": req.village_id,
        "business_id": business["business_id"],
        "own_capital": req.own_capital,
        "expected_investment": req.expected_investment,
        "experience_level": req.experience_level,
        "is_existing_business": req.is_existing,
        "monthly_household_income": req.monthly_income,
        "risk_tolerance": req.risk_tolerance,
        "viability_score": viability["viability_score"],
        "recommendation": recommendation["decision"]
    })
    
    return FeasibilityResponse(
        assessment_id=assessment_id,
        viability_score=viability["viability_score"],
        composite_score=viability["viability_score"],
        classification=viability["classification"],
        status_color=viability["status_color"],
        status_badge=viability["status_badge"],
        breakdown=viability["breakdown"],
        factor_scores=factor_scores,
        recommendation=recommendation,
        financial_summary={
            "project_cost": fin_plan["project_cost"],
            "loan_amount": fin_plan["loan_amount"],
            "monthly_emi": fin_plan["monthly_emi"],
            "monthly_net_profit": fin_plan["monthly_net_profit"],
            "dscr": fin_plan["dscr"],
            "break_even_revenue": fin_plan["break_even_revenue"],
            "margin_of_safety_pct": fin_plan["margin_of_safety_pct"]
        },
        hyperlocal_summary={
            "customer_pool": hl_metrics["customer_pool"],
            "num_competitors": hl_metrics["num_competitors"],
            "unmet_demand_rupees": hl_metrics["estimated_unmet_demand_rupees"],
            "market_demand_score": hl_metrics["market_demand_score"],
            "competition_score": hl_metrics["competition_score"]
        }
    )


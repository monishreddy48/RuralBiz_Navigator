"""
FastAPI Router for Financial Calculator & Amortization
"""
from fastapi import APIRouter
from backend.app.models.financial import FinancialPlanRequest, FinancialPlanResponse
from backend.app.core.financial_engine import calculate_financial_plan, generate_amortization_schedule

router = APIRouter(prefix="/financial", tags=["Financial Planning"])

@router.post("/calculate", response_model=FinancialPlanResponse)
async def calculate_finance(req: FinancialPlanRequest):
    plan = calculate_financial_plan(
        project_cost=req.project_cost,
        own_contribution=req.own_contribution,
        annual_interest_rate=req.annual_interest_rate,
        tenure_months=req.tenure_months,
        moratorium_months=req.moratorium_months,
        monthly_sales=req.monthly_sales,
        variable_cost_ratio=req.variable_cost_ratio,
        monthly_fixed_cost=req.monthly_fixed_cost,
        unit_price=req.unit_price
    )
    return plan


"""
Pydantic Schemas for Financial Planning & Debt Structuring
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class FinancialPlanRequest(BaseModel):
    project_cost: float = Field(..., ge=1000.0, description="Total project setup outlay in ₹")
    own_contribution: float = Field(..., ge=0.0, description="Own capital contribution in ₹")
    annual_interest_rate: float = Field(default=9.5, ge=0.0, le=30.0, description="Annual loan interest rate %")
    tenure_months: int = Field(default=60, ge=6, le=120, description="Repayment tenure in months")
    moratorium_months: int = Field(default=3, ge=0, le=24, description="Grace period before principal repayment in months")
    monthly_sales: float = Field(default=65000.0, ge=1000.0, description="Estimated monthly sales in ₹")
    variable_cost_ratio: float = Field(default=0.48, ge=0.05, le=0.95, description="Variable cost / COGS ratio (0.0 - 1.0)")
    monthly_fixed_cost: float = Field(default=7500.0, ge=0.0, description="Monthly fixed overhead in ₹")
    unit_price: float = Field(default=80.0, ge=1.0, description="Estimated unit selling price in ₹")

class AmortizationScheduleRow(BaseModel):
    month: int
    opening_balance: float
    emi: float
    interest: float
    principal: float
    closing_balance: float
    is_moratorium: bool

class CashFlowMonthRow(BaseModel):
    month: int
    revenue: float
    variable_costs: float
    fixed_costs: float
    operating_profit: float
    emi: float
    net_cash_flow: float
    closing_cash: float

class FinancialPlanResponse(BaseModel):
    project_cost: float
    own_contribution: float
    own_pct: float
    loan_amount: float
    loan_pct: float
    annual_interest_rate: float
    tenure_months: int
    moratorium_months: int
    monthly_emi: float
    total_repayment: float
    total_interest: float
    monthly_sales: float
    monthly_variable_costs: float
    monthly_fixed_costs: float
    monthly_operating_profit: float
    monthly_net_profit: float
    net_margin_pct: float
    break_even_revenue: float
    break_even_units: int
    current_monthly_units: int
    margin_of_safety_pct: float
    dscr: float
    dscr_status: str
    dscr_badge: str
    financial_fit_score: float
    amortization_schedule: List[AmortizationScheduleRow]
    cash_flow_12: List[CashFlowMonthRow]


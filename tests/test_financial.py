"""
Unit Tests for RuralBiz Navigator - Financial Engine
Covers reducing-balance EMI, amortization, break-even, DSCR, cash flows, and edge cases.
"""
import pytest
import math
from core.financial_engine import (
    calculate_reducing_balance_emi,
    generate_amortization_schedule,
    calculate_financial_plan
)

def test_reducing_balance_emi_standard():
    """Verify EMI formula matches standard bank amortization tables."""
    # Principal = 1,00,000, 9.5% p.a., 60 months
    # Formula: P * r * (1+r)^n / ((1+r)^n - 1)
    # monthly r = 0.095 / 12 = 0.007916666...
    # Expected EMI ~ 2100.19
    emi = calculate_reducing_balance_emi(100000.0, 9.5, 60)
    assert 2095.0 <= emi <= 2105.0

def test_reducing_balance_emi_zero_interest():
    """Zero interest should result in equal principal division."""
    emi = calculate_reducing_balance_emi(60000.0, 0.0, 60)
    assert emi == 1000.0

def test_reducing_balance_emi_zero_loan():
    """Zero principal should yield zero EMI."""
    emi = calculate_reducing_balance_emi(0.0, 10.0, 60)
    assert emi == 0.0

def test_amortization_schedule_closing_balance():
    """Amortization schedule must bring loan balance to zero at maturity."""
    principal = 50000.0
    tenure = 24
    rate = 10.0
    schedule = generate_amortization_schedule(principal, rate, tenure, moratorium_months=0)
    
    assert len(schedule) == tenure
    assert schedule[0]["opening_balance"] == principal
    assert schedule[-1]["closing_balance"] == 0.0
    
    # Sum of principal paid must equal initial principal
    total_principal_paid = sum(row["principal"] for row in schedule)
    assert math.isclose(total_principal_paid, principal, abs_tol=1.0)

def test_moratorium_handling():
    """During moratorium, principal paid should be zero and closing balance remains unchanged."""
    principal = 100000.0
    tenure = 36
    moratorium = 3
    schedule = generate_amortization_schedule(principal, 9.0, tenure, moratorium_months=moratorium)
    
    for m in range(moratorium):
        assert schedule[m]["is_moratorium"] is True
        assert schedule[m]["principal"] == 0.0
        assert schedule[m]["closing_balance"] == principal
        assert schedule[m]["interest"] > 0.0
        
    # Post-moratorium should reduce balance
    assert schedule[moratorium]["principal"] > 0.0

def test_break_even_point_calculation():
    """Break-even revenue should equal Fixed Costs / (1 - Variable Cost Ratio)."""
    # Fixed costs = 10,000, EMI = 0, Var ratio = 0.5 -> BEP = 10000 / 0.5 = 20,000
    plan = calculate_financial_plan(
        project_cost=100000,
        own_contribution=100000, # Zero loan
        monthly_sales=50000,
        variable_cost_ratio=0.50,
        monthly_fixed_cost=10000,
        unit_price=100
    )
    assert plan["loan_amount"] == 0.0
    assert plan["monthly_emi"] == 0.0
    assert plan["break_even_revenue"] == 20000.0
    assert plan["break_even_units"] == 200 # 20000 / 100

def test_dscr_classification():
    """DSCR must accurately classify strong, acceptable, and caution tiers."""
    # Strong: Op Profit 30,000, EMI 10,000 -> DSCR = 3.0
    plan_strong = calculate_financial_plan(
        project_cost=200000,
        own_contribution=50000,
        monthly_sales=100000,
        variable_cost_ratio=0.50,
        monthly_fixed_cost=10000,
        annual_interest_rate=9.0,
        tenure_months=60
    )
    assert plan_strong["dscr"] > 1.5
    assert plan_strong["dscr_badge"] == "STRONG"

    # Default / Loss case: Op Profit <= 0
    plan_loss = calculate_financial_plan(
        project_cost=200000,
        own_contribution=50000,
        monthly_sales=15000, # Very low sales
        variable_cost_ratio=0.60,
        monthly_fixed_cost=12000,
        annual_interest_rate=10.0,
        tenure_months=36
    )
    assert plan_loss["dscr"] == 0.0
    assert plan_loss["dscr_badge"] == "HIGH_RISK"

def test_cash_flow_continuity():
    """Each month's closing cash balance must equal prior closing + current net cash flow."""
    plan = calculate_financial_plan(
        project_cost=150000,
        own_contribution=50000,
        monthly_sales=60000,
        variable_cost_ratio=0.45,
        monthly_fixed_cost=8000
    )
    cf = plan["cash_flow_12"]
    assert len(cf) == 12
    
    for i in range(1, len(cf)):
        prev_closing = cf[i-1]["closing_cash"]
        curr_net = cf[i]["net_cash_flow"]
        curr_closing = cf[i]["closing_cash"]
        assert math.isclose(curr_closing, prev_closing + curr_net, abs_tol=0.05)

def test_financial_edge_cases():
    """Handles extreme inputs without crashing."""
    # Very large investment
    plan_large = calculate_financial_plan(
        project_cost=50000000.0,
        own_contribution=5000000.0,
        monthly_sales=5000000.0
    )
    assert plan_large["monthly_emi"] > 0.0
    assert plan_large["dscr"] > 0.0
    
    # Zero sales revenue
    plan_zero_sales = calculate_financial_plan(
        project_cost=100000.0,
        own_contribution=20000.0,
        monthly_sales=0.0
    )
    assert plan_zero_sales["monthly_operating_profit"] < 0
    assert plan_zero_sales["margin_of_safety_pct"] == -100.0

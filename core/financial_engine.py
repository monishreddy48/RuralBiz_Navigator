"""
RuralBiz Navigator - Deterministic Financial Engine
Implements reducing-balance EMI, amortization, 12-month cash flows, break-even, and DSCR.
NO LLM calculations are used.
"""
from typing import Dict, Any, List
import math
import pandas as pd
from config import DSCR_THRESHOLDS

def calculate_reducing_balance_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int
) -> float:
    """
    Standard reducing-balance monthly EMI calculation.
    Handles zero-interest and zero-principal edge cases safely.
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    
    if annual_interest_rate <= 0:
        return round(principal / tenure_months, 2)
    
    monthly_rate = (annual_interest_rate / 100.0) / 12.0
    factor = math.pow(1.0 + monthly_rate, tenure_months)
    emi = principal * monthly_rate * factor / (factor - 1.0)
    return round(emi, 2)

def generate_amortization_schedule(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
    moratorium_months: int = 0
) -> List[Dict[str, Any]]:
    """
    Generates month-by-month loan repayment schedule with optional moratorium.
    During moratorium, simple interest is charged without principal reduction.
    """
    if principal <= 0 or tenure_months <= 0:
        return []
    
    monthly_rate = (annual_interest_rate / 100.0) / 12.0 if annual_interest_rate > 0 else 0.0
    repayment_months = max(1, tenure_months - moratorium_months)
    
    # Calculate regular EMI for the post-moratorium period
    regular_emi = calculate_reducing_balance_emi(principal, annual_interest_rate, repayment_months)
    
    schedule = []
    balance = principal
    
    for m in range(1, tenure_months + 1):
        opening_bal = balance
        if m <= moratorium_months:
            # Moratorium period: Interest service only
            interest = round(opening_bal * monthly_rate, 2)
            principal_paid = 0.0
            emi_paid = interest
            closing_bal = opening_bal
        else:
            interest = round(opening_bal * monthly_rate, 2)
            principal_paid = min(opening_bal, round(regular_emi - interest, 2))
            emi_paid = round(principal_paid + interest, 2)
            closing_bal = max(0.0, round(opening_bal - principal_paid, 2))
            balance = closing_bal
            
        schedule.append({
            "month": m,
            "opening_balance": opening_bal,
            "emi": emi_paid,
            "interest": interest,
            "principal": principal_paid,
            "closing_balance": closing_bal,
            "is_moratorium": (m <= moratorium_months)
        })
        
        if closing_bal <= 0:
            break
            
    return schedule

def calculate_financial_plan(
    project_cost: float,
    own_contribution: float,
    annual_interest_rate: float = 9.5,
    tenure_months: int = 60,
    moratorium_months: int = 3,
    monthly_sales: float = 65000.0,
    variable_cost_ratio: float = 0.48,
    monthly_fixed_cost: float = 7500.0,
    unit_price: float = 80.0
) -> Dict[str, Any]:
    """
    Comprehensive financial plan computation:
    - Capital structuring (own vs loan)
    - EMI and interest burden
    - Monthly P&L
    - 12-month cash flow simulation
    - Break-even revenue and units
    - DSCR and risk assessment
    """
    project_cost = max(1000.0, float(project_cost))
    own_contribution = max(0.0, min(project_cost, float(own_contribution)))
    loan_amount = max(0.0, project_cost - own_contribution)
    
    own_pct = round((own_contribution / project_cost) * 100.0, 1)
    loan_pct = round((loan_amount / project_cost) * 100.0, 1)
    
    # 1. EMI Calculation
    repayment_months = max(1, tenure_months - moratorium_months)
    monthly_emi = calculate_reducing_balance_emi(loan_amount, annual_interest_rate, repayment_months)
    
    # Amortization summary
    amort_schedule = generate_amortization_schedule(loan_amount, annual_interest_rate, tenure_months, moratorium_months)
    total_repayment = sum(row["emi"] for row in amort_schedule) if amort_schedule else 0.0
    total_interest = sum(row["interest"] for row in amort_schedule) if amort_schedule else 0.0
    
    # 2. Operating P&L (Monthly steady state)
    monthly_sales = max(0.0, float(monthly_sales))
    var_cost_ratio = max(0.05, min(0.95, float(variable_cost_ratio)))
    fixed_costs = max(0.0, float(monthly_fixed_cost))
    
    monthly_var_cost = round(monthly_sales * var_cost_ratio, 2)
    total_operating_costs = round(monthly_var_cost + fixed_costs, 2)
    operating_profit = round(monthly_sales - total_operating_costs, 2)  # EBITDA
    net_profit = round(operating_profit - monthly_emi, 2)
    net_margin_pct = round((net_profit / monthly_sales) * 100.0, 1) if monthly_sales > 0 else 0.0

    # 3. Break-Even Analysis
    # BEP Revenue = (Fixed Costs + Monthly EMI) / (1 - Variable Cost Ratio)
    contribution_margin_ratio = 1.0 - var_cost_ratio
    total_fixed_burden = fixed_costs + monthly_emi
    break_even_revenue = round(total_fixed_burden / contribution_margin_ratio, 2) if contribution_margin_ratio > 0 else 999999.0
    
    unit_price = max(1.0, float(unit_price))
    break_even_units = math.ceil(break_even_revenue / unit_price) if unit_price > 0 else 0
    current_units = math.ceil(monthly_sales / unit_price) if unit_price > 0 else 0
    
    # Margin of Safety %
    margin_of_safety_pct = round(((monthly_sales - break_even_revenue) / monthly_sales) * 100.0, 1) if monthly_sales > 0 else -100.0

    # 4. Debt Service Coverage Ratio (DSCR)
    # DSCR = Operating Profit (EBITDA) / Monthly EMI
    if loan_amount <= 0 or monthly_emi <= 0:
        dscr = 999.0
        dscr_status = "Debt-Free / No Loan Burden"
        dscr_badge = "STRONG"
    else:
        if operating_profit <= 0:
            dscr = 0.0
            dscr_status = "Insolvent / Operating Loss"
            dscr_badge = "HIGH_RISK"
        else:
            dscr = round(operating_profit / monthly_emi, 2)
            if dscr >= DSCR_THRESHOLDS["strong"]:
                dscr_status = "Strong Debt Servicing Ability"
                dscr_badge = "STRONG"
            elif dscr >= DSCR_THRESHOLDS["acceptable"]:
                dscr_status = "Acceptable Debt Coverage"
                dscr_badge = "ACCEPTABLE"
            elif dscr >= DSCR_THRESHOLDS["caution"]:
                dscr_status = "Caution - Very Tight Cash Buffer"
                dscr_badge = "CAUTION"
            else:
                dscr_status = "High Repayment Risk - Default Danger"
                dscr_badge = "HIGH_RISK"

    # 5. 12-Month Dynamic Cash Flow Projection
    # Incorporates realistic ramp-up (Months 1-3 ramp: 65%, 80%, 95%, 100% thereafter)
    cash_flow_12 = []
    running_cash = own_contribution * 0.15  # 15% own equity reserved as initial cash float
    
    ramp_factors = [0.65, 0.80, 0.92, 1.0, 1.0, 1.02, 1.02, 1.05, 1.05, 1.05, 1.08, 1.08]
    
    for m in range(1, 13):
        ramp = ramp_factors[m - 1]
        m_sales = round(monthly_sales * ramp, 2)
        m_var_cost = round(m_sales * var_cost_ratio, 2)
        m_fixed = fixed_costs
        m_op_profit = round(m_sales - (m_var_cost + m_fixed), 2)
        
        # Look up EMI for this month from amort schedule
        m_emi = amort_schedule[m - 1]["emi"] if len(amort_schedule) >= m else monthly_emi
        
        m_net_flow = round(m_op_profit - m_emi, 2)
        running_cash = round(running_cash + m_net_flow, 2)
        
        cash_flow_12.append({
            "month": m,
            "revenue": m_sales,
            "variable_costs": m_var_cost,
            "fixed_costs": m_fixed,
            "operating_profit": m_op_profit,
            "emi": m_emi,
            "net_cash_flow": m_net_flow,
            "closing_cash": running_cash
        })

    # 6. Financial Fit Score (0-100)
    # Evaluates how comfortable this business is for the given capital & debt
    fit_score = 50.0
    # Own capital ratio bonus (up to +25)
    fit_score += min(25.0, (own_pct / 50.0) * 25.0)
    # DSCR bonus (up to +25)
    if dscr >= 1.5:
        fit_score += 25.0
    elif dscr >= 1.2:
        fit_score += 18.0
    elif dscr >= 1.0:
        fit_score += 10.0
    else:
        fit_score -= 20.0
    # Margin of Safety bonus
    if margin_of_safety_pct > 25.0:
        fit_score += 15.0
    elif margin_of_safety_pct > 10.0:
        fit_score += 8.0
    elif margin_of_safety_pct < 0:
        fit_score -= 25.0
        
    financial_fit_score = round(max(5.0, min(100.0, fit_score)), 1)

    return {
        "project_cost": project_cost,
        "own_contribution": own_contribution,
        "own_pct": own_pct,
        "loan_amount": loan_amount,
        "loan_pct": loan_pct,
        "annual_interest_rate": annual_interest_rate,
        "tenure_months": tenure_months,
        "moratorium_months": moratorium_months,
        "monthly_emi": monthly_emi,
        "total_repayment": round(total_repayment, 2),
        "total_interest": round(total_interest, 2),
        "monthly_sales": monthly_sales,
        "monthly_variable_costs": monthly_var_cost,
        "monthly_fixed_costs": fixed_costs,
        "monthly_operating_profit": operating_profit,
        "monthly_net_profit": net_profit,
        "net_margin_pct": net_margin_pct,
        "break_even_revenue": break_even_revenue,
        "break_even_units": break_even_units,
        "current_monthly_units": current_units,
        "margin_of_safety_pct": margin_of_safety_pct,
        "dscr": dscr,
        "dscr_status": dscr_status,
        "dscr_badge": dscr_badge,
        "financial_fit_score": financial_fit_score,
        "amortization_schedule": amort_schedule,
        "cash_flow_12": cash_flow_12
    }

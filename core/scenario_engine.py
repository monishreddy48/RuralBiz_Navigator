"""
RuralBiz Navigator - What-If Scenario Stress Testing Engine
Evaluates sensitivity to shocks in sales, price, variable/fixed costs, and interest rates.
"""
from typing import Dict, Any
from core.financial_engine import calculate_financial_plan
from core.viability_engine import calculate_viability_score

def run_stress_scenario(
    base_plan: Dict[str, Any],
    hyperlocal_metrics: Dict[str, Any],
    business: Dict[str, Any],
    locality: Dict[str, Any],
    sales_vol_delta_pct: float = 0.0,
    price_delta_pct: float = 0.0,
    var_cost_delta_pct: float = 0.0,
    fixed_cost_delta_pct: float = 0.0,
    interest_rate_delta: float = 0.0,
    loan_amount_delta_pct: float = 0.0
) -> Dict[str, Any]:
    """
    Computes stress case financial metrics under shocks and compares with base case.
    All calculations are deterministic.
    """
    base_sales = base_plan["monthly_sales"]
    base_price = float(business.get("unit_price_estimate", 100.0))
    base_var_ratio = float(business.get("variable_cost_ratio", 0.5))
    base_fixed = base_plan["monthly_fixed_costs"]
    base_rate = base_plan["annual_interest_rate"]
    base_loan = base_plan["loan_amount"]
    base_tenure = base_plan["tenure_months"]
    base_moratorium = base_plan["moratorium_months"]
    base_project_cost = base_plan["project_cost"]
    
    # 1. Apply Shocks
    # Volume and price compound into sales revenue: Sales = Vol * Price
    effective_vol_mult = max(0.1, 1.0 + (sales_vol_delta_pct / 100.0))
    effective_price_mult = max(0.5, 1.0 + (price_delta_pct / 100.0))
    stress_sales = round(base_sales * effective_vol_mult * effective_price_mult, 2)
    stress_unit_price = round(base_price * effective_price_mult, 2)
    
    # Variable cost ratio shock (e.g. raw material spike)
    effective_var_mult = max(0.5, 1.0 + (var_cost_delta_pct / 100.0))
    stress_var_ratio = min(0.92, round(base_var_ratio * effective_var_mult / effective_price_mult, 3))
    
    # Fixed cost shock (e.g. rent / wage increase)
    effective_fixed_mult = max(0.5, 1.0 + (fixed_cost_delta_pct / 100.0))
    stress_fixed = round(base_fixed * effective_fixed_mult, 2)
    
    # Interest rate adjustment
    stress_rate = max(0.0, round(base_rate + interest_rate_delta, 2))
    
    # Loan amount adjustment
    stress_loan = max(0.0, round(base_loan * (1.0 + (loan_amount_delta_pct / 100.0)), 2))
    stress_project_cost = round(base_project_cost + (stress_loan - base_loan), 2)
    stress_own = max(0.0, stress_project_cost - stress_loan)
    
    # 2. Re-compute Financial Plan under Stress
    stress_plan = calculate_financial_plan(
        project_cost=stress_project_cost,
        own_contribution=stress_own,
        annual_interest_rate=stress_rate,
        tenure_months=base_tenure,
        moratorium_months=base_moratorium,
        monthly_sales=stress_sales,
        variable_cost_ratio=stress_var_ratio,
        monthly_fixed_cost=stress_fixed,
        unit_price=stress_unit_price
    )
    
    # 3. Re-compute Viability Score under Stress
    stress_viability = calculate_viability_score(
        hyperlocal_metrics=hyperlocal_metrics,
        financial_plan=stress_plan,
        business=business,
        locality=locality
    )
    
    # 4. Survival Assessment
    stress_net_profit = stress_plan["monthly_net_profit"]
    stress_dscr = stress_plan["dscr"]
    stress_mos = stress_plan["margin_of_safety_pct"]
    
    if stress_net_profit > 0 and (stress_dscr >= 1.1 or stress_loan == 0) and stress_mos >= 0:
        survival_status = "SURVIVES WITH BUFFER"
        survival_verdict = "YES - The business sustains operational profitability and debt servicing even under this stress shock."
        survival_color = "#10B981"  # Emerald Green
    elif stress_net_profit > 0 and stress_dscr < 1.1 and stress_loan > 0:
        survival_status = "VULNERABLE - DEBT STRESS"
        survival_verdict = "MARGINAL - The business generates operating income, but debt obligations exceed safety limits. High risk of delayed EMI."
        survival_color = "#F59E0B"  # Amber
    else:
        survival_status = "FAILS / INSOLVENT"
        survival_verdict = f"NO - Business incurs negative monthly net cash flow (-₹{abs(stress_net_profit):,.0f}) under this stress scenario."
        survival_color = "#EF4444"  # Red

    return {
        "shocks": {
            "sales_vol_delta_pct": sales_vol_delta_pct,
            "price_delta_pct": price_delta_pct,
            "var_cost_delta_pct": var_cost_delta_pct,
            "fixed_cost_delta_pct": fixed_cost_delta_pct,
            "interest_rate_delta": interest_rate_delta,
            "loan_amount_delta_pct": loan_amount_delta_pct
        },
        "base_case": {
            "monthly_sales": base_plan["monthly_sales"],
            "monthly_net_profit": base_plan["monthly_net_profit"],
            "monthly_emi": base_plan["monthly_emi"],
            "break_even_revenue": base_plan["break_even_revenue"],
            "dscr": base_plan["dscr"],
            "viability_score": base_plan.get("viability_score", 0.0)
        },
        "stress_case": {
            "monthly_sales": stress_plan["monthly_sales"],
            "monthly_net_profit": stress_plan["monthly_net_profit"],
            "monthly_emi": stress_plan["monthly_emi"],
            "break_even_revenue": stress_plan["break_even_revenue"],
            "dscr": stress_plan["dscr"],
            "viability_score": stress_viability["viability_score"],
            "stress_plan": stress_plan
        },
        "survival_status": survival_status,
        "survival_verdict": survival_verdict,
        "survival_color": survival_color
    }

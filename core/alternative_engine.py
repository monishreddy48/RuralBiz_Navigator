"""
RuralBiz Navigator - Business Alternatives Recommender
Ranks all available micro-business categories for the user's locality and budget.
"""
from typing import Dict, Any, List
import pandas as pd
from database.db import get_businesses, get_competitors
from core.hyperlocal_engine import calculate_hyperlocal_metrics
from core.financial_engine import calculate_financial_plan
from core.viability_engine import calculate_viability_score

def evaluate_business_alternatives(
    locality: Dict[str, Any],
    available_capital: float,
    current_business_category: str = None
) -> List[Dict[str, Any]]:
    """
    Ranks all 10 rural business benchmarks against the user's location and capital.
    Produces deterministic comparative viability scores.
    """
    businesses_df = get_businesses()
    competitors_df = get_competitors(locality_id=locality.get("village_id"))
    
    alternatives = []
    
    for _, b_row in businesses_df.iterrows():
        b_dict = dict(b_row)
        cat = b_dict["category"]
        
        # Filter competitors for this specific business type in this locality
        cat_competitors = competitors_df[competitors_df["business_type"] == cat]
        
        # 1. Hyper-local metrics
        hl_metrics = calculate_hyperlocal_metrics(locality, b_dict, cat_competitors)
        
        # 2. Financial plan using benchmark parameters and user's available capital
        typical_capex = float(b_dict["typical_capex"])
        typical_wc = float(b_dict["typical_working_capital"])
        project_cost = typical_capex + typical_wc
        
        # Equity contribution capped at available capital, remainder is loan
        own_contrib = min(project_cost, max(0.0, float(available_capital)))
        
        fin_plan = calculate_financial_plan(
            project_cost=project_cost,
            own_contribution=own_contrib,
            monthly_sales=float(b_dict["typical_monthly_sales"]),
            variable_cost_ratio=float(b_dict["variable_cost_ratio"]),
            monthly_fixed_cost=float(b_dict["monthly_fixed_cost"]),
            unit_price=float(b_dict.get("unit_price_estimate", 100))
        )
        
        # 3. Viability Score
        viability = calculate_viability_score(hl_metrics, fin_plan, b_dict, locality)
        
        # 4. Generate Comparative Highlights
        highlights = []
        if fin_plan["own_pct"] >= 50.0:
            highlights.append("Low debt reliance (Own capital covers >50% of setup cost)")
        if hl_metrics["competition_score"] >= 75:
            highlights.append(f"Low competition in {locality.get('village_name', 'village')}")
        if hl_metrics["market_demand_score"] >= 75:
            highlights.append("Strong local agricultural / household demand match")
        if fin_plan["dscr"] >= 1.5:
            highlights.append("Robust debt service buffer (DSCR > 1.5)")
        if not highlights:
            highlights.append("Moderate initial investment requirement")
            
        alternatives.append({
            "business_id": b_dict["business_id"],
            "business_name": b_dict["business_name"],
            "category": cat,
            "project_cost": project_cost,
            "own_capital_required": own_contrib,
            "loan_required": fin_plan["loan_amount"],
            "monthly_net_profit": fin_plan["monthly_net_profit"],
            "dscr": fin_plan["dscr"],
            "viability_score": viability["viability_score"],
            "classification": viability["classification"],
            "status_color": viability["status_color"],
            "market_demand_score": hl_metrics["market_demand_score"],
            "competition_score": hl_metrics["competition_score"],
            "financial_fit_score": fin_plan["financial_fit_score"],
            "highlights": highlights,
            "is_current": (cat.lower() == str(current_business_category).lower())
        })
        
    # Sort descending by viability score
    alternatives.sort(key=lambda x: x["viability_score"], reverse=True)
    return alternatives

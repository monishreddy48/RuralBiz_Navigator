"""
RuralBiz Navigator - Deterministic Viability Engine
Combines hyper-local metrics and financial feasibility into a weighted 0-100 viability score.
"""
from typing import Dict, Any
from config import VIABILITY_WEIGHTS, VIABILITY_THRESHOLDS

def calculate_viability_score(
    hyperlocal_metrics: Dict[str, Any],
    financial_plan: Dict[str, Any],
    business: Dict[str, Any],
    locality: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes deterministic viability score (0-100) and factor breakdowns.
    """
    # 1. Component Scores
    market_demand = float(hyperlocal_metrics.get("market_demand_score", 60.0))
    competition = float(hyperlocal_metrics.get("competition_score", 60.0))
    accessibility = float(hyperlocal_metrics.get("accessibility_score", 60.0))
    financial_fit = float(financial_plan.get("financial_fit_score", 50.0))
    
    # 2. Growth Potential Score (0-100)
    growth_str = str(business.get("growth_potential", "Moderate")).lower()
    base_growth = 85.0 if "high" in growth_str else (65.0 if "mod" in growth_str else 45.0)
    # Uplift from locality purchasing power and population
    purchasing_pwr = float(locality.get("purchasing_power_index", 60.0))
    growth_potential = (base_growth * 0.7) + (purchasing_pwr * 0.3)
    growth_potential = round(max(10.0, min(100.0, growth_potential)), 1)
    
    # 3. Risk Resilience Score (0-100, where HIGHER is safer / lower risk)
    risk_level_str = str(business.get("risk_level", "Medium")).lower()
    base_risk_resilience = 85.0 if "low" in risk_level_str else (65.0 if "med" in risk_level_str else 45.0)
    # Impact of DSCR on risk resilience
    dscr = float(financial_plan.get("dscr", 1.2))
    if dscr >= 1.5:
        base_risk_resilience += 15.0
    elif dscr < 1.0:
        base_risk_resilience -= 25.0
    risk_resilience = round(max(5.0, min(100.0, base_risk_resilience)), 1)

    # 4. Weighted Total
    w = VIABILITY_WEIGHTS
    total_score = (
        (market_demand * w["market_demand"]) +
        (competition * w["competition"]) +
        (accessibility * w["accessibility"]) +
        (financial_fit * w["financial_fit"]) +
        (growth_potential * w["growth_potential"]) +
        (risk_resilience * w["risk"])
    )
    final_score = round(max(0.0, min(100.0, total_score)), 1)

    # 5. Classification
    if final_score >= VIABILITY_THRESHOLDS["strong"]:
        classification = "Strong Opportunity"
        status_color = "#10B981"  # Emerald Green
        status_badge = "STRONG"
    elif final_score >= VIABILITY_THRESHOLDS["promising"]:
        classification = "Promising"
        status_color = "#3B82F6"  # Blue
        status_badge = "PROMISING"
    elif final_score >= VIABILITY_THRESHOLDS["caution"]:
        classification = "Needs Caution"
        status_color = "#F59E0B"  # Amber
        status_badge = "CAUTION"
    else:
        classification = "High Risk"
        status_color = "#EF4444"  # Red
        status_badge = "HIGH_RISK"

    breakdown = {
        "Market Demand": market_demand,
        "Competition": competition,
        "Accessibility": accessibility,
        "Financial Fit": financial_fit,
        "Growth Potential": growth_potential,
        "Risk Resilience": risk_resilience
    }

    return {
        "viability_score": final_score,
        "classification": classification,
        "status_color": status_color,
        "status_badge": status_badge,
        "breakdown": breakdown,
        "weights": w
    }

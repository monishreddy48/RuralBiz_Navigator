"""
RuralBiz Navigator - Recommendation Engine
Determines GO / MODIFY / AVOID decision, grounded evidence, and deterministic SWOT.
"""
from typing import Dict, Any, List
from config import DECISION_THRESHOLDS

def generate_business_recommendation(
    viability_result: Dict[str, Any],
    financial_plan: Dict[str, Any],
    hyperlocal_metrics: Dict[str, Any],
    business: Dict[str, Any],
    locality: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluates viability score, DSCR, and cash flow to determine
    GO, MODIFY, or AVOID recommendation with evidence and SWOT.
    """
    viability_score = viability_result["viability_score"]
    dscr = financial_plan["dscr"]
    net_profit = financial_plan["monthly_net_profit"]
    margin_of_safety = financial_plan["margin_of_safety_pct"]
    num_competitors = hyperlocal_metrics["num_competitors"]
    customer_pool = hyperlocal_metrics["customer_pool"]
    own_pct = financial_plan["own_pct"]
    
    reasons: List[str] = []
    
    # Decision Logic
    is_go = (
        viability_score >= DECISION_THRESHOLDS["go_viability"] and
        dscr >= 1.2 and
        net_profit > 0 and
        margin_of_safety > 10.0
    )
    
    is_avoid = (
        viability_score < DECISION_THRESHOLDS["modify_viability"] or
        net_profit <= 0 or
        (dscr < 1.0 and financial_plan["loan_amount"] > 0) or
        margin_of_safety < -15.0
    )
    
    if is_go:
        decision = "GO"
        decision_label = "Proceed with Business Execution"
        decision_color = "#10B981"  # Emerald Green
        reasons.append(f"Strong overall viability score of {viability_score}/100 indicates robust local demand.")
        reasons.append(f"Comfortable Debt Service Coverage Ratio (DSCR) of {dscr:.2f} provides a healthy repayment cushion.")
        reasons.append(f"Monthly projected net cash flow is positive at ₹{net_profit:,.0f} with a {margin_of_safety:.1f}% margin of safety.")
        reasons.append(f"Addressable rural customer catchment of ~{customer_pool:,} households within 5-10 km radius.")
        confidence = "High"
    elif not is_avoid:
        decision = "MODIFY"
        decision_label = "Viable with Structural Adjustments"
        decision_color = "#F59E0B"  # Amber
        reasons.append(f"Moderate viability score of {viability_score}/100 shows potential but requires risk mitigation.")
        if dscr < 1.2:
            reasons.append(f"Debt coverage is tight (DSCR {dscr:.2f}); consider increasing equity contribution or extending loan tenure.")
        if own_pct < 15.0:
            reasons.append(f"Own equity is low ({own_pct:.1f}%); exploring credit-linked subsidy schemes like PMEGP/PMFME is recommended.")
        if num_competitors >= 2:
            reasons.append(f"{num_competitors} competitors operate in the locality; specialize in quality or competitive pricing.")
        if len(reasons) < 3:
            reasons.append("Optimize initial machinery CapEx to reduce monthly fixed loan burden.")
        confidence = "Medium"
    else:
        decision = "AVOID"
        decision_label = "High Risk - Reconsider or Choose Alternative"
        decision_color = "#EF4444"  # Red
        if viability_score < DECISION_THRESHOLDS["modify_viability"]:
            reasons.append(f"Low viability score of {viability_score}/100 points to weak local market fundamentals.")
        if net_profit <= 0:
            reasons.append(f"Projected monthly operating profit after EMI is negative (-₹{abs(net_profit):,.0f}).")
        if dscr < 1.0 and financial_plan["loan_amount"] > 0:
            reasons.append(f"Critical default risk: DSCR is {dscr:.2f} (below 1.0 threshold required for commercial debt).")
        if num_competitors >= 3:
            reasons.append(f"Market saturation: {num_competitors} existing competitors are already splitting local demand.")
        confidence = "High"

    # Evidence String
    evidence_text = (
        f"Grounded in local demographic indicators ({locality.get('village_name', 'Locality')}: "
        f"Pop {locality.get('population', 0):,}, Purchasing Power Index {locality.get('purchasing_power_index', 0)}), "
        f"{num_competitors} mapped local competitors, and standard benchmark unit economics "
        f"(Typical CapEx ₹{business.get('typical_capex', 0):,.0f}, Margin {float(business.get('typical_margin', 0.25))*100:.0f}%)."
    )

    # Deterministic SWOT
    swot = generate_swot_analysis(hyperlocal_metrics, financial_plan, business, locality)

    return {
        "decision": decision,
        "decision_label": decision_label,
        "decision_color": decision_color,
        "reasons": reasons,
        "evidence": evidence_text,
        "source": "Prototype locality dataset + benchmark dataset",
        "confidence": confidence,
        "disclaimer": "Evidence based on prototype/simulated dataset. Not formal investment advice.",
        "swot": swot
    }

def generate_swot_analysis(
    hyperlocal_metrics: Dict[str, Any],
    financial_plan: Dict[str, Any],
    business: Dict[str, Any],
    locality: Dict[str, Any]
) -> Dict[str, List[str]]:
    """
    Produces deterministic SWOT categories based on analysis facts.
    """
    strengths = []
    weaknesses = []
    opportunities = []
    threats = []

    # Strengths
    if financial_plan.get("own_pct", 0) >= 25.0:
        strengths.append(f"Healthy entrepreneur equity stake ({financial_plan['own_pct']:.0f}% own capital).")
    if hyperlocal_metrics.get("market_demand_score", 0) >= 70:
        strengths.append("High local demand alignment with village agricultural / demographic base.")
    if financial_plan.get("dscr", 0) >= 1.3:
        strengths.append(f"Strong cash buffer for debt servicing (DSCR {financial_plan['dscr']:.2f}).")
    if not strengths:
        strengths.append("Low entry barriers and existing local familiarity with the trade.")

    # Weaknesses
    if financial_plan.get("loan_pct", 0) >= 80.0:
        weaknesses.append(f"High leverage ({financial_plan['loan_pct']:.0f}% debt) creates vulnerability to delayed revenue.")
    if financial_plan.get("margin_of_safety_pct", 0) < 15.0:
        weaknesses.append(f"Low margin of safety ({financial_plan['margin_of_safety_pct']:.1f}% buffer above break-even).")
    if str(business.get("skill_requirement", "")).lower() == "high":
        weaknesses.append("Requires specialized technical skill; training required before scale.")
    if not weaknesses:
        weaknesses.append("Limited initial working capital for sudden bulk supplier orders.")

    # Opportunities
    if hyperlocal_metrics.get("estimated_unmet_demand_rupees", 0) > 20000:
        opportunities.append(f"Estimated unmet local demand of ~₹{hyperlocal_metrics['estimated_unmet_demand_rupees']:,.0f}/month.")
    if float(locality.get("road_access_score", 0)) >= 75:
        opportunities.append("Favorable road connectivity allows supply expansion to neighboring weekly markets (haats).")
    opportunities.append("Eligibility for credit-linked government subsidies (PMEGP / MUDRA / PMFME).")

    # Threats
    if hyperlocal_metrics.get("num_competitors", 0) >= 2:
        threats.append(f"Price competition from {hyperlocal_metrics['num_competitors']} existing village providers.")
    threats.append("Fluctuations in raw material costs and seasonal demand variations.")
    if float(locality.get("bank_access_score", 50)) < 60:
        threats.append("Limited local banking branch density may slow working capital renewals.")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunities": opportunities,
        "threats": threats
    }

"""
RuralBiz Navigator - Scheme Navigator Engine
Deterministic rule-based routing for verified Indian government micro-enterprise schemes.
NO LLM decides eligibility.
"""
from typing import Dict, Any, List
from database.db import get_schemes

def evaluate_schemes(
    project_cost: float,
    business_category: str,
    target_group_tags: List[str] = None,
    is_existing: bool = False
) -> List[Dict[str, Any]]:
    """
    Evaluates verified government schemes against entrepreneur profile deterministically.
    Returns ranked list of schemes with matching status and detailed terms.
    """
    schemes = get_schemes()
    target_group_tags = [t.lower() for t in (target_group_tags or ["general", "rural"])]
    
    results = []
    
    for s in schemes:
        min_cost = float(s.get("min_project_cost", 0.0))
        max_cost = float(s.get("max_project_cost", 10000000.0))
        eligible_categories = [c.lower() for c in s.get("business_types", [])]
        target_group_desc = str(s.get("target_group", "")).lower()
        
        # 1. Cost Alignment Check
        cost_matches = (min_cost <= project_cost <= max_cost)
        
        # 2. Business Category Check
        category_matches = (business_category.lower() in eligible_categories) or ("any" in eligible_categories)
        
        # 3. Target Group Alignment
        group_matches = False
        is_women = any("women" in t or "female" in t for t in target_group_tags)
        is_sc_st = any("sc" in t or "st" in t for t in target_group_tags)
        is_artisan = any("artisan" in t or "craft" in t or "vishwakarma" in t for t in target_group_tags)
        is_shg = any("shg" in t or "self help" in t for t in target_group_tags)
        
        if any(term in target_group_desc for term in ["any", "individual", "micro-entrepreneur", "rural"]):
            group_matches = True
        if is_women and "women" in target_group_desc:
            group_matches = True
        if is_sc_st and ("sc" in target_group_desc or "st" in target_group_desc):
            group_matches = True
        if is_artisan and ("artisan" in target_group_desc or "craft" in target_group_desc or "darzi" in target_group_desc):
            group_matches = True
        if is_shg and "shg" in target_group_desc:
            group_matches = True

        # Special constraint: Stand-Up India requires SC/ST or Women
        if s["scheme_id"] == "SCH_006":
            if not (is_women or is_sc_st):
                group_matches = False

        # 4. Status Determination
        eligibility_checks = [
            {
                "criterion": f"Project Cost within limit (₹{min_cost:,.0f} - ₹{max_cost:,.0f})",
                "passed": cost_matches,
                "detail": f"Your project cost: ₹{project_cost:,.0f}"
            },
            {
                "criterion": f"Business Category eligible ({business_category})",
                "passed": category_matches,
                "detail": f"Eligible for {len(eligible_categories)} trade sectors"
            },
            {
                "criterion": "Target beneficiary group alignment",
                "passed": group_matches,
                "detail": s.get("target_group", "")[:80] + "..."
            }
        ]
        
        # Classification
        if cost_matches and category_matches and group_matches:
            match_status = "MATCHED"
            status_color = "#10B981"  # Emerald Green
            fit_reason = f"Excellent fit: Project budget (₹{project_cost:,.0f}) and trade '{business_category}' align with scheme guidelines."
        elif (cost_matches and category_matches) or (category_matches and group_matches):
            match_status = "POSSIBLE"
            status_color = "#3B82F6"  # Blue
            fit_reason = f"Potential route: Trade fits, but review budget boundaries or documentation criteria."
        elif category_matches:
            match_status = "VERIFICATION REQUIRED"
            status_color = "#F59E0B"  # Amber
            fit_reason = f"Category fits, but project cost ₹{project_cost:,.0f} is outside standard ceiling (₹{min_cost:,.0f} - ₹{max_cost:,.0f})."
        else:
            match_status = "NOT MATCHED"
            status_color = "#9CA3AF"  # Gray
            fit_reason = f"Business category or applicant profile outside this scheme's target focus."

        # Approximate Subsidy Potential
        subsidy_desc = s.get("subsidy_available", "N/A")
        estimated_subsidy_val = 0.0
        if "25%" in subsidy_desc or "35%" in subsidy_desc:
            # PMEGP / PMFME
            sub_pct = 0.35 if (is_women or is_sc_st) else 0.25
            estimated_subsidy_val = min(1000000.0, project_cost * sub_pct)
        elif "15,000" in subsidy_desc:
            estimated_subsidy_val = 15000.0

        results.append({
            "scheme_id": s["scheme_id"],
            "name": s["name"],
            "description": s["description"],
            "match_status": match_status,
            "status_color": status_color,
            "fit_reason": fit_reason,
            "loan_available": s.get("loan_available", ""),
            "subsidy_available": s.get("subsidy_available", ""),
            "estimated_subsidy_rupees": round(estimated_subsidy_val, 2),
            "margin_requirement": s.get("margin_requirement", ""),
            "interest_notes": s.get("interest_notes", ""),
            "collateral_notes": s.get("collateral_notes", ""),
            "application_route": s.get("application_route", ""),
            "documents": s.get("documents", []),
            "source_url": s.get("source_url", ""),
            "last_verified_date": s.get("last_verified_date", ""),
            "verification_status": s.get("verification_status", "VERIFIED"),
            "eligibility_checks": eligibility_checks
        })

    # Sort: MATCHED first, then POSSIBLE, then VERIFICATION REQUIRED, then NOT MATCHED
    rank_order = {"MATCHED": 1, "POSSIBLE": 2, "VERIFICATION REQUIRED": 3, "NOT MATCHED": 4}
    results.sort(key=lambda x: rank_order.get(x["match_status"], 99))
    return results

"""
FastAPI Router for Government Scheme Navigator
"""
from fastapi import APIRouter
from typing import List
from backend.app.models.market import SchemeMatchRequest, SchemeMatchItem, EligibilityCheck
from backend.app.core.scheme_engine import evaluate_schemes

router = APIRouter(prefix="/schemes", tags=["Government Schemes"])

@router.post("/match", response_model=List[SchemeMatchItem])
async def match_schemes(req: SchemeMatchRequest):
    results = evaluate_schemes(
        project_cost=req.project_cost,
        business_category=req.business_category,
        target_group_tags=req.target_group_tags,
        is_existing=req.is_existing
    )
    
    output = []
    for s in results:
        checks = [
            EligibilityCheck(criterion=c["criterion"], passed=c["passed"], detail=c["detail"])
            for c in s.get("eligibility_checks", [])
        ]
        output.append(SchemeMatchItem(
            scheme_id=s["scheme_id"],
            name=s["name"],
            description=s["description"],
            match_status=s["match_status"],
            status_color=s["status_color"],
            fit_reason=s["fit_reason"],
            loan_available=s.get("loan_available"),
            subsidy_available=s.get("subsidy_available"),
            estimated_subsidy_rupees=s.get("estimated_subsidy_rupees", 0.0),
            margin_requirement=s.get("margin_requirement"),
            interest_notes=s.get("interest_notes"),
            collateral_notes=s.get("collateral_notes"),
            application_route=s.get("application_route"),
            source_url=s.get("source_url"),
            eligibility_checks=checks,
            documents=s.get("documents", [])
        ))
    return output


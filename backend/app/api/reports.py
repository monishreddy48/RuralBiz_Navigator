"""
FastAPI Router for Detailed Project Report (DPR) PDF Generation & Download
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.app.db.database import (
    get_locality_by_id, get_business_by_category, get_competitors_df, get_schemes
)
from backend.app.core.hyperlocal_engine import calculate_hyperlocal_metrics
from backend.app.core.financial_engine import calculate_financial_plan
from backend.app.core.viability_engine import calculate_viability_score
from backend.app.core.recommendation_engine import generate_business_recommendation
from backend.app.core.scheme_engine import evaluate_schemes
from backend.app.reports.pdf_generator import generate_dpr_pdf

router = APIRouter(prefix="/reports", tags=["DPR Reports"])

class DPRDownloadRequest(BaseModel):
    user_name: Optional[str] = "Demo Entrepreneur"
    village_id: str = "VIL_001"
    category: str = "Food Processing"
    expected_investment: float = 215000.0
    own_capital: float = 300000.0
    experience_level: str = "Intermediate"
    is_existing: bool = False
    monthly_income: float = 30000.0
    risk_tolerance: str = "Moderate"

@router.post("/dpr/download")
async def download_dpr(req: DPRDownloadRequest):
    locality = get_locality_by_id(req.village_id)
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
        
    business = get_business_by_category(req.category)
    if not business:
        raise HTTPException(status_code=404, detail="Business category not found")
        
    comp_df = get_competitors_df(locality_id=req.village_id, business_type=req.category)
    hl = calculate_hyperlocal_metrics(locality, business, comp_df)
    
    fin = calculate_financial_plan(
        project_cost=req.expected_investment,
        own_contribution=req.own_capital,
        monthly_sales=float(business.get("typical_monthly_sales", 65000.0)),
        variable_cost_ratio=float(business.get("variable_cost_ratio", 0.48)),
        monthly_fixed_cost=float(business.get("monthly_fixed_cost", 7500.0)),
        unit_price=float(business.get("unit_price_estimate", 80.0))
    )
    
    viab = calculate_viability_score(hl, fin, business, locality)
    rec = generate_business_recommendation(viab, fin, hl, business, locality)
    schemes = evaluate_schemes(req.expected_investment, req.category, ["General", "Rural"], req.is_existing)
    
    assessment_data = {
        "name": req.user_name,
        "village_id": req.village_id,
        "category": req.category,
        "own_capital": req.own_capital,
        "expected_investment": req.expected_investment,
        "experience": req.experience_level,
        "is_existing": req.is_existing,
        "risk_tolerance": req.risk_tolerance,
        "monthly_income": req.monthly_income
    }
    
    pdf_bytes = generate_dpr_pdf(
        assessment_data=assessment_data,
        locality=locality,
        business=business,
        hyperlocal_metrics=hl,
        financial_plan=fin,
        viability_result=viab,
        recommendation=rec,
        schemes=schemes
    )
    
    filename = f"RuralBiz_DPR_{req.village_id}_{req.category.replace(' ', '_')}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


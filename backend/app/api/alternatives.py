"""
FastAPI Router for Business Alternatives Recommender
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.models.market import AlternativeItem
from backend.app.db.database import get_locality_by_id
from backend.app.core.alternative_engine import evaluate_business_alternatives

router = APIRouter(prefix="/alternatives", tags=["Business Alternatives"])

@router.get("/rank", response_model=List[AlternativeItem])
async def rank_alternatives(
    village_id: str = Query(..., description="Target village ID"),
    available_capital: float = Query(300000.0, ge=10000.0, description="Available entrepreneur capital in ₹"),
    current_category: Optional[str] = Query(None, description="Currently selected business category")
):
    locality = get_locality_by_id(village_id)
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
        
    alts = evaluate_business_alternatives(
        locality=locality,
        available_capital=available_capital,
        current_business_category=current_category
    )
    
    return [AlternativeItem(**a) for a in alts]


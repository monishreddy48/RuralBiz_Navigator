"""
FastAPI Router for Hyper-Local Market & Catchment GIS
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.models.market import LocalityItem, CompetitorItem, CatchmentResponse
from backend.app.db.database import (
    get_localities, get_locality_by_id, get_businesses, get_business_by_category, get_competitors_df
)
from backend.app.core.hyperlocal_engine import calculate_hyperlocal_metrics

router = APIRouter(prefix="/market", tags=["Hyperlocal Market"])

@router.get("/localities", response_model=List[LocalityItem])
async def list_localities():
    localities = get_localities()
    return localities

@router.get("/businesses")
async def list_businesses():
    businesses = get_businesses()
    return businesses

@router.get("/catchment/{village_id}", response_model=CatchmentResponse)
async def get_catchment(village_id: str, category: str = Query("Food Processing")):
    locality = get_locality_by_id(village_id)
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
        
    business = get_business_by_category(category)
    if not business:
        raise HTTPException(status_code=404, detail=f"Business category '{category}' not found")
        
    comp_df = get_competitors_df(locality_id=village_id, business_type=category)
    hl = calculate_hyperlocal_metrics(locality, business, comp_df)
    
    competitors_list = []
    if comp_df is not None and not comp_df.empty:
        for _, row in comp_df.iterrows():
            competitors_list.append(CompetitorItem(
                competitor_id=str(row["competitor_id"]),
                business_name=str(row["business_name"]),
                business_type=str(row["business_type"]),
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                estimated_monthly_sales=float(row.get("estimated_monthly_sales", 0.0)),
                price_level=str(row.get("price_level", "Medium")),
                customer_rating=float(row.get("customer_rating", 3.5)),
                distance_from_center=float(row.get("distance_from_center", 2.0)),
                strength=row.get("strength"),
                weakness=row.get("weakness")
            ))
            
    return CatchmentResponse(
        locality=LocalityItem(**locality),
        business_category=category,
        competitors=competitors_list,
        customer_pool=hl["customer_pool"],
        market_demand_score=hl["market_demand_score"],
        competition_score=hl["competition_score"],
        accessibility_score=hl["accessibility_score"],
        estimated_unmet_demand_rupees=hl["estimated_unmet_demand_rupees"],
        opportunity_score=hl["local_opportunity_score"]
    )


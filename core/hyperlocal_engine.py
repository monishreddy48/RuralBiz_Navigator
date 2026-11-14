"""
RuralBiz Navigator - Hyper-Local Market Engine
Calculates local demand, competitor saturation, accessibility, and market gap deterministically.
"""
from typing import Dict, Any
import numpy as np

def calculate_hyperlocal_metrics(
    locality: Dict[str, Any],
    business: Dict[str, Any],
    competitors_df
) -> Dict[str, Any]:
    """
    Computes hyper-local market indicators based on demographic, competitor,
    and connectivity factors.
    
    All formulas are deterministic.
    """
    population = float(locality.get("population", 3000))
    households = float(locality.get("households", population / 5.0))
    local_demand_idx = float(locality.get("local_demand_index", 60.0))
    purchasing_power_idx = float(locality.get("purchasing_power_index", 60.0))
    agri_dep = float(locality.get("agriculture_dependency", 50.0))
    livestock_dep = float(locality.get("livestock_dependency", 50.0))
    
    market_dist = float(locality.get("market_distance_km", 5.0))
    road_access = float(locality.get("road_access_score", 70.0))
    transport_score = float(locality.get("public_transport_score", 65.0))
    bank_access = float(locality.get("bank_access_score", 60.0))
    weekly_mkt_freq = float(locality.get("weekly_market_frequency", 1.0))
    
    category = business.get("category", "")
    typical_sales = float(business.get("typical_monthly_sales", 50000.0))
    
    # 1. Competitor Density & Saturation
    num_competitors = len(competitors_df) if competitors_df is not None else 0
    total_comp_sales = float(competitors_df["estimated_monthly_sales"].sum()) if num_competitors > 0 else 0.0
    avg_comp_rating = float(competitors_df["customer_rating"].mean()) if num_competitors > 0 else 3.5
    if np.isnan(avg_comp_rating):
        avg_comp_rating = 3.5

    # 2. Category Relevance Multiplier based on local ecosystem
    category_fit = 1.0
    if category in ["Dairy", "Poultry"]:
        category_fit = 0.6 + (livestock_dep / 100.0) * 0.7
    elif category in ["Food Processing", "Vegetable Processing"]:
        category_fit = 0.6 + (agri_dep / 100.0) * 0.7
    elif category in ["Retail / General Store", "Digital / Service Centre"]:
        # Benefits from higher population and purchasing power
        category_fit = 0.5 + (purchasing_power_idx / 100.0) * 0.4 + (population / 5000.0) * 0.3
    elif category in ["Tailoring", "Handicrafts"]:
        category_fit = 0.7 + (weekly_mkt_freq * 0.15)
    elif category in ["Mobile Repair", "Small Manufacturing"]:
        category_fit = 0.6 + (road_access / 100.0) * 0.5
    
    category_fit = max(0.5, min(1.4, category_fit))

    # 3. Estimated Customer Pool (5-10 km radius)
    # Rural cluster multiplier: Nearby hamlet catchment expands with market distance
    catchment_multiplier = 1.0 + (market_dist / 15.0)
    customer_pool = int(households * catchment_multiplier * 0.45 * category_fit)
    
    # 4. Market Demand Score (0-100)
    # Balances local demand index, purchasing power, and category ecosystem alignment
    demand_raw = (local_demand_idx * 0.45) + (purchasing_power_idx * 0.35) + (category_fit * 30.0 * 0.20)
    market_demand_score = round(max(10.0, min(100.0, demand_raw)), 1)
    
    # 5. Competition Score (0-100, HIGHER means more favorable / less saturated)
    if num_competitors == 0:
        competition_score = 90.0  # Blue ocean, but requires building demand
    elif num_competitors == 1:
        competition_score = 78.0  # Healthy room for alternate choice
    elif num_competitors == 2:
        competition_score = 64.0  # Moderate competition
    elif num_competitors == 3:
        competition_score = 50.0  # Saturated
    else:
        competition_score = max(20.0, 45.0 - (num_competitors - 3) * 8.0)
    
    # If competitors have low ratings, opportunity increases
    if num_competitors > 0 and avg_comp_rating < 4.0:
        competition_score += (4.0 - avg_comp_rating) * 8.0
    competition_score = round(max(10.0, min(100.0, competition_score)), 1)

    # 6. Accessibility Score (0-100)
    # Road access, public transit, proximity to mandi/town, and banking presence
    mandi_proximity_score = max(10.0, 100.0 - (market_dist * 3.5))
    accessibility_score = (
        (road_access * 0.35) +
        (transport_score * 0.25) +
        (bank_access * 0.25) +
        (mandi_proximity_score * 0.15)
    )
    accessibility_score = round(max(10.0, min(100.0, accessibility_score)), 1)

    # 7. Estimated Market Gap (₹ Monthly Unmet Demand)
    avg_spend_per_customer = (typical_sales / max(1, (households * 0.25))) * (purchasing_power_idx / 70.0)
    total_local_demand_rupees = customer_pool * avg_spend_per_customer * category_fit
    unmet_demand_rupees = max(0.0, total_local_demand_rupees - total_comp_sales)
    
    # 8. Local Opportunity Score (0-100)
    local_opp_raw = (market_demand_score * 0.40) + (competition_score * 0.35) + (accessibility_score * 0.25)
    local_opportunity_score = round(max(15.0, min(100.0, local_opp_raw)), 1)

    return {
        "market_demand_score": market_demand_score,
        "competition_score": competition_score,
        "accessibility_score": accessibility_score,
        "local_opportunity_score": local_opportunity_score,
        "customer_pool": customer_pool,
        "num_competitors": num_competitors,
        "avg_competitor_rating": round(avg_comp_rating, 2),
        "total_competitor_sales": total_comp_sales,
        "estimated_unmet_demand_rupees": round(unmet_demand_rupees, -2),
        "category_fit_multiplier": round(category_fit, 2)
    }

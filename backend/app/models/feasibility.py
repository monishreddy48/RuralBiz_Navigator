"""
Pydantic Schemas for Business Feasibility Assessment
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class FeasibilityRequest(BaseModel):
    user_name: Optional[str] = "Demo Entrepreneur"
    village_id: str = Field(..., description="Village identifier, e.g. VIL_001")
    category: str = Field(..., description="Business category, e.g. Food Processing")
    expected_investment: float = Field(..., ge=10000.0, le=10000000.0, description="Total project setup outlay in ₹")
    own_capital: float = Field(..., ge=0.0, le=10000000.0, description="Available entrepreneur equity in ₹")
    annual_interest_rate: Optional[float] = 9.5
    tenure_months: Optional[int] = 60
    moratorium_months: Optional[int] = 3
    monthly_sales: Optional[float] = None
    experience_level: str = Field(default="Intermediate (1-3 yrs)")
    is_existing: bool = Field(default=False)
    monthly_income: float = Field(default=30000.0, ge=0.0)
    risk_tolerance: str = Field(default="Moderate")

class ViabilityBreakdown(BaseModel):
    market_demand: float
    competition: float
    accessibility: float
    financial_fit: float
    growth_potential: float
    risk_resilience: float

class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class RecommendationResponse(BaseModel):
    decision: str
    verdict: Optional[str] = None
    decision_label: str
    decision_color: str
    reasons: List[str]
    evidence: str
    source: str
    confidence: str
    disclaimer: str
    swot: SWOTAnalysis

class FeasibilityResponse(BaseModel):
    assessment_id: Optional[str] = None
    viability_score: float
    composite_score: Optional[float] = None
    classification: str
    status_color: str
    status_badge: str
    breakdown: Dict[str, float]
    factor_scores: Optional[List[Dict[str, Any]]] = None
    recommendation: RecommendationResponse
    financial_summary: Dict[str, Any]
    hyperlocal_summary: Dict[str, Any]


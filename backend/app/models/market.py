"""
Pydantic Schemas for Market, Schemes, Simulator, Alternatives, and AI
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# --- Market Models ---
class CompetitorItem(BaseModel):
    competitor_id: str
    business_name: str
    business_type: str
    latitude: float
    longitude: float
    estimated_monthly_sales: float
    price_level: str
    customer_rating: float
    distance_from_center: float
    strength: Optional[str] = None
    weakness: Optional[str] = None

class LocalityItem(BaseModel):
    village_id: str
    village_name: str
    district: str
    state: str
    latitude: float
    longitude: float
    population: int
    households: int
    market_distance_km: float
    road_access_score: float
    public_transport_score: float
    bank_access_score: float
    purchasing_power_index: float
    local_demand_index: float

class CatchmentResponse(BaseModel):
    locality: LocalityItem
    business_category: str
    competitors: List[CompetitorItem]
    customer_pool: int
    market_demand_score: float
    competition_score: float
    accessibility_score: float
    estimated_unmet_demand_rupees: float
    opportunity_score: float

# --- Schemes Models ---
class SchemeMatchRequest(BaseModel):
    project_cost: float = Field(..., ge=10000.0)
    business_category: str
    target_group_tags: List[str] = Field(default_factory=lambda: ["General", "Rural"])
    is_existing: bool = False

class EligibilityCheck(BaseModel):
    criterion: str
    passed: bool
    detail: str

class SchemeMatchItem(BaseModel):
    scheme_id: str
    name: str
    description: str
    match_status: str # MATCHED, POSSIBLE, VERIFICATION REQUIRED
    status_color: str
    fit_reason: str
    loan_available: Optional[str] = None
    subsidy_available: Optional[str] = None
    estimated_subsidy_rupees: float = 0.0
    margin_requirement: Optional[str] = None
    interest_notes: Optional[str] = None
    collateral_notes: Optional[str] = None
    application_route: Optional[str] = None
    source_url: Optional[str] = None
    eligibility_checks: List[EligibilityCheck]
    documents: List[str]

# --- Simulator Models ---
class SimulatorRequest(BaseModel):
    village_id: str
    category: str
    project_cost: float
    own_capital: float
    sales_vol_delta_pct: float = Field(default=-20.0, ge=-50.0, le=50.0)
    price_delta_pct: float = Field(default=-5.0, ge=-30.0, le=30.0)
    var_cost_delta_pct: float = Field(default=15.0, ge=-20.0, le=50.0)
    fixed_cost_delta_pct: float = Field(default=10.0, ge=-20.0, le=50.0)
    interest_rate_delta: float = Field(default=1.5, ge=-3.0, le=5.0)
    loan_amount_delta_pct: float = Field(default=0.0, ge=-40.0, le=40.0)

class SimulatorResponse(BaseModel):
    survival_status: str
    survival_verdict: str
    survival_color: str
    base_case: Dict[str, Any]
    stress_case: Dict[str, Any]
    shocks_applied: Dict[str, float]

# --- Alternatives Models ---
class AlternativeItem(BaseModel):
    business_id: str
    business_name: str
    category: str
    project_cost: float
    own_capital_required: float
    loan_required: float
    monthly_net_profit: float
    dscr: float
    viability_score: float
    classification: str
    status_color: str
    market_demand_score: float
    competition_score: float
    financial_fit_score: float
    highlights: List[str]
    is_current: bool

# --- AI Models ---
class AIChatRequest(BaseModel):
    question: str
    language: str = "en"
    context: Optional[Dict[str, Any]] = None

class AIChatResponse(BaseModel):
    answer: str
    provider: str
    language: str


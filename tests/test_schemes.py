"""
Unit Tests for RuralBiz Navigator - Scheme Engine
Verifies rule-based routing, cost boundary checks, and category matching.
"""
import pytest
from core.scheme_engine import evaluate_schemes
from database.db import init_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Ensure database seed schemes are loaded."""
    init_db()

def test_scheme_mudra_shishu_boundary():
    """Project cost <= 50,000 must match PM MUDRA Shishu."""
    schemes = evaluate_schemes(project_cost=35000.0, business_category="Tailoring")
    shishu_matches = [s for s in schemes if "Shishu" in s["name"]]
    
    assert len(shishu_matches) > 0
    assert shishu_matches[0]["match_status"] == "MATCHED"

def test_scheme_pmegp_eligibility():
    """Rural Food Processing project of 2,15,000 must match PMEGP."""
    schemes = evaluate_schemes(
        project_cost=215000.0,
        business_category="Food Processing",
        target_group_tags=["General", "Rural"]
    )
    pmegp = [s for s in schemes if "PMEGP" in s["name"]][0]
    assert pmegp["match_status"] == "MATCHED"
    # General rural subsidy is 25%
    assert pmegp["estimated_subsidy_rupees"] == round(215000.0 * 0.25, 2)

def test_scheme_standup_india_constraints():
    """Stand-Up India requires Women or SC/ST entrepreneurs."""
    # General male applicant without women or SC/ST tag
    schemes_gen = evaluate_schemes(
        project_cost=1500000.0,
        business_category="Small Manufacturing",
        target_group_tags=["General", "Rural"]
    )
    standup_gen = [s for s in schemes_gen if "Stand-Up" in s["name"]][0]
    assert standup_gen["match_status"] != "MATCHED"

    # Women entrepreneur applicant
    schemes_women = evaluate_schemes(
        project_cost=1500000.0,
        business_category="Small Manufacturing",
        target_group_tags=["Women Entrepreneur", "Rural"]
    )
    standup_women = [s for s in schemes_women if "Stand-Up" in s["name"]][0]
    assert standup_women["match_status"] == "MATCHED"

def test_scheme_status_sorting():
    """Schemes must be sorted with MATCHED first, followed by POSSIBLE and NOT MATCHED."""
    schemes = evaluate_schemes(project_cost=100000.0, business_category="Dairy")
    statuses = [s["match_status"] for s in schemes]
    
    rank_map = {"MATCHED": 1, "POSSIBLE": 2, "VERIFICATION REQUIRED": 3, "NOT MATCHED": 4}
    ranks = [rank_map.get(st, 99) for st in statuses]
    assert ranks == sorted(ranks)

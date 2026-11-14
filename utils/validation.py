"""
RuralBiz Navigator - Input Validation Utilities
Validates entrepreneur inputs, capital requirements, and financial constraints safely.
"""
from typing import Dict, Any, List

def validate_assessment_inputs(
    own_capital: float,
    expected_investment: float,
    monthly_sales: float = 0.0,
    tenure_months: int = 60,
    interest_rate: float = 9.5
) -> List[str]:
    """
    Validates form fields and returns list of error messages (empty if valid).
    """
    errors = []
    
    if own_capital < 0:
        errors.append("Available own capital cannot be negative.")
        
    if expected_investment <= 0:
        errors.append("Expected total project cost must be greater than zero.")
        
    if own_capital > expected_investment:
        errors.append("Available own capital cannot exceed the total project cost. (Excess capital can be kept as emergency liquidity).")
        
    if tenure_months < 6 or tenure_months > 120:
        errors.append("Loan tenure must be between 6 months and 120 months (10 years).")
        
    if interest_rate < 0 or interest_rate > 35:
        errors.append("Annual interest rate must be between 0% and 35%.")
        
    return errors

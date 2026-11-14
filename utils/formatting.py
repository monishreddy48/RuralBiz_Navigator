"""
RuralBiz Navigator - Formatting Utilities
Indian Rupee currency formatting and number representations.
"""

def format_inr(amount: float, include_symbol: bool = True) -> str:
    """
    Formats a numeric amount into standard Indian Rupee notation (lakhs and crores).
    e.g., 250000 -> ₹2,50,000
          12500000 -> ₹1,25,00,000
    """
    if amount is None:
        return "₹0" if include_symbol else "0"
        
    prefix = "₹" if include_symbol else ""
    is_negative = amount < 0
    amount = abs(round(amount))
    
    s = str(int(amount))
    if len(s) <= 3:
        formatted = s
    else:
        # Last 3 digits
        last_three = s[-3:]
        remaining = s[:-3]
        # In Indian system, remaining digits are grouped by 2
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three

    res = f"{prefix}{formatted}"
    return f"-{res}" if is_negative else res

def format_pct(val: float, decimals: int = 1) -> str:
    """Format float into percentage string e.g., 24.5%"""
    if val is None:
        return "0.0%"
    return f"{val:.{decimals}f}%"

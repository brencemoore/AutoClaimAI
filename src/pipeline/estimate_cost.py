'''
Estimates the cost of car repairs based on detected damage and car details.
Will estimate labor, part, and total costs.
'''

import json
from pathlib import Path

# Labor rates by state ($/hour) - Source: autoleap.com

with open("./src/cost_data/labor_rates.json", "r") as f:
    LABOR_RATES = json.load(f)

# National average labor rate
NATIONAL_AVG_LABOR_RATE = LABOR_RATES.get("National_Average")  # $/hour

# Labor time estimates (hours) based on damage type and severity
# Format: {part: {severity: {damage_type: hours}}}

with open("./src/cost_data/labor_time_table.json", "r") as f:
    LABOR_TIME_TABLE = json.load(f)

# Part cost estimates ($) based on part type and severity
# Format: {part: {severity: base_cost}}

with open("./src/cost_data/part_cost_table.json", "r") as f:
    PART_COST_TABLE = json.load(f)

# Default values for unknown cases
DEFAULT_LABOR_HOURS = LABOR_TIME_TABLE.get("Default")
DEFAULT_PART_COST = PART_COST_TABLE.get("Default")


def get_labor_hours(part, severity, damage_type):
    """
    Get estimated labor hours for a specific repair.
    
    Args:
        part: Damaged car part (e.g., "Door", "Bumper")
        severity: Damage severity ("Minor", "Moderate", "Severe")
        damage_type: Type of damage (e.g., "dent", "scratch")
    
    Returns:
        Estimated labor hours (float)
    """
    # Normalize damage type to lowercase
    damage_type_lower = damage_type.lower()
    
    # Check if we have data for this combination
    if part in LABOR_TIME_TABLE:
        if severity in LABOR_TIME_TABLE[part]:
            # Try exact match first
            if damage_type_lower in LABOR_TIME_TABLE[part][severity]:
                return LABOR_TIME_TABLE[part][severity][damage_type_lower]
            # Default to "damage" if specific type not found
            elif "damage" in LABOR_TIME_TABLE[part][severity]:
                return LABOR_TIME_TABLE[part][severity]["damage"]
    
    # Return default if no match found
    return DEFAULT_LABOR_HOURS


def get_part_cost(part, severity):
    """
    Get estimated part cost for a specific repair.
    
    Args:
        part: Damaged car part
        severity: Damage severity
    
    Returns:
        Estimated part cost (float)
    """
    if part in PART_COST_TABLE and severity in PART_COST_TABLE[part]:
        return PART_COST_TABLE[part][severity]
    return DEFAULT_PART_COST


def calculate_labor_cost(labor_hours, state=None):
    """
    Calculate labor cost based on hours and state.
    
    Args:
        labor_hours: Number of labor hours
        state: State name (optional, uses national average if None)
    
    Returns:
        Labor cost (float)
    """
    labor_rate = LABOR_RATES.get(state, NATIONAL_AVG_LABOR_RATE)
    return labor_hours * labor_rate


def estimate_repair_cost(part, severity, damage_type, state=None):
    """
    Estimate total repair cost for a single damage.
    
    Args:
        part: Damaged car part
        severity: Damage severity
        damage_type: Type of damage
        state: State for labor rate (optional)
    
    Returns:
        Dictionary with cost breakdown
    """
    labor_hours = get_labor_hours(part, severity, damage_type)
    part_cost = get_part_cost(part, severity)
    labor_cost = calculate_labor_cost(labor_hours, state)
    total_cost = part_cost + labor_cost
    
    return {
        "part_cost": round(part_cost, 2),
        "labor_hours": round(labor_hours, 2),
        "labor_rate": LABOR_RATES.get(state, NATIONAL_AVG_LABOR_RATE),
        "labor_cost": round(labor_cost, 2),
        "estimated_cost": round(total_cost, 2)
    }


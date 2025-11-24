'''
Estimates the cost of car repairs based on detected damage and car details.
Will estimate labor, part, and total costs.
'''

import json
from pathlib import Path

# Labor rates by state ($/hour) - Source: autoleap.com
LABOR_RATES = {
    "Maine": 135, "New_Hampshire": 127.5, "Vermont": 122.5, "Massachusetts": 132.5,
    "Rhode_Island": 125, "Connecticut": 132.5, "New_York": 137.5, "New_Jersey": 142.5,
    "Pennsylvania": 137.5, "Ohio": 135, "Michigan": 140, "Indiana": 140,
    "Illinois": 132.5, "Wisconsin": 137.5, "Minnesota": 142.5, "Iowa": 137.5,
    "Missouri": 142.5, "North_Dakota": 137.5, "South_Dakota": 140, "Nebraska": 142.5,
    "Kansas": 142.5, "Delaware": 137.5, "Maryland": 140, "Virginia": 137.5,
    "West_Virginia": 142.5, "North_Carolina": 95, "South_Carolina": 137.5,
    "Georgia": 145, "Florida": 142.5, "Kentucky": 145, "Tennessee": 145,
    "Mississippi": 152.5, "Alabama": 145, "Oklahoma": 142.5, "Texas": 142.5,
    "Arkansas": 145, "Louisiana": 145, "Idaho": 137.5, "Montana": 145,
    "Wyoming": 152.5, "Nevada": 135, "Utah": 137.5, "Colorado": 142.5,
    "Arizona": 132.5, "New_Mexico": 140, "Alaska": 142.5, "Washington": 140,
    "Oregon": 135, "California": 165, "Hawaii": 130
}

# National average labor rate
NATIONAL_AVG_LABOR_RATE = 140  # $/hour

# Labor time estimates (hours) based on damage type and severity
# Format: {part: {severity: {damage_type: hours}}}
LABOR_TIME_TABLE = {
    "Door": {
        "Minor": {"dent": 1.5, "scratch": 1.0, "damage": 2.0},
        "Moderate": {"dent": 3.0, "scratch": 2.5, "damage": 4.0},
        "Severe": {"dent": 5.0, "scratch": 4.0, "damage": 8.0}
    },
    "Bumper": {
        "Minor": {"dent": 1.0, "scratch": 1.5, "damage": 2.0},
        "Moderate": {"dent": 2.5, "scratch": 2.0, "damage": 3.5},
        "Severe": {"dent": 4.0, "scratch": 3.5, "damage": 6.0}
    },
    "Hood": {
        "Minor": {"dent": 2.0, "scratch": 1.5, "damage": 2.5},
        "Moderate": {"dent": 3.5, "scratch": 3.0, "damage": 5.0},
        "Severe": {"dent": 6.0, "scratch": 5.0, "damage": 8.0}
    },
    "Window": {
        "Minor": {"crack": 0.5, "scratch": 0.5, "damage": 1.0},
        "Moderate": {"crack": 1.0, "scratch": 1.0, "damage": 1.5},
        "Severe": {"crack": 2.0, "scratch": 1.5, "damage": 2.5}
    },
    "Headlight": {
        "Minor": {"crack": 0.5, "scratch": 0.5, "damage": 1.0},
        "Moderate": {"crack": 1.0, "scratch": 0.75, "damage": 1.5},
        "Severe": {"crack": 1.5, "scratch": 1.0, "damage": 2.0}
    },
    "Mirror": {
        "Minor": {"crack": 0.5, "scratch": 0.5, "damage": 1.0},
        "Moderate": {"crack": 1.0, "scratch": 0.75, "damage": 1.5},
        "Severe": {"crack": 1.5, "scratch": 1.0, "damage": 2.5}
    },
    "Body/Unknown": {
        "Minor": {"dent": 2.0, "scratch": 1.5, "damage": 2.5},
        "Moderate": {"dent": 4.0, "scratch": 3.0, "damage": 5.0},
        "Severe": {"dent": 6.0, "scratch": 4.5, "damage": 8.0}
    },
    "Wind Shield": {
        "Minor": {"crack": 1.0, "scratch": 1.0, "damage": 1.5},
        "Moderate": {"crack": 2.0, "scratch": 1.5, "damage": 2.5},
        "Severe": {"crack": 3.0, "scratch": 2.0, "damage": 4.0}
    }
}

# Part cost estimates ($) based on part type and severity
# Format: {part: {severity: base_cost}}
PART_COST_TABLE = {
    "Door": {"Minor": 200, "Moderate": 500, "Severe": 1200},
    "Bumper": {"Minor": 150, "Moderate": 400, "Severe": 900},
    "Hood": {"Minor": 250, "Moderate": 600, "Severe": 1400},
    "Window": {"Minor": 100, "Moderate": 250, "Severe": 450},
    "Headlight": {"Minor": 150, "Moderate": 300, "Severe": 600},
    "Mirror": {"Minor": 100, "Moderate": 200, "Severe": 400},
    "Body/Unknown": {"Minor": 300, "Moderate": 700, "Severe": 1500},
    "Wind Shield": {"Minor": 200, "Moderate": 400, "Severe": 800}
}

# Default values for unknown cases
DEFAULT_LABOR_HOURS = 3.0
DEFAULT_PART_COST = 500


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


def save_cost_tables(output_path="src/data/cost_tables.json"):
    """
    Save the cost tables to a JSON file for reference or modification.
    
    Args:
        output_path: Path to save the JSON file
    """
    from pathlib import Path
    import os
    
    output_path = Path(output_path)
    os.makedirs(output_path.parent, exist_ok=True)
    
    cost_data = {
        "labor_rates": LABOR_RATES,
        "labor_time_table": LABOR_TIME_TABLE,
        "part_cost_table": PART_COST_TABLE,
        "defaults": {
            "labor_hours": DEFAULT_LABOR_HOURS,
            "part_cost": DEFAULT_PART_COST,
            "national_avg_labor_rate": NATIONAL_AVG_LABOR_RATE
        }
    }
    
    with open(output_path, "w") as f:
        json.dump(cost_data, f, indent=4)
    
    print(f"Cost tables saved to: {output_path.resolve()}")


# Example usage
if __name__ == "__main__":
    # Test the estimation
    test_cases = [
        ("Door", "Minor", "dent", "California"),
        ("Bumper", "Severe", "damage", "Texas"),
        ("Headlight", "Moderate", "crack", None),
    ]
    
    for part, severity, damage_type, state in test_cases:
        result = estimate_repair_cost(part, severity, damage_type, state)
        print(f"\n{part} - {severity} {damage_type} ({state or 'National Avg'}):")
        print(json.dumps(result, indent=2))
    
    # Save cost tables
    save_cost_tables()
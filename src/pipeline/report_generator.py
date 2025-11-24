'''
Generates a report of the estimated costs based off of aggregated data from the pipeline and user input.
'''

import json
from .detect_damage import classify_damage, damage_severity, classify_part
from .car_classification import classify_car
from .estimate_cost import estimate_repair_cost

def generate_report(image_path, car_year, state=None):
    """
    Generate a damage report for a single image.
    
    Args:
        image_path: Path to the image file
        car_year: Year of the vehicle
        state: State for labor rate calculation (optional)
    
    Returns:
        Dictionary containing the damage report
    """
    
    # Get vehicle information
    make, model = classify_car(image_path)
    
    # Get damage information
    damaged_part = classify_part(image_path)
    type_of_damage = classify_damage(image_path)
    damaged_severity = damage_severity(image_path)
    
    # Estimate costs based on detected damage
    cost_estimate = estimate_repair_cost(
        part=damaged_part,
        severity=damaged_severity,
        damage_type=type_of_damage,
        state=state
    )
    
    report = {
        "vehicle": {
            "make": make,
            "model": model,
            "year": car_year
        },
        "damaged_part": {
            "part": damaged_part,
            "type_of_damage": type_of_damage,
            "severity": damaged_severity,
            "part_cost": cost_estimate["part_cost"],
            "labor_hours": cost_estimate["labor_hours"],
            "labor_rate": cost_estimate["labor_rate"],
            "labor_cost": cost_estimate["labor_cost"],
            "estimated_cost": cost_estimate["estimated_cost"]
        }
    }
    return report


def aggregate_reports(reports):
    """
    Combine multiple reports into one aggregated report.
    
    Args:
        reports: List of individual damage reports
    
    Returns:
        Dictionary containing the aggregated report
    """
    
    if not reports:
        return {}

    # Take vehicle info from the first report
    vehicle_info = reports[0]["vehicle"]

    # Combine all damaged parts
    damaged_parts = []
    total_cost = 0
    total_part_cost = 0
    total_labor_cost = 0
    total_labor_hours = 0
    
    for report in reports:
        part_info = report.get("damaged_part", {})
        if part_info:
            damaged_parts.append(part_info)
            total_part_cost += part_info.get("part_cost", 0)
            total_labor_cost += part_info.get("labor_cost", 0)
            total_labor_hours += part_info.get("labor_hours", 0)
            total_cost += part_info.get("estimated_cost", 0)

    aggregated_report = {
        "vehicle": vehicle_info,
        "damaged_parts": damaged_parts,
        "summary": {
            "total_damages": len(damaged_parts),
            "total_part_cost": round(total_part_cost, 2),
            "total_labor_hours": round(total_labor_hours, 2),
            "total_labor_cost": round(total_labor_cost, 2),
            "total_estimated_cost": round(total_cost, 2)
        }
    }

    return aggregated_report


def save_report(report, output_dir="outputs"):
    """
    Save the aggregated report to a JSON file in the outputs folder.
    
    Args:
        report: The report dictionary to save
        output_dir: Directory to save the report (default: "outputs")
    """
    import os
    from pathlib import Path
    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / "report.json"

    # Creates a new report file if one already exists (does not overwrite)
    counter = 1    
    while output_path.exists():
        output_path = Path(f"{output_dir}/report({counter}).json")
        counter += 1

    # Save aggregated report to outputs folder
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"\nReport saved to:\n{output_path.resolve()}\n")
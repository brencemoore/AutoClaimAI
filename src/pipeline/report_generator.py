'''
Generates a report of the estimated costs based off of aggregated data from the pipeline and user input.
Includes shopping guide without requiring API keys.
'''

import json
import os
from pathlib import Path
from datetime import datetime
from .detect_damage import classify_damage, damage_severity, classify_part
from .car_classification import classify_car
from .estimate_cost import estimate_repair_cost

# Import shopping guide functionality
try:
    from .parts_shopping import create_shopping_guide
    SHOPPING_AVAILABLE = True
except ImportError:
    SHOPPING_AVAILABLE = False


def generate_report(image_path, car_year, state=None, include_shopping=True):
    """
    Generate a damage report for a single image.
    
    Args:
        image_path: Path to the image file
        car_year: Year of the vehicle
        state: State for labor rate calculation (optional)
        include_shopping: Whether to include shopping guide info
    
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
    
    # Add shopping guide if requested and available
    if include_shopping and SHOPPING_AVAILABLE:
        shopping_guide = create_shopping_guide(
            part=damaged_part,
            estimated_cost=cost_estimate["part_cost"],
            labor_cost=cost_estimate["labor_cost"],
            year=car_year,
            make=make,
            model=model
        )
        report["shopping_guide"] = shopping_guide
    
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
    shopping_guides = []
    
    for report in reports:
        part_info = report.get("damaged_part", {})
        if part_info:
            damaged_parts.append(part_info)
            total_part_cost += part_info.get("part_cost", 0)
            total_labor_cost += part_info.get("labor_cost", 0)
            total_labor_hours += part_info.get("labor_hours", 0)
            total_cost += part_info.get("estimated_cost", 0)
        
        # Collect shopping guides
        if "shopping_guide" in report:
            shopping_guides.append(report["shopping_guide"])

    aggregated_report = {
        "vehicle": vehicle_info,
        "timestamp": datetime.now().isoformat(),
        "damaged_parts": damaged_parts,
        "summary": {
            "total_damages": len(damaged_parts),
            "total_part_cost": round(total_part_cost, 2),
            "total_labor_hours": round(total_labor_hours, 2),
            "total_labor_cost": round(total_labor_cost, 2),
            "total_estimated_cost": round(total_cost, 2)
        }
    }
    
    # Add shopping guides if available
    if shopping_guides:
        aggregated_report["shopping_guides"] = shopping_guides

    return aggregated_report


def save_report(report, output_dir="outputs"):
    """
    Save the aggregated report to a JSON file in the outputs folder.
    
    Args:
        report: The report dictionary to save
        output_dir: Directory to save the report (default: "outputs")
    """
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

    print(f"\nReport saved to: {output_path.resolve()}")
    return output_path


def save_parts_report(aggregated_report, output_dir="outputs"):
    """
    Save parts-only report to separate JSON file.
    
    Args:
        aggregated_report: The aggregated report dictionary
        output_dir: Directory to save the report (default: "outputs")
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    parts_report = {
        "vehicle": aggregated_report["vehicle"],
        "timestamp": aggregated_report.get("timestamp", datetime.now().isoformat()),
        "parts_summary": {
            "total_damages": aggregated_report["summary"]["total_damages"],
            "total_part_cost": aggregated_report["summary"]["total_part_cost"]
        },
        "damaged_parts": [
            {
                "part": part["part"],
                "type_of_damage": part["type_of_damage"],
                "severity": part["severity"],
                "part_cost": part["part_cost"]
            }
            for part in aggregated_report["damaged_parts"]
        ]
    }
    
    # Include shopping guides if available
    if "shopping_guides" in aggregated_report:
        parts_report["shopping_guides"] = aggregated_report["shopping_guides"]
    
    output_path = Path(output_dir) / "parts_report.json"
    
    # Creates a new report file if one already exists (does not overwrite)
    counter = 1
    while output_path.exists():
        output_path = Path(f"{output_dir}/parts_report({counter}).json")
        counter += 1
    
    with open(output_path, 'w') as f:
        json.dump(parts_report, f, indent=4)
    
    print(f"Parts report saved: {output_path.resolve()}")
    return output_path


def save_labor_report(aggregated_report, output_dir="outputs"):
    """
    Save labor-only report to separate JSON file.
    
    Args:
        aggregated_report: The aggregated report dictionary
        output_dir: Directory to save the report (default: "outputs")
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    labor_report = {
        "vehicle": aggregated_report["vehicle"],
        "timestamp": aggregated_report.get("timestamp", datetime.now().isoformat()),
        "labor_summary": {
            "total_damages": aggregated_report["summary"]["total_damages"],
            "total_labor_hours": aggregated_report["summary"]["total_labor_hours"],
            "total_labor_cost": aggregated_report["summary"]["total_labor_cost"],
            "labor_rate": aggregated_report["damaged_parts"][0].get("labor_rate", "N/A") if aggregated_report["damaged_parts"] else "N/A"
        },
        "labor_details": [
            {
                "part": part["part"],
                "type_of_damage": part["type_of_damage"],
                "severity": part["severity"],
                "labor_hours": part["labor_hours"],
                "labor_rate": part.get("labor_rate", "N/A"),
                "labor_cost": part["labor_cost"]
            }
            for part in aggregated_report["damaged_parts"]
        ]
    }
    
    output_path = Path(output_dir) / "labor_report.json"
    
    # Creates a new report file if one already exists (does not overwrite)
    counter = 1
    while output_path.exists():
        output_path = Path(f"{output_dir}/labor_report({counter}).json")
        counter += 1
    
    with open(output_path, 'w') as f:
        json.dump(labor_report, f, indent=4)
    
    print(f"Labor report saved: {output_path.resolve()}")
    return output_path


def save_shopping_guide_text(report, output_dir="outputs"):
    """
    Save a human-readable shopping guide text file.
    
    Args:
        report: The aggregated report with shopping guides
        output_dir: Directory to save the guide
    """
    if not SHOPPING_AVAILABLE or "shopping_guides" not in report:
        return None
    
    from .parts_shopping import save_shopping_guide
    
    output_path = save_shopping_guide(
        shopping_guides=report["shopping_guides"],
        vehicle_info=report["vehicle"],
        total_estimates=report["summary"],
        output_dir=output_dir
    )
    
    return output_path
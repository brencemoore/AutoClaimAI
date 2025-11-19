# Generates a report of the estimated costs based off of aggregated data from pipeline and user input.

import json
from .detect_damage import classify_damage, damage_severity, classify_part
from .car_classification import classify_car

def generate_report(image_path):
    
    # Placeholder data. Will be replaced with actual model inference and data extraction.
    make, model = classify_car(image_path)
    damaged_part = classify_part(image_path)
    type_of_damage = classify_damage(image_path)
    damaged_severity = damage_severity(image_path)
    part_cost = 1200
    labor_cost = 300
    estimated_cost = part_cost + labor_cost
    
    report = {
        "vehicle":
        {
            "make": make,
            "model": model,
            "year": 2020
        },
        "damaged_part":
        {
            "part": damaged_part,
            "type_of_damage": type_of_damage,
            "severity": damaged_severity,
            "part_cost": part_cost,
            "labor_cost": labor_cost,
            "estimated_cost": estimated_cost
        }
    }
    return report


# Combine multiple reports into one aggregated report.
def aggregate_reports(reports):
    
    if not reports:
        return {}

    # Take vehicle info from the first report
    vehicle_info = reports[0]["vehicle"]

    # Combine all damaged parts
    damaged_parts = []
    total_cost = 0
    total_part_cost = 0
    total_labor_cost = 0
    for report in reports:
        part_info = report.get("damaged_part", {})
        if part_info:
            damaged_parts.append(part_info)
            total_part_cost += part_info.get("part_cost", 0)
            total_labor_cost += part_info.get("labor_cost", 0)
            total_cost += part_info.get("estimated_cost", 0)

    aggregated_report = {
        "vehicle": vehicle_info,
        "damaged_part": damaged_parts,
        "total_part_cost": total_part_cost,
        "total_labor_cost": total_labor_cost,
        "total_estimated_cost": total_cost
    }

    return aggregated_report


# Save the aggregated report to a JSON file in the outputs folder.
def save_report(report, output_dir="outputs"):
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
    

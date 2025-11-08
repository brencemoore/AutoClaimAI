# Generates a report of the estimated costs based off of aggregated data from pipeline and user input.

import json

def generate_report(image_path):
    
    # Placeholder data. Will be replaced with actual model inference and data extraction.
    make, model = "Toyota", "Camry"
    damaged_part = "front bumper"
    damaged_severities = "moderate"
    estimated_cost = 1200
    
    report = {
        "vehicle":
        {
            "make": make,
            "model": model,
            "year": 2020
        },
        "damaged_parts":
        {
            "part": damaged_part,
            "severity": damaged_severities,
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
    for report in reports:
        part_info = report.get("damaged_parts", {})
        if part_info:
            damaged_parts.append(part_info)
            total_cost += part_info.get("estimated_cost", 0)

    aggregated_report = {
        "vehicle": vehicle_info,
        "damaged_parts": damaged_parts,
        "total_estimated_cost": total_cost
    }

    return aggregated_report

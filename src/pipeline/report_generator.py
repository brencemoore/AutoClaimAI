# Generates a report of the estimated costs based off of aggregated data from pipeline and user input.

import json

def generate_report(image_path):
    
    make, model = "Toyota", "Camry"  # Placeholder values for vehicle make and model
    damaged_parts = ["front bumper", "left headlight"]  # Placeholder for damaged parts
    damaged_severities = {"front bumper": "moderate", "left headlight": "severe"}  # Placeholder severities
    estimated_costs = {"front bumper": 1200, "left headlight": 800}  # Placeholder costs
    
    report = {
        "vehicle": {
            "make": make,
            "model": model,
            "year": 2020
        },
        "damaged_parts":
            [
                {
                    "part": part,
                    "severity": damaged_severities[part],
                    "estimated_cost": estimated_costs[part]
                } for part in damaged_parts
            ],
            
        "total_estimated_cost": sum(estimated_costs.values()),
    }
    
    return report
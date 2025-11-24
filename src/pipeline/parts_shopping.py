'''
Generates shopping guide for car parts without requiring API keys.
Uses estimated costs and provides links to online retailers for users to check prices.
'''

import json
from typing import Dict, List

# Popular online auto parts retailers
PARTS_RETAILERS = {
    "RockAuto": {
        "url": "https://www.rockauto.com",
        "search_url": "https://www.rockauto.com/en/catalog/{year},{make},{model}",
        "pros": ["Huge selection", "Competitive prices", "Parts diagrams"],
        "cons": ["Shipping can be expensive", "Multiple warehouses"],
        "quality_tiers": ["Economy", "Daily Driver", "Premium"]
    },
    "PartsGeek": {
        "url": "https://www.partsgeek.com",
        "search_url": "https://www.partsgeek.com/catalog/{year}/{make}/{model}",
        "pros": ["Free shipping over $99", "Good customer service", "Fast shipping"],
        "cons": ["Limited premium brands"],
        "quality_tiers": ["Value", "Standard", "Premium"]
    },
    "AutoZone": {
        "url": "https://www.autozone.com",
        "search_url": "https://www.autozone.com/parts/{year}/{make}/{model}",
        "pros": ["Local pickup available", "Rewards program", "In-store support"],
        "cons": ["Higher prices", "Limited body parts"],
        "quality_tiers": ["Economy", "Standard"]
    },
    "CarParts.com": {
        "url": "https://www.carparts.com",
        "search_url": "https://www.carparts.com/{year}-{make}-{model}",
        "pros": ["90-day returns", "Good warranties", "Fast shipping"],
        "cons": ["Limited selection on older cars"],
        "quality_tiers": ["Standard", "Premium"]
    },
    "1A Auto": {
        "url": "https://www.1aauto.com",
        "search_url": "https://www.1aauto.com/{year}-{make}-{model}",
        "pros": ["Video installation guides", "Good quality", "Detailed fitment"],
        "cons": ["Slightly higher prices"],
        "quality_tiers": ["Standard", "Premium"]
    }
}

# Part name mapping for better search results
PART_SEARCH_TERMS = {
    "Door": ["door shell", "door panel", "door skin"],
    "Bumper": ["bumper cover", "front bumper", "rear bumper"],
    "Hood": ["hood panel", "hood assembly"],
    "Window": ["door glass", "window regulator", "side window"],
    "Headlight": ["headlight assembly", "headlamp", "head light"],
    "Mirror": ["side mirror", "door mirror", "mirror assembly"],
    "Body/Unknown": ["body panel", "fender", "quarter panel"],
    "Wind Shield": ["windshield", "front glass", "windscreen"]
}


def generate_shopping_options(part: str, estimated_cost: float) -> List[Dict]:
    """
    Generate shopping options for a car part without API.
    
    Args:
        part: Name of the damaged part
        estimated_cost: Base estimated cost from our tables
    
    Returns:
        List of shopping options with price ranges
    """
    options = []
    
    # OEM (Original Equipment Manufacturer) - Highest Quality
    options.append({
        "type": "OEM (Original Equipment)",
        "quality": "Highest",
        "price_range": {
            "min": round(estimated_cost * 1.1, 2),
            "max": round(estimated_cost * 1.5, 2),
            "estimated": round(estimated_cost * 1.3, 2)
        },
        "warranty": "Manufacturer warranty (typically 12+ months)",
        "source": "Dealership or authorized OEM suppliers",
        "pros": [
            "Perfect fit guaranteed",
            "Highest quality materials",
            "Best warranty coverage",
            "Maintains vehicle value"
        ],
        "cons": [
            "Most expensive option",
            "May require ordering",
            "Longer wait time"
        ],
        "best_for": "New vehicles (less than 5 years old), leased vehicles, maintaining resale value"
    })
    
    # OEM Equivalent / Certified Aftermarket - Good Quality
    options.append({
        "type": "OEM Equivalent (Certified Aftermarket)",
        "quality": "High",
        "price_range": {
            "min": round(estimated_cost * 0.8, 2),
            "max": round(estimated_cost * 1.1, 2),
            "estimated": estimated_cost
        },
        "warranty": "1-2 year warranty",
        "source": "Certified aftermarket brands (CAPA certified)",
        "pros": [
            "Good quality at reasonable price",
            "CAPA certified for fitment",
            "Solid warranty coverage",
            "Best value for most repairs"
        ],
        "cons": [
            "Not OEM brand",
            "Minor fit variations possible"
        ],
        "best_for": "Most repairs - best balance of quality and price"
    })
    
    # Aftermarket Standard - Economy Option
    options.append({
        "type": "Aftermarket Standard",
        "quality": "Standard",
        "price_range": {
            "min": round(estimated_cost * 0.5, 2),
            "max": round(estimated_cost * 0.8, 2),
            "estimated": round(estimated_cost * 0.65, 2)
        },
        "warranty": "90 days - 1 year limited warranty",
        "source": "Budget aftermarket suppliers",
        "pros": [
            "Most affordable option",
            "Usually in stock",
            "Good for older vehicles"
        ],
        "cons": [
            "Lower quality materials",
            "Fit may not be perfect",
            "Shorter warranty",
            "May need adjustment"
        ],
        "best_for": "Older vehicles (10+ years), budget-conscious repairs, high-mileage cars"
    })
    
    # Used / Salvage - Lowest Cost
    if part in ["Door", "Hood", "Bumper", "Mirror"]:  # Parts commonly available used
        options.append({
            "type": "Used / Salvage Yard",
            "quality": "Variable",
            "price_range": {
                "min": round(estimated_cost * 0.2, 2),
                "max": round(estimated_cost * 0.4, 2),
                "estimated": round(estimated_cost * 0.3, 2)
            },
            "warranty": "Limited or no warranty (as-is)",
            "source": "Auto salvage yards, Pull-A-Part, LKQ",
            "pros": [
                "Lowest cost option",
                "OEM parts at fraction of cost",
                "Environmentally friendly"
            ],
            "cons": [
                "Condition varies",
                "No warranty typically",
                "May need painting/refinishing",
                "Limited availability"
            ],
            "best_for": "Older vehicles, tight budgets, mechanically sound parts"
        })
    
    return options


def generate_retailer_links(part: str, year: str, make: str, model: str) -> List[Dict]:
    """
    Generate links to online retailers for price checking.
    
    Args:
        part: Damaged part name
        year: Vehicle year
        make: Vehicle make
        model: Vehicle model
    
    Returns:
        List of retailer information with search URLs
    """
    retailer_links = []
    
    # Get search terms for this part
    search_terms = PART_SEARCH_TERMS.get(part, [part.lower()])
    
    for name, info in PARTS_RETAILERS.items():
        # Format the search URL with vehicle info
        url = info["search_url"].format(
            year=year.lower(),
            make=make.lower().replace(" ", "-"),
            model=model.lower().replace(" ", "-")
        )
        
        retailer_links.append({
            "name": name,
            "url": url,
            "search_terms": search_terms,
            "pros": info["pros"],
            "cons": info["cons"],
            "quality_tiers": info["quality_tiers"]
        })
    
    return retailer_links


def create_shopping_guide(part: str, estimated_cost: float, labor_cost: float,
                         year: str, make: str, model: str) -> Dict:
    """
    Create a complete shopping guide for a damaged part.
    
    Args:
        part: Damaged part name
        estimated_cost: Estimated part cost
        labor_cost: Estimated labor cost
        year: Vehicle year
        make: Vehicle make
        model: Vehicle model
    
    Returns:
        Dictionary with shopping guide information
    """
    return {
        "part": part,
        "vehicle": f"{year} {make} {model}",
        "cost_breakdown": {
            "estimated_part_cost": estimated_cost,
            "estimated_labor_cost": labor_cost,
            "estimated_total": estimated_cost + labor_cost
        },
        "shopping_options": generate_shopping_options(part, estimated_cost),
        "where_to_buy": generate_retailer_links(part, year, make, model),
        "tips": [
            "Always verify part fitment before purchasing",
            "Compare prices across multiple retailers",
            "Check shipping costs - they can add up",
            "Consider warranty coverage for your needs",
            "Read customer reviews when available",
            "OEM parts are best for newer vehicles",
            "Aftermarket parts can save money on older cars",
            "Used parts require inspection but can save 60-80%"
        ]
    }


def format_shopping_report(shopping_guides: List[Dict], vehicle_info: Dict, 
                          total_estimates: Dict) -> str:
    """
    Format a human-readable shopping report.
    
    Args:
        shopping_guides: List of shopping guides for each part
        vehicle_info: Dictionary with year, make, model
        total_estimates: Dictionary with total cost breakdowns
    
    Returns:
        Formatted string report
    """
    lines = []
    lines.append("=" * 80)
    lines.append(" " * 25 + "AUTO PARTS SHOPPING GUIDE")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Vehicle: {vehicle_info['year']} {vehicle_info['make']} {vehicle_info['model']}")
    lines.append("")
    lines.append("COST SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Parts Cost:  ${total_estimates['total_part_cost']:.2f}")
    lines.append(f"Total Labor Cost:  ${total_estimates['total_labor_cost']:.2f}")
    lines.append(f"TOTAL ESTIMATE:    ${total_estimates['total_estimated_cost']:.2f}")
    lines.append("")
    
    for i, guide in enumerate(shopping_guides, 1):
        lines.append("=" * 80)
        lines.append(f"PART {i}: {guide['part']}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Estimated Cost: ${guide['cost_breakdown']['estimated_part_cost']:.2f} "
                    f"(Labor: ${guide['cost_breakdown']['estimated_labor_cost']:.2f})")
        lines.append("")
        
        # Shopping Options
        lines.append("SHOPPING OPTIONS:")
        lines.append("-" * 80)
        lines.append("")
        
        for j, option in enumerate(guide['shopping_options'], 1):
            lines.append(f"{j}. {option['type']}")
            lines.append(f"   Quality Level: {option['quality']}")
            
            price_range = option['price_range']
            lines.append(f"   Price Range: ${price_range['min']:.2f} - ${price_range['max']:.2f}")
            lines.append(f"   Estimated: ${price_range['estimated']:.2f}")
            lines.append(f"   Warranty: {option['warranty']}")
            lines.append(f"   Source: {option['source']}")
            lines.append(f"   ")
            lines.append(f"   ✓ Pros: {', '.join(option['pros'])}")
            lines.append(f"   ✗ Cons: {', '.join(option['cons'])}")
            lines.append(f"   ")
            lines.append(f"   💡 Best For: {option['best_for']}")
            lines.append("")
        
        # Where to Buy
        lines.append("WHERE TO SHOP ONLINE:")
        lines.append("-" * 80)
        lines.append("")
        
        for retailer in guide['where_to_buy']:
            lines.append(f"🔗 {retailer['name']}")
            lines.append(f"   {retailer['url']}")
            lines.append(f"   Search for: {', '.join(retailer['search_terms'])}")
            lines.append(f"   Quality tiers: {', '.join(retailer['quality_tiers'])}")
            lines.append("")
        
        lines.append("")
    
    # General Tips
    lines.append("=" * 80)
    lines.append("SHOPPING TIPS")
    lines.append("=" * 80)
    lines.append("")
    for tip in shopping_guides[0]['tips']:  # Tips are the same for all
        lines.append(f"• {tip}")
    lines.append("")
    
    # Paint Note
    lines.append("=" * 80)
    lines.append("IMPORTANT NOTES")
    lines.append("=" * 80)
    lines.append("")
    lines.append("🎨 PAINTING: Most body parts require professional painting after installation.")
    lines.append("   Paint costs typically range from $200-$500 per panel depending on:")
    lines.append("   - Single stage vs. multi-stage paint")
    lines.append("   - Color matching complexity")
    lines.append("   - Clear coat and finish quality")
    lines.append("")
    lines.append("🔧 INSTALLATION: Labor costs vary by shop and location.")
    lines.append("   Consider getting quotes from multiple repair shops.")
    lines.append("")
    lines.append("📋 INSURANCE: If filing a claim, check with your insurance about:")
    lines.append("   - Approved repair shops")
    lines.append("   - OEM vs aftermarket parts requirements")
    lines.append("   - Your deductible and coverage limits")
    lines.append("")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def save_shopping_guide(shopping_guides: List[Dict], vehicle_info: Dict,
                       total_estimates: Dict, output_dir: str = "outputs"):
    """
    Save shopping guide to a text file.
    
    Args:
        shopping_guides: List of shopping guides
        vehicle_info: Vehicle information
        total_estimates: Total cost estimates
        output_dir: Output directory
    """
    import os
    from pathlib import Path
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / "shopping_guide.txt"
    
    # Create numbered file if exists
    counter = 1
    while output_path.exists():
        output_path = Path(f"{output_dir}/shopping_guide({counter}).txt")
        counter += 1
    
    report = format_shopping_report(shopping_guides, vehicle_info, total_estimates)
    
    with open(output_path, "w") as f:
        f.write(report)
    
    print(f"\n💡 Shopping guide saved to: {output_path.resolve()}")
    return output_path


# Example usage
if __name__ == "__main__":
    # Example: Create shopping guide for a bumper
    guide = create_shopping_guide(
        part="Bumper",
        estimated_cost=400.0,
        labor_cost=350.0,
        year="2020",
        make="Honda",
        model="Accord"
    )
    
    print(json.dumps(guide, indent=2))
    
    # Save to file
    vehicle = {"year": "2020", "make": "Honda", "model": "Accord"}
    totals = {
        "total_part_cost": 400.0,
        "total_labor_cost": 350.0,
        "total_estimated_cost": 750.0
    }
    
    save_shopping_guide([guide], vehicle, totals)
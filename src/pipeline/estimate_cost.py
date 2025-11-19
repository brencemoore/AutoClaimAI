'''
Estimates the cost of car repairs based on detected damage and car details.
Will estimate labor, part, and total costs.
'''

# NOT DONE | NOT DONE | NOT DONE | NOT DONE | NOT DONE
# NOT DONE | NOT DONE | NOT DONE | NOT DONE | NOT DONE
# NOT DONE | NOT DONE | NOT DONE | NOT DONE | NOT DONE
# NOT DONE | NOT DONE | NOT DONE | NOT DONE | NOT DONE

# Will be a function to be called from report_generator.py

import json

# Flat rate gathered from "https://autoleap.com/blog/average-automotive-repair-labor-rates-by-state/", gathered 15 November 2025
# May not be relevant and may be better to generalize and not consider state.
flat_rate_by_state = {
    {"Maine": 135},
    {"New_Hampshire": 127.5},
    {"Vermont": 122.5},
    {"Massachusetts": 132.5},
    {"Rhode_Island": 125},
    {"Connecticut": 132.5},
    {"New_York": 137.5},
    {"New_Jersey": 142.5},
    {"Pennsylvania": 137.5},
    {"Ohio": 135},
    {"Michigan": 140},
    {"Indiana": 140},
    {"Illinois": 132.5},
    {"Wisconsin": 137.5},
    {"Minnesota": 142.5},
    {"Iowa": 137.5},
    {"Missouri": 142.5},
    {"North_Dakota": 137.5},
    {"South_Dakota": 140},
    {"Nebraska": 142.5},
    {"Kansas": 142.5},
    {"Delaware": 137.5},
    {"Maryland": 140},
    {"Virginia": 137.5},
    {"West_Virginia": 142.5},
    {"North_Carolina": 95},
    {"South_Carolina": 137.5},
    {"Georgia": 145},
    {"Florida": 142.5},
    {"Kentucky": 145},
    {"Tennessee": 145},
    {"Mississippi": 152.5},
    {"Alabama": 145},
    {"Oklahoma": 142.5},
    {"Texas": 142.5},
    {"Arkansas": 145},
    {"Louisiana": 145},
    {"Idaho": 137.5},
    {"Montana": 145},
    {"Wyoming": 152.5},
    {"Nevada": 135},
    {"Utah": 137.5},
    {"Colorado": 142.5},
    {"Arizona": 132.5},
    {"New_Mexico": 140},
    {"Alaska": 142.5},
    {"Washington": 140},
    {"Oregon": 135},
    {"California": 165},
    {"Hawaii": 130}
}


# Service Type	Avg. Repair Time (Hours)	Avg. Hourly Rate (U.S.)	Avg. Hourly Rate (Chicago)	Estimated Labor Cost (U.S.)	Estimated Labor Cost (Chicago)
# Small Dent Repair	1 – 1.5	$90	$110	$90 – $135	$110 – $165
# Bumper Repair or Replacement	2 – 3	$95	$125	$190 – $285	$250 – $375
# Full Repaint (per panel)	3 – 4	$100	$140	$300 – $400	$420 – $560
# Collision Frame Straightening	4 – 6	$105	$145	$420 – $630	$580 – $870
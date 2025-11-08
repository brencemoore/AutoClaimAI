# main file, runs report generator
import os
import sys
import json
from pathlib import Path
from pipeline.report_generator import generate_report
from pipeline.report_generator import aggregate_reports

def main():
    os.makedirs("outputs", exist_ok=True)
    
    # Determine folder path based off of number of user arguments
    # Default to "input" folder if no arguments provided
    if len(sys.argv) == 1:
        folder_path = Path(__file__).resolve().parent.parent / "input"
        
    # Check for correct number of arguments 
    elif len(sys.argv) != 2:
        print("Usage: python main.py /path/to/image_folder")
        return

    # Uses User provided folder path
    else:
        folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    # Creates an array of images from the selected input folder
    supported_ext = (".jpg", ".jpeg", ".png", ".bmp")
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
              if f.lower().endswith(supported_ext)]

    if not images:
        print("No image files found.")
        return

    # Generate and print aggregated report from each image   
    aggregated_report = aggregate_reports([generate_report(img) for img in images])
    
    
    print(f"\nAggregated Report:\n")
    print(json.dumps(aggregated_report, indent=4))
    
    # Save aggregated report to outputs folder
    output_path = Path("outputs/aggregated_report.json")
    with open(output_path, "w") as f:
        json.dump(aggregated_report, f, indent=4)
    
if __name__ == "__main__":
    main()
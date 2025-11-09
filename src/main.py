# main file, runs report generator
import os
import sys
import json
from pathlib import Path
import pipeline.report_generator as report_gen

def main():    
    # Determine folder path based off of number of user arguments
    # Default to "input" folder if no arguments provided
    if len(sys.argv) == 1:
        input_path = Path(__file__).resolve().parent.parent / "input"
        print(f"\nIf you wish to select a specific input folder, please provide the folder path as a command line argument when running the program.\n")
        
    # Check for correct number of arguments 
    elif len(sys.argv) != 2:
        print("Usage: python main.py /path/to/image_folder")
        return

    # Uses User provided folder path
    else:
        input_path = sys.argv[1]

    if not os.path.isdir(input_path):
        print("Invalid folder path.")
        return

    # Creates an array of images from the selected input folder
    supported_ext = (".jpg", ".jpeg", ".png", ".bmp")
    images = [os.path.join(input_path, f) for f in os.listdir(input_path) 
              if f.lower().endswith(supported_ext)]

    if not images:
        print("No image files found.")
        return

    # Generate and print aggregated report from each image
    aggregated_report = report_gen.aggregate_reports([report_gen.generate_report(img) for img in images])

    # Print aggregated report to console
    print(f"Aggregated Report:")
    print(json.dumps(aggregated_report, indent=4))
    
    # Save aggregated report to outputs folder
    report_gen.save_report(aggregated_report)
    

if __name__ == "__main__":
    main()
    

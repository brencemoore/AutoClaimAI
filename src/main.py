# main file, runs report generator
import os
import sys
import json
from pathlib import Path
from pipeline.report_generator import generate_report

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

    # Generate and print report for each image
    for img in images:
        report = generate_report(img)
        print(f"\n=== REPORT FOR ===\n")
        print(f"Image path: {img}\n")
        print(json.dumps(report, indent=2, sort_keys=False))
        
        # Save report to outputs folder
        img_name = os.path.splitext(os.path.basename(img))[0]
        output_path = Path("outputs") / f"{img_name}_report.json"
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
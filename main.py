'''
Main file to run the AutoClaimAI pipeline. Runs report_generator.py to generate a report based off
of all images in a given input folder.

Includes shopping guide feature without requiring API keys.
'''

import os
import sys
from pathlib import Path
import src.pipeline.report_generator as report_gen

def print_banner():
    """Print a nice banner for the application"""
    print("\n" + "="*70)
    print(" "*20 + "AUTO CLAIM AI")
    print(" "*15 + "Vehicle Damage Assessment")
    print("="*70 + "\n")

def get_user_input():
    """Get user input for vehicle details and options"""
    print("VEHICLE INFORMATION")
    print("-" * 70)
    
    car_year = input("Enter the year of your vehicle: ").strip()
    while not car_year.isdigit() or len(car_year) != 4:
        print("Please enter a valid 4-digit year (e.g., 2020)")
        car_year = input("Enter the year of your vehicle: ").strip()
    
    state = input("Enter your state (or press Enter for national average): ").strip()
    if state:
        state = state.replace(" ", "_")
    else:
        state = None
    
    # Ask about shopping guide
    print("\nREPORT OPTIONS")
    print("-" * 70)
    print("Would you like to include a parts shopping guide?")
    print("This will provide price ranges and links to online retailers.")
    
    include_shopping = input("Include shopping guide? (Y/n): ").strip().lower()
    include_shopping = include_shopping != 'n'  # Default to yes unless they say no
    
    return car_year, state, include_shopping

def main():    
    print_banner()
    
    # Determine folder path based off of number of user arguments
    if len(sys.argv) == 1:
        input_path = Path(__file__).resolve().parent / "input"
        print(f"Using default input folder: {input_path}")
        print(f"Tip: Run 'python main.py /path/to/folder' to use a different folder\n")
        
    elif len(sys.argv) > 2:
        print("Usage: python main.py [/path/to/image_folder]")
        return
    else:
        input_path = sys.argv[1]

    if not os.path.isdir(input_path):
        print(f"Error: Invalid folder path: {input_path}")
        return

    # Find images
    supported_ext = (".jpg", ".jpeg", ".png", ".bmp")
    images = [os.path.join(input_path, f) for f in os.listdir(input_path) 
              if f.lower().endswith(supported_ext)]

    if not images:
        print(f"Error: No image files found in {input_path}")
        print(f"Supported formats: {', '.join(supported_ext)}")
        return

    print(f"Found {len(images)} image(s) to process\n")
    
    # Get user input
    car_year, state, include_shopping = get_user_input()
    
    print(f"\n{'='*70}")
    print("PROCESSING IMAGES")
    print("="*70 + "\n")

    # Generate reports for each image
    reports = []
    for i, img in enumerate(images, 1):
        print(f"[{i}/{len(images)}] Processing: {os.path.basename(img)}")
        try:
            report = report_gen.generate_report(img, car_year, state, include_shopping)
            reports.append(report)
            print(f"Complete - {report['damaged_part']['part']} ({report['damaged_part']['severity']})")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    if not reports:
        print("\nNo reports generated successfully.")
        return

    # Generate aggregated report
    print(f"\n{'='*70}")
    print("GENERATING REPORT")
    print("="*70 + "\n")
    
    aggregated_report = report_gen.aggregate_reports(reports)

    # Print summary to console
    report_gen.print_report_summary(aggregated_report)
    
    # Save reports
    print(f"\n{'='*70}")
    print("SAVING REPORTS")
    print("="*70 + "\n")
    
    # Save complete report (original)
    json_output = report_gen.save_report(aggregated_report)
    
    # Save separate parts and labor reports
    parts_output = report_gen.save_parts_report(aggregated_report)
    labor_output = report_gen.save_labor_report(aggregated_report)
    
    # Save shopping guide if included
    if include_shopping and "shopping_guides" in aggregated_report:
        shopping_output = report_gen.save_shopping_guide_text(aggregated_report)
        if shopping_output:
            print(f"\nTIP: Check the shopping guide for where to buy parts!")
            print(f"   File: {shopping_output}")
    
    # Print next steps
    report_gen.print_next_steps(json_output, parts_output, labor_output)
    
    print("\nReport complete! Thank you for using AutoClaimAI.")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
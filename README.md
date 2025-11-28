
### Notebooks for evaluation
- If you want to make your own evaluation create a google colab notebook and upload your data and/or weight to drive and develop that way.

### Data source for repair times and parts
https://charm.li/ - free open sources is fairly comprehensive from 1986 to 2013
https://vehicledatabases.com/ has a VIN decoding api for searching for vehicle data and parts + labor pricing
Carvis.ai AI native tool for doing the same as vehicle database in an AI native way
https://www.motor.com/wp-content/uploads/daas-estimated-work-times-product-description.pdf - RESTful api call that provides up to date parts and labor times along with cost estimates paid

# AutoClaimAI

AutoClaimAI is an automated vehicle damage assessment tool that uses AI to detect, classify, and estimate the severity of car damages from images. It processes images in bulk or individually and generates structured reports to assist with insurance claims or repair estimates.

## Features
- Detects and classifies car damage from images
- Estimates severity of detected damage (minor, moderate, severe)
- Processes all images in a folder or a single image
- Estimates costs of car damages based off of researched tables and info
- Outputs structured reports for further analysis

## Installation
1. Clone this repository:
	```
	git clone https://github.com/brencemoore/AutoClaimAI
	cd AutoClaimAI
	```
2. Install dependencies:
	```
	pip install -r requirements.txt
	```

## Requirements
- Python 3.8+
- See `requirements.txt` for required packages


## Usage

All commands are run in the terminal. The exact usage format may depend on your machine and Python environment.

To process **all images** in the `input` folder:
```bash
python main.py
```

To process a **specific folder** of images:
```bash
python main.py FILE_DIR
```
Replace `FILE_DIR` with the path to your image directory.

**Note:** Each program run stores its results in a separate `.json` file in the `outputs/` directory. This makes it easy to track and compare different runs.

This project is designed for terminal use, but could easily be ported to a GUI, desktop app, or web application if desired.

## Input
- Place images to be processed in the `input/` directory, or specify a different directory as an argument.


## Output
- Each run generates a separate `.json` report file in the `outputs/` directory, containing the results for that batch or image set.


## Project Structure
- `src/` - Main source code
	- `pipeline/` - Core pipeline code (damage detection, classification, etc.)
		- `car_classification.py` - Contains function for classifying make and model of a car
		- `detect_damage.py` - Contains functions for classifying info from damaged parts of a car
		- `estimate_cost.py` - Contains data and functions to estimate the cost of damages from aggregated data
		- `parts_shopping.py` - Generates infor for shopping guidance based off of researched data and .json file
		- `report_generator.py` - A function that creates the output report files using functions from `car_classification.py`, `detect_damage.py`, `estimate_cost.py`, and `parts_shopping.py`
	- `models/` - Locally stored models
		- `car-damage.pt` - Stores pre-trained weights for classifying severity of damages
		- `car-part.pt` - Stores pre-trained weights for classifying part that is damaged
	- `cost_data/` - Contains .json data for shopping data
		- `labor_rates.json`
		- `labor_time_table.json`
		- `part_cost_table.json`
		- `part_search_terms.json`
		- `parts_retailer.json`
- `input/`
- `outputs/`
- `notebooks/` - Jupyter notebooks for evaluating models with precision, recall, and f1
	- `evaluate_car_classification.ipynb`
	- `evaluate_car_part_classification.ipynb`
	- `evaluate_damage_type.ipynb`
	- `evaluating_damage_severity.ipynb`
- `main.py` - Runs entire AI pipeline
- `requirements.txt` - Contains libraries needed that may not be pre-installed


## Model Source, Evaluation and Metrics Notebooks, and Dataset Links
- Make and model:
	- Model source:  [dima806/car_models_image_detection](https://huggingface.co/dima806/car_models_image_detection)
	- Google Colab notebook:  [evaluate_car_part_classification.ipynb](https://colab.research.google.com/drive/1OHagyo6YzcB0_K5hX7kqSqNKWhLvGGfv?usp=sharing)
	- Dataset used:  [Cars Collection Dataset](https://www.kaggle.com/datasets/ashfaqsyed/cars-collection-dataset/data)
- Damaged part:
	- Model source:  [suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8](https://github.com/suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8)
	- Google Colab notebook:  [evaluate_car_part_classification.ipynb](https://colab.research.google.com/drive/1ubblz5FCEhtWhqSUsrH4MnHS5meu-kyq?usp=sharing)
	- Dataset used:  [suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8/Data](https://github.com/suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8) (had to do a lot of cleaning)
- Damage severity:
	- Model source:  [nezahatkorkmaz/car-damage-level-detection-yolov8](https://huggingface.co/nezahatkorkmaz/car-damage-level-detection-yolov8)
	- Google Colab notebook:  [evaluating_damage_severity.ipynb](https://colab.research.google.com/drive/1nuZP2vxpEATY-TVELBEF35pzo8vJfHzm?usp=sharing)
	- Dataset used:  [Car Damage Severity Dataset](https://www.kaggle.com/datasets/prajwalbhamere/car-damage-severity-dataset)
- Damage type:
	- Model source:  [beingamit99/car_damage_detection](https://huggingface.co/beingamit99/car_damage_detection)
	- Google Colab notebook:  [evaluate_damage_type.ipynb](https://colab.research.google.com/drive/1ZmUPRiCWr56zcHdCqCqHoiXzjBAybBfb?usp=sharing)
	- Dataset used:  [Vehicle Damage Identification](https://www.kaggle.com/datasets/gauravduttakiit/vehicle-damage-identification)
- Cost prediction:
	- Model source:  
	- Google Colab notebook:  
	- Dataset used:  


## Developer Notes

### Pipeline Structure
- The program's pipeline is structured so that `main.py` calls the `report_generator` module. The `report_generator` module then calls functions from various other Python files, each of which uses an AI model to determine the values for variables needed to create the report and estimate costs. This modular approach allows for easy extension and maintenance of the codebase.

### Out-of-Scope Modules
- The following module is likely out of scope and not needed for the main workflow:
	- `read_plate.py`
    - As of now it is deleted, but if more time is available we can maybe implement this.

### Requirements and Dependencies
- As development proceeds, add any new required libraries to `requirements.txt`.
- When using a model, add a comment in the code specifying where the model was obtained from (e.g., Hugging Face link) for easier report writing and reproducibility.

### Evaluation and Reporting
- It is currently undecided whether model evaluations will be performed in a Jupyter notebook or in a separate Python file. Choose the approach that best fits your workflow and document your choice.

---

## Contact
For questions or support, please open an issue in this repository.

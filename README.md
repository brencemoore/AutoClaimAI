# PLEASE MAKE YOUR OWN BRANCH

### Remaining Tasks
- The following components still need to be implemented or improved:
	- Creating or integrating a cost table for estimation
	- Evaluating cost estimation
	- Evaluating damaged part classification
	- Evaluating damaged part severity
	- Evaluating the type of damage

- The most critical parts to measure and refine are:
	- Damaged part classification
	- Cost table estimation

# Data source for repair times and parts
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
- Outputs structured reports for further analysis

## Installation
1. Clone this repository:
	```
	git clone <repo-url>
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
		- `report_generator.py` - A function that creates the output report files using functinos from `car_classification.py`, `detect_damage.py`, and `estimate_cost.py`
	- `models/` - Locally stored models
		- `car-damage.pt` - Stores pre-trained weights for classifying severity of damages
		- `car-part.pt` - Stores pre-trained weights for classifying part that is damaged
- `input/` - Folder for input images
- `outputs/` - Folder for output reports (one `.json` per run)
- `notebooks/` - Jupyter notebooks for evaluation
	- `evaluate_car_classification.ipynb` - Creates a confusion matrix and measures precision, recall, and f1 for make and model classification
- `main.py` - Runs entire AI pipeline
- `requirements.txt` - Contains libraries needed that may not be pre-installed


## Model Source, Evaluation and Metrics Notebooks, and Dataset Links
- Make and model:
	- Model source:  https://huggingface.co/dima806/car_models_image_detection
	- Google Colab notebook:  https://colab.research.google.com/drive/1OHagyo6YzcB0_K5hX7kqSqNKWhLvGGfv?usp=sharing
	- Dataset used:  https://www.kaggle.com/datasets/ashfaqsyed/cars-collection-dataset/data
- Damaged part:
	- Model source:  https://github.com/suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8
	- Google Colab notebook:  https://colab.research.google.com/drive/1ubblz5FCEhtWhqSUsrH4MnHS5meu-kyq?usp=sharing
	- Dataset used:  https://github.com/suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8 (had to do a lot of cleaning)
- Damage severity:
	- Model source:  https://huggingface.co/nezahatkorkmaz/car-damage-level-detection-yolov8
	- Google Colab notebook:  
	- Dataset used:  
- Damage type:
	- Model source:  https://huggingface.co/beingamit99/car_damage_detection
	- Google Colab notebook:  
	- Dataset used:  
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

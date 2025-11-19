'''
Uses pre-trained models to classify the type and severity of car damage from a given image.
'''

# From 'https://huggingface.co/beingamit99/car_damage_detection'

# Classifies the type of damage on the car
def classify_damage(image_path):
    from transformers import pipeline
    pipe = pipeline("image-classification", model="beingamit99/car_damage_detection")
    result = pipe(image_path)
    print(f'Results: {result}')
    best = max(result, key=lambda x: x['score'])
    return best['label']


# From 'https://huggingface.co/nezahatkorkmaz/car-damage-level-detection-yolov8'

# Classifies the severity of the damage on the car
def damage_severity(image_path):
    from ultralytics import YOLO
    from pathlib import Path

    model_path = Path(__file__).resolve().parent.parent / "models" / "car-damage.pt"
    model = YOLO(model_path)
    results = model(image_path)
    
    # Extract classification probabilities
    probs = results[0].probs
    
    severity = ['Minor', 'Moderate', 'Severe']
    
    return severity[probs.top1]
    

# From 'https://github.com/suryaremanan/Damaged-Car-parts-prediction-using-YOLOv8' (best.pt)

# Classifies the damaged part of the car
def classify_part(image_path):
    from ultralytics import YOLO
    from pathlib import Path

    model_path = Path(__file__).resolve().parent.parent / "models" / "car-part.pt"
    model = YOLO(model_path)
    results = model(image_path)
    
    # Extract detected class names
    detected_parts = results[0].names
    boxes = results[0].boxes
    
    # Return 'unknown' if part cannot be determined
    if boxes is None or boxes.cls is None or len(boxes.cls) == 0:
        return "Unknown"

    # If there are detections, get the most confident one
    classes = boxes.cls.cpu().numpy()
    confidences = boxes.conf.cpu().numpy()
    best_idx = confidences.argmax()
    best_class = int(classes[best_idx])
    
    parts = ['Door', 'Window', 'Headlight', 'Mirror', 'Body/Unknown', 'Hood', 'Bumper', 'Wind Shield']

    return parts[best_class]


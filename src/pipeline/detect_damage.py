'''
Uses pre-trained models to classify the type and severity of car damage from a given image.
'''

# From 'https://huggingface.co/beingamit99/car_damage_detection'

def classify_damage(image_path):
    from transformers import pipeline
    pipe = pipeline("image-classification", model="beingamit99/car_damage_detection")
    result = pipe(image_path)
    print(f'Results: {result}')
    best = max(result, key=lambda x: x['score'])
    return best['label']


# From 'https://huggingface.co/nezahatkorkmaz/car-damage-level-detection-yolov8'

def damage_severity(image_path):
    from ultralytics import YOLO
    from pathlib import Path

    model_path = Path(__file__).resolve().parent.parent / "models" / "car-damage.pt"
    model = YOLO(model_path)
    results = model(image_path)
    
    # Extract classification probabilities
    probs = results[0].probs
    
    severity = ['minor', 'moderate', 'severe']
    
    return severity[probs.top1]
    

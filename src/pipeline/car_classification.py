'''
Detects the make and model of the car from an image.
'''

# From 'https://huggingface.co/dima806/car_models_image_detection'

def classify_car(image_path):
    from transformers import pipeline
    pipe = pipeline("image-classification", model="dima806/car_models_image_detection")
    result = pipe(image_path)
    
    make_and_model = result[0]["label"]
    
    make = make_and_model.split(' ')[0].capitalize()
    model = make_and_model.split(' ')[1].capitalize()
    
    return make, model


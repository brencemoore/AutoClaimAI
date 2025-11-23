'''
Uses a pre-trained model to detect the make and model of the car from an image.
'''

# From 'https://huggingface.co/dima806/car_models_image_detection'

def classify_car(image_path):
    from transformers import pipeline
    pipe = pipeline("image-classification", model="dima806/car_models_image_detection", device=0, use_fast=True)
    result = pipe(image_path)
    
    make_and_model = result[0]["label"]
    
    split_string = make_and_model.split(' ')

    make = split_string[0]
    model = split_string[1]

    split_string = split_string[2:]
    for x in range(len(split_string)):
        model = model + ' ' + split_string[x]
    
    return make.upper(), model.upper()


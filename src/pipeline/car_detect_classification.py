from hf_utils import call_hf_api, load_image_as_bytes

model = "facebook/detr-resnet-101"   # Example model

img = load_image_as_bytes("test_images/car1.jpg")
result = call_hf_api(model, img, task_type="image")

print(result)

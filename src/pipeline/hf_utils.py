import requests
import os

# Load your Hugging Face API key from environment variable
# (everyone on your team will set this once in Colab)
API_KEY = os.getenv("HF_API_KEY")

if API_KEY is None:
    raise ValueError("❌ Missing Hugging Face API Key. Run: os.environ['HF_API_KEY'] = 'your_key_here'")

# Base inference URL for hosted models
HF_API_URL = "https://api-inference.huggingface.co/models/"

def call_hf_api(model_name, inputs, task_type="image"):
    """
    Sends an inference request to a Hugging Face model API.
    
    Args:
        model_name (str): HF model id, e.g. "openai/clip-vit-base-patch32"
        inputs: image bytes OR text, depending on model
        task_type (str): "image" or "text"
    
    Returns:
        JSON response from Hugging Face API
    """

    headers = {"Authorization": f"Bearer {API_KEY}"}

    if task_type == "image":
        response = requests.post(
            HF_API_URL + model_name,
            headers=headers,
            data=inputs  # raw image bytes
        )
    elif task_type == "text":
        response = requests.post(
            HF_API_URL + model_name,
            headers=headers,
            json={"inputs": inputs}
        )
    else:
        raise ValueError("task_type must be 'image' or 'text'")

    if response.status_code != 200:
        print("⚠️ Error with Hugging Face request:", response.text)

    return response.json()


def load_image_as_bytes(path):
    """
    Loads an image from disk and returns raw bytes ready for the HF API.
    """
    with open(path, "rb") as f:
        return f.read()

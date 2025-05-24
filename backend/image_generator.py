import requests
import os
from PIL import Image
import io
import base64
from create_default_image import create_default_image

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Using a different model that's more accessible
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_image(prompt):
    try:
        # First, ensure we have a default image
        default_image_path = os.path.join(current_dir, "default_image.png")
        if not os.path.exists(default_image_path):
            default_image_path = create_default_image()

        # Prepare the prompt
        full_prompt = f"Create a fun, colorful illustration for kids: {prompt}"
        
        # Make the API request
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": full_prompt,
                "parameters": {
                    "negative_prompt": "ugly, blurry, poor quality, distorted",
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5
                }
            }
        )
        
        if response.status_code == 200:
            # Create a PIL Image from the response content
            image = Image.open(io.BytesIO(response.content))
            
            # Save the image temporarily in the backend directory
            temp_path = os.path.join(current_dir, "temp_image.png")
            image.save(temp_path, format="PNG")
            os.chmod(temp_path, 0o644)  # Set correct permissions
            return temp_path
        else:
            print(f"Error: {response.status_code}, {response.text}")
            # Return the default image path
            return default_image_path
            
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        # Return the default image path
        return default_image_path

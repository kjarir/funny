import requests
import os
from PIL import Image
import io
import base64
from create_default_image import create_default_image

current_dir = os.path.dirname(os.path.abspath(__file__))

# Stability AI API endpoint
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
API_KEY = "sk-Aln8DOvKp3w4vxGbclU8k04cT0O2M2SzfHYYL34BD0bYPGLr"  # Replace with your Stability AI API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def generate_image(prompt):
    try:
        default_image_path = os.path.join(current_dir, "default_image.png")
        if not os.path.exists(default_image_path):
            default_image_path = create_default_image()

        full_prompt = f"Create a vibrant, detailed, and engaging illustration for children: {prompt}. Style: colorful, whimsical, and child-friendly"
        
        # Make the API request
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "text_prompts": [
                    {
                        "text": full_prompt,
                        "weight": 1
                    },
                    {
                        "text": "ugly, blurry, poor quality, distorted, scary, inappropriate",
                        "weight": -1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,  # Using correct SDXL dimensions
                "width": 1024,   # Using correct SDXL dimensions
                "samples": 1,
                "steps": 30,
                "style_preset": "fantasy-art"  # Changed to fantasy-art for more whimsical results
            }
        )

        if response.status_code == 200:
            result = response.json()
            
            if 'artifacts' in result and len(result['artifacts']) > 0:
                # Get the base64 image data
                image_data = base64.b64decode(result['artifacts'][0]['base64'])
                image = Image.open(io.BytesIO(image_data))
                
                # Save the image temporarily
                temp_path = os.path.join(current_dir, "temp_image.png")
                image.save(temp_path, format="PNG")
                os.chmod(temp_path, 0o644)
                return temp_path

        print(f"Error: {response.status_code}, {response.text}")
        return default_image_path

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return default_image_path

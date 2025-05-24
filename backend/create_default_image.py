from PIL import Image, ImageDraw, ImageFont
import os

def create_default_image():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a new image with a white background
    img = Image.new('RGB', (512, 512), color='white')
    d = ImageDraw.Draw(img)
    
    # Add some text
    try:
        # Try to use a system font
        font = ImageFont.truetype("Arial", 40)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw text
    text = "Image Generation\nFailed"
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (512 - text_width) // 2
    y = (512 - text_height) // 2
    
    d.text((x, y), text, fill='black', font=font)
    
    # Save the image in the backend directory
    default_image_path = os.path.join(current_dir, 'default_image.png')
    img.save(default_image_path)
    
    # Ensure the file has the correct permissions
    os.chmod(default_image_path, 0o644)
    
    return default_image_path

if __name__ == "__main__":
    create_default_image() 

import base64
from pathlib import Path
from sdk import VeniceClient, ImageAPI
from dotenv import load_dotenv
import os

load_dotenv()

# Example usage
client = VeniceClient(os.environ.get('VENICE_API_KEY', 'XXXX'))
api = ImageAPI(client)

# Define the input and output file paths using pathlib
input_image_path = Path("generated_image.png")  # Replace with your image file
output_image_path = Path("upscaled_image.png")

# Check if the input file exists
if not input_image_path.is_file():
    raise FileNotFoundError(f"Input image not found: {input_image_path}")

# Read the image file and encode it to base64
with open(input_image_path, "rb") as image_file:
    image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

# Upscale the image using the base64-encoded string
image_data = api.upscale_image(image_base64=image_base64, scale=2.7, enhance=False)

# Save the upscaled image
output_image_path.write_bytes(image_data)

print(f"Upscaled image saved to {output_image_path}")

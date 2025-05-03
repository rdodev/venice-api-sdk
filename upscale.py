from sdk import VeniceClient, ImageAPI
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

# Example usage
client = VeniceClient(os.environ.get('VENICE_API_KEY', 'XXXX'))
api = ImageAPI(client)
# Your code here
# Define the input and output file paths using pathlib
input_image = Path("upscaled_image.png")  # Replace with your image file
output_image = Path("upscaled4x_image.png")

# Check if the input file exists
if not input_image.is_file():
    raise FileNotFoundError(f"Input image not found: {input_image}")

# Upscale the image
image_data = api.upscale_image(image_path=str(input_image), scale=1.2, enhance="false")

# Save the upscaled image
output_image.write_bytes(image_data)

print(f"Upscaled image saved to {output_image}")

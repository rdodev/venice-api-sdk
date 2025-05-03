from .client import VeniceClient, VeniceAPIError
from .models import GenerateImageRequest
from typing import Union
import mimetypes
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageAPI:
    """API class for image-related endpoints."""

    def __init__(self, client: VeniceClient):
        """Initialize with a VeniceClient instance.

        Args:
            client: The VeniceClient instance to use for requests.
        """
        self.client = client

    def generate_image(self, request: GenerateImageRequest) -> bytes:
        """Generate an image based on the request.

        Args:
            request: The image generation request object.

        Returns:
            The binary image data.
        """
        response = self.client.post("/image/generate", json=request.dict(exclude_none=True))
        self._validate_image_response(response)
        return response.content

    def generate_image_simple(self, prompt: str, model: str, **kwargs) -> bytes:
        """Convenience method to generate an image with simple parameters.

        Args:
            prompt: The text prompt for the image.
            model: The model ID to use.
            **kwargs: Additional optional parameters.

        Returns:
            The binary image data.
        """
        request = GenerateImageRequest(prompt=prompt, model=model, **kwargs)
        return self.generate_image(request)

    def upscale_image(self, image_path: str, scale: Union[int, float] = 2, enhance: str = "false", **kwargs) -> bytes:
        """Upscale an image.

        Args:
            image_path: Path to the image file to upscale.
            scale: The scale factor (1-4).
            enhance: Whether to enhance the image ("true" or "false").
            **kwargs: Additional optional parameters.

        Returns:
            The binary upscaled image data.

        Raises:
            FileNotFoundError: If the input image file does not exist.
            VeniceAPIError: If the API request fails or returns invalid/empty image data.
        """
        import os
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Input image not found: {image_path}")

        logger.debug(f"Uploading image: {image_path} with scale={scale}, enhance={enhance}")
        with open(image_path, "rb") as f:
            # Guess MIME type based on file extension
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type or not mime_type.startswith("image/"):
                mime_type = "application/octet-stream"
            files = {"image": (os.path.basename(image_path), f, mime_type)}
            data = {"scale": scale, "enhance": enhance, **{k: str(v) for k, v in kwargs.items()}}
            response = self.client.post("/image/upscale", files=files, data=data)

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response content length: {len(response.content)} bytes")

            self._validate_image_response(response)
            if not response.content:
                raise VeniceAPIError("API returned an empty response body")
            return response.content

    def _validate_image_response(self, response):
        """Validate that the response contains valid image data.

        Args:
            response: The HTTP response object.

        Raises:
            VeniceAPIError: If the response is not a valid image.
        """
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            try:
                error_data = response.json()
                error_message = error_data.get("error", "Unknown error")
            except ValueError:
                error_message = response.text or "Invalid response format"
            raise VeniceAPIError(f"Expected image data, got {content_type}: {error_message}")

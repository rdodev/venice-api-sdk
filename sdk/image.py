from .client import VeniceClient, VeniceAPIError
from .models import GenerateImageRequest
from typing import Union
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

        Raises:
            VeniceAPIError: If the API request fails or returns invalid/empty image data.
        """
        logger.debug(f"Generating image with model: {request.model}, prompt length: {len(request.prompt)}")
        response = self.client.post("/image/generate", json=request.dict(exclude_none=True))
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response content length: {len(response.content)} bytes")
        self._validate_image_response(response)
        if not response.content:
            raise VeniceAPIError("API returned an empty response body")
        return response.content

    def generate_image_simple(self, prompt: str, model: str, **kwargs) -> bytes:
        """Convenience method to generate an image with simple parameters.

        Args:
            prompt: The text prompt for the image.
            model: The model ID to use.
            **kwargs: Additional optional parameters.

        Returns:
            The binary image data.

        Raises:
            VeniceAPIError: If the API request fails or returns invalid/empty image data.
        """
        logger.debug(f"Generating image with prompt length: {len(prompt)}, model: {model}")
        request = GenerateImageRequest(prompt=prompt, model=model, **kwargs)
        return self.generate_image(request)

    def upscale_image(self, image_base64: str, scale: float = 2.0, enhance: bool = False, **kwargs) -> bytes:
        """Upscale an image using a JSON request with a base64-encoded image string.

        Args:
            image_base64: The base64-encoded string of the image to upscale.
            scale: The scale factor (1-4). Default is 2.0.
            enhance: Whether to enhance the image. Default is False.
            **kwargs: Additional optional parameters (e.g., enhanceCreativity, enhancePrompt, replication).

        Returns:
            The binary upscaled image data.

        Raises:
            VeniceAPIError: If the API request fails or returns invalid/empty image data.
        """
        request_data = {
            "image": image_base64,
            "scale": scale,
            "enhance": enhance,
            **kwargs
        }
        response = self.client.post("/image/upscale", json=request_data)

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

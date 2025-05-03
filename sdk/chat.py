from .client import VeniceClient, VeniceAPIError
from .models import ChatCompletionRequest, ChatCompletionResponse, Message
from typing import List
import logging
from pydantic import ValidationError

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatAPI:
    """API class for chat-related endpoints."""

    def __init__(self, client: VeniceClient):
        """Initialize with a VeniceClient instance.

        Args:
            client: The VeniceClient instance to use for requests.
        """
        self.client = client

    def create_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Create a chat completion.

        Args:
            request: The chat completion request object.

        Returns:
            The chat completion response object.

        Raises:
            VeniceAPIError: If the API request fails, returns an empty response, or the response cannot be parsed/validated.
        """
        logger.debug(f"Creating chat completion with model: {request.model}, number of messages: {len(request.messages)}")
        response = self.client.post("/chat/completions", json=request.dict(exclude_none=True))
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response content length: {len(response.content)} bytes")
        if not response.content:
            raise VeniceAPIError("API returned an empty response body")
        try:
            response_data = response.json()
            return ChatCompletionResponse(**response_data)
        except ValueError as e:
            raise VeniceAPIError(f"Failed to parse response as JSON: {e}")
        except ValidationError as e:
            raise VeniceAPIError(f"Response validation failed: {e}")
        except Exception as e:
            raise VeniceAPIError(f"Unexpected error: {e}")

    def create_completion_simple(self, messages: List[dict], model: str, **kwargs) -> ChatCompletionResponse:
        """Convenience method to create a chat completion with simple parameters.

        Args:
            messages: List of message dictionaries.
            model: The model ID to use.
            **kwargs: Additional optional parameters.

        Returns:
            The chat completion response object.

        Raises:
            VeniceAPIError: If the API request fails, returns an empty response, or the response cannot be parsed/validated.
        """
        logger.debug(f"Creating chat completion with {len(messages)} messages, model: {model}")
        request = ChatCompletionRequest(
            messages=[Message(**msg) for msg in messages],
            model=model,
            **kwargs
        )
        return self.create_completion(request)

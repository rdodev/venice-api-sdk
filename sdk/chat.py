from .client import VeniceClient
from .models import ChatCompletionRequest, ChatCompletionResponse
from typing import List

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
        """
        response = self.client.post("/chat/completions", json=request.dict(exclude_none=True))
        return ChatCompletionResponse(**response.json())

    def create_completion_simple(self, messages: List[dict], model: str, **kwargs) -> ChatCompletionResponse:
        """Convenience method to create a chat completion with simple parameters.

        Args:
            messages: List of message dictionaries.
            model: The model ID to use.
            **kwargs: Additional optional parameters.

        Returns:
            The chat completion response object.
        """
        request = ChatCompletionRequest(
            messages=[Message(**msg) for msg in messages],
            model=model,
            **kwargs
        )
        return self.create_completion(request)

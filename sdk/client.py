import requests
from typing import Optional

class VeniceClient:
    """Main client class for interacting with the Venice.ai API."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.venice.ai/api/v1"):
        """Initialize the client with an optional API key and base URL.

        Args:
            api_key: The API key for authentication (optional).
            base_url: The base URL of the API (default: "https://api.venice.ai/api/v1").
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(self, path: str, **kwargs) -> Optional[requests.Response]:
        """Make a GET request to the API.

        Args:
            path: The endpoint path (e.g., '/models').
            **kwargs: Additional arguments for the request.

        Returns:
            The HTTP response object.

        Raises:
            VeniceAPIError: If the request fails.
        """
        try:
            response = self.session.get(f"{self.base_url}{path}", **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def post(self, path: str, **kwargs) -> Optional[requests.Response]:
        """Make a POST request to the API.

        Args:
            path: The endpoint path (e.g., '/chat/completions').
            **kwargs: Additional arguments for the request (e.g., json, files).

        Returns:
            The HTTP response object.

        Raises:
            VeniceAPIError: If the request fails.
        """
        try:
            response = self.session.post(f"{self.base_url}{path}", **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError) -> None:
        """Handle HTTP errors by raising appropriate exceptions."""
        response = error.response
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        else:
            raise VeniceAPIError(f"API error: {response.status_code} {response.text}")

class VeniceAPIError(Exception):
    """Base exception for Venice API errors."""
    pass

class AuthenticationError(VeniceAPIError):
    """Exception raised for authentication failures."""
    pass

class RateLimitError(VeniceAPIError):
    """Exception raised when rate limit is exceeded."""
    pass

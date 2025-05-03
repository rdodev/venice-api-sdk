from pydantic import BaseModel
from typing import List, Union, Optional, Dict, Any

class Message(BaseModel):
    """Message model for chat completions."""
    role: str
    content: Union[str, List[Dict[str, Any]]]

class ChatCompletionRequest(BaseModel):
    """Request model for chat completions."""
    messages: List[Message]
    model: str
    frequency_penalty: Optional[float] = 0
    max_completion_tokens: Optional[int] = None
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.15
    top_p: Optional[float] = 0.9
    # Add other fields as needed from the Swagger schema

class Choice(BaseModel):
    """Choice model in chat completion response."""
    finish_reason: str
    index: int
    message: Message

class ChatCompletionResponse(BaseModel):
    """Response model for chat completions."""
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Dict[str, Any]

class GenerateImageRequest(BaseModel):
    """Request model for image generation."""
    model: str
    prompt: str
    height: Optional[int] = 1024
    width: Optional[int] = 1024
    format: Optional[str] = "png"

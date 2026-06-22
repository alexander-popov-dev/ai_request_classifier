from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Self

T = TypeVar('T')

class BaseAIClient(ABC, Generic[T]):
    """Abstract generic AI client with context manager lifecycle."""

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key: str = api_key
        self._model: str = model
        self._client: T | None = None

    @abstractmethod
    def start(self) -> None:
        """Initialize the underlying AI SDK client."""

    @abstractmethod
    def close(self) -> None:
        """Release the underlying AI SDK client resources."""

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @abstractmethod
    def request(self, contents: str, prompt: str) -> str:
        """Send prompt and contents to the AI and return a raw text response."""

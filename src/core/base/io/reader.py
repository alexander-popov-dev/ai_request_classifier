from abc import ABC, abstractmethod

from src.core.schemas import RequestRecord


class BaseRequestReader(ABC):
    """Abstract reader that loads request records from an external source."""

    @abstractmethod
    def read(self) -> list[RequestRecord]:
        """Load and return all request records."""

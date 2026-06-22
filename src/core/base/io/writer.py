from abc import ABC, abstractmethod

from src.core.schemas import RequestAnalysis


class BaseResultWriter(ABC):
    """Abstract writer that persists classification results."""

    @abstractmethod
    def write(self, results: list[RequestAnalysis]) -> None:
        """Persist a list of classification results."""

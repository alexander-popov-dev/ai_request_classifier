from abc import ABC, abstractmethod

from src.core.schemas import RequestAnalysis, RequestRecord


class BaseAIRequestAnalysisParser(ABC):
    """Abstract parser converting raw AI response text into RequestAnalysis."""

    @abstractmethod
    def parse(self, response: str, request_record: RequestRecord) -> RequestAnalysis:
        """Parse raw AI response into a RequestAnalysis for the given record."""

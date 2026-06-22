from pydantic import BaseModel

from src.core.enums import CategoryType, PriorityType


class RequestRecord(BaseModel):
    """Incoming request record read from an external source."""

    id: str
    channel: str
    timestamp: str
    raw_text: str

    def to_contents(self) -> str:
        """Serialize fields into a formatted string for LLM input."""
        return (
            f"Channel: {self.channel}\n"
            f"Timestamp: {self.timestamp}\n"
            f"Request text: {self.raw_text}"
        )

class RequestAnalysis(BaseModel):
    """Classification result produced by the AI for a single RequestRecord."""

    source: RequestRecord
    category: CategoryType | None = None
    target_department: str | None = None
    priority: PriorityType | None = None
    short_summary: str | None = None
    requested_actions: list[str] = []
    needs_clarification: bool | None = None
    is_duplicate_hint: str | None = None
    language: str | None = None
    error: str | None = None

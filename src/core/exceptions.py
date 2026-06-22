class AIClientError(Exception):
    """Base error for AI client failures."""


class BuildAIClientError(AIClientError):
    """Raised when the AI client cannot be initialized."""


class RequestAIClientError(AIClientError):
    """Raised when an AI API request fails."""


class ParsingError(Exception):
    """Base error for response parsing failures."""


class RequestAnalysisParserError(ParsingError):
    """Raised when AI response cannot be parsed into RequestAnalysis."""


class RetryError(Exception):
    """Raised when all retry attempts have been exhausted."""


class ReaderError(Exception):
    """Base error for input reader failures."""


class CsvReaderError(ReaderError):
    """Raised when CSV input cannot be read or parsed."""

import json

from src.core.base.ai.parser import BaseAIRequestAnalysisParser
from src.core.exceptions import RequestAnalysisParserError
from src.core.schemas import RequestAnalysis, RequestRecord


class GeminiRequestAnalysisParser(BaseAIRequestAnalysisParser):
    """Parses JSON response from Gemini into a RequestAnalysis instance."""

    def parse(self, response: str, request_record: RequestRecord) -> RequestAnalysis:
        """Deserialize Gemini JSON response and attach the source RequestRecord."""
        text = response.strip()

        try:
            if text.startswith("```"):
                lines = text.splitlines()
                lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                text = "\n".join(lines)

            data = json.loads(text.strip())
            data["source"] = request_record

            return RequestAnalysis(**data)

        except Exception as e:
            raise RequestAnalysisParserError(e)

import logging
import time

from src.core.base.ai.client import BaseAIClient
from src.core.base.ai.parser import BaseAIRequestAnalysisParser
from src.core.decorators import retry
from src.core.exceptions import RequestAIClientError, RequestAnalysisParserError, RetryError
from src.core.schemas import RequestRecord, RequestAnalysis

logger = logging.getLogger(__name__)

class RequestClassifierService:
    """Orchestrates AI classification of multiple request records."""

    def __init__(
        self,
        prompt: str,
        client: BaseAIClient,
        parser: BaseAIRequestAnalysisParser,
        request_delay: float = 0.0,
    ) -> None:
        self._prompt = prompt
        self._client = client
        self._parser = parser
        self._request_delay = request_delay

    def execute(self, request_records: list[RequestRecord]) -> list[RequestAnalysis]:
        """Classify all records sequentially and return results."""
        results = []

        for i, request_record in enumerate(request_records):
            logger.info(f"[{i + 1}/{len(request_records)}][{request_record.id}] Processing started")
            results.append(self.classify(request_record=request_record))
            logger.info(f"[{i + 1}/{len(request_records)}][{request_record.id}] Processing finished")

            if i < len(request_records) - 1:
                time.sleep(self._request_delay)

        return results

    def classify(self, request_record: RequestRecord) -> RequestAnalysis:
        """Classify a single record, returning an error result on retry exhaustion."""
        try:
            return self._classify(request_record=request_record)
        except RetryError as e:
            return RequestAnalysis(source=request_record, error=str(e))

    @retry(attempts=3, exceptions=(RequestAIClientError, RequestAnalysisParserError))
    def _classify(self, request_record: RequestRecord) -> RequestAnalysis:
        """Send request to AI and parse response; retried on failure."""
        logger.info("Send request to AI")
        response = self._client.request(contents=request_record.to_contents(), prompt=self._prompt)

        logger.info("Parsing AI response")
        return self._parser.parse(response=response, request_record=request_record)

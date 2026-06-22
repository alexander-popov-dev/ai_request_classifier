import logging

from src.ai.gemini.client import GeminiClient
from src.ai.gemini.parser import GeminiRequestAnalysisParser
from src.ai.gemini.prompts import REQUEST_CLASSIFIER_PROMPT
from src.config import Settings
from src.core.exceptions import BuildAIClientError
from src.readers.csv_reader import CsvRequestReader
from src.service import RequestClassifierService
from src.writers.json_writer import JsonResultWriter
from src.writers.md_writer import MarkdownResultWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    """Entry point: read input, run classification, write results."""
    settings = Settings()

    reader = CsvRequestReader(file_path=settings.input_file)
    request_records = reader.read()

    try:
        with GeminiClient(api_key=settings.gemini_api_key, model=settings.gemini_model) as client:
            service = RequestClassifierService(
                prompt=REQUEST_CLASSIFIER_PROMPT,
                client=client,
                parser=GeminiRequestAnalysisParser(),
                request_delay=settings.request_delay,
            )
            results = service.execute(request_records=request_records)
    except BuildAIClientError as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        raise SystemExit(1)

    json_writer = JsonResultWriter(file_path=settings.output_file)
    md_writer = MarkdownResultWriter(file_path=settings.report_file)

    json_writer.write(results)
    md_writer.write(results)

    logger.info(f"Done: {len(results)} requests → {settings.output_file}, {settings.report_file}")


if __name__ == "__main__":
    main()

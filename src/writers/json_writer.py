import json
from pathlib import Path

from src.core.base.io.writer import BaseResultWriter
from src.core.schemas import RequestAnalysis


class JsonResultWriter(BaseResultWriter):
    """Writes classification results to a JSON file."""

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def write(self, results: list[RequestAnalysis]) -> None:
        """Serialize results to JSON and write to the configured file path."""
        results_dict = [result.model_dump(exclude_none=True) for result in results]
        results_json = json.dumps(results_dict, ensure_ascii=False, indent=4)

        path = Path(self._file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(results_json, encoding="utf-8")

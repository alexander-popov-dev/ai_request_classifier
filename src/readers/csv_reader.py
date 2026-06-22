import csv

from src.core.base.io.reader import BaseRequestReader
from src.core.exceptions import CsvReaderError
from src.core.schemas import RequestRecord


class CsvRequestReader(BaseRequestReader):
    """Reads request records from a CSV file."""

    def __init__(self, file_path: str):
        self._file_path = file_path

    def read(self) -> list[RequestRecord]:
        """Read all rows from the CSV file as RequestRecord instances."""
        try:
            with open(self._file_path, newline="", encoding="utf-8") as file:
                return [RequestRecord(**row) for row in csv.DictReader(file)]
        except Exception as e:
            raise CsvReaderError(e)

import csv
from typing import List

from pipeline.pipeline import NextStep
from pipeline.steps.context import Context


class FormatValidationStep:
    def __init__(self, headers: List[str]) -> None:
        self._headers = headers

    @property
    def headers(self) -> List[str]:
        return self._headers

    def __call__(self, context: Context, next_step: NextStep) -> None:
        if not context.file.name.endswith(".csv"):
            raise ValueError("Unsupported file type.")
        context.file.seek(0)
        reader = csv.reader(context.file)
        headers = next(reader)
        self.validate_headers(headers)

        for item in reader:
            record = dict(zip(headers, item))
            context.record = record
            context.total_records += 1
            next_step(context)

    def validate_headers(self, headers: List[str]) -> None:
        if headers != self._headers:
            raise ValueError(f"Invalid headers in the csv file. Expected: {self._headers}, got: {headers}")

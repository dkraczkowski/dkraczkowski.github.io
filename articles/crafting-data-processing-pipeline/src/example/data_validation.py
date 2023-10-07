from typing import List

from example.context import Context
from pipeline.pipeline import NextStep


class DataValidationStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        self._naive_email_validator(context.record.get("Email"))
        try:
            context.record["FirstName"], context.record["LastName"] = self._format_name(context.record["Name"])
            context.record["Age"] = int(context.record["Age"])
            next_step(context)
        except Exception as error:
            raise ValueError(f"Failed to validate record: `{context.record}`") from error

    @staticmethod
    def _format_name(name: str) -> List[str]:
        return name.split(" ")

    @staticmethod
    def _naive_email_validator(email: str) -> None:
        if "@" not in email:
            raise ValueError(f"Invalid email address `{email}`")

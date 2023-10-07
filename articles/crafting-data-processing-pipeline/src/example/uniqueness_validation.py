from typing import List

from example.context import Context
from pipeline.pipeline import NextStep


class UniquenessValidationStep:
    def __init__(self, reserved_emails: List[str]) -> None:
        self._reserved_emails = reserved_emails

    def __call__(self, context: Context, next_step: NextStep) -> None:
        if context.record["Email"] in self._reserved_emails:
            raise ValueError("User with this email already exists.")

        next_step(context)

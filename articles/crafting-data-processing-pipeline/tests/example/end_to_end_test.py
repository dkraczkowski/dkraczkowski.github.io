from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection
from typing import TextIO

import pytest

from example.context import UserRecord
from example.data_validation import DataValidationStep
from example.format_validation import FormatValidationStep
from example.uniqueness_validation import UniquenessValidationStep
from example.user_creation import UserCreationStep
from pipeline.pipeline import Pipeline, NextStep


@pytest.mark.sqlite_db(data="users.yaml")
def test_can_import_users_with_pipeline(sqlite_db: Connection, fixture_dir: Path) -> None:
    # given
    @dataclass
    class Context:
        file: TextIO
        record: UserRecord = None
        total_records: int = 0
        imported_records: int = 0
        failed_records: int = 0

    def error_handler(error: Exception, context: Context, next_step: NextStep):
        context.failed_records += 1

    pipeline = Pipeline[Context](
        FormatValidationStep(["Name", "Email", "Age"]),
        DataValidationStep(),
        UniquenessValidationStep(["test@test.com"]),
        UserCreationStep(sqlite_db),
    )
    file = (fixture_dir / "valid_data.csv").open(mode="r")

    ctx = Context(file=file)

    # when
    pipeline(ctx, error_handler)

    # then
    assert ctx.imported_records == 2
    assert ctx.failed_records == 2




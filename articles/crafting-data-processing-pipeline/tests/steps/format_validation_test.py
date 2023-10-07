from dataclasses import dataclass
from pathlib import Path
from typing import TextIO, Dict, Any
from unittest.mock import MagicMock

import pytest

from pipeline.steps.format_validation import FormatValidationStep


def test_can_instantiate() -> None:
    # given
    instance = FormatValidationStep(headers=["One", "Two"])

    # then
    assert isinstance(instance, FormatValidationStep)


def test_can_accept_csv_file_with_valid_headers(fixture_dir: Path) -> None:
    # given
    file = (fixture_dir / "valid_data.csv").open(mode="r")
    records_count = file.read().count("\n") - 1  # excluding header
    validation_step = FormatValidationStep(headers=["Name", "Email", "Age"])
    call_next = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]
        total_records: int = 0

    # when
    context = Context(file, {})
    validation_step.__call__(context, call_next)

    # then
    assert call_next.call_count == records_count
    assert context.record


def test_fails_on_invalid_file(fixture_dir: Path) -> None:
    # given
    file = (fixture_dir / "valid_data.xml").open(mode="r")
    validation_step = FormatValidationStep(headers=["Name", "Email", "Age"])

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(file, {})

    # then
    with pytest.raises(ValueError, match="Unsupported file type *"):
        validation_step.__call__(context, MagicMock())


def test_fail_csv_file_with_invalid_headers(fixture_dir: Path) -> None:
    # given
    file = (fixture_dir / "valid_data.csv").open(mode="r")
    validation_step = FormatValidationStep(headers=["Name", "Email", "Role"])

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(file, {})

    # then
    with pytest.raises(ValueError, match="Invalid headers in the csv file *"):
        validation_step.__call__(context, MagicMock())

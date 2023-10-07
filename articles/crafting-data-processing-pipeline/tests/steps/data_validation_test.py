from dataclasses import dataclass
from typing import TextIO, Dict, Any
from unittest.mock import MagicMock

import pytest

from pipeline.steps.context import UserRecord
from pipeline.steps.data_validation import DataValidationStep


@pytest.mark.parametrize("record", [
    {
        "Name": "Bob Bylan",
        "Age": "55",
        "Email": "email@address.com",
    },
    {
        "Name": "Elise Kooper",
        "Age": 12,
        "Email": "kooper@elise.com",
    }
])
def test_can_validate_record(record: UserRecord) -> None:
    # given
    step = DataValidationStep()
    next_step = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(MagicMock(), record)

    # when
    step.__call__(context, next_step)

    # then
    assert next_step.called


@pytest.mark.parametrize("record", [
    {
        "Name": "Bob Bylan",
        "Age": "Invalid Age",
        "Email": "email@address.com",
    },
    {
        "Name": "Elise Kooper",
        "Age": 12,
        "Email": "invalidemailaddress.com",
    },
    {
        "MissingName": "",
        "Age": 10,
        "Email": "email@address.com"
    }
])
def test_can_invalidate_record(record: UserRecord) -> None:
    # given
    step = DataValidationStep()
    next_step = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(MagicMock(), record)

    # when
    with pytest.raises(ValueError):
        step.__call__(context, next_step)

    # then
    assert not next_step.called

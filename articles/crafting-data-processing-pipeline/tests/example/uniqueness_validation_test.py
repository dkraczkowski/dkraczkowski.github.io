from dataclasses import dataclass
from typing import TextIO, Dict, Any
from unittest.mock import MagicMock

import pytest
from sqlite3 import Connection

from example.uniqueness_validation import UniquenessValidationStep


@pytest.mark.sqlite_db(data="users.yaml")
def test_can_process_unique_item(sqlite_db: Connection) -> None:
    # given
    step = UniquenessValidationStep(reserved_emails=["test@test.com", "bob@example.com"])
    next_step = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(MagicMock(), {
        "Email": "uniqu@email.com",
    })

    # when
    step.__call__(context, next_step)

    # then
    assert next_step.called


def test_should_not_process_duplicates() -> None:
    # given
    step = UniquenessValidationStep(reserved_emails=["test@test.com", "bob@example.com"])
    next_step = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]

    context = Context(MagicMock(), {
        "Email": "test@test.com",
    })

    # when
    with pytest.raises(ValueError, match="User with this email already exist*"):
        step.__call__(context, next_step)

    # then
    assert not next_step.called

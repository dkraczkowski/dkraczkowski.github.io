import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Dict, TextIO, Any
from unittest.mock import MagicMock

import pytest

from example.user_creation import UserCreationStep


@pytest.mark.sqlite_db(data="users.yaml")
def test_can_save_user_no_duplications(sqlite_db: Connection) -> None:
    # given
    step = UserCreationStep(sqlite_db)
    next_step = MagicMock()

    @dataclass
    class Context:
        file: TextIO
        record: Dict[str, Any]
        imported_records: int = 0

    context_data = {
        "FirstName": "Bob",
        "LastName": "Bobber",
        "Email": "test@test.com",
        "Age": 12,
    }

    context = Context(MagicMock(), context_data)

    # when
    step.__call__(context, next_step)

    # then
    assert next_step.called
    cursor = sqlite_db.cursor()
    result = cursor.execute("SELECT *FROM users WHERE email = ?", [context_data["Email"]])
    result.row_factory = sqlite3.Row
    data = dict(result.fetchone())

    assert data == {
        "id": 2,
        "first_name": context_data["FirstName"],
        "last_name": context_data["LastName"],
        "email": context_data["Email"],
        "age": context_data["Age"]
    }



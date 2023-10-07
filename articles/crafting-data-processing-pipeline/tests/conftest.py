from os import path
from pathlib import Path
from sqlite3 import Connection, connect

import pytest
import yaml


@pytest.fixture
def test_dir() -> Path:
    return Path(path.join(path.dirname(__file__)))


@pytest.fixture
def fixture_dir(test_dir: Path) -> Path:
    return test_dir / "fixtures"


@pytest.fixture
def sqlite_db(fixture_dir: Path, request) -> Connection:
    marker = request.node.get_closest_marker("sqlite_db")
    connection = connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            age INTEGER
        )
    """)
    if marker and "data" in marker.kwargs:
        data_file = (fixture_dir / marker.kwargs["data"]).open(mode="r")
        users = yaml.safe_load(data_file)
        for user in users:
            cursor.execute(
                """
                   INSERT INTO users (first_name, last_name, email, age)
                   VALUES (?, ?, ?, ?)
                """,
                (user["first_name"], user["last_name"], user["email"], user["age"])
            )

    return connection

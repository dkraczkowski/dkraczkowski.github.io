from dataclasses import dataclass
from typing import Protocol, runtime_checkable, TextIO, TypedDict, Union


class UserRecord(TypedDict, total=False):
    Email: str
    Name: str
    Age: Union[str, int]
    FirstName: str
    LastName: str


@runtime_checkable
class Context(Protocol):
    file: TextIO
    record: UserRecord
    total_records: int
    imported_records: int


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    age: int

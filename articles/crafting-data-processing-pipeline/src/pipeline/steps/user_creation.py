from dataclasses import asdict
from sqlite3 import Connection

from pipeline.pipeline import NextStep
from pipeline.steps.context import Context, User


class UserCreationStep:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def __call__(self, context: Context, next_step: NextStep) -> None:
        user = User(
            id=0,
            first_name=context.record["FirstName"],
            last_name=context.record["LastName"],
            email=context.record["Email"],
            age=context.record["Age"],
        )

        self._persist_user(user)
        context.imported_records += 1
        next_step(context)

    def _persist_user(self, user: User) -> None:
        db_record = asdict(user)
        cursor = self._connection.cursor()
        cursor.execute(
            """INSERT INTO users (first_name, last_name, email, age)
            VALUES (?, ?, ?, ?)""",
            (db_record["first_name"], db_record["last_name"], db_record["email"], db_record["age"])
        )
        user.id = int(cursor.lastrowid)  # naive id generation


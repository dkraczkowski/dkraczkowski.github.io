from uuid import UUID


class Id:
    def __init__(self, value: str = "") -> None:
        if value:
            self.value = UUID(value, version=4)


class Entity:
    def __init__(self):
        self._id = Id()

    @property
    def id(self) -> Id:
        return self._id

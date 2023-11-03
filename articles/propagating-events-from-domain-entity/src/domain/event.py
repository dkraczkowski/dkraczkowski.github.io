from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class DomainEvent(ABC):
    def __init__(self) -> None:
        self.created_at = datetime.now()
        self.id = uuid4()

    @property
    @abstractmethod
    def namespace(self) -> str:
        ...

    @property
    def name(self) -> str:
        return f"{self.namespace}.{self.__class__.__name__}"

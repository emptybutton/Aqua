from abc import ABC, abstractmethod
from typing import Optional

from src.aqua.domain import entities


class Users(ABC):
    @abstractmethod
    def add(self, user: entities.User) -> None:
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[entities.User]:
        ...


class Records(ABC):
    @abstractmethod
    def add(self, record: entities.Record) -> None:
        ...

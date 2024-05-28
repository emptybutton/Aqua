from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from src.auth.domain import entities
from src.auth.domain import value_objects


class Users(ABC):
    @abstractmethod
    def add(self, user: entities.User) -> None:
        ...

    @abstractmethod
    def has_with_name(
        self,
        username: value_objects.Username
    ) -> Optional[entities.User]:
        ...


_Value = TypeVar("_Value")


class Container(Generic[_Value], ABC):
    @abstractmethod
    def get(self) -> _Value:
        ...

    @abstractmethod
    def set(self, value: _Value) -> None:
        ...

from abc import ABC, abstractmethod
from typing import TypeVar, Generic


_ValueT = TypeVar("_ValueT")


class Values(Generic[_ValueT], ABC):
    @abstractmethod
    def add(self, value: _ValueT) -> None: ...

    @abstractmethod
    def remove(self, value: _ValueT) -> None: ...

    @abstractmethod
    def has(self, value: _ValueT) -> bool: ...

from typing import TypeVar, Generic

from src.shared.domain.ports.repos import Values


_ValueT = TypeVar("_ValueT")


class NoValues(Generic[_ValueT], Values[_ValueT]):
    def add(self, _: _ValueT) -> None:
        pass

    def remove(self, _: _ValueT) -> None:
        pass

    def has(self, _: _ValueT) -> bool:
        return False

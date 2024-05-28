from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TypeVar, Generic


_ValueT = TypeVar("_ValueT")


class UoW(Generic[_ValueT], AbstractAsyncContextManager["UoW[_ValueT]"]):
    async def __aenter__(self) -> "UoW[_ValueT]":
        return self

    @abstractmethod
    def register_new(self, value: _ValueT) -> None:
        ...

    @abstractmethod
    def register_dirty(self, value: _ValueT) -> None:
        ...

    @abstractmethod
    def register_deleted(self, value: _ValueT) -> None:
        ...

from copy import copy
from typing import Iterable, Iterator, Generic, TypeVar


_T = TypeVar("_T")


class InMemoryUoW(Generic[_T]):
    def __init__(self, storage: Iterable[_T] = tuple()) -> None:
        self.__storage_before_transaction: list[_T] | None = None
        self._storage: list[_T] = list(storage)

    def __iter__(self) -> Iterator[_T]:
        return iter(map(copy, self._storage))

    def __len__(self) -> int:
        return len(self._storage)

    def __getitem__(self, index: int) -> _T:
        return self._storage[index]

    def begin(self) -> None:
        assert self.__storage_before_transaction is None
        self.__storage_before_transaction = list(self._storage)

    def rollback(self) -> None:
        assert self.__storage_before_transaction is not None
        self._storage = self.__storage_before_transaction

    def commit(self) -> None:
        assert self.__storage_before_transaction is not None
        self.__storage_before_transaction = None

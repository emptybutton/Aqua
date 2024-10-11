from collections import deque
from copy import copy
from typing import Generic, Iterable, Iterator, TypeVar


_T = TypeVar("_T")


class TransactionalContainer(Generic[_T]):
    class Error(Exception): ...

    class NoTrasactionError(Error): ...

    def __init__(self, storage: Iterable[_T] = tuple()) -> None:
        self.__storage_snapshot_stack: deque[list[_T]] = deque()
        self._storage: list[_T] = list(storage)

    def __iter__(self) -> Iterator[_T]:
        return iter(map(copy, self._storage))

    def __len__(self) -> int:
        return len(self._storage)

    def __getitem__(self, index: int) -> _T:
        return copy(self._storage[index])

    def begin(self) -> None:
        self.__storage_snapshot_stack.append(list(self._storage))

    def rollback(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise TransactionalContainer.NoTrasactionError

        self._storage = storage_snapshot

    def commit(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise TransactionalContainer.NoTrasactionError

from abc import ABC
from collections import deque
from copy import deepcopy
from typing import Generic, TypeVar


_Storage = TypeVar("_Storage")


class TransactionalContainer(Generic[_Storage], ABC):
    class Error(Exception): ...

    class NoTrasactionError(Error): ...

    _storage: _Storage

    def __init__(self) -> None:
        self.__storage_snapshot_stack: deque[_Storage] = deque()

    @property
    def storage(self) -> _Storage:
        return deepcopy(self._storage)

    def begin(self) -> None:
        self.__storage_snapshot_stack.append(deepcopy(self._storage))

    def rollback(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise TransactionalContainer.NoTrasactionError

        self._storage = storage_snapshot

    def commit(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise TransactionalContainer.NoTrasactionError

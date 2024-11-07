from abc import ABC
from collections import deque
from copy import deepcopy


class Error(Exception): ...


class NoTrasactionError(Error): ...


class TransactionalInMemoryStorage[StorageT](ABC):
    _storage: StorageT

    def __init__(self) -> None:
        self.__storage_snapshot_stack: deque[StorageT] = deque()

    @property
    def storage(self) -> StorageT:
        return deepcopy(self._storage)

    def begin(self) -> None:
        self.__storage_snapshot_stack.append(deepcopy(self._storage))

    def rollback(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise NoTrasactionError

        self._storage = storage_snapshot

    def commit(self) -> None:
        storage_snapshot = self.__storage_snapshot_stack.pop()

        if storage_snapshot is None:
            raise NoTrasactionError
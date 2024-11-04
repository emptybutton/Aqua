from types import TracebackType
from typing import Any, Self, Type

from aqua.application.ports.transactions import Transaction, TransactionFor
from aqua.infrastructure.periphery.storages.transactional_storage import (
    TransactionalInMemoryStorage,
)


class InMemoryStorageTransaction(Transaction):
    def __init__(self, storage: TransactionalInMemoryStorage[Any]) -> None:
        self.__is_rollbacked = False
        self.__storage = storage

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        self.__storage.rollback()

    async def __aenter__(self) -> Self:
        self.__storage.begin()
        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.__is_rollbacked:
            return error is None

        if error is None:
            self.__storage.commit()
        else:
            self.__storage.rollback()

        return error is None


class InMemoryStorageTransactionFor(
    TransactionFor[TransactionalInMemoryStorage[Any]]
):
    def __call__(
        self, storage: TransactionalInMemoryStorage[Any]
    ) -> InMemoryStorageTransaction:
        return InMemoryStorageTransaction(storage)

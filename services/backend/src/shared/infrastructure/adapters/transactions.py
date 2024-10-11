from types import TracebackType
from typing import Any, Self, Type

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncSessionTransaction,
    AsyncTransaction,
)

from shared.application.ports import transactions
from shared.infrastructure.periphery import uows
from shared.infrastructure.periphery.containers import TransactionalContainer


class DBConnectionTransaction(transactions.Transaction):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection
        self.__is_rollbacked = False

    @property
    def connection(self) -> AsyncConnection:
        return self.__connection

    @property
    def __commiter(self) -> AsyncConnection | AsyncTransaction:
        savepoint = self.__connection.get_nested_transaction()
        if savepoint is not None:
            return savepoint

        transaction = self.__connection.get_transaction()
        if transaction is not None:
            return transaction

        return self.__connection

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        await self.__commiter.rollback()

    async def __aenter__(self) -> Self:
        in_transaction = self.__connection.in_transaction()
        in_nested_transaction = self.__connection.in_nested_transaction()

        if in_transaction or in_nested_transaction:
            await self.__connection.begin_nested()
        else:
            await self.__connection.begin()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.__is_rollbacked:
            return True

        if error is None:
            await self.__commiter.commit()
        else:
            await self.__commiter.rollback()

        return error is None


class DBConnectionTransactionFactory(transactions.TransactionFactory[Any]):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    def __call__(self, _: Any) -> DBConnectionTransaction:  # noqa: ANN401
        return DBConnectionTransaction(self.__connection)


class TransactionalContainerTransaction(transactions.Transaction):
    def __init__(
        self, container: TransactionalContainer[Any]
    ) -> None:
        self.__is_rollbacked = False
        self.__container = container

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        self.__container.rollback()

    async def __aenter__(self) -> Self:
        self.__container.begin()
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
            self.__container.commit()
        else:
            self.__container.rollback()

        return error is None


class TransactionalContainerTransactionFactory(
    transactions.TransactionFactory[TransactionalContainer[Any]]
):
    def __call__(
        self, container: TransactionalContainer[Any],
    ) -> TransactionalContainerTransaction:
        return TransactionalContainerTransaction(container)


class DBTransaction(transactions.Transaction):
    """deprecated: use `DBConnectionTransaction`"""

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__is_rollbacked = False

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @property
    def __commiter(self) -> AsyncSession | AsyncSessionTransaction:
        sync_savepoint = self.__session.sync_session.get_nested_transaction()
        if sync_savepoint is not None:
            savepoint = AsyncSessionTransaction(self.__session, nested=True)
            savepoint.sync_transaction = sync_savepoint

            return savepoint

        sync_transaction = self.__session.sync_session.get_transaction()
        if sync_transaction is not None:
            transaction = AsyncSessionTransaction(self.__session, nested=False)
            transaction.sync_transaction = sync_transaction

            return transaction

        return self.__session

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        await self.__commiter.rollback()

    async def __aenter__(self) -> Self:
        in_transaction = self.__session.in_transaction()
        in_nested_transaction = self.__session.in_nested_transaction()

        if in_transaction or in_nested_transaction:
            await self.__session.begin_nested()
        else:
            await self.__session.begin()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.__is_rollbacked:
            return True

        if error is None:
            await self.__commiter.commit()
        else:
            await self.__commiter.rollback()

        return error is None


class DBTransactionFactory(transactions.TransactionFactory[Any]):
    """deprecated: use `DBConnectionTransactionFactory"""

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __call__(self, _: Any) -> DBTransaction:  # noqa: ANN401
        return DBTransaction(self.__session)


class InMemoryUoWTransaction(transactions.Transaction):
    """deprecated: use `TransactionalContainerTransaction"""

    def __init__(self, uow: uows.InMemoryUoW[Any]) -> None:
        self.__is_rollbacked = False
        self.__uow = uow

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        self.__uow.rollback()

    async def __aenter__(self) -> Self:
        self.__uow.begin()
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
            self.__uow.commit()
        else:
            self.__uow.rollback()

        return error is None


class InMemoryUoWTransactionFactory(transactions.TransactionFactory[Any]):
    """deprecated: use `TransactionalContainerTransactionFactory"""

    def __call__(self, uow: Any) -> InMemoryUoWTransaction:  # noqa: ANN401
        assert isinstance(uow, uows.InMemoryUoW)
        return InMemoryUoWTransaction(uow)

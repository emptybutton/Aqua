from types import TracebackType
from typing import Self, Type

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncTransaction

from aqua.application.ports.transactions import Transaction, TransactionFor
from aqua.infrastructure.adapters.repos.db.users import DBUsers


class DBTransaction(Transaction):
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


class DBTransactionForDBUsers(TransactionFor[DBUsers]):
    def __call__(self, db_users: DBUsers) -> DBTransaction:
        return DBTransaction(db_users.connection)

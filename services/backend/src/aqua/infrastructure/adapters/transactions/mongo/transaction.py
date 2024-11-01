from types import TracebackType
from typing import Self, Type

from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.transactions import Transaction, TransactionFor
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers


class NestedTransactionError(Exception): ...


class MongoTransaction(Transaction):
    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session
        self.__is_completed = False

    async def rollback(self) -> None:
        self.__is_completed = True
        await self.__session.abort_transaction()

    async def __aenter__(self) -> Self:
        if self.__session.in_transaction:
            raise NestedTransactionError

        self.__is_completed = False
        await self.__session.start_transaction()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if not self.__is_completed:
            await self.__session.commit_transaction()


class MongoTransactionForMongoUsers(TransactionFor[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoTransaction:
        return MongoTransaction(mongo_users.session)

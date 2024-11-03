from typing import Annotated, AsyncIterable

from dishka import FromComponent, Provider, Scope, from_context, provide
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as MongoSession,
)
from sqlalchemy.ext.asyncio import AsyncConnection as SAConnection
from sqlalchemy.ext.asyncio import AsyncSession as SASession

from aqua.application.ports.loggers import Logger
from aqua.infrastructure.adapters.loggers.structlog.dev_logger import (
    StructlogDevLogger,
)
from aqua.infrastructure.adapters.loggers.structlog.prod_logger import (
    StructlogProdLogger,
)
from aqua.infrastructure.adapters.mappers.db.day_mapper import DBDayMapperTo
from aqua.infrastructure.adapters.mappers.db.record_mapper import (
    DBRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.db.user_mapper import DBUserMapperTo
from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapperTo,
)
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.adapters.transactions.db.transaction import (
    DBTransactionForDBUsers,
)
from aqua.infrastructure.adapters.transactions.mongo.transaction import (
    MongoTransactionForMongoUsers,
)
from aqua.infrastructure.adapters.views.db.day_view_from import (
    DBDayViewFrom,
)
from aqua.infrastructure.adapters.views.db.user_view_from import (
    DBUserViewFrom,
)
from aqua.infrastructure.adapters.views.in_memory.cancellation_view_of import (
    InMemoryCancellationViewOf,
)
from aqua.infrastructure.adapters.views.in_memory.registration_view_of import (
    InMemoryRegistrationViewOf,
)
from aqua.infrastructure.adapters.views.in_memory.writing_view_of import (
    InMemoryWritingViewOf,
)
from aqua.infrastructure.adapters.views.mongo.day_view_from import (
    DBDayViewFromMongoUsers,
)
from aqua.infrastructure.adapters.views.mongo.user_view_from import (
    DBUserViewFromMongoUsers,
)
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.storages.mongo.clients import (
    client_with,
)
from shared.infrastructure.periphery.envs import Env


class NoConncetionError(Exception): ...


class ConnectionProvider(Provider):
    component = "db_connections"

    session = from_context(provides=SASession | None, scope=Scope.REQUEST)
    connection = from_context(provides=SAConnection | None, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_connection(
        self, session: SASession | None, connection: SAConnection | None
    ) -> SAConnection:
        if connection is not None:
            return connection

        if session is None:
            raise NoConncetionError

        bind = session.bind

        if not isinstance(bind, SAConnection):
            raise NoConncetionError

        return bind

    @provide(scope=Scope.APP)
    async def get_client(self) -> AsyncIterable[AsyncMongoClient[Document]]:
        client = client_with()
        yield client
        await client.close()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, client: AsyncMongoClient[Document]
    ) -> AsyncIterable[MongoSession]:
        async with client.start_session() as session:
            yield session


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_logger(self) -> Logger:
        return StructlogDevLogger() if Env.for_dev else StructlogProdLogger()


class MapperProvider(Provider):
    component = "mappers"

    @provide(scope=Scope.APP)
    def get_day_mapper_to(self) -> DBDayMapperTo:
        return DBDayMapperTo()

    @provide(scope=Scope.APP)
    def get_user_mapper_to(self) -> DBUserMapperTo:
        return DBUserMapperTo()

    @provide(scope=Scope.APP)
    def get_record_mapper_to(self) -> DBRecordMapperTo:
        return DBRecordMapperTo()

    @provide(scope=Scope.APP)
    def get_mongo_day_mapper_to(self) -> MongoDayMapperTo:
        return MongoDayMapperTo()

    @provide(scope=Scope.APP)
    def get_mongo_user_mapper_to(self) -> MongoUserMapperTo:
        return MongoUserMapperTo()

    @provide(scope=Scope.APP)
    def get_mongo_record_mapper_to(self) -> MongoRecordMapperTo:
        return MongoRecordMapperTo()


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(
        self,
        connection: Annotated[SAConnection, FromComponent("db_connections")],
    ) -> DBUsers:
        return DBUsers(connection)

    @provide(scope=Scope.REQUEST)
    def get_mongo_users(
        self,
        session: Annotated[MongoSession, FromComponent("db_connections")],
    ) -> MongoUsers:
        return MongoUsers(session)


class TransactionProvider(Provider):
    component = "transactions"

    @provide(scope=Scope.APP)
    def get_transaction_for_users(self) -> DBTransactionForDBUsers:
        return DBTransactionForDBUsers()

    @provide(scope=Scope.APP)
    def get_mongo_transaction_for_mongo_users(
        self,
    ) -> MongoTransactionForMongoUsers:
        return MongoTransactionForMongoUsers()


class ViewProvider(Provider):
    component = "views"

    @provide(scope=Scope.APP)
    def get_day_view_from(self) -> DBDayViewFrom:
        return DBDayViewFrom()

    @provide(scope=Scope.APP)
    def get_user_view_from(self) -> DBUserViewFrom:
        return DBUserViewFrom()

    @provide(scope=Scope.APP)
    def get_day_view_from_mongo_users(self) -> DBDayViewFromMongoUsers:
        return DBDayViewFromMongoUsers()

    @provide(scope=Scope.APP)
    def get_user_view_from_mongo_users(self) -> DBUserViewFromMongoUsers:
        return DBUserViewFromMongoUsers()

    @provide(scope=Scope.APP)
    def get_cancellation_view_of(self) -> InMemoryCancellationViewOf:
        return InMemoryCancellationViewOf()

    @provide(scope=Scope.APP)
    def get_registration_view_of(self) -> InMemoryRegistrationViewOf:
        return InMemoryRegistrationViewOf()

    @provide(scope=Scope.APP)
    def get_writing_view_of(self) -> InMemoryWritingViewOf:
        return InMemoryWritingViewOf()

from typing import Annotated, AsyncIterable

from dishka import FromComponent, Provider, Scope, provide
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.loggers import Logger
from aqua.infrastructure.adapters.loggers.structlog.dev_logger import (
    StructlogDevLogger,
)
from aqua.infrastructure.adapters.loggers.structlog.prod_logger import (
    StructlogProdLogger,
)
from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapperTo,
)
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.adapters.transactions.mongo.transaction import (
    MongoTransactionForMongoUsers,
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
from aqua.infrastructure.periphery.pymongo.clients import client_with
from aqua.infrastructure.periphery.pymongo.document import Document
from shared.infrastructure.periphery.envs import Env


class NoConncetionError(Exception): ...


class MongoProvider(Provider):
    component = "mongo"

    @provide(scope=Scope.APP)
    async def get_client(self) -> AsyncIterable[AsyncMongoClient[Document]]:
        client = client_with()
        yield client
        await client.close()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, client: AsyncMongoClient[Document]
    ) -> AsyncIterable[AsyncClientSession]:
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
    def get_mongo_users(
        self, session: Annotated[AsyncClientSession, FromComponent("mongo")]
    ) -> MongoUsers:
        return MongoUsers(session)


class TransactionProvider(Provider):
    component = "transactions"

    @provide(scope=Scope.APP)
    def get_mongo_transaction_for_mongo_users(
        self,
    ) -> MongoTransactionForMongoUsers:
        return MongoTransactionForMongoUsers()


class ViewProvider(Provider):
    component = "views"

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

from typing import Annotated, Iterable

from dishka import FromComponent, Provider, Scope, from_context, provide
from pymongo import AsyncClientSession

from aqua.application.ports.loggers import Logger
from aqua.infrastructure.adapters.loggers.structlog.dev_logger import (
    StructlogDevLogger,
)
from aqua.infrastructure.adapters.loggers.structlog.prod_logger import (
    StructlogProdLogger,
)
from aqua.infrastructure.adapters.mappers.db.day_mapper import MongoDayMapperTo
from aqua.infrastructure.adapters.mappers.db.record_mapper import (
    DBRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.db.user_mapper import MongoUserMapperTo
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.transactions.db.transaction import (
    DBTransactionForDBUsers,
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
from aqua.infrastructure.periphery.storages import mongo
from shared.infrastructure.periphery.envs import Env


class NoConncetionError(Exception): ...


class MongoSessionProvider(Provider):
    component = "mongo_sessions"

    @provide(scope=Scope.REQUEST)
    def get_session(self) -> Iterable[AsyncClientSession]:
        async with mongo.clients.client.start_session() as session:
            yield session


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_logger(self) -> Logger:
        return StructlogDevLogger() if Env.for_dev else StructlogProdLogger()


class MapperProvider(Provider):
    component = "mappers"

    @provide(scope=Scope.APP)
    def get_day_mapper_to(self) -> ЬщтпщDayMapperTo:
        return DBDayMapperTo()

    @provide(scope=Scope.APP)
    def get_user_mapper_to(self) -> DBUserMapperTo:
        return DBUserMapperTo()

    @provide(scope=Scope.APP)
    def get_record_mapper_to(self) -> DBRecordMapperTo:
        return DBRecordMapperTo()


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(
        self,
        connection: Annotated[AsyncConnection, FromComponent("db_connections")],
    ) -> DBUsers:
        return DBUsers(connection)


class TransactionProvider(Provider):
    component = "transactions"

    @provide(scope=Scope.APP)
    def get_transaction_for_users(self) -> DBTransactionForDBUsers:
        return DBTransactionForDBUsers()


class ViewProvider(Provider):
    component = "views"

    @provide(scope=Scope.APP)
    def get_day_view_from(self) -> DBDayViewFrom:
        return DBDayViewFrom()

    @provide(scope=Scope.APP)
    def get_user_view_from(self) -> DBUserViewFrom:
        return DBUserViewFrom()

    @provide(scope=Scope.APP)
    def get_cancellation_view_of(self) -> InMemoryCancellationViewOf:
        return InMemoryCancellationViewOf()

    @provide(scope=Scope.APP)
    def get_registration_view_of(self) -> InMemoryRegistrationViewOf:
        return InMemoryRegistrationViewOf()

    @provide(scope=Scope.APP)
    def get_writing_view_of(self) -> InMemoryWritingViewOf:
        return InMemoryWritingViewOf()

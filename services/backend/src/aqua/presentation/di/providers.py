from typing import Annotated

from dishka import FromComponent, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

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
from shared.infrastructure.periphery.envs import Env


type _ConncetionFromDishka = Annotated[
    AsyncConnection, FromComponent("db_connections")
]


class NoConncetionError(Exception): ...


class ConnectionProvider(Provider):
    component = "db_connections"

    session = from_context(provides=AsyncSession | None, scope=Scope.REQUEST)
    connection = from_context(
        provides=AsyncConnection | None, scope=Scope.REQUEST
    )

    @provide(scope=Scope.REQUEST)
    def get_connection(
        self, session: AsyncSession | None, connection: AsyncConnection | None
    ) -> AsyncConnection:
        if connection is not None:
            return connection

        if session is None:
            raise NoConncetionError

        bind = session.bind

        if not isinstance(bind, AsyncConnection):
            raise NoConncetionError

        return bind


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


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(self, connection: _ConncetionFromDishka) -> DBUsers:
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

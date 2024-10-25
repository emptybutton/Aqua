from typing import Annotated

from dishka import FromComponent, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from aqua.application import ports
from aqua.infrastructure import adapters
from shared.infrastructure.periphery.envs import Env


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(
        self, session: Annotated[AsyncSession, FromComponent("db_connections")]
    ) -> adapters.repos.DBUsers:
        return adapters.repos.DBUsers(session)

    @provide(scope=Scope.REQUEST)
    def get_records(
        self, session: Annotated[AsyncSession, FromComponent("db_connections")]
    ) -> adapters.repos.DBRecords:
        return adapters.repos.DBRecords(session)

    @provide(scope=Scope.REQUEST)
    def get_days(
        self, session: Annotated[AsyncSession, FromComponent("db_connections")]
    ) -> adapters.repos.DBDays:
        return adapters.repos.DBDays(session)


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_logger(self) -> ports.loggers.Logger:
        if Env.for_dev:
            return adapters.loggers.StructlogDevLogger()

        return adapters.loggers.StructlogProdLogger()


class Error(Exception): ...


class NoSessionError(Error): ...


class NoSessionAndNoConncetionError(Error): ...


class SessionWithoutConncetionError(Error): ...


class MultilevelPeripheryProvider(Provider):
    component = "db_connections"

    session = from_context(provides=AsyncSession | None, scope=Scope.REQUEST)
    connection = from_context(
        provides=AsyncConnection | None, scope=Scope.REQUEST
    )

    @provide(scope=Scope.REQUEST)
    def get_session(self, session: AsyncSession | None) -> AsyncSession:
        if session is None:
            raise NoSessionError

        return session

    @provide(scope=Scope.REQUEST)
    def get_connection(
        self, session: AsyncSession | None, connection: AsyncConnection | None
    ) -> AsyncConnection:
        if connection is not None:
            return connection

        if session is not None:
            bind = session.bind

            if not isinstance(bind, AsyncConnection):
                raise SessionWithoutConncetionError

            return bind

        raise NoSessionAndNoConncetionError

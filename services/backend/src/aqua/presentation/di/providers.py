from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.infrastructure import adapters


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBUsers:
        return adapters.repos.DBUsers(session)

    @provide(scope=Scope.REQUEST)
    def get_records(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBRecords:
        return adapters.repos.DBRecords(session)

    @provide(scope=Scope.REQUEST)
    def get_days(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBDays:
        return adapters.repos.DBDays(session)


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_logger(
        self,
    ) -> adapters.loggers.LoguruLogger:
        return adapters.loggers.LoguruLogger()

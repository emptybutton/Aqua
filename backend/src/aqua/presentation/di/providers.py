from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application import ports
from aqua.infrastructure import adapters


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_users(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> ports.repos.Users:
        return adapters.repos.DBUsers(session)

    @provide(scope=Scope.REQUEST)
    def get_records(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> ports.repos.Records:
        return adapters.repos.DBRecords(session)

    @provide(scope=Scope.REQUEST)
    def get_days(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> ports.repos.Days:
        return adapters.repos.DBDays(session)

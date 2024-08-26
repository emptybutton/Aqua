from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application import ports
from auth.infrastructure import adapters
from shared.infrastructure.periphery.envs import Env


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_a(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBUsers:
        return adapters.repos.DBUsers(session)

    @provide(scope=Scope.REQUEST)
    def get_b(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBSessions:
        return adapters.repos.DBSessions(session)


class SerializerProvider(Provider):
    component = "serializers"

    @provide(scope=Scope.APP)
    def get_b(self) -> adapters.serializers.SHA256PasswordHasher:
        return adapters.serializers.SHA256PasswordHasher()


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_a(self) -> ports.loggers.Logger:
        if Env.for_dev:
            return adapters.loggers.StructlogDevLogger()

        return adapters.loggers.StructlogProdLogger()

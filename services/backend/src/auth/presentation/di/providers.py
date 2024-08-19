from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure import adapters


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
    def get_b(self) -> adapters.serializers.PasswordSerializer:
        return adapters.serializers.PasswordSerializer()


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_a(self) -> adapters.loggers.StructlogDevLogger:
        return adapters.loggers.StructlogDevLogger()

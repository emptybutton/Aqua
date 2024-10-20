from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from shared.infrastructure.periphery.db import engines
from shared.infrastructure.periphery.envs import Env


class PeripheryProvider(Provider):
    component = "periphery"

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        connection = AsyncConnection(engines.postgres_engine)

        async with connection:
            yield AsyncSession(connection, autobegin=False)


class LogerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_aqua_logger(
        self,
    ) -> ports.loggers.AquaLogger[adapters.clients.aqua.AquaFacade]:
        if Env.for_dev:
            return adapters.loggers.AquaFacadeDevLogger()

        return adapters.loggers.AquaFacadeProdLogger()

    @provide(scope=Scope.APP)
    def get_auth_logger(
        self,
    ) -> ports.loggers.AuthLogger[adapters.clients.auth.AuthFacade]:
        if Env.for_dev:
            return adapters.loggers.AuthFacadeDevLogger()

        return adapters.loggers.AuthFacadeProdLogger()


class ClientProvider(Provider):
    component = "clients"

    @provide(scope=Scope.REQUEST)
    def get_aqua(self) -> adapters.clients.aqua.AquaFacade:
        return adapters.clients.aqua.AquaFacade()

    @provide(scope=Scope.REQUEST)
    def get_auth(self) -> adapters.clients.auth.AuthFacade:
        return adapters.clients.auth.AuthFacade()

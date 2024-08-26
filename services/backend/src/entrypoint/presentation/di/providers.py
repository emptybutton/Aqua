from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from shared.infrastructure.periphery.db import sessions
from shared.infrastructure.periphery.envs import Env


class PeripheryProvider(Provider):
    component = "periphery"

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        async with sessions.postgres_session_factory() as session:
            yield session


class LogerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_aqua_logger(
        self,
    ) -> ports.loggers.AquaLogger[adapters.clients.AquaFacade]:
        if Env.for_dev:
            return adapters.loggers.AquaFacadeDevLogger()

        return adapters.loggers.AquaFacadeProdLogger()

    @provide(scope=Scope.APP)
    def get_auth_logger(
        self,
    ) -> ports.loggers.AuthLogger[adapters.clients.AuthFacade]:
        if Env.for_dev:
            return adapters.loggers.AuthFacadeDevLogger()

        return adapters.loggers.AuthFacadeProdLogger()


class ClientProvider(Provider):
    component = "clients"

    @provide(scope=Scope.REQUEST)
    def get_aqua(self) -> adapters.clients.AquaFacade:
        return adapters.clients.AquaFacade()

    @provide(scope=Scope.REQUEST)
    def get_auth(self) -> adapters.clients.AuthFacade:
        return adapters.clients.AuthFacade()

from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from entrypoint.infrastructure import adapters
from shared.infrastructure.periphery.db import sessions


class PeripheryProvider(Provider):
    component = "periphery"

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        async with sessions.postgres_session_factory() as session:
            yield session


class LogerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_aqua_logger(self) -> adapters.loggers.AquaFacadeDevLogger:
        return adapters.loggers.AquaFacadeDevLogger()

    @provide(scope=Scope.APP)
    def get_auth_logger(self) -> adapters.loggers.AuthFacadeDevLogger:
        return adapters.loggers.AuthFacadeDevLogger()


class ClientProvider(Provider):
    component = "clients"

    @provide(scope=Scope.REQUEST)
    def get_aqua(self) -> adapters.clients.AquaFacade:
        return adapters.clients.AquaFacade()

    @provide(scope=Scope.REQUEST)
    def get_auth(self) -> adapters.clients.AuthFacade:
        return adapters.clients.AuthFacade()

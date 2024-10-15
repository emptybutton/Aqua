from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application import ports
from auth.infrastructure.adapters import (
    gateways,
    loggers,
    mappers,
    repos,
    views,
)
from shared.infrastructure.periphery.envs import Env


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_a(
        self, connection: Annotated[AsyncConnection, FromComponent("periphery")]
    ) -> repos.db.DBAccounts:
        return repos.db.DBAccounts(connection)


class MepperProvider(Provider):
    component = "mappers"

    @provide(scope=Scope.APP)
    def get_a(self) -> mappers.db.account.DBAccountMapperFactory:
        return mappers.db.account.DBAccountMapperFactory()

    @provide(scope=Scope.APP)
    def get_b(self) -> mappers.db.account_name.DBAccountNameMapperFactory:
        return mappers.db.account_name.DBAccountNameMapperFactory()

    @provide(scope=Scope.APP)
    def get_c(self) -> mappers.db.session.DBSessionMapperFactory:
        return mappers.db.session.DBSessionMapperFactory()


class LoggerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_a(self) -> ports.loggers.Logger:
        if Env.for_dev:
            return loggers.structlog.dev.StructlogDevLogger()

        return loggers.structlog.prod.StructlogProdLogger()


class ViewProvider(Provider):
    component = "views"

    @provide(scope=Scope.APP)
    def get_a(self) -> views.db.DBAccountViewFrom:
        return views.db.DBAccountViewFrom()


class GatewayProvider(Provider):
    component = "gateways"

    @provide(scope=Scope.APP)
    def get_a(self) -> gateways.db.DBGatewayFactory:
        return gateways.db.DBGatewayFactory()

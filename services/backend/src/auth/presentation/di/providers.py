from typing import Annotated, AsyncIterable

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection as SAConnection

from auth.application import ports
from auth.infrastructure.adapters import (
    gateways,
    loggers,
    mappers,
    repos,
    transactions,
    views,
)
from auth.infrastructure.periphery import envs
from auth.infrastructure.periphery.sqlalchemy.engines import postgres_engine


class SqlalchemyProvider(Provider):
    class Error(Exception): ...

    class NoSessionError(Error): ...

    class NoSessionAndNoConncetionError(Error): ...

    class SessionWithoutConncetionError(Error): ...

    component = "sqlalchemy"

    @provide(scope=Scope.REQUEST)
    async def get_connection(self) -> AsyncIterable[SAConnection]:
        async with postgres_engine.connect() as connection:
            yield connection


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_a(
        self, connection: Annotated[SAConnection, FromComponent("sqlalchemy")]
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
        if envs.is_dev:
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


class TransactionProvider(Provider):
    component = "transactions"

    @provide(scope=Scope.REQUEST)
    def get_db_conncetion_transaction(
        self, connection: Annotated[SAConnection, FromComponent("sqlalchemy")]
    ) -> transactions.DBConnectionTransaction:
        return transactions.DBConnectionTransaction(connection)

    @provide(scope=Scope.REQUEST)
    def get_db_conncetion_transaction_factory(
        self, connection: Annotated[SAConnection, FromComponent("sqlalchemy")]
    ) -> transactions.DBConnectionTransactionFactory:
        return transactions.DBConnectionTransactionFactory(connection)

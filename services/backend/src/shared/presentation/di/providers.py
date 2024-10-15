from typing import Annotated

from dishka import FromComponent, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from shared.infrastructure import adapters


class PeripheryProvider(Provider):
    class Error(Exception): ...

    class NoSessionError(Error): ...

    class NoSessionAndNoConncetionError(Error): ...

    component = "periphery"

    session = from_context(
        provides=AsyncSession | None, scope=Scope.REQUEST
    )
    connection = from_context(
        provides=AsyncConnection | None, scope=Scope.REQUEST
    )

    @provide(scope=Scope.REQUEST)
    def get_session(self, session: AsyncSession | None) -> AsyncSession:
        if session is None:
            raise PeripheryProvider.NoSessionError

        return session

    @provide(scope=Scope.REQUEST)
    async def get_connection(
        self, session: AsyncSession | None, connection: AsyncConnection | None
    ) -> AsyncConnection:
        if connection is not None:
            return connection

        if session is not None:
            return await session.connection()

        raise PeripheryProvider.NoSessionAndNoConncetionError


class TransactionProvider(Provider):
    component = "transactions"

    @provide(scope=Scope.REQUEST)
    def get_transaction(
        self, session: Annotated[AsyncSession, FromComponent("periphery")]
    ) -> adapters.transactions.DBTransaction:
        return adapters.transactions.DBTransaction(session)

    @provide(scope=Scope.REQUEST)
    def get_transaction_factory(
        self, session: Annotated[AsyncSession, FromComponent("periphery")]
    ) -> adapters.transactions.DBTransactionFactory:
        return adapters.transactions.DBTransactionFactory(session)

    @provide(scope=Scope.REQUEST)
    def get_db_conncetion_transaction(
        self, connection: Annotated[AsyncConnection, FromComponent("periphery")]
    ) -> adapters.transactions.DBConnectionTransaction:
        return adapters.transactions.DBConnectionTransaction(connection)

    @provide(scope=Scope.REQUEST)
    def get_db_conncetion_transaction_factory(
        self, connection: Annotated[AsyncConnection, FromComponent("periphery")]
    ) -> adapters.transactions.DBConnectionTransactionFactory:
        return adapters.transactions.DBConnectionTransactionFactory(connection)


class IndexProvider(Provider):
    component = "indexes"

    @provide(scope=Scope.APP)
    def get_index_factory(self) -> adapters.indexes.EmptySortingIndexFactory:
        return adapters.indexes.EmptySortingIndexFactory()

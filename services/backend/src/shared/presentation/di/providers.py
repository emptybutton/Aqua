from typing import Annotated

from dishka import FromComponent, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure import adapters


class PeripheryProvider(Provider):
    component = "periphery"

    session = from_context(provides=AsyncSession, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_session(self, session: AsyncSession) -> AsyncSession:
        return session


class TransactionProvider(Provider):
    component = "transactions"

    session = from_context(provides=AsyncSession, scope=Scope.REQUEST)

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

from typing import Annotated, TypeAlias, Callable

from dishka import Provider, provide, Scope, from_context, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from shared.application import ports
from shared.infrastructure import adapters


TransactionFactory: TypeAlias = Callable[..., ports.transactions.Transaction]


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
    def get_transaction_factory(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> TransactionFactory:
        return lambda *_, **__: adapters.transactions.DBTransaction(session)

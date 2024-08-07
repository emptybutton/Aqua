from typing import Type, Self, Any
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from shared.application.ports import transactions


class DBTransaction(transactions.Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def __aenter__(self) -> Self:
        await self._session.begin_nested()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if error is None:
            await self._session.commit()
        else:
            await self._session.rollback()

        return error is None


class DBTransactionFactory(
    transactions.TransactionFactory[Any, DBTransaction],
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def __call__(self, _: Any) -> DBTransaction:  # noqa: ANN401
        return DBTransaction(self._session)

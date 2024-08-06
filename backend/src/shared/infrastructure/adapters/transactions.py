from typing import Optional, Type, Self
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
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if error is None:
            await self._session.commit()
        else:
            await self._session.rollback()

        return error is None

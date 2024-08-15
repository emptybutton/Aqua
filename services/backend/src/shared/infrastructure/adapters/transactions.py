from typing import Type, Self, Any
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from shared.application.ports import transactions


class DBTransaction(transactions.Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__is_rollbacked = False

    @property
    def session(self) -> AsyncSession:
        return self.__session

    async def rollback(self) -> None:
        if self.__session.is_active:
            self.__is_rollbacked = True
            await self.__session.rollback()

    async def __aenter__(self) -> Self:
        await self.__session.begin_nested()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.__is_rollbacked:
            return True

        if error is None:
            await self.__session.commit()
        else:
            await self.__session.rollback()

        return error is None


class DBTransactionFactory(
    transactions.TransactionFactory[Any],
):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __call__(self, _: Any) -> DBTransaction:  # noqa: ANN401
        return DBTransaction(self.__session)

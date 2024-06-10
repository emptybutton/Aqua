from typing import Optional, Type, TypeVar
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncTransaction

from src.shared.application.ports import uows


_ValueT = TypeVar("_ValueT")


class FakeUoW(uows.UoW[_ValueT]):
    def register_new(self, value: _ValueT) -> None: ...

    def register_dirty(self, value: _ValueT) -> None: ...

    def register_deleted(self, value: _ValueT) -> None: ...

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        ...


class TransactionalUoW(FakeUoW[object]):
    __transaction: Optional[AsyncTransaction] = None

    def __init__(
        self,
        connetion: AsyncConnection,
        *,
        closes: bool = True,
    ) -> None:
        self.__connetion = connetion
        self.__closes = closes

    async def __aenter__(self) -> "TransactionalUoW":
        assert not self.__connetion.closed
        assert self.__transaction is None

        self.__transaction = await self.__connetion.begin()

        return self

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        assert self.__transaction is not None

        if error is None:
            await self.__transaction.commit()
        else:
            await self.__transaction.rollback()

        if self.__closes:
            await self.__connetion.close()

        self.__transaction = None

        return error is None

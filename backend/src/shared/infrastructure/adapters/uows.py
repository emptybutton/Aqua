from typing import Optional, Type, TypeVar
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncConnection

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
    __is_nested: bool

    def __init__(
        self,
        connetion: AsyncConnection,
        *,
        closes: bool = True,
    ) -> None:
        self.__connetion = connetion
        self.__closes = closes

        self.__is_nested = self.__connetion.in_transaction()

    async def __aenter__(self) -> "TransactionalUoW":
        assert not self.__connetion.closed

        if self.__connetion.in_transaction():
            return self

        await self.__connetion.begin()

        return self

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        assert not self.__connetion.closed

        if self.__is_nested:
            return error is None

        if error is None:
            await self.__connetion.commit()
        else:
            await self.__connetion.rollback()

        if self.__closes:
            await self.__connetion.close()

        self.__transaction = None

        return error is None

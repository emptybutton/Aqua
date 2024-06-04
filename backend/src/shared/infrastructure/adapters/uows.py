from dataclasses import dataclass
from typing import Optional, Type
from types import TracebackType

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncConnection, AsyncTransaction
)

from src.shared.application.ports import uows


class FakeUoW(uows.UoW[object]):
    def register_new(self, value: object) -> None: ...

    def register_dirty(self, value: object) -> None: ...

    def register_deleted(self, value: object) -> None: ...

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        ...


@dataclass
class TransactionalUoW(FakeUoW):
    __engine: AsyncEngine
    __connetion: Optional[AsyncConnection] = None
    __transaction: Optional[AsyncTransaction] = None

    async def __aenter__(self) -> "TransactionalUoW":
        assert self.__connetion is None
        assert self.__transaction is None

        self.__connetion = self.__engine.connect()
        self.__transaction = await self.__connetion.begin()

        return self

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        assert self.__connetion is not None
        assert self.__transaction is not None

        if error is None:
            await self.__transaction.commit()
        else:
            await self.__transaction.rollback()

        await self.__connetion.close()

        self.__connetion = None
        self.__transaction = None

        return error is None

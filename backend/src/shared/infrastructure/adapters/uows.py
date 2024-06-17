from typing import Optional, Type, TypeVar, Self
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

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


class DBUoW(FakeUoW[_ValueT]):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    async def __aenter__(self) -> Self:
        await self.__session.begin_nested()

        return self

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if error is None:
            await self._finish_work()
            await self.__session.commit()
        else:
            await self.__session.rollback()

        return error is None

    async def _finish_work(self) -> None:
        ...

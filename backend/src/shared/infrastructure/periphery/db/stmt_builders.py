from typing import Self

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession


class STMTBuilder:
    def __init__(self, *, is_in_trasaction: bool) -> None:
        self.__is_in_trasaction = is_in_trasaction

    def select(self, *args: object) -> "SelectBuilder":
        stmt = select(*args)

        if self.__is_in_trasaction:
            stmt = stmt.with_for_update()

        return SelectBuilder(stmt, is_in_trasaction=self.__is_in_trasaction)

    @classmethod
    def of(cls, session: AsyncSession) -> Self:
        return cls(is_in_trasaction=session.is_active)


class SelectBuilder:
    def __init__(self, stmt: Select, *, is_in_trasaction: bool) -> None:
        self.__stmt = stmt
        self.__is_in_trasaction = is_in_trasaction

    def build(self) -> Select:
        return self.__stmt

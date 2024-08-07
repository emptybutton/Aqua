from typing import Self, Any, TypeVar, Generic

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select


_AnyTupleT = TypeVar("_AnyTupleT", bound=tuple[Any, ...])


class STMTBuilder:
    def __init__(self, *, is_in_trasaction: bool) -> None:
        self.__is_in_trasaction = is_in_trasaction

    def select(self, *args: Any) -> "SelectBuilder[_AnyTupleT]":  # noqa: ANN401
        stmt = select(*args)

        if self.__is_in_trasaction:
            stmt = stmt.with_for_update()

        return SelectBuilder(stmt, is_in_trasaction=self.__is_in_trasaction)

    @classmethod
    def of(cls, session: AsyncSession) -> Self:
        return cls(is_in_trasaction=session.is_active)


class SelectBuilder(Generic[_AnyTupleT]):
    def __init__(
        self,
        stmt: Select[_AnyTupleT],
        *,
        is_in_trasaction: bool,
    ) -> None:
        self.__stmt = stmt
        self.__is_in_trasaction = is_in_trasaction

    def build(self) -> Select[_AnyTupleT]:
        return self.__stmt

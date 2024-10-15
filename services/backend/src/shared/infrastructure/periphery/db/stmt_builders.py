from typing import Any, Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.sql.expression import Select


class STMTBuilder:
    def __init__(self, subject: AsyncSession | AsyncConnection) -> None:
        self.__subject = subject

    def select(self, *args: Any) -> "SelectBuilder":  # noqa: ANN401
        stmt = select(*args)

        if self.__is_in_trasaction:
            stmt = stmt.with_for_update()

        return SelectBuilder(stmt)

    @classmethod
    def of(cls, session: AsyncSession) -> Self:
        """deprecated: use `__init__`."""

        return cls(session)

    @property
    def __is_in_trasaction(self) -> bool:
        return (
            self.__subject.in_transaction()
            or self.__subject.in_nested_transaction()
        )


class SelectBuilder:
    def __init__(self, stmt: Select[tuple[Any, ...]]) -> None:
        self.__stmt = stmt

    def build(self) -> Select[tuple[Any, ...]]:
        return self.__stmt

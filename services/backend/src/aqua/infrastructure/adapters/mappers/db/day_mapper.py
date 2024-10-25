from typing import Iterable

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from aqua.application.ports.mappers import DayMapper, DayMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    maybe_result_value_of,
    result_value_of,
    target_value_of,
    water_balance_value_of,
)
from aqua.infrastructure.periphery.sqlalchemy.values import Value, updating
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBDayMapper(DayMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, days: Iterable[Day]) -> None:
        days = frozenset(days)

        if not days:
            return

        stmt = insert(tables.day_table)

        values = list(map(self.__value_of, days))
        await self.__connection.execute(stmt, values)

    async def update_all(self, days: Iterable[Day]) -> None:
        days = frozenset(days)

        if not days:
            return

        stmt = (
            update(tables.day_table)
            .where(tables.day_table.c.id == bindparam("id_"))
            .values(
                user_id=bindparam("user_id_"),
                water_balance=bindparam("water_balance_"),
                target=bindparam("target_"),
                date_=bindparam("date__"),
                pinned_result=bindparam("pinned_result_"),
            )
        )

        values = list(map(self.__value_of, days))
        await self.__connection.execute(stmt, updating(values))

    def __value_of(self, day: Day) -> Value:
        return dict(
            id=day.id,
            user_id=day.user_id,
            water_balance=water_balance_value_of(day.water_balance),
            target=target_value_of(day.target),
            date_=day.date_,
            pinned_result=maybe_result_value_of(day.pinned_result),
            correct_result=result_value_of(day.correct_result),
            result=result_value_of(day.result),
        )


class DBDayMapperTo(DayMapperTo[DBUsers]):
    def __call__(self, db_users: DBUsers) -> DBDayMapper:
        return DBDayMapper(db_users.connection)

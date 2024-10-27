from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection

from aqua.application.ports.repos import Users
from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    glass_of,
    maybe_result_of,
    maybe_weight_of,
    target_of,
    time_of,
    water_balance_of,
    water_of,
)
from aqua.infrastructure.periphery.sqlalchemy.stmt_builders import STMTBuilder
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBUsers(Users):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection
        self.__stmt_builder = STMTBuilder(connection)

    @property
    def connection(self) -> AsyncConnection:
        return self.__connection

    @property
    def stmt_builder(self) -> STMTBuilder:
        return self.__stmt_builder

    async def user_with_id(self, user_id: UUID) -> User | None:
        stmt = (
            self.__stmt_builder.select(
                tables.user_table.c.target.label("user_target"),
                tables.user_table.c.glass.label("user_glass"),
                tables.user_table.c.weight.label("user_weight"),
                tables.record_table.c.id.label("record_id"),
                tables.record_table.c.drunk_water.label("record_drunk_water"),
                tables.record_table.c.recording_time.label(
                    "record_recording_time"
                ),
                tables.record_table.c.is_cancelled.label("is_record_cancelled"),
                tables.day_table.c.id.label("day_id"),
                tables.day_table.c.water_balance.label("day_water_balance"),
                tables.day_table.c.target.label("day_target"),
                tables.day_table.c.date_.label("day_date"),
                tables.day_table.c.pinned_result.label("day_pinned_result"),
            )
            .build()
            .join_from(
                tables.user_table,
                tables.record_table,
                (
                    (tables.user_table.c.id == user_id)
                    & (tables.record_table.c.user_id == user_id)
                ),
            )
            .join(tables.day_table, tables.day_table.c.user_id == user_id)
        )

        result = await self.__connection.execute(stmt)
        rows = result.all()

        if len(rows) == 0:
            return None

        days = Entities[Day]()
        records = Entities[Record]()

        for row in rows:
            day = Day(
                id=row.day_id,
                events=list(),
                user_id=user_id,
                date_=row.day_date,
                target=target_of(row.target),
                water_balance=water_balance_of(row.water_balance),
                pinned_result=maybe_result_of(row.day_pinned_result),
            )
            days.add(day)

        for row in rows:
            record = Record(
                id=row.record_id,
                events=list(),
                user_id=user_id,
                drunk_water=water_of(row.record_drunk_water),
                recording_time=time_of(row.record_recording_time),
                is_cancelled=row.is_record_cancelled,
            )
            records.add(record)

        row = rows[0]

        return User(
            id=user_id,
            events=list(),
            target=target_of(row.user_target),
            glass=glass_of(row.record_drunk_water),
            weight=maybe_weight_of(row.user_weight),
            days=days,
            records=records,
        )

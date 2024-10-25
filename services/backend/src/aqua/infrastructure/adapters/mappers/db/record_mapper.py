from typing import Iterable

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from aqua.application.ports.mappers import RecordMapper, RecordMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    time_value_of,
    water_value_of,
)
from aqua.infrastructure.periphery.sqlalchemy.values import Value, updating
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBRecordMapper(RecordMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, records: Iterable[Record]) -> None:
        records = frozenset(records)

        if not records:
            return

        stmt = insert(tables.record_table)

        values = list(map(self.__value_of, records))
        await self.__connection.execute(stmt, values)

    async def update_all(self, records: Iterable[Record]) -> None:
        records = frozenset(records)

        if not records:
            return

        stmt = (
            update(tables.record_table)
            .where(tables.record_table.c.id == bindparam("id_"))
            .values(
                user_id=bindparam("user_id_"),
                drunk_water=bindparam("drunk_water_"),
                recording_time=bindparam("recording_time_"),
                is_cancelled=bindparam("is_cancelled_"),
            )
        )

        values = list(map(self.__value_of, records))
        await self.__connection.execute(stmt, updating(values))

    def __value_of(self, record: Record) -> Value:
        return dict(
            id=record.id,
            user_id=record.user_id,
            drunk_water=water_value_of(record.drunk_water),
            recording_time=time_value_of(record.recording_time),
            is_cancelled=record.is_cancelled,
        )


class DBRecordMapperTo(RecordMapperTo[DBUsers]):
    def __call__(self, db_users: DBUsers) -> DBRecordMapper:
        return DBRecordMapper(db_users.connection)

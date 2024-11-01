from typing import Iterable

from pymongo import AsyncClientSession

from aqua.application.ports.mappers import RecordMapper, RecordMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.repos.in_memory.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import (
    execute,
    to_map,
    to_push,
)
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    time_value_of,
    water_value_of,
)


class MongoRecordMapper(RecordMapper):
    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, records: Iterable[Record]) -> None:
        operations = (
            to_push(
                self._document_of(record),
                prefix="record",
                id=record.user_id,
                sort=-1,
            )
            for record in records
        )

        await execute(
            operations,
            session=self.__session,
            comment="push user records",
            namespace="db.users",
        )

    async def update_all(self, records: Iterable[Record]) -> None:
        operations = (
            to_map(
                self._document_of(record), prefix="record", id=record.user_id
            )
            for record in records
        )

        await execute(
            operations,
            session=self.__session,
            comment="update user records",
            namespace="db.users",
        )

    def _document_of(self, record: Record) -> Document:
        subid = record.id.hex

        return {
            "_id": record.user_id,
            f"records.{subid}.drunk_water": water_value_of(record.drunk_water),
            f"records.{subid}.recording_time": time_value_of(
                record.recording_time
            ),
            f"records.{subid}.is_cancelled": record.is_cancelled,
        }


class MongoRecordMapperTo(RecordMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoRecordMapper:
        return MongoRecordMapper(mongo_users.session)

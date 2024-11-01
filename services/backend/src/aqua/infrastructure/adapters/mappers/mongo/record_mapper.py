from typing import Iterable

from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.mappers import RecordMapper, RecordMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import (
    ArrayOperations,
    execute,
)
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    time_value_of,
    water_value_of,
)


class MongoRecordMapper(RecordMapper):
    __operations = ArrayOperations(
        namespace="db.users", prefix="record", sort=-1
    )

    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, records: Iterable[Record]) -> None:
        operations = (
            self.__operations.to_push(
                self._document_of(record),
                id=record.user_id,
            )
            for record in records
        )

        await execute(
            operations, session=self.__session, comment="push user records"
        )

    async def update_all(self, records: Iterable[Record]) -> None:
        operations = (
            self.__operations.to_map(
                self._document_of(record), id=record.user_id
            )
            for record in records
        )

        await execute(
            operations, session=self.__session, comment="update user records"
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

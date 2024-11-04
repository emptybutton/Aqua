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
from aqua.infrastructure.periphery.serializing.from_model.to_document import (
    document_time_of,
    document_water_of,
)


class MongoRecordMapper(RecordMapper):
    __operations = ArrayOperations(
        namespace="db.users", prefix="record", sort={"recording_time": -1}
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
        return {
            "_id": record.id,
            "drunk_water": document_water_of(record.drunk_water),
            "recording_time": document_time_of(record.recording_time),
            "is_cancelled": record.is_cancelled,
        }


class MongoRecordMapperTo(RecordMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoRecordMapper:
        return MongoRecordMapper(mongo_users.session)

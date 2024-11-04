from typing import Iterable

from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.mappers import DayMapper, DayMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import (
    ArrayOperations,
    execute,
)
from aqua.infrastructure.periphery.serializing.from_model.to_document import (
    document_result_of,
    document_target_of,
    document_water_balance_of,
    maybe_document_result_of,
)
from aqua.infrastructure.periphery.serializing.from_native.to_document import (
    document_date_of,
)


class MongoDayMapper(DayMapper):
    __operations = ArrayOperations(namespace="db.users", prefix="day")

    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, days: Iterable[Day]) -> None:
        operations = (
            self.__operations.to_push(self._document_of(day), id=day.user_id)
            for day in days
        )

        await execute(
            operations, session=self.__session, comment="push user days"
        )

    async def update_all(self, days: Iterable[Day]) -> None:
        operations = (
            self.__operations.to_map(self._document_of(day), id=day.user_id)
            for day in days
        )

        await execute(
            operations, session=self.__session, comment="update user days"
        )

    def _document_of(self, day: Day) -> Document:
        return {
            "_id": day.id,
            "water_balance": document_water_balance_of(day.water_balance),
            "target": document_target_of(day.target),
            "date": document_date_of(day.date_),
            "pinned_result": maybe_document_result_of(day.pinned_result),
            "correct_result": document_result_of(day.correct_result),
            "result": document_result_of(day.result),
        }


class MongoDayMapperTo(DayMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoDayMapper:
        return MongoDayMapper(mongo_users.session)

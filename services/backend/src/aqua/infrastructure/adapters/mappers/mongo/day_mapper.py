from typing import Iterable

from pymongo import AsyncClientSession

from aqua.application.ports.mappers import DayMapper, DayMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.infrastructure.adapters.repos.in_memory.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import (
    execute,
    to_map,
    to_push,
)
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    maybe_result_value_of,
    result_value_of,
    target_value_of,
    water_balance_value_of,
)


class MongoDayMapper(DayMapper):
    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, days: Iterable[Day]) -> None:
        operations = (
            to_push(self._document_of(day), prefix="day", id=day.user_id)
            for day in days
        )

        await execute(
            operations,
            session=self.__session,
            comment="push user days",
            namespace="db.users",
        )

    async def update_all(self, days: Iterable[Day]) -> None:
        operations = (
            to_map(self._document_of(day), prefix="day", id=day.user_id)
            for day in days
        )

        await execute(
            operations,
            session=self.__session,
            comment="update user days",
            namespace="db.users",
        )

    def _document_of(self, day: Day) -> Document:
        return {
            "_id": day.id,
            "water_balance": water_balance_value_of(
                day.water_balance
            ),
            "target": target_value_of(day.target),
            "date": day.date_,
            "pinned_result": maybe_result_value_of(
                day.pinned_result
            ),
            "correct_result": result_value_of(day.correct_result),
            "result": result_value_of(day.result),
        }


class MongoDayMapperTo(DayMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoDayMapper:
        return MongoDayMapper(mongo_users.session)

from datetime import datetime
from typing import Any
from uuid import UUID

from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.repos import Users
from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.serializing.from_document.to_native import (
    native_date_of,
)
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    glass_of,
    maybe_result_of,
    maybe_weight_of,
    target_of,
    time_of,
    water_balance_of,
    water_of,
)
from aqua.infrastructure.periphery.validation.objects import (
    StrictValidationObject,
)


class MongoUsers(Users):
    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    @property
    def session(self) -> AsyncClientSession:
        return self.__session

    async def user_with_id(self, user_id: UUID) -> User | None:
        document = await self.session.client.db.users.find_one(user_id)

        return None if document is None else self.__loaded_user_from(document)

    def __loaded_user_from(self, document: dict[str, Any]) -> User:
        user_object = StrictValidationObject(document)

        days = Entities[Day]()
        records = Entities[Record]()

        for day_document in user_object["days", list]:
            day_object = StrictValidationObject(day_document)
            day = Day(
                id=day_object["_id", UUID],
                events=list(),
                user_id=user_object["_id", UUID],
                date_=native_date_of(day_object["date", datetime]),
                target=target_of(day_object["target", int]),
                water_balance=water_balance_of(
                    day_object["water_balance", int]
                ),
                pinned_result=maybe_result_of(
                    day_object.n["pinned_result", int]
                ),
            )
            days.add(day)

        for record_document in user_object["records", list]:
            record_object = StrictValidationObject(record_document)
            record = Record(
                id=record_object["_id", UUID],
                events=list(),
                user_id=user_object["_id", UUID],
                drunk_water=water_of(record_object["drunk_water", int]),
                recording_time=time_of(
                    record_object["recording_time", datetime]
                ),
                is_cancelled=record_object["is_cancelled", bool],
            )
            records.add(record)

        return User(
            id=user_object["_id", UUID],
            events=list(),
            target=target_of(user_object["target", int]),
            glass=glass_of(user_object["glass", int]),
            weight=maybe_weight_of(user_object["weight", int]),
            days=days,
            records=records,
        )

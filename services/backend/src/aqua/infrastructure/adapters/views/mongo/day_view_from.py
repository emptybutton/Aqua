from datetime import date, datetime
from typing import Iterable, cast
from uuid import UUID

from aqua.application.ports.views import DayViewFrom
from aqua.domain.framework.iterable import one_from
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operators import (
    cond_about,
    in_date_range,
)
from aqua.infrastructure.periphery.serializing.from_document.to_native import (
    native_datetime_of,
)
from aqua.infrastructure.periphery.serializing.from_native.to_document import (
    document_date_of,
)
from aqua.infrastructure.periphery.serializing.from_table_attribute.to_view import (  # noqa: E501
    old_maybe_result_view_of,
    old_result_view_of,
)
from aqua.infrastructure.periphery.validation.objects import (
    StrictValidationObject,
)
from aqua.infrastructure.periphery.views.db.day_view import (
    DBDayView,
    DBDayViewRecordData,
    empty_db_day_view_with,
)


class DBDayViewFromMongoUsers(DayViewFrom[MongoUsers, DBDayView]):
    async def __call__(
        self, mongo_users: MongoUsers, *, user_id: UUID, date_: date
    ) -> DBDayView:
        document_date = document_date_of(date_)
        pipeline = [
            {"$match": {"_id": user_id, "days.date": document_date}},
            {"$project": {
                "days": {"$filter": {
                    "input": "$days",
                    "cond": {"$eq": ["$$this.date", document_date]}
                }},
                "records": {"$filter": {
                    "input": "$records",
                    "cond": {
                        "$and": [
                            {"$eq": ["$$this.is_cancelled", False]},
                            *cond_about(
                                in_date_range(document_date),
                                field="$$this.recording_time"
                            )
                        ]
                    }
                }}
            }}
        ]
        documents = await mongo_users.session.client.db.users.aggregate(
            pipeline, session=mongo_users.session
        )
        document = one_from(await documents.to_list())

        if document is None:
            return empty_db_day_view_with(user_id=user_id, date_=date_)

        day_object = StrictValidationObject(cast(Document, document["days"][0]))

        return DBDayView(
            user_id=user_id,
            date_=date_,
            target_water_balance_milliliters=day_object["target", int],
            water_balance_milliliters=day_object["water_balance", int],
            result_code=old_result_view_of(day_object["result", int]),
            correct_result_code=old_result_view_of(
                day_object["correct_result", int]
            ),
            pinned_result_code=old_maybe_result_view_of(
                day_object.n["pinned_result", int]
            ),
            records=tuple(_records_from(document["records"])),
        )


def _records_from(documents: list[Document]) -> Iterable[DBDayViewRecordData]:
    for record_object in map(StrictValidationObject, documents):
        yield DBDayViewRecordData(
            record_id=record_object["_id", UUID],
            drunk_water_milliliters=record_object["drunk_water", int],
            recording_time=native_datetime_of(
                record_object["recording_time", datetime]
            ),
        )

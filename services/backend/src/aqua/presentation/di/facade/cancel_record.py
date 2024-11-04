from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal
from uuid import UUID

from result import Err, Ok
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.cancel_record import cancel_record
from aqua.application.ports.loggers import Logger
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapperTo,
)
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.adapters.transactions.mongo.transaction import (
    MongoTransactionForMongoUsers,
)
from aqua.infrastructure.adapters.views.in_memory.cancellation_view_of import (
    InMemoryCancellationViewOf,
)
from aqua.infrastructure.periphery.serializing.from_model.to_view import (
    old_result_view_of,
    target_view_of,
    time_view_of,
    water_balance_view_of,
    water_view_of,
)
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class RecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    day_records: tuple[RecordData, ...]
    cancelled_record: RecordData


async def perform(
    user_id: UUID,
    record_id: UUID,
    *,
    session: AsyncSession | None = None,  # noqa: ARG001
) -> Output | Literal["no_record"]:
    async with adapter_container() as container:
        view_result = await cancel_record(
            user_id,
            record_id,
            view_of=await container.get(InMemoryCancellationViewOf, "views"),
            users=await container.get(MongoUsers, "repos"),
            transaction_for=await container.get(
                MongoTransactionForMongoUsers, "transactions"
            ),
            logger=await container.get(Logger, "loggers"),
            user_mapper_to=await container.get(MongoUserMapperTo, "mappers"),
            record_mapper_to=await container.get(
                MongoRecordMapperTo, "mappers"
            ),
            day_mapper_to=await container.get(MongoDayMapperTo, "mappers"),
        )

    match view_result:
        case Err(_):
            return "no_record"
        case Ok(view):
            user = view.user
            day = view.output.day
            cancelled_record = view.output.cancelled_record
            records = view.records

    return Output(
        user_id=user.user_id,
        target_water_balance_milliliters=target_view_of(day.target),
        date_=day.date_,
        water_balance_milliliters=water_balance_view_of(day.water_balance),
        result_code=old_result_view_of(day.result),
        real_result_code=old_result_view_of(day.correct_result),
        is_result_pinned=day.is_result_pinned,
        day_records=tuple(map(_data_of, records)),
        cancelled_record=_data_of(cancelled_record),
    )


def _data_of(record: Record) -> RecordData:
    return RecordData(
        record_id=record.id,
        drunk_water_milliliters=water_view_of(record.drunk_water),
        recording_time=time_view_of(record.recording_time),
    )

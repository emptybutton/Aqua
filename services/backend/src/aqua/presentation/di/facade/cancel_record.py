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
from aqua.infrastructure.adapters.mappers.db.day_mapper import DBDayMapperTo
from aqua.infrastructure.adapters.mappers.db.record_mapper import (
    DBRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.db.user_mapper import DBUserMapperTo
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.transactions.db.transaction import (
    DBTransactionForDBUsers,
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
    session: AsyncSession,
) -> Output | Literal["no_record"]:
    request_container = adapter_container(
        context={AsyncSession | None: session}
    )
    async with request_container as container:
        view_result = await cancel_record(
            user_id,
            record_id,
            view_of=await container.get(
                InMemoryCancellationViewOf, "views"
            ),
            users=await container.get(DBUsers, "repos"),
            transaction_for=await container.get(
                DBTransactionForDBUsers, "transactions"
            ),
            logger=await container.get(Logger, "loggers"),
            user_mapper_to=await container.get(DBUserMapperTo, "mappers"),
            record_mapper_to=await container.get(
                DBRecordMapperTo, "mappers"
            ),
            day_mapper_to=await container.get(DBDayMapperTo, "mappers"),
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

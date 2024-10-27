from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from result import Err, Ok
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.write_water import (
    NoUserError as _NoUserApplicationError,
)
from aqua.application.cases.write_water import (
    write_water,
)
from aqua.application.ports.loggers import Logger
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.primitives.vos.water import NegativeWaterAmountError
from aqua.infrastructure.adapters.mappers.db.day_mapper import DBDayMapperTo
from aqua.infrastructure.adapters.mappers.db.record_mapper import (
    DBRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.db.user_mapper import DBUserMapperTo
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.transactions.db.transaction import (
    DBTransactionForDBUsers,
)
from aqua.infrastructure.adapters.views.in_memory.writing_view_of import (
    InMemoryWritingViewOf,
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
    previous_records: tuple[RecordData, ...]
    new_record: RecordData


class Error(Exception): ...


class IncorrectWaterAmountError(Error): ...


class NoUserError(Error): ...


async def perform(
    user_id: UUID, milliliters: int | None, *, session: AsyncSession
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        view_result = await write_water(
            user_id,
            milliliters,
            view_of=await container.get(InMemoryWritingViewOf, "views"),
            users=await container.get(DBUsers, "repos"),
            transaction_for=await container.get(
                DBTransactionForDBUsers, "transactions"
            ),
            logger=await container.get(Logger, "loggers"),
            user_mapper_to=await container.get(DBUserMapperTo, "mappers"),
            record_mapper_to=await container.get(DBRecordMapperTo, "mappers"),
            day_mapper_to=await container.get(DBDayMapperTo, "mappers"),
        )

    match view_result:
        case Err(_NoUserApplicationError()):
            raise NoUserError
        case Err(NegativeWaterAmountError()):
            raise IncorrectWaterAmountError
        case Ok(view):
            user = view.user
            day = view.day
            new_record = view.new_record
            previous_records = view.previous_records

    return Output(
        user_id=user.id,
        date_=day.date_,
        target_water_balance_milliliters=target_view_of(day.target),
        water_balance_milliliters=water_balance_view_of(day.water_balance),
        result_code=old_result_view_of(day.result),
        real_result_code=old_result_view_of(day.correct_result),
        is_result_pinned=day.is_result_pinned,
        new_record=_record_data_of(new_record),
        previous_records=tuple(map(_record_data_of, previous_records)),
    )


def _record_data_of(record: Record) -> RecordData:
    return RecordData(
        record_id=record.id,
        drunk_water_milliliters=water_view_of(record.drunk_water),
        recording_time=time_view_of(record.recording_time),
    )

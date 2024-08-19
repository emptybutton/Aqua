from dataclasses import dataclass
from datetime import datetime, date
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import write_water
from aqua.domain import value_objects as vos, entities
from aqua.presentation.di.containers import adapter_container
from aqua.infrastructure.adapters import repos, loggers
from shared.infrastructure.adapters.transactions import DBTransactionFactory


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


IncorrectWaterAmountError: TypeAlias = vos.Water.IncorrectAmountError

NoUserError: TypeAlias = write_water.NoUserError

Error: TypeAlias = write_water.Error | IncorrectWaterAmountError


async def perform(
    user_id: UUID,
    milliliters: int | None,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await write_water.perform(
            user_id,
            milliliters,
            users=await container.get(repos.DBUsers, "repos"),
            records=await container.get(repos.DBRecords, "repos"),
            days=await container.get(repos.DBDays, "repos"),
            record_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            day_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            user_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            logger=await container.get(loggers.StructlogDevLogger, "loggers"),
        )

    return Output(
        user_id=result.new_record.user_id,
        date_=result.day.date_,
        target_water_balance_milliliters=result.day.target.water.milliliters,
        water_balance_milliliters=result.day.water_balance.water.milliliters,
        result_code=result.day.result.value,
        real_result_code=result.day.correct_result.value,
        is_result_pinned=result.day.is_result_pinned,
        new_record=_record_data_of(result.new_record),
        previous_records=tuple(map(_record_data_of, result.previous_records)),
    )


def _record_data_of(record: entities.Record) -> RecordData:
    return RecordData(
        record_id=record.id,
        drunk_water_milliliters=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )

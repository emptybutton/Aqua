from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application import ports
from aqua.application.cases import cancel_record
from aqua.domain import entities
from aqua.infrastructure.adapters import repos
from aqua.presentation.di.containers import adapter_container
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
    day_records: tuple[RecordData, ...]
    cancelled_record: RecordData


async def perform(
    user_id: UUID,
    record_id: UUID,
    *,
    session: AsyncSession,
) -> Output | Literal["no_record"]:
    async with adapter_container(context={AsyncSession: session}) as container:
        try:
            result = await cancel_record.perform(
                user_id,
                record_id,
                days=await container.get(repos.DBDays, "repos"),
                records=await container.get(repos.DBRecords, "repos"),
                logger=await container.get(ports.loggers.Logger, "loggers"),
                day_transaction_for=await container.get(
                    DBTransactionFactory, "transactions"
                ),
                record_transaction_for=await container.get(
                    DBTransactionFactory, "transactions"
                ),
            )
        except (cancel_record.NoRecordError, cancel_record.NoDayError):
            return "no_record"

    cancelled_record = _record_data_of(result.cancelled_record)
    day_records = tuple(map(_record_data_of, result.day_records))
    target = result.day.target.water.milliliters

    return Output(
        user_id=result.day.user_id,
        target_water_balance_milliliters=target,
        date_=result.day.date_,
        water_balance_milliliters=result.day.water_balance.water.milliliters,
        result_code=result.day.result.value,
        real_result_code=result.day.correct_result.value,
        is_result_pinned=result.day.is_result_pinned,
        day_records=day_records,
        cancelled_record=cancelled_record,
    )


def _record_data_of(record: entities.Record) -> RecordData:
    return RecordData(
        record_id=record.id,
        drunk_water_milliliters=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )

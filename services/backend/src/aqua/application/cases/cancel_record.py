from dataclasses import dataclass
from typing import TypeVar
from uuid import UUID

from aqua.application.ports import loggers, repos
from aqua.domain import entities
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    day: entities.Day
    day_records: tuple[entities.Record, ...]
    cancelled_record: entities.Record


class Error(Exception): ...


class NoDayError(Error): ...


class NoRecordError(Error): ...


_DaysT = TypeVar("_DaysT", bound=repos.Days)

_RecordsT = TypeVar("_RecordsT", bound=repos.Records)


async def perform(
    user_id: UUID,
    record_id: UUID,
    *,
    days: _DaysT,
    records: _RecordsT,
    day_transaction_for: TransactionFactory[_DaysT],
    record_transaction_for: TransactionFactory[_RecordsT],
    logger: loggers.Logger,
) -> Output:
    async with day_transaction_for(days), record_transaction_for(records):
        record = await records.find_not_accidental_with_id(record_id)

        if not record:
            raise NoRecordError

        day = await days.find_from(
            record.recording_time.date(), user_id=user_id
        )

        if not day:
            await logger.log_record_without_day(record)
            raise NoDayError

        entities.cancel_record(record=record, day=day)
        await logger.log_record_cancellation(record=record, day=day)

        await records.update(record)
        await days.update(day)

        found_day_records = await records.find_not_accidental_from(
            record.recording_time.date(),
            user_id=user_id,
        )

        return Output(
            cancelled_record=record,
            day=day,
            day_records=found_day_records,
        )

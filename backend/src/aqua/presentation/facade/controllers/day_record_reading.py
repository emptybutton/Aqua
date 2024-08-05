from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID
from typing import TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import day_record_reading
from aqua.domain import entities
from aqua.infrastructure.adapters import repos


@dataclass(frozen=True, kw_only=True)
class RecordDTO:
    id: UUID
    drunk_water: int
    recording_time: datetime


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    records: tuple[RecordDTO, ...]


BaseError: TypeAlias = day_record_reading.BaseError

NoUserError: TypeAlias = day_record_reading.NoUserError


def _dto_of(record: entities.Record) -> RecordDTO:
    return RecordDTO(
        id=record.id,
        drunk_water=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )


async def read_day_records(
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession,
) -> OutputDTO:
    records = await day_record_reading.read_day_records(
        user_id,
        date_,
        users=repos.Users(session),
        records=repos.Records(session),
    )

    return OutputDTO(records=tuple(map(_dto_of, records)))

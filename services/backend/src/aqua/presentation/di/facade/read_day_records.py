from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID
from typing import TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import read_day_records
from aqua.domain import entities
from aqua.infrastructure import adapters
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class RecordData:
    id: UUID
    drunk_water: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True)
class Output:
    records: tuple[RecordData, ...]


Error: TypeAlias = read_day_records.Error

NoUserError: TypeAlias = read_day_records.NoUserError


async def perform(
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        records = await read_day_records.perform(
            user_id,
            date_,
            users=await container.get(adapters.repos.DBUsers),
            records=await container.get(adapters.repos.DBRecords),
        )

    return Output(records=tuple(map(_data_of, records)))


def _data_of(record: entities.Record) -> RecordData:
    return RecordData(
        id=record.id,
        drunk_water=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )

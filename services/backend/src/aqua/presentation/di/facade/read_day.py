from dataclasses import dataclass
from datetime import date, datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import read_day
from aqua.infrastructure.adapters import repos, loggers
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool

    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    records: tuple[RecordData, ...]


Error: TypeAlias = read_day.Error

NoUserError: TypeAlias = read_day.NoUserError


async def perform(
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await read_day.perform(
            user_id,
            date_,
            users=await container.get(repos.DBUsers, "repos"),
            days=await container.get(repos.DBDays, "repos"),
            records=await container.get(repos.DBRecords, "repos"),
            logger=await container.get(loggers.LoguruLogger, "loggers"),
        )

    records = tuple(
        Output.RecordData(
            record_id=record.id,
            drunk_water_milliliters=record.drunk_water.milliliters,
            recording_time=record.recording_time,
        )
        for record in result.records
    )

    return Output(
        user_id=result.day.user_id,
        target_water_balance_milliliters=result.day.target.water.milliliters,
        date_=result.day.date_,
        water_balance_milliliters=result.day.water_balance.water.milliliters,
        result_code=result.day.result.value,
        real_result_code=result.day.correct_result.value,
        is_result_pinned=result.day.is_result_pinned,
        records=records,
    )

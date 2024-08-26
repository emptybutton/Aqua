from dataclasses import dataclass
from datetime import date, datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application import ports
from aqua.application.cases import read_user
from aqua.infrastructure.adapters import repos
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: int | None
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


Error: TypeAlias = read_user.Error

NoUserError: TypeAlias = read_user.NoUserError


async def perform(user_id: UUID, *, session: AsyncSession) -> Output | None:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await read_user.perform(
            user_id,
            users=await container.get(repos.DBUsers, "repos"),
            days=await container.get(repos.DBDays, "repos"),
            records=await container.get(repos.DBRecords, "repos"),
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    records = tuple(
        Output.RecordData(
            record_id=record.id,
            drunk_water_milliliters=record.drunk_water.milliliters,
            recording_time=record.recording_time,
        )
        for record in result.records
    )

    weight_kilograms = (
        None if result.user.weight is None else result.user.weight.kilograms
    )

    return Output(
        user_id=result.user.id,
        glass_milliliters=result.user.glass.capacity.milliliters,
        weight_kilograms=weight_kilograms,
        target_water_balance_milliliters=result.day.target.water.milliliters,
        date_=result.day.date_,
        water_balance_milliliters=result.day.water_balance.water.milliliters,
        result_code=result.day.result.value,
        real_result_code=result.day.correct_result.value,
        is_result_pinned=result.day.is_result_pinned,
        records=records,
    )

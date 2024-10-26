from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.view_day import view_day
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.views.db.day_view_from import (
    DBDayViewFrom,
)
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


class Error(Exception): ...


class NoUserError(Error): ...


async def perform(
    user_id: UUID, date_: date, *, session: AsyncSession
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        view = await view_day(
            user_id,
            date_,
            view_from=await container.get(DBDayViewFrom, "views"),
            users=await container.get(DBUsers, "repos"),
        )

    records = tuple(
        Output.RecordData(
            record_id=record_view.id,
            drunk_water_milliliters=record_view.drunk_water_milliliters,
            recording_time=record_view.recording_time,
        )
        for record_view in view.records
    )

    return Output(
        user_id=view.user_id,
        date_=view.date_,
        target_water_balance_milliliters=view.target_water_balance_milliliters,
        water_balance_milliliters=view.water_balance_milliliters,
        result_code=view.result_code,
        real_result_code=view.correct_result_code,
        is_result_pinned=view.pinned_result_code is not None,
        records=records,
    )

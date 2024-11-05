from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.view_day import view_day
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.adapters.views.mongo.day_view_from import (
    DBDayViewFromMongoUsers,
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
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession | None = None,  # noqa: ARG001
) -> Output:
    async with adapter_container() as container:
        view = await view_day(
            user_id,
            date_,
            view_from=await container.get(DBDayViewFromMongoUsers, "views"),
            users=await container.get(MongoUsers, "repos"),
        )

    records = tuple(
        Output.RecordData(
            record_id=record_view.record_id,
            drunk_water_milliliters=record_view.drunk_water_milliliters,
            recording_time=record_view.recording_time,
        )
        for record_view in view.records
    )

    target_water_balance_milliliters = (
        _output_target_water_balance_milliliters_of(
            view.target_water_balance_milliliters
        )
    )

    return Output(
        user_id=view.user_id,
        date_=view.date_,
        target_water_balance_milliliters=target_water_balance_milliliters,
        water_balance_milliliters=view.water_balance_milliliters,
        result_code=view.result_code,
        real_result_code=view.correct_result_code,
        is_result_pinned=view.pinned_result_code is not None,
        records=records,
    )


def _output_target_water_balance_milliliters_of(
    view_target_water_balance_milliliters: int | None
) -> int:
    if view_target_water_balance_milliliters is None:
        return 0

    return view_target_water_balance_milliliters

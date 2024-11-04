from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.view_user import view_user
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.adapters.views.mongo.user_view_from import (
    DBUserViewFromMongoUsers,
)
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True, slots=True)
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

    @dataclass(kw_only=True, frozen=True, slots=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    records: tuple[RecordData, ...]


class Error(Exception): ...


class NoUserError(Error): ...


async def perform(
    user_id: UUID, *, session: AsyncSession | None = None
) -> Output | None:  # noqa: ARG001
    async with adapter_container() as container:
        view = await view_user(
            user_id,
            view_from=await container.get(DBUserViewFromMongoUsers, "views"),
            users=await container.get(MongoUsers, "repos"),
        )

    if view is None:
        return None

    records = tuple(
        Output.RecordData(
            record_id=record.id,
            drunk_water_milliliters=record.drunk_water.milliliters,
            recording_time=record.recording_time,
        )
        for record in view.records
    )

    return Output(
        user_id=view.user_id,
        glass_milliliters=view.glass_milliliters,
        weight_kilograms=view.weight_kilograms,
        target_water_balance_milliliters=view.target_water_balance_milliliters,
        date_=view.date_,
        water_balance_milliliters=view.water_balance_milliliters,
        result_code=view.result_code,
        real_result_code=view.correct_result_code,
        is_result_pinned=view.pinned_result_code is not None,
        records=records,
    )

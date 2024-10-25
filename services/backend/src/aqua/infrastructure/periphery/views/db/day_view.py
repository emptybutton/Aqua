from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from aqua.domain.model.core.vos.target import Result
from aqua.infrastructure.periphery.serializing.from_model.to_view import (
    old_result_view_of,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class DBDayViewRecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True, slots=True)
class DBDayView:
    user_id: UUID
    date_: date
    target_water_balance_milliliters: int | None
    water_balance_milliliters: int
    result_code: int
    correct_result_code: int
    pinned_result_code: int | None
    records: tuple[DBDayViewRecordData, ...]


def empty_db_day_view_with(
    *,
    user_id: UUID,
    date_: date,
) -> DBDayView:
    return DBDayView(
        user_id=user_id,
        date_=date_,
        target_water_balance_milliliters=None,
        water_balance_milliliters=0,
        result_code=old_result_view_of(Result.not_enough_water),
        correct_result_code=old_result_view_of(Result.not_enough_water),
        pinned_result_code=None,
        records=tuple(),
    )

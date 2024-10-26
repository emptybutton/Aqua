from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass(kw_only=True, frozen=True, slots=True)
class DBUserViewRecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True, slots=True)
class DBUserViewData:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: int | None
    date_: date
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    correct_result_code: int
    pinned_result_code: int | None
    records: tuple[DBUserViewRecordData, ...]


type DBUserView = DBUserViewData | None

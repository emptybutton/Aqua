from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class RegisteredUserView(BaseModel):
    user_id: UUID
    username: str
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


class RecordView(BaseModel):
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


class NewRecordView(BaseModel):
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool


class UserView(BaseModel):
    user_id: UUID
    username: str | None
    glass_milliliters: int | None
    weight_kilograms: int | None
    target_water_balance_milliliters: int | None
    water_balance_milliliters: int | None
    date_: date | None
    result_code: int | None
    real_result_code: int | None
    is_result_pinned: bool | None
    records: tuple[RecordView, ...]


class DayView(BaseModel):
    user_id: UUID
    target_water_balance_milliliters: int | None
    water_balance_milliliters: int | None
    date_: date | None
    result_code: int | None
    real_result_code: int | None
    is_result_pinned: bool | None
    records: tuple[RecordView, ...]

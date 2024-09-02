from datetime import date, datetime
from typing import Literal
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
    class Data(BaseModel):
        target_water_balance_milliliters: int
        water_balance_milliliters: int
        result_code: int
        real_result_code: int
        is_result_pinned: bool
        date_: date
        previous_records: tuple[RecordView, ...]
        new_record: RecordView

    user_id: UUID
    data: Data | Literal["incorrect_water_amount"] | None


class UserView(BaseModel):
    class FirstPart(BaseModel):
        username: str

    class SecondPart(BaseModel):
        glass_milliliters: int
        weight_kilograms: int | None
        target_water_balance_milliliters: int
        date_: date
        water_balance_milliliters: int
        result_code: int
        real_result_code: int
        is_result_pinned: bool
        records: tuple[RecordView, ...]

    user_id: UUID
    first_part: FirstPart | None
    second_part: SecondPart | None


class DayView(BaseModel):
    class Data(BaseModel):
        target_water_balance_milliliters: int
        date_: date
        water_balance_milliliters: int
        result_code: int
        real_result_code: int
        is_result_pinned: bool
        records: tuple[RecordView, ...]

    user_id: UUID
    data: Data | None


class AuthorizedUserView(BaseModel):
    user_id: UUID
    username: str

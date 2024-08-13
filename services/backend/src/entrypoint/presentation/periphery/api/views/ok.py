from datetime import datetime
from uuid import UUID
from typing import ClassVar

from fastapi import status

from entrypoint.presentation.periphery.api.views.common import View


class AccessView(View):
    status_code: ClassVar[int] = status.HTTP_200_OK

    jwt: str


class NewUserView(View):
    status_code: ClassVar[int] = status.HTTP_201_CREATED

    jwt: str
    water_balance_milliliters: int
    glass_milliliters: int


class UserView(View):
    status_code: ClassVar[int] = status.HTTP_200_OK

    user_id: UUID
    username: str
    glass_milliliters: int
    target_water_balance_milliliters: int
    weight_kilograms: int | None


class RecordView(View):
    status_code: ClassVar[int] = status.HTTP_200_OK

    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


class NewRecordView(RecordView):
    status_code: ClassVar[int] = status.HTTP_201_CREATED


class DayRecordsView(View):
    status_code: ClassVar[int] = status.HTTP_200_OK

    records: tuple[RecordView, ...]

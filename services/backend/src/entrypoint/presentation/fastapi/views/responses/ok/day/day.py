from datetime import date
from uuid import UUID

from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)
from entrypoint.presentation.fastapi.views.responses.common.record import (
    RecordSchema,
)


class DaySchema(BaseModel):
    user_id: UUID
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    records: tuple[RecordSchema, ...]


day_response_model = ResponseModel(DaySchema, status.HTTP_200_OK)

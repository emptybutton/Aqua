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


class NewRecordSchema(BaseModel):
    user_id: UUID
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    date_: date
    previous_records: tuple[RecordSchema, ...]
    new_record: RecordSchema


new_record_response_model = ResponseModel(
    NewRecordSchema, status.HTTP_201_CREATED
)

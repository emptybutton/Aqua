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


class UserSchemaFirstPart(BaseModel):
    username: str


class UserSchemaSecondPart(BaseModel):
    glass_milliliters: int
    weight_kilograms: int | None
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    records: tuple[RecordSchema, ...]


class UserSchema(BaseModel):
    user_id: UUID
    first_part: UserSchemaFirstPart | None
    second_part: UserSchemaSecondPart | None


user_response_model = ResponseModel(UserSchema, status.HTTP_200_OK)

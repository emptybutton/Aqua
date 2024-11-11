from uuid import UUID

from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class RegisteredUserSchema(BaseModel):
    user_id: UUID
    username: str
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


registered_user_response_model = ResponseModel(
    RegisteredUserSchema, status.HTTP_201_CREATED
)

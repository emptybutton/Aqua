from uuid import UUID

from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class RenamedUserSchema(BaseModel):
    user_id: UUID
    new_username: str
    previous_username: str


renamed_user_response_model = ResponseModel(
    RenamedUserSchema, status.HTTP_200_OK
)

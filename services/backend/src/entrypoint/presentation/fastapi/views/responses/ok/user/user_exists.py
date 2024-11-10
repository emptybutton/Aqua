from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class UserExistsSchema(BaseModel):
    exists: bool


user_exists_response_model = ResponseModel(UserExistsSchema, status.HTTP_200_OK)

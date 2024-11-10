from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class InvalidPasswordSchema(BaseModel):
    detail: Detail = [DetailPartSchema(type="InvalidPasswordError", msg="")]


invalid_password_response_model = ResponseModel(
    InvalidPasswordSchema, status.HTTP_401_UNAUTHORIZED
)

from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class EmptyUsernameSchema(BaseModel):
    detail: Detail = [DetailPartSchema(type="EmptyUsernameError", msg="")]


empty_username_response_model = ResponseModel(
    EmptyUsernameSchema, status.HTTP_400_BAD_REQUEST
)

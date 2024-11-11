from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class NotAuthenticatedSchema(BaseModel):
    detail: Detail = [DetailPartSchema(type="NotAuthenticatedError", msg="")]


not_authenticated_response_model = ResponseModel(
    NotAuthenticatedSchema, status.HTTP_401_UNAUTHORIZED
)

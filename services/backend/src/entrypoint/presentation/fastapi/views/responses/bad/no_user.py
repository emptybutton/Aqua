from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class NoUserSchema(BaseModel):
    detail: Detail = [DetailPartSchema(type="NoUserError", msg="")]


no_user_response_model = ResponseModel(NoUserSchema, status.HTTP_404_NOT_FOUND)

from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class TakenUsernameSchema(BaseModel):
    detail: Detail = [
        DetailPartSchema(
            type="UsernameTakenError", msg="another user already owns this name"
        )
    ]


taken_username_response_model = ResponseModel(
    TakenUsernameSchema, status.HTTP_409_CONFLICT
)

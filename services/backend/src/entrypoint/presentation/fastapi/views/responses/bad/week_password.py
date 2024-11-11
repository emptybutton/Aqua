from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class WeekPasswordSchema(BaseModel):
    detail: Detail = [DetailPartSchema(
        type="WeekPasswordError",
        msg=(
            "password must not contain only numbers or only letters, "
            "but must contain both upper and lower case letters and be 8 "
            "or more characters long"
        ),
    )]


week_password_response_model = ResponseModel(
    WeekPasswordSchema, status.HTTP_400_BAD_REQUEST
)

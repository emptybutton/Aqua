from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class InvalidWaterSchema(BaseModel):
    detail: Detail = [DetailPartSchema(
        type="InvalidWaterAmountError",
        msg="the amount of water should be >= 0",
    )]


invalid_water_amount_response_model = ResponseModel(
    InvalidWaterSchema, status.HTTP_400_BAD_REQUEST
)

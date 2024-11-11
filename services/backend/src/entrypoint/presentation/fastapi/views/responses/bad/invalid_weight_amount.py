from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class InvalidWeightSchema(BaseModel):
    detail: Detail = [DetailPartSchema(
        type="InvalidWeightAmountError",
        msg="weight kilograms should be >= 0",
    )]


invalid_weight_amount_response_model = ResponseModel(
    InvalidWeightSchema, status.HTTP_400_BAD_REQUEST
)

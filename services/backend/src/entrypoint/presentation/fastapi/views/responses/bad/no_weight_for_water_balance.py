from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class NoWeightForWaterBalanceSchema(BaseModel):
    detail: Detail = [
        DetailPartSchema(
            type="NoWeightForWaterBalanceError",
            msg="weight is required if water balance is not specified",
        )
    ]


no_weight_for_water_balance_response_model = ResponseModel(
    NoWeightForWaterBalanceSchema, status.HTTP_400_BAD_REQUEST
)

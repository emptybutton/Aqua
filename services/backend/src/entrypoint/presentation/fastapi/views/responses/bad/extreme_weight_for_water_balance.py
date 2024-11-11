from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class ExtremeWeightForWaterBalanceSchema(BaseModel):
    detail: Detail = [DetailPartSchema(
        type="ExtremeWeightForWaterBalanceError",
        msg=(
            "weight must be between 30 and 150 kg inclusive to"
            " calculate water balance"
        ),
    )]


extreme_weight_for_water_balance_response_model = ResponseModel(
    ExtremeWeightForWaterBalanceSchema, status.HTTP_400_BAD_REQUEST
)

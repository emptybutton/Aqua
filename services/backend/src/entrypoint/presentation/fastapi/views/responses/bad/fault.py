from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class FaultSchema(BaseModel):
    detail: Detail = [
        DetailPartSchema(type="InternalError", msg="service unavailable")
    ]


fault_response_model = ResponseModel(
    FaultSchema, status.HTTP_500_INTERNAL_SERVER_ERROR
)

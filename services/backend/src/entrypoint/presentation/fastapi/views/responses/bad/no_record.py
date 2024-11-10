from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class NoRecordSchema(BaseModel):
    detail: Detail = [DetailPartSchema(type="NoRecordError", msg="")]


no_record_response_model = ResponseModel(
    NoRecordSchema, status.HTTP_404_NOT_FOUND
)

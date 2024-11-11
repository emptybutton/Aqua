from fastapi import status
from pydantic import BaseModel

from entrypoint.presentation.fastapi.views.responses.common.detail import (
    Detail,
    DetailPartSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


class InvalidSessionIDHEXSchema(BaseModel):
    detail: Detail = [DetailPartSchema(
        type="InvalidSessionIDHEXError",
        msg="session id hex must be a 32-character hexadecimal string",
    )]


invalid_session_id_hex_response_model = ResponseModel(
    InvalidSessionIDHEXSchema, status.HTTP_400_BAD_REQUEST
)

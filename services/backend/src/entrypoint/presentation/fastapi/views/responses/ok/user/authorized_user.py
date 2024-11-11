from fastapi import status

from entrypoint.presentation.fastapi.views.responses.common.identified_user import (  # noqa: E501
    IdentifiedUserSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    ResponseModel,
)


authorized_user_response_model = ResponseModel(
    IdentifiedUserSchema, status.HTTP_200_OK
)

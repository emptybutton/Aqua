from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.authorize_user import authorize_user as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import (
    InvalidHexError,
    optional_valid_id_of,
)
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.cookies import SessionCookie
from entrypoint.presentation.fastapi.views.responses.bad.fault import (
    fault_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_password import (  # noqa: E501
    invalid_password_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_session_id_hex import (  # noqa: E501
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.no_user import (
    no_user_response_model,
)
from entrypoint.presentation.fastapi.views.responses.common.identified_user import (  # noqa: E501
    IdentifiedUserSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.responses.ok.user.authorized_user import (  # noqa: E501
    authorized_user_response_model,
)


class AuthorizeUserRequestModel(BaseModel):
    username: str
    password: str


@router.post(
    "/user/authorize",
    tags=[Tag.access_endpoints],
    status_code=authorized_user_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        no_user_response_model,
        invalid_password_response_model,
        invalid_session_id_hex_response_model,
        authorized_user_response_model,
    ),
)
async def authorize_user(
    request_model: AuthorizeUserRequestModel,
    session_id_hex: cookies.optional_session_id_cookie = None,
) -> Response:
    session_id = optional_valid_id_of(session_id_hex)

    if isinstance(session_id, InvalidHexError):
        return invalid_session_id_hex_response_model.to_response()

    result = await service(
        session_id, request_model.username, request_model.password
    )

    if result == "error":
        return fault_response_model.to_response()

    if result == "no_user":
        return no_user_response_model.to_response()

    if result == "incorrect_password":
        return invalid_password_response_model.to_response()

    body = IdentifiedUserSchema(
        user_id=result.user_id, username=result.username
    )
    response = authorized_user_response_model.to_response(body)

    session_cookie = SessionCookie(response)
    session_cookie.set(result.new_session_id)

    return response

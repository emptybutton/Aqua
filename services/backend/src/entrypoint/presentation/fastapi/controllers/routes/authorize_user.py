
from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.cancel_record import cancel_record as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import (
    optional_valid_id_of,
)
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.bad.fault import fault_response_model
from entrypoint.presentation.fastapi.views.bad.invalid_session_id_hex import (
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.bad.no_user import (
    no_user_response_model,
)
from entrypoint.presentation.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.cookies import SessionCookie
from entrypoint.presentation.fastapi.views.ok.user.authorized_user import (
    authorized_user_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_password import (  # noqa: E501
    invalid_password_response_model,
)
from entrypoint.presentation.fastapi.views.responses.common.identified_user import (  # noqa: E501
    IdentifiedUserSchema,
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
    session_id_hex: cookies.optional_session_id_cookie,
) -> Response:
    session_id = optional_valid_id_of(session_id_hex)

    if session_id == "invalid_hex":
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

from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.change_password import change_password as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import valid_id_of
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.responses.bad.fault import (
    fault_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_session_id_hex import (  # noqa: E501
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.not_authenticated import (  # noqa: E501
    not_authenticated_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.week_password import (
    week_password_response_model,
)
from entrypoint.presentation.fastapi.views.responses.common.identified_user import (  # noqa: E501
    IdentifiedUserSchema,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.responses.ok.user.user_with_changed_password import (  # noqa: E501
    user_with_changed_password_response_model,
)


class ChangePasswordRequestModel(BaseModel):
    new_password: str


@router.patch(
    "/user/password",
    tags=[Tag.current_user_endpoints],
    status_code=user_with_changed_password_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        week_password_response_model,
        not_authenticated_response_model,
        invalid_session_id_hex_response_model,
        user_with_changed_password_response_model,
    ),
)
async def change_password(
    request_model: ChangePasswordRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = valid_id_of(session_id_hex)

    if session_id is None:
        return invalid_session_id_hex_response_model.to_response()

    result = await service(session_id, request_model.new_password)

    if result == "error":
        return fault_response_model.to_response()

    if result == "not_authenticated":
        return not_authenticated_response_model.to_response()

    if result.auth_output == "error":
        return fault_response_model.to_response()

    if result.auth_output == "week_password":
        return week_password_response_model.to_response()

    body = IdentifiedUserSchema(
        user_id=result.auth_output.user_id,
        username=result.auth_output.username,
    )
    return user_with_changed_password_response_model.to_response(body)

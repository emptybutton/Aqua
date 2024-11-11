from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.rename_user import rename_user as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import valid_id_of
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.bad.empty_username import (
    empty_username_response_model,
)
from entrypoint.presentation.fastapi.views.bad.fault import fault_response_model
from entrypoint.presentation.fastapi.views.bad.invalid_session_id_hex import (
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.bad.not_authenticated import (
    not_authenticated_response_model,
)
from entrypoint.presentation.fastapi.views.bad.taken_username import (
    taken_username_response_model,
)
from entrypoint.presentation.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.ok.user.renamed_user import (
    RenamedUserSchema,
    renamed_user_response_model,
)


class RenameUserRequestModel(BaseModel):
    new_username: str


@router.patch(
    "/user/name",
    tags=[Tag.current_user_endpoints],
    status_code=renamed_user_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        invalid_session_id_hex_response_model,
        not_authenticated_response_model,
        taken_username_response_model,
        empty_username_response_model,
        renamed_user_response_model,
    ),
)
async def rename_user(
    request_model: RenameUserRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = valid_id_of(session_id_hex)

    if session_id is None:
        return invalid_session_id_hex_response_model.to_response()

    result = await service(session_id, request_model.new_username)

    if result == "error":
        return fault_response_model.to_response()

    if result == "not_authenticated":
        return not_authenticated_response_model.to_response()

    if result.auth_output == "error":
        return fault_response_model.to_response()

    if result.auth_output == "new_username_taken":
        return taken_username_response_model.to_response()

    if result.auth_output == "empty_new_username":
        return empty_username_response_model.to_response()

    body = RenamedUserSchema(
        user_id=result.auth_output.user_id,
        new_username=result.auth_output.new_username,
        previous_username=result.auth_output.previous_username,
    )

    return renamed_user_response_model.to_response(body)

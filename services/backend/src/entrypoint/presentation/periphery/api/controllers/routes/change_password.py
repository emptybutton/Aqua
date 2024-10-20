from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class ChangePasswordRequestModel(BaseModel):
    new_password: str


@router.patch(
    "/user/password",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.user_with_changed_password_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.user_with_changed_password_view,
    ),
)
async def change_password(
    request_model: ChangePasswordRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = id_of(session_id_hex)

    if session_id is None:
        return views.responses.bad.not_authenticated_view.to_response()

    result = await facade.change_password.perform(
        session_id,
        request_model.new_password,
    )

    if result == "error":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    username = None
    error: views.bodies.ok.UserWithChangedPasswordView.Error = None

    if isinstance(result.data, facade.change_password.OkData):
        username = result.data.username
    elif result.data == "error":
        error = "unexpected_error"
    elif result.data == "week_password":
        error = "week_password_error"

    body = views.bodies.ok.UserWithChangedPasswordView(
        user_id=result.user_id,
        username=username,
        error=error,
    )
    return views.responses.ok.user_with_changed_password_view.to_response(body)

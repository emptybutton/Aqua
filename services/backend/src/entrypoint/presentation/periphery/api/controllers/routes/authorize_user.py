from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class AuthorizeUserRequestModel(BaseModel):
    username: str
    password: str


@router.post(
    "/user/authorize",
    tags=[Tag.access_endpoints],
    status_code=views.responses.ok.authorized_user_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.no_user_view,
        views.responses.bad.incorrect_password_view,
        views.responses.ok.authorized_user_view,
    ),
)
async def authorize_user(request_model: AuthorizeUserRequestModel) -> Response:
    result = await facade.authorize_user.perform(
        request_model.username,
        request_model.password,
    )

    if result == "not_working":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "no_user":
        return views.responses.bad.no_user_view.to_response()

    if result == "incorrect_password":
        return views.responses.bad.incorrect_password_view.to_response()

    body = views.bodies.ok.AuthorizedUserView(
        user_id=result.user_id,
        username=result.username,
    )
    response = views.responses.ok.authorized_user_view.to_response(body)

    session_cookie = views.cookies.SessionCookie(response)
    session_cookie.set(result.session_id)

    return response

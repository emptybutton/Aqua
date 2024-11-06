from fastapi import Response

from entrypoint.presentation.di import services
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


@router.get(
    "/user/exists",
    tags=[Tag.other_users_endpoints],
    status_code=views.responses.ok.user_exists_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.ok.user_exists_view,
    ),
)
async def user_exists(username: str) -> Response:
    result = await services.user_exists.perform(username)

    if result == "error":
        return views.responses.bad.backend_is_not_working_view.to_response()

    body = views.bodies.ok.UserExistsView(exists=result)
    return views.responses.ok.user_exists_view.to_response(body)

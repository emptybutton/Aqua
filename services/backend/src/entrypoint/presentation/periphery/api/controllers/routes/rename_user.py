from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class RenameUserRequestModel(BaseModel):
    new_username: str


@router.patch(
    "/user/name",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.renamed_user_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.renamed_user_view,
    ),
)
async def rename_user(
    request_model: RenameUserRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = id_of(session_id_hex)

    if session_id is None:
        return views.responses.bad.not_authenticated_view.to_response()

    result = await facade.rename_user.perform(
        session_id,
        request_model.new_username,
    )

    if result == "error":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    data: views.bodies.ok.RenamedUserView.Data

    if result.other_data == "error":
        data = None
    elif not isinstance(result.other_data, facade.rename_user.OkOtherData):
        data = result.other_data
    else:
        data = views.bodies.ok.RenamedUserView.OkData(
            new_username=result.other_data.new_username,
            previous_username=result.other_data.previous_username,
        )

    body = views.bodies.ok.RenamedUserView(user_id=result.user_id, data=data)
    return views.responses.ok.renamed_user_view.to_response(body)

from fastapi import Response

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


@router.get(
    "/user",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.user_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.user_view,
    ),
)
async def read_user(session_id_hex: cookies.session_id_cookie) -> Response:
    session_id = id_of(session_id_hex)

    if session_id is None:
        return views.responses.bad.not_authenticated_view.to_response()

    result = await facade.read_user.perform(session_id)

    if result == "not_working":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    if result.first_part is None:
        first_part = None
    else:
        first_part = views.bodies.ok.UserView.FirstPart(
            username=result.first_part.username,
        )

    if result.second_part is None:
        second_part = None
    else:
        records = tuple(
            views.bodies.ok.RecordView(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.second_part.records
        )
        target = result.second_part.target_water_balance_milliliters
        second_part = views.bodies.ok.UserView.SecondPart(
            glass_milliliters=result.second_part.glass_milliliters,
            weight_kilograms=result.second_part.weight_kilograms,
            target_water_balance_milliliters=target,
            date_=result.second_part.date_,
            water_balance_milliliters=result.second_part.water_balance_milliliters,
            result_code=result.second_part.result_code,
            real_result_code=result.second_part.real_result_code,
            is_result_pinned=result.second_part.is_result_pinned,
            records=records,
        )

    body = views.bodies.ok.UserView(
        user_id=result.user_id,
        first_part=first_part,
        second_part=second_part,
    )
    return views.responses.ok.user_view.to_response(body)
